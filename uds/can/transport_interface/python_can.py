"""Implementation of UDS Transport Interface for CAN bus using python-can as bus manager."""

__all__ = ["PythonCanTransportInterface"]

from asyncio import AbstractEventLoop, get_running_loop
from asyncio import timeout as async_timeout
from asyncio.exceptions import TimeoutError as AsyncioTimeoutError
from datetime import datetime
from functools import cached_property
from time import perf_counter
from typing import Any
from warnings import warn

from can import AsyncBufferedReader, BufferedReader, BusABC
from can import Message as PythonCanFrame
from can import Notifier
from can.interfaces import BACKENDS
from uds.addressing import AddressingType, TransmissionDirection
from uds.utilities import TimeMillisecondsAlias, validate_timeout

from ..addressing import AbstractCanAddressingInformation
from ..frame import CanDlcHandler, CanIdHandler, CanVersion
from ..packet import CanPacket, CanPacketRecord, CanPacketType
from .common import AbstractCanTransportInterface


class PythonCanTransportInterface(AbstractCanTransportInterface):
    """
    Transport Interface for managing UDS on CAN with python-can package as bus handler.

    .. note:: Documentation for python-can package: https://python-can.readthedocs.io/
    """

    _MAX_TX_WAIT: float = 0.005  # s
    """Maximal time to wait for CAN frames transmission."""

    _MAX_LISTENER_TIMEOUT: float = 4280.  # s
    """Maximal timeout value accepted by python-can listeners."""
    _MIN_NOTIFIER_TIMEOUT: float = 0.001  # s
    """Minimal timeout for notifiers that does not cause malfunctioning of listeners."""

    _INTERFACES_USING_WALL_TIME_TIMESTAMPS = frozenset({"vector", "kvaser", "etas", "ixxat", "nican", "pcan",
                                                        "socketcan", "udp_multicast", "iscan", "slcan", "robotell",
                                                        "neousys", "virtual", "seeedstudio", "nixnet"})

    def __init__(self,
                 network_manager: BusABC,
                 addressing_information: AbstractCanAddressingInformation,
                 notifier: Notifier | None = None,
                 async_notifier: Notifier | None = None,
                 **configuration_params: Any) -> None:
        """
        Create Transport Interface that uses python-can package to control CAN bus.

        :param network_manager: Python-can bus object for handling CAN network.
        :param addressing_information: Addressing Information configuration of a simulated node that is taking part in
            DoCAN communication.
        :param notifier: Python-can notifier object for reporting received and sent CAN Frames to listeners.
            Leave None to create new notifier when needed.

            .. warning:: Only one notifier object shall be active at any time.

        :param async_notifier: Python-can notifier object for reporting received and sent CAN Frames to async listeners.
            Leave None to create new notifier when needed.

            .. warning:: Only one notifier object shall be active at any time.

        :param configuration_params: Additional configuration parameters.

            - :parameter n_as_timeout: Timeout value for :ref:`N_As <knowledge-base-can-n-as>` time parameter.
            - :parameter n_ar_timeout: Timeout value for :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter.
            - :parameter n_bs_timeout: Timeout value for :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter.
            - :parameter n_br: Value of :ref:`N_Br <knowledge-base-can-n-br>` time parameter to use in communication.
            - :parameter n_cs: Value of :ref:`N_Cs <knowledge-base-can-n-cs>` time parameter to use in communication.
            - :parameter n_cr_timeout: Timeout value for :ref:`N_Cr <knowledge-base-can-n-cr>` time parameter.
            - :parameter dlc: Base CAN DLC value to use for CAN packets.
            - :parameter min_dlc: Minimal CAN DLC to use for CAN Packets during Data Optimization.
            - :parameter use_data_optimization: Information whether to use
                :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>`.
            - :parameter filler_byte: Filler byte value to use for
                :ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>`.
            - :parameter flow_control_parameters_generator: Generator with Flow Control parameters to use.
            - :parameter can_version: Version of CAN protocol to be used for packets sending.
            - :parameter bitrate_switch: Whether bitrate switch (BRS) shall be set in sent packets.
        """
        super().__init__(network_manager=network_manager,
                         addressing_information=addressing_information,
                         **configuration_params)
        self.notifier = notifier
        self.async_notifier = async_notifier
        self.__rx_frames_buffer = BufferedReader()
        self.__tx_frames_buffer = BufferedReader()
        self.__fc_frames_buffer = BufferedReader()
        self.__async_rx_frames_buffer = AsyncBufferedReader()
        self.__async_tx_frames_buffer = AsyncBufferedReader()
        self.__async_fc_frames_buffer = AsyncBufferedReader()

    def __del__(self) -> None:
        """Safely close all threads opened by this object."""
        super().__del__()
        self.__rx_frames_buffer.stop()
        self.__tx_frames_buffer.stop()
        self.__fc_frames_buffer.stop()
        self.__async_rx_frames_buffer.stop()
        self.__async_tx_frames_buffer.stop()
        self.__async_fc_frames_buffer.stop()

    @property
    def network_manager(self) -> BusABC:
        """Get python-can Bus object used by this Transport Interface for CAN communication."""
        return super().network_manager

    @network_manager.setter
    def network_manager(self, value: BusABC) -> None:
        """Set python-can Bus object to be used by this Transport Interface for CAN communication."""
        AbstractCanTransportInterface.network_manager.fset(self, value)
        self.__dict__.pop("backend", None)

    @cached_property
    def backend(self) -> str:
        """Get name of used backed by python-can for CAN communication."""
        network_manager_class_name = self.network_manager.__class__.__name__
        network_manager_module = self.network_manager.__class__.__module__
        for backend_name, (module_path, class_name) in BACKENDS.items():
            if network_manager_module.startswith(module_path) and network_manager_class_name == class_name:
                return backend_name
        raise RuntimeError(f"Python-can backed used as network_manager ({self.network_manager}) "
                           f"could not be recognised.")

    @property
    def notifier(self) -> Notifier | None:
        """Notifier used by python-can for reporting received and sent CAN Frames to listeners."""
        return self.__notifier

    @notifier.setter
    def notifier(self, value: Notifier | None) -> None:
        """
        Set notifier for reporting received and sent CAN Frames to listeners.

        :param value: Value of notifier to set.

        :raise TypeError: Value is not None neither Notifier type.
        """
        if value is None:
            self.__notifier = None
        elif isinstance(value, Notifier):
            self.__notifier = value
            if self.__notifier.timeout > self._MIN_NOTIFIER_TIMEOUT:
                self.__notifier.timeout = self._MIN_NOTIFIER_TIMEOUT
                warn(message=f"Notifier's timeout value was changed to {self._MIN_NOTIFIER_TIMEOUT}[s] "
                             f"due to performance reasons.",
                     category=UserWarning)
        else:
            raise TypeError(f"Provided value is not None neither Notifier type. Actual type: {type(value)}.")

    @property
    def async_notifier(self) -> Notifier | None:
        """Notifier used by python-can for reporting received and sent CAN Frames to async listeners."""
        return self.__async_notifier

    @async_notifier.setter
    def async_notifier(self, value: Notifier | None) -> None:
        """
        Set notifier for reporting received and sent CAN Frames to async listeners.

        :param value: Value of notifier to set.

        :raise TypeError: Value is not None neither Notifier type.
        """
        if value is None:
            self.__async_notifier = None
        elif isinstance(value, Notifier):
            self.__async_notifier = value
            if self.__async_notifier.timeout > self._MIN_NOTIFIER_TIMEOUT:
                self.__async_notifier.timeout = self._MIN_NOTIFIER_TIMEOUT
                warn(message=f"Asynchronous Notifier's timeout value was changed to {self._MIN_NOTIFIER_TIMEOUT}[s] "
                             f"due to performance reasons.",
                     category=UserWarning)
        else:
            raise TypeError(f"Provided value is not None neither Notifier type. Actual type: {type(value)}.")

    @property
    def is_sync_active(self) -> bool:
        """Get flag indicating whether CAN synchronous communication is active."""
        if self.notifier is None or self.notifier.stopped:
            return False
        if self.network_manager not in self.notifier._bus_list:
            return False
        if self.__rx_frames_buffer.is_stopped or self.__rx_frames_buffer not in self.notifier.listeners:
            return False
        if self.__tx_frames_buffer.is_stopped or self.__tx_frames_buffer not in self.notifier.listeners:
            return False
        if self.__fc_frames_buffer.is_stopped or self.__fc_frames_buffer not in self.notifier.listeners:
            return False
        return True

    @property
    def is_async_active(self) -> bool:
        """Get flag indicating whether CAN asynchronous communication is active."""
        if self.async_notifier is None or self.async_notifier.stopped:
            return False
        if self.network_manager not in self.async_notifier._bus_list:
            return False
        if (self.__async_rx_frames_buffer.is_stopped
                or self.__async_rx_frames_buffer not in self.async_notifier.listeners):
            return False
        if (self.__async_tx_frames_buffer.is_stopped
                or self.__async_tx_frames_buffer not in self.async_notifier.listeners):
            return False
        if (self.__async_fc_frames_buffer.is_stopped
                or self.__async_fc_frames_buffer not in self.async_notifier.listeners):
            return False
        return True

    def setup_sync(self) -> None:
        """
        Prepare this Transport Interface for synchronous communication.

        This method activates synchronous communication and deactivates asynchronous communication.
        """
        self.teardown_async()
        self.__rx_frames_buffer.is_stopped = False  # noqa: vulture
        self.__tx_frames_buffer.is_stopped = False  # noqa: vulture
        self.__fc_frames_buffer.is_stopped = False  # noqa: vulture
        if self.notifier is None or self.notifier.stopped:
            self.notifier = Notifier(bus=self.network_manager,
                                     listeners=[self.__rx_frames_buffer,
                                                self.__tx_frames_buffer,
                                                self.__fc_frames_buffer],
                                     timeout=self._MIN_NOTIFIER_TIMEOUT)
        if self.network_manager not in self.notifier._bus_list:
            self.notifier.add_bus(self.network_manager)
        if self.__rx_frames_buffer not in self.notifier.listeners:
            self.notifier.add_listener(self.__rx_frames_buffer)
        if self.__tx_frames_buffer not in self.notifier.listeners:
            self.notifier.add_listener(self.__tx_frames_buffer)
        if self.__fc_frames_buffer not in self.notifier.listeners:
            self.notifier.add_listener(self.__fc_frames_buffer)

    def setup_async(self, loop: AbstractEventLoop) -> None:
        """
        Configure CAN frame notifier for asynchronous communication.

        :param loop: An :mod:`asyncio` event loop to use.
        """
        self.teardown_sync()
        if (self.async_notifier is None
                or self.async_notifier.stopped
                or self.async_notifier._loop != loop):  # pylint: disable= protected-access
            self.__async_rx_frames_buffer = AsyncBufferedReader(loop=loop)
            self.__async_tx_frames_buffer = AsyncBufferedReader(loop=loop)
            self.__async_fc_frames_buffer = AsyncBufferedReader(loop=loop)
            self.async_notifier = Notifier(bus=self.network_manager,
                                           listeners=[self.__async_rx_frames_buffer,
                                                      self.__async_tx_frames_buffer,
                                                      self.__async_fc_frames_buffer],
                                           timeout=self._MIN_NOTIFIER_TIMEOUT,
                                           loop=loop)
        else:
            self.__async_rx_frames_buffer.is_stopped = False  # noqa: vulture
            self.__async_tx_frames_buffer.is_stopped = False  # noqa: vulture
            self.__async_fc_frames_buffer.is_stopped = False  # noqa: vulture
        if self.network_manager not in self.async_notifier._bus_list:
            self.async_notifier.add_bus(self.network_manager)
        if self.__async_rx_frames_buffer not in self.async_notifier.listeners:
            self.async_notifier.add_listener(self.__async_rx_frames_buffer)
        if self.__async_tx_frames_buffer not in self.async_notifier.listeners:
            self.async_notifier.add_listener(self.__async_tx_frames_buffer)
        if self.__async_fc_frames_buffer not in self.async_notifier.listeners:
            self.async_notifier.add_listener(self.__async_fc_frames_buffer)

    def teardown_sync(self, suppress_warning: bool = False) -> None:
        """
        Stop and remove CAN frame notifier for synchronous communication.

        :param suppress_warning: Do not warn about mixing Synchronous and Asynchronous implementation.
        """
        super().teardown_sync(suppress_warning=suppress_warning)
        if self.notifier is not None:
            self.notifier.stop()
            self.notifier = None
            if not suppress_warning:
                warn(message="Notifier (python-can) for synchronous communication was stopped.",
                     category=RuntimeWarning)

    def teardown_async(self, suppress_warning: bool = False) -> None:
        """
        Stop and remove CAN frame notifier for asynchronous communication.

        :param suppress_warning: Do not warn about mixing Synchronous and Asynchronous implementation.
        """
        super().teardown_async(suppress_warning=suppress_warning)
        if self.async_notifier is not None:
            self.async_notifier.stop()
            self.async_notifier = None
            if not suppress_warning:
                warn(message="Notifier (python-can) for asynchronous communication was stopped.",
                     category=RuntimeWarning)


    def _wait_for_flow_control(self, timeout_timestamp: float) -> CanPacketRecord:
        """
        Wait until a Flow Control CAN packet is received.

        :param timeout_timestamp: Deadline for receiving the Flow Control CAN packet,
            expressed as a :func:`time.perf_counter` timestamp.

        :return: Record containing historical information about the received Flow Control CAN packet.
        """
        packet_record = None
        while (packet_record is None
               or packet_record.addressing_type != AddressingType.PHYSICAL
               or packet_record.packet_type != CanPacketType.FLOW_CONTROL):
            remaining_time_ms = (timeout_timestamp - perf_counter()) * 1000.
            packet_record = self._wait_for_rx_packet(buffer=self.__fc_frames_buffer, timeout=remaining_time_ms)
        return packet_record

    async def _async_wait_for_flow_control(self, timeout_timestamp: float) -> CanPacketRecord:
        """
        Asynchronously wait until a Flow Control CAN packet is received.

        :param timeout_timestamp: Deadline for receiving the Flow Control CAN packet,
            expressed as a :func:`time.perf_counter` timestamp.

        :return: Record containing historical information about the received Flow Control CAN packet.
        """
        packet_record = None
        while (packet_record is None
               or packet_record.addressing_type != AddressingType.PHYSICAL
               or packet_record.packet_type != CanPacketType.FLOW_CONTROL):
            remaining_time_ms = (timeout_timestamp - perf_counter()) * 1000.
            packet_record = await self._async_wait_for_rx_packet(buffer=self.__async_fc_frames_buffer,
                                                                 timeout=remaining_time_ms)
        return packet_record

    def _wait_for_rx_packet(self,
                            buffer: BufferedReader,
                            timeout: TimeMillisecondsAlias | None = None) -> CanPacketRecord:
        """
        Wait until a CAN packet is received.

        :param buffer: Buffer from which the received CAN packet is read.
        :param timeout: Maximum time to wait for a CAN packet, in milliseconds.
            Leave None to wait indefinitely.

        :raise TimeoutError: If the timeout is reached before a CAN packet is received.

        :return: Record containing historical information about the received CAN packet.
        """
        timeout_left_s = self._MAX_LISTENER_TIMEOUT if timeout is None else timeout / 1000.
        timeout_timestamp = perf_counter() + timeout_left_s
        packet_addressing_type = None
        received_frame = None
        while packet_addressing_type is None or received_frame is None:
            timestamp_now = perf_counter()
            timeout_left_s = self._MAX_LISTENER_TIMEOUT if timeout is None else timeout_timestamp - timestamp_now
            if timeout_left_s <= 0:
                raise TimeoutError("Timeout was reached before a CAN packet was received.")
            received_frame = buffer.get_message(timeout=timeout_left_s)
            if received_frame is not None:
                packet_addressing_type = self.addressing_information.is_input_packet(
                    can_id=received_frame.arbitration_id,
                    raw_frame_data=received_frame.data)
        return CanPacketRecord(frame=received_frame,
                               direction=TransmissionDirection.RECEIVED,
                               addressing_type=packet_addressing_type,
                               addressing_format=self.segmenter.addressing_format,
                               transmission_time=datetime.fromtimestamp(received_frame.timestamp)
                               if self.backend in self._INTERFACES_USING_WALL_TIME_TIMESTAMPS else datetime.now(),
                               transmission_timestamp=perf_counter(),
                               transmission_native_timestamp=received_frame.timestamp)

    async def _async_wait_for_rx_packet(self,
                                        buffer: AsyncBufferedReader,
                                        timeout: TimeMillisecondsAlias | None = None) -> CanPacketRecord:
        """
        Asynchronously wait until a CAN packet is received.

        :param buffer: Buffer from which the received CAN packet is read.
        :param timeout: Maximum time to wait for a CAN packet, in milliseconds.
            Leave None to wait indefinitely.

        :raise TimeoutError: If the timeout is reached before a CAN packet is received.

        :return: Record containing historical information about the received CAN packet.
        """
        timeout_left_s = self._MAX_LISTENER_TIMEOUT if timeout is None else timeout / 1000.
        timestamp_timeout = perf_counter() + timeout_left_s
        packet_addressing_type = None
        received_frame = None
        while packet_addressing_type is None or received_frame is None:
            timestamp_now = perf_counter()
            timeout_left_s = self._MAX_LISTENER_TIMEOUT if timeout is None else timestamp_timeout - timestamp_now
            if timeout_left_s <= 0:
                raise TimeoutError("Timeout was reached before a CAN packet was received.")
            try:
                async with async_timeout(timeout_left_s):
                    received_frame = await buffer.get_message()
            except TimeoutError:
                received_frame = None
            if received_frame is not None:
                packet_addressing_type = self.addressing_information.is_input_packet(
                    can_id=received_frame.arbitration_id,
                    raw_frame_data=received_frame.data)
        return CanPacketRecord(frame=received_frame,
                               direction=TransmissionDirection.RECEIVED,
                               addressing_type=packet_addressing_type,
                               addressing_format=self.segmenter.addressing_format,
                               transmission_time=datetime.fromtimestamp(received_frame.timestamp)
                               if self.backend in self._INTERFACES_USING_WALL_TIME_TIMESTAMPS else datetime.now(),
                               transmission_timestamp=perf_counter(),
                               transmission_native_timestamp=received_frame.timestamp)

    def _wait_for_tx_frame(self,
                           buffer: BufferedReader,
                           frame: PythonCanFrame,
                           timestamp: float) -> PythonCanFrame:
        """
        Wait for record of sent CAN frame.

        :param buffer: Listener to which CAN Frame would be delivered.
        :param frame: Object of CAN frame that was scheduled for sending.
        :param timestamp: Timestamp when CAN frame transmission was started.

        :raise TimeoutError: Timeout was reached before a CAN frame was observed.

        :return: Record containing historical information about the transmitted CAN packet or None if not observed.
        """
        timestamp_timeout = timestamp + self._MAX_TX_WAIT
        sent_frame = None
        while sent_frame is None:
            timestamp_now = perf_counter()
            timeout_left_s = timestamp_timeout - timestamp_now
            if timeout_left_s <= 0:
                raise TimeoutError("Timeout was reached before a CAN frame was observed.")
            sent_frame = buffer.get_message(timeout=timeout_left_s)
            if (sent_frame is None
                    or sent_frame.is_rx
                    or sent_frame.arbitration_id != frame.arbitration_id
                    or sent_frame.data != frame.data):
                sent_frame = None  # another frame fetched
        return sent_frame

    async def _async_wait_for_tx_frame(self,
                                       buffer: AsyncBufferedReader,
                                       frame: PythonCanFrame,
                                       timestamp: float) -> PythonCanFrame:
        """
        Wait for record of sent CAN frame.

        :param buffer: Listener to which CAN Frame would be delivered.
        :param frame: Object of CAN frame that was scheduled for sending.
        :param timestamp: Timestamp when CAN frame transmission was started.

        :raise TimeoutError: Timeout was reached before a CAN frame was observed.

        :return: Record containing historical information about the transmitted CAN packet or None if not observed.
        """
        timestamp_timeout = timestamp + self._MAX_TX_WAIT
        sent_frame = None
        while sent_frame is None:
            timestamp_now = perf_counter()
            timeout_left_s = timestamp_timeout - timestamp_now
            if timeout_left_s <= 0:
                raise TimeoutError("Timeout was reached before a CAN frame was observed.")
            async with async_timeout(timeout_left_s):
                sent_frame = await buffer.get_message()
            if (sent_frame is None
                    or sent_frame.is_rx
                    or sent_frame.arbitration_id != frame.arbitration_id
                    or sent_frame.data != frame.data):
                sent_frame = None  # another frame fetched
        return sent_frame

    def clear_received_frame_buffers(self) -> None:
        """
        Clear buffers for storing received CAN frames.

        .. warning:: This makes all previously received CAN packets inaccessible.
        """
        while not self.__rx_frames_buffer.buffer.empty():
            self.__rx_frames_buffer.buffer.get_nowait()
        while not self.__async_rx_frames_buffer.buffer.empty():
            self.__async_rx_frames_buffer.buffer.get_nowait()

    def clear_transmitted_frame_buffers(self) -> None:
        """Clear buffers for storing transmitted CAN frames."""
        while not self.__tx_frames_buffer.buffer.empty():
            self.__tx_frames_buffer.buffer.get_nowait()
        while not self.__async_tx_frames_buffer.buffer.empty():
            self.__async_tx_frames_buffer.buffer.get_nowait()

    def clear_flow_control_frame_buffers(self) -> None:
        """Clear buffers for storing received Flow Control CAN frames."""
        while not self.__fc_frames_buffer.buffer.empty():
            self.__fc_frames_buffer.buffer.get_nowait()
        while not self.__async_fc_frames_buffer.buffer.empty():
            self.__async_fc_frames_buffer.buffer.get_nowait()

    @staticmethod
    def is_supported_network_manager(bus_manager: Any) -> bool:
        """
        Check whether provided value is a bus manager that is supported by this Transport Interface.

        :param bus_manager: Value to check.

        :return: True if provided bus object is python-can Bus object, False otherwise.
        """
        if not isinstance(bus_manager, BusABC):
            return False
        network_manager_class_name = bus_manager.__class__.__name__
        network_manager_module = bus_manager.__class__.__module__
        for backend_name, (module_path, class_name) in BACKENDS.items():
            if network_manager_module.startswith(module_path) and network_manager_class_name == class_name:
                return True
        return False

    def send_packet(self, packet: CanPacket) -> CanPacketRecord:  # type: ignore
        """
        Transmit CAN packet.

        .. warning:: Must not be called within an asynchronous function.

        :param packet: CAN packet to send.

        :raise TypeError: Provided packet is not CAN packet.

        :return: Record with historic information about transmitted CAN packet.
        """
        if not isinstance(packet, CanPacket):
            raise TypeError(f"Provided value is not an instance of CanPacket class. Actual type: {type(packet)}.")
        self.setup_sync()
        is_flow_control_packet = packet.packet_type == CanPacketType.FLOW_CONTROL
        timeout_ms = self.n_ar_timeout if is_flow_control_packet else self.n_as_timeout
        fd = self.can_version == CanVersion.CAN_FD or CanDlcHandler.is_can_fd_specific_dlc(packet.dlc)
        can_frame = PythonCanFrame(arbitration_id=packet.can_id,
                                   is_extended_id=CanIdHandler.is_extended_can_id(packet.can_id),
                                   data=packet.raw_frame_data,
                                   is_fd=fd,
                                   bitrate_switch=self.bitrate_switch,
                                   is_rx=False,
                                   is_error_frame=False,
                                   is_remote_frame=False)
        self.time_sync.sync()
        self.clear_transmitted_frame_buffers()
        timestamp_start = perf_counter()
        self.network_manager.send(msg=can_frame, timeout=timeout_ms / 1000.)
        timestamp_end = perf_counter()
        try:
            sent_can_frame = self._wait_for_tx_frame(buffer=self.__tx_frames_buffer,
                                                     frame=can_frame,
                                                     timestamp=timestamp_start)
        except TimeoutError:
            warn(message="CAN frame that was sent, was not observed. Transmission time will be approximated.",
                 category=RuntimeWarning)
            transmission_timestamp = timestamp_end
            sent_can_frame = PythonCanFrame(arbitration_id=can_frame.arbitration_id,
                                            is_extended_id=can_frame.is_extended_id,
                                            data=can_frame.data,
                                            is_fd=can_frame.is_fd,
                                            bitrate_switch=can_frame.bitrate_switch,
                                            is_rx=False,
                                            is_error_frame=False,
                                            is_remote_frame=False,
                                            timestamp=self.time_sync.perf_counter_to_time(timestamp_end))
        else:
            transmission_timestamp = perf_counter()
        if is_flow_control_packet:
            self._update_n_ar_measured((timestamp_end - timestamp_start) * 1000.)
        else:
            self._update_n_as_measured((timestamp_end - timestamp_start) * 1000.)
        return CanPacketRecord(frame=sent_can_frame,
                               direction=TransmissionDirection.TRANSMITTED,
                               addressing_type=packet.addressing_type,
                               addressing_format=packet.addressing_format,
                               transmission_time=datetime.fromtimestamp(
                                   sent_can_frame.timestamp
                                   if self.backend in self._INTERFACES_USING_WALL_TIME_TIMESTAMPS else
                                   self.time_sync.perf_counter_to_time(transmission_timestamp)),
                               transmission_timestamp=transmission_timestamp,
                               transmission_native_timestamp=sent_can_frame.timestamp)

    async def async_send_packet(self,
                                packet: CanPacket,  # type: ignore
                                loop: AbstractEventLoop | None = None) -> CanPacketRecord:
        """
        Transmit asynchronously CAN packet.

        :param packet: CAN packet to send.
        :param loop: An asyncio event loop used for observing messages.

        :return: Record with historic information about transmitted CAN packet.
        """
        if not isinstance(packet, CanPacket):
            raise TypeError(f"Provided value is not an instance of CanPacket class. Actual type: {type(packet)}.")
        loop = loop if isinstance(loop, AbstractEventLoop) else get_running_loop()
        self.setup_async(loop=loop)
        is_flow_control_packet = packet.packet_type == CanPacketType.FLOW_CONTROL
        timeout_ms = self.n_ar_timeout if is_flow_control_packet else self.n_as_timeout
        fd = self.can_version == CanVersion.CAN_FD or CanDlcHandler.is_can_fd_specific_dlc(packet.dlc)
        can_frame = PythonCanFrame(arbitration_id=packet.can_id,
                                   is_extended_id=CanIdHandler.is_extended_can_id(packet.can_id),
                                   data=packet.raw_frame_data,
                                   is_fd=fd,
                                   bitrate_switch=self.bitrate_switch,
                                   is_rx=False,
                                   is_error_frame=False,
                                   is_remote_frame=False)
        self.time_sync.sync()
        self.clear_transmitted_frame_buffers()
        timestamp_start = perf_counter()
        self.network_manager.send(msg=can_frame, timeout=timeout_ms / 1000.)
        timestamp_end = perf_counter()
        try:
            sent_can_frame = await self._async_wait_for_tx_frame(buffer=self.__async_tx_frames_buffer,
                                                                 frame=can_frame,
                                                                 timestamp=timestamp_start)
        except (TimeoutError, AsyncioTimeoutError):
            warn(message="CAN frame that was sent, was not observed. Transmission time will be approximated.",
                 category=RuntimeWarning)
            transmission_timestamp = timestamp_end
            sent_can_frame = PythonCanFrame(arbitration_id=can_frame.arbitration_id,
                                            is_extended_id=can_frame.is_extended_id,
                                            data=can_frame.data,
                                            is_fd=can_frame.is_fd,
                                            bitrate_switch=can_frame.bitrate_switch,
                                            is_rx=False,
                                            is_error_frame=False,
                                            is_remote_frame=False,
                                            timestamp=self.time_sync.perf_counter_to_time(timestamp_end))
        else:
            transmission_timestamp = perf_counter()
        if is_flow_control_packet:
            self._update_n_ar_measured((timestamp_end - timestamp_start) * 1000.)
        else:
            self._update_n_as_measured((timestamp_end - timestamp_start) * 1000.)
        return CanPacketRecord(frame=sent_can_frame,
                               direction=TransmissionDirection.TRANSMITTED,
                               addressing_type=packet.addressing_type,
                               addressing_format=packet.addressing_format,
                               transmission_time=datetime.fromtimestamp(
                                   sent_can_frame.timestamp
                                   if self.backend in self._INTERFACES_USING_WALL_TIME_TIMESTAMPS else
                                   self.time_sync.perf_counter_to_time(transmission_timestamp)),
                               transmission_timestamp=transmission_timestamp,
                               transmission_native_timestamp=sent_can_frame.timestamp)

    def receive_packet(self, timeout: TimeMillisecondsAlias | None = None) -> CanPacketRecord:
        """
        Receive CAN packet.

        .. warning:: Must not be called within an asynchronous function.

        :param timeout: Maximal time (in milliseconds) to wait.
            Leave None to wait forever.

        :return: Record with historic information about received CAN packet.
        """
        validate_timeout(timeout)
        self.setup_sync()
        return self._wait_for_rx_packet(buffer=self.__rx_frames_buffer, timeout=timeout)

    async def async_receive_packet(self,
                                   timeout: TimeMillisecondsAlias | None = None,
                                   loop: AbstractEventLoop | None = None) -> CanPacketRecord:
        """
        Receive asynchronously CAN packet.

        :param timeout: Maximal time (in milliseconds) to wait.
            Leave None to wait forever.
        :param loop: An asyncio event loop used for observing messages.

        :return: Record with historic information about received CAN packet.
        """
        validate_timeout(timeout)
        loop = loop if isinstance(loop, AbstractEventLoop) else get_running_loop()
        self.setup_async(loop=loop)
        return await self._async_wait_for_rx_packet(buffer=self.__async_rx_frames_buffer, timeout=timeout)

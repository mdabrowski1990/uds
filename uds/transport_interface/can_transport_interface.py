"""Definition and implementation of UDS Transport Interface for CAN bus."""

__all__ = ["AbstractCanTransportInterface", "PyCanTransportInterface"]

from typing import Any, Optional
from abc import abstractmethod
from warnings import warn
from asyncio import AbstractEventLoop, wait_for, get_running_loop
from datetime import datetime
from time import time

from can import BusABC, AsyncBufferedReader, BufferedReader, Notifier, Message

from uds.utilities import TimeMilliseconds, ValueWarning
from uds.can import AbstractCanAddressingInformation, CanIdHandler, CanDlcHandler
from uds.packet import CanPacket, CanPacketRecord, CanPacketType
from uds.transmission_attributes import TransmissionDirection
from uds.segmentation import CanSegmenter
from .abstract_transport_interface import AbstractTransportInterface


class AbstractCanTransportInterface(AbstractTransportInterface):
    """
    Abstract definition of Transport Interface for managing UDS on CAN bus.

    CAN Transport Interfaces are meant to handle UDS middle layers (Transport and Network) on CAN bus.
    """

    N_AS_TIMEOUT: TimeMilliseconds = 1000
    """Timeout value of :ref:`N_As <knowledge-base-can-n-as>` time parameter according to ISO 15765-2."""
    N_AR_TIMEOUT: TimeMilliseconds = 1000
    """Timeout value of :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter according to ISO 15765-2."""
    N_BS_TIMEOUT: TimeMilliseconds = 1000
    """Timeout value of :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter according to ISO 15765-2."""
    N_CR_TIMEOUT: TimeMilliseconds = 1000
    """Timeout value of :ref:`N_Cr <knowledge-base-can-n-cr>` time parameter according to ISO 15765-2."""

    DEFAULT_N_BR: TimeMilliseconds = 0
    """Default value of :ref:`N_Br <knowledge-base-can-n-br>` time parameter."""
    DEFAULT_N_CS: Optional[TimeMilliseconds] = None
    """Default value of :ref:`N_Cs <knowledge-base-can-n-br>` time parameter."""

    def __init__(self,
                 can_bus_manager: Any,
                 addressing_information: AbstractCanAddressingInformation,
                 **kwargs: Any) -> None:
        """
        Create Transport Interface (an object for handling UDS Transport and Network layers).

        :param can_bus_manager: An object that handles CAN bus (Physical and Data layers of OSI Model).
        :param addressing_information: Addressing Information of CAN Transport Interface.
        :param kwargs: Optional arguments that are specific for CAN bus.

            - :parameter n_as_timeout: Timeout value for :ref:`N_As <knowledge-base-can-n-as>` time parameter.
            - :parameter n_ar_timeout: Timeout value for :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter.
            - :parameter n_bs_timeout: Timeout value for :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter.
            - :parameter n_br: Value of :ref:`N_Br <knowledge-base-can-n-br>` time parameter to use in communication.
            - :parameter n_cs: Value of :ref:`N_Cs <knowledge-base-can-n-cs>` time parameter to use in communication.
            - :parameter n_cr_timeout: Timeout value for :ref:`N_Cr <knowledge-base-can-n-cr>` time parameter.
            - :parameter dlc: Base CAN DLC value to use for CAN Packets.
            - :parameter use_data_optimization: Information whether to use CAN Frame Data Optimization.
            - :parameter filler_byte: Filler byte value to use for CAN Frame Data Padding.

        :raise TypeError: Provided Addressing Information value has unexpected type.
        """
        if not isinstance(addressing_information, AbstractCanAddressingInformation):
            raise TypeError("Unsupported type of Addressing Information was provided.")
        self.__addressing_information: AbstractCanAddressingInformation = addressing_information
        super().__init__(bus_manager=can_bus_manager)
        self.n_as_timeout = kwargs.pop("n_as_timeout", self.N_AS_TIMEOUT)
        self.n_ar_timeout = kwargs.pop("n_ar_timeout", self.N_AR_TIMEOUT)
        self.n_bs_timeout = kwargs.pop("n_bs_timeout", self.N_BS_TIMEOUT)
        self.n_br = kwargs.pop("n_br", self.DEFAULT_N_BR)
        self.n_cs = kwargs.pop("n_cs", self.DEFAULT_N_CS)
        self.n_cr_timeout = kwargs.pop("n_cr_timeout", self.N_CR_TIMEOUT)
        self.__segmenter = CanSegmenter(addressing_information=addressing_information, **kwargs)

    @property
    def segmenter(self) -> CanSegmenter:
        """Value of the segmenter used by this CAN Transport Interface."""
        return self.__segmenter

    # Time parameter - CAN Network Layer

    @property
    def n_as_timeout(self) -> TimeMilliseconds:
        """Timeout value for N_As time parameter."""
        return self.__n_as_timeout

    @n_as_timeout.setter
    def n_as_timeout(self, value: TimeMilliseconds):
        """
        Set timeout value for N_As time parameter.

        :param value: Value of timeout to set.

        :raise TypeError: Provided value is not int or float.
        :raise ValueError: Provided value is less or equal 0.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided time parameter value must be int or float type.")
        if value <= 0:
            raise ValueError("Provided time parameter value must be greater than 0.")
        if value != self.N_AS_TIMEOUT:
            warn(message="Non-default value of N_As timeout was set.",
                 category=ValueWarning)
        self.__n_as_timeout = value

    @property
    @abstractmethod
    def n_as_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_As time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """

    @property
    def n_ar_timeout(self) -> TimeMilliseconds:
        """Timeout value for N_Ar time parameter."""
        return self.__n_ar_timeout

    @n_ar_timeout.setter
    def n_ar_timeout(self, value: TimeMilliseconds):
        """
        Set timeout value for N_Ar time parameter.

        :param value: Value of timeout to set.

        :raise TypeError: Provided value is not int or float.
        :raise ValueError: Provided value is less or equal 0.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided time parameter value must be int or float type.")
        if value <= 0:
            raise ValueError("Provided time parameter value must be greater than 0.")
        if value != self.N_AR_TIMEOUT:
            warn(message="Non-default value of N_Ar timeout was set.",
                 category=ValueWarning)
        self.__n_ar_timeout = value

    @property
    @abstractmethod
    def n_ar_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_Ar time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """

    @property
    def n_bs_timeout(self) -> TimeMilliseconds:
        """Timeout value for N_Bs time parameter."""
        return self.__n_bs_timeout

    @n_bs_timeout.setter
    def n_bs_timeout(self, value: TimeMilliseconds):
        """
        Set timeout value for N_Bs time parameter.

        :param value: Value of timeout to set.

        :raise TypeError: Provided value is not int or float.
        :raise ValueError: Provided value is less or equal 0.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided time parameter value must be int or float type.")
        if value <= 0:
            raise ValueError("Provided time parameter value must be greater than 0.")
        if value != self.N_BS_TIMEOUT:
            warn(message="Non-default value of N_Bs timeout was set.",
                 category=ValueWarning)
        self.__n_bs_timeout = value

    @property  # noqa
    @abstractmethod
    def n_bs_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_Bs time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """

    @property
    def n_br(self) -> TimeMilliseconds:
        """
        Get the value of N_Br time parameter which is currently set.

        .. note:: The actual (observed on the bus) value will be slightly longer as it also includes computation
            and CAN Interface delays.
        """
        return self.__n_br

    @n_br.setter
    def n_br(self, value: TimeMilliseconds):
        """
        Set the value of N_Br time parameter to use.

        :param value: The value to set.

        :raise TypeError: Provided value is not int or float.
        :raise ValueError: Provided value is out of range.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided time parameter value must be int or float type.")
        if not 0 <= value < self.n_br_max:
            raise ValueError("Provided time parameter value is out of range.")
        self.__n_br = value

    @property
    def n_br_max(self) -> TimeMilliseconds:
        """
        Get the maximum valid value of N_Br time parameter.

        .. warning:: To assess maximal value of :ref:`N_Br <knowledge-base-can-n-br>`, the actual value of
            :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter is required.
            Either the latest measured value of N_Ar would be used, or 0ms would be assumed (if there are
            no measurement result).
        """
        n_ar_measured = 0 if self.n_ar_measured is None else self.n_ar_measured
        return 0.9 * self.n_bs_timeout - n_ar_measured

    @property
    def n_cs(self) -> Optional[TimeMilliseconds]:
        """
        Get the value of N_Cs time parameter which is currently set.

        .. note:: The actual (observed on the bus) value will be slightly longer as it also includes computation
            and CAN Interface delays.
        """
        return self.__n_cs

    @n_cs.setter
    def n_cs(self, value: Optional[TimeMilliseconds]):
        """
        Set the value of N_Cs time parameter to use.

        :param value: The value to set.

        :raise TypeError: Provided value is not int or float.
        :raise ValueError: Provided value is out of range.
        """
        if value is not None:
            if not isinstance(value, (int, float)):
                raise TypeError("Provided time parameter value must be int or float type.")
            if not 0 <= value < self.n_cs_max:
                raise ValueError("Provided time parameter value is out of range.")
        self.__n_cs = value

    @property
    def n_cs_max(self) -> TimeMilliseconds:
        """
        Get the maximum valid value of N_Cs time parameter.

        .. warning:: To assess maximal value of :ref:`N_Cs <knowledge-base-can-n-cs>`, the actual value of
            :ref:`N_As <knowledge-base-can-n-as>` time parameter is required.
            Either the latest measured value of N_Ar would be used, or 0ms would be assumed (if there are
            no measurement result).
        """
        n_as_measured = 0 if self.n_as_measured is None else self.n_as_measured
        return 0.9 * self.n_cr_timeout - n_as_measured

    @property
    def n_cr_timeout(self) -> TimeMilliseconds:
        """Timeout value for N_Cr time parameter."""
        return self.__n_cr_timeout

    @n_cr_timeout.setter
    def n_cr_timeout(self, value: TimeMilliseconds):
        """
        Set timeout value for N_Cr time parameter.

        :param value: Value of timeout to set.

        :raise TypeError: Provided value is not int or float.
        :raise ValueError: Provided value is less or equal 0.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided time parameter value must be int or float type.")
        if value <= 0:
            raise ValueError("Provided time parameter value must be greater than 0.")
        if value != self.N_CR_TIMEOUT:
            warn(message="Non-default value of N_Cr timeout was set.",
                 category=ValueWarning)
        self.__n_cr_timeout = value

    @property  # noqa
    @abstractmethod
    def n_cr_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_Cr time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """

    # Communication parameters

    @property
    def addressing_information(self) -> AbstractCanAddressingInformation:
        """Addressing Information of Transport Interface."""
        return self.__addressing_information

    @property
    def dlc(self) -> int:
        """
        Value of base CAN DLC to use for output CAN Packets.

        .. note:: All output CAN Packets will have this DLC value set unless
            :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>` is used.
        """
        return self.segmenter.dlc

    @dlc.setter
    def dlc(self, value: int):
        """
        Set value of base CAN DLC to use for output CAN Packets.

        :param value: Value to set.
        """
        self.segmenter.dlc = value

    @property
    def use_data_optimization(self) -> bool:
        """Information whether to use CAN Frame Data Optimization during CAN Packets creation."""
        return self.segmenter.use_data_optimization

    @use_data_optimization.setter
    def use_data_optimization(self, value: bool):
        """
        Set whether to use CAN Frame Data Optimization during CAN Packets creation.

        :param value: Value to set.
        """
        self.segmenter.use_data_optimization = value

    @property
    def filler_byte(self) -> int:
        """Filler byte value to use for output CAN Frame Data Padding during segmentation."""
        return self.segmenter.filler_byte

    @filler_byte.setter
    def filler_byte(self, value: int):
        """
        Set value of filler byte to use for output CAN Frame Data Padding.

        :param value: Value to set.
        """
        self.segmenter.filler_byte = value


class PyCanTransportInterface(AbstractCanTransportInterface):
    """
    Transport Interface for managing UDS on CAN with python-can package as bus handler.

    .. note:: Documentation for python-can package: https://python-can.readthedocs.io/
    """

    _MAX_LISTENER_TIMEOUT: float = 4280000.  # ms
    """Maximal timeout value accepted by python-can listeners."""
    _MIN_NOTIFIER_TIMEOUT: float = 0.0000001  # s
    """Minimal timeout for notifiers that does not cause malfunctioning of listeners."""

    def __init__(self,
                 can_bus_manager: BusABC,
                 addressing_information: AbstractCanAddressingInformation,
                 **kwargs: Any) -> None:
        """
        Create python-can Transport Interface.

        :param can_bus_manager: Python-can bus object for handling CAN.

            .. warning:: Bus must have capability of receiving transmitted frame (``receive_own_messages=True`` set).

        :param addressing_information: Addressing Information of CAN Transport Interface.
        :param kwargs: Optional arguments that are specific for CAN bus.

            - :parameter n_as_timeout: Timeout value for :ref:`N_As <knowledge-base-can-n-as>` time parameter.
            - :parameter n_ar_timeout: Timeout value for :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter.
            - :parameter n_bs_timeout: Timeout value for :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter.
            - :parameter n_br: Value of :ref:`N_Br <knowledge-base-can-n-br>` time parameter to use in communication.
            - :parameter n_cs: Value of :ref:`N_Cs <knowledge-base-can-n-cs>` time parameter to use in communication.
            - :parameter n_cr_timeout: Timeout value for :ref:`N_Cr <knowledge-base-can-n-cr>` time parameter.
            - :parameter dlc: Base CAN DLC value to use for CAN Packets.
            - :parameter use_data_optimization: Information whether to use CAN Frame Data Optimization.
            - :parameter filler_byte: Filler byte value to use for CAN Frame Data Padding.
        """
        self.__n_as_measured: Optional[TimeMilliseconds] = None
        self.__n_ar_measured: Optional[TimeMilliseconds] = None
        self.__n_bs_measured: Optional[TimeMilliseconds] = None
        self.__n_cr_measured: Optional[TimeMilliseconds] = None
        super().__init__(can_bus_manager=can_bus_manager,
                         addressing_information=addressing_information,
                         **kwargs)
        self.__notifier: Optional[Notifier] = None
        self.__frames_buffer = BufferedReader()
        self.__async_notifier: Optional[Notifier] = None
        self.__async_frames_buffer = AsyncBufferedReader()

    def __del__(self):
        # TODO: docstring and unit tests
        self._teardown_notifier(suppress_warning=True)
        self._teardown_async_notifier(suppress_warning=True)

    @property
    def n_as_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_As time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """
        return self.__n_as_measured

    @property
    def n_ar_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_Ar time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """
        return self.__n_ar_measured

    @property  # noqa
    def n_bs_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_Bs time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """
        return self.__n_bs_measured

    @property  # noqa
    def n_cr_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_Cr time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """
        return self.__n_cr_measured

    def _teardown_notifier(self, suppress_warning: bool = False) -> None:
        # TODO: docstring and unit tests
        if self.__notifier is not None:
            self.__notifier.stop(self._MIN_NOTIFIER_TIMEOUT)
            self.__notifier = None
            if not suppress_warning:
                warn(message="Asynchronous (`PyCanTransportInterface.async_send_packet`, "
                             "`PyCanTransportInterface.async_receive_packet methods`) "
                             "and synchronous (`PyCanTransportInterface.send_packet`, "
                             "`PyCanTransportInterface.receive_packet methods`) shall not be used together.",
                     category=UserWarning)

    def _teardown_async_notifier(self, suppress_warning: bool = False):
        # TODO: docstring and unit tests
        if self.__async_notifier is not None:
            self.__async_notifier.stop(self._MIN_NOTIFIER_TIMEOUT)
            self.__async_notifier = None
            if not suppress_warning:
                if not suppress_warning:
                    warn(message="Asynchronous (`PyCanTransportInterface.async_send_packet`, "
                                 "`PyCanTransportInterface.async_receive_packet methods`) "
                                 "and synchronous (`PyCanTransportInterface.send_packet`, "
                                 "`PyCanTransportInterface.receive_packet methods`) shall not be used together.",
                         category=UserWarning)

    def _setup_notifier(self) -> None:
        # TODO: docstring and unit tests
        self._teardown_async_notifier()
        if self.__notifier is None:
            self.__notifier = Notifier(bus=self.bus_manager,
                                       listeners=[self.__frames_buffer],
                                       timeout=self._MIN_NOTIFIER_TIMEOUT)

    def _setup_async_notifier(self, loop) -> None:
        # TODO: docstring and unit tests
        self._teardown_notifier()
        if self.__async_notifier is None:
            self.__async_notifier = Notifier(bus=self.bus_manager,
                                             listeners=[self.__async_frames_buffer],
                                             timeout=self._MIN_NOTIFIER_TIMEOUT,
                                             loop=loop)

    def clear_frames_buffers(self) -> None:
        # TODO: docstring and unit tests
        for _ in range(self.__frames_buffer.buffer.qsize()):
            self.__frames_buffer.buffer.get_nowait()
        for _ in range(self.__async_frames_buffer.buffer.qsize()):
            self.__async_frames_buffer.buffer.get_nowait()

    @staticmethod
    def is_supported_bus_manager(bus_manager: Any) -> bool:
        """
        Check whether provided value is a bus manager that is supported by this Transport Interface.

        :param bus_manager: Value to check.

        :return: True if provided bus object is compatible with this Transport Interface, False otherwise.
        """
        return isinstance(bus_manager, BusABC)

    def send_packet(self, packet: CanPacket) -> CanPacketRecord:  # type: ignore
        """
        Transmit CAN packet.

        .. warning:: Must not be called within an asynchronous function.

        :param packet: CAN packet to send.

        :return: Record with historic information about transmitted CAN packet.
        """
        time_start = time()
        if not isinstance(packet, CanPacket):
            raise TypeError("Provided packet value does not contain a CAN Packet.")
        is_flow_control_packet = packet.packet_type == CanPacketType.FLOW_CONTROL
        timeout = self.n_ar_timeout if is_flow_control_packet else self.n_as_timeout
        can_message = Message(arbitration_id=packet.can_id,
                              is_extended_id=CanIdHandler.is_extended_can_id(packet.can_id),
                              data=packet.raw_frame_data,
                              is_fd=CanDlcHandler.is_can_fd_specific_dlc(packet.dlc))
        self._setup_notifier()
        self.clear_frames_buffers()
        self.bus_manager.send(can_message)
        observed_frame = None
        while observed_frame is None \
                or observed_frame.arbitration_id != packet.can_id \
                or tuple(observed_frame.data) != packet.raw_frame_data \
                or not observed_frame.is_rx \
                or observed_frame.timestamp < time_start:
            timeout_left = timeout / 1000. - (time() - time_start)
            if timeout_left <= 0:
                raise TimeoutError("Timeout was reached before observing a CAN Packet being transmitted.")
            observed_frame = self.__frames_buffer.get_message(timeout=timeout_left)
        if is_flow_control_packet:
            self.__n_ar_measured = observed_frame.timestamp - time_start
        else:
            self.__n_as_measured = observed_frame.timestamp - time_start
        return CanPacketRecord(frame=observed_frame,
                               direction=TransmissionDirection.TRANSMITTED,
                               addressing_type=packet.addressing_type,
                               addressing_format=packet.addressing_format,
                               transmission_time=datetime.fromtimestamp(observed_frame.timestamp))

    def receive_packet(self, timeout: Optional[TimeMilliseconds] = None) -> CanPacketRecord:
        """
        Receive CAN packet.

        .. warning:: Must not be called within an asynchronous function.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TypeError: Provided timeout value is not None neither int nor float type.
        :raise ValueError: Provided timeout value is less or equal 0.
        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information about received CAN packet.
        """
        time_start = time()
        if timeout is not None:
            if not isinstance(timeout, (int, float)):
                raise TypeError("Provided timeout value is not None neither int nor float type.")
            if timeout <= 0:
                raise ValueError("Provided timeout value is less or equal 0.")
        self._setup_notifier()
        packet_addressing_type = None
        while packet_addressing_type is None:
            time_now = time()
            timeout_left = self._MAX_LISTENER_TIMEOUT if timeout is None else timeout / 1000. - (time_now - time_start)
            if timeout_left <= 0:
                raise TimeoutError("Timeout was reached before a CAN Packet was received.")
            received_frame = self.__frames_buffer.get_message(timeout=timeout_left)
            if received_frame is None:
                raise TimeoutError("Timeout was reached before a CAN Packet was received.")
            if timeout is not None and (received_frame.timestamp - time_start) * 1000. > timeout:
                raise TimeoutError("CAN Packet was received after timeout.")
            packet_addressing_type = self.segmenter.is_input_packet(can_id=received_frame.arbitration_id,
                                                                    data=received_frame.data)
        return CanPacketRecord(frame=received_frame,
                               direction=TransmissionDirection.RECEIVED,
                               addressing_type=packet_addressing_type,
                               addressing_format=self.segmenter.addressing_format,
                               transmission_time=datetime.fromtimestamp(received_frame.timestamp))

    async def async_send_packet(self,
                                packet: CanPacket,  # type: ignore
                                loop: Optional[AbstractEventLoop] = None) -> CanPacketRecord:
        """
        Transmit CAN packet.

        :param packet: CAN packet to send.
        :param loop: An asyncio event loop used for observing messages.

        :raise TypeError: Provided packet is not CAN Packet.

        :return: Record with historic information about transmitted CAN packet.
        """
        time_start = time()
        if not isinstance(packet, CanPacket):
            raise TypeError("Provided packet value does not contain a CAN Packet.")
        loop = get_running_loop() if loop is None else loop
        is_flow_control_packet = packet.packet_type == CanPacketType.FLOW_CONTROL
        timeout = self.n_ar_timeout if is_flow_control_packet else self.n_as_timeout
        self._setup_async_notifier(loop)
        self.clear_frames_buffers()
        can_message = Message(arbitration_id=packet.can_id,
                              is_extended_id=CanIdHandler.is_extended_can_id(packet.can_id),
                              data=packet.raw_frame_data,
                              is_fd=CanDlcHandler.is_can_fd_specific_dlc(packet.dlc))
        self.bus_manager.send(can_message)
        observed_frame = None
        while observed_frame is None \
                or observed_frame.arbitration_id != packet.can_id \
                or tuple(observed_frame.data) != packet.raw_frame_data \
                or not observed_frame.is_rx \
                or observed_frame.timestamp < time_start:
            timeout_left = timeout / 1000. - (time() - time_start)
            observed_frame = await wait_for(self.__async_frames_buffer.get_message(), timeout=timeout_left)
        if is_flow_control_packet:
            self.__n_ar_measured = observed_frame.timestamp - time_start
        else:
            self.__n_as_measured = observed_frame.timestamp - time_start
        return CanPacketRecord(frame=observed_frame,
                               direction=TransmissionDirection.TRANSMITTED,
                               addressing_type=packet.addressing_type,
                               addressing_format=packet.addressing_format,
                               transmission_time=datetime.fromtimestamp(observed_frame.timestamp))

    async def async_receive_packet(self,
                                   timeout: Optional[TimeMilliseconds] = None,
                                   loop: Optional[AbstractEventLoop] = None) -> CanPacketRecord:
        """
        Receive CAN packet.

        :param timeout: Maximal time (in milliseconds) to wait.
        :param loop: An asyncio event loop used for observing messages.

        :raise TypeError: Provided timeout value is not None neither int nor float type.
        :raise ValueError: Provided timeout value is less or equal 0.
        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information about received CAN packet.
        """
        time_start = time()
        if timeout is not None:
            if not isinstance(timeout, (int, float)):
                raise TypeError("Provided timeout value is not None neither int nor float type.")
            if timeout <= 0:
                raise ValueError("Provided timeout value is less or equal 0.")
        loop = get_running_loop() if loop is None else loop
        self._setup_async_notifier(loop)
        packet_addressing_type = None
        while packet_addressing_type is None:
            if timeout is None:
                timeout_left = None
            else:
                timeout_left = timeout / 1000. - (time() - time_start)
                if timeout_left <= 0:
                    raise TimeoutError("Timeout was reached before a CAN Packet was received.")
            received_frame = await wait_for(self.__async_frames_buffer.get_message(),
                                            timeout=timeout_left)
            packet_addressing_type = self.segmenter.is_input_packet(can_id=received_frame.arbitration_id,
                                                                    data=received_frame.data)
        return CanPacketRecord(frame=received_frame,
                               direction=TransmissionDirection.RECEIVED,
                               addressing_type=packet_addressing_type,
                               addressing_format=self.segmenter.addressing_format,
                               transmission_time=datetime.fromtimestamp(received_frame.timestamp))

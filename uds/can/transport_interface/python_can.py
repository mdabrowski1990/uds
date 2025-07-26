"""Implementation of UDS Transport Interface for CAN bus using python-can as bus manager."""

__all__ = ["PyCanTransportInterface"]

from asyncio import AbstractEventLoop, get_running_loop, wait_for
from datetime import datetime
from time import time
from typing import Any, List, Optional, Tuple, Union
from warnings import warn

from can import AsyncBufferedReader, BufferedReader, BusABC
from can import Message as PythonCanMessage
from can import Notifier
from uds.message import UdsMessage, UdsMessageRecord
from uds.utilities import (
    NewMessageReceptionWarning,
    TimeMillisecondsAlias,
    TransmissionDirection,
    UnexpectedPacketReceptionWarning,
)

from ..addressing import AbstractCanAddressingInformation
from ..frame import CanDlcHandler, CanIdHandler
from ..packet import CanFlowStatus, CanPacket, CanPacketRecord, CanPacketType, CanSTminTranslator
from .common import AbstractCanTransportInterface


class PyCanTransportInterface(AbstractCanTransportInterface):
    """
    Transport Interface for managing UDS on CAN with python-can package as bus handler.

    .. note:: Documentation for python-can package: https://python-can.readthedocs.io/
    """

    _MAX_LISTENER_TIMEOUT: float = 4280000.  # ms
    """Maximal timeout value accepted by python-addressing listeners."""
    _MIN_NOTIFIER_TIMEOUT: float = 0.001  # s
    """Minimal timeout for notifiers that does not cause malfunctioning of listeners."""

    def __init__(self,
                 network_manager: BusABC,
                 addressing_information: AbstractCanAddressingInformation,
                 **configuration_params: Any) -> None:
        """
        Create python-addressing Transport Interface.

        :param network_manager: Python-can bus object for handling CAN network.

            .. warning:: Bus must have capability of observing transmitted frames.

        :param addressing_information: Addressing Information of UDS entity simulated by this CAN Transport Interface.
        :param configuration_params: Additional configuration parameters.

            - :parameter n_as_timeout: Timeout value for :ref:`N_As <knowledge-base-can-n-as>` time parameter.
            - :parameter n_ar_timeout: Timeout value for :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter.
            - :parameter n_bs_timeout: Timeout value for :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter.
            - :parameter n_br: Value of :ref:`N_Br <knowledge-base-can-n-br>` time parameter to use in communication.
            - :parameter n_cs: Value of :ref:`N_Cs <knowledge-base-can-n-cs>` time parameter to use in communication.
            - :parameter n_cr_timeout: Timeout value for :ref:`N_Cr <knowledge-base-can-n-cr>` time parameter.
            - :parameter dlc: Base CAN DLC value to use for CAN packets.
            - :parameter use_data_optimization: Information whether to use
                :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>`.
            - :parameter filler_byte: Filler byte value to use for
                :ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>`.
            - :parameter flow_control_parameters_generator: Generator with Flow Control parameters to use.
        """
        super().__init__(network_manager=network_manager,
                         addressing_information=addressing_information,
                         **configuration_params)
        self.__frames_buffer = BufferedReader()
        self.__async_frames_buffer = AsyncBufferedReader()
        self.__notifier: Optional[Notifier] = None
        self.__async_notifier: Optional[Notifier] = None

    def __del__(self) -> None:
        """Safely close all threads opened by this object."""
        self.__teardown_notifier(suppress_warning=True)
        self.__teardown_async_notifier(suppress_warning=True)

    def __teardown_notifier(self, suppress_warning: bool = False) -> None:
        """
        Stop and remove CAN frame notifier for synchronous communication.

        :param suppress_warning: Do not warn about mixing Synchronous and Asynchronous implementation.
        """
        if self.__notifier is not None:
            self.__notifier.stop(self._MIN_NOTIFIER_TIMEOUT)
            self.__notifier = None
            if not suppress_warning:
                warn(message="Asynchronous (`PyCanTransportInterface.async_send_packet`, "
                             "`PyCanTransportInterface.async_receive_packet methods`) "
                             "and synchronous (`PyCanTransportInterface.send_packet`, "
                             "`PyCanTransportInterface.receive_packet methods`) shall not be used together.",
                     category=UserWarning)

    def __teardown_async_notifier(self, suppress_warning: bool = False) -> None:
        """
        Stop and remove CAN frame notifier for asynchronous communication.

        :param suppress_warning: Do not warn about mixing Synchronous and Asynchronous implementation.
        """
        if self.__async_notifier is not None:
            self.__async_notifier.stop(self._MIN_NOTIFIER_TIMEOUT)
            self.__async_notifier = None
            if not suppress_warning:
                warn(message="Asynchronous (`PyCanTransportInterface.async_send_packet`, "
                             "`PyCanTransportInterface.async_receive_packet methods`) "
                             "and synchronous (`PyCanTransportInterface.send_packet`, "
                             "`PyCanTransportInterface.receive_packet methods`) shall not be used together.",
                     category=UserWarning)

    def __setup_notifier(self) -> None:
        """Configure CAN frame notifier for synchronous communication."""
        self.__teardown_async_notifier()
        if self.__notifier is None:
            self.__notifier = Notifier(bus=self.network_manager,
                                       listeners=[self.__frames_buffer],
                                       timeout=self._MIN_NOTIFIER_TIMEOUT)

    def __setup_async_notifier(self, loop: AbstractEventLoop) -> None:
        """
        Configure CAN frame notifier for asynchronous communication.

        :param loop: An :mod:`asyncio` event loop to use.
        """
        self.__teardown_notifier()
        if self.__async_notifier is None:
            self.__async_notifier = Notifier(bus=self.network_manager,
                                             listeners=[self.__async_frames_buffer],
                                             timeout=self._MIN_NOTIFIER_TIMEOUT,
                                             loop=loop)

    def _send_cf_packets_block(self,
                               cf_packets_block: List[CanPacket],
                               delay: TimeMillisecondsAlias) -> Tuple[CanPacketRecord, ...]:
        """
        Send block of Consecutive Frame CAN packets.

        :param cf_packets_block: Consecutive Frame CAN packets to send.
        :param delay: Minimal delay between sending following Consecutive Frames [ms].

        :raise TransmissionInterruptionError: A new UDS message transmission was started while sending this message.

        :return: Records with historic information about transmitted Consecutive Frame CAN packets.
        """
        packet_records = []
        for cf_packet in cf_packets_block:
            time_now_ms = time() * 1000
            time_end_ms = time_now_ms + delay
            while time_now_ms < time_end_ms:
                try:
                    self.receive_packet(timeout=time_end_ms - time_now_ms)
                except TimeoutError:
                    pass
                else:
                    warn(message="An unrelated CAN packet was received during UDS message transmission.",
                         category=UnexpectedPacketReceptionWarning)
                time_now_ms = time() * 1000
            packet_records.append(self.send_packet(cf_packet))
        return tuple(packet_records)

    async def _async_send_cf_packets_block(self,
                                           cf_packets_block: List[CanPacket],
                                           delay: TimeMillisecondsAlias,
                                           loop: Optional[AbstractEventLoop] = None) -> Tuple[CanPacketRecord, ...]:
        """
        Send block of Consecutive Frame CAN packets asynchronously.

        :param cf_packets_block: Consecutive Frame CAN packets to send.
        :param delay: Minimal delay between sending following Consecutive Frames [ms].
        :param loop: An asyncio event loop to use for scheduling this task.

        :raise TransmissionInterruptionError: A new UDS message transmission was started while sending this message.

        :return: Records with historic information about transmitted Consecutive Frame CAN packets.
        """
        packet_records = []
        for cf_packet in cf_packets_block:
            time_now_ms = time() * 1000
            time_end_ms = time_now_ms + delay
            while time_now_ms < time_end_ms:
                try:
                    await self.async_receive_packet(timeout=time_end_ms - time_now_ms, loop=loop)
                except TimeoutError:
                    pass
                else:
                    warn(message="An unrelated CAN packet was received during UDS message transmission.",
                         category=UnexpectedPacketReceptionWarning)
                time_now_ms = time() * 1000
            packet_records.append(await self.async_send_packet(cf_packet, loop=loop))
        return tuple(packet_records)

    def _message_receive_start(self, initial_packet: CanPacketRecord) -> UdsMessageRecord:
        """
        Continue to receive message after receiving initial packet.

        :param initial_packet: Record of a packet initiating UDS message reception.

        :raise NotImplementedError: Unhandled CAN packet starting a new CAN message transmission was received.

        :return: Record of UDS message received.
        """
        if initial_packet.packet_type == CanPacketType.SINGLE_FRAME:
            return UdsMessageRecord([initial_packet])
        if initial_packet.packet_type == CanPacketType.FIRST_FRAME:
            return self._receive_consecutive_frames(first_frame=initial_packet)
        raise NotImplementedError("CAN packet of unhandled type was received.")

    async def _async_message_receive_start(self,
                                           initial_packet: CanPacketRecord,
                                           loop: Optional[AbstractEventLoop] = None) -> UdsMessageRecord:
        """
        Continue to receive message asynchronously after receiving initial packet.

        :param initial_packet: Record of a packet initiating UDS message reception.
        :param loop: An asyncio event loop used for observing messages.

        :raise NotImplementedError: Unhandled CAN packet starting a new CAN message transmission was received.

        :return: Record of UDS message received.
        """
        if initial_packet.packet_type == CanPacketType.SINGLE_FRAME:
            return UdsMessageRecord([initial_packet])
        if initial_packet.packet_type == CanPacketType.FIRST_FRAME:
            return await self._async_receive_consecutive_frames(first_frame=initial_packet, loop=loop)
        raise NotImplementedError("CAN packet of unhandled type was received.")

    def _receive_cf_packets_block(self,
                                  sequence_number: int,
                                  block_size: int,
                                  remaining_data_length: int) -> Union[UdsMessageRecord, Tuple[CanPacketRecord, ...]]:
        """
        Receive block of :ref:`Consecutive Frames <knowledge-base-can-consecutive-frame>`.

        :param sequence_number: Current :ref:`Sequence Number <knowledge-base-can-sequence-number>`
            (next Consecutive Frame shall have this value set).
        :param block_size: :ref:`Block Size <knowledge-base-can-block-size>` value sent in the last
            :ref:`Flow Control CAN packet <knowledge-base-can-flow-control>`.
        :param remaining_data_length: Number of remaining data bytes to receive in UDS message.

        :return: Either:
            - Record of UDS message if reception was interrupted by a new UDS message transmission.
            - Tuple with records of received Consecutive Frames.
        """
        received_cf: List[CanPacketRecord] = []
        received_payload_size = 0
        remaining_timeout = self.n_cr_timeout
        time_start_ms = time() * 1000
        while received_payload_size < remaining_data_length and (len(received_cf) != block_size or block_size == 0):
            received_packet = self.receive_packet(timeout=remaining_timeout)
            if CanPacketType.is_initial_packet_type(received_packet.packet_type):
                warn(message="A new UDS message is transmitted. Aborted reception of previous message.",
                     category=NewMessageReceptionWarning)
                return self._message_receive_start(initial_packet=received_packet)
            if (received_packet.packet_type == CanPacketType.CONSECUTIVE_FRAME
                    and received_packet.sequence_number == sequence_number):
                received_cf.append(received_packet)
                received_payload_size += len(received_packet.payload)
                sequence_number = (received_packet.sequence_number + 1) & 0xF
                remaining_timeout = self.n_cr_timeout
                time_start_ms = time() * 1000
            else:
                warn(message="Either Consecutive Frame was missed or an unrelated CAN packet was received "
                             "during UDS message reception.",
                     category=UnexpectedPacketReceptionWarning)
                time_now_ms = time() * 1000
                remaining_timeout = (time_start_ms + self.n_cr_timeout) - time_now_ms
        return tuple(received_cf)

    async def _async_receive_cf_packets_block(self,
                                              sequence_number: int,
                                              block_size: int,
                                              remaining_data_length: int,
                                              loop: Optional[AbstractEventLoop] = None
                                              ) -> Union[UdsMessageRecord, Tuple[CanPacketRecord, ...]]:
        """
        Receive asynchronously block of :ref:`Consecutive Frames <knowledge-base-addressing-consecutive-frame>`.

        :param sequence_number: Current :ref:`Sequence Number <knowledge-base-addressing-sequence-number>`
            (next Consecutive Frame shall have this value set).
        :param block_size: :ref:`Block Size <knowledge-base-can-block-size>` value sent in the last
            :ref:`Flow Control CAN packet <knowledge-base-can-flow-control>`.
        :param remaining_data_length: Number of remaining data bytes to receive in UDS message.
        :param loop: An asyncio event loop used for observing messages.

        :return: Either:
            - Record of UDS message if reception was interrupted by a new UDS message transmission.
            - Tuple with records of received Consecutive Frames.
        """
        received_cf: List[CanPacketRecord] = []
        received_payload_size: int = 0
        remaining_timeout = self.n_cr_timeout
        time_start_ms = time() * 1000
        while received_payload_size < remaining_data_length and (len(received_cf) != block_size or block_size == 0):
            received_packet = await self.async_receive_packet(timeout=remaining_timeout, loop=loop)
            if CanPacketType.is_initial_packet_type(received_packet.packet_type):
                warn(message="A new UDS message is transmitted. Aborted reception of previous message.",
                     category=NewMessageReceptionWarning)
                return await self._async_message_receive_start(initial_packet=received_packet, loop=loop)
            if (received_packet.packet_type == CanPacketType.CONSECUTIVE_FRAME
                    and received_packet.sequence_number == sequence_number):
                received_cf.append(received_packet)
                received_payload_size += len(received_packet.payload)
                sequence_number = (received_packet.sequence_number + 1) & 0xF
                remaining_timeout = self.n_cr_timeout
                time_start_ms = time() * 1000
            else:
                warn(message="Either Consecutive Frame was missed or an unrelated CAN packet was received "
                             "during UDS message reception.",
                     category=UnexpectedPacketReceptionWarning)
                time_now_ms = time() * 1000
                remaining_timeout = (time_start_ms + self.n_cr_timeout) - time_now_ms
        return tuple(received_cf)

    def _receive_consecutive_frames(self, first_frame: CanPacketRecord) -> UdsMessageRecord:
        """
        Receive Consecutive Frames after reception of First Frame.

        :param first_frame: :ref:`First Frame <knowledge-base-addressing-first-frame>` that was received.

        :raise TimeoutError: :ref:`N_Cr <knowledge-base-addressing-n-cr>` timeout was reached.
        :raise OverflowError: Flow Control packet with :ref:`Flow Status <knowledge-base-can-flow-status>` equal to
            OVERFLOW was sent.

        :return: Record of UDS message that was formed provided First Frame and received Consecutive Frames.
        """
        packets_records: List[CanPacketRecord] = [first_frame]
        message_data_length: int = first_frame.data_length
        received_data_length: int = len(first_frame.payload)
        sequence_number: int = 1
        flow_control_iterator = iter(self.flow_control_parameters_generator)
        while True:
            try:
                received_packet = self.receive_packet(timeout=self.n_br)
            except (TimeoutError, ValueError):
                pass
            else:
                if CanPacketType.is_initial_packet_type(received_packet.packet_type):
                    warn(message="A new UDS message is transmitted. Aborted reception of previous message.",
                         category=NewMessageReceptionWarning)
                    return self._message_receive_start(initial_packet=received_packet)
                warn(message="An unrelated CAN packet was received during UDS message transmission.",
                     category=UnexpectedPacketReceptionWarning)
            flow_status, block_size, st_min = next(flow_control_iterator)
            fc_packet = self.segmenter.get_flow_control_packet(flow_status=flow_status,
                                                               block_size=block_size,
                                                               st_min=st_min)
            packets_records.append(self.send_packet(fc_packet))
            if flow_status == CanFlowStatus.Overflow:
                raise OverflowError("Flow Control with Flow Status `OVERFLOW` was transmitted.")
            if flow_status == CanFlowStatus.ContinueToSend:
                remaining_data_length = message_data_length - received_data_length
                cf_block = self._receive_cf_packets_block(sequence_number=sequence_number,
                                                          block_size=block_size,
                                                          remaining_data_length=remaining_data_length)
                if isinstance(cf_block, UdsMessageRecord):  # handle in case another message interrupted
                    return cf_block
                packets_records.extend(cf_block)
                received_data_length += len(cf_block[0].payload) * len(cf_block)
                if received_data_length >= message_data_length:
                    break
                sequence_number = (cf_block[-1].sequence_number + 1) & 0xF
        return UdsMessageRecord(packets_records)

    async def _async_receive_consecutive_frames(self,
                                                first_frame: CanPacketRecord,
                                                loop: Optional[AbstractEventLoop] = None) -> UdsMessageRecord:
        """
        Receive asynchronously Consecutive Frames after reception of First Frame.

        :param first_frame: :ref:`First Frame <knowledge-base-addressing-first-frame>` that was received.
        :param loop: An asyncio event loop used for observing messages.

        :raise TimeoutError: :ref:`N_Cr <knowledge-base-addressing-n-cr>` timeout was reached.
        :raise OverflowError: Flow Control packet with :ref:`Flow Status <knowledge-base-can-flow-status>` equal to
            OVERFLOW was sent.
        :raise NotImplementedError: Unhandled CAN packet starting a new CAN message transmission was received.

        :return: Record of UDS message that was formed provided First Frame and received Consecutive Frames.
        """
        packets_records: List[CanPacketRecord] = [first_frame]
        message_data_length: int = first_frame.data_length  # type: ignore
        received_data_length: int = len(first_frame.payload)  # type: ignore
        sequence_number: int = 1
        flow_control_iterator = iter(self.flow_control_parameters_generator)
        while True:
            try:
                received_packet = await self.async_receive_packet(timeout=self.n_br, loop=loop)
            except (TimeoutError, ValueError):
                pass
            else:
                if CanPacketType.is_initial_packet_type(received_packet.packet_type):
                    warn(message="A new UDS message is transmitted. Aborted reception of previous message.",
                         category=NewMessageReceptionWarning)
                    return await self._async_message_receive_start(initial_packet=received_packet, loop=loop)
                warn(message="An unrelated CAN packet was received during UDS message transmission.",
                     category=UnexpectedPacketReceptionWarning)
            flow_status, block_size, st_min = next(flow_control_iterator)
            fc_packet = self.segmenter.get_flow_control_packet(flow_status=flow_status,
                                                               block_size=block_size,
                                                               st_min=st_min)
            packets_records.append(await self.async_send_packet(fc_packet, loop=loop))
            if flow_status == CanFlowStatus.Overflow:
                raise OverflowError("Flow Control with Flow Status `OVERFLOW` was transmitted.")
            if flow_status == CanFlowStatus.ContinueToSend:
                remaining_data_length = message_data_length - received_data_length
                cf_block = await self._async_receive_cf_packets_block(sequence_number=sequence_number,
                                                                      block_size=block_size,  # type: ignore
                                                                      remaining_data_length=remaining_data_length,
                                                                      loop=loop)
                if isinstance(cf_block, UdsMessageRecord):  # handle in case another message interrupted
                    return cf_block
                packets_records.extend(cf_block)
                received_data_length += len(cf_block[0].payload) * len(cf_block)  # type: ignore
                if received_data_length >= message_data_length:
                    break
                sequence_number = (cf_block[-1].sequence_number + 1) & 0xF  # type: ignore
        return UdsMessageRecord(packets_records)

    def clear_frames_buffers(self) -> None:
        """
        Clear buffers with transmitted and received frames.

        .. warning:: This will cause that all CAN packets received in a past are no longer accessible.
        """
        for _ in range(self.__frames_buffer.buffer.qsize()):
            self.__frames_buffer.buffer.get_nowait()
        for _ in range(self.__async_frames_buffer.buffer.qsize()):
            self.__async_frames_buffer.buffer.get_nowait()

    @staticmethod
    def is_supported_network_manager(bus_manager: Any) -> bool:
        """
        Check whether provided value is a bus manager that is supported by this Transport Interface.

        :param bus_manager: Value to check.

        :return: True if provided bus object is compatible with this Transport Interface, False otherwise.
        """
        return isinstance(bus_manager, BusABC)

    def send_packet(self, packet: CanPacket) -> CanPacketRecord:
        """
        Transmit CAN packet.

        .. warning:: Must not be called within an asynchronous function.

        :param packet: CAN packet to send.

        :raise TypeError: Provided packet is not CAN packet.
        :raise TimeoutError: Timeout was reached before a CAN packet could be transmitted.

        :return: Record with historic information about transmitted CAN packet.
        """
        if not isinstance(packet, CanPacket):
            raise TypeError("Provided packet value does not contain a CAN packet.")
        is_flow_control_packet = packet.packet_type == CanPacketType.FLOW_CONTROL
        self.__setup_notifier()
        self.clear_frames_buffers()
        can_frame = PythonCanMessage(arbitration_id=packet.can_id,
                                     is_extended_id=CanIdHandler.is_extended_can_id(packet.can_id),
                                     data=packet.raw_frame_data,
                                     is_fd=CanDlcHandler.is_can_fd_specific_dlc(packet.dlc))
        timeout_s = (self.n_ar_timeout if is_flow_control_packet else self.n_as_timeout) / 1000.
        time_start_s = time()
        self.network_manager.send(can_frame)
        observed_frame = None
        while observed_frame is None \
                or observed_frame.arbitration_id != packet.can_id \
                or bytes(observed_frame.data) != packet.raw_frame_data \
                or not observed_frame.is_rx:
            timeout_left = timeout_s - (time() - time_start_s)
            if timeout_left <= 0:
                raise TimeoutError("Timeout was reached before observing a CAN packet being transmitted.")
            observed_frame = self.__frames_buffer.get_message(timeout=timeout_left)
        time_sent_s = time()  # Temporary solution due to https://github.com/mdabrowski1990/uds/issues/228
        if is_flow_control_packet:
            self._update_n_ar_measured((time_sent_s - time_start_s) * 1000.)
        else:
            self._update_n_as_measured((time_sent_s - time_start_s) * 1000.)
        return CanPacketRecord(frame=observed_frame,
                               direction=TransmissionDirection.TRANSMITTED,
                               addressing_type=packet.addressing_type,
                               addressing_format=packet.addressing_format,
                               transmission_time=datetime.fromtimestamp(observed_frame.timestamp))

    async def async_send_packet(self,
                                packet: CanPacket,
                                loop: Optional[AbstractEventLoop] = None) -> CanPacketRecord:
        """
        Transmit asynchronously CAN packet.

        :param packet: CAN packet to send.
        :param loop: An asyncio event loop used for observing messages.

        :raise TypeError: Provided packet is not CAN packet.
        :raise TimeoutError: Timeout was reached before a CAN packet could be transmitted.

        :return: Record with historic information about transmitted CAN packet.
        """
        if not isinstance(packet, CanPacket):
            raise TypeError("Provided packet value does not contain a CAN packet.")
        loop = get_running_loop() if loop is None else loop
        is_flow_control_packet = packet.packet_type == CanPacketType.FLOW_CONTROL
        self.__setup_async_notifier(loop)
        self.clear_frames_buffers()
        can_frame = PythonCanMessage(arbitration_id=packet.can_id,
                                     is_extended_id=CanIdHandler.is_extended_can_id(packet.can_id),
                                     data=packet.raw_frame_data,
                                     is_fd=CanDlcHandler.is_can_fd_specific_dlc(packet.dlc))
        timeout_s = (self.n_ar_timeout if is_flow_control_packet else self.n_as_timeout) / 1000.
        time_start_s = time()
        self.network_manager.send(can_frame)
        observed_frame = None
        while observed_frame is None \
                or observed_frame.arbitration_id != packet.can_id \
                or bytes(observed_frame.data) != packet.raw_frame_data \
                or not observed_frame.is_rx:
            timeout_left = timeout_s - (time() - time_start_s)
            if timeout_left <= 0:
                raise TimeoutError("Timeout was reached before a CAN packet could be transmitted.")
            observed_frame = await wait_for(self.__async_frames_buffer.get_message(), timeout=timeout_left)
        time_sent_s = time()  # Temporary solution due to https://github.com/mdabrowski1990/uds/issues/228
        if is_flow_control_packet:
            self._update_n_ar_measured((time_sent_s - time_start_s) * 1000.)
        else:
            self._update_n_as_measured((time_sent_s - time_start_s) * 1000.)
        return CanPacketRecord(frame=observed_frame,
                               direction=TransmissionDirection.TRANSMITTED,
                               addressing_type=packet.addressing_type,
                               addressing_format=packet.addressing_format,
                               transmission_time=datetime.fromtimestamp(observed_frame.timestamp))

    def receive_packet(self, timeout: Optional[TimeMillisecondsAlias] = None) -> CanPacketRecord:
        """
        Receive CAN packet.

        .. warning:: Must not be called within an asynchronous function.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TypeError: Provided timeout value is not None neither int nor float type.
        :raise ValueError: Provided timeout value is less or equal 0.
        :raise TimeoutError: Timeout was reached before a CAN packet was received.

        :return: Record with historic information about received CAN packet.
        """
        if timeout is not None:
            if not isinstance(timeout, (int, float)):
                raise TypeError("Provided timeout value is not None neither int nor float type.")
            if timeout <= 0:
                raise ValueError("Provided timeout value is less or equal 0.")
        self.__setup_notifier()
        packet_addressing_type = None
        if timeout is not None:
            time_end_ms = (time() * 1000) + timeout
        while packet_addressing_type is None:
            if timeout is not None:
                time_now_ms = time() * 1000
                if time_end_ms <= time_now_ms:
                    raise TimeoutError("Timeout was reached before a CAN packet was received.")
                timeout = time_end_ms - time_now_ms
            timeout_left = self._MAX_LISTENER_TIMEOUT if timeout is None else timeout / 1000.
            received_frame = self.__frames_buffer.get_message(timeout=timeout_left)
            if received_frame is None:
                raise TimeoutError("Timeout was reached before a CAN packet was received.")
            packet_addressing_type = self.segmenter.is_input_packet(can_id=received_frame.arbitration_id,
                                                                    raw_frame_data=received_frame.data)
        return CanPacketRecord(frame=received_frame,
                               direction=TransmissionDirection.RECEIVED,
                               addressing_type=packet_addressing_type,
                               addressing_format=self.segmenter.addressing_format,
                               transmission_time=datetime.fromtimestamp(received_frame.timestamp))

    async def async_receive_packet(self,
                                   timeout: Optional[TimeMillisecondsAlias] = None,
                                   loop: Optional[AbstractEventLoop] = None) -> CanPacketRecord:
        """
        Receive asynchronously CAN packet.

        :param timeout: Maximal time (in milliseconds) to wait.
        :param loop: An asyncio event loop used for observing messages.

        :raise TypeError: Provided timeout value is not None neither int nor float type.
        :raise ValueError: Provided timeout value is less or equal 0.
        :raise TimeoutError: Timeout was reached before a CAN packet was received.

        :return: Record with historic information about received CAN packet.
        """
        if timeout is not None:
            if not isinstance(timeout, (int, float)):
                raise TypeError("Provided timeout value is not None neither int nor float type.")
            if timeout <= 0:
                raise ValueError("Provided timeout value is less or equal 0.")
        loop = get_running_loop() if loop is None else loop
        self.__setup_async_notifier(loop)
        packet_addressing_type = None
        if timeout is not None:
            time_end_ms = (time() * 1000) + timeout
        while packet_addressing_type is None:
            if timeout is not None:
                time_now_ms = time() * 1000
                if time_end_ms <= time_now_ms:
                    raise TimeoutError("Timeout was reached before a UDS message was received.")
                timeout = time_end_ms - time_now_ms
            received_frame = await wait_for(self.__async_frames_buffer.get_message(),
                                            timeout=None if timeout is None else timeout / 1000.)
            packet_addressing_type = self.segmenter.is_input_packet(can_id=received_frame.arbitration_id,
                                                                    raw_frame_data=received_frame.data)
        return CanPacketRecord(frame=received_frame,
                               direction=TransmissionDirection.RECEIVED,
                               addressing_type=packet_addressing_type,
                               addressing_format=self.segmenter.addressing_format,
                               transmission_time=datetime.fromtimestamp(received_frame.timestamp))

    def send_message(self, message: UdsMessage) -> UdsMessageRecord:
        """
        Transmit UDS message over CAN.

        .. warning:: Must not be called within an asynchronous function.

        :param message: A message to send.

        :raise OverflowError: Flow Control packet with Flow Status equal to OVERFLOW was received.
        :raise TransmissionInterruptionError: A new UDS message transmission was started while sending this message.
        :raise NotImplementedError: Flow Control CAN packet with unknown Flow Status was received.

        :return: Record with historic information about transmitted UDS message.
        """
        packets_to_send = list(self.segmenter.segmentation(message))
        packet_records = [self.send_packet(packets_to_send.pop(0))]
        while packets_to_send:
            record = self.receive_packet(timeout=self.n_bs_timeout)
            if record.packet_type == CanPacketType.FLOW_CONTROL:
                packet_records.append(record)
                if record.flow_status == CanFlowStatus.ContinueToSend:
                    number_of_packets = len(packets_to_send) if record.block_size == 0 else record.block_size
                    delay_between_cf = self.n_cs if self.n_cs is not None else \
                        CanSTminTranslator.decode(record.st_min)  # type: ignore
                    packet_records.extend(self._send_cf_packets_block(
                        cf_packets_block=packets_to_send[:number_of_packets],
                        delay=delay_between_cf))
                    packets_to_send = packets_to_send[number_of_packets:]
                elif record.flow_status == CanFlowStatus.Wait:
                    continue
                elif record.flow_status == CanFlowStatus.Overflow:
                    raise OverflowError("Flow Control with Flow Status `OVERFLOW` was received.")
                else:
                    raise NotImplementedError(f"Unknown Flow Status received: {record.flow_status}")
            else:
                warn(message="An unrelated CAN packet was received during UDS message transmission.",
                     category=UnexpectedPacketReceptionWarning)
        message_records = UdsMessageRecord(packet_records)
        self._update_n_bs_measured(message_records)
        return message_records

    async def async_send_message(self,
                                 message: UdsMessage,
                                 loop: Optional[AbstractEventLoop] = None) -> UdsMessageRecord:
        """
        Transmit asynchronously UDS message over CAN.

        :param message: A message to send.
        :param loop: An asyncio event loop to use for scheduling this task.

        :raise OverflowError: Flow Control packet with Flow Status equal to OVERFLOW was received.
        :raise TransmissionInterruptionError: A new UDS message transmission was started while sending this message.
        :raise NotImplementedError: Flow Control CAN packet with unknown Flow Status was received.

        :return: Record with historic information about transmitted UDS message.
        """
        packets_to_send = list(self.segmenter.segmentation(message))
        packet_records = [await self.async_send_packet(packets_to_send.pop(0), loop=loop)]
        while packets_to_send:
            record = await self.async_receive_packet(timeout=self.n_bs_timeout, loop=loop)
            if record.packet_type == CanPacketType.FLOW_CONTROL:
                packet_records.append(record)
                if record.flow_status == CanFlowStatus.ContinueToSend:
                    number_of_packets = len(packets_to_send) if record.block_size == 0 else record.block_size
                    delay_between_cf = self.n_cs if self.n_cs is not None else \
                        CanSTminTranslator.decode(record.st_min)  # type: ignore
                    packet_records.extend(
                        await self._async_send_cf_packets_block(cf_packets_block=packets_to_send[:number_of_packets],
                                                                delay=delay_between_cf,
                                                                loop=loop))
                    packets_to_send = packets_to_send[number_of_packets:]
                elif record.flow_status == CanFlowStatus.Wait:
                    continue
                elif record.flow_status == CanFlowStatus.Overflow:
                    raise OverflowError("Flow Control with Flow Status `OVERFLOW` was received.")
                else:
                    raise NotImplementedError(f"Unknown Flow Status received: {record.flow_status}")
            else:
                warn(message="An unrelated CAN packet was received during UDS message transmission.",
                     category=UnexpectedPacketReceptionWarning)
        message_records = UdsMessageRecord(packet_records)
        self._update_n_bs_measured(message_records)
        return message_records

    def receive_message(self, timeout: Optional[TimeMillisecondsAlias] = None) -> UdsMessageRecord:
        """
        Receive UDS message over CAN.

        .. warning:: Must not be called within an asynchronous function.

        :param timeout: Maximal time (in milliseconds) to wait for UDS message transmission to start.
            This means that receiving might last longer if First Frame was received within provided time.

        :raise TypeError: Provided timeout value is not None neither int nor float type.
        :raise ValueError: Provided timeout value is less or equal 0.
        :raise TimeoutError: Timeout was reached.
            Either Single Frame / First Frame not received within [timeout] ms
            or N_As, N_Ar, N_Bs, N_Cr timeout reached.

        :return: Record with historic information about received UDS message.
        """
        if timeout is not None:
            if not isinstance(timeout, (int, float)):
                raise TypeError("Provided timeout value is not None neither int nor float type.")
            if timeout <= 0:
                raise ValueError("Provided timeout value is less or equal 0.")
        if timeout is not None:
            time_end_ms = (time() * 1000) + timeout
        while True:
            if timeout is not None:
                time_now_ms = time() * 1000
                if time_end_ms <= time_now_ms:
                    raise TimeoutError("Timeout was reached before a UDS message was received.")
                timeout = time_end_ms - time_now_ms
            received_packet = self.receive_packet(timeout=timeout)
            if CanPacketType.is_initial_packet_type(received_packet.packet_type):
                return self._message_receive_start(initial_packet=received_packet)
            warn(message="A CAN packet that does not start UDS message transmission was received.",
                 category=UnexpectedPacketReceptionWarning)

    async def async_receive_message(self,
                                    timeout: Optional[TimeMillisecondsAlias] = None,
                                    loop: Optional[AbstractEventLoop] = None) -> UdsMessageRecord:
        """
        Receive asynchronously UDS message over CAN.

        :param timeout: Maximal time (in milliseconds) to wait for UDS message transmission to start.
            This means that receiving might last longer if First Frame was received within provided time.
        :param loop: An asyncio event loop to use for scheduling this task.

        :raise TypeError: Provided timeout value is not None neither int nor float type.
        :raise ValueError: Provided timeout value is less or equal 0.
        :raise TimeoutError: Timeout was reached.
            Either Single Frame / First Frame not received within [timeout] ms
            or N_As, N_Ar, N_Bs, N_Cr timeout reached.

        :return: Record with historic information about received UDS message.
        """
        if timeout is not None:
            if not isinstance(timeout, (int, float)):
                raise TypeError("Provided timeout value is not None neither int nor float type.")
            if timeout <= 0:
                raise ValueError("Provided timeout value is less or equal 0.")
        if timeout is not None:
            time_end_ms = (time() * 1000) + timeout
        while True:
            if timeout is not None:
                time_now_ms = time() * 1000
                if time_end_ms <= time_now_ms:
                    raise TimeoutError("Timeout was reached before a UDS message was received.")
                timeout = time_end_ms - time_now_ms
            received_packet = await self.async_receive_packet(timeout=timeout, loop=loop)
            if CanPacketType.is_initial_packet_type(received_packet.packet_type):
                return await self._async_message_receive_start(initial_packet=received_packet, loop=loop)
            warn(message="A CAN packet that does not start UDS message transmission was received.",
                 category=UnexpectedPacketReceptionWarning)

"""Implementation of UDS Transport Interface for CAN bus using python-can as bus manager."""

__all__ = ["PyCanTransportInterface"]

from asyncio import AbstractEventLoop, get_running_loop
from asyncio import sleep as async_sleep
from asyncio import wait_for
from datetime import datetime
from time import sleep, time
from typing import Any, List, Optional, Tuple, Union
from warnings import warn

from can import AsyncBufferedReader, BufferedReader, BusABC
from can import Message as PythonCanMessage
from can import Notifier
from uds.addressing import AddressingType, TransmissionDirection
from uds.message import UdsMessage, UdsMessageRecord
from uds.utilities import NewMessageReceptionWarning, TimeMillisecondsAlias, UnexpectedPacketReceptionWarning

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
    """Maximal timeout value accepted by python-can listeners."""
    _MIN_NOTIFIER_TIMEOUT: float = 0.001  # s
    """Minimal timeout for notifiers that does not cause malfunctioning of listeners."""
    network_manager: BusABC

    def __init__(self,
                 network_manager: BusABC,
                 addressing_information: AbstractCanAddressingInformation,
                 **configuration_params: Any) -> None:
        """
        Create Transport Interface that uses python-can package to control CAN bus.

        :param network_manager: Python-can bus object for handling CAN network.
        :param addressing_information: Addressing Information configuration of a simulated node that is taking part in
            DoCAN communication.
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
        self.__notifier: Optional[Notifier] = None
        self.__async_notifier: Optional[Notifier] = None
        # listeners for receiving packets
        self.__rx_frames_buffer = BufferedReader()
        self.__async_rx_frames_buffer = AsyncBufferedReader()
        # listeners for receiving FC packets when sending messages
        self.__tx_frames_buffer = BufferedReader()
        self.__async_tx_frames_buffer = AsyncBufferedReader()

    def __del__(self) -> None:
        """Safely close all threads opened by this object."""
        self.__teardown_notifier(suppress_warning=True)
        self.__teardown_async_notifier(suppress_warning=True)
        self.__rx_frames_buffer.stop()
        self.__async_rx_frames_buffer.stop()
        self.__tx_frames_buffer.stop()
        self.__async_tx_frames_buffer.stop()

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
                                       listeners=[self.__rx_frames_buffer,
                                                  self.__tx_frames_buffer],
                                       timeout=self._MIN_NOTIFIER_TIMEOUT)

    def __setup_async_notifier(self, loop: AbstractEventLoop) -> None:
        """
        Configure CAN frame notifier for asynchronous communication.

        :param loop: An :mod:`asyncio` event loop to use.
        """
        self.__teardown_notifier()
        if self.__async_notifier is None:
            self.__async_notifier = Notifier(bus=self.network_manager,
                                             listeners=[self.__async_rx_frames_buffer,
                                                        self.__async_tx_frames_buffer],
                                             timeout=self._MIN_NOTIFIER_TIMEOUT,
                                             loop=loop)

    def _send_cf_packets_block(self,
                               cf_packets_block: List[CanPacket],
                               delay: TimeMillisecondsAlias,
                               fc_transmission_time: datetime) -> Tuple[CanPacketRecord, ...]:
        """
        Send block of Consecutive Frame CAN packets.

        :param cf_packets_block: Consecutive Frame CAN packets to send.
        :param delay: Minimal delay between sending following Consecutive Frames [ms].
        :param fc_transmission_time: Transmission time of the proceeding Flow Control packet.

        :return: Records with historic information about transmitted Consecutive Frame CAN packets.
        """
        packet_records = []
        time_end_s = fc_transmission_time.timestamp() + delay / 1000.
        for cf_packet in cf_packets_block:
            time_to_wait = time_end_s - time()
            if time_to_wait > 0:
                sleep(time_to_wait)
            cf_packet_record = self.send_packet(cf_packet)
            time_end_s = cf_packet_record.transmission_time.timestamp() + delay / 1000.
            packet_records.append(cf_packet_record)
        return tuple(packet_records)

    async def _async_send_cf_packets_block(self,
                                           cf_packets_block: List[CanPacket],
                                           delay: TimeMillisecondsAlias,
                                           fc_transmission_time: datetime,
                                           loop: AbstractEventLoop) -> Tuple[CanPacketRecord, ...]:
        """
        Send block of Consecutive Frame CAN packets asynchronously.

        :param cf_packets_block: Consecutive Frame CAN packets to send.
        :param delay: Minimal delay between sending following Consecutive Frames [ms].
        :param fc_transmission_time: Transmission time of the proceeding Flow Control packet.
        :param loop: An asyncio event loop to use for scheduling this task.

        :return: Records with historic information about transmitted Consecutive Frame CAN packets.
        """
        packet_records = []
        time_end_s = fc_transmission_time.timestamp() + delay / 1000.
        for cf_packet in cf_packets_block:
            time_to_wait = time_end_s - time()
            if time_to_wait > 0:
                await async_sleep(time_end_s - time())
            cf_packet_record = await self.async_send_packet(cf_packet, loop=loop)
            time_end_s = cf_packet_record.transmission_time.timestamp() + delay / 1000.
            packet_records.append(cf_packet_record)
        return tuple(packet_records)

    def _wait_for_flow_control(self, last_packet_transmission_time: datetime) -> CanPacketRecord:
        """
        Wait till Flow Control CAN Packet is received.

        :param last_packet_transmission_time: Moment of time when the last CAN Packet was transmitted.

        :return: Record with historic information about received Flow Control CAN packet.
        """
        packet_record = None
        time_end_s = last_packet_transmission_time.timestamp() + self.n_bs_timeout / 1000.
        while (packet_record is None
               or packet_record.addressing_type != AddressingType.PHYSICAL
               or packet_record.packet_type != CanPacketType.FLOW_CONTROL):
            remaining_time_ms = (time_end_s - time()) * 1000.
            packet_record = self._wait_for_packet(buffer=self.__tx_frames_buffer, timeout=remaining_time_ms)
        return packet_record

    async def _async_wait_for_flow_control(self, last_packet_transmission_time: datetime) -> CanPacketRecord:
        """
        Wait till Flow Control CAN Packet is received.

        :param last_packet_transmission_time: Moment of time when the last CAN Packet was transmitted.

        :return: Record with historic information about received Flow Control CAN packet.
        """
        packet_record = None
        time_end_s = last_packet_transmission_time.timestamp() + self.n_bs_timeout / 1000.
        while (packet_record is None
               or packet_record.addressing_type != AddressingType.PHYSICAL
               or packet_record.packet_type != CanPacketType.FLOW_CONTROL):
            remaining_time_ms = (time_end_s - time()) * 1000.
            packet_record = await self._async_wait_for_packet(buffer=self.__async_tx_frames_buffer,
                                                              timeout=remaining_time_ms)
        return packet_record

    def _wait_for_packet(self,
                         buffer: BufferedReader,
                         timeout: Optional[TimeMillisecondsAlias] = None) -> CanPacketRecord:
        """
        Wait till CAN Packet is received.

        :param buffer: Listener to which CAN Packet would be delivered.
        :param timeout: Maximal time (in milliseconds) to wait.
            Leave None to wait forever.

        :raise TimeoutError: Timeout was reached before a CAN packet arrived.

        :return: Record with historic information about received CAN packet.
        """
        packet_addressing_type = None
        if timeout is not None:
            time_end_ms = (time() * 1000.) + timeout
        while packet_addressing_type is None:
            if timeout is not None:
                time_now_ms = time() * 1000.
                if time_end_ms <= time_now_ms:
                    raise TimeoutError("Timeout was reached before a CAN packet was received.")
                timeout = time_end_ms - time_now_ms
            timeout_left_s = self._MAX_LISTENER_TIMEOUT if timeout is None else timeout / 1000.
            received_frame = buffer.get_message(timeout=timeout_left_s)
            if received_frame is None:
                raise TimeoutError("Timeout was reached before a CAN packet was received.")
            packet_addressing_type = self.addressing_information.is_input_packet(
                can_id=received_frame.arbitration_id, raw_frame_data=received_frame.data)
        return CanPacketRecord(frame=received_frame,  # type: ignore
                               direction=TransmissionDirection.RECEIVED,
                               addressing_type=packet_addressing_type,
                               addressing_format=self.segmenter.addressing_format,
                               transmission_time=datetime.fromtimestamp(received_frame.timestamp))  # type: ignore

    async def _async_wait_for_packet(self,
                                     buffer: AsyncBufferedReader,
                                     timeout: Optional[TimeMillisecondsAlias] = None) -> CanPacketRecord:
        """
        Wait till CAN Packet is received.

        :param buffer: Listener to which CAN Packet would be delivered.
        :param timeout: Maximal time (in milliseconds) to wait.
            Leave None to wait forever.

        :raise TimeoutError: Timeout was reached before a CAN packet arrived.

        :return: Record with historic information about received CAN packet.
        """
        packet_addressing_type = None
        if timeout is not None:
            time_end_ms = (time() * 1000.) + timeout
        while packet_addressing_type is None:
            if timeout is not None:
                time_now_ms = time() * 1000.
                if time_end_ms <= time_now_ms:
                    raise TimeoutError("Timeout was reached before a CAN packet was received.")
                timeout = time_end_ms - time_now_ms
            timeout_left_s = None if timeout is None else timeout / 1000.
            received_frame = await wait_for(buffer.get_message(), timeout=timeout_left_s)
            packet_addressing_type = self.addressing_information.is_input_packet(
                can_id=received_frame.arbitration_id, raw_frame_data=received_frame.data)
        return CanPacketRecord(frame=received_frame,
                               direction=TransmissionDirection.RECEIVED,
                               addressing_type=packet_addressing_type,
                               addressing_format=self.segmenter.addressing_format,
                               transmission_time=datetime.fromtimestamp(received_frame.timestamp))

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
        time_start_ms = time() * 1000.
        while received_payload_size < remaining_data_length and (len(received_cf) != block_size or block_size == 0):
            received_packet = self.receive_packet(timeout=remaining_timeout)
            if CanPacketType.is_initial_packet_type(received_packet.packet_type):
                warn(message="A new DoCAN message transmission was started. "
                             "Reception of the previous message was aborted.",
                     category=NewMessageReceptionWarning)
                return self._message_receive_start(initial_packet=received_packet)
            if (received_packet.packet_type == CanPacketType.CONSECUTIVE_FRAME
                    and received_packet.sequence_number == sequence_number):
                received_cf.append(received_packet)
                received_payload_size += len(received_packet.payload)  # type: ignore
                sequence_number = (received_packet.sequence_number + 1) & 0xF
                remaining_timeout = self.n_cr_timeout
                time_start_ms = time() * 1000.
            else:
                time_now_ms = time() * 1000.
                remaining_timeout = (time_start_ms + self.n_cr_timeout) - time_now_ms
        return tuple(received_cf)

    async def _async_receive_cf_packets_block(self,
                                              sequence_number: int,
                                              block_size: int,
                                              remaining_data_length: int,
                                              loop: Optional[AbstractEventLoop] = None
                                              ) -> Union[UdsMessageRecord, Tuple[CanPacketRecord, ...]]:
        """
        Receive asynchronously block of :ref:`Consecutive Frames <knowledge-base-can-consecutive-frame>`.

        :param sequence_number: Current :ref:`Sequence Number <knowledge-base-can-sequence-number>`
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
        time_start_ms = time() * 1000.
        while received_payload_size < remaining_data_length and (len(received_cf) != block_size or block_size == 0):
            received_packet = await self.async_receive_packet(timeout=remaining_timeout, loop=loop)
            if CanPacketType.is_initial_packet_type(received_packet.packet_type):
                warn(message="A new DoCAN message transmission was started. "
                             "Reception of the previous message was aborted.",
                     category=NewMessageReceptionWarning)
                return await self._async_message_receive_start(initial_packet=received_packet, loop=loop)
            if (received_packet.packet_type == CanPacketType.CONSECUTIVE_FRAME
                    and received_packet.sequence_number == sequence_number):
                received_cf.append(received_packet)
                received_payload_size += len(received_packet.payload)  # type: ignore
                sequence_number = (received_packet.sequence_number + 1) & 0xF
                remaining_timeout = self.n_cr_timeout
                time_start_ms = time() * 1000.
            else:
                time_now_ms = time() * 1000.
                remaining_timeout = (time_start_ms + self.n_cr_timeout) - time_now_ms
        return tuple(received_cf)

    def _receive_consecutive_frames(self, first_frame: CanPacketRecord) -> UdsMessageRecord:
        """
        Receive Consecutive Frames after reception of First Frame.

        :param first_frame: :ref:`First Frame <knowledge-base-can-first-frame>` that was received.

        :raise TimeoutError: :ref:`N_Cr <knowledge-base-can-n-cr>` timeout was reached.
        :raise OverflowError: Flow Control packet with :ref:`Flow Status <knowledge-base-can-flow-status>` equal to
            OVERFLOW was sent.

        :return: Record of UDS message that was formed provided First Frame and received Consecutive Frames.
        """
        packets_records: List[CanPacketRecord] = [first_frame]
        message_data_length: int = first_frame.data_length  # type: ignore
        received_data_length: int = len(first_frame.payload)  # type: ignore
        sequence_number: int = 1
        flow_control_iterator = iter(self.flow_control_parameters_generator)
        while True:
            try:
                received_packet = self.receive_packet(timeout=self.n_br)
            except (TimeoutError, ValueError):
                pass
            else:
                if CanPacketType.is_initial_packet_type(received_packet.packet_type):
                    warn(message="A new DoCAN message transmission was started. "
                                 "Reception of the previous message was aborted.",
                         category=NewMessageReceptionWarning)
                    return self._message_receive_start(initial_packet=received_packet)
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
                                                          block_size=block_size,  # type: ignore
                                                          remaining_data_length=remaining_data_length)
                if isinstance(cf_block, UdsMessageRecord):  # handle in case another message interrupted
                    return cf_block
                packets_records.extend(cf_block)
                received_data_length += len(cf_block[0].payload) * len(cf_block)  # type: ignore
                if received_data_length >= message_data_length:
                    break
                sequence_number = (cf_block[-1].sequence_number + 1) & 0xF  # type: ignore
        return UdsMessageRecord(packets_records)

    async def _async_receive_consecutive_frames(self,
                                                first_frame: CanPacketRecord,
                                                loop: Optional[AbstractEventLoop] = None) -> UdsMessageRecord:
        """
        Receive asynchronously Consecutive Frames after reception of First Frame.

        :param first_frame: :ref:`First Frame <knowledge-base-can-first-frame>` that was received.
        :param loop: An asyncio event loop used for observing messages.

        :raise TimeoutError: :ref:`N_Cr <knowledge-base-can-n-cr>` timeout was reached.
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
                    warn(message="A new DoCAN message transmission was started. "
                                 "Reception of the previous message was aborted.",
                         category=NewMessageReceptionWarning)
                    return await self._async_message_receive_start(initial_packet=received_packet, loop=loop)
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
        raise NotImplementedError(f"CAN packet of unhandled type was received: {initial_packet.packet_type}")

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
        raise NotImplementedError(f"CAN packet of unhandled type was received: {initial_packet.packet_type}")

    def clear_rx_frames_buffers(self) -> None:
        """
        Clear buffers used for storing received CAN frames.

        .. warning:: This will cause that all CAN packets received in a past are no longer accessible.
        """
        for _ in range(self.__rx_frames_buffer.buffer.qsize()):
            self.__rx_frames_buffer.buffer.get_nowait()
        for _ in range(self.__async_rx_frames_buffer.buffer.qsize()):
            self.__async_rx_frames_buffer.buffer.get_nowait()

    def clear_tx_frames_buffers(self) -> None:
        """Clear buffers used for storing transmitted CAN frames."""
        for _ in range(self.__tx_frames_buffer.buffer.qsize()):
            self.__tx_frames_buffer.buffer.get_nowait()
        for _ in range(self.__async_tx_frames_buffer.buffer.qsize()):
            self.__async_tx_frames_buffer.buffer.get_nowait()

    @staticmethod
    def is_supported_network_manager(bus_manager: Any) -> bool:
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

        :raise TypeError: Provided packet is not CAN packet.

        :return: Record with historic information about transmitted CAN packet.
        """
        if not isinstance(packet, CanPacket):
            raise TypeError(f"Provided value is not an instance of CanPacket class. Actual type: {type(packet)}.")
        is_flow_control_packet = packet.packet_type == CanPacketType.FLOW_CONTROL
        timeout_ms = self.n_ar_timeout if is_flow_control_packet else self.n_as_timeout
        can_frame = PythonCanMessage(arbitration_id=packet.can_id,
                                     is_extended_id=CanIdHandler.is_extended_can_id(packet.can_id),
                                     data=packet.raw_frame_data,
                                     is_fd=CanDlcHandler.is_can_fd_specific_dlc(packet.dlc),
                                     is_rx=False,
                                     is_error_frame=False,
                                     is_remote_frame=False)
        time_start_s = time()
        self.network_manager.send(msg=can_frame, timeout=timeout_ms / 1000.)
        time_sent_s = time()
        sent_frame = PythonCanMessage(arbitration_id=can_frame.arbitration_id,
                                      is_extended_id=can_frame.is_extended_id,
                                      data=can_frame.data,
                                      is_fd=can_frame.is_fd,
                                      is_rx=False,
                                      is_error_frame=False,
                                      is_remote_frame=False,
                                      timestamp=time_sent_s)
        transmission_time = datetime.fromtimestamp(sent_frame.timestamp)
        if is_flow_control_packet:
            self._update_n_ar_measured((time_sent_s - time_start_s) * 1000.)
        else:
            self._update_n_as_measured((time_sent_s - time_start_s) * 1000.)
        return CanPacketRecord(frame=sent_frame,
                               direction=TransmissionDirection.TRANSMITTED,
                               addressing_type=packet.addressing_type,
                               addressing_format=packet.addressing_format,
                               transmission_time=transmission_time)

    async def async_send_packet(self,
                                packet: CanPacket,  # type: ignore
                                loop: Optional[AbstractEventLoop] = None) -> CanPacketRecord:
        """
        Transmit asynchronously CAN packet.

        :param packet: CAN packet to send.
        :param loop: An asyncio event loop used for observing messages.

        :return: Record with historic information about transmitted CAN packet.
        """
        return self.send_packet(packet=packet)

    def receive_packet(self, timeout: Optional[TimeMillisecondsAlias] = None) -> CanPacketRecord:
        """
        Receive CAN packet.

        .. warning:: Must not be called within an asynchronous function.

        :param timeout: Maximal time (in milliseconds) to wait.
            Leave None to wait forever.

        :raise TypeError: Timeout value must be None, int or float type.
        :raise ValueError: Provided timeout value is less or equal to 0.

        :return: Record with historic information about received CAN packet.
        """
        if timeout is not None:
            if not isinstance(timeout, (int, float)):
                raise TypeError("Timeout value must be None, int or float type.")
            if timeout <= 0:
                raise ValueError(f"Provided timeout value is less or equal to 0. Actual value: {timeout}")
        self.__setup_notifier()
        return self._wait_for_packet(buffer=self.__rx_frames_buffer, timeout=timeout)

    async def async_receive_packet(self,
                                   timeout: Optional[TimeMillisecondsAlias] = None,
                                   loop: Optional[AbstractEventLoop] = None) -> CanPacketRecord:
        """
        Receive asynchronously CAN packet.

        :param timeout: Maximal time (in milliseconds) to wait.
            Leave None to wait forever.
        :param loop: An asyncio event loop used for observing messages.

        :raise TypeError: Timeout value must be None, int or float type.
        :raise ValueError: Provided timeout value is less or equal to 0.

        :return: Record with historic information about received CAN packet.
        """
        if timeout is not None:
            if not isinstance(timeout, (int, float)):
                raise TypeError("Timeout value must be None, int or float type.")
            if timeout <= 0:
                raise ValueError(f"Provided timeout value is less or equal to 0. Actual value: {timeout}")
        if isinstance(loop, AbstractEventLoop):
            self.__setup_async_notifier(loop=loop)
        else:
            self.__setup_async_notifier(loop=get_running_loop())
        return await self._async_wait_for_packet(buffer=self.__async_rx_frames_buffer, timeout=timeout)

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
        self.__setup_notifier()
        self.clear_tx_frames_buffers()
        packets_to_send = list(self.segmenter.segmentation(message))
        packet_records = [self.send_packet(packets_to_send.pop(0))]
        while packets_to_send:
            flow_control_record = self._wait_for_flow_control(
                last_packet_transmission_time=packet_records[-1].transmission_time)
            packet_records.append(flow_control_record)
            if flow_control_record.flow_status == CanFlowStatus.ContinueToSend:
                cf_number_to_send = len(packets_to_send) if flow_control_record.block_size == 0 \
                    else flow_control_record.block_size
                delay_between_cf = self.n_cs if self.n_cs is not None \
                    else CanSTminTranslator.decode(flow_control_record.st_min)  # type: ignore
                packet_records.extend(
                    self._send_cf_packets_block(
                        cf_packets_block=packets_to_send[:cf_number_to_send],
                        delay=delay_between_cf,
                        fc_transmission_time=flow_control_record.transmission_time))
                packets_to_send = packets_to_send[cf_number_to_send:]
            elif flow_control_record.flow_status == CanFlowStatus.Wait:
                continue
            elif flow_control_record.flow_status == CanFlowStatus.Overflow:
                raise OverflowError("Flow Control with Flow Status `OVERFLOW` was received.")
            else:
                raise NotImplementedError(f"Unknown Flow Status received: {flow_control_record.flow_status}")
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
        loop = loop if isinstance(loop, AbstractEventLoop) else get_running_loop()
        self.__setup_async_notifier(loop)
        self.clear_tx_frames_buffers()
        packets_to_send = list(self.segmenter.segmentation(message))
        packet_records = [await self.async_send_packet(packets_to_send.pop(0), loop=loop)]
        while packets_to_send:
            flow_control_record = await self._async_wait_for_flow_control(
                last_packet_transmission_time=packet_records[-1].transmission_time)
            packet_records.append(flow_control_record)
            if flow_control_record.flow_status == CanFlowStatus.ContinueToSend:
                cf_number_to_send = len(packets_to_send) if flow_control_record.block_size == 0 \
                    else flow_control_record.block_size
                delay_between_cf = self.n_cs if self.n_cs is not None \
                    else CanSTminTranslator.decode(flow_control_record.st_min)  # type: ignore
                packet_records.extend(
                    await self._async_send_cf_packets_block(cf_packets_block=packets_to_send[:cf_number_to_send],
                                                            delay=delay_between_cf,
                                                            fc_transmission_time=flow_control_record.transmission_time,
                                                            loop=loop))
                packets_to_send = packets_to_send[cf_number_to_send:]
            elif flow_control_record.flow_status == CanFlowStatus.Wait:
                continue
            elif flow_control_record.flow_status == CanFlowStatus.Overflow:
                raise OverflowError("Flow Control with Flow Status `OVERFLOW` was received.")
            else:
                raise NotImplementedError(f"Unknown Flow Status received: {flow_control_record.flow_status}")
        message_records = UdsMessageRecord(packet_records)
        self._update_n_bs_measured(message_records)
        return message_records

    def receive_message(self, timeout: Optional[TimeMillisecondsAlias] = None) -> UdsMessageRecord:
        """
        Receive UDS message over CAN.

        .. warning:: Must not be called within an asynchronous function.

        :param timeout: Maximal time (in milliseconds) to wait for UDS message transmission to start.
            This means that receiving might last longer if First Frame was received within provided time.
            Leave None to wait forever.

        :raise TypeError: Timeout value must be None, int or float type.
        :raise ValueError: Provided timeout value is less or equal to 0.
        :raise TimeoutError: Timeout was reached.
            Either Single Frame / First Frame not received within [timeout] ms
            or N_As, N_Ar, N_Bs, N_Cr timeout reached.

        :return: Record with historic information about received UDS message.
        """
        if timeout is not None:
            if not isinstance(timeout, (int, float)):
                raise TypeError("Timeout value must be None, int or float type.")
            if timeout <= 0:
                raise ValueError(f"Provided timeout value is less or equal to 0. Actual value: {timeout}")
        if timeout is not None:
            time_end_ms = (time() * 1000.) + timeout
        self.__setup_notifier()
        while True:
            if timeout is not None:
                time_now_ms = time() * 1000.
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
            Leave None to wait forever.
        :param loop: An asyncio event loop to use for scheduling this task.

        :raise TypeError: Timeout value must be None, int or float type.
        :raise ValueError: Provided timeout value is less or equal to 0.
        :raise TimeoutError: Timeout was reached.
            Either Single Frame / First Frame not received within [timeout] ms
            or N_As, N_Ar, N_Bs, N_Cr timeout reached.

        :return: Record with historic information about received UDS message.
        """
        if timeout is not None:
            if not isinstance(timeout, (int, float)):
                raise TypeError("Timeout value must be None, int or float type.")
            if timeout <= 0:
                raise ValueError(f"Provided timeout value is less or equal to 0. Actual value: {timeout}")
        if timeout is not None:
            time_end_ms = (time() * 1000.) + timeout
        loop = get_running_loop() if loop is None else loop
        self.__setup_async_notifier(loop=loop)
        while True:
            if timeout is not None:
                time_now_ms = time() * 1000.
                if time_end_ms <= time_now_ms:
                    raise TimeoutError("Timeout was reached before a UDS message was received.")
                timeout = time_end_ms - time_now_ms
            received_packet = await self.async_receive_packet(timeout=timeout, loop=loop)
            if CanPacketType.is_initial_packet_type(received_packet.packet_type):
                return await self._async_message_receive_start(initial_packet=received_packet, loop=loop)
            warn(message="A CAN packet that does not start UDS message transmission was received.",
                 category=UnexpectedPacketReceptionWarning)

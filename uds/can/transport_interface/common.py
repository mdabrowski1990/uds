"""Definition of UDS Transport Interface for CAN bus."""

__all__ = ["AbstractCanTransportInterface"]

from abc import ABC, abstractmethod
from asyncio import AbstractEventLoop, get_running_loop
from asyncio import sleep as async_sleep
from asyncio.exceptions import TimeoutError as AsyncioTimeoutError
from time import perf_counter, sleep
from typing import Any
from warnings import warn

from uds.addressing import TransmissionDirection
from uds.message import UdsMessage, UdsMessageRecord
from uds.transport_interface import AbstractTransportInterface
from uds.utilities import (
    MessageTransmissionNotStartedError,
    NewMessageReceptionWarning,
    TimeMillisecondsAlias,
    TimestampAlias,
    UnexpectedPacketReceptionWarning,
    ValueWarning,
    validate_time,
    validate_timeout,
)

from ..addressing import AbstractCanAddressingInformation
from ..frame import CanVersion
from ..packet import (
    AbstractFlowControlParametersGenerator,
    CanFlowStatus,
    CanPacket,
    CanPacketRecord,
    CanPacketType,
    CanSTminTranslator,
    DefaultFlowControlParametersGenerator,
)
from ..segmenter import CanSegmenter


class AbstractCanTransportInterface(AbstractTransportInterface, ABC):
    """
    Abstract definition of Transport Interface for managing Diagnostics on CAN.

    CAN Transport Interfaces are meant to handle UDS middle layers (Transport and Network) on CAN bus.
    """

    N_AS_TIMEOUT: TimeMillisecondsAlias = 1000
    """Timeout value of :ref:`N_As <knowledge-base-can-n-as>` time parameter according to ISO 15765-2."""
    N_AR_TIMEOUT: TimeMillisecondsAlias = 1000
    """Timeout value of :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter according to ISO 15765-2."""
    N_BS_TIMEOUT: TimeMillisecondsAlias = 1000
    """Timeout value of :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter according to ISO 15765-2."""
    N_CR_TIMEOUT: TimeMillisecondsAlias = 1000
    """Timeout value of :ref:`N_Cr <knowledge-base-can-n-cr>` time parameter according to ISO 15765-2."""
    DEFAULT_N_BR: TimeMillisecondsAlias = 0
    """Default value for :ref:`N_Br <knowledge-base-can-n-br>` time parameter."""
    DEFAULT_N_CS: TimeMillisecondsAlias | None = None
    """Default value for :ref:`N_Cs <knowledge-base-can-n-cs>` time parameter."""
    DEFAULT_FLOW_CONTROL_PARAMETERS = DefaultFlowControlParametersGenerator()
    """Default values generator for :ref:`Flow Control <knowledge-base-can-flow-control>` parameters
    (:ref:`Flow Status <knowledge-base-can-flow-status>`,
    :ref:`Block Size <knowledge-base-can-block-size>`,
    :ref:`Separation Time minimum <knowledge-base-can-st-min>`)."""

    addressing_information: AbstractCanAddressingInformation

    def __init__(self,
                 network_manager: Any,
                 addressing_information: AbstractCanAddressingInformation,
                 n_as_timeout: TimeMillisecondsAlias = N_AS_TIMEOUT,
                 n_ar_timeout: TimeMillisecondsAlias = N_AR_TIMEOUT,
                 n_bs_timeout: TimeMillisecondsAlias = N_BS_TIMEOUT,
                 n_cr_timeout: TimeMillisecondsAlias = N_CR_TIMEOUT,
                 n_br: TimeMillisecondsAlias = DEFAULT_N_BR,
                 n_cs: TimeMillisecondsAlias | None = DEFAULT_N_CS,
                 flow_control_parameters_generator: AbstractFlowControlParametersGenerator
                 = DEFAULT_FLOW_CONTROL_PARAMETERS,
                 can_version: CanVersion = CanVersion.CLASSIC_CAN,
                 bitrate_switch: bool = False,
                 **segmenter_configuration: Any) -> None:
        """
        Create Transport Interface (an object for handling UDS Transport and Network layers).

        :param network_manager: An object that handles CAN bus (Physical and Data layers of OSI Model).
        :param addressing_information: Addressing Information configuration of a simulated node that is taking part in
            DoCAN communication.
        :param n_as_timeout: Timeout value for :ref:`N_As <knowledge-base-can-n-as>` time parameter.
        :param n_ar_timeout: Timeout value for :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter.
        :param n_bs_timeout: Timeout value for :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter.
        :param n_cr_timeout: Timeout value for :ref:`N_Cr <knowledge-base-can-n-cr>` time parameter.
        :param n_br: Value of :ref:`N_Br <knowledge-base-can-n-br>` time parameter to use in communication.
        :param n_cs: Value of :ref:`N_Cs <knowledge-base-can-n-cs>` time parameter to use in communication.
        :param flow_control_parameters_generator: Generator with Flow Control parameters to use.
        :param can_version: Version of CAN protocol to be used for packets sending.
        :param bitrate_switch: Whether bitrate switch (BRS) shall be set in sent packets.
        :param segmenter_configuration: Configuration parameters for CAN Segmenter.

            - :parameter dlc: Base CAN DLC value to use for CAN packets.
            - :parameter min_dlc: Minimal CAN DLC to use for CAN Packets during Data Optimization.
            - :parameter use_data_optimization: Information whether to use
                :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>`.
            - :parameter filler_byte: Filler byte value to use for
                :ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>`.
        """
        super().__init__(network_manager=network_manager)
        self.__n_ar_measured: TimeMillisecondsAlias | None = None
        self.__n_as_measured: TimeMillisecondsAlias | None = None
        self.__n_bs_measured: tuple[TimeMillisecondsAlias, ...] | None = None
        self.__n_cr_measured: tuple[TimeMillisecondsAlias, ...] | None = None
        self.n_as_timeout = n_as_timeout
        self.n_ar_timeout = n_ar_timeout
        self.n_bs_timeout = n_bs_timeout
        self.n_cr_timeout = n_cr_timeout
        self.n_br = n_br
        self.n_cs = n_cs
        self.flow_control_parameters_generator = flow_control_parameters_generator
        self.segmenter = CanSegmenter(addressing_information=addressing_information, **segmenter_configuration)
        self.can_version = can_version
        self.bitrate_switch = bitrate_switch

    # General

    @property
    def segmenter(self) -> CanSegmenter:
        """Get the segmenter used by this CAN Transport Interface."""
        return self.__segmenter

    @segmenter.setter
    def segmenter(self, value: CanSegmenter) -> None:
        """
        Set segmenter value for this Transport Interface.

        :param value: CAN Segmenter value to set.

        :raise TypeError: Provided value is not CAN Segmenter.
        """
        if not isinstance(value, CanSegmenter):
            raise TypeError(f"Provided value is not CAN Segmenter type. Actual type: {type(value)}.")
        self.__segmenter = value

    # Communication parameters

    @property
    def can_version(self) -> CanVersion:
        """Get version of CAN protocol to be used for packets sending."""
        return self.__can_version

    @can_version.setter
    def can_version(self, value: CanVersion) -> None:
        """
        Set version of CAN protocol to be used for packets sending.

        .. warning:: Value cross-check with other attributes (e.g. DLC) is not performed.

        .. note:: Frames with DLC > 8 will always be sent as CAN FD, regardless of this value,
            as Classic CAN cannot support DLC values greater than 8.

        :param value: Value to set.
        """
        self.__can_version = CanVersion.validate_member(value)

    @property
    def bitrate_switch(self) -> bool:
        """Get value of bitrate switch (BRS) to be used for packets sending."""
        return self.__bitrate_switch

    @bitrate_switch.setter
    def bitrate_switch(self, value: bool) -> None:
        """
        Set value of bitrate switch (BRS) to be used for packets sending.

        .. note:: This value will be ignored if CLASSICAL CAN is used.

        :param value: Value to set.
        """
        self.__bitrate_switch = bool(value)

    @property
    def dlc(self) -> int:
        """
        Value of base CAN DLC to use for output CAN packets.

        .. note:: All output CAN packets will have this DLC value set unless
            :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>` is used.
        """
        return self.segmenter.dlc

    @dlc.setter
    def dlc(self, value: int) -> None:
        """
        Set value of base CAN DLC to use for output CAN packets.

        :param value: Value to set.
        """
        self.segmenter.dlc = value

    @property
    def min_dlc(self) -> int | None:
        """
        Value of minimal CAN DLC to use for CAN Packets during Data Optimization.

        .. note:: Output CAN Packets (created by :meth:`~uds.segmentation.can_segmenter.CanSegmenter.segmentation`)
            will never have DLC smaller than this value even if
            :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>` is used.
        """
        return self.segmenter.min_dlc

    @min_dlc.setter
    def min_dlc(self, value: int | None) -> None:
        """
        Set value of minimal CAN DLC to use for CAN Packets during Data Optimization.

        :param value: Value to set.
        """
        self.segmenter.min_dlc = value

    @property
    def use_data_optimization(self) -> bool:
        """
        Information whether to use CAN Frame Data Optimization during CAN packets creation.

        .. seealso::
            :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>`
        """
        return self.segmenter.use_data_optimization

    @use_data_optimization.setter
    def use_data_optimization(self, value: bool) -> None:
        """
        Set whether to use CAN Frame Data Optimization during CAN packets creation.

        .. seealso::
            :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>`

        :param value: Value to set.
        """
        self.segmenter.use_data_optimization = value

    @property
    def filler_byte(self) -> int:
        """
        Filler byte value to use for output CAN Frame Data Padding during segmentation.

        .. seealso::
            :ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>`
        """
        return self.segmenter.filler_byte

    @filler_byte.setter
    def filler_byte(self, value: int) -> None:
        """
        Set value of filler byte to use for output CAN Frame Data Padding.

        .. seealso::
            :ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>`

        :param value: Value to set.
        """
        self.segmenter.filler_byte = value

    @property
    def flow_control_parameters_generator(self) -> AbstractFlowControlParametersGenerator:
        """Get generator of Flow Control parameters (Flow Status, Block Size, Separation Time minimum)."""
        return self.__flow_control_parameters_generator

    @flow_control_parameters_generator.setter
    def flow_control_parameters_generator(self, value: AbstractFlowControlParametersGenerator) -> None:
        """
        Set value of Flow Control parameters (Flow Status, Block Size, Separation Time minimum) generator.

        :param value: Value to set.
        """
        if not isinstance(value, AbstractFlowControlParametersGenerator):
            raise TypeError("Provided Flow Control parameters generator value has incorrect type. "
                            f"Actual type: {type(value)}.")
        self.__flow_control_parameters_generator = value

    # Time parameter - CAN Network Layer

    @property
    def n_as_timeout(self) -> TimeMillisecondsAlias:
        """Timeout value for :ref:`N_As <knowledge-base-can-n-as>` time parameter."""
        return self.__n_as_timeout

    @n_as_timeout.setter
    def n_as_timeout(self, value: TimeMillisecondsAlias) -> None:
        """
        Set timeout value for :ref:`N_As <knowledge-base-can-n-as>` time parameter.

        :param value: Value of timeout to set.
        """
        validate_time(value, accept_zero=False)
        if value != self.N_AS_TIMEOUT:
            warn(message="Non-default value of N_As timeout was set.",
                 category=ValueWarning)
        self.__n_as_timeout = value

    @property
    def n_as_measured(self) -> TimeMillisecondsAlias | None:
        """
        Get the last measured value of :ref:`N_As <knowledge-base-can-n-as>` time parameter.

        .. note:: The last measurement comes from the last transmission of Single Frame or First Fame CAN Packet using
            either :meth:`~uds.can.transport_interface.common.AbstractCanTransportInterface.send_packet`
            or :meth:`~uds.can.transport_interface.common.AbstractCanTransportInterface.async_send_packet` method.

        :return: Time in milliseconds or None if the value was never measured.
        """
        return self.__n_as_measured

    @property
    def n_ar_timeout(self) -> TimeMillisecondsAlias:
        """Timeout value for :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter."""
        return self.__n_ar_timeout

    @n_ar_timeout.setter
    def n_ar_timeout(self, value: TimeMillisecondsAlias) -> None:
        """
        Set timeout value for :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter.

        :param value: Value of timeout to set.
        """
        validate_time(value, accept_zero=False)
        if value != self.N_AR_TIMEOUT:
            warn(message="Non-default value of N_Ar timeout was set.",
                 category=ValueWarning)
        self.__n_ar_timeout = value

    @property
    def n_ar_measured(self) -> TimeMillisecondsAlias | None:
        """
        Get the last measured value of :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter.

        .. note:: The last measurement comes from the last transmission of Flow Control CAN Packet using either
            :meth:`~uds.can.transport_interface.common.AbstractCanTransportInterface.receive_packet` or
            :meth:`~uds.can.transport_interface.common.AbstractCanTransportInterface.async_receive_packet` method.

        :return: Time in milliseconds or None if the value was never measured.
        """
        return self.__n_ar_measured

    @property
    def n_bs_timeout(self) -> TimeMillisecondsAlias:
        """Timeout value for :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter."""
        return self.__n_bs_timeout

    @n_bs_timeout.setter
    def n_bs_timeout(self, value: TimeMillisecondsAlias) -> None:
        """
        Set timeout value for :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter.

        :param value: Value of timeout to set.
        """
        validate_time(value, accept_zero=False)
        if value != self.N_BS_TIMEOUT:
            warn(message="Non-default value of N_Bs timeout was set.",
                 category=ValueWarning)
        self.__n_bs_timeout = value

    @property
    def n_bs_measured(self) -> tuple[TimeMillisecondsAlias, ...] | None:
        """
        Get the last measured values of :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter.

        .. note:: The last measurement comes from the last transmission of UDS message using either
            :meth:`~uds.transport_interface.addressing.AbstractCanTransportInterface.send_message` or
            :meth:`~uds.transport_interface.addressing.AbstractCanTransportInterface.async_send_message` method.

        :return: Tuple with times in milliseconds or None if the values could not be measured.
        """
        return self.__n_bs_measured

    @property
    def n_br(self) -> TimeMillisecondsAlias:
        """
        Get the value of :ref:`N_Br <knowledge-base-can-n-br>` time parameter which is currently set.

        .. note:: The actual (observed on the bus) value will be slightly longer as it also includes computation
            and CAN Interface delays.
        """
        return self.__n_br

    @n_br.setter
    def n_br(self, value: TimeMillisecondsAlias) -> None:
        """
        Set the value of :ref:`N_Br <knowledge-base-can-n-br>` time parameter to use.

        :param value: The value to set.
        """
        validate_time(value, accept_zero=True)
        if value >= self.n_br_max:
            raise ValueError("Provided time parameter value is greater than N_Br Max value. "
                             f"Expected: value < {self.n_br_max}. Actual value: {value}.")
        self.__n_br = value

    @property
    def n_br_max(self) -> TimeMillisecondsAlias:
        """
        Get the maximum valid value of :ref:`N_Br <knowledge-base-can-n-br>` time parameter.

        .. warning:: To assess maximal value of :ref:`N_Br <knowledge-base-can-n-br>`, the actual value of
            :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter is required.
            Either the latest measured value of :ref:`N_Ar <knowledge-base-can-n-ar>` would be used,
            or 0ms would be assumed (if there are no measurement result).
        """
        n_ar_measured = 0 if self.n_ar_measured is None else self.n_ar_measured
        return 0.9 * self.n_bs_timeout - n_ar_measured

    @property
    def n_cs(self) -> TimeMillisecondsAlias | None:
        """
        Get the value of :ref:`N_Cs <knowledge-base-can-n-cs>` time parameter which is currently set.

        .. note:: The actual (observed on the bus) value will be slightly longer as it also includes computation
            and CAN Interface delays.
        """
        return self.__n_cs

    @n_cs.setter
    def n_cs(self, value: TimeMillisecondsAlias | None) -> None:
        """
        Set the value of :ref:`N_Cs <knowledge-base-can-n-cs>` time parameter to use.

        :param value: The value to set.
            - None - use timing compatible with :ref:`STmin <knowledge-base-can-st-min>` value received in a preceding
                :ref:`Flow Control CAN packet <knowledge-base-can-flow-control>`
            - int/float type - timing value to be used regardless of a received
                :ref:`STmin <knowledge-base-can-st-min>` value
        """
        if value is not None:
            validate_time(value, accept_zero=True)
            if value >= self.n_cs_max:
                raise ValueError("Provided time parameter value is greater than N_Cs Max value. "
                                 f"Expected: value < {self.n_cs_max}. Actual value: {value}.")
        self.__n_cs = value

    @property
    def n_cs_max(self) -> TimeMillisecondsAlias:
        """
        Get the maximum valid value of :ref:`N_Cs <knowledge-base-can-n-cs>` time parameter.

        .. warning:: To assess maximal value of :ref:`N_Cs <knowledge-base-can-n-cs>`, the actual value of
            :ref:`N_As <knowledge-base-can-n-as>` time parameter is required.
            Either the latest measured value of :ref:`N_As <knowledge-base-can-n-as>` would be used,
            or 0ms would be assumed (if there are no measurement result).
        """
        n_as_measured = 0 if self.n_as_measured is None else self.n_as_measured
        return 0.9 * self.n_cr_timeout - n_as_measured

    @property
    def n_cr_timeout(self) -> TimeMillisecondsAlias:
        """Timeout value for :ref:`N_Cr <knowledge-base-can-n-cr>` time parameter."""
        return self.__n_cr_timeout

    @n_cr_timeout.setter
    def n_cr_timeout(self, value: TimeMillisecondsAlias) -> None:
        """
        Set timeout value for :ref:`N_Cr <knowledge-base-can-n-cr>` time parameter.

        :param value: Value of timeout to set.
        """
        validate_time(value, accept_zero=False)
        if value != self.N_CR_TIMEOUT:
            warn(message="Non-default value of N_Cr timeout was set.",
                 category=ValueWarning)
        self.__n_cr_timeout = value

    @property
    def n_cr_measured(self) -> tuple[TimeMillisecondsAlias, ...] | None:
        """
        Get the last measured values of :ref:`N_Cr <knowledge-base-can-n-cr>` time parameter.

        .. note:: The last measurement comes from the last reception of UDS message using either
            :meth:`~uds.transport_interface.addressing.AbstractCanTransportInterface.receive_message` or
            :meth:`~uds.transport_interface.addressing.AbstractCanTransportInterface.async_receive_message` method.

        :return: Tuple with times in milliseconds or None if the values could not be measured.
        """
        return self.__n_cr_measured

    def _update_n_ar_measured(self, value: TimeMillisecondsAlias) -> None:
        """
        Update measured values of :ref:`N_Ar <knowledge-base-can-n-ar>`.

        :param value: Value to set.
        """
        validate_time(value, accept_zero=True)
        if value > self.n_ar_timeout:
            warn("Measured value of N_Ar was greater than N_Ar timeout.",
                 category=ValueWarning)
        self.__n_ar_measured = value

    def _update_n_as_measured(self, value: TimeMillisecondsAlias) -> None:
        """
        Update measured values of :ref:`N_As <knowledge-base-can-n-as>`.

        :param value: Value to set.
        """
        validate_time(value, accept_zero=True)
        if value > self.n_as_timeout:
            warn("Measured value of N_As was greater than N_As timeout.",
                 category=ValueWarning)
        self.__n_as_measured = value

    def _update_n_bs_measured(self, message_record: UdsMessageRecord) -> None:
        """
        Update measured values of :ref:`N_Bs <knowledge-base-can-n-bs>` according to timestamps of CAN packet records.

        :param message_record: Record of UDS message transmitted over CAN.

        :raise TypeError: Provided value is not UDS message record.
        :raise ValueError: Provided UDS message record was not transmitted.
        """
        if not isinstance(message_record, UdsMessageRecord):
            raise TypeError(f"Provided value is not UDS Message Record type. Actual type: {type(message_record)}.")
        if message_record.direction != TransmissionDirection.TRANSMITTED:
            raise ValueError("Provided UDS Message Record was not transmitted.")
        if len(message_record.packets_records) == 1:
            self.__n_bs_measured = None
        else:
            n_bs_measured = []
            for i, packet_record in enumerate(message_record.packets_records[1:]):
                if packet_record.packet_type == CanPacketType.FLOW_CONTROL:
                    n_bs = (packet_record.transmission_timestamp
                            - message_record.packets_records[i].transmission_timestamp)
                    n_bs_measured.append(round(n_bs * 1000, 3))
            self.__n_bs_measured = tuple(n_bs_measured)

    def _update_n_cr_measured(self, message_record: UdsMessageRecord) -> None:
        """
        Update measured values of :ref:`N_Cr <knowledge-base-can-n-cr>` according to timestamps of CAN packet records.

        :param message_record: Record of UDS message received over CAN.

        :raise TypeError: Provided value is not UDS message record.
        :raise ValueError: Provided UDS message record was not received.
        """
        if not isinstance(message_record, UdsMessageRecord):
            raise TypeError(f"Provided value is not UDS Message Record type. Actual type: {type(message_record)}.")
        if message_record.direction != TransmissionDirection.RECEIVED:
            raise ValueError("Provided UDS Message Record was not received.")
        if len(message_record.packets_records) == 1:
            self.__n_cr_measured = None
        else:
            n_cr_measured = []
            for i, packet_record in enumerate(message_record.packets_records[1:]):
                if packet_record.packet_type == CanPacketType.CONSECUTIVE_FRAME:
                    n_cr = (packet_record.transmission_timestamp
                            - message_record.packets_records[i].transmission_timestamp)
                    n_cr_measured.append(round(n_cr * 1000, 3))
            self.__n_cr_measured = tuple(n_cr_measured)

    def clear_measurements(self) -> None:
        """Clear measured values of CAN communication parameters."""
        self.__n_ar_measured = None
        self.__n_as_measured = None
        self.__n_bs_measured = None
        self.__n_cr_measured = None

    # Packets transmission and reception

    def _send_cf_packets_block(self,
                               cf_packets_block: list[CanPacket],
                               delay: TimeMillisecondsAlias,
                               fc_transmission_timestamp: float) -> tuple[CanPacketRecord, ...]:
        """
        Send a block of Consecutive Frame CAN packets.

        :param cf_packets_block: Consecutive Frame CAN packets to send.
        :param delay: Minimum delay between sending following Consecutive Frame packets [ms].
        :param fc_transmission_timestamp: Transmission timestamp of the preceding Flow Control packet.

        :return: Records containing historical information about the transmitted Consecutive Frame CAN packets.
        """
        packet_records = []
        timestamp_send = fc_transmission_timestamp + delay / 1000.
        for cf_packet in cf_packets_block:
            time_to_wait_s = timestamp_send - perf_counter()
            if time_to_wait_s > 0:
                sleep(time_to_wait_s)
            cf_packet_record = self.send_packet(cf_packet)
            timestamp_send = cf_packet_record.transmission_timestamp + delay / 1000.
            packet_records.append(cf_packet_record)
        return tuple(packet_records)

    async def _async_send_cf_packets_block(self,
                                           cf_packets_block: list[CanPacket],
                                           delay: TimeMillisecondsAlias,
                                           fc_transmission_timestamp: float,
                                           loop: AbstractEventLoop) -> tuple[CanPacketRecord, ...]:
        """
        Asynchronously send a block of Consecutive Frame CAN packets.

        :param cf_packets_block: Consecutive Frame CAN packets to send.
        :param delay: Minimum delay between sending following Consecutive Frame packets [ms].
        :param fc_transmission_timestamp: Transmission timestamp of the preceding Flow Control packet.
        :param loop: The asyncio event loop to use for scheduling this task.

        :return: Records containing historical information about the transmitted Consecutive Frame CAN packets.
        """
        packet_records = []
        timestamp_send = fc_transmission_timestamp + delay / 1000.
        for cf_packet in cf_packets_block:
            time_to_wait_s = timestamp_send - perf_counter()
            if time_to_wait_s > 0:
                await async_sleep(time_to_wait_s)
            cf_packet_record = await self.async_send_packet(cf_packet, loop=loop)
            timestamp_send = cf_packet_record.transmission_timestamp + delay / 1000.
            packet_records.append(cf_packet_record)
        return tuple(packet_records)

    def _receive_cf_packets_block(self,
                                  sequence_number: int,
                                  block_size: int,
                                  remaining_data_length: int,
                                  timestamp_end: TimestampAlias | None
                                  ) -> UdsMessageRecord | tuple[CanPacketRecord, ...]:
        """
        Receive block of :ref:`Consecutive Frames <knowledge-base-can-consecutive-frame>`.

        :param sequence_number: Current :ref:`Sequence Number <knowledge-base-can-sequence-number>`
            (next Consecutive Frame shall have this value set).
        :param block_size: :ref:`Block Size <knowledge-base-can-block-size>` value sent in the last
            :ref:`Flow Control CAN packet <knowledge-base-can-flow-control>`.
        :param remaining_data_length: Number of remaining data bytes to receive in UDS message.
        :param timestamp_end: The final timestamp till when the reception must be completed.

        :raise TimeoutError: Timeout was reached. Either:
            - Consecutive Frame did not arrive before reaching N_Cr timeout
            - Diagnostic message reception

        :return: Either:
            - Record of UDS message if reception was interrupted by a new UDS message transmission.
            - Tuple with records of received Consecutive Frames.
        """
        timestamp_start = perf_counter()
        timeout_end_ms = float("inf")
        received_cf: list[CanPacketRecord] = []
        received_payload_size: int = 0
        while received_payload_size < remaining_data_length and (len(received_cf) != block_size or block_size == 0):
            timestamp_now = perf_counter()
            # check final (timestamp_end) timeout
            if timestamp_end is not None:
                timeout_end_ms = (timestamp_end - timestamp_now) * 1000.
            if timeout_end_ms <= 0:
                raise TimeoutError("Total message reception timeout was reached.")
            # check n_cr timeout
            time_elapsed_ms = (timestamp_now - timestamp_start) * 1000.
            remaining_n_cr_timeout_ms = self.n_cr_timeout - time_elapsed_ms
            if remaining_n_cr_timeout_ms <= 0:
                raise TimeoutError("Timeout (N_Cr) was reached before Consecutive Frame CAN packet was received.")
            # receive packet
            received_packet = self.receive_packet(timeout=min(timeout_end_ms, remaining_n_cr_timeout_ms))
            # handle new message reception
            if CanPacketType.is_initial_packet_type(received_packet.packet_type):
                warn(message="A new DoCAN message transmission was started. "
                             "Reception of the previous message was aborted.",
                     category=NewMessageReceptionWarning)
                return self._message_receive_start(initial_packet=received_packet,
                                                   timestamp_end=timestamp_end)
            # handle following Consecutive Frame
            if (received_packet.packet_type == CanPacketType.CONSECUTIVE_FRAME
                    and received_packet.sequence_number == sequence_number):
                timestamp_start = perf_counter()
                received_cf.append(received_packet)
                received_payload_size += len(received_packet.payload)  # type: ignore
                sequence_number = (received_packet.sequence_number + 1) & 0xF
        return tuple(received_cf)

    async def _async_receive_cf_packets_block(self,
                                              sequence_number: int,
                                              block_size: int,
                                              remaining_data_length: int,
                                              timestamp_end: TimestampAlias | None,
                                              loop: AbstractEventLoop
                                              ) -> UdsMessageRecord | tuple[CanPacketRecord, ...]:
        """
        Receive asynchronously block of :ref:`Consecutive Frames <knowledge-base-can-consecutive-frame>`.

        :param sequence_number: Current :ref:`Sequence Number <knowledge-base-can-sequence-number>`
            (next Consecutive Frame shall have this value set).
        :param block_size: :ref:`Block Size <knowledge-base-can-block-size>` value sent in the last
            :ref:`Flow Control CAN packet <knowledge-base-can-flow-control>`.
        :param remaining_data_length: Number of remaining data bytes to receive in UDS message.
        :param timestamp_end: The final timestamp till when the reception must be completed.
        :param loop: An asyncio event loop used for observing messages.

        :return: Either:
            - Record of UDS message if reception was interrupted by a new UDS message transmission.
            - Tuple with records of received Consecutive Frames.
        """
        timestamp_start = perf_counter()
        timeout_end_ms = float("inf")
        received_cf: list[CanPacketRecord] = []
        received_payload_size: int = 0
        while received_payload_size < remaining_data_length and (len(received_cf) != block_size or block_size == 0):
            timestamp_now = perf_counter()
            # check final (timestamp_end) timeout
            if timestamp_end is not None:
                timeout_end_ms = (timestamp_end - timestamp_now) * 1000.
            if timeout_end_ms <= 0:
                raise TimeoutError("Total message reception timeout was reached.")
            # check n_cr timeout
            time_elapsed_ms = (timestamp_now - timestamp_start) * 1000.
            remaining_n_cr_timeout_ms = self.n_cr_timeout - time_elapsed_ms
            if remaining_n_cr_timeout_ms <= 0:
                raise TimeoutError("Timeout (N_Cr) was reached before Consecutive Frame CAN packet was received.")
            # receive packet
            received_packet = await self.async_receive_packet(timeout=min(remaining_n_cr_timeout_ms, timeout_end_ms),
                                                              loop=loop)
            # handle new message reception
            if CanPacketType.is_initial_packet_type(received_packet.packet_type):
                warn(message="A new DoCAN message transmission was started. "
                             "Reception of the previous message was aborted.",
                     category=NewMessageReceptionWarning)
                return await self._async_message_receive_start(initial_packet=received_packet,
                                                               timestamp_end=timestamp_end,
                                                               loop=loop)
            # handle following Consecutive Frame
            if (received_packet.packet_type == CanPacketType.CONSECUTIVE_FRAME
                    and received_packet.sequence_number == sequence_number):
                timestamp_start = perf_counter()
                received_cf.append(received_packet)
                received_payload_size += len(received_packet.payload)  # type: ignore
                sequence_number = (received_packet.sequence_number + 1) & 0xF
        return tuple(received_cf)

    def _receive_consecutive_frames(self,
                                    first_frame: CanPacketRecord,
                                    timestamp_end: TimestampAlias | None) -> UdsMessageRecord:
        """
        Receive Consecutive Frames after reception of First Frame.

        :param first_frame: :ref:`First Frame <knowledge-base-can-first-frame>` that was received.
        :param timestamp_end: The final timestamp till when the reception must be completed.

        :raise OverflowError: Flow Control packet with :ref:`Flow Status <knowledge-base-can-flow-status>` equal to
            OVERFLOW was sent.

        :return: Record of UDS message that was formed provided First Frame and received Consecutive Frames.
        """
        packets_records: list[CanPacketRecord] = [first_frame]
        message_data_length: int = first_frame.data_length  # type: ignore
        received_data_length: int = len(first_frame.payload)  # type: ignore
        sequence_number: int = 1
        flow_control_iterator = iter(self.flow_control_parameters_generator)
        while True:
            if timestamp_end is not None:
                remaining_end_timeout_ms = (timestamp_end - perf_counter()) * 1000.
                if remaining_end_timeout_ms < 0:
                    raise TimeoutError("Total message reception timeout was reached.")
            time_elapsed_ms = (perf_counter() - packets_records[-1].transmission_timestamp) * 1000.
            remaining_n_br_timeout_ms = self.n_br - time_elapsed_ms
            if remaining_n_br_timeout_ms > 0:
                try:
                    received_packet = self.receive_packet(timeout=remaining_n_br_timeout_ms)
                except TimeoutError:
                    pass
                else:
                    if CanPacketType.is_initial_packet_type(received_packet.packet_type):
                        warn(message="A new DoCAN message transmission was started. "
                                     "Reception of the previous message was aborted.",
                             category=NewMessageReceptionWarning)
                        return self._message_receive_start(initial_packet=received_packet,
                                                           timestamp_end=timestamp_end)
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
                                                          remaining_data_length=remaining_data_length,
                                                          timestamp_end=timestamp_end)
                if isinstance(cf_block, UdsMessageRecord):  # in case another message interrupted
                    return cf_block
                packets_records.extend(cf_block)
                received_data_length += len(cf_block[0].payload) * len(cf_block)  # type: ignore
                if received_data_length >= message_data_length:
                    break
                sequence_number = (cf_block[-1].sequence_number + 1) & 0xF  # type: ignore
        return UdsMessageRecord(packets_records)

    async def _async_receive_consecutive_frames(self,
                                                first_frame: CanPacketRecord,
                                                timestamp_end: TimestampAlias | None,
                                                loop: AbstractEventLoop) -> UdsMessageRecord:
        """
        Receive asynchronously Consecutive Frames after reception of First Frame.

        :param first_frame: :ref:`First Frame <knowledge-base-can-first-frame>` that was received.
        :param timestamp_end: The final timestamp till when the reception must be completed.
        :param loop: An asyncio event loop used for observing messages.

        :raise TimeoutError: :ref:`N_Cr <knowledge-base-can-n-cr>` timeout was reached.
        :raise OverflowError: Flow Control packet with :ref:`Flow Status <knowledge-base-can-flow-status>` equal to
            OVERFLOW was sent.
        :raise NotImplementedError: Unhandled CAN packet starting a new CAN message transmission was received.

        :return: Record of UDS message that was formed provided First Frame and received Consecutive Frames.
        """
        packets_records: list[CanPacketRecord] = [first_frame]
        message_data_length: int = first_frame.data_length  # type: ignore
        received_data_length: int = len(first_frame.payload)  # type: ignore
        sequence_number: int = 1
        flow_control_iterator = iter(self.flow_control_parameters_generator)
        while True:
            if timestamp_end is not None:
                remaining_end_timeout_ms = (timestamp_end - perf_counter()) * 1000.
                if remaining_end_timeout_ms < 0:
                    raise TimeoutError("Total message reception timeout was reached.")
            time_elapsed_ms = (perf_counter() - packets_records[-1].transmission_timestamp) * 1000.
            remaining_n_br_timeout_ms = self.n_br - time_elapsed_ms
            if remaining_n_br_timeout_ms > 0:
                try:
                    received_packet = await self.async_receive_packet(timeout=remaining_n_br_timeout_ms, loop=loop)
                except (TimeoutError, AsyncioTimeoutError):
                    pass
                else:
                    if CanPacketType.is_initial_packet_type(received_packet.packet_type):
                        warn(message="A new DoCAN message transmission was started. "
                                     "Reception of the previous message was aborted.",
                             category=NewMessageReceptionWarning)
                        return await self._async_message_receive_start(initial_packet=received_packet,
                                                                       timestamp_end=timestamp_end,
                                                                       loop=loop)
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
                                                                      timestamp_end=timestamp_end,
                                                                      loop=loop)
                if isinstance(cf_block, UdsMessageRecord):  # in case another message interrupted
                    return cf_block
                packets_records.extend(cf_block)
                received_data_length += len(cf_block[0].payload) * len(cf_block)  # type: ignore
                if received_data_length >= message_data_length:
                    break
                sequence_number = (cf_block[-1].sequence_number + 1) & 0xF  # type: ignore
        return UdsMessageRecord(packets_records)

    def _message_receive_start(self,
                               initial_packet: CanPacketRecord,
                               timestamp_end: TimestampAlias | None) -> UdsMessageRecord:
        """
        Continue to receive message after receiving initial packet.

        :param initial_packet: Record of a packet initiating UDS message reception.
        :param timestamp_end: The final timestamp till when the reception must be completed.

        :raise NotImplementedError: Unhandled CAN packet starting a new CAN message transmission was received.

        :return: Record of UDS message received.
        """
        if initial_packet.packet_type == CanPacketType.SINGLE_FRAME:
            return UdsMessageRecord([initial_packet])
        if initial_packet.packet_type == CanPacketType.FIRST_FRAME:
            return self._receive_consecutive_frames(first_frame=initial_packet,
                                                    timestamp_end=timestamp_end)
        raise NotImplementedError(f"CAN packet of unhandled type was received: {initial_packet.packet_type}")

    async def _async_message_receive_start(self,
                                           initial_packet: CanPacketRecord,
                                           timestamp_end: TimestampAlias | None,
                                           loop: AbstractEventLoop) -> UdsMessageRecord:
        """
        Continue to receive message asynchronously after receiving initial packet.

        :param initial_packet: Record of a packet initiating UDS message reception.
        :param timestamp_end: The final timestamp till when the reception must be completed.
        :param loop: An asyncio event loop used for observing messages.

        :raise NotImplementedError: Unhandled CAN packet starting a new CAN message transmission was received.

        :return: Record of UDS message received.
        """
        if initial_packet.packet_type == CanPacketType.SINGLE_FRAME:
            return UdsMessageRecord([initial_packet])
        if initial_packet.packet_type == CanPacketType.FIRST_FRAME:
            return await self._async_receive_consecutive_frames(first_frame=initial_packet,
                                                                timestamp_end=timestamp_end,
                                                                loop=loop)
        raise NotImplementedError(f"CAN packet of unhandled type was received: {initial_packet.packet_type}")

    @abstractmethod
    def _wait_for_flow_control(self, timeout_timestamp: float) -> CanPacketRecord:
        """
        Wait until a Flow Control CAN packet is received.

        :param timeout_timestamp: Deadline for receiving the Flow Control CAN packet,
            expressed as a :func:`time.perf_counter` timestamp.

        :return: Record containing historical information about the received Flow Control CAN packet.
        """

    @abstractmethod
    async def _async_wait_for_flow_control(self, timeout_timestamp: float) -> CanPacketRecord:
        """
        Asynchronously wait until a Flow Control CAN packet is received.

        :param timeout_timestamp: Deadline for receiving the Flow Control CAN packet,
            expressed as a :func:`time.perf_counter` timestamp.

        :return: Record containing historical information about the received Flow Control CAN packet.
        """

    @abstractmethod
    def clear_received_frame_buffers(self) -> None:
        """
        Clear buffers for storing received CAN frames.

        .. warning:: This makes all previously received CAN packets inaccessible.
        """

    @abstractmethod
    def clear_transmitted_frame_buffers(self) -> None:
        """Clear buffers for storing transmitted CAN frames."""

    @abstractmethod
    def clear_flow_control_frame_buffers(self) -> None:
        """Clear buffers for storing received Flow Control CAN frames."""

    @abstractmethod
    def send_packet(self, packet: CanPacket) -> CanPacketRecord:  # type: ignore
        """
        Transmit CAN packet.

        :param packet: CAN packet to send.

        :return: Record with historic information about transmitted packet.
        """

    @abstractmethod
    async def async_send_packet(self,
                                packet: CanPacket,  # type: ignore
                                loop: AbstractEventLoop | None = None) -> CanPacketRecord:
        """
        Transmit CAN packet asynchronously.

        :param packet: CAN packet to send.
        :param loop: An asyncio event loop to use for scheduling this task.

        :return: Record with historic information about transmitted packet.
        """

    @abstractmethod
    def receive_packet(self, timeout: TimeMillisecondsAlias | None = None) -> CanPacketRecord:
        """
        Receive CAN packet.

        :param timeout: Maximal time (in milliseconds) to wait.
            Leave None to wait forever.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information about received packet.
        """

    @abstractmethod
    async def async_receive_packet(self,
                                   timeout: TimeMillisecondsAlias | None = None,
                                   loop: AbstractEventLoop | None = None) -> CanPacketRecord:
        """
        Receive CAN packet asynchronously.

        :param timeout: Maximal time (in milliseconds) to wait.
            Leave None to wait forever.
        :param loop: An asyncio event loop to use for scheduling this task.

        :raise TimeoutError: Timeout was reached.
        :raise asyncio.TimeoutError: Timeout was reached.

        :return: Record with historic information about received packet.
        """

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
        self.setup_sync()
        self.clear_flow_control_frame_buffers()
        packets_to_send = list(self.segmenter.segmentation(message))
        packet_records = [self.send_packet(packets_to_send.pop(0))]
        while packets_to_send:
            flow_control_record = self._wait_for_flow_control(
                timeout_timestamp=packet_records[-1].transmission_timestamp + self.n_bs_timeout / 1000.)
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
                        fc_transmission_timestamp=flow_control_record.transmission_timestamp))
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
                                 loop: AbstractEventLoop | None = None) -> UdsMessageRecord:
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
        self.setup_async(loop)
        self.clear_flow_control_frame_buffers()
        packets_to_send = list(self.segmenter.segmentation(message))
        packet_records = [await self.async_send_packet(packets_to_send.pop(0), loop=loop)]
        while packets_to_send:
            flow_control_record = await self._async_wait_for_flow_control(
                timeout_timestamp=packet_records[-1].transmission_timestamp + self.n_bs_timeout / 1000.)
            packet_records.append(flow_control_record)
            if flow_control_record.flow_status == CanFlowStatus.ContinueToSend:
                cf_number_to_send = len(packets_to_send) if flow_control_record.block_size == 0 \
                    else flow_control_record.block_size
                delay_between_cf = self.n_cs if self.n_cs is not None \
                    else CanSTminTranslator.decode(flow_control_record.st_min)  # type: ignore
                packet_records.extend(
                    await self._async_send_cf_packets_block(
                        cf_packets_block=packets_to_send[:cf_number_to_send],
                        delay=delay_between_cf,
                        fc_transmission_timestamp=flow_control_record.transmission_timestamp,
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

    def receive_message(self,
                        start_timeout: TimeMillisecondsAlias | None = None,
                        end_timeout: TimeMillisecondsAlias | None = None) -> UdsMessageRecord:
        """
        Receive UDS message over CAN.

        :param start_timeout: Maximal time (in milliseconds) to wait for the start of a message transmission.
            Leave None to wait forever.
        :param end_timeout: Maximal time (in milliseconds) to wait for a message transmission to finish.
            Leave None to wait forever.

        :raise MessageTransmissionNotStartedError: Timeout was exceeded before message reception started.
        :raise TimeoutError: Timeout was exceeded during message receiving (before all packets received).

        :return: Record with historic information about received UDS message.
        """
        timestamp_now = perf_counter()
        validate_timeout(start_timeout)
        validate_timeout(end_timeout)
        if start_timeout is not None:
            if end_timeout is not None and end_timeout < start_timeout:
                timestamp_start_timeout = timestamp_now + end_timeout / 1000.
            else:
                timestamp_start_timeout = timestamp_now + start_timeout / 1000.
        remaining_timeout_ms = None
        if end_timeout is not None:
            timestamp_end_timeout = timestamp_now + end_timeout / 1000.
        else:
            timestamp_end_timeout = None
        self.setup_sync()
        while True:
            # calculate remaining timeout
            if start_timeout is not None:
                timestamp_now = perf_counter()
                if timestamp_start_timeout <= timestamp_now:
                    raise MessageTransmissionNotStartedError("Timeout was reached before a UDS message was received.")
                remaining_timeout_ms = (timestamp_start_timeout - timestamp_now) * 1000.
            # receive packet
            try:
                received_packet = self.receive_packet(timeout=remaining_timeout_ms)
            except TimeoutError as exception:
                raise MessageTransmissionNotStartedError("Timeout was reached before a UDS message was received.") \
                    from exception
            # handle received packet
            if CanPacketType.is_initial_packet_type(received_packet.packet_type):
                return self._message_receive_start(initial_packet=received_packet,
                                                   timestamp_end=timestamp_end_timeout)
            warn(message="A CAN packet that does not start UDS message transmission was received.",
                 category=UnexpectedPacketReceptionWarning)

    async def async_receive_message(self,
                                    start_timeout: TimeMillisecondsAlias | None = None,
                                    end_timeout: TimeMillisecondsAlias | None = None,
                                    loop: AbstractEventLoop | None = None) -> UdsMessageRecord:
        """
        Receive asynchronously UDS message over CAN.

        :param start_timeout: Maximal time (in milliseconds) to wait for the start of a message transmission.
            Leave None to wait forever.
        :param end_timeout: Maximal time (in milliseconds) to wait for a message transmission to finish.
            Leave None to wait forever.
        :param loop: An asyncio event loop to use for scheduling this task.

        :raise MessageTransmissionNotStartedError: Timeout was exceeded before message reception started.
        :raise TimeoutError: Timeout was exceeded during message receiving (before all packets received).

        :return: Record with historic information about received UDS message.
        """
        timestamp_now = perf_counter()
        validate_timeout(start_timeout)
        validate_timeout(end_timeout)
        if start_timeout is not None:
            if end_timeout is not None and end_timeout < start_timeout:
                timestamp_start_timeout = timestamp_now + end_timeout / 1000.
            else:
                timestamp_start_timeout = timestamp_now + start_timeout / 1000.
        remaining_timeout_ms = None
        if end_timeout is not None:
            timestamp_end_timeout = timestamp_now + end_timeout / 1000.
        else:
            timestamp_end_timeout = None
        loop = get_running_loop() if loop is None else loop
        self.setup_async(loop=loop)
        while True:
            # calculate remaining timeout
            if start_timeout is not None:
                timestamp_now = perf_counter()
                if timestamp_start_timeout <= timestamp_now:
                    raise MessageTransmissionNotStartedError("Timeout was reached before a UDS message was received.")
                remaining_timeout_ms = (timestamp_start_timeout - timestamp_now) * 1000.
            # receive packet
            try:
                received_packet = await self.async_receive_packet(timeout=remaining_timeout_ms, loop=loop)
            except (TimeoutError, AsyncioTimeoutError) as exception:
                raise MessageTransmissionNotStartedError("Timeout was reached before a UDS message was received.") \
                    from exception
            # handle received packet
            if CanPacketType.is_initial_packet_type(received_packet.packet_type):
                return await self._async_message_receive_start(initial_packet=received_packet,
                                                               timestamp_end=timestamp_end_timeout,
                                                               loop=loop)
            warn(message="A CAN packet that does not start UDS message transmission was received.",
                 category=UnexpectedPacketReceptionWarning)

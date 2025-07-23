"""Segmentation specific for CAN bus."""

__all__ = ["CanSegmenter"]

from typing import Optional, Tuple, Type, Union

from uds.addressing import AbstractAddressingInformation, AddressingType
from uds.message import UdsMessage, UdsMessageRecord
from uds.packet import AbstractPacket, AbstractPacketRecord, PacketsContainersSequence
from uds.segmentation import AbstractSegmenter, SegmentationError
from uds.utilities import validate_raw_byte

from .addressing import AbstractCanAddressingInformation, CanAddressingFormat
from .frame import DEFAULT_FILLER_BYTE, CanDlcHandler
from .packet import (
    MAX_LONG_FF_DL_VALUE,
    MAX_SHORT_FF_DL_VALUE,
    CanFlowStatus,
    CanPacket,
    CanPacketRecord,
    CanPacketType,
    get_consecutive_frame_max_payload_size,
    get_first_frame_payload_size,
    get_max_sf_dl,
)


class CanSegmenter(AbstractSegmenter):
    """Segmenter class that provides utilities for segmentation and desegmentation specific for CAN bus."""

    def __init__(self, *,
                 addressing_information: AbstractCanAddressingInformation,
                 dlc: int = CanDlcHandler.MIN_BASE_UDS_DLC,
                 use_data_optimization: bool = False,
                 filler_byte: int = DEFAULT_FILLER_BYTE) -> None:
        """
        Configure CAN Segmenter.

        :param addressing_information: Addressing Information configuration of a CAN node.
        :param dlc: Base CAN DLC value to use for creating CAN Packets.
        :param use_data_optimization: Information whether to use CAN Frame Data Optimization in created CAN Packets
            during segmentation.
        :param filler_byte: Filler byte value to use for CAN Frame Data Padding in created CAN Packets during
            segmentation.
        """
        super().__init__(addressing_information=addressing_information)
        self.dlc = dlc
        self.use_data_optimization = use_data_optimization
        self.filler_byte = filler_byte

    @property
    def supported_addressing_information_class(self) -> Type[AbstractAddressingInformation]:
        """Addressing Information class supported by this segmenter."""
        return AbstractCanAddressingInformation

    @property
    def supported_packet_class(self) -> Type[AbstractPacket]:
        """Packet class supported by CAN segmenter."""
        return CanPacket

    @property
    def supported_packet_record_class(self) -> Type[AbstractPacketRecord]:
        """Packet Record class supported by CAN segmenter."""
        return CanPacketRecord

    @property
    def addressing_format(self) -> CanAddressingFormat:
        """CAN Addressing Format used."""
        return self.addressing_information.ADDRESSING_FORMAT

    @property
    def dlc(self) -> int:
        """
        Value of base CAN DLC to use for CAN Packets.

        .. note:: All output CAN Packets (created by :meth:`~uds.segmentation.can_segmenter.CanSegmenter.segmentation`)
            will have this DLC value set unless
            :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>` is used.
        """
        return self.__dlc

    @dlc.setter
    def dlc(self, value: int) -> None:
        """
        Set value of base CAN DLC to use for CAN Packets.

        :param value: Value to set.

        :raise ValueError: Provided value is too small.
        """
        CanDlcHandler.validate_dlc(value)
        if value < CanDlcHandler.MIN_BASE_UDS_DLC:
            raise ValueError(f"Provided value is too small. Expected: DLC >= {CanDlcHandler.MIN_BASE_UDS_DLC}. "
                             f"Actual value: {value}")
        self.__dlc: int = value

    @property
    def use_data_optimization(self) -> bool:
        """Information whether to use CAN Frame Data Optimization during CAN Packet creation."""
        return self.__use_data_optimization

    @use_data_optimization.setter
    def use_data_optimization(self, value: bool) -> None:
        """
        Set whether to use CAN Frame Data Optimization during CAN Packets creation.

        :param value: Value to set.
        """
        self.__use_data_optimization: bool = bool(value)

    @property
    def filler_byte(self) -> int:
        """Filler byte value to use for CAN Frame Data Padding during segmentation."""
        return self.__filler_byte

    @filler_byte.setter
    def filler_byte(self, value: int) -> None:
        """
        Set value of filler byte to use for CAN Frame Data Padding.

        :param value: Value to set.
        """
        validate_raw_byte(value)
        self.__filler_byte: int = value

    def __physical_segmentation(self, message: UdsMessage) -> Tuple[CanPacket, ...]:
        """
        Segment physically addressed diagnostic message.

        :param message: UDS message to divide into packets.

        :raise SegmentationError: Provided diagnostic message cannot be segmented.

        :return: CAN packets that are an outcome of UDS message segmentation.
        """
        message_payload_size = len(message.payload)
        if message_payload_size > MAX_LONG_FF_DL_VALUE:
            raise SegmentationError("Provided diagnostic message cannot be segmented to CAN Packet as it is too big "
                                    "to transmit it over CAN bus.")
        if message_payload_size <= get_max_sf_dl(addressing_format=self.addressing_format,
                                                 dlc=self.dlc):
            single_frame = CanPacket(packet_type=CanPacketType.SINGLE_FRAME,
                                     payload=message.payload,
                                     filler_byte=self.filler_byte,
                                     dlc=None if self.use_data_optimization else self.dlc,
                                     **self.addressing_information.tx_physical_params)
            return (single_frame,)
        ff_payload_size = get_first_frame_payload_size(addressing_format=self.addressing_format,
                                                       dlc=self.dlc,
                                                       long_ff_dl_format=message_payload_size > MAX_SHORT_FF_DL_VALUE)
        first_frame = CanPacket(packet_type=CanPacketType.FIRST_FRAME,
                                payload=message.payload[:ff_payload_size],
                                dlc=self.dlc,
                                data_length=message_payload_size,
                                **self.addressing_information.tx_physical_params)
        cf_payload_size = get_consecutive_frame_max_payload_size(addressing_format=self.addressing_format, dlc=self.dlc)
        total_cfs_number = (message_payload_size - ff_payload_size + cf_payload_size - 1) // cf_payload_size
        consecutive_frames = []
        for cf_index in range(total_cfs_number):
            sequence_number = (cf_index + 1) % 0x10
            payload_i_start = ff_payload_size + cf_index * cf_payload_size
            payload_i_stop = payload_i_start + cf_payload_size
            last_cf = cf_index == total_cfs_number-1
            consecutive_frame = CanPacket(packet_type=CanPacketType.CONSECUTIVE_FRAME,
                                          payload=message.payload[payload_i_start: payload_i_stop],
                                          dlc=None if last_cf and self.use_data_optimization else self.dlc,
                                          sequence_number=sequence_number,
                                          filler_byte=self.filler_byte,
                                          **self.addressing_information.tx_physical_params)
            consecutive_frames.append(consecutive_frame)
        return first_frame, *consecutive_frames

    def __functional_segmentation(self, message: UdsMessage) -> Tuple[CanPacket, ...]:
        """
        Segment functionally addressed diagnostic message.

        :param message: UDS message to divide into packets.

        :raise SegmentationError: Provided diagnostic message cannot be segmented.

        :return: CAN packets that are an outcome of UDS message segmentation.
        """
        max_payload_size = get_max_sf_dl(addressing_format=self.addressing_format, dlc=self.dlc)
        message_payload_size = len(message.payload)
        if message_payload_size > max_payload_size:
            raise SegmentationError("Provided diagnostic message cannot be segmented using functional addressing "
                                    "as it will not fit into a Single Frame.")
        single_frame = CanPacket(packet_type=CanPacketType.SINGLE_FRAME,
                                 payload=message.payload,
                                 filler_byte=self.filler_byte,
                                 dlc=None if self.use_data_optimization else self.dlc,
                                 **self.addressing_information.tx_functional_params)
        return (single_frame,)

    def is_desegmented_message(self, packets: PacketsContainersSequence) -> bool:
        """
        Check whether provided packets are full sequence of packets that form exactly one diagnostic message.

        :param packets: Packets sequence to check.

        :raise ValueError: Provided value is not CAN packets sequence.
        :raise NotImplementedError: There is missing implementation for the provided initial packet type.
            Please create an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            with detailed description if you face this error.

        :return: True if the packets form exactly one diagnostic message.
            False if there are missing, additional or inconsistent (e.g. two packets that initiate a message) packets.
        """
        if not self.is_supported_packets_sequence_type(packets):
            raise ValueError("Provided packets are not consistent CAN Packets sequence.")
        if not CanPacketType.is_initial_packet_type(packets[0].packet_type):
            return False
        if packets[0].packet_type == CanPacketType.SINGLE_FRAME:
            return len(packets) == 1
        if packets[0].packet_type == CanPacketType.FIRST_FRAME:
            total_payload_size = packets[0].data_length
            payload_bytes_found = len(packets[0].payload)
            for following_packet in packets[1:]:
                if CanPacketType.is_initial_packet_type(following_packet.packet_type):
                    return False
                if payload_bytes_found >= total_payload_size:
                    return False
                if following_packet.payload is not None:
                    payload_bytes_found += len(following_packet.payload)
            return payload_bytes_found >= total_payload_size
        raise NotImplementedError(f"Unknown packet type received: {packets[0].packet_type}")

    def get_flow_control_packet(self,
                                flow_status: CanFlowStatus,
                                block_size: Optional[int] = None,
                                st_min: Optional[int] = None) -> CanPacket:
        """
        Create Flow Control CAN packet.

        :param flow_status: Value of Flow Status parameter.
        :param block_size: Value of Block Size parameter.
            This parameter is only required with ContinueToSend Flow Status, leave None otherwise.
        :param st_min: Value of Separation Time minimum (STmin) parameter.
            This parameter is only required with ContinueToSend Flow Status, leave None otherwise.

        :return: Flow Control CAN packet with provided parameters.
        """
        return CanPacket(packet_type=CanPacketType.FLOW_CONTROL,
                         flow_status=flow_status,
                         block_size=block_size,
                         st_min=st_min,
                         filler_byte=self.filler_byte,
                         dlc=None if self.use_data_optimization else self.dlc,
                         **self.addressing_information.tx_physical_params)

    def desegmentation(self, packets: PacketsContainersSequence) -> Union[UdsMessage, UdsMessageRecord]:
        """
        Perform desegmentation of CAN packets.

        :param packets: CAN packets to desegment into UDS message.

        :raise SegmentationError: Provided packets are not a complete packets sequence that form a diagnostic message.
        :raise NotImplementedError: There is missing implementation for the provided CAN Packets.
            Please create an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            with detailed description if you face this error.

        :return: A diagnostic message that is an outcome of CAN packets desegmentation.
        """
        if not self.is_desegmented_message(packets):
            raise SegmentationError("Provided packets are not a complete packets sequence")
        if isinstance(packets[0], CanPacketRecord):
            return UdsMessageRecord(packets)
        if isinstance(packets[0], CanPacket):
            if packets[0].packet_type == CanPacketType.SINGLE_FRAME and len(packets) == 1:
                return UdsMessage(payload=packets[0].payload,  # type: ignore
                                  addressing_type=packets[0].addressing_type)
            if packets[0].packet_type == CanPacketType.FIRST_FRAME:
                payload_bytes = bytearray()
                for packet in packets:
                    if packet.payload is not None:
                        payload_bytes += bytearray(packet.payload)
                return UdsMessage(payload=payload_bytes[:packets[0].data_length],
                                  addressing_type=packets[0].addressing_type)
            raise SegmentationError("Unexpectedly, something went wrong...")
        raise NotImplementedError("Missing implementation for provided CAN Packet.")

    def segmentation(self, message: UdsMessage) -> Tuple[CanPacket, ...]:
        """
        Perform segmentation of a diagnostic message.

        :param message: UDS message to divide into packets.

        :raise TypeError: Provided value is not instance of UdsMessage class.
        :raise NotImplementedError: There is missing implementation for the Addressing Type used by provided message.
            Please create an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            with detailed description if you face this error.

        :return: CAN packets that are an outcome of UDS message segmentation.
        """
        if not isinstance(message, UdsMessage):
            raise TypeError(f"Provided value is not instance of UdsMessage class. Actual type: {type(message)}")
        if message.addressing_type == AddressingType.PHYSICAL:
            return self.__physical_segmentation(message)
        if message.addressing_type == AddressingType.FUNCTIONAL:
            return self.__functional_segmentation(message)
        raise NotImplementedError("Unhandled addressing type.")

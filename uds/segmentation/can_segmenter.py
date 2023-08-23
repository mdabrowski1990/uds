"""Segmentation specific for CAN bus."""

__all__ = ["CanSegmenter"]

from typing import Optional, Union, Tuple, Type
from copy import copy

from uds.utilities import RawBytesList, validate_raw_byte
from uds.transmission_attributes import AddressingType
from uds.can import AbstractCanAddressingInformation, CanAddressingInformation, \
    CanAddressingFormat, CanAddressingFormatAlias, \
    CanDlcHandler, CanSingleFrameHandler, CanFirstFrameHandler, CanConsecutiveFrameHandler, DEFAULT_FILLER_BYTE
from uds.packet import CanPacket, CanPacketRecord, CanPacketType, \
    AbstractUdsPacket, AbstractUdsPacketRecord, AbstractUdsPacketContainer, PacketsContainersSequence, PacketsTuple
from uds.message import UdsMessage, UdsMessageRecord
from .abstract_segmenter import AbstractSegmenter, SegmentationError


class CanSegmenter(AbstractSegmenter):
    """Segmenter class that provides utilities for segmentation and desegmentation on CAN bus."""

    def __init__(self, *,
                 addressing_information: AbstractCanAddressingInformation,
                 dlc: int = CanDlcHandler.MIN_BASE_UDS_DLC,
                 use_data_optimization: bool = False,
                 filler_byte: int = DEFAULT_FILLER_BYTE) -> None:
        """
        Configure CAN Segmenter.

        :param addressing_information: Addressing Information configuration of a CAN entity.
        :param dlc: Base CAN DLC value to use for creating CAN Packets.
        :param use_data_optimization: Information whether to use CAN Frame Data Optimization in created CAN Packets
            during segmentation.
        :param filler_byte: Filler byte value to use for CAN Frame Data Padding in created CAN Packets during
            segmentation.
        """
        self.addressing_information = addressing_information
        self.dlc = dlc
        self.use_data_optimization = use_data_optimization
        self.filler_byte = filler_byte

    @property
    def supported_packet_class(self) -> Type[AbstractUdsPacket]:
        """Class of UDS Packet supported by CAN segmenter."""
        return CanPacket

    @property
    def supported_packet_record_class(self) -> Type[AbstractUdsPacketRecord]:
        """Class of UDS Packet Record supported by CAN segmenter."""
        return CanPacketRecord

    @property
    def addressing_format(self) -> CanAddressingFormatAlias:
        """CAN Addressing format used."""
        return self.addressing_information.addressing_format

    @property
    def rx_packets_physical_ai(self) -> AbstractCanAddressingInformation.PacketAIParamsAlias:
        """Addressing Information parameters of incoming physically addressed CAN packets."""
        return self.addressing_information.rx_packets_physical_ai

    @property
    def tx_packets_physical_ai(self) -> AbstractCanAddressingInformation.PacketAIParamsAlias:
        """Addressing Information parameters of outgoing physically addressed CAN packets."""
        return self.addressing_information.tx_packets_physical_ai

    @property
    def rx_packets_functional_ai(self) -> AbstractCanAddressingInformation.PacketAIParamsAlias:
        """Addressing Information parameters of incoming functionally addressed CAN packets."""
        return self.addressing_information.rx_packets_functional_ai

    @property
    def tx_packets_functional_ai(self) -> AbstractCanAddressingInformation.PacketAIParamsAlias:
        """Addressing Information parameters of outgoing functionally addressed CAN packets."""
        return self.addressing_information.tx_packets_functional_ai

    @property
    def addressing_information(self) -> AbstractCanAddressingInformation:
        """Addressing Information configuration of a CAN entity."""
        return self.__addressing_information

    @addressing_information.setter
    def addressing_information(self, value: AbstractCanAddressingInformation):
        """
        Set Addressing Information configuration to be used for segmentation and desegmentation.

        :param value: Addressing Information configuration to set.

        :raise TypeError: Provided value has unexpected type.
        """
        if not isinstance(value, AbstractCanAddressingInformation):
            raise TypeError(f"Provided `value` is not CAN Addressing Information type. Actual type: {type(value)}")
        self.__addressing_information: AbstractCanAddressingInformation = value

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
    def dlc(self, value: int):
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
    def use_data_optimization(self, value: bool):
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
    def filler_byte(self, value: int):
        """
        Set value of filler byte to use for CAN Frame Data Padding.

        :param value: Value to set.
        """
        validate_raw_byte(value)
        self.__filler_byte: int = value

    def is_input_packet(self, **kwargs) -> Optional[AddressingType]:
        """
        Check if provided frame attributes belong to a UDS CAN packet which is an input for this CAN Segmenter.

        :param kwargs: Attributes of a CAN frame to check.

        :return: Addressing Type used for transmission of this UDS CAN packet according to the configuration of this
            CAN Segmenter (if provided attributes belongs to an input UDS CAN packet), otherwise None.
        """
        try:
            decoded_frame_ai = CanAddressingInformation.decode_packet_ai(
                addressing_format=self.addressing_format,
                can_id=kwargs["can_id"],
                ai_data_bytes=kwargs["data"][:self.addressing_information.AI_DATA_BYTES_NUMBER])
            decoded_frame_ai.update(can_id=kwargs["can_id"], addressing_format=self.addressing_format)
        except ValueError:
            return None
        if decoded_frame_ai == self.rx_packets_physical_ai:
            return AddressingType.PHYSICAL
        if decoded_frame_ai == self.rx_packets_functional_ai:
            return AddressingType.FUNCTIONAL
        # TODO: make sure it works

    def desegmentation(self, packets: PacketsContainersSequence) -> Union[UdsMessage, UdsMessageRecord]:  # TODO: review
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
            return UdsMessageRecord(packets)  # type: ignore
        if isinstance(packets[0], CanPacket):
            if packets[0].packet_type == CanPacketType.SINGLE_FRAME and len(packets) == 1:
                return UdsMessage(payload=packets[0].payload,  # type: ignore
                                  addressing_type=packets[0].addressing_type)
            if packets[0].packet_type == CanPacketType.FIRST_FRAME:
                payload_bytes: RawBytesList = []
                for packet in packets:
                    if packet.payload is not None:
                        payload_bytes.extend(packet.payload)
                return UdsMessage(payload=payload_bytes[:packets[0].data_length],
                                  addressing_type=packets[0].addressing_type)
            raise SegmentationError("Unexpectedly, something went wrong...")
        raise NotImplementedError(f"Missing implementation for provided CAN Packet: {type(packets[0])}")

    def segmentation(self, message: UdsMessage) -> PacketsTuple:
        """
        Perform segmentation of a diagnostic message.

        :param message: UDS message to divide into UDS packets.

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
        raise NotImplementedError(f"Unknown addressing type received: {message.addressing_type}")

    def is_desegmented_message(self, packets: PacketsContainersSequence) -> bool:  # TODO: review
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
            payload_bytes_found = len(packets[0].payload)  # type: ignore
            for following_packet in packets[1:]:
                if CanPacketType.is_initial_packet_type(following_packet.packet_type):
                    return False
                if payload_bytes_found >= total_payload_size:  # type: ignore
                    return False
                if following_packet.payload is not None:
                    payload_bytes_found += len(following_packet.payload)
            return payload_bytes_found >= total_payload_size  # type: ignore
        raise NotImplementedError(f"Unknown packet type received: {packets[0].packet_type}")

    def __physical_segmentation(self, message: UdsMessage) -> PacketsTuple:  # TODO: rework
        """
        Segment physically addressed diagnostic message.

        :param message: UDS message to divide into UDS packets.

        :raise SegmentationError: Provided diagnostic message cannot be segmented.

        :return: CAN packets that are an outcome of UDS message segmentation.
        """
        message_payload_size = len(message.payload)
        if message_payload_size > CanFirstFrameHandler.MAX_LONG_FF_DL_VALUE:
            raise SegmentationError("Provided diagnostic message cannot be segmented to CAN Packet as it is too big "
                                    "to transmit it over CAN bus.")
        if message_payload_size <= CanSingleFrameHandler.get_max_payload_size(addressing_format=self.addressing_format,
                                                                              dlc=self.dlc):
            single_frame = CanPacket(packet_type=CanPacketType.SINGLE_FRAME,
                                     payload=message.payload,
                                     filler_byte=self.filler_byte,
                                     dlc=None if self.use_data_optimization else self.dlc,
                                     **self.physical_ai)
            return (single_frame,)
        ff_payload_size = CanFirstFrameHandler.get_payload_size(
            addressing_format=self.addressing_format,
            dlc=self.dlc,
            long_ff_dl_format=message_payload_size > CanFirstFrameHandler.MAX_SHORT_FF_DL_VALUE)
        first_frame = CanPacket(packet_type=CanPacketType.FIRST_FRAME,
                                payload=message.payload[:ff_payload_size],
                                dlc=self.dlc,
                                data_length=message_payload_size,
                                **self.physical_ai)
        cf_payload_size = CanConsecutiveFrameHandler.get_max_payload_size(addressing_format=self.addressing_format,
                                                                          dlc=self.dlc)
        total_cfs_number = (message_payload_size - ff_payload_size + cf_payload_size - 1) // cf_payload_size
        consecutive_frames = []
        for cf_index in range(total_cfs_number):
            sequence_number = (cf_index + 1) % 0x10
            payload_i_start = ff_payload_size + cf_index * cf_payload_size
            payload_i_stop = payload_i_start + cf_payload_size
            consecutive_frame = CanPacket(packet_type=CanPacketType.CONSECUTIVE_FRAME,
                                          payload=message.payload[payload_i_start: payload_i_stop],
                                          dlc=None if self.use_data_optimization and cf_index == total_cfs_number - 1
                                          else self.dlc,
                                          sequence_number=sequence_number,
                                          filler_byte=self.filler_byte,
                                          **self.physical_ai)
            consecutive_frames.append(consecutive_frame)
        return (first_frame, *consecutive_frames)

    def __functional_segmentation(self, message: UdsMessage) -> PacketsTuple:  # TODO: rework
        """
        Segment functionally addressed diagnostic message.

        :param message: UDS message to divide into UDS packets.

        :raise SegmentationError: Provided diagnostic message cannot be segmented.

        :return: CAN packets that are an outcome of UDS message segmentation.
        """
        max_payload_size = CanSingleFrameHandler.get_max_payload_size(addressing_format=self.addressing_format,
                                                                      dlc=self.dlc)
        message_payload_size = len(message.payload)
        if message_payload_size > max_payload_size:
            raise SegmentationError("Provided diagnostic message cannot be segmented using functional addressing "
                                    "as it will not fit into a Single Frame.")
        single_frame = CanPacket(packet_type=CanPacketType.SINGLE_FRAME,
                                 payload=message.payload,
                                 filler_byte=self.filler_byte,
                                 dlc=None if self.use_data_optimization else self.dlc,
                                 **self.functional_ai)
        return (single_frame,)

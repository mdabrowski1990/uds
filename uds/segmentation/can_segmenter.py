"""Segmentation specific for CAN bus."""

__all__ = ["CanSegmenter"]

from typing import Optional, Union, Tuple, Dict, Type
from copy import copy

from uds.utilities import RawByte, validate_raw_byte, AmbiguityError
from uds.transmission_attributes import AddressingType, AddressingTypeAlias
from uds.can import CanAddressingInformationHandler, CanAddressingFormat, CanAddressingFormatAlias, \
    CanDlcHandler, CanIdHandler, CanSingleFrameHandler, CanFirstFrameHandler, CanConsecutiveFrameHandler, \
    DEFAULT_FILLER_BYTE
from uds.packet import CanPacket, CanPacketRecord, CanPacketType, PacketAlias, PacketsSequence, PacketsDefinitionTuple
from uds.message import UdsMessage, UdsMessageRecord
from .abstract_segmenter import AbstractSegmenter, SegmentationError


AIArgsAlias = Dict[str, Optional[Union[int, RawByte]]]
"""Alias of Addressing Information arguments to configure CAN Segmenter communication model."""
AIParamsAlias = Dict[str, Optional[Union[int, RawByte, AddressingTypeAlias]]]
"""Alias of Addressing Information parameters used by CAN Segmenter for each communication model."""


class CanSegmenter(AbstractSegmenter):
    """Segmenter class that provides utilities for segmentation and desegmentation on CAN bus."""

    def __init__(self, *,
                 addressing_format: CanAddressingFormatAlias,
                 physical_ai: Optional[AIArgsAlias] = None,
                 functional_ai: Optional[AIArgsAlias] = None,
                 dlc: int = CanDlcHandler.MIN_BASE_UDS_DLC,
                 use_data_optimization: bool = False,
                 filler_byte: RawByte = DEFAULT_FILLER_BYTE) -> None:
        """
        Configure CAN Segmenter.

        :param addressing_format: CAN Addressing format used.
        :param physical_ai: CAN Addressing Information parameters to use for physically addressed communication.
            Leave None if the segmenter will not be used for segmenting physically addressed messages.
        :param functional_ai: CAN Addressing Information parameters to use for functionally addressed communication.
            Leave None if the segmenter will not be used for segmenting functionally addressed messages.
        :param dlc: Base CAN DLC value to use for CAN Packets.
        :param use_data_optimization: Information whether to use CAN Frame Data Optimization during segmentation.
        :param filler_byte: Filler byte value to use for CAN Frame Data Padding during segmentation.
        """
        CanAddressingFormat.validate_member(addressing_format)
        self.__addressing_format: CanAddressingFormatAlias = CanAddressingFormat(addressing_format)
        self.physical_ai = physical_ai
        self.functional_ai = functional_ai
        self.dlc = dlc
        self.use_data_optimization = use_data_optimization
        self.filler_byte = filler_byte

    @property
    def supported_packet_classes(self) -> tuple[Type[PacketAlias], ...]:
        """Classes that define packet objects supported by this segmenter."""
        return CanPacket, CanPacketRecord

    @property
    def addressing_format(self) -> CanAddressingFormatAlias:
        """CAN Addressing format used."""
        return self.__addressing_format

    @property
    def physical_ai(self) -> Optional[AIParamsAlias]:
        """
        CAN Addressing Information parameters used for physically addressed communication.

        None if physically addressed communication parameters are not configured.
        """
        return copy(self.__physical_ai)

    @physical_ai.setter
    def physical_ai(self, value: Optional[AIArgsAlias]):
        """
        Set value of CAN Addressing Information parameters to use for physically addressed communication.

        :param value: Value to set.
        """
        if value is None:
            self.__physical_ai: Optional[AIParamsAlias] = None
        else:
            CanAddressingInformationHandler.validate_ai(
                addressing_format=self.addressing_format,
                addressing_type=AddressingType.PHYSICAL,
                **value)
            self.__physical_ai: Optional[AIParamsAlias] = copy(value)
            self.__physical_ai.update(
                addressing_format=self.addressing_format,
                **{CanAddressingInformationHandler.ADDRESSING_TYPE_NAME: AddressingType.PHYSICAL})

    @property
    def functional_ai(self) -> AIParamsAlias:
        """
        CAN Addressing Information parameters used for functionally addressed communication.

        None if functionally addressed communication parameters are not configured.
        """
        return copy(self.__functional_ai)

    @functional_ai.setter
    def functional_ai(self, value: Optional[AIArgsAlias]):
        """
        Set value of CAN Addressing Information parameters to use for functionally addressed communication.

        :param value: Value to set.
        """
        if value is None:
            self.__functional_ai: Optional[AIParamsAlias] = None
        else:
            CanAddressingInformationHandler.validate_ai(
                addressing_format=self.addressing_format,
                addressing_type=AddressingType.FUNCTIONAL,
                **value)
            self.__functional_ai: Optional[AIParamsAlias] = copy(value)
            self.__functional_ai.update(
                addressing_format=self.addressing_format,
                **{CanAddressingInformationHandler.ADDRESSING_TYPE_NAME: AddressingType.FUNCTIONAL})

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
        """
        CanDlcHandler.validate_dlc(value)
        self.__dlc: int = value

    @property
    def use_data_optimization(self) -> bool:
        """Information whether to use CAN Frame Data Optimization for CAN Packet created during segmentation."""
        return self.__use_data_optimization

    @use_data_optimization.setter
    def use_data_optimization(self, value: bool):
        """
        Set whether to use CAN Frame Data Optimization for CAN Packet created during segmentation.

        :param value: Value to set.
        """
        self.__use_data_optimization: bool = bool(value)

    @property
    def filler_byte(self) -> RawByte:
        """Filler byte value to use for CAN Frame Data Padding during segmentation."""
        return self.__filler_byte

    @filler_byte.setter
    def filler_byte(self, value: RawByte):
        """
        Set value of filler byte to use for CAN Frame Data Padding.

        :param value: Value to set.
        """
        validate_raw_byte(value)
        self.__filler_byte: RawByte = value

    def desegmentation(self, packets: PacketsSequence) -> Union[UdsMessage, UdsMessageRecord]:
        """
        Perform desegmentation of CAN packets.

        :param packets: CAN packets to desegment into UDS message.

        :raise SegmentationError: Provided packets are not a complete packets sequence that form a diagnostic message.
        :raise NotImplementedError: There is missing implementation for the provided CAN Packets.
            Please create an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            with detailed description if you face this error.

        :return: A diagnostic message that is an outcome of CAN packets desegmentation.
        """
        if not self.is_complete_packets_sequence(packets):
            raise SegmentationError("Provided packets are not a complete packets sequence")
        if isinstance(packets[0], CanPacketRecord):
            return UdsMessageRecord(packets)
        if isinstance(packets[0], CanPacket):
            if packets[0].packet_type == CanPacketType.SINGLE_FRAME and len(packets) == 1:
                return UdsMessage(payload=packets[0].payload, addressing_type=packets[0].addressing_type)
            if packets[0].packet_type == CanPacketType.FIRST_FRAME:
                payload_bytes = []
                for packet in packets:
                    if packet.payload is not None:
                        payload_bytes.extend(packet.payload)
                return UdsMessage(payload=payload_bytes[:packets[0].data_length],
                                  addressing_type=packets[0].addressing_type)
            raise SegmentationError("Unexpectedly, something went wrong...")
        raise NotImplementedError(f"Missing implementation for provided CAN Packet: {type(packets[0])}")

    def segmentation(self, message: UdsMessage) -> PacketsDefinitionTuple:
        """
        Perform segmentation of a diagnostic message.

        :param message: UDS message to divide into UDS packets.

        :raise TypeError: Provided value is not instance of UdsMessage class.
        :raise AmbiguityError: Segmentation cannot be completed because CAN Segmenter is not properly configured.
        :raise NotImplementedError: There is missing implementation for the Addressing Type used by provided message.
            Please create an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            with detailed description if you face this error.

        :return: CAN packets that are an outcome of UDS message segmentation.
        """
        if not isinstance(message, UdsMessage):
            raise TypeError(f"Provided value is not instance of UdsMessage class. Actual type: {type(message)}")
        if message.addressing_type == AddressingType.PHYSICAL:
            if self.physical_ai is None:
                raise AmbiguityError("Provided diagnostic message cannot be segmented as physical addressing "
                                     "information are not configured.")
            return self.__physical_segmentation(message)
        if message.addressing_type == AddressingType.FUNCTIONAL:
            if self.functional_ai is None:
                raise AmbiguityError("Provided diagnostic message cannot be segmented as functional addressing "
                                     "information are not configured.")
            return self.__functional_segmentation(message)
        raise NotImplementedError(f"Unknown addressing type received: {message.addressing_type}")

    def is_complete_packets_sequence(self, packets: PacketsSequence) -> bool:
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
        if not self.is_supported_packets_sequence(packets):
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

    def __physical_segmentation(self, message: UdsMessage) -> PacketsDefinitionTuple:
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
        max_sf_payload_size = CanSingleFrameHandler.get_max_payload_size(addressing_format=self.addressing_format,
                                                                         dlc=self.dlc)
        if message_payload_size <= max_sf_payload_size:
            sf = CanPacket(packet_type=CanPacketType.SINGLE_FRAME,
                           payload=message.payload,
                           filler_byte=self.filler_byte,
                           dlc=None if self.use_data_optimization else self.dlc,
                           **self.physical_ai)

            return sf,
        is_long_ff_dl_format_used = message_payload_size > CanFirstFrameHandler.MAX_SHORT_FF_DL_VALUE
        ff_payload_size = CanFirstFrameHandler.get_payload_size(addressing_format=self.addressing_format,
                                                                dlc=self.dlc,
                                                                long_ff_dl_format=is_long_ff_dl_format_used)
        ff = CanPacket(packet_type=CanPacketType.FIRST_FRAME,
                       payload=message.payload[:ff_payload_size],
                       dlc=self.dlc,
                       data_length=message_payload_size,
                       **self.physical_ai)
        cf_payload_size = CanConsecutiveFrameHandler.get_max_payload_size(addressing_format=self.addressing_format,
                                                                          dlc=self.dlc)
        total_cf_number = (message_payload_size - ff_payload_size + cf_payload_size - 1) // cf_payload_size
        cfs = []
        for cf_index in range(total_cf_number):
            sequence_number = (cf_index + 1) % 0x10
            payload_i_start = ff_payload_size + cf_index*cf_payload_size
            payload_i_stop = payload_i_start + cf_payload_size
            cf = CanPacket(packet_type=CanPacketType.CONSECUTIVE_FRAME,
                           payload=message.payload[payload_i_start: payload_i_stop],
                           dlc=None if self.use_data_optimization and cf_index == total_cf_number-1 else self.dlc,
                           sequence_number=sequence_number,
                           filler_byte=self.filler_byte,
                           **self.physical_ai)
            cfs.append(cf)
        return ff, *cfs

    def __functional_segmentation(self, message: UdsMessage) -> PacketsDefinitionTuple:
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
        sf = CanPacket(packet_type=CanPacketType.SINGLE_FRAME,
                       payload=message.payload,
                       filler_byte=self.filler_byte,
                       dlc=None if self.use_data_optimization else self.dlc,
                       **self.functional_ai)
        return sf,

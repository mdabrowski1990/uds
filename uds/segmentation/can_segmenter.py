"""Segmentation specific for CAN bus."""

__all__ = ["CanSegmenter"]

from typing import Optional, Union, Tuple, Dict, Type

from uds.utilities import RawByte, AmbiguityError
from uds.transmission_attributes import AddressingType, AddressingTypeAlias
from uds.can import CanAddressingFormat, CanAddressingFormatAlias, CanDlcHandler, CanIdHandler, DEFAULT_FILLER_BYTE
from uds.packet import CanPacket, CanPacketRecord, PacketAlias, PacketsSequence, PacketsDefinitionTuple
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

    @property
    def supported_packet_classes(self) -> tuple[Type[PacketAlias], ...]:
        """Classes that define packet objects supported by this segmenter."""
        return CanPacket, CanPacketRecord

    @property
    def addressing_format(self) -> CanAddressingFormatAlias:
        """CAN Addressing format used."""

    @property
    def physical_ai(self) -> Optional[AIParamsAlias]:
        """
        CAN Addressing Information parameters used for physically addressed communication.

        None if physically addressed communication parameters are not configured.
        """

    @physical_ai.setter
    def physical_ai(self, value: Optional[AIArgsAlias]):
        """
        Set value of CAN Addressing Information parameters to use for physically addressed communication.

        :param value: Value to set.
        """

    @property
    def functional_ai(self) -> AIParamsAlias:
        """
        CAN Addressing Information parameters used for functionally addressed communication.

        None if functionally addressed communication parameters are not configured.
        """

    @functional_ai.setter
    def functional_ai(self, value: Optional[AIArgsAlias]):
        """
        Set value of CAN Addressing Information parameters to use for functionally addressed communication.

        :param value: Value to set.
        """

    @property
    def dlc(self) -> int:
        """
        Value of base CAN DLC to use for CAN Packets.

        .. note:: All output CAN Packets (created by :meth:`~uds.segmentation.can_segmenter.CanSegmenter.segmentation`)
            will have this DLC value set unless
            :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>` is used.
        """

    @dlc.setter
    def dlc(self, value: int):
        """
        Set value of base CAN DLC to use for CAN Packets.

        :param value: Value to set.
        """

    @property
    def use_data_optimization(self) -> bool:
        """Information whether to use CAN Frame Data Optimization for CAN Packet created during segmentation."""

    @use_data_optimization.setter
    def use_data_optimization(self, value: bool):
        """
        Set whether to use CAN Frame Data Optimization for CAN Packet created during segmentation.

        :param value: Value to set.
        """

    @property
    def filler_byte(self) -> RawByte:
        """Filler byte value to use for CAN Frame Data Padding during segmentation."""

    @filler_byte.setter
    def filler_byte(self, value: RawByte):
        """
        Set value of filler byte to use for CAN Frame Data Padding.

        :param value: Value to set.
        """

    def is_following_packets_sequence(self, packets: PacketsSequence) -> bool:
        """
        Check whether provided packets are a sequence of following CAN packets.

        .. note:: This function will return True under following conditions:

            - a sequence of packets was provided
            - the first packet in the sequence is an initial packet
            - no other packet in the sequence is an initial packet
            - each packet (except the first one) is a consecutive packet for the previous packet in the sequence
              or controlling the flow of packets

        :param packets: Packets sequence to check.

        :return: True if the provided packets are a sequence of following packets, otherwise False.
        """

    def is_complete_packets_sequence(self, packets: PacketsSequence) -> bool:
        """
        Check whether provided packets are full sequence of packets that form exactly one diagnostic message.

        :param packets: Packets sequence to check.

        :return: True if the packets form exactly one diagnostic message.
            False if there are missing, additional or inconsistent (e.g. two packets that initiate a message) packets.
        """

    def get_consecutive_packets_number(self, first_packet: PacketAlias) -> int:
        """
        Get number of consecutive packets that must follow this packet to fully store a diagnostic message.

        :param first_packet: The first packet of a segmented diagnostic message.

        :raise ValueError: Provided value is not an an initial packet.

        :return: Number of following packets that together carry a diagnostic message.
        """

    def segmentation(self, message: UdsMessage) -> PacketsDefinitionTuple:
        """
        Perform segmentation of a diagnostic message.

        :param message: UDS message to divide into UDS packets.

        :raise SegmentationError: Provided diagnostic message cannot be segmented.
        :raise AmbiguityError: Segmentation cannot be completed because CAN Segmenter is not configured.

        :return: CAN packets that are an outcome of UDS message segmentation.
        """

    def desegmentation(self, packets: PacketsSequence) -> Union[UdsMessage, UdsMessageRecord]:
        """
        Perform desegmentation of CAN packets.

        :param packets: CAN packets to desegment into UDS message.

        :raise SegmentationError: Provided packets are not a complete packet sequence that form a diagnostic message.

        :return: A diagnostic message that is an outcome of CAN packets desegmentation.
        """

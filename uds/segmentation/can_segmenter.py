"""Segmentation specific for CAN bus."""

__all__ = ["CanSegmenter"]

from typing import Optional, Union, Tuple, Type

from uds.utilities import RawByte
from uds.can import CanAddressingFormat, CanAddressingFormatAlias, DEFAULT_FILLER_BYTE
from uds.packet import CanPacket, CanPacketRecord, PacketAlias, PacketsSequence, PacketsDefinitionTuple
from uds.message import UdsMessage, UdsMessageRecord
from .abstract_segmenter import AbstractSegmenter, SegmentationError


class CanSegmenter(AbstractSegmenter):
    """Segmenter class that provides utilities for segmentation and desegmentation on CAN bus."""

    def __init__(self, *,
                 addressing_format: CanAddressingFormatAlias,
                 dlc: int,
                 use_data_optimization: bool = False,
                 filler_byte: RawByte = DEFAULT_FILLER_BYTE,
                 physical_can_id: Optional[int] = None,
                 physical_target_address: Optional[RawByte] = None,
                 physical_source_address: Optional[RawByte] = None,
                 physical_extension_address: Optional[RawByte] = None,
                 functional_can_id: Optional[int] = None,
                 functional_target_address: Optional[RawByte] = None,
                 functional_source_address: Optional[RawByte] = None,
                 functional_extension_address: Optional[RawByte] = None) -> None:
        """
        Configure CAN segmenter.

        :param addressing_format: CAN addressing format to use.
        :param dlc: Maximal value of DLC to use
        :param use_data_optimization: TODO
        :param filler_byte: TODO
        :param physical_can_id: TODO
        :param physical_target_address: TODO
        :param physical_source_address: TODO
        :param physical_extension_address: TODO
        :param functional_can_id: TODO
        :param functional_target_address: TODO
        :param functional_source_address: TODO
        :param functional_extension_address: TODO
        """

    @property
    def supported_packet_classes(self) -> tuple[Type[PacketAlias], ...]:
        """Classes that define packet objects supported by this segmenter."""
        return CanPacket, CanPacketRecord

    def is_following_packets_sequence(self, packets: PacketsSequence) -> bool:
        ...

    def is_complete_packets_sequence(self, packets: PacketsSequence) -> bool:
        ...

    def get_consecutive_packets_number(self, first_packet: PacketAlias) -> int:
        ...

    def segmentation(self, message: UdsMessage) -> PacketsDefinitionTuple:
        ...

    def desegmentation(self, packets: PacketsSequence) -> Union[UdsMessage, UdsMessageRecord]:
        ...

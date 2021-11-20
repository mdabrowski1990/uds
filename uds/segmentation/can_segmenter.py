"""Segmentation specific for CAN bus."""

__all__ = ["CanSegmenter"]

from typing import Tuple, Type

from uds.packet import CanPacket, CanPacketRecord, PacketAlias
from .abstract_segmenter import AbstractSegmenter, SegmentationError


class CanSegmenter(AbstractSegmenter):
    """Segmenter class that provides utilities for segmentation and desegmentation on CAN bus."""

    def __init__(self, addressing_format, dlc,
                 physical_can_id, physical_target_address, physical_source_address, physical_extension_address,
                 functional_can_id, functional_target_address, functional_source_address, functional_extension_address,
                 ) -> None:  # TODO
        ...

    @property
    def supported_packet_classes(self) -> tuple[Type[PacketAlias], ...]:
        """Classes that define packet objects supported by this segmenter."""
        return CanPacket, CanPacketRecord


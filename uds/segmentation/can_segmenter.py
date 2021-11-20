"""Segmentation specific for CAN bus."""

__all__ = ["CanSegmenter"]

from typing import Tuple, Type

from uds.packet import CanPacket, CanPacketRecord, PacketAlias
from .abstract_segmenter import AbstractSegmenter, SegmentationError


class CanSegmenter(AbstractSegmenter):
    """Segmenter class that provides utilities for segmentation and desegmentation on CAN bus."""

    @property
    def supported_packet_classes(self) -> tuple[Type[PacketAlias], ...]:
        """Classes that define packet objects supported by this segmenter."""
        return CanPacket, CanPacketRecord


"""Common definition of segmentation and desegmentation executors."""

__all__ = ["AbstractSegmenter"]

from abc import ABC, abstractmethod

from uds.messages import UdsMessage, PacketsTuple, PacketsSequence


class AbstractSegmenter(ABC):
    """Abstract definition of TODO"""

    @abstractmethod
    def segmentation(self, message: UdsMessage) -> PacketsTuple:
        ...

    @abstractmethod
    def desegmentation(self, packets: PacketsSequence) -> UdsMessage:
        ...

"""Definition of API for segmentation and desegmentation strategies."""

__all__ = ["SegmentationError", "AbstractSegmenter"]

from typing import Tuple, Type, Union, Any
from abc import ABC, abstractmethod

from uds.message import UdsMessage, UdsMessageRecord
from uds.packet import PacketAlias, PacketsSequence, PacketsDefinitionTuple


class SegmentationError(ValueError):
    """UDS segmentation or desegmentation process cannot be completed due to input data inconsistency."""


class AbstractSegmenter(ABC):
    """
    Abstract definition of a segmenter class.

    Segmenter classes defines UDS segmentation and desegmentation duties.
    They contain helper methods that are essential for successful
    :ref:`segmentation <knowledge-base-message-segmentation>` and
    :ref:`desegmentation <knowledge-base-packets-desegmentation>` execution.

    .. note:: Each concrete segmenter class handles exactly one bus.
    """

    @abstractmethod
    def supported_packet_classes(self) -> Tuple[Type[PacketAlias], ...]:
        """Classes that define packet objects supported by this segmenter."""

    def is_supported_packet(self, value: Any) -> bool:
        """
        Check if the argument value is a packet object of a supported type.

        :param value: Value to check.

        :return: True if provided value is an object of a supported packet type, False otherwise.
        """
        return isinstance(value, self.supported_packet_classes)  # type: ignore

    def is_supported_packets_sequence(self, value: Any) -> bool:
        """
        Check if the argument value is a packet sequence of a supported type.

        :param value: Value to check.

        :return: True if provided value is a packet sequence of a supported type, False otherwise.
        """
        if not isinstance(value, (list, tuple)):
            # not a sequence
            return False
        if not all(self.is_supported_packet(element) for element in value):
            # at least one element is not a packet of a supported type
            return False
        # check if all packets are the same type
        return len({type(element) for element in value}) == 1

    @abstractmethod
    def is_complete_packets_sequence(self, packets: PacketsSequence) -> bool:
        """
        Check whether provided packets are full sequence of packets that form exactly one diagnostic message.

        :param packets: Packets sequence to check.

        :return: True if the packets form exactly one diagnostic message.
            False if there are missing, additional or inconsistent (e.g. two packets that initiate a message) packets.
        """

    @abstractmethod
    def desegmentation(self, packets: PacketsSequence) -> Union[UdsMessage, UdsMessageRecord]:
        """
        Perform desegmentation of UDS packets.

        :param packets: UDS packets to desegment into UDS message.

        :raise SegmentationError: Provided packets are not a complete packet sequence that form a diagnostic message.

        :return: A diagnostic message that is an outcome of UDS packets desegmentation.
        """

    @abstractmethod
    def segmentation(self, message: UdsMessage) -> PacketsDefinitionTuple:
        """
        Perform segmentation of a diagnostic message.

        :param message: UDS message to divide into UDS packets.

        :raise SegmentationError: Provided diagnostic message cannot be segmented.

        :return: UDS packets that are an outcome of UDS message segmentation.
        """

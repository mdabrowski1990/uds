"""
Definition of API for segmentation and desegmentation strategies.

:ref:`Segmentation <knowledge-base-segmentation>` defines two processes:
 - :ref:`diagnostic message segmentation <knowledge-base-message-segmentation>`
 - :ref:`packets desegmentation <knowledge-base-packets-desegmentation>`
"""

__all__ = ["SegmentationError", "AbstractSegmenter"]

from typing import Tuple, Union, Any
from abc import ABC, abstractmethod

from uds.message import UdsMessage, UdsMessageRecord
from .abstract_packet import PacketAlias, PacketsSequence, PacketsDefinitionTuple


class SegmentationError(ValueError):
    """UDS segmentation or desegmentation process cannot be completed due to input data inconsistency."""


class AbstractSegmenter(ABC):
    """
    Abstract definition of a segmenter class.

    Segmenter classes defines UDS segmentation and desegmentation
    `strategies <https://www.tutorialspoint.com/design_pattern/strategy_pattern.htm>`_.
    They contain helper methods that are essential for successful
    :ref:`segmentation <knowledge-base-message-segmentation>` and
    :ref:`desegmentation <knowledge-base-packets-desegmentation>` execution.

    .. note:: Each concrete segmenter class handles exactly one bus.
    """

    @property
    @abstractmethod
    def supported_packet_classes(self) -> Tuple[type]:
        """Classes that define packet objects supported by this segmenter."""

    def is_supported_packet(self, value: Any) -> bool:
        """
        Check if the argument value is a packet object of a supported type.

        :param value: Value to check.

        :return: True if provided value is an object of a supported packet type, False otherwise.
        """
        return isinstance(value, self.supported_packet_classes)

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
    def is_following_packets_sequence(self, packets: PacketsSequence) -> bool:
        """
        Check whether provided packets are a sequence of following packets.

        .. note:: This function will return True under following conditions:

            - a sequence of packets was provided
            - the first packet in the sequence is an initial packet
            - no other packet in the sequence is an initial packet
            - each packet (except the first one) is a consecutive packet for the previous packet in the sequence

        :param packets: Packets sequence to check.

        :raise ValueError: Provided value is not a packets sequence of a supported type.

        :return: True if the provided packets are a sequence of following packets, otherwise False.
        """

    def is_complete_packets_sequence(self, packets: PacketsSequence) -> bool:
        """
        Check whether provided packets are full sequence of packets that form exactly one diagnostic message.

        :param packets: Packets sequence to check.

        :return: True if the packets form exactly one diagnostic message.
            False if there are missing, additional or inconsistent (e.g. two packets that initiate a message) packets.
        """
        return self.is_following_packets_sequence(packets) and \
            self.get_consecutive_packets_number(packets[0]) == len(packets)

    @abstractmethod
    def get_consecutive_packets_number(self, first_packet: PacketAlias) -> int:  # noqa: F841
        """
        Get number of consecutive packets that must follow this packet to fully store a diagnostic message.

        :param first_packet: The first packet of a segmented diagnostic message.

        :raise ValueError: Provided value is not an an initial packet.

        :return: Number of following packets that together carry a diagnostic message.
        """

    @abstractmethod
    def segmentation(self, message: UdsMessage) -> PacketsDefinitionTuple:  # noqa: F841
        """
        Perform segmentation of a diagnostic message.

        :param message: UDS message to divide into UDS packets.

        :raise TypeError: Provided 'message' argument is not :class:`~uds.message.uds_message.UdsMessage` type.

        :return: UDS packets that are an outcome of UDS message segmentation.
        """

    @abstractmethod
    def desegmentation(self, packets: PacketsSequence) -> Union[UdsMessage, UdsMessageRecord]:
        """
        Perform desegmentation of UDS packets.

        :param packets: UDS packets to desegment into UDS message.

        :raise SegmentationError: Provided packets are not a complete packet sequence that form a diagnostic message.

        :return: A diagnostic message that is an outcome of UDS packets desegmentation.
        """

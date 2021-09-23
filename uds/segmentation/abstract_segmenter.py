"""Definition of API for segmentation and desegmentation strategies."""

__all__ = ["SegmentationError", "AbstractSegmenter"]

from typing import Tuple, Union, Any
from abc import ABC, abstractmethod

from uds.messages import UdsMessage, UdsMessageRecord, \
    PacketTyping, PacketsSequence, PacketsDefinitionTuple, PacketTypesTuple


class SegmentationError(ValueError):
    """UDS segmentation or desegmentation process cannot be completed due to input data inconsistency."""


class AbstractSegmenter(ABC):
    """
    Abstract definition of a segmenter class.

    Segmenter classes defines UDS segmentation and desegmentation
    `strategies <https://www.tutorialspoint.com/design_pattern/strategy_pattern.htm>`_.
    They contain helper methods that are essential for successful segmentation and desegmentation execution.
    Each concrete segmenter class handles a single bus.
    """

    @property
    @abstractmethod
    def supported_packet_classes(self) -> Tuple[type]:
        """Classes that define packet objects supported by this segmenter."""

    @property
    @abstractmethod
    def initial_packet_types(self) -> PacketTypesTuple:
        """Types of packets that initiates a diagnostic message transmission for handled bys."""
        ...

    def is_supported_packet(self, value: Any) -> bool:
        """
        Check if the argument value is a packet object of a supported type.

        :param value: Value to check.

        :return: True if provided value is an object of a supported packet type, False otherwise.
        """
        # TODO: tests and code

    def _validate_packet(self, packet: PacketTyping) -> None:
        """
        Validate whether the argument contains an object of a supported packet type.

        :param packet: Packet object to check.

        :raise TypeError: Provided value is not an object of a supported packet type.
        """
        # TODO: tests and code
        # if not self._is_supported_packet(value=packet):
        #     raise TypeError(f"Provided value is not supported packet type. Actual value: {packet}.")

    def is_supported_packets_sequence(self, value: Any) -> bool:
        """
        Check if the argument value is a packet sequence of a supported type.

        :param value: Value to check.

        :return: True if provided value is a packet sequence of a supported type, False otherwise.
        """
        # TODO: tests and code

    def _validate_packets_sequence(self, packets: PacketsSequence) -> None:
        """
        Validate whether the argument contains a packet sequence of a supported type.

        :param packets: Packet sequence to check.

        :raise TypeError: Provided value is not an object of a supported packet type.
        """
        # TODO: tests and code

    def is_initial_packet(self, packet: PacketTyping) -> bool:
        """
        Check whether a provided packet initiates a diagnostic message.

        :param packet: Packet to check.

        :raise TypeError: TODO

        :return: True if the packet is the only or the first packet of a diagnostic message.
        """
        # TODO: tests and code

    @abstractmethod
    def get_consecutive_packets_number(self, first_packet: PacketTyping) -> int:  # type: ignore
        """
        Get number of consecutive packets that must follow this packet to fully store a diagnostic message.

        :param first_packet: The first packet of a segmented diagnostic message.

        :return: Number of following packets that together carry a diagnostic message.
        """
        # TODO: tests and code

    @abstractmethod
    def is_following_packets_sequence(self, packets: PacketsSequence) -> bool:
        """
        Check whether provided packets are a sequence of following packets that might form a diagnostic message.

        :param packets: Packets sequence to check.

        :return: True if the packets are
        """

    @abstractmethod
    def is_complete_packets_sequence(self, packets: PacketsSequence) -> bool:  # type: ignore
        """
        Check whether provided packets are full sequence of packets that form exactly one diagnostic message.

        :param packets: Packets sequence to check.

        :return: True if the packets form exactly one diagnostic message.
            False if there are missing, additional or inconsistent (e.g. two packets that initiate a message) packets.
        """
        # TODO: tests and code

    @abstractmethod
    def segmentation(self, message: UdsMessage) -> PacketsDefinitionTuple:  # type: ignore
        """
        Perform diagnostic message segmentation.

        :param message: UDS message to divide into UDS packets.

        :raise TypeError: Provided 'message' argument is not :class:`~uds.messages.uds_message.UdsMessage` type.

        :return: UDS packets that are the outcome of UDS message segmentation.
        """
        if not isinstance(message, UdsMessage):
            raise TypeError(f"Provided value is not UdsMessage type. Actual value: {message}.")

    @abstractmethod
    def desegmentation(self, packets: PacketsSequence) -> Union[UdsMessage, UdsMessageRecord]:  # type: ignore
        """
        Perform diagnostic message desegmentation.

        :param packets: UDS packets to desegment into UDS message.

        :raise SegmentationError: Provided packets are not a complete packets set that form a diagnostic message.

        :return: Diagnostic message created from received packets.
        """
        # TODO: tests and code

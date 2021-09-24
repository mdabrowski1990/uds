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
        """Types of packets that initiates a diagnostic message transmission for the managed bus."""

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

    def is_initial_packet(self, packet: PacketTyping) -> bool:
        """
        Check whether a provided packet initiates a diagnostic message.

        :param packet: Packet to check.

        :raise TypeError: Provided value is not an object of a supported packet type.

        :return: True if the packet is the only or the first packet of a diagnostic message.
        """
        if not self.is_supported_packet(packet):
            raise TypeError(f"Provided value is not a packet object that is supported by this Segmenter. "
                            f"Actual value: {packet}.")
        return packet.packet_type in self.initial_packet_types

    @abstractmethod
    def get_consecutive_packets_number(self, first_packet: PacketTyping) -> int:  # type: ignore
        """
        Get number of consecutive packets that must follow this packet to fully store a diagnostic message.

        :param first_packet: The first packet of a segmented diagnostic message.

        :raise ValueError: Provided value is not an an initial packet.

        :return: Number of following packets that together carry a diagnostic message.
        """
        if not self.is_initial_packet(first_packet):
            raise ValueError(f"Provided value is not an initial packet of a type supported by this Segmenter. "
                             f"Actual value: {first_packet}.")

    @abstractmethod
    def is_following_packets_sequence(self, packets: PacketsSequence) -> bool:  # type: ignore
        """
        Check whether provided packets are a sequence of following packets.

        Note: This function will return True under following conditions:
         - a sequence of packets was provided
         - the first packet in the sequence is an initial packet
         - no other packet in the sequence is an initial packet
         - each packet (except the first one) is a consecutive packet for the previous packet in the sequence

        :param packets: Packets sequence to check.

        :raise ValueError: Provided value is not a packets sequence of a supported type.

        :return: True if the provided packets are a sequence of following packets, otherwise False.
        """
        if not self.is_supported_packets_sequence(packets):
            raise ValueError(f"Provided value is not a packets sequence of a supported type."
                             f"Actual value: {packets}.")
        if not self.is_initial_packet(packets[0]):
            return False

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

        :raise SegmentationError: Provided packets are not a complete packet sequence that form a diagnostic message.

        :return: Diagnostic message created from received packets.
        """
        if not self.is_complete_packets_sequence(packets):
            raise SegmentationError(f"Provided packets are not a complete that form a diagnostic message. "
                                    f"Actual value: {packets}.")

"""Definition of API for segmentation and desegmentation strategies."""

__all__ = ["SegmentationError", "AbstractSegmenter"]

from typing import Union, Any
from abc import ABC, abstractmethod

from uds.messages import UdsMessage, UdsMessageRecord, AbstractUdsPacket, AbstractUdsPacketRecord, \
    PacketTyping, PacketsSequence, PacketsDefinitionTuple


class SegmentationError(ValueError):
    """UDS segmentation or desegmentation process cannot be completed due to input data inconsistency."""


class AbstractSegmenter(ABC):
    """
    Abstract definition of segmenter class.

    Segmenters are classes with UDS segmentation and desegmentation
    `strategies <https://www.tutorialspoint.com/design_pattern/strategy_pattern.htm>`_.
    They contain helper methods that are essential for successful segmentation and desegmentation execution.
    """

    @abstractmethod
    def _is_supported_packet(self, value: Any) -> bool:
        """
        Check if the argument value is a packet object of a supported type.

        :param value: Value to check.

        :return: True if provided value is an object of a supported packet type, False otherwise.
        """

    def _validate_packet(self, packet: PacketTyping) -> None:
        """
        Validate whether the argument value contains an object of a supported packet type.

        :param packet: Value to check.

        :raise TypeError: Provided value is not an object of a supported packet type.
        """
        # TODO: continue here - Unit Tests, docstrings, etc
        # if not self._is_supported_packet(value=packet):
        #     raise TypeError(f"Provided value is not supported packet type. Actual value: {packet}.")

    @abstractmethod
    def _is_supported_packets_sequence(self, packets: PacketsSequence) -> bool:
        """
        Check
        :param packets:
        :return:
        """

    @abstractmethod
    def _validate_packets_sequence(self, packets: PacketsSequence) -> None:
        ...

    @abstractmethod
    def is_first_packet(self, packet: PacketTyping) -> bool:  # type: ignore
        """
        Check whether a provided packet initiates a diagnostic message.

        :param packet: Packet to check.

        :raise TypeError: Provided `packet` argument is not :class:`~uds.messages.uds_packet.AbstractUdsPacket`
            or :class:`~uds.messages.uds_packet.AbstractUdsPacketRecord` type.

        :return: True if the packet is the only or the first packet of a diagnostic message.
        """
        # TODO: _is_packet
        if not isinstance(packet, (AbstractUdsPacket, AbstractUdsPacketRecord)):
            raise TypeError(f"Provided value is not AbstractUdsPacket or AbstractUdsPacketRecord type. "
                            f"Actual value: {packet}.")

    @abstractmethod
    def get_consecutive_packets_number(self, first_packet: PacketTyping) -> int:  # type: ignore
        """
        Get number of consecutive packets that must follow this packet to fully store a diagnostic message.

        :param first_packet: The first packet of a segmented diagnostic message.

        :raise ValueError: Provided `packet` argument is not a packet that initiates diagnostic message.

        :return: Number of following packets that together carry a diagnostic message.
        """
        if not self.is_first_packet(packet=first_packet):
            raise ValueError(f"Provided value is not a first packet. Actual value: {first_packet}.")

    @abstractmethod
    def is_following_packets_sequence(self, packets: PacketsSequence) -> bool:
        """

        :param packets:
        :return:
        """

    @abstractmethod
    def is_complete_packets_sequence(self, packets: PacketsSequence) -> bool:  # type: ignore
        """
        Check whether provided packets are full sequence of packets that form exactly one diagnostic message.

        :param packets: Packets sequence to check.

        :raise TypeError: Provided 'packets' argument is not list or tuple type.
        :raise ValueError: Elements of 'packets' argument are not :class:`~uds.messages.uds_packet.AbstractUdsPacket`
            or :class:`~uds.messages.uds_packet.AbstractUdsPacketRecord` type.

        :return: True if the packets form exactly one diagnostic message.
            False if there are missing, additional or inconsistent (e.g. two packets that initiate a message) packets.
        """
        if not isinstance(packets, (tuple, list)):
            raise TypeError(f"Provided value is not tuple or list type. Actual value: {packets}.")
        # TODO: _is_packet_sequence

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

        :return: Diagnostic message created from these packets.
            :class:`~uds.messages.uds_message.UdsMessage` type would be returned
            if :class:`~uds.messages.uds_packet.AbstractUdsPacket` are provided.
            :class:`~uds.messages.uds_message.UdsMessageRecord` type would be returned
            if :class:`~uds.messages.uds_packet.AbstractUdsPacketRecord` are provided.
        """
        if not self.is_complete_packet_set(packets=packets):
            raise SegmentationError("Provided packets are not forming exactly one diagnostic message. "
                                    f"Actual value: {packets}.")

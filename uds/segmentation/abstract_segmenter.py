"""Definition of segmentation and desegmentation strategies."""

__all__ = ["SegmentationError", "AbstractSegmenter"]

from abc import ABC, abstractmethod
from typing import Any, Optional, Sequence, Type, Union

from uds.addressing import AbstractAddressingInformation, AddressingType
from uds.message import UdsMessage, UdsMessageRecord
from uds.packet import (
    AbstractPacket,
    AbstractPacketContainer,
    AbstractPacketRecord,
    PacketsContainersSequence,
    PacketsTuple,
)


class SegmentationError(ValueError):
    """UDS segmentation or desegmentation process cannot be completed due to input data inconsistency."""


class AbstractSegmenter(ABC):
    """
    Abstract definition of a segmenter class.

    Segmenter classes defines UDS segmentation and desegmentation tasks.
    They contain helper methods that are essential for successful
    :ref:`segmentation <knowledge-base-message-segmentation>` and
    :ref:`desegmentation <knowledge-base-packets-desegmentation>` execution.

    .. note:: Each concrete segmenter class handles exactly one bus/network type.
    """

    def __init__(self, addressing_information: AbstractAddressingInformation) -> None:
        """
        Initialize common configuration for all segmenters.

        :param addressing_information: Addressing Information configuration for this UDS Entity.
        """
        self.addressing_information = addressing_information

    @property
    @abstractmethod
    def supported_addressing_information_class(self) -> Type[AbstractAddressingInformation]:
        """Addressing Information class supported by this segmenter."""

    @property
    @abstractmethod
    def supported_packet_class(self) -> Type[AbstractPacket]:
        """Packet class supported by this segmenter."""

    @property
    @abstractmethod
    def supported_packet_record_class(self) -> Type[AbstractPacketRecord]:
        """Packet Record class supported by this segmenter."""

    @property
    def addressing_information(self) -> AbstractAddressingInformation:
        """Addressing Information configuration for this UDS Entity."""
        return self.__addressing_information

    @addressing_information.setter
    def addressing_information(self, value: AbstractAddressingInformation) -> None:
        """
        Set Addressing Information configuration for this UDS Entity.

        :param value: Value to set.

        :raise TypeError: Provided value is not Addressing Information type compatible with this segmenter.
        """
        if not isinstance(value, self.supported_addressing_information_class):
            raise TypeError("Provided value is not an object of Addressing Information class "
                            "supported by this segmenter.")
        self.__addressing_information = value

    def is_supported_packet_type(self, packet: AbstractPacketContainer) -> bool:
        """
        Check if the argument value is a packet object of a supported type.

        :param packet: Packet object to check.

        :return: True if provided value is an object of a supported packet type, False otherwise.
        """
        return isinstance(packet, (self.supported_packet_class, self.supported_packet_record_class))

    def is_supported_packets_sequence_type(self, packets: Sequence[AbstractPacketContainer]) -> bool:
        """
        Check if the argument value is a packets sequence of a supported type.

        :param packets: Packets sequence to check.

        :return: True if provided value is a packets sequence of a supported type, False otherwise.
        """
        if not isinstance(packets, Sequence):
            # not a sequence
            return False
        if not all(self.is_supported_packet_type(packet) for packet in packets):
            # at least one element is not a packet of a supported type
            return False
        # check if all packets are the same type
        return len({type(packet) for packet in packets}) == 1

    @abstractmethod
    def is_desegmented_message(self, packets: PacketsContainersSequence) -> bool:
        """
        Check whether provided packets are full sequence of packets that form exactly one diagnostic message.

        :param packets: Packets sequence to check.

        :return: True if the packets form exactly one diagnostic message.
            False if there are missing, additional or inconsistent (e.g. two packets that initiate a message) packets.
        """

    @abstractmethod
    def desegmentation(self, packets: PacketsContainersSequence) -> Union[UdsMessage, UdsMessageRecord]:
        """
        Perform desegmentation of packets.

        :param packets: Packets to collect into UDS message.

        :raise SegmentationError: Provided packets are not a complete packet sequence that form a diagnostic message.

        :return: A diagnostic message that is carried by provided packets.
        """

    @abstractmethod
    def segmentation(self, message: UdsMessage) -> PacketsTuple:
        """
        Perform segmentation of a diagnostic message.

        :param message: UDS message to divide into packets.

        :raise SegmentationError: Provided diagnostic message cannot be segmented.

        :return: Packet(s) that carry provided diagnostic message.
        """

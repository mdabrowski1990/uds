"""Definition of API for segmentation and desegmentation strategies."""

__all__ = ["SegmentationError", "AbstractSegmenter"]

from abc import ABC, abstractmethod
from typing import Optional, Sequence, Type, Union

from uds.message import UdsMessage, UdsMessageRecord
from uds.packet import (
    AbstractUdsPacket,
    AbstractUdsPacketContainer,
    AbstractUdsPacketRecord,
    PacketsContainersSequence,
    PacketsTuple,
)
from uds.transmission_attributes import AddressingType


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

    @property
    @abstractmethod
    def supported_packet_class(self) -> Type[AbstractUdsPacket]:
        """Class of UDS Packet supported by this segmenter."""

    @property
    @abstractmethod
    def supported_packet_record_class(self) -> Type[AbstractUdsPacketRecord]:
        """Class of UDS Packet Record supported by this segmenter."""

    def is_supported_packet_type(self, packet: AbstractUdsPacketContainer) -> bool:
        """
        Check if the argument value is a packet object of a supported type.

        :param packet: Packet object to check.

        :return: True if provided value is an object of a supported packet type, False otherwise.
        """
        return isinstance(packet, (self.supported_packet_class, self.supported_packet_record_class))

    @abstractmethod
    def is_input_packet(self, **kwargs) -> Optional[AddressingType]:
        """
        Check if provided frame attributes belong to a UDS packet which is an input for this Segmenter.

        :param kwargs: Attributes of a frame to check.

        :return: Addressing Type used for transmission of this UDS packet according to the configuration of this
            Segmenter (if provided attributes belongs to an input UDS packet), otherwise None.
        """

    def is_supported_packets_sequence_type(self, packets: Sequence[AbstractUdsPacketContainer]) -> bool:
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
        Perform desegmentation of UDS packets.

        :param packets: UDS packets to desegment into UDS message.

        :raise SegmentationError: Provided packets are not a complete packet sequence that form a diagnostic message.

        :return: A diagnostic message that is carried by provided UDS packets.
        """

    @abstractmethod
    def segmentation(self, message: UdsMessage) -> PacketsTuple:
        """
        Perform segmentation of a diagnostic message.

        :param message: UDS message to divide into UDS packets.

        :raise SegmentationError: Provided diagnostic message cannot be segmented.

        :return: UDS packet(s) that carry provided diagnostic message.
        """

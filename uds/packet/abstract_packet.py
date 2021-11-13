"""
Implementation of UDS packets that is common for all bus types.

:ref:`UDS packets <knowledge-base-uds-packet>` are defined on middle layers of UDS OSI Model.
"""

__all__ = ["AbstractUdsPacket", "AbstractUdsPacketRecord",
           "PacketAlias", "PacketsTuple", "PacketsSequence",
           "PacketsDefinitionTuple", "PacketsDefinitionSequence",
           "PacketsRecordsTuple", "PacketsRecordsSequence",
           "PacketTypesTuple"]

from abc import ABC, abstractmethod
from typing import Union, Optional, Any, Tuple, List

from uds.utilities import RawBytesTuple, ReassignmentError, TimeStamp
from uds.transmission_attributes.addressing import AddressingType
from uds.transmission_attributes.transmission_direction import TransmissionDirection, TransmissionDirectionAlias
from .abstract_packet_type import AbstractUdsPacketType


class AbstractUdsPacket(ABC):
    """Abstract definition of UDS Packet (Network Protocol Data Unit - N_PDU)."""

    @property
    @abstractmethod
    def addressing_type(self) -> AddressingType:
        """Addressing type for which this packet is relevant."""

    @property
    @abstractmethod
    def raw_frame_data(self) -> RawBytesTuple:
        """Raw data bytes of a frame that carries this packet."""

    @property
    @abstractmethod
    def packet_type(self) -> AbstractUdsPacketType:
        """UDS packet type value - N_PCI value of this N_PDU."""

    @property
    @abstractmethod
    def payload(self) -> Optional[RawBytesTuple]:
        """Payload bytes of a diagnostic message carried by this packet."""

    @property
    @abstractmethod
    def data_length(self) -> Optional[int]:
        """Payload bytes number of a diagnostic message which is carried by this packet."""


class AbstractUdsPacketRecord(ABC):
    """Abstract definition of a storage for historic information about transmitted or received UDS Packet."""

    @abstractmethod
    def __init__(self, frame: Any, direction: TransmissionDirectionAlias) -> None:
        """
        Create a record of a historic information about a packet that was either received or transmitted.

        :param frame: Frame that carried this UDS packet.
        :param direction: Information whether this packet was transmitted or received.
        """
        self.frame = frame
        self.direction = direction  # type: ignore

    @abstractmethod
    def __validate_frame(self, value: Any) -> None:
        """
        Validate a frame argument.

        :param value: Value to validate.

        :raise TypeError: The frame argument has unsupported.
        :raise ValueError: Some attribute of the frame argument is missing or its value is unexpected.
        """

    @property
    def frame(self) -> Any:
        """Frame that carried this packet."""
        return self.__frame

    @frame.setter
    def frame(self, value: TransmissionDirectionAlias):
        """
        Set value of frame attribute.

        :param value: Frame value to set.

        :raise ReassignmentError: There is a call to change the value after the initial assignment (in __init__).
        """
        try:
            self.__getattribute__("_AbstractUdsPacketRecord__frame")
        except AttributeError:
            self.__validate_frame(value)
            self.__frame = value
        else:
            raise ReassignmentError("You cannot change value of 'frame' attribute once it is assigned.")

    @property
    def direction(self) -> TransmissionDirection:
        """Information whether this packet was transmitted or received."""
        return self.__direction

    @direction.setter
    def direction(self, value: TransmissionDirectionAlias):
        """
        Set value of direction attribute.

        :param value: Direction value to set.

        :raise ReassignmentError: There is a call to change the value after the initial assignment (in __init__).
        """
        try:
            self.__getattribute__("_AbstractUdsPacketRecord__direction")
        except AttributeError:
            TransmissionDirection.validate_member(value)
            self.__direction = TransmissionDirection(value)
        else:
            raise ReassignmentError("You cannot change value of 'direction' attribute once it is assigned.")

    @property
    @abstractmethod
    def raw_frame_data(self) -> RawBytesTuple:
        """Raw data bytes of a frame that carries this packet."""

    @property
    @abstractmethod
    def addressing_type(self) -> AddressingType:
        """Addressing type over which this packet was transmitted."""

    @property
    @abstractmethod
    def transmission_time(self) -> TimeStamp:
        """Time stamp when this packet was fully transmitted on a bus."""

    @property
    @abstractmethod
    def packet_type(self) -> AbstractUdsPacketType:
        """UDS packet type value - N_PCI value of this N_PDU."""

    @property
    @abstractmethod
    def payload(self) -> Optional[RawBytesTuple]:
        """Payload bytes of a diagnostic message carried by this packet."""

    @property
    @abstractmethod
    def data_length(self) -> Optional[int]:
        """Payload bytes number of a diagnostic message which was carried by this packet."""


# TODO: get rid of these if possible
PacketTypesTuple = Tuple[AbstractUdsPacketType, ...]
"""Typing alias of a tuple filled with :class:`~uds.message.uds_packet.AbstractUdsPacketType` members."""

PacketsDefinitionTuple = Tuple[AbstractUdsPacket, ...]
"""Typing alias of a tuple filled with :class:`~uds.message.uds_packet.AbstractUdsPacket` instances."""
PacketsDefinitionSequence = Union[PacketsDefinitionTuple, List[AbstractUdsPacket]]
"""Typing alias of a sequence filled with :class:`~uds.message.uds_packet.AbstractUdsPacket` instances."""

PacketsRecordsTuple = Tuple[AbstractUdsPacketRecord, ...]
"""Typing alias of a tuple filled with :class:`~uds.message.uds_packet.AbstractUdsPacketRecord` instances."""
PacketsRecordsSequence = Union[PacketsRecordsTuple, List[AbstractUdsPacketRecord]]
"""Typing alias of a sequence filled with :class:`~uds.message.uds_packet.AbstractUdsPacketRecord` instances."""

PacketAlias = Union[AbstractUdsPacket, AbstractUdsPacketRecord]
"""Typing alias of UDS packet."""
PacketsTuple = Union[PacketsDefinitionTuple, PacketsRecordsTuple]  # noqa: F841
"""Typing alias of a tuple filled with UDS packets."""
PacketsSequence = Union[PacketsDefinitionSequence, PacketsRecordsSequence]
"""Typing alias of a sequence filled with UDS packets."""

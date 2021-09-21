"""
Module with common implementation of UDS packets for all bus types.

UDS Packets are defined on middle layers of UDS OSI Model.
"""

__all__ = ["AbstractUdsPacketType", "AbstractUdsPacket", "AbstractUdsPacketRecord",
           "PacketsTuple", "PacketsSequence", "PacketsRecordsTuple", "PacketsRecordsSequence"]

from abc import ABC, abstractmethod
from typing import Union, Tuple, List, Any

from uds.utilities import NibbleEnum, ValidatedEnum, ExtendableEnum, \
    RawBytes, RawBytesTuple, validate_raw_bytes,\
    ReassignmentError, TimeStamp
from .transmission_attributes import AddressingMemberTyping, AddressingType, \
    TransmissionDirection, DirectionMemberTyping


class AbstractUdsPacketType(NibbleEnum, ValidatedEnum, ExtendableEnum):
    """
    Abstract definition of UDS packet type.

    Packet type information is carried by Network Protocol Control Information (N_PCI).
    Enums with packet types (N_PCI) values for certain buses (e.g. CAN, LIN, FlexRay) must inherit after this class.

    Note: There are some differences in values for each bus (e.g. LIN does not use Flow Control).
    """


class AbstractUdsPacket(ABC):
    """Abstract definition of UDS Packet (Network Protocol Data Unit - N_PDU)."""

    def __init__(self, raw_data: RawBytes, addressing: AddressingMemberTyping) -> None:
        """
        Create a storage for a single UDS packet.

        :param raw_data: Raw bytes of UDS packet data.
        :param addressing: Addressing type for which this packet is relevant.
        """
        self.raw_data = raw_data  # type: ignore
        self.addressing = addressing  # type: ignore

    @property
    def addressing(self) -> AddressingType:
        """Addressing type for which this packet is relevant."""
        return self.__addressing

    @addressing.setter
    def addressing(self, value: AddressingMemberTyping):
        """
        Set value of addressing type attribute.

        :param value: Value of addressing type to set.
        """
        AddressingType.validate_member(value)
        self.__addressing = AddressingType(value)

    @property
    def raw_data(self) -> RawBytesTuple:
        """Raw bytes of data that this packet carries."""
        return self.__raw_data

    @raw_data.setter
    def raw_data(self, value: RawBytes):
        """
        Set value of raw bytes of data.

        :param value: Raw bytes of data to be carried by this packet.
        """
        validate_raw_bytes(value)
        self.__raw_data = tuple(value)

    @property
    @abstractmethod
    def payload(self) -> RawBytesTuple:
        """Diagnostic message payload carried by this packet."""

    @property  # noqa: F841
    @abstractmethod
    def packet_type_enum(self) -> type:
        """Enum with possible UDS packet types."""

    @property  # noqa: F841
    @abstractmethod
    def packet_type(self) -> AbstractUdsPacketType:
        """UDS packet type value - N_PCI value of this N_PDU."""


class AbstractUdsPacketRecord(ABC):
    """Abstract definition of a storage for historic information about transmitted or received UDS Packet."""

    @abstractmethod
    def __init__(self, frame: object, direction: DirectionMemberTyping) -> None:
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
        Validate whether the argument contains value with a frame object.

        :param value: Value to validate.

        :raise TypeError: The frame argument has other type than expected.
        :raise ValueError: Some attribute of the frame argument is missing or its value is unexpected.
        """

    @property
    def frame(self) -> object:
        """Frame that carried this packet."""
        return self.__frame

    @frame.setter
    def frame(self, value: DirectionMemberTyping):
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
    def direction(self, value: DirectionMemberTyping):
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
    def raw_data(self) -> RawBytesTuple:
        """Raw bytes of data that this packet carried."""

    @property
    @abstractmethod
    def payload(self) -> RawBytesTuple:
        """Diagnostic message payload carried by this packet."""

    @property
    @abstractmethod
    def addressing(self) -> AddressingType:
        """Addressing type over which this packet was transmitted."""

    @property  # noqa: F841
    @abstractmethod
    def transmission_time(self) -> TimeStamp:
        """Time stamp when this packet was fully transmitted on a bus."""

    @property  # noqa: F841
    @abstractmethod
    def packet_type_enum(self) -> type:
        """Enum with possible UDS packet types."""

    @property  # noqa: F841
    @abstractmethod
    def packet_type(self) -> AbstractUdsPacketType:
        """UDS packet type value - N_PCI value of this N_PDU."""


PacketsTuple = Tuple[AbstractUdsPacket, ...]
"""Typing alias of a tuple filled with UDS Packets."""
PacketsSequence = Union[PacketsTuple, List[AbstractUdsPacket]]
"""Typing alias of a sequence filled with UDS Packets."""

PacketsRecordsTuple = Tuple[AbstractUdsPacketRecord, ...]
"""Typing alias of a tuple filled with UDS Packets Records."""
PacketsRecordsSequence = Union[PacketsRecordsTuple, List[AbstractUdsPacketRecord]]
"""Typing alias of a sequence filled with UDS Packets Records."""

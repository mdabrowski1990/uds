"""
Implementation of UDS packets that is common for all bus types.

:ref:`UDS packets <knowledge-base-uds-packet>` are defined on middle layers of UDS OSI Model.
"""

__all__ = ["AbstractUdsPacketType", "AbstractUdsPacket", "AbstractUdsPacketRecord",
           "PacketTyping", "PacketsTuple", "PacketsSequence",
           "PacketsDefinitionTuple", "PacketsDefinitionSequence",
           "PacketsRecordsTuple", "PacketsRecordsSequence",
           "PacketTypesTuple"]

from abc import ABC, abstractmethod
from typing import Union, Tuple, List, Any

from uds.utilities import NibbleEnum, ValidatedEnum, ExtendableEnum, \
    RawBytesTuple, ReassignmentError, TimeStamp
from uds.transmission_attributes.addressing import AddressingType
from uds.transmission_attributes.transmission_direction import TransmissionDirection, TransmissionDirectionMemberAlias


class AbstractUdsPacketType(NibbleEnum, ValidatedEnum, ExtendableEnum):
    """
    Abstract definition of UDS packet type.

    Packet type information is carried by :ref:`Network Protocol Control Information (N_PCI) <knowledge-base-n-pci>`.
    Enums with packet types (N_PCI) values for certain buses (e.g. CAN, LIN, FlexRay) must inherit after this class.

    .. note:: There are differences in values for each bus (e.g. LIN does not use Flow Control).
    """

    @classmethod
    @abstractmethod
    def is_initial_packet_type(cls, value: Any) -> bool:
        """
        Check whether given argument is a member or a value of packet type that initiates a diagnostic message.

        :param value: Value to check.

        :return: True if given argument is a packet type that initiates a diagnostic message, else False.
        """


class AbstractUdsPacket(ABC):
    """Abstract definition of UDS Packet (Network Protocol Data Unit - N_PDU)."""

    @property
    @abstractmethod
    def addressing(self) -> AddressingType:
        """Addressing type for which this packet is relevant."""

    @property
    @abstractmethod
    def raw_frame_data(self) -> RawBytesTuple:
        """Raw data bytes of a frame that carries this CAN packet."""

    @property
    @abstractmethod
    def packet_type(self) -> AbstractUdsPacketType:
        """UDS packet type value - N_PCI value of this N_PDU."""


class AbstractUdsPacketRecord(ABC):
    """Abstract definition of a storage for historic information about transmitted or received UDS Packet."""

    @abstractmethod
    def __init__(self, frame: object, direction: TransmissionDirectionMemberAlias) -> None:
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
    def frame(self, value: TransmissionDirectionMemberAlias):
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
    def direction(self, value: TransmissionDirectionMemberAlias):
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
        """Raw data bytes of a frame that carried this CAN packet."""

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
    def packet_type(self) -> AbstractUdsPacketType:
        """UDS packet type value - N_PCI value of this N_PDU."""


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

PacketTyping = Union[AbstractUdsPacket, AbstractUdsPacketRecord]
"""Typing alias of UDS packet."""
PacketsTuple = Union[PacketsDefinitionTuple, PacketsRecordsTuple]  # noqa: F841
"""Typing alias of a tuple filled with UDS packets."""
PacketsSequence = Union[PacketsDefinitionSequence, PacketsRecordsSequence]
"""Typing alias of a sequence filled with UDS packets."""

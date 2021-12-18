"""
Implementation of UDS packets that is common for all bus types.

:ref:`UDS packets <knowledge-base-uds-packet>` are defined on middle layers of UDS OSI Model.
"""

__all__ = ["AbstractUdsPacketContainer", "AbstractUdsPacket", "AbstractUdsPacketRecord",
           "PacketsContainersSequence", "PacketsContainersTuple", "PacketsContainersList",
           "PacketsSequence", "PacketsTuple", "PacketsList",
           "PacketsRecordsSequence", "PacketsRecordsTuple", "PacketsRecordsList"]

from abc import ABC, abstractmethod
from typing import Union, Optional, Any, Tuple, List

from uds.utilities import RawBytesTuple, ReassignmentError, TimeStamp
from uds.transmission_attributes.addressing import AddressingTypeAlias
from uds.transmission_attributes.transmission_direction import TransmissionDirection, TransmissionDirectionAlias
from .abstract_packet_type import AbstractUdsPacketTypeAlias


class AbstractUdsPacketContainer(ABC):
    """Abstract definition of a container with UDS Packet information."""

    @property
    @abstractmethod
    def addressing_type(self) -> AddressingTypeAlias:
        """Addressing for which this packet is relevant."""

    @property
    @abstractmethod
    def raw_frame_data(self) -> RawBytesTuple:
        """Raw data bytes of a frame that carries this packet."""

    @property
    @abstractmethod
    def packet_type(self) -> AbstractUdsPacketTypeAlias:
        """Type (N_PCI value) of this UDS packet."""

    @property
    @abstractmethod
    def payload(self) -> Optional[RawBytesTuple]:
        """Raw payload bytes of a diagnostic message that are carried by this packet."""

    @property
    @abstractmethod
    def data_length(self) -> Optional[int]:
        """Payload bytes number of a diagnostic message which was carried by this packet."""


class AbstractUdsPacket(AbstractUdsPacketContainer):
    """Abstract definition of UDS Packet (Network Protocol Data Unit - N_PDU)."""

    @property
    @abstractmethod
    def addressing_type(self) -> AddressingTypeAlias:
        """Addressing for which this packet is relevant."""

    @property
    @abstractmethod
    def raw_frame_data(self) -> RawBytesTuple:
        """Raw data bytes of a frame that carries this packet."""

    @property
    @abstractmethod
    def packet_type(self) -> AbstractUdsPacketTypeAlias:
        """Type (N_PCI value) of this UDS packet."""

    @property
    @abstractmethod
    def payload(self) -> Optional[RawBytesTuple]:
        """Raw payload bytes of a diagnostic message that are carried by this packet."""

    @property
    @abstractmethod
    def data_length(self) -> Optional[int]:
        """Payload bytes number of a diagnostic message which was carried by this packet."""


class AbstractUdsPacketRecord(AbstractUdsPacketContainer):
    """Abstract definition of a storage for historic information about transmitted or received UDS Packet."""

    @abstractmethod
    def __init__(self,
                 frame: Any,
                 direction: TransmissionDirectionAlias,
                 transmission_time: TimeStamp) -> None:
        """
        Create a record of historic information about a packet that was either received or transmitted.

        :param frame: Frame that carried this UDS packet.
        :param direction: Information whether this packet was transmitted or received.
        :param transmission_time: Time stamp when this packet was fully transmitted on a bus.
        """
        self.frame = frame
        self.direction = direction
        self.transmission_time = transmission_time

    @property
    def frame(self) -> Any:
        """Frame that carried this packet."""
        return self.__frame

    @frame.setter
    def frame(self, value: Any):
        """
        Set value of frame attribute.

        :param value: Frame value to set.

        :raise ReassignmentError: There is a call to change the value after the initial assignment (in __init__).
        """
        try:
            self.__getattribute__("_AbstractUdsPacketRecord__frame")
        except AttributeError:
            self._validate_frame(value)
            self.__frame = value
        else:
            raise ReassignmentError("You cannot change value of 'frame' attribute once it is assigned.")

    @property
    def direction(self) -> TransmissionDirectionAlias:
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
    def transmission_time(self) -> TimeStamp:
        """Time stamp when this packet was fully transmitted on a bus."""
        return self.__transmission_time

    @transmission_time.setter
    def transmission_time(self, value: TimeStamp):
        """
        Set value of transmission_time attribute.

        :param value: Direction value to set.

        :raise TypeError: Provided value has unexpected type.
        :raise ReassignmentError: There is a call to change the value after the initial assignment (in __init__).
        """
        try:
            self.__getattribute__("_AbstractUdsPacketRecord__transmission_time")
        except AttributeError:
            if not isinstance(value, TimeStamp):
                raise TypeError(f"Provided value has invalid type: {type(value)}")  # pylint: disable=raise-missing-from
            self.__transmission_time = value
        else:
            raise ReassignmentError("You cannot change value of 'transmission_time' attribute once it is assigned.")

    @property
    @abstractmethod
    def addressing_type(self) -> AddressingTypeAlias:
        """Addressing for which this packet is relevant."""

    @property
    @abstractmethod
    def raw_frame_data(self) -> RawBytesTuple:
        """Raw data bytes of a frame that carries this packet."""

    @property
    @abstractmethod
    def packet_type(self) -> AbstractUdsPacketTypeAlias:
        """Type (N_PCI value) of this UDS packet."""

    @property
    @abstractmethod
    def payload(self) -> Optional[RawBytesTuple]:
        """Raw payload bytes of a diagnostic message that are carried by this packet."""

    @property
    @abstractmethod
    def data_length(self) -> Optional[int]:
        """Payload bytes number of a diagnostic message which was carried by this packet."""

    @staticmethod
    @abstractmethod
    def _validate_frame(value: Any) -> None:
        """
        Validate a frame argument.

        :param value: Value to validate.

        :raise TypeError: The frame argument has unsupported.
        :raise ValueError: Some attribute of the frame argument is missing or its value is unexpected.
        """


PacketsContainersTuple = Tuple[AbstractUdsPacketContainer, ...]
"""Typing alias of a tuple filled with :class:`~uds.packet.abstract_packet.AbstractUdsPacketContainer` instances."""
PacketsContainersList = List[AbstractUdsPacketContainer]
"""Typing alias of a list filled with :class:`~uds.packet.abstract_packet.AbstractUdsPacketContainer` instances."""
PacketsContainersSequence = Union[PacketsContainersTuple, PacketsContainersList]
"""Typing alias of a sequence filled with :class:`~uds.packet.abstract_packet.AbstractUdsPacketContainer` instances."""

PacketsTuple = Tuple[AbstractUdsPacket, ...]
"""Typing alias of a tuple filled with :class:`~uds.packet.abstract_packet.AbstractUdsPacket` instances."""
PacketsList = List[AbstractUdsPacket]
"""Typing alias of a list filled with :class:`~uds.packet.abstract_packet.AbstractUdsPacket` instances."""
PacketsSequence = Union[PacketsTuple, PacketsList]
"""Typing alias of a sequence filled with :class:`~uds.packet.abstract_packet.AbstractUdsPacket` instances."""

PacketsRecordsTuple = Tuple[AbstractUdsPacketRecord, ...]
"""Typing alias of a tuple filled with :class:`~uds.packet.abstract_packet.AbstractUdsPacketRecord` instances."""
PacketsRecordsList = List[AbstractUdsPacketRecord]
"""Typing alias of a list filled with :class:`~uds.packet.abstract_packet.AbstractUdsPacketRecord` instances."""
PacketsRecordsSequence = Union[PacketsRecordsTuple, PacketsRecordsList]
"""Typing alias of a sequence filled with :class:`~uds.packet.abstract_packet.AbstractUdsPacketRecord` instances."""

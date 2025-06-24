"""Abstract definition of UDS packets that is common for all bus types."""

__all__ = ["AbstractUdsPacketContainer", "AbstractUdsPacket", "AbstractUdsPacketRecord",
           "PacketsContainersSequence", "PacketsTuple", "PacketsRecordsTuple", "PacketsRecordsSequence"]

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional, Sequence, Tuple

from uds.transmission_attributes.addressing import AddressingType
from uds.transmission_attributes.transmission_direction import TransmissionDirection
from uds.utilities import ReassignmentError

from .abstract_packet_type import AbstractUdsPacketType


class AbstractUdsPacketContainer(ABC):
    """Abstract definition of a container with UDS Packet information."""

    @property
    @abstractmethod
    def raw_frame_data(self) -> bytes:
        """Raw data bytes of a frame that carries this packet."""

    @property
    @abstractmethod
    def addressing_type(self) -> AddressingType:
        """Addressing for which this packet is relevant."""

    @property
    @abstractmethod
    def packet_type(self) -> AbstractUdsPacketType:
        """Type (N_PCI value) of this UDS packet."""

    @property
    @abstractmethod
    def data_length(self) -> Optional[int]:
        """Payload bytes number of a diagnostic message which was carried by this packet."""

    @property
    @abstractmethod
    def payload(self) -> Optional[bytes]:
        """Raw payload bytes of a diagnostic message that are carried by this packet."""


class AbstractUdsPacket(AbstractUdsPacketContainer, ABC):
    """Abstract definition of UDS Packet (Network Protocol Data Unit - N_PDU)."""


class AbstractUdsPacketRecord(AbstractUdsPacketContainer, ABC):
    """Abstract definition of a storage for historic information about transmitted or received UDS Packet."""

    @abstractmethod
    def __init__(self,
                 frame: Any,
                 direction: TransmissionDirection,
                 transmission_time: datetime) -> None:
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
    def frame(self, value: Any) -> None:
        """
        Set value of frame attribute.

        :param value: Frame value to set.

        :raise ReassignmentError: There is a call to change the value after the initial assignment (in __init__).
        """
        try:
            getattr(self, "_AbstractUdsPacketRecord__frame")
        except AttributeError:
            self._validate_frame(value)
            self.__frame = value
        else:
            raise ReassignmentError("You cannot change value of 'frame' attribute once it is assigned.")

    @property
    def direction(self) -> TransmissionDirection:
        """Information whether this packet was transmitted or received."""
        return self.__direction

    @direction.setter
    def direction(self, value: TransmissionDirection) -> None:
        """
        Set value of direction attribute.

        :param value: Direction value to set.

        :raise ReassignmentError: There is a call to change the value after the initial assignment (in __init__).
        """
        try:
            getattr(self, "_AbstractUdsPacketRecord__direction")
        except AttributeError:
            self.__direction = TransmissionDirection.validate_member(value)
        else:
            raise ReassignmentError("You cannot change value of 'direction' attribute once it is assigned.")

    @property
    def transmission_time(self) -> datetime:
        """Time when this packet was fully transmitted on a bus."""
        return self.__transmission_time

    @transmission_time.setter
    def transmission_time(self, value: datetime) -> None:
        """
        Set value when this packet was transmitted on a bus.

        :param value: Value of transmission time to set.

        :raise TypeError: Provided value has unexpected type.
        :raise ReassignmentError: There is a call to change the value after the initial assignment (in __init__).
        """
        try:
            getattr(self, "_AbstractUdsPacketRecord__transmission_time")
        except AttributeError:
            if not isinstance(value, datetime):
                raise TypeError(f"Provided value has invalid type: {type(value)}")  # pylint: disable=raise-missing-from
            self.__transmission_time = value
        else:
            raise ReassignmentError("You cannot change value of 'transmission_time' attribute once it is assigned.")

    @staticmethod
    @abstractmethod
    def _validate_frame(value: Any) -> None:
        """
        Validate a frame argument.

        :param value: Value to validate.

        :raise TypeError: Provided frame object has unsupported type.
        :raise ValueError: At least one attribute of the frame object is missing or its value is unexpected.
        """


PacketsContainersSequence = Sequence[AbstractUdsPacketContainer]
"""Alias for a sequence filled with packet or packet record object."""

PacketsTuple = Tuple[AbstractUdsPacket, ...]
"""Alias for a packet objects tuple."""
PacketsRecordsTuple = Tuple[AbstractUdsPacketRecord, ...]
"""Alias for a packet record objects tuple."""
PacketsRecordsSequence = Sequence[AbstractUdsPacketRecord]
"""Alias for a packet record objects sequence."""

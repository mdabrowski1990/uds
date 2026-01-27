"""Abstract definition of packets that is common for all bus/network types."""

__all__ = ["AbstractPacketContainer", "AbstractPacket", "AbstractPacketRecord",
           "PacketsContainersSequence", "PacketsTuple", "PacketsRecordsTuple", "PacketsRecordsSequence"]

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional, Sequence, Tuple

from uds.addressing import AddressingType, TransmissionDirection
from uds.utilities import ReassignmentError, bytes_to_hex

from .abstract_packet_type import AbstractPacketType


class AbstractPacketContainer(ABC):
    """Abstract definition of a container with packet information."""

    def __str__(self) -> str:
        """Present object in string format."""
        return (f"{self.__class__.__name__}("
                f"payload={None if self.payload is None else bytes_to_hex(self.payload)}, "
                f"addressing_type={self.addressing_type}, "
                f"packet_type={self.packet_type}, "
                f"raw_frame_data={bytes_to_hex(self.raw_frame_data)})")

    @property
    @abstractmethod
    def raw_frame_data(self) -> bytes:
        """Raw data bytes of a frame that carries this packet."""

    @property
    @abstractmethod
    def packet_type(self) -> AbstractPacketType:
        """Type (N_PCI value) of this packet."""

    @property
    @abstractmethod
    def data_length(self) -> Optional[int]:
        """Payload bytes number of a diagnostic message."""

    @property
    @abstractmethod
    def addressing_type(self) -> AddressingType:
        """Addressing for which this packet is relevant."""

    @property
    @abstractmethod
    def payload(self) -> Optional[bytes]:
        """Diagnostic message payload carried by this packet."""


class AbstractPacket(AbstractPacketContainer, ABC):
    """Abstract definition of a packet (Network Protocol Data Unit - N_PDU)."""


class AbstractPacketRecord(AbstractPacketContainer, ABC):
    """Abstract definition of a storage for historic information about transmitted or received packet."""

    @abstractmethod
    def __init__(self,
                 frame: Any,
                 direction: TransmissionDirection,
                 transmission_time: datetime,
                 transmission_timestamp: float) -> None:
        """
        Create a record of historic information about a packet.

        :param frame: Frame that carried this packet.
        :param direction: Information whether this packet was transmitted or received.
        :param transmission_time: Time stamp when this packet was fully transmitted on a bus/network.
        """
        self.frame = frame
        self.direction = direction
        self.transmission_time = transmission_time
        self.transmission_timestamp = transmission_timestamp
        self._validate_attributes()

    def __str__(self) -> str:
        """Present object in string format."""
        return (f"{self.__class__.__name__}("
                f"payload={None if self.payload is None else bytes_to_hex(self.payload)}, "
                f"addressing_type={self.addressing_type}, "
                f"packet_type={self.packet_type}, "
                f"raw_frame_data={bytes_to_hex(self.raw_frame_data)}, "
                f"direction={self.direction}, "
                f"transmission_time={self.transmission_time})")

    @property
    def frame(self) -> Any:
        """Frame that carried this packet."""
        return self.__frame

    @frame.setter
    def frame(self, value: Any) -> None:
        """
        Set value of frame attribute.

        :param value: Frame value to set.

        :raise ReassignmentError: An attempt to change the value after object creation.
        """
        if hasattr(self, "_AbstractPacketRecord__frame"):
            raise ReassignmentError("Value of 'frame' attribute cannot be changed once assigned.")
        self._validate_frame(value)
        self.__frame = value

    @property
    def direction(self) -> TransmissionDirection:
        """Information whether this packet was transmitted or received."""
        return self.__direction

    @direction.setter
    def direction(self, value: TransmissionDirection) -> None:
        """
        Set value of direction attribute.

        :param value: Direction value to set.

        :raise ReassignmentError: An attempt to change the value after object creation.
        """
        if hasattr(self, "_AbstractPacketRecord__direction"):
            raise ReassignmentError("Value of 'direction' attribute cannot be changed once assigned.")
        self.__direction = TransmissionDirection.validate_member(value)

    @property
    def transmission_time(self) -> datetime:
        """Time when this packet was transmitted on a bus/network."""
        return self.__transmission_time

    @transmission_time.setter
    def transmission_time(self, value: datetime) -> None:
        """
        Set time value when this packet was transmitted on a bus/network.

        :param value: Value of transmission time to set.

        :raise TypeError: Provided value is not datetime type.
        :raise ReassignmentError: An attempt to change the value after object creation.
        """
        if not isinstance(value, datetime):
            raise TypeError(f"Provided value is not datetime type. Actual type: {type(value)}.")
        if hasattr(self, "_AbstractPacketRecord__transmission_time"):
            raise ReassignmentError("Value of 'transmission_time' attribute cannot be changed once assigned.")
        self.__transmission_time = value

    @property
    def transmission_timestamp(self) -> float:
        """Timestamp when this packet was transmitted on a bus/network."""
        return self.__transmission_timestamp

    @transmission_timestamp.setter
    def transmission_timestamp(self, value: float) -> None:
        """
        Set timestamp value when this packet was transmitted on a bus/network.

        :param value: Value of transmission timestamp to set.

        :raise TypeError: Provided value is not float type.
        :raise ReassignmentError: An attempt to change the value after object creation.
        """
        if not isinstance(value, float):
            raise TypeError(f"Provided value is not float type. Actual type: {type(value)}.")
        if hasattr(self, "_AbstractPacketRecord__transmission_timestamp"):
            raise ReassignmentError("Value of 'transmission_timestamp' attribute cannot be changed once assigned.")
        self.__transmission_timestamp = value

    @staticmethod
    @abstractmethod
    def _validate_frame(value: Any) -> None:
        """
        Validate a frame argument.

        :param value: Value to validate.
        """

    @abstractmethod
    def _validate_attributes(self) -> None:
        """Validate whether attributes that were set are a valid for a Packet record."""


PacketsContainersSequence = Sequence[AbstractPacketContainer]
"""Alias for a sequence filled with packet or packet record objects."""

PacketsTuple = Tuple[AbstractPacket, ...]
"""Alias for a packet objects tuple."""
PacketsRecordsTuple = Tuple[AbstractPacketRecord, ...]
"""Alias for a packet record objects tuple."""
PacketsRecordsSequence = Sequence[AbstractPacketRecord]
"""Alias for a packet record objects sequence."""

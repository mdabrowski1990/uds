"""Abstract definition of packets that is common for all bus/network types."""

__all__ = ["AbstractPacketContainer", "AbstractPacket", "AbstractPacketRecord",
           "PacketsContainersSequenceAlias", "PacketsTupleAlias", "PacketsRecordsTupleAlias",
           "PacketsRecordsSequenceAlias"]

from abc import ABC, abstractmethod
from collections.abc import Sequence
from datetime import datetime
from time import perf_counter
from typing import Any
from warnings import warn

from uds.addressing import AddressingType, TransmissionDirection
from uds.utilities import ReassignmentError, bytes_to_hex

from .abstract_packet_type import AbstractPacketType


class AbstractPacketContainer(ABC):
    """Abstract definition of a container with packet information."""

    def __str__(self) -> str:
        """Present object in string format."""
        return (f"{self.__class__.__name__}("
                f"raw_frame_data={bytes_to_hex(self.raw_frame_data)}, "
                f"payload={None if self.payload is None else bytes_to_hex(self.payload)}, "
                f"addressing_type={self.addressing_type}, "
                f"packet_type={self.packet_type})")

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
    def data_length(self) -> int | None:
        """Payload bytes number of a diagnostic message."""

    @property
    @abstractmethod
    def addressing_type(self) -> AddressingType:
        """Addressing for which this packet is relevant."""

    @property
    @abstractmethod
    def payload(self) -> bytes | None:
        """Diagnostic message payload carried by this packet."""


class AbstractPacket(AbstractPacketContainer, ABC):
    """Abstract definition of a packet (Network Protocol Data Unit - N_PDU)."""


class AbstractPacketRecord(AbstractPacketContainer, ABC):
    """Abstract container for historical information about transmitted or received packets."""

    @abstractmethod
    def __init__(self,
                 frame: Any,
                 direction: TransmissionDirection,
                 transmission_time: datetime,
                 transmission_timestamp: float,
                 transmission_native_timestamp: float | None) -> None:
        """
        Create a record of historic information about a packet.

        :param frame: Frame that carried this packet.
        :param direction: Information whether this packet was transmitted or received.
        :param transmission_time: Wall-clock time at which the packet was transmitted or received
        :param transmission_timestamp: Monotonic timestamp associated with the packet transmission or reception.
        :param transmission_native_timestamp: Timestamp provided by the underlying network manager.
        """
        self.frame = frame
        self.direction = direction
        self.transmission_time = transmission_time
        self.transmission_timestamp = transmission_timestamp
        self.transmission_native_timestamp = transmission_native_timestamp
        self._validate_attributes()

    def __str__(self) -> str:
        """Present object in string format."""
        return (f"{self.__class__.__name__}("
                f"raw_frame_data={bytes_to_hex(self.raw_frame_data)}, "
                f"addressing_type={self.addressing_type}, "
                f"direction={self.direction}, "
                f"payload={None if self.payload is None else bytes_to_hex(self.payload)}, "
                f"packet_type={self.packet_type}, "
                f"transmission_time={self.transmission_time}, "
                f"transmission_timestamp={self.transmission_timestamp}, "
                f"transmission_native_timestamp={self.transmission_native_timestamp})")

    @property
    def frame(self) -> Any:
        """Frame that carried this packet."""
        return self.__frame

    @frame.setter
    def frame(self, value: Any) -> None:
        """
        Set value of frame attribute.

        :param value: Frame value to set.

        :raise ReassignmentError: An attempt to change the value after it has been set.
        """
        if hasattr(self, "_AbstractPacketRecord__frame"):
            raise ReassignmentError("Value of 'frame' attribute cannot be changed once set.")
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

        :raise ReassignmentError: An attempt to change the value after it has been set.
        """
        if hasattr(self, "_AbstractPacketRecord__direction"):
            raise ReassignmentError("Value of 'direction' attribute cannot be changed once set.")
        self.__direction = TransmissionDirection.validate_member(value)

    @property
    def transmission_time(self) -> datetime:
        """
        Get the approximate wall-clock time at which the packet was transmitted or received.

        .. warning:: This value is approximate.
            The most precise available timestamp is provided by
            :attr:`~uds.packet.abstract_packet.AbstractPacketRecord.transmission_native_timestamp`.
        """
        return self.__transmission_time

    @transmission_time.setter
    def transmission_time(self, value: datetime) -> None:
        """
        Set the approximate wall-clock time at which the packet was transmitted or received.

        :param value: Approximate wall-clock transmission time.
        :raise TypeError: Provided value is not a datetime instance.
        :raise ReassignmentError: An attempt to change the value after it has been set.
        """
        time_now = datetime.now()
        if not isinstance(value, datetime):
            raise TypeError(f"Provided value is not datetime type. Actual type: {type(value)}.")
        if hasattr(self, "_AbstractPacketRecord__transmission_time"):
            raise ReassignmentError("Value of 'transmission_time' attribute cannot be changed once set.")
        if value > time_now:
            warn(message="Future time provided as `transmission_time` to a packet record. "
                         "Current time was used instead.",
                 category=RuntimeWarning)
            value = time_now
        self.__transmission_time = value

    @property
    def transmission_timestamp(self) -> float:
        """
        Get the approximate monotonic timestamp associated with the packet transmission or reception.

        This value is obtained from :func:`~time.perf_counter` and is suitable for measuring elapsed time relative
        to other timestamps obtained from the same clock.

        .. warning:: This value is approximate.
            The most precise available timestamp is provided by
            :attr:`~uds.packet.abstract_packet.AbstractPacketRecord.transmission_native_timestamp`.
        """
        return self.__transmission_timestamp

    @transmission_timestamp.setter
    def transmission_timestamp(self, value: float) -> None:
        """
        Set the approximate monotonic timestamp associated with the packet transmission or reception.

        :param value: Monotonic timestamp associated with the packet transmission or reception.
        :raise TypeError: Provided value is not float type.
        :raise ReassignmentError: An attempt to change the value after it has been set.
        """
        timestamp_now = perf_counter()
        if not isinstance(value, float):
            raise TypeError(f"Provided value is not float type. Actual type: {type(value)}.")
        if hasattr(self, "_AbstractPacketRecord__transmission_timestamp"):
            raise ReassignmentError("Value of 'transmission_timestamp' attribute cannot be changed once set.")
        if value > timestamp_now:
            warn(message="Future timestamp provided as `transmission_timestamp` to a packet record. "
                         "Current timestamp was used instead.",
                 category=RuntimeWarning)
            value = timestamp_now
        self.__transmission_timestamp = value

    @property
    def transmission_native_timestamp(self) -> float | None:
        """
        Get the timestamp provided by the underlying Transport Interface.

        .. note:: This value represents the timestamp natively reported by the network manager (attribute
            :attr:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.network_manager`
            in Transport Interface) that transmitted or received the packet.
        """
        return self.__transmission_native_timestamp

    @transmission_native_timestamp.setter
    def transmission_native_timestamp(self, value: float | None) -> None:
        """
        Set the timestamp provided by the underlying Transport Interface.

        :param value: Native timestamp provided by the network manager.
        :raise TypeError: Provided value is not float or None type.
        :raise ReassignmentError: An attempt to change the value after it has been set.
        """
        if value is not None and not isinstance(value, float):
            raise TypeError(f"Provided value is not float or None type. Actual type: {type(value)}.")
        if hasattr(self, "_AbstractPacketRecord__transmission_native_timestamp"):
            raise ReassignmentError("Value of 'transmission_native_timestamp' attribute cannot be changed once set.")
        self.__transmission_native_timestamp = value

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


PacketsContainersSequenceAlias = Sequence[AbstractPacketContainer]
"""Alias for a sequence filled with packet or packet record objects."""

PacketsTupleAlias = tuple[AbstractPacket, ...]
"""Alias for a packet objects tuple."""
PacketsRecordsTupleAlias = tuple[AbstractPacketRecord, ...]
"""Alias for a packet record objects tuple."""
PacketsRecordsSequenceAlias = Sequence[AbstractPacketRecord]
"""Alias for a packet record objects sequence."""

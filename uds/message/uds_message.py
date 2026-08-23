"""
Module with common implementation of all diagnostic messages (requests and responses).

:ref:`Diagnostic message <knowledge-base-diagnostic-message>` are defined on upper layers of UDS OSI Model.
"""

__all__ = [
    "NEGATIVE_RESPONSE_MESSAGE_LENGTH",
    "AbstractUdsMessageContainer",
    "UdsMessage", "UdsMessageRecord",
]

from abc import ABC, abstractmethod
from collections.abc import Sequence
from datetime import datetime

from uds.addressing import AddressingType, TransmissionDirection
from uds.packet import AbstractPacketRecord, PacketsRecordsSequenceAlias, PacketsRecordsTupleAlias
from uds.utilities import RawBytesAlias, ReassignmentError, bytes_to_hex, validate_raw_bytes

NEGATIVE_RESPONSE_MESSAGE_LENGTH: int = 3
"""Payload length of :ref:`Negative Response Message <knowledge-base-negative-response-message>`."""


class AbstractUdsMessageContainer(ABC):
    """Abstract definition of a container with diagnostic message information."""

    def __str__(self) -> str:
        """Present object in string format."""
        return (f"{self.__class__.__name__}("
                f"payload={bytes_to_hex(self.payload)}, "
                f"addressing_type={self.addressing_type})")

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """
        Compare with other object.

        :param other: Object to compare.

        :return: True if other object has the same type and carries the same diagnostic message, otherwise False.
        """

    @property
    @abstractmethod
    def payload(self) -> bytes | bytearray:
        """Raw payload bytes carried by this diagnostic message."""

    @property
    @abstractmethod
    def addressing_type(self) -> AddressingType:
        """Addressing for which this diagnostic message is relevant."""


class UdsMessage(AbstractUdsMessageContainer):
    """
    Representation of a diagnostic message.

    Objects of this class store all relevant attributes of a
    :ref:`diagnostic message <knowledge-base-diagnostic-message>`.
    Such objects can later be used for message segmentation or transmission.
    Historical data associated with a transmitted message is stored
    in :class:`~uds.message.uds_message.UdsMessageRecord`.
    """

    def __init__(self, payload: RawBytesAlias, addressing_type: AddressingType) -> None:
        """
        Create a storage for a single diagnostic message.

        :param payload: Raw payload bytes carried by this diagnostic message.
        :param addressing_type: Addressing for which this diagnostic message is relevant.
        """
        self.payload = payload
        self.addressing_type = addressing_type

    def __eq__(self, other: object) -> bool:
        """
        Compare with other object.

        :param other: Object to compare.

        :raise TypeError: Compared value is not an instance of UdsMessage class.

        :return: True if other object has the same type and carries the same diagnostic message, otherwise False.
        """
        if not isinstance(other, self.__class__):
            raise TypeError("UDS Message addressing only be compared with another UDS Message. "
                            f"Actual type: {type(other)}.")
        return self.addressing_type == other.addressing_type and self.payload == other.payload

    @property
    def payload(self) -> bytearray:
        """Raw payload bytes carried by this diagnostic message."""
        return self.__payload

    @payload.setter
    def payload(self, value: RawBytesAlias) -> None:
        """
        Set value of raw payload bytes that this diagnostic message carries.

        :param value: Payload value to set.
        """
        validate_raw_bytes(value)
        self.__payload = bytearray(value)

    @property
    def addressing_type(self) -> AddressingType:
        """Addressing for which this diagnostic message is relevant."""
        return self.__addressing_type

    @addressing_type.setter
    def addressing_type(self, value: AddressingType) -> None:
        """
        Set value of addressing for this diagnostic message.

        :param value: Addressing value to set.
        """
        self.__addressing_type = AddressingType.validate_member(value)


class UdsMessageRecord(AbstractUdsMessageContainer):
    """Container for historical information about a diagnostic message that was received or transmitted."""

    def __init__(self, packets_records: PacketsRecordsSequenceAlias) -> None:
        """
        Create a record of historic information about a diagnostic message.

        :param packets_records: Sequence (in transmission order) of packets records that carried
            this diagnostic message.
        """
        self.packets_records = packets_records

    def __eq__(self, other: object) -> bool:
        """
        Compare with other object.

        :param other: Object to compare.

        :raise TypeError: Compared value is not an instance of UdsMessageRecord class.

        :return: True if other object has the same type and carries the same diagnostic message, otherwise False.
        """
        if not isinstance(other, self.__class__):
            raise TypeError("UDS Message Record addressing only be compared with another UDS Message Record. "
                            f"Actual type: {type(other)}.")
        return self.addressing_type == other.addressing_type \
            and self.payload == other.payload \
            and self.direction == other.direction

    def __str__(self) -> str:
        """Present object in string format."""
        return (f"{self.__class__.__name__}("
                f"payload={bytes_to_hex(self.payload)}, "
                f"addressing_type={self.addressing_type}, "
                f"direction={self.direction}, "
                f"transmission_start_time={self.transmission_start_time}, "
                f"transmission_start_timestamp={self.transmission_start_timestamp}, "
                f"transmission_end_time={self.transmission_end_time}, "
                f"transmission_end_timestamp={self.transmission_end_timestamp})")

    @staticmethod
    def __validate_packets_records(value: PacketsRecordsSequenceAlias) -> None:
        """
        Validate whether the argument contains records with packets.

        :param value: Value to validate.

        :raise TypeError: Provided value is not a sequence.
        :raise ValueError: At least one of sequence elements is not an object of
            :class:`~uds.message.uds_packet.AbstractPacketRecord` class.
        """
        if not isinstance(value, Sequence):
            raise TypeError(f"Provided value is not a sequence. Actual type: {type(value)}")
        if not value or any(not isinstance(element, AbstractPacketRecord) for element in value):
            raise ValueError("Provided value must contain only instances of AbstractPacketRecord class. "
                             f"Actual value: {value}.")

    @property
    def packets_records(self) -> PacketsRecordsTupleAlias:
        """
        Sequence (in transmission order) of packets records that carried this diagnostic message.

        :ref:`Packets <knowledge-base-packet>` sequence is a complete sequence of packets that was exchanged
        during this diagnostic message transmission.
        """
        return self.__packets_records

    @packets_records.setter
    def packets_records(self, value: PacketsRecordsSequenceAlias) -> None:
        """
        Assign records value of packets that carried this diagnostic message .

        Provided value must be a complete sequence of :ref:`packets <knowledge-base-packet>` that were exchanged
        during this diagnostic message transmission.
        Sequence must not contain any packets that are unrelated to transmission of this message.

        :param value: Sequence of Packet Records to set.

        raise ReassignmentError("Value of 'frame' attribute cannot be changed once set.")
        """
        if hasattr(self, "_UdsMessageRecord__packets_records"):
            raise ReassignmentError("Value of 'packets_records' attribute cannot be changed once set.")
        self.__validate_packets_records(value)
        self.__packets_records = tuple(value)

    @property
    def payload(self) -> bytes:
        """Raw payload bytes carried by this diagnostic message."""
        number_of_bytes = self.packets_records[0].data_length
        message_payload = bytearray()
        for packet in self.packets_records:
            if packet.payload is not None:
                message_payload += bytearray(packet.payload)
        return bytes(message_payload[:number_of_bytes])

    @property
    def addressing_type(self) -> AddressingType:
        """Addressing which was used to transmit this diagnostic message."""
        return self.packets_records[0].addressing_type

    @property
    def direction(self) -> TransmissionDirection:
        """Information whether this message was received or sent."""
        return self.packets_records[0].direction

    @property
    def transmission_start_time(self) -> datetime:
        """
        Get the approximate wall-clock time at which this message transmission was initiated.

        .. warning:: This value is approximate.
            The most precise available timestamp is provided by
            :attr:`~uds.message.uds_message.UdsMessageRecord.transmission_start_native_timestamp`.
        """
        return self.packets_records[0].transmission_time

    @property
    def transmission_end_time(self) -> datetime:
        """
        Get the approximate wall-clock time at which this message transmission was completed.

        .. warning:: This value is approximate.
            The most precise available timestamp is provided by
            :attr:`~uds.message.uds_message.UdsMessageRecord.transmission_end_native_timestamp`.
        """
        return self.packets_records[-1].transmission_time

    @property
    def transmission_start_timestamp(self) -> float:
        """
        Get the approximate monotonic timestamp associated with the start of this message transmission.

        .. warning:: This value is approximate.
            The most precise available timestamp is provided by
            :attr:`~uds.message.uds_message.UdsMessageRecord.transmission_start_native_timestamp`.
        """
        return self.packets_records[0].transmission_timestamp

    @property
    def transmission_end_timestamp(self) -> float:
        """
        Get the approximate monotonic timestamp associated with the end of this message transmission.

        .. warning:: This value is approximate.
            The most precise available timestamp is provided by
            :attr:`~uds.message.uds_message.UdsMessageRecord.transmission_end_native_timestamp`.
        """
        return self.packets_records[-1].transmission_timestamp

    @property
    def transmission_start_native_timestamp(self) -> float:
        """
        Get the native timestamp at the start of this message transmission.

        This timestamp is provided by the underlying Transport Interface.
        """
        return self.packets_records[0].transmission_native_timestamp

    @property
    def transmission_end_native_timestamp(self) -> float:
        """
        Get the native timestamp at the end of this message transmission.

        This timestamp is provided by the underlying Transport Interface.
        """
        return self.packets_records[-1].transmission_native_timestamp

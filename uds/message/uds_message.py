"""
Module with common implementation of all diagnostic messages (requests and responses).

:ref:`Diagnostic message <knowledge-base-diagnostic-message>` are defined on upper layers of UDS OSI Model.
"""

__all__ = ["AbstractUdsMessageContainer", "UdsMessage", "UdsMessageRecord"]

from typing import Any
from abc import ABC, abstractmethod
from datetime import datetime

from uds.utilities import RawBytesAlias, RawBytesTupleAlias, RawBytesListAlias, validate_raw_bytes, ReassignmentError
from uds.transmission_attributes import TransmissionDirection, AddressingType
from uds.packet import AbstractUdsPacketRecord, PacketsRecordsTuple, PacketsRecordsSequence


class AbstractUdsMessageContainer(ABC):
    """Abstract definition of a container with a diagnostic message information."""

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """
        Compare with other object.

        :param other: Object to compare.

        :return: True if other object has the same type and carries the same diagnostic message, otherwise False.
        """

    @property
    @abstractmethod
    def payload(self) -> RawBytesTupleAlias:
        """Raw payload bytes carried by this diagnostic message."""

    @property
    @abstractmethod
    def addressing_type(self) -> AddressingType:
        """Addressing for which this diagnostic message is relevant."""


class UdsMessage(AbstractUdsMessageContainer):
    """
    Definition of a diagnostic message.

    Objects of this class act as a storage for all relevant attributes of a
    :ref:`diagnostic message <knowledge-base-diagnostic-message>`.
    Later on, such object might be used in a segmentation process or to transmit the message.
    Once a message is transmitted, its historic data would be stored in
    :class:`~uds.message.uds_message.UdsMessageRecord`.
    """

    def __init__(self, payload: RawBytesAlias, addressing_type: AddressingType) -> None:
        """
        Create a storage for a single diagnostic message.

        :param payload: Raw payload bytes carried by this diagnostic message.
        :param addressing_type: Addressing for which this diagnostic message is relevant.
        """
        self.payload = payload  # type: ignore
        self.addressing_type = addressing_type

    def __eq__(self, other: object) -> bool:
        """
        Compare with other object.

        :param other: Object to compare.

        :return: True if other object has the same type and carries the same diagnostic message, otherwise False.
        """
        if not isinstance(other, self.__class__):
            raise TypeError("UDS Message can only be compared with another UDS Message")
        return self.addressing_type == other.addressing_type and self.payload == other.payload

    @property
    def payload(self) -> RawBytesTupleAlias:
        """Raw payload bytes carried by this diagnostic message."""
        return self.__payload

    @payload.setter
    def payload(self, value: RawBytesAlias):
        """
        Set value of raw payload bytes that this diagnostic message carries.

        :param value: Payload value to set.
        """
        validate_raw_bytes(value)
        self.__payload = tuple(value)

    @property
    def addressing_type(self) -> AddressingType:
        """Addressing for which this diagnostic message is relevant."""
        return self.__addressing_type

    @addressing_type.setter
    def addressing_type(self, value: AddressingType):
        """
        Set value of addressing for this diagnostic message.

        :param value: Addressing value to set.
        """
        self.__addressing_type = AddressingType.validate_member(value)


class UdsMessageRecord(AbstractUdsMessageContainer):
    """Storage for historic information about a diagnostic message that was either received or transmitted."""

    def __init__(self, packets_records: PacketsRecordsSequence) -> None:
        """
        Create a record of historic information about a diagnostic message that was either received or transmitted.

        :param packets_records: Sequence (in transmission order) of UDS packets records that carried this
            diagnostic message.
        """
        self.packets_records = packets_records  # type: ignore

    def __eq__(self, other: object) -> bool:
        """
        Compare with other object.

        :param other: Object to compare.

        :return: True if other object has the same type and carries the same diagnostic message, otherwise False.
        """
        if not isinstance(other, self.__class__):
            raise TypeError("UDS Message Record can only be compared with another UDS Message Record")
        return self.addressing_type == other.addressing_type \
            and self.payload == other.payload \
            and self.direction == other.direction

    @staticmethod
    def __validate_packets_records(value: Any) -> None:
        """
        Validate whether the argument contains UDS Packets records.

        :param value: Value to validate.

        :raise TypeError: UDS Packet Records sequence is not list or tuple type.
        :raise ValueError: At least one of UDS Packet Records sequence elements is not an object of
            :class:`~uds.message.uds_packet.AbstractUdsPacketRecord` class.
        """
        if not isinstance(value, (tuple, list)):
            raise TypeError(f"Provided value is not list or tuple type. "
                            f"Actual type: {type(value)}")
        if not value or any(not isinstance(element, AbstractUdsPacketRecord) for element in value):
            raise ValueError(f"Provided value must contain only instances of AbstractUdsPacketRecord class. "
                             f"Actual value: {value}")

    @property
    def packets_records(self) -> PacketsRecordsTuple:
        """
        Sequence (in transmission order) of UDS packets records that carried this diagnostic message.

        :ref:`UDS packets <knowledge-base-uds-packet>` sequence is a complete sequence of packets that was exchanged
        during this diagnostic message transmission.
        """
        return self.__packets_records

    @packets_records.setter
    def packets_records(self, value: PacketsRecordsSequence):
        """
        Assign records value of UDS Packets that carried this diagnostic message .

        Provided :ref:`UDS packets <knowledge-base-uds-packet>` sequence must be a complete sequence of packets that
        was exchanged during this diagnostic message transmission. Sequence must not contain any packets that are
        unrelated to transmission of this message.

        :param value: UDS Packet Records sequence value to set.

        :raise ReassignmentError: There is a call to change the value after the initial assignment (in __init__).
        """
        try:
            getattr(self, "_UdsMessageRecord__packets_records")
        except AttributeError:
            self.__validate_packets_records(value)
            self.__packets_records = tuple(value)
        else:
            raise ReassignmentError("You cannot change value of 'packets_records' attribute once it is assigned.")

    @property
    def payload(self) -> RawBytesTupleAlias:
        """Raw payload bytes carried by this diagnostic message."""
        number_of_bytes = self.packets_records[0].data_length
        message_payload: RawBytesListAlias = []
        for packet in self.packets_records:
            if packet.payload is not None:
                message_payload.extend(packet.payload)
        return tuple(message_payload[:number_of_bytes])

    @property
    def addressing_type(self) -> AddressingType:
        """Addressing which was used to transmit this diagnostic message."""
        return self.packets_records[0].addressing_type

    @property
    def direction(self) -> TransmissionDirection:
        """Information whether this message was received or sent."""
        return self.packets_records[0].direction

    @property  # noqa: F841
    def transmission_start(self) -> datetime:
        """
        Time stamp when transmission of this message was initiated.

        It is determined by a moment of time when the first packet (that carried this message) was published
        to a bus (either received or transmitted).

        :return: Time stamp when transmission of this message was initiated.
        """
        return self.packets_records[0].transmission_time

    @property  # noqa: F841
    def transmission_end(self) -> datetime:
        """
        Time stamp when transmission of this message was completed.

        It is determined by a moment of time when the last packet (that carried this message) was published
        to a bus (either received or transmitted).

        :return: Time stamp when transmission of this message was completed.
        """
        return self.packets_records[-1].transmission_time

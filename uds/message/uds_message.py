"""
Module with common implementation of all diagnostic messages (requests and responses).

:ref:`Diagnostic message <knowledge-base-diagnostic-message>` are defined on upper layers of UDS OSI Model.
"""

__all__ = ["UdsMessage", "UdsMessageRecord"]

from typing import Any

from uds.utilities import RawBytes, RawBytesTuple, validate_raw_bytes, ReassignmentError, TimeStamp
from uds.transmission_attributes import TransmissionDirection, AddressingType, AddressingTypeAlias
from uds.packet import AbstractUdsPacketRecord, PacketsRecordsTuple, PacketsRecordsSequence


class UdsMessage:
    """
    Definition of a diagnostic message.

    Objects of this class act as a storage for all relevant attributes of a
    :ref:`diagnostic message <knowledge-base-diagnostic-message>`.
    Later on, such object might be used in a segmentation process or to transmit the message.
    Once a message is transmitted, its historic data would be stored in
    :class:`~uds.message.uds_message.UdsMessageRecord`.
    """

    def __init__(self, payload: RawBytes, addressing_type: AddressingTypeAlias) -> None:
        """
        Create a storage for a single diagnostic message.

        :param payload: Raw bytes of payload that this diagnostic message carries.
        :param addressing_type: Addressing type for which this message is relevant.
        """
        self.payload = payload  # type: ignore
        self.addressing_type = addressing_type  # type: ignore

    @property
    def payload(self) -> RawBytesTuple:
        """Raw bytes of payload that this diagnostic message carries."""
        return self.__payload

    @payload.setter
    def payload(self, value: RawBytes):
        """
        Set value of raw payload bytes that this diagnostic message carries.

        :param value: Payload value to set.
        """
        validate_raw_bytes(value)
        self.__payload = tuple(value)

    @property
    def addressing_type(self) -> AddressingType:
        """Addressing type for which this message is relevant."""
        return self.__addressing_type

    @addressing_type.setter
    def addressing_type(self, value: AddressingTypeAlias):
        """
        Set value of addressing type for which this diagnostic message is relevant.

        :param value: Addressing value to set.
        """
        AddressingType.validate_member(value)
        self.__addressing_type = AddressingType(value)


class UdsMessageRecord:
    """Storage for historic information about a diagnostic message that was either received or transmitted."""

    def __init__(self, payload: RawBytes, packets_records: PacketsRecordsSequence) -> None:
        """
        Create a record of a historic information about a diagnostic message that was either received or transmitted.

        :param packets_records: Sequence (in transmission order) of UDS packets records that carried this
            diagnostic message.
        """
        self.payload = payload  # type: ignore
        self.packets_records = packets_records  # type: ignore

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
    def payload(self) -> RawBytesTuple:
        """Raw bytes of payload that this diagnostic message carried."""
        return self.__payload

    @payload.setter
    def payload(self, value: RawBytes):
        """
        Set value of raw payload bytes which this diagnostic message carried.

        :param value: Payload value to set.

        :raise ReassignmentError: There is a call to change the value after the initial assignment (in __init__).
        """
        try:
            self.__getattribute__("_UdsMessageRecord__payload")
        except AttributeError:
            validate_raw_bytes(value)
            self.__payload = tuple(value)
        else:
            raise ReassignmentError("You cannot change value of 'payload' attribute once it is assigned.")

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
            self.__getattribute__("_UdsMessageRecord__packets_records")
        except AttributeError:
            self.__validate_packets_records(value)
            self.__packets_records = tuple(value)
        else:
            raise ReassignmentError("You cannot change value of 'packets_records' attribute once it is assigned.")

    @property
    def addressing_type(self) -> AddressingType:
        """Addressing type which was used to transmit this message."""
        return self.packets_records[0].addressing_type

    @property
    def direction(self) -> TransmissionDirection:
        """Information whether this message was received or sent by the code."""
        return self.packets_records[0].direction

    @property  # noqa: F841
    def transmission_start(self) -> TimeStamp:
        """
        Time stamp when transmission of this message was initiated.

        It is determined by a moment of time when the first packet (that carried this message) was published
        to a bus (either received or transmitted).

        :return: Time stamp when transmission of this message was initiated.
        """
        return self.packets_records[0].transmission_time

    @property  # noqa: F841
    def transmission_end(self) -> TimeStamp:
        """
        Time stamp when transmission of this message was completed.

        It is determined by a moment of time when the last packet (that carried this message) was published
        to a bus (either received or transmitted).

        :return: Time stamp when transmission of this message was completed.
        """
        return self.packets_records[-1].transmission_time

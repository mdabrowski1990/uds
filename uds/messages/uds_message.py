"""Common implementation of all diagnostic messages (requests and responses)."""

__all__ = ["UdsMessage", "UdsMessageRecord"]

from typing import Union, Tuple, List

from uds.utilities import RawBytes, RawBytesTuple, validate_raw_bytes, ReassignmentError, TimeStamp
from .transmission_attributes import AddressingType, AddressingMemberTyping, TransmissionDirection
from .uds_packet import AbstractUdsPacketRecord

PacketsRecordsTuple = Tuple[AbstractUdsPacketRecord, ...]
PacketsRecordsSequence = Union[PacketsRecordsTuple,  # pylint: disable=unsubscriptable-object
                               List[AbstractUdsPacketRecord]]


class UdsMessage:
    """Definition of diagnostic messages that are exchanged by UDS servers and clients."""

    def __init__(self, raw_message: RawBytes, addressing: AddressingMemberTyping) -> None:
        """
        Create a storage for a single diagnostic message.

        :param raw_message: Raw bytes of data that this diagnostic message carries.
        :param addressing: Addressing type for which this message is relevant.
        """
        self.raw_message = raw_message  # type: ignore
        self.addressing = addressing  # type: ignore

    @property
    def raw_message(self) -> RawBytesTuple:
        """Raw bytes of data that this diagnostic message carries."""
        return self.__raw_message

    @raw_message.setter
    def raw_message(self, value: RawBytes):
        """
        Set value of raw data bytes that this diagnostic message carries.

        :param value: Raw message value to set.
        """
        validate_raw_bytes(value)
        self.__raw_message = tuple(value)

    @property
    def addressing(self) -> AddressingType:
        """Addressing type for which this message is relevant."""
        return self.__addressing

    @addressing.setter
    def addressing(self, value: AddressingMemberTyping):
        """
        Set value of addressing type for which this diagnostic message is relevant.

        :param value: Addressing value to set.
        """
        AddressingType.validate_member(value)
        self.__addressing = AddressingType(value)


class UdsMessageRecord:
    """Definition of a record that stores historic information about transmitted or received UDSMessage."""

    def __init__(self, raw_message: RawBytes, packets_records: PacketsRecordsSequence) -> None:
        """
        Create a historic record of a diagnostic message that was either received of transmitted to a bus.

        :param raw_message: Raw bytes of data that this diagnostic message carried.
        :param packets_records: Sequence (in transmission order) of UDS packets records that carried this
            diagnostic message.
        """
        self.raw_message = raw_message  # type: ignore
        self.packets_records = packets_records  # type: ignore

    @staticmethod
    def __validate_packets_records(packets_records: PacketsRecordsSequence) -> None:
        """
        Validate UDS Packet Records sequence argument.

        :param packets_records: Value of UDS Packet Records sequence to validate.

        :raise TypeError: UDS Packet Records sequence is not list or tuple type.
        :raise ValueError: At least one of UDS Packet Records sequence elements is not an object of
            AbstractUdsPacketRecord class.
        """
        if not isinstance(packets_records, (tuple, list)):
            raise TypeError(f"Provided value of 'packets_records' is not list or tuple type. "
                            f"Actual type: {type(packets_records)}.")
        if not packets_records or any([not isinstance(packet, AbstractUdsPacketRecord) for packet in packets_records]):
            raise ValueError(f"Provided value of 'packets_records' must contain only instances of "
                             f"AbstractUdsPacketRecord class. Actual value: {packets_records}")

    @property
    def raw_message(self) -> RawBytesTuple:
        """Raw bytes of data that this diagnostic message carried."""
        return self.__raw_message

    @raw_message.setter
    def raw_message(self, value: RawBytes):
        """
        Set value of raw message which this diagnostic message carried.

        :param value: Raw message value to set.

        :raise ReassignmentError: There is a call to change the value after the initial assignment (in __init__).
        """
        try:
            self.__getattribute__("_UdsMessageRecord__raw_message")
        except AttributeError:
            validate_raw_bytes(value)
            self.__raw_message = tuple(value)
        else:
            raise ReassignmentError("You cannot change value of 'raw_message' attribute once it is assigned.")

    @property
    def packets_records(self) -> PacketsRecordsTuple:
        """Sequence (in transmission order) of UDS packets records that carried this diagnostic message."""
        return self.__packets_records

    @packets_records.setter
    def packets_records(self, value: PacketsRecordsSequence):
        """
        Assign records value of UDS Packets that carried this diagnostic message .

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
    def addressing(self) -> AddressingType:
        """Addressing type which was used to transmit this message."""
        return self.packets_records[0].addressing

    @property
    def direction(self) -> TransmissionDirection:
        """Information whether this message was received or sent by the code."""
        return self.packets_records[0].direction

    @property  # noqa: F841
    def transmission_start(self) -> TimeStamp:
        """
        Time stamp when transmission of this messages was initiated.

        It is determined by a moment of time when the first packet (that carried this message) was published
        to a bus (either received or transmitted).

        :return: Time stamp when transmission of this message was initiated.
        """
        return self.packets_records[0].transmission_time

    @property  # noqa: F841
    def transmission_end(self) -> TimeStamp:
        """
        Time stamp when transmission of this messages was completed.

        It is determined by a moment of time when the last packet (that carried this message) was published
        to a bus (either received or transmitted).

        :return: Time stamp when transmission of this message was completed.
        """
        return self.packets_records[-1].transmission_time

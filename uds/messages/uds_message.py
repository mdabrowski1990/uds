"""Common implementation of all UDS messages (requests and responses)."""

__all__ = ["UdsMessage", "UdsMessageRecord"]

from typing import Union, Tuple, List

from uds.utilities import RawBytes, RawBytesTuple, validate_raw_bytes, ReassignmentError, TimeStamp
from .transmission_attributes import AddressingType, AddressingMemberTyping, TransmissionDirection
from .npdu import AbstractNPDURecord

NPDURecordsTuple = Tuple[AbstractNPDURecord, ...]
NPDURecordsSequence = Union[NPDURecordsTuple, List[AbstractNPDURecord]]  # pylint: disable=unsubscriptable-object


class UdsMessage:
    """Definition a diagnostic messages that are exchanged by UDS servers and clients."""

    def __init__(self, raw_message: RawBytes, addressing: AddressingMemberTyping) -> None:
        """
        Create a storage for information of a single diagnostic message.

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
        Set value of raw message which this diagnostic message carries.

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

    def __init__(self, raw_message: RawBytes, npdu_sequence: NPDURecordsSequence) -> None:
        """
        Create historic record of a diagnostic message that was either received of transmitted to a bus.

        :param raw_message: Raw bytes of data that this diagnostic message carried.
        :param npdu_sequence: Record of N_PDUs (in transmission order) that carried this diagnostic message.
        """
        self.raw_message = raw_message  # type: ignore
        self.npdu_sequence = npdu_sequence  # type: ignore

    @staticmethod
    def __validate_npdu_sequence(npdu_sequence: NPDURecordsSequence) -> None:
        """
        Validate N_PDUs sequence argument.

        :param npdu_sequence: Value of N_PDUs sequence to validate.

        :raise TypeError: N_PDUs sequence is not list or tuple type.
        :raise ValueError: At least one of N_PDUs sequence elements is not an object of N_PDU.
        """
        if not isinstance(npdu_sequence, (tuple, list)):
            raise TypeError(f"Provided value of 'npdu_sequence' is not list or tuple type. "
                            f"Actual type: {type(npdu_sequence)}.")
        if not npdu_sequence or any([not isinstance(npdu, AbstractNPDURecord) for npdu in npdu_sequence]):
            raise ValueError(f"Provided value of 'npdu_sequence' must contain only instances of AbstractNPDURecord "
                             f"class. Actual value: {npdu_sequence}")

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
    def npdu_sequence(self) -> NPDURecordsTuple:
        """Sequence (in transmission order) of Network Protocol Data Units that carried this diagnostic message."""
        return self.__npdu_sequence

    @npdu_sequence.setter
    def npdu_sequence(self, value: NPDURecordsSequence):
        """
        Assign N_PDUs which carried this diagnostic message .

        :param value: N_PDUs sequence value to set.

        :raise ReassignmentError: There is a call to change the value after the initial assignment (in __init__).
        """
        try:
            self.__getattribute__("_UdsMessageRecord__npdu_sequence")
        except AttributeError:
            self.__validate_npdu_sequence(value)
            self.__npdu_sequence = tuple(value)
        else:
            raise ReassignmentError("You cannot change value of 'npdu_sequence' attribute once it is assigned.")

    @property
    def addressing(self) -> AddressingType:
        """Addressing type which was used to transmit this message."""
        return self.npdu_sequence[0].addressing

    @property
    def direction(self) -> TransmissionDirection:
        """Information whether this message was received or sent by the code."""
        return self.npdu_sequence[0].direction

    @property  # noqa: F841
    def transmission_start(self) -> TimeStamp:
        """
        Time stamp when transmission of this messages was initiated.

        It is determined by a moment of time when the first N_PDU (that carried this message) was either published
        to a bus (either received or transmitted).

        :return: Time stamp when transmission of this message was initiated.
        """
        return self.npdu_sequence[0].transmission_time

    @property  # noqa: F841
    def transmission_end(self) -> TimeStamp:
        """
        Time stamp when transmission of this messages was completed.

        It is determined by a moment of time when the last N_PDU (that carried this message) was either published
        to a bus (either received or transmitted).

        :return: Time stamp when transmission of this message was completed.
        """
        return self.npdu_sequence[-1].transmission_time

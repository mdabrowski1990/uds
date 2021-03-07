"""Common implementation of all UDS messages (requests and responses)."""

__all__ = ["UdsMessage"]

from typing import Optional

from .addressing import AddressingType
from .pdu import AbstractPDU
from .types import RawMessage, PDUs


class UdsMessage:
    """Common implementation of all UDS messages (requests and responses)."""

    def __init__(self,
                 raw_message: RawMessage,
                 pdu_sequence: Optional[PDUs] = None) -> None:  # pylint: disable=unsubscriptable-object
        """
        Create storage for a single UDS message.

        :param raw_message: A single message that consists of raw bytes only.
        :param pdu_sequence: Sequence of PDUs (Protocol Data Units) that were published to a bus to send/receive
            this messages. It should be None, if message was never transmitted.
        """
        # verify arguments
        self.__validate_raw_message(raw_message=raw_message)
        if pdu_sequence is not None:
            self.__validate_pdu_sequence(pdu_sequence=pdu_sequence)
        # update data
        self.__raw_message = tuple(raw_message)
        self.__pdu_sequence = tuple() if pdu_sequence is None else tuple(pdu_sequence)

    @staticmethod
    def __validate_raw_message(raw_message: RawMessage) -> None:
        """
        Verify raw message argument.

        :param raw_message: Raw message value to validate.

        :raise TypeError: Raw message is not list or tuple type.
        :raise ValueError: Any of raw message elements is not raw byte value.
        """
        if not isinstance(raw_message, (tuple, list)):
            raise TypeError("'raw_message' is not list or tuple type")
        if not all([isinstance(raw_byte, int) and 0x00 <= raw_byte <= 0xFF for raw_byte in raw_message]):
            raise ValueError("'raw_message' does not contain raw bytes (int value between 0 and 255) values only")

    @staticmethod
    def __validate_pdu_sequence(pdu_sequence: PDUs) -> None:
        """
        Verify pdu sequence argument.

        :param pdu_sequence: PDUs sequence to validate.

        :raise TypeError: PDUs sequence is not list or tuple type.
        :raise ValueError: Any of PDUs sequence elements is not PDU.
        """
        if not isinstance(pdu_sequence, (tuple, list)):
            raise TypeError("'pdu_sequence' is not list or tuple type")
        if not all([isinstance(pdu, AbstractPDU) for pdu in pdu_sequence]):
            raise ValueError("'pdu_sequence' does not contain AbstractPDU instances only")

    @property
    def pdu_sequence(self) -> PDUs:
        """
        Get PDUs that were sent/received to transmit this message over any bus.

        :return: PDUs list that were sent/received or empty list if this message was never transmitted.
        """
        return self.__pdu_sequence

    @property
    def raw_message(self) -> RawMessage:
        """Raw message that this message carries."""
        return self.__raw_message

    @property
    def addressing(self) -> Optional[AddressingType]:  # pylint: disable=unsubscriptable-object
        """
        Addressing type over which this message was transmitted.

        :return: Addressing over which this message was sent/received. None if messages was never transmitted.
        """
        return self.pdu_sequence[0].addressing if self.pdu_sequence else None

"""Common implementation of all UDS messages (requests and responses)."""

__all__ = ["UdsMessage"]

from typing import List, Optional

from .addressing import AddressingType

TypingRawMessage = List[int]


class UdsMessage:
    """Common implementation of all UDS messages (requests and responses)."""

    def __init__(self, raw_message: TypingRawMessage, pdu_list=None) -> None:  # TODO: annotation
        """
        Create storage related to a single UDS messages.

        :param raw_message: Raw messages (list of bytes).
        :param pdu_list: List of PDUs (Protocol Data Units) that were published to a bus to transmit/receive
            this messages.
        """
        self.__raw_message = raw_message
        self.__pdu_list = [] if pdu_list is None else pdu_list

    @property
    def pdu_list(self) -> List:  # TODO: annotation
        """
        Get PDUs list that were transmitted/received and together make this message.

        :return: PDUs list that were transmitted/received or empty list if this message was not transmitted/received.
        """
        return self.__pdu_list

    @property
    def raw_message(self) -> TypingRawMessage:
        """Getter of 'raw_message' that this object carries."""
        return self.__raw_message

    @property
    def addressing(self) -> Optional[AddressingType]:
        """
        Get of addressing type over which this message were transmitted/received.

        :return: Addressing over which the messages was transmitted/received.
            None if messages was not transmitted/received.
        """
        return self.pdu_list[0].addressing if self.pdu_list else None

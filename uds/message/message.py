"""Module with UDS messages (requests and responses) implementation."""

__all__ = ["UdsMessage", "UdsRequest", "UdsResponse"]

from typing import List
from enum import Enum

TypingRawMessage = List[int]


class AddressingType(Enum):
    """
    Types of communication (addressing) defined by UDS.

    Options:
    - PHYSICAL - 1 (client) to 1 (server) communication
    - FUNCTIONAL - 1 (client) to many (servers) communication
    - BROADCAST - 1 (client) to many (servers) communication that does not require response
    """

    PHYSICAL = "Physical"
    FUNCTIONAL = "Functional"
    BROADCAST = "Broadcast"


class UdsResponseType(Enum):
    """
    Types of UDS response messages.

    Options:
    - POSITIVE - response message
        WARNING! Positive response message might be incompatible with messaging database
    - NEGATIVE - negative response message in format [0x7F, SID, NRC]
        Where:
        SID - Service Identifier of request (identifies request to which it is response)
        NRC - Negative Response Code (provides reason why responded negatively)
    - INVALID - response message that is incompatible with UDS standard
    """

    POSITIVE = "Positive Response Message"
    NEGATIVE = "Negative Response Message"
    INVALID = "Invalid"


class UdsMessage:
    """Common implementation of UDS messages (requests and responses)."""

    def __init__(self, raw_message: TypingRawMessage, pdu_list=None) -> None:  # TODO: annotation
        """
        Create storage related to a single UDS message.

        :param raw_message: Raw message (list of bytes).
        :param pdu_list: List of PDUs (Protocol Data Units) that were published to a bus to transmit/receive
            this message.
        """
        self.__raw_message = raw_message
        self.__pdu_list = [] if pdu_list is None else pdu_list

    @property
    def pdu_list(self):  # TODO: annotation
        """:return: List of PDUs (Protocol Data Units) that were published to a bus to transmit/receive this message."""
        return self.__pdu_list

    @property
    def raw_message(self) -> TypingRawMessage:
        """Getter of 'raw_message' that this object carries."""
        return self.__raw_message

    @property
    def addressing(self):  # TODO: annotation
        """Getter of 'addressing' over which the message was transmitted,"""
        return self.pdu_list[0].addressing if self.pdu_list else None


class UdsRequest(UdsMessage):
    """
    Storage for diagnostic requests information.

    UDS request is always sent by client and received by server.
    """


class UdsResponse(UdsMessage):
    """
    Storage for diagnostic responses information.

    UDS response is always sent by server and received by client.
    """

    def get_response_type(self) -> UdsResponseType:
        if self.raw_message:
            if len(self.raw_message) == 3 and self.raw_message[0] ==
        return UdsResponseType.INVALID

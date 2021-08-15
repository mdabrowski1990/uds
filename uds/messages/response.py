"""Module with UDS response messages implementation."""

__all__ = ["UdsResponse", "UdsResponseType"]

from enum import Enum

from .uds_message import UdsMessage
from .service_identifiers import RequestSID, ResponseSID


class UdsResponseType(Enum):
    """
    Types of UDS response messages.

    Options:
    - POSITIVE - response messages
        !WARNING! Note that this status does not reflect compatibility with message format (messaging database).
    - NEGATIVE - negative response messages in format [0x7F, SID, NRC]
        Where:
        SID - Service Identifier of request (identifies request to which it is response)
        NRC - Negative Response Code (provides reason why responded negatively)
    - INVALID - response messages that is incompatible with UDS standard
    """

    POSITIVE = "Positive Response Message"
    NEGATIVE = "Negative Response Message"
    INVALID = "Invalid"


class UdsResponse(UdsMessage):
    """
    Storage for a single diagnostic response message.

    UDS response is always sent by a server and received by a client.
    """

    def get_response_type(self) -> UdsResponseType:
        """Get type of this response message."""
        if self.raw_message:
            if len(self.raw_message) == 3 and self.raw_message[0] == ResponseSID.NegativeResponse and \
                    RequestSID.is_request_sid(value=self.raw_message[1]):
                return UdsResponseType.NEGATIVE
            if ResponseSID.is_response_sid(self.raw_message[0]):
                return UdsResponseType.POSITIVE
        return UdsResponseType.INVALID

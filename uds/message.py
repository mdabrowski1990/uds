"""Module with UDS messages (requests and responses) implementation."""

__all__ = ["UdsMessage", "UdsRequest", "UdsResponse"]


from enum import Enum


class Addressing(Enum):
    # TODO: docsstring

    PHYSICAL = "Physical"
    FUNCTIONAL = "Functional"
    # TODO: ? BROADCAST = "Broadcast"


class UdsResponseType(Enum):
    # TODO: docstring

    POSITIVE = "Positive Response Message"
    NEGATIVE = "Negative Response Message"
    INVALID = "Invalid"


class UdsMessage:
    """Common implementation of UDS messages (requests and responses)."""

    def __init__(self, raw_message):
        self.__raw_message = raw_message
        self.__pdu_list = []

    def __set_pdu_list(self, pdu_list):  # TODO: annotation
        # TODO verify, these are PDUs
        self.__pdu_list = pdu_list

    def __get_pdu_list(self):  # TODO: annotation
        return self.__pdu_list

    pdu_list = property(fget=__get_pdu_list, fset=__set_pdu_list)

    def __set_raw_message(self, raw_message):  # TODO: annotation
        # TODO: reset pdu
        self.__raw_message = raw_message

    def __get_raw_message(self):  # TODO: annotation
        return self.__raw_message

    raw_message = property(fget=__get_raw_message, fset=__set_raw_message)

    @property
    def addressing(self):  # TODO: annotation
        """Getter of 'addressing' over which the message was transmitted,"""
        return self.pdu_list[-1].addressing if self.pdu_list else None


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
        ...  # TODO

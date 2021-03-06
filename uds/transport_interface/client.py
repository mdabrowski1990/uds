"""Transport Interface for Client."""

__all__ = ["UdsSequenceError", "TransportInterfaceClient"]

from abc import abstractmethod

from .types import AddressingType, UdsRequest, UdsResponses
from .common import TransportInterface


class UdsSequenceError(Exception):
    """Request message was not sent before attempt to receive response messages."""


class TransportInterfaceClient(TransportInterface):
    """Abstract definition of Client's side of Transport Interface."""

    @abstractmethod
    def send_request(self, request: UdsRequest, addressing: AddressingType) -> UdsRequest:  # noqa: F841
        """
        Transmit one request message.

        :param request: Request message to transmit.
        :param addressing: Addressing type to use for the transmission.

        :return: Transmitted request message updated with data related to transmission.
        """

    @abstractmethod
    def receive_responses(self, p2_timeout, p2ext_timeout, p6_timeout, p6ext_timeout) -> UdsResponses:  # noqa: F841
        """
        Get all possible responses to the last sent request message.

        WARNING!
        This method will wait till all possible diagnostic responses are received or one of the timeouts occurs.

        :param p2_timeout: Maximal time to wait after the successful transmission of a request message for
            the start of incoming response messages (first PDU).
        :param p2ext_timeout: Maximal time to wait after reception of a negative response message with
            NRC 0x78 (ResponsePending) for the start of incoming response messages.
        :param p6_timeout: Maximal time to wait after the successful transmission of a request message for
            the complete reception of the corresponding response message.
        :param p6ext_timeout: Maximal time to wait after reception of a negative response message with
            NRC 0x78 (ResponsePending) for the complete reception of the corresponding response message.

        :raise UdsSequenceError: Request message was not sent before calling this method.

        :return: All diagnostic responses received to the last sent diagnostic request.
        """

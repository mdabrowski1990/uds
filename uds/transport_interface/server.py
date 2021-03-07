"""Transport Interface for Client."""

__all__ = ["TransportInterfaceServer"]

from abc import abstractmethod
from typing import Optional

from .types import AddressingType, AddressingTypes, UdsRequest, UdsResponse
from .common import TransportInterface


class TransportInterfaceServer(TransportInterface):
    """Abstract definition of Client's side of Transport Interface."""

    @abstractmethod
    def send_response(self,
                      response: UdsResponse,  # noqa: F841
                      addressing: AddressingType,
                      stop_on_request_addressing_types: AddressingTypes) -> Optional[UdsResponse]:  # noqa: F841
        """
        Transmit one response message.

        Example use cases
            - This method was called to response a physically addressed request, but during transmission of
            the response message, another physically addressed request is received (or at least the first PDU).
            Expectations: The transmission of response message shall be aborted, because
            :parameter stop_on_request_addressing_types contains AddressingType.PHYSICAL
            - This method was called to response a physically addressed request, but during transmission of
            the response message, another functionally addressed request is received (e.g. TesterPresent).
            Expectations: The transmission of response message shall be continued, because
            :parameter stop_on_request_addressing_types does not contain AddressingType.FUNCTIONAL

        :param response: Response message to transmit.
        :param addressing: Addressing type to use for the transmission.
        :param stop_on_request_addressing_types: Addressing types of new incoming request messages to stop this
            response message transmission.

        :return: Transmitted response message updated with data related to its transmission.
            None if transmission is aborted due to another request message transmission.
        """

    @abstractmethod
    def get_received_request(self, addressing: Optional[AddressingType] = None) -> Optional[UdsRequest]:
        """
        Get last received request message.

        :param addressing: Addressing type for which last request message to be returned.
            If None given, then the last request message is returned regardless of addressing type over which received.

        :return: Request message that was last received or None if no request message was received.
        """

    @abstractmethod
    def receive_request(self, addressing: Optional[AddressingType] = None) -> UdsRequest:
        """
        Wait till incoming request message is received and return it.

        WARNING
            This method might keep the program in the infinite loop if no request is ever received.

        :param addressing: Addressing type to monitor for incoming request message.
            If None given, then return first request message received over any of the addressing types.

        :return: The first request message that was received since the call of this method.
        """

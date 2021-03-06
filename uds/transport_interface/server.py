"""Transport Interface for Client."""

__all__ = ["TransportInterfaceServer"]

from abc import abstractmethod
from typing import Optional

from .types import AddressingType, UdsRequest, UdsResponse
from .common import TransportInterface


class TransportInterfaceServer(TransportInterface):
    """Abstract definition of Client's side of Transport Interface."""

    @abstractmethod
    def send_response(self,
                      response: UdsResponse,  # noqa: F841
                      addressing: AddressingType) -> UdsResponse:
        """
        Transmit one response message.

        :param response: Response message to transmit.
        :param addressing: Addressing type to use for the transmission.
        TODO: add option to stop transmission on request PDU (physical addressing)
        TODO: add option to stop transmission on request PDU (functional addressing)

        :return: Transmitted response message updated with data related to transmission.
        """

    def get_received_request(self, addressing: Optional[AddressingType] = None) -> Optional[UdsRequest]:
        """
        Get last received request message.

        :param addressing: Addressing type for which last request message to be returned.
            If None given, then the last request message is returned regardless of addressing type over which received.

        :return: Request message that was last received.
        """

    def receive_request(self, addressing: Optional[AddressingType] = None) -> UdsRequest:
        """
        Wait till incoming request message is received and return it.

        :param addressing: Addressing type to monitor for incoming request message.
            If None given, then return first request message received over any of the addressing types.

        :return: The first request message that was received since the call of this method.
        """

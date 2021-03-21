"""Transport Interface for Client."""

__all__ = ["TransportInterfaceServer"]

from abc import abstractmethod

from .types import UdsRequests, UdsResponse
from .common import TransportInterface


class TransportInterfaceServer(TransportInterface):
    """Abstract definition of Client's side of Transport Interface."""

    @abstractmethod
    def flush_received_pdus(self) -> None:
        """Forget all received PDUs that were silently received up to now."""

    @abstractmethod
    def send_response(self, response: UdsResponse) -> UdsResponse:
        """
        Transmit response message.

        :param response: Response message to transmit.

        :return: Transmitted response message updated with data related to its transmission.
        """

    @abstractmethod
    def get_received_requests(self) -> UdsRequests:
        """Get request messages that were received since the last call of this method."""

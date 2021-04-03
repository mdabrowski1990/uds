"""Transport Interface for Client."""

__all__ = ["TransportInterfaceServer"]

from abc import abstractmethod
from typing import Optional

from .types import UdsRequests, UdsResponse, TimeMilliseconds
from .common import TransportInterface


class TransportInterfaceServer(TransportInterface):  # TODO: rework for asynchronous implementation
    """Abstract definition of Client's side of Transport Interface."""

    @abstractmethod
    def flush_received_pdus(self) -> None:
        """Forget all received PDUs that were silently received up to now."""

    @abstractmethod
    async def schedule_response(self, response: UdsResponse,
                                delay: Optional[TimeMilliseconds] = None) -> UdsResponse:  # noqa: F841
        """
        Transmit response message.

        :param response: Response message to transmit.
        :param delay: TODO

        :return: Transmitted response message updated with data related to its transmission.
        """

    @abstractmethod
    def get_received_requests(self) -> UdsRequests:
        """Get request messages that were received since the last call of this method."""

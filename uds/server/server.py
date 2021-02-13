"""Server implementation for UDS protocol."""

__all__ = ["Server", "ResponseManager"]

from uds.transport_protocol import AbstractTPInterface
from .response_manager import ResponseManager


class Server:
    """
    Factory of UDS servers.

    UDS server receives diagnostic requests and sends diagnostic response.
    Each server object simulates a single on-board ECU.
    """

    def __init__(self,
                 tp_interface: AbstractTPInterface,
                 response_manager: ResponseManager) -> None:
        """
        Configure UDS server simulation.

        UDS server will use provided Transport Protocol Interface to receive diagnostic responses and automatically
        respond to them according to set of rules defined in 'response_manager'.

        :param tp_interface: Transport Protocol Interface for handling Layer 4 (and all below) of UDS communication.
        :param response_manager: Manager which decides how to respond to any received diagnostic request.
        """
        self.__tp_interface = tp_interface
        self.__response_manager = response_manager

    def turn_on(self) -> None:
        """Start simulation (automatic responding) of the UDS server."""

    def turn_of(self) -> None:
        """Stop simulation (automatic responding) of the UDS server."""

    response_manager = property()  # TODO: add setter and getter

"""UDS Client side implementation."""

__all__ = ["Client"]

from typing import List

from .transport_protocol import AbstractTPInterface


class Client:
    """
    Factory of UDS clients.

    UDS Client sends diagnostic requests and receives diagnostic response. It always initiates communication
    in each sub-net. Examples of UDS Clients:
    - diagnostic tester
    - gateway node that converts diagnostic request from bus A to bus B (e.g. LIN Master node)
    """

    def __init__(self, tp_interface: AbstractTPInterface) -> None:
        """
        Configure UDS client.

        UDS client will use provided Transport Protocol Interface to send diagnostic requests and receive
        diagnostic responses.

        :param tp_interface: Transport Protocol Interface for handling Layer 4 (and all below) of UDS communication.
        """
        self.__tp_interface = tp_interface

    def send_physical_request(self, request) -> None:  # TODO: annotation
        """
        Send physically (targets a single ECU) addressed request.

        :param request: Diagnostic request to send.
        """

    def send_functional_request(self, request) -> None:  # TODO: annotation
        """
        Send functionally (targets all ECUs) addressed request.

        :param request: Diagnostic request to send.
        """

    def get_responses_to_last_request(self) -> List:
        """
        Get list of responses received to the last sent diagnostic request.

        :return: List with diagnostic response messages received in the chronological order.
        """

    def start_tester_present(self) -> None:  # TODO: consider addressing - physical/functional
        """Turn on cyclical sending of Tester Present message."""
        self.__tp_interface.start_tester_present()

    def stop_tester_present(self) -> None:  # TODO: consider addressing - physical/functional
        """Turn off cyclical sending of Tester Present message."""
        self.__tp_interface.stop_tester_present()

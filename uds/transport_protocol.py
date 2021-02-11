"""
Module with abstract Transport Protocol Interface definition.

Transport Protocol Interface is meant to handle UDS protocol layers 3 (Network) and 4 (Transport Protocol).
There are many buses that supports UDS and each of them has special implementation of these layers, e.g.
- DoCAN
- DoLIN
- DoIP
Due to this, there is need to create common (shared) interface as abstraction layer (in the code), so the implementation
enable integration with any of low layer buses.
"""

__all__ = ["AbstractTPInterface"]

from typing import List
from abc import ABC, abstractmethod


class AbstractTPInterface(ABC):
    """Common interface for handling layers 3 and 4 of UDS protocol for any bus."""
    # TODO: I expect some common code here (e.g. message segmentation, and queuing N_PDUs)

    @abstractmethod
    def __init__(self, **kwargs) -> None:  # TODO: params, annotation and docstring
        """Configure Transport Protocol Interface."""

    @abstractmethod
    def send_response(self, response) -> None:  # TODO: params, annotation and docstring
        # TODO: consider addressing
        """
        Send diagnostic response.

        WARNING: Available for Server only!
        """

    @abstractmethod
    def send_request(self, request) -> None:  # TODO: params, annotation and docstring
        # TODO: consider addressing
        """
        Send diagnostic request.

        WARNING: Available for Client only!
        """

    @abstractmethod
    def get_last_sent_message(self):  # TODO: params, annotation and docstring
        """Get last sent diagnostic message with end of transmission timestamp."""

    @abstractmethod
    def get_responses_to_last_request(self) -> List:  # TODO: params, annotation and docstring
        # TODO: consider addressing
        """
        Get list of response messages to last sent diagnostic request.

        WARNING: Available for Client only!
        """

    @abstractmethod
    def start_tester_present(self) -> None:  # TODO: docstring
        # TODO: consider addressing
        """
        Turn on cyclical sending of Tester Present message.

        WARNING: Available for Client only!
        """

    @abstractmethod
    def stop_tester_present(self) -> None:  # TODO: docstring
        # TODO: consider addressing
        """
        Turn off cyclical sending of Tester Present message.

        WARNING: Available for Client only!
        """

    @abstractmethod
    def send_pdu(self, pdu) -> None:  # TODO: params, annotation and docstring
        # TODO: consider addressing
        """Send a single N_PDU."""

    @abstractmethod
    def get_last_sent_pdu(self):  # TODO: params, annotation and docstring
        # TODO: consider addressing
        """Get last sent N_PDU with end of transmission timestamp."""

    @abstractmethod
    def get_received_pdu(self) -> List:  # TODO: params, annotation and docstring
        # TODO: consider addressing
        """Get list of N_PDUs that were received since last execution of this method."""


"""
Module with abstract Transport Protocol Interface definition.

Transport Protocol Interface is meant to handle UDS protocol 4 (Transport Protocol) and other below it
(directly or indirectly).
There are many buses that supports UDS and each of them has special implementation for these layers, e.g.
- DoCAN (ISO 15765-2)
- DoLIN
- DoIP (ISO 13400-2 and 13400-3)
Due to this, there is need to create common (shared) interface as abstraction layer (in the code), so the implementation
enable integration with any of low layer buses.
"""

__all__ = ["AbstractTPInterface"]

from typing import List
from abc import ABC, abstractmethod

from .utilities import RepeatedCall
from .message import UdsRequest, UdsResponse, UdsMessage


class AbstractTPInterface(ABC):
    """Common interface for handling layer 4 of UDS protocol for any bus."""
    # TODO: I expect some common code here (e.g. message segmentation, and queuing N_PDUs)

    @abstractmethod
    def __init__(self, **kwargs) -> None:  # TODO: params, annotation and docstring
        """Configure Transport Protocol Interface."""

    @abstractmethod
    def send_pdu(self, pdu, addressing) -> None:  # TODO: annotation
        """
        Send a single Network Protocol Data Unit (N_PDU).

        WARNING: N_PDU format might differ for different buses (e.g. Ethernet uses much different N_PDUs than CAN).

        :param pdu: Network PDU to transmit.
        :param addressing: Type of addressing to use for the Network PDU transmission.
        """

    @abstractmethod
    def get_last_sent_pdu(self):  # TODO: annotation
        """
        Get the last N_PDU that was successfully transmitted by this interface.

        WARNING! Returned value might be different than the last N_PDU that was provided to 'send_pdu'  method.
            This will happen if the last provided N_PDU was not transmitted yet.

        :return :The last transmitted N_PDU or None if no N_PDU was ever transmitted by this interface.
        """

    @abstractmethod
    def get_received_pdu(self) -> List:  # TODO: params, annotation and docstring
        # TODO: consider addressing
        """Get list of N_PDUs that were received since last execution of this method."""

    @abstractmethod
    def send_request(self, request, addressing) -> None:  # TODO: annotation
        """
        Send diagnostic request.

        WARNING: Available for Client only!

        :param request: Request message to transmit.
        :param addressing: Type of addressing to use for the request message transmission.
        """

    @abstractmethod
    def send_response(self, response, addressing) -> None:  # TODO: annotation
        """
        Send diagnostic response.

        WARNING: Available for Server only!

        :param response: Response message to transmit.
        :param addressing: Type of addressing to use for the response message transmission.
        """

    def get_last_sent_message(self):  # TODO: annotation
        """
        Get the last message that was successfully transmitted by this interface.

        WARNING! Returned value might be different than the last message that was provided to 'send_request'
            or 'send_response' method. This will happen if the last provided message was not transmitted yet.

        :return: The last transmitted message (either request or response) or None if no message was ever
            transmitted by this interface.
        """

    @abstractmethod
    def get_response_messages(self) -> List:  # TODO: annotation
        """
        Get list of responses received to the last diagnostic request scheduled for transmission.

        This method might wait till all response messages are received or response timeout occurs.
        WARNING: Available for Client only!

        :return: List with diagnostic response messages received in the chronological order.
        """

    def start_tester_present(self,
                             addressing,  # TODO: annotation
                             suppress_response: bool = True) -> None:
        """
        Turn on cyclical sending of Tester Present message.

        :param addressing: Type of addressing to use for the tester present messages transmission.
        :param suppress_response: True if responses from recipients to be suppressed, False otherwise.
            Response messages suppression is realized via setting Suppress Positive Response Message Indication Bit
            in Tester Present request messages.
        """

    def stop_tester_present(self) -> None:
        """
        Turn off cyclical sending of Tester Present message.

        WARNING: Available for Client only!
        """

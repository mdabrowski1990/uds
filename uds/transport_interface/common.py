"""
Module with abstract Transport Interface definition.

Transport Interface is meant to handle UDS layer 4 (Transport) and all below it.
There are many buses that supports UDS and each of them has special implementation, therefore there are many
ISO standards that describes desired behavior such as:
- ISO 15765-2 (DoCAN)
- ISO 13400-2 and 13400-3 (DoIP)
This module contains common (shared) interface as abstraction layer.
"""

__all__ = ["AbstractTransportInterface"]

from typing import List, Union
from abc import ABC, abstractmethod

from ..messages import AbstractPDU, AddressingType, UdsResponse, UdsRequest


class AbstractTransportInterface(ABC):
    """Common (for both server and client) interface for handling layer 4 of UDS protocol for any bus."""

    p2_server_max: int = 50  # Maximal value [ms] of P2Server recommended by ISO 14229-2
    p2ext_server_max: int = 5000  # Maximal value [ms] of P2*Server recommended by ISO 14229-2

    @abstractmethod
    def send_pdu(self, pdu: AbstractPDU, addressing: AddressingType) -> None:
        """
        Send a single Network Protocol Data Unit (N_PDU).

        WARNING: N_PDU format might differ for different buses (e.g. Ethernet uses much different N_PDUs than CAN).

        :param pdu: Network PDU to transmit.
        :param addressing: Type of addressing to use for the Network PDU transmission.
        """

    @abstractmethod
    def get_last_sent_pdu(self) -> AbstractPDU:
        """
        Get the last N_PDU that was successfully transmitted by this interface.

        WARNING! Returned value might be different than the last N_PDU that was provided to 'send_pdu'  method.
            This will happen if the last provided N_PDU was not transmitted yet.

        :return :The last transmitted N_PDU or None if no N_PDU was ever transmitted by this interface.
        """

    @abstractmethod
    def get_received_pdu(self) -> List[AbstractPDU]:
        """Get list of N_PDUs that were received since last execution of this method."""

    @abstractmethod
    def _segment_message(self, message: Union[UdsResponse, UdsRequest]) -> List[AbstractPDU]:
        """
        Performs UDS message segmentation.

        :param message: Message to be segmented.

        :return: N_PDUs that carries the message.
        """

    # @abstractmethod
    # def send_request(self, request, addressing) -> None:  # TODO: annotation
    #     """
    #     Send diagnostic request.
    #
    #     WARNING: Available for Client only!
    #
    #     :param request: Request messages to transmit.
    #     :param addressing: Type of addressing to use for the request messages transmission.
    #     """
    #
    # @abstractmethod
    # def send_response(self, response, addressing) -> None:  # TODO: annotation
    #     """
    #     Send diagnostic response.
    #
    #     WARNING: Available for Server only!
    #
    #     :param response: Response messages to transmit.
    #     :param addressing: Type of addressing to use for the response messages transmission.
    #     """
    #
    # def get_last_sent_message(self):  # TODO: annotation
    #     """
    #     Get the last messages that was successfully transmitted by this interface.
    #
    #     WARNING! Returned value might be different than the last messages that was provided to 'send_request'
    #         or 'send_response' method. This will happen if the last provided messages was not transmitted yet.
    #
    #     :return: The last transmitted messages (either request or response) or None if no messages was ever
    #         transmitted by this interface.
    #     """
    #
    # @abstractmethod
    # def get_response_messages(self) -> List:  # TODO: annotation
    #     """
    #     Get list of responses received to the last diagnostic request scheduled for transmission.
    #
    #     This method might wait till all response messages are received or response timeout occurs.
    #     WARNING: Available for Client only!
    #
    #     :return: List with diagnostic response messages received in the chronological order.
    #     """
    #
    # def start_tester_present(self,
    #                          addressing,  # TODO: annotation
    #                          suppress_response: bool = True) -> None:
    #     """
    #     Turn on cyclical sending of Tester Present messages.
    #
    #     :param addressing: Type of addressing to use for the tester present messages transmission.
    #     :param suppress_response: True if responses from recipients to be suppressed, False otherwise.
    #         Response messages suppression is realized via setting Suppress Positive Response Message Indication Bit
    #         in Tester Present request messages.
    #     """
    #
    # def stop_tester_present(self) -> None:
    #     """
    #     Turn off cyclical sending of Tester Present messages.
    #
    #     WARNING: Available for Client only!
    #     """

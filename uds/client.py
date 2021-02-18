"""Client implementation for UDS protocol."""

__all__ = ["Client"]

from typing import List

from .transport_protocol import AbstractTPInterface


class Client:
    """
    Factory of UDS clients.

    UDS client sends diagnostic requests and receives diagnostic response. It always initiates communication
    in each sub-net. Examples of UDS clients:
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

    def send_request(self,
                     request,  # TODO: annotation
                     addressing) -> None:  # TODO: annotation, default value
        """
        Send physically (targets a single ECU) addressed request.

        :param request: Diagnostic request to send.
        :param addressing: Type of addressing to use for the request messages transmission.
        """
        self.__tp_interface.send_request(request=request, addressing=addressing)

    def get_last_sent_request(self):  # TODO: annotation
        """
        Get the last request messages that was successfully transmitted by this client.

        WARNING! Returned value might be different than the last request messages that was provided to 'send_request'
            method. This will happen if the last provided messages was not transmitted by the tp_interface yet.

        :return: The last transmitted request messages or None if no request was ever transmitted by this client.
        """
        return self.__tp_interface.get_last_sent_message()

    def get_response_messages(self) -> List:  # TODO: annotation
        """
        Get list of responses received to the last diagnostic request scheduled for transmission.

        This method might wait till all response messages are received or response timeout occurs.

        :return: List with diagnostic response messages received in the chronological order.
        """
        return self.__tp_interface.get_response_messages()

    def start_tester_present(self,
                             addressing,  # TODO: annotation, default
                             suppress_response: bool = True) -> None:
        """
        Turn on cyclical sending of Tester Present messages.

        :param addressing: Type of addressing to use for the tester present messages transmission.
        :param suppress_response: True if responses from recipients to be suppressed, False otherwise.
            Response messages suppression is realized via setting Suppress Positive Response Message Indication Bit
            in Tester Present request messages.
        """
        self.__tp_interface.start_tester_present(addressing=addressing, suppress_response=suppress_response)

    def stop_tester_present(self) -> None:
        """Turn off cyclical sending of Tester Present messages."""
        self.__tp_interface.stop_tester_present()

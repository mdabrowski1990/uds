"""UDS Client side implementation."""


__all__ = ["Client"]


from typing import List, Optional


class Client:
    """
    Factory of client (diagnostic tester).

    UDS Client sends diagnostic requests and received diagnostic response.
    It always initiates communication in each sub-net.

    :param messaging_database: Database that contains UDS services' messages formats and interpretation of its data.
    """

    def __init__(self,
                 tp_interface,
                 messaging_database: Optional[UdsMessagingDatabase] = None) -> None:
        """
        Configure a single UDS client.

        UDS client is able to send diagnostic requests and receive diagnostic responses over provided
        transport protocol interface.

        :param tp_interface: Transport Protocol interface for handling Layer 4 (and all below) of UDS communication.
        :param messaging_database: Database to be used for interpretation of UDS responses.
        """
        self.__tp_interface = tp_interface
        self.__messaging_database = None
        self.messaging_database = messaging_database

    def send_physical_request(self, request) -> None:
        """
        Send physically (targets a single ECU) addressed request over configured communication channel.

        :param request: Diagnostic request to send.
        """
        raw_request = request.raw_message if isinstance(request, UdsMessage) else request
        self.__tp_interface.send_physical_request(raw_request)

    def send_functional_request(self, request) -> None:
        """
        Send functionally (targets all ECUs) addressed request over configured communication channel.

        :param request: Diagnostic request to send.
        """
        raw_request = request.raw_message if isinstance(request, UdsMessage) else request
        self.__tp_interface.send_functional_request(raw_request)

    def get_responses_to_last_request(self) -> List:
        """
        Get list of responses to the last request that was sent by the Client.

        :return: List with diagnostic messages received in the response ordered chronologically.
        """
        raw_responses = self.__tp_interface.get_responses_to_last_request()
        if self.messaging_database is not None:
            return [self.messaging_database.get_message(_raw_response) for _raw_response in raw_responses]
        return raw_responses

    def start_tester_present(self) -> None:
        """Turn on cyclical sending of Tester Present message."""
        self.__tp_interface.start_tester_present()

    def stop_tester_present(self) -> None:
        """Turn off cyclical sending of Tester Present message."""
        self.__tp_interface.stop_tester_present()

    def __get_messaging_database(self):
        """Getter of 'messaging_database' attribute."""
        return self.__messaging_database

    def __set_messaging_database(self, messaging_database: Optional[UdsMessagingDatabase]) -> None:
        """Setter of 'messaging_database' attribute."""
        if messaging_database is not None and not isinstance(messaging_database, UdsMessagingDatabase):
            raise TypeError  # TODO: provide message
        self.__messaging_database = messaging_database

    messaging_database = property(fget=__get_messaging_database,
                                  fset=__set_messaging_database,
                                  doc="Messaging database of Client instance.")

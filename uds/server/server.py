"""UDS server implementation."""

__all__ = ["Server"]

from typing import Optional

from .types import TimeMilliseconds
from .consts import DEFAULT_P2EXT_SERVER_MAX, DEFAULT_P2_SERVER_MAX
from .response_manager import ResponseManager


class Server:
    """
    UDS Server simulator.

    UDS server receives diagnostic requests and sends diagnostic response.
    Each server object simulates a single on-board ECU.
    """
    __P2_SERVER_MIN: TimeMilliseconds = 0
    __P2EXT_SERVER_MIN: TimeMilliseconds = 0

    def __init__(self,
                 transport_interface,
                 response_manager: ResponseManager,
                 p4_server: Optional[TimeMilliseconds] = None,
                 p2_server: Optional[TimeMilliseconds] = None,
                 p2ext_server: Optional[TimeMilliseconds] = None,
                 p2_server_max: TimeMilliseconds = DEFAULT_P2_SERVER_MAX,
                 p2ext_server_max: TimeMilliseconds = DEFAULT_P2EXT_SERVER_MAX) -> None:
        """
        Configure simulation of UDS Server.

        :param transport_interface: Interface to be used for sending and receiving UDS messages.
        :param response_manager: Manager which automatically generates responses to received UDS requests.
        :param p4_server: TODO
            ISO 14229-2 explanation of P4Server:
            This is the time between the reception of a request (T_Data.indication) and the start of the transmission
            of the final response (T_Data.request) at the server side.
        :param p2_server: TODO
            ISO 14229-2 explanation of P2Server:
            Performance requirement for the server to start with the response message after the reception of a request
            message (indicated via T_Data.ind).
        :param p2ext_server: TODO
            ISO 14229-2 explanation of P2*Server:
            Performance requirement for the server to start with the response message after the transmission of
            a negative response message (indicated via T_Data.con) with negative response code 0x78 (enhanced
            response timing).
        :param p2_server_max: TODO
        :param p2ext_server_max: TODO
        """

    def turn_on(self) -> None:
        """Turn on server simulation and automatic responses to received requests messages."""

    def turn_off(self) -> None:
        """Turn off server simulation and automatic responses to received requests messages."""

    @property
    def response_manager(self) -> ResponseManager:
        """Response manager used by the server."""

    @response_manager.setter
    def response_manager(self, value: ResponseManager) -> None:
        """
        Set new value of response manager.

        :raise TypeError: Provided value is not ResponseManager type.
        """

    @property
    def p2_server(self) -> TimeMilliseconds:
        """Value of P2Server used by the server."""

    @p2_server.setter
    def p2_server(self, value: TimeMilliseconds) -> None:
        """
        Set new value of P2Server.

        :raise ValueError: Provided value is out of range P2Server_min-P2Server_max.
        :raise TypeError: Provided value has incompatible type.
        """

    @property
    def p2_server_max(self) -> TimeMilliseconds:
        """Maximal value of P2Server that can be used by the server."""

    @p2_server_max.setter
    def p2_server_max(self, value: TimeMilliseconds) -> None:
        """
        Set maximal value of P2Server that can be used by the server.

        :raise TypeError: Provided value has incompatible type.
        """

    @property
    def p2ext_server(self) -> TimeMilliseconds:
        """Value of P2*Server used by the server."""

    @p2ext_server.setter
    def p2ext_server(self, value: TimeMilliseconds) -> None:
        """
        Set new value of P2*Server.

        :raise ValueError: Provided value is out of range P2*Server_min-P2*Server_max.
        :raise TypeError: Provided value has incompatible type.
        """

    @property
    def p2ext_server_max(self) -> TimeMilliseconds:
        """Maximal value of P2*Server that can be used by the server."""

    @p2ext_server_max.setter
    def p2ext_server_max(self, value: TimeMilliseconds) -> None:
        """
        Set maximal value of P2*Server that can be used by the server.

        :raise TypeError: Provided value has incompatible type.
        """

    @property
    def p4_server(self) -> TimeMilliseconds:
        """Value of P4Server used by the server."""

    @p4_server.setter
    def p4_server(self, value: TimeMilliseconds) -> None:
        """
        Set new value of P4Server.

        :raise ValueError: Provided value is out of range.
        :raise TypeError: Provided value has incompatible type.
        """

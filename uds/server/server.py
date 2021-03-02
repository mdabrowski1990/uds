"""UDS server implementation."""

__all__ = ["Server"]

from typing import Optional, Union

from uds.constants import DEFAULT_P2EXT_SERVER_MAX, DEFAULT_P2_SERVER_MAX, TypingTimeMilliseconds
from .response_manager import ResponseManager


class Server:
    """
    UDS Server simulator.

    UDS server receives diagnostic requests and sends diagnostic response.
    Each server object simulates a single on-board ECU.
    """

    def __init__(self,
                 transport_interface,
                 response_manager: ResponseManager,
                 p4_server: Optional[TypingTimeMilliseconds] = None,
                 p2_server: Optional[TypingTimeMilliseconds] = None,
                 p2ext_server: Optional[TypingTimeMilliseconds] = None,
                 p2_server_max: TypingTimeMilliseconds = DEFAULT_P2_SERVER_MAX,
                 p2ext_server_max: TypingTimeMilliseconds = DEFAULT_P2EXT_SERVER_MAX) -> None:
        """

        :param transport_interface:
        :param response_manager:
        :param p4_server:
        :param p2_server:
        :param p2ext_server_max:
        """

    def turn_on(self) -> None:
        """

        :return:
        """

    def turn_off(self) -> None:
        """

        :return:
        """

    @property
    def response_manager(self) -> ResponseManager:
        """

        :return:
        """

    @response_manager.setter
    def response_manager(self, value_to_set: ResponseManager) -> None:
        """

        :param value_to_set:
        :return:
        """

    @property
    def p2_server(self) -> TypingTimeMilliseconds:
        """

        :return:
        """

    @p2_server.setter
    def p2_server(self, value_to_set: TypingTimeMilliseconds) -> None:
        """

        :param value_to_set:
        :return:
        """

    @property
    def p2_server_max(self) -> TypingTimeMilliseconds:
        """

        :return:
        """

    @p2_server_max.setter
    def p2_server_max(self, value_to_set: TypingTimeMilliseconds) -> None:
        """

        :param value_to_set:
        :return:
        """

    @property
    def p2ext_server(self) -> TypingTimeMilliseconds:
        """

        :return:
        """

    @p2ext_server.setter
    def p2ext_server(self, value_to_set: TypingTimeMilliseconds) -> None:
        """

        :param value_to_set:
        :return:
        """

    @property
    def p2ext_server_max(self) -> TypingTimeMilliseconds:
        """

        :return:
        """

    @p2ext_server_max.setter
    def p2ext_server_max(self, value_to_set: TypingTimeMilliseconds) -> None:
        """

        :param value_to_set:
        :return:
        """

    @property
    def p4_server(self) -> TypingTimeMilliseconds:
        """

        :return:
        """

    @p4_server.setter
    def p4_server(self, value_to_set: TypingTimeMilliseconds) -> None:
        """

        :param value_to_set:
        :return:
        """

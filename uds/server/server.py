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

    def __init__(self,
                 transport_interface,
                 response_manager: ResponseManager,
                 p4_server: Optional[TimeMilliseconds] = None,
                 p2_server: Optional[TimeMilliseconds] = None,
                 p2ext_server: Optional[TimeMilliseconds] = None,
                 p2_server_max: TimeMilliseconds = DEFAULT_P2_SERVER_MAX,
                 p2ext_server_max: TimeMilliseconds = DEFAULT_P2EXT_SERVER_MAX) -> None:
        """
        TODO

        :param transport_interface:
        :param response_manager:
        :param p4_server:
        :param p2_server:
        :param p2ext_server_max:
        """

    def turn_on(self) -> None:
        """
        TODO

        :return:
        """

    def turn_off(self) -> None:
        """
        TODO

        :return:
        """

    @property
    def response_manager(self) -> ResponseManager:
        """
        TODO

        :return:
        """

    @response_manager.setter
    def response_manager(self, value_to_set: ResponseManager) -> None:
        """
        TODO

        :param value_to_set:
        :return:
        """

    @property
    def p2_server(self) -> TimeMilliseconds:
        """
        TODO

        :return:
        """

    @p2_server.setter
    def p2_server(self, value_to_set: TimeMilliseconds) -> None:
        """
        TODO

        :param value_to_set:
        :return:
        """

    @property
    def p2_server_max(self) -> TimeMilliseconds:
        """
        TODO

        :return:
        """

    @p2_server_max.setter
    def p2_server_max(self, value_to_set: TimeMilliseconds) -> None:
        """
        TODO

        :param value_to_set:
        :return:
        """

    @property
    def p2ext_server(self) -> TimeMilliseconds:
        """
        TODO

        :return:
        """

    @p2ext_server.setter
    def p2ext_server(self, value_to_set: TimeMilliseconds) -> None:
        """
        TODO

        :param value_to_set:
        :return:
        """

    @property
    def p2ext_server_max(self) -> TimeMilliseconds:
        """
        TODO

        :return:
        """

    @p2ext_server_max.setter
    def p2ext_server_max(self, value_to_set: TimeMilliseconds) -> None:
        """
        TODO

        :param value_to_set:
        :return:
        """

    @property
    def p4_server(self) -> TimeMilliseconds:
        """
        TODO

        :return:
        """

    @p4_server.setter
    def p4_server(self, value_to_set: TimeMilliseconds) -> None:
        """
        TODO

        :param value_to_set:
        :return:
        """

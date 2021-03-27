"""UDS server implementation."""

__all__ = ["Server"]

from typing import Optional
from warnings import warn

from uds.transport_interface import TransportInterfaceServer

from .types import TimeMilliseconds
from .consts import DEFAULT_P2EXT_SERVER_MAX, DEFAULT_P2_SERVER_MAX, DEFAULT_P4_SERVER_MAX
from .response_manager import ResponseManager


class ServerSimulationWarning(Warning):
    """
    Warning informing about inconsistent simulation directives from the user.

    Examples the warning will be reported:
     - P2Server_max value of Server is set below current value P2Server
     - P2*Server_max value of Server is set below current value P2*Server
    """


class Server:  # TODO: mechanism for safe update of parameters (e.g. p4_server set, then p2_server changed)
    """
    UDS Server simulator.

    UDS server receives diagnostic requests and sends diagnostic response.
    Each server object simulates a single on-board ECU.
    """

    __P2_SERVER_MIN: TimeMilliseconds = 0
    __P2EXT_SERVER_MIN: TimeMilliseconds = 0
    __DEFAULT_P2_SERVER: TimeMilliseconds = __P2_SERVER_MIN
    __DEFAULT_P2EXT_SERVER: TimeMilliseconds = 0.9 * DEFAULT_P2EXT_SERVER_MAX

    def __init__(self,
                 transport_interface: TransportInterfaceServer,
                 response_manager: ResponseManager,
                 p4_server: Optional[TimeMilliseconds] = None,  # pylint: disable=unsubscriptable-object
                 p4_server_max: Optional[TimeMilliseconds] = DEFAULT_P4_SERVER_MAX,
                 p2_server: TimeMilliseconds = __DEFAULT_P2_SERVER,
                 p2ext_server: TimeMilliseconds = __DEFAULT_P2EXT_SERVER,
                 p2_server_max: TimeMilliseconds = DEFAULT_P2_SERVER_MAX,
                 p2ext_server_max: TimeMilliseconds = DEFAULT_P2EXT_SERVER_MAX) -> None:
        """
        Configure simulation of UDS Server.

        :param transport_interface: Interface to be used for sending and receiving UDS messages.
        :param response_manager: Manager which automatically generates responses to received UDS requests.
        :param p4_server: Value in milliseconds of p4server to use in server simulation.
            ISO 14229-2 explanation of P4Server:
            This is the time between the reception of a request (T_Data.indication) and the start of the transmission
            of the final response (T_Data.request) at the server side.
        :param p2_server: Value in milliseconds of P2Server to use in server simulation.
            ISO 14229-2 explanation of P2Server:
            Performance requirement for the server to start with the response message after the reception of a request
            message (indicated via T_Data.ind).
        :param p2ext_server: Value in milliseconds of P2*Server to use in server simulation.
            ISO 14229-2 explanation of P2*Server:
            Performance requirement for the server to start with the response message after the transmission of
            a negative response message (indicated via T_Data.con) with negative response code 0x78 (enhanced
            response timing).
        :param p2_server_max: Maximal value (in milliseconds) of P2Server that can be set.
        :param p2ext_server_max: Maximal value (in milliseconds) of P2*Server that can be set.
        """
        # pylint: disable=unsubscriptable-object
        self.__validate_transport_interface(transport_interface=transport_interface)
        self.__transport_interface = transport_interface
        self.response_manager = response_manager
        # set default timing values
        self.__p2_server: TimeMilliseconds = self.__P2_SERVER_MIN
        self.__p2_server_max: TimeMilliseconds = DEFAULT_P2EXT_SERVER_MAX
        self.__p2ext_server: TimeMilliseconds = self.__P2EXT_SERVER_MIN
        self.__p2ext_server_max: TimeMilliseconds = DEFAULT_P2EXT_SERVER_MAX
        self.__p4_server: Optional[TimeMilliseconds] = None
        self.__p4_server_max: Optional[TimeMilliseconds] = DEFAULT_P4_SERVER_MAX
        # set proper timing values with validation
        self.p2_server_max = p2_server_max
        self.p2ext_server_max = p2ext_server_max
        self.p4_server_max = p4_server_max  # type: ignore
        self.p2_server = p2_server
        self.p2ext_server = p2ext_server
        self.p4_server = p4_server  # type: ignore

    # transport_interface

    @staticmethod
    def __validate_transport_interface(transport_interface) -> None:
        """
        Verify transport interface argument.

        :param transport_interface: Server transport interface to validate.

        :raise TypeError: Transport interface is not TransportInterfaceServer type.
        """
        if not isinstance(transport_interface, TransportInterfaceServer):
            raise TypeError("'transport_interface' is not TransportInterfaceServer type")

    @property
    def transport_interface(self) -> TransportInterfaceServer:
        """Transport Interface used by the server."""
        return self.__transport_interface

    # response manager

    @property
    def response_manager(self) -> ResponseManager:
        """Response manager used by the server."""
        return self.__response_manager

    @response_manager.setter
    def response_manager(self, value: ResponseManager) -> None:
        """
        Set new value of response manager.

        :raise TypeError: Provided value is not ResponseManager type.
        """
        if not isinstance(value, ResponseManager):
            raise TypeError("'value' is not ResponseManager type")
        self.__response_manager = value

    # P2Server

    @property
    def p2_server_min(self) -> TimeMilliseconds:
        """Minimal value of P2Server that can be used by the server."""
        return self.__P2_SERVER_MIN

    @property
    def p2_server_max(self) -> TimeMilliseconds:
        """Maximal value of P2Server that can be used by the server."""
        return self.__p2_server_max

    @p2_server_max.setter
    def p2_server_max(self, value: TimeMilliseconds) -> None:
        """
        Set maximal value of P2Server that can be used by the server.

        :raise ValueError: Provided value is lower than P2Server_min.
        :raise TypeError: Provided value has incompatible type.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("'value' is not int or float type")
        if not self.p2_server_min < value:
            raise ValueError(f"'value' is not greater than P2Server_min. P2Server_min = {self.p2_server_min}.")
        self.__p2_server_max = value
        if self.p2_server > self.p2_server_max:
            self.p2_server = self.p2_server_max
            warn(message="P2Server value has been adjusted after P2Server_max changed its value.",
                 category=ServerSimulationWarning)

    @property
    def p2_server(self) -> TimeMilliseconds:
        """Value of P2Server used by the server."""
        return self.__p2_server

    @p2_server.setter
    def p2_server(self, value: TimeMilliseconds) -> None:
        """
        Set new value of P2Server.

        :raise ValueError: Provided value is not in range P2Server_min-P2Server_max.
        :raise TypeError: Provided value has incompatible type.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("'value' is not int or float type")
        if not self.p2_server_min <= value <= self.p2_server_max:
            raise ValueError(f"'value' is not: P2Server_min <= value <= P2Server_max. "
                             f"P2Server_min = {self.p2_server_min}. P2Server_max = {self.p2_server_max}")
        self.__p2_server = value
        if self.p4_server < self.p4_server_min:
            self.p4_server = None  # type: ignore
            warn(message="P4Server value has been adjusted after P2Server changed its value.",
                 category=ServerSimulationWarning)

    # P2*Server

    @property
    def p2ext_server_min(self) -> TimeMilliseconds:
        """Minimal value of P2*Server that can be used by the server."""
        return self.__P2EXT_SERVER_MIN

    @property
    def p2ext_server_max(self) -> TimeMilliseconds:
        """Maximal value of P2*Server that can be used by the server."""
        return self.__p2ext_server_max

    @p2ext_server_max.setter
    def p2ext_server_max(self, value: TimeMilliseconds) -> None:
        """
        Set maximal value of P2*Server that can be used by the server.

        :raise ValueError: Provided value is lower than P2*Server_min.
        :raise TypeError: Provided value has incompatible type.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("'value' is not int or float type")
        if not self.p2ext_server_min < value:
            raise ValueError(f"'value' is not greater than P2*Server_min. P2*Server_min = {self.p2ext_server_min}.")
        self.__p2ext_server_max = value
        if self.p2ext_server > self.p2ext_server_max:
            self.p2ext_server = self.p2ext_server_max
            warn(message="P2*Server value has been adjusted after P2*Server_max changed its value.",
                 category=ServerSimulationWarning)

    @property
    def p2ext_server(self) -> TimeMilliseconds:
        """Value of P2*Server used by the server."""
        return self.__p2ext_server

    @p2ext_server.setter
    def p2ext_server(self, value: TimeMilliseconds) -> None:
        """
        Set new value of P2*Server.

        :raise ValueError: Provided value is not in range P2*Server_min-P2*Server_max.
        :raise TypeError: Provided value has incompatible type.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("'value' is not int or float type")
        if not self.p2ext_server_min <= value <= self.p2ext_server_max:
            raise ValueError(f"'value' is not: P2*Server_min <= value <= P2*Server_max. "
                             f"P2*Server_min = {self.p2ext_server_min}. P2*Server_max = {self.p2ext_server_max}")
        self.__p2ext_server = value

    # P4Server

    @property
    def p4_server_min(self) -> TimeMilliseconds:
        """Minimal value of P4Server that can be used by the server."""
        return self.p2_server

    @property
    def p4_server_max(self) -> TimeMilliseconds:
        """Minimal value of P4Server that can be used by the server."""
        return self.__p4_server_max if self.__p4_server_max is not None else self.p2_server_max

    @p4_server_max.setter
    def p4_server_max(self, value: Optional[TimeMilliseconds]) -> None:  # pylint: disable=unsubscriptable-object
        """
        Set maximal value of P4Server that can be used by the server.

        If None provided, then the P2Server_max is equal to P2Server_max.

        :raise ValueError: Provided value is lower than P2Server_max.
        :raise TypeError: Provided value has incompatible type.
        """
        if value is not None:
            if not isinstance(value, (int, float)):
                raise TypeError("'value' is not int or float type")
            if not self.p2_server_max <= value:
                raise ValueError(f"'value' is less than P2Server_max. P2Server_max = {self.p2_server_max}.")
        self.__p4_server_max = value
        if self.p4_server > self.p4_server_max:
            self.p4_server = self.p4_server_max
            warn(message="P4Server value has been adjusted after P4Server_max changed its value.",
                 category=ServerSimulationWarning)

    @property
    def p4_server(self) -> TimeMilliseconds:
        """Value of P4Server used by the server."""
        return self.p2_server if self.__p4_server is None else self.__p4_server

    @p4_server.setter
    def p4_server(self, value: Optional[TimeMilliseconds]) -> None:  # pylint: disable=unsubscriptable-object
        """
        Set new value of P4Server.

        If None provided, then the P4Server is equal to P2Server.

        :raise ValueError: Provided value is lower than P4Server_min.
        :raise TypeError: Provided value has incompatible type.
        """
        if value is not None:
            if not isinstance(value, (int, float)):
                raise TypeError("'value' is not None, int or float type")
            if not self.p4_server_min <= value <= self.p4_server_max:
                raise ValueError(f"'value' is not: P4Server_min <= value <= P4Server_max. "
                                 f"P4Server_min = {self.p4_server_min}. P4Server_max = {self.p4_server_max}")
        self.__p4_server = value

    # simulation

    # def _schedule_response(self, request) -> None:
    #     """
    #     Set up transmission of a response message.
    #
    #     :param request: Request for which the response will be transmitted.
    #     """
    #     if self.p4_server == self.p2_server:
    #         self  # TODO: transmit final response message
    #     else:
    #         self  # TODO: transmit response pending(s) before final message
    #
    # def x(self, request):
    #     response = self.response_manager.create_response(request=request)
    #     self.__transport_interface.send_response(response=response)

    def turn_on(self) -> None:
        """Turn on server simulation and automatic responses to received requests messages."""
        self.__transport_interface.flush_received_pdus()

    def turn_off(self) -> None:
        """Turn off server simulation and automatic responses to received requests messages."""

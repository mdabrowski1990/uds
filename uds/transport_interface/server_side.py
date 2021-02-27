"""Abstract Transport Interface for Server side."""

__all__ = ["AbstractTIServer"]

from typing import Any, Union, Optional
from abc import abstractmethod

from uds.messages import UdsResponse, UdsRequest, AddressingType
from .common import AbstractTransportInterface

TimeMilliseconds = Union[int, float]


class AbstractTIServer(AbstractTransportInterface):
    """Abstract Transport Interface for Server side."""

    @abstractmethod
    def __init__(self, p2_server: TimeMilliseconds, p2ext_server: TimeMilliseconds, **specific_params: Any) -> None:
        """
        Configure common part of Transport layer for Server.

        :param p2_server: Value in milliseconds of P2Server to be used by the server.
            ISO 14229-2 explanation of P2Server:
            Performance requirement for the server to start with the response message after the reception of a request
            message (indicated via T_Data.ind).
        :param p2ext_server: Value in milliseconds of P2*Server to be used by the server.
            ISO 14229-2 explanation of P2*Server:
            Performance requirement for the server to start with the response message after the transmission of
            a negative response message (indicated via T_Data.con) with negative response code 0x78 (enhanced
            response timing).
        """
        self.p2_server = p2_server
        self.p2ext_server = p2ext_server

    @property
    def p2_server_min(self) -> TimeMilliseconds:
        """
        Minimal value (in milliseconds) of P2Server to be used by the server.

        ISO 14229-2 explanation of P2Server:
        Performance requirement for the server to start with the response message after the reception of a request
        message (indicated via T_Data.ind).
        """
        return 0

    @property
    def p2ext_server_min(self) -> TimeMilliseconds:
        """
        Minimal value (in milliseconds) of P2*Server to be used by the server.

        ISO 14229-2 explanation of P2*Server:
        Performance requirement for the server to start with the response message after the transmission of
        a negative response message (indicated via T_Data.con) with negative response code 0x78 (enhanced
        response timing).
        """
        return 0

    @property
    def p4_server_min(self) -> TimeMilliseconds:
        """
        Minimal value (in milliseconds) of P4Server to be used by the server.

        ISO 14229-2 explanation of P4Server:
        This is the time between the reception of a request (T_Data.indication) and the start of the transmission of
        the final response (T_Data.request) at the server side.
        """
        return self.p2_server

    @abstractmethod
    def receive_request(self) -> UdsRequest:
        """
        Monitor the bus until PDUs that can be connected into a UDS request are received.

        :return: The UDS request that was just received from the bus.
        """

    @abstractmethod
    def send_response(self, response: UdsResponse, addressing: AddressingType) -> UdsResponse:
        """
        Send UDS response to the bus.

        :param response: UDS response to send.
        :param addressing: Addressing over which response to be sent.

        TODO: raise exception in case of interrupt

        :return UDS Response that was sent.
        """

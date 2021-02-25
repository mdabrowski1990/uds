"""Abstract Transport Interface for Client side."""

__all__ = ["AbstractTIClient"]

from typing import Any
from abc import abstractmethod

from .common import AbstractTransportInterface


class AbstractTIClient(AbstractTransportInterface):
    """Abstract Transport Interface for Client side."""

    def __init__(self,
                 p2_client: int,
                 p2ext_client: int,
                 delta_p2_request: int = 0,
                 delta_p2_response: int = 0,
                 delta_p6_request: int = 0,
                 delta_p6_response: int = 0,
                 **specific_params: Any) -> None:
        """
        Configure Transport layer for Client.

        :param p2_client: Value in milliseconds of P2Client to be used by the Transport Interface.
            ISO 14229-2 explanation:
            Timeout for the client to wait after successful transmission of a request message for the start of
            incoming response messages.
        :param p2ext_client: Value in milliseconds of P2*Client to be used by the Transport Interface.
            ISO 14229-2 explanation:
            Enhanced timeout for the client to wait after the reception of a negative response message with negative
            response code 0x78 for the start of incoming response messages.
        :param delta_p2_request: Value in milliseconds of ΔP2request to be used by the Transport Interface.
        :param delta_p2_response: Value in milliseconds of ΔP2response to be used by the Transport Interface.
        :param delta_p6_request: Value in milliseconds of ΔP6request to be used by the Transport Interface.
        :param delta_p6_response: Value in milliseconds of ΔP6response to be used by the Transport Interface.
        :param specific_params: Any other params that are specific for given Transport Interface.
        """
        self.p2_client = p2_client
        self.p2ext_client = p2ext_client
        self.delta_p2_request = delta_p2_request
        self.delta_p2_response = delta_p2_response
        self.delta_p6_request = delta_p6_request
        self.delta_p6_response = delta_p6_response

    @property
    def delta_p2_max(self) -> int:
        """
        Maximal value (in milliseconds) of ΔP2.

        ISO 14229-2 explanation:
        The worst case vehicle network design-dependent message transmission delay such as delays introduced by gateways
        and bus-load depended arbitration. The value of ΔP2 is divided into the time to transmit the request to
        the addressed server/ECU (ΔP2request) and in case the protocol supports T_DataSOM.ind till the start of
        the response transmission indicated by T_DataSOM.ind or T_Data.ind if the response is a single frame
        message (e.g. ISO 15765 DoCAN).
        """
        return self.delta_p2_response + self.delta_p2_request

    @property
    def delta_p6_max(self) -> int:
        """
        Maximal value (in milliseconds) of ΔP6.

        TODO: ISO 14229-2 explanation
        """
        return self.delta_p6_response + self.delta_p6_request

    @property
    def p2_client_min(self) -> int:
        """
        Minimal value (in milliseconds) of P2Client.

        TODO: ISO 14229-2 explanation
        """
        return self.p2_server_max + self.delta_p2_max

    @property
    def p2ext_client_min(self) -> int:
        """
        Minimal value (in milliseconds) of P2*Client.

        TODO: ISO 14229-2 explanation
        """
        return self.p2ext_server_max + self.delta_p2_response

    @property
    def p6_client_min(self) -> int:
        """
        Minimal value (in milliseconds) of P6Client.

        TODO: ISO 14229-2 explanation
        """
        return self.p2_server_max + self.delta_p6_max

    @property
    def p6ext_client_min(self) -> int:
        """
        Minimal value (in milliseconds) of P6*Client.

        TODO: ISO 14229-2 explanation
        """
        return self.p2ext_server_max + self.delta_p6_response

    @property
    def p3_client_min(self) -> int:
        """
        Minimal value (in milliseconds) of P3Client.

        TODO: ISO 14229-2 explanation
        """
        return self.p2_server_max + self.delta_p2_max

    # TODO: abstract methods

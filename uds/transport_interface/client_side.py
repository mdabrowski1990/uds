"""Abstract Transport Interface for Client side."""

__all__ = ["AbstractTIClient"]

from typing import Any, Union, List
from abc import abstractmethod

from uds.messages import UdsRequest, UdsResponse, AddressingType
from .common import AbstractTransportInterface

TimeMilliseconds = Union[int, float]


class AbstractTIClient(AbstractTransportInterface):
    """Abstract Transport Interface for Client side."""

    @abstractmethod
    def __init__(self,
                 p2_client: TimeMilliseconds,
                 p2ext_client: TimeMilliseconds,
                 delta_p2_request: TimeMilliseconds = 0,
                 delta_p2_response: TimeMilliseconds = 0,
                 delta_p6_request: TimeMilliseconds = 0,
                 delta_p6_response: TimeMilliseconds = 0,
                 **specific_params: Any) -> None:  # noqa: F841
        """
        Configure common part of Transport layer for Client.

        :param p2_client: Value in milliseconds of P2Client to be used by the client.
            ISO 14229-2 explanation of P2Client:
            Timeout for the client to wait after successful transmission of a request message (indicated via T_Data.con)
            for the start of incoming response messages (indicated via T_DataSOM.ind of a multi-frame message or
            T_Data.ind of a SingleFrame message).
        :param p2ext_client: Value in milliseconds of P2*Client to be used by the client.
            ISO 14229-2 explanation of P2*Client:
            Enhanced timeout for the client to wait after the reception of a negative response message with negative
            response code 0x78 (indicated via T_Data.ind) for the start of incoming response messages (indicated via
            T_DataSOM.ind of a multi-frame message or T_Data.ind of a SingleFrame message).
        :param delta_p2_request: Value in milliseconds of ΔP2request to be used by the client.
        :param delta_p2_response: Value in milliseconds of ΔP2response to be used by the client.
        :param delta_p6_request: Value in milliseconds of ΔP6request to be used by the client.
        :param delta_p6_response: Value in milliseconds of ΔP6response to be used by the client.
        :param specific_params: Any other params that are specific for given client's Transport Interface.
        """
        self.p2_client = p2_client
        self.p2ext_client = p2ext_client
        self.delta_p2_request = delta_p2_request
        self.delta_p2_response = delta_p2_response
        self.delta_p6_request = delta_p6_request
        self.delta_p6_response = delta_p6_response

    @property
    def delta_p2_max(self) -> TimeMilliseconds:
        """
        Maximal value (in milliseconds) of ΔP2 to be used by the client.

        ISO 14229-2 explanation of ΔP2:
        The worst case vehicle network design-dependent message transmission delay such as delays introduced by gateways
        and bus-load depended arbitration. The value of ΔP2 is divided into the time to transmit the request to
        the addressed server/ECU (ΔP2request) and in case the protocol supports T_DataSOM.ind till the start of
        the response transmission indicated by T_DataSOM.ind or T_Data.ind if the response is a single frame
        message (e.g. ISO 15765 DoCAN).
        """
        return self.delta_p2_response + self.delta_p2_request

    @property
    def delta_p6_max(self) -> TimeMilliseconds:
        """
        Maximal value (in milliseconds) of ΔP6 to be used by the client.

        ISO 14229-2 explanation of ΔP6:
        The worst case vehicle network design-dependent message transmission delay such as delays introduced by gateways
        and bus-load depended arbitration. The value of ΔP6 is divided into the time to transmit the request to
        the addressed server/ECU (ΔP6request) and the time to transmit the complete response to
        the client/tester (ΔP6response). The ΔP6 is independent of whether a protocol supports
        a T_DataSOM.ind (e.g. ISO 15765 DoCAN) or does not support a T_DataSOM.Ind (e.g. ISO 13400 DoIP).
        """
        return self.delta_p6_response + self.delta_p6_request

    @property  # noqa: F841
    def p2_client_min(self) -> TimeMilliseconds:
        """
        Minimal value (in milliseconds) of P2Client to be used by the client.

        ISO 14229-2 explanation of P2Client:
        Timeout for the client to wait after successful transmission of a request message (indicated via T_Data.con)
        for the start of incoming response messages (indicated via T_DataSOM.ind of a multi-frame message or
        T_Data.ind of a SingleFrame message).
        """
        return self.p2_server_max + self.delta_p2_max

    @property  # noqa: F841
    def p2ext_client_min(self) -> TimeMilliseconds:
        """
        Minimal value (in milliseconds) of P2*Client to be used by the client.

        ISO 14229-2 explanation of P2*Client:
        Enhanced timeout for the client to wait after the reception of a negative response message with negative
        response code 0x78 (indicated via T_Data.ind) for the start of incoming response messages (indicated via
        T_DataSOM.ind of a multi-frame message or T_Data.ind of a SingleFrame message).
        """
        return self.p2ext_server_max + self.delta_p2_response

    @property  # noqa: F841
    def p6_client_min(self) -> TimeMilliseconds:
        """
        Minimal value (in milliseconds) of P6Client to be used by the client.

        ISO 14229-2 explanation of P6Client:
        Timeout for the client to wait after the successful transmission of a request message (indicated via T_Data.con)
        for the complete reception of the corresponding response message (indicated via T_Data.ind) e.g. ISO 13400 DoIP.
        """
        return self.p2_server_max + self.delta_p6_max

    @property  # noqa: F841
    def p6ext_client_min(self) -> TimeMilliseconds:
        """
        Minimal value (in milliseconds) of P6*Client to be used by the client.

        ISO 14229-2 explanation of P6*Client:
        Enhanced timeout for the client to wait after the reception of a negative response message with negative
        response code 0x78 (indicated via T_Data.ind) for the complete reception of the corresponding response
        messages (indicated via T_Data.ind) e.g. ISO 13400 DoIP.
        """
        return self.p2ext_server_max + self.delta_p6_response

    @property  # noqa: F841
    def p3_client_min(self) -> TimeMilliseconds:
        """
        Minimal value (in milliseconds) of P3Client_Phys and P3Client_Func to be used by the client.

        ISO 14229-2 explanation of P3Client_Phys:
        Minimum time for the client to wait after the successful transmission of a physically addressed request
        message (indicated via T_Data.con) with no response required before it can transmit the next physically
        addressed request message.

        ISO 14229-2 explanation of P3Client_Func:
        Minimum time for the client to wait after the successful transmission of a functionally addressed request
        message (indicated via T_Data.con) before it can transmit the next functionally addressed request message
        in case no response is required or the requested data is only supported by a subset of the functionally
        addressed servers.
        """
        return self.p2_server_max + self.delta_p2_max

    @abstractmethod
    def send_request(self, request: UdsRequest, addressing: AddressingType) -> None:  # noqa: F841
        """
        Send UDS request to the bus.

        :param request: UDS request to send.
        :param addressing: Addressing over which request to be sent.
        """

    @abstractmethod
    def get_response_messages(self) -> List[UdsResponse]:
        """
        Get all response messaged received to the last sent request message by this interface.

        WARNING!
        This function might last varying amount of time as it wait till all possible responses are received or
        timeout occurs.

        :return: List of UDS messages that were received as responses to the last request sent by this interface.
        """

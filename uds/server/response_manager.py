"""
Implementation of manager which is meant auto-generate responses to any received request.

ResponseManager is meant to:
 - store current diagnostic states of server ECU (contains state machine)
 - contain ordered rules which determines how to create a response message to any received request
"""

__all__ = ["ResponseManager"]

from typing import Optional, List, Container

from uds.messages import ResponseSID, AddressingType, UdsRequest, UdsResponse, NRC, POSSIBLE_REQUEST_SIDS
from .types import CurrentStatesValues
from .server_state import ServerState
from .response_rule import ResponseRule


Rules = List[ResponseRule]
States = Container[ServerState]


class _EmergencyServiceNotSupported(ResponseRule):
    """Emergency Rule to respond negatively with NRC Service Not Supported."""

    def is_triggered(self, request: UdsRequest, current_states: CurrentStatesValues) -> bool:
        """
        Check if the rule might be used to generate a response message for the received request.

        :param request: Request message that was received.
        :param current_states: Current values of all server's states.

        :return: True if the rule is applicable in provided situation, False otherwise.
        """
        return True

    def create_response(self, request: UdsRequest, current_states: CurrentStatesValues) -> Optional[UdsResponse]:
        """
        Create response message according to the rule.

        :param request: Request message for which response to be generated.
        :param current_states: Current values of all server's states.

        :return: Response message that was generated. None if no message to be sent in the response.
        """
        raw_negative_message = [ResponseSID.NegativeResponse.value,
                                request.raw_message[0],
                                NRC.ServiceNotSupported.value]
        return UdsResponse(raw_message=raw_negative_message)


class _EmergencyNoResponse(ResponseRule):
    """Emergency Rule to stay silent and not respond."""

    def is_triggered(self, request: UdsRequest, current_states: CurrentStatesValues) -> bool:
        """
        Check if the rule might be used to generate a response message for the received request.

        :param request: Request message that was received.
        :param current_states: Current values of all server's states.

        :return: True if the rule is applicable in provided situation, False otherwise.
        """
        return True

    def create_response(self, request: UdsRequest, current_states: CurrentStatesValues) -> Optional[UdsResponse]:
        """
        Create response message according to the rule.

        :param request: Request message for which response to be generated.
        :param current_states: Current values of all server's states.

        :return: Response message that was generated. None if no message to be sent in the response.
        """
        return None


class ResponseManager:
    """
    Unit that automatically creates responses for incoming requests according to the set of rules.

    ResponseManager is meant to fully simulate responses of any server (ECU). It stores current state of the server and
    contains rules (ordered according to priority) which describes how to create response message in given situation.
    """

    __EMERGENCY_RESPONSE_RULES = (
        _EmergencyServiceNotSupported(addressing_types={AddressingType.PHYSICAL},
                                      related_request_sids=POSSIBLE_REQUEST_SIDS),
        _EmergencyNoResponse(addressing_types={AddressingType.BROADCAST, AddressingType.FUNCTIONAL},
                             related_request_sids=POSSIBLE_REQUEST_SIDS),
    )

    def __init__(self, response_rules: Rules, server_states: States) -> None:
        """
        Create response manager, define rules it uses and states that it contains.

        :param response_rules: Rules (in priority order) that the manager is meant to use to generate response messages
            to any incoming request.
        :param server_states: States (e.g. DiagnosticSession SecurityAccess) of the server might change during
            the diagnostic communication.
        """

    @property
    def current_states_values(self) -> CurrentStatesValues:
        """Values for all the states that the simulated server currently is in."""

    @property
    def response_rules(self) -> Rules:
        """Rules (in priority order) that the manager is currently using."""

    def create_response(self, request: UdsRequest) -> Optional[UdsResponse]:
        """
        Create response message according to the rule.

        :param request: Request message for which response to be generated.

        :return: Response message that was generated. None if no message to be sent in the response.
        """

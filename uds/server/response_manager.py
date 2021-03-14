"""
Implementation of manager which is meant auto-generate responses to any received request.

ResponseManager is meant to:
 - store current diagnostic states of server ECU (contains state machine)
 - contain ordered rules which determines how to create a response message to any received request
"""

__all__ = ["ResponseManager"]

from warnings import warn
from typing import Union, Optional, List, Tuple, Set, Dict

from uds.messages import ResponseSID, AddressingType, UdsRequest, UdsResponse, NRC, POSSIBLE_REQUEST_SIDS
from .types import CurrentStatesValues
from .server_state import ServerState
from .response_rule import ResponseRule

# pylint: disable=unsubscriptable-object
ResponseRulesTuple = Tuple[ResponseRule, ...]
ResponseRulesList = List[ResponseRule]
ResponseRulesDict = Dict[AddressingType, Dict[int, ResponseRulesList]]
ResponseRulesSequence = Union[ResponseRulesList, ResponseRulesTuple]
ServerStatesSet = Set[ServerState]
ServerStatesSequence = Union[List[ServerState], Tuple[ServerState, ...], ServerStatesSet]


class EmergencyRuleUsed(Warning):
    """Warning triggered by accessing any of Emergency Rules."""


class EmergencyRuleError(Exception):
    """Error related to Emergency Rules."""


class _EmergencyServiceNotSupported(ResponseRule):
    """Emergency Rule to respond negatively with NRC Service Not Supported."""

    def is_triggered(self, request: UdsRequest, current_states: CurrentStatesValues) -> bool:  # noqa: F841
        """
        Check if the rule might be used to generate a response message for the received request.

        :param request: Request message that was received.
        :param current_states: Current values of all server's states.

        :return: True if the rule is applicable in provided situation, False otherwise.
        """
        return True

    def create_response(self, request: UdsRequest, current_states: CurrentStatesValues) -> Optional[UdsResponse]:  # noqa: F841
        """
        Create response message according to the rule.

        :param request: Request message for which response to be generated.
        :param current_states: Current values of all server's states.

        :return: Response message that was generated. None if no message to be sent in the response.
        """
        raw_negative_message = [ResponseSID.NegativeResponse.value,  # type: ignore
                                request.raw_message[0],
                                NRC.ServiceNotSupported.value]  # type: ignore
        return UdsResponse(raw_message=raw_negative_message)


class _EmergencyNoResponse(ResponseRule):
    """Emergency Rule to stay silent and do not respond."""

    def is_triggered(self, request: UdsRequest, current_states: CurrentStatesValues) -> bool:  # noqa: F841
        """
        Check if the rule might be used to generate a response message for the received request.

        :param request: Request message that was received.
        :param current_states: Current values of all server's states.

        :return: True if the rule is applicable in provided situation, False otherwise.
        """
        return True

    def create_response(self, request: UdsRequest, current_states: CurrentStatesValues) -> Optional[UdsResponse]:  # noqa: F841
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

    def __init__(self, response_rules: ResponseRulesSequence, server_states: ServerStatesSequence) -> None:
        """
        Create response manager, define rules it uses and states that it contains.

        :param response_rules: Rules (in priority order) that the manager is meant to use to generate response messages
            to any incoming request.
        :param server_states: States (e.g. DiagnosticSession SecurityAccess) of the server might change during
            the diagnostic communication.
        """
        self.__validate_server_states(server_states=server_states)
        self.__server_states = set(server_states)
        self.__response_rules_tuple: ResponseRulesTuple = ()  # default value
        self.__response_rules_dict: ResponseRulesDict = {}  # default value
        self.response_rules = tuple(response_rules)

    @staticmethod
    def __validate_response_rules(response_rules: ResponseRulesSequence) -> None:
        """
        Verify response rules argument.

        :param response_rules: Response rules to generate response messages to any incoming request.

        :raise TypeError: Response rules argument is not list or tuple type.
        :raise ValueError: At least one of response rules elements is not response rule.
        """
        if not isinstance(response_rules, (tuple, list)):
            raise TypeError("'response_rules' is not list or tuple type")
        if not all([isinstance(response_rules, ResponseRule) for response_rules in response_rules]):
            raise ValueError("'response_rules' does not contain ResponseRule instances only")

    @staticmethod
    def __validate_server_states(server_states: ServerStatesSequence) -> None:
        """
        Verify server states argument.

        :param server_states: Server state to be stored in the server.

        :raise TypeError: Server states argument is not list, tuple or set type.
        :raise ValueError: At least one of server states elements is not server state.
        """
        if not isinstance(server_states, (tuple, list, set)):
            raise TypeError("'server_states' is not list, tuple or set type")
        if not all([isinstance(server_state, ServerState) for server_state in server_states]):
            raise ValueError("'server_states' does not contain ServerState instances only")

    @staticmethod
    def _create_response_rules_dict(response_rules: ResponseRulesSequence) -> ResponseRulesDict:
        """
        Create dictionary with quick access for rules related to given addressing and SID.

        :param response_rules: Response rules from which quick access dictionary to be created.

        :return: Dictionary with quick rules access.
        """
        rules_dict: ResponseRulesDict = {}
        for rule in response_rules:
            for addressing in rule.addressing_types:
                addressing_rules_dict = rules_dict.setdefault(addressing, {})
                for sid in rule.related_request_sids:
                    addressing_rules_dict.setdefault(sid, []).append(rule)
        return rules_dict

    @property
    def current_states_values(self) -> CurrentStatesValues:
        """Values for all the states that the simulated server currently is in."""
        transitions = []
        # perform all transitions due to idle state
        for state in self.__server_states:
            idle_transition = state.update_on_idle()
            if idle_transition is not None:
                transitions.append((state.state_name, idle_transition))
        # perform all transitions cause by idle state transitions
        while transitions:
            state_name, transition = transitions.pop(0)
            for state in self.__server_states:
                if state_name in state.depends_on:
                    state_transition = state.update_on_other_state_transition(state_name=state_name,
                                                                              previous_value=transition[0],
                                                                              new_value=transition[1])
                    if state_transition is not None:
                        transitions.append((state.state_name, state_transition))
        # return actual values
        return {state.state_name: state.current_value for state in self.__server_states}

    @property
    def response_rules(self) -> ResponseRulesTuple:
        """Rules (in priority order) that the manager is currently using."""
        return self.__response_rules_tuple

    @response_rules.setter
    def response_rules(self, value: ResponseRulesSequence) -> None:
        """Set rules (in priority order) that the manager will use."""
        self.__validate_response_rules(response_rules=value)
        self.__response_rules_tuple = tuple(value)
        self.__response_rules_dict = self._create_response_rules_dict(response_rules=value)

    def create_response(self, request: UdsRequest) -> Optional[UdsResponse]:
        """
        Create response message according to the rule.

        :param request: Request message for which response to be generated.

        :raise EmergencyRuleError:

        :return: Response message that was generated. None if no message to be sent in the response.
        """
        if request.addressing is None:
            raise ValueError("Provided request messages has no assigned addressing value.")
        current_state = self.current_states_values
        user_rules = self.__response_rules_dict.get(request.addressing, {}).get(request.raw_message[0], [])
        for rule in user_rules:
            if rule.is_triggered(request=request, current_states=current_state):
                return rule.create_response(request=request, current_states=current_state)
        warn(message="No matching user rule was found. Emergency rules to be checked.", category=EmergencyRuleUsed)
        for emergency_rule in self.__EMERGENCY_RESPONSE_RULES:
            if emergency_rule.is_triggered(request=request, current_states=current_state):
                return emergency_rule.create_response(request=request, current_states=current_state)
        raise EmergencyRuleError(f"No matching emergency rule was found. Request addressing: {request.addressing}. "
                                 f"Request raw_message: {request.raw_message}")

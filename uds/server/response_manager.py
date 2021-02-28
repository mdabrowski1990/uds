"""
Implementation of manager which is meant auto-generate responses to any received request.

ResponseManager is meant to:
 - store current diagnostic states of server ECU (contains state machine)
 - contain ordered rules which determines how to create a response message to any received request
"""

__all__ = ["ServerState", "ResponseRule", "ResponseManager"]

from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple, Set, Container, Iterable, Dict, List

from uds.messages import UdsRequest, UdsResponse, AddressingType

TypingStateName = str
TypingStateNames = Set[TypingStateName]
TypingStateValue = Any
TypingStateValues = Container[TypingStateValue]
TypingStateTransition = Tuple[TypingStateValue, TypingStateValue]
TypingRequestSIDs = Iterable[int]
TypingAddressingTypes = Container[AddressingType]
TypingCurrentStatesValues = Dict[TypingStateName, TypingStateValue]


class ServerState(ABC):
    """
    A single diagnostic state (e.g. session, security access).

    AbstractClass contains common implementation of handler for any diagnostic state of simulated server.
    SubClass is meant to be contain set of rules (e.g. when to perform transition, what are possible values) that
    describes generic mechanism of the state.
    Instance of a SubClass is meant to additionally store current value of the state for a single simulated server.
    """

    def __init__(self, state_name: TypingStateName, initial_value: TypingStateValue) -> None:
        """
        Define the state.

        :param state_name: Name of the state.
        :param initial_value: Initial value that this state is supposed to be in.
        """
        if not isinstance(state_name, TypingStateName):
            raise TypeError(f"'state_name' is not {TypingStateName} type")
        if initial_value not in self.possible_values:
            raise ValueError(f"'initial_value' is not a member of 'possible_values'; "
                             f"initial_value={repr(initial_value)}; possible_values={repr(self.possible_values)}")
        self.state_name = state_name
        self.__current_value = initial_value

    @property
    def current_value(self) -> TypingStateValue:
        """
        Value that the server is currently in.

        WARNING!
        Execute 'update_on_idle' before reading the value to make sure that the state has not changed during
        the idle state.
        """
        return self.__current_value

    @property
    @abstractmethod
    def possible_values(self) -> TypingStateValues:
        """All possible values of this state."""

    @property
    @abstractmethod
    def depends_on(self) -> TypingStateNames:
        """
        Names of all states which change might cause transition of this state as well.

        Example:
            Assume this class contains definition of SecurityAccess state.
            According to ISO 14229 SecurityAccess might must always be in 'locked' state if ECU is in 'default session'.
            This means that this state depends on DiagnosticSession as transition to 'default session' must cause
            transition to 'locked' state of SecurityAccess.
        """

    @abstractmethod
    def update_on_request(self, request: UdsRequest) -> Optional[TypingStateTransition]:
        """
        Access whether adjustment of current value is needed after reception of the diagnostic request.

        Method to be executed after each successful reception of any diagnostic request by the server.

        :param request: Diagnostic request that was received.

        :return: None if state remain unchanged or StateTransition that was performed.
        """

    @abstractmethod
    def update_on_response(self, response: UdsResponse) -> Optional[TypingStateTransition]:
        """
        Access whether adjustment of current value is needed after transmission of the diagnostic response.

        Method to be executed after each successful transmission of any diagnostic response by the server.

        :param response: Diagnostic request that was transmitted.

        :return: None if state remain unchanged or StateTransition that was performed.
        """

    @abstractmethod
    def update_on_other_state_transition(self,
                                         state_name: TypingStateName,
                                         previous_value: TypingStateValue,
                                         new_value: TypingStateValue) -> Optional[TypingStateTransition]:
        """
        Access whether adjustment of current value is needed after transition of another state.

        :param state_name: Name of state that was changed.
        :param previous_value: Value from which the other state was changed.
        :param new_value: Value to which the other state was changed.

        :return: None if state remain unchanged or StateTransition that was performed.
        """

    @abstractmethod
    def update_on_idle(self) -> Optional[TypingStateTransition]:
        """
        Access whether adjustment of current state is needed after being in idle.

        Method to be executed anytime by the server.

        :return: None if state remain unchanged or StateTransition that was performed.
        """


class ResponseRule(ABC):
    """A single rule for creating response message by a server."""

    def __init__(self, addressing_types: TypingAddressingTypes, related_request_sids: TypingRequestSIDs) -> None:
        """
        Configure the rule.

        :param addressing_types: Addressing Type for which the rule is applicable.
        :param related_request_sids: Service Identifiers for which the rule is applicable.
        """

    @abstractmethod
    def is_triggered(self, request: UdsRequest, current_states: TypingCurrentStatesValues) -> bool:
        """
        Check if the rule might be used to generate a response message for the received request.

        :param request: Request message that was received.
        :param current_states: Current values of all server's states.

        :return: True if the rule is applicable in provided situation, False otherwise.
        """

    @abstractmethod
    def create_response(self, request: UdsRequest, current_states: TypingCurrentStatesValues) -> Optional[UdsResponse]:
        """
        Create response message according to the rule.

        :param request: Request message for which response to be generated.
        :param current_states: Current values of all server's states.

        :return: Response message that was generated. None if no message to be sent in the response.
        """


TypingRules = List[ResponseRule]
TypingStates = Container[ServerState]


class ResponseManager:
    """
    Unit that automatically creates responses for incoming requests according to the set of rules.

    ResponseManager is meant to fully simulate responses of any server (ECU). It stores current state of the server and
    contains rules (ordered according to priority) which describes how to create response message in given situation.
    """

    __EMERGENCY_RESPONSE_RULES = ()

    def __init__(self, response_rules: TypingRules, server_states: TypingStates) -> None:
        """
        Create response manager, define rules it uses and states that it contains.

        :param response_rules: Rules (in priority order) that the manager is meant to use to generate response messages
            to any incoming request.
        :param server_states: States (e.g. DiagnosticSession SecurityAccess) of the server might change during
            the diagnostic communication.
        """

    @property
    def current_states_values(self) -> TypingCurrentStatesValues:
        """Values for all the states that the simulated server currently is in."""

    @property
    def response_rules(self) -> TypingRules:
        """Rules (in priority order) that the manager is currently using."""

    def create_response(self, request: UdsRequest) -> Optional[UdsResponse]:
        """
        Create response message according to the rule.

        :param request: Request message for which response to be generated.

        :return: Response message that was generated. None if no message to be sent in the response.
        """

"""
Implementation of manager which is meant auto-generate responses to any received request.

ResponseManager is meant to:
 - store current diagnostic states of server ECU (contains state machine)
 - contain ordered rules which determines how to create a response message to any received request
"""

__all__ = ["ServerState", "ResponseRule", "ResponseManager"]

from abc import ABC, abstractmethod
from typing import Optional

from .types import *


class ServerState(ABC):
    """
    A single diagnostic state (e.g. session, security access).

    AbstractClass contains common implementation of handler for any diagnostic state of simulated server.
    SubClass is meant to be contain set of rules (e.g. when to perform transition, what are possible values) that
    describes generic mechanism of the state.
    Instance of a SubClass is meant to additionally store current value of the state for a single simulated server.
    """

    def __init__(self, state_name: StateName, initial_value: StateValue) -> None:
        """
        Define the state.

        :param state_name: Name of the state.
        :param initial_value: Initial value that this state is supposed to be in.
        """
        if not isinstance(state_name, StateName):
            raise TypeError(f"'state_name' is not {StateName} type")
        if initial_value not in self.possible_values:
            raise ValueError(f"'initial_value' is not a member of 'possible_values'; "
                             f"initial_value={repr(initial_value)}; possible_values={repr(self.possible_values)}")
        self.state_name = state_name
        self.__current_value = initial_value

    @property
    def current_value(self) -> StateValue:
        """
        Value that the server is currently in.

        WARNING!
        Execute 'update_on_idle' before reading the value to make sure that the state has not changed during
        the idle state.
        """
        return self.__current_value

    @property
    @abstractmethod
    def possible_values(self) -> StateValues:
        """All possible values of this state."""

    @property
    @abstractmethod
    def depends_on(self) -> StateNames:
        """
        Names of all states which change might cause transition of this state as well.

        Example:
            Assume this class contains definition of SecurityAccess state.
            According to ISO 14229 SecurityAccess might must always be in 'locked' state if ECU is in 'default session'.
            This means that this state depends on DiagnosticSession as transition to 'default session' must cause
            transition to 'locked' state of SecurityAccess.
        """

    @abstractmethod
    def update_on_request(self, request: UdsRequest) -> Optional[StateTransition]:
        """
        Access whether adjustment of current value is needed after reception of the diagnostic request.

        Method to be executed after each successful reception of any diagnostic request by the server.

        :param request: Diagnostic request that was received.

        :return: None if state remain unchanged or StateTransition that was performed.
        """

    @abstractmethod
    def update_on_response(self, response: UdsResponse) -> Optional[StateTransition]:
        """
        Access whether adjustment of current value is needed after transmission of the diagnostic response.

        Method to be executed after each successful transmission of any diagnostic response by the server.

        :param response: Diagnostic request that was transmitted.

        :return: None if state remain unchanged or StateTransition that was performed.
        """

    @abstractmethod
    def update_on_other_state_transition(self,
                                         state_name: StateName,
                                         previous_value: StateValue,
                                         new_value: StateValue) -> Optional[StateTransition]:
        """
        Access whether adjustment of current value is needed after transition of another state.

        :param state_name: Name of state that was changed.
        :param previous_value: Value from which the other state was changed.
        :param new_value: Value to which the other state was changed.

        :return: None if state remain unchanged or StateTransition that was performed.
        """

    @abstractmethod
    def update_on_idle(self) -> Optional[StateTransition]:
        """
        Access whether adjustment of current state is needed after being in idle.

        Method to be executed anytime by the server.

        :return: None if state remain unchanged or StateTransition that was performed.
        """


class ResponseRule(ABC):
    """A single rule for creating response message by a server."""

    def __init__(self, addressing_types: AddressingTypes, related_request_sids: RequestSIDs) -> None:
        """
        Configure the rule.

        :param addressing_types: Addressing Type for which the rule is applicable.
        :param related_request_sids: Service Identifiers for which the rule is applicable.
        """
        self.__validate_addressing_types(addressing_types=addressing_types)
        self.__validate_related_request_sids(related_request_sids=related_request_sids)
        self.__addressing_types = set(addressing_types)
        self.__related_request_sids = set(related_request_sids)

    @staticmethod
    def __validate_addressing_types(addressing_types: AddressingTypes) -> None:
        """
        Verify addressing types argument.

        :param addressing_types: Addressing types to validate.

        :raise TypeError: Addressing types argument is not Iterable.
        :raise ValueError: At least one member of addressing types is not AddressingType.
        """
        if not isinstance(addressing_types, (set, tuple, list)):
            raise TypeError("'addressing_types' is not iterable")
        if not all([isinstance(addressing_type, AddressingType) for addressing_type in addressing_types]):
            raise ValueError("'addressing_types' does not contain instances of AddressingType only")

    @staticmethod
    def __validate_related_request_sids(related_request_sids: RequestSIDs) -> None:
        """
        Verify related requests SIDs argument.

        :param related_request_sids: Requests SIDs to validate.

        :raise TypeError: Related requests SIDs argument is not Iterable.
        :raise ValueError: At least one member of related requests sids is not raw byte.
        """
        if not isinstance(related_request_sids, (set, tuple, list)):
            raise TypeError("'related_request_sids' is not iterable")
        if not all([isinstance(sid, int) and 0x00 <= sid <= 0xFF for sid in related_request_sids]):
            raise ValueError("'related_request_sids' does not contain raw bytes only")

    @abstractmethod
    def is_triggered(self, request: UdsRequest, current_states: CurrentStatesValues) -> bool:
        """
        Check if the rule might be used to generate a response message for the received request.

        :param request: Request message that was received.
        :param current_states: Current values of all server's states.

        :return: True if the rule is applicable in provided situation, False otherwise.
        """

    @abstractmethod
    def create_response(self, request: UdsRequest, current_states: CurrentStatesValues) -> Optional[UdsResponse]:
        """
        Create response message according to the rule.

        :param request: Request message for which response to be generated.
        :param current_states: Current values of all server's states.

        :return: Response message that was generated. None if no message to be sent in the response.
        """

    @property
    def addressing_types(self) -> AddressingTypes:
        """Addressing types of incoming requests for which this rule is supported."""
        return self.__addressing_types

    @property
    def related_request_sids(self) -> RequestSIDs:
        """Service Identifiers of incoming requests for which this rule is supported."""
        return self.__related_request_sids


Rules = List[ResponseRule]
States = Container[ServerState]


class ResponseManager:
    """
    Unit that automatically creates responses for incoming requests according to the set of rules.

    ResponseManager is meant to fully simulate responses of any server (ECU). It stores current state of the server and
    contains rules (ordered according to priority) which describes how to create response message in given situation.
    """

    __EMERGENCY_RESPONSE_RULES = ()

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
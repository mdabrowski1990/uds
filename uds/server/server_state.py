"""Implementation of server states stored and automatically updated by response manager."""

__all__ = ["ServerState"]

from abc import ABC, abstractmethod
from typing import Optional

from .types import StateName, StateNames, StateValue, StateValuesContainer, StateTransition, UdsRequest, UdsResponse


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
    def possible_values(self) -> StateValuesContainer:
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
    def update_on_response(self, response: UdsResponse) -> Optional[StateTransition]:  # noqa: F841
        """
        Access whether adjustment of current value is needed after transmission of the diagnostic response.

        Method to be executed after each successful transmission of any diagnostic response by the server.

        :param response: Diagnostic request that was transmitted.

        :return: None if state remain unchanged or StateTransition that was performed.
        """

    @abstractmethod
    def update_on_other_state_transition(self,
                                         state_name: StateName,
                                         previous_value: StateValue,  # noqa: F841
                                         new_value: StateValue) -> Optional[StateTransition]:  # noqa: F841
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

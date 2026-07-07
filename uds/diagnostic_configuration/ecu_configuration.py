"""Implementation for diagnostic ECU Configuration."""

from operator import getitem
from types import MappingProxyType
from typing import Any, Collection, Mapping, Set, Union

from uds.message import (
    SERVICES_WITH_DID,
    SERVICES_WITH_RID,
    SERVICES_WITH_SUBFUNCTION,
    RequestSID,
    ResponseSID,
    UdsMessage,
    UdsMessageRecord,
)
from uds.translator import BASE_TRANSLATOR
from uds.utilities import SPRMIB_MASK, InconsistencyError, ReassignmentError

from .state import State


class EcuDiagnosticConfiguration:
    """Configuration of restrictions used by ECU for diagnostic messages."""

    RequiredStatesAlias = Mapping[str, Collection[Any]]
    """Alias storing states names and required values."""

    def __init__(self, *,
                 states: Collection[State],
                 sid_restrictions: Mapping[Union[RequestSID, ResponseSID], RequiredStatesAlias],
                 subfunction_restrictions: Mapping[Union[RequestSID, ResponseSID], Mapping[int, RequiredStatesAlias]],
                 did_restrictions: Mapping[int, RequiredStatesAlias],
                 rid_restrictions: Mapping[int, RequiredStatesAlias]) -> None:
        """
        Configure restrictions used by ECU for diagnostic messages.

        :param states: ECU states relevant for diagnostic communication.
        :param sid_restrictions: Requirements on states to execute request message successfully with given SID value.
        :param subfunction_restrictions: Requirements on states to execute request message successfully with given SubFunction value.
        :param did_restrictions: Requirements on states to execute request message successfully with given DID value.
        :param rid_restrictions: Requirements on states to execute request message successfully with given RID value.

        .. note:: By default all possible restrictions are applied.

            Conclusions:
                If some parameter is always supported, all states have to be provided.
                If some parameter is never support, no need to provide include it as that is default assumption.
        """
        self.states = states
        self.sid_restrictions = sid_restrictions
        self.subfunction_restrictions = subfunction_restrictions
        self.did_restrictions = did_restrictions
        self.rid_restrictions = rid_restrictions

    def __getitem__(self, item: str) -> State:
        """Get State by name."""
        return self.states_mapping[item]

    @property
    def states(self) -> Set[State]:
        """Get ECU states that are relevant for diagnostic communication."""
        return self.__states

    @states.setter
    def states(self, states: Collection[State]) -> None:
        """
        Set ECU states relevant for diagnostic communication.

        :param states: ECU states relevant for diagnostic communication.
        """
        if hasattr(self, "_EcuDiagnosticConfiguration__states"):
            raise ReassignmentError("Value of 'states' attribute cannot be changed once assigned. "
                                    "Create a new object instead.")
        self.__states = set(states)
        self.__states_names = {state.name for state in self.__states}
        self.__states_mapping = {state.name: state for state in self.__states}

    @property
    def states_names(self) -> Set[str]:
        """Get names of all ECU states."""
        return self.__states_names

    @property
    def states_mapping(self) -> Mapping[str, State]:
        """Get names of all ECU states."""
        return self.__states_mapping

    @property
    def sid_restrictions(self) -> Mapping[Union[RequestSID, ResponseSID], RequiredStatesAlias]:
        """Get ECU restrictions for SID handling."""
        return self.__sid_restrictions

    @sid_restrictions.setter
    def sid_restrictions(self, value: Mapping[Union[RequestSID, ResponseSID], RequiredStatesAlias]) -> None:
        """
        Set ECU restrictions for SID handling.

        :param value:

        :raise TypeError:
        :raise ValueError:
        """
        if not isinstance(value, Mapping):
            raise TypeError(f"Provided value is not a Mapping. Actual type: {type(value)}.")
        mapping = dict(value)
        for sid, required_states in value.items():
            if not RequestSID.is_request_sid(sid) and not ResponseSID.is_response_sid(sid):
                raise ValueError(f"Mapping contains key that is neither RequestSID nor ResponseSID value. "
                                 f"Actual value: {sid!r}.")
            mapping[sid] = self.__validate_required_states(required_states)
        self.__sid_restrictions = MappingProxyType(mapping)

    @property
    def subfunction_restrictions(self) -> Mapping[Union[RequestSID, ResponseSID], RequiredStatesAlias]:
        """Get ECU restrictions for SID handling."""
        return self.__subfunction_restrictions

    @subfunction_restrictions.setter
    def subfunction_restrictions(self, value: Mapping[Union[RequestSID, ResponseSID], RequiredStatesAlias]) -> None:
        """Set ECU restrictions for SID handling."""
        if not isinstance(value, dict):
            raise TypeError
        self.__subfunction_restrictions = MappingProxyType(value)

    @property
    def did_restrictions(self) -> Mapping[Union[RequestSID, ResponseSID], RequiredStatesAlias]:
        """Get ECU restrictions for SID handling."""
        return self.__did_restrictions

    @did_restrictions.setter
    def did_restrictions(self, value: Mapping[Union[RequestSID, ResponseSID], RequiredStatesAlias]) -> None:
        """Set ECU restrictions for SID handling."""
        if not isinstance(value, dict):
            raise TypeError
        self.__did_restrictions = MappingProxyType(value)

    @property
    def rid_restrictions(self) -> Mapping[Union[RequestSID, ResponseSID], RequiredStatesAlias]:
        """Get ECU restrictions for SID handling."""
        return self.__rid_restrictions

    @rid_restrictions.setter
    def rid_restrictions(self, value: Mapping[Union[RequestSID, ResponseSID], RequiredStatesAlias]) -> None:
        """Set ECU restrictions for SID handling."""
        if not isinstance(value, dict):
            raise TypeError
        self.__rid_restrictions = MappingProxyType(value)

    def __validate_required_states(self, required_states: RequiredStatesAlias) -> RequiredStatesAlias:
        """
        Validate required states mapping.

        :param required_states: State name to restricted state values.

        :raise InconsistencyError: Provided mapping is not consistent with configured states.

        :return: The same mapping using non-mutable types.
        """
        mapping = dict(required_states)
        for state_name, state_values in required_states.items():
            if state_name not in self.states_names:
                raise InconsistencyError(f"Mapping contains name for a state that is not added: {state_name!r}.")
            state = getitem(self, state_name)
            if not state.possible_values.issuperset(state_values):
                raise InconsistencyError(f"Mapping contains state values that are unreachable. "
                                         f"State name: {state_name!r}. "
                                         f"All state values: {state.possible_values}. "
                                         f"Restriction values from mapping: {state_values}.")
            mapping[state_name] = frozenset(state_values)
        return MappingProxyType(mapping)

    def get_restrictions(self, message: Union[UdsMessage, UdsMessageRecord]) -> RequiredStatesAlias:
        """
        Get restrictions used by ECU for given diagnostic message.

        :param message: Message to get restrictions for.

        :return: Mapping with diagnostic message restrictions, where:
            - key is a state name
            - value is a collection of values that given state have to take to successfully execute the message
        """
        sid = message.payload[0]
        dids = set()
        rids = set()
        subfunction = None
        try:
            decoded_message = BASE_TRANSLATOR.decode(message)
        except ValueError:
            decoded_message = None
        if sid in SERVICES_WITH_SUBFUNCTION and len(message.payload) > 1:
            subfunction = message.payload[1] & (0xFF ^ SPRMIB_MASK)
        if sid in SERVICES_WITH_DID and decoded_message is not None:
            for decoded_data_record in decoded_message:
                if decoded_data_record.name == "DID" or (decoded_data_record.name.startwith("DID#") and decoded_data_record.name[4:].isdigit()):
                    if isinstance(decoded_data_record.raw_value, int):
                        dids.add(decoded_data_record.raw_value)
                    else:
                        dids.update(decoded_data_record.raw_value)
        if sid in SERVICES_WITH_RID and decoded_message is not None:
            for decoded_data_record in decoded_message:
                if decoded_data_record.name == "RID":
                    rids.add(decoded_data_record.raw_value)
        # TODO: collect states values
        # TODO: perform intersection on values of each state
        # TODO: return the outcome
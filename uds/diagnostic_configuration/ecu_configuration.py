"""Implementation for diagnostic ECU Configuration."""

from collections.abc import Collection, Mapping
from operator import getitem
from types import MappingProxyType
from typing import Any

from uds.message import (
    SERVICES_WITH_DID,
    SERVICES_WITH_RID,
    SERVICES_WITH_SUBFUNCTION,
    RequestSID,
    ResponseSID,
    SidAlias,
)
from uds.translator import BASE_TRANSLATOR, DecodedMessageAlias
from uds.utilities import (
    SUBFUNCTION_MASK,
    InconsistencyError,
    RawBytesAlias,
    ReassignmentError,
    validate_raw_2byte_value,
    validate_raw_byte,
    validate_raw_bytes,
)

from .state import State


class EcuDiagnosticConfiguration:
    """Configuration of restrictions used by ECU for diagnostic messages."""

    RequiredStatesAlias = Mapping[str, Collection[Any]]
    """Alias storing states names and required values."""

    def __init__(self, *,
                 states: Collection[State],
                 sid_restrictions: Mapping[SidAlias, RequiredStatesAlias],
                 subfunction_restrictions: Mapping[SidAlias, Mapping[int, RequiredStatesAlias]],
                 did_restrictions: Mapping[SidAlias, Mapping[int, RequiredStatesAlias]],
                 rid_restrictions: Mapping[SidAlias, Mapping[int, RequiredStatesAlias]]) -> None:
        """
        Configure restrictions used by ECU for diagnostic messages.

        :param states: ECU states relevant for diagnostic communication.
        :param sid_restrictions: Requirements on states to execute request message successfully with given SID value.
        :param subfunction_restrictions: Requirements on states to execute request message successfully with given
            SubFunction value.
        :param did_restrictions: Requirements on states to execute request message successfully with given DID value.
        :param rid_restrictions: Requirements on states to execute request message successfully with given RID value.

        .. note:: By default all possible restrictions are applied.

            Conclusions:
                If some parameter is always supported, all states and their values have to be provided.
                If some parameter is never support, no need to include restrictions with empty values.
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
    def states(self) -> set[State]:
        """Get :ref:`ECU states <knowledge-base-states>` relevant for diagnostic communication."""
        return self.__states

    @states.setter
    def states(self, states: Collection[State]) -> None:
        """
        Set :ref:`ECU states <knowledge-base-states>` relevant for diagnostic communication.

        :param states: ECU states relevant for diagnostic communication.
        """
        if hasattr(self, "_EcuDiagnosticConfiguration__states"):
            raise ReassignmentError("Value of 'states' attribute cannot be changed once assigned. "
                                    "Create a new object instead.")
        self.__states = set(states)
        self.__states_names = {state.name for state in self.__states}
        self.__states_mapping = {state.name: state for state in self.__states}

    @property
    def states_names(self) -> set[str]:
        """Get names of all ECU states."""
        return self.__states_names

    @property
    def states_mapping(self) -> Mapping[str, State]:
        """Get names of all ECU states."""
        return self.__states_mapping

    @property
    def sid_restrictions(self) -> Mapping[SidAlias, RequiredStatesAlias]:
        """Get ECU restrictions for SID handling."""
        return self.__sid_restrictions

    @sid_restrictions.setter
    def sid_restrictions(self, value: Mapping[SidAlias, RequiredStatesAlias]) -> None:
        """
        Set ECU restrictions for SID handling.

        :param value: Value to set.

        :raise TypeError: Value is not Mapping type.
        :raise ValueError: Keys in the Mapping are not SID values only.
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
    def subfunction_restrictions(self) -> Mapping[SidAlias, Mapping[int, RequiredStatesAlias]]:
        """Get ECU restrictions for SubFunctions handling."""
        return self.__subfunction_restrictions

    @subfunction_restrictions.setter
    def subfunction_restrictions(self, value: Mapping[SidAlias, Mapping[int, RequiredStatesAlias]]) -> None:
        """
        Set ECU restrictions for SubFunctions handling.

        :param value: Value to set.

        :raise TypeError: Value is not Mapping type.
        :raise ValueError: Keys in the Mapping are not SID values only.
        :raise InconsistencyError: Key in provided mapping does not belong to service that contains SubFunctions
            in their message format.
        """
        if not isinstance(value, Mapping):
            raise TypeError(f"Provided value is not a Mapping. Actual type: {type(value)}.")
        mapping = dict(value)
        for sid, subfunction_required_states in value.items():
            if not RequestSID.is_request_sid(sid) and not ResponseSID.is_response_sid(sid):
                raise ValueError(f"Mapping contains key that is neither RequestSID nor ResponseSID value. "
                                 f"Actual value: {sid!r}.")
            if sid not in SERVICES_WITH_SUBFUNCTION:
                raise InconsistencyError(f"Mapping contains key that is SID for services that does not "
                                         f"use SubFunctions. Actual value: {sid!r}. "
                                         f"Update `uds.message.SERVICES_WITH_SUBFUNCTION` if this is "
                                         f"False-Negative error.")
            subfunction_mapping = {}
            for subfunction, required_states in subfunction_required_states.items():
                validate_raw_byte(subfunction)
                subfunction_mapping[subfunction & SUBFUNCTION_MASK] = self.__validate_required_states(required_states)
            mapping[sid] = MappingProxyType(subfunction_mapping)
        self.__subfunction_restrictions = MappingProxyType(mapping)

    @property
    def did_restrictions(self) -> Mapping[SidAlias, Mapping[int, RequiredStatesAlias]]:
        """Get ECU restrictions for DIDs handling."""
        return self.__did_restrictions

    @did_restrictions.setter
    def did_restrictions(self, value: Mapping[SidAlias, Mapping[int, RequiredStatesAlias]]) -> None:
        """
        Set ECU restrictions for DID handling.

        :param value: Value to set.

        :raise TypeError: Value is not Mapping type.
        :raise ValueError: Keys in the Mapping are not SID values only.
        :raise InconsistencyError: Key in provided mapping does not belong to service that contains DIDs
            in their message format.
        """
        if not isinstance(value, Mapping):
            raise TypeError(f"Provided value is not a Mapping. Actual type: {type(value)}.")
        mapping = dict(value)
        for sid, did_required_states in value.items():
            if not RequestSID.is_request_sid(sid) and not ResponseSID.is_response_sid(sid):
                raise ValueError(f"Mapping contains key that is neither RequestSID nor ResponseSID value. "
                                 f"Actual value: {sid!r}.")
            if sid not in SERVICES_WITH_DID:
                raise InconsistencyError(f"Mapping contains key that is SID for services that does not use DIDs. "
                                         f"Actual value: {sid!r}. "
                                         f"Update `uds.message.SERVICES_WITH_DID` if this is False-Negative error.")
            did_mapping = {}
            for did, required_states in did_required_states.items():
                validate_raw_2byte_value(did)
                did_mapping[did] = self.__validate_required_states(required_states)
            mapping[sid] = MappingProxyType(did_mapping)
        self.__did_restrictions = MappingProxyType(mapping)

    @property
    def rid_restrictions(self) -> Mapping[SidAlias, Mapping[int, RequiredStatesAlias]]:
        """Get ECU restrictions for SID handling."""
        return self.__rid_restrictions

    @rid_restrictions.setter
    def rid_restrictions(self, value: Mapping[SidAlias, Mapping[int, RequiredStatesAlias]]) -> None:
        """
        Set ECU restrictions for RID handling.

        :param value: Value to set.

        :raise TypeError: Value is not Mapping type.
        :raise ValueError: Keys in the Mapping are not SID values only.
        :raise InconsistencyError: Key in provided mapping does not belong to service that contains RIDs
            in their message format.
        """
        if not isinstance(value, Mapping):
            raise TypeError(f"Provided value is not a Mapping. Actual type: {type(value)}.")
        mapping = dict(value)
        for sid, rid_required_states in value.items():
            if not RequestSID.is_request_sid(sid) and not ResponseSID.is_response_sid(sid):
                raise ValueError(f"Mapping contains key that is neither RequestSID nor ResponseSID value. "
                                 f"Actual value: {sid!r}.")
            if sid not in SERVICES_WITH_RID:
                raise InconsistencyError(f"Mapping contains key that is SID for services that does not use RIDs. "
                                         f"Actual value: {sid!r}. "
                                         f"Update `uds.message.SERVICES_WITH_RID` if this is False-Negative error.")
            rid_mapping = {}
            for rid, required_states in rid_required_states.items():
                validate_raw_2byte_value(rid)
                rid_mapping[rid] = self.__validate_required_states(required_states)
            mapping[sid] = MappingProxyType(rid_mapping)
        self.__rid_restrictions = MappingProxyType(mapping)

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

    @staticmethod
    def __extract_subfunction(message_payload: RawBytesAlias) -> None | int:
        """Extract subfunction from message payload."""
        if message_payload[0] in SERVICES_WITH_SUBFUNCTION and len(message_payload) > 1:
            return message_payload[1] & SUBFUNCTION_MASK
        return None

    @staticmethod
    def __extract_dids(decoded_message: DecodedMessageAlias) -> set[int]:
        """Extract DIDs from decoded message."""
        dids = set()
        if decoded_message[0]["raw_value"] in SERVICES_WITH_DID:
            for decoded_data_record in decoded_message:
                if (decoded_data_record["name"] == "DID"
                        or (decoded_data_record["name"].startswith("DID#") and decoded_data_record["name"][
                            4:].isdigit())):
                    if isinstance(decoded_data_record["raw_value"], int):
                        dids.add(decoded_data_record["raw_value"])
                    else:
                        dids.update(decoded_data_record["raw_value"])
        return dids

    @staticmethod
    def __extract_rids(decoded_message: DecodedMessageAlias) -> set[int]:
        """Extract RIDs from decoded message."""
        rids = set()
        if decoded_message[0]["raw_value"] in SERVICES_WITH_RID:
            for decoded_data_record in decoded_message:
                if (decoded_data_record["name"] == "RID"
                        or (decoded_data_record["name"].startswith("RID#") and decoded_data_record["name"][
                            4:].isdigit())):
                    if isinstance(decoded_data_record["raw_value"], int):
                        rids.add(decoded_data_record["raw_value"])
                    else:
                        rids.update(decoded_data_record["raw_value"])
        return rids

    def combine_restrictions(self, *restrictions: RequiredStatesAlias) -> RequiredStatesAlias:
        """
        Combine multiple restrictions.

        :param restrictions: Restrictions to combine.

        :raise ValueError: At least one restriction must be provided.

        :return: Combined restrictions.
        """
        if not restrictions:
            raise ValueError("No restrictions to combine were provided")
        combined_restrictions = {}
        for state_name in self.states_names:
            all_possible_values = self.states_mapping[state_name].possible_values
            combined_restrictions[state_name] = set.intersection(*[set(restriction.get(state_name, all_possible_values))
                                                                   for restriction in restrictions])
        return combined_restrictions

    def get_restrictions(self, message_payload: RawBytesAlias) -> RequiredStatesAlias:
        """
        Get restrictions used by ECU for given diagnostic message.

        :param message_payload: Payload of message to get restrictions for.

        :return: Mapping with diagnostic message restrictions, where:
            - key is a state name
            - value is a collection of values that given state have to take to successfully execute the message
        """
        validate_raw_bytes(message_payload, allow_empty=False)
        sid = message_payload[0]
        try:
            decoded_message = BASE_TRANSLATOR.decode(message_payload)
        except (ValueError, KeyError):
            dids = set()
            rids = set()
        else:
            dids = self.__extract_dids(decoded_message=decoded_message)
            rids = self.__extract_rids(decoded_message=decoded_message)
        subfunction = self.__extract_subfunction(message_payload=message_payload)
        restrictions = [self.sid_restrictions[sid]]
        if subfunction is not None:
            restrictions.append(self.subfunction_restrictions[sid][subfunction])
        for did in dids:
            restrictions.append(self.did_restrictions[sid][did])
        for rid in rids:
            restrictions.append(self.rid_restrictions[sid][rid])
        return self.combine_restrictions(*restrictions)

"""Implementation of container for storing diagnostic messages restrictions."""

from typing import Collection, Dict, Any, Union, Set, Optional

from uds.message import RequestSID, UdsMessage, UdsMessageRecord, ResponseSID, SERVICES_WITH_SUBFUNCTION, SERVICES_WITH_DID, SERVICES_WITH_RID
from uds.utilities import ReassignmentError, SPRMIB_MASK
from .state import State
from uds.translator import BASE_TRANSLATOR


class EcuDiagnosticConfiguration:
    """Configuration of restrictions used by ECU for diagnostic messages."""

    RequiredStatesAlias = Dict[str, Collection[Any]]
    """Alias storing states names and required values."""

    def __init__(self, *,
                 states: Collection[State],
                 sid_restrictions: Dict[Union[RequestSID, ResponseSID], RequiredStatesAlias],
                 subfunction_restrictions: Dict[Union[RequestSID, ResponseSID], Dict[int, RequiredStatesAlias]],
                 did_restrictions: Dict[int, RequiredStatesAlias],
                 rid_restrictions: Dict[int, RequiredStatesAlias]) -> None:
        """
        Configure restrictions used by ECU for diagnostic messages.

        :param states: ECU states relevant for diagnostic communication.
        :param sid_restrictions: Requirements on states to execute request message successfully with given SID value.
        :param subfunction_restrictions: Requirements on states to execute request message successfully with given SubFunction value.
        :param did_restrictions: Requirements on states to execute request message successfully with given DID value.
        :param rid_restrictions: Requirements on states to execute request message successfully with given RID value.

        .. note:: By default all possible restrictions are applied.

            Conclusion: If some parameter is always supported, all states have to be provided.
        """
        self.states = states
        self.sid_restrictions = sid_restrictions
        self.subfunction_restrictions = subfunction_restrictions
        self.did_restrictions = did_restrictions
        self.rid_restrictions = rid_restrictions

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
            raise ReassignmentError("Value of 'states' attribute cannot be changed once assigned.")
        self.__states = set(states)

    @property
    def sid_restrictions(self) -> Dict[Union[RequestSID, ResponseSID], RequiredStatesAlias]:
        return self.__sid_restrictions

    @sid_restrictions.setter
    def sid_restrictions(self, value: Dict[Union[RequestSID, ResponseSID], RequiredStatesAlias]) -> None:
        if not isinstance(value, dict):
            raise TypeError
        self.__sid_restrictions = value

    # TODO: subfunction_restrictions
    # TODO: did_restrictions
    # TODO: rid_restrictions

    def get_restrictions(self, message: Union[UdsMessage, UdsMessageRecord]) -> RequiredStatesAlias:
        """
        Get restrictions used by ECU for given diagnostic message.

        :param message: Message to get restrictions for.

        :return: Dictionary with diagnostic message restrictions, where:
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
"""Implementation of container for storing diagnostic messages restrictions."""

from typing import Collection, Dict, Any, Union

from uds.message import RequestSID, UdsMessage, UdsMessageRecord
from .state import State


class EcuDiagnosticConfiguration:
    """Configuration of restrictions used by ECU for diagnostic messages."""

    RequiredStatesAlias = Dict[str, Collection[Any]]
    """Alias storing states names and required values."""

    def __init__(self, *,
                 states: Collection[State],
                 sid_restrictions: Dict[RequestSID, RequiredStatesAlias],
                 sub_function_restrictions: Dict[RequestSID, Dict[int, RequiredStatesAlias]],
                 did_restrictions: Dict[int, RequiredStatesAlias],
                 rid_restrictions: Dict[int, RequiredStatesAlias]) -> None:
        """
        Configure restrictions used by ECU for diagnostic messages.

        :param states: ECU states relevant for diagnostic communication.
        :param sid_restrictions: Requirements on states to execute request message successfully with given SID value.
        :param sub_function_restrictions: Requirements on states to execute request message successfully with given SubFunction value.
        :param did_restrictions: Requirements on states to execute request message successfully with given DID value.
        :param rid_restrictions: Requirements on states to execute request message successfully with given RID value.

        .. note:: By default no restrictions are applied.

            Conclusion: There is no need to provide restrictions for parameters that are always supported.
        """
        # TODO

    def get_restrictions(self, message: Union[UdsMessage, UdsMessageRecord]) -> RequiredStatesAlias:
        """
        Get restrictions used by ECU for given diagnostic message.

        :param message: Message to get restrictions for.

        :return: Dictionary with diagnostic message restrictions, where:
            - key is a state name
            - value is a collection of values that given state have to take to successfully execute the message
        """
        # TODO

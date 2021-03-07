"""
Implementation of manager which is meant auto-generate responses to any received request.

ResponseManager is meant to:
 - store current diagnostic states of server ECU (contains state machine)
 - contain ordered rules which determines how to create a response message to any received request
"""

__all__ = ["ResponseRule", "ResponseManager"]

from abc import ABC, abstractmethod
from typing import Optional

from .types import *
from .server_state import ServerState




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

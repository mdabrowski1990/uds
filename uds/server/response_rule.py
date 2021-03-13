"""Implementation of response rules for automatical creation of response messages to any request."""

__all__ = ["ResponseRule"]

from abc import ABC, abstractmethod
from typing import Optional

from .types import AddressingType, AddressingTypes, RequestSIDRawValues, UdsRequest, UdsResponse, CurrentStatesValues


class ResponseRule(ABC):
    """A single rule for creating response message by a server."""

    def __init__(self, addressing_types: AddressingTypes, related_request_sids: RequestSIDRawValues) -> None:
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
    def __validate_related_request_sids(related_request_sids: RequestSIDRawValues) -> None:
        """
        Verify related requests SIDs argument.

        :param related_request_sids: Requests SIDs to validate.

        :raise TypeError: Related requests SIDs argument is not Iterable.
        :raise ValueError: At least one member of related requests sids is not raw byte.
        """
        if not isinstance(related_request_sids, (set, tuple, list)):
            raise TypeError("'related_request_sids' is not set, tuple or list")
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
    def related_request_sids(self) -> RequestSIDRawValues:
        """Service Identifiers of incoming requests for which this rule is supported."""
        return self.__related_request_sids

"""Attributes that describes UDS transmission."""

__all__ = ["AddressingType", "AddressingMemberTyping", "TransmissionDirection", "DirectionMemberTyping"]

from typing import Union

from aenum import StrEnum

from ..utilities import ValidatedEnum


class AddressingType(StrEnum, ValidatedEnum):
    """
    Types of communication (addressing) defined by UDS.

    Options:
    - PHYSICAL - 1 (client) to 1 (server) communication
    - FUNCTIONAL - 1 (client) to many (servers) communication
    - BROADCAST - 1 (client) to many (servers) communication that does not require response
    """

    PHYSICAL = "Physical"
    FUNCTIONAL = "Functional"
    BROADCAST = "Broadcast"


AddressingMemberTyping = Union[AddressingType, str]  # pylint: disable=unsubscriptable-object


class TransmissionDirection(StrEnum, ValidatedEnum):
    """
    Direction of communication.

    Options:
    - RECEIVED - receiving (received from a bus by python code)
    - TRANSMITTED - transmission (pushed to a bus by python code)
    """

    RECEIVED = "Rx"
    TRANSMITTED = "Tx"


DirectionMemberTyping = Union[TransmissionDirection, str]  # pylint: disable=unsubscriptable-object

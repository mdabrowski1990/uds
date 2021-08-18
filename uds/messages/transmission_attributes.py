"""Attributes that describes UDS transmission."""

__all__ = ["AddressingType", "AddressingMemberTyping", "TransmissionDirection", "DirectionMemberTyping"]

from typing import Union

from aenum import StrEnum

from uds.utilities import ValidatedEnum


class AddressingType(StrEnum, ValidatedEnum):
    """
    Types of communication (addressing) defined by UDS.

    Options:
    - PHYSICAL - 1 (client) to 1 (server) communication
    - FUNCTIONAL - 1 (client) to many (servers) communication
    - BROADCAST - 1 (client) to many (servers) communication that does not require response
    """

    PHYSICAL = "Physical"  # noqa: F841
    FUNCTIONAL = "Functional"  # noqa: F841
    BROADCAST = "Broadcast"  # noqa: F841


AddressingMemberTyping = Union[AddressingType, str]  # pylint: disable=unsubscriptable-object


class TransmissionDirection(StrEnum, ValidatedEnum):
    """
    Direction of communication.

    Options:
    - RECEIVED - receiving (received from a bus by python code)
    - TRANSMITTED - transmission (pushed to a bus by python code)
    """

    RECEIVED = "Rx"  # noqa: F841
    TRANSMITTED = "Tx"  # noqa: F841


DirectionMemberTyping = Union[TransmissionDirection, str]  # pylint: disable=unsubscriptable-object

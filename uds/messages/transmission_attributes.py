"""Attributes that describes UDS transmission."""

__all__ = ["AddressingType", "AddressingMemberTyping", "TransmissionDirection", "DirectionMemberTyping"]

from typing import Union

from aenum import StrEnum

from uds.utilities import ValidatedEnum


class AddressingType(StrEnum, ValidatedEnum):
    """Types of communication (addressing) defined by UDS."""

    PHYSICAL = "Physical"  # noqa: F841
    """Physical addressing - 1 (client) to 1 (server) communication."""
    FUNCTIONAL = "Functional"  # noqa: F841
    """Functional addressing - 1 (client) to many (servers) communication."""
    BROADCAST = "Broadcast"  # noqa: F841
    """
    Functional addressing using broadcast transmission - 1 (client) to many (servers) communication that does not
    require response from recipients.

    Note: This is not a unique addressing.
    """  # TODO: finish note and clarify why it is added


AddressingMemberTyping = Union[AddressingType, str]


class TransmissionDirection(StrEnum, ValidatedEnum):
    """
    Direction of communication.

    Options:
    - RECEIVED - receiving (received from a bus by python code)
    - TRANSMITTED - transmission (pushed to a bus by python code)
    """

    RECEIVED = "Rx"  # noqa: F841
    TRANSMITTED = "Tx"  # noqa: F841


DirectionMemberTyping = Union[TransmissionDirection, str]

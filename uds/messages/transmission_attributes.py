"""Attributes that describes UDS communication."""

__all__ = ["AddressingType", "AddressingMemberTyping", "TransmissionDirection", "DirectionMemberTyping"]

from typing import Union

from aenum import StrEnum

from uds.utilities import ValidatedEnum


class AddressingType(StrEnum, ValidatedEnum):
    """Model of UDS communication."""

    PHYSICAL = "Physical"  # noqa: F841
    """Physical addressing - 1 (client) to 1 (server) communication."""
    FUNCTIONAL = "Functional"  # noqa: F841
    """Functional addressing - 1 (client) to many (servers) communication."""


AddressingMemberTyping = Union[AddressingType, str]
"""Typing that describes AddressingType member."""


class TransmissionDirection(StrEnum, ValidatedEnum):
    """Direction of a communication."""

    RECEIVED = "Rx"  # noqa: F841
    """Incoming transmission from the perspective of the code."""
    TRANSMITTED = "Tx"  # noqa: F841
    """Outcoming transmission from the perspective of the code."""


DirectionMemberTyping = Union[TransmissionDirection, str]
"""Typing that describes TransmissionDirection member."""

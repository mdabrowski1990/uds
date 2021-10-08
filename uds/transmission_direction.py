"""Definition of communication direction."""

__all__ = ["TransmissionDirection", "DirectionMemberTyping"]

from typing import Union

from aenum import StrEnum

from uds.utilities import ValidatedEnum


class TransmissionDirection(StrEnum, ValidatedEnum):
    """Direction of a communication."""

    RECEIVED = "Rx"  # noqa: F841
    """Incoming transmission from the perspective of the code."""
    TRANSMITTED = "Tx"  # noqa: F841
    """Outcoming transmission from the perspective of the code."""


DirectionMemberTyping = Union[TransmissionDirection, str]
"""Typing alias that describes TransmissionDirection member."""

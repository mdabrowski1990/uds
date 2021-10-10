"""Definition of communication direction."""

__all__ = ["TransmissionDirection", "TransmissionDirectionTyping"]

from typing import Union

from aenum import StrEnum, unique

from uds.utilities import ValidatedEnum


@unique
class TransmissionDirection(StrEnum, ValidatedEnum):
    """Direction of a communication."""

    RECEIVED = "Rx"  # noqa: F841
    """Incoming transmission from the perspective of the code."""
    TRANSMITTED = "Tx"  # noqa: F841
    """Outcoming transmission from the perspective of the code."""


TransmissionDirectionTyping = Union[TransmissionDirection, str]
"""Typing alias that describes :class:`~uds.transmission_direction.TransmissionDirection` member."""

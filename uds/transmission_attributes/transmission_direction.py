"""Definition of communication direction."""

__all__ = ["TransmissionDirection", "TransmissionDirectionAlias"]

from typing import Union

from aenum import StrEnum, unique

from uds.utilities import ValidatedEnum


@unique
class TransmissionDirection(StrEnum, ValidatedEnum):
    """Direction of a communication."""

    RECEIVED = "Rx"  # noqa: F841
    """Incoming transmission from the perspective of the code."""
    TRANSMITTED = "Tx"  # noqa: F841
    """Outgoing transmission from the perspective of the code."""


TransmissionDirectionAlias = Union[TransmissionDirection, str]
"""Alias that describes :class:`~uds.transmission_attributes.transmission_direction.TransmissionDirection` member."""

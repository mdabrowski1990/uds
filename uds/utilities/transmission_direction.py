"""Definition of communication direction."""

__all__ = ["TransmissionDirection"]

from aenum import StrEnum as AStrEnum
from aenum import unique

from .enums import ValidatedEnum


@unique
class TransmissionDirection(ValidatedEnum, AStrEnum):  # type: ignore
    """Direction of a communication."""

    RECEIVED: "TransmissionDirection" = "Rx"  # type: ignore
    """Incoming transmission from the perspective of the code."""
    TRANSMITTED: "TransmissionDirection" = "Tx"  # type: ignore
    """Outgoing transmission from the perspective of the code."""

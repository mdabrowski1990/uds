"""Definition of communication direction."""

__all__ = ["TransmissionDirection"]

from aenum import StrEnum, unique

from uds.utilities import ValidatedEnum


@unique
class TransmissionDirection(ValidatedEnum, StrEnum):
    """Direction of a communication."""

    RECEIVED: "TransmissionDirection" = "Rx"  # type: ignore  # noqa: F841
    """Incoming transmission from the perspective of the code."""
    TRANSMITTED: "TransmissionDirection" = "Tx"  # type: ignore  # noqa: F841
    """Outgoing transmission from the perspective of the code."""

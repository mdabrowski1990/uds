"""Definition UDS Addressing Formats for CAN bus."""

__all__ = ["CanAddressingFormat"]

from aenum import StrEnum, unique

from uds.utilities import ValidatedEnum


@unique
class CanAddressingFormat(ValidatedEnum, StrEnum):  # type: ignore
    """
    Addressing formats used for UDS communication over CAN bus.

    :ref:`CAN addressing formats <knowledge-base-can-addressing>` determines how
    :ref:`Network Address Information (N_AI) <knowledge-base-n-ai>` are provided.
    """

    NORMAL_ADDRESSING: "CanAddressingFormat" = "Normal Addressing"  # type: ignore
    """:ref:`Normal addressing <knowledge-base-can-normal-addressing>` format."""
    NORMAL_FIXED_ADDRESSING: "CanAddressingFormat" = "Normal Fixed Addressing"  # type: ignore
    """:ref:`Normal fixed addressing <knowledge-base-can-normal-fixed-addressing>` format.
    It is a sub-format of :ref:`Normal addressing <knowledge-base-can-normal-addressing>` which uses 29-bit
    CAN Identifiers only."""
    EXTENDED_ADDRESSING: "CanAddressingFormat" = "Extended Addressing"  # type: ignore
    """:ref:`Extended addressing <knowledge-base-can-extended-addressing>` format."""
    MIXED_11BIT_ADDRESSING: "CanAddressingFormat" = "Mixed 11-bit Addressing"  # type: ignore
    """:ref:`Mixed addressing with 11-bit CAN ID <knowledge-base-can-mixed-11-bit-addressing>` format.
    It is a sub-format of :ref:`mixed addressing <knowledge-base-can-mixed-addressing>`."""
    MIXED_29BIT_ADDRESSING: "CanAddressingFormat" = "Mixed 29-bit Addressing"  # type: ignore
    """:ref:`Mixed addressing with 29-bit CAN ID <knowledge-base-can-mixed-29-bit-addressing>` format.
    It is a sub-format of :ref:`mixed addressing <knowledge-base-can-mixed-addressing>`."""

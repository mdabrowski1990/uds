"""Implementation of CAN Addressing Formats."""

__all__ = ["CanAddressingFormat"]

from aenum import StrEnum, unique

from uds.utilities import ValidatedEnum


@unique
class CanAddressingFormat(StrEnum, ValidatedEnum):
    """
    Definition of CAN addressing formats.

    :ref:`CAN addressing formats <knowledge-base-can-addressing>` determines how (in which fields of a CAN Packet)
    :ref:`Network Address Information (N_AI) <knowledge-base-n-ai>` is provided.
    """

    NORMAL_11BIT_ADDRESSING: "CanAddressingFormat" = "Normal 11-bit Addressing"  # type: ignore
    """:ref:`Normal addressing <knowledge-base-can-normal-addressing>` format that uses 11-bit CAN Identifiers."""
    NORMAL_FIXED_ADDRESSING: "CanAddressingFormat" = "Normal Fixed Addressing"  # type: ignore
    """:ref:`Normal fixed addressing <knowledge-base-can-normal-fixed-addressing>` format.
    It is a subformat of :ref:`Normal addressing <knowledge-base-can-normal-addressing>` which uses 29-bit
    CAN Identifiers only."""
    EXTENDED_ADDRESSING: "CanAddressingFormat" = "Extended Addressing"  # type: ignore
    """:ref:`Extended addressing <knowledge-base-can-extended-addressing>` format."""
    MIXED_11BIT_ADDRESSING: "CanAddressingFormat" = "Mixed 11-bit Addressing"  # type: ignore
    """:ref:`Mixed addressing with 11-bit CAN ID <knowledge-base-can-mixed-11-bit-addressing>` format.
    It is a subformat of :ref:`mixed addressing <knowledge-base-can-mixed-addressing>`."""
    MIXED_29BIT_ADDRESSING: "CanAddressingFormat" = "Mixed 29-bit Addressing"  # type: ignore
    """:ref:`Mixed addressing with 29-bit CAN ID <knowledge-base-can-mixed-29-bit-addressing>` format.
    It is a subformat of :ref:`mixed addressing <knowledge-base-can-mixed-addressing>`."""

"""Implementation of CAN Addressing Formats."""

__all__ = ["CanAddressingFormat"]

from aenum import StrEnum, unique

from uds.utilities import ValidatedEnum


@unique
class CanAddressingFormat(ValidatedEnum, StrEnum):  # type: ignore
    """
    Definition of CAN addressing formats.

    :ref:`CAN addressing formats <knowledge-base-addressing-addressing>` determines how (in which fields of a CAN Packet)
    :ref:`Network Address Information (N_AI) <knowledge-base-n-ai>` is provided.
    """

    NORMAL_ADDRESSING: "CanAddressingFormat" = "Normal Addressing"  # type: ignore
    """:ref:`Normal addressing <knowledge-base-addressing-normal-addressing>` format."""
    NORMAL_FIXED_ADDRESSING: "CanAddressingFormat" = "Normal Fixed Addressing"  # type: ignore
    """:ref:`Normal fixed addressing <knowledge-base-addressing-normal-fixed-addressing>` format.
    It is a sub-format of :ref:`Normal addressing <knowledge-base-addressing-normal-addressing>` which uses 29-bit
    CAN Identifiers only."""
    EXTENDED_ADDRESSING: "CanAddressingFormat" = "Extended Addressing"  # type: ignore
    """:ref:`Extended addressing <knowledge-base-addressing-extended-addressing>` format."""
    MIXED_11BIT_ADDRESSING: "CanAddressingFormat" = "Mixed 11-bit Addressing"  # type: ignore
    """:ref:`Mixed addressing with 11-bit CAN ID <knowledge-base-addressing-mixed-11-bit-addressing>` format.
    It is a sub-format of :ref:`mixed addressing <knowledge-base-addressing-mixed-addressing>`."""
    MIXED_29BIT_ADDRESSING: "CanAddressingFormat" = "Mixed 29-bit Addressing"  # type: ignore
    """:ref:`Mixed addressing with 29-bit CAN ID <knowledge-base-addressing-mixed-29-bit-addressing>` format.
    It is a sub-format of :ref:`mixed addressing <knowledge-base-addressing-mixed-addressing>`."""

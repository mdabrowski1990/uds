"""CAN Addressing Formats definitions."""

__all__ = ["CanAddressingFormat", "CanAddressingFormatAlias"]

from typing import Union

from aenum import StrEnum, unique

from uds.utilities import ValidatedEnum


@unique
class CanAddressingFormat(StrEnum, ValidatedEnum):
    """
    Definition of CAN addressing formats.

    :ref:`CAN addressing formats <knowledge-base-can-addressing>` determines how
    :ref:`Network Address Information (N_AI) <knowledge-base-n-ai>` is provided in a CAN packet.
    """

    NORMAL_11BIT_ADDRESSING = "Normal 11-bit Addressing"
    """:ref:`Normal addressing <knowledge-base-can-normal-addressing>` that uses 11-bit CAN Identifiers."""
    NORMAL_FIXED_ADDRESSING = "Normal Fixed Addressing"
    """:ref:`Normal fixed addressing <knowledge-base-can-normal-fixed-addressing>` format.
    It uses 29-bit CAN Identifiers only."""
    EXTENDED_ADDRESSING = "Extended Addressing"
    """:ref:`Extended addressing <knowledge-base-can-extended-addressing>` format that uses either 11-bit or 29-bit
    CAN Identifiers."""
    MIXED_11BIT_ADDRESSING = "Mixed 11-bit Addressing"
    """:ref:`Mixed addressing with 11-bit CAN ID <knowledge-base-can-mixed-11-bit-addressing>`. It is a subformat
    of :ref:`mixed addressing <knowledge-base-can-mixed-addressing>` that uses 11-bit CAN Identifiers."""
    MIXED_29BIT_ADDRESSING = "Mixed 29-bit Addressing"
    """:ref:`Mixed addressing with 29-bit CAN ID <knowledge-base-can-mixed-29-bit-addressing>`. It is a subformat
    of :ref:`mixed addressing <knowledge-base-can-mixed-addressing>` that uses 29-bit CAN Identifiers."""


CanAddressingFormatAlias = Union[CanAddressingFormat, str]
"""Alias that describes :class:`~uds.can.addressing_format.CanAddressingFormat` member."""

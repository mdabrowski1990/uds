"""
Definition of attributes that are specific for CAN packets.

This module contains implementation of :ref:`CAN packet <knowledge-base-uds-can-packet>` attributes that describe:
 - :ref:`CAN frame <knowledge-base-can-frame>`
 - :ref:`CAN packet addressing format <knowledge-base-can-addressing>`
 - :ref:`CAN packet data field <knowledge-base-can-data-field>`
 - :ref:`CAN packet type <knowledge-base-can-n-pci>`
"""

__all__ = ["CanPacketType", "CanPacketTypeMemberTyping", "CanAddressingFormat", "CanAddressingFormatTyping",
           "CanIdHandler", "DEFAULT_FILLER_BYTE"]

from typing import Union, Any

from aenum import unique, StrEnum

from uds.utilities import RawByte, ValidatedEnum
from .abstract_packet import AbstractUdsPacketType


DEFAULT_FILLER_BYTE: RawByte = 0xCC
"""Default value of Filler Byte that is specified by ISO 15765-2:2016 (chapter 10.4.2.1).
Filler Byte is used for :ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>`."""


class CanIdHandler:
    """
    Helper class that provides utilities for CAN Identifier field.

    CAN Identifier (CAN ID) is a CAN frame field that informs about a sender and a content of CAN frames.

    CAN supports two formats of CAN ID:
     - Standard (11-bit Identifier)
     - Extended (29-bit Identifier)
    """

    MIN_11BIT_VALUE: int = 0
    MAX_11BIT_VALUE: int = 0x7FF
    MIN_29BIT_VALUE: int = 0x800
    MAX_29BIT_VALUE: int = 0x1FFFFFFF

    @classmethod
    def is_standard_can_id(cls, value: int) -> bool:
        """
        Check if provided value is Standard (11-bit) CAN ID.

        :param value: Value to check.

        :return: True if value is a valid 11-bit CAN ID, False otherwise.
        """
        return cls.MIN_11BIT_VALUE <= value <= cls.MAX_11BIT_VALUE

    @classmethod
    def is_extended_can_id(cls, value: int) -> bool:
        """
        Check if provided value is Extended (29-bit) CAN ID.

        :param value: Value to check.

        :return: True if value is a valid 29-bit CAN ID, False otherwise.
        """
        return cls.MIN_29BIT_VALUE <= value <= cls.MAX_29BIT_VALUE

    @classmethod
    def is_can_id(cls, value: int) -> bool:
        """
        Check if provided value is either Standard or Extended CAN ID.

        :param value: Value to check.

        :return: True if value is a valid CAN ID, False otherwise.
        """
        return cls.is_standard_can_id(value) or cls.is_extended_can_id(value)

    @classmethod
    def validate_can_id(cls, value: Any) -> None:
        """
        Validate if provided value is

        :param value:

        :raise TypeError: Provided value is not int type.
        :raise ValueError: Provided value is out of CAN Identifier values range.
        """
        if not isinstance(value, int):
            raise TypeError(f"Provided value is not int type. Actual type: {type(value)}.")
        if not cls.is_can_id(value):
            raise ValueError(f"Provided value is out of CAN Identifier values range. Actual value: {value}.")


@unique
class CanPacketType(AbstractUdsPacketType):
    """
    Definition of CAN packet types.

    :ref:`CAN packet types <knowledge-base-can-n-pci>` are
    :ref:`Network Protocol Control Information (N_PCI) <knowledge-base-n-pci>` values that are specific for CAN bus.
    """

    SINGLE_FRAME = 0x0
    """:ref:`Single Frame (SF) <knowledge-base-can-single-frame>` CAN packet type."""
    FIRST_FRAME = 0x1
    """:ref:`First Frame (FF) <knowledge-base-can-first-frame>` CAN packet type."""
    CONSECUTIVE_FRAME = 0x2  # noqa: F841
    """:ref:`Consecutive Frame (CF) <knowledge-base-can-consecutive-frame>` CAN packet type."""
    FLOW_CONTROL = 0x3  # noqa: F841
    """:ref:`Flow Control (FC) <knowledge-base-can-flow-control>` CAN packet type."""

    @classmethod
    def is_initial_packet_type(cls, value: Any) -> bool:
        """
        Check whether given argument is a member or a value of a packet type that initiates a diagnostic message.

        :param value: Value to check.

        :return: True if given argument is a packet type that initiates a diagnostic message, else False.
        """
        cls.validate_member(value)
        return cls(value) in (cls.SINGLE_FRAME, cls.FIRST_FRAME)


CanPacketTypeMemberTyping = Union[CanPacketType, int]
"""Typing alias that describes :class:`~uds.packet.can_packet_attributes.CanPacketType` member."""


@unique
class CanAddressingFormat(StrEnum, ValidatedEnum):
    """
    Definition of CAN addressing formats.

    :ref:`CAN addressing formats <knowledge-base-can-addressing>` determines how
    :ref:`Network Address Information (N_AI) <knowledge-base-n-ai>` is provided in a CAN packet.
    """

    NORMAL_11BIT_ADDRESSING = "Normal 11-bit Addressing"  # noqa: F841
    """:ref:`Normal addressing <knowledge-base-can-normal-addressing>` that uses 11-bit CAN Identifiers."""
    NORMAL_FIXED_ADDRESSING = "Normal Fixed Addressing"  # noqa: F841
    """:ref:`Normal fixed addressing <knowledge-base-can-normal-fixed-addressing>` format.
    It uses 29-bit CAN Identifiers only."""
    EXTENDED_ADDRESSING = "Extended Addressing"  # noqa: F841
    """:ref:`Extended addressing <knowledge-base-can-extended-addressing>` format that uses either 11-bit or 29-bit
    CAN Identifiers."""
    MIXED_11BIT_ADDRESSING = "Mixed 11-bit Addressing"  # noqa: F841
    """:ref:`Mixed addressing with 11-bit CAN ID <knowledge-base-can-mixed-11-bit-addressing>`. It is a subformat
    of :ref:`mixed addressing <knowledge-base-can-mixed-addressing>` that uses 11-bit CAN Identifiers."""
    MIXED_29BIT_ADDRESSING = "Mixed 29-bit Addressing"  # noqa: F841
    """:ref:`Mixed addressing with 29-bit CAN ID <knowledge-base-can-mixed-29-bit-addressing>`. It is a subformat
    of :ref:`mixed addressing <knowledge-base-can-mixed-addressing>` that uses 29-bit CAN Identifiers."""


CanAddressingFormatTyping = Union[CanAddressingFormat, str]
"""Typing alias that describes :class:`~uds.packet.can_packet_attributes.CanAddressingFormat` member."""

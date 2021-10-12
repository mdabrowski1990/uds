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

from typing import Union, Any, Tuple

from aenum import unique, StrEnum

from uds.utilities import RawByte, validate_raw_byte, ValidatedEnum
from uds.transmission_attributes import AddressingType, AddressingTypeMemberTyping
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
    """Minimum value of 11-bit CAN ID."""
    MAX_11BIT_VALUE: int = (1 << 11) - 1
    """Maximum value of 11-bit CAN ID."""
    MIN_29BIT_VALUE: int = MAX_11BIT_VALUE + 1
    """Minimum value of 29-bit CAN ID."""
    MAX_29BIT_VALUE: int = (1 << 29) - 1
    """Maximum value of 29-bit CAN ID."""

    NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET: int = 0x18DA0000
    """Physical CAN ID value with Target Address and Source Address information erased.
    CAN ID value is compatible with Normal Fixed Addressing format."""
    NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET: int = 0x18DB0000
    """Functional CAN ID value with Target Address and Source Address information erased.
    CAN ID value is compatible with Normal Fixed Addressing format."""
    MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET: int = 0x18CE0000
    """Physical CAN ID value with Target Address and Source Address information erased.
    CAN ID value is compatible with Mixed Addressing 29-bit format."""
    MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET: int = 0x18CD0000
    """Functional CAN ID value with Target Address and Source Address information erased.
    CAN ID value is compatible with Mixed 29-bit Addressing format."""

    NORMAL_FIXED_CAN_ID_INFO_TYPING = Tuple[AddressingType, RawByte, RawByte]
    """Typing alias of information carried by CAN ID in Normal Fixed Addressing format."""
    MIXED_29BIT_CAN_ID_INFO_TYPING = Tuple[AddressingType, RawByte, RawByte]
    """Typing alias of information carried by CAN ID in Mixed 29-bit Addressing format."""

    @classmethod
    def get_normal_fixed_addressed_can_id(cls,
                                          addressing_type: AddressingTypeMemberTyping,
                                          target_address: RawByte,
                                          source_address: RawByte) -> int:
        """
        Get CAN ID value for Normal Fixed Addressing format.

        :param addressing_type: Addressing type used.
        :param target_address: Target address value to use.
        :param source_address: Source address value to use.

        :return: Value of CAN ID for Normal Fixed Addressing format that was generated from provided values.
        """
        AddressingType.validate_member(addressing_type)
        validate_raw_byte(target_address)
        validate_raw_byte(source_address)
        addressing_type_instance = AddressingType(addressing_type)
        if addressing_type_instance == AddressingType.PHYSICAL:
            return cls.NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET + (target_address << 8) + source_address
        if addressing_type_instance == AddressingType.FUNCTIONAL:
            return cls.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET + (target_address << 8) + source_address
        raise NotImplementedError(f"Unknown addressing type value was provided: {addressing_type}")

    @classmethod
    def get_mixed_addressed_29bit_can_id(cls,
                                         addressing_type: AddressingTypeMemberTyping,
                                         target_address: RawByte,
                                         source_address: RawByte) -> int:
        """
        Get CAN ID value for Mixed Addressing format that uses 29-bit CAN Identifiers.

        :param addressing_type: Addressing type used.
        :param target_address: Target address value to use.
        :param source_address: Source address value to use.

        :return: Value of CAN ID for Mixed 29-bit Addressing format that was generated from provided values.
        """
        AddressingType.validate_member(addressing_type)
        validate_raw_byte(target_address)
        validate_raw_byte(source_address)
        addressing_type_instance = AddressingType(addressing_type)
        if addressing_type_instance == AddressingType.PHYSICAL:
            return cls.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET + (target_address << 8) + source_address
        if addressing_type_instance == AddressingType.FUNCTIONAL:
            return cls.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET + (target_address << 8) + source_address
        raise NotImplementedError(f"Unknown addressing type value was provided: {addressing_type}")

    @classmethod
    def decode_normal_fixed_addressed_can_id(cls, can_id: int) -> NORMAL_FIXED_CAN_ID_INFO_TYPING:
        """
        Extract information out of CAN ID using Normal Fixed Addressing format.

        :param can_id: CAN ID from which data to be extracted.

        :raise ValueError: Provided CAN ID is not compatible with Normal Fixed Addressing format.

        :return: Tuple with [Addressing Type], [Target Address] and [Source Address] values decoded out of CAN ID.
        """
        cls.validate_can_id(can_id)
        if not cls.is_normal_fixed_addressed_can_id(can_id):
            raise ValueError(f"Provided CAN ID value is out of range. "
                             f"Expected CAN ID using Normal Fixed Addressing format. Actual value: {can_id}")
        target_address = (can_id >> 8) & 0xFF
        source_address = can_id & 0xFF
        can_id_offset = can_id & (~0xFFFF)  # value with Target Address and Source Address information erased
        if can_id_offset == cls.NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET:
            return AddressingType.PHYSICAL, target_address, source_address
        if can_id_offset == cls.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET:
            return AddressingType.FUNCTIONAL, target_address, source_address
        raise NotImplementedError("CAN ID in Normal Fixed Addressing format was provided, but cannot be handled."
                                  f"Actual value: {can_id}")

    @classmethod
    def decode_mixed_addressed_29bit_can_id(cls, can_id: int) -> MIXED_29BIT_CAN_ID_INFO_TYPING:
        """
        Extract information out of CAN ID using Normal Fixed Addressing format.

        :param can_id: CAN ID from which data to be extracted.

        :raise ValueError: Provided CAN ID is not compatible with Normal Fixed Addressing format.

        :return: Tuple with [Addressing Type], [Target Address] and [Source Address] values decoded out of CAN ID.
        """
        cls.validate_can_id(can_id)
        if not cls.is_mixed_addressed_29bit_can_id(can_id):
            raise ValueError(f"Provided CAN ID value is out of range. "
                             f"Expected 29-bit CAN ID using Mixed Addressing format. Actual value: {can_id}")
        target_address = (can_id >> 8) & 0xFF
        source_address = can_id & 0xFF
        can_id_offset = can_id & (~0xFFFF)  # value with Target Address and Source Address information erased
        if can_id_offset == cls.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET:
            return AddressingType.PHYSICAL, target_address, source_address
        if can_id_offset == cls.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET:
            return AddressingType.FUNCTIONAL, target_address, source_address
        raise NotImplementedError("CAN ID in Normal Fixed Addressing format was provided, but cannot be handled."
                                  f"Actual value: {can_id}")

    @classmethod
    def is_normal_fixed_addressed_can_id(cls, value: int) -> bool:
        """
        Check if provided value is CAN ID that uses Normal Fixed Addressing format.

        :param value: Value to check.

        :return: True if value is a valid CAN ID for Normal Fixed Addressing format, False otherwise.
        """
        if cls.NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET <= value <= cls.NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET + 0xFFFF:
            return True
        if cls.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET <= value \
                <= cls.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET + 0xFFFF:
            return True
        return False

    @classmethod
    def is_mixed_addressed_29bit_can_id(cls, value: int) -> bool:
        """
        Check if provided value is CAN ID that uses Mixed 29-bit Addressing format.

        :param value: Value to check.

        :return: True if value is a valid CAN ID for Normal Mixed 29-bit format, False otherwise.
        """
        if cls.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET <= value <= cls.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET + 0xFFFF:
            return True
        if cls.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET <= value \
                <= cls.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET + 0xFFFF:
            return True
        return False

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
        Validate if provided value is either Standard or Extended CAN ID.

        :param value: Value to validate.

        :raise TypeError: Provided value is not int type.
        :raise ValueError: Provided value is out of CAN Identifier values range.
        """
        if not isinstance(value, int):
            raise TypeError(f"Provided value is not int type. Actual type: {type(value)}")
        if not cls.is_can_id(value):
            raise ValueError(f"Provided value is out of CAN Identifier values range. Actual value: {value}")


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

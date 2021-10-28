"""
Implementation for CAN frame fields that are influenced by UDS.

Handlers for :ref:`CAN Frame <knowledge-base-can-frame>` fields:
 - CAN Identifier
 - DLC
 - Data
"""

__all__ = ["CanIdHandler"]

from typing import Any, Optional, Tuple

from uds.transmission_attributes import AddressingType, AddressingTypeMemberAlias
from uds.utilities import RawByte, validate_raw_byte
from .addressing_format import CanAddressingFormat, CanAddressingFormatAlias


DEFAULT_FILLER_BYTE: RawByte = 0xCC  # TODO: try to find a better place for it
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
    """Minimum value of Physical CAN ID (with Target Address and Source Address information erased) that is compatible
    with :ref:`Normal Fixed Addressing Format <knowledge-base-can-normal-fixed-addressing>.`"""
    NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET: int = 0x18DB0000
    """Minimum value of Functional CAN ID (with Target Address and Source Address information erased) that is compatible
    with :ref:`Normal Fixed Addressing Format <knowledge-base-can-normal-fixed-addressing>.`"""
    MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET: int = 0x18CE0000
    """Minimum value of Physical CAN ID (with Target Address and Source Address information erased) that is compatible
    with :ref:`Mixed 29-bit Addressing Format <knowledge-base-can-mixed-29-bit-addressing>.`"""
    MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET: int = 0x18CD0000
    """Minimum value of Functional CAN ID (with Target Address and Source Address information erased) that is compatible
    with :ref:`Mixed 29-bit Addressing Format <knowledge-base-can-mixed-29-bit-addressing>.`"""

    NORMAL_FIXED_CAN_ID_INFO_TYPING = Tuple[AddressingType, RawByte, RawByte]
    """Typing alias of information carried by CAN ID in Normal Fixed Addressing format."""
    MIXED_29BIT_CAN_ID_INFO_TYPING = Tuple[AddressingType, RawByte, RawByte]
    """Typing alias of information carried by CAN ID in Mixed 29-bit Addressing format."""

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

    @classmethod
    def is_can_id(cls, value: int) -> bool:
        """
        Check if provided value is either Standard (11-bit) or Extended (29-bit) CAN ID.

        :param value: Value to check.

        :return: True if value is a valid CAN ID, False otherwise.
        """
        return cls.is_standard_can_id(value) or cls.is_extended_can_id(value)

    @classmethod
    def is_standard_can_id(cls, can_id: int) -> bool:
        """
        Check if provided value is Standard (11-bit) CAN ID.

        :param can_id: Value to check.

        :return: True if value is a valid 11-bit CAN ID, False otherwise.
        """
        return isinstance(can_id, int) and cls.MIN_11BIT_VALUE <= can_id <= cls.MAX_11BIT_VALUE

    @classmethod
    def is_extended_can_id(cls, can_id: int) -> bool:
        """
        Check if provided value is Extended (29-bit) CAN ID.

        :param can_id: Value to check.

        :return: True if value is a valid 29-bit CAN ID, False otherwise.
        """
        return isinstance(can_id, int) and cls.MIN_29BIT_VALUE <= can_id <= cls.MAX_29BIT_VALUE

    @classmethod
    def is_compatible_can_id(cls,
                             can_id: int,
                             addressing_format: CanAddressingFormatAlias,
                             addressing: Optional[AddressingTypeMemberAlias] = None) -> bool:
        """
        Check if provided value of CAN ID is compatible with addressing format used.

        :param can_id: Value to check.
        :param addressing_format: Addressing format used.
        :param addressing: Addressing type for which consistency check to be performed.
            Leave None to not perform consistency check with Addressing Type.

        :raise NotImplementedError: A valid addressing format was provided, but the implementation for it is missing.
            Please raise an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            whenever you see this error.

        :return: True if CAN ID value is compatible with provided addressing format, False otherwise.
        """
        cls.validate_can_id(can_id)
        CanAddressingFormat.validate_member(addressing_format)
        if addressing_format == CanAddressingFormat.NORMAL_11BIT_ADDRESSING:
            return cls.is_normal_11bit_addressed_can_id(can_id=can_id)
        if addressing_format == CanAddressingFormat.NORMAL_FIXED_ADDRESSING:
            return cls.is_normal_fixed_addressed_can_id(can_id=can_id, addressing=addressing)
        if addressing_format == CanAddressingFormat.EXTENDED_ADDRESSING:
            return cls.is_extended_addressed_can_id(can_id=can_id)
        if addressing_format == CanAddressingFormat.MIXED_11BIT_ADDRESSING:
            return cls.is_mixed_11bit_addressed_can_id(can_id=can_id)
        if addressing_format == CanAddressingFormat.MIXED_29BIT_ADDRESSING:
            return cls.is_mixed_29bit_addressed_can_id(can_id=can_id, addressing=addressing)
        raise NotImplementedError(f"Missing implementation for: {addressing_format}")

    @classmethod
    def is_normal_11bit_addressed_can_id(cls, can_id: int) -> bool:
        """
        Check if provided value of CAN ID uses Normal 11-bit Addressing format.

        :param can_id: Value to check.

        :return: True if value is a valid CAN ID for Normal 11-bit Addressing format, False otherwise.
        """
        return cls.is_standard_can_id(can_id)

    @classmethod
    def is_normal_fixed_addressed_can_id(cls, can_id: int,
                                         addressing: Optional[AddressingTypeMemberAlias] = None) -> bool:
        """
        Check if provided value of CAN ID uses Normal Fixed Addressing format.

        :param can_id: Value to check.
        :param addressing: Addressing type for which consistency check to be performed.
            Leave None to not perform consistency check with Addressing Type.

        :return: True if value is a valid CAN ID for Normal Fixed Addressing format (consistent with provided
            addressing type), False otherwise.
        """
        if addressing is not None:
            AddressingType.validate_member(addressing)
        if (addressing is None or addressing == AddressingType.PHYSICAL) and \
                cls.NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET <= can_id \
                <= cls.NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET + 0xFFFF:
            return True
        if (addressing is None or addressing == AddressingType.FUNCTIONAL) and \
                cls.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET <= can_id \
                <= cls.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET + 0xFFFF:
            return True
        return False

    @classmethod
    def is_extended_addressed_can_id(cls, can_id: int) -> bool:
        """
        Check if provided value of CAN ID uses Extended Addressing format.

        :param can_id: Value to check.

        :return: True if value is a valid CAN ID for Extended Addressing format, False otherwise.
        """
        return cls.is_can_id(can_id)

    @classmethod
    def is_mixed_11bit_addressed_can_id(cls, can_id: int) -> bool:
        """
        Check if provided value of CAN ID uses Mixed 11-bit Addressing format.

        :param can_id: Value to check.

        :return: True if value is a valid CAN ID for Mixed 11-bit Addressing format, False otherwise.
        """
        return cls.is_standard_can_id(can_id)

    @classmethod
    def is_mixed_29bit_addressed_can_id(cls, can_id: int,
                                        addressing: Optional[AddressingTypeMemberAlias] = None) -> bool:
        """
        Check if provided value of CAN ID uses Mixed 29-bit Addressing format.

        :param can_id: Value to check.
        :param addressing: Addressing type for which consistency check to be performed.
            Leave None to not perform consistency check with Addressing Type.

        :return: True if value is a valid CAN ID for Normal Mixed 29-bit format, False otherwise.
        """
        if addressing is not None:
            AddressingType.validate_member(addressing)
        if (addressing is None or addressing == AddressingType.PHYSICAL) and \
                cls.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET <= can_id \
                <= cls.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET + 0xFFFF:
            return True
        if (addressing is None or addressing == AddressingType.FUNCTIONAL) and \
                cls.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET <= can_id \
                <= cls.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET + 0xFFFF:
            return True
        return False

    @classmethod
    def get_normal_fixed_addressed_can_id(cls,
                                          addressing_type: AddressingTypeMemberAlias,
                                          target_address: RawByte,
                                          source_address: RawByte) -> int:
        """
        Get CAN ID value for Normal Fixed Addressing format.

        :param addressing_type: Addressing type used.
        :param target_address: Target address value to use.
        :param source_address: Source address value to use.

        :raise NotImplementedError: A valid addressing type was provided, but the implementation for it is missing.
            Please raise an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            whenever you see this error.

        :return: Value of CAN ID for Normal Fixed Addressing format that was generated from provided values.
        """
        AddressingType.validate_member(addressing_type)
        validate_raw_byte(target_address)
        validate_raw_byte(source_address)
        if addressing_type == AddressingType.PHYSICAL:
            return cls.NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET + (target_address << 8) + source_address
        if addressing_type == AddressingType.FUNCTIONAL:
            return cls.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET + (target_address << 8) + source_address
        raise NotImplementedError(f"Unknown addressing type value was provided: {addressing_type}")

    @classmethod
    def get_mixed_addressed_29bit_can_id(cls,
                                         addressing_type: AddressingTypeMemberAlias,
                                         target_address: RawByte,
                                         source_address: RawByte) -> int:
        """
        Get CAN ID value for Mixed Addressing format that uses 29-bit CAN Identifiers.

        :param addressing_type: Addressing type used.
        :param target_address: Target address value to use.
        :param source_address: Source address value to use.

        :raise NotImplementedError: A valid addressing type was provided, but the implementation for it is missing.
            Please raise an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            whenever you see this error.

        :return: Value of CAN ID for Mixed 29-bit Addressing format that was generated from provided values.
        """
        AddressingType.validate_member(addressing_type)
        validate_raw_byte(target_address)
        validate_raw_byte(source_address)
        if addressing_type == AddressingType.PHYSICAL:
            return cls.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET + (target_address << 8) + source_address
        if addressing_type == AddressingType.FUNCTIONAL:
            return cls.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET + (target_address << 8) + source_address
        raise NotImplementedError(f"Unknown addressing type value was provided: {addressing_type}")

    @classmethod
    def decode_normal_fixed_addressed_can_id(cls, can_id: int) -> NORMAL_FIXED_CAN_ID_INFO_TYPING:
        """
        Extract information out of CAN ID using Normal Fixed Addressing format.

        :param can_id: CAN ID from which data to be extracted.

        :raise ValueError: Provided CAN ID is not compatible with Normal Fixed Addressing format.
        :raise NotImplementedError: A valid addressing type was provided, but the implementation for it is missing.
            Please raise an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            whenever you see this error.

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
            addressing_type = AddressingType(AddressingType.PHYSICAL)
            return addressing_type, target_address, source_address
        if can_id_offset == cls.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET:
            addressing_type = AddressingType(AddressingType.FUNCTIONAL)
            return addressing_type, target_address, source_address
        raise NotImplementedError("CAN ID in Normal Fixed Addressing format was provided, but cannot be handled."
                                  f"Actual value: {can_id}")

    @classmethod
    def decode_mixed_addressed_29bit_can_id(cls, can_id: int) -> MIXED_29BIT_CAN_ID_INFO_TYPING:
        """
        Extract information out of CAN ID using Normal Fixed Addressing format.

        :param can_id: CAN ID from which data to be extracted.

        :raise ValueError: Provided CAN ID is not compatible with Normal Fixed Addressing format.
        :raise NotImplementedError: A valid addressing type was provided, but the implementation for it is missing.
            Please raise an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            whenever you see this error.

        :return: Tuple with [Addressing Type], [Target Address] and [Source Address] values decoded out of CAN ID.
        """
        cls.validate_can_id(can_id)
        if not cls.is_mixed_29bit_addressed_can_id(can_id):
            raise ValueError(f"Provided CAN ID value is out of range. "
                             f"Expected 29-bit CAN ID using Mixed Addressing format. Actual value: {can_id}")
        target_address = (can_id >> 8) & 0xFF
        source_address = can_id & 0xFF
        can_id_offset = can_id & (~0xFFFF)  # value with Target Address and Source Address information erased
        if can_id_offset == cls.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET:
            addressing_type = AddressingType(AddressingType.PHYSICAL)
            return addressing_type, target_address, source_address
        if can_id_offset == cls.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET:
            addressing_type = AddressingType(AddressingType.FUNCTIONAL)
            return addressing_type, target_address, source_address
        raise NotImplementedError("CAN ID in Normal Fixed Addressing format was provided, but cannot be handled."
                                  f"Actual value: {can_id}")

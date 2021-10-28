"""
Definition of attributes that are specific for CAN packets.

This module contains implementation of :ref:`CAN packet <knowledge-base-uds-can-packet>` attributes that describe:
 - :ref:`CAN frame <knowledge-base-can-frame>`
 - :ref:`CAN packet addressing format <knowledge-base-can-addressing>`
 - :ref:`CAN packet data field <knowledge-base-can-data-field>`
 - :ref:`CAN packet type <knowledge-base-can-n-pci>`
"""

__all__ = ["CanAddressingFormat", "CanAddressingFormatTyping",
           "CanIdHandler", "CanDlcHandler", "DEFAULT_FILLER_BYTE"]

from typing import Optional, Union, Any, Tuple, Dict, Set
from bisect import bisect_left

from aenum import unique, StrEnum

from uds.utilities import RawByte, validate_raw_byte, ValidatedEnum
from uds.transmission_attributes import AddressingType, AddressingTypeMemberAlias
from .abstract_packet import AbstractUdsPacketType





# class CanIdHandler:
#     """
#     Helper class that provides utilities for CAN Identifier field.
#
#     CAN Identifier (CAN ID) is a CAN frame field that informs about a sender and a content of CAN frames.
#
#     CAN supports two formats of CAN ID:
#      - Standard (11-bit Identifier)
#      - Extended (29-bit Identifier)
#     """
#
#     MIN_11BIT_VALUE: int = 0
#     """Minimum value of 11-bit CAN ID."""
#     MAX_11BIT_VALUE: int = (1 << 11) - 1
#     """Maximum value of 11-bit CAN ID."""
#     MIN_29BIT_VALUE: int = MAX_11BIT_VALUE + 1
#     """Minimum value of 29-bit CAN ID."""
#     MAX_29BIT_VALUE: int = (1 << 29) - 1
#     """Maximum value of 29-bit CAN ID."""
#
#     NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET: int = 0x18DA0000
#     """Minimum value of Physical CAN ID (with Target Address and Source Address information erased) that is compatible
#     with :ref:`Normal Fixed Addressing Format <knowledge-base-can-normal-fixed-addressing>.`"""
#     NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET: int = 0x18DB0000
#     """Minimum value of Functional CAN ID (with Target Address and Source Address information erased) that is compatible
#     with :ref:`Normal Fixed Addressing Format <knowledge-base-can-normal-fixed-addressing>.`"""
#     MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET: int = 0x18CE0000
#     """Minimum value of Physical CAN ID (with Target Address and Source Address information erased) that is compatible
#     with :ref:`Mixed 29-bit Addressing Format <knowledge-base-can-mixed-29-bit-addressing>.`"""
#     MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET: int = 0x18CD0000
#     """Minimum value of Functional CAN ID (with Target Address and Source Address information erased) that is compatible
#     with :ref:`Mixed 29-bit Addressing Format <knowledge-base-can-mixed-29-bit-addressing>.`"""
#
#     NORMAL_FIXED_CAN_ID_INFO_TYPING = Tuple[AddressingType, RawByte, RawByte]
#     """Typing alias of information carried by CAN ID in Normal Fixed Addressing format."""
#     MIXED_29BIT_CAN_ID_INFO_TYPING = Tuple[AddressingType, RawByte, RawByte]
#     """Typing alias of information carried by CAN ID in Mixed 29-bit Addressing format."""
#
#     @classmethod
#     def get_normal_fixed_addressed_can_id(cls,
#                                           addressing_type: AddressingTypeMemberTyping,
#                                           target_address: RawByte,
#                                           source_address: RawByte) -> int:
#         """
#         Get CAN ID value for Normal Fixed Addressing format.
#
#         :param addressing_type: Addressing type used.
#         :param target_address: Target address value to use.
#         :param source_address: Source address value to use.
#
#         :return: Value of CAN ID for Normal Fixed Addressing format that was generated from provided values.
#         """
#         AddressingType.validate_member(addressing_type)
#         validate_raw_byte(target_address)
#         validate_raw_byte(source_address)
#         addressing_type_instance = AddressingType(addressing_type)
#         if addressing_type_instance == AddressingType.PHYSICAL:
#             return cls.NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET + (target_address << 8) + source_address
#         if addressing_type_instance == AddressingType.FUNCTIONAL:
#             return cls.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET + (target_address << 8) + source_address
#         raise NotImplementedError(f"Unknown addressing type value was provided: {addressing_type}")
#
#     @classmethod
#     def get_mixed_addressed_29bit_can_id(cls,
#                                          addressing_type: AddressingTypeMemberTyping,
#                                          target_address: RawByte,
#                                          source_address: RawByte) -> int:
#         """
#         Get CAN ID value for Mixed Addressing format that uses 29-bit CAN Identifiers.
#
#         :param addressing_type: Addressing type used.
#         :param target_address: Target address value to use.
#         :param source_address: Source address value to use.
#
#         :return: Value of CAN ID for Mixed 29-bit Addressing format that was generated from provided values.
#         """
#         AddressingType.validate_member(addressing_type)
#         validate_raw_byte(target_address)
#         validate_raw_byte(source_address)
#         addressing_type_instance = AddressingType(addressing_type)
#         if addressing_type_instance == AddressingType.PHYSICAL:
#             return cls.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET + (target_address << 8) + source_address
#         if addressing_type_instance == AddressingType.FUNCTIONAL:
#             return cls.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET + (target_address << 8) + source_address
#         raise NotImplementedError(f"Unknown addressing type value was provided: {addressing_type}")
#
#     @classmethod
#     def decode_normal_fixed_addressed_can_id(cls, can_id: int) -> NORMAL_FIXED_CAN_ID_INFO_TYPING:  # noqa
#         """
#         Extract information out of CAN ID using Normal Fixed Addressing format.
#
#         :param can_id: CAN ID from which data to be extracted.
#
#         :raise ValueError: Provided CAN ID is not compatible with Normal Fixed Addressing format.
#
#         :return: Tuple with [Addressing Type], [Target Address] and [Source Address] values decoded out of CAN ID.
#         """
#         cls.validate_can_id(can_id)
#         if not cls.is_normal_fixed_addressed_can_id(can_id):
#             raise ValueError(f"Provided CAN ID value is out of range. "
#                              f"Expected CAN ID using Normal Fixed Addressing format. Actual value: {can_id}")
#         target_address = (can_id >> 8) & 0xFF
#         source_address = can_id & 0xFF
#         can_id_offset = can_id & (~0xFFFF)  # value with Target Address and Source Address information erased
#         if can_id_offset == cls.NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET:
#             addressing_type = AddressingType(AddressingType.PHYSICAL)
#             return addressing_type, target_address, source_address
#         if can_id_offset == cls.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET:
#             addressing_type = AddressingType(AddressingType.FUNCTIONAL)
#             return addressing_type, target_address, source_address
#         raise NotImplementedError("CAN ID in Normal Fixed Addressing format was provided, but cannot be handled."
#                                   f"Actual value: {can_id}")
#
#     @classmethod
#     def decode_mixed_addressed_29bit_can_id(cls, can_id: int) -> MIXED_29BIT_CAN_ID_INFO_TYPING:  # noqa
#         """
#         Extract information out of CAN ID using Normal Fixed Addressing format.
#
#         :param can_id: CAN ID from which data to be extracted.
#
#         :raise ValueError: Provided CAN ID is not compatible with Normal Fixed Addressing format.
#
#         :return: Tuple with [Addressing Type], [Target Address] and [Source Address] values decoded out of CAN ID.
#         """
#         cls.validate_can_id(can_id)
#         if not cls.is_mixed_29bit_addressed_can_id(can_id):
#             raise ValueError(f"Provided CAN ID value is out of range. "
#                              f"Expected 29-bit CAN ID using Mixed Addressing format. Actual value: {can_id}")
#         target_address = (can_id >> 8) & 0xFF
#         source_address = can_id & 0xFF
#         can_id_offset = can_id & (~0xFFFF)  # value with Target Address and Source Address information erased
#         if can_id_offset == cls.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET:
#             addressing_type = AddressingType(AddressingType.PHYSICAL)
#             return addressing_type, target_address, source_address
#         if can_id_offset == cls.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET:
#             addressing_type = AddressingType(AddressingType.FUNCTIONAL)
#             return addressing_type, target_address, source_address
#         raise NotImplementedError("CAN ID in Normal Fixed Addressing format was provided, but cannot be handled."
#                                   f"Actual value: {can_id}")
#
#     @classmethod
#     def is_compatible_can_id(cls,
#                              can_id: int,
#                              addressing_format: CanAddressingFormatTyping,
#                              addressing: Optional[AddressingTypeMemberTyping] = None) -> bool:
#         """
#         Check if provided value of CAN ID is compatible with addressing format used.
#
#         :param can_id: Value to check.
#         :param addressing_format: Addressing format used.
#         :param addressing: Addressing type for which consistency check to be performed.
#             Leave None to not perform consistency check with Addressing Type.
#
#         :raise ValueError: Provided value is not a valid value of addressing_format.
#         :raise NotImplementedError: A valid addressing format was provided, but the implementation for it is missing.
#             Please raise an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
#             whenever you see this error.
#
#         :return: True if CAN ID value is compatible with provided addressing format, False otherwise.
#         """
#         cls.validate_can_id(can_id)
#         CanAddressingFormat.validate_member(addressing_format)
#         addressing_format_instance = CanAddressingFormat(addressing_format)
#         if addressing_format_instance == CanAddressingFormat.NORMAL_11BIT_ADDRESSING:
#             return cls.is_normal_11bit_addressed_can_id(can_id=can_id)
#         if addressing_format_instance == CanAddressingFormat.NORMAL_FIXED_ADDRESSING:
#             return cls.is_normal_fixed_addressed_can_id(can_id=can_id, addressing=addressing)
#         if addressing_format_instance == CanAddressingFormat.EXTENDED_ADDRESSING:
#             return cls.is_extended_addressed_can_id(can_id=can_id)
#         if addressing_format_instance == CanAddressingFormat.MIXED_11BIT_ADDRESSING:
#             return cls.is_mixed_11bit_addressed_can_id(can_id=can_id)
#         if addressing_format_instance == CanAddressingFormat.MIXED_29BIT_ADDRESSING:
#             return cls.is_mixed_29bit_addressed_can_id(can_id=can_id, addressing=addressing)
#         raise NotImplementedError(f"Missing implementation for: {addressing_format_instance}")
#
#     @classmethod
#     def is_normal_11bit_addressed_can_id(cls, can_id: int) -> bool:
#         """
#         Check if provided value of CAN ID uses Normal 11-bit Addressing format.
#
#         :param can_id: Value to check.
#
#         :return: True if value is a valid CAN ID for Normal 11-bit Addressing format, False otherwise.
#         """
#         return cls.is_standard_can_id(can_id)
#
#     @classmethod
#     def is_normal_fixed_addressed_can_id(cls, can_id: int,
#                                          addressing: Optional[AddressingTypeMemberTyping] = None) -> bool:
#         """
#         Check if provided value of CAN ID uses Normal Fixed Addressing format.
#
#         :param can_id: Value to check.
#         :param addressing: Addressing type for which consistency check to be performed.
#             Leave None to not perform consistency check with Addressing Type.
#
#         :return: True if value is a valid CAN ID for Normal Fixed Addressing format (consistent with provided
#             addressing type), False otherwise.
#         """
#         if addressing is None:
#             addressing_instance = None
#         else:
#             AddressingType.validate_member(addressing)
#             addressing_instance = AddressingType(addressing)
#         if addressing_instance in (None, AddressingType.PHYSICAL) and \
#                 cls.NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET <= can_id \
#                 <= cls.NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET + 0xFFFF:
#             return True
#         if addressing_instance in (None, AddressingType.FUNCTIONAL) and \
#                 cls.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET <= can_id \
#                 <= cls.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET + 0xFFFF:
#             return True
#         return False
#
#     @classmethod
#     def is_extended_addressed_can_id(cls, can_id: int) -> bool:
#         """
#         Check if provided value of CAN ID uses Extended Addressing format.
#
#         :param can_id: Value to check.
#
#         :return: True if value is a valid CAN ID for Extended Addressing format, False otherwise.
#         """
#         return cls.is_can_id(can_id)
#
#     @classmethod
#     def is_mixed_11bit_addressed_can_id(cls, can_id: int) -> bool:
#         """
#         Check if provided value of CAN ID uses Mixed 11-bit Addressing format.
#
#         :param can_id: Value to check.
#
#         :return: True if value is a valid CAN ID for Mixed 11-bit Addressing format, False otherwise.
#         """
#         return cls.is_standard_can_id(can_id)
#
#     @classmethod
#     def is_mixed_29bit_addressed_can_id(cls, can_id: int,
#                                         addressing: Optional[AddressingTypeMemberTyping] = None) -> bool:
#         """
#         Check if provided value of CAN ID uses Mixed 29-bit Addressing format.
#
#         :param can_id: Value to check.
#         :param addressing: Addressing type for which consistency check to be performed.
#             Leave None to not perform consistency check with Addressing Type.
#
#         :return: True if value is a valid CAN ID for Normal Mixed 29-bit format, False otherwise.
#         """
#         if addressing is None:
#             addressing_instance = None
#         else:
#             AddressingType.validate_member(addressing)
#             addressing_instance = AddressingType(addressing)
#         if addressing_instance in (None, AddressingType.PHYSICAL) and \
#                 cls.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET <= can_id \
#                 <= cls.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET + 0xFFFF:
#             return True
#         if addressing_instance in (None, AddressingType.FUNCTIONAL) and \
#                 cls.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET <= can_id \
#                 <= cls.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET + 0xFFFF:
#             return True
#         return False
#
#     @classmethod
#     def is_standard_can_id(cls, can_id: int) -> bool:
#         """
#         Check if provided value is Standard (11-bit) CAN ID.
#
#         :param can_id: Value to check.
#
#         :return: True if value is a valid 11-bit CAN ID, False otherwise.
#         """
#         return cls.MIN_11BIT_VALUE <= can_id <= cls.MAX_11BIT_VALUE
#
#     @classmethod
#     def is_extended_can_id(cls, can_id: int) -> bool:
#         """
#         Check if provided value is Extended (29-bit) CAN ID.
#
#         :param can_id: Value to check.
#
#         :return: True if value is a valid 29-bit CAN ID, False otherwise.
#         """
#         return cls.MIN_29BIT_VALUE <= can_id <= cls.MAX_29BIT_VALUE
#
#     @classmethod
#     def is_can_id(cls, value: int) -> bool:
#         """
#         Check if provided value is either Standard (11-bit) or Extended (29-bit) CAN ID.
#
#         :param value: Value to check.
#
#         :return: True if value is a valid CAN ID, False otherwise.
#         """
#         return cls.is_standard_can_id(value) or cls.is_extended_can_id(value)
#
#     @classmethod
#     def validate_can_id(cls, value: Any) -> None:
#         """
#         Validate if provided value is either Standard or Extended CAN ID.
#
#         :param value: Value to validate.
#
#         :raise TypeError: Provided value is not int type.
#         :raise ValueError: Provided value is out of CAN Identifier values range.
#         """
#         if not isinstance(value, int):
#             raise TypeError(f"Provided value is not int type. Actual type: {type(value)}")
#         if not cls.is_can_id(value):
#             raise ValueError(f"Provided value is out of CAN Identifier values range. Actual value: {value}")


class CanDlcHandler:
    """
    Helper class that provides utilities for CAN Data Length Code field.

    CAN Data Length Code (CAN DLC) is a CAN frame field that informs about number of data bytes carried in CAN frames.

    CAN DLC supports two value ranges:
     - 0x0-0x8 - supported by CLASSICAL CAN and CAN FD
     - 0x9-0xF - supported by CAN FD only
    """

    __DLC_VALUES: Tuple[int, ...] = tuple(range(0x10))
    __DATA_BYTES_NUMBERS: Tuple[int, ...] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 16, 20, 24, 32, 48, 64)
    __DLC_MAPPING: Dict[int, int] = dict(zip(__DLC_VALUES, __DATA_BYTES_NUMBERS))
    __DATA_BYTES_NUMBER_MAPPING: Dict[int, int] = dict(zip(__DATA_BYTES_NUMBERS, __DLC_VALUES))
    __DLC_SPECIFIC_FOR_CAN_FD: Set[int] = set(__DLC_VALUES[9:])

    MIN_DATA_BYTES_NUMBER: int = min(__DATA_BYTES_NUMBERS)
    """Minimum number of data bytes in a CAN frame."""
    MAX_DATA_BYTES_NUMBER: int = max(__DATA_BYTES_NUMBERS)
    """Maximum number of data bytes in a CAN frame."""
    MIN_DLC_VALUE: int = min(__DLC_VALUES)
    """Minimum value of a CAN Frame DLC parameter."""
    MAX_DLC_VALUE: int = max(__DLC_VALUES)
    """Maximum value of a CAN Frame DLC parameter."""

    @classmethod
    def decode(cls, dlc: int) -> int:
        """
        Map raw value of CAN DLC into number of data bytes.

        :param dlc: Raw value of CAN DLC.

        :return: Number of data bytes in a CAN frame that is represented by provided DLC value.
        """
        cls.validate_dlc(dlc)
        return cls.__DLC_MAPPING[dlc]

    @classmethod
    def encode(cls, data_bytes_number: int) -> int:
        """
        Map number of data bytes in a CAN frame into DLC value.

        :param data_bytes_number: Number of data bytes in a CAN frame.

        :return: DLC value of a CAN frame that represents provided number of data bytes.
        """
        cls.validate_data_bytes_number(data_bytes_number, True)
        return cls.__DATA_BYTES_NUMBER_MAPPING[data_bytes_number]

    @classmethod
    def get_min_dlc(cls, data_bytes_number: int) -> int:
        """
        Get minimum value of CAN DLC that enables carrying provided number of CAN data bytes.

        :param data_bytes_number: Number of payload data bytes in a CAN frame.

        :return: Minimum CAN DLC value that enables carrying provided number of CAN data bytes.
        """
        cls.validate_data_bytes_number(data_bytes_number, False)
        index = bisect_left(a=cls.__DATA_BYTES_NUMBERS, x=data_bytes_number)
        return cls.__DLC_VALUES[index]

    @classmethod
    def is_can_fd_specific_dlc(cls, dlc: int) -> bool:
        """
        Check whether provided DLC value is applicable for CAN FD only.

        :param dlc: Value of DLC to check.

        :return: True if provided DLC value is CAN FD specific, False otherwise.
        """
        return dlc in cls.__DLC_SPECIFIC_FOR_CAN_FD

    @classmethod
    def validate_dlc(cls, value: Any) -> None:
        """
        Validate whether provided value is a valid CAN DLC value.

        :param value: Value to validate.

        :raise TypeError: Provided values is not int type.
        :raise ValueError: Provided value is not a valid DLC value.
        """
        if not isinstance(value, int):
            raise TypeError(f"Provided value is not int type. Actual type: {type(value)}")
        if cls.__DLC_MAPPING.get(value, None) is None:
            raise ValueError(f"Provided value is out of DLC values range. Actual value: {value}")

    @classmethod
    def validate_data_bytes_number(cls, value: Any, exact_value: bool = True) -> None:
        """
        Validate whether provided value is a valid number of data bytes that might be carried a CAN frame.

        :param value: Value to validate.
        :param exact_value: Informs whether the value must be the exact number of CAN frame data bytes or number.
            - True - provided value must be the exact number of data bytes that might be carried by a CAN frame
            - False - provided value must be a number of data bytes that in range of minimum and maximum data bytes
              that CAN frame contain

        :raise TypeError: Provided values is not int type.
        :raise ValueError: Provided value is not number of data bytes that matches the criteria.
        """
        if not isinstance(value, int):
            raise TypeError(f"Provided value is not int type. Actual type: {type(value)}")
        if exact_value:
            if cls.__DATA_BYTES_NUMBER_MAPPING.get(value, None) is None:
                raise ValueError(f"Provided value is not a valid CAN Frame data bytes number. Actual value: {value}")
        else:
            if not cls.MIN_DATA_BYTES_NUMBER <= value <= cls.MAX_DATA_BYTES_NUMBER:
                raise ValueError(f"Provided value is out of CAN Frame data bytes number range. Actual value: {value}")





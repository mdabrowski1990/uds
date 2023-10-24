"""
Implementation for CAN frame fields that are influenced by UDS.

Handlers for :ref:`CAN Frame <knowledge-base-can-frame>` fields:
 - CAN Identifier
 - DLC
 - Data
"""

__all__ = ["CanIdHandler", "CanDlcHandler", "DEFAULT_FILLER_BYTE"]

from typing import Optional, Tuple, Set, TypedDict, Dict
from bisect import bisect_left

from uds.transmission_attributes import AddressingType
from uds.utilities import validate_raw_byte
from .addressing_format import CanAddressingFormat


DEFAULT_FILLER_BYTE: int = 0xCC
"""Default value of Filler Byte.
Filler Bytes are used for :ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>`.
.. note:: The value is specified by ISO 15765-2:2016 (chapter 10.4.2.1)."""


class CanIdHandler:
    """
    Helper class that provides utilities for CAN Identifier field.

    CAN Identifier (CAN ID) is a CAN frame field that informs about a sender and a content of CAN frames.

    CAN bus supports two formats of CAN ID:
     - Standard (11-bit Identifier)
     - Extended (29-bit Identifier)
    """

    MIN_STANDARD_VALUE: int = 0
    """Minimum value of Standard (11-bit) CAN ID."""
    MAX_STANDARD_VALUE: int = (1 << 11) - 1
    """Maximum value of Standard (11-bit) CAN ID."""
    MIN_EXTENDED_VALUE: int = MAX_STANDARD_VALUE + 1
    """Minimum value of Extended (29-bit) CAN ID."""
    MAX_EXTENDED_VALUE: int = (1 << 29) - 1
    """Maximum value of Extended (29-bit) CAN ID."""

    NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET: int = 0x18DA0000
    """Minimum value of physically addressed CAN ID in Normal Fixed Addressing format."""
    NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET: int = 0x18DB0000
    """Minimum value of functionally addressed CAN ID in Normal Fixed Addressing format."""
    MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET: int = 0x18CE0000
    """Minimum value of physically addressed CAN ID in Mixed 29-bit Addressing format."""
    MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET: int = 0x18CD0000
    """Minimum value of functionally addressed CAN ID in Mixed 29-bit Addressing format."""

    ADDRESSING_TYPE_NAME: str = "addressing_type"
    """Name of :ref:`Addressing Type <knowledge-base-can-addressing>` parameter in Addressing Information."""
    TARGET_ADDRESS_NAME: str = "target_address"
    """Name of Target Address parameter in Addressing Information."""
    SOURCE_ADDRESS_NAME: str = "source_address"
    """Name of Source Address parameter in Addressing Information."""

    class CanIdAIAlias(TypedDict, total=True):
        """Alias of :ref:`Addressing Information <knowledge-base-n-ai>` that is carried by CAN Identifier."""

        addressing_type: Optional[AddressingType]
        target_address: Optional[int]
        source_address: Optional[int]

    @classmethod
    def decode_can_id(cls, addressing_format: CanAddressingFormat, can_id: int) -> CanIdAIAlias:
        """
        Extract Addressing Information out of CAN ID.

        .. warning:: This methods might not extract any Addressing Information from the provided CAN ID as some of these
            information are system specific.

            For example, Addressing Type (even though it always depends on CAN ID value) will not be decoded when
            either Normal 11bit, Extended or Mixed 11bit addressing format is used as the Addressing Type (in such case)
            depends on system specific behaviour.

        :param addressing_format: Addressing format used.
        :param can_id: CAN ID from which Addressing Information to be extracted.

        :raise NotImplementedError: There is missing implementation for the provided Addressing Format.
            Please create an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            with detailed description if you face this error.

        :return: Dictionary with Addressing Information decoded out of the provided CAN ID.
        """
        CanAddressingFormat.validate_member(addressing_format)
        if addressing_format == CanAddressingFormat.NORMAL_FIXED_ADDRESSING:
            return cls.decode_normal_fixed_addressed_can_id(can_id)
        if addressing_format == CanAddressingFormat.MIXED_29BIT_ADDRESSING:
            return cls.decode_mixed_addressed_29bit_can_id(can_id)
        if addressing_format in (CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                 CanAddressingFormat.EXTENDED_ADDRESSING,
                                 CanAddressingFormat.MIXED_11BIT_ADDRESSING):
            return cls.CanIdAIAlias(addressing_type=None,
                                    target_address=None,
                                    source_address=None)  # no addressing information can be decoded
        raise NotImplementedError(f"Unknown addressing format value was provided: {addressing_format}")

    @classmethod
    def decode_normal_fixed_addressed_can_id(cls, can_id: int) -> CanIdAIAlias:
        """
        Extract Addressing Information out of CAN ID for Normal Fixed CAN Addressing format.

        :param can_id: CAN ID from which Addressing Information to be extracted.

        :raise ValueError: Provided CAN ID is not compatible with Normal Fixed Addressing format.
        :raise NotImplementedError: There is missing implementation for the provided CAN ID.
            Please create an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            with detailed description if you face this error.

        :return: Dictionary with Addressing Information decoded out of the provided CAN ID.
        """
        cls.validate_can_id(can_id)
        if not cls.is_normal_fixed_addressed_can_id(can_id):
            raise ValueError(f"Provided CAN ID value is out of range. "
                             f"Expected CAN ID using Normal Fixed Addressing format. Actual value: {can_id}")
        target_address = (can_id >> 8) & 0xFF
        source_address = can_id & 0xFF
        can_id_offset = can_id & (~0xFFFF)  # value with Target Address and Source Address information erased
        if can_id_offset == cls.NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET:
            return cls.CanIdAIAlias(addressing_type=AddressingType.PHYSICAL,
                                    target_address=target_address,
                                    source_address=source_address)
        if can_id_offset == cls.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET:
            return cls.CanIdAIAlias(addressing_type=AddressingType.FUNCTIONAL,
                                    target_address=target_address,
                                    source_address=source_address)
        raise NotImplementedError("CAN ID in Normal Fixed Addressing format was provided, but cannot be handled."
                                  f"Actual value: {can_id}")

    @classmethod
    def decode_mixed_addressed_29bit_can_id(cls, can_id: int) -> CanIdAIAlias:
        """
        Extract Addressing Information out of CAN ID for Mixed 29-bit CAN Addressing format.

        :param can_id: CAN ID from which Addressing Information to be extracted.

        :raise ValueError: Provided CAN ID is not compatible with Mixed 29-bit Addressing format.
        :raise NotImplementedError: There is missing implementation for the provided CAN ID.
            Please create an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            with detailed description if you face this error.

        :return: Dictionary with Addressing Information decoded out of the provided CAN ID.
        """
        cls.validate_can_id(can_id)
        if not cls.is_mixed_29bit_addressed_can_id(can_id):
            raise ValueError(f"Provided CAN ID value is out of range. "
                             f"Expected 29-bit CAN ID using Mixed Addressing format. Actual value: {can_id}")
        target_address = (can_id >> 8) & 0xFF
        source_address = can_id & 0xFF
        can_id_offset = can_id & (~0xFFFF)  # value with Target Address and Source Address information erased
        if can_id_offset == cls.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET:
            return cls.CanIdAIAlias(addressing_type=AddressingType.PHYSICAL,
                                    target_address=target_address,
                                    source_address=source_address)
        if can_id_offset == cls.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET:
            return cls.CanIdAIAlias(addressing_type=AddressingType.FUNCTIONAL,
                                    target_address=target_address,
                                    source_address=source_address)
        raise NotImplementedError("CAN ID in Normal Fixed Addressing format was provided, but cannot be handled."
                                  f"Actual value: {can_id}")

    @classmethod
    def encode_normal_fixed_addressed_can_id(cls,
                                             addressing_type: AddressingType,
                                             target_address: int,
                                             source_address: int) -> int:
        """
        Generate CAN ID value for Normal Fixed CAN Addressing format.

        :param addressing_type: Addressing type used.
        :param target_address: Target address value to use.
        :param source_address: Source address value to use.

        :raise NotImplementedError: There is missing implementation for the provided Addressing Type.
            Please create an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            with detailed description if you face this error.

        :return: Value of CAN ID (compatible with Normal Fixed Addressing Format) that was generated from
            the provided values.
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
    def encode_mixed_addressed_29bit_can_id(cls,
                                            addressing_type: AddressingType,
                                            target_address: int,
                                            source_address: int) -> int:
        """
        Generate CAN ID value for Mixed 29-bit CAN Addressing format.

        :param addressing_type: Addressing type used.
        :param target_address: Target address value to use.
        :param source_address: Source address value to use.

        :raise NotImplementedError: There is missing implementation for the provided Addressing Type.
            Please create an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            with detailed description if you face this error.

        :return: Value of CAN ID (compatible with Mixed 29-bit Addressing Format) that was generated from
            the provided values.
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
    def is_compatible_can_id(cls,
                             can_id: int,
                             addressing_format: CanAddressingFormat,
                             addressing_type: Optional[AddressingType] = None) -> bool:
        """
        Check if the provided value of CAN ID is compatible with addressing format used.

        :param can_id: Value to check.
        :param addressing_format: Addressing format used.
        :param addressing_type: Addressing type for which consistency check to be performed.
            Leave None to not perform consistency check with Addressing Type.

        :raise NotImplementedError: There is missing implementation for the provided Addressing Format.
            Please create an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            with detailed description if you face this error.

        :return: True if CAN ID value is compatible with provided addressing values, False otherwise.
        """
        cls.validate_can_id(can_id)
        CanAddressingFormat.validate_member(addressing_format)
        if addressing_format == CanAddressingFormat.NORMAL_11BIT_ADDRESSING:
            return cls.is_normal_11bit_addressed_can_id(can_id=can_id)
        if addressing_format == CanAddressingFormat.NORMAL_FIXED_ADDRESSING:
            return cls.is_normal_fixed_addressed_can_id(can_id=can_id, addressing_type=addressing_type)
        if addressing_format == CanAddressingFormat.EXTENDED_ADDRESSING:
            return cls.is_extended_addressed_can_id(can_id=can_id)
        if addressing_format == CanAddressingFormat.MIXED_11BIT_ADDRESSING:
            return cls.is_mixed_11bit_addressed_can_id(can_id=can_id)
        if addressing_format == CanAddressingFormat.MIXED_29BIT_ADDRESSING:
            return cls.is_mixed_29bit_addressed_can_id(can_id=can_id, addressing_type=addressing_type)
        raise NotImplementedError(f"Missing implementation for: {addressing_format}")

    @classmethod
    def is_normal_11bit_addressed_can_id(cls, can_id: int) -> bool:
        """
        Check if the provided value of CAN ID is compatible with Normal 11-bit Addressing format.

        :param can_id: Value to check.

        :return: True if value is a valid CAN ID for Normal 11-bit Addressing format, False otherwise.
        """
        return cls.is_standard_can_id(can_id)

    @classmethod
    def is_normal_fixed_addressed_can_id(cls,
                                         can_id: int,
                                         addressing_type: Optional[AddressingType] = None) -> bool:
        """
        Check if the provided value of CAN ID is compatible with Normal Fixed Addressing format.

        :param can_id: Value to check.
        :param addressing_type: Addressing type for which consistency check to be performed.
            Leave None to not perform consistency check with Addressing Type.

        :return: True if value is a valid CAN ID for Normal Fixed Addressing format and consistent with the provided
            Addressing Type, False otherwise.
        """
        if addressing_type is not None:
            AddressingType.validate_member(addressing_type)
        if (addressing_type is None or addressing_type == AddressingType.PHYSICAL) \
                and cls.NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET <= can_id \
                <= cls.NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET + 0xFFFF:
            return True
        if (addressing_type is None or addressing_type == AddressingType.FUNCTIONAL) \
                and cls.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET <= can_id \
                <= cls.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET + 0xFFFF:
            return True
        return False

    @classmethod
    def is_extended_addressed_can_id(cls, can_id: int) -> bool:
        """
        Check if the provided value of CAN ID is compatible with Extended Addressing format.

        :param can_id: Value to check.

        :return: True if value is a valid CAN ID for Extended Addressing format, False otherwise.
        """
        return cls.is_can_id(can_id)

    @classmethod
    def is_mixed_11bit_addressed_can_id(cls, can_id: int) -> bool:
        """
        Check if the provided value of CAN ID is compatible with Mixed 11-bit Addressing format.

        :param can_id: Value to check.

        :return: True if value is a valid CAN ID for Mixed 11-bit Addressing format, False otherwise.
        """
        return cls.is_standard_can_id(can_id)

    @classmethod
    def is_mixed_29bit_addressed_can_id(cls,
                                        can_id: int,
                                        addressing_type: Optional[AddressingType] = None) -> bool:
        """
        Check if the provided value of CAN ID is compatible with Mixed 29-bit Addressing format.

        :param can_id: Value to check.
        :param addressing_type: Addressing type for which consistency check to be performed.
            Leave None to not perform consistency check with Addressing Type.

        :return: True if value is a valid CAN ID for Mixed 29-bit Addressing format and consistent with the provided
            Addressing Type, False otherwise.
        """
        if addressing_type is not None:
            AddressingType.validate_member(addressing_type)
        if (addressing_type is None or addressing_type == AddressingType.PHYSICAL) \
                and cls.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET <= can_id \
                <= cls.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET + 0xFFFF:
            return True
        if (addressing_type is None or addressing_type == AddressingType.FUNCTIONAL) \
                and cls.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET <= can_id \
                <= cls.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET + 0xFFFF:
            return True
        return False

    @classmethod
    def is_can_id(cls, value: int) -> bool:
        """
        Check if the provided value is either Standard (11-bit) or Extended (29-bit) CAN ID.

        :param value: Value to check.

        :return: True if value is a valid CAN ID, False otherwise.
        """
        return cls.is_standard_can_id(value) or cls.is_extended_can_id(value)

    @classmethod
    def is_standard_can_id(cls, can_id: int) -> bool:
        """
        Check if the provided value is Standard (11-bit) CAN ID.

        :param can_id: Value to check.

        :return: True if value is a valid 11-bit CAN ID, False otherwise.
        """
        return isinstance(can_id, int) and cls.MIN_STANDARD_VALUE <= can_id <= cls.MAX_STANDARD_VALUE

    @classmethod
    def is_extended_can_id(cls, can_id: int) -> bool:
        """
        Check if the provided value is Extended (29-bit) CAN ID.

        :param can_id: Value to check.

        :return: True if value is a valid 29-bit CAN ID, False otherwise.
        """
        return isinstance(can_id, int) and cls.MIN_EXTENDED_VALUE <= can_id <= cls.MAX_EXTENDED_VALUE

    @classmethod
    def validate_can_id(cls, value: int, extended_can_id: Optional[bool] = None) -> None:
        """
        Validate whether provided value is either Standard or Extended CAN ID.

        :param value: Value to validate.
        :param extended_can_id: Flag whether to perform consistency check with CAN ID format.

            - None - does not check the format of the value
            - True - verify that the value uses Extended (29-bit) CAN ID format
            - False - verify that the value uses Standard (11-bit) CAN ID format

        :raise TypeError: Provided value is not int type.
        :raise ValueError: Provided value is out of CAN Identifier values range.
        """
        if not isinstance(value, int):
            raise TypeError(f"Provided value is not int type. Actual type: {type(value)}")
        if extended_can_id is None:
            if not cls.is_can_id(value):
                raise ValueError(f"Provided value is out of CAN Identifier values range. Actual value: {value}")
        elif extended_can_id:
            if not cls.is_extended_can_id(value):
                raise ValueError(f"Provided value is out of Extended (29-bit) CAN Identifier values range. "
                                 f"Actual value: {value}")
        else:
            if not cls.is_standard_can_id(value):
                raise ValueError(f"Provided value is out of Standard (11-bit) CAN Identifier values range. "
                                 f"Actual value: {value}")


class CanDlcHandler:
    """
    Helper class that provides utilities for CAN Data Length Code field.

    CAN Data Length Code (DLC) is a CAN frame field that informs about number of data bytes carried by CAN frames.

    CAN DLC supports two values ranges:
     - 0x0-0x8 - linear range which is supported by CLASSICAL CAN and CAN FD
     - 0x9-0xF - discrete range which is supported by CAN FD only
    """

    __DLC_VALUES: Tuple[int, ...] = tuple(range(0x10))
    __DATA_BYTES_NUMBERS: Tuple[int, ...] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 16, 20, 24, 32, 48, 64)
    __DLC_MAPPING: Dict[int, int] = dict(zip(__DLC_VALUES, __DATA_BYTES_NUMBERS))
    __DATA_BYTES_NUMBER_MAPPING: Dict[int, int] = dict(zip(__DATA_BYTES_NUMBERS, __DLC_VALUES))
    __DLC_SPECIFIC_FOR_CAN_FD: Set[int] = set(dlc for dlc in __DLC_VALUES if dlc > 8)

    MIN_DATA_BYTES_NUMBER: int = min(__DATA_BYTES_NUMBERS)
    """Minimum number of data bytes in a CAN frame."""
    MAX_DATA_BYTES_NUMBER: int = max(__DATA_BYTES_NUMBERS)
    """Maximum number of data bytes in a CAN frame."""
    MIN_DLC_VALUE: int = min(__DLC_VALUES)
    """Minimum value of DLC parameter."""
    MAX_DLC_VALUE: int = max(__DLC_VALUES)
    """Maximum value of DLC parameter."""

    MIN_BASE_UDS_DLC: int = 8
    """Minimum CAN DLC value that can be used for UDS communication.
    Lower values of DLC are only allowed when :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>`
    is used."""

    @classmethod
    def decode_dlc(cls, dlc: int) -> int:
        """
        Map a value of CAN DLC into a number of data bytes.

        :param dlc: Value of CAN DLC.

        :return: Number of data bytes in a CAN frame that is represented by provided DLC value.
        """
        cls.validate_dlc(dlc)
        return cls.__DLC_MAPPING[dlc]

    @classmethod
    def encode_dlc(cls, data_bytes_number: int) -> int:
        """
        Map a number of data bytes in a CAN frame into DLC value.

        :param data_bytes_number: Number of data bytes in a CAN frame.

        :return: DLC value of a CAN frame that represents provided number of data bytes.
        """
        cls.validate_data_bytes_number(data_bytes_number, True)
        return cls.__DATA_BYTES_NUMBER_MAPPING[data_bytes_number]

    @classmethod
    def get_min_dlc(cls, data_bytes_number: int) -> int:
        """
        Get a minimum value of CAN DLC that is required to carry the provided number of data bytes in a CAN frame.

        :param data_bytes_number: Number of data bytes in a CAN frame.

        :return: Minimum CAN DLC value that is required to carry provided number of data bytes in a CAN frame.
        """
        cls.validate_data_bytes_number(data_bytes_number, False)
        index = bisect_left(a=cls.__DATA_BYTES_NUMBERS, x=data_bytes_number)
        return cls.__DLC_VALUES[index]

    @classmethod
    def is_can_fd_specific_dlc(cls, dlc: int) -> bool:
        """
        Check whether the provided DLC value is CAN FD specific.

        :param dlc: Value of DLC to check.

        :return: True if provided DLC value is CAN FD specific, False otherwise.
        """
        return dlc in cls.__DLC_SPECIFIC_FOR_CAN_FD

    @classmethod
    def validate_dlc(cls, value: int) -> None:
        """
        Validate whether the provided value is a valid value of CAN DLC.

        :param value: Value to validate.

        :raise TypeError: Provided values is not int type.
        :raise ValueError: Provided value is not a valid DLC value.
        """
        if not isinstance(value, int):
            raise TypeError(f"Provided value is not int type. Actual type: {type(value)}")
        if not cls.MIN_DLC_VALUE <= value <= cls.MAX_DLC_VALUE:
            raise ValueError(f"Provided value is out of DLC values range. Actual value: {value}")

    @classmethod
    def validate_data_bytes_number(cls, value: int, exact_value: bool = True) -> None:
        """
        Validate whether provided value is a valid number of data bytes that might be carried a CAN frame.

        :param value: Value to validate.
        :param exact_value: Informs whether the value must be the exact number of data bytes in a CAN frame.

            - True - provided value must be the exact number of data bytes to be carried by a CAN frame.
            - False - provided value must be a number of data bytes that could be carried by a CAN frame
              (:ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>` is allowed).

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

"""
Implementation for CAN frame fields that are influenced by UDS.

Handlers for :ref:`CAN Frame <knowledge-base-can-frame>` fields:
 - CAN Identifier
 - DLC
 - Data
"""

__all__ = ["CanVersion", "CanIdHandler", "CanDlcHandler", "DEFAULT_FILLER_BYTE"]

from bisect import bisect_left
from typing import Dict, Optional, Set, Tuple

from uds.utilities import ValidatedEnum

DEFAULT_FILLER_BYTE: int = 0xCC
"""Default value of Filler Byte.
Filler Bytes are used for :ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>`.
.. note:: The value is specified by ISO 15765-2:2016 (chapter 10.4.2.1)."""


class CanVersion(ValidatedEnum):
    """:ref:`Versions of CAN bus <knowledge-base-can-versions>`."""

    CLASSIC_CAN: "CanVersion" = "Classic CAN"  # type: ignore
    """Classic CAN 2.0"""
    CAN_FD: "CanVersion" = "CAN FD"  # type: ignore
    """`CAN FD <https://en.wikipedia.org/wiki/CAN_FD>`_"""


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

    ADDRESSING_MASK: int = 0x3ff0000
    """CAN ID mask for bits enforced by SAE J1939 (Normal Fixed of Mixed 29bit addressing formats)."""
    NORMAL_FIXED_PHYSICAL_ADDRESSING_MASKED_VALUE: int = 0xDA0000
    """Masked value of physically addressed CAN ID in Normal Fixed Addressing format."""
    NORMAL_FIXED_FUNCTIONAL_ADDRESSING_MASKED_VALUE: int = 0xDB0000
    """Masked value of functionally addressed CAN ID in Normal Fixed Addressing format."""
    MIXED_29BIT_PHYSICAL_ADDRESSING_MASKED_VALUE: int = 0xCE0000
    """Masked value of physically addressed CAN ID in Mixed 29-bit Addressing format."""
    MIXED_29BIT_FUNCTIONAL_ADDRESSING_MASKED_VALUE: int = 0xCD0000
    """Masked value of functionally addressed CAN ID in Mixed 29-bit Addressing format."""
    TARGET_ADDRESS_BIT_OFFSET: int = 8
    """Bit offset of Target Address parameter in CAN Identifier."""
    SOURCE_ADDRESS_BIT_OFFSET: int = 0
    """Bit offset of Source Address parameter."""
    PRIORITY_BIT_OFFSET: int = 26
    """Bit offset of Priority parameter defined by SAE J1939."""
    DEFAULT_PRIORITY_VALUE: int = 0b110
    """Default value of Priority parameter defined by SAE J1939."""
    MIN_PRIORITY_VALUE: int = 0b000
    """Minimal value of Priority parameter defined by SAE J1939."""
    MAX_PRIORITY_VALUE: int = 0b111
    """Maximal value of Priority parameter defined by SAE J1939."""

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
            raise TypeError(f"Provided value is not int type. Actual type: {type(value)}.")
        if extended_can_id is None:
            if not cls.is_can_id(value):
                raise ValueError("Provided value is out of CAN Identifier values range. "
                                 f"Expected: {cls.MIN_STANDARD_VALUE} <= CAN ID <= {cls.MAX_EXTENDED_VALUE}. "
                                 f"Actual value: {value}")
        elif extended_can_id:
            if not cls.is_extended_can_id(value):
                raise ValueError("Provided value is out of Extended (29-bit) CAN Identifier values range. "
                                 f"Expected: {cls.MIN_EXTENDED_VALUE} <= CAN ID <= {cls.MAX_EXTENDED_VALUE}. "
                                 f"Actual value: {value}")
        else:
            if not cls.is_standard_can_id(value):
                raise ValueError("Provided value is out of Standard (11-bit) CAN Identifier values range."
                                 f"Expected: {cls.MIN_STANDARD_VALUE} <= CAN ID <= {cls.MAX_STANDARD_VALUE}. "
                                 f"Actual value: {value}")

    @classmethod
    def validate_priority(cls, value: int) -> None:
        """
        Validate whether provided priority value is in line with SAE J1939 definition.

        :param value: Value to validate.

        :raise TypeError: Provided value is not int type.
        :raise ValueError: Provided value is out of Priority values range.
        """
        if not isinstance(value, int):
            raise TypeError(f"Provided value is not int type. Actual type: {type(value)}.")
        if not cls.MIN_PRIORITY_VALUE <= value <= cls.MAX_PRIORITY_VALUE:
            raise ValueError("Provided Priority value is out of range. "
                             f"Expected: {cls.MIN_PRIORITY_VALUE} <= Priority <= {cls.MAX_PRIORITY_VALUE}. "
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
            raise TypeError(f"Provided value is not int type. Actual type: {type(value)}.")
        if not cls.MIN_DLC_VALUE <= value <= cls.MAX_DLC_VALUE:
            raise ValueError("Provided DLC value is out of range. "
                             f"Expected: {cls.MIN_DLC_VALUE} <= DLC <= {cls.MAX_DLC_VALUE}. Actual value: {value}")

    @classmethod
    def validate_data_bytes_number(cls, value: int, exact_value: bool = True) -> None:
        """
        Validate whether the provided number of data bytes might be carried in a CAN frame.

        :param value: Value to validate.
        :param exact_value: Informs whether the value must be the exact number of data bytes in a CAN frame.

            - True - provided value must be the exact number of data bytes to be carried by a CAN frame.
            - False - provided value must be a number of data bytes that could be carried by a CAN frame
              (:ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>` is allowed).

        :raise TypeError: Provided values is not int type.
        :raise ValueError: Provided value is not number of data bytes that matches the criteria.
        """
        if not isinstance(value, int):
            raise TypeError("Provided value is not int type.")
        if exact_value:
            if value not in cls.__DATA_BYTES_NUMBERS:
                raise ValueError("Provided value is not a valid CAN Frame data bytes number.")
        else:
            if not cls.MIN_DATA_BYTES_NUMBER <= value <= cls.MAX_DATA_BYTES_NUMBER:
                raise ValueError("Provided data bytes number of a CAN frame is out of range. "
                                 f"Expected: {cls.MIN_DATA_BYTES_NUMBER} <= DLC <= {cls.MAX_DATA_BYTES_NUMBER}. "
                                 f"Actual value: {value}")

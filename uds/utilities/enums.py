"""
Module with common and reused implementation of enums.

`Enumerated types (enums) <https://en.wikipedia.org/wiki/Enumerated_type#Python>`_ are data types that consists of
named values. This module provides extension to `aenum <https://pypi.org/project/aenum/>`_ package.
"""

__all__ = ["ExtendableEnum", "ValidatedEnum", "ByteEnum", "NibbleEnum"]

from typing import Any

from aenum import Enum, IntEnum, extend_enum

from .common_types import validate_nibble, validate_raw_byte


class ExtendableEnum(Enum):
    """Enum that supports new members adding."""

    @classmethod
    def add_member(cls, name: str, value: Any) -> Enum:
        """
        Register a new member.

        :param name: Name of a new member.
        :param value: Value of a new member.

        :raise ValueError: Such name or value is already in use.

        :return: The new member that was just created.
        """
        for member in cls:  # type: ignore
            if member.name == name:
                raise ValueError(f"Name '{name}' is already in use.")
            if member.value == value:
                raise ValueError(f"Value '{value}' is already in use.")
        extend_enum(cls, name, value)
        return cls[name]  # type: ignore


class ValidatedEnum(Enum):
    """Enum that supports members validation."""

    @classmethod
    def is_member(cls, value: Any) -> bool:
        """
        Check whether given argument is a member or a value stored by this Enum.

        :param value: Value to check.

        :return: True if given argument is a member or a value of this Enum, else False.
        """
        try:
            cls.validate_member(value)
        except ValueError:
            return False
        return True

    @classmethod
    def validate_member(cls, value: Any) -> "ValidatedEnum":
        """
        Validate whether given argument is a member or a value stored by this Enum.

        :param value: Value to validate.

        :raise ValueError: Provided value is not a member neither a value of this Enum.
        """
        try:
            return cls(value)
        except ValueError:
            # pylint: disable=raise-missing-from
            raise ValueError(f"Provided value is not a member of this Enum. Actual value: {value}")


class ByteEnum(IntEnum):
    """Enum which members are one byte integers (0x00-0xFF) only."""

    def __new__(cls, value: int):
        """
        Creation of a new member.

        :param value: One byte integer.
        """
        validate_raw_byte(value)
        member = int.__new__(cls, value)
        member._value_ = value  # noqa: F841
        return member


class NibbleEnum(IntEnum):
    """Enum which members are one nibble (4 bits) integers (0x0-0xF) only."""

    def __new__(cls, value: int):
        """
        Creation of a new member.

        :param value: One nibble (4 bits) integer.
        """
        validate_nibble(value)
        member = int.__new__(cls, value)
        member._value_ = value  # noqa: F841
        return member

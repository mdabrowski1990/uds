"""Implementation of Byte Enum."""

__all__ = ["ExtendableEnum", "ValidatedEnum", "ByteEnum"]

from typing import Any

from aenum import Enum, IntEnum, extend_enum


class ExtendableEnum(Enum):
    """Enum with method for adding new members."""

    @classmethod
    def add_member(cls, name: str, value: Any) -> Enum:
        """
        Register a new member.

        :param name: Name of a new member.
        :param value: Value of a new member.

        :raise ValueError: Such name or value is already defined.

        :return: The new member that was just created.
        """
        for member in list(cls):  # noqa: F841
            if member.name == name:
                raise ValueError(f"Name '{name}' is already in use.")
            if member.value == value:
                raise ValueError(f"Value '{value}' is already in use.")
        extend_enum(cls, name, value)
        return cls[name]


class ValidatedEnum(Enum):
    """Enum with methods for members validation."""

    @classmethod
    def is_member(cls, value: Any) -> bool:
        """
        Check whether given value is a member (or its value).

        :param value: Value to check.

        :return: True if given argument is member (or its value), else False.
        """
        try:
            cls(value)
        except ValueError:
            return False
        return True

    @classmethod
    def validate_member(cls, value: Any) -> None:
        """
        Validate whether given value is a member (or its value).

        :param value: Value to validate.

        :raise TypeError: Provided value is neither member (or its value) of this Enum.
        """
        if not cls.is_member(value=value):
            raise ValueError(f"Provided value is not a member of this Enum. Actual value: {value}.")


class ByteEnum(IntEnum):
    """Enum which members are one byte integers (0x00-0xFF)."""

    def __new__(cls, value: int):
        """
        Creation of a new member.

        :param value: One byte integer.

        :raise TypeError: Provided value is not int type.
        :raise ValueError: Provided value is not in inclusive range 0x00-0xFF.
        """
        if not isinstance(value, int):
            raise TypeError(f"Provided 'value' is not int type. Actual type: {type(value)}.")
        if not 0 <= value <= 255:
            raise ValueError(f"Provided 'value' is not in range 0x00-0xFF. Actual value = {value}.")
        member = int.__new__(cls, value)
        member._value_ = value  # noqa: F841
        return member

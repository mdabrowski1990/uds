"""Module with special `Enums <https://en.wikipedia.org/wiki/Enumerated_type#Python>`_ implementations."""

__all__ = ["ExtendableEnum", "ValidatedEnum", "ByteEnum", "NibbleEnum"]

from typing import Any

from aenum import Enum, IntEnum, extend_enum


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
            cls(value)
        except ValueError:
            return False
        return True

    @classmethod
    def validate_member(cls, value: Any) -> None:
        """
        Validate whether given argument is a member or a value stored by this Enum.

        :param value: Value to validate.

        :raise ValueError: Provided value is not a member neither a value of this Enum.
        """
        if not cls.is_member(value):
            raise ValueError(f"Provided value is not a member of this Enum. Actual value: {value}.")


class ByteEnum(IntEnum):
    """Enum which members are one byte integers (0x00-0xFF) only."""

    def __new__(cls, value: int):
        """
        Creation of a new member.

        :param value: One byte integer.

        :raise TypeError: Provided value is not int type.
        :raise ValueError: Provided value is not in inclusive range 0x00-0xFF.
        """
        if not isinstance(value, int):
            raise TypeError(f"Provided 'value' is not int type. Actual type: {type(value)}.")
        if not 0x00 <= value <= 0xFF:
            raise ValueError(f"Provided 'value' is not in range 0x00-0xFF. Actual value = {value}.")
        member = int.__new__(cls, value)
        member._value_ = value  # noqa: F841
        return member


class NibbleEnum(IntEnum):
    """Enum which members are one nibble (4 bits) integers (0x0-0xF) only."""

    def __new__(cls, value: int):
        """
        Creation of a new member.

        :param value: One nibble (4 bits) integer.

        :raise TypeError: Provided value is not int type.
        :raise ValueError: Provided value is not in inclusive range 0x0-0xF.
        """
        if not isinstance(value, int):
            raise TypeError(f"Provided 'value' is not int type. Actual type: {type(value)}.")
        if not 0x0 <= value <= 0xF:
            raise ValueError(f"Provided 'value' is not in range 0x0-0xF. Actual value = {value}.")
        member = int.__new__(cls, value)
        member._value_ = value  # noqa: F841
        return member

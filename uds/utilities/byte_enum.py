"""Implementation of Byte Enum."""

__all__ = ["ByteEnum"]

from aenum import IntEnum, extend_enum


class ByteEnum(IntEnum):
    """Enum which members can one byte integers (0x00-0xFF)."""

    def __new__(cls, value: int):
        """Creation of a new member."""
        if not isinstance(value, int):
            raise TypeError("'value' is not int type")
        if not 0 <= value <= 255:
            raise ValueError(f"'value' is not in range 0x00-0xFF. value = {value}.")
        member = int.__new__(cls, value)
        member._value_ = value  # noqa: F841
        return member

    @classmethod
    def add_member(cls, name: str, value: int) -> None:
        """
        Register a new member.

        :param name: Name of a new member.
        :param value: Value of a new member.

        :raise ValueError: Such name or value is already defined.
        """
        for member in cls.__members__:
            if member.name == name:
                raise ValueError(f"Name '{name}' is already in use.")
            if member.value == value:
                raise ValueError(f"Value '{value}' is already in use.")
        extend_enum(cls, name, value)

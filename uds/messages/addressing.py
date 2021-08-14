"""UDS messages addressing implementation."""

__all__ = ["AddressingType"]

from typing import Any
from enum import Enum


class AddressingType(Enum):
    """
    Types of communication (addressing) defined by UDS.

    Options:
    - PHYSICAL - 1 (client) to 1 (server) communication
    - FUNCTIONAL - 1 (client) to many (servers) communication
    - BROADCAST - 1 (client) to many (servers) communication that does not require response
    """

    PHYSICAL = "Physical"
    FUNCTIONAL = "Functional"
    BROADCAST = "Broadcast"

    @classmethod
    def is_addressing_type(cls, value: Any) -> bool:
        """
        Check whether given value is Addressing Type.

        :param value: Value to check.

        :return: True if value is addressing type, else False.
        """
        return isinstance(value, cls)

    @classmethod
    def validate_addressing_type(cls, value: Any) -> None:
        """
        Validate whether provided value stores an addressing type.

        :param value: Value to validate.

        :raise TypeError: Provided value is not proper addressing type.
        """
        if not cls.is_addressing_type(value=value):
            raise TypeError(f"Provided value is not addressing type. Actual type: {type(value)}.")

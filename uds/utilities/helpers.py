"""Module with helper method reused within the package."""

__all__ = ["validate_time", "validate_timeout", "find_element"]

from collections.abc import Sequence
from typing import Any, TypeVar

from .common_types import TimeMillisecondsAlias

T = TypeVar("T")


def validate_time(value: TimeMillisecondsAlias, accept_zero: bool = True) -> None:
    """
    Validate time value.

    :param value: Time value to check.
    :param accept_zero: Whether zero is acceptable value.

    :raise TypeError: Provided value is not int or float type.
    :raise ValueError: Provided value is a negative number or equal zero (accept_zero=False).
    """
    if not isinstance(value, (int, float)):
        raise TypeError(f"Time value must be int or float type. Actual type: {type(value)}.")
    if accept_zero and value < 0:
        raise ValueError(f"Provided time value is less than 0. Actual value: {value}")
    if not accept_zero and value <= 0:
        raise ValueError(f"Provided time value is less or equal to 0. Actual value: {value}")


def validate_timeout(value: TimeMillisecondsAlias | None) -> None:
    """
    Validate timeout value.

    :param value: Timeout value to check.

    :raise TypeError: Provided value is not None, int or float type.
    :raise ValueError: Provided value is not a positive number.
    """
    if value is not None:
        if not isinstance(value, (int, float)):
            raise TypeError(f"Timeout value must be None, int or float type. Actual type: {type(value)}.")
        if value <= 0:
            raise ValueError(f"Provided timeout value is less or equal to 0. Actual value: {value}")


def find_element(sequence: Sequence[T], **attributes: Any) -> T | None:
    """
    Find the element matching all given attributes.

    :param sequence: Sequence of elements to look in.
    :param attributes: Attributes of an object.

    :return: An object that was found or None if not found.
    """
    for element in sequence:
        if all(getattr(element, attr_name) == attr_value for attr_name, attr_value in attributes.items()):
            return element
    return None  # not found

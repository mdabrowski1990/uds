"""Module with helper method reused within the package."""

__all__ = ["validate_time", "validate_timeout", "find_element"]

from collections.abc import Sequence
from typing import Any, TypeVar, overload

from .common_types import TimeMillisecondsAlias

T1 = TypeVar("T1")
T2 = TypeVar("T2")


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


@overload
def find_element(sequence: Sequence[T1],
                 element_type: type[T2],
                 **attributes: Any
                 ) -> T2 | None:  # pragma: no cover
    ...


@overload
def find_element(sequence: Sequence[T1],
                 element_type: None = None,
                 **attributes: Any
                 ) -> T1 | None:  # pragma: no cover
    ...


def find_element(sequence: Sequence[Any],
                 element_type: type[Any] | None = None,
                 **attributes: Any,
                 ) -> Any | None:
    """
    Find the element matching all given attributes.

    :param sequence: Sequence of elements to look in.
    :param element_type: Element type to look for. None if type is irrelevant.
    :param attributes: Attributes of an object.
        If an element does not have an attribute, None value is assumed.

    :return: An object that was found or None if not found.
    """
    for element in sequence:
        if element_type is not None and not isinstance(element, element_type):
            continue
        if all(getattr(element, attr_name, None) == attr_value for attr_name, attr_value in attributes.items()):
            return element
    return None  # not found

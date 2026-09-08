"""Module with helper method reused within the package."""

__all__ = ["validate_time", "validate_timeout"]

from .common_types import TimeMillisecondsAlias


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

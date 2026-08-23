__all__ = ["validate_timeout"]

from .common_types import TimeMillisecondsAlias


def validate_timeout(value: TimeMillisecondsAlias | None) -> None:
    """
    Validate value of a timeout.

    :param value: Value of a timeout to check.

    :raise TypeError: Provided value is not int or float type.
    :raise ValueError: Provided value is a negative number.
    """
    if value is not None:
        if not isinstance(value, (int, float)):
            raise TypeError(f"Timeout value must be None, int or float type. Actual type: {type(value)}.")
        if value <= 0:
            raise ValueError(f"Provided timeout value is less or equal to 0. Actual value: {value}")

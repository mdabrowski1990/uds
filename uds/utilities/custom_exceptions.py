"""Custom exception that are used within the project."""


class ReassignmentError(Exception):
    """
    Attempt to set a new value to an attribute that cannot be changed.

    Example:
        Objects of class X are initialized with an attribute const_x that must not be changed after the object
        creation (outside __init__ method).

        ReassignmentError would be raised when a user tries to change the value of const_x attribute after the object
        is initialized.
    """


class InconsistentArgumentsError(ValueError):
    """
    Provided values of arguments are not compatible with each other.

    Example:
        A function takes two parameters: a, b

        Let's assume that the function requires to: a > b

        The function would raise InconsistentArgumentsError when values of a and b are not satisfying
        the requirement (a <= b).
    """


class UnusedArgumentError(ValueError):
    """
    At least one argument (that was provided by user) will be ignored.

    Example:
        A function takes two parameters: a, b

        Let's assume that parameter a must always be provided. Parameter b is used only when a == 1.

        The function would raise this exception for following parameters: a=0, b=10.
    """


class UnusedArgumentWarning(Warning):
    """
    At least one argument (that was provided by user) will be ignored.

    It is meant to be used in less strict situation than :class:`~uds.utilities.custom_exceptions.UnusedArgumentError`.

    Example:
        A function takes two parameters: a, b

        Let's assume that parameter a must always be provided. Parameter b is used only when a == 1.

        The function would warn (with this warning) for following parameters: a=0, b=10.
    """


class AmbiguityError(ValueError):
    """Operation cannot be executed because it is ambiguous."""

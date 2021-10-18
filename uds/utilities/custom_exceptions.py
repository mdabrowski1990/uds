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
    At least one provided argument cannot be used.

    Example:
        A function takes two parameters: a, b

        Let's assume that parameter a must always be provided. Parameter b is used only when a == 1.

        The function would warn about UnusedArgumentsWarning if a != 1 and b value was provided.
    """


class AmbiguityError(ValueError):
    """Operation cannot be executed because it is ambiguous."""

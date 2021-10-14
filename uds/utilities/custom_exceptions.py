"""Custom exception used within the project."""


class ReassignmentError(Exception):
    """Attempt to set a new value of an attribute that cannot be changed after the initial value was already set."""


class InconsistentArgumentsError(ValueError):
    """
    Provided values of arguments are not compatible with each other.

    Example:
        A function takes two parameters: a, b
        Function requires: a > b
        This function would raise InconsistentArgumentsError when values of a and b are not satisfying the requirement.
    """


class UnusedArgumentsWarning(Warning):
    """Some of provided arguments will not be used."""

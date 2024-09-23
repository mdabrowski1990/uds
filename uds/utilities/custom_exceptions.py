"""Custom exception that are used within the project."""


class ReassignmentError(Exception):
    """
    An attempt to set a new value to an unchangeable attribute.

    Example:
        Objects of class X are initialized with an attribute const_x that must not be changed after the object
        creation (outside __init__ method).

        ReassignmentError would be raised when a user tries to change the value of const_x attribute after the object
        is initialized.
    """


class InconsistentArgumentsError(ValueError):
    """
    Provided arguments values are not compatible with each other.

    Example:
        A function takes two parameters: `a`, `b`

        Let's assume that the function requires that: `a > b`

        The function would raise InconsistentArgumentsError when values of `a` and `b` are not satisfying
        the requirement (`a > b`), e.g. `a = 0`, `b = 1`.
    """


class UnusedArgumentError(ValueError):
    """
    At least one argument (that was provided by user) will be ignored.

    Example:
        A function takes two parameters: a, b

        Let's assume that parameter `a` must always be provided. Parameter `b` is used only when `a == 1`.

        The function would raise this exception when both parameters are provided but `a != 1`.
    """


class AmbiguityError(ValueError):
    """Operation cannot be executed because it is ambiguous."""


class TransmissionInterruptionError(RuntimeError):
    """
    An unexpected packet was received during UDS message transmission.

    According to UDS ISO Standards the transmission shall be stopped.
    """

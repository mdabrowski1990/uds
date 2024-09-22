"""Custom warnings that are used within the project."""


class UnusedArgumentWarning(Warning):
    """
    At least one argument (that was provided by user) will be ignored.

    It is meant to be used in less strict situation than :class:`~uds.utilities.custom_exceptions.UnusedArgumentError`.

    Example:
        A function takes two parameters: a, b

        Let's assume that parameter `a` must always be provided. Parameter `b` is used only when `a == 1`.

        The function would warn (using this warning) when both parameters are provided but `a != 1`.
    """


class ValueWarning(Warning):
    """Value of the argument is out of typical range, but the package is able to handle it."""


class TransmissionInterruptionWarning(RuntimeWarning):
    """
    An unexpected packet was received during UDS message transmission.

    According to UDS ISO Standards a received packet shall be ignored.
    """

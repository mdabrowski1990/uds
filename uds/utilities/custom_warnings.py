"""Custom warnings that are used within the project."""


class UnusedArgumentWarning(Warning):
    """
    At least one argument (that was provided by user) will be ignored.

    It is meant to be used in less strict situation than :class:`~uds.utilities.custom_exceptions.UnusedArgumentError`.

    Example:
        A function takes two parameters: a, b

        Let's assume that parameter a must always be provided. Parameter b is used only when a == 1.

        The function would warn (with this warning) for following parameters: a=0, b=10.
    """

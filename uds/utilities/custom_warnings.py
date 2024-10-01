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


class UnexpectedPacketReceptionWarning(RuntimeWarning):
    """
    An unexpected packet was received.

    TODO: refer to knowledge-base section of error handling, remove note then

    .. note::
        According to UDS ISO 15765-2 Standard:

        As a general rule, arrival of an unexpected N_PDU from any node shall be ignored, with the exception of
        SF N_PDUs and physically addressed FF N_PDUs; functionally addressed FirstFrames shall be ignored.
    """


class MessageReceptionWarning(RuntimeWarning):
    """
    A new UDS message transmission was started while in process of receiving UDS message.

    TODO: refer to knowledge-base section of error handling, remove note then

    .. note::
        According to UDS ISO 15765-2 Standard:

        As a general rule, arrival of an unexpected N_PDU from any node shall be ignored, with the exception of
        SF N_PDUs and physically addressed FF N_PDUs; functionally addressed FirstFrames shall be ignored.
    """

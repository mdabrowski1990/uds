"""
Implementation of diagnostic messages addressing.

Diagnostic messages :ref:`addressing <knowledge-base-addressing>` describes a communication model that is used
during a transmission.
"""

__all__ = ["AddressingType", "AddressingTypeMemberTyping"]

from typing import Union

from aenum import StrEnum

from uds.utilities import ValidatedEnum


class AddressingType(StrEnum, ValidatedEnum):
    """
    Addressing types values defined by UDS protocol.

    :ref:`Addressing <knowledge-base-addressing>` describes a communication model that is used for
    a diagnostic message transmission.
    """

    PHYSICAL = "Physical"  # noqa: F841
    """:ref:`Physical addressing <knowledge-base-physical-addressing>` - 1 (client) to 1 (server) communication."""
    FUNCTIONAL = "Functional"  # noqa: F841
    """:ref:`Functional addressing <knowledge-base-functional-addressing>` - 1 (client) to many (servers)
    communication."""


AddressingTypeMemberTyping = Union[AddressingType, str]
"""Typing alias that describes :class:`~uds.message.addressing.AddressingType` member."""

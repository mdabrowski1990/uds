"""
UDS addressing implementation.

Diagnostic messages :ref:`addressing <knowledge-base-addressing>` describes a communication model that is used
during a transmission.
"""

__all__ = ["AddressingType", "AddressingMemberTyping"]

from typing import Union

from aenum import StrEnum

from uds.utilities import ValidatedEnum


class AddressingType(StrEnum, ValidatedEnum):
    """Model of UDS communication."""

    PHYSICAL = "Physical"  # noqa: F841
    """Physical addressing - 1 (client) to 1 (server) communication."""
    FUNCTIONAL = "Functional"  # noqa: F841
    """Functional addressing - 1 (client) to many (servers) communication."""


AddressingMemberTyping = Union[AddressingType, str]
"""Typing alias that describes AddressingType member."""

"""
Implementation of diagnostic messages addressing.

:ref:`Addressing <knowledge-base-addressing>` describes a communication model that is used during UDS communication.
"""

__all__ = ["AddressingType", "AddressingTypeAlias"]

from typing import Union

from aenum import StrEnum, unique

from uds.utilities import ValidatedEnum


@unique
class AddressingType(StrEnum, ValidatedEnum):
    """
    Addressing types values defined by UDS protocol.

    :ref:`Addressing <knowledge-base-addressing>` describes a communication model that is used during UDS communication.
    """

    PHYSICAL = "Physical"
    """:ref:`Physical addressing <knowledge-base-physical-addressing>` - 1 (client) to 1 (server) communication."""
    FUNCTIONAL = "Functional"
    """:ref:`Functional addressing <knowledge-base-functional-addressing>` - 1 (client) to many (servers)
    communication."""


AddressingTypeAlias = Union[AddressingType, str]
"""Alias that describes :class:`~uds.transmission_attributes.addressing.AddressingType` member."""

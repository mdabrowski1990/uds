"""Definition of Addressing Types used for UDS communication."""

__all__ = ["AddressingType"]

from aenum import StrEnum, unique

from uds.utilities import ValidatedEnum


@unique
class AddressingType(ValidatedEnum, StrEnum):
    """
    Addressing types values defined by UDS protocol.

    :ref:`Addressing <knowledge-base-addressing>` describes a communication model that is used during UDS communication.
    """

    PHYSICAL: "AddressingType" = "Physical"  # type: ignore
    """:ref:`Physical addressing <knowledge-base-physical-addressing>` - 1 (client) to 1 (server) communication."""
    FUNCTIONAL: "AddressingType" = "Functional"  # type: ignore
    """:ref:`Functional addressing <knowledge-base-functional-addressing>` - 1 (client) to many (servers)
    communication."""

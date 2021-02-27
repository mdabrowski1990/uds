"""UDS messages addressing implementation."""

__all__ = ["AddressingType"]

from enum import Enum


class AddressingType(Enum):
    """
    Types of communication (addressing) defined by UDS.

    Options:
    - PHYSICAL - 1 (client) to 1 (server) communication
    - FUNCTIONAL - 1 (client) to many (servers) communication
    - BROADCAST - 1 (client) to many (servers) communication that does not require response
    """

    PHYSICAL = "Physical"  # noqa: F841
    FUNCTIONAL = "Functional"  # noqa: F841
    BROADCAST = "Broadcast"  # noqa: F841

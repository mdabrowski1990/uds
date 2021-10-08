"""
CAN bus specific implementation of UDS packets.

:ref:`CAN packets <knowledge-base-uds-can-packet>`.
"""

__all__ = ["CanPacketType", "CanAddressingFormat", "CanPacket", "CanPacketRecord"]

from typing import Any

from aenum import StrEnum, unique

from uds.utilities import ValidatedEnum, NibbleEnum
from .abstract_packet import AbstractUdsPacketType, AbstractUdsPacket, AbstractUdsPacketRecord


@unique
class CanPacketType(AbstractUdsPacketType):
    """Definition of :ref:`CAN packet types <knowledge-base-can-n-pci>`."""

    SINGLE_FRAME = 0x0
    """:ref:`Single Frame (SF) <knowledge-base-can-single-frame>` on CAN bus."""
    FIRST_FRAME = 0x1
    """:ref:`First Frame (FF) <knowledge-base-can-first-frame>` on CAN bus."""
    CONSECUTIVE_FRAME = 0x2
    """:ref:`Consecutive Frame (CF) <knowledge-base-can-consecutive-frame>` on CAN bus."""
    FLOW_CONTROL = 0x3
    """:ref:`Flow Control (FC) <knowledge-base-can-flow-control>` on CAN bus."""

    @classmethod
    def is_initial_packet_type(cls, value: Any) -> bool:
        """
        Check whether given argument is a member or a value of packet type that initiates a diagnostic message.

        :param value: Value to check.

        :return: True if given argument is a packet type that initiates a diagnostic message, else False.
        """
        cls.validate_member(value)
        return cls(value) in (cls.SINGLE_FRAME, cls.FIRST_FRAME)


@unique
class CanAddressingFormat(StrEnum, ValidatedEnum):
    """Definition of :ref:`CAN addressing formats <knowledge-base-can-addressing>`."""

    NORMAL_11BIT_ADDRESSING = "Normal 11-bit Addressing"
    """This value represents :ref:`normal addressing <knowledge-base-can-normal-addressing>` that uses
    11-bit CAN Identifiers."""
    NORMAL_FIXED_ADDRESSING = "Normal Fixed Addressing"
    """:ref:`Normal fixed addressing <knowledge-base-can-normal-fixed-addressing>` format. 
    It uses 29-bit CAN Identifiers only."""
    EXTENDED_11BIT_ADDRESSING = "Extended 11-bit Addressing"
    """:ref:`Extended addressing <knowledge-base-can-extended-addressing>` format that uses 11-bit CAN Identifiers."""
    EXTENDED_29BIT_ADDRESSING = "Extended 29-bit Addressing"
    """:ref:`Extended addressing <knowledge-base-can-extended-addressing>` format that uses 29-bit CAN Identifiers."""
    MIXED_11BIT_ADDRESSING = "Mixed 11-bit Addressing"
    """:ref:`Mixed addressing with 11-bit CAN ID <knowledge-base-can-mixed-11-bit-addressing>`.
    Subformat of :ref:`mixed addressing <knowledge-base-can-mixed-addressing>` that uses 11-bit CAN Identifiers."""
    MIXED_29BIT_ADDRESSING = "Mixed 29-bit Addressing"
    """:ref:`Mixed addressing with 29-bit CAN ID <knowledge-base-can-mixed-29-bit-addressing>`.
    Subformat of :ref:`mixed addressing <knowledge-base-can-mixed-addressing>` that uses 29-bit CAN Identifiers."""


@unique
class CanFlowStatus(NibbleEnum, ValidatedEnum):
    ...  # TODO


class CanPacket(AbstractUdsPacket):
    """TODO: knowledge base first"""


class CanPacketRecord(AbstractUdsPacketRecord):
    """TODO: knowledge base first"""

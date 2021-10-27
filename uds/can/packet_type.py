"""CAN packet types definitions."""

__all__ = ["CanPacketType", "CanPacketTypeMemberAlias"]

from typing import Any, Union

from aenum import unique

from uds.packet import AbstractUdsPacketType


@unique
class CanPacketType(AbstractUdsPacketType):
    """
    Definition of CAN packet types.

    :ref:`CAN packet types <knowledge-base-can-n-pci>` are
    :ref:`Network Protocol Control Information (N_PCI) <knowledge-base-n-pci>` values that are specific for CAN bus.
    """

    SINGLE_FRAME = 0x0
    """:ref:`Single Frame (SF) <knowledge-base-can-single-frame>` CAN packet type."""
    FIRST_FRAME = 0x1
    """:ref:`First Frame (FF) <knowledge-base-can-first-frame>` CAN packet type."""
    CONSECUTIVE_FRAME = 0x2
    """:ref:`Consecutive Frame (CF) <knowledge-base-can-consecutive-frame>` CAN packet type."""
    FLOW_CONTROL = 0x3
    """:ref:`Flow Control (FC) <knowledge-base-can-flow-control>` CAN packet type."""

    @classmethod
    def is_initial_packet_type(cls, value: Any) -> bool:
        """
        Check whether given argument is a member or a value of a CAN packet type that initiates a diagnostic message.

        :param value: Value to check.

        :return: True if given argument is a packet type that initiates a diagnostic message, else False.
        """
        cls.validate_member(value)
        return cls(value) in (cls.SINGLE_FRAME, cls.FIRST_FRAME)


CanPacketTypeMemberAlias = Union[CanPacketType, int]
"""Alias that describes :class:`~uds.can.packet_type.CanPacketType` member type."""

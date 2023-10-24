"""CAN packet types definitions."""

__all__ = ["CanPacketType"]

from aenum import unique

from uds.can import CanSingleFrameHandler, CanFirstFrameHandler, CanConsecutiveFrameHandler, CanFlowControlHandler
from .abstract_packet_type import AbstractUdsPacketType


@unique
class CanPacketType(AbstractUdsPacketType):
    """
    Definition of CAN packet types.

    :ref:`CAN packet types <knowledge-base-can-n-pci>` are
    :ref:`Network Protocol Control Information (N_PCI) <knowledge-base-n-pci>` values that are specific for CAN bus.
    """

    SINGLE_FRAME: "CanPacketType" = CanSingleFrameHandler.SINGLE_FRAME_N_PCI  # type: ignore
    """CAN packet type (N_PCI) value of :ref:`Single Frame (SF) <knowledge-base-can-single-frame>`."""
    FIRST_FRAME: "CanPacketType" = CanFirstFrameHandler.FIRST_FRAME_N_PCI  # type: ignore
    """CAN packet type (N_PCI) value of First Frame (FF) <knowledge-base-can-first-frame>`."""
    CONSECUTIVE_FRAME: "CanPacketType" = CanConsecutiveFrameHandler.CONSECUTIVE_FRAME_N_PCI  # type: ignore
    """CAN packet type (N_PCI) value of :ref:`Consecutive Frame (CF) <knowledge-base-can-consecutive-frame>`."""
    FLOW_CONTROL: "CanPacketType" = CanFlowControlHandler.FLOW_CONTROL_N_PCI  # type: ignore
    """CAN packet type (N_PCI) value of :ref:`Flow Control (FC) <knowledge-base-can-flow-control>`."""

    @classmethod
    def is_initial_packet_type(cls, value: "CanPacketType") -> bool:
        """
        Check whether given argument is a CAN packet type that initiates a diagnostic message.

        :param value: Value to check.

        :return: True if given argument is a packet type that initiates a diagnostic message, else False.
        """
        cls.validate_member(value)
        return value in (cls.SINGLE_FRAME, cls.FIRST_FRAME)

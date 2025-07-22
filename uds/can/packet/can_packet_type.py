"""CAN packet types definitions."""

__all__ = ["CanPacketType"]

from aenum import unique

from uds.packet.abstract_packet_type import AbstractPacketType
from .single_frame import SINGLE_FRAME_N_PCI
from .first_frame import FIRST_FRAME_N_PCI
from .consecutive_frame import CONSECUTIVE_FRAME_N_PCI
from .flow_control import FLOW_CONTROL_N_PCI


@unique
class CanPacketType(AbstractPacketType):
    """
    Definition of CAN packet types.

    :ref:`CAN packet types <knowledge-base-can-n-pci>` are
    :ref:`Network Protocol Control Information (N_PCI) <knowledge-base-n-pci>` values that are specific for CAN bus.
    """

    SINGLE_FRAME: "CanPacketType" = SINGLE_FRAME_N_PCI  # type: ignore
    """CAN packet type (N_PCI) value of :ref:`Single Frame (SF) <knowledge-base-can-single-frame>`."""
    FIRST_FRAME: "CanPacketType" = FIRST_FRAME_N_PCI  # type: ignore
    """CAN packet type (N_PCI) value of First Frame (FF) <knowledge-base-can-first-frame>`."""
    CONSECUTIVE_FRAME: "CanPacketType" = CONSECUTIVE_FRAME_N_PCI  # type: ignore
    """CAN packet type (N_PCI) value of :ref:`Consecutive Frame (CF) <knowledge-base-can-consecutive-frame>`."""
    FLOW_CONTROL: "CanPacketType" = FLOW_CONTROL_N_PCI  # type: ignore
    """CAN packet type (N_PCI) value of :ref:`Flow Control (FC) <knowledge-base-can-flow-control>`."""

    @classmethod
    def is_initial_packet_type(cls, value: "CanPacketType") -> bool:
        """
        Check whether given argument is a CAN packet type that initiates a diagnostic message.

        :param value: Value to check.

        :return: True if given argument is a packet type that initiates a diagnostic message, else False.
        """
        return cls.validate_member(value) in (cls.SINGLE_FRAME, cls.FIRST_FRAME)

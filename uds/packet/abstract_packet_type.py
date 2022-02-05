"""Common (abstract) implementation of UDS Packet Types."""

__all__ = ["AbstractUdsPacketType", "AbstractUdsPacketTypeAlias"]

from typing import Any, Union
from abc import abstractmethod

from uds.utilities import NibbleEnum, ValidatedEnum, ExtendableEnum


class AbstractUdsPacketType(NibbleEnum, ValidatedEnum, ExtendableEnum):
    """
    Abstract definition of UDS packet type.

    Packet type information is carried by :ref:`Network Protocol Control Information (N_PCI) <knowledge-base-n-pci>`.
    Enums with packet types (N_PCI) values for certain buses (e.g. CAN, LIN, FlexRay) must inherit after this class.

    .. note:: There are differences in values for each bus (e.g. LIN does not use Flow Control).
    """

    @classmethod
    @abstractmethod
    def is_initial_packet_type(cls, value: Any) -> bool:
        """
        Check whether given argument is a member or a value of packet type that initiates a diagnostic message.

        :param value: Value to check.

        :return: True if given argument is a packet type that initiates a diagnostic message, else False.
        """


AbstractUdsPacketTypeAlias = Union[AbstractUdsPacketType, int]
"""Alias that describes :class:`~uds.packet.abstract_packet_type.AbstractUdsPacketType` member."""

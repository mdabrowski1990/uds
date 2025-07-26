"""Common (abstract) implementation of Packet Types."""

__all__ = ["AbstractPacketType"]

from abc import abstractmethod

from uds.utilities import ExtendableEnum, NibbleEnum, ValidatedEnum


class AbstractPacketType(ValidatedEnum, ExtendableEnum, NibbleEnum):
    """
    Abstract definition of packet type.

    Packet type information is carried by :ref:`Network Protocol Control Information (N_PCI) <knowledge-base-n-pci>`.
    Enums with packet types (N_PCI) values definition for each concrete bus/network type (e.g. CAN, LIN, FlexRay)
    must inherit after this class.

    .. note:: There are differences in values for each bus/network type (e.g. LIN does not use Flow Control
    while CAN bus does).
    """

    @classmethod
    @abstractmethod
    def is_initial_packet_type(cls, value: "AbstractPacketType") -> bool:
        """
        Check whether given argument is a member or a value of packet type that initiates a diagnostic message.

        :param value: Value to check.

        :return: True if given argument is a packet type that initiates a diagnostic message, else False.
        """

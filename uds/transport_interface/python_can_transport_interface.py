"""
Implementation of python-can Transport Interface.

Documentation for python-can package: https://python-can.readthedocs.io/
"""

__all__ = ["PyCanTransportInterface"]

from typing import Optional, Any

from uds.utilities import TimeMilliseconds
from uds.packet import CanPacket, CanPacketRecord
from uds.message import UdsMessage, UdsMessageRecord
from .abstract_can_transport_interface import AbstractCanTransportInterface


class PyCanTransportInterface(AbstractCanTransportInterface):
    """Transport Interface for managing UDS on CAN using python-can package."""

    @property
    def n_as_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_As time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """
        raise NotImplementedError

    @property
    def n_ar_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_Ar time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """
        raise NotImplementedError

    @property
    def n_bs_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_Bs time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """
        raise NotImplementedError

    @property
    def n_cr_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_Cr time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """
        raise NotImplementedError

    @AbstractCanTransportInterface.dlc.setter  # type: ignore  # TODO: redefine dlc getter as well if needed
    def dlc(self, value: int):
        """
        Set value of base CAN DLC to use for CAN Packets.

        :param value: Value to set.
        """
        # TODO: verify whether the dlc is compatible with the bus configuration
        raise NotImplementedError

    @staticmethod
    def is_supported_bus_manager(bus_manager: Any) -> bool:
        """
        Check whether provided value is a bus manager that is supported by this Transport Interface.

        :param bus_manager: Value to check.

        :return: True if provided bus object is compatible with this Transport Interface, False otherwise.
        """
        raise NotImplementedError

    async def await_packet_received(self, timeout: Optional[TimeMilliseconds] = None) -> CanPacketRecord:
        """
        Wait until the next CAN packet is received.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information of a packet that was just received.
        """
        raise NotImplementedError

    async def await_packet_transmitted(self, timeout: Optional[TimeMilliseconds] = None) -> CanPacketRecord:
        """
        Wait until the next CAN packet is transmitted.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information of a packet that was just transmitted.
        """
        raise NotImplementedError

    async def await_message_received(self, timeout: Optional[TimeMilliseconds] = None) -> UdsMessageRecord:
        """
        Wait until the next UDS message is received.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information of a message that was just received.
        """
        raise NotImplementedError

    async def await_message_transmitted(self, timeout: Optional[TimeMilliseconds] = None) -> UdsMessageRecord:
        """
        Wait until the next UDS message is transmitted.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information of a message that was just transmitted.
        """
        raise NotImplementedError

    def send_packet(self, packet: CanPacket, delay: Optional[TimeMilliseconds] = None) -> None:
        """
        Transmit CAN packet on the configured bus.

        :param packet: CAN packet to send.
        :param delay: Value of a delay (in milliseconds) if the transmission to be scheduled in the future.
            None if the transmission to be executed immediately.
        """
        raise NotImplementedError

    def send_message(self, message: UdsMessage, delay: Optional[TimeMilliseconds] = None) -> None:
        """
        Transmit UDS message on the configured bus.

        :param message: A message to send.
        :param delay: Value of a delay (in milliseconds) if the transmission to be scheduled in the future.
            None if the transmission to be executed immediately.
        """
        raise NotImplementedError

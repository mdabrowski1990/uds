"""Implementation of Transport Interfaces for CAN bus handled by python-can."""

__all__ = ["PyCanTransportInterface"]

from typing import Optional, Any

from can import BusABC

from uds.utilities import TimeMilliseconds
from uds.packet import CanPacket, CanPacketRecord
from uds.message import UdsMessage, UdsMessageRecord
from uds.can import CanAddressingFormatAlias
from uds.segmentation import CanAIArgsAlias
from .abstract_can_transport_interface import AbstractCanTransportInterface


class PyCanTransportInterface(AbstractCanTransportInterface):
    """
    Transport Interface for CAN that is compatible with python-can.

    Documentation for python-can: https://python-can.readthedocs.io/
    """

    def __init__(self,  # pylint: disable=super-init-not-called
                 can_bus: BusABC,  # noqa: F841
                 max_packet_records_stored: int,  # noqa: F841
                 max_message_records_stored: int,  # noqa: F841
                 addressing_format: CanAddressingFormatAlias,  # noqa: F841
                 physical_ai: CanAIArgsAlias,  # noqa: F841
                 functional_ai: CanAIArgsAlias,  # noqa: F841
                 **kwargs: Any) -> None:  # noqa: F841
        """
        Create Transport Interface (an object for handling UDS Transport and Network layers).

        :param bus_manager: An object that handles the bus (Physical and Data layers of OSI Model).
        :param max_packet_records_stored: Maximal number of UDS packet records to be stored in
            :attr:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.packet_records`.
        :param max_message_records_stored: Maximal number of UDS message records to be stored in
            :attr:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.message_records`.
        :param kwargs: Optional arguments that are specific for CAN bus.

            - :parameter n_as_timeout: Timeout value for :ref:`N_As <knowledge-base-can-n-as>` time parameter.
            - :parameter n_ar_timeout: Timeout value for :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter.
            - :parameter n_bs_timeout: Timeout value for :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter.
            - :parameter n_br: Value of :ref:`N_Br <knowledge-base-can-n-br>` time parameter to use in communication.
            - :parameter n_cs: Value of :ref:`N_Cs <knowledge-base-can-n-cs>` time parameter to use in communication.
            - :parameter n_cr_timeout: Timeout value for :ref:`N_Cr <knowledge-base-can-n-cr>` time parameter.
            - :parameter dlc: Base CAN DLC value to use for CAN Packets.
            - :parameter use_data_optimization: Information whether to use CAN Frame Data Optimization.
            - :parameter filler_byte: Filler byte value to use for CAN Frame Data Padding.
            - :parameter flow_control_generator: Generator of Flow Control CAN packets.
        """
        raise NotImplementedError

    @property  # noqa: F841
    def n_as_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_As time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """
        raise NotImplementedError

    @property  # noqa: F841
    def n_ar_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_Ar time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """
        raise NotImplementedError

    @property  # noqa: F841
    def n_bs_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_Bs time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """
        raise NotImplementedError

    @property  # noqa: F841
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
    def is_supported_bus_manager(bus_manager: Any) -> bool:  # noqa: F841
        """
        Check whether provided value is a bus manager that is supported by this Transport Interface.

        :param bus_manager: Value to check.

        :return: True if provided bus object is compatible with this Transport Interface, False otherwise.
        """
        raise NotImplementedError

    async def await_packet_received(self, timeout: Optional[TimeMilliseconds] = None) -> CanPacketRecord:  # noqa: F841
        """
        Wait until the next UDS packet is received.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information of a packet that was just received.
        """
        raise NotImplementedError

    async def await_packet_transmitted(self, timeout: Optional[TimeMilliseconds] = None) -> CanPacketRecord:  # noqa: F841
        """
        Wait until the next UDS packet is transmitted.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information of a packet that was just transmitted.
        """
        raise NotImplementedError

    async def await_message_transmitted(self, timeout: Optional[TimeMilliseconds] = None) -> UdsMessageRecord:  # noqa: F841
        """
        Wait until the next UDS message is received.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information of a message that was just received.
        """
        raise NotImplementedError

    async def await_message_received(self, timeout: Optional[TimeMilliseconds] = None) -> UdsMessageRecord:  # noqa: F841
        """
        Wait until the next UDS message is transmitted.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information of a message that was just transmitted.
        """
        raise NotImplementedError

    def send_packet(self, packet: CanPacket, delay: Optional[TimeMilliseconds] = None) -> None:  # noqa: F841
        """
        Transmit UDS packet on the configured bus.

        :param packet: A packet to send.
        :param delay: Value of a delay (in milliseconds) if the transmission to be scheduled in the future.
            None if the transmission to be executed immediately.
        """
        raise NotImplementedError

    def send_message(self, message: UdsMessage, delay: Optional[TimeMilliseconds] = None) -> None:  # noqa: F841
        """
        Transmit UDS message on the configured bus.

        :param message: A message to send.
        :param delay: Value of a delay (in milliseconds) if the transmission to be scheduled in the future.
            None if the transmission to be executed immediately.
        """
        raise NotImplementedError

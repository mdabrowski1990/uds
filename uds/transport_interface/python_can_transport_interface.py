"""
Implementation of python-can Transport Interface.

Documentation for python-can package: https://python-can.readthedocs.io/
"""

__all__ = ["PyCanTransportInterface"]

from typing import Optional, Any

from can import BusABC, AsyncBufferedReader, BufferedReader, Notifier, Message

from uds.utilities import TimeMilliseconds
from uds.can import AbstractCanAddressingInformation, CanIdHandler, CanDlcHandler
from uds.packet import CanPacket, CanPacketRecord
from uds.transmission_attributes import TransmissionDirection
from .abstract_can_transport_interface import AbstractCanTransportInterface


class PyCanTransportInterface(AbstractCanTransportInterface):
    """Transport Interface for managing UDS on CAN with python-can package as bus handler."""

    def __init__(self,
                 can_bus_manager: Any,
                 addressing_information: AbstractCanAddressingInformation,
                 **kwargs: Any) -> None:
        """
        Create python-can Transport Interface.

        :param can_bus_manager: An object that handles CAN bus (Physical and Data layers of OSI Model).
        :param addressing_information: Addressing Information of CAN Transport Interface.
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
        """
        self.__n_as_measured: Optional[TimeMilliseconds] = None
        self.__n_ar_measured: Optional[TimeMilliseconds] = None
        self.__n_bs_measured: Optional[TimeMilliseconds] = None
        self.__n_cr_measured: Optional[TimeMilliseconds] = None
        super().__init__(can_bus_manager=can_bus_manager,
                         addressing_information=addressing_information,
                         **kwargs)
        self.__async_listener = AsyncBufferedReader()
        self.__sync_listener = BufferedReader()
        self.__can_notifier = Notifier(bus=self.bus_manager,
                                       listeners=[self.__async_listener, self.__sync_listener])

    @property
    def n_as_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_As time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """
        return self.__n_as_measured

    @property
    def n_ar_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_Ar time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """
        return self.__n_ar_measured

    @property  # noqa
    def n_bs_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_Bs time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """
        return self.__n_bs_measured

    @property  # noqa
    def n_cr_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_Cr time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """
        return self.__n_cr_measured

    @staticmethod
    def is_supported_bus_manager(bus_manager: Any) -> bool:
        """
        Check whether provided value is a bus manager that is supported by this Transport Interface.

        :param bus_manager: Value to check.

        :return: True if provided bus object is compatible with this Transport Interface, False otherwise.
        """
        return isinstance(bus_manager, BusABC)  # TODO: check that receive_own_messages is set

    def send_packet(self, packet: CanPacket) -> CanPacketRecord:  # type: ignore
        """
        Transmit CAN packet.

        :param packet: CAN packet to send.

        :raise TypeError: Provided packet is not CAN Packet.

        :return: Record with historic information about transmitted CAN packet.
        """
        if not isinstance(packet, CanPacket):
            raise TypeError("Provided packet value does not contain CAN Packet.")
        can_message = Message(arbitration_id=packet.can_id,
                              is_extended_id=CanIdHandler.is_extended_can_id(packet.can_id),
                              data=packet.raw_frame_data,
                              is_fd=CanDlcHandler.is_can_fd_specific_dlc(packet.dlc))
        self.bus_manager.send(can_message)
        # TODO: get sent packet from self.__sync_listener - NOTE: we have to see sent messages
        # TODO: create CanPacketRecord and return it

    async def receive_packet(self, timeout: Optional[TimeMilliseconds] = None) -> CanPacketRecord:
        """
        Receive CAN packet.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TypeError: Provided timeout value is not None neither int nor float type.
        :raise ValueError: Provided timeout value is less or equal 0.
        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information about received CAN packet.
        """
        if timeout is not None:
            if not isinstance(timeout, (int, float)):
                raise TypeError("Provided timeout value is not None neither int nor float type.")
            if timeout <= 0:
                raise ValueError("Provided timeout value is less or equal 0.")
        received_frame = await self.__async_listener.get_message()
        while False:  # TODO: check if received message is either physically or functionally addressed packet directed for this node
            received_message = await self.__async_listener.get_message()
        packet_addressing_type = ...  # TODO: extract
        packet_addressing_format = ...  # TODO: extract
        received_datetime = ...  # TODO: extract
        return CanPacketRecord(frame=received_frame,
                               direction=TransmissionDirection.RECEIVED,
                               addressing_type=packet_addressing_type,
                               addressing_format=packet_addressing_format,
                               transmission_time=received_datetime)

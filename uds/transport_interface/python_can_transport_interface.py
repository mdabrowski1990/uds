"""
Implementation of python-can Transport Interface.

Documentation for python-can package: https://python-can.readthedocs.io/
"""

__all__ = ["PyCanTransportInterface"]

from typing import Optional, Any

from can import BusABC

from uds.utilities import TimeMilliseconds
from uds.can import AbstractCanAddressingInformation
from .abstract_transport_interface import AbstractTransportInterface
from .abstract_can_transport_interface import AbstractCanTransportInterface


class PyCanTransportInterface(AbstractCanTransportInterface):
    """Transport Interface for managing UDS on CAN using python-can package."""

    def __init__(self,
                 can_bus_manager: Any,
                 addressing_information: AbstractCanAddressingInformation,
                 packet_records_number: int = AbstractTransportInterface.DEFAULT_PACKET_RECORDS_NUMBER,
                 message_records_number: int = AbstractTransportInterface.DEFAULT_MESSAGE_RECORDS_NUMBER,
                 **kwargs: Any) -> None:
        """
        Create python-can Transport Interface.

        :param can_bus_manager: An object that handles CAN bus (Physical and Data layers of OSI Model).
        :param addressing_information: Addressing Information of CAN Transport Interface.
        :param packet_records_number: Number of UDS packet records to store.
        :param message_records_number: Number of UDS Message records to store.
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
        self.__n_as_measured: Optional[TimeMilliseconds] = None
        self.__n_ar_measured: Optional[TimeMilliseconds] = None
        self.__n_bs_measured: Optional[TimeMilliseconds] = None
        self.__n_cr_measured: Optional[TimeMilliseconds] = None
        super().__init__(can_bus_manager=can_bus_manager,
                         addressing_information=addressing_information,
                         packet_records_number=packet_records_number,
                         message_records_number=message_records_number,
                         **kwargs)

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

    @property  # noqa: F841
    def n_bs_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_Bs time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """
        return self.__n_bs_measured

    @property  # noqa: F841
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
        return isinstance(bus_manager, BusABC)

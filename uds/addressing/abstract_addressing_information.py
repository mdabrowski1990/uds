"""Definition of UDS Addressing Information for storing Client/Server Addresses."""

from abc import ABC, abstractmethod
from typing import TypedDict
from types import MappingProxyType
from .addressing_type import AddressingType


class AbstractAddressingInformation(ABC):
    """Definition of Addressing Information parameters for any UDS entity that is common for all communication buses."""

    ADDRESSING_TYPE_NAME: str = "addressing_type"
    """Name of :ref:`Addressing Type <knowledge-base-can-addressing>` parameter in Addressing Information."""

    def __init__(self,
                 rx_packets_physical_params: dict,
                 tx_packets_physical_params: dict,
                 rx_packets_functional_params: dict,
                 tx_packets_functional_params: dict) -> None:
        """
        Configure Addressing Information of UDS Entity (either server or client).

        :param rx_packets_physical_params: Addressing parameters of incoming physically addressed communication.
        :param tx_packets_physical_params: Addressing parameters of outgoing physically addressed communication.
        :param rx_packets_functional_params: Addressing parameters of incoming functionally addressed communication.
        :param tx_packets_functional_params: Addressing parameters of outgoing functionally addressed communication.
        """
        self.rx_packets_physical_params = rx_packets_physical_params
        self.tx_packets_physical_params = tx_packets_physical_params
        self.rx_packets_functional_params = rx_packets_functional_params
        self.tx_packets_functional_params = tx_packets_functional_params

    @property
    def rx_packets_physical_params(self) -> MappingProxyType:
        return self.__rx_packets_physical_params

    @rx_packets_physical_params.setter
    def rx_packets_physical_params(self, value: dict) -> None:
        value.update({"addressing_type": AddressingType.PHYSICAL})
        self.__rx_packets_physical_params = MappingProxyType(value)

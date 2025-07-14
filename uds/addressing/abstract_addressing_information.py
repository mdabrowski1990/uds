"""Definition of UDS Addressing Information for storing Client/Server Addresses."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Mapping
from types import MappingProxyType

from .addressing_type import AddressingType

from uds.utilities import ReassignmentError


class AbstractAddressingInformation(ABC):
    """Storage for addressing related parameters for any UDS entity."""

    ADDRESSING_TYPE_NAME: str = "addressing_type"
    """Name of :ref:`Addressing Type <knowledge-base-addressing-addressing>` parameter in Addressing Information."""

    def __init__(self,
                 rx_physical_params: Mapping[str, Any],
                 tx_physical_params: Mapping[str, Any],
                 rx_functional_params: Mapping[str, Any],
                 tx_functional_params: Mapping[str, Any]) -> None:
        """
        Configure Addresses of UDS Entity (either a server or a client).

        :param rx_physical_params: Addressing parameters for incoming physically addressed communication.
        :param tx_physical_params: Addressing parameters for outgoing physically addressed communication.
        :param rx_functional_params: Addressing parameters for incoming functionally addressed communication.
        :param tx_functional_params: Addressing parameters for outgoing functionally addressed communication.
        """
        self.rx_physical_params = rx_physical_params
        self.tx_physical_params = tx_physical_params
        self.rx_functional_params = rx_functional_params
        self.tx_functional_params = tx_functional_params
        self._validate_addressing_information()


    @abstractmethod
    def validate_addressing_params(self, **addressing_params: Any) -> Dict[str, Any]:
        """Check whether the provided parameters are complete and compatible for this Addressing format."""

    @abstractmethod
    def _validate_addressing_information(self) -> None:
        """Check whether the provided addressing information are valid."""

    @property
    def rx_physical_params(self) -> MappingProxyType:
        """Get addressing parameters for incoming physically addressed communication."""
        return self.__rx_physical_params

    @rx_physical_params.setter
    def rx_physical_params(self, addressing_params: Mapping[str, Any]) -> None:
        """
        Set addressing parameters for incoming physically addressed communication.

        :param addressing_params: Addressing parameters to set.

        :raise ReassignmentError: An attempt to change the value after object creation.
        """
        try:
            getattr(self, "_AbstractAddressingInformation__rx_physical_params")
        except AttributeError:
            params = dict(addressing_params)
            params[self.ADDRESSING_TYPE_NAME] = AddressingType.PHYSICAL
            self.__rx_physical_params = MappingProxyType(self.validate_addressing_params(**params))
        else:
            raise ReassignmentError("You cannot change value of 'rx_physical_params' attribute once it is assigned. "
                                    "Create a new object instead.")

    @property
    def tx_physical_params(self) -> MappingProxyType:
        """Get addressing parameters for outgoing physically addressed communication."""
        return self.__tx_physical_params

    @tx_physical_params.setter
    def tx_physical_params(self, addressing_params: Mapping[str, Any]) -> None:
        """
        Set addressing parameters for outgoing physically addressed communication.

        :param addressing_params: Addressing parameters to set.

        :raise ReassignmentError: An attempt to change the value after object creation.
        """
        try:
            getattr(self, "_AbstractAddressingInformation__tx_physical_params")
        except AttributeError:
            params = dict(addressing_params)
            params[self.ADDRESSING_TYPE_NAME] = AddressingType.PHYSICAL
            self.__tx_physical_params = MappingProxyType(self.validate_addressing_params(**params))
        else:
            raise ReassignmentError("You cannot change value of 'tx_physical_params' attribute once it is assigned. "
                                    "Create a new object instead.")
        
    @property
    def rx_functional_params(self) -> MappingProxyType:
        """Get addressing parameters for incoming functionally addressed communication."""
        return self.__rx_functional_params

    @rx_functional_params.setter
    def rx_functional_params(self, addressing_params: Mapping[str, Any]) -> None:
        """
        Set addressing parameters for incoming functionally addressed communication.

        :param addressing_params: Addressing parameters to set.

        :raise ReassignmentError: An attempt to change the value after object creation.
        """
        try:
            getattr(self, "_AbstractAddressingInformation__rx_functional_params")
        except AttributeError:
            params = dict(addressing_params)
            params[self.ADDRESSING_TYPE_NAME] = AddressingType.FUNCTIONAL
            self.__rx_functional_params = MappingProxyType(self.validate_addressing_params(**params))
        else:
            raise ReassignmentError("You cannot change value of 'rx_functional_params' attribute once it is assigned. "
                                    "Create a new object instead.")

    @property
    def tx_functional_params(self) -> MappingProxyType:
        """Get addressing parameters for outgoing functionally addressed communication."""
        return self.__tx_functional_params

    @tx_functional_params.setter
    def tx_functional_params(self, addressing_params: Mapping[str, Any]) -> None:
        """
        Set addressing parameters for outgoing functionally addressed communication.

        :param addressing_params: Addressing parameters to set.

        :raise ReassignmentError: An attempt to change the value after object creation.
        """
        try:
            getattr(self, "_AbstractAddressingInformation__tx_functional_params")
        except AttributeError:
            params = dict(addressing_params)
            params[self.ADDRESSING_TYPE_NAME] = AddressingType.FUNCTIONAL
            self.__tx_functional_params = MappingProxyType(self.validate_addressing_params(**params))
        else:
            raise ReassignmentError("You cannot change value of 'tx_functional_params' attribute once it is assigned. "
                                    "Create a new object instead.")

    def get_other_end(self) -> "AbstractAddressingInformation":
        """
        Get Addressing Information of UDS entity on the other end of UDS communication.

        :return: UDS Addressing Information of a UDS entity that this one communicates with.
        """
        return self.__class__(rx_physical_params=self.tx_physical_params,
                              tx_physical_params=self.rx_physical_params,
                              rx_functional_params=self.tx_functional_params,
                              tx_functional_params=self.rx_functional_params)

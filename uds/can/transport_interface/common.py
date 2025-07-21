"""Definition of UDS Transport Interface for CAN bus."""

__all__ = ["AbstractCanTransportInterface"]

from abc import abstractmethod
from typing import Any, Optional, Tuple
from warnings import warn

from uds.addressing import AbstractCanAddressingInformation
from uds.can import AbstractFlowControlParametersGenerator, DefaultFlowControlParametersGenerator
from uds.message import UdsMessageRecord
from uds.packet import CanPacketType
from uds.segmentation import CanSegmenter
from uds.transport_interface.abstract_transport_interface import AbstractTransportInterface
from uds.utilities import TimeMillisecondsAlias, ValueWarning


class AbstractCanTransportInterface(AbstractTransportInterface):
    """
    Abstract definition of Transport Interface for managing UDS on CAN bus.

    CAN Transport Interfaces are meant to handle UDS middle layers (Transport and Network) on CAN bus.
    """

    N_AS_TIMEOUT: TimeMillisecondsAlias = 1000
    """Timeout value of :ref:`N_As <knowledge-base-can-n-as>` time parameter according to ISO 15765-2."""
    N_AR_TIMEOUT: TimeMillisecondsAlias = 1000
    """Timeout value of :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter according to ISO 15765-2."""
    N_BS_TIMEOUT: TimeMillisecondsAlias = 1000
    """Timeout value of :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter according to ISO 15765-2."""
    N_CR_TIMEOUT: TimeMillisecondsAlias = 1000
    """Timeout value of :ref:`N_Cr <knowledge-base-can-n-cr>` time parameter according to ISO 15765-2."""

    DEFAULT_N_BR: TimeMillisecondsAlias = 0
    """Default value of :ref:`N_Br <knowledge-base-can-n-br>` time parameter."""
    DEFAULT_N_CS: Optional[TimeMillisecondsAlias] = None
    """Default value of :ref:`N_Cs <knowledge-base-can-n-cs>` time parameter."""
    DEFAULT_FLOW_CONTROL_PARAMETERS = DefaultFlowControlParametersGenerator()
    """Default value of :ref:`Flow Control <knowledge-base-can-flow-control>` parameters
    (:ref:`Flow Status <knowledge-base-can-flow-status>`,
    :ref:`Block Size <knowledge-base-can-block-size>`,
    :ref:`Separation Time minimum <knowledge-base-can-st-min>`)."""

    def __init__(self,
                 can_bus_manager: Any,
                 addressing_information: AbstractCanAddressingInformation,
                 **kwargs: Any) -> None:
        """
        Create Transport Interface (an object for handling UDS Transport and Network layers).

        :param can_bus_manager: An object that handles CAN bus (Physical and Data layers of OSI Model).
        :param addressing_information: Addressing Information of CAN Transport Interface.
        :param kwargs: Optional arguments that are specific for CAN bus.

            - :parameter n_as_timeout: Timeout value for :ref:`N_As <knowledge-base-can-n-as>` time parameter.
            - :parameter n_ar_timeout: Timeout value for :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter.
            - :parameter n_bs_timeout: Timeout value for :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter.
            - :parameter n_br: Value of :ref:`N_Br <knowledge-base-can-n-br>` time parameter to use in communication.
            - :parameter n_cs: Value of :ref:`N_Cs <knowledge-base-can-n-cs>` time parameter to use in communication.
            - :parameter n_cr_timeout: Timeout value for :ref:`N_Cr <knowledge-base-can-n-cr>` time parameter.
            - :parameter dlc: Base CAN DLC value to use for CAN packets.
            - :parameter use_data_optimization: Information whether to use
                :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>`.
            - :parameter filler_byte: Filler byte value to use for
                :ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>`.
            - :parameter flow_control_parameters_generator: Generator with Flow Control parameters to use.

        :raise TypeError: Provided Addressing Information value has unexpected type.
        """
        if not isinstance(addressing_information, AbstractCanAddressingInformation):
            raise TypeError("Unsupported type of Addressing Information was provided.")
        self.__addressing_information: AbstractCanAddressingInformation = addressing_information
        super().__init__(bus_manager=can_bus_manager)
        self.__n_bs_measured: Optional[Tuple[TimeMillisecondsAlias, ...]] = None
        self.__n_cr_measured: Optional[Tuple[TimeMillisecondsAlias, ...]] = None
        self.n_as_timeout = kwargs.pop("n_as_timeout", self.N_AS_TIMEOUT)
        self.n_ar_timeout = kwargs.pop("n_ar_timeout", self.N_AR_TIMEOUT)
        self.n_bs_timeout = kwargs.pop("n_bs_timeout", self.N_BS_TIMEOUT)
        self.n_cr_timeout = kwargs.pop("n_cr_timeout", self.N_CR_TIMEOUT)
        self.n_br = kwargs.pop("n_br", self.DEFAULT_N_BR)
        self.n_cs = kwargs.pop("n_cs", self.DEFAULT_N_CS)
        self.flow_control_parameters_generator = kwargs.pop("flow_control_parameters_generator",
                                                            self.DEFAULT_FLOW_CONTROL_PARAMETERS)
        self.__segmenter = CanSegmenter(addressing_information=addressing_information, **kwargs)

    # Common

    def _update_n_bs_measured(self, message: UdsMessageRecord) -> None:
        """
        Update measured values of :ref:`N_Bs <knowledge-base-can-n-bs>` according to timestamps of CAN packet records.

        :param message: Record of UDS message transmitted over CAN.
        """
        if len(message.packets_records) == 1:
            self.__n_bs_measured = None
        else:
            n_bs_measured = []
            for i, packet_record in enumerate(message.packets_records[1:]):
                if packet_record.packet_type == CanPacketType.FLOW_CONTROL:
                    n_bs = packet_record.transmission_time - message.packets_records[i].transmission_time
                    n_bs_measured.append(round(n_bs.total_seconds() * 1000, 3))
            self.__n_bs_measured = tuple(n_bs_measured)

    def _update_n_cr_measured(self, message: UdsMessageRecord) -> None:
        """
        Update measured values of :ref:`N_Cr <knowledge-base-can-n-cr>` according to timestamps of CAN packet records.

        :param message: Record of UDS message transmitted over CAN.
        """
        if len(message.packets_records) == 1:
            self.__n_cr_measured = None
        else:
            n_cr_measured = []
            for i, packet_record in enumerate(message.packets_records[1:]):
                if packet_record.packet_type == CanPacketType.CONSECUTIVE_FRAME:
                    n_cr = packet_record.transmission_time - message.packets_records[i].transmission_time
                    n_cr_measured.append(round(n_cr.total_seconds() * 1000, 3))
            self.__n_cr_measured = tuple(n_cr_measured)

    @property
    def segmenter(self) -> CanSegmenter:
        """Value of the segmenter used by this CAN Transport Interface."""
        return self.__segmenter

    # Time parameter - CAN Network Layer

    @property
    def n_as_timeout(self) -> TimeMillisecondsAlias:
        """Timeout value for :ref:`N_As <knowledge-base-can-n-as>` time parameter."""
        return self.__n_as_timeout

    @n_as_timeout.setter
    def n_as_timeout(self, value: TimeMillisecondsAlias) -> None:
        """
        Set timeout value for :ref:`N_As <knowledge-base-can-n-as>` time parameter.

        :param value: Value of timeout to set.

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided value is less or equal 0.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided time parameter value must be int or float type.")
        if value <= 0:
            raise ValueError("Provided time parameter value must be greater than 0.")
        if value != self.N_AS_TIMEOUT:
            warn(message="Non-default value of N_As timeout was set.",
                 category=ValueWarning)
        self.__n_as_timeout = value

    @property
    @abstractmethod
    def n_as_measured(self) -> Optional[TimeMillisecondsAlias]:
        """
        Get the last measured value of :ref:`N_As <knowledge-base-can-n-as>` time parameter.

        .. note:: The last measurement comes from the last transmission of Single Frame or First Fame CAN Packet using
            either :meth:`~uds.transport_interface.addressing.AbstractCanTransportInterface.send_packet`
            or :meth:`~uds.transport_interface.addressing.AbstractCanTransportInterface.async_send_packet` method.

        :return: Time in milliseconds or None if the value was never measured.
        """

    @property
    def n_ar_timeout(self) -> TimeMillisecondsAlias:
        """Timeout value for :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter."""
        return self.__n_ar_timeout

    @n_ar_timeout.setter
    def n_ar_timeout(self, value: TimeMillisecondsAlias) -> None:
        """
        Set timeout value for :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter.

        :param value: Value of timeout to set.

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided value is less or equal 0.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided time parameter value must be int or float type.")
        if value <= 0:
            raise ValueError("Provided time parameter value must be greater than 0.")
        if value != self.N_AR_TIMEOUT:
            warn(message="Non-default value of N_Ar timeout was set.",
                 category=ValueWarning)
        self.__n_ar_timeout = value

    @property
    @abstractmethod
    def n_ar_measured(self) -> Optional[TimeMillisecondsAlias]:
        """
        Get the last measured value of :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter.

        .. note:: The last measurement comes from the last transmission of Flow Control CAN Packet using either
            :meth:`~uds.transport_interface.addressing.AbstractCanTransportInterface.send_packet` or
            :meth:`~uds.transport_interface.addressing.AbstractCanTransportInterface.async_send_packet` method.

        :return: Time in milliseconds or None if the value was never measured.
        """

    @property
    def n_bs_timeout(self) -> TimeMillisecondsAlias:
        """Timeout value for :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter."""
        return self.__n_bs_timeout

    @n_bs_timeout.setter
    def n_bs_timeout(self, value: TimeMillisecondsAlias) -> None:
        """
        Set timeout value for :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter.

        :param value: Value of timeout to set.

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided value is less or equal 0.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided time parameter value must be int or float type.")
        if value <= 0:
            raise ValueError("Provided time parameter value must be greater than 0.")
        if value != self.N_BS_TIMEOUT:
            warn(message="Non-default value of N_Bs timeout was set.",
                 category=ValueWarning)
        self.__n_bs_timeout = value

    @property  # noqa
    def n_bs_measured(self) -> Optional[Tuple[TimeMillisecondsAlias, ...]]:
        """
        Get the last measured values of :ref:`N_Bs <knowledge-base-addressing-n-bs>` time parameter.

        .. note:: The last measurement comes from the last transmission of UDS message using either
            :meth:`~uds.transport_interface.addressing.AbstractCanTransportInterface.send_message` or
            :meth:`~uds.transport_interface.addressing.AbstractCanTransportInterface.async_send_message` method.

        :return: Tuple with times in milliseconds or None if the values could not be measured.
        """
        return self.__n_bs_measured

    @property
    def n_br(self) -> TimeMillisecondsAlias:
        """
        Get the value of :ref:`N_Br <knowledge-base-addressing-n-br>` time parameter which is currently set.

        .. note:: The actual (observed on the bus) value will be slightly longer as it also includes computation
            and CAN Interface delays.
        """
        return self.__n_br

    @n_br.setter
    def n_br(self, value: TimeMillisecondsAlias) -> None:
        """
        Set the value of :ref:`N_Br <knowledge-base-addressing-n-br>` time parameter to use.

        :param value: The value to set.

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided value is out of range (0 <= value < MAX N_Br).
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided time parameter value must be int or float type.")
        if not 0 <= value < self.n_br_max:
            raise ValueError("Provided time parameter value is out of range.")
        self.__n_br = value

    @property
    def n_br_max(self) -> TimeMillisecondsAlias:
        """
        Get the maximum valid value of :ref:`N_Br <knowledge-base-addressing-n-br>` time parameter.

        .. warning:: To assess maximal value of :ref:`N_Br <knowledge-base-addressing-n-br>`, the actual value of
            :ref:`N_Ar <knowledge-base-addressing-n-ar>` time parameter is required.
            Either the latest measured value of :ref:`N_Ar <knowledge-base-addressing-n-ar>` would be used,
            or 0ms would be assumed (if there are no measurement result).
        """
        n_ar_measured = 0 if self.n_ar_measured is None else self.n_ar_measured
        return 0.9 * self.n_bs_timeout - n_ar_measured

    @property
    def n_cs(self) -> Optional[TimeMillisecondsAlias]:
        """
        Get the value of :ref:`N_Cs <knowledge-base-addressing-n-cs>` time parameter which is currently set.

        .. note:: The actual (observed on the bus) value will be slightly longer as it also includes computation
            and CAN Interface delays.
        """
        return self.__n_cs

    @n_cs.setter
    def n_cs(self, value: Optional[TimeMillisecondsAlias]) -> None:
        """
        Set the value of :ref:`N_Cs <knowledge-base-addressing-n-cs>` time parameter to use.

        :param value: The value to set.
            - None - use timing compatible with :ref:`STmin <knowledge-base-can-st-min>` value received in a preceding
                :ref:`Flow Control CAN packet <knowledge-base-can-flow-control>`
            - int/float type - timing value to be used regardless of a received
                :ref:`STmin <knowledge-base-can-st-min>` value

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided value is out of range (0 <= value < MAX N_Cs).
        """
        if value is not None:
            if not isinstance(value, (int, float)):
                raise TypeError("Provided time parameter value must be int or float type.")
            if not 0 <= value < self.n_cs_max:
                raise ValueError("Provided time parameter value is out of range.")
        self.__n_cs = value

    @property
    def n_cs_max(self) -> TimeMillisecondsAlias:
        """
        Get the maximum valid value of :ref:`N_Cs <knowledge-base-addressing-n-cs>` time parameter.

        .. warning:: To assess maximal value of :ref:`N_Cs <knowledge-base-addressing-n-cs>`, the actual value of
            :ref:`N_As <knowledge-base-addressing-n-as>` time parameter is required.
            Either the latest measured value of :ref:`N_As <knowledge-base-addressing-n-as>` would be used,
            or 0ms would be assumed (if there are no measurement result).
        """
        n_as_measured = 0 if self.n_as_measured is None else self.n_as_measured
        return 0.9 * self.n_cr_timeout - n_as_measured

    @property
    def n_cr_timeout(self) -> TimeMillisecondsAlias:
        """Timeout value for :ref:`N_Cr <knowledge-base-addressing-n-cr>` time parameter."""
        return self.__n_cr_timeout

    @n_cr_timeout.setter
    def n_cr_timeout(self, value: TimeMillisecondsAlias) -> None:
        """
        Set timeout value for :ref:`N_Cr <knowledge-base-addressing-n-cr>` time parameter.

        :param value: Value of timeout to set.

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided value is less or equal 0.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided time parameter value must be int or float type.")
        if value <= 0:
            raise ValueError("Provided time parameter value must be greater than 0.")
        if value != self.N_CR_TIMEOUT:
            warn(message="Non-default value of N_Cr timeout was set.",
                 category=ValueWarning)
        self.__n_cr_timeout = value

    @property  # noqa
    def n_cr_measured(self) -> Optional[Tuple[TimeMillisecondsAlias, ...]]:
        """
        Get the last measured values of :ref:`N_Cr <knowledge-base-addressing-n-cr>` time parameter.

        .. note:: The last measurement comes from the last reception of UDS message using either
            :meth:`~uds.transport_interface.addressing.AbstractCanTransportInterface.receive_message` or
            :meth:`~uds.transport_interface.addressing.AbstractCanTransportInterface.async_receive_message` method.

        :return: Tuple with times in milliseconds or None if the values could not be measured.
        """
        return self.__n_cr_measured

    # Communication parameters

    @property
    def addressing_information(self) -> AbstractCanAddressingInformation:
        """
        Addressing Information of Transport Interface.

        .. warning:: Once the value is set, it must not be changed as it might cause communication problems.
        """
        return self.__addressing_information

    @property
    def dlc(self) -> int:
        """
        Value of base CAN DLC to use for output CAN packets.

        .. note:: All output CAN packets will have this DLC value set unless
            :ref:`CAN Frame Data Optimization <knowledge-base-addressing-data-optimization>` is used.
        """
        return self.segmenter.dlc

    @dlc.setter
    def dlc(self, value: int) -> None:
        """
        Set value of base CAN DLC to use for output CAN packets.

        :param value: Value to set.
        """
        self.segmenter.dlc = value

    @property
    def use_data_optimization(self) -> bool:
        """
        Information whether to use CAN Frame Data Optimization during CAN packets creation.

        .. seealso::
            :ref:`CAN Frame Data Optimization <knowledge-base-addressing-data-optimization>`
        """
        return self.segmenter.use_data_optimization

    @use_data_optimization.setter
    def use_data_optimization(self, value: bool) -> None:
        """
        Set whether to use CAN Frame Data Optimization during CAN packets creation.

        .. seealso::
            :ref:`CAN Frame Data Optimization <knowledge-base-addressing-data-optimization>`

        :param value: Value to set.
        """
        self.segmenter.use_data_optimization = value

    @property
    def filler_byte(self) -> int:
        """
        Filler byte value to use for output CAN Frame Data Padding during segmentation.

        .. seealso::
            :ref:`CAN Frame Data Padding <knowledge-base-addressing-frame-data-padding>`
        """
        return self.segmenter.filler_byte

    @filler_byte.setter
    def filler_byte(self, value: int) -> None:
        """
        Set value of filler byte to use for output CAN Frame Data Padding.

        .. seealso::
            :ref:`CAN Frame Data Padding <knowledge-base-addressing-frame-data-padding>`

        :param value: Value to set.
        """
        self.segmenter.filler_byte = value

    @property
    def flow_control_parameters_generator(self) -> AbstractFlowControlParametersGenerator:
        """Get generator of Flow Control parameters (Flow Status, Block Size, Separation Time minimum)."""
        return self.__flow_control_parameters_generator

    @flow_control_parameters_generator.setter
    def flow_control_parameters_generator(self, value: AbstractFlowControlParametersGenerator) -> None:
        """
        Set value of Flow Control parameters (Flow Status, Block Size, Separation Time minimum) generator.

        :param value: Value to set.
        """
        if not isinstance(value, AbstractFlowControlParametersGenerator):
            raise TypeError("Provided Flow Control parameters generator value has incorrect type.")
        self.__flow_control_parameters_generator = value

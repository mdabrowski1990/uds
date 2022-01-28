"""Abstract definition of UDS Transport Interface for CAN bus."""

__all__ = ["AbstractCanTransportInterface"]


from typing import Optional, Union, Any, Iterator, Iterable
from abc import abstractmethod

from uds.utilities import TimeMilliseconds, RawByte
from uds.packet import CanPacket, CanPacketType
from uds.can import AbstractCanAddressingInformation, CanFlowStatus, CanSTminTranslator
from uds.segmentation import CanSegmenter
from .abstract_transport_interface import AbstractTransportInterface


class AbstractCanTransportInterface(AbstractTransportInterface):
    """
    Abstract definition of Transport Interface for managing UDS on CAN bus.

    CAN Transport Interfaces are meant to handle UDS middle layers (Transport and Network) on CAN bus.
    """

    FlowControlGeneratorAlias = Union[CanPacket, Iterator[CanPacket]]
    """Alias of :ref:`Flow Control <knowledge-base-can-flow-control>` CAN Packets generator."""

    N_AS_TIMEOUT: TimeMilliseconds = 1000
    """Timeout value of :ref:`N_As <knowledge-base-can-n-as>` time parameter according to ISO 15765-2."""
    N_AR_TIMEOUT: TimeMilliseconds = 1000
    """Timeout value of :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter according to ISO 15765-2."""
    N_BS_TIMEOUT: TimeMilliseconds = 1000
    """Timeout value of :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter according to ISO 15765-2."""
    N_CR_TIMEOUT: TimeMilliseconds = 1000
    """Timeout value of :ref:`N_Cr <knowledge-base-can-n-cr>` time parameter according to ISO 15765-2."""

    DEFAULT_N_BR: TimeMilliseconds = 0
    """Default value of :ref:`N_Br <knowledge-base-can-n-br>` time parameter."""
    DEFAULT_N_CS: Optional[TimeMilliseconds] = None
    """Default value of :ref:`N_Cs <knowledge-base-can-n-br>` time parameter."""

    DEFAULT_FLOW_CONTROL_ARGS = {
        "packet_type": CanPacketType.FLOW_CONTROL,
        "flow_status": CanFlowStatus.ContinueToSend,
        "block_size": 0x10,
        "st_min": CanSTminTranslator.encode(0),
    }
    """Default parameters of Flow Control CAN Packet."""

    def __init__(self,
                 can_bus_manager: Any,
                 addressing_information: AbstractCanAddressingInformation,
                 packet_records_number: int,
                 message_records_number: int,
                 **kwargs: Any) -> None:
        """
        Create Transport Interface (an object for handling UDS Transport and Network layers).

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

        :raise TypeError: Provided Addressing Information value has unexpected type.
        """
        if not isinstance(addressing_information, AbstractCanAddressingInformation):
            raise TypeError("Unsupported type of Addressing Information was provided.")
        self.__addressing_information: AbstractCanAddressingInformation = addressing_information
        super().__init__(bus_manager=can_bus_manager,
                         packet_records_number=packet_records_number,
                         message_records_number=message_records_number)
        self.n_as_timeout = kwargs.pop("n_as_timeout", self.N_AS_TIMEOUT)
        self.n_ar_timeout = kwargs.pop("n_ar_timeout", self.N_AR_TIMEOUT)
        self.n_bs_timeout = kwargs.pop("n_bs_timeout", self.N_BS_TIMEOUT)
        self.n_br = kwargs.pop("n_br", self.DEFAULT_N_BR)
        self.n_cs = kwargs.pop("n_cs", self.DEFAULT_N_CS)
        self.n_cr_timeout = kwargs.pop("n_cr_timeout", self.N_CR_TIMEOUT)
        flow_control_generator = kwargs.pop("flow_control_generator", None)
        self.__segmenter = CanSegmenter(addressing_format=addressing_information.addressing_format,
                                        physical_ai=addressing_information.tx_packets_physical_ai,
                                        functional_ai=addressing_information.tx_packets_functional_ai,
                                        **kwargs)
        self.flow_control_generator = flow_control_generator if flow_control_generator is not None else \
            CanPacket(**self.DEFAULT_FLOW_CONTROL_ARGS,
                      **addressing_information.tx_packets_physical_ai,
                      dlc=None if self.use_data_optimization else self.dlc,
                      filler_byte=self.filler_byte)

    @property
    def segmenter(self) -> CanSegmenter:
        """Value of the segmenter used by this CAN Transport Interface."""
        return self.__segmenter

    # Time parameter - CAN Network Layer

    @property
    def n_as_timeout(self) -> TimeMilliseconds:
        """Timeout value for N_As time parameter."""
        raise NotImplementedError

    @n_as_timeout.setter
    def n_as_timeout(self, value: TimeMilliseconds):
        """
        Set timeout value for N_As time parameter.

        :param value: Value of timeout to set.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def n_as_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_As time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """

    @property
    def n_ar_timeout(self) -> TimeMilliseconds:
        """Timeout value for N_Ar time parameter."""
        raise NotImplementedError

    @n_ar_timeout.setter
    def n_ar_timeout(self, value: TimeMilliseconds):
        """
        Set timeout value for N_Ar time parameter.

        :param value: Value of timeout to set.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def n_ar_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_Ar time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """

    @property
    def n_bs_timeout(self) -> TimeMilliseconds:
        """Timeout value for N_Bs time parameter."""
        raise NotImplementedError

    @n_bs_timeout.setter
    def n_bs_timeout(self, value: TimeMilliseconds):
        """
        Set timeout value for N_Bs time parameter.

        :param value: Value of timeout to set.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def n_bs_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_Bs time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """

    @property
    def n_br(self) -> TimeMilliseconds:
        """
        Get the value of N_Br time parameter which is currently set.

        .. note:: The actual (observed on the bus) value will be slightly longer as it also includes computation
            and CAN Interface delays.
        """
        raise NotImplementedError

    @n_br.setter
    def n_br(self, value: TimeMilliseconds):
        """
        Set the value of N_Br time parameter to use.

        :param value: The value to set.
        """
        raise NotImplementedError

    @property
    def n_br_max(self) -> TimeMilliseconds:
        """
        Get the maximum valid value of N_Br time parameter.

        .. warning:: To assess maximal value of :ref:`N_Br <knowledge-base-can-n-br>`, the actual value of
            :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter is required.
            Either the latest measured value of N_Ar would be used, or 0ms would be assumed (if there are
            no measurement result).
        """
        raise NotImplementedError

    @property
    def n_cs(self) -> TimeMilliseconds:
        """
        Get the value of N_Cs time parameter which is currently set.

        .. note:: The actual (observed on the bus) value will be slightly longer as it also includes computation
            and CAN Interface delays.
        """
        raise NotImplementedError

    @n_cs.setter
    def n_cs(self, value: TimeMilliseconds):
        """
        Set the value of N_Cs time parameter to use.

        :param value: The value to set.
        """
        raise NotImplementedError

    @property
    def n_cs_max(self) -> TimeMilliseconds:
        """
        Get the maximum valid value of N_Cs time parameter.

        .. warning:: To assess maximal value of :ref:`N_Cs <knowledge-base-can-n-cs>`, the actual value of
            :ref:`N_As <knowledge-base-can-n-as>` time parameter is required.
            Either the latest measured value of N_Ar would be used, or 0ms would be assumed (if there are
            no measurement result).
        """
        raise NotImplementedError

    @property
    def n_cr_timeout(self) -> TimeMilliseconds:
        """Timeout value for N_Cr time parameter."""
        raise NotImplementedError

    @n_cr_timeout.setter
    def n_cr_timeout(self, value: TimeMilliseconds):
        """
        Set timeout value for N_Cr time parameter.

        :param value: Value of timeout to set.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def n_cr_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_Cr time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """

    # Communication parameters

    @property
    def addressing_information(self) -> AbstractCanAddressingInformation:
        """Addressing Information of Transport Interface."""
        return self.__addressing_information

    @property
    def dlc(self) -> int:
        """
        Value of base CAN DLC to use for CAN Packets.

        .. note:: All output CAN Packets will have this DLC value set unless
            :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>` is used.
        """
        return self.segmenter.dlc

    @dlc.setter
    def dlc(self, value: int):
        """
        Set value of base CAN DLC to use for CAN Packets.

        :param value: Value to set.
        """
        self.segmenter.dlc = value

    @property
    def use_data_optimization(self) -> bool:
        """Information whether to use CAN Frame Data Optimization during CAN Packets creation."""
        return self.segmenter.use_data_optimization

    @use_data_optimization.setter
    def use_data_optimization(self, value: bool):
        """
        Set whether to use CAN Frame Data Optimization during CAN Packets creation.

        :param value: Value to set.
        """
        self.segmenter.use_data_optimization = value

    @property
    def filler_byte(self) -> RawByte:
        """Filler byte value to use for CAN Frame Data Padding during segmentation."""
        return self.segmenter.filler_byte

    @filler_byte.setter
    def filler_byte(self, value: RawByte):
        """
        Set value of filler byte to use for CAN Frame Data Padding.

        :param value: Value to set.
        """
        self.segmenter.filler_byte = value

    # Flow Control

    @property
    def flow_control_generator(self) -> FlowControlGeneratorAlias:
        """Get the generator of Flow Control CAN Packets."""
        return self.__flow_control_generator

    @flow_control_generator.setter
    def flow_control_generator(self, value: FlowControlGeneratorAlias):
        """
        Set the value of Flow Control generator.

        :param value: The value of Flow Control CAN Packet generator to use.
            It must be either:

            - object of `CanPacket` class - in this case the same Flow Control CAN Packet will always be used
            - generator of `CanPacket` objects - built-in functions `iter` and `next` will be used on the generator
              to restart iteration (upon reception of a new First Frame) and to produce the following
              Flow Control CAN Packets

        :raise TypeError: Provided value has unexpected type.
        """
        if not isinstance(value, (CanPacket, Iterable)):
            raise TypeError("Provided value is not CAN Packet neither CAN Packet generator.")
        self.__flow_control_generator = value
        self.__flow_control_iterator = None

    def _get_flow_control(self, is_first: bool) -> CanPacket:
        """
        Get the next Flow Control CAN Packet to send.

        .. warning:: This method is restricted for internal use and shall not be called by the user as it might cause
            malfunctioning of Flow Control CAN Packets generation.

        :param is_first: Information whether it is the first Flow Control to respond to a message.

            - True - Flow Control to return is the first Flow Control CAN Packet to send in current diagnostic message
              reception. In other words, it is the first Flow Control which directly responds to
              :ref:`First Frame <knowledge-base-can-first-frame>`.
            - False - Flow Control to return is the following Flow Control CAN Packet to send in current
              diagnostic message reception. In other words, there was at least one Flow Control already sent since
              the reception of the last :ref:`First Frame <knowledge-base-can-first-frame>`.

        :return: Flow Control CAN Packet to send in this diagnostic message reception
        """
        if isinstance(self.flow_control_generator, CanPacket):
            return self.flow_control_generator
        if is_first:
            self.__flow_control_iterator = iter(self.flow_control_generator)
        return next(self.__flow_control_iterator)

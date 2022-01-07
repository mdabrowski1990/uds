"""Abstract definition of UDS Transport Interface for CAN bus."""

__all__ = ["AbstractCanTransportInterface", "FlowControlGeneratorAlias"]


from typing import Optional, Union, Any, Iterator
from abc import abstractmethod

from uds.utilities import TimeMilliseconds, RawByte
from uds.packet import CanPacket
from uds.can import CanAddressingFormatAlias
from uds.segmentation import CanSegmenter, CanAIArgsAlias, CanAIParamsAlias
from .abstract_transport_interface import AbstractTransportInterface
from .packet_queues import PacketsQueue, TimestampedPacketsQueue


FlowControlGeneratorAlias = Union[CanPacket, Iterator[CanPacket]]
"""Alias that describes types used for :ref:`Flow Control <knowledge-base-can-flow-control>` CAN Packets generation."""


class AbstractCanTransportInterface(AbstractTransportInterface):
    """
    Abstract definition of Transport Interface for CAN bus.

    CAN Transport Interfaces are meant to handle middle layers (Transport and Network) for CAN bus.
    """

    def __init__(self,  # pylint: disable=super-init-not-called
                 bus_manager: Any,  # noqa: F841
                 max_packet_records_stored: int,  # noqa: F841
                 max_message_records_stored: int,  # noqa: F841
                 addressing_format: CanAddressingFormatAlias,  # noqa: F841
                 physical_ai: CanAIArgsAlias,  # noqa: F841
                 functional_ai: CanAIArgsAlias,  # noqa: F841
                 **kwargs: Any) -> None:  # noqa: F841
        """
        Create Transport Interface (an object for handling UDS Transport and Network layers).

        :param bus_manager: An object that handles CAN bus (Physical and Data layers of OSI Model).
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
    def segmenter(self) -> CanSegmenter:
        """Value of the segmenter used by this CAN Transport Interface."""
        raise NotImplementedError

    @property  # noqa: F841
    def _input_packets_queue(self) -> PacketsQueue:
        """Queue with records of CAN Packet that were either received or transmitted."""
        raise NotImplementedError

    @property  # noqa: F841
    def _output_packet_queue(self) -> TimestampedPacketsQueue:
        """Queue with CAN Packets that are planned for the transmission."""
        raise NotImplementedError

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

    @property  # noqa: F841
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

    @property  # noqa: F841
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

    @property  # noqa: F841
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

    @property  # noqa: F841
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

    @property  # noqa: F841
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

    @property  # noqa: F841
    @abstractmethod
    def n_cr_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_Cr time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """

    # Communication parameters

    @property
    def addressing_format(self) -> CanAddressingFormatAlias:
        """CAN Addressing format used."""
        # TODO: get from the segmenter
        raise NotImplementedError

    @property
    def physical_ai(self) -> CanAIParamsAlias:
        """CAN Addressing Information parameters used for physically addressed communication."""
        # TODO: get from the segmenter
        raise NotImplementedError

    @physical_ai.setter
    def physical_ai(self, value: CanAIArgsAlias):
        """
        Set value of CAN Addressing Information parameters to use for physically addressed communication.

        :param value: Value to set.
        """
        # TODO: set in the segmenter
        raise NotImplementedError

    @property
    def functional_ai(self) -> CanAIParamsAlias:
        """CAN Addressing Information parameters used for functionally addressed communication."""
        # TODO: get from the segmenter
        raise NotImplementedError

    @functional_ai.setter
    def functional_ai(self, value: CanAIArgsAlias):
        """
        Set value of CAN Addressing Information parameters to use for functionally addressed communication.

        :param value: Value to set.
        """
        # TODO: set in the segmenter
        raise NotImplementedError

    @property
    def dlc(self) -> int:
        """
        Value of base CAN DLC to use for CAN Packets.

        .. note:: All output CAN Packets will have this DLC value set unless
            :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>` is used.
        """
        # TODO: get from the segmenter
        raise NotImplementedError

    @dlc.setter
    def dlc(self, value: int):
        """
        Set value of base CAN DLC to use for CAN Packets.

        :param value: Value to set.
        """
        # TODO: set in the segmenter
        raise NotImplementedError

    @property
    def use_data_optimization(self) -> bool:
        """Information whether to use CAN Frame Data Optimization during CAN Packets creation."""
        # TODO: get from the segmenter
        raise NotImplementedError

    @use_data_optimization.setter
    def use_data_optimization(self, value: bool):
        """
        Set whether to use CAN Frame Data Optimization during CAN Packets creation.

        :param value: Value to set.
        """
        # TODO: set in the segmenter
        raise NotImplementedError

    @property
    def filler_byte(self) -> RawByte:
        """Filler byte value to use for CAN Frame Data Padding during segmentation."""
        # TODO: get from the segmenter
        raise NotImplementedError

    @filler_byte.setter
    def filler_byte(self, value: RawByte):
        """
        Set value of filler byte to use for CAN Frame Data Padding.

        :param value: Value to set.
        """
        # TODO: set in the segmenter
        raise NotImplementedError

    # Flow Control

    @property
    def flow_control_generator(self) -> FlowControlGeneratorAlias:
        """Get the generator of Flow Control CAN Packets."""
        raise NotImplementedError

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
        """
        raise NotImplementedError

    def _get_flow_control(self, is_first: bool) -> CanPacket:  # noqa: F841
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
        raise NotImplementedError

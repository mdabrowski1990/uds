"""Definition of UDS Transport Interface for CAN bus."""

__all__ = ["AbstractCanTransportInterface"]

from abc import ABC
from typing import Any, Optional, Tuple
from warnings import warn

from uds.addressing import TransmissionDirection
from uds.message import UdsMessageRecord
from uds.transport_interface import AbstractTransportInterface
from uds.utilities import TimeMillisecondsAlias, ValueWarning

from ..addressing import AbstractCanAddressingInformation
from ..frame import CanVersion
from ..packet import AbstractFlowControlParametersGenerator, CanPacketType, DefaultFlowControlParametersGenerator
from ..segmenter import CanSegmenter


class AbstractCanTransportInterface(AbstractTransportInterface, ABC):
    """
    Abstract definition of Transport Interface for managing Diagnostics on CAN.

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
    """Default value for :ref:`N_Br <knowledge-base-can-n-br>` time parameter."""
    DEFAULT_N_CS: Optional[TimeMillisecondsAlias] = None
    """Default value for :ref:`N_Cs <knowledge-base-can-n-cs>` time parameter."""
    DEFAULT_FLOW_CONTROL_PARAMETERS = DefaultFlowControlParametersGenerator()
    """Default values generator for :ref:`Flow Control <knowledge-base-can-flow-control>` parameters
    (:ref:`Flow Status <knowledge-base-can-flow-status>`,
    :ref:`Block Size <knowledge-base-can-block-size>`,
    :ref:`Separation Time minimum <knowledge-base-can-st-min>`)."""

    def __init__(self,
                 network_manager: Any,
                 addressing_information: AbstractCanAddressingInformation,
                 n_as_timeout: TimeMillisecondsAlias = N_AS_TIMEOUT,
                 n_ar_timeout: TimeMillisecondsAlias = N_AR_TIMEOUT,
                 n_bs_timeout: TimeMillisecondsAlias = N_BS_TIMEOUT,
                 n_cr_timeout: TimeMillisecondsAlias = N_CR_TIMEOUT,
                 n_br: TimeMillisecondsAlias = DEFAULT_N_BR,
                 n_cs: Optional[TimeMillisecondsAlias] = DEFAULT_N_CS,
                 flow_control_parameters_generator: AbstractFlowControlParametersGenerator
                 = DEFAULT_FLOW_CONTROL_PARAMETERS,
                 can_version: CanVersion = CanVersion.CLASSIC_CAN,
                 bitrate_switch: bool = False,
                 **segmenter_configuration: Any) -> None:
        """
        Create Transport Interface (an object for handling UDS Transport and Network layers).

        :param network_manager: An object that handles CAN bus (Physical and Data layers of OSI Model).
        :param addressing_information: Addressing Information configuration of a simulated node that is taking part in
            DoCAN communication.
        :param n_as_timeout: Timeout value for :ref:`N_As <knowledge-base-can-n-as>` time parameter.
        :param n_ar_timeout: Timeout value for :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter.
        :param n_bs_timeout: Timeout value for :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter.
        :param n_cr_timeout: Timeout value for :ref:`N_Cr <knowledge-base-can-n-cr>` time parameter.
        :param n_br: Value of :ref:`N_Br <knowledge-base-can-n-br>` time parameter to use in communication.
        :param n_cs: Value of :ref:`N_Cs <knowledge-base-can-n-cs>` time parameter to use in communication.
        :param flow_control_parameters_generator: Generator with Flow Control parameters to use.
        :param can_version: Version of CAN protocol to be used for packets sending.
        :param bitrate_switch: Whether bitrate switch (BRS) shall be set in sent packets.
        :param segmenter_configuration: Configuration parameters for CAN Segmenter.

            - :parameter dlc: Base CAN DLC value to use for CAN packets.
            - :parameter min_dlc: min_dlc: Minimal CAN DLC to use for CAN Packets during Data Optimization.
            - :parameter use_data_optimization: Information whether to use
                :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>`.
            - :parameter filler_byte: Filler byte value to use for
                :ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>`.
        """
        super().__init__(network_manager=network_manager)
        self.__n_ar_measured: Optional[TimeMillisecondsAlias] = None
        self.__n_as_measured: Optional[TimeMillisecondsAlias] = None
        self.__n_bs_measured: Optional[Tuple[TimeMillisecondsAlias, ...]] = None
        self.__n_cr_measured: Optional[Tuple[TimeMillisecondsAlias, ...]] = None
        self.n_as_timeout = n_as_timeout
        self.n_ar_timeout = n_ar_timeout
        self.n_bs_timeout = n_bs_timeout
        self.n_cr_timeout = n_cr_timeout
        self.n_br = n_br
        self.n_cs = n_cs
        self.flow_control_parameters_generator = flow_control_parameters_generator
        self.segmenter = CanSegmenter(addressing_information=addressing_information, **segmenter_configuration)
        self.can_version = can_version
        self.bitrate_switch = bitrate_switch

    # General

    @property
    def segmenter(self) -> CanSegmenter:
        """Get the segmenter used by this CAN Transport Interface."""
        return self.__segmenter

    @segmenter.setter
    def segmenter(self, value: CanSegmenter) -> None:
        """
        Set segmenter value for this Transport Interface.

        :param value: CAN Segmenter value to set.

        :raise TypeError: Provided value is not CAN Segmenter.
        """
        if not isinstance(value, CanSegmenter):
            raise TypeError(f"Provided value is not CAN Segmenter type. Actual type: {type(value)}.")
        self.__segmenter = value

    # Communication parameters

    @property
    def can_version(self) -> CanVersion:
        """Get version of CAN protocol to be used for packets sending."""
        return self.__can_version

    @can_version.setter
    def can_version(self, value: CanVersion) -> None:
        """
        Set version of CAN protocol to be used for packets sending.

        .. warning:: Value cross-check with other attributes (e.g. DLC) is not performed.

        .. note:: Frames with DLC > 8 will always be sent as CAN FD, regardless of this value,
            as Classic CAN cannot support DLC values greater than 8.

        :param value: Value to set.
        """
        self.__can_version = CanVersion.validate_member(value)

    @property
    def bitrate_switch(self) -> bool:
        """Get value of bitrate switch (BRS) to be used for packets sending."""
        return self.__bitrate_switch

    @bitrate_switch.setter
    def bitrate_switch(self, value: bool) -> None:
        """
        Set value of bitrate switch (BRS) to be used for packets sending.

        .. note:: This value will be ignored if CLASSICAL CAN is used.

        :param value: Value to set.
        """
        self.__bitrate_switch = bool(value)

    @property
    def dlc(self) -> int:
        """
        Value of base CAN DLC to use for output CAN packets.

        .. note:: All output CAN packets will have this DLC value set unless
            :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>` is used.
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
    def min_dlc(self) -> Optional[int]:
        """
        Value of minimal CAN DLC to use for CAN Packets during Data Optimization.

        .. note:: Output CAN Packets (created by :meth:`~uds.segmentation.can_segmenter.CanSegmenter.segmentation`)
            will never have DLC smaller than this value even if
            :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>` is used.
        """
        return self.segmenter.min_dlc

    @min_dlc.setter
    def min_dlc(self, value: Optional[int]) -> None:
        """
        Set value of minimal CAN DLC to use for CAN Packets during Data Optimization.

        :param value: Value to set.
        """
        self.segmenter.min_dlc = value

    @property
    def use_data_optimization(self) -> bool:
        """
        Information whether to use CAN Frame Data Optimization during CAN packets creation.

        .. seealso::
            :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>`
        """
        return self.segmenter.use_data_optimization

    @use_data_optimization.setter
    def use_data_optimization(self, value: bool) -> None:
        """
        Set whether to use CAN Frame Data Optimization during CAN packets creation.

        .. seealso::
            :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>`

        :param value: Value to set.
        """
        self.segmenter.use_data_optimization = value

    @property
    def filler_byte(self) -> int:
        """
        Filler byte value to use for output CAN Frame Data Padding during segmentation.

        .. seealso::
            :ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>`
        """
        return self.segmenter.filler_byte

    @filler_byte.setter
    def filler_byte(self, value: int) -> None:
        """
        Set value of filler byte to use for output CAN Frame Data Padding.

        .. seealso::
            :ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>`

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
            raise TypeError("Provided Flow Control parameters generator value has incorrect type. "
                            f"Actual type: {type(value)}.")
        self.__flow_control_parameters_generator = value

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
        :raise ValueError: Provided value is less or equal to 0.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f"Provided time parameter value must be int or float type. Actual type: {type(value)}.")
        if value <= 0:
            raise ValueError(f"Provided time parameter value must be greater than 0. Actual value: {value}")
        if value != self.N_AS_TIMEOUT:
            warn(message="Non-default value of N_As timeout was set.",
                 category=ValueWarning)
        self.__n_as_timeout = value

    @property
    def n_as_measured(self) -> Optional[TimeMillisecondsAlias]:
        """
        Get the last measured value of :ref:`N_As <knowledge-base-can-n-as>` time parameter.

        .. note:: The last measurement comes from the last transmission of Single Frame or First Fame CAN Packet using
            either :meth:`~uds.can.transport_interface.common.AbstractCanTransportInterface.send_packet`
            or :meth:`~uds.can.transport_interface.common.AbstractCanTransportInterface.async_send_packet` method.

        :return: Time in milliseconds or None if the value was never measured.
        """
        return self.__n_as_measured

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
        :raise ValueError: Provided value is less or equal to 0.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f"Provided time parameter value must be int or float type. Actual type: {type(value)}.")
        if value <= 0:
            raise ValueError(f"Provided time parameter value must be greater than 0. Actual value: {value}")
        if value != self.N_AR_TIMEOUT:
            warn(message="Non-default value of N_Ar timeout was set.",
                 category=ValueWarning)
        self.__n_ar_timeout = value

    @property
    def n_ar_measured(self) -> Optional[TimeMillisecondsAlias]:
        """
        Get the last measured value of :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter.

        .. note:: The last measurement comes from the last transmission of Flow Control CAN Packet using either
            :meth:`~uds.can.transport_interface.common.AbstractCanTransportInterface.receive_packet` or
            :meth:`~uds.can.transport_interface.common.AbstractCanTransportInterface.async_receive_packet` method.

        :return: Time in milliseconds or None if the value was never measured.
        """
        return self.__n_ar_measured

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
        :raise ValueError: Provided value is less or equal to 0.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f"Provided time parameter value must be int or float type. Actual type: {type(value)}.")
        if value <= 0:
            raise ValueError(f"Provided time parameter value must be greater than 0. Actual value: {value}")
        if value != self.N_BS_TIMEOUT:
            warn(message="Non-default value of N_Bs timeout was set.",
                 category=ValueWarning)
        self.__n_bs_timeout = value

    @property
    def n_bs_measured(self) -> Optional[Tuple[TimeMillisecondsAlias, ...]]:
        """
        Get the last measured values of :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter.

        .. note:: The last measurement comes from the last transmission of UDS message using either
            :meth:`~uds.transport_interface.addressing.AbstractCanTransportInterface.send_message` or
            :meth:`~uds.transport_interface.addressing.AbstractCanTransportInterface.async_send_message` method.

        :return: Tuple with times in milliseconds or None if the values could not be measured.
        """
        return self.__n_bs_measured

    @property
    def n_br(self) -> TimeMillisecondsAlias:
        """
        Get the value of :ref:`N_Br <knowledge-base-can-n-br>` time parameter which is currently set.

        .. note:: The actual (observed on the bus) value will be slightly longer as it also includes computation
            and CAN Interface delays.
        """
        return self.__n_br

    @n_br.setter
    def n_br(self, value: TimeMillisecondsAlias) -> None:
        """
        Set the value of :ref:`N_Br <knowledge-base-can-n-br>` time parameter to use.

        :param value: The value to set.

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided value is out of range (0 <= value < MAX N_Br).
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f"Provided time parameter value must be int or float type. Actual type: {type(value)}.")
        if not 0 <= value < self.n_br_max:
            raise ValueError("Provided time parameter value is out of range. "
                             f"Expected: 0 <= value < {self.n_br_max}. Actual value: {value}.")
        self.__n_br = value

    @property
    def n_br_max(self) -> TimeMillisecondsAlias:
        """
        Get the maximum valid value of :ref:`N_Br <knowledge-base-can-n-br>` time parameter.

        .. warning:: To assess maximal value of :ref:`N_Br <knowledge-base-can-n-br>`, the actual value of
            :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter is required.
            Either the latest measured value of :ref:`N_Ar <knowledge-base-can-n-ar>` would be used,
            or 0ms would be assumed (if there are no measurement result).
        """
        n_ar_measured = 0 if self.n_ar_measured is None else self.n_ar_measured
        return 0.9 * self.n_bs_timeout - n_ar_measured

    @property
    def n_cs(self) -> Optional[TimeMillisecondsAlias]:
        """
        Get the value of :ref:`N_Cs <knowledge-base-can-n-cs>` time parameter which is currently set.

        .. note:: The actual (observed on the bus) value will be slightly longer as it also includes computation
            and CAN Interface delays.
        """
        return self.__n_cs

    @n_cs.setter
    def n_cs(self, value: Optional[TimeMillisecondsAlias]) -> None:
        """
        Set the value of :ref:`N_Cs <knowledge-base-can-n-cs>` time parameter to use.

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
                raise TypeError(f"Provided time parameter value must be int or float type. Actual type: {type(value)}.")
            if not 0 <= value < self.n_cs_max:
                raise ValueError("Provided time parameter value is out of range. "
                                 f"Expected: 0 <= value < {self.n_cs_max}. Actual value: {value}.")
        self.__n_cs = value

    @property
    def n_cs_max(self) -> TimeMillisecondsAlias:
        """
        Get the maximum valid value of :ref:`N_Cs <knowledge-base-can-n-cs>` time parameter.

        .. warning:: To assess maximal value of :ref:`N_Cs <knowledge-base-can-n-cs>`, the actual value of
            :ref:`N_As <knowledge-base-can-n-as>` time parameter is required.
            Either the latest measured value of :ref:`N_As <knowledge-base-can-n-as>` would be used,
            or 0ms would be assumed (if there are no measurement result).
        """
        n_as_measured = 0 if self.n_as_measured is None else self.n_as_measured
        return 0.9 * self.n_cr_timeout - n_as_measured

    @property
    def n_cr_timeout(self) -> TimeMillisecondsAlias:
        """Timeout value for :ref:`N_Cr <knowledge-base-can-n-cr>` time parameter."""
        return self.__n_cr_timeout

    @n_cr_timeout.setter
    def n_cr_timeout(self, value: TimeMillisecondsAlias) -> None:
        """
        Set timeout value for :ref:`N_Cr <knowledge-base-can-n-cr>` time parameter.

        :param value: Value of timeout to set.

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided value is less or equal to 0.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f"Provided time parameter value must be int or float type. Actual type: {type(value)}.")
        if value <= 0:
            raise ValueError(f"Provided time parameter value must be greater than 0. Actual value: {value}")
        if value != self.N_CR_TIMEOUT:
            warn(message="Non-default value of N_Cr timeout was set.",
                 category=ValueWarning)
        self.__n_cr_timeout = value

    @property
    def n_cr_measured(self) -> Optional[Tuple[TimeMillisecondsAlias, ...]]:
        """
        Get the last measured values of :ref:`N_Cr <knowledge-base-can-n-cr>` time parameter.

        .. note:: The last measurement comes from the last reception of UDS message using either
            :meth:`~uds.transport_interface.addressing.AbstractCanTransportInterface.receive_message` or
            :meth:`~uds.transport_interface.addressing.AbstractCanTransportInterface.async_receive_message` method.

        :return: Tuple with times in milliseconds or None if the values could not be measured.
        """
        return self.__n_cr_measured

    def _update_n_ar_measured(self, value: TimeMillisecondsAlias) -> None:
        """
        Update measured values of :ref:`N_Ar <knowledge-base-can-n-ar>`.

        :param value: Value to set.

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided value is out of range.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f"Provided value is not int or float type. Actual type: {type(value)}.")
        if value < 0:
            raise ValueError(f"Provided time parameter cannot be a negative number. Actual value: {value}")
        if value > self.n_ar_timeout:
            warn("Measured value of N_Ar was greater than N_Ar timeout.",
                 category=ValueWarning)
        self.__n_ar_measured = value

    def _update_n_as_measured(self, value: TimeMillisecondsAlias) -> None:
        """
        Update measured values of :ref:`N_As <knowledge-base-can-n-as>`.

        :param value: Value to set.

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided value is out of range.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f"Provided value is not int or float type. Actual type: {type(value)}.")
        if value < 0:
            raise ValueError(f"Provided time parameter cannot be a negative number. Actual value: {value}")
        if value > self.n_as_timeout:
            warn("Measured value of N_As was greater than N_As timeout.",
                 category=ValueWarning)
        self.__n_as_measured = value

    def _update_n_bs_measured(self, message_record: UdsMessageRecord) -> None:
        """
        Update measured values of :ref:`N_Bs <knowledge-base-can-n-bs>` according to timestamps of CAN packet records.

        :param message_record: Record of UDS message transmitted over CAN.

        :raise TypeError: Provided value is not UDS message record.
        :raise ValueError: Provided UDS message record was not transmitted.
        """
        if not isinstance(message_record, UdsMessageRecord):
            raise TypeError(f"Provided value is not UDS Message Record type. Actual type: {type(message_record)}.")
        if message_record.direction != TransmissionDirection.TRANSMITTED:
            raise ValueError("Provided UDS Message Record was not transmitted.")
        if len(message_record.packets_records) == 1:
            self.__n_bs_measured = None
        else:
            n_bs_measured = []
            for i, packet_record in enumerate(message_record.packets_records[1:]):
                if packet_record.packet_type == CanPacketType.FLOW_CONTROL:
                    n_bs = (packet_record.transmission_timestamp
                            - message_record.packets_records[i].transmission_timestamp)
                    n_bs_measured.append(round(n_bs * 1000, 3))
            self.__n_bs_measured = tuple(n_bs_measured)

    def _update_n_cr_measured(self, message_record: UdsMessageRecord) -> None:
        """
        Update measured values of :ref:`N_Cr <knowledge-base-can-n-cr>` according to timestamps of CAN packet records.

        :param message_record: Record of UDS message received over CAN.

        :raise TypeError: Provided value is not UDS message record.
        :raise ValueError: Provided UDS message record was not received.
        """
        if not isinstance(message_record, UdsMessageRecord):
            raise TypeError(f"Provided value is not UDS Message Record type. Actual type: {type(message_record)}.")
        if message_record.direction != TransmissionDirection.RECEIVED:
            raise ValueError("Provided UDS Message Record was not received.")
        if len(message_record.packets_records) == 1:
            self.__n_cr_measured = None
        else:
            n_cr_measured = []
            for i, packet_record in enumerate(message_record.packets_records[1:]):
                if packet_record.packet_type == CanPacketType.CONSECUTIVE_FRAME:
                    n_cr = (packet_record.transmission_timestamp
                            - message_record.packets_records[i].transmission_timestamp)
                    n_cr_measured.append(round(n_cr * 1000, 3))
            self.__n_cr_measured = tuple(n_cr_measured)

    def clear_measurements(self) -> None:
        """Clear measured values of CAN communication parameters."""
        self.__n_ar_measured = None
        self.__n_as_measured = None
        self.__n_bs_measured = None
        self.__n_cr_measured = None

"""Definition and implementation of UDS Transport Interface for CAN bus."""

__all__ = ["AbstractCanTransportInterface", "PyCanTransportInterface"]

from abc import abstractmethod
from asyncio import AbstractEventLoop, get_running_loop, wait_for
from datetime import datetime
from time import time
from typing import Any, List, Optional, Tuple, Union
from warnings import warn

from can import AsyncBufferedReader, BufferedReader, BusABC, Message, Notifier
from uds.can import (
    AbstractCanAddressingInformation,
    AbstractFlowControlParametersGenerator,
    CanDlcHandler,
    CanFlowStatus,
    CanIdHandler,
    CanSTminTranslator,
    DefaultFlowControlParametersGenerator,
)
from uds.message import UdsMessage, UdsMessageRecord
from uds.packet import CanPacket, CanPacketRecord, CanPacketType
from uds.segmentation import CanSegmenter
from uds.transmission_attributes import TransmissionDirection
from uds.utilities import (
    TimeMillisecondsAlias,
    MessageTransmissionError,
    UnexpectedPacketReceptionWarning,
    ValueWarning,
    MessageReceptionWarning
)

from .abstract_transport_interface import AbstractTransportInterface


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
    """Default value of :ref:`Flow Control <knowledge-base-can-flow-control>` parameters (
    :ref:`Flow Status <knowledge-base-can-flow-status>`, :ref:`Block Size <knowledge-base-can-block-size>`,
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
            - :parameter use_data_optimization: Information whether to use CAN Frame Data Optimization.
            - :parameter filler_byte: Filler byte value to use for CAN Frame Data Padding.
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
        Update measured values of N_Bs according to timestamps of CAN packet records.

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
        Update measured values of N_Cr according to timestamps of CAN packet records.

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
    def n_as_timeout(self, value: TimeMillisecondsAlias):
        """
        Set timeout value for :ref:`N_As <knowledge-base-can-n-as>` time parameter.

        :param value: Value of timeout to set.

        :raise TypeError: Provided value is not int or float.
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

        :return: Time in milliseconds or None if the value was never measured.
        """

    @property
    def n_ar_timeout(self) -> TimeMillisecondsAlias:
        """Timeout value for :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter."""
        return self.__n_ar_timeout

    @n_ar_timeout.setter
    def n_ar_timeout(self, value: TimeMillisecondsAlias):
        """
        Set timeout value for :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter.

        :param value: Value of timeout to set.

        :raise TypeError: Provided value is not int or float.
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

        :return: Time in milliseconds or None if the value was never measured.
        """

    @property
    def n_bs_timeout(self) -> TimeMillisecondsAlias:
        """Timeout value for :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter."""
        return self.__n_bs_timeout

    @n_bs_timeout.setter
    def n_bs_timeout(self, value: TimeMillisecondsAlias):
        """
        Set timeout value for :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter.

        :param value: Value of timeout to set.

        :raise TypeError: Provided value is not int or float.
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
        Get the last measured values of :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter.

        .. note:: The last measurement comes from the last transmission of UDS message using either
            :meth:`~uds.transport_interface.can_transport_interface.AbstractCanTransportInterface.send_message`
            :meth:`~uds.transport_interface.can_transport_interface.AbstractCanTransportInterface.async_send_message`
            method.

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
    def n_br(self, value: TimeMillisecondsAlias):
        """
        Set the value of :ref:`N_Br <knowledge-base-can-n-br>` time parameter to use.

        :param value: The value to set.

        :raise TypeError: Provided value is not int or float.
        :raise ValueError: Provided value is out of range.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided time parameter value must be int or float type.")
        if not 0 <= value < self.n_br_max:
            raise ValueError("Provided time parameter value is out of range.")
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
    def n_cs(self, value: Optional[TimeMillisecondsAlias]):
        """
        Set the value of :ref:`N_Cs <knowledge-base-can-n-cs>` time parameter to use.

        :param value: The value to set.
            - None - use timing compatible with STmin value received in a preceding Flow Control packet
            - int/float type - timing value to be used regardless of a received STmin value

        :raise TypeError: Provided value is not int or float.
        :raise ValueError: Provided value is out of range.
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
    def n_cr_timeout(self, value: TimeMillisecondsAlias):
        """
        Set timeout value for :ref:`N_Cr <knowledge-base-can-n-cr>` time parameter.

        :param value: Value of timeout to set.

        :raise TypeError: Provided value is not int or float.
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
        Get the last measured values of :ref:`N_Cr <knowledge-base-can-n-cr>` time parameter.

        .. note:: The last measurement comes from the last reception of UDS message using either
            :meth:`~uds.transport_interface.can_transport_interface.AbstractCanTransportInterface.receive_message`
            :meth:`~uds.transport_interface.can_transport_interface.AbstractCanTransportInterface.async_receive_message`
            method.

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
            :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>` is used.
        """
        return self.segmenter.dlc

    @dlc.setter
    def dlc(self, value: int):
        """
        Set value of base CAN DLC to use for output CAN packets.

        :param value: Value to set.
        """
        self.segmenter.dlc = value

    @property
    def use_data_optimization(self) -> bool:
        """Information whether to use CAN Frame Data Optimization during CAN packets creation."""
        return self.segmenter.use_data_optimization

    @use_data_optimization.setter
    def use_data_optimization(self, value: bool):
        """
        Set whether to use CAN Frame Data Optimization during CAN packets creation.

        :param value: Value to set.
        """
        self.segmenter.use_data_optimization = value

    @property
    def filler_byte(self) -> int:
        """Filler byte value to use for output CAN Frame Data Padding during segmentation."""
        return self.segmenter.filler_byte

    @filler_byte.setter
    def filler_byte(self, value: int):
        """
        Set value of filler byte to use for output CAN Frame Data Padding.

        :param value: Value to set.
        """
        self.segmenter.filler_byte = value

    @property
    def flow_control_parameters_generator(self) -> AbstractFlowControlParametersGenerator:
        """Get generator of Flow Control parameters (Flow Status, Block Size, Separation Time minimum)."""
        return self.__flow_control_parameters_generator

    @flow_control_parameters_generator.setter
    def flow_control_parameters_generator(self, value: AbstractFlowControlParametersGenerator):
        """
        Set value of Flow Control parameters (Flow Status, Block Size, Separation Time minimum) generator.

        :param value: Value to set.
        """
        if not isinstance(value, AbstractFlowControlParametersGenerator):
            raise TypeError("Provided Flow Control parameters generator value has incorrect type.")
        self.__flow_control_parameters_generator = value


class PyCanTransportInterface(AbstractCanTransportInterface):
    """
    Transport Interface for managing UDS on CAN with python-can package as bus handler.

    .. note:: Documentation for python-can package: https://python-can.readthedocs.io/
    """

    _MAX_LISTENER_TIMEOUT: float = 4280000.  # ms
    """Maximal timeout value accepted by python-can listeners."""
    _MIN_NOTIFIER_TIMEOUT: float = 0.001  # s
    """Minimal timeout for notifiers that does not cause malfunctioning of listeners."""

    def __init__(self,
                 can_bus_manager: BusABC,
                 addressing_information: AbstractCanAddressingInformation,
                 **kwargs: Any) -> None:
        """
        Create python-can Transport Interface.

        :param can_bus_manager: Python-can bus object for handling CAN.

            .. warning:: Bus must have capability of receiving transmitted frames (``receive_own_messages=True`` set).

        :param addressing_information: Addressing Information of CAN Transport Interface.
        :param kwargs: Optional arguments that are specific for CAN bus.

            - :parameter n_as_timeout: Timeout value for :ref:`N_As <knowledge-base-can-n-as>` time parameter.
            - :parameter n_ar_timeout: Timeout value for :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter.
            - :parameter n_bs_timeout: Timeout value for :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter.
            - :parameter n_br: Value of :ref:`N_Br <knowledge-base-can-n-br>` time parameter to use in communication.
            - :parameter n_cs: Value of :ref:`N_Cs <knowledge-base-can-n-cs>` time parameter to use in communication.
            - :parameter n_cr_timeout: Timeout value for :ref:`N_Cr <knowledge-base-can-n-cr>` time parameter.
            - :parameter dlc: Base CAN DLC value to use for CAN packets.
            - :parameter use_data_optimization: Information whether to use CAN Frame Data Optimization.
            - :parameter filler_byte: Filler byte value to use for CAN Frame Data Padding.
            - :parameter flow_control_parameters_generator: Generator with Flow Control parameters to use.
        """
        self.__n_as_measured: Optional[TimeMillisecondsAlias] = None
        self.__n_ar_measured: Optional[TimeMillisecondsAlias] = None
        super().__init__(can_bus_manager=can_bus_manager,
                         addressing_information=addressing_information,
                         **kwargs)
        self.__frames_buffer = BufferedReader()
        self.__notifier: Optional[Notifier] = None
        self.__async_frames_buffer = AsyncBufferedReader()
        self.__async_notifier: Optional[Notifier] = None

    def __del__(self):
        """Safely close all threads open by this object."""
        self._teardown_notifier(suppress_warning=True)
        self._teardown_async_notifier(suppress_warning=True)

    @property
    def n_as_measured(self) -> Optional[TimeMillisecondsAlias]:
        """
        Get the last measured value of :ref:`N_As <knowledge-base-can-n-as>` time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """
        return self.__n_as_measured

    @property
    def n_ar_measured(self) -> Optional[TimeMillisecondsAlias]:
        """
        Get the last measured value of :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """
        return self.__n_ar_measured

    def _teardown_notifier(self, suppress_warning: bool = False) -> None:
        """
        Stop and remove CAN frame notifier for synchronous communication.

        :param suppress_warning: Do not warn about mixing Synchronous and Asynchronous implementation.
        """
        if self.__notifier is not None:
            self.__notifier.stop(self._MIN_NOTIFIER_TIMEOUT)
            self.__notifier = None
            if not suppress_warning:
                warn(message="Asynchronous (`PyCanTransportInterface.async_send_packet`, "
                             "`PyCanTransportInterface.async_receive_packet methods`) "
                             "and synchronous (`PyCanTransportInterface.send_packet`, "
                             "`PyCanTransportInterface.receive_packet methods`) shall not be used together.",
                     category=UserWarning)

    def _teardown_async_notifier(self, suppress_warning: bool = False) -> None:
        """
        Stop and remove CAN frame notifier for asynchronous communication.

        :param suppress_warning: Do not warn about mixing Synchronous and Asynchronous implementation.
        """
        if self.__async_notifier is not None:
            self.__async_notifier.stop(self._MIN_NOTIFIER_TIMEOUT)
            self.__async_notifier = None
            if not suppress_warning:
                warn(message="Asynchronous (`PyCanTransportInterface.async_send_packet`, "
                             "`PyCanTransportInterface.async_receive_packet methods`) "
                             "and synchronous (`PyCanTransportInterface.send_packet`, "
                             "`PyCanTransportInterface.receive_packet methods`) shall not be used together.",
                     category=UserWarning)

    def _setup_notifier(self) -> None:
        """Configure CAN frame notifier for synchronous communication."""
        self._teardown_async_notifier()
        if self.__notifier is None:
            self.__notifier = Notifier(bus=self.bus_manager,
                                       listeners=[self.__frames_buffer],
                                       timeout=self._MIN_NOTIFIER_TIMEOUT)

    def _setup_async_notifier(self, loop: AbstractEventLoop) -> None:
        """
        Configure CAN frame notifier for asynchronous communication.

        :param loop: An :mod:`asyncio` event loop to use.
        """
        self._teardown_notifier()
        if self.__async_notifier is None:
            self.__async_notifier = Notifier(bus=self.bus_manager,
                                             listeners=[self.__async_frames_buffer],
                                             timeout=self._MIN_NOTIFIER_TIMEOUT,
                                             loop=loop)

    def _send_cf_packets_block(self,
                               cf_packets_block: List[CanPacket],
                               delay: TimeMillisecondsAlias) -> Tuple[CanPacketRecord, ...]:
        """
        Send block of Consecutive Frame CAN packets.

        :param cf_packets_block: Consecutive Frame CAN packets to send.
        :param delay: Minimal delay between sending following Consecutive Frames [ms].

        :raise TransmissionInterruptionError: A new UDS message transmission was started while sending this message.

        :return: Records with historic information about transmitted Consecutive Frame CAN packets.
        """
        packet_records = []
        for cf_packet in cf_packets_block:
            time_now_ms = time() * 1000
            time_end_ms = time_now_ms + delay
            while time_now_ms < time_end_ms:
                try:
                    received_packet = self.receive_packet(timeout=time_end_ms - time_now_ms)
                except TimeoutError:
                    pass
                else:
                    if CanPacketType.is_initial_packet_type(received_packet.packet_type):
                        raise MessageTransmissionError("A new UDS message transmission was started while sending "
                                                       "this message.")
                    warn(message="An unrelated CAN packet was received during UDS message transmission.",
                         category=UnexpectedPacketReceptionWarning)
                time_now_ms = time() * 1000
            packet_records.append(self.send_packet(cf_packet))
        return tuple(packet_records)

    async def _async_send_cf_packets_block(self,
                                           cf_packets_block: List[CanPacket],
                                           delay: TimeMillisecondsAlias,
                                           loop: Optional[AbstractEventLoop] = None) -> Tuple[CanPacketRecord, ...]:
        """
        Send block of Consecutive Frame CAN packets asynchronously.

        :param cf_packets_block: Consecutive Frame CAN packets to send.
        :param delay: Minimal delay between sending following Consecutive Frames [ms].
        :param loop: An asyncio event loop to use for scheduling this task.

        :raise TransmissionInterruptionError: A new UDS message transmission was started while sending this message.

        :return: Records with historic information about transmitted Consecutive Frame CAN packets.
        """
        packet_records = []
        for cf_packet in cf_packets_block:
            time_now_ms = time() * 1000
            time_end_ms = time_now_ms + delay
            while time_now_ms < time_end_ms:
                try:
                    received_packet = await self.async_receive_packet(timeout=time_end_ms - time_now_ms, loop=loop)
                except TimeoutError:
                    pass
                else:
                    if CanPacketType.is_initial_packet_type(received_packet.packet_type):
                        raise MessageTransmissionError("A new UDS message transmission was started while sending "
                                                       "this message.")
                    warn(message="An unrelated CAN packet was received during UDS message transmission.",
                         category=UnexpectedPacketReceptionWarning)
                time_now_ms = time() * 1000
            packet_records.append(await self.async_send_packet(cf_packet, loop=loop))
        return tuple(packet_records)

    def _receive_cf_packets_block(self, sequence_number: int, block_size: int, remaining_data_length: int) \
            -> Union[UdsMessageRecord, Tuple[CanPacketRecord, ...]]:
        """
        Receive block of Consecutive Frames.

        :param sequence_number: Current Sequence Number (next Consecutive Frame shall have this value set).
        :param block_size: Block Size value sent in the last Flow Control CAN packet.
        :param remaining_data_length: Number of remaining data bytes to receive in UDS message.

        :raise NotImplementedError: Unhandled CAN packet starting a new CAN message transmission was received.

        :return: Either:
            - Record of UDS message if reception was interrupted by a new UDS message transmission.
            - Tuple with records of received Consecutive Frames.
        """
        received_cf = []
        received_payload_size = 0
        remaining_timeout = self.n_cr_timeout
        time_start_ms = time() * 1000
        while received_payload_size < remaining_data_length and (len(received_cf) != block_size or block_size == 0):
            received_packet = self.receive_packet(timeout=remaining_timeout)
            if CanPacketType.is_initial_packet_type(received_packet.packet_type):
                warn(message="A new UDS message is transmitted. Aborted reception of previous message.",
                     category=MessageReceptionWarning)
                if received_packet.packet_type == CanPacketType.SINGLE_FRAME:
                    return UdsMessageRecord([received_packet])
                if received_packet.packet_type == CanPacketType.FIRST_FRAME:
                    return self._receive_consecutive_frames(first_frame=received_packet)
                raise NotImplementedError(f"CAN packet of unhandled type was received.")
            if (received_packet.packet_type == CanPacketType.CONSECUTIVE_FRAME
                    and received_packet.sequence_number == sequence_number):
                received_cf.append(received_packet)
                received_payload_size += len(received_packet.payload)
                sequence_number = (received_packet.sequence_number + 1) & 0xF
                remaining_timeout = self.n_cr_timeout
                time_start_ms = time() * 1000
            else:
                warn(message="An unrelated CAN packet was received during UDS message transmission.",
                     category=UnexpectedPacketReceptionWarning)
                time_now_ms = time() * 1000
                remaining_timeout = (time_start_ms + self.n_cr_timeout) - time_now_ms
        return tuple(received_cf)

    def _receive_consecutive_frames(self, first_frame: CanPacketRecord) -> UdsMessageRecord:
        """
        Receive Consecutive Frames after reception of First Frame.

        :param first_frame: First Frame that was received.

        :raise TimeoutError: :ref:`N_Cr <knowledge-base-can-n-cr> timeout was reached.
        :raise OverflowError: Flow Control packet with Flow Status equal to OVERFLOW was sent.
        :raise NotImplementedError: Unhandled CAN packet starting a new CAN message transmission was received.

        :return: Record of UDS message that was formed provided First Frame and received Consecutive Frames.
        """
        packets_records = [first_frame]
        message_data_length = first_frame.data_length
        received_data_length = len(first_frame.payload)
        sequence_number = 1
        flow_control_iterator = iter(self.flow_control_parameters_generator)
        while True:
            try:
                received_packet = self.receive_packet(timeout=self.n_br)
            except (TimeoutError, ValueError):
                pass
            else:
                if CanPacketType.is_initial_packet_type(received_packet.packet_type):
                    warn(message="A new UDS message is transmitted. Aborted reception of previous message.",
                         category=MessageReceptionWarning)
                    if received_packet.packet_type == CanPacketType.SINGLE_FRAME:
                        return UdsMessageRecord([received_packet])
                    if received_packet.packet_type == CanPacketType.FIRST_FRAME:
                        return self._receive_consecutive_frames(first_frame=received_packet)
                    raise NotImplementedError(f"CAN packet of unhandled type was received.")
                else:
                    warn(message="An unrelated CAN packet was received during UDS message transmission.",
                         category=UnexpectedPacketReceptionWarning)
            flow_status, block_size, st_min = next(flow_control_iterator)
            fc_packet = self.segmenter.get_flow_control_packet(flow_status=flow_status,
                                                               block_size=block_size,
                                                               st_min=st_min)
            packets_records.append(self.send_packet(fc_packet))
            if flow_status == CanFlowStatus.Overflow:
                raise OverflowError("Flow Control with Flow Status `OVERFLOW` was transmitted.")
            if flow_status == CanFlowStatus.ContinueToSend:
                remaining_data_length = message_data_length - received_data_length
                cf_block = self._receive_cf_packets_block(sequence_number=sequence_number,
                                                          block_size=block_size,
                                                          remaining_data_length=remaining_data_length)
                if isinstance(cf_block, UdsMessageRecord):  # handle in case another message interrupted
                    return cf_block
                packets_records.extend(cf_block)
                received_data_length += len(cf_block[0].payload) * len(cf_block)
                if received_data_length >= message_data_length:
                    break
                sequence_number = (cf_block[-1].sequence_number + 1) & 0xF
        return UdsMessageRecord(packets_records)

    async def _async_receive_consecutive_frames(self,
                                                first_frame: CanPacketRecord,
                                                loop: Optional[AbstractEventLoop] = None) -> UdsMessageRecord:
        ...

    def clear_frames_buffers(self) -> None:
        """
        Clear buffers with transmitted and received frames.

        .. warning:: This will cause that all CAN packets received in a past are no longer accessible.
        """
        for _ in range(self.__frames_buffer.buffer.qsize()):
            self.__frames_buffer.buffer.get_nowait()
        for _ in range(self.__async_frames_buffer.buffer.qsize()):
            self.__async_frames_buffer.buffer.get_nowait()

    @staticmethod
    def is_supported_bus_manager(bus_manager: Any) -> bool:
        """
        Check whether provided value is a bus manager that is supported by this Transport Interface.

        :param bus_manager: Value to check.

        :return: True if provided bus object is compatible with this Transport Interface, False otherwise.
        """
        return isinstance(bus_manager, BusABC)

    def send_packet(self, packet: CanPacket) -> CanPacketRecord:  # type: ignore
        """
        Transmit CAN packet.

        .. warning:: Must not be called within an asynchronous function.

        :param packet: CAN packet to send.

        :raise TypeError: Provided packet is not CAN packet.
        :raise TimeoutError: Timeout was reached before a CAN packet could be transmitted.

        :return: Record with historic information about transmitted CAN packet.
        """
        if not isinstance(packet, CanPacket):
            raise TypeError("Provided packet value does not contain a CAN packet.")
        is_flow_control_packet = packet.packet_type == CanPacketType.FLOW_CONTROL
        self._setup_notifier()
        self.clear_frames_buffers()
        can_frame = Message(arbitration_id=packet.can_id,
                            is_extended_id=CanIdHandler.is_extended_can_id(packet.can_id),
                            data=packet.raw_frame_data,
                            is_fd=CanDlcHandler.is_can_fd_specific_dlc(packet.dlc))
        timeout_s = (self.n_ar_timeout if is_flow_control_packet else self.n_as_timeout) / 1000.
        time_start_s = time()
        self.bus_manager.send(can_frame)
        observed_frame = None
        while observed_frame is None \
                or observed_frame.arbitration_id != packet.can_id \
                or tuple(observed_frame.data) != packet.raw_frame_data \
                or not observed_frame.is_rx:
            timeout_left = timeout_s - (time() - time_start_s)
            if timeout_left <= 0:
                raise TimeoutError("Timeout was reached before observing a CAN packet being transmitted.")
            observed_frame = self.__frames_buffer.get_message(timeout=timeout_left)
        time_sent_s = time()
        if is_flow_control_packet:
            # Temporary solution due to https://github.com/mdabrowski1990/uds/issues/228
            # self.__n_ar_measured = (observed_frame.timestamp - time_start) * 1000.
            self.__n_ar_measured = (time_sent_s - time_start_s) * 1000.
        else:
            # Temporary solution due to https://github.com/mdabrowski1990/uds/issues/228
            # self.__n_as_measured = (observed_frame.timestamp - time_start) * 1000.
            self.__n_as_measured = (time_sent_s - time_start_s) * 1000.
        return CanPacketRecord(frame=observed_frame,
                               direction=TransmissionDirection.TRANSMITTED,
                               addressing_type=packet.addressing_type,
                               addressing_format=packet.addressing_format,
                               transmission_time=datetime.fromtimestamp(observed_frame.timestamp))

    async def async_send_packet(self,
                                packet: CanPacket,  # type: ignore
                                loop: Optional[AbstractEventLoop] = None) -> CanPacketRecord:
        """
        Transmit asynchronously CAN packet.

        :param packet: CAN packet to send.
        :param loop: An asyncio event loop used for observing messages.

        :raise TypeError: Provided packet is not CAN packet.
        :raise TimeoutError: Timeout was reached before a CAN packet could be transmitted.

        :return: Record with historic information about transmitted CAN packet.
        """
        if not isinstance(packet, CanPacket):
            raise TypeError("Provided packet value does not contain a CAN packet.")
        loop = get_running_loop() if loop is None else loop
        is_flow_control_packet = packet.packet_type == CanPacketType.FLOW_CONTROL
        self._setup_async_notifier(loop)
        self.clear_frames_buffers()
        can_frame = Message(arbitration_id=packet.can_id,
                            is_extended_id=CanIdHandler.is_extended_can_id(packet.can_id),
                            data=packet.raw_frame_data,
                            is_fd=CanDlcHandler.is_can_fd_specific_dlc(packet.dlc))
        timeout_s = (self.n_ar_timeout if is_flow_control_packet else self.n_as_timeout) / 1000.
        time_start_s = time()
        self.bus_manager.send(can_frame)
        observed_frame = None
        while observed_frame is None \
                or observed_frame.arbitration_id != packet.can_id \
                or tuple(observed_frame.data) != packet.raw_frame_data \
                or not observed_frame.is_rx:
            timeout_left = timeout_s - (time() - time_start_s)
            if timeout_left <= 0:
                raise TimeoutError("Timeout was reached before a CAN packet could be transmitted.")
            observed_frame = await wait_for(self.__async_frames_buffer.get_message(), timeout=timeout_left)
        time_sent_s = time()
        if is_flow_control_packet:
            # Temporary solution due to https://github.com/mdabrowski1990/uds/issues/228
            # self.__n_ar_measured = (observed_frame.timestamp - time_start) * 1000.
            self.__n_ar_measured = (time_sent_s - time_start_s) * 1000.
        else:
            # Temporary solution due to https://github.com/mdabrowski1990/uds/issues/228
            # self.__n_as_measured = (observed_frame.timestamp - time_start) * 1000.
            self.__n_as_measured = (time_sent_s - time_start_s) * 1000.
        return CanPacketRecord(frame=observed_frame,
                               direction=TransmissionDirection.TRANSMITTED,
                               addressing_type=packet.addressing_type,
                               addressing_format=packet.addressing_format,
                               transmission_time=datetime.fromtimestamp(observed_frame.timestamp))

    def receive_packet(self, timeout: Optional[TimeMillisecondsAlias] = None) -> CanPacketRecord:
        """
        Receive CAN packet.

        .. warning:: Must not be called within an asynchronous function.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TypeError: Provided timeout value is not None neither int nor float type.
        :raise ValueError: Provided timeout value is less or equal 0.
        :raise TimeoutError: Timeout was reached before a CAN packet was received.

        :return: Record with historic information about received CAN packet.
        """
        if timeout is not None:
            if not isinstance(timeout, (int, float)):
                raise TypeError("Provided timeout value is not None neither int nor float type.")
            if timeout <= 0:
                raise ValueError("Provided timeout value is less or equal 0.")
        self._setup_notifier()
        packet_addressing_type = None
        if timeout is not None:
            time_end_ms = (time() * 1000) + timeout
        while packet_addressing_type is None:
            if timeout is not None:
                time_now_ms = time() * 1000
                if time_end_ms <= time_now_ms:
                    raise TimeoutError("Timeout was reached before a CAN packet was received.")
                timeout = time_end_ms - time_now_ms
            timeout_left = self._MAX_LISTENER_TIMEOUT if timeout is None else timeout / 1000.
            received_frame = self.__frames_buffer.get_message(timeout=timeout_left)
            if received_frame is None:
                raise TimeoutError("Timeout was reached before a CAN packet was received.")
            packet_addressing_type = self.segmenter.is_input_packet(can_id=received_frame.arbitration_id,
                                                                    data=received_frame.data)
        return CanPacketRecord(frame=received_frame,
                               direction=TransmissionDirection.RECEIVED,
                               addressing_type=packet_addressing_type,
                               addressing_format=self.segmenter.addressing_format,
                               transmission_time=datetime.fromtimestamp(received_frame.timestamp))

    async def async_receive_packet(self,
                                   timeout: Optional[TimeMillisecondsAlias] = None,
                                   loop: Optional[AbstractEventLoop] = None) -> CanPacketRecord:
        """
        Receive asynchronously CAN packet.

        :param timeout: Maximal time (in milliseconds) to wait.
        :param loop: An asyncio event loop used for observing messages.

        :raise TypeError: Provided timeout value is not None neither int nor float type.
        :raise ValueError: Provided timeout value is less or equal 0.
        :raise TimeoutError: Timeout was reached before a CAN packet was received.

        :return: Record with historic information about received CAN packet.
        """
        if timeout is not None:
            if not isinstance(timeout, (int, float)):
                raise TypeError("Provided timeout value is not None neither int nor float type.")
            if timeout <= 0:
                raise ValueError("Provided timeout value is less or equal 0.")
        loop = get_running_loop() if loop is None else loop
        self._setup_async_notifier(loop)
        packet_addressing_type = None
        if timeout is not None:
            time_end_ms = (time() * 1000) + timeout
        while packet_addressing_type is None:
            if timeout is not None:
                time_now_ms = time() * 1000
                if time_end_ms <= time_now_ms:
                    raise TimeoutError("Timeout was reached before a UDS message was received.")
                timeout = time_end_ms - time_now_ms
            received_frame = await wait_for(self.__async_frames_buffer.get_message(),
                                            timeout=None if timeout is None else timeout / 1000.)
            packet_addressing_type = self.segmenter.is_input_packet(can_id=received_frame.arbitration_id,
                                                                    data=received_frame.data)
        return CanPacketRecord(frame=received_frame,
                               direction=TransmissionDirection.RECEIVED,
                               addressing_type=packet_addressing_type,
                               addressing_format=self.segmenter.addressing_format,
                               transmission_time=datetime.fromtimestamp(received_frame.timestamp))

    def send_message(self, message: UdsMessage) -> UdsMessageRecord:
        """
        Transmit UDS message over CAN.

        .. warning:: Must not be called within an asynchronous function.

        :param message: A message to send.

        :raise OverflowError: Flow Control packet with Flow Status equal to OVERFLOW was received.
        :raise TransmissionInterruptionError: A new UDS message transmission was started while sending this message.
        :raise NotImplementedError: Flow Control CAN packet with unknown Flow Status was received.

        :return: Record with historic information about transmitted UDS message.
        """
        packets_to_send = list(self.segmenter.segmentation(message))
        packet_records = [self.send_packet(packets_to_send.pop(0))]
        while packets_to_send:
            record = self.receive_packet(timeout=self.N_BS_TIMEOUT)
            if record.packet_type == CanPacketType.FLOW_CONTROL:
                packet_records.append(record)
                if record.flow_status == CanFlowStatus.ContinueToSend:
                    number_of_packets = len(packets_to_send) if record.block_size == 0 else record.block_size
                    delay_between_cf = self.n_cs if self.n_cs is not None else \
                        CanSTminTranslator.decode(record.st_min)  # type: ignore
                    packet_records.extend(self._send_cf_packets_block(
                        cf_packets_block=packets_to_send[:number_of_packets],
                        delay=delay_between_cf))
                    packets_to_send = packets_to_send[number_of_packets:]
                elif record.flow_status == CanFlowStatus.Wait:
                    continue
                elif record.flow_status == CanFlowStatus.Overflow:
                    raise OverflowError("Flow Control with Flow Status `OVERFLOW` was received.")
                else:
                    raise NotImplementedError(f"Unknown Flow Status received: {record.flow_status}")
            elif CanPacketType.is_initial_packet_type(record.packet_type):
                raise MessageTransmissionError("A new UDS message transmission was started while sending this message.")
            else:
                warn(message="An unrelated CAN packet was received during UDS message transmission.",
                     category=UnexpectedPacketReceptionWarning)
        message_records = UdsMessageRecord(packet_records)
        self._update_n_bs_measured(message_records)
        return message_records

    async def async_send_message(self,
                                 message: UdsMessage,
                                 loop: Optional[AbstractEventLoop] = None) -> UdsMessageRecord:
        """
        Transmit asynchronously UDS message over CAN.

        :param message: A message to send.
        :param loop: An asyncio event loop to use for scheduling this task.

        :raise OverflowError: Flow Control packet with Flow Status equal to OVERFLOW was received.
        :raise TransmissionInterruptionError: A new UDS message transmission was started while sending this message.
        :raise NotImplementedError: Flow Control CAN packet with unknown Flow Status was received.

        :return: Record with historic information about transmitted UDS message.
        """
        packets_to_send = list(self.segmenter.segmentation(message))
        packet_records = [await self.async_send_packet(packets_to_send.pop(0), loop=loop)]
        while packets_to_send:
            record = await self.async_receive_packet(timeout=self.N_BS_TIMEOUT, loop=loop)
            if record.packet_type == CanPacketType.FLOW_CONTROL:
                packet_records.append(record)
                if record.flow_status == CanFlowStatus.ContinueToSend:
                    number_of_packets = len(packets_to_send) if record.block_size == 0 else record.block_size
                    delay_between_cf = self.n_cs if self.n_cs is not None else \
                        CanSTminTranslator.decode(record.st_min)  # type: ignore
                    packet_records.extend(
                        await self._async_send_cf_packets_block(cf_packets_block=packets_to_send[:number_of_packets],
                                                                delay=delay_between_cf,
                                                                loop=loop))
                    packets_to_send = packets_to_send[number_of_packets:]
                elif record.flow_status == CanFlowStatus.Wait:
                    continue
                elif record.flow_status == CanFlowStatus.Overflow:
                    raise OverflowError("Flow Control with Flow Status `OVERFLOW` was received.")
                else:
                    raise NotImplementedError(f"Unknown Flow Status received: {record.flow_status}")
            elif CanPacketType.is_initial_packet_type(record.packet_type):
                raise MessageTransmissionError("A new UDS message transmission was started while sending this message.")
            else:
                warn(message="An unrelated CAN packet was received during UDS message transmission.",
                     category=UnexpectedPacketReceptionWarning)
        message_records = UdsMessageRecord(packet_records)
        self._update_n_bs_measured(message_records)
        return message_records

    def receive_message(self, timeout: Optional[TimeMillisecondsAlias] = None) -> UdsMessageRecord:
        """
        Receive UDS message over CAN.

        .. warning:: Must not be called within an asynchronous function.

        :param timeout: Maximal time (in milliseconds) to wait for UDS message transmission to start.
            This means that receiving might last longer if First Frame was received within provided time.

        :raise TypeError: Provided timeout value is not None neither int nor float type.
        :raise ValueError: Provided timeout value is less or equal 0.
        :raise TimeoutError: Timeout was reached.
            Either Single Frame / First Frame not received within [timeout] ms
            or N_As, N_Ar, N_Bs, N_Cr timeout reached.

        :return: Record with historic information about received UDS message.
        """
        if timeout is not None:
            if not isinstance(timeout, (int, float)):
                raise TypeError("Provided timeout value is not None neither int nor float type.")
            if timeout <= 0:
                raise ValueError("Provided timeout value is less or equal 0.")
        if timeout is not None:
            time_end_ms = (time() * 1000) + timeout
        while True:
            if timeout is not None:
                time_now_ms = time() * 1000
                if time_end_ms <= time_now_ms:
                    raise TimeoutError("Timeout was reached before a UDS message was received.")
                timeout = time_end_ms - time_now_ms
            received_packet = self.receive_packet(timeout=timeout)
            if received_packet.packet_type == CanPacketType.SINGLE_FRAME:
                return UdsMessageRecord([received_packet])
            if received_packet.packet_type == CanPacketType.FIRST_FRAME:
                return self._receive_consecutive_frames(first_frame=received_packet)
            warn(message="A CAN packet that does not start UDS message transmission was received.",
                 category=UnexpectedPacketReceptionWarning)

    async def async_receive_message(self,
                                    timeout: Optional[TimeMillisecondsAlias] = None,
                                    loop: Optional[AbstractEventLoop] = None) -> UdsMessageRecord:
        """
        Receive asynchronously UDS message over CAN.

        :param timeout: Maximal time (in milliseconds) to wait for UDS message transmission to start.
            This means that receiving might last longer if First Frame was received within provided time.
        :param loop: An asyncio event loop to use for scheduling this task.

        :raise TypeError: Provided timeout value is not None neither int nor float type.
        :raise ValueError: Provided timeout value is less or equal 0.
        :raise TimeoutError: Timeout was reached.
            Either Single Frame / First Frame not received within [timeout] ms
            or N_As, N_Ar, N_Bs, N_Cr timeout reached.

        :return: Record with historic information about received UDS message.
        """
        if timeout is not None:
            if not isinstance(timeout, (int, float)):
                raise TypeError("Provided timeout value is not None neither int nor float type.")
            if timeout <= 0:
                raise ValueError("Provided timeout value is less or equal 0.")
        if timeout is not None:
            time_end_ms = (time() * 1000) + timeout
        while True:
            if timeout is not None:
                time_now_ms = time() * 1000
                if time_end_ms <= time_now_ms:
                    raise TimeoutError("Timeout was reached before a UDS message was received.")
                timeout = time_end_ms - time_now_ms
            received_packet = await self.async_receive_packet(timeout=timeout, loop=loop)
            if received_packet.packet_type == CanPacketType.SINGLE_FRAME:
                return UdsMessageRecord([received_packet])
            if received_packet.packet_type == CanPacketType.FIRST_FRAME:
                return await self._async_receive_consecutive_frames(first_frame=received_packet, loop=loop)
            warn(message="A CAN packet that does not start UDS message transmission was received.",
                 category=UnexpectedPacketReceptionWarning)

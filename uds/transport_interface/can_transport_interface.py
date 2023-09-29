"""Definition and implementation of UDS Transport Interface for CAN bus."""

__all__ = ["AbstractCanTransportInterface", "PyCanTransportInterface"]

from typing import Any, Optional, Union
from abc import abstractmethod
from warnings import warn
from asyncio import AbstractEventLoop, wait_for, get_running_loop
from datetime import datetime
from time import time

from can import BusABC, AsyncBufferedReader, BufferedReader, Notifier, Message

from uds.utilities import TimeMilliseconds, ValueWarning
from uds.can import AbstractCanAddressingInformation, CanIdHandler, CanDlcHandler
from uds.packet import CanPacket, AnyCanPacket, CanPacketRecord, CanPacketType
from uds.transmission_attributes import TransmissionDirection
from uds.segmentation import CanSegmenter
from .abstract_transport_interface import AbstractTransportInterface


class AbstractCanTransportInterface(AbstractTransportInterface):
    """
    Abstract definition of Transport Interface for managing UDS on CAN bus.

    CAN Transport Interfaces are meant to handle UDS middle layers (Transport and Network) on CAN bus.
    """

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
            - :parameter dlc: Base CAN DLC value to use for CAN Packets.
            - :parameter use_data_optimization: Information whether to use CAN Frame Data Optimization.
            - :parameter filler_byte: Filler byte value to use for CAN Frame Data Padding.

        :raise TypeError: Provided Addressing Information value has unexpected type.
        """
        if not isinstance(addressing_information, AbstractCanAddressingInformation):
            raise TypeError("Unsupported type of Addressing Information was provided.")
        self.__addressing_information: AbstractCanAddressingInformation = addressing_information
        super().__init__(bus_manager=can_bus_manager)
        self.n_as_timeout = kwargs.pop("n_as_timeout", self.N_AS_TIMEOUT)
        self.n_ar_timeout = kwargs.pop("n_ar_timeout", self.N_AR_TIMEOUT)
        self.n_bs_timeout = kwargs.pop("n_bs_timeout", self.N_BS_TIMEOUT)
        self.n_br = kwargs.pop("n_br", self.DEFAULT_N_BR)
        self.n_cs = kwargs.pop("n_cs", self.DEFAULT_N_CS)
        self.n_cr_timeout = kwargs.pop("n_cr_timeout", self.N_CR_TIMEOUT)
        self.__segmenter = CanSegmenter(addressing_information=addressing_information, **kwargs)

    @property
    def segmenter(self) -> CanSegmenter:
        """Value of the segmenter used by this CAN Transport Interface."""
        return self.__segmenter

    # Time parameter - CAN Network Layer

    @property
    def n_as_timeout(self) -> TimeMilliseconds:
        """Timeout value for N_As time parameter."""
        return self.__n_as_timeout

    @n_as_timeout.setter
    def n_as_timeout(self, value: TimeMilliseconds):
        """
        Set timeout value for N_As time parameter.

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
    def n_as_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_As time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """

    @property
    def n_ar_timeout(self) -> TimeMilliseconds:
        """Timeout value for N_Ar time parameter."""
        return self.__n_ar_timeout

    @n_ar_timeout.setter
    def n_ar_timeout(self, value: TimeMilliseconds):
        """
        Set timeout value for N_Ar time parameter.

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
    def n_ar_measured(self) -> Optional[TimeMilliseconds]:
        """
        Get the last measured value of N_Ar time parameter.

        :return: Time in milliseconds or None if the value was never measured.
        """

    @property
    def n_bs_timeout(self) -> TimeMilliseconds:
        """Timeout value for N_Bs time parameter."""
        return self.__n_bs_timeout

    @n_bs_timeout.setter
    def n_bs_timeout(self, value: TimeMilliseconds):
        """
        Set timeout value for N_Bs time parameter.

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
        return self.__n_br

    @n_br.setter
    def n_br(self, value: TimeMilliseconds):
        """
        Set the value of N_Br time parameter to use.

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
    def n_br_max(self) -> TimeMilliseconds:
        """
        Get the maximum valid value of N_Br time parameter.

        .. warning:: To assess maximal value of :ref:`N_Br <knowledge-base-can-n-br>`, the actual value of
            :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter is required.
            Either the latest measured value of N_Ar would be used, or 0ms would be assumed (if there are
            no measurement result).
        """
        n_ar_measured = 0 if self.n_ar_measured is None else self.n_ar_measured
        return 0.9 * self.n_bs_timeout - n_ar_measured

    @property
    def n_cs(self) -> Optional[TimeMilliseconds]:
        """
        Get the value of N_Cs time parameter which is currently set.

        .. note:: The actual (observed on the bus) value will be slightly longer as it also includes computation
            and CAN Interface delays.
        """
        return self.__n_cs

    @n_cs.setter
    def n_cs(self, value: Optional[TimeMilliseconds]):
        """
        Set the value of N_Cs time parameter to use.

        :param value: The value to set.

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
    def n_cs_max(self) -> TimeMilliseconds:
        """
        Get the maximum valid value of N_Cs time parameter.

        .. warning:: To assess maximal value of :ref:`N_Cs <knowledge-base-can-n-cs>`, the actual value of
            :ref:`N_As <knowledge-base-can-n-as>` time parameter is required.
            Either the latest measured value of N_Ar would be used, or 0ms would be assumed (if there are
            no measurement result).
        """
        n_as_measured = 0 if self.n_as_measured is None else self.n_as_measured
        return 0.9 * self.n_cr_timeout - n_as_measured

    @property
    def n_cr_timeout(self) -> TimeMilliseconds:
        """Timeout value for N_Cr time parameter."""
        return self.__n_cr_timeout

    @n_cr_timeout.setter
    def n_cr_timeout(self, value: TimeMilliseconds):
        """
        Set timeout value for N_Cr time parameter.

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
        Value of base CAN DLC to use for output CAN Packets.

        .. note:: All output CAN Packets will have this DLC value set unless
            :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>` is used.
        """
        return self.segmenter.dlc

    @dlc.setter
    def dlc(self, value: int):
        """
        Set value of base CAN DLC to use for output CAN Packets.

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


class PyCanTransportInterface(AbstractCanTransportInterface):
    """
    Transport Interface for managing UDS on CAN with python-can package as bus handler.

    .. note:: Documentation for python-can package: https://python-can.readthedocs.io/
    """

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
        return isinstance(bus_manager, BusABC)  # TODO: check that receive_own_messages is set (if possible)

    def send_packet(self, packet: Union[CanPacket, AnyCanPacket]) -> CanPacketRecord:
        """
        Transmit CAN packet.

        .. warning:: Must not be called within an asynchronous function.

        :param packet: CAN packet to send.

        :return: Record with historic information about transmitted CAN packet.
        """
        time_start = time()
        if not isinstance(packet, (CanPacket, AnyCanPacket)):
            raise TypeError("Provided packet value does not contain a CAN Packet.")
        is_flow_control_packet = packet.packet_type == CanPacketType.FLOW_CONTROL
        timeout = self.n_ar_timeout if is_flow_control_packet else self.n_as_timeout
        can_message = Message(arbitration_id=packet.can_id,
                              is_extended_id=CanIdHandler.is_extended_can_id(packet.can_id),
                              data=packet.raw_frame_data,
                              is_fd=CanDlcHandler.is_can_fd_specific_dlc(packet.dlc))
        message_listener = BufferedReader()
        notifier = Notifier(bus=self.bus_manager,
                            listeners=[message_listener])
        self.bus_manager.send(can_message)
        observed_frame = None
        while observed_frame is None \
                or observed_frame.arbitration_id != packet.can_id \
                or tuple(observed_frame.data) != packet.raw_frame_data \
                or not observed_frame.is_rx:
            time_now = time()
            timeout_left = timeout - (time_now - time_start) * 1000.
            observed_frame = message_listener.get_message(timeout=timeout_left)
        notifier.stop()
        if is_flow_control_packet:
            self.__n_ar_measured = (observed_frame.timestamp - time_start) * 1000.
        else:
            self.__n_as_measured = (observed_frame.timestamp - time_start) * 1000.
        return CanPacketRecord(frame=observed_frame,
                               direction=TransmissionDirection.TRANSMITTED,
                               addressing_type=packet.addressing_type,
                               addressing_format=packet.addressing_format,
                               transmission_time=datetime.fromtimestamp(observed_frame.timestamp))

    def receive_packet(self, timeout: Optional[TimeMilliseconds] = None) -> CanPacketRecord:  # TODO: make it possible to receive old packets (received in a past)
        """
        Receive CAN packet.

        .. warning:: Must not be called within an asynchronous function.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TypeError: Provided timeout value is not None neither int nor float type.
        :raise ValueError: Provided timeout value is less or equal 0.
        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information about received CAN packet.
        """
        time_start = time()
        if timeout is not None:
            if not isinstance(timeout, (int, float)):
                raise TypeError("Provided timeout value is not None neither int nor float type.")
            if timeout <= 0:
                raise ValueError("Provided timeout value is less or equal 0.")
        message_listener = BufferedReader()
        notifier = Notifier(bus=self.bus_manager,
                            listeners=[message_listener])
        packet_addressing_type = None
        while packet_addressing_type is None:
            time_now = time()
            timeout_left = None if timeout is None else timeout - (time_now - time_start)*1000
            received_frame = message_listener.get_message(timeout=timeout_left)
            packet_addressing_type = self.segmenter.is_input_packet(can_id=received_frame.arbitration_id,
                                                                    data=received_frame.data)
        notifier.stop()
        return CanPacketRecord(frame=received_frame,
                               direction=TransmissionDirection.RECEIVED,
                               addressing_type=packet_addressing_type,
                               addressing_format=self.segmenter.addressing_format,
                               transmission_time=datetime.fromtimestamp(received_frame.timestamp))

    async def async_send_packet(self,
                                packet: Union[CanPacket, AnyCanPacket],
                                loop: Optional[AbstractEventLoop] = None) -> CanPacketRecord:  # type: ignore
        """
        Transmit CAN packet.

        :param packet: CAN packet to send.
        :param loop: An asyncio event loop used for observing messages.

        :raise TypeError: Provided packet is not CAN Packet.

        :return: Record with historic information about transmitted CAN packet.
        """
        time_start = time()
        if not isinstance(packet, (CanPacket, AnyCanPacket)):
            raise TypeError("Provided packet value does not contain a CAN Packet.")
        loop = get_running_loop() if loop is None else loop
        is_flow_control_packet = packet.packet_type == CanPacketType.FLOW_CONTROL
        timeout = self.n_ar_timeout if is_flow_control_packet else self.n_as_timeout
        async_message_listener = AsyncBufferedReader()
        async_notifier = Notifier(bus=self.bus_manager,
                                  listeners=[async_message_listener],
                                  loop=loop)
        can_message = Message(arbitration_id=packet.can_id,
                              is_extended_id=CanIdHandler.is_extended_can_id(packet.can_id),
                              data=packet.raw_frame_data,
                              is_fd=CanDlcHandler.is_can_fd_specific_dlc(packet.dlc))
        self.bus_manager.send(can_message)
        observed_frame = None
        while observed_frame is None \
                or observed_frame.arbitration_id != packet.can_id \
                or tuple(observed_frame.data) != packet.raw_frame_data \
                or not observed_frame.is_rx:
            time_now = time()
            timeout_left = timeout - (time_now - time_start) * 1000.
            observed_frame = await wait_for(async_message_listener.get_message(), timeout=timeout_left)
        async_notifier.stop()
        if is_flow_control_packet:
            self.__n_ar_measured = (observed_frame.timestamp - time_start) * 1000.
        else:
            self.__n_as_measured = (observed_frame.timestamp - time_start) * 1000.
        return CanPacketRecord(frame=observed_frame,
                               direction=TransmissionDirection.TRANSMITTED,
                               addressing_type=packet.addressing_type,
                               addressing_format=packet.addressing_format,
                               transmission_time=datetime.fromtimestamp(observed_frame.timestamp))

    async def async_receive_packet(self,
                                   timeout: Optional[TimeMilliseconds] = None,
                                   loop: Optional[AbstractEventLoop] = None) -> CanPacketRecord:
        """
        Receive CAN packet.

        :param timeout: Maximal time (in milliseconds) to wait.
        :param loop: An asyncio event loop used for observing messages.

        :raise TypeError: Provided timeout value is not None neither int nor float type.
        :raise ValueError: Provided timeout value is less or equal 0.
        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information about received CAN packet.
        """
        loop = get_running_loop() if loop is None else loop
        time_start = time()
        if timeout is not None:
            if not isinstance(timeout, (int, float)):
                raise TypeError("Provided timeout value is not None neither int nor float type.")
            if timeout <= 0:
                raise ValueError("Provided timeout value is less or equal 0.")
        async_message_listener = AsyncBufferedReader()
        async_notifier = Notifier(bus=self.bus_manager,
                                  listeners=[async_message_listener],
                                  loop=loop)
        packet_addressing_type = None
        while packet_addressing_type is None:
            time_now = time()
            _timeout_left = None if timeout is None else timeout - (time_now - time_start)*1000
            received_frame = await wait_for(async_message_listener.get_message(),
                                            timeout=_timeout_left,
                                            loop=loop)
            packet_addressing_type = self.segmenter.is_input_packet(can_id=received_frame.arbitration_id,
                                                                    data=received_frame.data)
        async_notifier.stop()
        return CanPacketRecord(frame=received_frame,
                               direction=TransmissionDirection.RECEIVED,
                               addressing_type=packet_addressing_type,
                               addressing_format=self.segmenter.addressing_format,
                               transmission_time=datetime.fromtimestamp(received_frame.timestamp))

import asyncio
from abc import ABC, abstractmethod
from datetime import datetime
from threading import Timer
from time import sleep
from typing import List, Optional

import pytest
from tests.system_tests.transport_interface.can.common import AbstractCanTests

from can import Bus, Message
from uds.can import CanAddressingFormat, CanAddressingInformation, CanFlowStatus, DefaultFlowControlParametersGenerator
from uds.message import UdsMessage, UdsMessageRecord
from uds.packet import CanPacket, CanPacketRecord, CanPacketType
from uds.transmission_attributes import AddressingType, TransmissionDirection
from uds.transport_interface import PyCanTransportInterface
from uds.utilities import TimeMillisecondsAlias


class AbstractPythonCanTests(AbstractCanTests):
    """
    Definition of system tests (with hardware) for Diagnostic over CAN (DoCAN) with python-can.

    Requires hardware setup:
        - 2x CAN bus hardware interfaces that can be controlled using python-can package
        - both CAN interfaces are connected (so they can communicate with other) - termination (resistor) is part of
            CAN cables connection
    """

    MAKE_TIMING_CHECKS: bool = True

    can_interface_1: Bus
    can_interface_2: Bus
    sent_message: Optional[UdsMessageRecord]
    sent_packet: Optional[CanPacketRecord]
    _timers: List[Timer]

    @abstractmethod
    def setup_class(self):
        """Create bus objects."""
        self.can_interface_1: Bus  # configure in concrete classes accordingly to hardware setup
        self.can_interface_2: Bus   # configure in concrete classes accordingly to hardware setup

    def setup_method(self):
        """Prepare CAN bus objects for tests."""
        self.can_interface_1.flush_tx_buffer()
        self.can_interface_2.flush_tx_buffer()
        self.sent_message: Optional[UdsMessageRecord] = None
        self.sent_packet: Optional[CanPacketRecord] = None
        self._timers: List[Timer] = []

    def teardown_method(self):
        """Finish all tasks that were open during test."""
        for _timer in self._timers:
            if not _timer.finished.is_set():
                sleep(0.001)
            _timer.cancel()
        if self._timers:
            self._timers = []
            sleep(self.TASK_TIMING_TOLERANCE / 1000.)

    def teardown_class(self):
        """Safely close CAN bus objects."""
        self.can_interface_1.shutdown()
        self.can_interface_2.shutdown()

    def send_frame(self,
                   can_interface: Bus,
                   frame: Message,
                   delay: TimeMillisecondsAlias) -> Timer:
        """
        Send CAN packet over CAN interface.

        :param can_interface: CAN interface to send the packet over.
        :param frame: CAN frame to send.
        :param delay: Time [ms] after which the transmission will be started.

        :return: Timer object with scheduled task.
        """
        timer = Timer(interval=delay / 1000., function=can_interface.send, args=(frame, ))
        self._timers.append(timer)
        timer.start()
        return timer

    @staticmethod
    async def async_send_frame(can_interface: Bus,
                               frame: Message,
                               delay: TimeMillisecondsAlias) -> None:
        """
        Send CAN packet asynchronously over CAN interface.

        :param can_interface: CAN interface to send the packet over.
        :param frame: CAN frame to send.
        :param delay: Time [ms] after which the transmission will be started.
        """
        await asyncio.sleep(delay / 1000.)
        return can_interface.send(frame)

    def send_packet(self,
                    can_transport_interface: PyCanTransportInterface,
                    packet: CanPacket,
                    delay: TimeMillisecondsAlias) -> Timer:
        """
        Send CAN packet over CAN interface.

        .. note:: The result (UDS message record) will be available be in `self.sent_packet` attribute.

        :param can_transport_interface: Transport Interface to use for transmission.
        :param packet: CAN packet to send.
        :param delay: Time [ms] after which the transmission will be started.

        :return: Timer object with scheduled task.
        """

        def _send_packet():
            self.sent_packet = can_transport_interface.send_packet(packet)

        timer = Timer(interval=delay/1000., function=_send_packet)
        self._timers.append(timer)
        timer.start()
        return timer

    @staticmethod
    async def async_send_packet(can_transport_interface: PyCanTransportInterface,
                                packet: CanPacket,
                                delay: TimeMillisecondsAlias) -> CanPacketRecord:
        """
        Send CAN packet asynchronously over CAN interface.

        :param can_transport_interface: Transport Interface to use for transmission.
        :param packet: CAN packet to send.
        :param delay: Time [ms] after which the transmission will be started.

        :return: Future CAN packet record.
        """
        await asyncio.sleep(delay / 1000.)
        return await can_transport_interface.async_send_packet(packet=packet)

    def send_message(self,
                     can_transport_interface: PyCanTransportInterface,
                     message: UdsMessage,
                     delay: TimeMillisecondsAlias) -> Timer:
        """
        Send CAN message over CAN interface.

        .. note:: The result (UDS message record) will be available be in `self.sent_message` attribute.

        :param can_transport_interface: Transport Interface to use for transmission.
        :param message: UDS message to send.
        :param delay: Time [ms] after which the transmission will be started.

        :return: Timer object with scheduled task.
        """

        def _send_message():
            self.sent_message = can_transport_interface.send_message(message)

        timer = Timer(interval=delay/1000., function=_send_message)
        self._timers.append(timer)
        timer.start()
        return timer

    @staticmethod
    async def async_send_message(can_transport_interface: PyCanTransportInterface,
                                 message: UdsMessage,
                                 delay: TimeMillisecondsAlias) -> UdsMessageRecord:
        """
        Send CAN message asynchronously over CAN interface.

        :param can_transport_interface: Transport Interface to use for transmission.
        :param message: UDS message to send.
        :param delay: Time [ms] after which the transmission will be started.

        :return: Future UDS message record.
        """
        await asyncio.sleep(delay / 1000.)
        return await can_transport_interface.async_send_message(message=message)


class AbstractCanPacketTests(AbstractPythonCanTests, ABC):
    """Common implementation of system tests related to sending and receiving CAN packets."""

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_information, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
                                  tx_physical={"can_id": 0x611},
                                  rx_physical={"can_id": 0x612},
                                  tx_functional={"can_id": 0x6FF},
                                  rx_functional={"can_id": 0x6FE}),
         {"filler_byte": 0x1E, "payload": [0x10, 0x04]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                  tx_physical={"can_id": 0xDA1BFF, "target_address": 0x1B, "source_address": 0xFF},
                                  rx_physical={"can_id": 0xDAFF1B, "target_address": 0xFF, "source_address": 0x1B},
                                  tx_functional={"can_id": 0x1CDBACFE, "target_address": 0xAC, "source_address": 0xFE},
                                  rx_functional={"can_id": 0x1CDBFEAC, "target_address": 0xFE, "source_address": 0xAC}),
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x13}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                  tx_physical={"can_id": 0x987, "target_address": 0x90},
                                  rx_physical={"can_id": 0x987, "target_address": 0xFE},
                                  tx_functional={"can_id": 0x11766, "target_address": 0xFF},
                                  rx_functional={"can_id": 0x11765, "target_address": 0xFF}),
         {"payload": [0x32, 0xFF], "sequence_number": 0xF}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x651, "address_extension": 0x87},
                                  rx_physical={"can_id": 0x652, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x6FE, "address_extension": 0xA5},
                                  rx_functional={"can_id": 0x6FF, "address_extension": 0xA5}),
         {"dlc": 8, "flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x15, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF, "address_extension": 0x87},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x1CCDACFE, "target_address": 0xAC, "source_address": 0xFE, "address_extension": 0xFF},
                                  rx_functional={"can_id": 0x1CCDFEAC, "target_address": 0xFE, "source_address": 0xAC, "address_extension": 0xFF}),
         {"filler_byte": 0xBC, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A, 0x12, 0xBC], "dlc": 0xF}),
    ])
    def test_send_packet(self, packet_type, addressing_type, addressing_information, packet_type_specific_kwargs):
        """
        Check for simple sending of a CAN packet.

        Procedure:
        1. Send CAN packet via Transport Interface.
            Expected: CAN packet record returned.
        2. Validate transmitted CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the transmitted CAN packet.

        :param packet_type: Type of CAN packet to send.
        :param addressing_type: Addressing type to use for transmitting a CAN packet.
        :param addressing_information: Example Addressing Information of a CAN Node.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        """
        if addressing_type == AddressingType.PHYSICAL:
            can_id = addressing_information.tx_packets_physical_ai["can_id"]
            target_address = addressing_information.tx_packets_physical_ai["target_address"]
            source_address = addressing_information.tx_packets_physical_ai["source_address"]
            address_extension = addressing_information.tx_packets_physical_ai["address_extension"]
        else:
            can_id = addressing_information.tx_packets_functional_ai["can_id"]
            target_address = addressing_information.tx_packets_functional_ai["target_address"]
            source_address = addressing_information.tx_packets_functional_ai["source_address"]
            address_extension = addressing_information.tx_packets_functional_ai["address_extension"]
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=addressing_information)
        packet = CanPacket(packet_type=packet_type,
                           addressing_format=addressing_information.addressing_format,
                           addressing_type=addressing_type,
                           can_id=can_id,
                           target_address=target_address,
                           source_address=source_address,
                           address_extension=address_extension,
                           **packet_type_specific_kwargs)
        datetime_before_send = datetime.now()
        packet_record = can_transport_interface.send_packet(packet)
        datetime_after_send = datetime.now()
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.TRANSMITTED
        assert packet_record.raw_frame_data == packet.raw_frame_data
        assert packet_record.addressing_format == packet.addressing_format == addressing_information.addressing_format
        assert packet_record.packet_type == packet.packet_type == packet_type
        assert packet_record.can_id == packet.can_id == can_id
        assert packet_record.addressing_type == packet.addressing_type == addressing_type
        assert packet_record.target_address == packet.target_address == target_address
        assert packet_record.source_address == packet.source_address == source_address
        assert packet_record.address_extension == packet.address_extension == address_extension
        # timing parameters
        transmission_time_ms = (datetime_after_send - datetime_before_send).total_seconds() * 1000.
        if packet_type == CanPacketType.FLOW_CONTROL:
            assert can_transport_interface.n_as_measured is None
            if self.MAKE_TIMING_CHECKS:
                assert 0 < can_transport_interface.n_ar_measured < transmission_time_ms
        else:
            assert can_transport_interface.n_ar_measured is None
            if self.MAKE_TIMING_CHECKS:
                assert 0 < can_transport_interface.n_as_measured < transmission_time_ms
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            assert datetime_before_send < packet_record.transmission_time < datetime_after_send

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_information, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
                                  tx_physical={"can_id": 0x611},
                                  rx_physical={"can_id": 0x612},
                                  tx_functional={"can_id": 0x6FF},
                                  rx_functional={"can_id": 0x6FE}),
         {"filler_byte": 0x1E, "payload": [0x10, 0x04]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                  tx_physical={"can_id": 0xDA1BFF, "target_address": 0x1B, "source_address": 0xFF},
                                  rx_physical={"can_id": 0xDAFF1B, "target_address": 0xFF, "source_address": 0x1B},
                                  tx_functional={"can_id": 0x1CDBACFE, "target_address": 0xAC, "source_address": 0xFE},
                                  rx_functional={"can_id": 0x1CDBFEAC, "target_address": 0xFE, "source_address": 0xAC}),
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x13}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                  tx_physical={"can_id": 0x987, "target_address": 0x90},
                                  rx_physical={"can_id": 0x987, "target_address": 0xFE},
                                  tx_functional={"can_id": 0x11766, "target_address": 0xFF},
                                  rx_functional={"can_id": 0x11765, "target_address": 0xFF}),
         {"payload": [0x32, 0xFF], "sequence_number": 0xF}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x651, "address_extension": 0x87},
                                  rx_physical={"can_id": 0x652, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x6FE, "address_extension": 0xA5},
                                  rx_functional={"can_id": 0x6FF, "address_extension": 0xA5}),
         {"dlc": 8, "flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x15, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF, "address_extension": 0x87},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x1CCDACFE, "target_address": 0xAC, "source_address": 0xFE, "address_extension": 0xFF},
                                  rx_functional={"can_id": 0x1CCDFEAC, "target_address": 0xFE, "source_address": 0xAC, "address_extension": 0xFF}),
         {"filler_byte": 0xBC, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A, 0x12, 0xBC], "dlc": 0xF}),
    ])
    @pytest.mark.asyncio
    async def test_async_send_packet(self, packet_type, addressing_type, addressing_information,
                                     packet_type_specific_kwargs):
        """
        Check for simple asynchronous sending of a CAN packet.

        Procedure:
        1. Send (using async method) a CAN packet via Transport Interface.
            Expected: CAN packet record returned.
        2. Validate transmitted CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the transmitted CAN packet.

        :param packet_type: Type of CAN packet to send.
        :param addressing_type: Addressing type to use for transmitting a CAN packet.
        :param addressing_information: Example Addressing Information of a CAN Node.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        """
        if addressing_type == AddressingType.PHYSICAL:
            can_id = addressing_information.tx_packets_physical_ai["can_id"]
            target_address = addressing_information.tx_packets_physical_ai["target_address"]
            source_address = addressing_information.tx_packets_physical_ai["source_address"]
            address_extension = addressing_information.tx_packets_physical_ai["address_extension"]
        else:
            can_id = addressing_information.tx_packets_functional_ai["can_id"]
            target_address = addressing_information.tx_packets_functional_ai["target_address"]
            source_address = addressing_information.tx_packets_functional_ai["source_address"]
            address_extension = addressing_information.tx_packets_functional_ai["address_extension"]
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=addressing_information)
        packet = CanPacket(packet_type=packet_type,
                           addressing_format=addressing_information.addressing_format,
                           addressing_type=addressing_type,
                           can_id=can_id,
                           target_address=target_address,
                           source_address=source_address,
                           address_extension=address_extension,
                           **packet_type_specific_kwargs)
        datetime_before_send = datetime.now()
        packet_record = await can_transport_interface.async_send_packet(packet)
        datetime_after_send = datetime.now()
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.TRANSMITTED
        assert packet_record.raw_frame_data == packet.raw_frame_data
        assert packet_record.addressing_format == packet.addressing_format == addressing_information.addressing_format
        assert packet_record.packet_type == packet.packet_type == packet_type
        assert packet_record.can_id == packet.can_id == can_id
        assert packet_record.addressing_type == packet.addressing_type == addressing_type
        assert packet_record.target_address == packet.target_address == target_address
        assert packet_record.source_address == packet.source_address == source_address
        assert packet_record.address_extension == packet.address_extension == address_extension
        # timing parameters
        transmission_time_ms = (datetime_after_send - datetime_before_send).total_seconds() * 1000.
        if packet_type == CanPacketType.FLOW_CONTROL:
            assert can_transport_interface.n_as_measured is None
            if self.MAKE_TIMING_CHECKS:
                assert 0 < can_transport_interface.n_ar_measured < transmission_time_ms
        else:
            assert can_transport_interface.n_ar_measured is None
            if self.MAKE_TIMING_CHECKS:
                assert 0 < can_transport_interface.n_as_measured < transmission_time_ms
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            assert datetime_before_send < packet_record.transmission_time < datetime_after_send

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_information, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
                                  tx_physical={"can_id": 0x611},
                                  rx_physical={"can_id": 0x612},
                                  tx_functional={"can_id": 0x6FF},
                                  rx_functional={"can_id": 0x6FE}),
         {"filler_byte": 0x1E, "payload": [0x10, 0x04]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                  tx_physical={"can_id": 0xDA1BFF, "target_address": 0x1B, "source_address": 0xFF},
                                  rx_physical={"can_id": 0xDAFF1B, "target_address": 0xFF, "source_address": 0x1B},
                                  tx_functional={"can_id": 0x1CDBACFE, "target_address": 0xAC, "source_address": 0xFE},
                                  rx_functional={"can_id": 0x1CDBFEAC, "target_address": 0xFE, "source_address": 0xAC}),
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x13}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                  tx_physical={"can_id": 0x987, "target_address": 0x90},
                                  rx_physical={"can_id": 0x987, "target_address": 0xFE},
                                  tx_functional={"can_id": 0x11766, "target_address": 0xFF},
                                  rx_functional={"can_id": 0x11765, "target_address": 0xFF}),
         {"payload": [0x32, 0xFF], "sequence_number": 0xF}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x651, "address_extension": 0x87},
                                  rx_physical={"can_id": 0x652, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x6FE, "address_extension": 0xA5},
                                  rx_functional={"can_id": 0x6FF, "address_extension": 0xA5}),
         {"dlc": 8, "flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x15, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF, "address_extension": 0x87},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x1CCDACFE, "target_address": 0xAC, "source_address": 0xFE, "address_extension": 0xFF},
                                  rx_functional={"can_id": 0x1CCDFEAC, "target_address": 0xFE, "source_address": 0xAC, "address_extension": 0xFF}),
         {"filler_byte": 0xBC, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A, 0x12, 0xBC], "dlc": 0xF}),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        # TODO: adjust values to be closer to boundary when https://github.com/mdabrowski1990/uds/issues/228 resolved
        (1000, 950),  # ms
        (50, 20),
    ])
    def test_receive_packet(self, packet_type, addressing_type, addressing_information,
                            packet_type_specific_kwargs,
                            timeout, send_after):
        """
        Check for a simple CAN packet receiving.

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frame that carries received CAN packet.
        2. Call method to receive packet via Transport Interface with timeout set just after CAN packet
            reaches CAN bus.
            Expected: CAN packet is received.
        3. Validate received CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the received CAN packet.

        :param packet_type: Type of CAN packet to send.
        :param addressing_type: Addressing type to use for transmitting a CAN packet.
        :param addressing_information: Example Addressing Information of a CAN Node.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        :param timeout: Timeout to pass to receive method [ms].
        :param send_after: Time when to send CAN frame after call of receive method [ms].
        """
        if addressing_type == AddressingType.PHYSICAL:
            can_id = addressing_information.rx_packets_physical_ai["can_id"]
            target_address = addressing_information.rx_packets_physical_ai["target_address"]
            source_address = addressing_information.rx_packets_physical_ai["source_address"]
            address_extension = addressing_information.rx_packets_physical_ai["address_extension"]
        else:
            can_id = addressing_information.rx_packets_functional_ai["can_id"]
            target_address = addressing_information.rx_packets_functional_ai["target_address"]
            source_address = addressing_information.rx_packets_functional_ai["source_address"]
            address_extension = addressing_information.rx_packets_functional_ai["address_extension"]
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=addressing_information)
        packet = CanPacket(packet_type=packet_type,
                           addressing_format=addressing_information.addressing_format,
                           addressing_type=addressing_type,
                           can_id=can_id,
                           target_address=target_address,
                           source_address=source_address,
                           address_extension=address_extension,
                           **packet_type_specific_kwargs)
        can_frame = Message(arbitration_id=packet.can_id,
                            data=packet.raw_frame_data,
                            is_fd=packet.dlc > 8)
        datetime_before_send = datetime.now()
        self.send_frame(can_interface=self.can_interface_2,
                        frame=can_frame,
                        delay=send_after)
        datetime_before_receive = datetime.now()
        packet_record = can_transport_interface.receive_packet(timeout=timeout)
        datetime_after_receive = datetime.now()
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.RECEIVED
        assert packet_record.raw_frame_data == tuple(can_frame.data)
        assert packet_record.addressing_format == addressing_information.addressing_format
        assert packet_record.addressing_type == addressing_type
        assert packet_record.can_id == can_frame.arbitration_id == can_id
        assert packet_record.target_address == target_address
        assert packet_record.source_address == source_address
        assert packet_record.address_extension == address_extension
        # performance
        receiving_time_ms = (datetime_before_send - datetime_before_receive).total_seconds() * 1000.
        if self.MAKE_TIMING_CHECKS:
            assert send_after <= receiving_time_ms < timeout
            assert datetime_before_receive < packet_record.transmission_time < datetime_after_receive

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_information, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
                                  tx_physical={"can_id": 0x611},
                                  rx_physical={"can_id": 0x612},
                                  tx_functional={"can_id": 0x6FF},
                                  rx_functional={"can_id": 0x6FE}),
         {"filler_byte": 0x1E, "payload": [0x10, 0x04]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                  tx_physical={"can_id": 0xDA1BFF, "target_address": 0x1B, "source_address": 0xFF},
                                  rx_physical={"can_id": 0xDAFF1B, "target_address": 0xFF, "source_address": 0x1B},
                                  tx_functional={"can_id": 0x1CDBACFE, "target_address": 0xAC, "source_address": 0xFE},
                                  rx_functional={"can_id": 0x1CDBFEAC, "target_address": 0xFE, "source_address": 0xAC}),
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x13}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                  tx_physical={"can_id": 0x987, "target_address": 0x90},
                                  rx_physical={"can_id": 0x987, "target_address": 0xFE},
                                  tx_functional={"can_id": 0x11766, "target_address": 0xFF},
                                  rx_functional={"can_id": 0x11765, "target_address": 0xFF}),
         {"payload": [0x32, 0xFF], "sequence_number": 0xF}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x651, "address_extension": 0x87},
                                  rx_physical={"can_id": 0x652, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x6FE, "address_extension": 0xA5},
                                  rx_functional={"can_id": 0x6FF, "address_extension": 0xA5}),
         {"dlc": 8, "flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x15, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF, "address_extension": 0x87},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x1CCDACFE, "target_address": 0xAC, "source_address": 0xFE, "address_extension": 0xFF},
                                  rx_functional={"can_id": 0x1CCDFEAC, "target_address": 0xFE, "source_address": 0xAC, "address_extension": 0xFF}),
         {"filler_byte": 0xBC, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A, 0x12, 0xBC], "dlc": 0xF}),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        # TODO: adjust values to be closer to boundary when https://github.com/mdabrowski1990/uds/issues/228 resolved
        (1000, 950),  # ms
        (50, 20),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_packet(self, packet_type, addressing_type, addressing_information,
                                        packet_type_specific_kwargs,
                                        timeout, send_after):
        """
        Check for a simple asynchronous CAN packet (physically addressed) receiving.

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frame that carries received CAN packet.
        2. Call async method to receive packet via Transport Interface with timeout set just after CAN packet
            reaches CAN bus.
            Expected: CAN packet is received.
        3. Validate received CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the received CAN packet.

        :param packet_type: Type of CAN packet to send.
        :param addressing_type: Addressing type to use for transmitting a CAN packet.
        :param addressing_information: Example Addressing Information of a CAN Node.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        :param timeout: Timeout to pass to receive method [ms].
        :param send_after: Time when to send CAN frame after call of receive method [ms].
        """
        if addressing_type == AddressingType.PHYSICAL:
            can_id = addressing_information.rx_packets_physical_ai["can_id"]
            target_address = addressing_information.rx_packets_physical_ai["target_address"]
            source_address = addressing_information.rx_packets_physical_ai["source_address"]
            address_extension = addressing_information.rx_packets_physical_ai["address_extension"]
        else:
            can_id = addressing_information.rx_packets_functional_ai["can_id"]
            target_address = addressing_information.rx_packets_functional_ai["target_address"]
            source_address = addressing_information.rx_packets_functional_ai["source_address"]
            address_extension = addressing_information.rx_packets_functional_ai["address_extension"]
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=addressing_information)
        packet = CanPacket(packet_type=packet_type,
                           addressing_format=addressing_information.addressing_format,
                           addressing_type=addressing_type,
                           can_id=can_id,
                           target_address=target_address,
                           source_address=source_address,
                           address_extension=address_extension,
                           **packet_type_specific_kwargs)
        can_frame = Message(arbitration_id=packet.can_id,
                            data=packet.raw_frame_data,
                            is_fd=packet.dlc > 8)
        datetime_before_send = datetime.now()
        send_frame_task = asyncio.create_task(self.async_send_frame(can_interface=self.can_interface_2,
                                                                    frame=can_frame,
                                                                    delay=send_after))
        datetime_before_receive = datetime.now()
        packet_record = await can_transport_interface.async_receive_packet(timeout=timeout)
        datetime_after_receive = datetime.now()
        await send_frame_task
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.RECEIVED
        assert packet_record.raw_frame_data == tuple(can_frame.data)
        assert packet_record.addressing_format == addressing_information.addressing_format
        assert packet_record.addressing_type == addressing_type
        assert packet_record.can_id == can_frame.arbitration_id == can_id
        assert packet_record.target_address == target_address
        assert packet_record.source_address == source_address
        assert packet_record.address_extension == address_extension
        # performance
        receiving_time_ms = (datetime_before_send - datetime_before_receive).total_seconds() * 1000.
        if self.MAKE_TIMING_CHECKS:
            assert send_after <= receiving_time_ms < timeout
            assert datetime_before_receive < packet_record.transmission_time < datetime_after_receive

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_information, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
                                  tx_physical={"can_id": 0x611},
                                  rx_physical={"can_id": 0x612},
                                  tx_functional={"can_id": 0x6FF},
                                  rx_functional={"can_id": 0x6FE}),
         {"filler_byte": 0x1E, "payload": [0x10, 0x04]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                  tx_physical={"can_id": 0xDA1BFF, "target_address": 0x1B, "source_address": 0xFF},
                                  rx_physical={"can_id": 0xDAFF1B, "target_address": 0xFF, "source_address": 0x1B},
                                  tx_functional={"can_id": 0x1CDBACFE, "target_address": 0xAC, "source_address": 0xFE},
                                  rx_functional={"can_id": 0x1CDBFEAC, "target_address": 0xFE, "source_address": 0xAC}),
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x13}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                  tx_physical={"can_id": 0x987, "target_address": 0x90},
                                  rx_physical={"can_id": 0x987, "target_address": 0xFE},
                                  tx_functional={"can_id": 0x11766, "target_address": 0xFF},
                                  rx_functional={"can_id": 0x11765, "target_address": 0xFF}),
         {"payload": [0x32, 0xFF], "sequence_number": 0xF}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x651, "address_extension": 0x87},
                                  rx_physical={"can_id": 0x652, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x6FE, "address_extension": 0xA5},
                                  rx_functional={"can_id": 0x6FF, "address_extension": 0xA5}),
         {"dlc": 8, "flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x15, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF, "address_extension": 0x87},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x1CCDACFE, "target_address": 0xAC, "source_address": 0xFE, "address_extension": 0xFF},
                                  rx_functional={"can_id": 0x1CCDFEAC, "target_address": 0xFE, "source_address": 0xAC, "address_extension": 0xFF}),
         {"filler_byte": 0xBC, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A, 0x12, 0xBC], "dlc": 0xF}),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        (1000, 1005),  # ms
        (50, 55),
    ])
    def test_receive_packet__timeout(self, addressing_information, addressing_type,
                                     packet_type, packet_type_specific_kwargs, timeout, send_after):
        """
        Check for a timeout during packet receiving.

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frame that carries received CAN packet.
        2. Call method to receive packet via Transport Interface with timeout set just before CAN packet reaches CAN bus.
            Expected: Timeout exception is raised.
        3. Call method to receive packet via Transport Interface second time with timeout after CAN packet reaches
            CAN bus.
            Expect: CAN packet received.

        :param packet_type: Type of CAN packet to send.
        :param addressing_type: Addressing type to use for transmitting a CAN packet.
        :param addressing_information: Example Addressing Information of a CAN Node.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        :param timeout: Timeout to pass to receive method [ms].
        :param send_after: Time when to send CAN frame after call of receive method [ms].
        """
        if addressing_type == AddressingType.PHYSICAL:
            can_id = addressing_information.rx_packets_physical_ai["can_id"]
            target_address = addressing_information.rx_packets_physical_ai["target_address"]
            source_address = addressing_information.rx_packets_physical_ai["source_address"]
            address_extension = addressing_information.rx_packets_physical_ai["address_extension"]
        else:
            can_id = addressing_information.rx_packets_functional_ai["can_id"]
            target_address = addressing_information.rx_packets_functional_ai["target_address"]
            source_address = addressing_information.rx_packets_functional_ai["source_address"]
            address_extension = addressing_information.rx_packets_functional_ai["address_extension"]
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=addressing_information)
        packet = CanPacket(packet_type=packet_type,
                           addressing_format=addressing_information.addressing_format,
                           addressing_type=addressing_type,
                           can_id=can_id,
                           target_address=target_address,
                           source_address=source_address,
                           address_extension=address_extension,
                           **packet_type_specific_kwargs)
        can_frame = Message(arbitration_id=packet.can_id,
                            data=packet.raw_frame_data,
                            is_fd=packet.dlc > 8)
        self.send_frame(can_interface=self.can_interface_2,
                        frame=can_frame,
                        delay=send_after)
        datetime_before_receive = datetime.now()
        with pytest.raises(TimeoutError):
            can_transport_interface.receive_packet(timeout=timeout)
        datetime_after_receive = datetime.now()
        receiving_time_ms = (datetime_after_receive - datetime_before_receive).total_seconds() * 1000.
        assert timeout < receiving_time_ms < timeout + self.TASK_TIMING_TOLERANCE
        # receive packet later
        packet_record = can_transport_interface.receive_packet(timeout=(send_after - timeout) * 10)
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.RECEIVED
        assert packet_record.raw_frame_data == tuple(can_frame.data)

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_information, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
                                  tx_physical={"can_id": 0x611},
                                  rx_physical={"can_id": 0x612},
                                  tx_functional={"can_id": 0x6FF},
                                  rx_functional={"can_id": 0x6FE}),
         {"filler_byte": 0x1E, "payload": [0x10, 0x04]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                  tx_physical={"can_id": 0xDA1BFF, "target_address": 0x1B, "source_address": 0xFF},
                                  rx_physical={"can_id": 0xDAFF1B, "target_address": 0xFF, "source_address": 0x1B},
                                  tx_functional={"can_id": 0x1CDBACFE, "target_address": 0xAC, "source_address": 0xFE},
                                  rx_functional={"can_id": 0x1CDBFEAC, "target_address": 0xFE, "source_address": 0xAC}),
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x13}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                  tx_physical={"can_id": 0x987, "target_address": 0x90},
                                  rx_physical={"can_id": 0x987, "target_address": 0xFE},
                                  tx_functional={"can_id": 0x11766, "target_address": 0xFF},
                                  rx_functional={"can_id": 0x11765, "target_address": 0xFF}),
         {"payload": [0x32, 0xFF], "sequence_number": 0xF}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x651, "address_extension": 0x87},
                                  rx_physical={"can_id": 0x652, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x6FE, "address_extension": 0xA5},
                                  rx_functional={"can_id": 0x6FF, "address_extension": 0xA5}),
         {"dlc": 8, "flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x15, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF, "address_extension": 0x87},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x1CCDACFE, "target_address": 0xAC, "source_address": 0xFE, "address_extension": 0xFF},
                                  rx_functional={"can_id": 0x1CCDFEAC, "target_address": 0xFE, "source_address": 0xAC, "address_extension": 0xFF}),
         {"filler_byte": 0xBC, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A, 0x12, 0xBC], "dlc": 0xF}),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        (1000, 1005),  # ms
        (50, 55),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_packet__timeout(self, addressing_information, addressing_type,
                                                 packet_type, packet_type_specific_kwargs, timeout, send_after):
        """
        Check for a timeout during packet asynchronous receiving.

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frame that carries received CAN packet.
        2. Call async method to receive packet via Transport Interface with timeout set before any CAN packet
            reaches CAN bus.
            Expected: Timeout exception is raised.
        3. Call async method to receive packet via Transport Interface second time with timeout after CAN packet reaches
            CAN bus.
            Expect: CAN packet received.

        :param packet_type: Type of CAN packet to send.
        :param addressing_type: Addressing type to use for transmitting a CAN packet.
        :param addressing_information: Example Addressing Information of a CAN Node.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        :param timeout: Timeout to pass to receive method [ms].
        :param send_after: Time when to send CAN frame after call of receive method [ms].
        """
        if addressing_type == AddressingType.PHYSICAL:
            can_id = addressing_information.rx_packets_physical_ai["can_id"]
            target_address = addressing_information.rx_packets_physical_ai["target_address"]
            source_address = addressing_information.rx_packets_physical_ai["source_address"]
            address_extension = addressing_information.rx_packets_physical_ai["address_extension"]
        else:
            can_id = addressing_information.rx_packets_functional_ai["can_id"]
            target_address = addressing_information.rx_packets_functional_ai["target_address"]
            source_address = addressing_information.rx_packets_functional_ai["source_address"]
            address_extension = addressing_information.rx_packets_functional_ai["address_extension"]
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=addressing_information)
        packet = CanPacket(packet_type=packet_type,
                           addressing_format=addressing_information.addressing_format,
                           addressing_type=addressing_type,
                           can_id=can_id,
                           target_address=target_address,
                           source_address=source_address,
                           address_extension=address_extension,
                           **packet_type_specific_kwargs)
        can_frame = Message(arbitration_id=packet.can_id,
                            data=packet.raw_frame_data,
                            is_fd=packet.dlc > 8)
        send_frame_task = asyncio.create_task(self.async_send_frame(can_interface=self.can_interface_2,
                                                                    frame=can_frame,
                                                                    delay=send_after))
        datetime_before_receive = datetime.now()
        with pytest.raises(TimeoutError):
            await can_transport_interface.async_receive_packet(timeout=timeout)
        datetime_after_receive = datetime.now()
        receiving_time_ms = (datetime_after_receive - datetime_before_receive).total_seconds() * 1000.
        assert timeout < receiving_time_ms < timeout + self.TASK_TIMING_TOLERANCE
        # receive packet later
        packet_record = await can_transport_interface.async_receive_packet(timeout=(send_after - timeout) * 10)
        await send_frame_task
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.RECEIVED
        assert packet_record.raw_frame_data == tuple(can_frame.data)


class AbstractMessageTests(AbstractPythonCanTests, ABC):
    """Common implementation of system tests related to sending and receiving UDS messages."""

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, 0x12, 0x34], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x50, 0x01], addressing_type=AddressingType.FUNCTIONAL),
    ])
    def test_send_message__sf(self, example_addressing_information, message):
        """
        Check for a simple synchronous UDS message sending.

        Procedure:
        1. Send a UDS message using Transport Interface (via CAN Interface).
            Expected: UDS message record returned.
        2. Validate transmitted UDS message record attributes.
            Expected: Attributes of UDS message record are in line with the transmitted UDS message.

        :param example_addressing_information: Example Addressing Information of a CAN Node.
        :param message: UDS message to send.
        """
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=example_addressing_information)
        datetime_before_send = datetime.now()
        message_record = can_transport_interface.send_message(message)
        datetime_after_send = datetime.now()
        assert isinstance(message_record, UdsMessageRecord)
        assert message_record.direction == TransmissionDirection.TRANSMITTED
        assert message_record.payload == message.payload
        assert message_record.addressing_type == message.addressing_type
        assert message_record.transmission_start == message_record.transmission_end
        assert len(message_record.packets_records) == 1
        assert message_record.packets_records[0].packet_type == CanPacketType.SINGLE_FRAME
        # timing parameters
        assert can_transport_interface.n_bs_measured is None
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            assert datetime_before_send < message_record.transmission_start < datetime_after_send

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, 0x12, 0x34], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x50, 0x01], addressing_type=AddressingType.FUNCTIONAL),
    ])
    @pytest.mark.asyncio
    async def test_async_send_message__sf(self, example_addressing_information, message):
        """
        Check for a simple asynchronous UDS message sending.

        Procedure:
        1. Send (using async method) a UDS message using Transport Interface (via CAN Interface).
            Expected: UDS message record returned.
        2. Validate transmitted UDS message record attributes.
            Expected: Attributes of UDS message record are in line with the transmitted UDS message.

        :param example_addressing_information: Example Addressing Information of a CAN Node.
        :param message: UDS message to send.
        """
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=example_addressing_information)
        datetime_before_send = datetime.now()
        message_record = await can_transport_interface.async_send_message(message)
        datetime_after_send = datetime.now()
        assert isinstance(message_record, UdsMessageRecord)
        assert message_record.direction == TransmissionDirection.TRANSMITTED
        assert message_record.payload == message.payload
        assert message_record.addressing_type == message.addressing_type
        assert message_record.transmission_start == message_record.transmission_end
        assert len(message_record.packets_records) == 1
        assert message_record.packets_records[0].packet_type == CanPacketType.SINGLE_FRAME
        # timing parameters
        assert can_transport_interface.n_bs_measured is None
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            assert datetime_before_send < message_record.transmission_start < datetime_after_send

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, 0x12, 0x34], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x50, 0x01], addressing_type=AddressingType.FUNCTIONAL),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        # TODO: adjust values to be closer to boundary when https://github.com/mdabrowski1990/uds/issues/228 resolved
        (1000, 950),  # ms
        (50, 20),
    ])
    def test_receive_message__sf(self, example_addressing_information, example_addressing_information_2nd_node,
                                 message, timeout, send_after):
        """
        Check for receiving of a UDS message (carried by Single Frame packet).

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frame that carries received
            UDS message (Single Frame).
        2. Call method to receive message via Transport Interface with timeout set just after UDS message
            reaches CAN bus.
            Expected: UDS message is received.
        3. Validate received UDS message record attributes.
            Expected: Attributes of UDS message record are in line with the received UDS message.

        :param example_addressing_information: Addressing Information of receiving CAN Node.
        :param example_addressing_information_2nd_node: Addressing Information of transmitting CAN Node.
        :param message: UDS message to transmit.
        :param timeout: Timeout to pass to receive method [ms].
        :param send_after: Time when to send CAN frame after call of receive method [ms].
        """
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=example_addressing_information)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            can_bus_manager=self.can_interface_2,
            addressing_information=example_addressing_information_2nd_node)
        self.send_message(can_transport_interface=can_transport_interface_2nd_node,
                          message=message,
                          delay=send_after)
        datetime_before_receive = datetime.now()
        message_record = can_transport_interface.receive_message(timeout=timeout)
        datetime_after_receive = datetime.now()
        assert isinstance(message_record, UdsMessageRecord)
        assert message_record.direction == TransmissionDirection.RECEIVED
        assert message_record.payload == message.payload
        assert message_record.addressing_type == message.addressing_type
        assert message_record.transmission_start == message_record.transmission_end
        assert len(message_record.packets_records) == 1
        assert message_record.packets_records[0].packet_type == CanPacketType.SINGLE_FRAME
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            assert datetime_before_receive < message_record.transmission_start < datetime_after_receive

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, 0x12, 0x34], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x50, 0x01], addressing_type=AddressingType.FUNCTIONAL),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        # TODO: adjust values to be closer to boundary when https://github.com/mdabrowski1990/uds/issues/228 resolved
        (1000, 950),  # ms
        (50, 20),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_message__sf(self, example_addressing_information,
                                             example_addressing_information_2nd_node,
                                             message, timeout, send_after):
        """
        Check for asynchronous receiving of a UDS message (carried by Single Frame packet).

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frame that carries received
            UDS message (Single Frame).
        2. Call async method to receive message via Transport Interface with timeout set just after UDS message
            reaches CAN bus.
            Expected: UDS message is received.
        3. Validate received UDS message record attributes.
            Expected: Attributes of UDS message record are in line with the received UDS message.

        :param example_addressing_information: Addressing Information of receiving CAN Node.
        :param example_addressing_information_2nd_node: Addressing Information of transmitting CAN Node.
        :param message: UDS message to transmit.
        :param timeout: Timeout value to pass to receive message method [ms].
        :param send_after: Time when to send CAN frame after call of receive method [ms].
        """
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=example_addressing_information)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            can_bus_manager=self.can_interface_2,
            addressing_information=example_addressing_information_2nd_node)
        send_message_task = asyncio.create_task(
            self.async_send_message(can_transport_interface=can_transport_interface_2nd_node,
                                    message=message,
                                    delay=send_after))

        datetime_before_receive = datetime.now()
        message_record = await can_transport_interface.async_receive_message(timeout=timeout)
        datetime_after_receive = datetime.now()
        await send_message_task
        assert isinstance(message_record, UdsMessageRecord)
        assert message_record.direction == TransmissionDirection.RECEIVED
        assert message_record.payload == message.payload
        assert message_record.addressing_type == message.addressing_type
        assert message_record.transmission_start == message_record.transmission_end
        assert len(message_record.packets_records) == 1
        assert message_record.packets_records[0].packet_type == CanPacketType.SINGLE_FRAME
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            assert datetime_before_receive < message_record.transmission_start < datetime_after_receive

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, 0x12, 0x34], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x50, 0x01], addressing_type=AddressingType.FUNCTIONAL),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        (1000, 1005),  # ms
        (50, 55),
    ])
    def test_receive_message__sf__timeout(self, example_addressing_information, example_addressing_information_2nd_node,
                                          message, timeout, send_after):
        """
        Check for a timeout during receiving of a UDS message.

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frame that carries received UDS message.
        2. Call method to receive message via Transport Interface with timeout set just before UDS message
            reaches CAN bus.
            Expected: Timeout exception is raised.
        3. Call method to receive message for the second time with timeout set after UDS message reaches CAN bus.
            Expected: Message is received.

        :param example_addressing_information: Addressing Information of receiving CAN Node.
        :param example_addressing_information_2nd_node: Addressing Information of transmitting CAN Node.
        :param message: UDS message to transmit.
        :param timeout: Timeout to pass to receive method [ms].
        :param send_after: Time when to send CAN frame after call of receive method [ms].
        """
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=example_addressing_information)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            can_bus_manager=self.can_interface_2,
            addressing_information=example_addressing_information_2nd_node)
        self.send_message(can_transport_interface=can_transport_interface_2nd_node,
                          message=message,
                          delay=send_after)
        datetime_before_receive = datetime.now()
        with pytest.raises(TimeoutError):
            can_transport_interface.receive_message(timeout=timeout)
        datetime_after_receive = datetime.now()
        receiving_time_ms = (datetime_after_receive - datetime_before_receive).total_seconds() * 1000.
        assert timeout < receiving_time_ms < timeout + self.TASK_TIMING_TOLERANCE
        # receive message later
        message_record = can_transport_interface.receive_message(timeout=(send_after - timeout) * 10)
        assert isinstance(message_record, UdsMessageRecord)
        assert message_record.direction == TransmissionDirection.RECEIVED
        assert message_record.payload == message.payload
        assert message_record.addressing_type == message.addressing_type

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, 0x12, 0x34], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x50, 0x01], addressing_type=AddressingType.FUNCTIONAL),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        (1000, 1005),  # ms
        (50, 55),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_message__sf__timeout(self, example_addressing_information,
                                                      example_addressing_information_2nd_node,
                                                      message, timeout, send_after):
        """
        Check for a timeout during asynchronous receiving of a UDS message.

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frame that carries received UDS message.
        2. Call async method to receive message via Transport Interface with timeout set before any CAN packet
            reaches CAN bus.
            Expected: Timeout exception is raised.
        3. Call method to receive message for the second time with timeout set after UDS message reaches CAN bus.
            Expected: Message is received.

        :param example_addressing_information: Addressing Information of receiving CAN Node.
        :param message: UDS message to transmit.
        :param timeout: Timeout value to pass to receive message method [ms].
        :param send_after: Time when to send CAN frame after call of receive method [ms].
        """
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=example_addressing_information)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            can_bus_manager=self.can_interface_2,
            addressing_information=example_addressing_information_2nd_node)
        send_message_task = asyncio.create_task(self.async_send_message(
            can_transport_interface=can_transport_interface_2nd_node,
            message=message,
            delay=send_after))
        datetime_before_receive = datetime.now()
        with pytest.raises(TimeoutError):
            await can_transport_interface.async_receive_message(timeout=timeout)
        datetime_after_receive = datetime.now()
        receiving_time_ms = (datetime_after_receive - datetime_before_receive).total_seconds() * 1000.
        assert timeout < receiving_time_ms < timeout + self.TASK_TIMING_TOLERANCE
        message_record = await can_transport_interface.async_receive_message(timeout=(send_after - timeout) * 10)
        await send_message_task
        assert isinstance(message_record, UdsMessageRecord)
        assert message_record.direction == TransmissionDirection.RECEIVED
        assert message_record.payload == message.payload
        assert message_record.addressing_type == message.addressing_type

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, *range(62)], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x62, 0x12, 0x34, *range(100, 250)], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        # TODO: adjust values to be closer to boundary when https://github.com/mdabrowski1990/uds/issues/228 resolved
        (1000, 970),  # ms
        (50, 20),
    ])
    def test_send_message__multi_packets(self, example_addressing_information, example_addressing_information_2nd_node,
                                         message, timeout, send_after):
        """
        Check for a synchronous multi packet (FF + CF) UDS message sending.

        Procedure:
        1. Schedule Flow Control CAN Packet with information to continue sending all consecutive frame packets at once.
        2. Send a UDS message using Transport Interface (via CAN Interface).
            Expected: UDS message record returned.
        3. Validate transmitted UDS message record attributes.
            Expected: Attributes of UDS message record are in line with the transmitted UDS message.

        :param example_addressing_information: Example Addressing Information of a CAN Node.
        :param example_addressing_information_2nd_node: Example Addressing Information of a CAN Node.
        :param message: UDS message to send.
        :param timeout: Value of N_Bs timeout [ms] to use.
        :param send_after: Delay to use for sending CAN flow control.
        """
        can_transport_interface = PyCanTransportInterface(
            can_bus_manager=self.can_interface_1,
            addressing_information=example_addressing_information,
            n_bs_timeout=timeout)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            can_bus_manager=self.can_interface_2,
            addressing_information=example_addressing_information_2nd_node)
        flow_control_packet = can_transport_interface_2nd_node.segmenter.get_flow_control_packet(
            flow_status=CanFlowStatus.ContinueToSend,
            block_size=0,
            st_min=0)
        self.send_packet(can_transport_interface=can_transport_interface_2nd_node,
                         packet=flow_control_packet,
                         delay=send_after)
        datetime_before_send = datetime.now()
        message_record = can_transport_interface.send_message(message)
        datetime_after_send = datetime.now()
        assert isinstance(message_record, UdsMessageRecord)
        assert message_record.direction == TransmissionDirection.TRANSMITTED
        assert message_record.payload == message.payload
        assert message_record.addressing_type == message.addressing_type
        assert message_record.transmission_start < message_record.transmission_end
        assert len(message_record.packets_records) > 1
        assert message_record.packets_records[0].packet_type == CanPacketType.FIRST_FRAME
        assert message_record.packets_records[0].direction == TransmissionDirection.TRANSMITTED
        assert message_record.packets_records[1].packet_type == CanPacketType.FLOW_CONTROL
        assert message_record.packets_records[1].direction == TransmissionDirection.RECEIVED
        assert all(following_packet.packet_type == CanPacketType.CONSECUTIVE_FRAME
                   and following_packet.direction == TransmissionDirection.TRANSMITTED
                   for following_packet in message_record.packets_records[2:])
        # timing parameters
        assert isinstance(can_transport_interface.n_bs_measured, tuple)
        assert len(can_transport_interface.n_bs_measured) == 1
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            assert datetime_before_send < message_record.transmission_start < datetime_after_send
            assert (send_after - self.TASK_TIMING_TOLERANCE
                    <= can_transport_interface.n_bs_measured[0]
                    <= send_after + self.TASK_TIMING_TOLERANCE)

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, *range(62)], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x62, 0x12, 0x34, *range(100, 250)], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        # TODO: adjust values to be closer to boundary when https://github.com/mdabrowski1990/uds/issues/228 resolved
        (1000, 950),  # ms
        (50, 10),
    ])
    @pytest.mark.asyncio
    async def test_async_send_message__multi_packets(self, example_addressing_information,
                                                     example_addressing_information_2nd_node,
                                                     message, timeout, send_after):
        """
        Check for an asynchronous multi packet (FF + CF) UDS message sending.

        Procedure:
        1. Schedule Flow Control CAN Packet with information to continue sending all consecutive frame packets at once.
        2. Send (using async method) a UDS message using Transport Interface (via CAN Interface).
            Expected: UDS message record returned.
        3. Validate transmitted UDS message record attributes.
            Expected: Attributes of UDS message record are in line with the transmitted UDS message.

        :param example_addressing_information: Example Addressing Information of a CAN Node.
        :param example_addressing_information_2nd_node: Example Addressing Information of a CAN Node.
        :param message: UDS message to send.
        :param timeout: Value of N_Bs timeout [ms] to use.
        :param send_after: Delay to use for sending CAN flow control.
        """
        can_transport_interface = PyCanTransportInterface(
            can_bus_manager=self.can_interface_1,
            addressing_information=example_addressing_information,
            n_bs_timeout=timeout)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            can_bus_manager=self.can_interface_2,
            addressing_information=example_addressing_information_2nd_node)
        flow_control_packet = can_transport_interface_2nd_node.segmenter.get_flow_control_packet(
            flow_status=CanFlowStatus.ContinueToSend,
            block_size=0,
            st_min=0)
        send_packet_task = asyncio.create_task(self.async_send_packet(
            can_transport_interface=can_transport_interface_2nd_node,
            packet=flow_control_packet,
            delay=send_after))
        datetime_before_send = datetime.now()
        message_record = await can_transport_interface.async_send_message(message)
        datetime_after_send = datetime.now()
        await send_packet_task
        assert isinstance(message_record, UdsMessageRecord)
        assert message_record.direction == TransmissionDirection.TRANSMITTED
        assert message_record.payload == message.payload
        assert message_record.addressing_type == message.addressing_type
        assert message_record.transmission_start < message_record.transmission_end
        assert len(message_record.packets_records) > 1
        assert message_record.packets_records[0].packet_type == CanPacketType.FIRST_FRAME
        assert message_record.packets_records[0].direction == TransmissionDirection.TRANSMITTED
        assert message_record.packets_records[1].packet_type == CanPacketType.FLOW_CONTROL
        assert message_record.packets_records[1].direction == TransmissionDirection.RECEIVED
        assert all(following_packet.packet_type == CanPacketType.CONSECUTIVE_FRAME
                   and following_packet.direction == TransmissionDirection.TRANSMITTED
                   for following_packet in message_record.packets_records[2:])
        # timing parameters
        assert isinstance(can_transport_interface.n_bs_measured, tuple)
        assert len(can_transport_interface.n_bs_measured) == 1
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            assert datetime_before_send < message_record.transmission_start < datetime_after_send
            assert (send_after - self.TASK_TIMING_TOLERANCE
                    <= can_transport_interface.n_bs_measured[0]
                    <= send_after + self.TASK_TIMING_TOLERANCE)

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, *range(62)], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x62, 0x12, 0x34, *range(100, 250)], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        (1000, 1010),  # ms
        (50, 60),
    ])
    def test_send_message__multi_packets__timeout(self, example_addressing_information,
                                                  example_addressing_information_2nd_node,
                                                  message, timeout, send_after):
        """
        Check for a timeout (N_Bs timeout exceeded) during synchronous multi packet (FF + CF) UDS message sending.

        Procedure:
        1. Schedule Flow Control CAN Packet just after N_Bs timeout.
        2. Send a UDS message using Transport Interface (via CAN Interface).
            Expected: Timeout exception is raised.

        :param example_addressing_information: Example Addressing Information of a CAN Node.
        :param example_addressing_information_2nd_node: Example Addressing Information of a CAN Node.
        :param message: UDS message to send.
        :param timeout: Value of N_Bs timeout [ms] to use.
        :param send_after: Delay to use for sending CAN flow control.
        """
        can_transport_interface = PyCanTransportInterface(
            can_bus_manager=self.can_interface_1,
            addressing_information=example_addressing_information,
            n_bs_timeout=timeout)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            can_bus_manager=self.can_interface_2,
            addressing_information=example_addressing_information_2nd_node)
        flow_control_packet = can_transport_interface_2nd_node.segmenter.get_flow_control_packet(
            flow_status=CanFlowStatus.ContinueToSend,
            block_size=0,
            st_min=0)
        self.send_packet(can_transport_interface=can_transport_interface_2nd_node,
                         packet=flow_control_packet,
                         delay=send_after)
        datetime_before_receive = datetime.now()
        with pytest.raises(TimeoutError):
            can_transport_interface.send_message(message)
        datetime_after_receive = datetime.now()
        # timing parameters
        receiving_time_ms = (datetime_after_receive - datetime_before_receive).total_seconds() * 1000.
        assert (can_transport_interface.n_bs_timeout
                < receiving_time_ms
                < can_transport_interface.n_bs_timeout + self.TASK_TIMING_TOLERANCE)

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, *range(62)], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x62, 0x12, 0x34, *range(100, 250)], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        (1000, 1010),  # ms
        (50, 60),
    ])
    @pytest.mark.asyncio
    async def test_async_send_message__multi_packets__timeout(self, example_addressing_information,
                                                              example_addressing_information_2nd_node,
                                                              message, timeout, send_after):
        """
        Check for a timeout (N_Bs timeout exceeded) during asynchronous multi packet (FF + CF) UDS message sending.

        Procedure:
        1. Schedule Flow Control CAN Packet just after N_Bs timeout.
        2. Send (using async method) a UDS message using Transport Interface (via CAN Interface).
            Expected: Timeout exception is raised.

        :param example_addressing_information: Example Addressing Information of a CAN Node.
        :param example_addressing_information_2nd_node: Example Addressing Information of a CAN Node.
        :param message: UDS message to send.
        :param timeout: Value of N_Bs timeout [ms] to use.
        :param send_after: Delay to use for sending CAN flow control.
        """
        can_transport_interface = PyCanTransportInterface(
            can_bus_manager=self.can_interface_1,
            addressing_information=example_addressing_information,
            n_bs_timeout=timeout)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            can_bus_manager=self.can_interface_2,
            addressing_information=example_addressing_information_2nd_node)
        flow_control_packet = can_transport_interface_2nd_node.segmenter.get_flow_control_packet(
            flow_status=CanFlowStatus.ContinueToSend,
            block_size=0,
            st_min=0)
        send_packet_task = asyncio.create_task(self.async_send_packet(
            can_transport_interface=can_transport_interface_2nd_node,
            packet=flow_control_packet,
            delay=send_after))
        datetime_before_receive = datetime.now()
        with pytest.raises(TimeoutError):
            await can_transport_interface.async_send_message(message)
        datetime_after_receive = datetime.now()
        await send_packet_task
        # timing parameters
        receiving_time_ms = (datetime_after_receive - datetime_before_receive).total_seconds() * 1000.
        assert (can_transport_interface.n_bs_timeout
                < receiving_time_ms
                < can_transport_interface.n_bs_timeout + self.TASK_TIMING_TOLERANCE)

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, *range(62)], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x62, 0x12, 0x34, *range(100, 250)], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("timeout, send_after, delay", [
        # TODO: adjust values to be closer to boundary when https://github.com/mdabrowski1990/uds/issues/228 resolved
        (1000, 950, 20),  # ms
        (50, 10, 50),
    ])
    def test_receive_message__multi_packets(self, example_addressing_information,
                                            example_addressing_information_2nd_node, message,
                                            timeout, send_after, delay):
        """
        Check for receiving of a UDS message (carried by First Frame and Consecutive Frame packets).

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frames that carry received
            UDS message (First Frame and then Consecutive Frames).
        2. Call method to receive message via Transport Interface.
            Expected: UDS message is received.
        3. Validate received UDS message record attributes.
            Expected: Attributes of UDS message record are in line with the received UDS message.

        :param example_addressing_information: Addressing Information of receiving CAN Node.
        :param example_addressing_information_2nd_node: Addressing Information of transmitting CAN Node.
        :param message: UDS message to transmit.
        :param timeout: Timeout value to pass to receive message method [ms].
        :param send_after: Time when to send First Frame after call of receive method [ms].
        :param delay: Time distance to use for sending Consecutive Frames [ms].
        """
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=example_addressing_information,
                                                          n_br=0)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            can_bus_manager=self.can_interface_2,
            addressing_information=example_addressing_information_2nd_node)
        packets = can_transport_interface_2nd_node.segmenter.segmentation(message)
        self.send_packet(can_transport_interface=can_transport_interface_2nd_node,
                         packet=packets[0],
                         delay=send_after)
        for i, cf_packet in enumerate(packets[1:], start=1):
            self.send_packet(can_transport_interface=can_transport_interface_2nd_node,
                             packet=cf_packet,
                             delay=send_after + i * delay)
        datetime_before_receive = datetime.now()
        message_record = can_transport_interface.receive_message(timeout=timeout)
        datetime_after_receive = datetime.now()
        assert isinstance(message_record, UdsMessageRecord)
        assert len(message_record.packets_records) == len(packets) + 1, \
            "All packets (including Flow Control) are stored"
        assert message_record.direction == TransmissionDirection.RECEIVED
        assert message_record.payload == message.payload
        assert message_record.addressing_type == message.addressing_type
        assert message_record.transmission_start < message_record.transmission_end
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            assert datetime_before_receive < message_record.transmission_start
            assert message_record.transmission_end < datetime_after_receive

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, *range(62)], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x62, 0x12, 0x34, *range(100, 250)], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("timeout, send_after, delay", [
        # TODO: adjust values to be closer to boundary when https://github.com/mdabrowski1990/uds/issues/228 resolved
        (1000, 950, 20),  # ms
        (50, 10, 50),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_message__multi_packets(self, example_addressing_information,
                                                        example_addressing_information_2nd_node, message,
                                                        timeout, send_after, delay):
        """
        Check for asynchronous receiving of a UDS message (carried by First Frame and Consecutive Frame packets).

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frames that carry received
            UDS message (First Frame and then Consecutive Frames).
        2. Call async method to receive message via Transport Interface.
            Expected: UDS message is received.
        3. Validate received UDS message record attributes.
            Expected: Attributes of UDS message record are in line with the received UDS message.

        :param example_addressing_information: Addressing Information of receiving CAN Node.
        :param example_addressing_information_2nd_node: Addressing Information of transmitting CAN Node.
        :param message: UDS message to transmit.
        :param timeout: Timeout value to pass to receive message method [ms].
        :param send_after: Time when to send First Frame after call of receive method [ms].
        :param delay: Time distance to use for sending Consecutive Frames [ms].
        """
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=example_addressing_information)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            can_bus_manager=self.can_interface_2,
            addressing_information=example_addressing_information_2nd_node)
        packets = can_transport_interface_2nd_node.segmenter.segmentation(message)

        async def _send_message():
            for packet in packets:
                await self.async_send_packet(can_transport_interface=can_transport_interface_2nd_node,
                                             packet=packet,
                                             delay=send_after if packet == packets[0] else delay)

        send_message_task = asyncio.create_task(_send_message())
        datetime_before_receive = datetime.now()
        message_record = await can_transport_interface.async_receive_message(timeout=timeout)
        datetime_after_receive = datetime.now()
        await send_message_task
        assert isinstance(message_record, UdsMessageRecord)
        assert len(message_record.packets_records) == len(packets) + 1, \
            "All packets (including Flow Control) are stored"
        assert message_record.direction == TransmissionDirection.RECEIVED
        assert message_record.payload == message.payload
        assert message_record.addressing_type == message.addressing_type
        assert message_record.transmission_start < message_record.transmission_end
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            assert datetime_before_receive < message_record.transmission_start
            assert message_record.transmission_end < datetime_after_receive

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, *range(62)], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x62, 0x12, 0x34, *range(100, 250)], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("timeout, send_after, delay", [
        # TODO: adjust values to be closer to boundary when https://github.com/mdabrowski1990/uds/issues/228 resolved
        (1000, 950, 20),  # ms
        (50, 10, 50),
    ])
    def test_receive_message__multi_packets__timeout(self, example_addressing_information,
                                                     example_addressing_information_2nd_node, message,
                                                     timeout, send_after, delay):
        """
        Check for a timeout during receiving of a UDS message (carried by First Frame and Consecutive Frame packets).

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frames that carries part of received
            UDS message (First Frame and then Consecutive Frames with one Consecutive Frame missing).
        2. Call method to receive message via Transport Interface.
            Expected: Timeout exception is raised.

        :param example_addressing_information: Addressing Information of receiving CAN Node.
        :param example_addressing_information_2nd_node: Addressing Information of transmitting CAN Node.
        :param message: UDS message to transmit.
        :param timeout: Timeout value to pass to receive message method [ms].
        :param send_after: Time when to send First Frame after call of receive method [ms].
        :param delay: Time distance to use for sending Consecutive Frames [ms].
        """
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=example_addressing_information,
                                                          n_br=0)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            can_bus_manager=self.can_interface_2,
            addressing_information=example_addressing_information_2nd_node)
        packets = can_transport_interface_2nd_node.segmenter.segmentation(message)
        self.send_packet(can_transport_interface=can_transport_interface_2nd_node,
                         packet=packets[0],
                         delay=send_after)
        for i, cf_packet in enumerate(packets[1:-1], start=1):
            self.send_packet(can_transport_interface=can_transport_interface_2nd_node,
                             packet=cf_packet,
                             delay=send_after + i * delay)
        datetime_before_receive = datetime.now()
        with pytest.raises(TimeoutError):
            can_transport_interface.receive_message(timeout=timeout)
        datetime_after_receive = datetime.now()
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            receiving_time_ms = (datetime_after_receive - datetime_before_receive).total_seconds() * 1000.
            expected_timeout_time = send_after + (len(packets) - 2) * delay + can_transport_interface.n_cr_timeout
            assert (expected_timeout_time - self.TASK_TIMING_TOLERANCE
                    < receiving_time_ms < expected_timeout_time + self.TASK_TIMING_TOLERANCE)

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, *range(62)], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x62, 0x12, 0x34, *range(100, 250)], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("timeout, send_after, delay", [
        # TODO: adjust values to be closer to boundary when https://github.com/mdabrowski1990/uds/issues/228 resolved
        (1000, 950, 20),  # ms
        (50, 10, 50),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_message__multi_packets__timeout(self, example_addressing_information,
                                                                 example_addressing_information_2nd_node, message,
                                                                 timeout, send_after, delay):
        """
        Check for a timeout during asynchronous receiving of a UDS message (carried by First Frame and
        Consecutive Frame packets).

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frames that carry received
            UDS message (First Frame and then Consecutive Frames).
        2. Call async method to receive message via Transport Interface.
            Expected: Timeout exception is raised.

        :param example_addressing_information: Addressing Information of receiving CAN Node.
        :param example_addressing_information_2nd_node: Addressing Information of transmitting CAN Node.
        :param message: UDS message to transmit.
        :param timeout: Timeout value to pass to receive message method [ms].
        :param send_after: Time when to send First Frame after call of receive method [ms].
        :param delay: Time distance to use for sending Consecutive Frames [ms].
        """
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=example_addressing_information)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            can_bus_manager=self.can_interface_2,
            addressing_information=example_addressing_information_2nd_node)
        packets = can_transport_interface_2nd_node.segmenter.segmentation(message)

        async def _send_message():
            for packet in packets[:-1]:
                await self.async_send_packet(can_transport_interface=can_transport_interface_2nd_node,
                                             packet=packet,
                                             delay=send_after if packet == packets[0] else delay)

        send_message_task = asyncio.create_task(_send_message())
        datetime_before_receive = datetime.now()
        with pytest.raises(TimeoutError):
            await can_transport_interface.async_receive_message(timeout=timeout)
        datetime_after_receive = datetime.now()
        await send_message_task
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            receiving_time_ms = (datetime_after_receive - datetime_before_receive).total_seconds() * 1000.
            expected_timeout_time = send_after + (len(packets) - 2) * delay + can_transport_interface.n_cr_timeout
            assert (expected_timeout_time - self.TASK_TIMING_TOLERANCE
                    < receiving_time_ms < expected_timeout_time + self.TASK_TIMING_TOLERANCE)


class AbstractUseCaseTests(AbstractPythonCanTests, ABC):
    """Common implementation of system tests wih typical use case scenarios."""

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_information, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
                                  tx_physical={"can_id": 0x611},
                                  rx_physical={"can_id": 0x612},
                                  tx_functional={"can_id": 0x6FF},
                                  rx_functional={"can_id": 0x6FE}),
         {"filler_byte": 0x1E, "payload": [0x10, 0x04]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                  tx_physical={"can_id": 0xDA1BFF, "target_address": 0x1B, "source_address": 0xFF},
                                  rx_physical={"can_id": 0xDAFF1B, "target_address": 0xFF, "source_address": 0x1B},
                                  tx_functional={"can_id": 0x1CDBACFE, "target_address": 0xAC, "source_address": 0xFE},
                                  rx_functional={"can_id": 0x1CDBFEAC, "target_address": 0xFE, "source_address": 0xAC}),
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x13}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                  tx_physical={"can_id": 0x987, "target_address": 0x90},
                                  rx_physical={"can_id": 0x987, "target_address": 0xFE},
                                  tx_functional={"can_id": 0x11766, "target_address": 0xFF},
                                  rx_functional={"can_id": 0x11765, "target_address": 0xFF}),
         {"payload": [0x32, 0xFF], "sequence_number": 0xF}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x651, "address_extension": 0x87},
                                  rx_physical={"can_id": 0x652, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x6FE, "address_extension": 0xA5},
                                  rx_functional={"can_id": 0x6FF, "address_extension": 0xA5}),
         {"dlc": 8, "flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x15, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF, "address_extension": 0x87},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x1CCDACFE, "target_address": 0xAC, "source_address": 0xFE, "address_extension": 0xFF},
                                  rx_functional={"can_id": 0x1CCDFEAC, "target_address": 0xFE, "source_address": 0xAC, "address_extension": 0xFF}),
         {"filler_byte": 0xBC, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A, 0x12, 0xBC], "dlc": 0xF}),
    ])
    def test_send_packet_on_one_receive_on_other_bus(self, packet_type, addressing_type,
                                                     addressing_information,
                                                     packet_type_specific_kwargs):
        """
        Check for sending and receiving CAN packet using two Transport Interfaces.

        Procedure:
        1. Send a CAN packet using Transport Interface 1 (via CAN Interface 1).
            Expected: CAN packet record returned.
        2. Receive a CAN packet using Transport Interface 2 (via CAN Interface 2).
            Expected: CAN packet is received.
        3. Validate received CAN packet records attributes.
            Expected: Attributes of CAN packet records are in line with each other
                (the same packet was received and transmitted).

        :param packet_type: Type of CAN packet to send.
        :param addressing_type: Addressing type to use for transmitting a CAN packet.
        :param addressing_information: Example Addressing Information of a CAN Node.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        """
        if addressing_type == AddressingType.PHYSICAL:
            can_id = addressing_information.tx_packets_physical_ai["can_id"]
            target_address = addressing_information.tx_packets_physical_ai["target_address"]
            source_address = addressing_information.tx_packets_physical_ai["source_address"]
            address_extension = addressing_information.tx_packets_physical_ai["address_extension"]
        else:
            can_id = addressing_information.tx_packets_functional_ai["can_id"]
            target_address = addressing_information.tx_packets_functional_ai["target_address"]
            source_address = addressing_information.tx_packets_functional_ai["source_address"]
            address_extension = addressing_information.tx_packets_functional_ai["address_extension"]
        can_transport_interface_1 = PyCanTransportInterface(
            can_bus_manager=self.can_interface_1,
            addressing_information=addressing_information.get_other_end())
        can_transport_interface_2 = PyCanTransportInterface(
            can_bus_manager=self.can_interface_2,
            addressing_information=addressing_information)
        packet = CanPacket(packet_type=packet_type,
                           addressing_format=addressing_information.addressing_format,
                           addressing_type=addressing_type,
                           can_id=can_id,
                           target_address=target_address,
                           source_address=source_address,
                           address_extension=address_extension,
                           **packet_type_specific_kwargs)
        sent_packet_record = can_transport_interface_2.send_packet(packet)
        received_packet_record = can_transport_interface_1.receive_packet(timeout=100)
        assert isinstance(sent_packet_record, CanPacketRecord)
        assert isinstance(received_packet_record, CanPacketRecord)
        assert sent_packet_record.direction == TransmissionDirection.TRANSMITTED
        assert received_packet_record.direction == TransmissionDirection.RECEIVED
        assert received_packet_record.raw_frame_data == sent_packet_record.raw_frame_data == packet.raw_frame_data
        assert (received_packet_record.addressing_format == sent_packet_record.addressing_format
                == packet.addressing_format == addressing_information.addressing_format)
        assert received_packet_record.packet_type == sent_packet_record.packet_type == packet.packet_type == packet_type
        assert received_packet_record.can_id == sent_packet_record.can_id == packet.can_id == can_id
        assert (received_packet_record.addressing_type == sent_packet_record.addressing_type
                == packet.addressing_type == addressing_type)
        assert (received_packet_record.target_address == sent_packet_record.target_address
                == packet.target_address == target_address)
        assert (received_packet_record.source_address == sent_packet_record.source_address
                == packet.source_address == source_address)
        assert (received_packet_record.address_extension == sent_packet_record.address_extension
                == packet.address_extension == address_extension)

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_information, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
                                  tx_physical={"can_id": 0x611},
                                  rx_physical={"can_id": 0x612},
                                  tx_functional={"can_id": 0x6FF},
                                  rx_functional={"can_id": 0x6FE}),
         {"filler_byte": 0x1E, "payload": [0x10, 0x04]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                  tx_physical={"can_id": 0xDA1BFF, "target_address": 0x1B, "source_address": 0xFF},
                                  rx_physical={"can_id": 0xDAFF1B, "target_address": 0xFF, "source_address": 0x1B},
                                  tx_functional={"can_id": 0x1CDBACFE, "target_address": 0xAC, "source_address": 0xFE},
                                  rx_functional={"can_id": 0x1CDBFEAC, "target_address": 0xFE, "source_address": 0xAC}),
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x13}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                  tx_physical={"can_id": 0x987, "target_address": 0x90},
                                  rx_physical={"can_id": 0x987, "target_address": 0xFE},
                                  tx_functional={"can_id": 0x11766, "target_address": 0xFF},
                                  rx_functional={"can_id": 0x11765, "target_address": 0xFF}),
         {"payload": [0x32, 0xFF], "sequence_number": 0xF}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x651, "address_extension": 0x87},
                                  rx_physical={"can_id": 0x652, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x6FE, "address_extension": 0xA5},
                                  rx_functional={"can_id": 0x6FF, "address_extension": 0xA5}),
         {"dlc": 8, "flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x15, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF, "address_extension": 0x87},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x1CCDACFE, "target_address": 0xAC, "source_address": 0xFE, "address_extension": 0xFF},
                                  rx_functional={"can_id": 0x1CCDFEAC, "target_address": 0xFE, "source_address": 0xAC, "address_extension": 0xFF}),
         {"filler_byte": 0xBC, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A, 0x12, 0xBC], "dlc": 0xF}),
    ])
    @pytest.mark.asyncio
    async def test_async_send_packet_on_one_receive_on_other_bus(self, packet_type, addressing_type,
                                                                 addressing_information,
                                                                 packet_type_specific_kwargs):
        """
        Check for asynchronous sending and receiving CAN packet using two Transport Interfaces.

        Procedure:
        1. Send (using async method) a CAN packet using Transport Interface 1 (via CAN Interface 1).
            Expected: CAN packet record returned.
        2. Receive (using async method) a CAN packet using Transport Interface 2 (via CAN Interface 2).
            Expected: CAN packet is received.
        3. Validate received CAN packet records attributes.
            Expected: Attributes of CAN packet records are in line with each other
                (the same packet was received and transmitted).

        :param packet_type: Type of CAN packet to send.
        :param addressing_type: Addressing type to use for transmitting a CAN packet.
        :param addressing_information: Example Addressing Information of a CAN Node.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        """
        if addressing_type == AddressingType.PHYSICAL:
            can_id = addressing_information.tx_packets_physical_ai["can_id"]
            target_address = addressing_information.tx_packets_physical_ai["target_address"]
            source_address = addressing_information.tx_packets_physical_ai["source_address"]
            address_extension = addressing_information.tx_packets_physical_ai["address_extension"]
        else:
            can_id = addressing_information.tx_packets_functional_ai["can_id"]
            target_address = addressing_information.tx_packets_functional_ai["target_address"]
            source_address = addressing_information.tx_packets_functional_ai["source_address"]
            address_extension = addressing_information.tx_packets_functional_ai["address_extension"]
        can_transport_interface_1 = PyCanTransportInterface(
            can_bus_manager=self.can_interface_1,
            addressing_information=addressing_information.get_other_end())
        can_transport_interface_2 = PyCanTransportInterface(
            can_bus_manager=self.can_interface_2,
            addressing_information=addressing_information)
        packet = CanPacket(packet_type=packet_type,
                           addressing_format=addressing_information.addressing_format,
                           addressing_type=addressing_type,
                           can_id=can_id,
                           target_address=target_address,
                           source_address=source_address,
                           address_extension=address_extension,
                           **packet_type_specific_kwargs)
        receive_packet_task = asyncio.create_task(can_transport_interface_1.async_receive_packet(timeout=100))
        sent_packet_record = await can_transport_interface_2.async_send_packet(packet)
        received_packet_record = await receive_packet_task
        assert isinstance(sent_packet_record, CanPacketRecord)
        assert isinstance(received_packet_record, CanPacketRecord)
        assert sent_packet_record.direction == TransmissionDirection.TRANSMITTED
        assert received_packet_record.direction == TransmissionDirection.RECEIVED
        assert received_packet_record.raw_frame_data == sent_packet_record.raw_frame_data == packet.raw_frame_data
        assert (received_packet_record.addressing_format == sent_packet_record.addressing_format
                == packet.addressing_format == addressing_information.addressing_format)
        assert received_packet_record.packet_type == sent_packet_record.packet_type == packet.packet_type == packet_type
        assert received_packet_record.can_id == sent_packet_record.can_id == packet.can_id == can_id
        assert (received_packet_record.addressing_type == sent_packet_record.addressing_type
                == packet.addressing_type == addressing_type)
        assert (received_packet_record.target_address == sent_packet_record.target_address
                == packet.target_address == target_address)
        assert (received_packet_record.source_address == sent_packet_record.source_address
                == packet.source_address == source_address)
        assert (received_packet_record.address_extension == sent_packet_record.address_extension
                == packet.address_extension == address_extension)

    @pytest.mark.parametrize("message, n_cs, n_br, block_size, st_min, wait_count, repeat_wait, send_after, timeout", [
        (UdsMessage(payload=[0x22, 0x12, 0x34], addressing_type=AddressingType.PHYSICAL),
         None, 0, 0, 0, 0, False, 10, 50),
        (UdsMessage(payload=[0x50, 0x01], addressing_type=AddressingType.FUNCTIONAL),
         None, 0, 0, 0, 0, False, 950, 1000),
        (UdsMessage(payload=[0x22, *range(62)], addressing_type=AddressingType.PHYSICAL),
         1, 800, 5, 50, 2, True, 100, 1000),
        (UdsMessage(payload=[0x62, 0x12, 0x34, *range(100, 250)], addressing_type=AddressingType.PHYSICAL),
         None, 100, 1, 127, 1, False, 950, 1000),
    ])
    def test_send_message_on_one_receive_on_other_bus(self, example_addressing_information,
                                                      example_addressing_information_2nd_node,
                                                      message, send_after, timeout,
                                                      n_cs, n_br, block_size, st_min, wait_count, repeat_wait):
        """
        Check for sending and receiving UDS message using two Transport Interfaces.

        Procedure:
        1. Send a UDS message using Transport Interface 1 (via CAN Interface 1).
            Expected: UDS message record returned.
        2. Receive a UDS message using Transport Interface 2 (via CAN Interface 2).
            Expected: UDS message is received.
        3. Validate received UDS message records attributes.
            Expected: Attributes of UDS message records are in line with each other
                (the same packet was received and transmitted).

        :param example_addressing_information: Addressing Information for a receiving CAN Node.
        :param example_addressing_information_2nd_node: Addressing Information for a transmitting CAN Node.
            It is compatible with `example_addressing_information`.
        :param message: UDS message to send.
        :param send_after: Delay after which message to be sent after message reception [ms].
        :param timeout: Timeout value to pass to receive message method [ms].
        :param n_cs: Value of N_Cs time parameter to use by sending node [ms].
        :param n_br: Value of N_Br time parameter to use by receiving node [ms].
        :param block_size: Block size parameter to send in Flow Control packets by receiving node.
        :param st_min: STmin parameter to send in Flow Control packets by receiving node.
        :param wait_count: Number of Flow Control frames with WAIT Flow Status to send by receiving node.
        :param repeat_wait: Whether receiving node shall repeat Flow Control frames with WAIT Flow Status.
        """
        flow_control_parameters_generator = DefaultFlowControlParametersGenerator(block_size=block_size,
                                                                                  st_min=st_min,
                                                                                  wait_count=wait_count,
                                                                                  repeat_wait=repeat_wait)
        can_transport_interface_1 = PyCanTransportInterface(
            can_bus_manager=self.can_interface_1,
            addressing_information=example_addressing_information,
            n_br=n_br,
            flow_control_parameters_generator=flow_control_parameters_generator)
        can_transport_interface_2 = PyCanTransportInterface(
            can_bus_manager=self.can_interface_2,
            addressing_information=example_addressing_information_2nd_node,
            n_cs=n_cs)

        timer = self.send_message(can_transport_interface=can_transport_interface_2,
                                  message=message,
                                  delay=send_after)
        received_message_record = can_transport_interface_1.receive_message(timeout=timeout)
        while not timer.finished.is_set():
            sleep(0.001)
        assert isinstance(self.sent_message, UdsMessageRecord)
        assert isinstance(received_message_record, UdsMessageRecord)
        assert self.sent_message.direction == TransmissionDirection.TRANSMITTED
        assert received_message_record.direction == TransmissionDirection.RECEIVED
        assert self.sent_message.addressing_type == received_message_record.addressing_type == message.addressing_type
        assert self.sent_message.payload == received_message_record.payload == message.payload

    @pytest.mark.parametrize("message, n_cs, n_br, block_size, st_min, wait_count, repeat_wait, send_after, timeout", [
        (UdsMessage(payload=[0x22, 0x12, 0x34], addressing_type=AddressingType.PHYSICAL),
         None, 0, 0, 0, 0, False, 10, 50),
        (UdsMessage(payload=[0x50, 0x01], addressing_type=AddressingType.FUNCTIONAL),
         None, 0, 0, 0, 0, False, 950, 1000),
        (UdsMessage(payload=[0x22, *range(62)], addressing_type=AddressingType.PHYSICAL),
         1, 800, 5, 50, 2, True, 100, 1000),
        (UdsMessage(payload=[0x62, 0x12, 0x34, *range(100, 250)], addressing_type=AddressingType.PHYSICAL),
         None, 100, 1, 127, 1, False, 950, 1000),
    ])
    @pytest.mark.asyncio
    async def test_async_send_message_on_one_receive_on_other_bus(self, example_addressing_information,
                                                                  example_addressing_information_2nd_node,
                                                                  message, send_after, timeout,
                                                                  n_cs, n_br, block_size, st_min, wait_count,
                                                                  repeat_wait):
        """
        Check for asynchronous sending and receiving UDS message using two Transport Interfaces.

        Procedure:
        1. Send (using async method) a UDS message using Transport Interface 1 (via CAN Interface 1).
            Expected: UDS message record returned.
        2. Receive (using async method) a UDS message using Transport Interface 2 (via CAN Interface 2).
            Expected: UDS message is received.
        3. Validate received UDS message records attributes.
            Expected: Attributes of UDS message records are in line with each other
                (the same packet was received and transmitted).

        :param example_addressing_information: Addressing Information for a receiving CAN Node.
        :param example_addressing_information_2nd_node: Addressing Information for a transmitting CAN Node.
            It is compatible with `example_addressing_information`.
        :param message: UDS message to send.
        :param send_after: Delay after which message to be sent after message reception [ms].
        :param timeout: Timeout value to pass to receive message method [ms].
        :param n_cs: Value of N_Cs time parameter to use by sending node [ms].
        :param n_br: Value of N_Br time parameter to use by receiving node [ms].
        :param block_size: Block size parameter to send in Flow Control packets by receiving node.
        :param st_min: STmin parameter to send in Flow Control packets by receiving node.
        :param wait_count: Number of Flow Control frames with WAIT Flow Status to send by receiving node.
        :param repeat_wait: Whether receiving node shall repeat Flow Control frames with WAIT Flow Status.
        """
        flow_control_parameters_generator = DefaultFlowControlParametersGenerator(block_size=block_size,
                                                                                  st_min=st_min,
                                                                                  wait_count=wait_count,
                                                                                  repeat_wait=repeat_wait)
        can_transport_interface_1 = PyCanTransportInterface(
            can_bus_manager=self.can_interface_1,
            addressing_information=example_addressing_information,
            n_br=n_br,
            flow_control_parameters_generator=flow_control_parameters_generator)
        can_transport_interface_2 = PyCanTransportInterface(
            can_bus_manager=self.can_interface_2,
            addressing_information=example_addressing_information_2nd_node,
            n_cs=n_cs)

        receive_message_task = asyncio.create_task(can_transport_interface_1.async_receive_message(timeout=timeout))
        sent_message_record = await can_transport_interface_2.async_send_message(message=message)
        received_message_record = await receive_message_task
        assert isinstance(sent_message_record, UdsMessageRecord)
        assert isinstance(received_message_record, UdsMessageRecord)
        assert sent_message_record.direction == TransmissionDirection.TRANSMITTED
        assert received_message_record.direction == TransmissionDirection.RECEIVED
        assert sent_message_record.addressing_type == received_message_record.addressing_type == message.addressing_type
        assert sent_message_record.payload == received_message_record.payload == message.payload


class AbstractErrorGuessingTests(AbstractPythonCanTests, ABC):
    """Common implementation of guessing errors system tests."""

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_information, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
                                  tx_physical={"can_id": 0x611},
                                  rx_physical={"can_id": 0x612},
                                  tx_functional={"can_id": 0x6FF},
                                  rx_functional={"can_id": 0x6FE}),
         {"filler_byte": 0x1E, "payload": [0x10, 0x04]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                  tx_physical={"can_id": 0xDA1BFF, "target_address": 0x1B, "source_address": 0xFF},
                                  rx_physical={"can_id": 0xDAFF1B, "target_address": 0xFF, "source_address": 0x1B},
                                  tx_functional={"can_id": 0x1CDBACFE, "target_address": 0xAC, "source_address": 0xFE},
                                  rx_functional={"can_id": 0x1CDBFEAC, "target_address": 0xFE, "source_address": 0xAC}),
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x13}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                  tx_physical={"can_id": 0x987, "target_address": 0x90},
                                  rx_physical={"can_id": 0x987, "target_address": 0xFE},
                                  tx_functional={"can_id": 0x11766, "target_address": 0xFF},
                                  rx_functional={"can_id": 0x11765, "target_address": 0xFF}),
         {"payload": [0x32, 0xFF], "sequence_number": 0xF}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x651, "address_extension": 0x87},
                                  rx_physical={"can_id": 0x652, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x6FE, "address_extension": 0xA5},
                                  rx_functional={"can_id": 0x6FF, "address_extension": 0xA5}),
         {"dlc": 8, "flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x15, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF, "address_extension": 0x87},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x1CCDACFE, "target_address": 0xAC, "source_address": 0xFE, "address_extension": 0xFF},
                                  rx_functional={"can_id": 0x1CCDFEAC, "target_address": 0xFE, "source_address": 0xAC, "address_extension": 0xFF}),
         {"filler_byte": 0xBC, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A, 0x12, 0xBC], "dlc": 0xF}),
    ])
    def test_timeout_then_send_packet(self, packet_type, addressing_type, addressing_information, packet_type_specific_kwargs):
        """
        Check for sending a CAN packet after a timeout exception during receiving.

        Procedure:
        1. Call method to receive packet via Transport Interface.
            Expected: Timeout exception is raised.
        2. Send a CAN packet via Transport Interface.
            Expected: CAN packet record returned.
        3. Validate transmitted CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the transmitted CAN packet.

        :param packet_type: Type of CAN packet to send.
        :param addressing_type: Addressing type to use for transmitting a CAN packet.
        :param addressing_information: Example Addressing Information of a CAN Node.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        """
        if addressing_type == AddressingType.PHYSICAL:
            can_id = addressing_information.tx_packets_physical_ai["can_id"]
            target_address = addressing_information.tx_packets_physical_ai["target_address"]
            source_address = addressing_information.tx_packets_physical_ai["source_address"]
            address_extension = addressing_information.tx_packets_physical_ai["address_extension"]
        else:
            can_id = addressing_information.tx_packets_functional_ai["can_id"]
            target_address = addressing_information.tx_packets_functional_ai["target_address"]
            source_address = addressing_information.tx_packets_functional_ai["source_address"]
            address_extension = addressing_information.tx_packets_functional_ai["address_extension"]
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=addressing_information)
        packet = CanPacket(packet_type=packet_type,
                           addressing_format=addressing_information.addressing_format,
                           addressing_type=addressing_type,
                           can_id=can_id,
                           target_address=target_address,
                           source_address=source_address,
                           address_extension=address_extension,
                           **packet_type_specific_kwargs)
        with pytest.raises(TimeoutError):
            can_transport_interface.receive_packet(timeout=100)
        packet_record = can_transport_interface.send_packet(packet)
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.TRANSMITTED
        assert packet_record.raw_frame_data == packet.raw_frame_data
        assert packet_record.addressing_format == packet.addressing_format == addressing_information.addressing_format
        assert packet_record.packet_type == packet.packet_type == packet_type
        assert packet_record.can_id == packet.can_id == can_id
        assert packet_record.addressing_type == packet.addressing_type == addressing_type
        assert packet_record.target_address == packet.target_address == target_address
        assert packet_record.source_address == packet.source_address == source_address
        assert packet_record.address_extension == packet.address_extension == address_extension

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_information, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
                                  tx_physical={"can_id": 0x611},
                                  rx_physical={"can_id": 0x612},
                                  tx_functional={"can_id": 0x6FF},
                                  rx_functional={"can_id": 0x6FE}),
         {"filler_byte": 0x1E, "payload": [0x10, 0x04]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                  tx_physical={"can_id": 0xDA1BFF, "target_address": 0x1B, "source_address": 0xFF},
                                  rx_physical={"can_id": 0xDAFF1B, "target_address": 0xFF, "source_address": 0x1B},
                                  tx_functional={"can_id": 0x1CDBACFE, "target_address": 0xAC, "source_address": 0xFE},
                                  rx_functional={"can_id": 0x1CDBFEAC, "target_address": 0xFE, "source_address": 0xAC}),
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x13}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                  tx_physical={"can_id": 0x987, "target_address": 0x90},
                                  rx_physical={"can_id": 0x987, "target_address": 0xFE},
                                  tx_functional={"can_id": 0x11766, "target_address": 0xFF},
                                  rx_functional={"can_id": 0x11765, "target_address": 0xFF}),
         {"payload": [0x32, 0xFF], "sequence_number": 0xF}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x651, "address_extension": 0x87},
                                  rx_physical={"can_id": 0x652, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x6FE, "address_extension": 0xA5},
                                  rx_functional={"can_id": 0x6FF, "address_extension": 0xA5}),
         {"dlc": 8, "flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x15, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF, "address_extension": 0x87},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x1CCDACFE, "target_address": 0xAC, "source_address": 0xFE, "address_extension": 0xFF},
                                  rx_functional={"can_id": 0x1CCDFEAC, "target_address": 0xFE, "source_address": 0xAC, "address_extension": 0xFF}),
         {"filler_byte": 0xBC, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A, 0x12, 0xBC], "dlc": 0xF}),
    ])
    @pytest.mark.asyncio
    async def test_async_timeout_then_send_packet(self, packet_type, addressing_type, addressing_information,
                                     packet_type_specific_kwargs):
        """
        Check for asynchronous sending a CAN packet after a timeout exception during asynchronous receiving.

        Procedure:
        1. Call async method to receive packet via Transport Interface.
            Expected: Timeout exception is raised.
        2. Send (using async method) a CAN packet via Transport Interface.
            Expected: CAN packet record returned.
        3. Validate transmitted CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the transmitted CAN packet.

        :param packet_type: Type of CAN packet to send.
        :param addressing_type: Addressing type to use for transmitting a CAN packet.
        :param addressing_information: Example Addressing Information of a CAN Node.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        """
        if addressing_type == AddressingType.PHYSICAL:
            can_id = addressing_information.tx_packets_physical_ai["can_id"]
            target_address = addressing_information.tx_packets_physical_ai["target_address"]
            source_address = addressing_information.tx_packets_physical_ai["source_address"]
            address_extension = addressing_information.tx_packets_physical_ai["address_extension"]
        else:
            can_id = addressing_information.tx_packets_functional_ai["can_id"]
            target_address = addressing_information.tx_packets_functional_ai["target_address"]
            source_address = addressing_information.tx_packets_functional_ai["source_address"]
            address_extension = addressing_information.tx_packets_functional_ai["address_extension"]
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=addressing_information)
        packet = CanPacket(packet_type=packet_type,
                           addressing_format=addressing_information.addressing_format,
                           addressing_type=addressing_type,
                           can_id=can_id,
                           target_address=target_address,
                           source_address=source_address,
                           address_extension=address_extension,
                           **packet_type_specific_kwargs)
        with pytest.raises((TimeoutError, asyncio.TimeoutError)):
            await can_transport_interface.async_receive_packet(timeout=100)
        packet_record = await can_transport_interface.async_send_packet(packet)
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.TRANSMITTED
        assert packet_record.raw_frame_data == packet.raw_frame_data
        assert packet_record.addressing_format == packet.addressing_format == addressing_information.addressing_format
        assert packet_record.packet_type == packet.packet_type == packet_type
        assert packet_record.can_id == packet.can_id == can_id
        assert packet_record.addressing_type == packet.addressing_type == addressing_type
        assert packet_record.target_address == packet.target_address == target_address
        assert packet_record.source_address == packet.source_address == source_address
        assert packet_record.address_extension == packet.address_extension == address_extension

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_information, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
                                  tx_physical={"can_id": 0x611},
                                  rx_physical={"can_id": 0x612},
                                  tx_functional={"can_id": 0x6FF},
                                  rx_functional={"can_id": 0x6FE}),
         {"filler_byte": 0x1E, "payload": [0x10, 0x04]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                  tx_physical={"can_id": 0xDA1BFF, "target_address": 0x1B, "source_address": 0xFF},
                                  rx_physical={"can_id": 0xDAFF1B, "target_address": 0xFF, "source_address": 0x1B},
                                  tx_functional={"can_id": 0x1CDBACFE, "target_address": 0xAC, "source_address": 0xFE},
                                  rx_functional={"can_id": 0x1CDBFEAC, "target_address": 0xFE, "source_address": 0xAC}),
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x13}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                  tx_physical={"can_id": 0x987, "target_address": 0x90},
                                  rx_physical={"can_id": 0x987, "target_address": 0xFE},
                                  tx_functional={"can_id": 0x11766, "target_address": 0xFF},
                                  rx_functional={"can_id": 0x11765, "target_address": 0xFF}),
         {"payload": [0x32, 0xFF], "sequence_number": 0xF}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x651, "address_extension": 0x87},
                                  rx_physical={"can_id": 0x652, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x6FE, "address_extension": 0xA5},
                                  rx_functional={"can_id": 0x6FF, "address_extension": 0xA5}),
         {"dlc": 8, "flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x15, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF, "address_extension": 0x87},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x1CCDACFE, "target_address": 0xAC, "source_address": 0xFE, "address_extension": 0xFF},
                                  rx_functional={"can_id": 0x1CCDFEAC, "target_address": 0xFE, "source_address": 0xAC, "address_extension": 0xFF}),
         {"filler_byte": 0xBC, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A, 0x12, 0xBC], "dlc": 0xF}),
    ])
    def test_timeout_then_receive_packet(self, packet_type, addressing_type, addressing_information,
                                         packet_type_specific_kwargs):
        """
        Check for receiving a CAN packet after a timeout exception during receiving.

        Procedure:
        1. Call method to receive packet via Transport Interface.
            Expected: Timeout exception is raised.
        2. Send a CAN frame that carries CAN packet targeting configured CAN Node.
        3. Call method to receive packet via Transport Interface.
            Expected: CAN packet is received.
        4. Validate received CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the received CAN packet.

        :param packet_type: Type of CAN packet to send.
        :param addressing_type: Addressing type to use for transmitting a CAN packet.
        :param addressing_information: Example Addressing Information of a CAN Node.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        """
        if addressing_type == AddressingType.PHYSICAL:
            can_id = addressing_information.rx_packets_physical_ai["can_id"]
            target_address = addressing_information.rx_packets_physical_ai["target_address"]
            source_address = addressing_information.rx_packets_physical_ai["source_address"]
            address_extension = addressing_information.rx_packets_physical_ai["address_extension"]
        else:
            can_id = addressing_information.rx_packets_functional_ai["can_id"]
            target_address = addressing_information.rx_packets_functional_ai["target_address"]
            source_address = addressing_information.rx_packets_functional_ai["source_address"]
            address_extension = addressing_information.rx_packets_functional_ai["address_extension"]
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=addressing_information)
        packet = CanPacket(packet_type=packet_type,
                           addressing_format=addressing_information.addressing_format,
                           addressing_type=addressing_type,
                           can_id=can_id,
                           target_address=target_address,
                           source_address=source_address,
                           address_extension=address_extension,
                           **packet_type_specific_kwargs)
        can_frame = Message(arbitration_id=packet.can_id,
                            data=packet.raw_frame_data,
                            is_fd=packet.dlc > 8)
        with pytest.raises(TimeoutError):
            can_transport_interface.receive_packet(timeout=100)
        datetime_before_send = datetime.now()
        self.can_interface_2.send(can_frame)
        packet_record = can_transport_interface.receive_packet(timeout=100)
        datetime_after_receive = datetime.now()
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.RECEIVED
        assert packet_record.raw_frame_data == tuple(can_frame.data)
        assert packet_record.addressing_format == addressing_information.addressing_format
        assert packet_record.addressing_type == addressing_type
        assert packet_record.can_id == can_frame.arbitration_id == can_id
        assert packet_record.target_address == target_address
        assert packet_record.source_address == source_address
        assert packet_record.address_extension == address_extension
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            assert datetime_before_send < packet_record.transmission_time < datetime_after_receive

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_information, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
                                  tx_physical={"can_id": 0x611},
                                  rx_physical={"can_id": 0x612},
                                  tx_functional={"can_id": 0x6FF},
                                  rx_functional={"can_id": 0x6FE}),
         {"filler_byte": 0x1E, "payload": [0x10, 0x04]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                  tx_physical={"can_id": 0xDA1BFF, "target_address": 0x1B, "source_address": 0xFF},
                                  rx_physical={"can_id": 0xDAFF1B, "target_address": 0xFF, "source_address": 0x1B},
                                  tx_functional={"can_id": 0x1CDBACFE, "target_address": 0xAC, "source_address": 0xFE},
                                  rx_functional={"can_id": 0x1CDBFEAC, "target_address": 0xFE, "source_address": 0xAC}),
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x13}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                  tx_physical={"can_id": 0x987, "target_address": 0x90},
                                  rx_physical={"can_id": 0x987, "target_address": 0xFE},
                                  tx_functional={"can_id": 0x11766, "target_address": 0xFF},
                                  rx_functional={"can_id": 0x11765, "target_address": 0xFF}),
         {"payload": [0x32, 0xFF], "sequence_number": 0xF}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x651, "address_extension": 0x87},
                                  rx_physical={"can_id": 0x652, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x6FE, "address_extension": 0xA5},
                                  rx_functional={"can_id": 0x6FF, "address_extension": 0xA5}),
         {"dlc": 8, "flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x15, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF, "address_extension": 0x87},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x1CCDACFE, "target_address": 0xAC, "source_address": 0xFE, "address_extension": 0xFF},
                                  rx_functional={"can_id": 0x1CCDFEAC, "target_address": 0xFE, "source_address": 0xAC, "address_extension": 0xFF}),
         {"filler_byte": 0xBC, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A, 0x12, 0xBC], "dlc": 0xF}),
    ])
    @pytest.mark.asyncio
    async def test_async_timeout_then_receive_packet(self, packet_type, addressing_type, addressing_information,
                                                     packet_type_specific_kwargs):
        """
        Check for asynchronous receiving a CAN packet after a timeout exception during receiving.

        Procedure:
        1. Call async method to receive packet via Transport Interface.
            Expected: Timeout exception is raised.
        2. Send a CAN frame that carries CAN packet targeting configured CAN Node.
        3. Call async method to receive packet via Transport Interface.
            Expected: CAN packet is received.
        4. Validate received CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the received CAN packet.

        :param packet_type: Type of CAN packet to send.
        :param addressing_type: Addressing type to use for transmitting a CAN packet.
        :param addressing_information: Example Addressing Information of a CAN Node.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        """
        if addressing_type == AddressingType.PHYSICAL:
            can_id = addressing_information.rx_packets_physical_ai["can_id"]
            target_address = addressing_information.rx_packets_physical_ai["target_address"]
            source_address = addressing_information.rx_packets_physical_ai["source_address"]
            address_extension = addressing_information.rx_packets_physical_ai["address_extension"]
        else:
            can_id = addressing_information.rx_packets_functional_ai["can_id"]
            target_address = addressing_information.rx_packets_functional_ai["target_address"]
            source_address = addressing_information.rx_packets_functional_ai["source_address"]
            address_extension = addressing_information.rx_packets_functional_ai["address_extension"]
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=addressing_information)
        packet = CanPacket(packet_type=packet_type,
                           addressing_format=addressing_information.addressing_format,
                           addressing_type=addressing_type,
                           can_id=can_id,
                           target_address=target_address,
                           source_address=source_address,
                           address_extension=address_extension,
                           **packet_type_specific_kwargs)
        can_frame = Message(arbitration_id=packet.can_id,
                            data=packet.raw_frame_data,
                            is_fd=packet.dlc > 8)
        with pytest.raises((TimeoutError, asyncio.TimeoutError)):
            await can_transport_interface.async_receive_packet(timeout=100)
        datetime_before_send = datetime.now()
        self.can_interface_2.send(can_frame)
        packet_record = await can_transport_interface.async_receive_packet(timeout=100)
        datetime_after_receive = datetime.now()
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.RECEIVED
        assert packet_record.raw_frame_data == tuple(can_frame.data)
        assert packet_record.addressing_format == addressing_information.addressing_format
        assert packet_record.addressing_type == addressing_type
        assert packet_record.can_id == can_frame.arbitration_id == can_id
        assert packet_record.target_address == target_address
        assert packet_record.source_address == source_address
        assert packet_record.address_extension == address_extension
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            assert datetime_before_send < packet_record.transmission_time < datetime_after_receive

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_information, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
                                  tx_physical={"can_id": 0x611},
                                  rx_physical={"can_id": 0x612},
                                  tx_functional={"can_id": 0x6FF},
                                  rx_functional={"can_id": 0x6FE}),
         {"filler_byte": 0x1E, "payload": [0x10, 0x04]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                  tx_physical={"can_id": 0xDA1BFF, "target_address": 0x1B, "source_address": 0xFF},
                                  rx_physical={"can_id": 0xDAFF1B, "target_address": 0xFF, "source_address": 0x1B},
                                  tx_functional={"can_id": 0x1CDBACFE, "target_address": 0xAC, "source_address": 0xFE},
                                  rx_functional={"can_id": 0x1CDBFEAC, "target_address": 0xFE, "source_address": 0xAC}),
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x13}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                  tx_physical={"can_id": 0x987, "target_address": 0x90},
                                  rx_physical={"can_id": 0x987, "target_address": 0xFE},
                                  tx_functional={"can_id": 0x11766, "target_address": 0xFF},
                                  rx_functional={"can_id": 0x11765, "target_address": 0xFF}),
         {"payload": [0x32, 0xFF], "sequence_number": 0xF}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x651, "address_extension": 0x87},
                                  rx_physical={"can_id": 0x652, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x6FE, "address_extension": 0xA5},
                                  rx_functional={"can_id": 0x6FF, "address_extension": 0xA5}),
         {"dlc": 8, "flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x15, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF, "address_extension": 0x87},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x1CCDACFE, "target_address": 0xAC, "source_address": 0xFE, "address_extension": 0xFF},
                                  rx_functional={"can_id": 0x1CCDFEAC, "target_address": 0xFE, "source_address": 0xAC, "address_extension": 0xFF}),
         {"filler_byte": 0xBC, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A, 0x12, 0xBC], "dlc": 0xF}),
    ])
    def test_observe_tx_packet(self, packet_type, addressing_type, addressing_information, packet_type_specific_kwargs):
        """
        Check for transmitting a CAN packet after a sending identical CAN frame.

        Procedure:
        1. Send a CAN frame (which is identical to a future CAN packet) directly using CAN interface.
        2. Send a CAN packet via Transport Interface.
            Expected: CAN packet record returned.
        2. Validate transmitted CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the transmitted CAN packet.
                Make sure timing confirms that it is packet transmitted in step two.

        :param packet_type: Type of CAN packet to send.
        :param addressing_type: Addressing type to use for transmitting a CAN packet.
        :param addressing_information: Example Addressing Information of a CAN Node.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        """
        if addressing_type == AddressingType.PHYSICAL:
            can_id = addressing_information.tx_packets_physical_ai["can_id"]
            target_address = addressing_information.tx_packets_physical_ai["target_address"]
            source_address = addressing_information.tx_packets_physical_ai["source_address"]
            address_extension = addressing_information.tx_packets_physical_ai["address_extension"]
        else:
            can_id = addressing_information.tx_packets_functional_ai["can_id"]
            target_address = addressing_information.tx_packets_functional_ai["target_address"]
            source_address = addressing_information.tx_packets_functional_ai["source_address"]
            address_extension = addressing_information.tx_packets_functional_ai["address_extension"]
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=addressing_information)
        packet = CanPacket(packet_type=packet_type,
                           addressing_format=addressing_information.addressing_format,
                           addressing_type=addressing_type,
                           can_id=can_id,
                           target_address=target_address,
                           source_address=source_address,
                           address_extension=address_extension,
                           **packet_type_specific_kwargs)
        can_frame = Message(arbitration_id=packet.can_id,
                            data=packet.raw_frame_data,
                            is_fd=packet.dlc > 8)
        self.can_interface_1.send(can_frame)
        sleep(0.1)
        datetime_before_send = datetime.now()
        packet_record = can_transport_interface.send_packet(packet)
        datetime_after_send = datetime.now()
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.TRANSMITTED
        assert packet_record.raw_frame_data == packet.raw_frame_data
        assert packet_record.addressing_format == packet.addressing_format == addressing_information.addressing_format
        assert packet_record.packet_type == packet.packet_type == packet_type
        assert packet_record.can_id == packet.can_id == can_id
        assert packet_record.addressing_type == packet.addressing_type == addressing_type
        assert packet_record.target_address == packet.target_address == target_address
        assert packet_record.source_address == packet.source_address == source_address
        assert packet_record.address_extension == packet.address_extension == address_extension
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            assert datetime_before_send < packet_record.transmission_time < datetime_after_send

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_information, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
                                  tx_physical={"can_id": 0x611},
                                  rx_physical={"can_id": 0x612},
                                  tx_functional={"can_id": 0x6FF},
                                  rx_functional={"can_id": 0x6FE}),
         {"filler_byte": 0x1E, "payload": [0x10, 0x04]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                  tx_physical={"can_id": 0xDA1BFF, "target_address": 0x1B, "source_address": 0xFF},
                                  rx_physical={"can_id": 0xDAFF1B, "target_address": 0xFF, "source_address": 0x1B},
                                  tx_functional={"can_id": 0x1CDBACFE, "target_address": 0xAC, "source_address": 0xFE},
                                  rx_functional={"can_id": 0x1CDBFEAC, "target_address": 0xFE, "source_address": 0xAC}),
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x13}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                  tx_physical={"can_id": 0x987, "target_address": 0x90},
                                  rx_physical={"can_id": 0x987, "target_address": 0xFE},
                                  tx_functional={"can_id": 0x11766, "target_address": 0xFF},
                                  rx_functional={"can_id": 0x11765, "target_address": 0xFF}),
         {"payload": [0x32, 0xFF], "sequence_number": 0xF}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x651, "address_extension": 0x87},
                                  rx_physical={"can_id": 0x652, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x6FE, "address_extension": 0xA5},
                                  rx_functional={"can_id": 0x6FF, "address_extension": 0xA5}),
         {"dlc": 8, "flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x15, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF, "address_extension": 0x87},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B, "address_extension": 0x87},
                                  tx_functional={"can_id": 0x1CCDACFE, "target_address": 0xAC, "source_address": 0xFE, "address_extension": 0xFF},
                                  rx_functional={"can_id": 0x1CCDFEAC, "target_address": 0xFE, "source_address": 0xAC, "address_extension": 0xFF}),
         {"filler_byte": 0xBC, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A, 0x12, 0xBC], "dlc": 0xF}),
    ])
    @pytest.mark.asyncio
    async def test_async_observe_tx_packet(self, packet_type, addressing_type, addressing_information,
                                           packet_type_specific_kwargs):
        """
        Check for asynchronous transmitting a CAN packet after a sending identical CAN frame.

        Procedure:
        1. Send a CAN frame (which is identical to a future CAN packet) directly using CAN interface.
        2. Send (using async method) a CAN packet via Transport Interface.
            Expected: CAN packet record returned.
        2. Validate transmitted CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the transmitted CAN packet.
                Make sure timing confirms that it is packet transmitted in step two.

        :param packet_type: Type of CAN packet to send.
        :param addressing_type: Addressing type to use for transmitting a CAN packet.
        :param addressing_information: Example Addressing Information of a CAN Node.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        """
        if addressing_type == AddressingType.PHYSICAL:
            can_id = addressing_information.tx_packets_physical_ai["can_id"]
            target_address = addressing_information.tx_packets_physical_ai["target_address"]
            source_address = addressing_information.tx_packets_physical_ai["source_address"]
            address_extension = addressing_information.tx_packets_physical_ai["address_extension"]
        else:
            can_id = addressing_information.tx_packets_functional_ai["can_id"]
            target_address = addressing_information.tx_packets_functional_ai["target_address"]
            source_address = addressing_information.tx_packets_functional_ai["source_address"]
            address_extension = addressing_information.tx_packets_functional_ai["address_extension"]
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=addressing_information)
        packet = CanPacket(packet_type=packet_type,
                           addressing_format=addressing_information.addressing_format,
                           addressing_type=addressing_type,
                           can_id=can_id,
                           target_address=target_address,
                           source_address=source_address,
                           address_extension=address_extension,
                           **packet_type_specific_kwargs)
        can_frame = Message(arbitration_id=packet.can_id,
                            data=packet.raw_frame_data,
                            is_fd=packet.dlc > 8)
        self.can_interface_1.send(can_frame)
        sleep(0.1)
        datetime_before_send = datetime.now()
        packet_record = await can_transport_interface.async_send_packet(packet)
        datetime_after_send = datetime.now()
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.TRANSMITTED
        assert packet_record.raw_frame_data == packet.raw_frame_data
        assert packet_record.payload == packet.payload
        assert packet_record.can_id == packet.can_id
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            assert datetime_before_send < packet_record.transmission_time < datetime_after_send

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, *range(62)], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x62, 0x12, 0x34, *range(100, 250)], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        # TODO: adjust values to be closer to boundary when https://github.com/mdabrowski1990/uds/issues/228 resolved
        (1000, 970),  # ms
        (50, 20),
    ])
    def test_overflow_during_message_sending(self, example_addressing_information,
                                             example_addressing_information_2nd_node,
                                             message, timeout, send_after):
        """
        Check for handling Overflow status during synchronous multi packet (FF + CF) UDS message sending.

        Procedure:
        1. Schedule Flow Control CAN Packet with Overflow information.
        2. Send a UDS message using Transport Interface (via CAN Interface).
            Expected: UDS message transmission stopped and an exception raised.

        :param example_addressing_information: Example Addressing Information of a CAN Node.
        :param example_addressing_information_2nd_node: Example Addressing Information of a CAN Node.
        :param message: UDS message to send.
        :param send_after: Delay to use for sending CAN flow control.
        """
        can_transport_interface = PyCanTransportInterface(
            can_bus_manager=self.can_interface_1,
            addressing_information=example_addressing_information,
            n_bs_timeout=timeout)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            can_bus_manager=self.can_interface_2,
            addressing_information=example_addressing_information_2nd_node)
        flow_control_packet = can_transport_interface_2nd_node.segmenter.get_flow_control_packet(
            flow_status=CanFlowStatus.Overflow)
        self.send_packet(can_transport_interface=can_transport_interface_2nd_node,
                         packet=flow_control_packet,
                         delay=send_after)
        with pytest.raises(OverflowError):
            can_transport_interface.send_message(message)

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, *range(62)], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x62, 0x12, 0x34, *range(100, 250)], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        # TODO: adjust values to be closer to boundary when https://github.com/mdabrowski1990/uds/issues/228 resolved
        (1000, 950),  # ms
        (50, 10),
    ])
    @pytest.mark.asyncio
    async def test_overflow_during_async_message_sending(self, example_addressing_information,
                                                         example_addressing_information_2nd_node,
                                                         message, timeout, send_after):
        """
        Check for handling Overflow status during asynchronous multi packet (FF + CF) UDS message sending.

        Procedure:
        1. Schedule Flow Control CAN Packet with Overflow information.
        2. Send (using async method) a UDS message using Transport Interface (via CAN Interface).
            Expected: UDS message transmission stopped and an exception raised.

        :param example_addressing_information: Example Addressing Information of a CAN Node.
        :param example_addressing_information_2nd_node: Example Addressing Information of a CAN Node.
        :param message: UDS message to send.
        :param send_after: Delay to use for sending CAN flow control.
        """
        can_transport_interface = PyCanTransportInterface(
            can_bus_manager=self.can_interface_1,
            addressing_information=example_addressing_information,
            n_bs_timeout=timeout)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            can_bus_manager=self.can_interface_2,
            addressing_information=example_addressing_information_2nd_node)
        flow_control_packet = can_transport_interface_2nd_node.segmenter.get_flow_control_packet(
            flow_status=CanFlowStatus.Overflow)
        send_packet_task = asyncio.create_task(self.async_send_packet(
            can_transport_interface=can_transport_interface_2nd_node,
            packet=flow_control_packet,
            delay=send_after))
        with pytest.raises(OverflowError):
            await can_transport_interface.async_send_message(message)
        await send_packet_task

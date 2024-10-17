import asyncio
from abc import abstractmethod
from datetime import datetime
from threading import Timer
from time import sleep, time
from typing import Optional

import pytest
from tests.system_tests.transport_interface.can.common import AbstractCanTests

from can import Bus, Message
from uds.can import CanAddressingFormat, CanAddressingInformation, CanFlowStatus, DefaultFlowControlParametersGenerator
from uds.message import UdsMessage, UdsMessageRecord
from uds.packet import CanPacket, CanPacketRecord, CanPacketType
from uds.segmentation import CanSegmenter
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

    DELAY_AFTER_RECEIVING_FRAME = 10.  # ms
    DELAY_AFTER_RECEIVING_MESSAGE = 1000.  # ms

    # TODO: https://github.com/mdabrowski1990/uds/issues/228 - set MAKE_TIMING_CHECKS to true when resolved
    MAKE_TIMING_CHECKS: bool = False

    @abstractmethod
    def setup_class(self):
        """Create bus objects."""
        self.can_interface_1: Bus  # TODO: configure accordingly to hardware setup
        self.can_interface_2: Bus   # TODO: configure accordingly to hardware setup
        self.sent_message: Optional[UdsMessageRecord] = None

    def setup_method(self):
        """Prepare CAN bus objects for tests."""
        self.can_interface_1.flush_tx_buffer()
        self.can_interface_2.flush_tx_buffer()
        self.sent_message = None

    def teardown_class(self):
        """Safely close CAN bus objects."""
        self.can_interface_1.shutdown()
        self.can_interface_2.shutdown()

    @staticmethod
    def send_packet(can_interface: Bus,
                    packet: CanPacket,
                    delay: TimeMillisecondsAlias) -> Timer:
        """
        Send CAN packet over CAN interface.

        :param can_interface: CAN interface to send the packet over.
        :param packet: CAN packet to send.
        :param delay: Time [ms] after which the transmission will be started.

        :return: Timer object with scheduled task.
        """
        can_frame = Message(arbitration_id=packet.can_id,
                            data=packet.raw_frame_data)
        timer = Timer(interval=delay / 1000., function=can_interface.send, args=(can_frame, ))
        timer.start()
        return timer

    @staticmethod
    async def async_send_packet(can_interface: Bus,
                                packet: CanPacket,
                                delay: TimeMillisecondsAlias) -> CanPacketRecord:
        """
        Send CAN packet asynchronously over CAN interface.

        :param can_interface: CAN interface to send the packet over.
        :param packet: CAN packet to send.
        :param delay: Time [ms] after which the transmission will be started.

        :return: Future CAN packet record.
        """
        can_frame = Message(arbitration_id=packet.can_id,
                            data=packet.raw_frame_data)
        await asyncio.sleep(delay / 1000.)
        return can_interface.send(can_frame)

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


class AbstractCanPacketTests(AbstractPythonCanTests):
    """Common implementation of system tests related to sending and receiving CAN packets."""

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_information, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
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
         AddressingType.PHYSICAL,
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

    async def test_async_send_packet(self):
        """Test asynchronous sending of CAN packet."""
        # TODO: fill like the one above
        # TODO: make sure AddressingInformation objects are correct. You can base on existing ones in this file.
        # TODO: for all test methods, replace custom code with self.send_packet, self.async_send_packet,
        #  self.send_message and self.async_send_message methods

    def test_receive_packet__physical(self):
        """Check for a simple CAN packet (physically addressed) receiving."""
        # TODO: fill like the one above
        # TODO: make sure AddressingInformation objects are correct. You can base on existing ones in this file.
        # TODO: for all test methods, replace custom code with self.send_packet, self.async_send_packet,
        #  self.send_message and self.async_send_message methods

    def test_receive_packet__functional(self):
        """Check for a simple CAN packet (functionally addressed) receiving."""
        # TODO: fill like the one above
        # TODO: make sure AddressingInformation objects are correct. You can base on existing ones in this file.
        # TODO: for all test methods, replace custom code with self.send_packet, self.async_send_packet,
        #  self.send_message and self.async_send_message methods

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_information, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
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
         AddressingType.PHYSICAL,
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

        :param addressing_information: Example Addressing Information of a CAN Node.
        :param addressing_type: Addressing type to use for transmitting a CAN packet.
        :param packet_type: Type of CAN packet to receive.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        :param timeout: Timeout to pass to receive method [ms].
        :param send_after: Time when to send CAN frame after call of receive method [ms].
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
        self.send_packet(can_interface=self.can_interface_2, packet=packet, delay=send_after)
        time_before_receive = time()
        with pytest.raises(TimeoutError):
            can_transport_interface.receive_packet(timeout=timeout)
        time_after_receive = time()
        assert timeout < (time_after_receive - time_before_receive) * 1000. < timeout + self.TASK_TIMING_TOLERANCE
        # timing parameters
        assert can_transport_interface.n_as_measured is None
        assert can_transport_interface.n_ar_measured is None
        # wait till packet arrives
        sleep((send_after - timeout + self.TASK_TIMING_TOLERANCE) / 1000.)

    async def test_async_receive_packet__physical(self):
        """Check for a simple asynchronous CAN packet (physically addressed) receiving."""

    async def test_async_receive_packet__functional(self):
        """Check for a simple asynchronous CAN packet (functionally addressed) receiving."""

    async def test_async_receive_packet__timeout(self):
        """Check for a timeout during packet asynchronous receiving."""



class AbstractMessageTests(AbstractPythonCanTests):
    """Abstract class for tests related to sending a UDS message."""

    def test_send_message__sf(self):
        """Check for a simple synchronous UDS message sending."""

    def test_send_message__multi_packets(self):
        """Check for a synchronous multi packet (FF + CF) UDS message sending."""

    async def test_async_send_message__sf(self):
        """Check for a simple asynchronous UDS message sending."""

    async def test_async_send_message__multi_packets(self):
        """Check for an asynchronous multi packet (FF + CF) UDS message sending."""

    def test_receive_message__sf(self):
        """Check for receiving of a UDS message (carried by Single Frame packet)."""

    def test_receive_message__multi_packets(self):
        """Check for receiving of a UDS message (carried by First Frame and Consecutive Frame packets)."""

    async def test_async_receive_message__sf(self):
        """Check for asynchronous receiving of a UDS message (carried by Single Frame packet)."""

    async def test_async_receive_message__multi_packets(self):
        """Check for asynchronous receiving of a UDS message (carried by First Frame and Consecutive Frame packets)."""

    def test_send_message__multi_packets__timeout(self):
        """Check for a timeout (N_Bs timeout exceeded) during synchronous multi packet (FF + CF) UDS message sending."""

    async def test_async_send_message__multi_packets__timeout(self):
        """Check for a timeout (N_Bs timeout exceeded) during asynchronous multi packet (FF + CF) UDS message sending."""

    def test_receive_message__sf__timeout(self):
        """Check for a timeout during receiving of a UDS message."""

    async def test_async_receive_message__sf__timeout(self):
        """Check for a timeout during asynchronous receiving of a UDS message."""


    def test_receive_message__multi_packets__timeout(self):
        """Check for a timeout during receiving of a UDS message (carried by First Frame and Consecutive Frame packets)."""

    async def test_async_receive_message__multi_packets__timeout(self):
        """Check for a timeout during asynchronous receiving of a UDS message (carried by First Frame and Consecutive Frame packets)."""


class AbstractUseCaseTests(AbstractCanPacketTests):

    def test_send_packet_on_one_receive_on_other_bus(self):
        """Check for sending and receiving CAN packet using two Transport Interfaces."""

    async def test_async_send_packet_on_one_receive_on_other_bus(self):
        """Check for asynchronous sending and receiving CAN packet using two Transport Interfaces."""

    def test_send_message_on_one_receive_on_other_bus(self):
        """Check for sending and receiving UDS message using two Transport Interfaces."""

    async def test_async_send_message_on_one_receive_on_other_bus(self):
        """Check for asynchronous sending and receiving UDS message using two Transport Interfaces."""


class AbstractErrorGuessingTests(AbstractPythonCanTests):

    def test_timeout_then_send_packet(self):
        """Check for sending a CAN packet after a timeout exception during receiving."""

    async def test_async_timeout_then_send_packet(self):
        """Check for asynchronous sending a CAN packet after a timeout exception during asynchronous receiving."""

    def test_timeout_then_receive_packet(self):
        """Check for receiving a CAN packet after a timeout exception during receiving."""

    async def test_async_timeout_then_receive_packet(self):
        """Check for asynchronous receiving a CAN packet after a timeout exception during receiving."""

    def test_observe_tx_packet(self):
        """Check for transmitting a CAN packet after a sending identical CAN frame."""

    async def test_async_observe_tx_packet(self):
        """ Check for asynchronous transmitting a CAN packet after a sending identical CAN frame."""

    def test_overflow_during_message_sending(self):
        """Check for handling Overflow status during synchronous multi packet (FF + CF) UDS message sending."""

    async def test_overflow_during_async_message_sending(self):
        """Check for handling Overflow status during asynchronous multi packet (FF + CF) UDS message sending."""

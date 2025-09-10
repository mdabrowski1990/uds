import asyncio
from abc import ABC, abstractmethod
from datetime import datetime
from threading import Timer
from time import sleep, time
from typing import Optional

import pytest
from tests.system_tests import BaseSystemTests

from can import Bus, Message
from uds.addressing import AddressingType, TransmissionDirection
from uds.can import (
    CanAddressingFormat,
    CanFlowStatus,
    CanPacket,
    CanPacketRecord,
    CanPacketType,
    DefaultFlowControlParametersGenerator,
    PyCanTransportInterface,
)
from uds.message import UdsMessage, UdsMessageRecord
from uds.utilities import TimeMillisecondsAlias


class AbstractPythonCanTests(BaseSystemTests, ABC):
    """
    Definition of system tests (with hardware) for Diagnostic over CAN (DoCAN) with python-can.

    Required hardware setup:
        - 2x CAN bus hardware interfaces that can be controlled using python-can package
        - both CAN interfaces are connected (so they can communicate with each other) using CAN bus cabling (twisted
          cables pair with a termination resistor)
    """

    TIMESTAMP_TOLERANCE: TimeMillisecondsAlias = 2  # python-can has low accuracy

    can_interface_1: Bus
    can_interface_2: Bus
    sent_packet: Optional[CanPacketRecord]

    @abstractmethod
    def _define_interfaces(self):
        """Define python-can interfaces"""

    def setup_method(self):
        """
        Prepare for testing:
        - configue python-can interfaces used for CAN communication
        - define variables used during tests
        """
        self._define_interfaces()
        super().setup_method()

    def teardown_method(self):
        """
        Clean after tests:
        - stop transmission using CAN interfaces
        - disconnect python-can interfaces
        - kill all started tasks
        """
        self.can_interface_1.flush_tx_buffer()
        self.can_interface_2.flush_tx_buffer()
        super().teardown_method()
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


class AbstractCanPacketTests(AbstractPythonCanTests, ABC):
    """Common implementation of system tests related to sending and receiving CAN packets."""

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_format, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_ADDRESSING,
         {"payload": [0x54]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x8}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.EXTENDED_ADDRESSING,
         {"payload": b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87\x78\x69\x5A\x4B\x3C\x2D\x1E\x0F\xFF",
          "sequence_number": 0xF, "filler_byte": 0x5A}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         {"flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x00, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         {"dlc": 0xF, "filler_byte": 0x00, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A]}),
    ])
    def test_send_packet(self, packet_type, addressing_type, addressing_format, packet_type_specific_kwargs,
                         parametrized_can_addressing_information):
        """
        Check for simple sending of a CAN packet.

        Procedure:
        1. Send CAN packet via Transport Interface.
            Expected: CAN packet record returned.
        2. Validate transmitted CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the transmitted CAN packet.

        :param packet_type: Type of CAN packet to send.
        :param addressing_type: Addressing type to use for transmitting a CAN packet.
        :param addressing_format: CAN Addressing Format to use.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=parametrized_can_addressing_information)
        if addressing_type == AddressingType.PHYSICAL:
            addressing_params = parametrized_can_addressing_information.tx_physical_params
        else:
            addressing_params = parametrized_can_addressing_information.tx_functional_params
        packet = CanPacket(packet_type=packet_type,
                           **addressing_params,
                           **packet_type_specific_kwargs)
        time_before_send = time()
        packet_record = can_transport_interface.send_packet(packet)
        time_after_send = time()
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.TRANSMITTED
        assert packet_record.raw_frame_data == packet.raw_frame_data
        assert (packet_record.addressing_format == packet.addressing_format == addressing_format
                == parametrized_can_addressing_information.ADDRESSING_FORMAT)
        assert packet_record.packet_type == packet.packet_type == packet_type
        assert packet_record.can_id == packet.can_id == addressing_params["can_id"]
        assert packet_record.addressing_type == packet.addressing_type == addressing_type
        assert packet_record.target_address == packet.target_address == addressing_params["target_address"]
        assert packet_record.source_address == packet.source_address == addressing_params["source_address"]
        assert packet_record.address_extension == packet.address_extension == addressing_params["address_extension"]
        # timing parameters
        transmission_time_ms = (time_after_send - time_before_send) * 1000.
        if packet_type == CanPacketType.FLOW_CONTROL:
            assert can_transport_interface.n_as_measured is None
            if self.MAKE_TIMING_CHECKS:
                assert 0 <= can_transport_interface.n_ar_measured <= transmission_time_ms + self.TIMESTAMP_TOLERANCE / 1000.
        else:
            assert can_transport_interface.n_ar_measured is None
            if self.MAKE_TIMING_CHECKS:
                assert 0 <= can_transport_interface.n_as_measured <= transmission_time_ms + self.TIMESTAMP_TOLERANCE / 1000.
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            assert (datetime.fromtimestamp(time_before_send - self.TIMESTAMP_TOLERANCE / 1000.)
                    <= packet_record.transmission_time
                    <= datetime.fromtimestamp(time_after_send + self.TIMESTAMP_TOLERANCE / 1000.))

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_format, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_ADDRESSING,
         {"payload": [0x54]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x8}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.EXTENDED_ADDRESSING,
         {"payload": b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87\x78\x69\x5A\x4B\x3C\x2D\x1E\x0F\xFF",
          "sequence_number": 0xF, "filler_byte": 0x5A}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         {"flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x00, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         {"dlc": 0xF, "filler_byte": 0x00, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A]}),
    ])
    @pytest.mark.asyncio
    async def test_async_send_packet(self, packet_type, addressing_type, addressing_format, packet_type_specific_kwargs,
                                     parametrized_can_addressing_information):
        """
        Check for simple asynchronous sending of a CAN packet.

        Procedure:
        1. Send (using async method) a CAN packet via Transport Interface.
            Expected: CAN packet record returned.
        2. Validate transmitted CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the transmitted CAN packet.

        :param packet_type: Type of CAN packet to send.
        :param addressing_type: Addressing type to use for transmitting a CAN packet.
        :param addressing_format: CAN Addressing Format to use.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=parametrized_can_addressing_information)
        if addressing_type == AddressingType.PHYSICAL:
            addressing_params = parametrized_can_addressing_information.tx_physical_params
        else:
            addressing_params = parametrized_can_addressing_information.tx_functional_params
        packet = CanPacket(packet_type=packet_type,
                           **addressing_params,
                           **packet_type_specific_kwargs)
        time_before_send = time()
        packet_record = await can_transport_interface.async_send_packet(packet)
        time_after_send = time()
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.TRANSMITTED
        assert packet_record.raw_frame_data == packet.raw_frame_data
        assert (packet_record.addressing_format == packet.addressing_format == addressing_format
                == parametrized_can_addressing_information.ADDRESSING_FORMAT)
        assert packet_record.packet_type == packet.packet_type == packet_type
        assert packet_record.can_id == packet.can_id == addressing_params["can_id"]
        assert packet_record.addressing_type == packet.addressing_type == addressing_type
        assert packet_record.target_address == packet.target_address == addressing_params["target_address"]
        assert packet_record.source_address == packet.source_address == addressing_params["source_address"]
        assert packet_record.address_extension == packet.address_extension == addressing_params["address_extension"]
        # timing parameters
        transmission_time_ms = (time_after_send - time_before_send) * 1000.
        if packet_type == CanPacketType.FLOW_CONTROL:
            assert can_transport_interface.n_as_measured is None
            if self.MAKE_TIMING_CHECKS:
                assert (0
                        <= can_transport_interface.n_ar_measured
                        <= transmission_time_ms + self.TIMESTAMP_TOLERANCE / 1000.)
        else:
            assert can_transport_interface.n_ar_measured is None
            if self.MAKE_TIMING_CHECKS:
                assert (0
                        <= can_transport_interface.n_as_measured
                        <= transmission_time_ms + self.TIMESTAMP_TOLERANCE / 1000.)
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            assert (datetime.fromtimestamp(time_before_send - self.TIMESTAMP_TOLERANCE / 1000.)
                    <= packet_record.transmission_time
                    <= datetime.fromtimestamp(time_after_send + self.TIMESTAMP_TOLERANCE / 1000.))

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_format, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_ADDRESSING,
         {"payload": [0x54]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x8}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.EXTENDED_ADDRESSING,
         {"payload": b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87\x78\x69\x5A\x4B\x3C\x2D\x1E\x0F\xFF",
          "sequence_number": 0xF, "filler_byte": 0x5A}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         {"flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x00, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         {"dlc": 0xF, "filler_byte": 0x00, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A]}),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        # TODO: adjust values to be closer to boundary when https://github.com/mdabrowski1990/uds/issues/228 resolved
        (1000, 950),  # ms
        (50, 20),
    ])
    def test_receive_packet(self, packet_type, addressing_type, addressing_format, packet_type_specific_kwargs,
                            timeout, send_after,
                            parametrized_can_addressing_information):
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
        :param addressing_format: CAN Addressing Format to use.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        :param timeout: Timeout to pass to receive method [ms].
        :param send_after: Time when to send CAN frame after call of receive method [ms].
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=parametrized_can_addressing_information)
        if addressing_type == AddressingType.PHYSICAL:
            addressing_params = parametrized_can_addressing_information.rx_physical_params
        else:
            addressing_params = parametrized_can_addressing_information.rx_functional_params
        packet = CanPacket(packet_type=packet_type,
                           **addressing_params,
                           **packet_type_specific_kwargs)
        can_frame = Message(arbitration_id=packet.can_id,
                            data=packet.raw_frame_data,
                            is_fd=packet.dlc > 8)
        self.send_frame(can_interface=self.can_interface_2,
                        frame=can_frame,
                        delay=send_after)
        time_before_receive = time()
        packet_record = can_transport_interface.receive_packet(timeout=timeout)
        time_after_receive = time()
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.RECEIVED
        assert packet_record.raw_frame_data == packet.raw_frame_data == bytes(can_frame.data)
        assert (packet_record.addressing_format == packet.addressing_format == addressing_format
                == parametrized_can_addressing_information.ADDRESSING_FORMAT)
        assert packet_record.packet_type == packet.packet_type == packet_type
        assert packet_record.addressing_type == packet.addressing_type == addressing_type
        assert packet_record.can_id == packet.can_id == can_frame.arbitration_id == addressing_params["can_id"]
        assert packet_record.target_address == packet.target_address == addressing_params["target_address"]
        assert packet_record.source_address == packet.source_address == addressing_params["source_address"]
        assert packet_record.address_extension == packet.address_extension == addressing_params["address_extension"]
        # performance
        receiving_time_ms = (time_after_receive - time_before_receive) * 1000.
        if self.MAKE_TIMING_CHECKS:
            assert send_after <= receiving_time_ms < timeout
            assert (datetime.fromtimestamp(time_before_receive - self.TIMESTAMP_TOLERANCE / 1000.)
                    <= packet_record.transmission_time
                    <= datetime.fromtimestamp(time_after_receive + self.TIMESTAMP_TOLERANCE / 1000.))

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_format, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_ADDRESSING,
         {"payload": [0x54]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x8}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.EXTENDED_ADDRESSING,
         {"payload": b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87\x78\x69\x5A\x4B\x3C\x2D\x1E\x0F\xFF",
          "sequence_number": 0xF, "filler_byte": 0x5A}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         {"flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x00, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         {"dlc": 0xF, "filler_byte": 0x00, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A]}),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        # TODO: adjust values to be closer to boundary when https://github.com/mdabrowski1990/uds/issues/228 resolved
        (1000, 950),  # ms
        (50, 20),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_packet(self, packet_type, addressing_type, addressing_format,
                                        packet_type_specific_kwargs,
                                        timeout, send_after,
                                        parametrized_can_addressing_information):
        """
        Check for a simple asynchronous CAN packet (physically addressed) receiving.

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frame that carries received CAN packet.
        2. Call async method to receive packet via Transport Interface with timeout set just after CAN packet
            reaches CAN bus.
            Expected: CAN packet is received.
        3. Validate received CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the received CAN packet.

        :param packet_type, addressing_type, : Example Addressing Information of a CAN Node.
        :param packet_type: Type of CAN packet to send.
        :param addressing_type: Addressing type to use for transmitting a CAN packet.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        :param timeout: Timeout to pass to receive method [ms].
        :param send_after: Time when to send CAN frame after call of receive method [ms].
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=parametrized_can_addressing_information)
        if addressing_type == AddressingType.PHYSICAL:
            addressing_params = parametrized_can_addressing_information.rx_physical_params
        else:
            addressing_params = parametrized_can_addressing_information.rx_functional_params
        packet = CanPacket(packet_type=packet_type,
                           **addressing_params,
                           **packet_type_specific_kwargs)
        can_frame = Message(arbitration_id=packet.can_id,
                            data=packet.raw_frame_data,
                            is_fd=packet.dlc > 8)
        send_frame_task = asyncio.create_task(self.async_send_frame(can_interface=self.can_interface_2,
                                                                    frame=can_frame,
                                                                    delay=send_after))
        time_before_receive = time()
        packet_record = await can_transport_interface.async_receive_packet(timeout=timeout)
        time_after_receive = time()
        await send_frame_task
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.RECEIVED
        assert packet_record.raw_frame_data == packet.raw_frame_data == bytes(can_frame.data)
        assert (packet_record.addressing_format == packet.addressing_format == addressing_format
                == parametrized_can_addressing_information.ADDRESSING_FORMAT)
        assert packet_record.packet_type == packet.packet_type == packet_type
        assert packet_record.addressing_type == packet.addressing_type == addressing_type
        assert packet_record.can_id == packet.can_id == can_frame.arbitration_id == addressing_params["can_id"]
        assert packet_record.target_address == packet.target_address == addressing_params["target_address"]
        assert packet_record.source_address == packet.source_address == addressing_params["source_address"]
        assert packet_record.address_extension == packet.address_extension == addressing_params["address_extension"]
        # performance
        receiving_time_ms = (time_after_receive - time_before_receive) * 1000.
        if self.MAKE_TIMING_CHECKS:
            assert send_after <= receiving_time_ms < timeout
            assert (datetime.fromtimestamp(time_before_receive - self.TIMESTAMP_TOLERANCE / 1000.)
                    <= packet_record.transmission_time
                    <= datetime.fromtimestamp(time_after_receive + self.TIMESTAMP_TOLERANCE / 1000.))

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_format, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_ADDRESSING,
         {"payload": [0x54]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x8}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.EXTENDED_ADDRESSING,
         {"payload": b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87\x78\x69\x5A\x4B\x3C\x2D\x1E\x0F\xFF",
          "sequence_number": 0xF, "filler_byte": 0x5A}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         {"flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x00, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         {"dlc": 0xF, "filler_byte": 0x00, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A]}),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        (1000, 1005),  # ms
        (50, 55),
    ])
    def test_receive_packet__timeout(self, packet_type, addressing_type, addressing_format, packet_type_specific_kwargs,
                                     timeout, send_after,
                                     parametrized_can_addressing_information):
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
        :param addressing_format: CAN Addressing Format to use.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        :param timeout: Timeout to pass to receive method [ms].
        :param send_after: Time when to send CAN frame after call of receive method [ms].
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=parametrized_can_addressing_information)
        if addressing_type == AddressingType.PHYSICAL:
            addressing_params = parametrized_can_addressing_information.rx_physical_params
        else:
            addressing_params = parametrized_can_addressing_information.rx_functional_params
        packet = CanPacket(packet_type=packet_type,
                           **addressing_params,
                           **packet_type_specific_kwargs)
        can_frame = Message(arbitration_id=packet.can_id,
                            data=packet.raw_frame_data,
                            is_fd=packet.dlc > 8)
        self.send_frame(can_interface=self.can_interface_2,
                        frame=can_frame,
                        delay=send_after)
        time_before_receive = time()
        with pytest.raises(TimeoutError):
            can_transport_interface.receive_packet(timeout=timeout)
        time_after_receive = time()
        receiving_time_ms = (time_after_receive - time_before_receive) * 1000.
        assert timeout <= receiving_time_ms < timeout + self.TASK_TIMING_TOLERANCE
        # receive packet later
        packet_record = can_transport_interface.receive_packet(timeout=(send_after - timeout) * 10)
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.RECEIVED
        assert packet_record.raw_frame_data == bytes(can_frame.data)
        assert packet_record.can_id == can_frame.arbitration_id

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_format, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_ADDRESSING,
         {"payload": [0x54]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x8}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.EXTENDED_ADDRESSING,
         {"payload": b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87\x78\x69\x5A\x4B\x3C\x2D\x1E\x0F\xFF",
          "sequence_number": 0xF, "filler_byte": 0x5A}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         {"flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x00, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         {"dlc": 0xF, "filler_byte": 0x00, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A]}),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        (1000, 1005),  # ms
        (50, 55),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_packet__timeout(self, packet_type, addressing_type, addressing_format,
                                                 packet_type_specific_kwargs,
                                                 timeout, send_after,
                                                 parametrized_can_addressing_information):
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
        :param addressing_format: CAN Addressing Format to use.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        :param timeout: Timeout to pass to receive method [ms].
        :param send_after: Time when to send CAN frame after call of receive method [ms].
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=parametrized_can_addressing_information)
        if addressing_type == AddressingType.PHYSICAL:
            addressing_params = parametrized_can_addressing_information.rx_physical_params
        else:
            addressing_params = parametrized_can_addressing_information.rx_functional_params
        packet = CanPacket(packet_type=packet_type,
                           **addressing_params,
                           **packet_type_specific_kwargs)
        can_frame = Message(arbitration_id=packet.can_id,
                            data=packet.raw_frame_data,
                            is_fd=packet.dlc > 8)
        send_frame_task = asyncio.create_task(self.async_send_frame(can_interface=self.can_interface_2,
                                                                    frame=can_frame,
                                                                    delay=send_after))
        time_before_receive = time()
        with pytest.raises(TimeoutError):
            await can_transport_interface.async_receive_packet(timeout=timeout)
        time_after_receive = time()
        receiving_time_ms = (time_after_receive - time_before_receive) * 1000.
        assert timeout <= receiving_time_ms < timeout + self.TASK_TIMING_TOLERANCE
        # receive packet later
        packet_record = await can_transport_interface.async_receive_packet(timeout=(send_after - timeout) * 10)
        await send_frame_task
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.RECEIVED
        assert packet_record.raw_frame_data == bytes(can_frame.data)
        assert packet_record.can_id == can_frame.arbitration_id


class AbstractMessageTests(AbstractPythonCanTests, ABC):
    """Common implementation of system tests related to sending and receiving UDS (DoCAN) messages."""

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, 0x12, 0x34, 0x56, 0x78], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x54], addressing_type=AddressingType.FUNCTIONAL),
    ])
    def test_send_message__sf(self, example_can_addressing_information, message):
        """
        Check for a simple synchronous UDS message sending.

        Procedure:
        1. Send a UDS message using Transport Interface (via CAN Interface).
            Expected: UDS message record returned.
        2. Validate transmitted UDS message record attributes.
            Expected: Attributes of UDS message record are in line with the transmitted UDS message.

        :param example_can_addressing_information: Example Addressing Information of a CAN Node.
        :param message: UDS message to send.
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=example_can_addressing_information)
        time_before_send = time()
        message_record = can_transport_interface.send_message(message)
        time_after_send = time()
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
            assert (datetime.fromtimestamp(time_before_send - self.TIMESTAMP_TOLERANCE / 1000.)
                    <= message_record.transmission_start
                    == message_record.transmission_end
                    <= datetime.fromtimestamp(time_after_send + self.TIMESTAMP_TOLERANCE / 1000.))

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, 0x12, 0x34, 0x56, 0x78], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x54], addressing_type=AddressingType.FUNCTIONAL),
    ])
    @pytest.mark.asyncio
    async def test_async_send_message__sf(self, example_can_addressing_information, message):
        """
        Check for a simple asynchronous UDS message sending.

        Procedure:
        1. Send (using async method) a UDS message using Transport Interface (via CAN Interface).
            Expected: UDS message record returned.
        2. Validate transmitted UDS message record attributes.
            Expected: Attributes of UDS message record are in line with the transmitted UDS message.

        :param example_can_addressing_information: Example Addressing Information of a CAN Node.
        :param message: UDS message to send.
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=example_can_addressing_information)
        time_before_send = time()
        message_record = await can_transport_interface.async_send_message(message)
        time_after_send = time()
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
            assert (datetime.fromtimestamp(time_before_send - self.TIMESTAMP_TOLERANCE / 1000.)
                    <= message_record.transmission_start
                    <= datetime.fromtimestamp(time_after_send + self.TIMESTAMP_TOLERANCE / 1000.))

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, 0x12, 0x34, 0x56, 0x78], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x54], addressing_type=AddressingType.FUNCTIONAL),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        # TODO: adjust values to be closer to boundary when https://github.com/mdabrowski1990/uds/issues/228 resolved
        (1000, 950),  # ms
        (50, 20),
    ])
    def test_receive_message__sf(self, example_can_addressing_information,
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

        :param example_can_addressing_information: Addressing Information of receiving CAN Node.
        :param message: UDS message to transmit.
        :param timeout: Maximal time (in milliseconds) to wait for the message transmission.
        :param send_after: Time when to send CAN frame after call of receive method [ms].
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=example_can_addressing_information)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            network_manager=self.can_interface_2,
            addressing_information=example_can_addressing_information.get_other_end())
        self.send_message(transport_interface=can_transport_interface_2nd_node,
                          message=message,
                          delay=send_after)
        time_before_receive = time()
        message_record = can_transport_interface.receive_message(start_timeout=timeout,
                                                                 end_timeout=timeout)
        time_after_receive = time()
        assert isinstance(message_record, UdsMessageRecord)
        assert message_record.direction == TransmissionDirection.RECEIVED
        assert message_record.payload == message.payload
        assert message_record.addressing_type == message.addressing_type
        assert message_record.transmission_start == message_record.transmission_end
        assert len(message_record.packets_records) == 1
        assert message_record.packets_records[0].packet_type == CanPacketType.SINGLE_FRAME
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            assert (datetime.fromtimestamp(time_before_receive - self.TIMESTAMP_TOLERANCE / 1000.)
                    <= message_record.transmission_start
                    <= datetime.fromtimestamp(time_after_receive + self.TIMESTAMP_TOLERANCE / 1000.))

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, 0x12, 0x34, 0x56, 0x78], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x54], addressing_type=AddressingType.FUNCTIONAL),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        # TODO: adjust values to be closer to boundary when https://github.com/mdabrowski1990/uds/issues/228 resolved
        (1000, 950),  # ms
        (50, 20),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_message__sf(self, example_can_addressing_information,
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

        :param example_can_addressing_information: Addressing Information of receiving CAN Node.
        :param message: UDS message to transmit.
        :param timeout: Maximal time (in milliseconds) to wait for the message transmission.
        :param send_after: Time when to send CAN frame after call of receive method [ms].
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=example_can_addressing_information)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            network_manager=self.can_interface_2,
            addressing_information=example_can_addressing_information.get_other_end())
        send_message_task = asyncio.create_task(
            self.async_send_message(transport_interface=can_transport_interface_2nd_node,
                                    message=message,
                                    delay=send_after))
        time_before_receive = time()
        message_record = await can_transport_interface.async_receive_message(start_timeout=timeout,
                                                                             end_timeout=timeout)
        time_after_receive = time()
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
            assert (datetime.fromtimestamp(time_before_receive - self.TIMESTAMP_TOLERANCE / 1000.)
                    <= message_record.transmission_start
                    <= datetime.fromtimestamp(time_after_receive + self.TIMESTAMP_TOLERANCE / 1000.))

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, 0x12, 0x34, 0x56, 0x78], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x54], addressing_type=AddressingType.FUNCTIONAL),
    ])
    @pytest.mark.parametrize("start_timeout, send_after", [
        (1000, 1010),  # ms
        (50, 60),
    ])
    def test_receive_message__sf__start_timeout(self, example_can_addressing_information,
                                                message, start_timeout, send_after):
        """
        Check for a timeout during receiving of a UDS message.

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frame that carries received UDS message.
        2. Call method to receive message via Transport Interface with timeout set just before UDS message
            reaches CAN bus.
            Expected: Timeout exception is raised.
        3. Call method to receive message for the second time with timeout set after UDS message reaches CAN bus.
            Expected: Message is received.

        :param example_can_addressing_information: Addressing Information of receiving CAN Node.
        :param message: UDS message to transmit.
        :param start_timeout: Maximal time (in milliseconds) to wait for the start of a message transmission.
        :param send_after: Time when to send CAN frame after call of receive method [ms].
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=example_can_addressing_information)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            network_manager=self.can_interface_2,
            addressing_information=example_can_addressing_information.get_other_end())
        self.send_message(transport_interface=can_transport_interface_2nd_node,
                          message=message,
                          delay=send_after)
        time_before_receive = time()
        with pytest.raises(TimeoutError):
            can_transport_interface.receive_message(start_timeout=start_timeout)
        time_after_receive = time()
        # receive message later
        message_record = can_transport_interface.receive_message(
            start_timeout=(send_after - start_timeout) * 10)
        assert isinstance(message_record, UdsMessageRecord)
        assert message_record.direction == TransmissionDirection.RECEIVED
        assert message_record.payload == message.payload
        assert message_record.addressing_type == message.addressing_type
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            receiving_time_ms = (time_after_receive - time_before_receive) * 1000.
            assert start_timeout <= receiving_time_ms < send_after + self.TASK_TIMING_TOLERANCE

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, 0x12, 0x34, 0x56, 0x78], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x54], addressing_type=AddressingType.FUNCTIONAL),
    ])
    @pytest.mark.parametrize("start_timeout, send_after", [
        (1000, 1010),  # ms
        (50, 60),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_message__sf__start_timeout(self, example_can_addressing_information,
                                                            message, start_timeout, send_after):
        """
        Check for a timeout during asynchronous receiving of a UDS message.

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frame that carries received UDS message.
        2. Call async method to receive message via Transport Interface with timeout set before any CAN packet
            reaches CAN bus.
            Expected: Timeout exception is raised.
        3. Call method to receive message for the second time with timeout set after UDS message reaches CAN bus.
            Expected: Message is received.

        :param example_can_addressing_information: Addressing Information of receiving CAN Node.
        :param message: UDS message to transmit.
        :param start_timeout: Maximal time (in milliseconds) to wait for the start of a message transmission.
        :param send_after: Time when to send CAN frame after call of receive method [ms].
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=example_can_addressing_information)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            network_manager=self.can_interface_2,
            addressing_information=example_can_addressing_information.get_other_end())
        send_message_task = asyncio.create_task(self.async_send_message(
            transport_interface=can_transport_interface_2nd_node,
            message=message,
            delay=send_after))
        time_before_receive = time()
        with pytest.raises(TimeoutError):
            await can_transport_interface.async_receive_message(start_timeout=start_timeout)
        time_after_receive = time()
        # receive message later
        message_record = await can_transport_interface.async_receive_message(
            start_timeout=(send_after - start_timeout) * 10)
        await send_message_task
        assert isinstance(message_record, UdsMessageRecord)
        assert message_record.direction == TransmissionDirection.RECEIVED
        assert message_record.payload == message.payload
        assert message_record.addressing_type == message.addressing_type
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            receiving_time_ms = (time_after_receive - time_before_receive) * 1000.
            assert start_timeout <= receiving_time_ms < send_after + self.TASK_TIMING_TOLERANCE

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, *range(62)], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x62, 0x12, 0x34, *range(100, 250)], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("n_bs_timeout, send_after", [
        # TODO: adjust values to be closer to boundary when https://github.com/mdabrowski1990/uds/issues/228 resolved
        (1000, 950),  # ms
        (50, 20),
    ])
    def test_send_message__multi_packets(self, example_can_addressing_information,
                                         message, n_bs_timeout, send_after):
        """
        Check for a synchronous multi packet (FF + CF) UDS message sending.

        Procedure:
        1. Schedule Flow Control CAN Packet with information to continue sending all consecutive frame packets at once.
        2. Send a UDS message using Transport Interface (via CAN Interface).
            Expected: UDS message record returned.
        3. Validate transmitted UDS message record attributes.
            Expected: Attributes of UDS message record are in line with the transmitted UDS message.

        :param example_can_addressing_information: Example Addressing Information of a CAN Node.
        :param message: UDS message to send.
        :param n_bs_timeout: Value of N_Bs timeout [ms] to use.
        :param send_after: Delay to use for sending CAN flow control.
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=example_can_addressing_information,
            n_bs_timeout=n_bs_timeout)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            network_manager=self.can_interface_2,
            addressing_information=example_can_addressing_information.get_other_end())
        flow_control_packet = can_transport_interface_2nd_node.segmenter.get_flow_control_packet(
            flow_status=CanFlowStatus.ContinueToSend,
            block_size=0,
            st_min=0)
        self.send_packet(transport_interface=can_transport_interface_2nd_node,
                         packet=flow_control_packet,
                         delay=send_after)
        time_before_send = time()
        message_record = can_transport_interface.send_message(message)
        time_after_send = time()
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
            assert (datetime.fromtimestamp(time_before_send - self.TIMESTAMP_TOLERANCE / 1000.)
                    <= message_record.transmission_start)
            assert (message_record.transmission_end
                    <= datetime.fromtimestamp(time_after_send + self.TIMESTAMP_TOLERANCE / 1000.))
            assert (send_after - self.TASK_TIMING_TOLERANCE
                    <= can_transport_interface.n_bs_measured[0]
                    <= send_after + self.TASK_TIMING_TOLERANCE)

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, *range(62)], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x62, 0x12, 0x34, *range(100, 250)], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("n_bs_timeout, send_after", [
        # TODO: adjust values to be closer to boundary when https://github.com/mdabrowski1990/uds/issues/228 resolved
        (1000, 950),  # ms
        (50, 20),
    ])
    @pytest.mark.asyncio
    async def test_async_send_message__multi_packets(self, example_can_addressing_information,
                                                     message, n_bs_timeout, send_after):
        """
        Check for an asynchronous multi packet (FF + CF) UDS message sending.

        Procedure:
        1. Schedule Flow Control CAN Packet with information to continue sending all consecutive frame packets at once.
        2. Send (using async method) a UDS message using Transport Interface (via CAN Interface).
            Expected: UDS message record returned.
        3. Validate transmitted UDS message record attributes.
            Expected: Attributes of UDS message record are in line with the transmitted UDS message.

        :param example_can_addressing_information: Example Addressing Information of a CAN Node.
        :param message: UDS message to send.
        :param n_bs_timeout: Value of N_Bs timeout [ms] to use.
        :param send_after: Delay to use for sending CAN flow control.
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=example_can_addressing_information,
            n_bs_timeout=n_bs_timeout)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            network_manager=self.can_interface_2,
            addressing_information=example_can_addressing_information.get_other_end())
        flow_control_packet = can_transport_interface_2nd_node.segmenter.get_flow_control_packet(
            flow_status=CanFlowStatus.ContinueToSend,
            block_size=0,
            st_min=0)
        send_packet_task = asyncio.create_task(self.async_send_packet(
            transport_interface=can_transport_interface_2nd_node,
            packet=flow_control_packet,
            delay=send_after))
        time_before_send = time()
        message_record = await can_transport_interface.async_send_message(message)
        time_after_send = time()
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
            assert (datetime.fromtimestamp(time_before_send - self.TIMESTAMP_TOLERANCE / 1000.)
                    <= message_record.transmission_start)
            assert (message_record.transmission_end
                    <= datetime.fromtimestamp(time_after_send + self.TIMESTAMP_TOLERANCE / 1000.))
            assert (send_after - self.TASK_TIMING_TOLERANCE
                    <= can_transport_interface.n_bs_measured[0]
                    <= send_after + self.TASK_TIMING_TOLERANCE)

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, *range(62)], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x62, 0x12, 0x34, *range(100, 250)], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("n_bs_timeout, send_after", [
        (1000, 1010),  # ms
        (50, 60),
    ])
    def test_send_message__multi_packets__n_bs_timeout(self, example_can_addressing_information,
                                                       message, n_bs_timeout, send_after):
        """
        Check for a timeout (N_Bs timeout exceeded) during synchronous multi packet (FF + CF) UDS message sending.

        Procedure:
        1. Schedule Flow Control CAN Packet just after N_Bs timeout.
        2. Send a UDS message using Transport Interface (via CAN Interface).
            Expected: Timeout exception is raised.

        :param example_can_addressing_information: Example Addressing Information of a CAN Node.
        :param message: UDS message to send.
        :param n_bs_timeout: Value of N_Bs timeout [ms] to use.
        :param send_after: Delay to use for sending CAN flow control.
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=example_can_addressing_information,
            n_bs_timeout=n_bs_timeout)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            network_manager=self.can_interface_2,
            addressing_information=example_can_addressing_information.get_other_end())
        flow_control_packet = can_transport_interface_2nd_node.segmenter.get_flow_control_packet(
            flow_status=CanFlowStatus.ContinueToSend,
            block_size=0,
            st_min=0)
        self.send_packet(transport_interface=can_transport_interface_2nd_node,
                         packet=flow_control_packet,
                         delay=send_after)
        time_before_receive = time()
        with pytest.raises(TimeoutError):
            can_transport_interface.send_message(message)
        time_after_receive = time()
        # timing parameters
        receiving_time_ms = (time_after_receive - time_before_receive) * 1000.
        assert (can_transport_interface.n_bs_timeout - self.TIMESTAMP_TOLERANCE
                < receiving_time_ms
                < can_transport_interface.n_bs_timeout + self.TASK_TIMING_TOLERANCE)

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, *range(62)], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x62, 0x12, 0x34, *range(100, 250)], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("n_bs_timeout, send_after", [
        (1000, 1010),  # ms
        (50, 60),
    ])
    @pytest.mark.asyncio
    async def test_async_send_message__multi_packets__n_bs_timeout(self, example_can_addressing_information,
                                                                   message, n_bs_timeout, send_after):
        """
        Check for a timeout (N_Bs timeout exceeded) during asynchronous multi packet (FF + CF) UDS message sending.

        Procedure:
        1. Schedule Flow Control CAN Packet just after N_Bs timeout.
        2. Send (using async method) a UDS message using Transport Interface (via CAN Interface).
            Expected: Timeout exception is raised.

        :param example_can_addressing_information: Example Addressing Information of a CAN Node.
        :param message: UDS message to send.
        :param n_bs_timeout: Value of N_Bs timeout [ms] to use.
        :param send_after: Delay to use for sending CAN flow control.
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=example_can_addressing_information,
            n_bs_timeout=n_bs_timeout)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            network_manager=self.can_interface_2,
            addressing_information=example_can_addressing_information.get_other_end())
        flow_control_packet = can_transport_interface_2nd_node.segmenter.get_flow_control_packet(
            flow_status=CanFlowStatus.ContinueToSend,
            block_size=0,
            st_min=0)
        send_packet_task = asyncio.create_task(self.async_send_packet(
            transport_interface=can_transport_interface_2nd_node,
            packet=flow_control_packet,
            delay=send_after))
        time_before_receive = time()
        with pytest.raises(TimeoutError):
            await can_transport_interface.async_send_message(message)
        time_after_receive = time()
        await send_packet_task
        # timing parameters
        receiving_time_ms = (time_after_receive - time_before_receive) * 1000.
        assert (can_transport_interface.n_bs_timeout - self.TIMESTAMP_TOLERANCE
                < receiving_time_ms
                < can_transport_interface.n_bs_timeout + self.TASK_TIMING_TOLERANCE)

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, *range(62)], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x62, 0x12, 0x34, *range(100, 250)], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("start_timeout, end_timeout, send_after, delay", [
        # TODO: adjust values to be closer to boundary when https://github.com/mdabrowski1990/uds/issues/228 resolved
        (1000, 2000, 950, 20),  # ms
        (50, 1500, 20, 50),
    ])
    def test_receive_message__multi_packets(self, example_can_addressing_information,
                                            message, start_timeout, end_timeout, send_after, delay):
        """
        Check for receiving of a UDS message (carried by First Frame and Consecutive Frame packets).

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frames that carry received
            UDS message (First Frame and then Consecutive Frames).
        2. Call method to receive message via Transport Interface.
            Expected: UDS message is received.
        3. Validate received UDS message record attributes.
            Expected: Attributes of UDS message record are in line with the received UDS message.

        :param example_can_addressing_information: Addressing Information of receiving CAN Node.
        :param message: UDS message to transmit.
        :param start_timeout: Maximal time (in milliseconds) to wait for the start of a message transmission.
        :param send_after: Time when to send First Frame after call of receive method [ms].
        :param end_timeout: Maximal time (in milliseconds) to wait for a message transmission to finish.
        :param delay: Time distance to use for sending Consecutive Frames [ms].
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=example_can_addressing_information,
            n_br=0)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            network_manager=self.can_interface_2,
            addressing_information=example_can_addressing_information.get_other_end())
        packets = can_transport_interface_2nd_node.segmenter.segmentation(message)
        for i, packet in enumerate(packets):
            self.send_packet(transport_interface=can_transport_interface_2nd_node,
                             packet=packet,
                             delay=send_after + i * delay)
        time_before_receive = time()
        message_record = can_transport_interface.receive_message(start_timeout=start_timeout,
                                                                 end_timeout=end_timeout)
        time_after_receive = time()
        assert isinstance(message_record, UdsMessageRecord)
        assert len(message_record.packets_records) == len(packets) + 1, \
            "All packets (including Flow Control) are stored"
        assert message_record.direction == TransmissionDirection.RECEIVED
        assert message_record.payload == message.payload
        assert message_record.addressing_type == message.addressing_type
        assert message_record.transmission_start < message_record.transmission_end
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            assert (datetime.fromtimestamp(time_before_receive - self.TIMESTAMP_TOLERANCE / 1000.)
                    <= message_record.transmission_start)
            assert (message_record.transmission_end
                    <= datetime.fromtimestamp(time_after_receive + self.TIMESTAMP_TOLERANCE / 1000.))

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, *range(62)], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x62, 0x12, 0x34, *range(100, 250)], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("start_timeout, end_timeout, send_after, delay", [
        # TODO: adjust values to be closer to boundary when https://github.com/mdabrowski1990/uds/issues/228 resolved
        (1000, 2000, 950, 20),  # ms
        (50, 2000, 20, 50),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_message__multi_packets(self, example_can_addressing_information,
                                                        message, start_timeout, end_timeout, send_after, delay):
        """
        Check for asynchronous receiving of a UDS message (carried by First Frame and Consecutive Frame packets).

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frames that carry received
            UDS message (First Frame and then Consecutive Frames).
        2. Call async method to receive message via Transport Interface.
            Expected: UDS message is received.
        3. Validate received UDS message record attributes.
            Expected: Attributes of UDS message record are in line with the received UDS message.

        :param example_can_addressing_information: Addressing Information of receiving CAN Node.
        :param message: UDS message to transmit.
        :param start_timeout: Maximal time (in milliseconds) to wait for the start of a message transmission.
        :param send_after: Time when to send First Frame after call of receive method [ms].
        :param end_timeout: Maximal time (in milliseconds) to wait for a message transmission to finish.
        :param delay: Time distance to use for sending Consecutive Frames [ms].
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=example_can_addressing_information)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            network_manager=self.can_interface_2,
            addressing_information=example_can_addressing_information.get_other_end())
        packets = can_transport_interface_2nd_node.segmenter.segmentation(message)

        async def _send_message():
            for packet in packets:
                await self.async_send_packet(transport_interface=can_transport_interface_2nd_node,
                                             packet=packet,
                                             delay=send_after if packet == packets[0] else delay)

        send_message_task = asyncio.create_task(_send_message())
        time_before_receive = time()
        message_record = await can_transport_interface.async_receive_message(start_timeout=start_timeout,
                                                                             end_timeout=end_timeout)
        time_after_receive = time()
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
            assert (datetime.fromtimestamp(time_before_receive - self.TIMESTAMP_TOLERANCE / 1000.)
                    <= message_record.transmission_start)
            assert (message_record.transmission_end
                    <= datetime.fromtimestamp(time_after_receive + self.TIMESTAMP_TOLERANCE / 1000.))

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, *range(62)], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x62, 0x12, 0x34, *range(100, 250)], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("start_timeout, send_after, delay", [
        (1000, 50, 20),  # ms
        (50, 0, 50),
    ])
    def test_receive_message__multi_packets__n_cr_timeout(self, example_can_addressing_information,
                                                          message, start_timeout, send_after, delay):
        """
        Check for a timeout during receiving of a UDS message (carried by First Frame and Consecutive Frame packets).

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frames that carries part of received
            UDS message (First Frame and then Consecutive Frames with one Consecutive Frame missing).
        2. Call method to receive message via Transport Interface.
            Expected: Timeout exception is raised.

        :param example_can_addressing_information: Addressing Information of receiving CAN Node.
        :param message: UDS message to transmit.
        :param start_timeout: Maximal time (in milliseconds) to wait for the start of a message transmission.
        :param send_after: Time when to send First Frame after call of receive method [ms].
        :param delay: Time distance to use for sending Consecutive Frames [ms].
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=example_can_addressing_information,
            n_br=0)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            network_manager=self.can_interface_2,
            addressing_information=example_can_addressing_information.get_other_end())
        packets = can_transport_interface_2nd_node.segmenter.segmentation(message)
        self.send_packet(transport_interface=can_transport_interface_2nd_node,
                         packet=packets[0],
                         delay=send_after)
        for i, cf_packet in enumerate(packets[1:-1], start=1):
            self.send_packet(transport_interface=can_transport_interface_2nd_node,
                             packet=cf_packet,
                             delay=send_after + i * delay)
        with pytest.raises(TimeoutError):
            can_transport_interface.receive_message(start_timeout=start_timeout)

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, *range(62)], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x62, 0x12, 0x34, *range(100, 250)], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("start_timeout, send_after, delay", [
        (1000, 50, 20),  # ms
        (50, 0, 50),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_message__multi_packets__n_cr_timeout(self, example_can_addressing_information,
                                                                      message, start_timeout, send_after, delay):
        """
        Check for a timeout during asynchronous receiving of a UDS message (carried by First Frame and
        Consecutive Frame packets).

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frames that carry received
            UDS message (First Frame and then Consecutive Frames).
        2. Call async method to receive message via Transport Interface.
            Expected: Timeout exception is raised.

        :param example_can_addressing_information: Addressing Information of receiving CAN Node.
            :param message: UDS message to transmit.
        :param start_timeout: Maximal time (in milliseconds) to wait for the start of a message transmission.
        :param send_after: Time when to send First Frame after call of receive method [ms].
        :param delay: Time distance to use for sending Consecutive Frames [ms].
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=example_can_addressing_information)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            network_manager=self.can_interface_2,
            addressing_information=example_can_addressing_information.get_other_end())
        packets = can_transport_interface_2nd_node.segmenter.segmentation(message)

        async def _send_message():
            for packet in packets[:-1]:
                await self.async_send_packet(transport_interface=can_transport_interface_2nd_node,
                                             packet=packet,
                                             delay=send_after if packet == packets[0] else delay)

        send_message_task = asyncio.create_task(_send_message())
        with pytest.raises(TimeoutError):
            await can_transport_interface.async_receive_message(start_timeout=start_timeout)
        await send_message_task

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22] +  [*range(255), *range(255)] * 15, addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x62, 0x12, 0x34] + [*range(100, 164)] * 65, addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("end_timeout, send_after, delay", [
        (1000, 50, 20),  # ms
        (2500, 10, 50),
    ])
    def test_receive_message__multi_packets__end_timeout(self, example_can_addressing_information,
                                                         message, end_timeout, send_after, delay):
        """
        Check for an end message timeout during synchronous multi packet (FF + CF) UDS message reception.

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frames that carry received
            UDS message (First Frame and then Consecutive Frames).
        2. Call method to receive message via Transport Interface with timeout set before the entire segmented
            UDS message is transmitted.
            Expected: Timeout exception is raised.

        :param example_can_addressing_information: Addressing Information of receiving CAN Node.
        :param message: UDS message to transmit.
        :param end_timeout: Maximal time (in milliseconds) to wait for the end of a message transmission.
        :param send_after: Time when to send First Frame after call of receive method [ms].
        :param delay: Time distance to use for sending Consecutive Frames [ms].
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=example_can_addressing_information,
            n_br=0)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            network_manager=self.can_interface_2,
            addressing_information=example_can_addressing_information.get_other_end())
        packets = can_transport_interface_2nd_node.segmenter.segmentation(message)
        for i, packet in enumerate(packets):
            self.send_packet(transport_interface=can_transport_interface_2nd_node,
                             packet=packet,
                             delay=send_after + i * delay)
        time_before_receive = time()
        with pytest.raises(TimeoutError):
            can_transport_interface.receive_message(start_timeout=2 * send_after + 50,
                                                    end_timeout=end_timeout)
        time_after_receive = time()
        # timing parameters
        receiving_time_ms = (time_after_receive - time_before_receive) * 1000.
        assert (end_timeout
                < receiving_time_ms
                < end_timeout + self.TASK_TIMING_TOLERANCE)

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22] +  [*range(255), *range(255)] * 15, addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x62, 0x12, 0x34] + [*range(100, 164)] * 65, addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("end_timeout, send_after, delay", [
        (1000, 50, 20),  # ms
        (2500, 10, 50),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_message__multi_packets__end_timeout(self, example_can_addressing_information,
                                                                     message, end_timeout, send_after, delay):
        """
        Check for an end message timeout during asynchronous multi packet (FF + CF) UDS message reception.

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frames that carry received
            UDS message (First Frame and then Consecutive Frames).
        2. Call method to receive message via Transport Interface with timeout set before the entire segmented
            UDS message is transmitted.
            Expected: Timeout exception is raised.

        :param example_can_addressing_information: Addressing Information of receiving CAN Node.
        :param message: UDS message to transmit.
        :param end_timeout: Maximal time (in milliseconds) to wait for the end of a message transmission.
        :param send_after: Time when to send First Frame after call of receive method [ms].
        :param delay: Time distance to use for sending Consecutive Frames [ms].
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=example_can_addressing_information,
            n_br=0)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            network_manager=self.can_interface_2,
            addressing_information=example_can_addressing_information.get_other_end())
        packets = can_transport_interface_2nd_node.segmenter.segmentation(message)

        async def _send_message():
            for packet in packets[:-1]:
                await self.async_send_packet(transport_interface=can_transport_interface_2nd_node,
                                             packet=packet,
                                             delay=send_after if packet == packets[0] else delay)

        send_message_task = asyncio.create_task(_send_message())

        time_before_receive = time()
        with pytest.raises(TimeoutError):
            await can_transport_interface.async_receive_message(start_timeout=2 * send_after + 50,
                                                                end_timeout=end_timeout)
        time_after_receive = time()
        send_message_task.cancel()
        try:
            await send_message_task
        except asyncio.CancelledError:
            ...
        # timing parameters
        receiving_time_ms = (time_after_receive - time_before_receive) * 1000.
        assert (end_timeout - self.TASK_TIMING_TOLERANCE  # TODO: end_timeout is desired value, but asyncio.wait_for works inconsistently
                < receiving_time_ms
                < end_timeout + self.TASK_TIMING_TOLERANCE)

    @pytest.mark.parametrize("tx_message, rx_message, tx_block_size, tx_st_min, rx_block_size, rx_st_min", [
        (
            UdsMessage(payload=[0x22, 0x12, 0x34, 0x56, 0x78], addressing_type=AddressingType.PHYSICAL),
            UdsMessage(payload=[0x54], addressing_type=AddressingType.FUNCTIONAL),
            0, 0, 0, 0
        ),
        (
            UdsMessage(payload=[0x22, *range(10)], addressing_type=AddressingType.PHYSICAL),
            UdsMessage(payload=[0x62, *range(15)], addressing_type=AddressingType.PHYSICAL),
            2, 25, 5, 120
        ),
        (
            UdsMessage(payload=[0x22, *range(256), *range(256), *range(256)],
                       addressing_type=AddressingType.PHYSICAL),
            UdsMessage(payload=[0x62, *range(256), *range(256), *range(256)],
                       addressing_type=AddressingType.PHYSICAL),
            0, 0, 2, 5,
        ),
    ])
    def test_full_duplex(self, example_can_addressing_information,
                         tx_message, rx_message, tx_block_size, tx_st_min, rx_block_size, rx_st_min):
        """
        Check for a full-duplex communication during synchronous UDS message sending.

        Procedure:
        1. Schedule receiving messages on both Transport Interfaces.
        2. Schedule sending messages on both Transport Interfaces.
        3. Wait till all tasks are finished (messages are sent and received).
        4. Validate UDS message record attributes.
            Expected: Attributes of received UDS message records are in line with messages attributes scheduled for
                the transmission.

        :param example_can_addressing_information: Example Addressing Information of a CAN Node.
        :param tx_message: UDS message to send on interface 1 and receive on interface 2.
        :param rx_message: UDS message to send on interface 2 and receive on interface 1.
        :param tx_block_size: Block Size parameter value for interface 1.
        :param tx_st_min: STmin parameter value for interface 1.
        :param rx_block_size: Block Size parameter value for interface 2.
        :param rx_st_min: STmin parameter value for interface 2.
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=example_can_addressing_information,
            flow_control_parameters_generator=DefaultFlowControlParametersGenerator(block_size=tx_block_size,
                                                                                    st_min=tx_st_min))
        can_transport_interface_2nd_node = PyCanTransportInterface(
            network_manager=self.can_interface_2,
            addressing_information=example_can_addressing_information.get_other_end(),
            flow_control_parameters_generator=DefaultFlowControlParametersGenerator(block_size=rx_block_size,
                                                                                    st_min=rx_st_min))
        timer_1 = self.receive_message(transport_interface=can_transport_interface_2nd_node,
                                       delay=0,
                                       start_timeout=50,
                                       end_timeout=None)
        timer_2 = self.send_message(transport_interface=can_transport_interface_2nd_node,
                                    message=rx_message,
                                    delay=10)
        timer_3 = self.send_message(transport_interface=can_transport_interface,
                                    message=tx_message,
                                    delay=10)
        received_rx_message_record = can_transport_interface.receive_message(start_timeout=50)
        while not all([timer_1.finished.is_set(), timer_2.finished.is_set(), timer_3.finished.is_set()]):
            sleep(self.TASK_TIMING_TOLERANCE / 1000.)
        received_tx_message_record = self.received_message
        assert isinstance(received_tx_message_record, UdsMessageRecord)
        assert isinstance(received_rx_message_record, UdsMessageRecord)
        assert received_tx_message_record.payload == tx_message.payload
        assert received_tx_message_record.addressing_type == tx_message.addressing_type
        assert received_rx_message_record.payload == rx_message.payload
        assert received_rx_message_record.addressing_type == rx_message.addressing_type

    @pytest.mark.parametrize("tx_message, rx_message, tx_block_size, tx_st_min, rx_block_size, rx_st_min", [
        (
            UdsMessage(payload=[0x22, 0x12, 0x34, 0x56, 0x78], addressing_type=AddressingType.PHYSICAL),
            UdsMessage(payload=[0x54], addressing_type=AddressingType.FUNCTIONAL),
            0, 0, 0, 0
        ),
        (
            UdsMessage(payload=[0x22, *range(10)], addressing_type=AddressingType.PHYSICAL),
            UdsMessage(payload=[0x62, *range(15)], addressing_type=AddressingType.PHYSICAL),
            2, 25, 5, 120
        ),
        (
            UdsMessage(payload=[0x22, *range(256), *range(256), *range(256)],
                       addressing_type=AddressingType.PHYSICAL),
            UdsMessage(payload=[0x62, *range(256), *range(256), *range(256)],
                       addressing_type=AddressingType.PHYSICAL),
            0, 0, 2, 5,
        ),
    ])
    @pytest.mark.asyncio
    async def test_async_full_duplex(self, example_can_addressing_information,
                                     tx_message, rx_message, tx_block_size, tx_st_min, rx_block_size, rx_st_min):
        """
        Check for a full-duplex communication during asynchronous UDS message sending.

        Procedure:
        1. Schedule receiving messages on both Transport Interfaces.
        2. Schedule sending messages on both Transport Interfaces.
        3. Wait till all tasks are finished (messages are sent and received).
        4. Validate UDS message record attributes.
            Expected: Attributes of received UDS message records are in line with the transmitted UDS messages records.

        :param example_can_addressing_information: Example Addressing Information of a CAN Node.
        :param tx_message: UDS message to send on interface 1 and receive on interface 2.
        :param rx_message: UDS message to send on interface 2 and receive on interface 1.
        :param tx_block_size: Block Size parameter value for interface 1.
        :param tx_st_min: STmin parameter value for interface 1.
        :param rx_block_size: Block Size parameter value for interface 2.
        :param rx_st_min: STmin parameter value for interface 2.
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=example_can_addressing_information,
            flow_control_parameters_generator=DefaultFlowControlParametersGenerator(block_size=tx_block_size,
                                                                                    st_min=tx_st_min))
        can_transport_interface_2nd_node = PyCanTransportInterface(
            network_manager=self.can_interface_2,
            addressing_information=example_can_addressing_information.get_other_end(),
            flow_control_parameters_generator=DefaultFlowControlParametersGenerator(block_size=rx_block_size,
                                                                                    st_min=rx_st_min))
        received_rx_message_task = asyncio.create_task(
            can_transport_interface.async_receive_message(start_timeout=50))
        received_tx_message_task = asyncio.create_task(
            can_transport_interface_2nd_node.async_receive_message(start_timeout=50))
        sent_tx_message_task = asyncio.create_task(
            can_transport_interface.async_send_message(message=tx_message))
        sent_rx_message_task = asyncio.create_task(
            can_transport_interface_2nd_node.async_send_message(message=rx_message))
        tasks = [received_tx_message_task,
                 received_rx_message_task,
                 sent_tx_message_task,
                 sent_rx_message_task]
        await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
        received_tx_message_record = await received_tx_message_task
        received_rx_message_record = await received_rx_message_task
        sent_tx_message_record = await sent_tx_message_task
        sent_rx_message_record = await sent_rx_message_task
        assert isinstance(received_tx_message_record, UdsMessageRecord)
        assert isinstance(received_rx_message_record, UdsMessageRecord)
        assert isinstance(sent_tx_message_record, UdsMessageRecord)
        assert isinstance(sent_rx_message_record, UdsMessageRecord)
        assert received_tx_message_record.payload == sent_tx_message_record.payload == tx_message.payload
        assert (received_tx_message_record.addressing_type == sent_tx_message_record.addressing_type
                == tx_message.addressing_type)
        assert received_rx_message_record.payload == sent_rx_message_record.payload == rx_message.payload
        assert (received_rx_message_record.addressing_type == sent_rx_message_record.addressing_type
                == rx_message.addressing_type)


class AbstractUseCaseTests(AbstractPythonCanTests, ABC):
    """Common implementation of system tests wih typical use case scenarios."""

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_format, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_ADDRESSING,
         {"payload": [0x54]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x8}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.EXTENDED_ADDRESSING,
         {"payload": b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87\x78\x69\x5A\x4B\x3C\x2D\x1E\x0F\xFF",
          "sequence_number": 0xF, "filler_byte": 0x5A}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         {"flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x00, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         {"dlc": 0xF, "filler_byte": 0x00, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A]}),
    ])
    def test_send_packet_on_one_receive_on_other_interface(self, packet_type, addressing_type, addressing_format,
                                                           packet_type_specific_kwargs,
                                                           parametrized_can_addressing_information):
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
        :param addressing_format: CAN Addressing Format to use.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        """
        can_transport_interface_1 = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=parametrized_can_addressing_information)
        can_transport_interface_2 = PyCanTransportInterface(
            network_manager=self.can_interface_2,
            addressing_information=parametrized_can_addressing_information.get_other_end())
        if addressing_type == AddressingType.PHYSICAL:
            addressing_params = parametrized_can_addressing_information.tx_physical_params
        else:
            addressing_params = parametrized_can_addressing_information.tx_functional_params
        packet = CanPacket(packet_type=packet_type,
                           **addressing_params,
                           **packet_type_specific_kwargs)
        sent_packet_record = can_transport_interface_1.send_packet(packet)
        received_packet_record = can_transport_interface_2.receive_packet(timeout=100)
        assert isinstance(sent_packet_record, CanPacketRecord)
        assert isinstance(received_packet_record, CanPacketRecord)
        assert sent_packet_record.direction == TransmissionDirection.TRANSMITTED
        assert received_packet_record.direction == TransmissionDirection.RECEIVED
        assert received_packet_record.raw_frame_data == sent_packet_record.raw_frame_data == packet.raw_frame_data
        assert (received_packet_record.addressing_format == sent_packet_record.addressing_format
                == packet.addressing_format == addressing_format
                == parametrized_can_addressing_information.ADDRESSING_FORMAT)
        assert received_packet_record.packet_type == sent_packet_record.packet_type == packet.packet_type == packet_type
        assert (received_packet_record.can_id == sent_packet_record.can_id == packet.can_id
                == addressing_params["can_id"])
        assert (received_packet_record.addressing_type == sent_packet_record.addressing_type
                == packet.addressing_type == addressing_type)
        assert (received_packet_record.target_address == sent_packet_record.target_address
                == packet.target_address == addressing_params["target_address"])
        assert (received_packet_record.source_address == sent_packet_record.source_address
                == packet.source_address == addressing_params["source_address"])
        assert (received_packet_record.address_extension == sent_packet_record.address_extension
                == packet.address_extension == addressing_params["address_extension"])

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_format, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_ADDRESSING,
         {"payload": [0x54]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x8}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.EXTENDED_ADDRESSING,
         {"payload": b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87\x78\x69\x5A\x4B\x3C\x2D\x1E\x0F\xFF",
          "sequence_number": 0xF, "filler_byte": 0x5A}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         {"flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x00, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         {"dlc": 0xF, "filler_byte": 0x00, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A]}),
    ])
    @pytest.mark.asyncio
    async def test_async_send_packet_on_one_receive_on_other_interface(self, packet_type, addressing_type,
                                                                       addressing_format,
                                                                       packet_type_specific_kwargs,
                                                                       parametrized_can_addressing_information):
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
        :param addressing_format: CAN Addressing Format to use.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        """
        can_transport_interface_1 = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=parametrized_can_addressing_information)
        can_transport_interface_2 = PyCanTransportInterface(
            network_manager=self.can_interface_2,
            addressing_information=parametrized_can_addressing_information.get_other_end())
        if addressing_type == AddressingType.PHYSICAL:
            addressing_params = parametrized_can_addressing_information.tx_physical_params
        else:
            addressing_params = parametrized_can_addressing_information.tx_functional_params
        packet = CanPacket(packet_type=packet_type,
                           **addressing_params,
                           **packet_type_specific_kwargs)
        receive_packet_task = asyncio.create_task(can_transport_interface_2.async_receive_packet(timeout=100))
        sent_packet_record = await can_transport_interface_1.async_send_packet(packet)
        received_packet_record = await receive_packet_task
        assert isinstance(sent_packet_record, CanPacketRecord)
        assert isinstance(received_packet_record, CanPacketRecord)
        assert sent_packet_record.direction == TransmissionDirection.TRANSMITTED
        assert received_packet_record.direction == TransmissionDirection.RECEIVED
        assert received_packet_record.raw_frame_data == sent_packet_record.raw_frame_data == packet.raw_frame_data
        assert (received_packet_record.addressing_format == sent_packet_record.addressing_format
                == packet.addressing_format == addressing_format
                == parametrized_can_addressing_information.ADDRESSING_FORMAT)
        assert received_packet_record.packet_type == sent_packet_record.packet_type == packet.packet_type == packet_type
        assert (received_packet_record.can_id == sent_packet_record.can_id == packet.can_id
                == addressing_params["can_id"])
        assert (received_packet_record.addressing_type == sent_packet_record.addressing_type
                == packet.addressing_type == addressing_type)
        assert (received_packet_record.target_address == sent_packet_record.target_address
                == packet.target_address == addressing_params["target_address"])
        assert (received_packet_record.source_address == sent_packet_record.source_address
                == packet.source_address == addressing_params["source_address"])
        assert (received_packet_record.address_extension == sent_packet_record.address_extension
                == packet.address_extension == addressing_params["address_extension"])

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
    def test_send_message_on_one_receive_on_other_interface(self, example_can_addressing_information,
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

        :param example_can_addressing_information: Addressing Information for a receiving CAN Node.
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
            network_manager=self.can_interface_1,
            addressing_information=example_can_addressing_information,
            n_br=n_br,
            flow_control_parameters_generator=flow_control_parameters_generator)
        can_transport_interface_2 = PyCanTransportInterface(
            network_manager=self.can_interface_2,
            addressing_information=example_can_addressing_information.get_other_end(),
            n_cs=n_cs)

        timer = self.send_message(transport_interface=can_transport_interface_1,
                                  message=message,
                                  delay=send_after)
        received_message_record = can_transport_interface_2.receive_message(start_timeout=timeout)
        while not timer.finished.is_set():
            sleep(self.TASK_TIMING_TOLERANCE / 1000.)
        assert isinstance(self.sent_message, UdsMessageRecord)
        assert isinstance(received_message_record, UdsMessageRecord)
        assert self.sent_message.direction == TransmissionDirection.TRANSMITTED
        assert received_message_record.direction == TransmissionDirection.RECEIVED
        assert self.sent_message.addressing_type == message.addressing_type
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
    async def test_async_send_message_on_one_receive_on_other_interface(self, example_can_addressing_information,
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

        :param example_can_addressing_information: Addressing Information for a receiving CAN Node.
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
            network_manager=self.can_interface_1,
            addressing_information=example_can_addressing_information,
            n_br=n_br,
            flow_control_parameters_generator=flow_control_parameters_generator)
        can_transport_interface_2 = PyCanTransportInterface(
            network_manager=self.can_interface_2,
            addressing_information=example_can_addressing_information.get_other_end(),
            n_cs=n_cs)

        receive_message_task = asyncio.create_task(can_transport_interface_2.async_receive_message(
            start_timeout=timeout))
        send_message_task = asyncio.create_task(
            self.async_send_message(transport_interface=can_transport_interface_1,
                                    message=message,
                                    delay=send_after))
        sent_message_record = await send_message_task
        received_message_record = await receive_message_task
        assert isinstance(sent_message_record, UdsMessageRecord)
        assert isinstance(received_message_record, UdsMessageRecord)
        assert sent_message_record.direction == TransmissionDirection.TRANSMITTED
        assert received_message_record.direction == TransmissionDirection.RECEIVED
        assert sent_message_record.addressing_type == message.addressing_type
        assert sent_message_record.payload == received_message_record.payload == message.payload


class AbstractErrorGuessingTests(AbstractPythonCanTests, ABC):
    """Common implementation of guessing errors system tests."""

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_format, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_ADDRESSING,
         {"payload": [0x54]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x8}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.EXTENDED_ADDRESSING,
         {"payload": b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87\x78\x69\x5A\x4B\x3C\x2D\x1E\x0F\xFF",
          "sequence_number": 0xF, "filler_byte": 0x5A}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         {"flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x00, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         {"dlc": 0xF, "filler_byte": 0x00, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A]}),
    ])
    def test_timeout_then_send_packet(self, packet_type, addressing_type, addressing_format, packet_type_specific_kwargs,
                                      parametrized_can_addressing_information):
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
        :param addressing_format: CAN Addressing Format to use.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=parametrized_can_addressing_information)
        if addressing_type == AddressingType.PHYSICAL:
            addressing_params = parametrized_can_addressing_information.tx_physical_params
        else:
            addressing_params = parametrized_can_addressing_information.tx_functional_params
        packet = CanPacket(packet_type=packet_type,
                           **addressing_params,
                           **packet_type_specific_kwargs)
        with pytest.raises(TimeoutError):
            can_transport_interface.receive_packet(timeout=100)
        packet_record = can_transport_interface.send_packet(packet)
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.TRANSMITTED
        assert packet_record.raw_frame_data == packet.raw_frame_data
        assert (packet_record.addressing_format == packet.addressing_format == addressing_format
                == parametrized_can_addressing_information.ADDRESSING_FORMAT)
        assert packet_record.packet_type == packet.packet_type == packet_type
        assert packet_record.can_id == packet.can_id == addressing_params["can_id"]
        assert packet_record.addressing_type == packet.addressing_type == addressing_type
        assert packet_record.target_address == packet.target_address == addressing_params["target_address"]
        assert packet_record.source_address == packet.source_address == addressing_params["source_address"]
        assert packet_record.address_extension == packet.address_extension == addressing_params["address_extension"]

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_format, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_ADDRESSING,
         {"payload": [0x54]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x8}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.EXTENDED_ADDRESSING,
         {"payload": b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87\x78\x69\x5A\x4B\x3C\x2D\x1E\x0F\xFF",
          "sequence_number": 0xF, "filler_byte": 0x5A}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         {"flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x00, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         {"dlc": 0xF, "filler_byte": 0x00, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A]}),
    ])
    @pytest.mark.asyncio
    async def test_async_timeout_then_send_packet(self, packet_type, addressing_type, addressing_format,
                                                  packet_type_specific_kwargs,
                                                  parametrized_can_addressing_information):
        """
        Check for asynchronous sending a CAN packet after a timeout exception during asynchronous receiving.

        Procedure:
        1. Call async method to receive packet via Transport Interface.
            Expected: Timeout exception is raised.
        2. Send (using async method) a CAN packet via Transport Interface.
            Expected: CAN packet record returned.
        3. Validate transmitted CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the transmitted CAN packet.

        :param example_can_addressing_information,: Example Addressing Information of a CAN Node.
        :param packet_type: Type of CAN packet to send.
        :param addressing_type: Addressing type to use for transmitting a CAN packet.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=parametrized_can_addressing_information)
        if addressing_type == AddressingType.PHYSICAL:
            addressing_params = parametrized_can_addressing_information.rx_physical_params
        else:
            addressing_params = parametrized_can_addressing_information.rx_functional_params
        packet = CanPacket(packet_type=packet_type,
                           **addressing_params,
                           **packet_type_specific_kwargs)
        with pytest.raises((TimeoutError, asyncio.TimeoutError)):
            await can_transport_interface.async_receive_packet(timeout=100)
        packet_record = await can_transport_interface.async_send_packet(packet)
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.TRANSMITTED
        assert packet_record.raw_frame_data == packet.raw_frame_data
        assert (packet_record.addressing_format == packet.addressing_format == addressing_format
                == parametrized_can_addressing_information.ADDRESSING_FORMAT)
        assert packet_record.packet_type == packet.packet_type == packet_type
        assert packet_record.can_id == packet.can_id == addressing_params["can_id"]
        assert packet_record.addressing_type == packet.addressing_type == addressing_type
        assert packet_record.target_address == packet.target_address == addressing_params["target_address"]
        assert packet_record.source_address == packet.source_address == addressing_params["source_address"]
        assert packet_record.address_extension == packet.address_extension == addressing_params["address_extension"]

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_format, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_ADDRESSING,
         {"payload": [0x54]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x8}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.EXTENDED_ADDRESSING,
         {"payload": b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87\x78\x69\x5A\x4B\x3C\x2D\x1E\x0F\xFF",
          "sequence_number": 0xF, "filler_byte": 0x5A}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         {"flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x00, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         {"dlc": 0xF, "filler_byte": 0x00, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A]}),
    ])
    def test_timeout_then_receive_packet(self, packet_type, addressing_type, addressing_format,
                                         packet_type_specific_kwargs,
                                         parametrized_can_addressing_information):
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
        :param addressing_format: CAN Addressing Format to use.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=parametrized_can_addressing_information)
        if addressing_type == AddressingType.PHYSICAL:
            addressing_params = parametrized_can_addressing_information.rx_physical_params
        else:
            addressing_params = parametrized_can_addressing_information.rx_functional_params
        packet = CanPacket(packet_type=packet_type,
                           **addressing_params,
                           **packet_type_specific_kwargs)
        can_frame = Message(arbitration_id=packet.can_id,
                            data=packet.raw_frame_data,
                            is_fd=packet.dlc > 8)
        with pytest.raises(TimeoutError):
            can_transport_interface.receive_packet(timeout=100)
        time_before_send = time()
        self.can_interface_2.send(can_frame)
        packet_record = can_transport_interface.receive_packet(timeout=100)
        time_after_receive = time()
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.RECEIVED
        assert packet_record.raw_frame_data == packet.raw_frame_data == bytes(can_frame.data)
        assert (packet_record.addressing_format == packet.addressing_format == addressing_format
                == parametrized_can_addressing_information.ADDRESSING_FORMAT)
        assert packet_record.packet_type == packet.packet_type == packet_type
        assert packet_record.addressing_type == packet.addressing_type == addressing_type
        assert packet_record.can_id == packet.can_id == can_frame.arbitration_id == addressing_params["can_id"]
        assert packet_record.target_address == packet.target_address == addressing_params["target_address"]
        assert packet_record.source_address == packet.source_address == addressing_params["source_address"]
        assert packet_record.address_extension == packet.address_extension == addressing_params["address_extension"]
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            assert (datetime.fromtimestamp(time_before_send - self.TIMESTAMP_TOLERANCE / 1000.)
                    <= packet_record.transmission_time
                    <= datetime.fromtimestamp(time_after_receive + self.TIMESTAMP_TOLERANCE / 1000.))

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_format, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_ADDRESSING,
         {"payload": [0x54]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x8}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.EXTENDED_ADDRESSING,
         {"payload": b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87\x78\x69\x5A\x4B\x3C\x2D\x1E\x0F\xFF",
          "sequence_number": 0xF, "filler_byte": 0x5A}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         {"flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x00, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         {"dlc": 0xF, "filler_byte": 0x00, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A]}),
    ])
    @pytest.mark.asyncio
    async def test_async_timeout_then_receive_packet(self, packet_type, addressing_type, addressing_format,
                                                     packet_type_specific_kwargs,
                                                     parametrized_can_addressing_information):
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
        :param addressing_format: CAN Addressing Format to use.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=parametrized_can_addressing_information)
        if addressing_type == AddressingType.PHYSICAL:
            addressing_params = parametrized_can_addressing_information.rx_physical_params
        else:
            addressing_params = parametrized_can_addressing_information.rx_functional_params
        packet = CanPacket(packet_type=packet_type,
                           **addressing_params,
                           **packet_type_specific_kwargs)
        can_frame = Message(arbitration_id=packet.can_id,
                            data=packet.raw_frame_data,
                            is_fd=packet.dlc > 8)
        with pytest.raises((TimeoutError, asyncio.TimeoutError)):
            await can_transport_interface.async_receive_packet(timeout=100)
        time_before_send = time()
        self.can_interface_2.send(can_frame)
        packet_record = await can_transport_interface.async_receive_packet(timeout=100)
        time_after_receive = time()
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.RECEIVED
        assert packet_record.raw_frame_data == packet.raw_frame_data == bytes(can_frame.data)
        assert (packet_record.addressing_format == packet.addressing_format == addressing_format
                == parametrized_can_addressing_information.ADDRESSING_FORMAT)
        assert packet_record.packet_type == packet.packet_type == packet_type
        assert packet_record.addressing_type == packet.addressing_type == addressing_type
        assert packet_record.can_id == packet.can_id == can_frame.arbitration_id == addressing_params["can_id"]
        assert packet_record.target_address == packet.target_address == addressing_params["target_address"]
        assert packet_record.source_address == packet.source_address == addressing_params["source_address"]
        assert packet_record.address_extension == packet.address_extension == addressing_params["address_extension"]
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            assert (datetime.fromtimestamp(time_before_send - self.TIMESTAMP_TOLERANCE / 1000.)
                    <= packet_record.transmission_time
                    <= datetime.fromtimestamp(time_after_receive + self.TIMESTAMP_TOLERANCE / 1000.))

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_format, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_ADDRESSING,
         {"payload": [0x54]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x8}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.EXTENDED_ADDRESSING,
         {"payload": b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87\x78\x69\x5A\x4B\x3C\x2D\x1E\x0F\xFF",
          "sequence_number": 0xF, "filler_byte": 0x5A}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         {"flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x00, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         {"dlc": 0xF, "filler_byte": 0x00, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A]}),
    ])
    def test_observe_tx_packet(self, packet_type, addressing_type, addressing_format, packet_type_specific_kwargs,
                               parametrized_can_addressing_information):
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
        :param addressing_format: CAN Addressing Format to use.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=parametrized_can_addressing_information)
        if addressing_type == AddressingType.PHYSICAL:
            addressing_params = parametrized_can_addressing_information.tx_physical_params
        else:
            addressing_params = parametrized_can_addressing_information.tx_functional_params
        packet = CanPacket(packet_type=packet_type,
                           **addressing_params,
                           **packet_type_specific_kwargs)
        can_frame = Message(arbitration_id=packet.can_id,
                            data=packet.raw_frame_data,
                            is_fd=packet.dlc > 8)
        self.can_interface_1.send(can_frame)
        sleep(0.1)
        time_before_send = time()
        packet_record = can_transport_interface.send_packet(packet)
        time_after_send = time()
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.TRANSMITTED
        assert packet_record.raw_frame_data == packet.raw_frame_data
        assert (packet_record.addressing_format == packet.addressing_format == addressing_format
                == parametrized_can_addressing_information.ADDRESSING_FORMAT)
        assert packet_record.packet_type == packet.packet_type == packet_type
        assert packet_record.can_id == packet.can_id == addressing_params["can_id"]
        assert packet_record.addressing_type == packet.addressing_type == addressing_type
        assert packet_record.target_address == packet.target_address == addressing_params["target_address"]
        assert packet_record.source_address == packet.source_address == addressing_params["source_address"]
        assert packet_record.address_extension == packet.address_extension == addressing_params["address_extension"]
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            assert (datetime.fromtimestamp(time_before_send - self.TIMESTAMP_TOLERANCE / 1000.)
                    <= packet_record.transmission_time
                    <= datetime.fromtimestamp(time_after_send + self.TIMESTAMP_TOLERANCE / 1000.))

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_format, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_ADDRESSING,
         {"payload": [0x54]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x8}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingFormat.EXTENDED_ADDRESSING,
         {"payload": b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87\x78\x69\x5A\x4B\x3C\x2D\x1E\x0F\xFF",
          "sequence_number": 0xF, "filler_byte": 0x5A}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         {"flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x00, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         {"dlc": 0xF, "filler_byte": 0x00, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A]}),
    ])
    @pytest.mark.asyncio
    async def test_async_observe_tx_packet(self, packet_type, addressing_type, addressing_format,
                                           packet_type_specific_kwargs,
                                           parametrized_can_addressing_information):
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
        :param addressing_format: CAN Addressing Format to use.
        :param packet_type_specific_kwargs: Parameters specific for this CAN packet type.
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=parametrized_can_addressing_information)
        if addressing_type == AddressingType.PHYSICAL:
            addressing_params = parametrized_can_addressing_information.tx_physical_params
        else:
            addressing_params = parametrized_can_addressing_information.tx_functional_params
        packet = CanPacket(packet_type=packet_type,
                           **addressing_params,
                           **packet_type_specific_kwargs)
        can_frame = Message(arbitration_id=packet.can_id,
                            data=packet.raw_frame_data,
                            is_fd=packet.dlc > 8)
        self.can_interface_1.send(can_frame)
        sleep(0.1)
        time_before_send = time()
        packet_record = await can_transport_interface.async_send_packet(packet)
        time_after_send = time()
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.TRANSMITTED
        assert packet_record.raw_frame_data == packet.raw_frame_data
        assert (packet_record.addressing_format == packet.addressing_format == addressing_format
                == parametrized_can_addressing_information.ADDRESSING_FORMAT)
        assert packet_record.packet_type == packet.packet_type == packet_type
        assert packet_record.can_id == packet.can_id == addressing_params["can_id"]
        assert packet_record.addressing_type == packet.addressing_type == addressing_type
        assert packet_record.target_address == packet.target_address == addressing_params["target_address"]
        assert packet_record.source_address == packet.source_address == addressing_params["source_address"]
        assert packet_record.address_extension == packet.address_extension == addressing_params["address_extension"]
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            assert (datetime.fromtimestamp(time_before_send - self.TIMESTAMP_TOLERANCE / 1000.)
                    <= packet_record.transmission_time
                    <= datetime.fromtimestamp(time_after_send + self.TIMESTAMP_TOLERANCE / 1000.))

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, *range(62)], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x62, 0x12, 0x34, *range(100, 250)], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        (1000, 50),  # ms
        (50, 0),
    ])
    def test_overflow_during_message_sending(self, example_can_addressing_information,
                                             message, timeout, send_after):
        """
        Check for handling Overflow status during synchronous multi packet (FF + CF) UDS message sending.

        Procedure:
        1. Schedule Flow Control CAN Packet with Overflow information.
        2. Send a UDS message using Transport Interface (via CAN Interface).
            Expected: UDS message transmission stopped and an exception raised.

        :param example_can_addressing_information: Example Addressing Information of a CAN Node.
        :param message: UDS message to send.
        :param send_after: Delay to use for sending CAN flow control.
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=example_can_addressing_information,
            n_bs_timeout=timeout)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            network_manager=self.can_interface_2,
            addressing_information=example_can_addressing_information.get_other_end())
        flow_control_packet = can_transport_interface_2nd_node.segmenter.get_flow_control_packet(
            flow_status=CanFlowStatus.Overflow)
        self.send_packet(transport_interface=can_transport_interface_2nd_node,
                         packet=flow_control_packet,
                         delay=send_after)
        with pytest.raises(OverflowError):
            can_transport_interface.send_message(message)

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x22, *range(62)], addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=[0x62, 0x12, 0x34, *range(100, 250)], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        (1000, 50),  # ms
        (50, 0),
    ])
    @pytest.mark.asyncio
    async def test_overflow_during_async_message_sending(self, example_can_addressing_information,
                                                         message, timeout, send_after):
        """
        Check for handling Overflow status during asynchronous multi packet (FF + CF) UDS message sending.

        Procedure:
        1. Schedule Flow Control CAN Packet with Overflow information.
        2. Send (using async method) a UDS message using Transport Interface (via CAN Interface).
            Expected: UDS message transmission stopped and an exception raised.

        :param example_can_addressing_information: Example Addressing Information of a CAN Node.
        :param message: UDS message to send.
        :param send_after: Delay to use for sending CAN flow control.
        """
        can_transport_interface = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=example_can_addressing_information,
            n_bs_timeout=timeout)
        can_transport_interface_2nd_node = PyCanTransportInterface(
            network_manager=self.can_interface_2,
            addressing_information=example_can_addressing_information.get_other_end())
        flow_control_packet = can_transport_interface_2nd_node.segmenter.get_flow_control_packet(
            flow_status=CanFlowStatus.Overflow)
        send_packet_task = asyncio.create_task(self.async_send_packet(
            transport_interface=can_transport_interface_2nd_node,
            packet=flow_control_packet,
            delay=send_after))
        with pytest.raises(OverflowError):
            await can_transport_interface.async_send_message(message)
        await send_packet_task

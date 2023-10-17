import pytest
import asyncio
from threading import Timer
from time import time, sleep
from datetime import datetime
from can import Bus, Message

from uds.can import CanAddressingInformation, CanAddressingFormat, CanFlowStatus
from uds.transport_interface import PyCanTransportInterface
from uds.transmission_attributes import AddressingType, TransmissionDirection
from uds.packet import CanPacket, CanPacketType, CanPacketRecord
from uds.message import UdsMessage


class TestPythonCanKvaser:
    """System Tests for `PyCanTransportInterface` with Kvaser as bus manager."""

    def setup_class(self):
        self.bus1 = Bus(interface="kvaser", channel=0, fd=True, receive_own_messages=True)
        self.bus2 = Bus(interface="kvaser", channel=1, fd=True, receive_own_messages=True)

    def teardown_class(self):
        """Safely close bus objects."""
        self.bus1.shutdown()
        self.bus2.shutdown()

    # send_packet

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_information, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x611},
                                  rx_physical={"can_id": 0x612},
                                  tx_functional={"can_id": 0x6FF},
                                  rx_functional={"can_id": 0x6FE}),
         {"filler_byte": 0x1E, "payload": [0x10, 0x04]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B},
                                  tx_functional={"target_address": 0xAC, "source_address": 0xFE},
                                  rx_functional={"target_address": 0xFE, "source_address": 0xAC}),
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x13}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                  tx_physical={"can_id": 0x987, "target_address": 0x90},
                                  rx_physical={"can_id": 0x987, "target_address": 0xFE},
                                  tx_functional={"can_id": 0x11765, "target_address": 0x5A},
                                  rx_functional={"can_id": 0x11765, "target_address": 0xFF}),
         {"payload": [0x32, 0xFF], "sequence_number": 0xF}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x651, "address_extension": 0x87},
                                  rx_physical={"can_id": 0x652, "address_extension": 0xFE},
                                  tx_functional={"can_id": 0x6FF, "address_extension": 0xA5},
                                  rx_functional={"can_id": 0x6FF, "address_extension": 0xFF}),
         {"dlc": 8, "flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x15, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF, "address_extension": 0x87},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B, "address_extension": 0x87},
                                  tx_functional={"target_address": 0xAC, "source_address": 0xFE, "address_extension": 0xFF},
                                  rx_functional={"target_address": 0xFE, "source_address": 0xAC, "address_extension": 0xFF}),
         {"filler_byte": 0xBC, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A, 0x12, 0xBC], "dlc":0xF}),
    ])
    def test_send_packet(self, packet_type, addressing_type, addressing_information, packet_type_specific_kwargs):
        # TODO: docstring
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
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.bus1,
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
        # performance checks
        # TODO: sometimes fail because of https://github.com/hardbyte/python-can/issues/1676 - uncomment when resolved
        # assert datetime_before_send < packet_record.transmission_time < datetime_after_send

    # receive_packet

    @pytest.mark.parametrize("addressing_type, addressing_information, frame", [
        (AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x611},
                                  rx_physical={"can_id": 0x612},
                                  tx_functional={"can_id": 0x6FF},
                                  rx_functional={"can_id": 0x6FE}),
         Message(data=[0x02, 0x10, 0x03])),
        (AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B},
                                  tx_functional={"target_address": 0xAC, "source_address": 0xFE},
                                  rx_functional={"target_address": 0xFE, "source_address": 0xAC}),
         Message(data=[0x2C] + list(range(100, 163)), is_fd=True)),
        (AddressingType.FUNCTIONAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                  tx_physical={"can_id": 0x987, "target_address": 0x90},
                                  rx_physical={"can_id": 0x987, "target_address": 0xFE},
                                  tx_functional={"can_id": 0x11765, "target_address": 0x5A},
                                  rx_functional={"can_id": 0x11765, "target_address": 0xFF}, ),
         Message(data=[0xFF, 0x30, 0xAB, 0x7F])),
        (AddressingType.FUNCTIONAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x651, "address_extension": 0x87},
                                  rx_physical={"can_id": 0x652, "address_extension": 0xFE},
                                  tx_functional={"can_id": 0x6FF, "address_extension": 0xA5},
                                  rx_functional={"can_id": 0x6FF, "address_extension": 0xFF}, ),
         Message(data=[0xFF, 0x11, 0x23, 0x62, 0x92, 0xD0, 0xB1, 0x00])),
        (AddressingType.FUNCTIONAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF,
                                               "address_extension": 0x87},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B,
                                               "address_extension": 0x87},
                                  tx_functional={"target_address": 0xAC, "source_address": 0xFE,
                                                 "address_extension": 0xFF},
                                  rx_functional={"target_address": 0xFE, "source_address": 0xAC,
                                                 "address_extension": 0xFF}, ),
         Message(data=[0xFF, 0x02, 0x3E, 0x80, 0xAA, 0xAA, 0xAA, 0xAA])),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        (1000, 1001),  # ms
        (50, 55),
    ])
    def test_receive_packet__timeout(self, addressing_information, addressing_type, frame, timeout, send_after):
        # TODO: docstring
        if addressing_type == AddressingType.PHYSICAL:
            frame.arbitration_id = addressing_information.rx_packets_physical_ai["can_id"]
        else:
            frame.arbitration_id = addressing_information.rx_packets_functional_ai["can_id"]
        # data parameter of `frame` object must be set manually and according to `addressing_format`
        # and `addressing_information`
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.bus1,
                                                          addressing_information=addressing_information)
        Timer(interval=send_after/1000., function=self.bus2.send, args=(frame,)).start()
        time_before_receive = time()
        with pytest.raises(TimeoutError):
            can_transport_interface.receive_packet(timeout=timeout)
        time_after_receive = time()
        assert timeout < (time_after_receive - time_before_receive) * 1000. < timeout + 25.

    @pytest.mark.parametrize("addressing_information, frame", [
        (CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x611},
                                  rx_physical={"can_id": 0x612},
                                  tx_functional={"can_id": 0x6FF},
                                  rx_functional={"can_id": 0x6FE}),
         Message(data=[0x02, 0x10, 0x03])),
        (CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B},
                                  tx_functional={"target_address": 0xAC, "source_address": 0xFE},
                                  rx_functional={"target_address": 0xFE, "source_address": 0xAC}),
         Message(data=[0x2C] + list(range(100, 163)), is_fd=True)),
        (CanAddressingInformation(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                  tx_physical={"can_id": 0x987, "target_address": 0x90},
                                  rx_physical={"can_id": 0x987, "target_address": 0xFE},
                                  tx_functional={"can_id": 0x11765, "target_address": 0x5A},
                                  rx_functional={"can_id": 0x11765, "target_address": 0xFF}),
         Message(data=[0xFE, 0x30, 0xAB, 0x7F])),
        (CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x651, "address_extension": 0x87},
                                  rx_physical={"can_id": 0x652, "address_extension": 0xFE},
                                  tx_functional={"can_id": 0x6FF, "address_extension": 0xA5},
                                  rx_functional={"can_id": 0x6FF, "address_extension": 0xFF}),
         Message(data=[0xFE, 0x11, 0x23, 0x62, 0x92, 0xD0, 0xB1, 0x00])),
        (CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF, "address_extension": 0x87},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B, "address_extension": 0x87},
                                  tx_functional={"target_address": 0xAC, "source_address": 0xFE, "address_extension": 0xFF},
                                  rx_functional={"target_address": 0xFE, "source_address": 0xAC, "address_extension": 0xFF}),
         Message(data=[0x87, 0x02, 0x3E, 0x80, 0xAA, 0xAA, 0xAA, 0xAA])),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        (1000, 950),  # ms
        (50, 20),
    ])
    def test_receive_packet__physical(self, addressing_information, frame, timeout, send_after):
        # TODO: docstring
        frame.arbitration_id = addressing_information.rx_packets_physical_ai["can_id"]
        # data parameter of `frame` object must be set manually and according to `addressing_format`
        # and `addressing_information`
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.bus1,
                                                          addressing_information=addressing_information)
        Timer(interval=send_after/1000., function=self.bus2.send, args=(frame, )).start()
        datetime_before_receive = datetime.now()
        packet_record = can_transport_interface.receive_packet(timeout=timeout)
        datetime_after_receive = datetime.now()
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.RECEIVED
        assert packet_record.raw_frame_data == tuple(frame.data)
        assert packet_record.addressing_format == addressing_information.addressing_format
        assert packet_record.addressing_type == AddressingType.PHYSICAL
        assert packet_record.can_id == frame.arbitration_id == addressing_information.rx_packets_physical_ai["can_id"]
        assert packet_record.target_address == addressing_information.rx_packets_physical_ai["target_address"]
        assert packet_record.source_address == addressing_information.rx_packets_physical_ai["source_address"]
        assert packet_record.address_extension == addressing_information.rx_packets_physical_ai["address_extension"]
        # performance checks
        assert send_after <= (datetime_after_receive - datetime_before_receive).total_seconds() * 1000. < timeout
        # TODO: sometimes fail because of https://github.com/hardbyte/python-can/issues/1676 - uncomment when resolved
        # assert datetime_before_receive < packet_record.transmission_time < datetime_after_receive

    @pytest.mark.parametrize("addressing_information, frame", [
        (CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x611},
                                  rx_physical={"can_id": 0x612},
                                  tx_functional={"can_id": 0x6FF},
                                  rx_functional={"can_id": 0x6FE}),
         Message(data=[0x02, 0x10, 0x03])),
        (CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B},
                                  tx_functional={"target_address": 0xAC, "source_address": 0xFE},
                                  rx_functional={"target_address": 0xFE, "source_address": 0xAC}),
         Message(data=[0x2C] + list(range(100, 163)), is_fd=True)),
        (CanAddressingInformation(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                  tx_physical={"can_id": 0x987, "target_address": 0x90},
                                  rx_physical={"can_id": 0x987, "target_address": 0xFE},
                                  tx_functional={"can_id": 0x11765, "target_address": 0x5A},
                                  rx_functional={"can_id": 0x11765, "target_address": 0xFF},),
         Message(data=[0xFF, 0x30, 0xAB, 0x7F])),
        (CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x651, "address_extension": 0x87},
                                  rx_physical={"can_id": 0x652, "address_extension": 0xFE},
                                  tx_functional={"can_id": 0x6FF, "address_extension": 0xA5},
                                  rx_functional={"can_id": 0x6FF, "address_extension": 0xFF}, ),
         Message(data=[0xFF, 0x11, 0x23, 0x62, 0x92, 0xD0, 0xB1, 0x00])),
        (CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF, "address_extension": 0x87},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B, "address_extension": 0x87},
                                  tx_functional={"target_address": 0xAC, "source_address": 0xFE, "address_extension": 0xFF},
                                  rx_functional={"target_address": 0xFE, "source_address": 0xAC, "address_extension": 0xFF}, ),
         Message(data=[0xFF, 0x02, 0x3E, 0x80, 0xAA, 0xAA, 0xAA, 0xAA])),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        (1000, 950),  # ms
        (50, 20),
    ])
    def test_receive_packet__functional(self, addressing_information, frame, timeout, send_after):
        # TODO: docstring
        frame.arbitration_id = addressing_information.rx_packets_functional_ai["can_id"]
        # data parameter of `frame` object must be set manually and according to `addressing_format`
        # and `addressing_information`
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.bus1,
                                                          addressing_information=addressing_information)
        Timer(interval=send_after/1000., function=self.bus2.send, args=(frame, )).start()
        datetime_before_receive = datetime.now()
        packet_record = can_transport_interface.receive_packet(timeout=timeout)
        datetime_after_receive = datetime.now()
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.RECEIVED
        assert packet_record.raw_frame_data == tuple(frame.data)
        assert packet_record.addressing_format == addressing_information.addressing_format
        assert packet_record.addressing_type == AddressingType.FUNCTIONAL
        assert packet_record.can_id == frame.arbitration_id == addressing_information.rx_packets_functional_ai["can_id"]
        assert packet_record.target_address == addressing_information.rx_packets_functional_ai["target_address"]
        assert packet_record.source_address == addressing_information.rx_packets_functional_ai["source_address"]
        assert packet_record.address_extension == addressing_information.rx_packets_functional_ai["address_extension"]
        # performance checks
        assert send_after <= (datetime_after_receive - datetime_before_receive).total_seconds() * 1000. < timeout
        # TODO: sometimes fail because of https://github.com/hardbyte/python-can/issues/1676 - uncomment when resolved
        # assert datetime_before_receive < packet_record.transmission_time < datetime_after_receive

    # use cases

    def test_timeout_then_send(self, example_addressing_information):
        # TODO: docstring
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.bus1,
                                                          addressing_information=example_addressing_information)
        uds_message = UdsMessage(payload=[0x3E, 0x00], addressing_type=AddressingType.PHYSICAL)
        packet = can_transport_interface.segmenter.segmentation(uds_message)[0]
        with pytest.raises(TimeoutError):
            can_transport_interface.receive_packet(timeout=100)
        packet_record = can_transport_interface.send_packet(packet)
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.TRANSMITTED

    def test_timeout_then_receive(self, example_addressing_information, example_rx_frame):
        # TODO: docstring
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.bus1,
                                                          addressing_information=example_addressing_information)
        with pytest.raises(TimeoutError):
            can_transport_interface.receive_packet(timeout=100)
        self.bus2.send(example_rx_frame)
        packet_record = can_transport_interface.receive_packet(timeout=100)
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.RECEIVED

    def test_observe_tx_packet(self, example_addressing_information, example_tx_frame, example_tx_uds_message):
        # TODO: docstring
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.bus1,
                                                          addressing_information=example_addressing_information)
        packet = can_transport_interface.segmenter.segmentation(example_tx_uds_message)[0]
        self.bus1.send(example_tx_frame)
        sleep(0.1)
        datetime_before_send = datetime.now()
        packet_record = can_transport_interface.send_packet(packet)
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.TRANSMITTED
        assert packet_record.transmission_time > datetime_before_send


class TestAsyncPythonCanKvaser:
    """System Tests for asynchronous functions of `PyCanTransportInterface` with Kvaser as bus manager."""

    def setup_class(self):
        self.bus1 = Bus(interface="kvaser", channel=0, fd=True, receive_own_messages=True)
        self.bus2 = Bus(interface="kvaser", channel=1, fd=True, receive_own_messages=True)

    def teardown_class(self):
        """Safely close bus objects."""
        self.bus1.shutdown()
        self.bus2.shutdown()

    # async_receive_packet

    @pytest.mark.parametrize("timeout", [1000, 50])
    @pytest.mark.asyncio
    async def test_async_receive_packet__timeout(self, example_addressing_information, timeout):
        # TODO: docstring
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.bus1,
                                                          addressing_information=example_addressing_information)
        time_before_receive = time()
        with pytest.raises((TimeoutError, asyncio.TimeoutError)):
            await can_transport_interface.async_receive_packet(timeout=timeout)
        time_after_receive = time()
        assert timeout < (time_after_receive - time_before_receive) * 1000. < timeout + 25.

    @pytest.mark.parametrize("addressing_information, frame", [
        (CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x611},
                                  rx_physical={"can_id": 0x612},
                                  tx_functional={"can_id": 0x6FF},
                                  rx_functional={"can_id": 0x6FE}),
         Message(data=[0x02, 0x10, 0x03])),
        (CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B},
                                  tx_functional={"target_address": 0xAC, "source_address": 0xFE},
                                  rx_functional={"target_address": 0xFE, "source_address": 0xAC}),
         Message(data=[0x2C] + list(range(100, 163)), is_fd=True)),
        (CanAddressingInformation(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                  tx_physical={"can_id": 0x987, "target_address": 0x90},
                                  rx_physical={"can_id": 0x987, "target_address": 0xFE},
                                  tx_functional={"can_id": 0x11765, "target_address": 0x5A},
                                  rx_functional={"can_id": 0x11765, "target_address": 0xFF}),
         Message(data=[0xFE, 0x30, 0xAB, 0x7F])),
        (CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x651, "address_extension": 0x87},
                                  rx_physical={"can_id": 0x652, "address_extension": 0xFE},
                                  tx_functional={"can_id": 0x6FF, "address_extension": 0xA5},
                                  rx_functional={"can_id": 0x6FF, "address_extension": 0xFF}),
         Message(data=[0xFE, 0x11, 0x23, 0x62, 0x92, 0xD0, 0xB1, 0x00])),
        (CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF, "address_extension": 0x87},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B, "address_extension": 0x87},
                                  tx_functional={"target_address": 0xAC, "source_address": 0xFE, "address_extension": 0xFF},
                                  rx_functional={"target_address": 0xFE, "source_address": 0xAC, "address_extension": 0xFF}),
         Message(data=[0x87, 0x02, 0x3E, 0x80, 0xAA, 0xAA, 0xAA, 0xAA])),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        (1000, 950),  # ms
        (50, 20),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_packet__physical(self, addressing_information, frame, timeout, send_after):
        # TODO: docstring
        async def _send_frame():
            await asyncio.sleep(send_after/1000.)
            self.bus2.send(frame)

        frame.arbitration_id = addressing_information.rx_packets_physical_ai["can_id"]
        # data parameter of `frame` object must be set manually and according to `addressing_format`
        # and `addressing_information`
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.bus1,
                                                          addressing_information=addressing_information)
        future_record = can_transport_interface.async_receive_packet(timeout=timeout)
        datetime_before_receive = datetime.now()
        done_tasks, _ = await asyncio.wait([_send_frame(), future_record])
        datetime_after_receive = datetime.now()
        received_records = tuple(filter(lambda result: isinstance(result, CanPacketRecord),
                                        (done_task.result() for done_task in done_tasks)))
        assert len(received_records) == 1, "CAN Packet was received"
        packet_record = received_records[0]
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.RECEIVED
        assert packet_record.raw_frame_data == tuple(frame.data)
        assert packet_record.addressing_format == addressing_information.addressing_format
        assert packet_record.addressing_type == AddressingType.PHYSICAL
        assert packet_record.can_id == frame.arbitration_id == addressing_information.rx_packets_physical_ai["can_id"]
        assert packet_record.target_address == addressing_information.rx_packets_physical_ai["target_address"]
        assert packet_record.source_address == addressing_information.rx_packets_physical_ai["source_address"]
        assert packet_record.address_extension == addressing_information.rx_packets_physical_ai["address_extension"]
        # performance checks
        assert send_after <= (datetime_after_receive - datetime_before_receive).total_seconds() * 1000. < timeout
        # TODO: sometimes fail because of https://github.com/hardbyte/python-can/issues/1676 - uncomment when resolved
        # assert datetime_before_receive < packet_record.transmission_time < datetime_after_receive

    @pytest.mark.parametrize("addressing_information, frame", [
        (CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x611},
                                  rx_physical={"can_id": 0x612},
                                  tx_functional={"can_id": 0x6FF},
                                  rx_functional={"can_id": 0x6FE}),
         Message(data=[0x02, 0x10, 0x03])),
        (CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B},
                                  tx_functional={"target_address": 0xAC, "source_address": 0xFE},
                                  rx_functional={"target_address": 0xFE, "source_address": 0xAC}),
         Message(data=[0x2C] + list(range(100, 163)), is_fd=True)),
        (CanAddressingInformation(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                  tx_physical={"can_id": 0x987, "target_address": 0x90},
                                  rx_physical={"can_id": 0x987, "target_address": 0xFE},
                                  tx_functional={"can_id": 0x11765, "target_address": 0x5A},
                                  rx_functional={"can_id": 0x11765, "target_address": 0xFF},),
         Message(data=[0xFF, 0x30, 0xAB, 0x7F])),
        (CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x651, "address_extension": 0x87},
                                  rx_physical={"can_id": 0x652, "address_extension": 0xFE},
                                  tx_functional={"can_id": 0x6FF, "address_extension": 0xA5},
                                  rx_functional={"can_id": 0x6FF, "address_extension": 0xFF}, ),
         Message(data=[0xFF, 0x11, 0x23, 0x62, 0x92, 0xD0, 0xB1, 0x00])),
        (CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF, "address_extension": 0x87},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B, "address_extension": 0x87},
                                  tx_functional={"target_address": 0xAC, "source_address": 0xFE, "address_extension": 0xFF},
                                  rx_functional={"target_address": 0xFE, "source_address": 0xAC, "address_extension": 0xFF}, ),
         Message(data=[0xFF, 0x02, 0x3E, 0x80, 0xAA, 0xAA, 0xAA, 0xAA])),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        (1000, 950),  # ms
        (50, 20),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_packet__functional(self, addressing_information, frame, timeout, send_after):
        # TODO: docstring
        async def _send_frame():
            await asyncio.sleep(send_after/1000.)
            self.bus2.send(frame)

        frame.arbitration_id = addressing_information.rx_packets_functional_ai["can_id"]
        # data parameter of `frame` object must be set manually and according to `addressing_format`
        # and `addressing_information`
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.bus1,
                                                          addressing_information=addressing_information)
        future_record = can_transport_interface.async_receive_packet(timeout=timeout)
        datetime_before_receive = datetime.now()
        done_tasks, _ = await asyncio.wait([_send_frame(), future_record])
        datetime_after_receive = datetime.now()
        received_records = tuple(filter(lambda result: isinstance(result, CanPacketRecord),
                                        (done_task.result() for done_task in done_tasks)))
        assert len(received_records) == 1, "CAN Packet was received"
        packet_record = received_records[0]
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.RECEIVED
        assert packet_record.raw_frame_data == tuple(frame.data)
        assert packet_record.addressing_format == addressing_information.addressing_format
        assert packet_record.addressing_type == AddressingType.FUNCTIONAL
        assert packet_record.can_id == frame.arbitration_id == addressing_information.rx_packets_functional_ai["can_id"]
        assert packet_record.target_address == addressing_information.rx_packets_functional_ai["target_address"]
        assert packet_record.source_address == addressing_information.rx_packets_functional_ai["source_address"]
        assert packet_record.address_extension == addressing_information.rx_packets_functional_ai["address_extension"]
        # performance checks
        assert send_after <= (datetime_after_receive - datetime_before_receive).total_seconds() * 1000. < timeout
        # TODO: sometimes fail because of https://github.com/hardbyte/python-can/issues/1676 - uncomment when resolved
        # assert datetime_before_receive < packet_record.transmission_time < datetime_after_receive

    # async_send_packet

    @pytest.mark.parametrize("packet_type, addressing_type, addressing_information, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME,
         AddressingType.FUNCTIONAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x611},
                                  rx_physical={"can_id": 0x612},
                                  tx_functional={"can_id": 0x6FF},
                                  rx_functional={"can_id": 0x6FE}),
         {"filler_byte": 0x1E, "payload": [0x10, 0x04]}),
        (CanPacketType.FIRST_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B},
                                  tx_functional={"target_address": 0xAC, "source_address": 0xFE},
                                  rx_functional={"target_address": 0xFE, "source_address": 0xAC}),
         {"dlc": 8, "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10], "data_length": 0x13}),
        (CanPacketType.CONSECUTIVE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                  tx_physical={"can_id": 0x987, "target_address": 0x90},
                                  rx_physical={"can_id": 0x987, "target_address": 0xFE},
                                  tx_functional={"can_id": 0x11765, "target_address": 0x5A},
                                  rx_functional={"can_id": 0x11765, "target_address": 0xFF}),
         {"payload": [0x32, 0xFF], "sequence_number": 0xF}),
        (CanPacketType.FLOW_CONTROL,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x651, "address_extension": 0x87},
                                  rx_physical={"can_id": 0x652, "address_extension": 0xFE},
                                  tx_functional={"can_id": 0x6FF, "address_extension": 0xA5},
                                  rx_functional={"can_id": 0x6FF, "address_extension": 0xFF}),
         {"dlc": 8, "flow_status": CanFlowStatus.ContinueToSend, "block_size": 0x15, "st_min": 0xFE}),
        (CanPacketType.SINGLE_FRAME,
         AddressingType.PHYSICAL,
         CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF, "address_extension": 0x87},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B, "address_extension": 0x87},
                                  tx_functional={"target_address": 0xAC, "source_address": 0xFE, "address_extension": 0xFF},
                                  rx_functional={"target_address": 0xFE, "source_address": 0xAC, "address_extension": 0xFF}),
         {"filler_byte": 0xBC, "payload": [0x22, 0x12, 0x34, 0x12, 0x56, 0x12, 0x78, 0x12, 0x9A, 0x12, 0xBC], "dlc":0xF}),
    ])
    @pytest.mark.asyncio
    async def test_async_send_packet(self, packet_type, addressing_type, addressing_information, packet_type_specific_kwargs):
        # TODO: docstring
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
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.bus1,
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
        # performance checks
        # TODO: sometimes fail because of https://github.com/hardbyte/python-can/issues/1676 - uncomment when resolved
        # assert datetime_before_send < packet_record.transmission_time < datetime_after_send

    # use cases

    # TODO: multiple packets tests
    # Procedure 1 - timeout at receive then receive another packet
    # Procedure 2 - skip receiving packet, then receive exactly the same one later, make sure timing is good
    # Procedure 3 - send and receive in the same task, make sure both are executed.

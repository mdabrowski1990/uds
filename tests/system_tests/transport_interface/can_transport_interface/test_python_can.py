import pytest
from abc import ABC, abstractmethod
from threading import Timer
from can import Bus, Message
from datetime import datetime, timedelta

from uds.can import CanAddressingInformation, CanAddressingFormat, CanFlowStatus
from uds.transport_interface import PyCanTransportInterface
from uds.transmission_attributes import AddressingType, TransmissionDirection
from uds.packet import CanPacket, AnyCanPacket, CanPacketType, CanPacketRecord


class AbstractTestPyCan(ABC):

    @abstractmethod
    def setup_class(self):
        """Configure `self.bus1` and `self.bus2`. They are supposed to be connected through a termination."""
        self.bus1: Bus
        self.bus2: Bus

    # send_packet

    @pytest.mark.parametrize("packet_type, addressing_type, packet_type_specific_kwargs", [
        (CanPacketType.SINGLE_FRAME, AddressingType.FUNCTIONAL, {"filler_byte": 0x1E, "payload": [0x10, 0x04]}),
        (CanPacketType.FIRST_FRAME, AddressingType.PHYSICAL, {"dlc": 8,
                                                              "payload": [0x22, 0x10, 0x00, 0x10, 0x01, 0x10],
                                                              "data_length": 0x13}),
        (CanPacketType.CONSECUTIVE_FRAME, AddressingType.PHYSICAL, {"payload": [0x32, 0xFF], "sequence_number": 0xF}),
        (CanPacketType.FLOW_CONTROL, AddressingType.PHYSICAL, {"dlc": 8,
                                                               "flow_status": CanFlowStatus.ContinueToSend,
                                                               "block_size": 0x15,
                                                               "st_min": 0xFE}),
    ])
    def test_send_packet__11bit_addressing(self, packet_type, addressing_type, packet_type_specific_kwargs):
        addressing_information = CanAddressingInformation(
            addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
            tx_physical={"can_id": 0x611},
            rx_physical={"can_id": 0x612},
            tx_functional={"can_id": 0x6FF},
            rx_functional={"can_id": 0x6FE},
        )
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.bus1,
                                                          addressing_information=addressing_information)
        packet = CanPacket(packet_type=packet_type,
                           addressing_format=addressing_information.addressing_format,
                           addressing_type=addressing_type,
                           can_id=addressing_information.tx_packets_physical_ai["can_id"]
                           if addressing_type == AddressingType.PHYSICAL else
                           addressing_information.tx_packets_functional_ai["can_id"],
                           **packet_type_specific_kwargs)
        datetime_before_send = datetime.now()
        packet_record = can_transport_interface.send_packet(packet)
        datetime_after_send = datetime.now()
        assert isinstance(packet_record, CanPacketRecord)
        assert datetime_before_send < packet_record.transmission_time < datetime_after_send
        assert packet_record.direction == TransmissionDirection.TRANSMITTED
        assert packet_record.raw_frame_data == packet.raw_frame_data
        assert packet_record.can_id == packet.can_id
        assert packet_record.packet_type == packet.packet_type
        assert packet_record.addressing_format == packet.addressing_format == addressing_information.addressing_format
        assert packet_record.addressing_type == packet.addressing_type == addressing_type
        assert packet_record.target_address is packet.target_address is None
        assert packet_record.source_address is packet.source_address is None
        assert packet_record.address_extension is packet.address_extension is None

    # TODO: more addressings

    # receive_packet

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
         Message(data=[0xFE, 0x30, 0xAB, 0x7F])),
        (CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                  tx_physical={"can_id": 0x651, "address_extension": 0x87},
                                  rx_physical={"can_id": 0x652, "address_extension": 0xFE},
                                  tx_functional={"can_id": 0x6FF, "address_extension": 0xA5},
                                  rx_functional={"can_id": 0x6FF, "address_extension": 0xFF}, ),
         Message(data=[0xFE, 0x11, 0x23, 0x62, 0x92, 0xD0, 0xB1, 0x00])),
        (CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                  tx_physical={"target_address": 0x1B, "source_address": 0xFF, "address_extension": 0x87},
                                  rx_physical={"target_address": 0xFF, "source_address": 0x1B, "address_extension": 0x87},
                                  tx_functional={"target_address": 0xAC, "source_address": 0xFE, "address_extension": 0xFF},
                                  rx_functional={"target_address": 0xFE, "source_address": 0xAC, "address_extension": 0xFF}, ),
         Message(data=[0x87, 0x02, 0x3E, 0x80, 0xAA, 0xAA, 0xAA, 0xAA])),
    ])
    @pytest.mark.parametrize("timeout, send_after", [
        (1000, 950),  # ms
        (30, 1),
    ])
    def test_receive_packet__physical_receive(self, addressing_information, frame, timeout, send_after):
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
        assert datetime_before_receive < packet_record.transmission_time < datetime_after_receive
        assert packet_record.direction == TransmissionDirection.RECEIVED
        assert packet_record.raw_frame_data == tuple(frame.data)
        assert packet_record.can_id == frame.arbitration_id == addressing_information.rx_packets_physical_ai["can_id"]
        assert packet_record.addressing_format == addressing_information.addressing_format
        assert packet_record.addressing_type == AddressingType.PHYSICAL
        assert packet_record.target_address == addressing_information.rx_packets_physical_ai["target_address"]
        assert packet_record.source_address == addressing_information.rx_packets_physical_ai["source_address"]
        assert packet_record.address_extension == addressing_information.rx_packets_physical_ai["address_extension"]

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
        (30, 1),
    ])
    def test_receive_packet__functional_receive(self, addressing_information, frame, timeout, send_after):
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
        assert datetime_before_receive < packet_record.transmission_time < datetime_after_receive
        assert packet_record.direction == TransmissionDirection.RECEIVED
        assert packet_record.raw_frame_data == tuple(frame.data)
        assert packet_record.can_id == frame.arbitration_id == addressing_information.rx_packets_functional_ai["can_id"]
        assert packet_record.addressing_format == addressing_information.addressing_format
        assert packet_record.addressing_type == AddressingType.FUNCTIONAL
        assert packet_record.target_address == addressing_information.rx_packets_functional_ai["target_address"]
        assert packet_record.source_address == addressing_information.rx_packets_functional_ai["source_address"]
        assert packet_record.address_extension == addressing_information.rx_packets_functional_ai["address_extension"]

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
        (10, 15),
    ])
    def test_receive_packet__timeout(self, addressing_information, addressing_type, frame, timeout, send_after):
        if addressing_type == AddressingType.PHYSICAL:
            frame.arbitration_id = addressing_information.rx_packets_physical_ai["can_id"]
        else:
            frame.arbitration_id = addressing_information.rx_packets_functional_ai["can_id"]
        # data parameter of `frame` object must be set manually and according to `addressing_format`
        # and `addressing_information`
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.bus1,
                                                          addressing_information=addressing_information)
        Timer(interval=send_after/1000., function=self.bus2.send, args=(frame,)).start()
        with pytest.raises(TimeoutError):
            can_transport_interface.receive_packet(timeout=timeout)

    # async_receive_packet

    # TODO: test

    # async_send_packet

    # TODO: test


class TestPythonCanKvaser(AbstractTestPyCan):
    """System Tests for `PyCanTransportInterface` with Kvaser as bus manager."""

    def setup_class(self):
        self.bus1 = Bus(interface="kvaser", channel=0, fd=True, receive_own_messages=True)
        self.bus2 = Bus(interface="kvaser", channel=1, fd=True, receive_own_messages=True)

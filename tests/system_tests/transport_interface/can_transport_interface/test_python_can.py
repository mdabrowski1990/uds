import asyncio
from datetime import datetime
from threading import Timer
from time import sleep, time

import pytest

from can import Bus, Message
from uds.can import CanAddressingFormat, CanAddressingInformation, CanFlowStatus
from uds.message import UdsMessage
from uds.packet import CanPacket, CanPacketRecord, CanPacketType
from uds.transmission_attributes import AddressingType, TransmissionDirection
from uds.transport_interface import PyCanTransportInterface


class TestPythonCanKvaser:
    """
    System Tests for `PyCanTransportInterface` with Kvaser as bus manager.

    Hardware setup:
        - two Kvaser interfaces (either https://www.kvaser.com/products-services/our-products/#/?pc_int=usb)
          connected with each in the same CAN bus (do not forget about CAN termination)
    """

    TASK_TIMING_TOLERANCE = 30.  # ms

    def setup_class(self):
        self.can_interface_1 = Bus(interface="kvaser", channel=0, fd=True, receive_own_messages=True)
        self.can_interface_2 = Bus(interface="kvaser", channel=1, fd=True, receive_own_messages=True)

    def setup_method(self):
        self.can_interface_1.flush_tx_buffer()
        self.can_interface_2.flush_tx_buffer()

    def teardown_class(self):
        """Safely close bus objects."""
        self.can_interface_1.shutdown()
        self.can_interface_2.shutdown()

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
        """
        Check for simple sending of a CAN packet.

        Procedure:
        1. Send CAN packet via Transport Interface.
            Expected: CAN packet record returned.
        2. Validate transmitted CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the transmitted CAN packet.

        :param packet_type: Type of CAN Packet to send.
        :param addressing_type: Addressing type to use for transmitting a CAN packet.
        :param addressing_information: Example Addressing Information of a CAN Node.
        :param packet_type_specific_kwargs: Parameters specific for this CAN Packet type.
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
        # performance checks
        # TODO: https://github.com/mdabrowski1990/uds/issues/228 - uncomment when resolved
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
        """
        Check for a timeout during packet receiving.

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frame that carries received CAN packet.
        2. Call method to receive packet via Transport Interface with timeout set just before CAN packet reaches CAN bus.
            Expected: Timeout exception is raised.

        :param addressing_type: Addressing type to use for transmitting a CAN packet.
        :param addressing_information: Example Addressing Information of CAN Node.
        :param frame: CAN frame to send (must be decoded as UDS CAN Packet).
        :param timeout: Timeout to pass to receive method [ms].
        :param send_after: Time when to send CAN frame after call of receive method [ms].
        """
        if addressing_type == AddressingType.PHYSICAL:
            frame.arbitration_id = addressing_information.rx_packets_physical_ai["can_id"]
        else:
            frame.arbitration_id = addressing_information.rx_packets_functional_ai["can_id"]
        # data parameter of `frame` object must be set manually and according to `addressing_format`
        # and `addressing_information`
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=addressing_information)
        Timer(interval=send_after/1000., function=self.can_interface_2.send, args=(frame,)).start()
        time_before_receive = time()
        with pytest.raises(TimeoutError):
            can_transport_interface.receive_packet(timeout=timeout)
        time_after_receive = time()
        assert timeout < (time_after_receive - time_before_receive) * 1000. < timeout + self.TASK_TIMING_TOLERANCE

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
        """
        Check for a simple CAN packet (physically addressed) receiving.

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frame that carries received CAN packet.
        2. Call method to receive packet via Transport Interface with timeout set just after CAN packet reaches CAN bus.
            Expected: CAN packet is received.
        3. Validate received CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the received CAN packet.

        :param addressing_information: Example Addressing Information of CAN Node.
        :param frame: CAN frame to send (must be decoded as UDS CAN Packet).
        :param timeout: Timeout to pass to receive method [ms].
        :param send_after: Time when to send CAN frame after call of receive method [ms].
        """
        frame.arbitration_id = addressing_information.rx_packets_physical_ai["can_id"]
        # data parameter of `frame` object must be set manually and according to `addressing_format`
        # and `addressing_information`
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=addressing_information)
        Timer(interval=send_after/1000., function=self.can_interface_2.send, args=(frame,)).start()
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
        # TODO: https://github.com/mdabrowski1990/uds/issues/228 - uncomment when resolved
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
        """
        Check for a simple CAN packet (functionally addressed) receiving.

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frame that carries received CAN packet.
        2. Call method to receive packet via Transport Interface with timeout set just after CAN packet reaches CAN bus.
            Expected: CAN packet is received.
        3. Validate received CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the received CAN packet.

        :param addressing_information: Example Addressing Information of CAN Node.
        :param frame: CAN frame to send (must be decoded as UDS CAN Packet).
        :param timeout: Timeout to pass to receive method [ms].
        :param send_after: Time when to send CAN frame after call of receive method [ms].
        """
        frame.arbitration_id = addressing_information.rx_packets_functional_ai["can_id"]
        # data parameter of `frame` object must be set manually and according to `addressing_format`
        # and `addressing_information`
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=addressing_information)
        Timer(interval=send_after/1000., function=self.can_interface_2.send, args=(frame,)).start()
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
        # TODO: https://github.com/mdabrowski1990/uds/issues/228 - uncomment when resolved
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
        """
        Check for simple asynchronous sending of a CAN packet.

        Procedure:
        1. Send (using async method) a CAN packet via Transport Interface.
            Expected: CAN packet record returned.
        2. Validate transmitted CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the transmitted CAN packet.

        :param packet_type: Type of CAN Packet to send.
        :param addressing_type: Addressing type to use for transmitting a CAN packet.
        :param addressing_information: Example Addressing Information of a CAN Node.
        :param packet_type_specific_kwargs: Parameters specific for this CAN Packet type.
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
        # performance checks
        # TODO: https://github.com/mdabrowski1990/uds/issues/228 - uncomment when resolved
        # assert datetime_before_send < packet_record.transmission_time < datetime_after_send

    # async_receive_packet

    @pytest.mark.parametrize("timeout", [1000, 50])
    @pytest.mark.asyncio
    async def test_async_receive_packet__timeout(self, example_addressing_information, timeout):
        """
        Check for a timeout during packet asynchronous receiving.

        Procedure:
        1. Call async method to receive packet via Transport Interface with timeout set just before CAN packet reaches CAN bus.
            Expected: Timeout exception is raised.

        :param example_addressing_information: Example Addressing Information of a CAN Node.
        :param timeout: Timeout to pass to receive method [ms].
        """
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=example_addressing_information)
        time_before_receive = time()
        with pytest.raises((TimeoutError, asyncio.TimeoutError)):
            await can_transport_interface.async_receive_packet(timeout=timeout)
        time_after_receive = time()
        assert timeout < (time_after_receive - time_before_receive) * 1000. < timeout + self.TASK_TIMING_TOLERANCE

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
        """
        Check for a simple asynchronous CAN packet (physically addressed) receiving.

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frame that carries received CAN packet.
        2. Call async method to receive packet via Transport Interface with timeout set just after CAN packet reaches CAN bus.
            Expected: CAN packet is received.
        3. Validate received CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the received CAN packet.

        :param addressing_information: Example Addressing Information of CAN Node.
        :param frame: CAN frame to send (must be decoded as UDS CAN Packet).
        :param timeout: Timeout to pass to receive method [ms].
        :param send_after: Time when to send CAN frame after call of receive method [ms].
        """
        async def _send_frame():
            await asyncio.sleep(send_after/1000.)
            self.can_interface_2.send(frame)

        frame.arbitration_id = addressing_information.rx_packets_physical_ai["can_id"]
        # data parameter of `frame` object must be set manually and according to `addressing_format`
        # and `addressing_information`
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
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
        # TODO: https://github.com/mdabrowski1990/uds/issues/228 - uncomment when resolved
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
        """
        Check for a simple asynchronous CAN packet (functionally addressed) receiving.

        Procedure:
        1. Schedule transmission (using second CAN interface) of a CAN frame that carries received CAN packet.
        2. Call async method to receive packet via Transport Interface with timeout set just after CAN packet reaches CAN bus.
            Expected: CAN packet is received.
        3. Validate received CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the received CAN packet.

        :param addressing_information: Example Addressing Information of CAN Node.
        :param frame: CAN frame to send (must be decoded as UDS CAN Packet).
        :param timeout: Timeout to pass to receive method [ms].
        :param send_after: Time when to send CAN frame after call of receive method [ms].
        """
        async def _send_frame():
            await asyncio.sleep(send_after/1000.)
            self.can_interface_2.send(frame)

        frame.arbitration_id = addressing_information.rx_packets_functional_ai["can_id"]
        # data parameter of `frame` object must be set manually and according to `addressing_format`
        # and `addressing_information`
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
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
        # TODO: https://github.com/mdabrowski1990/uds/issues/228 - uncomment when resolved
        # assert datetime_before_receive < packet_record.transmission_time < datetime_after_receive

    # use cases

    @pytest.mark.parametrize("payload, addressing_type", [
        ([0x22, 0x10, 0xF5], AddressingType.PHYSICAL),
        ([0x3E, 0x80], AddressingType.FUNCTIONAL),
    ])
    def test_send_on_one_receive_on_other_bus(self, example_addressing_information,
                                              example_addressing_information_2nd_node,
                                              payload, addressing_type):
        """
        Check for sending and receiving CAN Packet using two Transport Interfaces.

        Procedure:
        1. Send a CAN Packet using Transport Interface 1 (via CAN Interface 1).
            Expected: CAN packet record returned.
        2. Receive a CAN Packet using Transport Interface 2 (via CAN Interface 2).
            Expected: CAN packet is received.
        3. Validate received CAN packet records attributes.
            Expected: Attributes of CAN packet records are in line with each other
                (the same packet was received and transmitted).

        :param example_addressing_information: Addressing Information for a receiving CAN Node.
        :param example_addressing_information_2nd_node: Addressing Information for a transmitting CAN Node.
            It is compatible with `example_addressing_information`.
        :param payload: Payload of CAN Message to send.
        :param addressing_type: Addressing Type of CAN Message to send.
        """
        can_transport_interface_1 = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                            addressing_information=example_addressing_information)
        can_transport_interface_2 = PyCanTransportInterface(can_bus_manager=self.can_interface_2,
                                                            addressing_information=example_addressing_information_2nd_node)
        uds_message = UdsMessage(payload=payload, addressing_type=addressing_type)
        packet = can_transport_interface_2.segmenter.segmentation(uds_message)[0]

        sent_packet_record = can_transport_interface_2.send_packet(packet)
        received_packet_record = can_transport_interface_1.receive_packet(timeout=100)
        assert isinstance(sent_packet_record, CanPacketRecord)
        assert isinstance(received_packet_record, CanPacketRecord)
        assert sent_packet_record.direction == TransmissionDirection.TRANSMITTED
        assert received_packet_record.direction == TransmissionDirection.RECEIVED
        assert sent_packet_record.addressing_format == received_packet_record.addressing_format
        assert sent_packet_record.can_id == received_packet_record.can_id
        assert sent_packet_record.raw_frame_data == received_packet_record.raw_frame_data
        assert sent_packet_record.addressing_type == received_packet_record.addressing_type

    @pytest.mark.parametrize("payload, addressing_type", [
        ([0x22, 0x10, 0xF5], AddressingType.PHYSICAL),
        ([0x3E, 0x80], AddressingType.FUNCTIONAL),
    ])
    @pytest.mark.asyncio
    async def test_async_send_on_one_receive_on_other_bus(self, example_addressing_information,
                                                          example_addressing_information_2nd_node,
                                                          payload, addressing_type):
        """
        Check for asynchronous sending and receiving CAN Packet using two Transport Interfaces.

        Procedure:
        1. Send (using async method) a CAN Packet using Transport Interface 1 (via CAN Interface 1).
            Expected: CAN packet record returned.
        2. Receive (using async method) a CAN Packet using Transport Interface 2 (via CAN Interface 2).
            Expected: CAN packet is received.
        3. Validate received CAN packet records attributes.
            Expected: Attributes of CAN packet records are in line with each other
                (the same packet was received and transmitted).

        :param example_addressing_information: Addressing Information for a receiving CAN Node.
        :param example_addressing_information_2nd_node: Addressing Information for a transmitting CAN Node.
            It is compatible with `example_addressing_information`.
        :param payload: Payload of CAN Message to send.
        :param addressing_type: Addressing Type of CAN Message to send.
        """
        can_transport_interface_1 = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                            addressing_information=example_addressing_information)
        can_transport_interface_2 = PyCanTransportInterface(can_bus_manager=self.can_interface_2,
                                                            addressing_information=example_addressing_information_2nd_node)
        uds_message = UdsMessage(payload=payload, addressing_type=addressing_type)
        packet = can_transport_interface_2.segmenter.segmentation(uds_message)[0]
        done_tasks, _ = await asyncio.wait([can_transport_interface_2.async_send_packet(packet),
                                            can_transport_interface_1.async_receive_packet(timeout=100)])
        packet_record_1, packet_record_2 = [done_task.result() for done_task in done_tasks]
        assert isinstance(packet_record_1, CanPacketRecord) and isinstance(packet_record_2, CanPacketRecord)
        assert {packet_record_1.direction, packet_record_2.direction} \
               == {TransmissionDirection.TRANSMITTED, TransmissionDirection.RECEIVED}
        assert packet_record_1.addressing_format == packet_record_2.addressing_format
        assert packet_record_1.can_id == packet_record_2.can_id
        assert packet_record_1.raw_frame_data == packet_record_2.raw_frame_data
        assert packet_record_1.addressing_type == packet_record_2.addressing_type

    # error guessing

    @pytest.mark.parametrize("payload, addressing_type", [
        ([0x62, 0x10, 0xF5, 0x12, 0x34, 0xF0], AddressingType.PHYSICAL),
        ([0x10, 0x81], AddressingType.FUNCTIONAL),
    ])
    def test_timeout_then_send(self, example_addressing_information, payload, addressing_type):
        """
        Check for sending a CAN Packet after a timeout exception during receiving.

        Procedure:
        1. Call method to receive packet via Transport Interface.
            Expected: Timeout exception is raised.
        2. Send a CAN packet via Transport Interface.
            Expected: CAN packet record returned.
        3. Validate transmitted CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the transmitted CAN packet.

        :param example_addressing_information: Example Addressing Information of a CAN Node.
        :param payload: Payload of CAN Message to send.
        :param addressing_type: Addressing Type of CAN Message to send.
        """
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=example_addressing_information)
        uds_message = UdsMessage(payload=payload, addressing_type=addressing_type)
        packet = can_transport_interface.segmenter.segmentation(uds_message)[0]
        with pytest.raises(TimeoutError):
            can_transport_interface.receive_packet(timeout=100)
        packet_record = can_transport_interface.send_packet(packet)
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.TRANSMITTED
        assert packet_record.addressing_type == packet.addressing_type == addressing_type
        assert packet_record.raw_frame_data == packet.raw_frame_data
        assert packet_record.payload == packet.payload == tuple(payload)
        assert packet_record.can_id == packet.can_id

    @pytest.mark.parametrize("payload, addressing_type", [
        ([0x62, 0x10, 0xF5, 0x12, 0x34, 0xF0], AddressingType.PHYSICAL),
        ([0x10, 0x81], AddressingType.FUNCTIONAL),
    ])
    @pytest.mark.asyncio
    async def test_async_timeout_then_send(self, example_addressing_information, payload, addressing_type):
        """
        Check for asynchronous sending a CAN Packet after a timeout exception during asynchronous receiving.

        Procedure:
        1. Call async method to receive packet via Transport Interface.
            Expected: Timeout exception is raised.
        2. Send (using async method) a CAN packet via Transport Interface.
            Expected: CAN packet record returned.
        3. Validate transmitted CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the transmitted CAN packet.

        :param example_addressing_information: Example Addressing Information of a CAN Node.
        :param payload: Payload of CAN Message to send.
        :param addressing_type: Addressing Type of CAN Message to send.
        """
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=example_addressing_information)
        uds_message = UdsMessage(payload=payload, addressing_type=addressing_type)
        packet = can_transport_interface.segmenter.segmentation(uds_message)[0]
        with pytest.raises((TimeoutError, asyncio.TimeoutError)):
            await can_transport_interface.async_receive_packet(timeout=100)
        packet_record = await can_transport_interface.async_send_packet(packet)
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.TRANSMITTED
        assert packet_record.addressing_type == packet.addressing_type == addressing_type
        assert packet_record.raw_frame_data == packet.raw_frame_data
        assert packet_record.payload == packet.payload == tuple(payload)
        assert packet_record.can_id == packet.can_id

    def test_timeout_then_receive(self, example_addressing_information, example_rx_frame):
        """
        Check for receiving a CAN Packet after a timeout exception during receiving.

        Procedure:
        1. Call method to receive packet via Transport Interface.
            Expected: Timeout exception is raised.
        2. Send a CAN frame that carries CAN packet targeting configured CAN Node.
        3. Call method to receive packet via Transport Interface.
            Expected: CAN packet is received.
        4. Validate received CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the received CAN packet.

        :param example_addressing_information: Example Addressing Information of a CAN Node.
        :param example_rx_frame: Example CAN frame that shall be recognized as a CAN packet.
        """
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=example_addressing_information)
        with pytest.raises(TimeoutError):
            can_transport_interface.receive_packet(timeout=100)
        datetime_before_send = datetime.now()
        self.can_interface_2.send(example_rx_frame)
        packet_record = can_transport_interface.receive_packet(timeout=100)
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.RECEIVED
        assert packet_record.transmission_time > datetime_before_send

    @pytest.mark.asyncio
    async def test_async_timeout_then_receive(self, example_addressing_information, example_rx_frame):
        """
        Check for asynchronous receiving a CAN Packet after a timeout exception during receiving.

        Procedure:
        1. Call async method to receive packet via Transport Interface.
            Expected: Timeout exception is raised.
        2. Send a CAN frame that carries CAN packet targeting configured CAN Node.
        3. Call async method to receive packet via Transport Interface.
            Expected: CAN packet is received.
        4. Validate received CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the received CAN packet.

        :param example_addressing_information: Example Addressing Information of a CAN Node.
        :param example_rx_frame: Example CAN frame that shall be recognized as a CAN packet.
        """
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=example_addressing_information)
        with pytest.raises((TimeoutError, asyncio.TimeoutError)):
            await can_transport_interface.async_receive_packet(timeout=100)
        datetime_before_send = datetime.now()
        self.can_interface_2.send(example_rx_frame)
        packet_record = await can_transport_interface.async_receive_packet(timeout=100)
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.RECEIVED
        assert packet_record.transmission_time > datetime_before_send

    def test_observe_tx_packet(self, example_addressing_information, example_tx_frame, example_tx_uds_message):
        """
        Check for transmitting a CAN Packet after a sending identical CAN frame.

        Procedure:
        1. Send a CAN frame (which is identical to a future CAN packet) directly using CAN interface.
        2. Send a CAN packet via Transport Interface.
            Expected: CAN packet record returned.
        2. Validate transmitted CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the transmitted CAN packet.
                Make sure timing confirms that it is packet transmitted in step two.

        :param example_addressing_information: Example Addressing Information of a CAN Node.
        :param example_tx_frame: Example CAN frame that shall be recognized as a CAN packet.
        :param example_tx_uds_message: CAN Message carried by CAN packet in example_tx_frame.
        """
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=example_addressing_information)
        packet = can_transport_interface.segmenter.segmentation(example_tx_uds_message)[0]
        self.can_interface_1.send(example_tx_frame)
        sleep(0.1)
        datetime_before_send = datetime.now()
        packet_record = can_transport_interface.send_packet(packet)
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.TRANSMITTED
        assert packet_record.raw_frame_data == packet.raw_frame_data == tuple(example_tx_frame.data)
        assert packet_record.payload == packet.payload
        assert packet_record.can_id == packet.can_id == example_tx_frame.arbitration_id
        assert packet_record.transmission_time > datetime_before_send

    @pytest.mark.asyncio
    async def test_async_observe_tx_packet(self, example_addressing_information, example_tx_frame, example_tx_uds_message):
        """
        Check for asynchronous transmitting a CAN Packet after a sending identical CAN frame.

        Procedure:
        1. Send a CAN frame (which is identical to a future CAN packet) directly using CAN interface.
        2. Send (using async method) a CAN packet via Transport Interface.
            Expected: CAN packet record returned.
        2. Validate transmitted CAN packet record attributes.
            Expected: Attributes of CAN packet record are in line with the transmitted CAN packet.
                Make sure timing confirms that it is packet transmitted in step two.

        :param example_addressing_information: Example Addressing Information of a CAN Node.
        :param example_tx_frame: Example CAN frame that shall be recognized as a CAN packet.
        :param example_tx_uds_message: CAN Message carried by CAN packet in example_tx_frame.
        """
        can_transport_interface = PyCanTransportInterface(can_bus_manager=self.can_interface_1,
                                                          addressing_information=example_addressing_information)
        packet = can_transport_interface.segmenter.segmentation(example_tx_uds_message)[0]
        self.can_interface_1.send(example_tx_frame)
        sleep(0.1)
        datetime_before_send = datetime.now()
        packet_record = await can_transport_interface.async_send_packet(packet)
        assert isinstance(packet_record, CanPacketRecord)
        assert packet_record.direction == TransmissionDirection.TRANSMITTED
        assert packet_record.raw_frame_data == packet.raw_frame_data
        assert packet_record.payload == packet.payload
        assert packet_record.can_id == packet.can_id
        assert packet_record.transmission_time > datetime_before_send

from can import Bus
from uds.can import CanAddressingFormat, CanAddressingInformation
from uds.message import UdsMessage
from uds.transmission_attributes import AddressingType
from uds.transport_interface import PyCanTransportInterface


def main():
    # configure CAN interfaces
    kvaser_interface_1 = Bus(interface="kvaser", channel=0, fd=True, receive_own_messages=True)  # receiving
    kvaser_interface_2 = Bus(interface="kvaser", channel=1, fd=True, receive_own_messages=True)  # sending

    # configure Addressing Information of a CAN Nodes (example values)
    ai_receive = CanAddressingInformation(
        addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
        tx_physical={"can_id": 0x611},
        rx_physical={"can_id": 0x612},
        tx_functional={"can_id": 0x6FF},
        rx_functional={"can_id": 0x6FE})
    ai_send = ai_receive.get_other_end()

    # create Transport Interface objects for UDS communication
    can_ti_1 = PyCanTransportInterface(can_bus_manager=kvaser_interface_1,
                                       addressing_information=ai_receive)
    can_ti_2 = PyCanTransportInterface(can_bus_manager=kvaser_interface_2,
                                       addressing_information=ai_send)

    # define UDS Messages to send
    message = UdsMessage(addressing_type=AddressingType.PHYSICAL, payload=[0x10, 0x03])

    # create CAN packets that carries those UDS Messages
    packet = can_ti_2.segmenter.segmentation(message)[0]

    # send and receive packet CAN packet
    sent_packet_record = can_ti_2.send_packet(packet)
    print(sent_packet_record)
    received_packet_record = can_ti_1.receive_packet(timeout=100)
    print(received_packet_record)

    # close connections with CAN interfaces
    del can_ti_1
    del can_ti_2
    kvaser_interface_1.shutdown()
    kvaser_interface_2.shutdown()


if __name__ == "__main__":
    main()

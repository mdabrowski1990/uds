from threading import Timer

from can import Bus, Message
from uds.can import CanAddressingFormat, CanAddressingInformation
from uds.transport_interface import PyCanTransportInterface


def main():
    # configure CAN interfaces
    kvaser_interface_1 = Bus(interface="kvaser", channel=0, fd=True, receive_own_messages=True)  # receiving
    kvaser_interface_2 = Bus(interface="kvaser", channel=1, fd=True, receive_own_messages=True)  # sending

    # configure Addressing Information of a CAN Node (example values)
    addressing_information = CanAddressingInformation(
        addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
        tx_physical={"can_id": 0x611},
        rx_physical={"can_id": 0x612},
        tx_functional={"can_id": 0x6FF},
        rx_functional={"can_id": 0x6FE})

    # create Transport Interface object for UDS communication
    can_ti = PyCanTransportInterface(can_bus_manager=kvaser_interface_1,
                                     addressing_information=addressing_information)

    # some frames to be received later on
    frame_1 = Message(arbitration_id=0x6FE, data=[0x02, 0x10, 0x03])
    frame_2 = Message(arbitration_id=0x611, data=[0x02, 0x10, 0x03])  # shall be ignored, as it is not observed CAN ID
    frame_3 = Message(arbitration_id=0x612, data=[0x02, 0x3E, 0x00, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA])

    # receive CAN packet 1
    Timer(interval=0.1, function=kvaser_interface_1.send, args=(frame_1,)).start()  # schedule transmission of frame 1
    record_1 = can_ti.receive_packet(timeout=1000)  # receive CAN packet 1 carried by frame 1
    print(record_1)  # show attributes of CAN packet record 1

    # receive CAN packet 2
    Timer(interval=0.1, function=kvaser_interface_1.send, args=(frame_2,)).start()  # schedule transmission of frame 2
    Timer(interval=0.2, function=kvaser_interface_1.send, args=(frame_3,)).start()  # schedule transmission of frame 3
    record_2 = can_ti.receive_packet(timeout=1000)  # receive CAN packet 2 carried by frame 3
    print(record_2)  # show attributes of CAN packet record 2

    # close connections with CAN interfaces
    del can_ti
    kvaser_interface_1.shutdown()
    kvaser_interface_2.shutdown()


if __name__ == "__main__":
    main()

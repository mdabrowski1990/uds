from pprint import pprint
from threading import Timer

from can import Bus, Message
from uds.transport_interface import PyCanTransportInterface
from uds.can import CanAddressingInformation, CanAddressingFormat

kvaser_bus = Bus(interface="kvaser", channel=0, fd=True, receive_own_messages=True)
kvaser_bus2 = Bus(interface="kvaser", channel=1, fd=True, receive_own_messages=True)

example_addressing_information = CanAddressingInformation(
    addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
    tx_physical={"can_id": 0x611},
    rx_physical={"can_id": 0x612},
    tx_functional={"can_id": 0x6FF},
    rx_functional={"can_id": 0x6FE},
)
can_ti = PyCanTransportInterface(can_bus_manager=kvaser_bus,
                                 addressing_information=example_addressing_information)

frame_1 = Message(arbitration_id=0x6FE, data=[0x10, 0x03])
frame_2 = Message(arbitration_id=0x611, data=[0x10, 0x03])  # shall be ignored, as it is not observed CAN ID
frame_3 = Message(arbitration_id=0x612, data=[0x3E, 0x00, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA])


def main():
    Timer(interval=0.1, function=kvaser_bus.send, args=(frame_1, )).run()
    record_1 = can_ti.receive_packet(timeout=1000)
    pprint(record_1.__dict__)

    Timer(interval=0.3, function=kvaser_bus.send, args=(frame_2, )).run()
    Timer(interval=0.8, function=kvaser_bus.send, args=(frame_3, )).run()
    record_2 = can_ti.receive_packet(timeout=1000)
    pprint(record_2.__dict__)


if __name__ == "__main__":
    main()

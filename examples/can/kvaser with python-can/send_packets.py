from pprint import pprint

from can import Bus
from uds.transport_interface import PyCanTransportInterface
from uds.can import CanAddressingInformation, CanAddressingFormat
from uds.message import UdsMessage
from uds.transmission_attributes import AddressingType

kvaser_bus = Bus(interface="kvaser", channel=0, fd=True, receive_own_messages=True)
example_addressing_information = CanAddressingInformation(
    addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
    tx_physical={"can_id": 0x611},
    rx_physical={"can_id": 0x612},
    tx_functional={"can_id": 0x6FF},
    rx_functional={"can_id": 0x6FE},
)
can_ti = PyCanTransportInterface(can_bus_manager=kvaser_bus,
                                 addressing_information=example_addressing_information)

message_1 = UdsMessage(addressing_type=AddressingType.PHYSICAL, payload=[0x10, 0x03])
message_2 = UdsMessage(addressing_type=AddressingType.FUNCTIONAL, payload=[0x3E])

packet_1 = can_ti.segmenter.segmentation(message_1)[0]
packet_2 = can_ti.segmenter.segmentation(message_2)[0]


def main():
    record_1 = can_ti.send_packet(packet_1)
    record_2 = can_ti.send_packet(packet_2)

    pprint(record_1.__dict__)
    pprint(record_2.__dict__)


if __name__ == "__main__":
    main()

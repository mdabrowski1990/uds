from pprint import pprint
import asyncio

from can import Bus, Message
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

kvaser_bus.send(Message(arbitration_id=0x611, data=list(range(8))))
sent_record_1 = can_ti.send_packet(packet=packet_1)
kvaser_bus.send(Message(arbitration_id=0x6FF, data=[0x01, 0x3E]))
sent_record_2 = can_ti.send_packet(packet=packet_2)

pprint(sent_record_1.__dict__)
pprint(sent_record_2.__dict__)

# kvaser_bus.send(Message(arbitration_id=0x612, data=list(range(8))))
# kvaser_bus.send(Message(arbitration_id=0x6FE, data=[0x01, 0x3E]))
# received_record_1 = asyncio.run(can_ti.receive_packet())
# received_record_2 = asyncio.run(can_ti.receive_packet())
#
# pprint(received_record_1.__dict__)
# pprint(received_record_2.__dict__)

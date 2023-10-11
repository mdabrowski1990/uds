import asyncio
from pprint import pprint

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


async def main():
    r1 = can_ti.async_receive_packet(timeout=1000)
    kvaser_bus2.send(frame_1)
    record_1 = await r1
    pprint(record_1.__dict__)

    r2 = can_ti.async_receive_packet(timeout=1000)
    kvaser_bus2.send(frame_2)
    kvaser_bus2.send(frame_3)
    record_2 = await r2
    pprint(record_2.__dict__)

    kvaser_bus.shutdown()
    kvaser_bus2.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

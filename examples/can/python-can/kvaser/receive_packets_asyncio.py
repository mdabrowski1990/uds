import asyncio
from pprint import pprint

from can import Bus, Message
from uds.can import CanAddressingFormat, CanAddressingInformation
from uds.transport_interface import PyCanTransportInterface


async def main():
    # configure CAN interfaces
    kvaser_interface_1 = Bus(interface="kvaser", channel=0, fd=True, receive_own_messages=True)
    kvaser_interface_2 = Bus(interface="kvaser", channel=1, fd=True, receive_own_messages=True)

    # configure Addressing Information of a CAN Node
    addressing_information = CanAddressingInformation(
        addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
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
    kvaser_interface_2.send(frame_1)  # transmit CAN Frame 1
    record_1 = await can_ti.async_receive_packet(timeout=1000)   # receive CAN packet 1 carried by frame 1
    pprint(record_1.__dict__)  # show attributes of CAN packet record 1

    # receive CAN packet 2
    kvaser_interface_2.send(frame_2)  # transmit CAN Frame 2
    kvaser_interface_2.send(frame_3)  # transmit CAN Frame 3
    record_2 = await can_ti.async_receive_packet(timeout=1000)
    pprint(record_2.__dict__)  # show attributes of CAN packet record 2

    # close connections with CAN interfaces
    del can_ti
    await asyncio.sleep(0.1)  # wait to make sure all tasks are closed
    kvaser_interface_1.shutdown()
    kvaser_interface_2.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

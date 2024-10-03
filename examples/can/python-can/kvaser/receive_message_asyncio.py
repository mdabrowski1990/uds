import asyncio
from pprint import pprint

from can import Bus, Message
from uds.can import CanAddressingFormat, CanAddressingInformation
from uds.transport_interface import PyCanTransportInterface


async def main():
    # configure CAN interfaces
    kvaser_interface_1 = Bus(interface="kvaser", channel=0, fd=True, receive_own_messages=True)  # receiving
    kvaser_interface_2 = Bus(interface="kvaser", channel=1, fd=True, receive_own_messages=True)  # sending

    # configure Addressing Information of a CAN Node (example values)
    addressing_information = CanAddressingInformation(
        addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
        tx_physical={"can_id": 0x611},
        rx_physical={"can_id": 0x612},
        tx_functional={"can_id": 0x6FF},
        rx_functional={"can_id": 0x6FE})

    # create Transport Interface object for UDS communication
    can_ti = PyCanTransportInterface(can_bus_manager=kvaser_interface_1,
                                     addressing_information=addressing_information)

    # define frames carrying a UDS message (to be received later on)
    frame_1 = Message(arbitration_id=0x612, data=[0x10, 0x0b, 0x62, 0x10, 0x00, 0x00, 0x01, 0x02])
    frame_2 = Message(arbitration_id=0x612, data=[0x21, 0x03, 0x04, 0x05, 0x06, 0x07, 0xCC, 0xCC])

    # define task of define UDS message transmission
    async def _send_message():
        await asyncio.sleep(0.01)
        kvaser_interface_2.send(frame_1)
        await asyncio.sleep(0.5)
        kvaser_interface_2.send(frame_2)

    send_message_task = asyncio.create_task(_send_message())

    # receive message
    received_message_record = await can_ti.async_receive_message(timeout=1000)  # 1000 [ms]
    await send_message_task
    pprint(received_message_record.__dict__)

    # close connections with CAN interfaces
    del can_ti
    kvaser_interface_1.shutdown()
    kvaser_interface_2.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

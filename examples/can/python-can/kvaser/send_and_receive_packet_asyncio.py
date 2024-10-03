import asyncio
from pprint import pprint

from can import Bus
from uds.can import CanAddressingFormat, CanAddressingInformation
from uds.message import UdsMessage
from uds.transmission_attributes import AddressingType
from uds.transport_interface import PyCanTransportInterface


async def main():
    # configure CAN interfaces
    kvaser_interface_1 = Bus(interface="kvaser", channel=0, fd=True, receive_own_messages=True)  # receiving
    kvaser_interface_2 = Bus(interface="kvaser", channel=1, fd=True, receive_own_messages=True)  # sending

    # configure Addressing Information of a CAN Node (example values)
    ai_receive = CanAddressingInformation(
        addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
        tx_physical={"can_id": 0x611},
        rx_physical={"can_id": 0x612},
        tx_functional={"can_id": 0x6FF},
        rx_functional={"can_id": 0x6FE})
    ai_send = CanAddressingInformation(
        addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
        tx_physical={"can_id": 0x612},
        rx_physical={"can_id": 0x611},
        tx_functional={"can_id": 0x6FE},
        rx_functional={"can_id": 0x6FF})

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
    receive_packet_task = asyncio.create_task(can_ti_1.async_receive_packet(timeout=100))
    sent_packet_record = await can_ti_2.async_send_packet(packet)
    pprint(sent_packet_record.__dict__)
    received_packet_record = await receive_packet_task
    pprint(received_packet_record.__dict__)

    # close connections with CAN interfaces
    del can_ti_1
    del can_ti_2
    kvaser_interface_1.shutdown()
    kvaser_interface_2.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

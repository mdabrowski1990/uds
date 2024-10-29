import asyncio
from pprint import pprint

from can import Bus
from uds.can import CanAddressingFormat, CanAddressingInformation
from uds.message import UdsMessage
from uds.transmission_attributes import AddressingType
from uds.transport_interface import PyCanTransportInterface


async def main():
    # configure CAN interfaces
    kvaser_interface_1 = Bus(interface="kvaser", channel=0, fd=True, receive_own_messages=True)
    # second interface is only used to acknowledge CAN frames sent by `kvaser_interface_1`,
    # you might comment it out if you have another device to do that
    kvaser_interface_2 = Bus(interface="kvaser", channel=1, fd=True, receive_own_messages=True)

    # configure Addressing Information of a CAN Node (example values set)
    addressing_information = CanAddressingInformation(
        addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
        tx_physical={"can_id": 0x611},
        rx_physical={"can_id": 0x612},
        tx_functional={"can_id": 0x6FF},
        rx_functional={"can_id": 0x6FE})

    # create Transport Interface object for UDS communication
    can_ti = PyCanTransportInterface(can_bus_manager=kvaser_interface_1,
                                     addressing_information=addressing_information)

    # define UDS Messages to send
    message = UdsMessage(addressing_type=AddressingType.FUNCTIONAL, payload=[0x10, 0x03])

    # send UDS Message
    message_record = await can_ti.async_send_message(message)
    pprint(message_record.__dict__)

    # close connections with CAN interfaces
    del can_ti
    kvaser_interface_1.shutdown()
    kvaser_interface_2.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

"""Send (on one interface) and received (on the second) asynchronously a message using Diagnostic on CAN protocol (ISO 15765)."""

import asyncio

from can import Bus
from uds.addressing import AddressingType
from uds.can import CanAddressingFormat, CanAddressingInformation, PyCanTransportInterface
from uds.message import UdsMessage


async def main():
    # configure CAN interface - https://python-can.readthedocs.io/en/stable/interfaces.html
    can_interface_1 = Bus(
        # provide configuration for your CAN interface
        interface="kvaser",  # replace with your CAN interface name
        channel=0,
        receive_own_messages=True,  # mandatory setting if you use Kvaser
        # configure your CAN bus
        bitrate=500_000,
        fd=True,
        data_bitrate=4_000_000)
    # configure CAN interface - https://python-can.readthedocs.io/en/stable/interfaces.html
    can_interface_2 = Bus(
        # provide configuration for your CAN interface
        interface="kvaser",  # replace with your CAN interface name
        channel=1,
        receive_own_messages=True,  # mandatory setting if you use Kvaser
        # configure your CAN bus
        bitrate=500_000,
        fd=True,
        data_bitrate=4_000_000)

    # configure addresses for Diagnostics on CAN communication
    # CAN Addressing Formats explanation:
    # https://uds.readthedocs.io/en/stable/pages/knowledge_base/packet.html#can-packet-addressing-formats
    ai_receive = CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
                                          tx_physical_params={"can_id": 0x611},
                                          rx_physical_params={"can_id": 0x612},
                                          tx_functional_params={"can_id": 0x6FF},
                                          rx_functional_params={"can_id": 0x6FE})
    ai_send = ai_receive.get_other_end()

    # create Transport Interface object for Diagnostics on CAN communication
    can_ti_1 = PyCanTransportInterface(network_manager=can_interface_1,
                                       addressing_information=ai_receive)
    can_ti_2 = PyCanTransportInterface(network_manager=can_interface_2,
                                       addressing_information=ai_send)

    # define UDS Message to send
    message = UdsMessage(addressing_type=AddressingType.PHYSICAL, payload=[0x62, 0x10, 0x00, *range(100)])

    # send and receive message
    receive_message_task = asyncio.create_task(can_ti_2.async_receive_message(timeout=1000))  # tomeout=1000 ms
    sent_message_record = await can_ti_1.async_send_message(message)
    received_message_record = await receive_message_task

    # show results
    print(sent_message_record)
    print(received_message_record)

    # close connections with CAN interfaces
    del can_ti_1
    del can_ti_2
    can_interface_1.shutdown()
    can_interface_2.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

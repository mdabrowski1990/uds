"""Send asynchronously a message using Diagnostic on CAN protocol (ISO 15765)."""

import asyncio

from can import Bus
from uds.addressing import AddressingType
from uds.can import CanAddressingFormat, CanAddressingInformation, CanVersion, PyCanTransportInterface
from uds.message import UdsMessage


async def main():
    # configure CAN interface - https://python-can.readthedocs.io/en/stable/interfaces.html
    can_interface = Bus(
        # provide configuration for your CAN interface
        interface="kvaser",  # replace with your CAN interface name
        channel=0,
        receive_own_messages=True,  # mandatory setting if you use Kvaser
        # configure your CAN bus
        bitrate=500_000,
        fd=False)

    # configure addresses for Diagnostics on CAN communication
    # CAN Addressing Formats explanation:
    # https://uds.readthedocs.io/en/stable/pages/knowledge_base/packet.html#can-packet-addressing-formats
    addressing_information = CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
                                                      rx_physical_params={"can_id": 0x611},
                                                      tx_physical_params={"can_id": 0x612},
                                                      rx_functional_params={"can_id": 0x6FF},
                                                      tx_functional_params={"can_id": 0x6FE})

    # create Transport Interface object for Diagnostics on CAN communication
    can_ti = PyCanTransportInterface(
        network_manager=can_interface,
        addressing_information=addressing_information,
        can_version=CanVersion.CLASSIC_CAN)  # send all diagnostic packets as Classic CAN frames

    # define UDS Messages to send
    message = UdsMessage(addressing_type=AddressingType.PHYSICAL, payload=[0x10, 0x03])

    # send UDS Message
    sent_message_record = await can_ti.async_send_message(message)

    # show sent message
    print(sent_message_record)

    # close connections with CAN interface
    del can_ti
    can_interface.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

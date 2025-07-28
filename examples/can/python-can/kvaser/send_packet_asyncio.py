"""Send asynchronously a packet defined by Diagnostic on CAN protocol (ISO 15765)."""

import asyncio

from can import Bus
from uds.addressing import AddressingType
from uds.can import CanAddressingFormat, CanAddressingInformation, PyCanTransportInterface
from uds.message import UdsMessage


async def main():
    # configure CAN interface
    can_interface = Bus(interface="kvaser",
                        channel=0,
                        receive_own_messages=True,  # mandatory if you use Kvaser
                        bitrate=500_000,  # adjust to your CAN bus
                        fd=True,  # adjust to your CAN bus
                        data_bitrate=4_000_000)    # adjust to your CAN bus

    # configure addresses for Diagnostics on CAN communication
    # CAN Addressing Formats explanation:
    # https://uds.readthedocs.io/en/stable/pages/knowledge_base/packet.html#can-packet-addressing-formats
    addressing_information = CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
                                                      rx_physical_params={"can_id": 0x611},
                                                      tx_physical_params={"can_id": 0x612},
                                                      rx_functional_params={"can_id": 0x6FF},
                                                      tx_functional_params={"can_id": 0x6FE})

    # create Transport Interface object for Diagnostics on CAN communication
    can_ti = PyCanTransportInterface(network_manager=can_interface,
                                     addressing_information=addressing_information)

    # define UDS Message
    message = UdsMessage(addressing_type=AddressingType.PHYSICAL, payload=[0x10, 0x03])
    # pick one CAN packet from UDS Message segmentation
    packet = can_ti.segmenter.segmentation(message)[0]

    # send CAN Packet
    sent_packet_record = await can_ti.async_send_packet(packet)

    # show sent packet
    print(sent_packet_record)

    # close connections with CAN interface
    del can_ti
    can_interface.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

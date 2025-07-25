import asyncio

from can import Bus
from uds.addressing import AddressingType
from uds.can import CanAddressingFormat, CanAddressingInformation, PyCanTransportInterface
from uds.message import UdsMessage


async def main():
    # configure CAN interfaces
    can_interface_1 = Bus(interface="kvaser",
                        channel=0,
                        bitrate=500000,
                        fd=True,
                        data_bitrate=4000000,
                        receive_own_messages=True)  # sending
    can_interface_2 = Bus(interface="kvaser",
                        channel=1,
                        bitrate=500000,
                        fd=True,
                        data_bitrate=4000000,
                        receive_own_messages=True)  # receiving

    # configure addresses for Diagnostics on CAN communication
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

    # define UDS Message
    message = UdsMessage(addressing_type=AddressingType.PHYSICAL, payload=[0x10, 0x03])
    # pick one CAN packet from UDS Message segmentation
    packet = can_ti_1.segmenter.segmentation(message)[0]

    # send and receive packet CAN packet
    receive_packet_task = asyncio.create_task(can_ti_2.async_receive_packet(timeout=100))
    sent_packet_record = await can_ti_1.async_send_packet(packet)
    received_packet_record = await receive_packet_task

    # show results
    print(sent_packet_record)
    print(received_packet_record)

    # close connections with CAN interfaces
    del can_ti_1
    del can_ti_2
    can_interface_1.shutdown()
    can_interface_2.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

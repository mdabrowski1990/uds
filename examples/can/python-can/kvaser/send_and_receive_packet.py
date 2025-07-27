"""Send (on one interface) and received (on the second) a packet defined by Diagnostic on CAN protocol (ISO 15765)."""

from can import Bus
from uds.addressing import AddressingType
from uds.can import CanAddressingFormat, CanAddressingInformation, PyCanTransportInterface
from uds.message import UdsMessage


def main():
    # configure CAN interfaces
    can_interface_1 = Bus(interface="kvaser",
                          channel=0,
                          receive_own_messages=True,  # mandatory if you use Kvaser
                          bitrate=500_000,  # adjust to your CAN bus
                          fd=True,  # adjust to your CAN bus
                          data_bitrate=4_000_000)  # adjust to your CAN bus
    can_interface_2 = Bus(interface="kvaser",
                          channel=0,
                          receive_own_messages=True,  # mandatory if you use Kvaser
                          bitrate=500_000,  # adjust to your CAN bus
                          fd=True,  # adjust to your CAN bus
                          data_bitrate=4_000_000)  # adjust to your CAN bus

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

    # define UDS Message
    message = UdsMessage(addressing_type=AddressingType.PHYSICAL, payload=[0x10, 0x03])
    # pick one CAN packet from UDS Message segmentation
    packet = can_ti_1.segmenter.segmentation(message)[0]

    # send and receive packet CAN packet
    sent_packet_record = can_ti_1.send_packet(packet)
    received_packet_record = can_ti_2.receive_packet(timeout=100)

    # show results
    print(sent_packet_record)
    print(received_packet_record)

    # close connections with CAN interfaces
    del can_ti_1
    del can_ti_2
    can_interface_1.shutdown()
    can_interface_2.shutdown()


if __name__ == "__main__":
    main()

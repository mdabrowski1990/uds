"""Send (on one interface) and received (on the second) a message using Diagnostic on CAN protocol (ISO 15765)."""

from threading import Timer
from time import sleep

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

    # define UDS Message to send
    message = UdsMessage(addressing_type=AddressingType.PHYSICAL, payload=[0x62, 0x10, 0x00, *range(100)])

    # prepare code for scheduling transmission
    sent_message_record = None
    def _send_message():
        nonlocal sent_message_record
        sent_message_record = can_ti_1.send_message(message)
    timer = Timer(interval=0.01,  # delay after which message will be sent, now 0.01 [s]
                  function=_send_message)

    # send and receive message
    timer.start()
    received_message_record = can_ti_2.receive_message(timeout=1000)  # timeout=1000 [ms]

    # wait till message is received
    while not timer.finished.is_set():
        sleep(0.01)

    # show results
    print(sent_message_record)
    print(received_message_record)

    # close connections with CAN interfaces
    del can_ti_1
    del can_ti_2
    can_interface_1.shutdown()
    can_interface_2.shutdown()


if __name__ == "__main__":
    main()

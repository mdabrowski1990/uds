from pprint import pprint
from threading import Timer
from time import sleep

from can import Bus
from uds.can import CanAddressingFormat, CanAddressingInformation
from uds.message import UdsMessage
from uds.transmission_attributes import AddressingType
from uds.transport_interface import PyCanTransportInterface


def main():
    # configure CAN interfaces
    kvaser_interface_1 = Bus(interface="kvaser", channel=0, fd=True, receive_own_messages=True)  # receiving
    kvaser_interface_2 = Bus(interface="kvaser", channel=1, fd=True, receive_own_messages=True)  # sending

    # configure Addressing Information of a CAN Nodes (example values)
    ai_receive = CanAddressingInformation(
        addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
        tx_physical={"can_id": 0x611},
        rx_physical={"can_id": 0x612},
        tx_functional={"can_id": 0x6FF},
        rx_functional={"can_id": 0x6FE})
    ai_send = CanAddressingInformation(
        addressing_format=ai_receive.addressing_format,
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
    message = UdsMessage(addressing_type=AddressingType.PHYSICAL, payload=[0x62, 0x10, 0x00, *range(100)])

    # prepare code for scheduling transmission
    sent_message_record = None

    def _send_message():
        nonlocal sent_message_record
        sent_message_record = can_ti_2.send_message(message)

    timer = Timer(interval=0.01,  # delay after which message will be sent, now 0.01 [s]
                  function=_send_message)

    # send and receive message
    timer.start()
    received_message_record = can_ti_1.receive_message(timeout=1000)  # 1000 [ms]

    # wait till message is received
    while not timer.finished.is_set():
        sleep(0.01)

    # show results
    pprint(received_message_record.__dict__)
    pprint(sent_message_record.__dict__)

    # close connections with CAN interfaces
    del can_ti_1
    del can_ti_2
    kvaser_interface_1.shutdown()
    kvaser_interface_2.shutdown()


if __name__ == "__main__":
    main()

from pprint import pprint
from time import sleep

from can import Bus
from uds.can import CanAddressingFormat, CanAddressingInformation
from uds.message import UdsMessage
from uds.transmission_attributes import AddressingType
from uds.transport_interface import PyCanTransportInterface


def main():
    # configure CAN interfaces
    kvaser_interface_1 = Bus(interface="kvaser", channel=0, fd=True, receive_own_messages=True)
    kvaser_interface_2 = Bus(interface="kvaser", channel=1, fd=True, receive_own_messages=True)

    # configure Addressing Information of a CAN Node
    addressing_information = CanAddressingInformation(
        addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
        tx_physical={"can_id": 0x611},
        rx_physical={"can_id": 0x612},
        tx_functional={"can_id": 0x6FF},
        rx_functional={"can_id": 0x6FE})

    # create Transport Interface object for UDS communication
    can_ti = PyCanTransportInterface(can_bus_manager=kvaser_interface_1,
                                     addressing_information=addressing_information)

    # define UDS Messages to send
    message_1 = UdsMessage(addressing_type=AddressingType.FUNCTIONAL, payload=[0x10, 0x03])
    message_2 = UdsMessage(addressing_type=AddressingType.PHYSICAL, payload=[0x22, *range(64)])

    # send CAN Message 1
    record_1 = can_ti.send_message(message_1)
    pprint(record_1.__dict__)

    # send CAN Packet 2
    record_2 = can_ti.send_message(message_2)
    pprint(record_2.__dict__)

    # close connections with CAN interfaces
    del can_ti
    sleep(0.1)  # wait to make sure all tasks are closed
    kvaser_interface_1.shutdown()
    kvaser_interface_2.shutdown()


if __name__ == "__main__":
    main()

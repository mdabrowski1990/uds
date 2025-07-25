from can import Bus
from uds.addressing import AddressingType
from uds.can import CanAddressingFormat, CanAddressingInformation, PyCanTransportInterface
from uds.message import UdsMessage


def main():
    # configure CAN interface
    can_interface = Bus(interface="kvaser",
                        channel=0,
                        bitrate=500000,
                        fd=True,
                        data_bitrate=4000000,
                        receive_own_messages=True)

    # configure addresses for Diagnostics on CAN communication
    addressing_information = CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
                                                      rx_physical_params={"can_id": 0x611},
                                                      tx_physical_params={"can_id": 0x612},
                                                      rx_functional_params={"can_id": 0x6FF},
                                                      tx_functional_params={"can_id": 0x6FE})

    # create Transport Interface object for Diagnostics on CAN communication
    can_ti = PyCanTransportInterface(network_manager=can_interface,
                                     addressing_information=addressing_information)

    # define UDS Messages to send
    message = UdsMessage(addressing_type=AddressingType.PHYSICAL, payload=[0x10, 0x03])

    # receive message
    received_message_record = can_ti.send_message(message=message)

    # show sent message
    print(received_message_record)

    # close connections with CAN interface
    del can_ti
    can_interface.shutdown()


if __name__ == "__main__":
    main()

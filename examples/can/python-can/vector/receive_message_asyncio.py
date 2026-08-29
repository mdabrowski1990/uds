"""Receive asynchronously a message using Diagnostic on CAN protocol (ISO 15765)."""

import asyncio

from can import Bus
from uds.can import CanAddressingFormat, CanAddressingInformation, PythonCanTransportInterface


async def main():
    # configure CAN interface - https://python-can.readthedocs.io/en/stable/interfaces.html
    can_interface = Bus(
        # provide configuration for your CAN interface
        interface="vector",
        app_name="python-can",  # name of the Application in Vector Hardware Config
        channel=0,
        receive_own_messages=True,  # recommended
        # configure your CAN bus
        bitrate=500_000,
        fd=True,
        data_bitrate=4_000_000)

    # configure addresses for Diagnostics on CAN communication
    # CAN Addressing Formats explanation:
    # https://uds.readthedocs.io/en/stable/pages/knowledge_base/packet.html#can-packet-addressing-formats
    addressing_information = CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
                                                      rx_physical_params={"can_id": 0x611},
                                                      tx_physical_params={"can_id": 0x612},
                                                      rx_functional_params={"can_id": 0x6FF},
                                                      tx_functional_params={"can_id": 0x6FE})

    # create Transport Interface object for Diagnostics on CAN communication
    can_ti = PythonCanTransportInterface(
        network_manager=can_interface,
        addressing_information=addressing_information)

    # receive UDS message
    received_message_record = await can_ti.async_receive_message(start_timeout=1000)  # timeout=1000 [ms]

    # show received message
    print(received_message_record)

    # close connections with CAN interface
    can_ti.teardown_sync(True)
    can_ti.teardown_async(True)
    can_interface.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

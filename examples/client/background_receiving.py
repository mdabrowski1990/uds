"""Start and stop receiving response messages in background."""

from uds.client import Client
from uds.transport_interface import AbstractTransportInterface


def main():
    # configure your own Transport Interface
    # https://uds.readthedocs.io/en/stable/pages/user_guide/quickstart.html#create-transport-interface
    transport_interface: AbstractTransportInterface

    # configure client
    # https://uds.readthedocs.io/en/stable/pages/user_guide/client.html#configuration
    client = Client(transport_interface=transport_interface)

    # start collecting all response messages sent to client
    client.start_receiving()

    # wait for a response message
    response_message_record = client.get_response()
    # present received message
    print(response_message_record)

    # stop collecting response messages
    client.stop_receiving()

if __name__ == "__main__":
    main()

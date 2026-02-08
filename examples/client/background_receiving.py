"""Start and stop receiving response messages in the background."""

from uds.client import Client
from uds.transport_interface import AbstractTransportInterface


def main():
    # configure your own Transport Interface
    # https://uds.readthedocs.io/en/stable/pages/user_guide/quickstart.html#create-transport-interface
    transport_interface: AbstractTransportInterface = ...  # TODO: provide your implementation here

    # configure the client
    # https://uds.readthedocs.io/en/stable/pages/user_guide/client.html#configuration
    client = Client(transport_interface=transport_interface)

    # start collecting all response messages sent to the client
    client.start_background_receiving()

    # try to get a response immediately
    response_message_record = client.get_response_no_wait()
    if response_message_record is None:
        print("No response received so far.")
    else:
        print("Received response:", response_message_record)

    # wait for a response message
    response_message_record = client.get_response(timeout=1000)  # wait up to 1000 ms for a response
    if response_message_record is None:
        print("No response received within timeout.")
    else:
        print("Received response:", response_message_record)

    # stop collecting response messages
    client.stop_background_receiving()


if __name__ == "__main__":
    main()
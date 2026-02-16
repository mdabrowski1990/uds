"""Start and stop periodic Tester Present sending."""

from uds.addressing import AddressingType
from uds.client import Client
from uds.transport_interface import AbstractTransportInterface


def main():
    # configure your own Transport Interface
    # https://uds.readthedocs.io/en/stable/pages/user_guide/quickstart.html#create-transport-interface
    transport_interface: AbstractTransportInterface = ...  # TODO: provide your implementation here

    # configure the client
    # https://uds.readthedocs.io/en/stable/pages/user_guide/client.html#configuration
    client = Client(transport_interface=transport_interface,
                    s3_client=1000)  # set 1000ms as period for Tester Present sending
    client.tester_present_storage_size = 10  # adjust number of records stored if needed

    # start periodic Tester Present sending
    client.start_tester_present(addressing_type=AddressingType.PHYSICAL,  # addressing type to use
                                sprmib=False)  # disable Suppress Positive Response Message Indication Bit

    # TODO: perform some action with tester present cyclically sent

    # stop periodic Tester Present sending
    client.stop_tester_present()

    # access records of Tester Present request messages
    print(client.last_sent_tester_present_requests)


if __name__ == "__main__":
    main()

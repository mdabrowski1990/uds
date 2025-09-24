"""Start and stop periodic Tester Present sending."""

from uds.client import Client
from uds.transport_interface import AbstractTransportInterface


def main():
    # configure your own Transport Interface
    # https://uds.readthedocs.io/en/stable/pages/user_guide/quickstart.html#create-transport-interface
    transport_interface: AbstractTransportInterface

    # configure client
    # TODO: put link here
    client = Client(transport_interface=transport_interface)

    # start periodic TesterPresent sending
    client.start_tester_present()

    # stop periodic TesterPresent sending
    client.stop_tester_present()


if __name__ == "__main__":
    main()

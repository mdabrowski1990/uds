"""Send a request message, collect all responses."""

from uds.client import Client
from uds.transport_interface import AbstractTransportInterface
from uds.message import UdsMessage
from uds.addressing import AddressingType


def main():
    # configure your own Transport Interface
    # https://uds.readthedocs.io/en/stable/pages/user_guide/quickstart.html#create-transport-interface
    transport_interface: AbstractTransportInterface

    # configure client
    # TODO: put link here
    client = Client(transport_interface=transport_interface)

    # define an example request message
    request = UdsMessage(payload=[0x14, 0xFF, 0xFF, 0xFF],
                         addressing_type=AddressingType.PHYSICAL)

    # send request, get all responses
    request_record, responses_records = client.send_request_receive_responses(request)

    # present sent message
    print(f"Sent request: {request_record}")

    # present received messages
    if responses_records:
        for i, response_record in enumerate(responses_records):
            print(f"Response #{i+1}: {response_record}")
    else:
        print("No response message received.")


if __name__ == "__main__":
    main()

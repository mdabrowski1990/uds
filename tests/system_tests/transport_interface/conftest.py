from pytest import fixture

from can import Message
from uds.can import CanAddressingFormat, CanAddressingInformation
from uds.message import UdsMessage
from uds.transmission_attributes import AddressingType


@fixture
def example_addressing_information():
    """Example Addressing Information of a CAN Node."""
    return CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
                                    tx_physical={"can_id": 0x611},
                                    rx_physical={"can_id": 0x612},
                                    tx_functional={"can_id": 0x6FF},
                                    rx_functional={"can_id": 0x6FE})


@fixture
def example_addressing_information_2nd_node():
    """
    Example Addressing Information of a 2nd CAN Node.

    .. note::
        Values of example_addressing_information and example_addressing_information_2nd_node are compatible, so
        these two CAN nodes can communicate with each other over physical and functional addressing.
    """
    return CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
                                    tx_physical={"can_id": 0x612},
                                    rx_physical={"can_id": 0x611},
                                    tx_functional={"can_id": 0x6FE},
                                    rx_functional={"can_id": 0x6FF})


@fixture
def example_rx_frame():
    """
    Example CAN Frame containing a CAN Packet with received addressing information.

    .. note::
        Compatible with example_addressing_information.
    """
    return Message(arbitration_id=0x612, data=[0x02, 0x10, 0x03])


@fixture
def example_tx_frame():
    """
    Example CAN Frame containing a CAN Packet with transmitted addressing information.

    .. note::
        Compatible with example_addressing_information.
    """
    return Message(arbitration_id=0x611, data=[0x02, 0x50, 0x03, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC])


@fixture
def example_tx_uds_message():
    """
    Example CAN Frame containing a CAN Packet with transmitted addressing information.

    .. note::
        It is the same message as one carried in example_tx_frame.
        Compatible with example_addressing_information.
    """
    return UdsMessage(payload=[0x50, 0x03], addressing_type=AddressingType.PHYSICAL)

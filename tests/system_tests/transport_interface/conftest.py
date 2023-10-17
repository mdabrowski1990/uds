from pytest import fixture

from can import Message

from uds.can import CanAddressingInformation, CanAddressingFormat
from uds.message import UdsMessage
from uds.transmission_attributes import AddressingType


@fixture
def example_addressing_information():
    """Example Addressing Information that can be used in test cases."""
    return CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                    tx_physical={"can_id": 0x611},
                                    rx_physical={"can_id": 0x612},
                                    tx_functional={"can_id": 0x6FF},
                                    rx_functional={"can_id": 0x6FE})


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
        The same as example_tx_frame.
        Compatible with example_addressing_information.
    """
    return UdsMessage(payload=[0x50, 0x03], addressing_type=AddressingType.PHYSICAL)

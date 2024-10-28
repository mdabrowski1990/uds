from pytest import fixture

from uds.can import AbstractCanAddressingInformation, CanAddressingFormat, CanAddressingInformation
from uds.message import UdsMessage
from uds.transmission_attributes import AddressingType


@fixture(params=[
    CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
                             tx_physical={"can_id": 0x611},
                             rx_physical={"can_id": 0x612},
                             tx_functional={"can_id": 0x6FF},
                             rx_functional={"can_id": 0x6FE}),
    CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                             tx_physical={"can_id": 0xDA1BFF, "target_address": 0x1B, "source_address": 0xFF},
                             rx_physical={"can_id": 0xDAFF1B, "target_address": 0xFF, "source_address": 0x1B},
                             tx_functional={"can_id": 0x1CDB00FE, "target_address": 0x00, "source_address": 0xFE},
                             rx_functional={"can_id": 0x1CDBFE00, "target_address": 0xFE, "source_address": 0x00}),
    CanAddressingInformation(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                             tx_physical={"can_id": 0x987, "target_address": 0x90},
                             rx_physical={"can_id": 0x987, "target_address": 0xFE},
                             tx_functional={"can_id": 0xDA1BFF, "target_address": 0xFF},
                             rx_functional={"can_id": 0x1CCDFEAC, "target_address": 0xFF}),
    CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                             tx_physical={"can_id": 0x651, "address_extension": 0x87},
                             rx_physical={"can_id": 0x652, "address_extension": 0x87},
                             tx_functional={"can_id": 0x6FE, "address_extension": 0xA5},
                             rx_functional={"can_id": 0x6FF, "address_extension": 0xA5}),
    CanAddressingInformation(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                             tx_physical={"can_id": 0xCE1BFF, "target_address": 0x1B, "source_address": 0xFF, "address_extension": 0x87},
                             rx_physical={"can_id": 0xCEFF1B, "target_address": 0xFF, "source_address": 0x1B, "address_extension": 0x87},
                             tx_functional={"can_id": 0x1CCDACFE, "target_address": 0xAC, "source_address": 0xFE, "address_extension": 0x00},
                             rx_functional={"can_id": 0x1CCDFEAC, "target_address": 0xFE, "source_address": 0xAC, "address_extension": 0x00}),
])
def example_addressing_information(request) -> AbstractCanAddressingInformation:
    """Example Addressing Information of a CAN Node."""
    return request.param


@fixture
def example_addressing_information_2nd_node(example_addressing_information) -> AbstractCanAddressingInformation:
    """
    Example Addressing Information of a 2nd CAN Node.

    .. note::
        Values of example_addressing_information and example_addressing_information_2nd_node are compatible, so
        these two CAN nodes can communicate with each other over physical and functional addressing.
    """
    return example_addressing_information.get_other_end()

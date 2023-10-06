from pytest import fixture

from uds.can import CanAddressingInformation, CanAddressingFormat


@fixture
def example_addressing_information():
    return CanAddressingInformation(addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                    tx_physical={"can_id": 0x611},
                                    rx_physical={"can_id": 0x612},
                                    tx_functional={"can_id": 0x6FF},
                                    rx_functional={"can_id": 0x6FE})

from pytest import fixture

from uds.addressing import AddressingType
from uds.can import CanAddressingFormat, CanAddressingInformation
from uds.can.addressing import (
    AbstractCanAddressingInformation,
    ExtendedCanAddressingInformation,
    Mixed11BitCanAddressingInformation,
    Mixed29BitCanAddressingInformation,
    NormalCanAddressingInformation,
    NormalFixedCanAddressingInformation,
)
from uds.message import UdsMessage


@fixture(params=list(CanAddressingFormat))
def example_can_addressing_format(request) -> CanAddressingFormat:
    return request.param


@fixture
def example_can_addressing_information(example_can_addressing_format) -> AbstractCanAddressingInformation:
    if example_can_addressing_format == CanAddressingFormat.NORMAL_ADDRESSING:
        return NormalCanAddressingInformation(rx_physical_params={"can_id": 0x720},
                                              tx_physical_params={"can_id": 0x748},
                                              rx_functional_params={"can_id": 0x7DF},
                                              tx_functional_params={"can_id": 0x748})
    if example_can_addressing_format == CanAddressingFormat.NORMAL_FIXED_ADDRESSING:
        return NormalFixedCanAddressingInformation(
            rx_physical_params={"source_address": 0x04, "target_address": 0xF0, "can_id": 0xDAF004},
            tx_physical_params={"source_address": 0xF0, "target_address": 0x04, "can_id": 0xDA04F0},
            rx_functional_params={"source_address": 0xF0, "target_address": 0x9F},
            tx_functional_params={"source_address": 0x9F, "target_address": 0xF0})
    if example_can_addressing_format == CanAddressingFormat.EXTENDED_ADDRESSING:
        return ExtendedCanAddressingInformation(rx_physical_params={"can_id": 0x741, "target_address": 0x76},
                                                tx_physical_params={"can_id": 0x742, "target_address": 0xFF},
                                                rx_functional_params={"can_id": 0x7DE, "target_address": 0xFF},
                                                tx_functional_params={"can_id": 0x7DF, "target_address": 0xFF})
    if example_can_addressing_format == CanAddressingFormat.MIXED_11BIT_ADDRESSING:
        return Mixed11BitCanAddressingInformation(rx_physical_params={"can_id": 0x741, "address_extension": 0x76},
                                                  tx_physical_params={"can_id": 0x742, "address_extension": 0x76},
                                                  rx_functional_params={"can_id": 0x741, "address_extension": 0xFF},
                                                  tx_functional_params={"can_id": 0x742, "address_extension": 0xFF})
    if example_can_addressing_format == CanAddressingFormat.MIXED_29BIT_ADDRESSING:
        return Mixed29BitCanAddressingInformation(
            rx_physical_params={"can_id": 0xCEF032, "address_extension": 0x76},
            tx_physical_params={"can_id": 0xCE32F0, "address_extension": 0x76},
            rx_functional_params={"can_id": 0x1CCD00FF, "address_extension": 0xFF},
            tx_functional_params={"can_id": 0x1CCDFF00, "address_extension": 0xFF})
    raise NotImplementedError


@fixture
def example_can_addressing_information_2nd_node(example_addressing_information) -> AbstractCanAddressingInformation:
    """
    Example Addressing Information of a 2nd CAN Node.

    .. note::
        Values of example_addressing_information and example_addressing_information_2nd_node are compatible, so
        these two CAN nodes addressing communicate with each other over physical and functional addressing.
    """
    return example_addressing_information.get_other_end()

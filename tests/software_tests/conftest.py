from random import choice, randint

from pytest import fixture

from can import Message
from uds.addressing import AddressingType
from uds.can import DEFAULT_FILLER_BYTE, CanAddressingFormat, CanDlcHandler, CanSegmenter
from uds.can.addressing import (
    AbstractCanAddressingInformation,
    ExtendedCanAddressingInformation,
    Mixed11BitCanAddressingInformation,
    Mixed29BitCanAddressingInformation,
    NormalCanAddressingInformation,
    NormalFixedCanAddressingInformation,
)
from uds.utilities import RawBytesAlias, TransmissionDirection

# Common


@fixture(params=[(0x00, 0xFF, 0xAA, 0x55), [0x00], (0xFF, ), [0x12, 0xFF, 0xE0, 0x1D, 0xC2, 0x3B, 0x00, 0xFF],
                 bytearray([0x54]), bytearray([0xFF, 0x00, 0xA4]), bytes([0x12, 0x34])])
def example_raw_bytes(request) -> RawBytesAlias:
    return request.param


@fixture(params=list(AddressingType))
def example_addressing_type(request) -> AddressingType:
    return request.param


@fixture(params=list(TransmissionDirection))
def example_transmission_direction(request) -> TransmissionDirection:
    return request.param


# CAN specific


@fixture(params=[
    Message(arbitration_id=0x644,
            is_extended_id=False,
            channel=1,
            dlc=8,
            data=[0x05, 0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE]),
    Message(arbitration_id=0x18DCAB34,
            is_extended_id=True,
            channel="Channel 2",
            dlc=0xF,
            data=[0xD0, 0x10, 0x00, 0xFE, 0xDC, 0xBA, 0x98] + list(range(50, 107)),
            is_fd=True,
            bitrate_switch=True),
])
def example_python_can_message(request) -> Message:
    return request.param


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

@fixture()
def example_can_segmenter(example_can_addressing_information) -> CanSegmenter:
    return CanSegmenter(addressing_information=example_can_addressing_information,
                        use_data_optimization=choice([True, False]),
                        dlc=randint(CanDlcHandler.MIN_BASE_UDS_DLC, CanDlcHandler.MAX_DLC_VALUE),
                        filler_byte=randint(0, 0xFF))

from random import choice, randint

from pytest import FixtureRequest, fixture

from can import Message
from uds.addressing import AddressingType
from uds.can import CanAddressingFormat, CanDlcHandler, CanSegmenter
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


@fixture(params=[
    (0x00, 0xFF, 0xAA, 0x55),
    [0x00],
    bytearray(range(0xFF)),
    b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87\x78\x69\x5A\x4B\x3C\x2D\x1E\x0F"])
def example_raw_bytes(request: FixtureRequest) -> RawBytesAlias:
    """Example values or Raw Bytes."""
    return request.param

@fixture(params=list(AddressingType))
def example_addressing_type(request: FixtureRequest) -> AddressingType:
    """Example value of Addressing Type."""
    return request.param

@fixture(params=list(TransmissionDirection))
def example_transmission_direction(request: FixtureRequest) -> TransmissionDirection:
    """Example value of Transmission Direction."""
    return request.param


# CAN Specific


def make_can_addressing_information(addressing_format: CanAddressingFormat) -> AbstractCanAddressingInformation:
    """
    Create example CAN Addressing Information.

    :param addressing_format: CAN Addressing Format to use.

    :return: Example CAN Addressing Information object using provided CAN Addressing Format.
    """
    if addressing_format == CanAddressingFormat.NORMAL_ADDRESSING:
        return NormalCanAddressingInformation(rx_physical_params={"can_id": 0x720},
                                              tx_physical_params={"can_id": 0x748},
                                              rx_functional_params={"can_id": 0x7DF},
                                              tx_functional_params={"can_id": 0x748})
    if addressing_format == CanAddressingFormat.NORMAL_FIXED_ADDRESSING:
        return NormalFixedCanAddressingInformation(
            rx_physical_params={"source_address": 0x04, "target_address": 0xF0, "can_id": 0xDAF004},
            tx_physical_params={"source_address": 0xF0, "target_address": 0x04, "can_id": 0xDA04F0},
            rx_functional_params={"source_address": 0xF0, "target_address": 0x9F},
            tx_functional_params={"source_address": 0x9F, "target_address": 0xF0})
    if addressing_format == CanAddressingFormat.EXTENDED_ADDRESSING:
        return ExtendedCanAddressingInformation(rx_physical_params={"can_id": 0x741, "target_address": 0x76},
                                                tx_physical_params={"can_id": 0x742, "target_address": 0xFF},
                                                rx_functional_params={"can_id": 0x7DE, "target_address": 0xFF},
                                                tx_functional_params={"can_id": 0x742, "target_address": 0xE2})
    if addressing_format == CanAddressingFormat.MIXED_11BIT_ADDRESSING:
        return Mixed11BitCanAddressingInformation(rx_physical_params={"can_id": 0x741, "address_extension": 0x76},
                                                  tx_physical_params={"can_id": 0x742, "address_extension": 0x76},
                                                  rx_functional_params={"can_id": 0x741, "address_extension": 0xFF},
                                                  tx_functional_params={"can_id": 0x742, "address_extension": 0xFF})
    if addressing_format == CanAddressingFormat.MIXED_29BIT_ADDRESSING:
        return Mixed29BitCanAddressingInformation(
            rx_physical_params={"can_id": 0xCEF032, "address_extension": 0x76},
            tx_physical_params={"can_id": 0xCE32F0, "address_extension": 0x76},
            rx_functional_params={"can_id": 0x1CCD00FF, "address_extension": 0xFF},
            tx_functional_params={"can_id": 0x1CCDFF00, "address_extension": 0xFF})
    raise NotImplementedError(f"Unsupported CAN addressing format: {addressing_format}")


@fixture(params=list(CanAddressingFormat))
def example_can_addressing_format(request: FixtureRequest) -> CanAddressingFormat:
    """Example value of CAN Addressing Format."""
    return request.param


@fixture
def example_can_addressing_information(example_can_addressing_format: CanAddressingFormat
                                       ) -> AbstractCanAddressingInformation:
    """
    Example value of CAN Addressing Information.

    :param example_can_addressing_format: Value of `example_can_addressing_format` fixture.
    """
    return make_can_addressing_information(example_can_addressing_format)


@fixture
def parametrized_can_addressing_information(addressing_format: CanAddressingFormat):
    """Example value of CAN Addressing Information for CAN Addressing Format used."""
    return make_can_addressing_information(addressing_format)


@fixture
def example_can_segmenter(example_can_addressing_information: AbstractCanAddressingInformation) -> CanSegmenter:
    """Example value of CAN Segmenter."""
    return CanSegmenter(addressing_information=example_can_addressing_information,
                        use_data_optimization=choice([True, False]),
                        dlc=randint(CanDlcHandler.MIN_BASE_UDS_DLC, CanDlcHandler.MAX_DLC_VALUE),
                        filler_byte=randint(0, 0xFF))


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
            data=[0xD0, 0x10, 0x00, 0xFE, 0xDC, 0xBA, 0x98, *range(50, 107)],
            is_fd=True,
            bitrate_switch=True),
])
def example_python_can_message(request: FixtureRequest) -> Message:
    """Example CAN Frame used by python-can library."""
    return request.param

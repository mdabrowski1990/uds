from pytest import fixture

from can import Message
from uds.can import (
    CanAddressingFormat,
    ExtendedCanAddressingInformation,
    Mixed11BitCanAddressingInformation,
    Mixed29BitCanAddressingInformation,
    NormalCanAddressingInformation,
    NormalFixedCanAddressingInformation,
)
from uds.segmentation import CanSegmenter
from uds.transmission_attributes import AddressingType, TransmissionDirection

# Common


@fixture(params=[(0x00, 0xFF, 0xAA, 0x55), [0x00], (0xFF, ), [0x12, 0xFF, 0xE0, 0x1D, 0xC2, 0x3B, 0x00, 0xFF],
                 bytearray([0x54]), bytearray([0xFF, 0x00, 0xA4])])
def example_raw_bytes(request):
    return request.param


@fixture(params=list(AddressingType))
def example_addressing_type(request):
    return request.param


@fixture(params=list(TransmissionDirection))
def example_transmission_direction(request):
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
def example_python_can_message(request):
    return request.param


@fixture(params=list(CanAddressingFormat))
def example_can_addressing_format(request):
    return request.param


@fixture(params=[
    CanSegmenter(addressing_information=NormalCanAddressingInformation(rx_physical={"can_id": 0x643},
                                                                       tx_physical={"can_id": 0x644},
                                                                       rx_functional={"can_id": 0x7DE},
                                                                       tx_functional={"can_id": 0x7DF})),
    CanSegmenter(addressing_information=NormalFixedCanAddressingInformation(rx_physical={"target_address": 0x12, "source_address": 0xF8},
                                                                            tx_physical={"can_id": 0x18DAF812,"target_address": 0xF8, "source_address": 0x12},
                                                                            rx_functional={"can_id": 0x18DB0BFF, "target_address": 0x0B, "source_address": 0xFF},
                                                                            tx_functional={"target_address": 0xFF, "source_address": 0x0B}),
                 dlc=0xF,
                 use_data_optimization=True,
                 filler_byte=0xE9),
    CanSegmenter(addressing_information=ExtendedCanAddressingInformation(rx_physical={"can_id": 0x752, "target_address": 0x9C},
                                                                         tx_physical={"can_id": 0x752, "target_address": 0xF0},
                                                                         rx_functional={"can_id": 0x12CDEF59, "target_address": 0x9A},
                                                                         tx_functional={"can_id": 0x9876543, "target_address": 0x0E}),
                 dlc=0xA,
                 filler_byte=0x55),
    CanSegmenter(addressing_information=Mixed11BitCanAddressingInformation(rx_physical={"can_id": 0x6FE, "address_extension": 0x6B},
                                                                           tx_physical={"can_id": 0x720, "address_extension": 0xD0},
                                                                           rx_functional={"can_id": 0x7BD, "address_extension": 0x9C},
                                                                           tx_functional={"can_id": 0x7BD, "address_extension": 0xF2}),
                 use_data_optimization=True),
    CanSegmenter(addressing_information=Mixed29BitCanAddressingInformation(rx_physical={"can_id": 0x18CEF1E2, "address_extension": 0x6B},
                                                                           tx_physical={"can_id": 0x18CEE2F1, "target_address": 0xE2, "source_address": 0xF1, "address_extension": 0xD0},
                                                                           rx_functional={"target_address": 0xFF, "source_address": 0xFF, "address_extension": 0x55},
                                                                           tx_functional={"can_id": 0x18CDFFFF, "address_extension": 0xEF}),
                 dlc=0xF,
                 filler_byte=0xAA),
])
def example_can_segmenter(request):
    return request.param

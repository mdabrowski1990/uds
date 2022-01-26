from pytest import fixture

from can import Message

from uds.transmission_attributes import TransmissionDirection, AddressingType
from uds.can import CanAddressingFormat
from uds.segmentation import CanSegmenter


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
    CanSegmenter(addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                 physical_ai=dict(can_id=0x724),
                 functional_ai=dict(can_id=0x7FF)),
    CanSegmenter(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                 physical_ai=dict(target_address=0x1E, source_address=0xFF),
                 functional_ai=dict(target_address=0xB1, source_address=0xFF),
                 dlc=0xF,
                 use_data_optimization=True,
                 filler_byte=0x71),
    CanSegmenter(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                 physical_ai=dict(target_address=0xE0, can_id=0x129834),
                 functional_ai=dict(target_address=0xFF, can_id=0x12FFFF),
                 dlc=0xC,
                 use_data_optimization=True,
                 filler_byte=0x8E)
])
def example_can_segmenter(request):
    return request.param

from pytest import fixture

from uds.messages import AddressingType, POSSIBLE_REQUEST_SIDS, TransmissionDirection


@fixture(params=[(0x00, 0xFF, 0xAA, 0x55), [0xA1], [0x12, 0xFF, 0xE0, 0x1D, 0xC2, 0x3B, 0x00, 0xFF], (0xFF, ), [0x00]])
def example_raw_bytes(request):
    return request.param


@fixture(params=[(0x10, 0x01), [0x22, 0xF1, 0x83, 0x43, 0xAB], (0x19, 0x02, 0xFF)])
def example_uds_request_raw_data(request):
    return request.param


@fixture(params=[(0x51, 0x01), [0x50, 0x03, 0x00, 0x50, 0x00, 0x50], [0x54], (0x59, 0x02, 0xCF)])
def example_uds_response_raw_data(request):
    return request.param


@fixture(params=[POSSIBLE_REQUEST_SIDS, [0x10, 0x11, 0x27], (0x22, 0x2E)])
def example_request_sids(request):
    return request.param


@fixture(params=list(AddressingType))
def example_addressing_type(request):
    return request.param


@fixture
def example_addressing_types():
    return list(AddressingType)


@fixture(params=list(TransmissionDirection))
def example_transmission_direction(request):
    return request.param

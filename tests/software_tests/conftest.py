from pytest import fixture

from uds.messages import AddressingType, POSSIBLE_REQUEST_SIDS


@fixture(params=[(0x10, 0x01), [0x11, 0x03], (0x22, 0x10, 0x01), [0x22, 0xF1, 0x83, 0x43, 0xAB], (0x19, 0x02, 0xFF)])
def example_uds_request_raw_data(request):
    return request.param


@fixture(params=[POSSIBLE_REQUEST_SIDS, [0x10, 0x11, 0x27], (0x22, 0x2E)])
def example_request_sids(request):
    return request.param


@fixture
def example_addressing_types():
    return list(AddressingType)

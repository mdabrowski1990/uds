from pytest import fixture

from uds.messages import AddressingType, POSSIBLE_REQUEST_SIDS, UdsRequest, UdsResponse


@fixture(params=[(0x10, 0x01), [0x22, 0xF1, 0x83, 0x43, 0xAB], (0x19, 0x02, 0xFF)])
def example_uds_request_raw_data(request):
    return request.param


@fixture
def example_uds_request(example_uds_request_raw_data):
    return UdsRequest(raw_message=example_uds_request_raw_data)


@fixture(params=[(0x51, 0x01), [0x50, 0x03, 0x00, 0x50, 0x00, 0x50], [0x54], (0x59, 0x02, 0xCF)])
def example_uds_response_raw_data(request):
    return request.param


@fixture
def example_uds_response(example_uds_response_raw_data):
    return UdsResponse(raw_message=example_uds_response_raw_data)


@fixture
def example_uds_request(example_uds_request_raw_data):
    return UdsRequest(raw_message=example_uds_request_raw_data)


@fixture(params=[POSSIBLE_REQUEST_SIDS, [0x10, 0x11, 0x27], (0x22, 0x2E)])
def example_request_sids(request):
    return request.param


@fixture(params=list(AddressingType))
def example_addressing_type(request):
    return request.param


@fixture
def example_addressing_types():
    return list(AddressingType)

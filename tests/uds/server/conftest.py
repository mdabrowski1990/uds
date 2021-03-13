from pytest import fixture

from uds.messages import AddressingType, UdsRequest


@fixture
def example_possible_state_values():
    return {"Default Session", "Programming Session", "Extended Session"}


@fixture
def example_initial_state(example_possible_state_values):
    return list(example_possible_state_values)[-1]


@fixture(params=[(0x10, 0x01), [0x11, 0x03], (0x22, 0x10, 0x01), [0x22, 0xF1, 0x83, 0x43, 0xAB], (0x19, 0x02, 0xFF)])
def example_request_sids(request):
    return request.param


@fixture
def example_addressing_types():
    return list(AddressingType)


@fixture
def example_uds_request_raw_data():
    return [0x10, 0x11]


@fixture
def example_uds_request(example_uds_request_raw_data):
    return UdsRequest(raw_message=example_uds_request_raw_data)

from pytest import fixture

from uds.messages import UdsRequest

SESSIONS = {"Default Session", "Programming Session", "Extended Session"}


@fixture
def example_possible_state_values():
    return SESSIONS


@fixture(params=SESSIONS)
def example_initial_state(request):
    return request.param


@fixture
def example_uds_request(example_uds_request_raw_data):
    return UdsRequest(raw_message=example_uds_request_raw_data)

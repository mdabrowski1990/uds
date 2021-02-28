from pytest import fixture

from uds.messages import AddressingType


@fixture
def example_possible_state_values():
    return {"Default Session", "Programming Session", "Extended Session"}


@fixture
def example_initial_state(example_possible_state_values):
    return list(example_possible_state_values)[-1]


@fixture
def example_request_sids():
    return {0x10, 0x11}


@fixture
def example_addressing_types():
    return list(AddressingType)

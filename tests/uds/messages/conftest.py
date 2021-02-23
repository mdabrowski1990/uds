from pytest import fixture


@fixture
def example_raw_message():
    return [0x10, 0x01]

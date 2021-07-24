from pytest import fixture

SESSIONS = {"Default Session", "Programming Session", "Extended Session"}


@fixture
def example_possible_state_values():
    return SESSIONS


@fixture(params=SESSIONS)
def example_initial_state(request):
    return request.param

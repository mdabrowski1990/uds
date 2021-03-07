import pytest
from mock import Mock

from uds.server.server_state import ServerState


class TestServerState:

    def setup(self):
        self.mock_server_state = Mock(spec=ServerState)

    # __init__

    @pytest.mark.parametrize("name", ["Diagnostic Session", "security_access"])
    @pytest.mark.parametrize("initial_value, possible_values", [
        ("Default Session", {"Default Session", "Programming Session", "Extended Session"}),
        ("locked", ["locked", "level1"]),
        ("default", ("default", "non default"))
    ])
    def test_init__valid(self, name, initial_value, possible_values):
        self.mock_server_state.possible_values = possible_values
        ServerState.__init__(self=self.mock_server_state, state_name=name, initial_value=initial_value)
        assert self.mock_server_state.state_name == name
        assert ServerState.current_value.fget(self.mock_server_state) == initial_value

    @pytest.mark.parametrize("name", [None, 1, b"ABCD"])
    def test_init__invalid_name(self, name, example_initial_state, example_possible_state_values):
        self.mock_server_state.possible_values = example_possible_state_values
        with pytest.raises(TypeError):
            ServerState.__init__(self=self.mock_server_state, state_name=name, initial_value=example_initial_state)

    @pytest.mark.parametrize("name", ["Diagnostic Session", "security_access"])
    @pytest.mark.parametrize("initial_value, possible_values", [
        ("default_session", {"Default Session", "Programming Session", "Extended Session"}),
        (0, ["locked", "level1"]),
        (None, ("default", "non default"))
    ])
    def test_init__invalid_initial_value(self, name, initial_value, possible_values):
        self.mock_server_state.possible_values = possible_values
        with pytest.raises(ValueError):
            ServerState.__init__(self=self.mock_server_state, state_name=name, initial_value=initial_value)
import pytest
from mock import Mock

from uds.server.response_manager import ServerState, ResponseRule, ResponseManager


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


class TestResponseRule:

    def setup(self):
        self.mock_response_rule = Mock(spec=ResponseRule)

    # __init__

    def test_init(self, addressing_types, related_request_sids):
        ResponseRule.__init__(self=self.mock_response_rule, addressing_types=addressing_types,
                              related_request_sids=related_request_sids)
        assert self.mock_response_rule.addressing_types == set(addressing_types)
        assert self.mock_response_rule.related_request_sids == set(related_request_sids)

    @pytest.mark.parametrize("addressing_types", [None, 1, "abcdef"])
    def test_init__invalid_type_addressing_types(self, addressing_types, example_request_sids):
        with pytest.raises(TypeError):
            ResponseRule.__init__(self=self.mock_response_rule, addressing_types=addressing_types,
                                  related_request_sids=example_request_sids)

    @pytest.mark.parametrize("addressing_types", [
        [None],
        {1, 2, 3, 4},
        ("xyz", "abcd")
    ])
    def test_init__invalid_value_addressing_types(self, addressing_types, example_request_sids):
        with pytest.raises(ValueError):
            ResponseRule.__init__(self=self.mock_response_rule, addressing_types=addressing_types,
                                  related_request_sids=example_request_sids)

    @pytest.mark.parametrize("related_request_sids", [None, 1, "abcdef"])
    def test_init__invalid_type_related_request_sids(self, example_addressing_types, related_request_sids):
        with pytest.raises(TypeError):
            ResponseRule.__init__(self=self.mock_response_rule, addressing_types=example_addressing_types,
                                  related_request_sids=related_request_sids)

    @pytest.mark.parametrize("related_request_sids", [
        [None],
        {1.5, 2, 3, 4},
        ("xyz", "abcd")
    ])
    def test_init__invalid_value_related_request_sids(self, example_addressing_types, related_request_sids):
        with pytest.raises(ValueError):
            ResponseRule.__init__(self=self.mock_response_rule, addressing_types=example_addressing_types,
                                  related_request_sids=related_request_sids)

    # addressing_types

    def test_addressing_types__cannot_change(self, example_addressing_types):
        with pytest.raises(Exception):
            ResponseRule.addressing_types.fset(self.mock_response_rule, example_addressing_types)

    # related_request_sids

    def test_related_request_sids__cannot_change(self, example_request_sids):
        with pytest.raises(Exception):
            ResponseRule.related_request_sids.fset(self.mock_response_rule, example_request_sids)

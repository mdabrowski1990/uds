import pytest
from mock import Mock, patch

from uds.diagnostic_configuration.state import State

SCRIPT_LOCATION = "uds.diagnostic_configuration.state"


class TestState:
    """Unit tests for 'State' class."""

    def setup_method(self):
        self.mock_state = Mock(spec=State)
        # patching
        self._patcher_set = patch(f"{SCRIPT_LOCATION}.set")
        self.mock_set = self._patcher_set.start()
        self._patcher_warn = patch(f"{SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()

    def teardown_method(self):
        self._patcher_set.stop()
        self._patcher_warn.stop()

    # __init__

    @pytest.mark.parametrize("name, possible_values", [
        ("Some name", {1, 2, 3},),
        (Mock(), Mock()),
    ])
    def test_init(self, name, possible_values):
        assert State.__init__(self.mock_state,
                              name=name,
                              possible_values=possible_values) is None
        assert self.mock_state.name == name
        assert self.mock_state.possible_values == possible_values
        assert self.mock_state._State__current_value is None

    # name

    def test_name__get(self):
        self.mock_state._State__name = Mock()
        assert State.name.fget(self.mock_state) == self.mock_state._State__name
        
    @pytest.mark.parametrize("name", [
        Mock(),
        None
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_name__set__type_error(self, mock_isinstance, name):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            State.name.fset(self.mock_state, name)
        mock_isinstance.assert_called_once_with(name, str)

    @pytest.mark.parametrize("name", [
        " \t\n ", ""
    ])
    def test_name__set__value_error(self, name):
        with pytest.raises(ValueError):
            State.name.fset(self.mock_state, name)

    @pytest.mark.parametrize("name", [
        "Example name",
        "Something"
    ])
    def test_name__set__valid__without_warning(self, name):
        assert State.name.fset(self.mock_state, name) is None
        assert self.mock_state._State__name == name
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("name", [
        "\tExample name\n",
        " Something"
    ])
    def test_name__set__valid__with_warning(self, name):
        assert State.name.fset(self.mock_state, name) is None
        assert self.mock_state._State__name == name.strip()
        self.mock_warn.assert_called_once()

    # possible_values

    def test_possible_values__get(self):
        self.mock_state._State__possible_values = Mock()
        assert State.possible_values.fget(self.mock_state) == self.mock_state._State__possible_values

    @pytest.mark.parametrize("possible_values", [
        ("State 1", "State 2"),
        range(0x80)
    ])
    def test_possible_values__set(self, possible_values):
        assert State.possible_values.fset(self.mock_state, possible_values) is None
        assert self.mock_state._State__possible_values == self.mock_set.return_value
        self.mock_set.assert_called_once_with(possible_values)

    # current_value

    def test_current_value__get(self):
        self.mock_state._State__current_value = Mock()
        assert State.current_value.fget(self.mock_state) == self.mock_state._State__current_value

    @pytest.mark.parametrize("current_value, possible_values", [
        ("abc", {"State 1", "State 2, State 3"}),
        (0x80, range(0x80)),
    ])
    def test_current_value__set__value_error(self, current_value, possible_values):
        self.mock_state.possible_values = possible_values
        with pytest.raises(ValueError):
            State.current_value.fset(self.mock_state, current_value)

    @pytest.mark.parametrize("current_value, possible_values", [
        ("State 1", {"State 1", "State 2, State 3"}),
        (0x5, range(0x80)),
        (None, range(0x80)),
    ])
    def test_current_value__set__valid(self, current_value, possible_values):
        self.mock_state.possible_values = possible_values
        assert State.current_value.fset(self.mock_state, current_value) is None
        assert self.mock_state._State__current_value == current_value

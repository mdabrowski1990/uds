import pytest
from mock import Mock, patch, MagicMock

from uds.diagnostic_configuration.ecu_configuration import EcuDiagnosticConfiguration, ReassignmentError

SCRIPT_LOCATION = "uds.diagnostic_configuration.ecu_configuration"


class TestState:
    """Unit tests for 'EcuDiagnosticConfiguration' class."""

    def setup_method(self):
        self.mock_ecu_diagnostic_configuration = Mock(spec=EcuDiagnosticConfiguration)
        # patching
        self._patcher_set = patch(f"{SCRIPT_LOCATION}.set")
        self.mock_set = self._patcher_set.start()

    def teardown_method(self):
        self._patcher_set.stop()

    # __init__

    @pytest.mark.parametrize("states, sid_restrictions, subfunction_restrictions, did_restrictions, rid_restrictions", [
        ("states", "sid_restrictions", "subfunction_restrictions", "did_restrictions", "rid_restrictions"),
        (Mock(), Mock(), Mock(), Mock(), Mock()),
    ])
    def test_init(self, states, sid_restrictions, subfunction_restrictions, did_restrictions, rid_restrictions):
        assert EcuDiagnosticConfiguration.__init__(self.mock_ecu_diagnostic_configuration,
                                                   states=states,
                                                   sid_restrictions=sid_restrictions,
                                                   subfunction_restrictions=subfunction_restrictions,
                                                   did_restrictions=did_restrictions,
                                                   rid_restrictions=rid_restrictions) is None
        assert self.mock_ecu_diagnostic_configuration.states == states
        assert self.mock_ecu_diagnostic_configuration.sid_restrictions == sid_restrictions
        assert self.mock_ecu_diagnostic_configuration.subfunction_restrictions == subfunction_restrictions
        assert self.mock_ecu_diagnostic_configuration.did_restrictions == did_restrictions
        assert self.mock_ecu_diagnostic_configuration.rid_restrictions == rid_restrictions

    # __getitem__

    @pytest.mark.parametrize("states_mapping", [
        {"State 1": Mock(), "State 2": Mock()},
        {"A": Mock(), "B": Mock()}
    ])
    def test_getitem(self, states_mapping):
        self.mock_ecu_diagnostic_configuration.states_mapping = states_mapping
        for state_name, state in states_mapping.items():
            assert EcuDiagnosticConfiguration.__getitem__(self.mock_ecu_diagnostic_configuration, state_name) == state

    # states

    def test_states__get(self):
        self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__states = Mock()
        assert (EcuDiagnosticConfiguration.states.fget(self.mock_ecu_diagnostic_configuration)
                == self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__states)

    @patch(f"{SCRIPT_LOCATION}.hasattr")
    def test_states__set__reassignment_error(self, mock_hasattr):
        mock_hasattr.return_value = True
        with pytest.raises(ReassignmentError):
            EcuDiagnosticConfiguration.states.fset(self.mock_ecu_diagnostic_configuration, MagicMock())
        mock_hasattr.assert_called_once_with(self.mock_ecu_diagnostic_configuration,
                                             f"_{EcuDiagnosticConfiguration.__name__}__states")

    @pytest.mark.parametrize("states", [
        (Mock(), Mock()),
        {"State 1", "State 2", "State 3"},
    ])
    def test_states__get__valid(self, states):
        assert EcuDiagnosticConfiguration.states.fset(self.mock_ecu_diagnostic_configuration, states) is None
        assert self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__states == self.mock_set.return_value
        self.mock_set.assert_called_once_with(states)

    # states_names

    def test_states_names__get(self):
        self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__states_names = Mock()
        assert (EcuDiagnosticConfiguration.states_names.fget(self.mock_ecu_diagnostic_configuration)
                == self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__states_names)

    # states_mapping

    def test_states_mapping__get(self):
        self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__states_mapping = Mock()
        assert (EcuDiagnosticConfiguration.states_mapping.fget(self.mock_ecu_diagnostic_configuration)
                == self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__states_mapping)

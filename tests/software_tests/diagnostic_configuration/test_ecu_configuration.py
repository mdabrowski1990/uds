import pytest
from mock import MagicMock, Mock, call, patch

from uds.diagnostic_configuration.ecu_configuration import (
    SERVICES_WITH_DID,
    SERVICES_WITH_RID,
    SERVICES_WITH_SUBFUNCTION,
    EcuDiagnosticConfiguration,
    InconsistencyError,
    Mapping,
    ReassignmentError,
)

SCRIPT_LOCATION = "uds.diagnostic_configuration.ecu_configuration"


class TestState:
    """Unit tests for 'EcuDiagnosticConfiguration' class."""

    def setup_method(self):
        self.mock_ecu_diagnostic_configuration = Mock(spec=EcuDiagnosticConfiguration)
        # patching
        self._patcher_set = patch(f"{SCRIPT_LOCATION}.set")
        self.mock_set = self._patcher_set.start()
        self._patcher_mapping_proxy_type = patch(f"{SCRIPT_LOCATION}.MappingProxyType")
        self.mock_mapping_proxy_type = self._patcher_mapping_proxy_type.start()
        self._patcher_validate_raw_byte = patch(f"{SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
        self._patcher_validate_raw_2byte_value = patch(f"{SCRIPT_LOCATION}.validate_raw_2byte_value")
        self.mock_validate_raw_2byte_value = self._patcher_validate_raw_2byte_value.start()
        self._patcher_is_request_sid = patch(f"{SCRIPT_LOCATION}.RequestSID.is_request_sid")
        self.mock_is_request_sid = self._patcher_is_request_sid.start()
        self._patcher_is_response_sid = patch(f"{SCRIPT_LOCATION}.ResponseSID.is_response_sid")
        self.mock_is_response_sid = self._patcher_is_response_sid.start()

    def teardown_method(self):
        self._patcher_set.stop()
        self._patcher_mapping_proxy_type.stop()
        self._patcher_validate_raw_byte.stop()
        self._patcher_validate_raw_2byte_value.stop()
        self._patcher_is_request_sid.stop()
        self._patcher_is_response_sid.stop()

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

    # sid_restrictions

    def test_sid_restrictions__get(self):
        self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__sid_restrictions = Mock()
        assert (EcuDiagnosticConfiguration.sid_restrictions.fget(self.mock_ecu_diagnostic_configuration)
                == self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__sid_restrictions)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_sid_restrictions__set__type_error(self, mock_isinstance):
        mock_value = Mock()
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            EcuDiagnosticConfiguration.sid_restrictions.fset(self.mock_ecu_diagnostic_configuration, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, Mapping)

    @pytest.mark.parametrize("value", [
        {1: Mock()},
        {0xFF: Mock(), 0xFE: Mock()},
    ])
    def test_sid_restrictions__set__value_error(self, value):
        self.mock_is_request_sid.return_value = False
        self.mock_is_response_sid.return_value = False
        with pytest.raises(ValueError):
            EcuDiagnosticConfiguration.sid_restrictions.fset(self.mock_ecu_diagnostic_configuration, value=value)

    @pytest.mark.parametrize("is_request_sid, is_response_sid, value", [
        (True, False, {1: Mock()}),
        (False, True, {0xFF: Mock(), 0xFE: Mock()}),
    ])
    def test_sid_restrictions__set__valid(self, is_request_sid, is_response_sid, value):
        self.mock_is_request_sid.return_value = is_request_sid
        self.mock_is_response_sid.return_value = is_response_sid
        assert EcuDiagnosticConfiguration.sid_restrictions.fset(self.mock_ecu_diagnostic_configuration,
                                                                value=value) is None
        assert (self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__sid_restrictions
                == self.mock_mapping_proxy_type.return_value)
        self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__validate_required_states.assert_has_calls(
            [call(v) for v in value.values()], any_order=True)

    # subfunction_restrictions

    def test_subfunction_restrictions__get(self):
        self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__subfunction_restrictions = Mock()
        assert (EcuDiagnosticConfiguration.subfunction_restrictions.fget(self.mock_ecu_diagnostic_configuration)
                == self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__subfunction_restrictions)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_subfunction_restrictions__set__type_error(self, mock_isinstance):
        mock_value = Mock()
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            EcuDiagnosticConfiguration.subfunction_restrictions.fset(self.mock_ecu_diagnostic_configuration, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, Mapping)

    @pytest.mark.parametrize("value", [
        {1: Mock()},
        {0xFF: Mock(), 0xFE: Mock()},
    ])
    def test_subfunction_restrictions__set__value_error(self, value):
        self.mock_is_request_sid.return_value = False
        self.mock_is_response_sid.return_value = False
        with pytest.raises(ValueError):
            EcuDiagnosticConfiguration.subfunction_restrictions.fset(self.mock_ecu_diagnostic_configuration,
                                                                     value=value)

    @pytest.mark.parametrize("value", [
        {0: Mock()},
        {0x100: Mock()},
    ])
    def test_subfunction_restrictions__set__inconsistency_error(self, value):
        self.mock_is_request_sid.return_value = True
        self.mock_is_response_sid.return_value = True
        with pytest.raises(InconsistencyError):
            EcuDiagnosticConfiguration.subfunction_restrictions.fset(self.mock_ecu_diagnostic_configuration,
                                                                     value=value)

    @pytest.mark.parametrize("is_request_sid, is_response_sid, value", [
        (True, False, {list(SERVICES_WITH_SUBFUNCTION)[0]: {0x00: Mock()}}),
        (False, True, {list(SERVICES_WITH_SUBFUNCTION)[-1]: {0x01: Mock()},
                       list(SERVICES_WITH_SUBFUNCTION)[-2]: {0x00: Mock(), 0x01: Mock(), 0x7F: Mock()}}),
    ])
    def test_subfunction_restrictions__set__valid(self, is_request_sid, is_response_sid, value):
        self.mock_is_request_sid.return_value = is_request_sid
        self.mock_is_response_sid.return_value = is_response_sid
        assert EcuDiagnosticConfiguration.subfunction_restrictions.fset(self.mock_ecu_diagnostic_configuration,
                                                                        value=value) is None
        assert (self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__subfunction_restrictions
                == self.mock_mapping_proxy_type.return_value)
        self.mock_validate_raw_byte.assert_has_calls(
            [call(subfunction)
             for subfunction_required_states in value.values()
             for subfunction in subfunction_required_states.keys()], any_order=True)
        self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__validate_required_states.assert_has_calls(
            [call(required_states)
             for subfunction_required_states in value.values()
             for required_states in subfunction_required_states.values()], any_order=True)

    # did_restrictions

    def test_did_restrictions__get(self):
        self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__did_restrictions = Mock()
        assert (EcuDiagnosticConfiguration.did_restrictions.fget(self.mock_ecu_diagnostic_configuration)
                == self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__did_restrictions)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_did_restrictions__set__type_error(self, mock_isinstance):
        mock_value = Mock()
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            EcuDiagnosticConfiguration.did_restrictions.fset(self.mock_ecu_diagnostic_configuration, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, Mapping)

    @pytest.mark.parametrize("value", [
        {1: Mock()},
        {0xFF: Mock(), 0xFE: Mock()},
    ])
    def test_did_restrictions__set__value_error(self, value):
        self.mock_is_request_sid.return_value = False
        self.mock_is_response_sid.return_value = False
        with pytest.raises(ValueError):
            EcuDiagnosticConfiguration.did_restrictions.fset(self.mock_ecu_diagnostic_configuration,
                                                                     value=value)

    @pytest.mark.parametrize("value", [
        {0: Mock()},
        {0x100: Mock()},
    ])
    def test_did_restrictions__set__inconsistency_error(self, value):
        self.mock_is_request_sid.return_value = True
        self.mock_is_response_sid.return_value = True
        with pytest.raises(InconsistencyError):
            EcuDiagnosticConfiguration.did_restrictions.fset(self.mock_ecu_diagnostic_configuration,
                                                                     value=value)

    @pytest.mark.parametrize("is_request_sid, is_response_sid, value", [
        (True, False, {list(SERVICES_WITH_DID)[0]: {0x0000: Mock()}}),
        (False, True, {list(SERVICES_WITH_DID)[-1]: {0xFFFF: Mock()},
                       list(SERVICES_WITH_DID)[-2]: {0x1234: Mock(), 0xF100: Mock(), 0x5A60: Mock()}}),
    ])
    def test_did_restrictions__set__valid(self, is_request_sid, is_response_sid, value):
        self.mock_is_request_sid.return_value = is_request_sid
        self.mock_is_response_sid.return_value = is_response_sid
        assert EcuDiagnosticConfiguration.did_restrictions.fset(self.mock_ecu_diagnostic_configuration,
                                                                value=value) is None
        assert (self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__did_restrictions
                == self.mock_mapping_proxy_type.return_value)
        self.mock_validate_raw_2byte_value.assert_has_calls(
            [call(did)
             for did_required_states in value.values()
             for did in did_required_states.keys()], any_order=True)
        self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__validate_required_states.assert_has_calls(
            [call(required_states)
             for did_required_states in value.values()
             for required_states in did_required_states.values()], any_order=True)

    # rid_restrictions

    def test_rid_restrictions__get(self):
        self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__rid_restrictions = Mock()
        assert (EcuDiagnosticConfiguration.rid_restrictions.fget(self.mock_ecu_diagnostic_configuration)
                == self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__rid_restrictions)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_rid_restrictions__set__type_error(self, mock_isinstance):
        mock_value = Mock()
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            EcuDiagnosticConfiguration.rid_restrictions.fset(self.mock_ecu_diagnostic_configuration, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, Mapping)

    @pytest.mark.parametrize("value", [
        {1: Mock()},
        {0xFF: Mock(), 0xFE: Mock()},
    ])
    def test_rid_restrictions__set__value_error(self, value):
        self.mock_is_request_sid.return_value = False
        self.mock_is_response_sid.return_value = False
        with pytest.raises(ValueError):
            EcuDiagnosticConfiguration.rid_restrictions.fset(self.mock_ecu_diagnostic_configuration,
                                                                     value=value)

    @pytest.mark.parametrize("value", [
        {0: Mock()},
        {0x100: Mock()},
    ])
    def test_rid_restrictions__set__inconsistency_error(self, value):
        self.mock_is_request_sid.return_value = True
        self.mock_is_response_sid.return_value = True
        with pytest.raises(InconsistencyError):
            EcuDiagnosticConfiguration.rid_restrictions.fset(self.mock_ecu_diagnostic_configuration,
                                                                     value=value)

    @pytest.mark.parametrize("is_request_sid, is_response_sid, value", [
        (True, False, {list(SERVICES_WITH_RID)[0]: {0x0000: Mock()}}),
        (False, True, {list(SERVICES_WITH_RID)[-1]: {0xFFFF: Mock()},
                       list(SERVICES_WITH_RID)[-2]: {0x1234: Mock(), 0xF100: Mock(), 0x5A60: Mock()}}),
    ])
    def test_rid_restrictions__set__valid(self, is_request_sid, is_response_sid, value):
        self.mock_is_request_sid.return_value = is_request_sid
        self.mock_is_response_sid.return_value = is_response_sid
        assert EcuDiagnosticConfiguration.rid_restrictions.fset(self.mock_ecu_diagnostic_configuration,
                                                                value=value) is None
        assert (self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__rid_restrictions
                == self.mock_mapping_proxy_type.return_value)
        self.mock_validate_raw_2byte_value.assert_has_calls(
            [call(rid)
             for rid_required_states in value.values()
             for rid in rid_required_states.keys()], any_order=True)
        self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__validate_required_states.assert_has_calls(
            [call(required_states)
             for rid_required_states in value.values()
             for required_states in rid_required_states.values()], any_order=True)

    # __validate_required_states

    # TODO

    # get_restrictions

    # TODO
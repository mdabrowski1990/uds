import pytest
from mock import MagicMock, Mock, call, patch

from uds.addressing import AddressingType
from uds.diagnostic_configuration.ecu_configuration import (
    SERVICES_WITH_DID,
    SERVICES_WITH_RID,
    SERVICES_WITH_SUBFUNCTION,
    SUBFUNCTION_MASK,
    EcuDiagnosticConfiguration,
    InconsistencyError,
    Mapping,
    ReassignmentError,
)
from uds.diagnostic_configuration.state_definitions import (
    DEFAULT_ADDRESSING_TYPE_STATE,
    DEFAULT_DIAGNOSTIC_SESSION_STATE,
    DEFAULT_SECURITY_ACCESS_STATE,
)

SCRIPT_LOCATION = "uds.diagnostic_configuration.ecu_configuration"


class TestEcuDiagnosticConfiguration:
    """Unit tests for 'EcuDiagnosticConfiguration' class."""

    def setup_method(self):
        self.mock_ecu_diagnostic_configuration = Mock(spec=EcuDiagnosticConfiguration)
        # patching
        self._patcher_set = patch(f"{SCRIPT_LOCATION}.set")
        self.mock_set = self._patcher_set.start()
        self._patcher_frozenset = patch(f"{SCRIPT_LOCATION}.frozenset")
        self.mock_frozenset = self._patcher_frozenset.start()
        self._patcher_mapping_proxy_type = patch(f"{SCRIPT_LOCATION}.MappingProxyType")
        self.mock_mapping_proxy_type = self._patcher_mapping_proxy_type.start()
        self._patcher_getitem = patch(f"{SCRIPT_LOCATION}.getitem")
        self.mock_getitem = self._patcher_getitem.start()
        self._patcher_validate_raw_byte = patch(f"{SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
        self._patcher_validate_raw_2byte_value = patch(f"{SCRIPT_LOCATION}.validate_raw_2byte_value")
        self.mock_validate_raw_2byte_value = self._patcher_validate_raw_2byte_value.start()
        self._patcher_is_request_sid = patch(f"{SCRIPT_LOCATION}.RequestSID.is_request_sid")
        self.mock_is_request_sid = self._patcher_is_request_sid.start()
        self._patcher_is_response_sid = patch(f"{SCRIPT_LOCATION}.ResponseSID.is_response_sid")
        self.mock_is_response_sid = self._patcher_is_response_sid.start()
        self._patcher_translator_decode = patch(f"{SCRIPT_LOCATION}.BASE_TRANSLATOR.decode")
        self.mock_translator_decode = self._patcher_translator_decode.start()

    def teardown_method(self):
        self._patcher_set.stop()
        self._patcher_frozenset.stop()
        self._patcher_mapping_proxy_type.stop()
        self._patcher_getitem.stop()
        self._patcher_validate_raw_byte.stop()
        self._patcher_validate_raw_2byte_value.stop()
        self._patcher_is_request_sid.stop()
        self._patcher_is_response_sid.stop()
        self._patcher_translator_decode.stop()

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
    def test_states__set__valid(self, states):
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

    @pytest.mark.parametrize("required_states", [
        {"State 1": Mock()},
        {"A": Mock(), "B": Mock(), "C": Mock()},
    ])
    def test_validate_required_states__inconsistency_error__state_name(self, required_states):
        mock_contains = Mock(return_value=False)
        self.mock_ecu_diagnostic_configuration.states_names = MagicMock(__contains__=mock_contains)
        with pytest.raises(InconsistencyError):
            EcuDiagnosticConfiguration._EcuDiagnosticConfiguration__validate_required_states(
                self.mock_ecu_diagnostic_configuration, required_states)
        mock_contains.assert_called_once()

    @pytest.mark.parametrize("required_states", [
        {"State 1": Mock()},
        {"A": Mock(), "B": Mock(), "C": Mock()},
    ])
    def test_validate_required_states__inconsistency_error__possible_values(self, required_states):
        mock_contains = Mock(return_value=True)
        self.mock_ecu_diagnostic_configuration.states_names = MagicMock(__contains__=mock_contains)
        mock_issuperset = Mock(return_value=False)
        mock_state = Mock(possible_values=Mock(issuperset=mock_issuperset))
        self.mock_getitem.return_value = mock_state
        with pytest.raises(InconsistencyError):
            EcuDiagnosticConfiguration._EcuDiagnosticConfiguration__validate_required_states(
                self.mock_ecu_diagnostic_configuration, required_states)
        mock_contains.assert_called_once()
        self.mock_getitem.assert_called_once()
        mock_issuperset.assert_called_once()

    @pytest.mark.parametrize("required_states", [
        {"State 1": Mock()},
        {"A": Mock(), "B": Mock(), "C": Mock()},
    ])
    def test_validate_required_states__valid(self, required_states):
        mock_contains = Mock(return_value=True)
        self.mock_ecu_diagnostic_configuration.states_names = MagicMock(__contains__=mock_contains)
        mock_issuperset = Mock(return_value=True)
        mock_state = Mock(possible_values=Mock(issuperset=mock_issuperset))
        self.mock_getitem.return_value = mock_state
        assert EcuDiagnosticConfiguration._EcuDiagnosticConfiguration__validate_required_states(
            self.mock_ecu_diagnostic_configuration, required_states) == self.mock_mapping_proxy_type.return_value
        mock_contains.assert_has_calls([call(state_name) for state_name in required_states.keys()], any_order=True)
        self.mock_getitem.assert_has_calls([call(self.mock_ecu_diagnostic_configuration, state_name)
                                            for state_name in required_states.keys()], any_order=True)
        mock_issuperset.assert_has_calls([call(values) for values in required_states.values()], any_order=True)
        self.mock_frozenset.assert_has_calls([call(value) for value in required_states.values()], any_order=True)
        self.mock_mapping_proxy_type.assert_called_once_with({
            state_name: self.mock_frozenset.return_value for state_name in required_states.keys()
        })

    # __extract_subfunction

    @pytest.mark.parametrize("message_payload", [
        (0x22, 0x12, 0x34),
        (0xFF, 0x00),
    ])
    def test_extract_subfunction__wrong_service(self, message_payload):
        assert EcuDiagnosticConfiguration._EcuDiagnosticConfiguration__extract_subfunction(message_payload) is None

    @pytest.mark.parametrize("message_payload", [
        (list(SERVICES_WITH_SUBFUNCTION)[0],),
        (list(SERVICES_WITH_SUBFUNCTION)[-1],),
    ])
    def test_extract_subfunction__too_short(self, message_payload):
        assert EcuDiagnosticConfiguration._EcuDiagnosticConfiguration__extract_subfunction(message_payload) is None

    @pytest.mark.parametrize("message_payload", [
        (list(SERVICES_WITH_SUBFUNCTION)[0], 0x01),
        (list(SERVICES_WITH_SUBFUNCTION)[0], 0xCF, *range(100)),
    ])
    def test_extract_subfunction(self, message_payload):
        assert (EcuDiagnosticConfiguration._EcuDiagnosticConfiguration__extract_subfunction(message_payload)
                == message_payload[1] & SUBFUNCTION_MASK)

    # __extract_dids

    @pytest.mark.parametrize("decoded_message", [
        ({"raw_value": 0x00}, Mock(), Mock(), Mock()),
        ({"raw_value":0x10}, Mock(), Mock()),
    ])
    def test_extract_dids__wrong_service(self, decoded_message):
        assert (EcuDiagnosticConfiguration._EcuDiagnosticConfiguration__extract_dids(decoded_message)
                == self.mock_set.return_value)
        self.mock_set.return_value.add.assert_not_called()
        self.mock_set.return_value.update.assert_not_called()

    @pytest.mark.parametrize("decoded_message, dids", [
        [
            ({"raw_value": list(SERVICES_WITH_DID)[0], "name": "SID"},
             {"raw_value": 0xF012, "name": "DID"}),
            {0xF012}
        ],
        [
            ({"raw_value": list(SERVICES_WITH_DID)[0], "name": "SID"},
             dict(raw_value=0x9153, name="DID#1"),
             dict(raw_value=0xFFFF, name="DID#2"),
             dict(raw_value=0x0000, name="Not a DID")),
            {0x9153, 0xFFFF}
        ],
    ])
    def test_extract_dids__add(self, decoded_message, dids):
        assert (EcuDiagnosticConfiguration._EcuDiagnosticConfiguration__extract_dids(decoded_message)
                == self.mock_set.return_value)
        self.mock_set.return_value.add.assert_has_calls([call(did) for did in dids], any_order=True)
        self.mock_set.return_value.update.assert_not_called()

    @pytest.mark.parametrize("decoded_message, dids", [
        [
            (dict(raw_value=list(SERVICES_WITH_DID)[0], name="SID"),
             dict(raw_value=(0xF012, 0x0000), name="DID")),
            {(0xF012, 0x0000)}
        ],
        [
            (dict(raw_value=list(SERVICES_WITH_DID)[0], name="SID"),
             dict(raw_value=(0x9153, 0xFFFF), name="DID"),
             dict(raw_value=0x1234, name="Something")),
            {(0x9153, 0xFFFF)}
        ],
    ])
    def test_extract_dids__update(self, decoded_message, dids):
        assert (EcuDiagnosticConfiguration._EcuDiagnosticConfiguration__extract_dids(decoded_message)
                == self.mock_set.return_value)
        self.mock_set.return_value.add.assert_not_called()
        self.mock_set.return_value.update.assert_has_calls([call(did) for did in dids], any_order=True)

    # __extract_rids

    @pytest.mark.parametrize("decoded_message", [
        (dict(raw_value=0x00), Mock(), Mock(), Mock()),
        (dict(raw_value=0x10), Mock(), Mock()),
    ])
    def test_extract_rids__wrong_service(self, decoded_message):
        assert (EcuDiagnosticConfiguration._EcuDiagnosticConfiguration__extract_rids(decoded_message)
                == self.mock_set.return_value)
        self.mock_set.return_value.add.assert_not_called()
        self.mock_set.return_value.update.assert_not_called()

    @pytest.mark.parametrize("decoded_message, rids", [
        [
            (dict(raw_value=list(SERVICES_WITH_RID)[0], name="SID"),
             dict(raw_value=0xF012, name="RID")),
            {0xF012}
        ],
        [
            (dict(raw_value=list(SERVICES_WITH_RID)[0], name="SID"),
             dict(raw_value=0x9153, name="RID#1"),
             dict(raw_value=0xFFFF, name="RID#2"),
             dict(raw_value=0x0000, name="Not a RID")),
            {0x9153, 0xFFFF}
        ],
    ])
    def test_extract_rids__add(self, decoded_message, rids):
        assert (EcuDiagnosticConfiguration._EcuDiagnosticConfiguration__extract_rids(decoded_message)
                == self.mock_set.return_value)
        self.mock_set.return_value.add.assert_has_calls([call(rid) for rid in rids], any_order=True)
        self.mock_set.return_value.update.assert_not_called()

    @pytest.mark.parametrize("decoded_message, rids", [
        [
            (dict(raw_value=list(SERVICES_WITH_RID)[0], name="SID"),
             dict(raw_value=(0xF012, 0x0000), name="RID")),
            {(0xF012, 0x0000)}
        ],
        [
            (dict(raw_value=list(SERVICES_WITH_RID)[0], name="SID"),
             dict(raw_value=(0x9153, 0xFFFF), name="RID"),
             dict(raw_value=0x1234, name="fdkuhtw")),
            {(0x9153, 0xFFFF)}
        ],
    ])
    def test_extract_rids__update(self, decoded_message, rids):
        assert (EcuDiagnosticConfiguration._EcuDiagnosticConfiguration__extract_rids(decoded_message)
                == self.mock_set.return_value)
        self.mock_set.return_value.add.assert_not_called()
        self.mock_set.return_value.update.assert_has_calls([call(rid) for rid in rids], any_order=True)

    # combine_restrictions

    def test_combine_restrictions__value_error(self):
        with pytest.raises(ValueError):
            EcuDiagnosticConfiguration.combine_restrictions(self.mock_ecu_diagnostic_configuration)

    @pytest.mark.parametrize("states_names, possible_values, restrictions", [
        (
                ["State 1", "State 2"],
                [(1, 2, 3, 4, 5), ("ON", "OFF")],
                [
                    {
                        "State 1": {1, 2, 3},
                        "State 2": {"ON", "OFF"},
                    },
                    {
                        "State 1": {1, 2, 3, 4, 5},
                        "State 2": {"ON"},
                    },
                ],
        ),
        (
                ["Session", "Security Access level"],
                [("Default", "Programming", "Extended", "Safety"), (1, 3, 5, 7, 9, 11, 61)],
                [
                    {
                        "Session": {"Default", "Extended", "Safety"},
                    },
                    {
                        "Session": {"Default", "Programming", "Extended", "Safety"},
                        "State 2": {5, 7, 9},
                    },
                ],
        ),
    ])
    def test_combine_restrictions__valid(self, states_names, possible_values, restrictions):
        self.mock_ecu_diagnostic_configuration.states_names = states_names
        self.mock_ecu_diagnostic_configuration.states_mapping = {
            state_name: Mock(possible_values=possible_values[i]) for i, state_name in enumerate(states_names)
        }
        assert EcuDiagnosticConfiguration.combine_restrictions(self.mock_ecu_diagnostic_configuration,
                                                               *restrictions) == {
                   state_name: self.mock_set.intersection.return_value for state_name in states_names
               }

    # get_restrictions

    @pytest.mark.parametrize("message_payload", [[0x10], (0x20, 0x01, 0x23)])
    def test_get_restrictions__sid_only(self, message_payload):
        mock_sid_restrictions = Mock()
        self.mock_translator_decode.side_effect = ValueError
        self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__extract_subfunction = Mock(
            return_value=None)
        self.mock_ecu_diagnostic_configuration.sid_restrictions = MagicMock(
            __getitem__=Mock(return_value=mock_sid_restrictions))
        assert (EcuDiagnosticConfiguration.get_restrictions(self.mock_ecu_diagnostic_configuration, message_payload)
                == self.mock_ecu_diagnostic_configuration.combine_restrictions.return_value)
        self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__extract_subfunction.assert_called_once_with(
            message_payload=message_payload)
        self.mock_ecu_diagnostic_configuration.sid_restrictions.__getitem__.assert_called_once_with(message_payload[0])
        self.mock_ecu_diagnostic_configuration.combine_restrictions.assert_called_once_with(mock_sid_restrictions)

    @pytest.mark.parametrize("message_payload", [[0x10], (0x20, 0x01, 0x23)])
    def test_get_restrictions__sid_subfunction(self, message_payload):
        mock_sid_restrictions = Mock()
        mock_subfunction_restrictions = Mock()
        self.mock_translator_decode.side_effect = ValueError
        self.mock_ecu_diagnostic_configuration.sid_restrictions = MagicMock(
            __getitem__=Mock(return_value=mock_sid_restrictions))
        self.mock_ecu_diagnostic_configuration.subfunction_restrictions = MagicMock(
            __getitem__=Mock(return_value=MagicMock(__getitem__=Mock(return_value=mock_subfunction_restrictions))))
        assert (EcuDiagnosticConfiguration.get_restrictions(self.mock_ecu_diagnostic_configuration, message_payload)
                == self.mock_ecu_diagnostic_configuration.combine_restrictions.return_value)
        self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__extract_subfunction.assert_called_once_with(
            message_payload=message_payload)
        self.mock_ecu_diagnostic_configuration.sid_restrictions.__getitem__.assert_called_once_with(message_payload[0])
        self.mock_ecu_diagnostic_configuration.subfunction_restrictions.__getitem__.assert_called_once_with(
            message_payload[0])
        self.mock_ecu_diagnostic_configuration.subfunction_restrictions.__getitem__.return_value.__getitem__.assert_called_once_with(
            self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__extract_subfunction.return_value)
        self.mock_ecu_diagnostic_configuration.combine_restrictions.assert_called_once_with(
            mock_sid_restrictions,
            mock_subfunction_restrictions)

    @pytest.mark.parametrize("message_payload, dids, rids", [
        ((0x20, 0x01, 0x23), [0x0000], []),
        ((0x20, 0x01, 0x23), [], [0xFFFF]),
        ([0x22, 0x12, 0x34, 0x56, 0x78], [0xF0E1, 0x5AB9], [0x258C, 0x94A0, 0xFD8E]),
    ])
    def test_get_restrictions__sid_dids_rids(self, message_payload, dids, rids):
        mock_sid_restrictions = Mock()
        mock_did_restrictions = Mock()
        mock_rid_restrictions = Mock()
        self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__extract_subfunction = Mock(
            return_value=None)
        self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__extract_dids = Mock(return_value=dids)
        self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__extract_rids = Mock(return_value=rids)
        self.mock_ecu_diagnostic_configuration.sid_restrictions = MagicMock(
            __getitem__=Mock(return_value=mock_sid_restrictions))
        self.mock_ecu_diagnostic_configuration.did_restrictions = MagicMock(
            __getitem__=Mock(return_value=MagicMock(__getitem__=Mock(return_value=mock_did_restrictions))))
        self.mock_ecu_diagnostic_configuration.rid_restrictions = MagicMock(
            __getitem__=Mock(return_value=MagicMock(__getitem__=Mock(return_value=mock_rid_restrictions))))
        assert (EcuDiagnosticConfiguration.get_restrictions(self.mock_ecu_diagnostic_configuration, message_payload)
                == self.mock_ecu_diagnostic_configuration.combine_restrictions.return_value)
        self.mock_ecu_diagnostic_configuration._EcuDiagnosticConfiguration__extract_subfunction.assert_called_once_with(
            message_payload=message_payload)
        self.mock_ecu_diagnostic_configuration.sid_restrictions.__getitem__.assert_called_once_with(message_payload[0])
        self.mock_ecu_diagnostic_configuration.did_restrictions.__getitem__.return_value.__getitem__.assert_has_calls(
            [call(did) for did in dids], any_order=True)
        self.mock_ecu_diagnostic_configuration.rid_restrictions.__getitem__.return_value.__getitem__.assert_has_calls(
            [call(rid) for rid in rids], any_order=True)
        self.mock_ecu_diagnostic_configuration.combine_restrictions.assert_called_once_with(
            mock_sid_restrictions, *[mock_did_restrictions] * len(dids), *[mock_rid_restrictions] * len(rids))


class TestEcuDiagnosticConfigurationIntegration:
    """Integration tests for 'EcuDiagnosticConfiguration' class."""

    EXAMPLE_STATES = (DEFAULT_DIAGNOSTIC_SESSION_STATE, DEFAULT_SECURITY_ACCESS_STATE, DEFAULT_ADDRESSING_TYPE_STATE)
    EXAMPLE_SID_RESTRICTIONS = {
        0x10: {
            DEFAULT_DIAGNOSTIC_SESSION_STATE.name: DEFAULT_DIAGNOSTIC_SESSION_STATE.possible_values,
            DEFAULT_SECURITY_ACCESS_STATE.name: DEFAULT_SECURITY_ACCESS_STATE.possible_values,
            DEFAULT_ADDRESSING_TYPE_STATE.name: DEFAULT_ADDRESSING_TYPE_STATE.possible_values,
        },
        0x22: {
            DEFAULT_DIAGNOSTIC_SESSION_STATE.name: {0x01, 0x03, 0x04},
            DEFAULT_SECURITY_ACCESS_STATE.name: DEFAULT_SECURITY_ACCESS_STATE.possible_values,
            DEFAULT_ADDRESSING_TYPE_STATE.name: DEFAULT_ADDRESSING_TYPE_STATE.possible_values,
        },
        0x2E: {
            DEFAULT_DIAGNOSTIC_SESSION_STATE.name: {0x03, 0x04},
            DEFAULT_SECURITY_ACCESS_STATE.name: {0x01, 0x03, 0x05},
            DEFAULT_ADDRESSING_TYPE_STATE.name: {AddressingType.PHYSICAL},
        },
        0x31: {
            DEFAULT_DIAGNOSTIC_SESSION_STATE.name: {0x02, 0x03, 0x04},
            DEFAULT_SECURITY_ACCESS_STATE.name: {0x01, 0x03, 0x05},
            DEFAULT_ADDRESSING_TYPE_STATE.name: {AddressingType.PHYSICAL},
        }
    }
    EXAMPLE_SUBFUNCTION_RESTRICTIONS = {
        0x10: {
            0x01: {
                DEFAULT_DIAGNOSTIC_SESSION_STATE.name: DEFAULT_DIAGNOSTIC_SESSION_STATE.possible_values,
                DEFAULT_SECURITY_ACCESS_STATE.name: DEFAULT_SECURITY_ACCESS_STATE.possible_values,
                DEFAULT_ADDRESSING_TYPE_STATE.name: DEFAULT_ADDRESSING_TYPE_STATE.possible_values,
            },
            0x02: {
                DEFAULT_DIAGNOSTIC_SESSION_STATE.name: DEFAULT_DIAGNOSTIC_SESSION_STATE.possible_values,
                DEFAULT_SECURITY_ACCESS_STATE.name: DEFAULT_SECURITY_ACCESS_STATE.possible_values,
                DEFAULT_ADDRESSING_TYPE_STATE.name: DEFAULT_ADDRESSING_TYPE_STATE.possible_values,
            },
            0x03: {
                DEFAULT_DIAGNOSTIC_SESSION_STATE.name: {0x01, 0x03, 0x04},
                DEFAULT_SECURITY_ACCESS_STATE.name: DEFAULT_SECURITY_ACCESS_STATE.possible_values,
                DEFAULT_ADDRESSING_TYPE_STATE.name: DEFAULT_ADDRESSING_TYPE_STATE.possible_values,
            },
            0x04: {
                DEFAULT_DIAGNOSTIC_SESSION_STATE.name: {0x01, 0x03, 0x04},
                DEFAULT_SECURITY_ACCESS_STATE.name: DEFAULT_SECURITY_ACCESS_STATE.possible_values,
                DEFAULT_ADDRESSING_TYPE_STATE.name: DEFAULT_ADDRESSING_TYPE_STATE.possible_values,
            },
        },
        0x31: {
            0x01: {
                DEFAULT_DIAGNOSTIC_SESSION_STATE.name: {0x02, 0x03, 0x04},
                DEFAULT_SECURITY_ACCESS_STATE.name: {0x01, 0x03, 0x05},
                DEFAULT_ADDRESSING_TYPE_STATE.name: {AddressingType.PHYSICAL},
            },
            0x02: {
                DEFAULT_DIAGNOSTIC_SESSION_STATE.name: {0x02, 0x03, 0x04},
                DEFAULT_SECURITY_ACCESS_STATE.name: {0x01, 0x03, 0x05},
                DEFAULT_ADDRESSING_TYPE_STATE.name: {AddressingType.PHYSICAL},
            },
            0x03: {
                DEFAULT_DIAGNOSTIC_SESSION_STATE.name: {0x02, 0x03, 0x04},
                DEFAULT_SECURITY_ACCESS_STATE.name: {0x01, 0x03, 0x05},
                DEFAULT_ADDRESSING_TYPE_STATE.name: {AddressingType.PHYSICAL},
            },
        },
    }
    EXAMPLE_DID_RESTRICTIONS = {
        0x22: {
            0x0100: {
                DEFAULT_DIAGNOSTIC_SESSION_STATE.name: {0x03, 0x04},
                DEFAULT_SECURITY_ACCESS_STATE.name: DEFAULT_SECURITY_ACCESS_STATE.possible_values,
                DEFAULT_ADDRESSING_TYPE_STATE.name: {AddressingType.PHYSICAL},
            },
            0xF186: {
                DEFAULT_DIAGNOSTIC_SESSION_STATE.name: DEFAULT_DIAGNOSTIC_SESSION_STATE.possible_values,
                DEFAULT_SECURITY_ACCESS_STATE.name: DEFAULT_SECURITY_ACCESS_STATE.possible_values,
                DEFAULT_ADDRESSING_TYPE_STATE.name: DEFAULT_ADDRESSING_TYPE_STATE.possible_values,
            },
        },
        0x2E: {
            0x0100: {
                DEFAULT_DIAGNOSTIC_SESSION_STATE.name: {0x03, 0x04},
                DEFAULT_SECURITY_ACCESS_STATE.name: {0x01, 0x03, 0x05},
                DEFAULT_ADDRESSING_TYPE_STATE.name: {AddressingType.PHYSICAL},
            },
        }
    }
    EXAMPLE_RID_RESTRICTIONS = {
        0x31: {
            0x1234: {
                DEFAULT_DIAGNOSTIC_SESSION_STATE.name: {0x02},
                DEFAULT_SECURITY_ACCESS_STATE.name: {0x01},
                DEFAULT_ADDRESSING_TYPE_STATE.name: {AddressingType.PHYSICAL},
            },
            0xABCD: {
                DEFAULT_DIAGNOSTIC_SESSION_STATE.name: {0x03, 0x4},
                DEFAULT_SECURITY_ACCESS_STATE.name: {0x03, 0x05},
                DEFAULT_ADDRESSING_TYPE_STATE.name: {AddressingType.PHYSICAL},
            },
        },
    }

    def test_init(self):
        ecu_diag_config = EcuDiagnosticConfiguration(states=self.EXAMPLE_STATES,
                                                     sid_restrictions=self.EXAMPLE_SID_RESTRICTIONS,
                                                     subfunction_restrictions=self.EXAMPLE_SUBFUNCTION_RESTRICTIONS,
                                                     did_restrictions=self.EXAMPLE_DID_RESTRICTIONS,
                                                     rid_restrictions=self.EXAMPLE_RID_RESTRICTIONS)
        assert ecu_diag_config.states == set(self.EXAMPLE_STATES)
        assert ecu_diag_config.states_names == set([state.name for state in self.EXAMPLE_STATES])
        assert ecu_diag_config.states_mapping == {
            state.name: state for state in self.EXAMPLE_STATES
        }

    @pytest.mark.parametrize("message_payload, message_restrictions", [
        (
            [0x10, 0x01],
            {
                DEFAULT_DIAGNOSTIC_SESSION_STATE.name: DEFAULT_DIAGNOSTIC_SESSION_STATE.possible_values,
                DEFAULT_SECURITY_ACCESS_STATE.name: DEFAULT_SECURITY_ACCESS_STATE.possible_values,
                DEFAULT_ADDRESSING_TYPE_STATE.name: DEFAULT_ADDRESSING_TYPE_STATE.possible_values,
            }
        ),
        (
            [0x10, 0x03],
            {
                DEFAULT_DIAGNOSTIC_SESSION_STATE.name: {0x01, 0x03, 0x04},
                DEFAULT_SECURITY_ACCESS_STATE.name: DEFAULT_SECURITY_ACCESS_STATE.possible_values,
                DEFAULT_ADDRESSING_TYPE_STATE.name: DEFAULT_ADDRESSING_TYPE_STATE.possible_values,
            }
        ),
        (
            [0x22, 0x01, 0x00],
            {
                DEFAULT_DIAGNOSTIC_SESSION_STATE.name: {0x03, 0x04},
                DEFAULT_SECURITY_ACCESS_STATE.name: DEFAULT_SECURITY_ACCESS_STATE.possible_values,
                DEFAULT_ADDRESSING_TYPE_STATE.name: {AddressingType.PHYSICAL},
            }
        ),
        (
            [0x2E, 0x01, 0x00],
            {
                DEFAULT_DIAGNOSTIC_SESSION_STATE.name: {0x03, 0x04},
                DEFAULT_SECURITY_ACCESS_STATE.name: {0x01, 0x03, 0x05},
                DEFAULT_ADDRESSING_TYPE_STATE.name: {AddressingType.PHYSICAL},
            }
        ),
        (
            [0x31, 0x01, 0x12, 0x34],
            {
                DEFAULT_DIAGNOSTIC_SESSION_STATE.name: {0x02},
                DEFAULT_SECURITY_ACCESS_STATE.name: {0x01},
                DEFAULT_ADDRESSING_TYPE_STATE.name: {AddressingType.PHYSICAL},
            }
        ),
        (
                [0x31, 0x03, 0xAB, 0xCD],
                {
                    DEFAULT_DIAGNOSTIC_SESSION_STATE.name: {0x03, 0x4},
                    DEFAULT_SECURITY_ACCESS_STATE.name: {0x03, 0x05},
                    DEFAULT_ADDRESSING_TYPE_STATE.name: {AddressingType.PHYSICAL},
                }
        ),
    ])
    def test_get_restrictions(self, message_payload, message_restrictions):
        ecu_diag_config = EcuDiagnosticConfiguration(states=self.EXAMPLE_STATES,
                                                     sid_restrictions=self.EXAMPLE_SID_RESTRICTIONS,
                                                     subfunction_restrictions=self.EXAMPLE_SUBFUNCTION_RESTRICTIONS,
                                                     did_restrictions=self.EXAMPLE_DID_RESTRICTIONS,
                                                     rid_restrictions=self.EXAMPLE_RID_RESTRICTIONS)
        assert ecu_diag_config.get_restrictions(message_payload=message_payload) == message_restrictions

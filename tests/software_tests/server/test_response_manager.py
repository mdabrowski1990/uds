import pytest
from mock import Mock

from uds.messages import UdsResponse, ResponseSID, NRC, POSSIBLE_REQUEST_SIDS, AddressingType
from uds.server.response_manager import ResponseManager, _EmergencyServiceNotSupported, _EmergencyNoResponse, \
    ResponseRule, ServerState


class TestEmergencyServiceNotSupported:
    """Tests for `_EmergencyServiceNotSupported` class."""

    def setup(self):
        self.mock_emergency_rule = Mock(spec=_EmergencyServiceNotSupported)

    def test_inheritance(self):
        assert issubclass(_EmergencyServiceNotSupported, ResponseRule)

    @pytest.mark.parametrize("current_states", [Mock(spec=dict), {}, {"a": 1, "b": 2}])
    def test_is_triggered(self, example_uds_request, current_states):
        assert _EmergencyServiceNotSupported.is_triggered(self=self.mock_emergency_rule, request=example_uds_request,
                                                          current_states=current_states) is True

    @pytest.mark.parametrize("current_states", [Mock(spec=dict), {}, {"a": 1, "b": 2}])
    def test_create_response(self, example_uds_request, current_states):
        response = _EmergencyServiceNotSupported.create_response(self=self.mock_emergency_rule,
                                                                 request=example_uds_request,
                                                                 current_states=current_states)
        assert isinstance(response, UdsResponse)
        assert len(response.raw_message) == 3
        assert response.raw_message[0] == ResponseSID.NegativeResponse.value
        assert response.raw_message[1] == example_uds_request.raw_message[0]
        assert response.raw_message[2] == NRC.ServiceNotSupported.value


class TestEmergencyNoResponse:
    """Tests for `_EmergencyNoResponse` class."""

    def setup(self):
        self.mock_emergency_rule = Mock(spec=_EmergencyNoResponse)

    def test_inheritance(self):
        assert issubclass(_EmergencyNoResponse, ResponseRule)

    @pytest.mark.parametrize("current_states", [Mock(spec=dict), {}, {"a": 1, "b": 2}])
    def test_is_triggered(self, example_uds_request, current_states):
        assert _EmergencyNoResponse.is_triggered(self=self.mock_emergency_rule, request=example_uds_request,
                                                 current_states=current_states) is True

    @pytest.mark.parametrize("current_states", [Mock(spec=dict), {}, {"a": 1, "b": 2}])
    def test_create_response(self, example_uds_request, current_states):
        assert _EmergencyNoResponse.create_response(self=self.mock_emergency_rule, request=example_uds_request,
                                                    current_states=current_states) is None


class TestResponseManager:
    """Tests for `ResponseManager` class."""

    def setup(self):
        self.mock_response_manager = Mock(spec=ResponseManager)

    def teardown(self):
        ...

    # __EMERGENCY_RESPONSE_RULES

    def test_emergency_rules_number(self):
        assert len(ResponseManager._ResponseManager__EMERGENCY_RESPONSE_RULES) >= 2

    def test_emergency_rules_types(self):
        assert all(isinstance(emergency_rule, (_EmergencyServiceNotSupported, _EmergencyNoResponse))
                   for emergency_rule in ResponseManager._ResponseManager__EMERGENCY_RESPONSE_RULES)
        assert any(isinstance(emergency_rule, _EmergencyNoResponse)
                   for emergency_rule in ResponseManager._ResponseManager__EMERGENCY_RESPONSE_RULES)
        assert any(isinstance(emergency_rule, _EmergencyServiceNotSupported)
                   for emergency_rule in ResponseManager._ResponseManager__EMERGENCY_RESPONSE_RULES)

    def test_emergency_rules_addressing_and_sids(self):
        """Verity that there are emergency response rules for all addressing and all possible request SIDS"""
        physically_addressed_rules_sids = set()
        functionally_addressed_rules_sids = set()
        broadcast_addressed_rules_sids = set()

        for emergency_rule in ResponseManager._ResponseManager__EMERGENCY_RESPONSE_RULES:
            if AddressingType.PHYSICAL in emergency_rule.addressing_types:
                physically_addressed_rules_sids.update(emergency_rule.related_request_sids)
            if AddressingType.FUNCTIONAL in emergency_rule.addressing_types:
                functionally_addressed_rules_sids.update(emergency_rule.related_request_sids)
            if AddressingType.BROADCAST in emergency_rule.addressing_types:
                broadcast_addressed_rules_sids.update(emergency_rule.related_request_sids)

        assert physically_addressed_rules_sids == functionally_addressed_rules_sids == broadcast_addressed_rules_sids \
               == POSSIBLE_REQUEST_SIDS

    # __init__

    @pytest.mark.parametrize("response_rules", [(1, 2), [Mock(spec=ResponseRule)]])
    @pytest.mark.parametrize("server_states", [("a", "b"), [Mock(spec=ServerState)]])
    def test_init__params_validation(self, response_rules, server_states):
        ResponseManager.__init__(self=self.mock_response_manager, response_rules=response_rules,
                                 server_states=server_states)
        self.mock_response_manager._ResponseManager__validate_server_states.assert_called_once_with(server_states=server_states)

    @pytest.mark.parametrize("response_rules", [(1, 2), [Mock(spec=ResponseRule)]])
    @pytest.mark.parametrize("server_states", [("a", "b"), [Mock(spec=ServerState)]])
    def test_init__value_setting(self, response_rules, server_states):
        ResponseManager.__init__(self=self.mock_response_manager, response_rules=response_rules,
                                 server_states=server_states)
        assert self.mock_response_manager._ResponseManager__response_rules_tuple == ()
        assert self.mock_response_manager._ResponseManager__response_rules_dict == {}
        assert self.mock_response_manager._ResponseManager__server_states == set(server_states)
        assert self.mock_response_manager.response_rules == response_rules

    # __validate_response_rules

    @pytest.mark.parametrize("response_rules", [
        (Mock(spec=ResponseRule), Mock(spec=ResponseRule), Mock(spec=ResponseRule)),
        [Mock(spec=ResponseRule)]
    ])
    def test_validate_response_rules__valid(self, response_rules):
        assert ResponseManager._ResponseManager__validate_response_rules(response_rules=response_rules) is None

    @pytest.mark.parametrize("response_rules", [{Mock(spec=ResponseRule)}, None, "abcde", 1, False])
    def test_validate_response_rules__wrong_type(self, response_rules):
        with pytest.raises(TypeError):
            ResponseManager._ResponseManager__validate_response_rules(response_rules=response_rules)

    @pytest.mark.parametrize("response_rules", [
        (Mock(spec=ResponseRule), Mock(), Mock(spec=ResponseRule)),
        [Mock(spec=ResponseRule), None],
        [1],
    ])
    def test_validate_response_rules__wrong_value(self, response_rules):
        with pytest.raises(ValueError):
            ResponseManager._ResponseManager__validate_response_rules(response_rules=response_rules)

    # __validate_server_states
    
    @pytest.mark.parametrize("server_states", [
        (Mock(spec=ServerState), Mock(spec=ServerState), Mock(spec=ServerState)),
        [Mock(spec=ServerState), Mock(spec=ServerState)],
        {Mock(spec=ServerState)}
    ])
    def test_validate_server_states__valid(self, server_states):
        assert ResponseManager._ResponseManager__validate_server_states(server_states=server_states) is None

    @pytest.mark.parametrize("server_states", [None, "abcde", 1, False])
    def test_validate_server_states__wrong_type(self, server_states):
        with pytest.raises(TypeError):
            ResponseManager._ResponseManager__validate_server_states(server_states=server_states)

    @pytest.mark.parametrize("server_states", [
        (Mock(spec=ServerState), Mock(), Mock(spec=ServerState)),
        [Mock(spec=ServerState), None],
        {"not a server state", Mock(spec=ServerState)},
        [1],
    ])
    def test_validate_server_states__wrong_value(self, server_states):
        with pytest.raises(ValueError):
            ResponseManager._ResponseManager__validate_server_states(server_states=server_states)

    # _create_response_rules_dict

    def test_create_response_rules_dict__no_rules(self):
        assert ResponseManager._create_response_rules_dict(response_rules=[]) == {}

    @pytest.mark.parametrize("addressing_types", [{AddressingType.BROADCAST}, list(AddressingType)])
    @pytest.mark.parametrize("related_request_sids", [{0x10}, {0x22, 0x2E, 0x31, 0x27}])
    def test_create_response_rules_dict__one_rule(self, addressing_types, related_request_sids):
        rule_mock = Mock(addressing_types=addressing_types, related_request_sids=related_request_sids)
        rules_dict = {addressing: {sid: [rule_mock] for sid in related_request_sids}
                      for addressing in addressing_types}
        assert ResponseManager._create_response_rules_dict(response_rules=[rule_mock]) == rules_dict

    @pytest.mark.parametrize("addressing_types", [{AddressingType.FUNCTIONAL}, list(AddressingType)])
    @pytest.mark.parametrize("related_request_sids", [{0x3E}, {0x22, 0x2E, 0x31, 0x27}])
    def test_create_response_rules_dict__rules_order(self, addressing_types, related_request_sids):
        rule_1 = Mock(addressing_types=addressing_types, related_request_sids=related_request_sids)
        rule_2 = Mock(addressing_types=addressing_types, related_request_sids=related_request_sids)
        rules_dict = {addressing: {sid: [rule_1, rule_2] for sid in related_request_sids}
                      for addressing in addressing_types}
        assert ResponseManager._create_response_rules_dict(response_rules=[rule_1, rule_2]) == rules_dict

    # response_rules

    @pytest.mark.parametrize("response_rules", [("rule1", "rule2"), Mock()])
    def test_get_response_rules(self, response_rules):
        self.mock_response_manager._ResponseManager__response_rules_tuple = response_rules
        assert ResponseManager.response_rules.fget(self=self.mock_response_manager) is response_rules

    @pytest.mark.parametrize("response_rules", [(), [Mock(), Mock()]])
    def test_set_response_rules__param_validation(self, response_rules):
        ResponseManager.response_rules.fset(self=self.mock_response_manager, value=response_rules)
        self.mock_response_manager._ResponseManager__validate_response_rules.assert_called_once_with(
            response_rules=response_rules)

    @pytest.mark.parametrize("response_rules", [(), [Mock(addressing="Physical", sids={0x10})]])
    @pytest.mark.parametrize("response_rules_dict", [{}, {"Physical Addressing": {0x10: [Mock()]}}])
    def test_set_response_rules__values(self, response_rules, response_rules_dict):
        self.mock_response_manager._create_response_rules_dict.return_value = response_rules_dict
        ResponseManager.response_rules.fset(self=self.mock_response_manager, value=response_rules)
        assert self.mock_response_manager._ResponseManager__response_rules_tuple == tuple(response_rules)
        assert self.mock_response_manager._ResponseManager__response_rules_dict == response_rules_dict
        self.mock_response_manager._create_response_rules_dict.assert_called_once_with(response_rules=response_rules)


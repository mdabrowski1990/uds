import pytest
from mock import Mock, patch

from uds.messages import UdsResponse, ResponseSID, NRC, POSSIBLE_REQUEST_SIDS, AddressingType
from uds.server.response_manager import ResponseManager, _EmergencyServiceNotSupported, _EmergencyNoResponse, \
    ResponseRule


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
        ...

    def teardown(self):
        ...

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

    def test(self):
        ...

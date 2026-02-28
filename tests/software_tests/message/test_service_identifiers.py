import pytest
from mock import Mock, call, patch

from uds.message.service_identifiers import (
    RESPONSE_REQUEST_SID_DIFF,
    ByteEnum,
    ExtendableEnum,
    InconsistencyError,
    RequestSID,
    ResponseSID,
    ValidatedEnum,
    define_service,
)

SCRIPT_LOCATION = "uds.message.service_identifiers"


class TestRequestSID:
    """Unit tests for 'RequestSID' enum."""

    def setup_method(self):
        self._patcher_warn = patch(f"{SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()
        self._patcher_is_member = patch(f"{SCRIPT_LOCATION}.RequestSID.is_member")
        self.mock_is_member = self._patcher_is_member.start()
        self.patcher_all_request_sids = patch(f"{SCRIPT_LOCATION}.ALL_REQUEST_SIDS")
        self.mock_all_request_sids = self.patcher_all_request_sids.start()

    def teardown_method(self):
        self._patcher_warn.stop()
        self._patcher_is_member.stop()
        self.patcher_all_request_sids.stop()

    def test_inheritance__byte_enum(self):
        assert issubclass(RequestSID, ByteEnum)

    def test_inheritance__validated_enum(self):
        assert issubclass(RequestSID, ValidatedEnum)

    def test_inheritance__extendable_enum(self):
        assert issubclass(ResponseSID, ExtendableEnum)

    @pytest.mark.parametrize("value", [1, 0x55, 0xFF])
    def test_is_request_sid__member(self, value):
        self.mock_is_member.return_value = True
        self.mock_all_request_sids.__contains__.return_value = True
        assert RequestSID.is_request_sid(value=value) is True
        self.mock_warn.assert_not_called()
        self.mock_is_member.assert_called_once_with(value)
        self.mock_all_request_sids.__contains__.assert_called_once_with(value)

    @pytest.mark.parametrize("value", [1, 0x55, 0xFF])
    def test_is_request_sid__unsupported(self, value):
        self.mock_is_member.return_value = False
        self.mock_all_request_sids.__contains__.return_value = True
        assert RequestSID.is_request_sid(value=value) is True
        self.mock_warn.assert_called_once()
        self.mock_is_member.assert_called_once_with(value)
        self.mock_all_request_sids.__contains__.assert_called_once_with(value)

    @pytest.mark.parametrize("value", [1, 0x55, 0xFF])
    def test_is_request_sid__invalid(self, value):
        self.mock_is_member.return_value = False
        self.mock_all_request_sids.__contains__.return_value = False
        assert RequestSID.is_request_sid(value=value) is False
        self.mock_warn.assert_not_called()
        self.mock_is_member.assert_not_called()
        self.mock_all_request_sids.__contains__.assert_called_once_with(value)


class TestResponseSID:
    """Unit tests for 'ResponseSID' enum."""

    def setup_method(self):
        self._patcher_warn = patch(f"{SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()
        self._patcher_is_member = patch(f"{SCRIPT_LOCATION}.ResponseSID.is_member")
        self.mock_is_member = self._patcher_is_member.start()
        self.patcher_all_response_sids = patch(f"{SCRIPT_LOCATION}.ALL_RESPONSE_SIDS")
        self.mock_all_response_sids = self.patcher_all_response_sids.start()

    def teardown_method(self):
        self._patcher_warn.stop()
        self._patcher_is_member.stop()
        self.patcher_all_response_sids.stop()

    def test_inheritance__byte_enum(self):
        assert issubclass(ResponseSID, ByteEnum)

    def test_inheritance__validated_enum(self):
        assert issubclass(ResponseSID, ValidatedEnum)

    def test_inheritance__extendable_enum(self):
        assert issubclass(ResponseSID, ExtendableEnum)

    @pytest.mark.parametrize("value", [1, 0x55, 0xFF])
    def test_is_response_sid__member(self, value):
        self.mock_is_member.return_value = True
        self.mock_all_response_sids.__contains__.return_value = True
        assert ResponseSID.is_response_sid(value=value) is True
        self.mock_warn.assert_not_called()
        self.mock_is_member.assert_called_once_with(value)
        self.mock_all_response_sids.__contains__.assert_called_once_with(value)

    @pytest.mark.parametrize("value", [1, 0x55, 0xFF])
    def test_is_response_sid__unsupported(self, value):
        self.mock_is_member.return_value = False
        self.mock_all_response_sids.__contains__.return_value = True
        assert ResponseSID.is_response_sid(value=value) is True
        self.mock_warn.assert_called_once()
        self.mock_is_member.assert_called_once_with(value)
        self.mock_all_response_sids.__contains__.assert_called_once_with(value)

    @pytest.mark.parametrize("value", [1, 0x55, 0xFF])
    def test_is_response_sid__invalid(self, value):
        self.mock_is_member.return_value = False
        self.mock_all_response_sids.__contains__.return_value = False
        assert ResponseSID.is_response_sid(value=value) is False
        self.mock_warn.assert_not_called()
        self.mock_is_member.assert_not_called()
        self.mock_all_response_sids.__contains__.assert_called_once_with(value)


class TestFunctions:
    """Unit tests for module functions."""

    def setup_method(self):
        self._patcher_is_sid_member = patch(f"{SCRIPT_LOCATION}.RequestSID.is_member")
        self.mock_is_sid_member = self._patcher_is_sid_member.start()
        self._patcher_is_rsid_member = patch(f"{SCRIPT_LOCATION}.ResponseSID.is_member")
        self.mock_is_rsid_member = self._patcher_is_rsid_member.start()
        self._patcher_add_sid_member = patch(f"{SCRIPT_LOCATION}.RequestSID.add_member")
        self.mock_add_sid_member = self._patcher_add_sid_member.start()
        self._patcher_add_rsid_member = patch(f"{SCRIPT_LOCATION}.ResponseSID.add_member")
        self.mock_add_rsid_member = self._patcher_add_rsid_member.start()

    def teardown_method(self):
        self._patcher_is_sid_member.stop()
        self._patcher_is_rsid_member.stop()
        self._patcher_add_sid_member.stop()
        self._patcher_add_rsid_member.stop()

    # define_service

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_define_service__type_error_1(self, mock_isinstance):
        mock_isinstance.return_value = False
        mock_sid = Mock()
        mock_name = Mock()
        with pytest.raises(TypeError):
            define_service(sid=mock_sid, name=mock_name)
        mock_isinstance.assert_called_once_with(mock_sid, int)
        self.mock_add_sid_member.assert_not_called()
        self.mock_add_rsid_member.assert_not_called()

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_define_service__type_error_2(self, mock_isinstance):
        mock_isinstance.side_effect = [True, False]
        mock_sid = Mock()
        mock_name = Mock()
        with pytest.raises(TypeError):
            define_service(sid=mock_sid, name=mock_name)
        mock_isinstance.assert_has_calls([call(mock_sid, int), call(mock_name, str)])
        self.mock_add_sid_member.assert_not_called()
        self.mock_add_rsid_member.assert_not_called()

    @pytest.mark.parametrize("sid", [-1, 0x100, 0x7F])
    def test_define_service__value_error(self, sid):
        mock_name = Mock(spec=str)
        with pytest.raises(ValueError):
            define_service(sid=sid, name=mock_name)
        self.mock_add_sid_member.assert_not_called()
        self.mock_add_rsid_member.assert_not_called()

    @pytest.mark.parametrize("sid", [RequestSID.DiagnosticSessionControl, RequestSID.LinkControl])
    def test_define_service__sid_inconsistency_error(self, sid):
        mock_name = Mock(spec=str)
        self.mock_is_sid_member.return_value = True
        self.mock_is_rsid_member.return_value = True
        with pytest.raises(InconsistencyError):
            define_service(sid=sid, name=mock_name)
        self.mock_is_sid_member.assert_called_once_with(sid)
        self.mock_is_rsid_member.assert_not_called()
        self.mock_add_sid_member.assert_not_called()
        self.mock_add_rsid_member.assert_not_called()

    @pytest.mark.parametrize("sid", [RequestSID.DiagnosticSessionControl, RequestSID.LinkControl])
    def test_define_service__rsid_inconsistency_error(self, sid):
        mock_name = Mock(spec=str)
        self.mock_is_sid_member.return_value = False
        self.mock_is_rsid_member.return_value = True
        with pytest.raises(InconsistencyError):
            define_service(sid=sid, name=mock_name)
        self.mock_is_sid_member.assert_called_once_with(sid)
        self.mock_is_rsid_member.assert_called_once_with(sid + RESPONSE_REQUEST_SID_DIFF)
        self.mock_add_sid_member.assert_not_called()
        self.mock_add_rsid_member.assert_not_called()

    @pytest.mark.parametrize("sid", [RequestSID.DiagnosticSessionControl, RequestSID.LinkControl])
    def test_define_service__valid(self, sid):
        mock_name = Mock(spec=str)
        self.mock_is_sid_member.return_value = False
        self.mock_is_rsid_member.return_value = False
        assert define_service(sid=sid, name=mock_name) == (self.mock_add_sid_member.return_value,
                                                           self.mock_add_rsid_member.return_value)
        self.mock_is_sid_member.assert_called_once_with(sid)
        self.mock_is_rsid_member.assert_called_once_with(sid + RESPONSE_REQUEST_SID_DIFF)
        self.mock_add_sid_member.assert_called_once_with(name=mock_name, value=sid)
        self.mock_add_rsid_member.assert_called_once_with(name=mock_name, value=sid + RESPONSE_REQUEST_SID_DIFF)


@pytest.mark.integration
class TestSIDIntegration:

    SYSTEM_SPECIFIC_REQUEST_SID_VALUES = range(0xBA, 0xBF)
    SYSTEM_SPECIFIC_RESPONSE_SID_VALUES = range(0xFA, 0xFF)

    def test_number_of_members(self):
        assert len(ResponseSID) == len(RequestSID) + 1, \
            "ResponseSID shall contain RSID for each SID and one additional element for 'NegativeResponse'."

    @pytest.mark.parametrize("request_sid_member", list(RequestSID))
    def test_rsid_members(self, request_sid_member):
        assert ResponseSID[request_sid_member.name] == request_sid_member + 0x40, \
            "Verify each ResponseSID member has correct value (SID + 0x40)."

    @pytest.mark.parametrize("undefined_value", SYSTEM_SPECIFIC_REQUEST_SID_VALUES)
    def test_undefined_request_sid(self, undefined_value):
        assert RequestSID.is_request_sid(undefined_value) is True
        assert RequestSID.is_member(undefined_value) is False

    @pytest.mark.parametrize("undefined_value", SYSTEM_SPECIFIC_RESPONSE_SID_VALUES)
    def test_undefined_response_sid(self, undefined_value):
        assert ResponseSID.is_response_sid(undefined_value) is True
        assert ResponseSID.is_member(undefined_value) is False

    @pytest.mark.parametrize("sid, name", [
        (SYSTEM_SPECIFIC_REQUEST_SID_VALUES[0], "NewSID"),
        (SYSTEM_SPECIFIC_REQUEST_SID_VALUES[1], "Another"),
    ])
    def test_define_service(self, sid, name):
        sid_member, rsid_member = define_service(sid=sid, name=name)
        assert sid_member.value == sid
        assert rsid_member.value == sid + RESPONSE_REQUEST_SID_DIFF
        assert sid_member.name == rsid_member.name == name

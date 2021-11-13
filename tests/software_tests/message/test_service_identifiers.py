import pytest
from mock import patch

from uds.message.service_identifiers import RequestSID, ResponseSID, \
    ByteEnum, ValidatedEnum, ExtendableEnum


class TestRequestSID:
    """Unit tests for 'RequestSID' enum."""

    SCRIPT_LOCATION = "uds.message.service_identifiers"

    def setup(self):
        self._patcher_warn = patch(f"{self.SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()
        self._patcher_is_member = patch(f"{self.SCRIPT_LOCATION}.RequestSID.is_member")
        self.mock_is_member = self._patcher_is_member.start()
        self._patcher_possible_request_sids = patch(f"{self.SCRIPT_LOCATION}.POSSIBLE_REQUEST_SIDS")
        self.mock_possible_request_sids = self._patcher_possible_request_sids.start()

    def teardown(self):
        self._patcher_warn.stop()
        self._patcher_is_member.stop()
        self._patcher_possible_request_sids.stop()

    def test_inheritance__byte_enum(self):
        assert issubclass(RequestSID, ByteEnum)

    def test_inheritance__validated_enum(self):
        assert issubclass(RequestSID, ValidatedEnum)

    def test_inheritance__extendable_enum(self):
        assert issubclass(ResponseSID, ExtendableEnum)

    @pytest.mark.parametrize("value", [1, 0x55, 0xFF])
    def test_is_request_sid__member(self, value):
        self.mock_is_member.return_value = True
        assert RequestSID.is_request_sid(value=value) is True
        self.mock_warn.assert_not_called()
        self.mock_is_member.assert_called_once_with(value)
        self.mock_possible_request_sids.__contains__.assert_not_called()

    @pytest.mark.parametrize("value", [1, 0x55, 0xFF])
    def test_is_request_sid__unsupported(self, value):
        self.mock_is_member.return_value = False
        self.mock_possible_request_sids.__contains__.return_value = True
        assert RequestSID.is_request_sid(value=value) is True
        self.mock_warn.assert_called_once()
        self.mock_is_member.assert_called_once_with(value)
        self.mock_possible_request_sids.__contains__.assert_called_once_with(value)

    @pytest.mark.parametrize("value", [1, 0x55, 0xFF])
    def test_is_request_sid__invalid(self, value):
        self.mock_is_member.return_value = False
        self.mock_possible_request_sids.__contains__.return_value = False
        assert RequestSID.is_request_sid(value=value) is False
        self.mock_warn.assert_not_called()
        self.mock_is_member.assert_called_once_with(value)
        self.mock_possible_request_sids.__contains__.assert_called_once_with(value)


class TestResponseSID:
    """Unit tests for 'ResponseSID' enum."""

    SCRIPT_LOCATION = TestRequestSID.SCRIPT_LOCATION

    def setup(self):
        self._patcher_warn = patch(f"{self.SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()
        self._patcher_is_member = patch(f"{self.SCRIPT_LOCATION}.ResponseSID.is_member")
        self.mock_is_member = self._patcher_is_member.start()
        self._patcher_possible_response_sids = patch(f"{self.SCRIPT_LOCATION}.POSSIBLE_RESPONSE_SIDS")
        self.mock_possible_response_sids = self._patcher_possible_response_sids.start()

    def teardown(self):
        self._patcher_warn.stop()
        self._patcher_is_member.stop()
        self._patcher_possible_response_sids.stop()

    def test_inheritance__byte_enum(self):
        assert issubclass(ResponseSID, ByteEnum)

    def test_inheritance__validated_enum(self):
        assert issubclass(ResponseSID, ValidatedEnum)

    def test_inheritance__extendable_enum(self):
        assert issubclass(ResponseSID, ExtendableEnum)

    @pytest.mark.parametrize("value", [1, 0x55, 0xFF])
    def test_is_response_sid__member(self, value):
        self.mock_is_member.return_value = True
        assert ResponseSID.is_response_sid(value=value) is True
        self.mock_warn.assert_not_called()
        self.mock_is_member.assert_called_once_with(value)
        self.mock_possible_response_sids.__contains__.assert_not_called()

    @pytest.mark.parametrize("value", [1, 0x55, 0xFF])
    def test_is_response_sid__unsupported(self, value):
        self.mock_is_member.return_value = False
        self.mock_possible_response_sids.__contains__.return_value = True
        assert ResponseSID.is_response_sid(value=value) is True
        self.mock_warn.assert_called_once()
        self.mock_is_member.assert_called_once_with(value)
        self.mock_possible_response_sids.__contains__.assert_called_once_with(value)

    @pytest.mark.parametrize("value", [1, 0x55, 0xFF])
    def test_is_response_sid__invalid(self, value):
        self.mock_is_member.return_value = False
        self.mock_possible_response_sids.__contains__.return_value = False
        assert ResponseSID.is_response_sid(value=value) is False
        self.mock_warn.assert_not_called()
        self.mock_is_member.assert_called_once_with(value)
        self.mock_possible_response_sids.__contains__.assert_called_once_with(value)


@pytest.mark.integration
class TestSIDIntegration:

    SYSTEM_SPECIFIC_REQUEST_SID_VALUES = range(0xBA, 0xBF)
    SYSTEM_SPECIFIC_RESPONSE_SID_VALUES = range(0xFA, 0xFF)

    def test_number_of_members(self):
        assert len(ResponseSID) == len(RequestSID) + 1, \
            "ResponseSID shall contain RSID for each SID and one additional element for 'NegativeResponse'."

    @pytest.mark.parametrize("request_sid_member", list(RequestSID))
    def test_rsid_members(self, request_sid_member):
        assert ResponseSID[request_sid_member.name] == request_sid_member.value + 0x40, \
            "Verify each ResponseSID member has correct value (SID + 0x40)."

    @pytest.mark.parametrize("undefined_value", SYSTEM_SPECIFIC_REQUEST_SID_VALUES)
    def test_undefined_request_sid(self, undefined_value):
        assert RequestSID.is_request_sid(undefined_value) is True
        assert RequestSID.is_member(undefined_value) is False

    @pytest.mark.parametrize("undefined_value", SYSTEM_SPECIFIC_RESPONSE_SID_VALUES)
    def test_undefined_response_sid(self, undefined_value):
        assert ResponseSID.is_response_sid(undefined_value) is True
        assert ResponseSID.is_member(undefined_value) is False

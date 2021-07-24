import pytest
from mock import patch

from uds.messages.service_identifiers import RequestSID, ResponseSID


class TestRequestSID:
    """Tests for RequestSID enum"""

    SCRIPT_LOCATION = "uds.messages.service_identifiers"
    EXAMPLE_REQUEST_SIDS = [0x10, 0x14, 0x22, 0x86]
    EXAMPLE_RESPONSE_SIDS = [0x50, 0x54, 0x62, 0xC6, 0x7F]

    def setup(self):
        self._patcher_warn = patch(f"{self.SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()

    def teardown(self):
        self._patcher_warn.stop()

    @pytest.mark.parametrize("valid_sid", EXAMPLE_REQUEST_SIDS)
    def test_is_request_sid__true(self, valid_sid):
        assert RequestSID.is_request_sid(value=valid_sid) is True

    @pytest.mark.parametrize("invalid_value", [-1, "something", 2.3] + EXAMPLE_RESPONSE_SIDS)
    def test_is_request_sid__false(self, invalid_value):
        assert RequestSID.is_request_sid(value=invalid_value) is False

    @patch(f"{SCRIPT_LOCATION}.POSSIBLE_REQUEST_SIDS")
    @pytest.mark.parametrize("invalid_value", [-1, "something", 2.3])
    def test_is_request_sid__warning(self, mock_possible_request_sids, invalid_value):
        mock_possible_request_sids.__contains__.return_value = True
        RequestSID.is_request_sid(value=invalid_value)
        self.mock_warn.assert_called_once()

    @patch(f"{SCRIPT_LOCATION}.POSSIBLE_REQUEST_SIDS")
    @pytest.mark.parametrize("invalid_value", [-1, "something", 2.3])
    def test_is_request_sid__no_warning(self, mock_possible_request_sids, invalid_value):
        mock_possible_request_sids.__contains__.return_value = False
        RequestSID.is_request_sid(value=invalid_value)
        self.mock_warn.assert_not_called()


class TestResponseSID:
    """Tests for ResponseSID Enum"""

    SCRIPT_LOCATION = TestRequestSID.SCRIPT_LOCATION
    EXAMPLE_REQUEST_SIDS = TestRequestSID.EXAMPLE_REQUEST_SIDS
    EXAMPLE_RESPONSE_SIDS = TestRequestSID.EXAMPLE_RESPONSE_SIDS

    def setup(self):
        self._patcher_warn = patch(f"{self.SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()

    def teardown(self):
        self._patcher_warn.stop()

    def test_number_of_members(self):
        assert len(ResponseSID) == len(RequestSID) + 1, \
            "ResponseSID shall contain RSID for each SID and one additional element for 'NegativeResponse'."

    @pytest.mark.parametrize("request_sid_member", list(RequestSID))
    def test_rsid_members(self, request_sid_member):
        assert ResponseSID[request_sid_member.name] == request_sid_member.value + 0x40, \
            "Verify each ResponseSID member has correct value (SID + 0x40)."

    @pytest.mark.parametrize("valid_rsid", EXAMPLE_RESPONSE_SIDS)
    def test_is_response_sid__true(self, valid_rsid):
        assert ResponseSID.is_response_sid(value=valid_rsid) is True

    @pytest.mark.parametrize("invalid_value", [-1, "something", 2.3] + EXAMPLE_REQUEST_SIDS)
    def test_is_response_sid__false(self, invalid_value):
        assert ResponseSID.is_response_sid(value=invalid_value) is False

    @patch(f"{SCRIPT_LOCATION}.POSSIBLE_RESPONSE_SIDS")
    @pytest.mark.parametrize("invalid_value", [-1, "something", 2.3])
    def test_is_request_sid__warning(self, mock_possible_response_sids, invalid_value):
        mock_possible_response_sids.__contains__.return_value = True
        ResponseSID.is_response_sid(value=invalid_value)
        self.mock_warn.assert_called_once()

    @patch(f"{SCRIPT_LOCATION}.POSSIBLE_RESPONSE_SIDS")
    @pytest.mark.parametrize("invalid_value", [-1, "something", 2.3])
    def test_is_request_sid__no_warning(self, mock_possible_response_sids, invalid_value):
        mock_possible_response_sids.__contains__.return_value = False
        ResponseSID.is_response_sid(value=invalid_value)
        self.mock_warn.assert_not_called()
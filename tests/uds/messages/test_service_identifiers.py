import pytest

from uds.messages.service_identifiers import RequestSID, ResponseSID


class TestRequestSID:
    """Tests for RequestSID enum"""

    EXAMPLE_REQUEST_SIDS = [0x10, 0x14, 0x22, 0x86]
    EXAMPLE_RESPONSE_SIDS = [0x50, 0x54, 0x62, 0xC6, 0x7F]

    @pytest.mark.parametrize("valid_sid", EXAMPLE_REQUEST_SIDS)
    def test_is_request_sid__true(self, valid_sid):
        assert RequestSID.is_request_sid(value=valid_sid) is True

    @pytest.mark.parametrize("invalid_value", [-1, "something", 2.3] + EXAMPLE_RESPONSE_SIDS)
    def test_is_request_sid__false(self, invalid_value):
        assert RequestSID.is_request_sid(value=invalid_value) is False


class TestResponseSID:
    """Tests for ResponseSID Enum"""

    EXAMPLE_REQUEST_SIDS = TestRequestSID.EXAMPLE_REQUEST_SIDS
    EXAMPLE_RESPONSE_SIDS = TestRequestSID.EXAMPLE_RESPONSE_SIDS

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

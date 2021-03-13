import pytest
from mock import Mock

from uds.messages.response import UdsMessage, UdsResponse, UdsResponseType


class TestsUdsResponse:
    """Tests for UdsResponse class."""

    def setup(self):
        self.mock_uds_response = Mock(spec=UdsResponse)

    # inheritance

    def test_inherits_after_uds_message(self):
        assert issubclass(UdsResponse, UdsMessage)

    # get_response_type

    @pytest.mark.parametrize("positive_response_message", [
        [0x54],
        [0x51, 0x01],
    ])
    def test_get_response_type__positive(self, positive_response_message):
        self.mock_uds_response.raw_message = positive_response_message
        assert UdsResponse.get_response_type(self=self.mock_uds_response) == UdsResponseType.POSITIVE

    @pytest.mark.parametrize("negative_response_message", [
        [0x7F, 0x10, 0x22],
        [0x7F, 0x31, 0xAA],
        [0x7F, 0x22, 0x10],
    ])
    def test_get_response_type__negative(self, negative_response_message):
        self.mock_uds_response.raw_message = negative_response_message
        assert UdsResponse.get_response_type(self=self.mock_uds_response) == UdsResponseType.NEGATIVE

    @pytest.mark.parametrize("request_message", [
        [0x10, 0x03],
        [0x11, 0x01],
        [0x14, 0xFF, 0xFF, 0xFF]
    ])
    def test_get_response_type__invalid(self, request_message):
        self.mock_uds_response.raw_message = request_message
        assert UdsResponse.get_response_type(self=self.mock_uds_response) == UdsResponseType.INVALID

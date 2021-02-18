import pytest
from mock import Mock

from uds.messages.base_message import UdsMessage


class TestUdsMessage:
    """Tests for 'UdsMessage' class."""

    def setup(self):
        self.mock_uds_message = Mock(spec=UdsMessage)

    # TODO: add __init__ tests

    # addressing

    def test_addressing__undefined(self):
        self.mock_uds_message.pdu_list = []
        assert UdsMessage.addressing.fget(self=self.mock_uds_message) is None

    @pytest.mark.parametrize("number_of_pdu", [1, 3, 6])
    def test_addressing__got_from_pdu(self, number_of_pdu):
        mock_pdu_1 = Mock()
        other_pdus = [Mock()] * (number_of_pdu-1)
        self.mock_uds_message.pdu_list = [mock_pdu_1] + other_pdus
        assert UdsMessage.addressing.fget(self=self.mock_uds_message) is mock_pdu_1.addressing

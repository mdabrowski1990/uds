import pytest
from mock import Mock

from uds.messages.base_message import UdsMessage, AbstractPDU


class TestUdsMessage:
    """Tests for 'UdsMessage' class."""

    def setup(self):
        self.mock_uds_message = Mock(spec=UdsMessage)

    # __init__

    @pytest.mark.parametrize("raw_message", [
        [0x10, 0x01],
        [0x22, 0x10, 0x01, 0x12, 0x34],
        [0x51, 0x03]
    ])
    @pytest.mark.parametrize("pdu_list", [
        [Mock(spec=AbstractPDU), Mock(spec=AbstractPDU)]
    ])
    def test_init(self, raw_message, pdu_list):
        UdsMessage.__init__(self=self.mock_uds_message, raw_message=raw_message, pdu_list=pdu_list)
        assert self.mock_uds_message._UdsMessage__raw_message == raw_message
        assert self.mock_uds_message._UdsMessage__pdu_list == pdu_list

    def test_init__no_pdu(self, example_raw_message):
        UdsMessage.__init__(self=self.mock_uds_message, raw_message=example_raw_message)
        assert self.mock_uds_message._UdsMessage__pdu_list == []

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

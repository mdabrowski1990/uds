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
        (0x22, 0x10, 0x01, 0x12, 0x34),
        [0x51, 0x03],
        (0x54, ),
    ])
    @pytest.mark.parametrize("pdu_sequence", [
        [Mock(spec=AbstractPDU), Mock(spec=AbstractPDU)],
        (Mock(spec=AbstractPDU), )
    ])
    def test_init__valid_values(self, raw_message, pdu_sequence):
        UdsMessage.__init__(self=self.mock_uds_message, raw_message=raw_message, pdu_sequence=pdu_sequence)
        # data validation
        self.mock_uds_message._UdsMessage__validate_raw_message.assert_called_once_with(raw_message=raw_message)
        self.mock_uds_message._UdsMessage__validate_pdu_sequence.assert_called_once_with(pdu_sequence=pdu_sequence)
        # raw_message verification
        assert isinstance(self.mock_uds_message._UdsMessage__raw_message, tuple), \
            "Value must be converted to tuple to be immutable"
        assert len(self.mock_uds_message._UdsMessage__raw_message) == len(raw_message), "Elements must be unchanged"
        assert all(value_set == value_provided for value_set, value_provided in
                   zip(self.mock_uds_message._UdsMessage__raw_message, raw_message)), "Elements must be unchanged"
        # pdu_sequence verification
        assert isinstance(self.mock_uds_message._UdsMessage__pdu_sequence, tuple), \
            "Value must be converted to tuple to be immutable"
        assert len(self.mock_uds_message._UdsMessage__pdu_sequence) == len(pdu_sequence), "Elements must be unchanged"
        assert all(value_set == value_provided for value_set, value_provided in
                   zip(self.mock_uds_message._UdsMessage__pdu_sequence, pdu_sequence)), "Elements must be unchanged"

    def test_init__no_pdus(self, example_raw_message):
        UdsMessage.__init__(self=self.mock_uds_message, raw_message=example_raw_message)
        assert self.mock_uds_message._UdsMessage__pdu_sequence == ()

    # __validate_raw_message

    @pytest.mark.parametrize("raw_message", [
        [0x10, 0x01],
        (0x22, 0x10, 0x01, 0x12, 0x34),
        [0x51, 0x03],
        (0x54, ),
    ])
    def test_validate_raw_message__valid(self, raw_message):
        assert UdsMessage._UdsMessage__validate_raw_message(raw_message=raw_message) is None

    @pytest.mark.parametrize("raw_message", [
        {0x10, 0x01},
        "abcdef",
        b"\x10\x01"
    ])
    def test_validate_raw_message__wrong_type(self, raw_message):
        with pytest.raises(TypeError):
            UdsMessage._UdsMessage__validate_raw_message(raw_message=raw_message)

    @pytest.mark.parametrize("raw_message", [
        [-1],
        [0x10, 0x100],
        [0x22, "10", "00"],
        [0x11, 1.]
    ])
    def test_validate_raw_message__wrong_value(self, raw_message):
        with pytest.raises(ValueError):
            UdsMessage._UdsMessage__validate_raw_message(raw_message=raw_message)

    # __validate_pdu_sequence

    @pytest.mark.parametrize("pdu_sequence", [
        [Mock(spec=AbstractPDU)],
        (Mock(spec=AbstractPDU), Mock(spec=AbstractPDU))
    ])
    def test_validate_pdu_sequence__valid(self, pdu_sequence):
        assert UdsMessage._UdsMessage__validate_pdu_sequence(pdu_sequence=pdu_sequence) is None

    @pytest.mark.parametrize("pdu_sequence", [
        {Mock(spec=AbstractPDU), Mock(spec=AbstractPDU)}
    ])
    def test_validate_pdu_sequence__wrong_type(self, pdu_sequence):
        with pytest.raises(TypeError):
            UdsMessage._UdsMessage__validate_pdu_sequence(pdu_sequence=pdu_sequence)

    @pytest.mark.parametrize("pdu_sequence", [
        [-1],
        (Mock(spec=AbstractPDU), "10"),
    ])
    def test_validate_pdu_sequence__wrong_value(self, pdu_sequence):
        with pytest.raises(ValueError):
            UdsMessage._UdsMessage__validate_pdu_sequence(pdu_sequence=pdu_sequence)

    # addressing

    def test_addressing__undefined(self):
        self.mock_uds_message.pdu_sequence = []
        assert UdsMessage.addressing.fget(self=self.mock_uds_message) is None

    @pytest.mark.parametrize("pdu_sequence", [
        [Mock(spec=AbstractPDU)],
        (Mock(spec=AbstractPDU), Mock(spec=AbstractPDU))
    ])
    def test_addressing__got_from_pdu(self, pdu_sequence):
        self.mock_uds_message.pdu_sequence = pdu_sequence
        assert UdsMessage.addressing.fget(self=self.mock_uds_message) is pdu_sequence[0].addressing

    # pdu_sequence

    @pytest.mark.parametrize("pdu_sequence", [0, Mock(), "xyz"])
    def test_pdu_sequence(self, pdu_sequence):
        self.mock_uds_message._UdsMessage__pdu_sequence = pdu_sequence
        assert UdsMessage.pdu_sequence.fget(self=self.mock_uds_message) is pdu_sequence

    # raw_message

    @pytest.mark.parametrize("raw_message", [0, Mock(), "xyz"])
    def test_raw_message(self, raw_message):
        self.mock_uds_message._UdsMessage__raw_message = raw_message
        assert UdsMessage.raw_message.fget(self=self.mock_uds_message) is raw_message

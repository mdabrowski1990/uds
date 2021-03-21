import pytest
from mock import Mock

from uds.messages.base_message import UdsMessage, AbstractPDU, AddressingType


class TestUdsMessage:
    """Tests for UdsMessage class."""

    def setup(self):
        self.mock_uds_message = Mock(spec=UdsMessage)

    # __init__

    def test_init__only_raw_message(self, example_raw_message):
        UdsMessage.__init__(self=self.mock_uds_message, raw_message=example_raw_message)
        # data validation
        self.mock_uds_message._UdsMessage__validate_raw_message.assert_called_once_with(raw_message=example_raw_message)
        self.mock_uds_message._UdsMessage__validate_pdu_sequence.assert_not_called()
        self.mock_uds_message._UdsMessage__validate_addressing.assert_not_called()
        # data setting
        assert self.mock_uds_message._UdsMessage__raw_message == tuple(example_raw_message)
        assert self.mock_uds_message._UdsMessage__pdu_sequence == tuple()
        assert self.mock_uds_message._UdsMessage__addressing is None

    @pytest.mark.parametrize("pdu_sequence", [
        [Mock(spec=AbstractPDU)],
        (Mock(spec=AbstractPDU), Mock(spec=AbstractPDU))
    ])
    def test_init__all_params(self, example_raw_message, example_addressing_type, pdu_sequence):
        UdsMessage.__init__(self=self.mock_uds_message, raw_message=example_raw_message, pdu_sequence=pdu_sequence,
                            addressing=example_addressing_type)
        # data validation
        self.mock_uds_message._UdsMessage__validate_raw_message.assert_called_once_with(raw_message=example_raw_message)
        self.mock_uds_message._UdsMessage__validate_pdu_sequence.assert_called_once_with(pdu_sequence=pdu_sequence)
        self.mock_uds_message._UdsMessage__validate_addressing.assert_called_once_with(addressing=example_addressing_type)
        # data setting
        assert self.mock_uds_message._UdsMessage__raw_message == tuple(example_raw_message)
        assert self.mock_uds_message._UdsMessage__pdu_sequence == tuple(pdu_sequence)
        assert self.mock_uds_message._UdsMessage__addressing == example_addressing_type

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
    def test_validate_raw_message__invalid_type(self, raw_message):
        with pytest.raises(TypeError):
            UdsMessage._UdsMessage__validate_raw_message(raw_message=raw_message)

    @pytest.mark.parametrize("raw_message", [
        [-1],
        [0x10, 0x100],
        [0x22, "10", "00"],
        [0x11, 1.]
    ])
    def test_validate_raw_message__invalid_value(self, raw_message):
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
    def test_validate_pdu_sequence__invalid_type(self, pdu_sequence):
        with pytest.raises(TypeError):
            UdsMessage._UdsMessage__validate_pdu_sequence(pdu_sequence=pdu_sequence)

    @pytest.mark.parametrize("pdu_sequence", [
        [-1],
        (Mock(spec=AbstractPDU), "10"),
    ])
    def test_validate_pdu_sequence__invalid_value(self, pdu_sequence):
        with pytest.raises(ValueError):
            UdsMessage._UdsMessage__validate_pdu_sequence(pdu_sequence=pdu_sequence)

    # __validate_addressing

    @pytest.mark.parametrize("addressing", [
        Mock(spec=AddressingType),
        AddressingType.FUNCTIONAL,
        AddressingType.PHYSICAL,
        AddressingType.BROADCAST,
    ])
    def test_validate_addressing__valid(self, addressing):
        assert UdsMessage._UdsMessage__validate_addressing(addressing=addressing) is None

    @pytest.mark.parametrize("addressing", [
        "not an addressing",
        1,
        None
    ])
    def test_validate_addressing__invalid_type(self, addressing):
        with pytest.raises(TypeError):
            UdsMessage._UdsMessage__validate_addressing(addressing=addressing)

    # addressing

    @pytest.mark.parametrize("addressing", [None, "functional", 0])
    def test_addressing__pdu_sequence_undefined(self, addressing):
        self.mock_uds_message.pdu_sequence = []
        self.mock_uds_message._UdsMessage__addressing = addressing
        assert UdsMessage.addressing.fget(self=self.mock_uds_message) is addressing

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

    # time_transmission_start

    def test_time_transmission_start__no_pdu(self):
        self.mock_uds_message.pdu_sequence = ()
        assert UdsMessage.time_transmission_start.fget(self=self.mock_uds_message) is None

    @pytest.mark.parametrize("pdu_sequence", [
        [Mock(spec=AbstractPDU)],
        (Mock(spec=AbstractPDU), Mock(spec=AbstractPDU), Mock(spec=AbstractPDU), Mock(spec=AbstractPDU)),
    ])
    @pytest.mark.parametrize("first_pdu_time", [1, None, "some time"])
    def test_time_transmission_start__pdus(self, pdu_sequence, first_pdu_time):
        pdu_sequence[0].time_transmitted = first_pdu_time
        self.mock_uds_message.pdu_sequence = pdu_sequence
        assert UdsMessage.time_transmission_start.fget(self=self.mock_uds_message) is first_pdu_time

    # time_transmission_start

    def test_time_transmission_end__no_pdu(self):
        self.mock_uds_message.pdu_sequence = ()
        assert UdsMessage.time_transmission_end.fget(self=self.mock_uds_message) is None

    @pytest.mark.parametrize("pdu_sequence", [
        [Mock(spec=AbstractPDU)],
        (Mock(spec=AbstractPDU), Mock(spec=AbstractPDU), Mock(spec=AbstractPDU), Mock(spec=AbstractPDU)),
    ])
    @pytest.mark.parametrize("last_pdu_time", [1, None, "some time"])
    def test_time_transmission_end__pdus(self, pdu_sequence, last_pdu_time):
        pdu_sequence[-1].time_transmitted = last_pdu_time
        self.mock_uds_message.pdu_sequence = pdu_sequence
        assert UdsMessage.time_transmission_end.fget(self=self.mock_uds_message) is last_pdu_time

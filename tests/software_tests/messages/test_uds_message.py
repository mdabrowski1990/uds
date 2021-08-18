import pytest
from mock import Mock, patch

from uds.messages.uds_message import UdsMessage, UdsMessageRecord, \
    AddressingType, TransmissionDirection, ReassignmentError, AbstractNPDURecord


class TestUdsMessage:
    """Tests for UdsMessage class."""

    SCRIPT_LOCATION = "uds.messages.uds_message"

    def setup(self):
        self.mock_uds_message = Mock(spec=UdsMessage)
        # patching
        self._patcher_validate_raw_bytes = patch(f"{self.SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
        self._patcher_validate_addressing = patch(f"{self.SCRIPT_LOCATION}.AddressingType.validate_member")
        self.mock_validate_addressing = self._patcher_validate_addressing.start()

    def teardown(self):
        self._patcher_validate_raw_bytes.stop()
        self._patcher_validate_addressing.stop()

    # __init__

    @pytest.mark.parametrize("raw_message", [None, [0x1, 0x02], "some message"])
    @pytest.mark.parametrize("addressing", ["Physical", 0, False, AddressingType.FUNCTIONAL])
    def test_init(self, raw_message, addressing):
        UdsMessage.__init__(self=self.mock_uds_message, raw_message=raw_message, addressing=addressing)
        assert self.mock_uds_message.raw_message == raw_message
        assert self.mock_uds_message.addressing == addressing

    # raw_message

    @pytest.mark.parametrize("value", [None, [0x1, 0x02], "some message"])
    def test_raw_message__get(self, value):
        self.mock_uds_message._UdsMessage__raw_message = value
        assert UdsMessage.raw_message.fget(self=self.mock_uds_message) is value

    def test_raw_message__set(self, example_raw_bytes):
        UdsMessage.raw_message.fset(self=self.mock_uds_message, value=example_raw_bytes)
        assert self.mock_uds_message._UdsMessage__raw_message == tuple(example_raw_bytes)
        self.mock_validate_raw_bytes.assert_called_once_with(example_raw_bytes)

    def test_raw_message__set_second_call(self, example_raw_bytes):
        self.mock_uds_message._UdsMessage__raw_message = "some value"
        UdsMessage.raw_message.fset(self=self.mock_uds_message, value=example_raw_bytes)
        assert self.mock_uds_message._UdsMessage__raw_message == tuple(example_raw_bytes)
        self.mock_validate_raw_bytes.assert_called_once_with(example_raw_bytes)

    # addressing

    @pytest.mark.parametrize("value", [None, AddressingType.PHYSICAL, "some addressing"])
    def test_addressing__get(self, value):
        self.mock_uds_message._UdsMessage__addressing = value
        assert UdsMessage.addressing.fget(self=self.mock_uds_message) is value

    def test_addressing__set_instance(self, example_addressing_type):
        UdsMessage.addressing.fset(self=self.mock_uds_message, value=example_addressing_type)
        assert self.mock_uds_message._UdsMessage__addressing == example_addressing_type
        self.mock_validate_addressing.assert_called_once_with(example_addressing_type)

    def test_addressing__set_value(self, example_addressing_type):
        UdsMessage.addressing.fset(self=self.mock_uds_message, value=example_addressing_type.value)
        assert self.mock_uds_message._UdsMessage__addressing == example_addressing_type
        self.mock_validate_addressing.assert_called_once_with(example_addressing_type.value)

    def test_addressing__set_second_call(self, example_addressing_type):
        self.mock_uds_message._UdsMessage__addressing = "some value"
        UdsMessage.addressing.fset(self=self.mock_uds_message, value=example_addressing_type)
        assert self.mock_uds_message._UdsMessage__addressing == example_addressing_type
        self.mock_validate_addressing.assert_called_once_with(example_addressing_type)


class TestUdsMessageRecord:

    SCRIPT_LOCATION = TestUdsMessage.SCRIPT_LOCATION

    def setup(self):
        self.mock_uds_message_record = Mock(spec=UdsMessageRecord)
        # patching
        self._patcher_validate_raw_bytes = patch(f"{self.SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
        self._patcher_validate_addressing = patch(f"{self.SCRIPT_LOCATION}.AddressingType.validate_member")
        self.mock_validate_addressing = self._patcher_validate_addressing.start()

    def teardown(self):
        self._patcher_validate_raw_bytes.stop()
        self._patcher_validate_addressing.stop()

    # __init__

    @pytest.mark.parametrize("raw_message", [None, [0x1, 0x02], "some message"])
    @pytest.mark.parametrize("npdu_sequence", [False, [1, 2, 3, 4], "abcdef"])
    def test_init(self, raw_message, npdu_sequence):
        UdsMessageRecord.__init__(self=self.mock_uds_message_record, raw_message=raw_message,
                                  npdu_sequence=npdu_sequence)
        assert self.mock_uds_message_record.raw_message == raw_message
        assert self.mock_uds_message_record.npdu_sequence == npdu_sequence

    # __validate_npdu_sequence

    @pytest.mark.parametrize("value", [
        (Mock(spec=AbstractNPDURecord),),
        [Mock(spec=AbstractNPDURecord), Mock(spec=AbstractNPDURecord)],
        (Mock(spec=AbstractNPDURecord), Mock(spec=AbstractNPDURecord), Mock(spec=AbstractNPDURecord))
    ])
    def test_validate_npdu_sequence__valid(self, value):
        assert UdsMessageRecord._UdsMessageRecord__validate_npdu_sequence(npdu_sequence=value) is None

    @pytest.mark.parametrize("value", [None, False, 0, Mock(spec=AbstractNPDURecord)])
    def test_validate_npdu_sequence__invalid_type(self, value):
        with pytest.raises(TypeError):
            UdsMessageRecord._UdsMessageRecord__validate_npdu_sequence(npdu_sequence=value)

    @pytest.mark.parametrize("value", [tuple(), [], ["a"], (None, ), (Mock(spec=AbstractNPDURecord), "not N_PDU")])
    def test_validate_npdu_sequence__invalid_value(self, value):
        with pytest.raises(ValueError):
            UdsMessageRecord._UdsMessageRecord__validate_npdu_sequence(npdu_sequence=value)

    # raw_message

    @pytest.mark.parametrize("value", [None, [0x1, 0x02], "some message"])
    def test_raw_message__get(self, value):
        self.mock_uds_message_record._UdsMessageRecord__raw_message = value
        assert UdsMessageRecord.raw_message.fget(self=self.mock_uds_message_record) is value

    def test_raw_message__set__first_call(self, example_raw_bytes):
        UdsMessageRecord.raw_message.fset(self=self.mock_uds_message_record, value=example_raw_bytes)
        assert self.mock_uds_message_record._UdsMessageRecord__raw_message == tuple(example_raw_bytes)
        self.mock_validate_raw_bytes.assert_called_once_with(example_raw_bytes)

    @pytest.mark.parametrize("old_value", [None, [0x1, 0x02], "some message"])
    @pytest.mark.parametrize("new_value", [None, [0x1, 0x02], "some message"])
    def test_raw_message__set__second_call(self, old_value, new_value):
        self.mock_uds_message_record._UdsMessageRecord__raw_message = old_value
        with pytest.raises(ReassignmentError):
            UdsMessageRecord.raw_message.fset(self=self.mock_uds_message_record, value=new_value)
        assert self.mock_uds_message_record._UdsMessageRecord__raw_message == old_value
        self.mock_validate_raw_bytes.assert_not_called()

    # npdu_sequence

    @pytest.mark.parametrize("value", [None, [Mock(), Mock()], "some sequence"])
    def test_npdu_sequence__get(self, value):
        self.mock_uds_message_record._UdsMessageRecord__npdu_sequence = value
        assert UdsMessageRecord.npdu_sequence.fget(self.mock_uds_message_record) is value

    @pytest.mark.parametrize("npdu_sequence", [
        (Mock(), Mock(), Mock()),
        [1, 2, 3, 4],
        "abcdefg"
    ])
    def test_npdu_sequence__set__first_call(self, npdu_sequence):
        UdsMessageRecord.npdu_sequence.fset(self=self.mock_uds_message_record, value=npdu_sequence)
        assert self.mock_uds_message_record._UdsMessageRecord__npdu_sequence == tuple(npdu_sequence)
        self.mock_uds_message_record._UdsMessageRecord__validate_npdu_sequence.assert_called_once_with(npdu_sequence)

    @pytest.mark.parametrize("old_value", [(Mock(), Mock(), Mock()), [1, 2, 3, 4], "abcdefg"])
    @pytest.mark.parametrize("new_value", [(Mock(), Mock(), Mock()), [1, 2, 3, 4], "abcdefg"])
    def test_npdu_sequence__set__second_call(self, old_value, new_value):
        self.mock_uds_message_record._UdsMessageRecord__npdu_sequence = old_value
        with pytest.raises(ReassignmentError):
            UdsMessageRecord.npdu_sequence.fset(self=self.mock_uds_message_record, value=new_value)
        assert self.mock_uds_message_record._UdsMessageRecord__npdu_sequence == old_value
        self.mock_uds_message_record._UdsMessageRecord__validate_npdu_sequence.assert_not_called()

    # addressing

    @pytest.mark.parametrize("npdu_sequence", [
        (Mock(spec=AbstractNPDURecord, addressing=AddressingType.PHYSICAL), ),
        (Mock(spec=AbstractNPDURecord, addressing=AddressingType.FUNCTIONAL),
         Mock(spec=AbstractNPDURecord, addressing=AddressingType.PHYSICAL)),
    ])
    def test_addressing__get(self, npdu_sequence):
        self.mock_uds_message_record.npdu_sequence = npdu_sequence
        assert UdsMessageRecord.addressing.fget(self=self.mock_uds_message_record) == npdu_sequence[0].addressing

    # direction

    @pytest.mark.parametrize("npdu_sequence", [
        (Mock(spec=AbstractNPDURecord, direction=TransmissionDirection.RECEIVED), ),
        (Mock(spec=AbstractNPDURecord, direction=TransmissionDirection.TRANSMITTED),
         Mock(spec=AbstractNPDURecord, direction=TransmissionDirection.RECEIVED)),
    ])
    def test_direction__get(self, npdu_sequence):
        self.mock_uds_message_record.npdu_sequence = npdu_sequence
        assert UdsMessageRecord.direction.fget(self=self.mock_uds_message_record) == npdu_sequence[0].direction

    # transmission_start

    @pytest.mark.parametrize("npdu_sequence", [
        (Mock(spec=AbstractNPDURecord, transmission_time=0),),
        (Mock(spec=AbstractNPDURecord, transmission_time=1), Mock(spec=AbstractNPDURecord, transmission_time=2)),
        (Mock(spec=AbstractNPDURecord, transmission_time=9654.3), Mock(spec=AbstractNPDURecord, transmission_time=-453),
         Mock(spec=AbstractNPDURecord, transmission_time=3.2),),
    ])
    def test_transmission_start__get(self, npdu_sequence):
        self.mock_uds_message_record.npdu_sequence = npdu_sequence
        assert UdsMessageRecord.transmission_start.fget(self=self.mock_uds_message_record) \
               == npdu_sequence[0].transmission_time

    # transmission_end

    @pytest.mark.parametrize("npdu_sequence", [
        (Mock(spec=AbstractNPDURecord, transmission_time=0),),
        (Mock(spec=AbstractNPDURecord, transmission_time=1), Mock(spec=AbstractNPDURecord, transmission_time=2)),
        (Mock(spec=AbstractNPDURecord, transmission_time=9654.3), Mock(spec=AbstractNPDURecord, transmission_time=-453),
         Mock(spec=AbstractNPDURecord, transmission_time=3.2),),
    ])
    def test_transmission_end__get(self, npdu_sequence):
        self.mock_uds_message_record.npdu_sequence = npdu_sequence
        assert UdsMessageRecord.transmission_end.fget(self=self.mock_uds_message_record) \
               == npdu_sequence[-1].transmission_time

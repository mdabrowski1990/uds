import pytest
from mock import Mock, patch

from uds.message.uds_message import UdsMessage, UdsMessageRecord, \
    AddressingType, ReassignmentError, AbstractUdsPacketRecord
from uds.transmission_attributes import TransmissionDirection


SCRIPT_LOCATION = "uds.message.uds_message"


class TestUdsMessage:
    """Unit tests for 'UdsMessage' class."""

    def setup_method(self):
        self.mock_uds_message = Mock(spec=UdsMessage)
        # patching
        self._patcher_validate_raw_bytes = patch(f"{SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
        self._patcher_validate_addressing = patch(f"{SCRIPT_LOCATION}.AddressingType.validate_member")
        self.mock_validate_addressing = self._patcher_validate_addressing.start()

    def teardown_method(self):
        self._patcher_validate_raw_bytes.stop()
        self._patcher_validate_addressing.stop()

    # __init__

    @pytest.mark.parametrize("payload", [None, [0x1, 0x02], "some message"])
    @pytest.mark.parametrize("addressing_type", ["Physical", 0, False, AddressingType.FUNCTIONAL])
    def test_init(self, payload, addressing_type):
        UdsMessage.__init__(self=self.mock_uds_message, payload=payload, addressing_type=addressing_type)
        assert self.mock_uds_message.payload == payload
        assert self.mock_uds_message.addressing_type == addressing_type

    # __eq__

    @pytest.mark.parametrize("message1, message2", [
        (Mock(spec=UdsMessage, payload=list(range(10)), addressing_type="some"),
         Mock(spec=UdsMessage, payload=list(range(10)), addressing_type="some")),
        (Mock(spec=UdsMessage, payload=list(range(10)), addressing_type="some"),
         Mock(spec=UdsMessage, payload=list(range(11)), addressing_type="some")),
        (Mock(spec=UdsMessage, payload=list(range(10)), addressing_type="some"),
         Mock(spec=UdsMessage, payload=list(range(10)), addressing_type="something else")),
        (Mock(spec=UdsMessage), Mock(spec=UdsMessage)),
    ])
    def test_eq(self, message1, message2):
        assert UdsMessage.__eq__(self=message1, other=message2) \
               is (message1.payload == message2.payload and message1.addressing_type == message2.addressing_type)

    @pytest.mark.parametrize("other_message", [Mock(spec=UdsMessageRecord), 1, Mock()])
    def test_eq__type_error(self, other_message):
        with pytest.raises(TypeError):
            UdsMessage.__eq__(self=self.mock_uds_message, other=other_message)

    # payload

    @pytest.mark.parametrize("value", [None, [0x1, 0x02], "some message"])
    def test_payload__get(self, value):
        self.mock_uds_message._UdsMessage__payload = value
        assert UdsMessage.payload.fget(self.mock_uds_message) is value

    def test_payload__set(self, example_raw_bytes):
        UdsMessage.payload.fset(self.mock_uds_message, value=example_raw_bytes)
        assert self.mock_uds_message._UdsMessage__payload == tuple(example_raw_bytes)
        self.mock_validate_raw_bytes.assert_called_once_with(example_raw_bytes)

    def test_payload__set_second_call(self, example_raw_bytes):
        self.mock_uds_message._UdsMessage__payload = "some value"
        self.test_payload__set(example_raw_bytes=example_raw_bytes)

    # addressing_type

    @pytest.mark.parametrize("value", [None, AddressingType.PHYSICAL, "some addressing"])
    def test_addressing_type__get(self, value):
        self.mock_uds_message._UdsMessage__addressing_type = value
        assert UdsMessage.addressing_type.fget(self.mock_uds_message) is value

    def test_addressing_type__set(self, example_addressing_type):
        UdsMessage.addressing_type.fset(self.mock_uds_message, value=example_addressing_type)
        assert self.mock_uds_message._UdsMessage__addressing_type == example_addressing_type
        self.mock_validate_addressing.assert_called_once_with(example_addressing_type)

    def test_addressing_type__set_second_call(self, example_addressing_type):
        self.mock_uds_message._UdsMessage__addressing_type = "some value"
        self.test_addressing_type__set(example_addressing_type=example_addressing_type)


class TestUdsMessageRecord:
    """Unit tests for 'UdsMessageRecord' class."""

    def setup_method(self):
        self.mock_uds_message_record = Mock(spec=UdsMessageRecord)
        # patching
        self._patcher_validate_raw_bytes = patch(f"{SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
        self._patcher_validate_addressing = patch(f"{SCRIPT_LOCATION}.AddressingType.validate_member")
        self.mock_validate_addressing = self._patcher_validate_addressing.start()

    def teardown_method(self):
        self._patcher_validate_raw_bytes.stop()
        self._patcher_validate_addressing.stop()

    # __init__

    @pytest.mark.parametrize("packets_records", [False, [1, 2, 3, 4], "abcdef"])
    def test_init(self, packets_records):
        UdsMessageRecord.__init__(self=self.mock_uds_message_record, packets_records=packets_records)
        assert self.mock_uds_message_record.packets_records == packets_records

    # __eq__

    @pytest.mark.parametrize("message1, message2", [
        (Mock(spec=UdsMessageRecord, payload=list(range(10)), addressing_type="some", direction="tx"),
         Mock(spec=UdsMessageRecord, payload=list(range(10)), addressing_type="some", direction="tx")),
        (Mock(spec=UdsMessageRecord, payload=list(range(10)), addressing_type="some", direction="rx"),
         Mock(spec=UdsMessageRecord, payload=list(range(11)), addressing_type="some", direction="rx")),
        (Mock(spec=UdsMessageRecord, payload=list(range(10)), addressing_type="some", direction="tx"),
         Mock(spec=UdsMessageRecord, payload=list(range(10)), addressing_type="something else", direction="tx")),
        (Mock(spec=UdsMessageRecord, payload=list(range(10)), addressing_type="some", direction="tx"),
         Mock(spec=UdsMessageRecord, payload=list(range(10)), addressing_type="some", direction="rx")),
        (Mock(spec=UdsMessageRecord), Mock(spec=UdsMessageRecord)),
    ])
    def test_eq(self, message1, message2):
        assert UdsMessageRecord.__eq__(self=message1, other=message2) \
               is (message1.payload == message2.payload
                   and message1.addressing_type == message2.addressing_type
                   and message1.direction == message2.direction)

    @pytest.mark.parametrize("other_message_record", [Mock(spec=UdsMessage), 1, Mock()])
    def test_eq__type_error(self, other_message_record):
        with pytest.raises(TypeError):
            UdsMessageRecord.__eq__(self=self.mock_uds_message_record, other=other_message_record)

    # __validate_packets_records

    @pytest.mark.parametrize("value", [
        (Mock(spec=AbstractUdsPacketRecord),),
        [Mock(spec=AbstractUdsPacketRecord), Mock(spec=AbstractUdsPacketRecord)],
        (Mock(spec=AbstractUdsPacketRecord), Mock(spec=AbstractUdsPacketRecord), Mock(spec=AbstractUdsPacketRecord))
    ])
    def test_validate_packets_records__valid(self, value):
        assert UdsMessageRecord._UdsMessageRecord__validate_packets_records(value=value) is None

    @pytest.mark.parametrize("value", [None, False, 0, Mock(spec=AbstractUdsPacketRecord)])
    def test_validate_packets_records__invalid_type(self, value):
        with pytest.raises(TypeError):
            UdsMessageRecord._UdsMessageRecord__validate_packets_records(value=value)

    @pytest.mark.parametrize("value", [tuple(), [], ["a"], (None, ), (Mock(spec=AbstractUdsPacketRecord), "not N_PDU")])
    def test_validate_packets_records__invalid_value(self, value):
        with pytest.raises(ValueError):
            UdsMessageRecord._UdsMessageRecord__validate_packets_records(value=value)

    # payload

    @pytest.mark.parametrize("packets", [
        [Mock(data_length=1, payload=[0x12])],
        (Mock(data_length=30, payload=(0xFE, 0xDC)), Mock(payload=None), Mock(payload=list(range(28)))),
        [Mock(data_length=10, payload=[0x1F, 0x2E, 0x3D, 0x4C]), Mock(payload=[0x5B, 0x6A, 0x79, 0x88, 0x97, 0xCC, 0xCC])]
    ])
    def test_payload__get(self, packets):
        self.mock_uds_message_record.packets_records = packets
        payload = UdsMessageRecord.payload.fget(self.mock_uds_message_record)
        assert isinstance(payload, tuple)
        assert len(payload) == self.mock_uds_message_record.packets_records[0].data_length

    # packets_records

    @pytest.mark.parametrize("value", [None, [Mock(), Mock()], "some sequence"])
    def test_packets_records__get(self, value):
        self.mock_uds_message_record._UdsMessageRecord__packets_records = value
        assert UdsMessageRecord.packets_records.fget(self.mock_uds_message_record) is value

    @pytest.mark.parametrize("packets_records", [
        (Mock(), Mock(), Mock()),
        [1, 2, 3, 4],
        "abcdefg"
    ])
    def test_packets_records__set__first_call(self, packets_records):
        UdsMessageRecord.packets_records.fset(self.mock_uds_message_record, value=packets_records)
        assert self.mock_uds_message_record._UdsMessageRecord__packets_records == tuple(packets_records)
        self.mock_uds_message_record._UdsMessageRecord__validate_packets_records.assert_called_once_with(packets_records)

    @pytest.mark.parametrize("old_value", [(Mock(), Mock(), Mock()), [1, 2, 3, 4], "abcdefg"])
    @pytest.mark.parametrize("new_value", [(Mock(), Mock(), Mock()), [1, 2, 3, 4], "abcdefg"])
    def test_packets_records__set__second_call(self, old_value, new_value):
        self.mock_uds_message_record._UdsMessageRecord__packets_records = old_value
        with pytest.raises(ReassignmentError):
            UdsMessageRecord.packets_records.fset(self.mock_uds_message_record, value=new_value)
        assert self.mock_uds_message_record._UdsMessageRecord__packets_records == old_value
        self.mock_uds_message_record._UdsMessageRecord__validate_packets_records.assert_not_called()

    # addressing_type

    @pytest.mark.parametrize("packets_records", [
        (Mock(spec=AbstractUdsPacketRecord, addressing_type=AddressingType.PHYSICAL),),
        (Mock(spec=AbstractUdsPacketRecord, addressing_type=AddressingType.FUNCTIONAL),
         Mock(spec=AbstractUdsPacketRecord, addressing_type=AddressingType.PHYSICAL)),
    ])
    def test_addressing_type__get(self, packets_records):
        self.mock_uds_message_record.packets_records = packets_records
        assert UdsMessageRecord.addressing_type.fget(self.mock_uds_message_record) == packets_records[0].addressing_type

    # direction

    @pytest.mark.parametrize("packets_records", [
        (Mock(spec=AbstractUdsPacketRecord, direction=TransmissionDirection.RECEIVED),),
        (Mock(spec=AbstractUdsPacketRecord, direction=TransmissionDirection.TRANSMITTED),
         Mock(spec=AbstractUdsPacketRecord, direction=TransmissionDirection.RECEIVED)),
    ])
    def test_direction__get(self, packets_records):
        self.mock_uds_message_record.packets_records = packets_records
        assert UdsMessageRecord.direction.fget(self.mock_uds_message_record) == packets_records[0].direction

    # transmission_start

    @pytest.mark.parametrize("packets_records", [
        (Mock(spec=AbstractUdsPacketRecord, transmission_time=0),),
        (Mock(spec=AbstractUdsPacketRecord, transmission_time=1), Mock(spec=AbstractUdsPacketRecord, transmission_time=2)),
        (Mock(spec=AbstractUdsPacketRecord, transmission_time=9654.3), Mock(spec=AbstractUdsPacketRecord, transmission_time=-453),
         Mock(spec=AbstractUdsPacketRecord, transmission_time=3.2),),
    ])
    def test_transmission_start__get(self, packets_records):
        self.mock_uds_message_record.packets_records = packets_records
        assert UdsMessageRecord.transmission_start.fget(self.mock_uds_message_record) \
               == packets_records[0].transmission_time

    # transmission_end

    @pytest.mark.parametrize("packets_records", [
        (Mock(spec=AbstractUdsPacketRecord, transmission_time=0),),
        (Mock(spec=AbstractUdsPacketRecord, transmission_time=1), Mock(spec=AbstractUdsPacketRecord, transmission_time=2)),
        (Mock(spec=AbstractUdsPacketRecord, transmission_time=9654.3), Mock(spec=AbstractUdsPacketRecord, transmission_time=-453),
         Mock(spec=AbstractUdsPacketRecord, transmission_time=3.2),),
    ])
    def test_transmission_end__get(self, packets_records):
        self.mock_uds_message_record.packets_records = packets_records
        assert UdsMessageRecord.transmission_end.fget(self.mock_uds_message_record) \
               == packets_records[-1].transmission_time

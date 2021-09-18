import pytest
from mock import Mock, patch

from uds.messages.uds_packet import AbstractUdsPacket, AbstractUdsPacketType, AbstractUdsPacketRecord, get_raw_packet_type, \
    AddressingType, NibbleEnum, ValidatedEnum, ExtendableEnum, TransmissionDirection, ReassignmentError


class TestFunctions:
    """Tests for helper functions in the package."""

    @pytest.mark.parametrize("raw_data, expected_result", [
        ([0x12], 0x1),
        ([0x00, 0x11, 0x22, 0x33], 0x0),
        ((0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10), 0xF),
        ((0xA5, 0x55, 0x33), 0xA),
    ])
    def test_get_raw_packet_type(self, raw_data, expected_result):
        assert get_raw_packet_type(raw_data) == expected_result


class TestAbstractPacketType:
    """Tests for 'AbstractPacketType' class."""

    def test_inheritance__nibble_enum(self):
        assert issubclass(AbstractUdsPacketType, NibbleEnum)

    def test_inheritance__validated_enum(self):
        assert issubclass(AbstractUdsPacketType, ValidatedEnum)

    def test_inheritance__extendable_enum(self):
        assert issubclass(AbstractUdsPacketType, ExtendableEnum)


class TestAbstractUdsPacket:
    """Tests for 'AbstractUdsPacket' class."""

    SCRIPT_LOCATION = "uds.messages.uds_packet"

    def setup(self):
        self.mock_abstract_packet = Mock(spec=AbstractUdsPacket)
        # patching
        self._patcher_validate_raw_bytes = patch(f"{self.SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
        self._patcher_validate_addressing_type = patch(f"{self.SCRIPT_LOCATION}.AddressingType.validate_member")
        self.mock_validate_addressing_type = self._patcher_validate_addressing_type.start()
        self._patcher_get_raw_packet_type = patch(f"{self.SCRIPT_LOCATION}.get_raw_packet_type")
        self.mock_get_raw_packet_type = self._patcher_get_raw_packet_type.start()

    def teardown(self):
        self._patcher_validate_raw_bytes.stop()
        self._patcher_validate_addressing_type.stop()
        self._patcher_get_raw_packet_type.stop()

    # __init__

    @pytest.mark.parametrize("raw_bytes", [None, 1, "some value", (1, 2, 3), [0x00, 0xFF]])
    @pytest.mark.parametrize("addressing_type", [None, 1, "some addressing", AddressingType.PHYSICAL])
    def test_init__valid(self, raw_bytes, addressing_type):
        AbstractUdsPacket.__init__(self=self.mock_abstract_packet, raw_data=raw_bytes, addressing=addressing_type)
        assert self.mock_abstract_packet.raw_data == raw_bytes
        assert self.mock_abstract_packet.addressing == addressing_type

    # raw_data

    @pytest.mark.parametrize("value_stored", [None, 0, (2, 3)])
    def test_raw_data__get(self, value_stored):
        self.mock_abstract_packet._AbstractUdsPacket__raw_data = value_stored
        assert AbstractUdsPacket.raw_data.fget(self=self.mock_abstract_packet) is value_stored

    def test_raw_data__set(self, example_raw_bytes):
        AbstractUdsPacket.raw_data.fset(self=self.mock_abstract_packet, value=example_raw_bytes)
        self.mock_validate_raw_bytes.assert_called_once_with(example_raw_bytes)
        assert self.mock_abstract_packet._AbstractUdsPacket__raw_data == tuple(example_raw_bytes)

    def test_raw_message__set_second_call(self, example_raw_bytes):
        self.mock_abstract_packet._AbstractUdsPacket__raw_data = "some value"
        self.test_raw_data__set(example_raw_bytes=example_raw_bytes)

    # addressing

    @pytest.mark.parametrize("value_stored", [None, 0, False, AddressingType.PHYSICAL])
    def test_addressing__get(self, value_stored):
        self.mock_abstract_packet._AbstractUdsPacket__addressing = value_stored
        assert AbstractUdsPacket.addressing.fget(self=self.mock_abstract_packet) is value_stored

    def test_addressing__set_instance(self, example_addressing_type):
        AbstractUdsPacket.addressing.fset(self=self.mock_abstract_packet, value=example_addressing_type)
        self.mock_validate_addressing_type.assert_called_once_with(example_addressing_type)
        assert self.mock_abstract_packet._AbstractUdsPacket__addressing == example_addressing_type

    def test_addressing__set_value(self, example_addressing_type):
        AbstractUdsPacket.addressing.fset(self=self.mock_abstract_packet, value=example_addressing_type.value)
        self.mock_validate_addressing_type.assert_called_once_with(example_addressing_type.value)
        assert self.mock_abstract_packet._AbstractUdsPacket__addressing == example_addressing_type

    def test_addressing__set_second_call(self, example_addressing_type):
        self.mock_abstract_packet._AbstractUdsPacket__addressing = "some value"
        self.test_addressing__set_instance(example_addressing_type=example_addressing_type)

    # packet_type

    def test_packet_type__get(self, example_raw_bytes):
        self.mock_abstract_packet.raw_data = example_raw_bytes
        assert AbstractUdsPacket.packet_type.fget(self=self.mock_abstract_packet) \
               is self.mock_abstract_packet.packet_type_enum.return_value
        self.mock_get_raw_packet_type.assert_called_once_with(example_raw_bytes)
        self.mock_abstract_packet.packet_type_enum.assert_called_once_with(self.mock_get_raw_packet_type.return_value)


class TestAbstractUdsPacketRecord:
    """Tests for 'AbstractUdsPacketRecord' class."""

    SCRIPT_LOCATION = TestAbstractUdsPacket.SCRIPT_LOCATION

    def setup(self):
        self.mock_packet_record = Mock(spec=AbstractUdsPacketRecord)
        # patching
        self._patcher_validate_direction = patch(f"{self.SCRIPT_LOCATION}.TransmissionDirection.validate_member")
        self.mock_validate_direction = self._patcher_validate_direction.start()
        self._patcher_get_raw_packet_type = patch(f"{self.SCRIPT_LOCATION}.get_raw_packet_type")
        self.mock_get_raw_packet_type = self._patcher_get_raw_packet_type.start()

    def teardown(self):
        self._patcher_validate_direction.stop()

    # __init__

    @pytest.mark.parametrize("frame", [None, Mock(), 1])
    @pytest.mark.parametrize("direction", ["Some Direction"] + list(TransmissionDirection))
    def test_init(self, frame, direction):
        AbstractUdsPacketRecord.__init__(self=self.mock_packet_record, frame=frame, direction=direction)
        assert self.mock_packet_record.frame == frame
        assert self.mock_packet_record.direction == direction

    # frame

    @pytest.mark.parametrize("frame", [None, 0, "some frame"])
    def test_frame__get(self, frame):
        self.mock_packet_record._AbstractUdsPacketRecord__frame = frame
        assert AbstractUdsPacketRecord.frame.fget(self=self.mock_packet_record) == frame

    @pytest.mark.parametrize("frame", [None, 0, "some frame"])
    def test_frame__set(self, frame):
        AbstractUdsPacketRecord.frame.fset(self=self.mock_packet_record, value=frame)
        assert self.mock_packet_record._AbstractUdsPacketRecord__frame == frame
        self.mock_packet_record._AbstractUdsPacketRecord__validate_frame.assert_called_once_with(frame)

    @pytest.mark.parametrize("old_value", [None, 0, "some frame"])
    @pytest.mark.parametrize("new_value", [None, True, "some frame", "some other frame"])
    def test_frame__set__second_attempt(self, old_value, new_value):
        self.mock_packet_record._AbstractUdsPacketRecord__frame = old_value
        with pytest.raises(ReassignmentError):
            AbstractUdsPacketRecord.frame.fset(self=self.mock_packet_record, value=new_value)
        assert self.mock_packet_record._AbstractUdsPacketRecord__frame == old_value
        self.mock_packet_record._AbstractUdsPacketRecord__validate_frame.assert_not_called()

    # direction

    @pytest.mark.parametrize("direction", [None, "some direction"] + list(TransmissionDirection))
    def test_direction__get(self, direction):
        self.mock_packet_record._AbstractUdsPacketRecord__direction = direction
        assert AbstractUdsPacketRecord.direction.fget(self=self.mock_packet_record) == direction

    def test_direction__set_instance(self, example_transmission_direction):
        AbstractUdsPacketRecord.direction.fset(self=self.mock_packet_record, value=example_transmission_direction)
        assert self.mock_packet_record._AbstractUdsPacketRecord__direction == example_transmission_direction
        self.mock_validate_direction.assert_called_once_with(example_transmission_direction)

    def test_direction__set_value(self, example_transmission_direction):
        AbstractUdsPacketRecord.direction.fset(self=self.mock_packet_record, value=example_transmission_direction.value)
        assert self.mock_packet_record._AbstractUdsPacketRecord__direction == example_transmission_direction
        self.mock_validate_direction.assert_called_once_with(example_transmission_direction.value)

    @pytest.mark.parametrize("old_value", [None, 0, "some direction"])
    @pytest.mark.parametrize("new_value", [None, True, "some direction", "some other direction"])
    def test_direction__set__second_attempt(self, old_value, new_value):
        self.mock_packet_record._AbstractUdsPacketRecord__direction = old_value
        with pytest.raises(ReassignmentError):
            AbstractUdsPacketRecord.direction.fset(self=self.mock_packet_record, value=new_value)
        assert self.mock_packet_record._AbstractUdsPacketRecord__direction == old_value
        self.mock_validate_direction.assert_not_called()

    # packet_type

    def test_packet_type__get(self, example_raw_bytes):
        self.mock_packet_record.raw_data = example_raw_bytes
        assert AbstractUdsPacketRecord.packet_type.fget(self=self.mock_packet_record) \
               is self.mock_packet_record.packet_type_enum.return_value
        self.mock_get_raw_packet_type.assert_called_once_with(example_raw_bytes)
        self.mock_packet_record.packet_type_enum.assert_called_once_with(self.mock_get_raw_packet_type.return_value)

import pytest
from mock import Mock, patch

from uds.packet.abstract_packet import (
    AbstractPacketContainer,
    AbstractPacketRecord,
    AddressingType,
    ReassignmentError,
    TransmissionDirection,
    datetime,
)

SCRIPT_LOCATION = "uds.packet.abstract_packet"


class TestAbstractPacketContainer:
    """Unit tests for 'AbstractPacketContainer' class."""

    def setup_method(self):
        self.mock_packet_container = Mock(spec=AbstractPacketContainer)

    # __str__

    @pytest.mark.parametrize("payload, raw_frame_data", [
        (None, b"\x00\xFF\xF1\xB9\x8A"),
        ([0xBE, 0xEF, 0xFF, 0x00], bytearray([0x50, 0x61, 0x72, 0x83, 0x94, 0xA5, 0xB6, 0xC7, 0xD8, 0xE9, 0xFA])),
    ])
    def test_str(self, payload, raw_frame_data):
        self.mock_packet_container.payload = payload
        self.mock_packet_container.raw_frame_data = raw_frame_data
        output_str = AbstractPacketContainer.__str__(self=self.mock_packet_container)
        assert output_str.startswith("AbstractPacketContainer(") and output_str.endswith(")")
        assert "payload=" in output_str
        assert "addressing_type=" in output_str
        assert "raw_frame_data=" in output_str
        assert "packet_type=" in output_str


class TestAbstractPacketRecord:
    """Unit tests for 'AbstractPacketRecord' class."""

    def setup_method(self):
        self.mock_packet_record = Mock(spec=AbstractPacketRecord)
        # patching
        self._patcher_validate_direction = patch(f"{SCRIPT_LOCATION}.TransmissionDirection.validate_member")
        self.mock_validate_direction = self._patcher_validate_direction.start()

    def teardown_method(self):
        self._patcher_validate_direction.stop()

    # __init__

    @pytest.mark.parametrize("frame", [Mock(), 1])
    @pytest.mark.parametrize("direction", ["Some Direction", "another direction"])
    @pytest.mark.parametrize("transmission_time", ["timestamp", 2.32])
    def test_init(self, frame, direction, transmission_time):
        AbstractPacketRecord.__init__(self=self.mock_packet_record,
                                      frame=frame,
                                      direction=direction,
                                      transmission_time=transmission_time)
        assert self.mock_packet_record.frame == frame
        assert self.mock_packet_record.direction == direction
        assert self.mock_packet_record.transmission_time == transmission_time

    # __str__

    @pytest.mark.parametrize("payload, raw_frame_data", [
        (None, b"\x00\xFF\xF1\xB9\x8A"),
        ([0xBE, 0xEF, 0xFF, 0x00], bytearray([0x50, 0x61, 0x72, 0x83, 0x94, 0xA5, 0xB6, 0xC7, 0xD8, 0xE9, 0xFA])),
    ])
    def test_str(self, payload, raw_frame_data):
        self.mock_packet_record.payload = payload
        self.mock_packet_record.raw_frame_data = raw_frame_data
        output_str = AbstractPacketRecord.__str__(self=self.mock_packet_record)
        assert output_str.startswith("AbstractPacketRecord(") and output_str.endswith(")")
        assert "payload=" in output_str
        assert "addressing_type=" in output_str
        assert "raw_frame_data=" in output_str
        assert "packet_type=" in output_str
        assert "direction=" in output_str
        assert "transmission_time=" in output_str

    # frame

    @pytest.mark.parametrize("frame", [None, 0, "some frame"])
    def test_frame__get(self, frame):
        self.mock_packet_record._AbstractPacketRecord__frame = frame
        assert AbstractPacketRecord.frame.fget(self.mock_packet_record) == frame

    @pytest.mark.parametrize("frame", [None, 0, "some frame"])
    def test_frame__set(self, frame):
        AbstractPacketRecord.frame.fset(self.mock_packet_record, value=frame)
        assert self.mock_packet_record._AbstractPacketRecord__frame == frame
        self.mock_packet_record._validate_frame.assert_called_once_with(frame)

    @pytest.mark.parametrize("old_value", [None, 0, "some frame"])
    @pytest.mark.parametrize("new_value", [None, True, "some frame"])
    def test_frame__set__second_attempt(self, old_value, new_value):
        self.mock_packet_record._AbstractPacketRecord__frame = old_value
        with pytest.raises(ReassignmentError):
            AbstractPacketRecord.frame.fset(self.mock_packet_record, value=new_value)
        assert self.mock_packet_record._AbstractPacketRecord__frame == old_value
        self.mock_packet_record._validate_frame.assert_not_called()

    # direction

    def test_direction__get(self):
        self.mock_packet_record._AbstractPacketRecord__direction = Mock()
        assert (AbstractPacketRecord.direction.fget(self.mock_packet_record)
                == self.mock_packet_record._AbstractPacketRecord__direction)

    def test_direction__set(self, example_transmission_direction):
        AbstractPacketRecord.direction.fset(self.mock_packet_record, value=example_transmission_direction)
        assert self.mock_packet_record._AbstractPacketRecord__direction == self.mock_validate_direction.return_value
        self.mock_validate_direction.assert_called_once_with(example_transmission_direction)

    @pytest.mark.parametrize("value", [Mock(), "some direction"])
    def test_direction__set__second_attempt(self, value):
        self.mock_packet_record._AbstractPacketRecord__direction = Mock()
        with pytest.raises(ReassignmentError):
            AbstractPacketRecord.direction.fset(self.mock_packet_record, value=value)

    # transmission_time

    def test_transmission_time__get(self):
        self.mock_packet_record._AbstractPacketRecord__transmission_time = Mock()
        assert (AbstractPacketRecord.transmission_time.fget(self.mock_packet_record)
                == self.mock_packet_record._AbstractPacketRecord__transmission_time)

    def test_transmission_time__set(self):
        value = Mock(spec=datetime)
        AbstractPacketRecord.transmission_time.fset(self.mock_packet_record, value=value)
        assert self.mock_packet_record._AbstractPacketRecord__transmission_time == value

    @pytest.mark.parametrize("value", [Mock(), "not a timestamp"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_transmission_time__set__invalid_type(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractPacketRecord.transmission_time.fset(self.mock_packet_record, value=value)
        mock_isinstance.assert_called_once_with(value, datetime)

    @pytest.mark.parametrize("value", [Mock(), "some transmission_time"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_transmission_time__set__second_attempt(self, mock_isinstance, value):
        self.mock_packet_record._AbstractPacketRecord__transmission_time = Mock()
        mock_isinstance.return_value = True
        with pytest.raises(ReassignmentError):
            AbstractPacketRecord.transmission_time.fset(self.mock_packet_record, value=value)

from unittest.mock import MagicMock

import pytest
from mock import Mock, patch

from uds.packet.abstract_packet import AbstractPacketContainer, AbstractPacketRecord, ReassignmentError, datetime

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
        self._patcher_warn = patch(f"{SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()
        self._patcher_perf_counter = patch(f"{SCRIPT_LOCATION}.perf_counter")
        self.mock_perf_counter = self._patcher_perf_counter.start()
        self._patcher_datetime = patch(f"{SCRIPT_LOCATION}.datetime")
        self.mock_datetime = self._patcher_datetime.start()
        self._patcher_validate_direction = patch(f"{SCRIPT_LOCATION}.TransmissionDirection.validate_member")
        self.mock_validate_direction = self._patcher_validate_direction.start()

    def teardown_method(self):
        self._patcher_warn.stop()
        self._patcher_validate_direction.stop()

    # __init__

    @pytest.mark.parametrize("frame, direction, transmission_time, transmission_timestamp", [
        (Mock(), Mock(), Mock(), Mock()),
        ("Some frame", "Some direction", "Some time", "Some timestamp"),
    ])
    def test_init(self, frame, direction, transmission_time, transmission_timestamp):
        AbstractPacketRecord.__init__(self=self.mock_packet_record,
                                      frame=frame,
                                      direction=direction,
                                      transmission_time=transmission_time,
                                      transmission_timestamp=transmission_timestamp)
        assert self.mock_packet_record.frame == frame
        assert self.mock_packet_record.direction == direction
        assert self.mock_packet_record.transmission_time == transmission_time
        assert self.mock_packet_record.transmission_timestamp == transmission_timestamp
        self.mock_packet_record._validate_attributes.assert_called_once_with()

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
        assert "transmission_timestamp=" in output_str

    # frame

    @pytest.mark.parametrize("frame", [Mock(), "some frame"])
    def test_frame__get(self, frame):
        self.mock_packet_record._AbstractPacketRecord__frame = frame
        assert AbstractPacketRecord.frame.fget(self.mock_packet_record) == frame

    @pytest.mark.parametrize("frame", [Mock(), "some frame"])
    def test_frame__set(self, frame):
        AbstractPacketRecord.frame.fset(self.mock_packet_record, value=frame)
        assert self.mock_packet_record._AbstractPacketRecord__frame == frame
        self.mock_packet_record._validate_frame.assert_called_once_with(frame)

    @pytest.mark.parametrize("value", [Mock(), "some frame"])
    def test_frame__set__second_attempt(self, value):
        self.mock_packet_record._AbstractPacketRecord__frame = Mock()
        with pytest.raises(ReassignmentError):
            AbstractPacketRecord.frame.fset(self.mock_packet_record, value=value)
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

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_transmission_time__set__with_warning(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_is_future = Mock(return_value=True)
        value = MagicMock(spec=datetime, __gt__=mock_is_future)
        AbstractPacketRecord.transmission_time.fset(self.mock_packet_record, value=value)
        assert (self.mock_packet_record._AbstractPacketRecord__transmission_time
                == self.mock_datetime.now.return_value)
        self.mock_datetime.now.assert_called_once()
        mock_is_future.assert_called_once_with(value, self.mock_datetime.now.return_value)
        self.mock_warn.assert_called_once()
        mock_isinstance.assert_called_once_with(value, self.mock_datetime)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_transmission_time__set__without_warning(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_is_future = Mock(return_value=False)
        value = MagicMock(spec=datetime, __gt__=mock_is_future)
        AbstractPacketRecord.transmission_time.fset(self.mock_packet_record, value=value)
        assert (self.mock_packet_record._AbstractPacketRecord__transmission_time
                == value)
        self.mock_datetime.now.assert_called_once()
        mock_is_future.assert_called_once_with(value, self.mock_datetime.now.return_value)
        self.mock_warn.assert_not_called()
        mock_isinstance.assert_called_once_with(value, self.mock_datetime)

    @pytest.mark.parametrize("value", [Mock(), "not a timestamp"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_transmission_time__set__invalid_type(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractPacketRecord.transmission_time.fset(self.mock_packet_record, value=value)
        mock_isinstance.assert_called_once_with(value, self.mock_datetime)

    @pytest.mark.parametrize("value", [Mock(), "some transmission_time"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_transmission_time__set__second_attempt(self, mock_isinstance, value):
        self.mock_packet_record._AbstractPacketRecord__transmission_time = Mock()
        mock_isinstance.return_value = True
        with pytest.raises(ReassignmentError):
            AbstractPacketRecord.transmission_time.fset(self.mock_packet_record, value=value)

    # transmission_timestamp

    def test_transmission_timestamp__get(self):
        self.mock_packet_record._AbstractPacketRecord__transmission_timestamp = Mock()
        assert (AbstractPacketRecord.transmission_timestamp.fget(self.mock_packet_record)
                == self.mock_packet_record._AbstractPacketRecord__transmission_timestamp)

    def test_transmission_timestamp__set__with_warning(self):
        mock_is_future = Mock(return_value=True)
        value = MagicMock(spec=float, __gt__=mock_is_future)
        AbstractPacketRecord.transmission_timestamp.fset(self.mock_packet_record, value=value)
        assert (self.mock_packet_record._AbstractPacketRecord__transmission_timestamp
                == self.mock_perf_counter.return_value)
        self.mock_perf_counter.assert_called_once()
        mock_is_future.assert_called_once_with(value, self.mock_perf_counter.return_value)
        self.mock_warn.assert_called_once()

    def test_transmission_timestamp__set__without_warning(self):
        mock_is_future = Mock(return_value=False)
        value = MagicMock(spec=float, __gt__=mock_is_future)
        AbstractPacketRecord.transmission_timestamp.fset(self.mock_packet_record, value=value)
        assert (self.mock_packet_record._AbstractPacketRecord__transmission_timestamp
                == value)
        self.mock_perf_counter.assert_called_once()
        mock_is_future.assert_called_once_with(value, self.mock_perf_counter.return_value)
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("value", [Mock(), "not a timestamp"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_transmission_timestamp__set__invalid_type(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractPacketRecord.transmission_timestamp.fset(self.mock_packet_record, value=value)
        mock_isinstance.assert_called_once_with(value, float)

    @pytest.mark.parametrize("value", [Mock(), "some transmission_timestamp"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_transmission_timestamp__set__second_attempt(self, mock_isinstance, value):
        self.mock_packet_record._AbstractPacketRecord__transmission_timestamp = Mock()
        mock_isinstance.return_value = True
        with pytest.raises(ReassignmentError):
            AbstractPacketRecord.transmission_timestamp.fset(self.mock_packet_record, value=value)

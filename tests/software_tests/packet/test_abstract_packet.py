import pytest
from mock import Mock, patch

from uds.packet.abstract_packet import AbstractUdsPacketRecord, \
    TransmissionDirection, ReassignmentError, TimeStamp


class TestAbstractUdsPacketRecord:
    """Unit tests for 'AbstractUdsPacketRecord' class."""

    SCRIPT_LOCATION = "uds.packet.abstract_packet"

    def setup(self):
        self.mock_packet_record = Mock(spec=AbstractUdsPacketRecord)
        # patching
        self._patcher_validate_direction = patch(f"{self.SCRIPT_LOCATION}.TransmissionDirection.validate_member")
        self.mock_validate_direction = self._patcher_validate_direction.start()

    def teardown(self):
        self._patcher_validate_direction.stop()

    # __init__

    @pytest.mark.parametrize("frame", [Mock(), 1])
    @pytest.mark.parametrize("direction", ["Some Direction", "another direction"])
    @pytest.mark.parametrize("transmission_time", ["timestamp", 2.32])
    def test_init(self, frame, direction, transmission_time):
        AbstractUdsPacketRecord.__init__(self=self.mock_packet_record,
                                         frame=frame,
                                         direction=direction,
                                         transmission_time=transmission_time)
        assert self.mock_packet_record.frame == frame
        assert self.mock_packet_record.direction == direction
        assert self.mock_packet_record.transmission_time == transmission_time

    # frame

    @pytest.mark.parametrize("frame", [None, 0, "some frame"])
    def test_frame__get(self, frame):
        self.mock_packet_record._AbstractUdsPacketRecord__frame = frame
        assert AbstractUdsPacketRecord.frame.fget(self=self.mock_packet_record) == frame

    @pytest.mark.parametrize("frame", [None, 0, "some frame"])
    def test_frame__set(self, frame):
        AbstractUdsPacketRecord.frame.fset(self=self.mock_packet_record, value=frame)
        assert self.mock_packet_record._AbstractUdsPacketRecord__frame == frame
        self.mock_packet_record._validate_frame.assert_called_once_with(frame)

    @pytest.mark.parametrize("old_value", [None, 0, "some frame"])
    @pytest.mark.parametrize("new_value", [None, True, "some frame"])
    def test_frame__set__second_attempt(self, old_value, new_value):
        self.mock_packet_record._AbstractUdsPacketRecord__frame = old_value
        with pytest.raises(ReassignmentError):
            AbstractUdsPacketRecord.frame.fset(self=self.mock_packet_record, value=new_value)
        assert self.mock_packet_record._AbstractUdsPacketRecord__frame == old_value
        self.mock_packet_record._validate_frame.assert_not_called()

    # direction

    @pytest.mark.parametrize("direction", [None, "some direction"] + list(TransmissionDirection))
    def test_direction__get(self, direction):
        self.mock_packet_record._AbstractUdsPacketRecord__direction = direction
        assert AbstractUdsPacketRecord.direction.fget(self=self.mock_packet_record) == direction

    def test_direction__set(self, example_transmission_direction):
        AbstractUdsPacketRecord.direction.fset(self=self.mock_packet_record, value=example_transmission_direction)
        assert self.mock_packet_record._AbstractUdsPacketRecord__direction == example_transmission_direction
        self.mock_validate_direction.assert_called_once_with(example_transmission_direction)

    @pytest.mark.parametrize("old_value", [None, 0, "some direction"])
    @pytest.mark.parametrize("new_value", [None, True, "some direction"])
    def test_direction__set__second_attempt(self, old_value, new_value):
        self.mock_packet_record._AbstractUdsPacketRecord__direction = old_value
        with pytest.raises(ReassignmentError):
            AbstractUdsPacketRecord.direction.fset(self=self.mock_packet_record, value=new_value)
        assert self.mock_packet_record._AbstractUdsPacketRecord__direction == old_value
        self.mock_validate_direction.assert_not_called()

    # transmission_time

    @pytest.mark.parametrize("transmission_time", [None, 0, "some transmission_time"])
    def test_transmission_time__get(self, transmission_time):
        self.mock_packet_record._AbstractUdsPacketRecord__transmission_time = transmission_time
        assert AbstractUdsPacketRecord.transmission_time.fget(self=self.mock_packet_record) == transmission_time

    def test_transmission_time__set(self):
        value = Mock(spec=TimeStamp)
        AbstractUdsPacketRecord.transmission_time.fset(self=self.mock_packet_record, value=value)
        assert self.mock_packet_record._AbstractUdsPacketRecord__transmission_time == value

    @pytest.mark.parametrize("value", [None, "not a timestamp"])
    def test_transmission_time__set__invalid_type(self, value):
        with pytest.raises(TypeError):
            AbstractUdsPacketRecord.transmission_time.fset(self=self.mock_packet_record, value=value)

    @pytest.mark.parametrize("old_value", [None, 0, "some transmission_time"])
    @pytest.mark.parametrize("new_value", [None, True, Mock(spec=TimeStamp)])
    def test_transmission_time__set__second_attempt(self, old_value, new_value):
        self.mock_packet_record._AbstractUdsPacketRecord__transmission_time = old_value
        with pytest.raises(ReassignmentError):
            AbstractUdsPacketRecord.transmission_time.fset(self=self.mock_packet_record, value=new_value)
        assert self.mock_packet_record._AbstractUdsPacketRecord__transmission_time == old_value

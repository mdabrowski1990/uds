from time import perf_counter

import pytest
from mock import Mock, patch

from uds.can import CanFlowStatus, CanPacketType
from uds.can.packet.can_packet_record import (
    AddressingType,
    CanAddressingFormat,
    CanPacketRecord,
    PythonCanFrame,
    ReassignmentError,
    TransmissionDirection,
    datetime,
)

SCRIPT_LOCATION = "uds.can.packet.can_packet_record"


class TestCanPacketRecord:
    """Unit tests for `CanPacketRecord` class."""

    def setup_method(self):
        self.mock_can_packet_record = Mock(spec=CanPacketRecord)
        # patching
        self._patcher_abstract_packet_record_init = patch(f"{SCRIPT_LOCATION}.AbstractPacketRecord.__init__")
        self.mock_abstract_packet_record_init = self._patcher_abstract_packet_record_init.start()
        self._patcher_addressing_type = patch(f"{SCRIPT_LOCATION}.AddressingType")
        self.mock_addressing_type = self._patcher_addressing_type.start()
        self._patcher_can_addressing_format = patch(f"{SCRIPT_LOCATION}.CanAddressingFormat")
        self.mock_can_addressing_format = self._patcher_can_addressing_format.start()
        self._patcher_can_addressing_information = patch(f"{SCRIPT_LOCATION}.CanAddressingInformation")
        self.mock_can_addressing_information = self._patcher_can_addressing_information.start()
        self._patcher_can_packet_type = patch(f"{SCRIPT_LOCATION}.CanPacketType")
        self.mock_can_packet_type = self._patcher_can_packet_type.start()

    def teardown_method(self):
        self._patcher_abstract_packet_record_init.stop()
        self._patcher_addressing_type.stop()
        self._patcher_can_addressing_format.stop()
        self._patcher_can_addressing_information.stop()
        self._patcher_can_packet_type.stop()

    # __init__

    @pytest.mark.parametrize("frame, direction, addressing_type, addressing_format, "
                             "transmission_time, transmission_timestamp", [
        (Mock(), Mock(), Mock(), Mock(), Mock(), Mock()),
        (Mock(spec=PythonCanFrame), TransmissionDirection.RECEIVED, AddressingType.FUNCTIONAL,
         CanAddressingFormat.NORMAL_ADDRESSING, Mock(spec=datetime), Mock(spec=float)),
    ])
    def test_init(self, frame, direction, addressing_type, addressing_format,
                  transmission_time, transmission_timestamp):
        assert CanPacketRecord.__init__(self=self.mock_can_packet_record,
                                        frame=frame,
                                        addressing_format=addressing_format,
                                        addressing_type=addressing_type,
                                        direction=direction,
                                        transmission_time=transmission_time,
                                        transmission_timestamp=transmission_timestamp) is None
        assert self.mock_can_packet_record.addressing_format == addressing_format
        assert self.mock_can_packet_record.addressing_type == addressing_type
        self.mock_abstract_packet_record_init.assert_called_once_with(frame=frame,
                                                                      direction=direction,
                                                                      transmission_time=transmission_time,
                                                                      transmission_timestamp=transmission_timestamp)

    # __str__

    @pytest.mark.parametrize("payload, raw_frame_data", [
        (None, b"\x00\xFF\xF1\xB9\x8A"),
        ([0xBE, 0xEF, 0xFF, 0x00], bytearray([0x50, 0x61, 0x72, 0x83, 0x94, 0xA5, 0xB6, 0xC7, 0xD8, 0xE9, 0xFA])),
    ])
    def test_str(self, payload, raw_frame_data):
        self.mock_can_packet_record.payload = payload
        self.mock_can_packet_record.raw_frame_data = raw_frame_data
        output_str = CanPacketRecord.__str__(self=self.mock_can_packet_record)
        assert output_str.startswith("CanPacketRecord(") and output_str.endswith(")")
        assert "payload=" in output_str
        assert "addressing_type=" in output_str
        assert "addressing_format=" in output_str
        assert "raw_frame_data=" in output_str
        assert "packet_type=" in output_str
        assert "can_id=" in output_str
        assert "direction=" in output_str
        assert "transmission_time=" in output_str

    # can_id

    def test_can_id__python_can(self):
        self.mock_can_packet_record.frame = Mock(spec=PythonCanFrame)
        assert (CanPacketRecord.can_id.fget(self.mock_can_packet_record)
                == self.mock_can_packet_record.frame.arbitration_id)

    def test_can_id__not_implemented(self):
        with pytest.raises(NotImplementedError):
            CanPacketRecord.can_id.fget(self.mock_can_packet_record)

    # raw_frame_data

    @pytest.mark.parametrize("raw_frame_data", [b"some raw data", range(10)])
    def test_raw_frame_data__python_can(self, raw_frame_data):
        self.mock_can_packet_record.frame = Mock(spec=PythonCanFrame, data=raw_frame_data)
        assert (CanPacketRecord.raw_frame_data.fget(self.mock_can_packet_record)
                == bytes(self.mock_can_packet_record.frame.data))

    def test_raw_frame_data__not_implemented(self):
        with pytest.raises(NotImplementedError):
            CanPacketRecord.raw_frame_data.fget(self.mock_can_packet_record)

    # addressing_format

    def test_addressing_format__get(self):
        self.mock_can_packet_record._CanPacketRecord__addressing_format = Mock()
        assert (CanPacketRecord.addressing_format.fget(self.mock_can_packet_record)
                == self.mock_can_packet_record._CanPacketRecord__addressing_format)

    def test_addressing_format__set__reassignment_error(self):
        self.mock_can_packet_record._CanPacketRecord__addressing_format = Mock()
        with pytest.raises(ReassignmentError):
            CanPacketRecord.addressing_format.fset(self.mock_can_packet_record, Mock())

    @pytest.mark.parametrize("value", [Mock(), CanAddressingFormat.NORMAL_ADDRESSING])
    def test_addressing_format__set__valid(self, value):
        assert CanPacketRecord.addressing_format.fset(self.mock_can_packet_record, value) is None
        assert (self.mock_can_packet_record._CanPacketRecord__addressing_format
                == self.mock_can_addressing_format.validate_member.return_value)
        self.mock_can_addressing_format.validate_member.assert_called_once_with(value)

    # addressing_type

    def test_addressing_type__get(self):
        self.mock_can_packet_record._CanPacketRecord__addressing_type = Mock()
        assert (CanPacketRecord.addressing_type.fget(self.mock_can_packet_record)
                == self.mock_can_packet_record._CanPacketRecord__addressing_type)

    def test_addressing_type__set__reassignment_error(self):
        self.mock_can_packet_record._CanPacketRecord__addressing_type = Mock()
        with pytest.raises(ReassignmentError):
            CanPacketRecord.addressing_type.fset(self.mock_can_packet_record, Mock())

    @pytest.mark.parametrize("value", [Mock(), CanAddressingFormat.NORMAL_ADDRESSING])
    def test_addressing_type__set__valid(self, value):
        assert CanPacketRecord.addressing_type.fset(self.mock_can_packet_record, value) is None
        assert (self.mock_can_packet_record._CanPacketRecord__addressing_type
                == self.mock_addressing_type.validate_member.return_value)
        self.mock_addressing_type.validate_member.assert_called_once_with(value)

    # _validate_frame

    @pytest.mark.parametrize("frame", [None, Mock()])
    def test_validate_frame__type_error(self, frame):
        with pytest.raises(TypeError):
            CanPacketRecord._validate_frame(frame)

    def test_validate_frame__python_can(self, example_python_can_message):
        assert CanPacketRecord._validate_frame(example_python_can_message) is None

    # _validate_attributes

    def test_validate_attributes(self):
        assert CanPacketRecord._validate_attributes(self.mock_can_packet_record) is None
        self.mock_can_addressing_information.validate_addressing_params.assert_called_once_with(
            addressing_format=self.mock_can_packet_record.addressing_format,
            addressing_type=self.mock_can_packet_record.addressing_type,
            can_id=self.mock_can_packet_record.can_id,
            target_address=self.mock_can_packet_record.target_address,
            source_address=self.mock_can_packet_record.source_address,
            address_extension=self.mock_can_packet_record.address_extension)
        self.mock_can_packet_type.validate_member.assert_called_once_with(self.mock_can_packet_record.packet_type)


@pytest.mark.integration
class TestCanPacketRecordIntegration:
    """Integration tests for `CanPacketRecord` class."""

    @pytest.mark.parametrize("kwargs, expected_attribute_values", [
        ({"frame": PythonCanFrame(arbitration_id=0x69C,
                                  is_extended_id=False,
                                  dlc=2,
                                  data=[0x01, 0x3E]),
          "direction": TransmissionDirection.RECEIVED,
          "addressing_type": AddressingType.PHYSICAL,
          "addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
          "transmission_time": datetime.now(),
          "transmission_timestamp": perf_counter()},
         {"raw_frame_data": b"\x01\x3E",
          "addressing_type": AddressingType.PHYSICAL,
          "addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
          "packet_type": CanPacketType.SINGLE_FRAME,
          "payload": b"\x3E",
          "data_length": 1,
          "can_id": 0x69C,
          "dlc": 2,
          "target_address": None,
          "source_address": None,
          "address_extension": None,
          "sequence_number": None,
          "flow_status": None,
          "block_size": None,
          "st_min": None,
          "direction": TransmissionDirection.RECEIVED}),
        ({"frame": PythonCanFrame(arbitration_id=0x18CD9BE0,
                                  is_extended_id=True,
                                  data=[0x37, 0x30, 0x08, 0xF1] + ([0x99] * 60),
                                  is_fd=True,
                                  bitrate_switch=True),
          "direction": TransmissionDirection.TRANSMITTED,
          "addressing_type": AddressingType.FUNCTIONAL,
          "addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "transmission_time": datetime.now(),
          "transmission_timestamp": perf_counter()},
         {"raw_frame_data": bytes([0x37, 0x30, 0x08, 0xF1] + ([0x99] * 60)),
          "addressing_type": AddressingType.FUNCTIONAL,
          "addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "packet_type": CanPacketType.FLOW_CONTROL,
          "payload": None,
          "data_length": None,
          "can_id": 0x18CD9BE0,
          "dlc": 0xF,
          "target_address": 0x9B,
          "source_address": 0xE0,
          "address_extension": 0x37,
          "sequence_number": None,
          "flow_status": CanFlowStatus.ContinueToSend,
          "block_size": 0x08,
          "st_min": 0xF1,
          "direction": TransmissionDirection.TRANSMITTED}),
    ])
    def test_init(self, kwargs, expected_attribute_values):
        packet_record = CanPacketRecord(**kwargs)
        for attr_name, attr_value in expected_attribute_values.items():
            assert getattr(packet_record, attr_name) == attr_value
        assert packet_record.frame == kwargs["frame"]
        assert packet_record.transmission_time == kwargs["transmission_time"]
        assert packet_record.transmission_timestamp == kwargs["transmission_timestamp"]

    @pytest.mark.parametrize("kwargs", [
        {"frame": PythonCanFrame(arbitration_id=0x68A,
                                 is_extended_id=False,
                                 dlc=8,
                                 data=[0xFF] * 8),
         "direction": TransmissionDirection.TRANSMITTED,
         "addressing_type": AddressingType.PHYSICAL,
         "addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
         "transmission_time": datetime.now(),
         "transmission_timestamp": perf_counter()},
        {"frame": PythonCanFrame(arbitration_id=0x12345678,
                                 is_extended_id=True,
                                 dlc=3,
                                 data=[0xFE, 0x01, 0x3E]),
         "direction": TransmissionDirection.RECEIVED,
         "addressing_type": AddressingType.FUNCTIONAL,
         "addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         "transmission_time": datetime.now(),
         "transmission_timestamp": perf_counter()},
    ])
    def test_init__value_error(self, kwargs):
        with pytest.raises(ValueError):
            CanPacketRecord(**kwargs)

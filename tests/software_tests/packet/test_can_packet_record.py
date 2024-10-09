from datetime import datetime

import pytest
from mock import Mock, patch

from uds.can import CanFlowStatus
from uds.packet.can_packet_record import (
    AbstractCanAddressingInformation,
    CanAddressingFormat,
    CanPacketRecord,
    CanPacketType,
    InconsistentArgumentsError,
    PythonCanMessage,
)
from uds.transmission_attributes import AddressingType, TransmissionDirection

SCRIPT_LOCATION = "uds.packet.can_packet_record"


class TestCanPacketRecord:
    """Unit tests for `CanPacketRecord` class."""

    def setup_method(self):
        self.mock_can_packet_record = Mock(spec=CanPacketRecord)
        # patching
        self._patcher_addressing_type_class = patch(f"{SCRIPT_LOCATION}.AddressingType")
        self.mock_addressing_type_class = self._patcher_addressing_type_class.start()
        self._patcher_can_addressing_format_class = patch(f"{SCRIPT_LOCATION}.CanAddressingFormat")
        self.mock_can_addressing_format_class = self._patcher_can_addressing_format_class.start()
        self._patcher_can_ai_class = patch(f"{SCRIPT_LOCATION}.CanAddressingInformation")
        self.mock_can_ai_class = self._patcher_can_ai_class.start()
        self._patcher_can_packet_type_class = patch(f"{SCRIPT_LOCATION}.CanPacketType")
        self.mock_can_packet_type_class = self._patcher_can_packet_type_class.start()
        self._patcher_can_id_handler_class = patch(f"{SCRIPT_LOCATION}.CanIdHandler")
        self.mock_can_id_handler_class = self._patcher_can_id_handler_class.start()
        self._patcher_can_dlc_handler_class = patch(f"{SCRIPT_LOCATION}.CanDlcHandler")
        self.mock_can_dlc_handler_class = self._patcher_can_dlc_handler_class.start()
        self._patcher_abstract_uds_packet_record_init = patch(f"{SCRIPT_LOCATION}.AbstractUdsPacketRecord.__init__")
        self.mock_abstract_uds_packet_record_init = self._patcher_abstract_uds_packet_record_init.start()

    def teardown_method(self):
        self._patcher_addressing_type_class.stop()
        self._patcher_can_addressing_format_class.stop()
        self._patcher_can_ai_class.stop()
        self._patcher_can_packet_type_class.stop()
        self._patcher_can_id_handler_class.stop()
        self._patcher_can_dlc_handler_class.stop()
        self._patcher_abstract_uds_packet_record_init.stop()

    # __init__

    @pytest.mark.parametrize("frame, direction", [
        ("some frame", "some direction"),
        (Mock(spec=PythonCanMessage), "TX"),
    ])
    @pytest.mark.parametrize("addressing_type, addressing_format, transmission_time", [
        ("some addressing type", "some format", "some timestamp"),
        ("Another type", "another format", 9.543),
    ])
    def test_init(self, frame, direction, addressing_type, addressing_format, transmission_time):
        CanPacketRecord.__init__(self=self.mock_can_packet_record,
                                 frame=frame,
                                 direction=direction,
                                 addressing_type=addressing_type,
                                 addressing_format=addressing_format,
                                 transmission_time=transmission_time)
        assert self.mock_can_packet_record._CanPacketRecord__addressing_type \
               == self.mock_addressing_type_class.validate_member.return_value
        assert self.mock_can_packet_record._CanPacketRecord__addressing_format \
               == self.mock_can_addressing_format_class.validate_member.return_value
        self.mock_abstract_uds_packet_record_init.assert_called_once_with(frame=frame,
                                                                          direction=direction,
                                                                          transmission_time=transmission_time)
        self.mock_can_packet_record._CanPacketRecord__assess_packet_type.assert_called_once_with()
        self.mock_can_packet_record._CanPacketRecord__assess_ai_attributes.assert_called_once_with()
        self.mock_addressing_type_class.validate_member.assert_called_once_with(addressing_type)
        self.mock_can_addressing_format_class.validate_member.assert_called_once_with(addressing_format)

    # raw_frame_data

    @pytest.mark.parametrize("raw_frame_data", ["some raw data", range(10)])
    def test_raw_frame_data__python_can(self, raw_frame_data):
        self.mock_can_packet_record.frame = Mock(spec=PythonCanMessage, data=raw_frame_data)
        assert CanPacketRecord.raw_frame_data.fget(self.mock_can_packet_record) \
               == tuple(self.mock_can_packet_record.frame.data)

    def test_raw_frame_data__not_implemented(self):
        with pytest.raises(NotImplementedError):
            CanPacketRecord.raw_frame_data.fget(self.mock_can_packet_record)

    # can_id

    def test_can_id__python_can(self):
        self.mock_can_packet_record.frame = Mock(spec=PythonCanMessage)
        assert CanPacketRecord.can_id.fget(self.mock_can_packet_record) \
               == self.mock_can_packet_record.frame.arbitration_id

    def test_can_id__not_implemented(self):
        with pytest.raises(NotImplementedError):
            CanPacketRecord.can_id.fget(self.mock_can_packet_record)

    # addressing_format

    @pytest.mark.parametrize("value", [None, "something", 1])
    def test_addressing_format(self, value):
        self.mock_can_packet_record._CanPacketRecord__addressing_format = value
        assert CanPacketRecord.addressing_format.fget(self.mock_can_packet_record) == value

    # addressing_type

    @pytest.mark.parametrize("value", [None, "something", 1])
    def test_addressing_type(self, value):
        self.mock_can_packet_record._CanPacketRecord__addressing_type = value
        assert CanPacketRecord.addressing_type.fget(self.mock_can_packet_record) == value

    # packet_type

    @pytest.mark.parametrize("value", [None, "something", 1])
    def test_packet_type(self, value):
        self.mock_can_packet_record._CanPacketRecord__packet_type = value
        assert CanPacketRecord.packet_type.fget(self.mock_can_packet_record) == value

    # target_address

    @pytest.mark.parametrize("value", [None, "something", 1])
    def test_target_address(self, value):
        self.mock_can_packet_record._CanPacketRecord__target_address = value
        assert CanPacketRecord.target_address.fget(self.mock_can_packet_record) == value

    # source_address

    @pytest.mark.parametrize("value", [None, "something", 1])
    def test_source_address(self, value):
        self.mock_can_packet_record._CanPacketRecord__source_address = value
        assert CanPacketRecord.source_address.fget(self.mock_can_packet_record) == value

    # address_extension

    @pytest.mark.parametrize("value", [None, "something", 1])
    def test_address_extension(self, value):
        self.mock_can_packet_record._CanPacketRecord__address_extension = value
        assert CanPacketRecord.address_extension.fget(self.mock_can_packet_record) == value

    # _validate_frame

    @pytest.mark.parametrize("frame", [None, "not a frame"])
    def test_validate_frame__invalid_type(self, frame):
        with pytest.raises(TypeError):
            CanPacketRecord._validate_frame(frame)

    def test_validate_frame__valid_python_can(self, example_python_can_message):
        assert CanPacketRecord._validate_frame(example_python_can_message) is None
        self.mock_can_id_handler_class.validate_can_id.assert_called_once_with(
            example_python_can_message.arbitration_id)
        self.mock_can_dlc_handler_class.validate_data_bytes_number.assert_called_once_with(
            len(example_python_can_message.data))

    # __assess_packet_type

    @pytest.mark.parametrize("raw_frame_data", [range(10), [0xFE, 0xDC, 0xBA, 0x98]])
    @pytest.mark.parametrize("ai_data_bytes_number", [0, 1])
    def test_assess_packet_type(self, raw_frame_data, ai_data_bytes_number):
        self.mock_can_packet_record.raw_frame_data = raw_frame_data
        self.mock_can_ai_class.get_ai_data_bytes_number.return_value = ai_data_bytes_number
        assert CanPacketRecord._CanPacketRecord__assess_packet_type(self=self.mock_can_packet_record) is None
        assert self.mock_can_packet_record._CanPacketRecord__packet_type \
               == self.mock_can_packet_type_class.validate_member.return_value
        n_pci_value = raw_frame_data[ai_data_bytes_number] >> 4
        self.mock_can_ai_class.get_ai_data_bytes_number.assert_called_once_with(
            self.mock_can_packet_record.addressing_format)
        self.mock_can_packet_type_class.validate_member.assert_called_once_with(n_pci_value)

    # __assess_ai_attributes

    @pytest.mark.parametrize("addressing_format, can_id, raw_frame_data", [
        ("some fortmat", "some id", (0x00, 0x12, 0xB4)),
        ("some other fortmat", 0x98765, [0xFE, 0xDC, 0xBA, 0x98, 0x76]),
    ])
    @pytest.mark.parametrize("decoded_ai", [
        {AbstractCanAddressingInformation.TARGET_ADDRESS_NAME: "TA",
         AbstractCanAddressingInformation.SOURCE_ADDRESS_NAME: "SA",
         AbstractCanAddressingInformation.ADDRESS_EXTENSION_NAME: "AE",
         AbstractCanAddressingInformation.ADDRESSING_TYPE_NAME: "Some Addressing"},
        {AbstractCanAddressingInformation.TARGET_ADDRESS_NAME: 0x12,
         AbstractCanAddressingInformation.SOURCE_ADDRESS_NAME: 0x34,
         AbstractCanAddressingInformation.ADDRESS_EXTENSION_NAME: 0x56,
         AbstractCanAddressingInformation.ADDRESSING_TYPE_NAME: None},
    ])
    @pytest.mark.parametrize("ai_data_bytes_number", [0, 1])
    def test_assess_ai_attributes(self, addressing_format, can_id, raw_frame_data,
                                  ai_data_bytes_number, decoded_ai):
        self.mock_can_packet_record.addressing_format = addressing_format
        self.mock_can_packet_record.can_id = can_id
        self.mock_can_packet_record.raw_frame_data = raw_frame_data
        self.mock_can_packet_record.addressing_type = "Some Addressing"
        self.mock_can_ai_class.get_ai_data_bytes_number.return_value = ai_data_bytes_number
        self.mock_can_ai_class.decode_packet_ai.return_value = decoded_ai
        assert CanPacketRecord._CanPacketRecord__assess_ai_attributes(self=self.mock_can_packet_record) is None
        self.mock_can_ai_class.get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        self.mock_can_ai_class.decode_packet_ai.assert_called_once_with(addressing_format=addressing_format,
                                                                        can_id=can_id,
                                                                        ai_data_bytes=raw_frame_data[:ai_data_bytes_number])
        assert self.mock_can_packet_record._CanPacketRecord__target_address == decoded_ai["target_address"]
        assert self.mock_can_packet_record._CanPacketRecord__source_address == decoded_ai["source_address"]
        assert self.mock_can_packet_record._CanPacketRecord__address_extension == decoded_ai["address_extension"]

    @pytest.mark.parametrize("addressing_format, can_id, raw_frame_data", [
        ("some fortmat", "some id", range(10)),
        ("some other fortmat", 0x98765, [0xFE, 0xDC, 0xBA, 0x98, 0x76]),
    ])
    @pytest.mark.parametrize("decoded_ai", [
        {AbstractCanAddressingInformation.TARGET_ADDRESS_NAME: "TA",
         AbstractCanAddressingInformation.SOURCE_ADDRESS_NAME: "SA",
         AbstractCanAddressingInformation.ADDRESS_EXTENSION_NAME: "AE",
         AbstractCanAddressingInformation.ADDRESSING_TYPE_NAME: "Some Addressing"},
        {AbstractCanAddressingInformation.TARGET_ADDRESS_NAME: 0x12,
         AbstractCanAddressingInformation.SOURCE_ADDRESS_NAME: 0x34,
         AbstractCanAddressingInformation.ADDRESS_EXTENSION_NAME: 0x56,
         AbstractCanAddressingInformation.ADDRESSING_TYPE_NAME: "Some Other Addressing"},
    ])
    @pytest.mark.parametrize("ai_data_bytes_number", [0, 1])
    def test_assess_ai_attributes__inconsistent_addressing(self, addressing_format, can_id, raw_frame_data,
                                                           ai_data_bytes_number, decoded_ai):
        self.mock_can_packet_record.addressing_format = addressing_format
        self.mock_can_packet_record.can_id = can_id
        self.mock_can_packet_record.raw_frame_data = raw_frame_data
        self.mock_can_ai_class.get_ai_data_bytes_number.return_value = ai_data_bytes_number
        self.mock_can_ai_class.decode_packet_ai.return_value = decoded_ai
        with pytest.raises(InconsistentArgumentsError):
            CanPacketRecord._CanPacketRecord__assess_ai_attributes(self=self.mock_can_packet_record)
        self.mock_can_ai_class.get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        self.mock_can_ai_class.decode_packet_ai.assert_called_once_with(addressing_format=addressing_format,
                                                                        can_id=can_id,
                                                                        ai_data_bytes=raw_frame_data[:ai_data_bytes_number])


@pytest.mark.integration
class TestCanPacketRecordIntegration:
    """Integration tests for `CanPacketRecord` class."""

    @pytest.mark.parametrize("kwargs, expected_attribute_values", [
        ({"frame": PythonCanMessage(arbitration_id=0x69C,
                                    is_extended_id=False,
                                    dlc=2,
                                    data=[0x01, 0x3E]),
          "direction": TransmissionDirection.RECEIVED,
          "addressing_type": AddressingType.PHYSICAL,
          "addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
          "transmission_time": datetime.now()},
         {"raw_frame_data": (0x01, 0x3E),
          "addressing_type": AddressingType.PHYSICAL,
          "addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
          "packet_type": CanPacketType.SINGLE_FRAME,
          "payload": (0x3E, ),
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
        ({"frame": PythonCanMessage(arbitration_id=0x18CD9BE0,
                                    is_extended_id=True,
                                    data=[0x37, 0x30, 0x08, 0xF1] + ([0x99] * 60),
                                    is_fd=True,
                                    bitrate_switch=True),
          "direction": TransmissionDirection.TRANSMITTED,
          "addressing_type": AddressingType.FUNCTIONAL,
          "addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "transmission_time": datetime.now()},
         {"raw_frame_data": tuple([0x37, 0x30, 0x08, 0xF1] + ([0x99] * 60)),
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
    def test_init__valid(self, kwargs, expected_attribute_values):
        packet_record = CanPacketRecord(**kwargs)
        for attr_name, attr_value in expected_attribute_values.items():
            assert getattr(packet_record, attr_name) == attr_value
        assert packet_record.frame == kwargs["frame"]
        assert packet_record.transmission_time == kwargs["transmission_time"]

    @pytest.mark.parametrize("kwargs", [
        {"frame": PythonCanMessage(arbitration_id=0x68A,
                                   is_extended_id=False,
                                   dlc=8,
                                   data=[0xFF] * 8),
         "direction": TransmissionDirection.TRANSMITTED,
         "addressing_type": AddressingType.PHYSICAL,
         "addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
         "transmission_time": datetime.now()},
        {"frame": PythonCanMessage(arbitration_id=0x12345678,
                                   is_extended_id=True,
                                   dlc=3,
                                   data=[0xFE, 0x01, 0x3E]),
         "direction": TransmissionDirection.RECEIVED,
         "addressing_type": AddressingType.FUNCTIONAL,
         "addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         "transmission_time": datetime.now()},
    ])
    def test_init__invalid(self, kwargs):
        with pytest.raises(ValueError):
            CanPacketRecord(**kwargs)

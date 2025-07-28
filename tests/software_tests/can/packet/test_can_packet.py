import pytest
from mock import Mock, patch

from uds.can import DEFAULT_FILLER_BYTE, CanFlowStatus
from uds.can.packet.can_packet import AddressingType, CanAddressingFormat, CanPacket, CanPacketType, ReassignmentError

SCRIPT_LOCATION = "uds.can.packet.can_packet"


class TestCanPacket:
    """Unit tests for 'CanPacket' class."""

    def setup_method(self):
        self.mock_can_packet = Mock(spec=CanPacket)
        # patching
        self._patcher_can_addressing_format = patch(f"{SCRIPT_LOCATION}.CanAddressingFormat")
        self.mock_can_addressing_format = self._patcher_can_addressing_format.start()
        self._patcher_can_addressing_information = patch(f"{SCRIPT_LOCATION}.CanAddressingInformation")
        self.mock_can_addressing_information = self._patcher_can_addressing_information.start()
        self._patcher_validate_can_packet_type = patch(f"{SCRIPT_LOCATION}.CanPacketType.validate_member")
        self.mock_validate_can_packet_type = self._patcher_validate_can_packet_type.start()
        self._patcher_create_single_frame_data = patch(f"{SCRIPT_LOCATION}.create_single_frame_data")
        self.mock_create_single_frame_data = self._patcher_create_single_frame_data.start()
        self._patcher_create_first_frame_data = patch(f"{SCRIPT_LOCATION}.create_first_frame_data")
        self.mock_create_first_frame_data = self._patcher_create_first_frame_data.start()
        self._patcher_create_consecutive_frame_data = patch(f"{SCRIPT_LOCATION}.create_consecutive_frame_data")
        self.mock_create_consecutive_frame_data = self._patcher_create_consecutive_frame_data.start()
        self._patcher_create_flow_control_data = patch(f"{SCRIPT_LOCATION}.create_flow_control_data")
        self.mock_create_flow_control_data = self._patcher_create_flow_control_data.start()

    def teardown_method(self):
        self._patcher_can_addressing_format.stop()
        self._patcher_can_addressing_information.stop()
        self._patcher_validate_can_packet_type.stop()
        self._patcher_create_single_frame_data.stop()
        self._patcher_create_first_frame_data.stop()
        self._patcher_create_consecutive_frame_data.stop()
        self._patcher_create_flow_control_data.stop()

    # __init__

    @pytest.mark.parametrize("addressing_format, packet_type, addressing_type, can_id, target_address, source_address, "
                             "address_extension, dlc, packet_type_specific_kwargs", [
        (Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), {}),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, CanPacketType.FIRST_FRAME, AddressingType.PHYSICAL, 0x798, 0x54,
         0x7C, 0x90, 8, {"ff_dl": 123, "payload": [0x12, 0x34, 0x56, 0x78, 0x89]}),
    ])
    def test_init__all_args(self, addressing_format, packet_type, addressing_type, can_id, target_address,
                            source_address, address_extension, dlc, packet_type_specific_kwargs):
        assert CanPacket.__init__(self.mock_can_packet,
                                  addressing_format=addressing_format,
                                  packet_type=packet_type,
                                  addressing_type=addressing_type,
                                  can_id=can_id,
                                  target_address=target_address,
                                  source_address=source_address,
                                  address_extension=address_extension,
                                  dlc=dlc,
                                  **packet_type_specific_kwargs) is None
        assert self.mock_can_packet._CanPacket__raw_frame_data == bytes()
        assert self.mock_can_packet.addressing_format == addressing_format
        self.mock_can_packet.set_addressing_information.assert_called_once_with(addressing_type=addressing_type,
                                                                                can_id=can_id,
                                                                                target_address=target_address,
                                                                                source_address=source_address,
                                                                                address_extension=address_extension)
        self.mock_can_packet.set_packet_data.assert_called_once_with(packet_type=packet_type,
                                                                     dlc=dlc,
                                                                     **packet_type_specific_kwargs)

    @pytest.mark.parametrize("addressing_format, packet_type, addressing_type, packet_type_specific_kwargs", [
        (Mock(), Mock(), Mock(), {}),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, CanPacketType.SINGLE_FRAME, AddressingType.PHYSICAL,
         {"sf_dl": 62, "payload": range(62)}),
    ])
    def test_init__mandatory_args(self, addressing_format, packet_type, addressing_type, packet_type_specific_kwargs):
        assert CanPacket.__init__(self.mock_can_packet,
                                  addressing_format=addressing_format,
                                  packet_type=packet_type,
                                  addressing_type=addressing_type,
                                  **packet_type_specific_kwargs) is None
        assert self.mock_can_packet._CanPacket__raw_frame_data == bytes()
        assert self.mock_can_packet.addressing_format == addressing_format
        self.mock_can_packet.set_addressing_information.assert_called_once_with(addressing_type=addressing_type,
                                                                                can_id=None,
                                                                                target_address=None,
                                                                                source_address=None,
                                                                                address_extension=None)
        self.mock_can_packet.set_packet_data.assert_called_once_with(packet_type=packet_type,
                                                                     dlc=None,
                                                                     **packet_type_specific_kwargs)

    # __str__

    @pytest.mark.parametrize("payload, raw_frame_data", [
        (None, b"\x00\xFF\xF1\xB9\x8A"),
        ([0xBE, 0xEF, 0xFF, 0x00], bytearray([0x50, 0x61, 0x72, 0x83, 0x94, 0xA5, 0xB6, 0xC7, 0xD8, 0xE9, 0xFA])),
    ])
    def test_str(self, payload, raw_frame_data):
        self.mock_can_packet.payload = payload
        self.mock_can_packet.raw_frame_data = raw_frame_data
        output_str = CanPacket.__str__(self=self.mock_can_packet)
        assert output_str.startswith("CanPacket(") and output_str.endswith(")")
        assert "payload=" in output_str
        assert "addressing_type=" in output_str
        assert "addressing_format=" in output_str
        assert "raw_frame_data=" in output_str
        assert "packet_type=" in output_str
        assert "can_id=" in output_str

    # can_id

    def test_can_id__get(self):
        self.mock_can_packet._CanPacket__can_id = Mock()
        assert (CanPacket.can_id.fget(self.mock_can_packet)
                == self.mock_can_packet._CanPacket__can_id)

    # raw_frame_data

    def test_raw_frame_data__get(self):
        self.mock_can_packet._CanPacket__raw_frame_data = Mock()
        assert (CanPacket.raw_frame_data.fget(self.mock_can_packet)
                == self.mock_can_packet._CanPacket__raw_frame_data)

    # addressing_format

    def test_addressing_format__get(self):
        self.mock_can_packet._CanPacket__addressing_format = Mock()
        assert (CanPacket.addressing_format.fget(self.mock_can_packet)
                == self.mock_can_packet._CanPacket__addressing_format)

    @pytest.mark.parametrize("value", [Mock(), CanAddressingFormat.NORMAL_ADDRESSING])
    def test_addressing_format__set(self, value):
        assert CanPacket.addressing_format.fset(self.mock_can_packet, value) is None
        assert (self.mock_can_packet._CanPacket__addressing_format
                == self.mock_can_addressing_format.validate_member.return_value)
        self.mock_can_addressing_format.validate_member.assert_called_once_with(value)

    def test_addressing_format__set__reassignment_error(self):
        self.mock_can_packet._CanPacket__addressing_format = Mock()
        with pytest.raises(ReassignmentError):
            CanPacket.addressing_format.fset(self.mock_can_packet, Mock())

    # addressing_type

    def test_addressing_type__get(self):
        self.mock_can_packet._CanPacket__addressing_type = Mock()
        assert (CanPacket.addressing_type.fget(self.mock_can_packet)
                == self.mock_can_packet._CanPacket__addressing_type)

    # set_addressing_information

    @pytest.mark.parametrize("addressing_type, ai_data_bytes, raw_frame_data", [
        (Mock(), bytearray([0x3B]), b"\xFE\xDC\xBA\x98\x76\x54\x32\x10"),
        (AddressingType.FUNCTIONAL, bytearray(), b""),
    ])
    def test_set_addressing_information__mandatory_args(self, addressing_type,
                                                        ai_data_bytes, raw_frame_data):
        self.mock_can_packet._CanPacket__raw_frame_data = raw_frame_data
        self.mock_can_addressing_information.encode_ai_data_bytes.return_value = ai_data_bytes
        assert CanPacket.set_addressing_information(self.mock_can_packet,
                                                    addressing_type=addressing_type) is None
        assert (self.mock_can_packet._CanPacket__can_id
                == self.mock_can_addressing_information.validate_addressing_params.return_value["can_id"])
        assert (self.mock_can_packet._CanPacket__addressing_type
                == self.mock_can_addressing_information.validate_addressing_params.return_value["addressing_type"])
        assert self.mock_can_packet._CanPacket__raw_frame_data[:len(ai_data_bytes)] == bytes(ai_data_bytes)
        assert (self.mock_can_packet._CanPacket__raw_frame_data[len(ai_data_bytes):]
                == raw_frame_data[len(ai_data_bytes):])
        self.mock_can_addressing_information.validate_addressing_params.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format,
            addressing_type=addressing_type,
            can_id=None,
            target_address=None,
            source_address=None,
            address_extension=None)
        self.mock_can_addressing_information.encode_ai_data_bytes.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format,
            target_address=self.mock_can_addressing_information.validate_addressing_params.return_value["target_address"],
            address_extension=self.mock_can_addressing_information.validate_addressing_params.return_value["address_extension"])

    @pytest.mark.parametrize("addressing_type, can_id, target_address, source_address, address_extension, "
                             "ai_data_bytes, raw_frame_data", [
        (Mock(), Mock(), Mock(), Mock(), Mock(), bytearray([0x12]), b"\xFE\xDC\xBA\x98\x76\x54\x32\x10"),
        (AddressingType.PHYSICAL, 0x123, 0x5C, 0x3A, 0xF0, bytearray([0xF0]), b""),
    ])
    def test_set_addressing_information__all_args(self, addressing_type, can_id, target_address, source_address,
                                                  address_extension,
                                                  ai_data_bytes, raw_frame_data):
        self.mock_can_packet._CanPacket__raw_frame_data = raw_frame_data
        self.mock_can_addressing_information.encode_ai_data_bytes.return_value = ai_data_bytes
        assert CanPacket.set_addressing_information(self.mock_can_packet,
                                                    addressing_type=addressing_type,
                                                    can_id=can_id,
                                                    target_address=target_address,
                                                    source_address=source_address,
                                                    address_extension=address_extension) is None
        assert (self.mock_can_packet._CanPacket__can_id
                == self.mock_can_addressing_information.validate_addressing_params.return_value["can_id"])
        assert (self.mock_can_packet._CanPacket__addressing_type
                == self.mock_can_addressing_information.validate_addressing_params.return_value["addressing_type"])
        assert self.mock_can_packet._CanPacket__raw_frame_data[:len(ai_data_bytes)] == bytes(ai_data_bytes)
        assert (self.mock_can_packet._CanPacket__raw_frame_data[len(ai_data_bytes):]
                == raw_frame_data[len(ai_data_bytes):])
        self.mock_can_addressing_information.validate_addressing_params.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format,
            addressing_type=addressing_type,
            can_id=can_id,
            target_address=target_address,
            source_address=source_address,
            address_extension=address_extension)
        self.mock_can_addressing_information.encode_ai_data_bytes.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format,
            target_address=self.mock_can_addressing_information.validate_addressing_params.return_value["target_address"],
            address_extension=self.mock_can_addressing_information.validate_addressing_params.return_value["address_extension"])

    # set_packet_data

    @pytest.mark.parametrize("packet_params", [
        {"dlc": Mock(), "filler_byte": Mock(), "payload": Mock()},
        {"payload": [0xFF]},
    ])
    def test_set_packet_data__single_frame(self, packet_params):
        assert CanPacket.set_packet_data(self.mock_can_packet,
                                         packet_type=CanPacketType.SINGLE_FRAME,
                                         **packet_params) is None
        if "dlc" not in packet_params:
            packet_params["dlc"] = None
        assert self.mock_can_packet._CanPacket__raw_frame_data == bytes(self.mock_create_single_frame_data)
        self.mock_create_single_frame_data.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format,
            target_address=self.mock_can_packet.target_address,
            address_extension=self.mock_can_packet.address_extension,
            **packet_params)
        self.mock_validate_can_packet_type.assert_called_once_with(CanPacketType.SINGLE_FRAME)

    @pytest.mark.parametrize("packet_params", [
        {"dlc": Mock(), "payload": Mock(), "data_length": Mock()},
        {"payload": [0xFF]},
    ])
    def test_set_packet_data__first_frame(self, packet_params):
        assert CanPacket.set_packet_data(self.mock_can_packet,
                                         packet_type=CanPacketType.FIRST_FRAME,
                                         **packet_params) is None
        if "dlc" not in packet_params:
            packet_params["dlc"] = None
        assert self.mock_can_packet._CanPacket__raw_frame_data == bytes(self.mock_create_first_frame_data)
        self.mock_create_first_frame_data.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format,
            target_address=self.mock_can_packet.target_address,
            address_extension=self.mock_can_packet.address_extension,
            **packet_params)
        self.mock_validate_can_packet_type.assert_called_once_with(CanPacketType.FIRST_FRAME)

    @pytest.mark.parametrize("packet_params", [
        {"dlc": Mock(), "payload": Mock(), "sequence_number": Mock(), "filler_byte": Mock()},
        {"payload": [0xFF], "sequence_number": 0x0},
    ])
    def test_set_packet_data__consecutive_frame(self, packet_params):
        assert CanPacket.set_packet_data(self.mock_can_packet,
                                         packet_type=CanPacketType.CONSECUTIVE_FRAME,
                                         **packet_params) is None
        if "dlc" not in packet_params:
            packet_params["dlc"] = None
        assert self.mock_can_packet._CanPacket__raw_frame_data == bytes(self.mock_create_consecutive_frame_data)
        self.mock_create_consecutive_frame_data.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format,
            target_address=self.mock_can_packet.target_address,
            address_extension=self.mock_can_packet.address_extension,
            **packet_params)
        self.mock_validate_can_packet_type.assert_called_once_with(CanPacketType.CONSECUTIVE_FRAME)

    @pytest.mark.parametrize("packet_params", [
        {"dlc": Mock(), "flow_status": Mock(), "block_size": Mock(), "st_min": Mock(), "filler_byte": Mock()},
        {"flow_status": 3},
    ])
    def test_set_packet_data__flow_control(self, packet_params):
        assert CanPacket.set_packet_data(self.mock_can_packet,
                                         packet_type=CanPacketType.FLOW_CONTROL,
                                         **packet_params) is None
        if "dlc" not in packet_params:
            packet_params["dlc"] = None
        assert self.mock_can_packet._CanPacket__raw_frame_data == bytes(self.mock_create_flow_control_data)
        self.mock_create_flow_control_data.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format,
            target_address=self.mock_can_packet.target_address,
            address_extension=self.mock_can_packet.address_extension,
            **packet_params)
        self.mock_validate_can_packet_type.assert_called_once_with(CanPacketType.FLOW_CONTROL)

    def test_set_packet_data__not_implemented(self):
        mock_packet_type = Mock()
        with pytest.raises(NotImplementedError):
            CanPacket.set_packet_data(self.mock_can_packet,
                                      packet_type=mock_packet_type)
        self.mock_validate_can_packet_type.assert_called_once_with(mock_packet_type)


@pytest.mark.integration
class TestCanPacketIntegration:
    """Integration tests for `CanPacket` class."""

    # __init__

    @pytest.mark.parametrize("init_kwargs, expected_attribute_values", [
        # SF
        ({"packet_type": CanPacketType.SINGLE_FRAME,
          "addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "addressing_type": AddressingType.PHYSICAL,
          "target_address": 0xE9,
          "source_address": 0xB7,
          "address_extension": 0xDB,
          "dlc": 8,
          "payload": b"\x3E"},
         {"raw_frame_data": bytes([0xDB, 0x01, 0x3E, DEFAULT_FILLER_BYTE, DEFAULT_FILLER_BYTE, DEFAULT_FILLER_BYTE,
                                   DEFAULT_FILLER_BYTE, DEFAULT_FILLER_BYTE]),
          "addressing_type": AddressingType.PHYSICAL,
          "addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "packet_type": CanPacketType.SINGLE_FRAME,
          "can_id": 0x18CEE9B7,
          "dlc": 8,
          "target_address": 0xE9,
          "source_address": 0xB7,
          "address_extension": 0xDB,
          "payload": b"\x3E",
          "data_length": 1,
          "sequence_number": None,
          "flow_status": None,
          "block_size": None,
          "st_min": None}),
        # FF
        ({"packet_type": CanPacketType.FIRST_FRAME,
          "addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "addressing_type": AddressingType.FUNCTIONAL,
          "can_id": 0x18DB023B,
          "target_address": 0x02,
          "source_address": 0x3B,
          "dlc": 0xF,
          "payload": bytes(range(50, 108)),
          "data_length": 0xFEDCBA98},
         {"raw_frame_data": bytes([0x10, 0x00, 0xFE, 0xDC, 0xBA, 0x98, *range(50, 108)]),
          "addressing_type": AddressingType.FUNCTIONAL,
          "addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "packet_type": CanPacketType.FIRST_FRAME,
          "can_id": 0x18DB023B,
          "dlc": 0xF,
          "target_address": 0x02,
          "source_address": 0x3B,
          "address_extension": None,
          "payload": bytes(range(50, 108)),
          "data_length": 0xFEDCBA98,
          "sequence_number": None,
          "flow_status": None,
          "block_size": None,
          "st_min": None}),
        # CF
        ({"packet_type": CanPacketType.CONSECUTIVE_FRAME,
          "addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "addressing_type": AddressingType.FUNCTIONAL,
          "can_id": 0x743,
          "target_address": 0xB1,
          "payload": b"\x91\x82",
          "sequence_number": 0x1},
         {"raw_frame_data": b"\xB1\x21\x91\x82",
          "addressing_type": AddressingType.FUNCTIONAL,
          "addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "packet_type": CanPacketType.CONSECUTIVE_FRAME,
          "can_id": 0x743,
          "dlc": 4,
          "target_address": 0xB1,
          "source_address": None,
          "address_extension": None,
          "payload": b"\x91\x82",
          "data_length": None,
          "sequence_number": 0x1,
          "flow_status": None,
          "block_size": None,
          "st_min": None}),
        # FC
        ({"packet_type": CanPacketType.FLOW_CONTROL,
          "addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
          "addressing_type": AddressingType.PHYSICAL,
          "can_id": 0x12688,
          "flow_status": CanFlowStatus.ContinueToSend,
          "block_size": 0xF9,
          "st_min": 0xE0},
         {"raw_frame_data": b"\x30\xF9\xE0",
          "addressing_type": AddressingType.PHYSICAL,
          "addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
          "packet_type": CanPacketType.FLOW_CONTROL,
          "can_id": 0x12688,
          "dlc": 3,
          "target_address": None,
          "source_address": None,
          "address_extension": None,
          "payload": None,
          "data_length": None,
          "sequence_number": None,
          "flow_status": CanFlowStatus.ContinueToSend,
          "block_size": 0xF9,
          "st_min": 0xE0}),
    ])
    def test_init(self, init_kwargs, expected_attribute_values):
        packet = CanPacket(**init_kwargs)
        for attr_name, attr_value in expected_attribute_values.items():
            assert getattr(packet, attr_name) == attr_value

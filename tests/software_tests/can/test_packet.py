import pytest
from mock import patch, Mock, call

from uds.can.packet import CanPacket, \
    CanPacketType, CanAddressingFormat, AddressingType, CanFlowStatus, DEFAULT_FILLER_BYTE, AmbiguityError


class TestCanPacket:
    """Tests for 'CanPacket' class."""

    SCRIPT_LOCATION = "uds.can.packet"

    def setup(self):
        self.mock_can_packet = Mock(spec=CanPacket)
        # patching
        self._patcher_warn = patch(f"{self.SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()
        self._patcher_can_id_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanIdHandler")
        self.mock_can_id_handler_class = self._patcher_can_id_handler_class.start()
        self._patcher_ai_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanAddressingInformationHandler")
        self.mock_ai_handler_class = self._patcher_ai_handler_class.start()
        self._patcher_single_frame_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanSingleFrameHandler")
        self.mock_single_frame_handler_class = self._patcher_single_frame_handler_class.start()
        self._patcher_first_frame_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanFirstFrameHandler")
        self.mock_first_frame_handler_class = self._patcher_first_frame_handler_class.start()
        self._patcher_consecutive_frame_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanConsecutiveFrameHandler")
        self.mock_consecutive_frame_handler_class = self._patcher_consecutive_frame_handler_class.start()
        self._patcher_flow_control_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanFlowControlHandler")
        self.mock_flow_control_handler_class = self._patcher_flow_control_handler_class.start()
        self._patcher_validate_addressing_format = patch(f"{self.SCRIPT_LOCATION}.CanAddressingFormat.validate_member")
        self.mock_validate_addressing_format = self._patcher_validate_addressing_format.start()

    def teardown(self):
        self._patcher_warn.stop()
        self._patcher_can_id_handler_class.stop()
        self._patcher_ai_handler_class.stop()
        self._patcher_single_frame_handler_class.stop()
        self._patcher_first_frame_handler_class.stop()
        self._patcher_consecutive_frame_handler_class.stop()
        self._patcher_flow_control_handler_class.stop()
        self._patcher_validate_addressing_format.stop()

    # __init__

    @pytest.mark.parametrize("packet_type, packet_type_specific_kwargs", [
        ("some packet type", {"v1": "some value", "v2": "Some other vlaue"}),
        (1, {"p1": "something", "p2": "something else"}),
    ])
    @pytest.mark.parametrize("addressing_type, addressing_format, dlc", [
        ("some addressing type", "some addressing format", "some dlc"),
        (AddressingType.FUNCTIONAL, CanAddressingFormat.NORMAL_11BIT_ADDRESSING, 8),
    ])
    @pytest.mark.parametrize("can_id, target_address, source_address, address_extension", [
        (None, 1, 2, 3),
        (0x675, None, None, None),
    ])
    def test_init(self, addressing_type, addressing_format, packet_type, can_id, dlc,
                  target_address, source_address, address_extension, packet_type_specific_kwargs):
        CanPacket.__init__(self=self.mock_can_packet,
                           packet_type=packet_type,
                           addressing_type=addressing_type,
                           addressing_format=addressing_format,
                           can_id=can_id,
                           target_address=target_address,
                           source_address=source_address,
                           address_extension=address_extension,
                           dlc=dlc,
                           **packet_type_specific_kwargs)
        assert self.mock_can_packet._CanPacket__addressing_format is None
        self.mock_can_packet.set_address_information.assert_called_once_with(addressing_type=addressing_type,
                                                                             addressing_format=addressing_format,
                                                                             can_id=can_id,
                                                                             target_address=target_address,
                                                                             source_address=source_address,
                                                                             address_extension=address_extension)
        self.mock_can_packet.set_packet_data.assert_called_once_with(packet_type=packet_type,
                                                                     dlc=dlc,
                                                                     **packet_type_specific_kwargs)

    # set_address_information

    @pytest.mark.parametrize("addressing_format", [None, "unknown addressing format"])
    @pytest.mark.parametrize("addressing_type, can_id, target_address, source_address, address_extension", [
        ("something", "CAN ID", "TA", "SA", "AE"),
        (AddressingType.PHYSICAL, 0x754, 0x31, 0xD0, 0xE3),
    ])
    def test_set_address_information__unknown_addressing_format(self, addressing_format, addressing_type, can_id,
                                                                target_address, source_address, address_extension):
        with pytest.raises(NotImplementedError):
            CanPacket.set_address_information(self=self.mock_can_packet,
                                              addressing_type=addressing_type,
                                              addressing_format=addressing_format,
                                              can_id=can_id,
                                              target_address=target_address,
                                              source_address=source_address,
                                              address_extension=address_extension)
        self.mock_validate_addressing_format.assert_called_once_with(addressing_format)

    @pytest.mark.parametrize("addressing_type, can_id", [
        ("something", "CAN ID"),
        (AddressingType.PHYSICAL, 0x754),
    ])
    def test_set_address_information__normal_11_bit(self, addressing_type, can_id):
        CanPacket.set_address_information(self=self.mock_can_packet,
                                          addressing_type=addressing_type,
                                          addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                          can_id=can_id)
        self.mock_can_packet.set_address_information_normal_11bit.assert_called_once_with(
            addressing_type=addressing_type, can_id=can_id)
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("addressing_type, can_id, target_address, source_address, address_extension", [
        ("something", "CAN ID", "TA", "SA", "AE"),
        (AddressingType.PHYSICAL, 0x754, 0x31, 0xD0, 0xE3),
    ])
    def test_set_address_information__normal_11_bit_with_warn(self, addressing_type, can_id,
                                                              target_address, source_address, address_extension):
        CanPacket.set_address_information(self=self.mock_can_packet,
                                          addressing_type=addressing_type,
                                          addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                          can_id=can_id,
                                          target_address=target_address,
                                          source_address=source_address,
                                          address_extension=address_extension)
        self.mock_can_packet.set_address_information_normal_11bit.assert_called_once_with(
            addressing_type=addressing_type, can_id=can_id)
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("addressing_type, can_id, target_address, source_address", [
        ("something", "CAN ID", "TA", "SA"),
        (AddressingType.PHYSICAL, 0x754, 0x31, 0xD0),
    ])
    def test_set_address_information__normal_fixed(self, addressing_type, can_id, target_address, source_address):
        CanPacket.set_address_information(self=self.mock_can_packet,
                                          addressing_type=addressing_type,
                                          addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                          can_id=can_id,
                                          target_address=target_address,
                                          source_address=source_address)
        self.mock_can_packet.set_address_information_normal_fixed.assert_called_once_with(addressing_type=addressing_type,
                                                                                          can_id=can_id,
                                                                                          target_address=target_address,
                                                                                          source_address=source_address)
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("addressing_type, can_id, target_address, source_address, address_extension", [
        ("something", "CAN ID", "TA", "SA", "AE"),
        (AddressingType.PHYSICAL, 0x754, 0x31, 0xD0, 0xE3),
    ])
    def test_set_address_information__normal_fixed_warn(self, addressing_type, can_id,
                                                        target_address, source_address, address_extension):
        CanPacket.set_address_information(self=self.mock_can_packet,
                                          addressing_type=addressing_type,
                                          addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                          can_id=can_id,
                                          target_address=target_address,
                                          source_address=source_address,
                                          address_extension=address_extension)
        self.mock_can_packet.set_address_information_normal_fixed.assert_called_once_with(addressing_type=addressing_type,
                                                                                          can_id=can_id,
                                                                                          target_address=target_address,
                                                                                          source_address=source_address)
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("addressing_type, can_id, target_address", [
        ("something", "CAN ID", "TA"),
        (AddressingType.PHYSICAL, 0x754, 0x31),
    ])
    def test_set_address_information__extended(self, addressing_type, can_id, target_address):
        CanPacket.set_address_information(self=self.mock_can_packet,
                                          addressing_type=addressing_type,
                                          addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                          can_id=can_id,
                                          target_address=target_address)
        self.mock_can_packet.set_address_information_extended.assert_called_once_with(addressing_type=addressing_type,
                                                                                      can_id=can_id,
                                                                                      target_address=target_address)
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("addressing_type, can_id, target_address, source_address, address_extension", [
        ("something", "CAN ID", "TA", "SA", "AE"),
        (AddressingType.PHYSICAL, 0x754, 0x31, 0xD0, 0xE3),
    ])
    def test_set_address_information__extended_warn(self, addressing_type, can_id,
                                                    target_address, source_address, address_extension):
        CanPacket.set_address_information(self=self.mock_can_packet,
                                          addressing_type=addressing_type,
                                          addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                          can_id=can_id,
                                          target_address=target_address,
                                          source_address=source_address,
                                          address_extension=address_extension)
        self.mock_can_packet.set_address_information_extended.assert_called_once_with(addressing_type=addressing_type,
                                                                                      can_id=can_id,
                                                                                      target_address=target_address)
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("addressing_type, can_id, address_extension", [
        ("something", "CAN ID", "AE"),
        (AddressingType.PHYSICAL, 0x754, 0xE3),
    ])
    def test_set_address_information__mixed_11bit(self, addressing_type, can_id, address_extension):
        CanPacket.set_address_information(self=self.mock_can_packet,
                                          addressing_type=addressing_type,
                                          addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                          can_id=can_id,
                                          address_extension=address_extension)
        self.mock_can_packet.set_address_information_mixed_11bit.assert_called_once_with(addressing_type=addressing_type,
                                                                                         can_id=can_id,
                                                                                         address_extension=address_extension)
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("addressing_type, can_id, target_address, source_address, address_extension", [
        ("something", "CAN ID", "TA", "SA", "AE"),
        (AddressingType.PHYSICAL, 0x754, 0x31, 0xD0, 0xE3),
    ])
    def test_set_address_information__mixed_11bit_warn(self, addressing_type, can_id,
                                                       target_address, source_address, address_extension):
        CanPacket.set_address_information(self=self.mock_can_packet,
                                          addressing_type=addressing_type,
                                          addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                          can_id=can_id,
                                          target_address=target_address,
                                          source_address=source_address,
                                          address_extension=address_extension)
        self.mock_can_packet.set_address_information_mixed_11bit.assert_called_once_with(addressing_type=addressing_type,
                                                                                         can_id=can_id,
                                                                                         address_extension=address_extension)
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("addressing_type, can_id, target_address, source_address, address_extension", [
        ("something", "CAN ID", "TA", "SA", "AE"),
        (AddressingType.PHYSICAL, 0x754, 0x31, 0xD0, 0xE3),
    ])
    def test_set_address_information__mixed_29bit(self, addressing_type, can_id,
                                                  target_address, source_address, address_extension):
        CanPacket.set_address_information(self=self.mock_can_packet,
                                          addressing_type=addressing_type,
                                          addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                          can_id=can_id,
                                          target_address=target_address,
                                          source_address=source_address,
                                          address_extension=address_extension)
        self.mock_can_packet.set_address_information_mixed_29bit.assert_called_once_with(addressing_type=addressing_type,
                                                                                         can_id=can_id,
                                                                                         target_address=target_address,
                                                                                         source_address=source_address,
                                                                                         address_extension=address_extension)
        self.mock_warn.assert_not_called()

    # set_address_information_normal_11bit

    @pytest.mark.parametrize("can_id", ["some CAN ID", 0x64A])
    def test_set_address_information_normal_11bit(self, example_addressing_type, can_id):
        CanPacket.set_address_information_normal_11bit(self=self.mock_can_packet,
                                                       addressing_type=example_addressing_type,
                                                       can_id=can_id)
        self.mock_ai_handler_class.validate_ai_normal_11bit.assert_called_once_with(
            addressing_type=example_addressing_type, can_id=can_id)
        self.mock_can_packet._CanPacket__validate_unambiguous_ai_change.assert_called_once_with(
            CanAddressingFormat.NORMAL_11BIT_ADDRESSING)
        assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.NORMAL_11BIT_ADDRESSING
        assert self.mock_can_packet._CanPacket__addressing_type == example_addressing_type
        assert self.mock_can_packet._CanPacket__can_id == can_id
        assert self.mock_can_packet._CanPacket__target_address is None
        assert self.mock_can_packet._CanPacket__source_address is None
        assert self.mock_can_packet._CanPacket__address_extension is None

    # set_address_information_normal_fixed

    @pytest.mark.parametrize("can_id", ["some CAN ID", 0x64A])
    @pytest.mark.parametrize("decoded_target_address, decoded_source_address", [
        ("TA", "SA"),
        (0x15, 0x6B),
    ])
    def test_set_address_information_normal_fixed__can_id(self, example_addressing_type, can_id,
                                                          decoded_target_address, decoded_source_address):
        self.mock_can_id_handler_class.decode_normal_fixed_addressed_can_id.return_value = {
            "addressing_type": example_addressing_type,
            "target_address": decoded_target_address,
            "source_address": decoded_source_address,
        }
        CanPacket.set_address_information_normal_fixed(self=self.mock_can_packet,
                                                       addressing_type=example_addressing_type,
                                                       can_id=can_id)
        self.mock_ai_handler_class.validate_ai_normal_fixed.assert_called_once_with(
            addressing_type=example_addressing_type,
            can_id=can_id,
            target_address=None,
            source_address=None)
        self.mock_can_packet._CanPacket__validate_unambiguous_ai_change.assert_called_once_with(
            CanAddressingFormat.NORMAL_FIXED_ADDRESSING)
        self.mock_ai_handler_class.decode_normal_fixed_addressed_can_id.assert_called_once_with(can_id)
        self.mock_ai_handler_class.encode_normal_fixed_addressed_can_id.assert_not_called()
        assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.NORMAL_FIXED_ADDRESSING
        assert self.mock_can_packet._CanPacket__addressing_type == example_addressing_type
        assert self.mock_can_packet._CanPacket__can_id == can_id
        assert self.mock_can_packet._CanPacket__target_address == decoded_target_address
        assert self.mock_can_packet._CanPacket__source_address == decoded_source_address
        assert self.mock_can_packet._CanPacket__address_extension is None

    @pytest.mark.parametrize("target_address, source_address", [
        ("TA", "SA"),
        (0x00, 0xFF),
    ])
    def test_set_address_information_normal_fixed__ta_sa(self, example_addressing_type, target_address, source_address):
        CanPacket.set_address_information_normal_fixed(self=self.mock_can_packet,
                                                       addressing_type=example_addressing_type,
                                                       target_address=target_address,
                                                       source_address=source_address)
        self.mock_ai_handler_class.validate_ai_normal_fixed.assert_called_once_with(
            addressing_type=example_addressing_type,
            can_id=None,
            target_address=target_address,
            source_address=source_address)
        self.mock_can_packet._CanPacket__validate_unambiguous_ai_change.assert_called_once_with(
            CanAddressingFormat.NORMAL_FIXED_ADDRESSING)
        self.mock_ai_handler_class.decode_normal_fixed_addressed_can_id.assert_not_called()
        self.mock_ai_handler_class.encode_normal_fixed_addressed_can_id.assert_called_once_with(
            addressing_type=example_addressing_type, target_address=target_address, source_address=source_address)
        assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.NORMAL_FIXED_ADDRESSING
        assert self.mock_can_packet._CanPacket__addressing_type == example_addressing_type
        assert self.mock_can_packet._CanPacket__can_id == self.mock_ai_handler_class.encode_normal_fixed_addressed_can_id.return_value
        assert self.mock_can_packet._CanPacket__target_address == target_address
        assert self.mock_can_packet._CanPacket__source_address == source_address
        assert self.mock_can_packet._CanPacket__address_extension is None

    # raw_frame_data

    @pytest.mark.parametrize("value", [None, "some", False, 5.5])
    def test_raw_frame_data__get(self, value):
        self.mock_can_packet._CanPacket__raw_frame_data = value
        assert CanPacket.raw_frame_data.fget(self=self.mock_can_packet) == value

    # addressing

    @pytest.mark.parametrize("value", [None, "some", False, 5.5])
    def test_addressing_type__get(self, value):
        self.mock_can_packet._CanPacket__addressing_type = value
        assert CanPacket.addressing_type.fget(self=self.mock_can_packet) == value

    # addressing_format

    @pytest.mark.parametrize("value", [None, "some", False, 5.5])
    def test_addressing_format__get(self, value):
        self.mock_can_packet._CanPacket__addressing_format = value
        assert CanPacket.addressing_format.fget(self=self.mock_can_packet) == value

    # packet_type

    @pytest.mark.parametrize("value", [None, "some", False, 5.5])
    def test_packet_type__get(self, value):
        self.mock_can_packet._CanPacket__packet_type = value
        assert CanPacket.packet_type.fget(self=self.mock_can_packet) == value

    # can_id

    @pytest.mark.parametrize("value", [None, "some", False, 5.5])
    def test_can_id__get(self, value):
        self.mock_can_packet._CanPacket__can_id = value
        assert CanPacket.can_id.fget(self=self.mock_can_packet) == value

    # dlc

    @pytest.mark.parametrize("value", [None, "some", False, 5.5])
    def test_dlc__get(self, value):
        self.mock_can_packet._CanPacket__dlc = value
        assert CanPacket.dlc.fget(self=self.mock_can_packet) == value

    # target_address

    @pytest.mark.parametrize("value", [None, "some", False, 5.5])
    def test_target_address__get(self, value):
        self.mock_can_packet._CanPacket__target_address = value
        assert CanPacket.target_address.fget(self=self.mock_can_packet) == value

    # source_address

    @pytest.mark.parametrize("value", [None, "some", False, 5.5])
    def test_source_address__get(self, value):
        self.mock_can_packet._CanPacket__source_address = value
        assert CanPacket.source_address.fget(self=self.mock_can_packet) == value

    # address_extension

    @pytest.mark.parametrize("value", [None, "some", False, 5.5])
    def test_address_extension__get(self, value):
        self.mock_can_packet._CanPacket__address_extension = value
        assert CanPacket.address_extension.fget(self=self.mock_can_packet) == value

    # payload

    @pytest.mark.parametrize("packet_type", [None, CanPacketType.FLOW_CONTROL, "something new"])
    def test_payload__none(self, packet_type):
        self.mock_can_packet.packet_type = packet_type
        assert CanPacket.payload.fget(self=self.mock_can_packet) is None

    @pytest.mark.parametrize("payload", [range(10), [0xFE, 0xDC]])
    def test_payload__single_frame(self, payload):
        self.mock_can_packet.packet_type = CanPacketType.SINGLE_FRAME
        self.mock_single_frame_handler_class.decode_payload.return_value = payload
        assert CanPacket.payload.fget(self=self.mock_can_packet) == tuple(payload)
        self.mock_single_frame_handler_class.decode_payload.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format, raw_frame_data=self.mock_can_packet.raw_frame_data)

    @pytest.mark.parametrize("payload", [range(10), [0xFE, 0xDC]])
    def test_payload__first_frame(self, payload):
        self.mock_can_packet.packet_type = CanPacketType.FIRST_FRAME
        self.mock_first_frame_handler_class.decode_payload.return_value = payload
        assert CanPacket.payload.fget(self=self.mock_can_packet) == tuple(payload)
        self.mock_first_frame_handler_class.decode_payload.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format, raw_frame_data=self.mock_can_packet.raw_frame_data)

    @pytest.mark.parametrize("payload", [range(10), [0xFE, 0xDC]])
    def test_payload__consecutive_frame(self, payload):
        self.mock_can_packet.packet_type = CanPacketType.CONSECUTIVE_FRAME
        self.mock_consecutive_frame_handler_class.decode_payload.return_value = payload
        assert CanPacket.payload.fget(self=self.mock_can_packet) == tuple(payload)
        self.mock_consecutive_frame_handler_class.decode_payload.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format, raw_frame_data=self.mock_can_packet.raw_frame_data)

    # data_length

    @pytest.mark.parametrize("packet_type", [None, CanPacketType.CONSECUTIVE_FRAME, CanPacketType.FLOW_CONTROL, "x"])
    def test_data_length__none(self, packet_type):
        self.mock_can_packet.packet_type = packet_type
        assert CanPacket.data_length.fget(self=self.mock_can_packet) is None

    def test_data_length__single_frame(self):
        self.mock_can_packet.packet_type = CanPacketType.SINGLE_FRAME
        assert CanPacket.data_length.fget(self=self.mock_can_packet) \
               == self.mock_single_frame_handler_class.decode_sf_dl.return_value
        self.mock_single_frame_handler_class.decode_sf_dl.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format,
            raw_frame_data=self.mock_can_packet.raw_frame_data)

    def test_data_length__first_frame(self):
        self.mock_can_packet.packet_type = CanPacketType.FIRST_FRAME
        assert CanPacket.data_length.fget(self=self.mock_can_packet) \
               == self.mock_first_frame_handler_class.decode_ff_dl.return_value
        self.mock_first_frame_handler_class.decode_ff_dl.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format,
            raw_frame_data=self.mock_can_packet.raw_frame_data)

    # sequence_number

    @pytest.mark.parametrize("packet_type", [None, CanPacketType.SINGLE_FRAME, CanPacketType.FIRST_FRAME,
                                             CanPacketType.FLOW_CONTROL, "x"])
    def test_sequence_number__none(self, packet_type):
        self.mock_can_packet.packet_type = packet_type
        assert CanPacket.sequence_number.fget(self=self.mock_can_packet) is None

    def test_sequence_number__consecutive_frame(self):
        self.mock_can_packet.packet_type = CanPacketType.CONSECUTIVE_FRAME
        assert CanPacket.sequence_number.fget(self=self.mock_can_packet) \
               == self.mock_consecutive_frame_handler_class.decode_sequence_number.return_value
        self.mock_consecutive_frame_handler_class.decode_sequence_number.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format,
            raw_frame_data=self.mock_can_packet.raw_frame_data)

    # flow_status

    @pytest.mark.parametrize("packet_type", [None, CanPacketType.SINGLE_FRAME, CanPacketType.FIRST_FRAME,
                                             CanPacketType.CONSECUTIVE_FRAME, "x"])
    def test_flow_status__none(self, packet_type):
        self.mock_can_packet.packet_type = packet_type
        assert CanPacket.flow_status.fget(self=self.mock_can_packet) is None

    def test_flow_status__flow_control(self):
        self.mock_can_packet.packet_type = CanPacketType.FLOW_CONTROL
        assert CanPacket.flow_status.fget(self=self.mock_can_packet) \
               == self.mock_flow_control_handler_class.decode_flow_status.return_value
        self.mock_flow_control_handler_class.decode_flow_status.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format,
            raw_frame_data=self.mock_can_packet.raw_frame_data)

    # block_size

    @pytest.mark.parametrize("packet_type", [None, CanPacketType.SINGLE_FRAME, CanPacketType.FIRST_FRAME,
                                             CanPacketType.CONSECUTIVE_FRAME, "x"])
    def test_block_size__none(self, packet_type):
        self.mock_can_packet.packet_type = packet_type
        assert CanPacket.block_size.fget(self=self.mock_can_packet) is None

    def test_block_size__flow_control(self):
        self.mock_can_packet.packet_type = CanPacketType.FLOW_CONTROL
        assert CanPacket.block_size.fget(self=self.mock_can_packet) \
               == self.mock_flow_control_handler_class.decode_block_size.return_value
        self.mock_flow_control_handler_class.decode_block_size.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format,
            raw_frame_data=self.mock_can_packet.raw_frame_data)

    # block_size

    @pytest.mark.parametrize("packet_type", [None, CanPacketType.SINGLE_FRAME, CanPacketType.FIRST_FRAME,
                                             CanPacketType.CONSECUTIVE_FRAME, "x"])
    def test_block_size__none(self, packet_type):
        self.mock_can_packet.packet_type = packet_type
        assert CanPacket.block_size.fget(self=self.mock_can_packet) is None

    def test_block_size__flow_control(self):
        self.mock_can_packet.packet_type = CanPacketType.FLOW_CONTROL
        assert CanPacket.block_size.fget(self=self.mock_can_packet) \
               == self.mock_flow_control_handler_class.decode_block_size.return_value
        self.mock_flow_control_handler_class.decode_block_size.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format,
            raw_frame_data=self.mock_can_packet.raw_frame_data)

    # st_min

    @pytest.mark.parametrize("packet_type", [None, CanPacketType.SINGLE_FRAME, CanPacketType.FIRST_FRAME,
                                             CanPacketType.CONSECUTIVE_FRAME, "x"])
    def test_st_min__none(self, packet_type):
        self.mock_can_packet.packet_type = packet_type
        assert CanPacket.st_min.fget(self=self.mock_can_packet) is None

    def test_st_min__flow_control(self):
        self.mock_can_packet.packet_type = CanPacketType.FLOW_CONTROL
        assert CanPacket.st_min.fget(self=self.mock_can_packet) \
               == self.mock_flow_control_handler_class.decode_st_min.return_value
        self.mock_flow_control_handler_class.decode_st_min.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format,
            raw_frame_data=self.mock_can_packet.raw_frame_data)

    # __validate_unambiguous_ai_change

    @pytest.mark.parametrize("new_addressing_format", list(CanAddressingFormat))
    def test_validate_unambiguous_ai_change__none(self, new_addressing_format):
        self.mock_can_packet.addressing_format = None
        CanPacket._CanPacket__validate_unambiguous_ai_change(self=self.mock_can_packet,
                                                             addressing_format=new_addressing_format)
        self.mock_ai_handler_class.get_ai_data_bytes_number.assert_not_called()

    @pytest.mark.parametrize("data_bytes_used", [0, 1])
    @pytest.mark.parametrize("new_addressing_format", ["value 1", "value 2"])
    @pytest.mark.parametrize("old_addressing_format", ["other 1", "other 2"])
    def test_validate_unambiguous_ai_change__compatible(self, new_addressing_format, old_addressing_format,
                                                        data_bytes_used):
        self.mock_can_packet.addressing_format = old_addressing_format
        self.mock_ai_handler_class.get_number_of_data_bytes_used.return_value = data_bytes_used
        CanPacket._CanPacket__validate_unambiguous_ai_change(self=self.mock_can_packet,
                                                             addressing_format=new_addressing_format)
        self.mock_ai_handler_class.get_ai_data_bytes_number.assert_has_calls(
            [call(new_addressing_format), call(old_addressing_format)], any_order=True)

    @pytest.mark.parametrize("data_bytes_used", [(0, 1), (1, 0)])
    @pytest.mark.parametrize("new_addressing_format", ["value 1", "value 2"])
    @pytest.mark.parametrize("old_addressing_format", ["other 1", "other 2"])
    def test_validate_unambiguous_ai_change__incompatible(self, new_addressing_format, old_addressing_format,
                                                          data_bytes_used):
        self.mock_can_packet.addressing_format = old_addressing_format
        self.mock_ai_handler_class.get_ai_data_bytes_number.side_effect = data_bytes_used
        with pytest.raises(AmbiguityError):
            CanPacket._CanPacket__validate_unambiguous_ai_change(self=self.mock_can_packet,
                                                                 addressing_format=new_addressing_format)
        self.mock_ai_handler_class.get_ai_data_bytes_number.assert_has_calls(
            [call(new_addressing_format), call(old_addressing_format)], any_order=True)


class TestCanPacketIntegration:
    """Integration tests for `CanPacket` class."""

    # __init__

    @pytest.mark.parametrize("init_args, expected_attribute_values", [
        # SF
        ({"packet_type": CanPacketType.SINGLE_FRAME,
          "addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "addressing_type": AddressingType.PHYSICAL,
          "target_address": 0xE9,
          "source_address": 0xB7,
          "address_extension": 0xDB,
          "dlc": 8,
          "payload": [0x3E]},
         {"raw_frame_data": (0xDB, 0x01, 0x3E, DEFAULT_FILLER_BYTE, DEFAULT_FILLER_BYTE, DEFAULT_FILLER_BYTE, DEFAULT_FILLER_BYTE, DEFAULT_FILLER_BYTE),
          "addressing_type": AddressingType.PHYSICAL,
          "addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "packet_type": CanPacketType.SINGLE_FRAME,
          "can_id": 0x18CEE9B7,
          "dlc": 8,
          "target_address": 0xE9,
          "source_address": 0xB7,
          "address_extension": 0xDB,
          "payload": (0x3E, ),
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
          "payload": tuple(range(50, 108)),
          "data_length": 0xFEDCBA98},
         {"raw_frame_data": tuple([0x10, 0x00, 0xFE, 0xDC, 0xBA, 0x98] + list(range(50, 108))),
          "addressing_type": AddressingType.FUNCTIONAL,
          "addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "packet_type": CanPacketType.FIRST_FRAME,
          "can_id": 0x18DB023B,
          "dlc": 0xF,
          "target_address": 0x02,
          "source_address": 0x3B,
          "address_extension": None,
          "payload": tuple(range(50, 108)),
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
          "payload": [0x91, 0x82],
          "sequence_number": 0x1},
         {"raw_frame_data": (0xB1, 0x21, 0x91, 0x82),
          "addressing_type": AddressingType.FUNCTIONAL,
          "addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "packet_type": CanPacketType.CONSECUTIVE_FRAME,
          "can_id": 0x743,
          "dlc": 4,
          "target_address": 0xB1,
          "source_address": None,
          "address_extension": None,
          "payload": (0x91, 0x82),
          "data_length": None,
          "sequence_number": 0x1,
          "flow_status": None,
          "block_size": None,
          "st_min": None}),
        # FC
        ({"packet_type": CanPacketType.FLOW_CONTROL,
          "addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
          "addressing_type": AddressingType.PHYSICAL,
          "can_id": 0x1234567,
          "flow_status": CanFlowStatus.ContinueToSend,
          "block_size": 0xF9,
          "st_min": 0xE0},
         {"raw_frame_data": (0x30, 0xF0, 0xE0),
          "addressing_type": AddressingType.PHYSICAL,
          "addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
          "packet_type": CanPacketType.FLOW_CONTROL,
          "can_id": 0x1234567,
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
    def test_init(self, init_args, expected_attribute_values):
        packet = CanPacket(**init_args)
        for attr_name, attr_value in expected_attribute_values.items():
            assert getattr(packet, attr_name) == attr_value

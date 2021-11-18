import pytest
from mock import patch, Mock, call

from uds.packet.can_packet import CanPacket, \
    CanPacketType, CanAddressingFormat, AddressingType, CanIdHandler, DEFAULT_FILLER_BYTE, AmbiguityError
from uds.can import CanFlowStatus


class TestCanPacket:
    """Unit tests for 'CanPacket' class."""

    SCRIPT_LOCATION = "uds.packet.can_packet"

    def setup(self):
        self.mock_can_packet = Mock(spec=CanPacket)
        mock_can_id_handler_class = Mock(spec=CanIdHandler,
                                         ADDRESSING_TYPE_NAME=CanIdHandler.ADDRESSING_TYPE_NAME,
                                         TARGET_ADDRESS_NAME=CanIdHandler.TARGET_ADDRESS_NAME,
                                         SOURCE_ADDRESS_NAME=CanIdHandler.SOURCE_ADDRESS_NAME)
        # patching
        self._patcher_warn = patch(f"{self.SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()
        self._patcher_can_dlc_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler")
        self.mock_can_dlc_handler_class = self._patcher_can_dlc_handler_class.start()
        self._patcher_can_id_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanIdHandler", mock_can_id_handler_class)
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
        self._patcher_addressing_type_class = patch(f"{self.SCRIPT_LOCATION}.AddressingType")
        self.mock_addressing_type_class = self._patcher_addressing_type_class.start()
        self._patcher_validate_addressing_format = patch(f"{self.SCRIPT_LOCATION}.CanAddressingFormat.validate_member")
        self.mock_validate_addressing_format = self._patcher_validate_addressing_format.start()
        self._patcher_validate_packet_type = patch(f"{self.SCRIPT_LOCATION}.CanPacketType.validate_member")
        self.mock_validate_packet_type = self._patcher_validate_packet_type.start()

    def teardown(self):
        self._patcher_warn.stop()
        self._patcher_can_dlc_handler_class.stop()
        self._patcher_can_id_handler_class.stop()
        self._patcher_ai_handler_class.stop()
        self._patcher_single_frame_handler_class.stop()
        self._patcher_first_frame_handler_class.stop()
        self._patcher_consecutive_frame_handler_class.stop()
        self._patcher_flow_control_handler_class.stop()
        self._patcher_addressing_type_class.stop()
        self._patcher_validate_addressing_format.stop()
        self._patcher_validate_packet_type.stop()

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

    @pytest.mark.parametrize("can_id, addressing_type", [
        ("some CAN ID", "some addressing type"),
        (0x64A, AddressingType.PHYSICAL),
    ])
    def test_set_address_information_normal_11bit(self, can_id, addressing_type):
        CanPacket.set_address_information_normal_11bit(self=self.mock_can_packet,
                                                       addressing_type=addressing_type,
                                                       can_id=can_id)
        self.mock_ai_handler_class.validate_ai_normal_11bit.assert_called_once_with(
            addressing_type=addressing_type, can_id=can_id)
        self.mock_can_packet._CanPacket__validate_unambiguous_ai_change.assert_called_once_with(
            CanAddressingFormat.NORMAL_11BIT_ADDRESSING)
        self.mock_addressing_type_class.assert_called_once_with(addressing_type)
        assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.NORMAL_11BIT_ADDRESSING
        assert self.mock_can_packet._CanPacket__addressing_type == self.mock_addressing_type_class.return_value
        assert self.mock_can_packet._CanPacket__can_id == can_id
        assert self.mock_can_packet._CanPacket__target_address is None
        assert self.mock_can_packet._CanPacket__source_address is None
        assert self.mock_can_packet._CanPacket__address_extension is None

    # set_address_information_normal_fixed

    @pytest.mark.parametrize("can_id, addressing_type", [
        ("some CAN ID", "some addressing type"),
        (0x64A, AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("decoded_target_address, decoded_source_address, decoded_addressing_type", [
        ("TA", "SA", "Addressing"),
        (0x15, 0x6B, AddressingType.PHYSICAL),
    ])
    def test_set_address_information_normal_fixed__can_id(self, can_id, addressing_type,
                                                          decoded_target_address, decoded_source_address,
                                                          decoded_addressing_type):
        self.mock_addressing_type_class.return_value = decoded_addressing_type
        self.mock_can_id_handler_class.decode_normal_fixed_addressed_can_id.return_value = {
            "addressing_type": decoded_addressing_type,
            "target_address": decoded_target_address,
            "source_address": decoded_source_address,
        }
        CanPacket.set_address_information_normal_fixed(self=self.mock_can_packet,
                                                       addressing_type=addressing_type,
                                                       can_id=can_id)
        self.mock_ai_handler_class.validate_ai_normal_fixed.assert_called_once_with(
            addressing_type=addressing_type,
            can_id=can_id,
            target_address=None,
            source_address=None)
        self.mock_can_packet._CanPacket__validate_unambiguous_ai_change.assert_called_once_with(
            CanAddressingFormat.NORMAL_FIXED_ADDRESSING)
        self.mock_can_id_handler_class.decode_normal_fixed_addressed_can_id.assert_called_once_with(can_id)
        self.mock_can_id_handler_class.encode_normal_fixed_addressed_can_id.assert_not_called()
        assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.NORMAL_FIXED_ADDRESSING
        assert self.mock_can_packet._CanPacket__addressing_type == self.mock_addressing_type_class.return_value
        assert self.mock_can_packet._CanPacket__can_id == can_id
        assert self.mock_can_packet._CanPacket__target_address == decoded_target_address
        assert self.mock_can_packet._CanPacket__source_address == decoded_source_address
        assert self.mock_can_packet._CanPacket__address_extension is None

    @pytest.mark.parametrize("target_address, source_address, addressing_type", [
        ("TA", "SA", "Addressing"),
        (0x15, 0x6B, AddressingType.PHYSICAL),
    ])
    def test_set_address_information_normal_fixed__ta_sa(self, addressing_type, target_address, source_address):
        CanPacket.set_address_information_normal_fixed(self=self.mock_can_packet,
                                                       addressing_type=addressing_type,
                                                       target_address=target_address,
                                                       source_address=source_address)
        self.mock_ai_handler_class.validate_ai_normal_fixed.assert_called_once_with(
            addressing_type=addressing_type,
            can_id=None,
            target_address=target_address,
            source_address=source_address)
        self.mock_can_packet._CanPacket__validate_unambiguous_ai_change.assert_called_once_with(
            CanAddressingFormat.NORMAL_FIXED_ADDRESSING)
        self.mock_can_id_handler_class.decode_normal_fixed_addressed_can_id.assert_not_called()
        self.mock_can_id_handler_class.encode_normal_fixed_addressed_can_id.assert_called_once_with(
            addressing_type=addressing_type, target_address=target_address, source_address=source_address)
        assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.NORMAL_FIXED_ADDRESSING
        assert self.mock_can_packet._CanPacket__addressing_type == self.mock_addressing_type_class.return_value
        assert self.mock_can_packet._CanPacket__can_id == self.mock_can_id_handler_class.encode_normal_fixed_addressed_can_id.return_value
        assert self.mock_can_packet._CanPacket__target_address == target_address
        assert self.mock_can_packet._CanPacket__source_address == source_address
        assert self.mock_can_packet._CanPacket__address_extension is None

    # set_address_information_extended

    @pytest.mark.parametrize("can_id, target_address, addressing_type", [
        ("CAN ID", "TA", "Addressing"),
        (0x98765, 0x1F, AddressingType.FUNCTIONAL),
    ])
    def test_set_address_information_extended(self, addressing_type, can_id, target_address):
        CanPacket.set_address_information_extended(self=self.mock_can_packet,
                                                   addressing_type=addressing_type,
                                                   can_id=can_id,
                                                   target_address=target_address)
        self.mock_ai_handler_class.validate_ai_extended.assert_called_once_with(
            addressing_type=addressing_type,
            can_id=can_id,
            target_address=target_address)
        self.mock_can_packet._CanPacket__validate_unambiguous_ai_change.assert_called_once_with(
            CanAddressingFormat.EXTENDED_ADDRESSING)
        assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.EXTENDED_ADDRESSING
        assert self.mock_can_packet._CanPacket__addressing_type == self.mock_addressing_type_class.return_value
        assert self.mock_can_packet._CanPacket__can_id == can_id
        assert self.mock_can_packet._CanPacket__target_address == target_address
        assert self.mock_can_packet._CanPacket__source_address is None
        assert self.mock_can_packet._CanPacket__address_extension is None

    # set_address_information_mixed_11bit

    @pytest.mark.parametrize("can_id, address_extension, addressing_type", [
        ("CAN ID", "AE", "Addressing"),
        (0x98765, 0x1F, AddressingType.FUNCTIONAL),
    ])
    def test_set_address_information_mixed_11bit(self, addressing_type, can_id, address_extension):
        CanPacket.set_address_information_mixed_11bit(self=self.mock_can_packet,
                                                      addressing_type=addressing_type,
                                                      can_id=can_id,
                                                      address_extension=address_extension)
        self.mock_ai_handler_class.validate_ai_mixed_11bit.assert_called_once_with(
            addressing_type=addressing_type,
            can_id=can_id,
            address_extension=address_extension)
        self.mock_can_packet._CanPacket__validate_unambiguous_ai_change.assert_called_once_with(
            CanAddressingFormat.MIXED_11BIT_ADDRESSING)
        assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.MIXED_11BIT_ADDRESSING
        assert self.mock_can_packet._CanPacket__addressing_type == self.mock_addressing_type_class.return_value
        assert self.mock_can_packet._CanPacket__can_id == can_id
        assert self.mock_can_packet._CanPacket__target_address is None
        assert self.mock_can_packet._CanPacket__source_address is None
        assert self.mock_can_packet._CanPacket__address_extension == address_extension

    # set_address_information_mixed_29bit

    @pytest.mark.parametrize("can_id, addressing_type", [
        ("some CAN ID", "some addressing type"),
        (0x64A, AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("decoded_target_address, decoded_source_address, decoded_addressing_type", [
        ("TA", "SA", "Addressing"),
        (0x15, 0x6B, AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("address_extension", ["some ae", 0x5F])
    def test_set_address_information_mixed_29bit__can_id(self, addressing_type, can_id, address_extension,
                                                         decoded_target_address, decoded_source_address, decoded_addressing_type):
        self.mock_addressing_type_class.return_value = decoded_addressing_type
        self.mock_can_id_handler_class.decode_mixed_addressed_29bit_can_id.return_value = {
            "addressing_type": decoded_addressing_type,
            "target_address": decoded_target_address,
            "source_address": decoded_source_address,
        }
        CanPacket.set_address_information_mixed_29bit(self=self.mock_can_packet,
                                                      addressing_type=addressing_type,
                                                      can_id=can_id,
                                                      address_extension=address_extension)
        self.mock_ai_handler_class.validate_ai_mixed_29bit.assert_called_once_with(
            addressing_type=addressing_type,
            can_id=can_id,
            target_address=None,
            source_address=None,
            address_extension=address_extension)
        self.mock_can_packet._CanPacket__validate_unambiguous_ai_change.assert_called_once_with(
            CanAddressingFormat.MIXED_29BIT_ADDRESSING)
        self.mock_can_id_handler_class.decode_mixed_addressed_29bit_can_id.assert_called_once_with(can_id)
        self.mock_can_id_handler_class.encode_mixed_addressed_29bit_can_id.assert_not_called()
        assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.MIXED_29BIT_ADDRESSING
        assert self.mock_can_packet._CanPacket__addressing_type == self.mock_addressing_type_class.return_value
        assert self.mock_can_packet._CanPacket__can_id == can_id
        assert self.mock_can_packet._CanPacket__target_address == decoded_target_address
        assert self.mock_can_packet._CanPacket__source_address == decoded_source_address
        assert self.mock_can_packet._CanPacket__address_extension == address_extension

    @pytest.mark.parametrize("target_address, source_address, address_extension, addressing_type", [
        ("TA", "SA", "AE", "Addressing"),
        (0x15, 0x6B, 0x5F, AddressingType.PHYSICAL),
    ])
    def test_set_address_information_mixed_29bit__ta_sa(self, addressing_type,
                                                        target_address, source_address, address_extension):
        CanPacket.set_address_information_mixed_29bit(self=self.mock_can_packet,
                                                      addressing_type=addressing_type,
                                                      target_address=target_address,
                                                      source_address=source_address,
                                                      address_extension=address_extension)
        self.mock_ai_handler_class.validate_ai_mixed_29bit.assert_called_once_with(
            addressing_type=addressing_type,
            can_id=None,
            target_address=target_address,
            source_address=source_address,
            address_extension=address_extension)
        self.mock_can_packet._CanPacket__validate_unambiguous_ai_change.assert_called_once_with(
            CanAddressingFormat.MIXED_29BIT_ADDRESSING)
        self.mock_can_id_handler_class.decode_normal_fixed_addressed_can_id.assert_not_called()
        self.mock_can_id_handler_class.encode_mixed_addressed_29bit_can_id.assert_called_once_with(
            addressing_type=addressing_type, target_address=target_address, source_address=source_address)
        assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.MIXED_29BIT_ADDRESSING
        assert self.mock_can_packet._CanPacket__addressing_type == self.mock_addressing_type_class.return_value
        assert self.mock_can_packet._CanPacket__can_id == self.mock_can_id_handler_class.encode_mixed_addressed_29bit_can_id.return_value
        assert self.mock_can_packet._CanPacket__target_address == target_address
        assert self.mock_can_packet._CanPacket__source_address == source_address
        assert self.mock_can_packet._CanPacket__address_extension == address_extension

    # set_packet_data

    @pytest.mark.parametrize("packet_type", [None, "unknown"])
    @pytest.mark.parametrize("dlc, kwargs", [
        ("some dlc", {"p1": "v1", "p2": "v2"}),
        (8, {}),
    ])
    def test_set_packet_data__unknown_packet_type(self, packet_type, dlc, kwargs):
        with pytest.raises(NotImplementedError):
            CanPacket.set_packet_data(self=self.mock_can_packet,
                                      packet_type=packet_type,
                                      dlc=dlc,
                                      **kwargs)
        self.mock_validate_packet_type.assert_called_once_with(packet_type)

    @pytest.mark.parametrize("dlc, kwargs", [
        ("some dlc", {"p1": "v1", "p2": "v2"}),
        (8, {}),
    ])
    def test_set_packet_data__single_frame(self, dlc, kwargs):
        CanPacket.set_packet_data(self=self.mock_can_packet,
                                  packet_type=CanPacketType.SINGLE_FRAME,
                                  dlc=dlc,
                                  **kwargs)
        self.mock_validate_packet_type.assert_called_once_with(CanPacketType.SINGLE_FRAME)
        self.mock_can_packet.set_single_frame_data.assert_called_once_with(dlc=dlc,
                                                                           **kwargs)

    @pytest.mark.parametrize("dlc, kwargs", [
        ("some dlc", {"p1": "v1", "p2": "v2"}),
        (8, {}),
    ])
    def test_set_packet_data__first_frame(self, dlc, kwargs):
        CanPacket.set_packet_data(self=self.mock_can_packet,
                                  packet_type=CanPacketType.FIRST_FRAME,
                                  dlc=dlc,
                                  **kwargs)
        self.mock_validate_packet_type.assert_called_once_with(CanPacketType.FIRST_FRAME)
        self.mock_can_packet.set_first_frame_data.assert_called_once_with(dlc=dlc,
                                                                          **kwargs)

    @pytest.mark.parametrize("dlc, kwargs", [
        ("some dlc", {"p1": "v1", "p2": "v2"}),
        (8, {}),
    ])
    def test_set_packet_data__consecutive_frame(self, dlc, kwargs):
        CanPacket.set_packet_data(self=self.mock_can_packet,
                                  packet_type=CanPacketType.CONSECUTIVE_FRAME,
                                  dlc=dlc,
                                  **kwargs)
        self.mock_validate_packet_type.assert_called_once_with(CanPacketType.CONSECUTIVE_FRAME)
        self.mock_can_packet.set_consecutive_frame_data.assert_called_once_with(dlc=dlc,
                                                                                **kwargs)

    @pytest.mark.parametrize("dlc, kwargs", [
        ("some dlc", {"p1": "v1", "p2": "v2"}),
        (8, {}),
    ])
    def test_set_packet_data__flow_control(self, dlc, kwargs):
        CanPacket.set_packet_data(self=self.mock_can_packet,
                                  packet_type=CanPacketType.FLOW_CONTROL,
                                  dlc=dlc,
                                  **kwargs)
        self.mock_validate_packet_type.assert_called_once_with(CanPacketType.FLOW_CONTROL)
        self.mock_can_packet.set_flow_control_data.assert_called_once_with(dlc=dlc,
                                                                           **kwargs)

    # set_single_frame_data

    @pytest.mark.parametrize("payload", [range(10), [0x50, 0xBC]])
    @pytest.mark.parametrize("raw_frame_data", [(0x12, 0x34), "some raw frame data"])
    def test_set_single_frame_data__mandatory_args(self, payload, raw_frame_data):
        self.mock_single_frame_handler_class.create_valid_frame_data.return_value = raw_frame_data
        CanPacket.set_single_frame_data(self=self.mock_can_packet,
                                        payload=payload)
        self.mock_single_frame_handler_class.create_valid_frame_data.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format,
            target_address=self.mock_can_packet.target_address,
            address_extension=self.mock_can_packet.address_extension,
            payload=payload,
            dlc=None,
            filler_byte=DEFAULT_FILLER_BYTE)
        self.mock_can_dlc_handler_class.encode_dlc.assert_called_once_with(len(raw_frame_data))
        assert self.mock_can_packet._CanPacket__raw_frame_data == tuple(raw_frame_data)
        assert self.mock_can_packet._CanPacket__dlc == self.mock_can_dlc_handler_class.encode_dlc.return_value
        assert self.mock_can_packet._CanPacket__packet_type == CanPacketType.SINGLE_FRAME

    @pytest.mark.parametrize("payload, dlc, filler_byte", [
        (range(10), 8, "filler byte"),
        ([0x50, 0xBC], 3, 0xC0),
    ])
    @pytest.mark.parametrize("raw_frame_data", [(0x12, 0x34), "some raw frame data"])
    def test_set_single_frame_data__all_args(self, payload, dlc, filler_byte, raw_frame_data):
        self.mock_single_frame_handler_class.create_valid_frame_data.return_value = raw_frame_data
        CanPacket.set_single_frame_data(self=self.mock_can_packet,
                                        dlc=dlc,
                                        filler_byte=filler_byte,
                                        payload=payload)
        self.mock_single_frame_handler_class.create_valid_frame_data.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format,
            target_address=self.mock_can_packet.target_address,
            address_extension=self.mock_can_packet.address_extension,
            payload=payload,
            dlc=dlc,
            filler_byte=filler_byte)
        self.mock_can_dlc_handler_class.encode_dlc.assert_not_called()
        assert self.mock_can_packet._CanPacket__raw_frame_data == tuple(raw_frame_data)
        assert self.mock_can_packet._CanPacket__dlc == dlc
        assert self.mock_can_packet._CanPacket__packet_type == CanPacketType.SINGLE_FRAME

    # set_first_frame_data

    @pytest.mark.parametrize("payload, data_length, dlc", [
        ("some payload", "some data length", "DLC"),
        ([0x3E], 0xFEBCA, 8),
    ])
    @pytest.mark.parametrize("raw_frame_data", [(0x12, 0x34), "some raw frame data"])
    def test_set_first_frame_data(self, payload, data_length, dlc, raw_frame_data):
        self.mock_first_frame_handler_class.create_valid_frame_data.return_value = raw_frame_data
        CanPacket.set_first_frame_data(self=self.mock_can_packet,
                                       payload=payload,
                                       data_length=data_length,
                                       dlc=dlc)
        self.mock_first_frame_handler_class.create_valid_frame_data.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format,
            target_address=self.mock_can_packet.target_address,
            address_extension=self.mock_can_packet.address_extension,
            payload=payload,
            dlc=dlc,
            ff_dl=data_length)
        assert self.mock_can_packet._CanPacket__raw_frame_data == tuple(raw_frame_data)
        assert self.mock_can_packet._CanPacket__dlc == dlc
        assert self.mock_can_packet._CanPacket__packet_type == CanPacketType.FIRST_FRAME

    # set_consecutive_frame_data

    @pytest.mark.parametrize("payload, sequence_number", [
        ("some payload", "some sequence number"),
        (range(10), 0xF),
    ])
    @pytest.mark.parametrize("raw_frame_data", [(0x12, 0x34), "some raw frame data"])
    def test_set_consecutive_frame_data__mandatory_args(self, payload, sequence_number, raw_frame_data):
        self.mock_consecutive_frame_handler_class.create_valid_frame_data.return_value = raw_frame_data
        CanPacket.set_consecutive_frame_data(self=self.mock_can_packet,
                                             sequence_number=sequence_number,
                                             payload=payload)
        self.mock_consecutive_frame_handler_class.create_valid_frame_data.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format,
            target_address=self.mock_can_packet.target_address,
            address_extension=self.mock_can_packet.address_extension,
            payload=payload,
            dlc=None,
            filler_byte=DEFAULT_FILLER_BYTE,
            sequence_number=sequence_number)
        self.mock_can_dlc_handler_class.encode_dlc.assert_called_once_with(len(raw_frame_data))
        assert self.mock_can_packet._CanPacket__raw_frame_data == tuple(raw_frame_data)
        assert self.mock_can_packet._CanPacket__dlc == self.mock_can_dlc_handler_class.encode_dlc.return_value
        assert self.mock_can_packet._CanPacket__packet_type == CanPacketType.CONSECUTIVE_FRAME

    @pytest.mark.parametrize("payload, sequence_number, dlc, filler_byte", [
        ("some payload", "some sequence number", "DLC", "filler"),
        (range(10), 0xF, 8, 0xAB),
    ])
    @pytest.mark.parametrize("raw_frame_data", [(0x12, 0x34), "some raw frame data"])
    def test_set_consecutive_frame_data__all_args(self, payload, sequence_number, dlc, filler_byte, raw_frame_data):
        self.mock_consecutive_frame_handler_class.create_valid_frame_data.return_value = raw_frame_data
        CanPacket.set_consecutive_frame_data(self=self.mock_can_packet,
                                             dlc=dlc,
                                             filler_byte=filler_byte,
                                             payload=payload,
                                             sequence_number=sequence_number)
        self.mock_consecutive_frame_handler_class.create_valid_frame_data.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format,
            target_address=self.mock_can_packet.target_address,
            address_extension=self.mock_can_packet.address_extension,
            payload=payload,
            dlc=dlc,
            filler_byte=filler_byte,
            sequence_number=sequence_number)
        self.mock_can_dlc_handler_class.encode_dlc.assert_not_called()
        assert self.mock_can_packet._CanPacket__raw_frame_data == tuple(raw_frame_data)
        assert self.mock_can_packet._CanPacket__dlc == dlc
        assert self.mock_can_packet._CanPacket__packet_type == CanPacketType.CONSECUTIVE_FRAME

    # set_flow_control_data

    @pytest.mark.parametrize("flow_status", ["som flow status", CanFlowStatus.Overflow])
    @pytest.mark.parametrize("raw_frame_data", [(0x12, 0x34), "some raw frame data"])
    def test_set_flow_control_data__mandatory_args(self, flow_status, raw_frame_data):
        self.mock_flow_control_handler_class.create_valid_frame_data.return_value = raw_frame_data
        CanPacket.set_flow_control_data(self=self.mock_can_packet,
                                        flow_status=flow_status)
        self.mock_flow_control_handler_class.create_valid_frame_data.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format,
            target_address=self.mock_can_packet.target_address,
            address_extension=self.mock_can_packet.address_extension,
            flow_status=flow_status,
            block_size=None,
            st_min=None,
            dlc=None,
            filler_byte=DEFAULT_FILLER_BYTE)
        self.mock_can_dlc_handler_class.encode_dlc.assert_called_once_with(len(raw_frame_data))
        assert self.mock_can_packet._CanPacket__raw_frame_data == tuple(raw_frame_data)
        assert self.mock_can_packet._CanPacket__dlc == self.mock_can_dlc_handler_class.encode_dlc.return_value
        assert self.mock_can_packet._CanPacket__packet_type == CanPacketType.FLOW_CONTROL

    @pytest.mark.parametrize("flow_status, block_size, st_min, dlc, filler_byte", [
        ("some flow status", "some block size", "some STmin", "DLC", "A filler"),
        (CanFlowStatus.ContinueToSend, 0x12, 0xFE, 8, 0x99),
    ])
    @pytest.mark.parametrize("raw_frame_data", [(0x12, 0x34), "some raw frame data"])
    def test_set_flow_control_data__all_args(self, flow_status, block_size, st_min, dlc, filler_byte, raw_frame_data):
        self.mock_flow_control_handler_class.create_valid_frame_data.return_value = raw_frame_data
        CanPacket.set_flow_control_data(self=self.mock_can_packet,
                                        flow_status=flow_status,
                                        block_size=block_size,
                                        st_min=st_min,
                                        dlc=dlc,
                                        filler_byte=filler_byte)
        self.mock_flow_control_handler_class.create_valid_frame_data.assert_called_once_with(
            addressing_format=self.mock_can_packet.addressing_format,
            target_address=self.mock_can_packet.target_address,
            address_extension=self.mock_can_packet.address_extension,
            flow_status=flow_status,
            block_size=block_size,
            st_min=st_min,
            dlc=dlc,
            filler_byte=filler_byte)
        assert self.mock_can_packet._CanPacket__raw_frame_data == tuple(raw_frame_data)
        assert self.mock_can_packet._CanPacket__dlc == dlc
        assert self.mock_can_packet._CanPacket__packet_type == CanPacketType.FLOW_CONTROL

    # raw_frame_data

    @pytest.mark.parametrize("value", ["some", 5.5])
    def test_raw_frame_data__get(self, value):
        self.mock_can_packet._CanPacket__raw_frame_data = value
        assert CanPacket.raw_frame_data.fget(self=self.mock_can_packet) == value

    # addressing

    @pytest.mark.parametrize("value", ["some", 5.5])
    def test_addressing_type__get(self, value):
        self.mock_can_packet._CanPacket__addressing_type = value
        assert CanPacket.addressing_type.fget(self=self.mock_can_packet) == value

    # addressing_format

    @pytest.mark.parametrize("value", ["some", 5.5])
    def test_addressing_format__get(self, value):
        self.mock_can_packet._CanPacket__addressing_format = value
        assert CanPacket.addressing_format.fget(self=self.mock_can_packet) == value

    # packet_type

    @pytest.mark.parametrize("value", ["some", 5.5])
    def test_packet_type__get(self, value):
        self.mock_can_packet._CanPacket__packet_type = value
        assert CanPacket.packet_type.fget(self=self.mock_can_packet) == value

    # can_id

    @pytest.mark.parametrize("value", ["some", 5.5])
    def test_can_id__get(self, value):
        self.mock_can_packet._CanPacket__can_id = value
        assert CanPacket.can_id.fget(self=self.mock_can_packet) == value

    # dlc

    @pytest.mark.parametrize("value", ["some", 5.5])
    def test_dlc__get(self, value):
        self.mock_can_packet._CanPacket__dlc = value
        assert CanPacket.dlc.fget(self=self.mock_can_packet) == value

    # target_address

    @pytest.mark.parametrize("value", ["some", 5.5])
    def test_target_address__get(self, value):
        self.mock_can_packet._CanPacket__target_address = value
        assert CanPacket.target_address.fget(self=self.mock_can_packet) == value

    # source_address

    @pytest.mark.parametrize("value", ["some", 5.5])
    def test_source_address__get(self, value):
        self.mock_can_packet._CanPacket__source_address = value
        assert CanPacket.source_address.fget(self=self.mock_can_packet) == value

    # address_extension

    @pytest.mark.parametrize("value", ["some", 5.5])
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

    @pytest.mark.parametrize("packet_type", [None,
                                             CanPacketType.SINGLE_FRAME,
                                             CanPacketType.FIRST_FRAME,
                                             CanPacketType.FLOW_CONTROL,
                                             "something new"])
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

    @pytest.mark.parametrize("packet_type", [None,
                                             CanPacketType.SINGLE_FRAME,
                                             CanPacketType.FIRST_FRAME,
                                             CanPacketType.CONSECUTIVE_FRAME,
                                             "something new"])
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

    @pytest.mark.parametrize("packet_type", [None,
                                             CanPacketType.SINGLE_FRAME,
                                             CanPacketType.FIRST_FRAME,
                                             CanPacketType.CONSECUTIVE_FRAME,
                                             "something new"])
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

    @pytest.mark.parametrize("packet_type", [None,
                                             CanPacketType.SINGLE_FRAME,
                                             CanPacketType.FIRST_FRAME,
                                             CanPacketType.CONSECUTIVE_FRAME,
                                             "something new"])
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

    @pytest.mark.parametrize("packet_type", [None,
                                             CanPacketType.SINGLE_FRAME,
                                             CanPacketType.FIRST_FRAME,
                                             CanPacketType.CONSECUTIVE_FRAME,
                                             "something new"])
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
    @pytest.mark.parametrize("new_addressing_format, old_addressing_format", [
        ("value 1", "value 2"),
        ("other 1", "abcd"),
    ])
    def test_validate_unambiguous_ai_change__compatible(self, new_addressing_format, old_addressing_format,
                                                        data_bytes_used):
        self.mock_can_packet.addressing_format = old_addressing_format
        self.mock_ai_handler_class.get_number_of_data_bytes_used.return_value = data_bytes_used
        CanPacket._CanPacket__validate_unambiguous_ai_change(self=self.mock_can_packet,
                                                             addressing_format=new_addressing_format)
        self.mock_ai_handler_class.get_ai_data_bytes_number.assert_has_calls(
            [call(new_addressing_format), call(old_addressing_format)], any_order=True)

    @pytest.mark.parametrize("data_bytes_used", [(0, 1), (1, 0)])
    @pytest.mark.parametrize("new_addressing_format, old_addressing_format", [
        ("value 1", "value 2"),
        ("other 1", "abcd"),
    ])
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
          "can_id": 0x688,
          "flow_status": CanFlowStatus.ContinueToSend,
          "block_size": 0xF9,
          "st_min": 0xE0},
         {"raw_frame_data": (0x30, 0xF9, 0xE0),
          "addressing_type": AddressingType.PHYSICAL,
          "addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
          "packet_type": CanPacketType.FLOW_CONTROL,
          "can_id": 0x688,
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

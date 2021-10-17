import pytest
from mock import patch, Mock, call

from uds.packet.can_packet import CanPacket, \
    AddressingType, CanAddressingFormat, InconsistentArgumentsError, UnusedArgumentError


class TestCanPacket:
    """Tests for `CanPacket` class."""

    SCRIPT_LOCATION = "uds.packet.can_packet"

    def setup(self):
        self.mock_can_packet = Mock(spec=CanPacket)
        # patching
        self._patcher_validate_addressing_type = patch(f"{self.SCRIPT_LOCATION}.AddressingType.validate_member")
        self.mock_validate_addressing_type = self._patcher_validate_addressing_type.start()
        self._patcher_validate_can_addressing_format = patch(
            f"{self.SCRIPT_LOCATION}.CanAddressingFormat.validate_member")
        self.mock_validate_can_addressing_format = self._patcher_validate_can_addressing_format.start()
        self._patcher_validate_can_packet_type = patch(f"{self.SCRIPT_LOCATION}.CanPacketType.validate_member")
        self.mock_validate_can_packet_type = self._patcher_validate_can_packet_type.start()
        self._patcher_validate_can_id = patch(f"{self.SCRIPT_LOCATION}.CanIdHandler.validate_can_id")
        self.mock_validate_can_id = self._patcher_validate_can_id.start()
        self._patcher_validate_can_dlc = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler.validate_dlc")
        self.mock_validate_can_dlc = self._patcher_validate_can_dlc.start()
        self._patcher_validate_raw_byte = patch(f"{self.SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()

    def teardown(self):
        self._patcher_validate_addressing_type.stop()
        self._patcher_validate_can_addressing_format.stop()
        self._patcher_validate_can_packet_type.stop()
        self._patcher_validate_can_id.stop()
        self._patcher_validate_can_dlc.stop()
        self._patcher_validate_raw_byte.stop()

    # __init__

    @pytest.mark.parametrize("error", [ValueError, TypeError])
    def test_init__error(self, error):
        self.mock_can_packet.set_address_information.side_effect = error
        self.mock_can_packet.set_data.side_effect = error
        with pytest.raises(error):
            CanPacket.__init__(self=self.mock_can_packet,
                               packet_type=None,
                               addressing=None,
                               addressing_format=None)
        assert self.mock_can_packet._CanPacket__addressing is None
        assert self.mock_can_packet._CanPacket__raw_frame_data is None
        assert self.mock_can_packet._CanPacket__packet_type is None
        assert self.mock_can_packet._CanPacket__addressing_format is None
        assert self.mock_can_packet._CanPacket__can_id is None
        assert self.mock_can_packet._CanPacket__dlc is None
        assert self.mock_can_packet._CanPacket__target_address is None
        assert self.mock_can_packet._CanPacket__address_extension is None

    @pytest.mark.parametrize("packet_type", ["some packet type", 1])
    @pytest.mark.parametrize("packet_type_specific_kwargs", [
        {"v1": "some value", "v2": "Some other vlaue"},
        {"p1": "something", "p2": "something else"}
    ])
    @pytest.mark.parametrize("addressing_type, addressing_format", [
        (None, None),
        (AddressingType.FUNCTIONAL, CanAddressingFormat.NORMAL_11BIT_ADDRESSING),
    ])
    @pytest.mark.parametrize("can_id, target_address, source_address, address_extension", [
        (None, 1, 2, 3),
        (0x675, None, None, None),
    ])
    @pytest.mark.parametrize("dlc, filler_byte", [
        (None, 0xCC),
        (8, 0xAA),
    ])
    def test_init(self, packet_type, addressing_type, addressing_format, can_id, target_address, source_address,
                  address_extension, dlc, filler_byte, packet_type_specific_kwargs):
        CanPacket.__init__(self=self.mock_can_packet,
                           packet_type=packet_type,
                           addressing=addressing_type,
                           addressing_format=addressing_format,
                           can_id=can_id,
                           target_address=target_address,
                           source_address=source_address,
                           address_extension=address_extension,
                           dlc=dlc,
                           filler_byte=filler_byte,
                           **packet_type_specific_kwargs)
        assert self.mock_can_packet._CanPacket__addressing is None
        assert self.mock_can_packet._CanPacket__raw_frame_data is None
        assert self.mock_can_packet._CanPacket__packet_type is None
        assert self.mock_can_packet._CanPacket__addressing_format is None
        assert self.mock_can_packet._CanPacket__can_id is None
        assert self.mock_can_packet._CanPacket__dlc is None
        assert self.mock_can_packet._CanPacket__target_address is None
        assert self.mock_can_packet._CanPacket__address_extension is None
        self.mock_can_packet.set_address_information.assert_called_once_with(
            addressing=addressing_type,
            addressing_format=addressing_format,
            can_id=can_id,
            target_address=target_address,
            source_address=source_address,
            address_extension=address_extension)
        self.mock_can_packet.set_data.assert_called_once_with(
            packet_type=packet_type,
            dlc=dlc,
            filler_byte=filler_byte,
            **packet_type_specific_kwargs)

    # set_address_information

    @pytest.mark.parametrize("addressing_format", [None, "unknown addressing format"])
    @pytest.mark.parametrize("addressing, can_id, target_address, source_address, address_extension", [
        ("something", "CAN ID", "TA", "SA", "AE"),
        (AddressingType.PHYSICAL, 0x754, 0x31, 0xD0, 0xE3),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingFormat")
    def test_set_address_information__unknown_addressing_format(self, mock_can_addressing_format_class,
                                                                addressing, addressing_format, can_id, target_address,
                                                                source_address, address_extension):
        mock_can_addressing_format_class.return_value = addressing_format
        with pytest.raises(NotImplementedError):
            CanPacket.set_address_information(self=self.mock_can_packet,
                                              addressing=addressing,
                                              addressing_format=addressing_format,
                                              can_id=can_id,
                                              target_address=target_address,
                                              source_address=source_address,
                                              address_extension=address_extension)
        self.mock_can_packet._CanPacket__validate_ai.assert_called_once_with(addressing=addressing,
                                                                             addressing_format=addressing_format,
                                                                             can_id=can_id,
                                                                             target_address=target_address,
                                                                             source_address=source_address,
                                                                             address_extension=address_extension)
        mock_can_addressing_format_class.assert_called_once_with(addressing_format)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                   CanAddressingFormat.NORMAL_11BIT_ADDRESSING.value])
    @pytest.mark.parametrize("can_id", [0x1234, 0x721])
    def test_set_address_information__normal_11_bit(self, addressing_format, example_addressing_type, can_id):
        CanPacket.set_address_information(self=self.mock_can_packet,
                                          addressing=example_addressing_type,
                                          addressing_format=addressing_format,
                                          can_id=can_id)
        self.mock_can_packet._CanPacket__set_address_information_normal_11bit.assert_called_once_with(
            addressing=example_addressing_type,
            can_id=can_id)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                                   CanAddressingFormat.NORMAL_FIXED_ADDRESSING.value])
    @pytest.mark.parametrize("can_id, target_address, source_address", [
        (0x12345, 0x65, 0xFD),
        (0xDCFE, None, None),
    ])
    def test_set_address_information__normal_fixed(self, addressing_format, example_addressing_type,
                                                   can_id, target_address, source_address):
        CanPacket.set_address_information(self=self.mock_can_packet,
                                          addressing=example_addressing_type,
                                          addressing_format=addressing_format,
                                          can_id=can_id,
                                          target_address=target_address,
                                          source_address=source_address)
        self.mock_can_packet._CanPacket__set_address_information_normal_fixed.assert_called_once_with(
            addressing=example_addressing_type,
            can_id=can_id,
            target_address=target_address,
            source_address=source_address)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.EXTENDED_ADDRESSING,
                                                   CanAddressingFormat.EXTENDED_ADDRESSING.value])
    @pytest.mark.parametrize("can_id, target_address", [
        (0x12345, 0x65),
        (0xDCFE, None),
    ])
    def test_set_address_information__extended(self, addressing_format, example_addressing_type,
                                               can_id, target_address):
        CanPacket.set_address_information(self=self.mock_can_packet,
                                          addressing=example_addressing_type,
                                          addressing_format=addressing_format,
                                          can_id=can_id,
                                          target_address=target_address)
        self.mock_can_packet._CanPacket__set_address_information_extended.assert_called_once_with(
            addressing=example_addressing_type,
            can_id=can_id,
            target_address=target_address)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                   CanAddressingFormat.MIXED_11BIT_ADDRESSING.value])
    @pytest.mark.parametrize("can_id, address_extension", [
        (0x12345, 0x65),
        (0xDCFE, None),
    ])
    def test_set_address_information__mixed_11bit(self, addressing_format, example_addressing_type,
                                                  can_id, address_extension):
        CanPacket.set_address_information(self=self.mock_can_packet,
                                          addressing=example_addressing_type,
                                          addressing_format=addressing_format,
                                          can_id=can_id,
                                          address_extension=address_extension)
        self.mock_can_packet._CanPacket__set_address_information_mixed_11bit.assert_called_once_with(
            addressing=example_addressing_type,
            can_id=can_id,
            address_extension=address_extension)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                                   CanAddressingFormat.MIXED_29BIT_ADDRESSING.value])
    @pytest.mark.parametrize("can_id, target_address, source_address, address_extension", [
        (0x12345, 0x65, 0xFA, 0x03),
        (0xDCFE, None, None, None),
    ])
    def test_set_address_information__mixed_29bit(self, addressing_format, example_addressing_type,
                                                  can_id, target_address, source_address, address_extension):
        CanPacket.set_address_information(self=self.mock_can_packet,
                                          addressing=example_addressing_type,
                                          addressing_format=addressing_format,
                                          can_id=can_id,
                                          target_address=target_address,
                                          source_address=source_address,
                                          address_extension=address_extension)
        self.mock_can_packet._CanPacket__set_address_information_mixed_29bit.assert_called_once_with(
            addressing=example_addressing_type,
            can_id=can_id,
            target_address=target_address,
            source_address=source_address,
            address_extension=address_extension)

    # __validate_ai

    @pytest.mark.parametrize("addressing", ["addressing", AddressingType.FUNCTIONAL])
    @pytest.mark.parametrize("addressing_format", ["addressing format", CanAddressingFormat.NORMAL_11BIT_ADDRESSING])
    @pytest.mark.parametrize("can_id, target_address, source_address, address_extension", [
        (0x918273, 0x8F, 0xEB, 0xA0),
        (0x881DB, 0x02, None, 0x0B),
    ])
    def test_validate_ai(self, addressing, addressing_format, can_id, target_address, source_address,
                         address_extension):
        CanPacket._CanPacket__validate_ai(self=self.mock_can_packet,
                                          addressing=addressing,
                                          addressing_format=addressing_format,
                                          can_id=can_id,
                                          target_address=target_address,
                                          source_address=source_address,
                                          address_extension=address_extension)
        self.mock_validate_addressing_type.assert_called_once_with(addressing)
        self.mock_validate_can_addressing_format.assert_called_once_with(addressing_format)
        self.mock_can_packet._CanPacket__validate_ai_consistency.assert_called_once_with(addressing=addressing,
                                                                                         addressing_format=addressing_format,
                                                                                         can_id=can_id,
                                                                                         target_address=target_address,
                                                                                         source_address=source_address,
                                                                                         address_extension=address_extension)

    # __validate_ai_consistency

    @pytest.mark.parametrize("addressing_format", [None, "some unknown addressing format"])
    @pytest.mark.parametrize("addressing, can_id, target_address, source_address, address_extension", [
        (None, None, None, None, None),
        (AddressingType.PHYSICAL, 0x7FF, None, None, None),
        (AddressingType.FUNCTIONAL, 0x18091232, 0x98, 0xB1, 0xC0),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingFormat")
    def test_validate_ai_consistency__unknown_addressing_format(self, mock_can_addressing_format_class,
                                                                addressing_format, addressing, can_id,
                                                                target_address, source_address, address_extension):
        mock_can_addressing_format_class.return_value = addressing_format
        with pytest.raises(NotImplementedError):
            CanPacket._CanPacket__validate_ai_consistency(self=self.mock_can_packet,
                                                          addressing=addressing,
                                                          addressing_format=addressing_format,
                                                          can_id=can_id,
                                                          target_address=target_address,
                                                          source_address=source_address,
                                                          address_extension=address_extension)
        mock_can_addressing_format_class.assert_called_once_with(addressing_format)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                   CanAddressingFormat.NORMAL_11BIT_ADDRESSING.value])
    @pytest.mark.parametrize("can_id, target_address, source_address, address_extension", [
        (None, None, None, None),
        (0x7FF, None, None, 0x97),
        (0x612, 0x54, 0xAA, None),
        (0x18091232, 0x98, 0xB1, 0xC0),
    ])
    def test_validate_ai_consistency__normal_11bit(self, addressing_format, example_addressing_type, can_id,
                                                   target_address, source_address, address_extension):
        CanPacket._CanPacket__validate_ai_consistency(self=self.mock_can_packet,
                                                      addressing=example_addressing_type,
                                                      addressing_format=addressing_format,
                                                      can_id=can_id,
                                                      target_address=target_address,
                                                      source_address=source_address,
                                                      address_extension=address_extension)
        self.mock_can_packet._CanPacket__validate_ai_consistency_normal_11bit.assert_called_once_with(
            can_id=can_id,
            target_address=target_address,
            source_address=source_address,
            address_extension=address_extension)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                                   CanAddressingFormat.NORMAL_FIXED_ADDRESSING.value])
    @pytest.mark.parametrize("can_id, target_address, source_address, address_extension", [
        (None, None, None, None),
        (0x7FF, None, None, 0x97),
        (0x612, 0x54, 0xAA, None),
        (0x18091232, 0x98, 0xB1, 0xC0),
    ])
    def test_validate_ai_consistency__normal_fixed(self, addressing_format, example_addressing_type, can_id,
                                                   target_address, source_address, address_extension):
        CanPacket._CanPacket__validate_ai_consistency(self=self.mock_can_packet,
                                                      addressing=example_addressing_type,
                                                      addressing_format=addressing_format,
                                                      can_id=can_id,
                                                      target_address=target_address,
                                                      source_address=source_address,
                                                      address_extension=address_extension)
        self.mock_can_packet._CanPacket__validate_ai_consistency_normal_fixed.assert_called_once_with(
            addressing=example_addressing_type,
            can_id=can_id,
            target_address=target_address,
            source_address=source_address,
            address_extension=address_extension)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.EXTENDED_ADDRESSING,
                                                   CanAddressingFormat.EXTENDED_ADDRESSING.value])
    @pytest.mark.parametrize("can_id, target_address, source_address, address_extension", [
        (None, None, None, None),
        (0x7FF, None, None, 0x97),
        (0x612, 0x54, 0xAA, None),
        (0x18091232, 0x98, 0xB1, 0xC0),
    ])
    def test_validate_ai_consistency__extended(self, addressing_format, example_addressing_type, can_id,
                                               target_address, source_address, address_extension):
        CanPacket._CanPacket__validate_ai_consistency(self=self.mock_can_packet,
                                                      addressing=example_addressing_type,
                                                      addressing_format=addressing_format,
                                                      can_id=can_id,
                                                      target_address=target_address,
                                                      source_address=source_address,
                                                      address_extension=address_extension)
        self.mock_can_packet._CanPacket__validate_ai_consistency_extended.assert_called_once_with(
            addressing=example_addressing_type,
            can_id=can_id,
            target_address=target_address,
            source_address=source_address,
            address_extension=address_extension)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                   CanAddressingFormat.MIXED_11BIT_ADDRESSING.value])
    @pytest.mark.parametrize("can_id, target_address, source_address, address_extension", [
        (None, None, None, None),
        (0x7FF, None, None, 0x97),
        (0x612, 0x54, 0xAA, None),
        (0x18091232, 0x98, 0xB1, 0xC0),
    ])
    def test_validate_ai_consistency__mixed_11bit(self, addressing_format, example_addressing_type, can_id,
                                                  target_address, source_address, address_extension):
        CanPacket._CanPacket__validate_ai_consistency(self=self.mock_can_packet,
                                                      addressing=example_addressing_type,
                                                      addressing_format=addressing_format,
                                                      can_id=can_id,
                                                      target_address=target_address,
                                                      source_address=source_address,
                                                      address_extension=address_extension)
        self.mock_can_packet._CanPacket__validate_ai_consistency_mixed_11bit.assert_called_once_with(
            addressing=example_addressing_type,
            can_id=can_id,
            target_address=target_address,
            source_address=source_address,
            address_extension=address_extension)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                                   CanAddressingFormat.MIXED_29BIT_ADDRESSING.value])
    @pytest.mark.parametrize("can_id, target_address, source_address, address_extension", [
        (None, None, None, None),
        (0x7FF, None, None, 0x97),
        (0x612, 0x54, 0xAA, None),
        (0x18091232, 0x98, 0xB1, 0xC0),
    ])
    def test_validate_ai_consistency__mixed_29bit(self, addressing_format, example_addressing_type, can_id,
                                                  target_address, source_address, address_extension):
        CanPacket._CanPacket__validate_ai_consistency(self=self.mock_can_packet,
                                                      addressing=example_addressing_type,
                                                      addressing_format=addressing_format,
                                                      can_id=can_id,
                                                      target_address=target_address,
                                                      source_address=source_address,
                                                      address_extension=address_extension)
        self.mock_can_packet._CanPacket__validate_ai_consistency_mixed_29bit.assert_called_once_with(
            addressing=example_addressing_type,
            can_id=can_id,
            target_address=target_address,
            source_address=source_address,
            address_extension=address_extension)

    # __validate_ai_consistency_normal_11bit

    @pytest.mark.parametrize("can_id", [0x1234, 0x98FA])
    @pytest.mark.parametrize("target_address, source_address, address_extension", [
        (0, 0, 0),
        (0x05, None, None),
        (None, 0xFB, None),
        (None, None, 0x9C),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_11bit_addressed_can_id")
    def test_validate_ai_consistency_normal_11bit__unused_args(self, mock_is_normal_11bit_addressed_can_id,
                                                               can_id, target_address, source_address,
                                                               address_extension):
        mock_is_normal_11bit_addressed_can_id.return_value = True
        with pytest.raises(UnusedArgumentError):
            CanPacket._CanPacket__validate_ai_consistency_normal_11bit(self=self.mock_can_packet,
                                                                       can_id=can_id,
                                                                       target_address=target_address,
                                                                       source_address=source_address,
                                                                       address_extension=address_extension)

    @pytest.mark.parametrize("can_id", [0x1234, 0x98FA])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_11bit_addressed_can_id")
    def test_validate_ai_consistency_normal_11bit__invalid_can_id(self, mock_is_normal_11bit_addressed_can_id, can_id):
        mock_is_normal_11bit_addressed_can_id.return_value = False
        with pytest.raises(InconsistentArgumentsError):
            CanPacket._CanPacket__validate_ai_consistency_normal_11bit(self=self.mock_can_packet,
                                                                       can_id=can_id,
                                                                       target_address=None,
                                                                       source_address=None,
                                                                       address_extension=None)

    @pytest.mark.parametrize("can_id", [0x1234, 0x98FA])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_11bit_addressed_can_id")
    def test_validate_ai_consistency_normal_11bit__valid(self, mock_is_normal_11bit_addressed_can_id, can_id):
        mock_is_normal_11bit_addressed_can_id.return_value = True
        CanPacket._CanPacket__validate_ai_consistency_normal_11bit(self=self.mock_can_packet,
                                                                   can_id=can_id,
                                                                   target_address=None,
                                                                   source_address=None,
                                                                   address_extension=None)

    # __validate_ai_consistency_normal_fixed

    @pytest.mark.parametrize("can_id, target_address, source_address", [
        (0xABCDEF, None, None),
        (None, 0x12, 0x98),
    ])
    @pytest.mark.parametrize("address_extension", [0x00, 0x55, 0xFF])
    def test_validate_ai_consistency_normal_11bit__unused_args(self, example_addressing_type,
                                                               can_id, target_address, source_address,
                                                               address_extension):
        with pytest.raises(UnusedArgumentError):
            CanPacket._CanPacket__validate_ai_consistency_normal_fixed(self=self.mock_can_packet,
                                                                       addressing=example_addressing_type,
                                                                       can_id=can_id,
                                                                       target_address=target_address,
                                                                       source_address=source_address,
                                                                       address_extension=address_extension)

    @pytest.mark.parametrize("can_id, target_address, source_address", [
        (0xABCDEF, 0x09, None),
        (0x727384, None, 0xB1),
        (0xABCDEF, 0x9E, 0xFD),
    ])
    def test_validate_ai_consistency_normal_11bit__redundant_args(self, example_addressing_type,
                                                                  can_id, target_address, source_address):
        with pytest.raises(InconsistentArgumentsError):
            CanPacket._CanPacket__validate_ai_consistency_normal_fixed(self=self.mock_can_packet,
                                                                       addressing=example_addressing_type,
                                                                       can_id=can_id,
                                                                       target_address=target_address,
                                                                       source_address=source_address,
                                                                       address_extension=None)

    @pytest.mark.parametrize("can_id, target_address, source_address", [
        (None, 0x09, None),
        (None, None, 0xB1),
        (None, None, None),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_fixed_addressed_can_id")
    def test_validate_ai_consistency_normal_11bit__missing_args(self, example_addressing_type,
                                                                can_id, target_address, source_address):
        with pytest.raises(InconsistentArgumentsError):
            CanPacket._CanPacket__validate_ai_consistency_normal_fixed(self=self.mock_can_packet,
                                                                       addressing=example_addressing_type,
                                                                       can_id=can_id,
                                                                       target_address=target_address,
                                                                       source_address=source_address,
                                                                       address_extension=None)




    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                                   CanAddressingFormat.NORMAL_FIXED_ADDRESSING.value])
    @pytest.mark.parametrize("can_id, target_address, source_address", [
        (None, 0x8B, 0xB1),
        (None, 0x00, 0xFF),
        (0x987645, None, None),
        (0xBE0F8, None, None),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_fixed_addressed_can_id")
    def test_validate_address_information_consistency__normal_fixed__valid(self, mock_is_normal_fixed_addressed_can_id,
                                                                           addressing_format,
                                                                           can_id, target_address, source_address):
        mock_is_normal_fixed_addressed_can_id.return_value = True
        CanPacket._CanPacket__validate_address_information_consistency(self=self.mock_can_packet,
                                                                       addressing_format=addressing_format,
                                                                       can_id=can_id,
                                                                       target_address=target_address,
                                                                       source_address=source_address,
                                                                       address_extension=None)
        if can_id is None:
            self.mock_validate_can_id.assert_not_called()
            mock_is_normal_fixed_addressed_can_id.assert_not_called()
            self.mock_validate_raw_byte.assert_has_calls([call(target_address), call(source_address)])
        else:
            self.mock_validate_can_id.assert_called_once_with(can_id)
            mock_is_normal_fixed_addressed_can_id.assert_called_once_with(can_id)
            self.mock_validate_raw_byte.assert_not_called()

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                                   CanAddressingFormat.NORMAL_FIXED_ADDRESSING.value])
    @pytest.mark.parametrize("can_id", [0x12BDA, 0xA4890])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_fixed_addressed_can_id")
    def test_validate_address_information_consistency__normal_fixed__invalid_can_id(self,
                                                                                    mock_is_normal_fixed_addressed_can_id,
                                                                                    addressing_format, can_id):
        mock_is_normal_fixed_addressed_can_id.return_value = False
        with pytest.raises(InconsistentArgumentsError):
            CanPacket._CanPacket__validate_address_information_consistency(self=self.mock_can_packet,
                                                                           addressing_format=addressing_format,
                                                                           can_id=can_id,
                                                                           target_address=None,
                                                                           source_address=None,
                                                                           address_extension=None)
        self.mock_validate_can_id.assert_called_once_with(can_id)
        mock_is_normal_fixed_addressed_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                                   CanAddressingFormat.NORMAL_FIXED_ADDRESSING.value])
    @pytest.mark.parametrize("target_address, source_address", [
        (None, None),
        (None, 0x77),
        (0x91, None),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_fixed_addressed_can_id")
    def test_validate_address_information_consistency__normal_fixed__missing_args(self,
                                                                                  mock_is_normal_fixed_addressed_can_id,
                                                                                  addressing_format,
                                                                                  target_address, source_address):
        mock_is_normal_fixed_addressed_can_id.return_value = True
        with pytest.raises(InconsistentArgumentsError):
            CanPacket._CanPacket__validate_address_information_consistency(self=self.mock_can_packet,
                                                                           addressing_format=addressing_format,
                                                                           can_id=None,
                                                                           target_address=target_address,
                                                                           source_address=source_address,
                                                                           address_extension=None)

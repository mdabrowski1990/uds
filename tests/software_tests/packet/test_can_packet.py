import pytest

from mock import patch, Mock, call

from uds.packet.can_packet import CanPacketType, CanAddressingFormat, CanFlowStatus, CanSTminTranslator, CanPacket, \
    AddressingType, IncompatibleCanAddressingFormatError, InconsistentArgumentsError
from uds.packet.abstract_packet import AbstractUdsPacketType
from uds.utilities import ValidatedEnum, NibbleEnum


class TestCanPacket:
    """Tests for 'CanPacket' class."""

    SCRIPT_LOCATION = "uds.packet.can_packet"

    def setup(self):
        self.mock_can_packet = Mock(spec=CanPacket)
        # patching
        self._patcher_validate_addressing_type = patch(f"{self.SCRIPT_LOCATION}.AddressingType.validate_member")
        self.mock_validate_addressing_type = self._patcher_validate_addressing_type.start()
        self._patcher_validate_can_addressing_format = patch(f"{self.SCRIPT_LOCATION}.CanAddressingFormat.validate_member")
        self.mock_validate_can_addressing_format = self._patcher_validate_can_addressing_format.start()
        self._patcher_validate_can_id = patch(f"{self.SCRIPT_LOCATION}.CanIdHandler.validate_can_id")
        self.mock_validate_can_id = self._patcher_validate_can_id.start()
        self._patcher_validate_raw_byte = patch(f"{self.SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()

    def teardown(self):
        self._patcher_validate_addressing_type.stop()
        self._patcher_validate_can_addressing_format.stop()
        self._patcher_validate_can_id.stop()
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
        assert self.mock_can_packet._CanPacket__target_address is None
        assert self.mock_can_packet._CanPacket__source_address is None
        assert self.mock_can_packet._CanPacket__address_extension is None
        assert self.mock_can_packet._CanPacket__dlc is None
        assert self.mock_can_packet._CanPacket__use_data_optimization is None
        assert self.mock_can_packet._CanPacket__filler_byte is None

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
    @pytest.mark.parametrize("use_data_optimization, dlc, filler_byte", [
        (True, None, 0xCC),
        (False, 8, 0xAA),
    ])
    def test_init(self, packet_type, addressing_type, addressing_format, can_id, target_address, source_address,
                  address_extension, use_data_optimization, dlc, filler_byte, packet_type_specific_kwargs):
        CanPacket.__init__(self=self.mock_can_packet,
                           packet_type=packet_type,
                           addressing=addressing_type,
                           addressing_format=addressing_format,
                           can_id=can_id,
                           target_address=target_address,
                           source_address=source_address,
                           address_extension=address_extension,
                           use_data_optimization=use_data_optimization,
                           dlc=dlc,
                           filler_byte=filler_byte,
                           **packet_type_specific_kwargs)
        assert self.mock_can_packet._CanPacket__addressing is None
        assert self.mock_can_packet._CanPacket__raw_frame_data is None
        assert self.mock_can_packet._CanPacket__packet_type is None
        assert self.mock_can_packet._CanPacket__addressing_format is None
        assert self.mock_can_packet._CanPacket__can_id is None
        assert self.mock_can_packet._CanPacket__target_address is None
        assert self.mock_can_packet._CanPacket__source_address is None
        assert self.mock_can_packet._CanPacket__address_extension is None
        assert self.mock_can_packet._CanPacket__dlc is None
        assert self.mock_can_packet._CanPacket__use_data_optimization is None
        assert self.mock_can_packet._CanPacket__filler_byte is None
        self.mock_can_packet.set_address_information.assert_called_once_with(
            addressing=addressing_type,
            addressing_format=addressing_format,
            can_id=can_id,
            target_address=target_address,
            source_address=source_address,
            address_extension=address_extension)
        self.mock_can_packet.set_data.assert_called_once_with(
            packet_type=packet_type,
            use_data_optimization=use_data_optimization,
            dlc=dlc,
            filler_byte=filler_byte,
            **packet_type_specific_kwargs)

    # __set_address_information_normal_11bit

    @pytest.mark.parametrize("previous_can_address_format", [CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                                             CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                             CanAddressingFormat.EXTENDED_ADDRESSING,
                                                             "something else"])
    @pytest.mark.parametrize("can_id", ["some ID", 0x1234567])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_11bit_addressed_can_id")
    def test_set_address_information_normal_11bit__incompatible_format(self, mock_is_normal_11bit_addressed_can_id,
                                                                       example_addressing_type, can_id,
                                                                       previous_can_address_format):
        self.mock_can_packet.addressing_format = previous_can_address_format
        with pytest.raises(IncompatibleCanAddressingFormatError):
            CanPacket._CanPacket__set_address_information_normal_11bit(self=self.mock_can_packet,
                                                                       addressing=example_addressing_type,
                                                                       can_id=can_id)
        mock_is_normal_11bit_addressed_can_id.assert_not_called()

    @pytest.mark.parametrize("previous_can_address_format", [None, CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                             CanAddressingFormat.NORMAL_FIXED_ADDRESSING])
    @pytest.mark.parametrize("can_id", ["some ID", 0x1234567])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_11bit_addressed_can_id")
    def test_set_address_information_normal_11bit__value_error(self, mock_is_normal_11bit_addressed_can_id,
                                                               example_addressing_type, can_id,
                                                               previous_can_address_format):
        self.mock_can_packet.addressing_format = previous_can_address_format
        mock_is_normal_11bit_addressed_can_id.return_value = False
        with pytest.raises(ValueError):
            CanPacket._CanPacket__set_address_information_normal_11bit(self=self.mock_can_packet,
                                                                       addressing=example_addressing_type,
                                                                       can_id=can_id)
        mock_is_normal_11bit_addressed_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("previous_can_address_format", [None, CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                             CanAddressingFormat.NORMAL_FIXED_ADDRESSING])
    @pytest.mark.parametrize("can_id", ["some ID", 0x1234567])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_11bit_addressed_can_id")
    def test_set_address_information_normal_11bit__change(self, mock_is_normal_11bit_addressed_can_id,
                                                          example_addressing_type, can_id, previous_can_address_format):
        self.mock_can_packet.addressing_format = previous_can_address_format
        mock_is_normal_11bit_addressed_can_id.return_value = True
        CanPacket._CanPacket__set_address_information_normal_11bit(self=self.mock_can_packet,
                                                                   addressing=example_addressing_type,
                                                                   can_id=can_id)
        mock_is_normal_11bit_addressed_can_id.assert_called_once_with(can_id)
        assert self.mock_can_packet._CanPacket__addressing == example_addressing_type
        assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.NORMAL_11BIT_ADDRESSING
        assert self.mock_can_packet._CanPacket__can_id == can_id
        assert self.mock_can_packet._CanPacket__target_address is None
        assert self.mock_can_packet._CanPacket__source_address is None
        assert self.mock_can_packet._CanPacket__address_extension is None

    # __set_address_information_normal_fixed

    @pytest.mark.parametrize("previous_can_address_format", [CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                                             CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                             CanAddressingFormat.EXTENDED_ADDRESSING,
                                                             "something else"])
    def test_set_address_information_normal_fixed__incompatible_format(self, example_addressing_type,
                                                                       previous_can_address_format):
        self.mock_can_packet.addressing_format = previous_can_address_format
        with pytest.raises(IncompatibleCanAddressingFormatError):
            CanPacket._CanPacket__set_address_information_normal_fixed(self=self.mock_can_packet,
                                                                       addressing=example_addressing_type)

    @pytest.mark.parametrize("previous_can_address_format", [None, CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                             CanAddressingFormat.NORMAL_FIXED_ADDRESSING])
    @pytest.mark.parametrize("addressing, decoded_addressing, can_id, ta, decoded_ta, sa, decoded_sa", [
        (AddressingType.PHYSICAL, AddressingType.FUNCTIONAL, 0x987656, None, 0x11, None, 0x12),
        (AddressingType.FUNCTIONAL, AddressingType.PHYSICAL, 0x987656, None, 0x11, None, 0x12),
        (AddressingType.PHYSICAL, AddressingType.PHYSICAL, 0x1234567, 0x81, 0x91, None, 0x88),
        (AddressingType.PHYSICAL, AddressingType.PHYSICAL, 0x1234567, None, 0x91, 0x68, 0x69),
        (AddressingType.FUNCTIONAL, AddressingType.FUNCTIONAL, 0x987656, 0xFD, 0x11, 0xEC, 0xED),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.decode_normal_fixed_addressed_can_id")
    def test_set_address_information_normal_fixed__inconsistent_can_id_decoded_values(self, mock_decode_normal_fixed_can_id,
                                                                                      previous_can_address_format,
                                                                                      addressing, can_id, ta, sa,
                                                                                      decoded_addressing, decoded_ta,
                                                                                      decoded_sa):
        mock_decode_normal_fixed_can_id.return_value = (decoded_addressing, decoded_ta, decoded_sa)
        self.mock_can_packet.addressing_format = previous_can_address_format
        with pytest.raises(InconsistentArgumentsError):
            CanPacket._CanPacket__set_address_information_normal_fixed(self=self.mock_can_packet,
                                                                       addressing=addressing,
                                                                       can_id=can_id,
                                                                       target_address=ta,
                                                                       source_address=sa)

    @pytest.mark.parametrize("previous_can_address_format", [None, CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                             CanAddressingFormat.NORMAL_FIXED_ADDRESSING])
    @pytest.mark.parametrize("can_id, target_address, source_address", [
        (None, None, 0x12),
        (None, 0xDF, None),
        (None, None, None),
    ])
    def test_set_address_information_normal_fixed__inconsistent_none_values(self, example_addressing_type,
                                                                            previous_can_address_format, can_id,
                                                                            target_address, source_address):
        self.mock_can_packet.addressing_format = previous_can_address_format
        with pytest.raises(InconsistentArgumentsError):
            CanPacket._CanPacket__set_address_information_normal_fixed(self=self.mock_can_packet,
                                                                       addressing=example_addressing_type,
                                                                       can_id=can_id,
                                                                       target_address=target_address,
                                                                       source_address=source_address)

    @pytest.mark.parametrize("previous_can_address_format", [None, CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                             CanAddressingFormat.NORMAL_FIXED_ADDRESSING])
    @pytest.mark.parametrize("addressing, target_address, source_address", [
        (AddressingType.PHYSICAL, 0x12, 0x34),
        (AddressingType.FUNCTIONAL, 0x80, 0xB1),
    ])
    @pytest.mark.parametrize("generated_can_id", [0x18DA0508, 0x18DB624D, 0x7FF, 0x12345678])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.get_normal_fixed_addressed_can_id")
    def test_set_address_information_normal_fixed__change_without_can_id(self, mock_get_normal_fixed_can_id,
                                                                         previous_can_address_format, addressing,
                                                                         generated_can_id, target_address, source_address):
        mock_get_normal_fixed_can_id.return_value = generated_can_id
        self.mock_can_packet.addressing_format = previous_can_address_format
        CanPacket._CanPacket__set_address_information_normal_fixed(self=self.mock_can_packet,
                                                                   addressing=addressing,
                                                                   can_id=None,
                                                                   target_address=target_address,
                                                                   source_address=source_address)
        mock_get_normal_fixed_can_id.assert_called_once_with(addressing_type=addressing,
                                                             target_address=target_address,
                                                             source_address=source_address)
        assert self.mock_can_packet._CanPacket__addressing == addressing
        assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.NORMAL_FIXED_ADDRESSING
        assert self.mock_can_packet._CanPacket__can_id == generated_can_id
        assert self.mock_can_packet._CanPacket__target_address == target_address
        assert self.mock_can_packet._CanPacket__source_address == source_address
        assert self.mock_can_packet._CanPacket__address_extension is None

    @pytest.mark.parametrize("previous_can_address_format", [None, CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                             CanAddressingFormat.NORMAL_FIXED_ADDRESSING])
    @pytest.mark.parametrize("addressing, can_id, ta, decoded_ta, sa, decoded_sa", [
        (AddressingType.PHYSICAL, 0x987656, None, 0x11, None, 0x12),
        (AddressingType.FUNCTIONAL, 0x987656, None, 0x11, None, 0x12),
        (AddressingType.PHYSICAL, 0x1234567, 0x81, 0x81, None, 0x88),
        (AddressingType.PHYSICAL, 0x1234567, None, 0x91, 0x68, 0x68),
        (AddressingType.FUNCTIONAL, 0x987656, 0xFD, 0xFD, 0xEC, 0xEC),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.decode_normal_fixed_addressed_can_id")
    def test_set_address_information_normal_fixed__change_with_can_id(self, mock_decode_normal_fixed_can_id,
                                                                      previous_can_address_format, addressing,
                                                                      can_id, ta, sa, decoded_ta, decoded_sa):
        mock_decode_normal_fixed_can_id.return_value = (addressing, decoded_ta, decoded_sa)
        self.mock_can_packet.addressing_format = previous_can_address_format
        CanPacket._CanPacket__set_address_information_normal_fixed(self=self.mock_can_packet,
                                                                   addressing=addressing,
                                                                   can_id=can_id,
                                                                   target_address=ta,
                                                                   source_address=sa)
        mock_decode_normal_fixed_can_id.assert_called_once_with(can_id=can_id)
        assert self.mock_can_packet._CanPacket__addressing == addressing
        assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.NORMAL_FIXED_ADDRESSING
        assert self.mock_can_packet._CanPacket__can_id == can_id
        assert self.mock_can_packet._CanPacket__target_address == decoded_ta
        assert self.mock_can_packet._CanPacket__source_address == decoded_sa
        assert self.mock_can_packet._CanPacket__address_extension is None

    # __set_address_information_extended

    @pytest.mark.parametrize("previous_can_address_format", [CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                                             CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                             "something else"])
    @pytest.mark.parametrize("can_id", ["some ID", 0x7FF])
    @pytest.mark.parametrize("target_address", ["some target address", 0x55])
    def test_set_address_information_extended__incompatible_format(self, example_addressing_type, can_id,
                                                                   target_address, previous_can_address_format):
        self.mock_can_packet.addressing_format = previous_can_address_format
        with pytest.raises(IncompatibleCanAddressingFormatError):
            CanPacket._CanPacket__set_address_information_extended(self=self.mock_can_packet, can_id=can_id,
                                                                   target_address=target_address,
                                                                   addressing=example_addressing_type)

    @pytest.mark.parametrize("previous_can_address_format", [None, CanAddressingFormat.EXTENDED_ADDRESSING,
                                                             CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                             CanAddressingFormat.MIXED_29BIT_ADDRESSING])
    @pytest.mark.parametrize("can_id", ["some ID", 0x7FF])
    @pytest.mark.parametrize("target_address", ["some target address", 0x55])
    def test_set_address_information_extended__change(self, example_addressing_type, can_id, target_address,
                                                      previous_can_address_format):
        self.mock_can_packet.addressing_format = previous_can_address_format
        CanPacket._CanPacket__set_address_information_extended(self=self.mock_can_packet, addressing=example_addressing_type,
                                                               can_id=can_id, target_address=target_address)
        assert self.mock_can_packet._CanPacket__addressing == example_addressing_type
        assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.EXTENDED_ADDRESSING
        assert self.mock_can_packet._CanPacket__can_id == can_id
        assert self.mock_can_packet._CanPacket__target_address == target_address
        assert self.mock_can_packet._CanPacket__source_address is None
        assert self.mock_can_packet._CanPacket__address_extension is None

    # __set_address_information_mixed_11bit

    @pytest.mark.parametrize("previous_can_address_format", [CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                                             CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                             "something else"])
    @pytest.mark.parametrize("can_id", ["some ID", 0x7FF])
    @pytest.mark.parametrize("address_extension", ["some address extension", 0x55])
    def test_set_address_information_mixed_11bit__incompatible_format(self, example_addressing_type, can_id,
                                                                      address_extension, previous_can_address_format):
        self.mock_can_packet.addressing_format = previous_can_address_format
        with pytest.raises(IncompatibleCanAddressingFormatError):
            CanPacket._CanPacket__set_address_information_mixed_11bit(self=self.mock_can_packet, can_id=can_id,
                                                                      address_extension=address_extension,
                                                                      addressing=example_addressing_type)

    @pytest.mark.parametrize("previous_can_address_format", [None, CanAddressingFormat.EXTENDED_ADDRESSING,
                                                             CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                             CanAddressingFormat.MIXED_29BIT_ADDRESSING])
    @pytest.mark.parametrize("can_id", ["some ID", 0x7FF])
    @pytest.mark.parametrize("address_extension", ["some address extension", 0x55])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_mixed_11bit_addressed_can_id")
    def test_set_address_information_mixed_11bit__value_error(self, mock_is_mixed_11bit_addressed_can_id,
                                                               example_addressing_type, can_id, address_extension,
                                                               previous_can_address_format):
        self.mock_can_packet.addressing_format = previous_can_address_format
        mock_is_mixed_11bit_addressed_can_id.return_value = False
        with pytest.raises(ValueError):
            CanPacket._CanPacket__set_address_information_mixed_11bit(self=self.mock_can_packet,
                                                                      addressing=example_addressing_type,
                                                                      can_id=can_id, address_extension=address_extension)
        mock_is_mixed_11bit_addressed_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("previous_can_address_format", [None, CanAddressingFormat.EXTENDED_ADDRESSING,
                                                             CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                             CanAddressingFormat.MIXED_29BIT_ADDRESSING])
    @pytest.mark.parametrize("can_id", ["some ID", 0x7FF])
    @pytest.mark.parametrize("address_extension", ["some address extension", 0x55])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_mixed_11bit_addressed_can_id")
    def test_set_address_information_mixed_11bit__change(self, mock_is_mixed_11bit_addressed_can_id,
                                                         example_addressing_type, can_id, address_extension,
                                                         previous_can_address_format):
        self.mock_can_packet.addressing_format = previous_can_address_format
        mock_is_mixed_11bit_addressed_can_id.return_value = True
        CanPacket._CanPacket__set_address_information_mixed_11bit(self=self.mock_can_packet, addressing=example_addressing_type,
                                                                  can_id=can_id, address_extension=address_extension)
        mock_is_mixed_11bit_addressed_can_id.assert_called_once_with(can_id)
        assert self.mock_can_packet._CanPacket__addressing == example_addressing_type
        assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.MIXED_11BIT_ADDRESSING
        assert self.mock_can_packet._CanPacket__can_id == can_id
        assert self.mock_can_packet._CanPacket__target_address is None
        assert self.mock_can_packet._CanPacket__source_address is None
        assert self.mock_can_packet._CanPacket__address_extension == address_extension

    # __set_address_information_mixed_29bit

    @pytest.mark.parametrize("previous_can_address_format", [CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                                             CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                             "something else"])
    @pytest.mark.parametrize("address_extension", ["some address extension", 0x55])
    def test_set_address_information_mixed_29bit__incompatible_format(self, example_addressing_type, address_extension,
                                                                      previous_can_address_format):
        self.mock_can_packet.addressing_format = previous_can_address_format
        with pytest.raises(IncompatibleCanAddressingFormatError):
            CanPacket._CanPacket__set_address_information_mixed_29bit(self=self.mock_can_packet,
                                                                      addressing=example_addressing_type,
                                                                      address_extension=address_extension)

    @pytest.mark.parametrize("previous_can_address_format", [None, CanAddressingFormat.EXTENDED_ADDRESSING,
                                                             CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                             CanAddressingFormat.MIXED_29BIT_ADDRESSING])
    @pytest.mark.parametrize("address_extension", ["some address extension", 0x55])
    @pytest.mark.parametrize("can_id, target_address, source_address", [
        (None, None, 0x12),
        (None, 0xDF, None),
        (None, None, None),
    ])
    def test_set_address_information_mixed_29bit__inconsistent_none_values(self, example_addressing_type,
                                                                           previous_can_address_format, can_id,
                                                                           address_extension,
                                                                           target_address, source_address):
        self.mock_can_packet.addressing_format = previous_can_address_format
        with pytest.raises(InconsistentArgumentsError):
            CanPacket._CanPacket__set_address_information_mixed_29bit(self=self.mock_can_packet,
                                                                      addressing=example_addressing_type,
                                                                      address_extension=address_extension,
                                                                      can_id=can_id,
                                                                      target_address=target_address,
                                                                      source_address=source_address)

    @pytest.mark.parametrize("previous_can_address_format", [None, CanAddressingFormat.EXTENDED_ADDRESSING,
                                                             CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                             CanAddressingFormat.MIXED_29BIT_ADDRESSING])
    @pytest.mark.parametrize("address_extension", ["some address extension", 0x55])
    @pytest.mark.parametrize("addressing, decoded_addressing, can_id, ta, decoded_ta, sa, decoded_sa", [
        (AddressingType.PHYSICAL, AddressingType.FUNCTIONAL, 0x987656, None, 0x11, None, 0x12),
        (AddressingType.FUNCTIONAL, AddressingType.PHYSICAL, 0x987656, None, 0x11, None, 0x12),
        (AddressingType.PHYSICAL, AddressingType.PHYSICAL, 0x1234567, 0x81, 0x91, None, 0x88),
        (AddressingType.PHYSICAL, AddressingType.PHYSICAL, 0x1234567, None, 0x91, 0x68, 0x69),
        (AddressingType.FUNCTIONAL, AddressingType.FUNCTIONAL, 0x987656, 0xFD, 0x11, 0xEC, 0xED),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.decode_mixed_addressed_29bit_can_id")
    def test_set_address_information_mixed_29bit__inconsistent_can_id_decoded_values(self,
                                                                                     mock_decode_mixed_addressed_29bit_can_id,
                                                                                     previous_can_address_format,
                                                                                     addressing, decoded_addressing,
                                                                                     can_id, ta, decoded_ta,
                                                                                     sa, decoded_sa, address_extension):
        mock_decode_mixed_addressed_29bit_can_id.return_value = (decoded_addressing, decoded_ta, decoded_sa)
        self.mock_can_packet.addressing_format = previous_can_address_format
        with pytest.raises(InconsistentArgumentsError):
            CanPacket._CanPacket__set_address_information_mixed_29bit(self=self.mock_can_packet, addressing=addressing,
                                                                      can_id=can_id, address_extension=address_extension,
                                                                      target_address=ta, source_address=sa)

    @pytest.mark.parametrize("previous_can_address_format", [None, CanAddressingFormat.EXTENDED_ADDRESSING,
                                                             CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                             CanAddressingFormat.MIXED_29BIT_ADDRESSING])
    @pytest.mark.parametrize("address_extension", ["some address extension", 0x55])
    @pytest.mark.parametrize("addressing, target_address, source_address", [
        (AddressingType.PHYSICAL, 0x12, 0x34),
        (AddressingType.FUNCTIONAL, 0x80, 0xB1),
    ])
    @pytest.mark.parametrize("generated_can_id", [0x18CE0508, 0x7FF, 0x12345678])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.get_mixed_addressed_29bit_can_id")
    def test_set_address_information_mixed_29bit__change_without_can_id(self, mock_get_mixed_addressed_29bit_can_id,
                                                                        previous_can_address_format, addressing,
                                                                        generated_can_id, target_address,
                                                                        source_address, address_extension):
        mock_get_mixed_addressed_29bit_can_id.return_value = generated_can_id
        self.mock_can_packet.addressing_format = previous_can_address_format
        CanPacket._CanPacket__set_address_information_mixed_29bit(self=self.mock_can_packet,
                                                                  addressing=addressing,
                                                                  can_id=None,
                                                                  target_address=target_address,
                                                                  source_address=source_address,
                                                                  address_extension=address_extension)
        mock_get_mixed_addressed_29bit_can_id.assert_called_once_with(addressing_type=addressing,
                                                                      target_address=target_address,
                                                                      source_address=source_address)
        assert self.mock_can_packet._CanPacket__addressing == addressing
        assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.MIXED_29BIT_ADDRESSING
        assert self.mock_can_packet._CanPacket__can_id == generated_can_id
        assert self.mock_can_packet._CanPacket__target_address == target_address
        assert self.mock_can_packet._CanPacket__source_address == source_address
        assert self.mock_can_packet._CanPacket__address_extension == address_extension

    @pytest.mark.parametrize("previous_can_address_format", [None, CanAddressingFormat.EXTENDED_ADDRESSING,
                                                             CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                             CanAddressingFormat.MIXED_29BIT_ADDRESSING])
    @pytest.mark.parametrize("address_extension", ["some address extension", 0x55])
    @pytest.mark.parametrize("addressing, can_id, ta, decoded_ta, sa, decoded_sa", [
        (AddressingType.PHYSICAL, 0x987656, None, 0x11, None, 0x12),
        (AddressingType.FUNCTIONAL, 0x987656, None, 0x11, None, 0x12),
        (AddressingType.PHYSICAL, 0x1234567, 0x81, 0x81, None, 0x88),
        (AddressingType.PHYSICAL, 0x1234567, None, 0x91, 0x68, 0x68),
        (AddressingType.FUNCTIONAL, 0x987656, 0xFD, 0xFD, 0xEC, 0xEC),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.decode_mixed_addressed_29bit_can_id")
    def test_set_address_information_mixed_29bit__change_with_can_id(self, mock_decode_mixed_addressed_29bit_can_id,
                                                                     previous_can_address_format, addressing,
                                                                     can_id, ta, sa, decoded_ta, decoded_sa,
                                                                     address_extension):
        mock_decode_mixed_addressed_29bit_can_id.return_value = (addressing, decoded_ta, decoded_sa)
        self.mock_can_packet.addressing_format = previous_can_address_format
        CanPacket._CanPacket__set_address_information_mixed_29bit(self=self.mock_can_packet,
                                                                  addressing=addressing,
                                                                  can_id=can_id,
                                                                  target_address=ta,
                                                                  source_address=sa,
                                                                  address_extension=address_extension)
        mock_decode_mixed_addressed_29bit_can_id.assert_called_once_with(can_id=can_id)
        assert self.mock_can_packet._CanPacket__addressing == addressing
        assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.MIXED_29BIT_ADDRESSING
        assert self.mock_can_packet._CanPacket__can_id == can_id
        assert self.mock_can_packet._CanPacket__target_address == decoded_ta
        assert self.mock_can_packet._CanPacket__source_address == decoded_sa
        assert self.mock_can_packet._CanPacket__address_extension == address_extension

    # __validate_address_information

    @pytest.mark.parametrize("addressing", [None, "addressing", AddressingType.FUNCTIONAL])
    @pytest.mark.parametrize("addressing_format", [None, "addressing format", CanAddressingFormat.NORMAL_11BIT_ADDRESSING])
    def test_validate_address_information__sanity_check(self, addressing, addressing_format):
        CanPacket._CanPacket__validate_address_information(addressing=addressing, addressing_format=addressing_format,
                                                           can_id=None, target_address=None, source_address=None,
                                                           address_extension=None)
        self.mock_validate_addressing_type.assert_called_once_with(addressing)
        self.mock_validate_can_addressing_format.assert_called_once_with(addressing_format)
        self.mock_validate_can_id.assert_not_called()
        self.mock_validate_raw_byte.assert_not_called()

    @pytest.mark.parametrize("addressing", [None, "addressing"])
    @pytest.mark.parametrize("addressing_format", [None, "addressing format"])
    @pytest.mark.parametrize("can_id", [0, "some CAN ID"])
    @pytest.mark.parametrize("target_address", [0x55, "some Target Address"])
    @pytest.mark.parametrize("source_address", [0x12, "some Source Address"])
    @pytest.mark.parametrize("address_extension", [0xFE, "some Address Extension"])
    def test_validate_address_information__sanity_check_2(self, addressing, addressing_format, can_id, target_address,
                                                          source_address, address_extension):
        CanPacket._CanPacket__validate_address_information(addressing=addressing, addressing_format=addressing_format,
                                                           can_id=can_id, target_address=target_address,
                                                           source_address=source_address,
                                                           address_extension=address_extension)
        self.mock_validate_addressing_type.assert_called_once_with(addressing)
        self.mock_validate_can_addressing_format.assert_called_once_with(addressing_format)
        self.mock_validate_can_id.assert_called_once_with(can_id)
        self.mock_validate_raw_byte.assert_has_calls([call(target_address), call(source_address), call(address_extension)])

    # packet_type

    @pytest.mark.parametrize("value_stored", [AddressingType.PHYSICAL, AddressingType.FUNCTIONAL])
    def test_addressing__get(self, value_stored):
        self.mock_can_packet._CanPacket__addressing = value_stored
        assert CanPacket.addressing.fget(self=self.mock_can_packet) is value_stored

    # raw_frame_data

    @pytest.mark.parametrize("value_stored", [
        (0x02, 0x3E, 0x00),
        (0x10, 0x0A, 0x22, 0x00, 0x01, 0x00, 0x02, 0x00),
        (0x21, 0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE),
        (0x30, 0x00, 0x00, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC),
    ])
    def test_raw_frame_data__get(self, value_stored):
        self.mock_can_packet._CanPacket__raw_frame_data = value_stored
        assert CanPacket.raw_frame_data.fget(self=self.mock_can_packet) is value_stored

    # packet_type

    @pytest.mark.parametrize("value_stored", [None, CanPacketType.SINGLE_FRAME, CanPacketType.FIRST_FRAME.value])
    def test_packet_type__get(self, value_stored):
        self.mock_can_packet._CanPacket__packet_type = value_stored
        assert CanPacket.packet_type.fget(self=self.mock_can_packet) is value_stored

    # addressing_format

    @pytest.mark.parametrize("value_stored", [None, CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                              CanAddressingFormat.EXTENDED_ADDRESSING])
    def test_addressing_format__get(self, value_stored):
        self.mock_can_packet._CanPacket__addressing_format = value_stored
        assert CanPacket.addressing_format.fget(self=self.mock_can_packet) is value_stored

    # can_id

    @pytest.mark.parametrize("value_stored", [0x7FF, 0x18DA4512, 0x18CEF0E2])
    def test_can_id__get(self, value_stored):
        self.mock_can_packet._CanPacket__can_id = value_stored
        assert CanPacket.can_id.fget(self=self.mock_can_packet) is value_stored

    # target_address

    @pytest.mark.parametrize("value_stored", [None, 0, 5, 0xFF])
    def test_target_address__get(self, value_stored):
        self.mock_can_packet._CanPacket__target_address = value_stored
        assert CanPacket.target_address.fget(self=self.mock_can_packet) is value_stored

    # source_address

    @pytest.mark.parametrize("value_stored", [None, 0, 5, 0xFF])
    def test_source_address__get(self, value_stored):
        self.mock_can_packet._CanPacket__source_address = value_stored
        assert CanPacket.source_address.fget(self=self.mock_can_packet) is value_stored

    # address_extension

    @pytest.mark.parametrize("value_stored", [None, 0, 5, 0xFF])
    def test_address_extension__get(self, value_stored):
        self.mock_can_packet._CanPacket__address_extension = value_stored
        assert CanPacket.address_extension.fget(self=self.mock_can_packet) is value_stored

    # dlc

    @pytest.mark.parametrize("value_stored", [2, 4, 5, 8, 9, 0xF])
    def test_dlc__get(self, value_stored):
        self.mock_can_packet._CanPacket__dlc = value_stored
        assert CanPacket.dlc.fget(self=self.mock_can_packet) is value_stored

    # use_data_optimization

    @pytest.mark.parametrize("value_stored", [True, False])
    def test_use_data_optimization__get(self, value_stored):
        self.mock_can_packet._CanPacket__use_data_optimization = value_stored
        assert CanPacket.use_data_optimization.fget(self=self.mock_can_packet) is value_stored

    # filler_byte

    @pytest.mark.parametrize("value_stored", [True, False])
    def test_filler_byte__get(self, value_stored):
        self.mock_can_packet._CanPacket__filler_byte = value_stored
        assert CanPacket.filler_byte.fget(self=self.mock_can_packet) is value_stored


@pytest.mark.integration
class TestCanSTminIntegration:
    """Integration tests for CanSTmin class."""

    @pytest.mark.parametrize("value", [0x00, 0x01, 0x12, 0x50, 0x6D, 0x7E, 0x7F, 0xF1, 0xF4, 0xF9])
    def test_encode_and_decode(self, value):
        value_encoded = CanSTminTranslator.encode(value)
        assert CanSTminTranslator.decode(value_encoded) == value

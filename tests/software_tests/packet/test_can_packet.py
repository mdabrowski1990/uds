import pytest
from mock import patch, Mock, call

from uds.packet.can_packet import CanPacket, \
    AddressingType, CanAddressingFormat, CanPacketType, \
    InconsistentArgumentsError, UnusedArgumentError, AmbiguityError


class TestCanPacket:
    """Tests for `CanPacket` class."""

    SCRIPT_LOCATION = "uds.packet.can_packet"

    def setup(self):
        self.mock_can_packet = Mock(spec=CanPacket)
        # patching
        self._patcher_validate_addressing_type = patch(f"{self.SCRIPT_LOCATION}.AddressingType.validate_member")
        self.mock_validate_addressing_type = self._patcher_validate_addressing_type.start()
        self._patcher_validate_can_addressing_format = \
            patch(f"{self.SCRIPT_LOCATION}.CanAddressingFormat.validate_member")
        self.mock_validate_can_addressing_format = self._patcher_validate_can_addressing_format.start()
        self._patcher_get_data_bytes_used_by_can_addressing_format = \
            patch(f"{self.SCRIPT_LOCATION}.CanAddressingFormat.get_number_of_data_bytes_used")
        self.mock_get_data_bytes_used_by_can_addressing_format = \
            self._patcher_get_data_bytes_used_by_can_addressing_format.start()
        self._patcher_validate_can_packet_type = patch(f"{self.SCRIPT_LOCATION}.CanPacketType.validate_member")
        self.mock_validate_can_packet_type = self._patcher_validate_can_packet_type.start()
        self._patcher_validate_can_id = patch(f"{self.SCRIPT_LOCATION}.CanIdHandler.validate_can_id")
        self.mock_validate_can_id = self._patcher_validate_can_id.start()
        self._patcher_decode_normal_fixed_addressed_can_id = \
            patch(f"{self.SCRIPT_LOCATION}.CanIdHandler.decode_normal_fixed_addressed_can_id")
        self.mock_decode_normal_fixed_addressed_can_id = self._patcher_decode_normal_fixed_addressed_can_id.start()
        self._patcher_decode_mixed_addressed_29bit_can_id = \
            patch(f"{self.SCRIPT_LOCATION}.CanIdHandler.decode_mixed_addressed_29bit_can_id")
        self.mock_decode_mixed_addressed_29bit_can_id = self._patcher_decode_mixed_addressed_29bit_can_id.start()
        self._patcher_validate_dlc = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler.validate_dlc")
        self.mock_validate_dlc = self._patcher_validate_dlc.start()
        self._patcher_validate_raw_byte = patch(f"{self.SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()

    def teardown(self):
        self._patcher_validate_addressing_type.stop()
        self._patcher_validate_can_addressing_format.stop()
        self._patcher_get_data_bytes_used_by_can_addressing_format.stop()
        self._patcher_validate_can_packet_type.stop()
        self._patcher_validate_can_id.stop()
        self._patcher_decode_normal_fixed_addressed_can_id.stop()
        self._patcher_decode_mixed_addressed_29bit_can_id.stop()
        self._patcher_validate_dlc.stop()
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

    # raw_frame_data

    @pytest.mark.parametrize("value", [None, "some", False, 5.5])
    def test_raw_frame_data__get(self, value):
        self.mock_can_packet._CanPacket__raw_frame_data = value
        assert CanPacket.raw_frame_data.fget(self=self.mock_can_packet) == value

    # addressing

    @pytest.mark.parametrize("value", [None, "some", False, 5.5])
    def test_addressing__get(self, value):
        self.mock_can_packet._CanPacket__addressing = value
        assert CanPacket.addressing.fget(self=self.mock_can_packet) == value

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

    # address_extension

    @pytest.mark.parametrize("value", [None, "some", False, 5.5])
    def test_address_extension__get(self, value):
        self.mock_can_packet._CanPacket__address_extension = value
        assert CanPacket.address_extension.fget(self=self.mock_can_packet) == value

    # target_address

    @pytest.mark.parametrize("value", [None, "some", False, 5.5])
    def test_target_address__get(self, value):
        self.mock_can_packet._CanPacket__target_address = value
        assert CanPacket.target_address.fget(self=self.mock_can_packet) == value

    # source_address

    @pytest.mark.parametrize("address_extension", [None, "unknown", CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                   CanAddressingFormat.EXTENDED_ADDRESSING,
                                                   CanAddressingFormat.MIXED_11BIT_ADDRESSING])
    def test_source_address__get__none(self, address_extension):
        self.mock_can_packet.address_extension = address_extension
        assert CanPacket.source_address.fget(self=self.mock_can_packet) is None

    @pytest.mark.parametrize("value", [None, "some", False, 5.5])
    def test_source_address__get__normal_fixed(self, value):
        self.mock_decode_normal_fixed_addressed_can_id.return_value = ("addressing type", "target address", value)
        self.mock_can_packet.addressing_format = CanAddressingFormat.NORMAL_FIXED_ADDRESSING
        assert CanPacket.source_address.fget(self=self.mock_can_packet) is value
        self.mock_decode_normal_fixed_addressed_can_id.assert_called_once_with(self.mock_can_packet.can_id)

    @pytest.mark.parametrize("value", [None, "some", False, 5.5])
    def test_source_address__get__mixed_29bit(self, value):
        self.mock_decode_mixed_addressed_29bit_can_id.return_value = ("addressing type", "target address", value)
        self.mock_can_packet.addressing_format = CanAddressingFormat.MIXED_29BIT_ADDRESSING
        assert CanPacket.source_address.fget(self=self.mock_can_packet) is value
        self.mock_decode_mixed_addressed_29bit_can_id.assert_called_once_with(self.mock_can_packet.can_id)

    # set_address_information

    @pytest.mark.parametrize("addressing_format", [None, "unknown addressing format"])
    @pytest.mark.parametrize("addressing, can_id, target_address, source_address, address_extension", [
        ("something", "CAN ID", "TA", "SA", "AE"),
        (AddressingType.PHYSICAL, 0x754, 0x31, 0xD0, 0xE3),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingFormat")
    @patch(f"{SCRIPT_LOCATION}.AddressingType")
    def test_set_address_information__unknown_addressing_format(self, mock_addressing_type_class,
                                                                mock_can_addressing_format_class,
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
        self.mock_can_packet.validate_address_information.assert_called_once_with(addressing=addressing,
                                                                                  addressing_format=addressing_format,
                                                                                  can_id=can_id,
                                                                                  target_address=target_address,
                                                                                  source_address=source_address,
                                                                                  address_extension=address_extension)
        mock_can_addressing_format_class.assert_called_once_with(addressing_format)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                   CanAddressingFormat.NORMAL_11BIT_ADDRESSING.value])
    @pytest.mark.parametrize("addressing, addressing_instance", [
        (AddressingType.PHYSICAL, AddressingType.PHYSICAL),
        (AddressingType.PHYSICAL.value, AddressingType.PHYSICAL),
        (AddressingType.FUNCTIONAL.value, AddressingType.FUNCTIONAL),
    ])
    @pytest.mark.parametrize("can_id", [0x1234, 0x721])
    def test_set_address_information__normal_11_bit(self, addressing_format, addressing, addressing_instance, can_id):
        CanPacket.set_address_information(self=self.mock_can_packet,
                                          addressing=addressing,
                                          addressing_format=addressing_format,
                                          can_id=can_id)
        self.mock_can_packet._CanPacket__set_address_information_normal_11bit.assert_called_once_with(
            addressing=addressing_instance,
            can_id=can_id)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                                   CanAddressingFormat.NORMAL_FIXED_ADDRESSING.value])
    @pytest.mark.parametrize("addressing, addressing_instance", [
        (AddressingType.PHYSICAL, AddressingType.PHYSICAL),
        (AddressingType.PHYSICAL.value, AddressingType.PHYSICAL),
        (AddressingType.FUNCTIONAL.value, AddressingType.FUNCTIONAL),
    ])
    @pytest.mark.parametrize("can_id, target_address, source_address", [
        (0x12345, 0x65, 0xFD),
        (0xDCFE, None, None),
    ])
    def test_set_address_information__normal_fixed(self, addressing_format, addressing, addressing_instance,
                                                   can_id, target_address, source_address):
        CanPacket.set_address_information(self=self.mock_can_packet,
                                          addressing=addressing,
                                          addressing_format=addressing_format,
                                          can_id=can_id,
                                          target_address=target_address,
                                          source_address=source_address)
        self.mock_can_packet._CanPacket__set_address_information_normal_fixed.assert_called_once_with(
            addressing=addressing_instance,
            can_id=can_id,
            target_address=target_address,
            source_address=source_address)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.EXTENDED_ADDRESSING,
                                                   CanAddressingFormat.EXTENDED_ADDRESSING.value])
    @pytest.mark.parametrize("addressing, addressing_instance", [
        (AddressingType.PHYSICAL, AddressingType.PHYSICAL),
        (AddressingType.PHYSICAL.value, AddressingType.PHYSICAL),
        (AddressingType.FUNCTIONAL.value, AddressingType.FUNCTIONAL),
    ])
    @pytest.mark.parametrize("can_id, target_address", [
        (0x12345, 0x65),
        (0xDCFE, None),
    ])
    def test_set_address_information__extended(self, addressing_format, addressing, addressing_instance,
                                               can_id, target_address):
        CanPacket.set_address_information(self=self.mock_can_packet,
                                          addressing=addressing,
                                          addressing_format=addressing_format,
                                          can_id=can_id,
                                          target_address=target_address)
        self.mock_can_packet._CanPacket__set_address_information_extended.assert_called_once_with(
            addressing=addressing_instance,
            can_id=can_id,
            target_address=target_address)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                   CanAddressingFormat.MIXED_11BIT_ADDRESSING.value])
    @pytest.mark.parametrize("addressing, addressing_instance", [
        (AddressingType.PHYSICAL, AddressingType.PHYSICAL),
        (AddressingType.PHYSICAL.value, AddressingType.PHYSICAL),
        (AddressingType.FUNCTIONAL.value, AddressingType.FUNCTIONAL),
    ])
    @pytest.mark.parametrize("can_id, address_extension", [
        (0x12345, 0x65),
        (0xDCFE, None),
    ])
    def test_set_address_information__mixed_11bit(self, addressing_format, addressing, addressing_instance,
                                                  can_id, address_extension):
        CanPacket.set_address_information(self=self.mock_can_packet,
                                          addressing=addressing,
                                          addressing_format=addressing_format,
                                          can_id=can_id,
                                          address_extension=address_extension)
        self.mock_can_packet._CanPacket__set_address_information_mixed_11bit.assert_called_once_with(
            addressing=addressing_instance,
            can_id=can_id,
            address_extension=address_extension)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                                   CanAddressingFormat.MIXED_29BIT_ADDRESSING.value])
    @pytest.mark.parametrize("addressing, addressing_instance", [
        (AddressingType.PHYSICAL, AddressingType.PHYSICAL),
        (AddressingType.PHYSICAL.value, AddressingType.PHYSICAL),
        (AddressingType.FUNCTIONAL.value, AddressingType.FUNCTIONAL),
    ])
    @pytest.mark.parametrize("can_id, target_address, source_address, address_extension", [
        (0x12345, 0x65, 0xFA, 0x03),
        (0xDCFE, None, None, None),
    ])
    def test_set_address_information__mixed_29bit(self, addressing_format, addressing, addressing_instance,
                                                  can_id, target_address, source_address, address_extension):
        CanPacket.set_address_information(self=self.mock_can_packet,
                                          addressing=addressing,
                                          addressing_format=addressing_format,
                                          can_id=can_id,
                                          target_address=target_address,
                                          source_address=source_address,
                                          address_extension=address_extension)
        self.mock_can_packet._CanPacket__set_address_information_mixed_29bit.assert_called_once_with(
            addressing=addressing_instance,
            can_id=can_id,
            target_address=target_address,
            source_address=source_address,
            address_extension=address_extension)

    # validate_address_information

    @pytest.mark.parametrize("addressing", ["addressing", AddressingType.FUNCTIONAL])
    @pytest.mark.parametrize("addressing_format", ["addressing format", CanAddressingFormat.NORMAL_11BIT_ADDRESSING])
    @pytest.mark.parametrize("can_id, target_address, source_address, address_extension", [
        (0x918273, 0x8F, 0xEB, 0xA0),
        (0x881DB, 0x02, None, 0x0B),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_ai_consistency")
    def test_validate_address_information(self, mock_validate_ai_consistency, addressing, addressing_format,
                                          can_id, target_address, source_address, address_extension):
        CanPacket.validate_address_information(addressing=addressing,
                                               addressing_format=addressing_format,
                                               can_id=can_id,
                                               target_address=target_address,
                                               source_address=source_address,
                                               address_extension=address_extension)
        self.mock_validate_addressing_type.assert_called_once_with(addressing)
        self.mock_validate_can_addressing_format.assert_called_once_with(addressing_format)
        mock_validate_ai_consistency.assert_called_once_with(addressing=addressing,
                                                             addressing_format=addressing_format,
                                                             can_id=can_id,
                                                             target_address=target_address,
                                                             source_address=source_address,
                                                             address_extension=address_extension)

    # validate_data

    @pytest.mark.parametrize("dlc", [5.5, 8, "something"])
    @pytest.mark.parametrize("packet_type", [0, CanPacketType.FLOW_CONTROL, "some type"])
    @pytest.mark.parametrize("filler_byte", [0xFF, "some value"])
    @pytest.mark.parametrize("kwargs", [{}, {"a": "some a value", "b": "some b value"}])
    @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_data_consistency")
    def test_validate_data__dlc_int(self, mock_validate_data_consistency, packet_type, filler_byte, dlc, kwargs):
        CanPacket.validate_data(packet_type=packet_type,
                                dlc=dlc,
                                filler_byte=filler_byte,
                                **kwargs)
        self.mock_validate_dlc.assert_called_once_with(dlc)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        self.mock_validate_can_packet_type.assert_called_once_with(packet_type)
        mock_validate_data_consistency.assert_called_once_with(packet_type=packet_type,
                                                               dlc=dlc,
                                                               **kwargs)

    @pytest.mark.parametrize("packet_type", [0, CanPacketType.FLOW_CONTROL, "some type"])
    @pytest.mark.parametrize("filler_byte", [0xFF, "some value"])
    @pytest.mark.parametrize("kwargs", [{}, {"a": "some a value", "b": "some b value"}])
    @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_data_consistency")
    def test_validate_data__dlc_none(self, mock_validate_data_consistency, packet_type, filler_byte, kwargs):
        CanPacket.validate_data(packet_type=packet_type,
                                dlc=None,
                                filler_byte=filler_byte,
                                **kwargs)
        self.mock_validate_dlc.assert_not_called()
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        self.mock_validate_can_packet_type.assert_called_once_with(packet_type)
        mock_validate_data_consistency.assert_called_once_with(packet_type=packet_type,
                                                               dlc=None,
                                                               **kwargs)

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
            CanPacket._CanPacket__validate_ai_consistency(addressing=addressing,
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
    @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_ai_consistency_normal_11bit")
    def test_validate_ai_consistency__normal_11bit(self, mock_validate_ai_consistency_normal_11bit,
                                                   addressing_format, example_addressing_type, can_id,
                                                   target_address, source_address, address_extension):
        CanPacket._CanPacket__validate_ai_consistency(addressing=example_addressing_type,
                                                      addressing_format=addressing_format,
                                                      can_id=can_id,
                                                      target_address=target_address,
                                                      source_address=source_address,
                                                      address_extension=address_extension)
        mock_validate_ai_consistency_normal_11bit.assert_called_once_with(can_id=can_id,
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
    @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_ai_consistency_normal_fixed")
    def test_validate_ai_consistency__normal_fixed(self, mock_validate_ai_consistency_normal_fixed,
                                                   addressing_format, example_addressing_type, can_id,
                                                   target_address, source_address, address_extension):
        CanPacket._CanPacket__validate_ai_consistency(addressing=example_addressing_type,
                                                      addressing_format=addressing_format,
                                                      can_id=can_id,
                                                      target_address=target_address,
                                                      source_address=source_address,
                                                      address_extension=address_extension)
        mock_validate_ai_consistency_normal_fixed.assert_called_once_with(addressing=example_addressing_type,
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
    @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_ai_consistency_extended")
    def test_validate_ai_consistency__extended(self, mock_validate_ai_consistency_extended,
                                               addressing_format, example_addressing_type, can_id,
                                               target_address, source_address, address_extension):
        CanPacket._CanPacket__validate_ai_consistency(addressing=example_addressing_type,
                                                      addressing_format=addressing_format,
                                                      can_id=can_id,
                                                      target_address=target_address,
                                                      source_address=source_address,
                                                      address_extension=address_extension)
        mock_validate_ai_consistency_extended.assert_called_once_with(can_id=can_id,
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
    @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_ai_consistency_mixed_11bit")
    def test_validate_ai_consistency__mixed_11bit(self, mock_validate_ai_consistency_mixed_11bit,
                                                  addressing_format, example_addressing_type, can_id,
                                                  target_address, source_address, address_extension):
        CanPacket._CanPacket__validate_ai_consistency(addressing=example_addressing_type,
                                                      addressing_format=addressing_format,
                                                      can_id=can_id,
                                                      target_address=target_address,
                                                      source_address=source_address,
                                                      address_extension=address_extension)
        mock_validate_ai_consistency_mixed_11bit.assert_called_once_with(can_id=can_id,
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
    @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_ai_consistency_mixed_29bit")
    def test_validate_ai_consistency__mixed_29bit(self, mock_validate_ai_consistency_mixed_29bit,
                                                  addressing_format, example_addressing_type, can_id,
                                                  target_address, source_address, address_extension):
        CanPacket._CanPacket__validate_ai_consistency(addressing=example_addressing_type,
                                                      addressing_format=addressing_format,
                                                      can_id=can_id,
                                                      target_address=target_address,
                                                      source_address=source_address,
                                                      address_extension=address_extension)
        mock_validate_ai_consistency_mixed_29bit.assert_called_once_with(addressing=example_addressing_type,
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
            CanPacket._CanPacket__validate_ai_consistency_normal_11bit(can_id=can_id,
                                                                       target_address=target_address,
                                                                       source_address=source_address,
                                                                       address_extension=address_extension)

    @pytest.mark.parametrize("can_id", [0x1234, 0x98FA])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_11bit_addressed_can_id")
    def test_validate_ai_consistency_normal_11bit__invalid_can_id(self, mock_is_normal_11bit_addressed_can_id, can_id):
        mock_is_normal_11bit_addressed_can_id.return_value = False
        with pytest.raises(InconsistentArgumentsError):
            CanPacket._CanPacket__validate_ai_consistency_normal_11bit(can_id=can_id,
                                                                       target_address=None,
                                                                       source_address=None,
                                                                       address_extension=None)

    @pytest.mark.parametrize("can_id", [0x1234, 0x98FA])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_11bit_addressed_can_id")
    def test_validate_ai_consistency_normal_11bit__valid(self, mock_is_normal_11bit_addressed_can_id, can_id):
        mock_is_normal_11bit_addressed_can_id.return_value = True
        CanPacket._CanPacket__validate_ai_consistency_normal_11bit(can_id=can_id,
                                                                   target_address=None,
                                                                   source_address=None,
                                                                   address_extension=None)

    # __validate_ai_consistency_normal_fixed

    @pytest.mark.parametrize("can_id, target_address, source_address", [
        (0xABCDEF, None, None),
        (None, 0x12, 0x98),
    ])
    @pytest.mark.parametrize("address_extension", [0x00, 0x55, 0xFF])
    def test_validate_ai_consistency_normal_fixed__unused_args(self, example_addressing_type,
                                                               can_id, target_address, source_address,
                                                               address_extension):
        with pytest.raises(UnusedArgumentError):
            CanPacket._CanPacket__validate_ai_consistency_normal_fixed(addressing=example_addressing_type,
                                                                       can_id=can_id,
                                                                       target_address=target_address,
                                                                       source_address=source_address,
                                                                       address_extension=address_extension)

    @pytest.mark.parametrize("can_id, target_address, source_address", [
        (0xABCDEF, 0x09, None),
        (0x727384, None, 0xB1),
        (0xABCDEF, 0x9E, 0xFD),
    ])
    def test_validate_ai_consistency_normal_fixed__redundant_args(self, example_addressing_type,
                                                                  can_id, target_address, source_address):
        with pytest.raises(InconsistentArgumentsError):
            CanPacket._CanPacket__validate_ai_consistency_normal_fixed(addressing=example_addressing_type,
                                                                       can_id=can_id,
                                                                       target_address=target_address,
                                                                       source_address=source_address,
                                                                       address_extension=None)

    @pytest.mark.parametrize("can_id, target_address, source_address", [
        (None, 0x09, None),
        (None, None, 0xB1),
        (None, None, None),
    ])
    def test_validate_ai_consistency_normal_fixed__missing_args(self, example_addressing_type,
                                                                can_id, target_address, source_address):
        with pytest.raises(InconsistentArgumentsError):
            CanPacket._CanPacket__validate_ai_consistency_normal_fixed(addressing=example_addressing_type,
                                                                       can_id=can_id,
                                                                       target_address=target_address,
                                                                       source_address=source_address,
                                                                       address_extension=None)

    @pytest.mark.parametrize("target_address", [0x00, 0x55, 0xFF])
    @pytest.mark.parametrize("source_address", [0x00, 0xAA, 0xFF])
    def test_validate_ai_consistency_normal_fixed__byte_params_validation(self, example_addressing_type,
                                                                          target_address, source_address):
        CanPacket._CanPacket__validate_ai_consistency_normal_fixed(addressing=example_addressing_type,
                                                                   can_id=None,
                                                                   target_address=target_address,
                                                                   source_address=source_address,
                                                                   address_extension=None)
        self.mock_validate_raw_byte.assert_has_calls([call(target_address), call(source_address)])

    @pytest.mark.parametrize("can_id", [0, "some CAN ID", 0x12343])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_fixed_addressed_can_id")
    def test_validate_ai_consistency_normal_fixed__invalid_can_id(self, mock_is_normal_fixed_addressed_can_id,
                                                                  example_addressing_type, can_id):
        mock_is_normal_fixed_addressed_can_id.return_value = False
        with pytest.raises(InconsistentArgumentsError):
            CanPacket._CanPacket__validate_ai_consistency_normal_fixed(addressing=example_addressing_type,
                                                                       can_id=can_id,
                                                                       target_address=None,
                                                                       source_address=None,
                                                                       address_extension=None)
        self.mock_validate_can_id.assert_called_once_with(can_id)
        mock_is_normal_fixed_addressed_can_id.assert_called_once_with(can_id=can_id,
                                                                      addressing=example_addressing_type)

    @pytest.mark.parametrize("can_id", [0, "some CAN ID", 0x12343])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_fixed_addressed_can_id")
    def test_validate_ai_consistency_normal_fixed__valid(self, mock_is_normal_fixed_addressed_can_id,
                                                         example_addressing_type, can_id):
        mock_is_normal_fixed_addressed_can_id.return_value = True
        CanPacket._CanPacket__validate_ai_consistency_normal_fixed(addressing=example_addressing_type,
                                                                   can_id=can_id,
                                                                   target_address=None,
                                                                   source_address=None,
                                                                   address_extension=None)
        self.mock_validate_can_id.assert_called_once_with(can_id)
        mock_is_normal_fixed_addressed_can_id.assert_called_once_with(can_id=can_id,
                                                                      addressing=example_addressing_type)

    # __validate_ai_consistency_extended

    @pytest.mark.parametrize("can_id, target_address", [
        (0x8572, 0x1B),
        (0xF09B, 0xC5),
    ])
    @pytest.mark.parametrize("source_address, address_extension", [
        (0x01, None),
        (None, 0xFC),
        (0x0F, 0x7A),
    ])
    def test_validate_ai_consistency_extended__unused_args(self, can_id, target_address,
                                                           source_address, address_extension):
        with pytest.raises(UnusedArgumentError):
            CanPacket._CanPacket__validate_ai_consistency_extended(can_id=can_id,
                                                                   target_address=target_address,
                                                                   source_address=source_address,
                                                                   address_extension=address_extension)

    @pytest.mark.parametrize("can_id", [0x0, 0x7A2, 0x19FAB3])
    @pytest.mark.parametrize("target_address", [0x00, 0x8F, 0xFF])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_extended_addressed_can_id")
    def test_validate_ai_consistency_extended__invalid_can_id(self, mock_is_extended_addressed_can_id,
                                                              can_id, target_address):
        mock_is_extended_addressed_can_id.return_value = False
        with pytest.raises(InconsistentArgumentsError):
            CanPacket._CanPacket__validate_ai_consistency_extended(can_id=can_id,
                                                                   target_address=target_address,
                                                                   source_address=None,
                                                                   address_extension=None)
        self.mock_validate_can_id.assert_called_once_with(can_id)
        mock_is_extended_addressed_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("can_id", [0x0, 0x7A2, 0x19FAB3])
    @pytest.mark.parametrize("target_address", [0x00, 0x8F, 0xFF])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_extended_addressed_can_id")
    def test_validate_ai_consistency_extended__valid(self, mock_is_extended_addressed_can_id, can_id, target_address):
        mock_is_extended_addressed_can_id.return_value = True
        CanPacket._CanPacket__validate_ai_consistency_extended(can_id=can_id,
                                                               target_address=target_address,
                                                               source_address=None,
                                                               address_extension=None)
        self.mock_validate_can_id.assert_called_once_with(can_id)
        mock_is_extended_addressed_can_id.assert_called_once_with(can_id)
        self.mock_validate_raw_byte.assert_called_once_with(target_address)

    # __validate_ai_consistency_mixed_11bit

    @pytest.mark.parametrize("can_id, address_extension", [
        (0x8572, 0x1B),
        (0xF09B, 0xC5),
    ])
    @pytest.mark.parametrize("target_address, source_address", [
        (0x01, None),
        (None, 0xFC),
        (0x0F, 0x7A),
    ])
    def test_validate_ai_consistency_mixed_11bit__unused_args(self, can_id, target_address,
                                                              source_address, address_extension):
        with pytest.raises(UnusedArgumentError):
            CanPacket._CanPacket__validate_ai_consistency_mixed_11bit(can_id=can_id,
                                                                      target_address=target_address,
                                                                      source_address=source_address,
                                                                      address_extension=address_extension)

    @pytest.mark.parametrize("can_id", [0x0, 0x7A2, 0x19FAB3])
    @pytest.mark.parametrize("address_extension", [0x00, 0x8F, 0xFF])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_mixed_11bit_addressed_can_id")
    def test_validate_ai_consistency_mixed_11bit__invalid_can_id(self, mock_is_mixed_11bit_addressed_can_id,
                                                                 can_id, address_extension):
        mock_is_mixed_11bit_addressed_can_id.return_value = False
        with pytest.raises(InconsistentArgumentsError):
            CanPacket._CanPacket__validate_ai_consistency_mixed_11bit(can_id=can_id,
                                                                      target_address=None,
                                                                      source_address=None,
                                                                      address_extension=address_extension)
        self.mock_validate_can_id.assert_called_once_with(can_id)
        mock_is_mixed_11bit_addressed_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("can_id", [0x0, 0x7A2, 0x19FAB3])
    @pytest.mark.parametrize("address_extension", [0x00, 0x8F, 0xFF])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_mixed_11bit_addressed_can_id")
    def test_validate_ai_consistency_mixed_11bit__valid(self, mock_is_mixed_11bit_addressed_can_id,
                                                        can_id, address_extension):
        mock_is_mixed_11bit_addressed_can_id.return_value = True
        CanPacket._CanPacket__validate_ai_consistency_mixed_11bit(can_id=can_id,
                                                                  target_address=None,
                                                                  source_address=None,
                                                                  address_extension=address_extension)
        self.mock_validate_can_id.assert_called_once_with(can_id)
        mock_is_mixed_11bit_addressed_can_id.assert_called_once_with(can_id)
        self.mock_validate_raw_byte.assert_called_once_with(address_extension)

    # __validate_ai_consistency_mixed_29bit

    @pytest.mark.parametrize("can_id, target_address, source_address", [
        (0xABCDEF, 0x09, None),
        (0x727384, None, 0xB1),
        (0xABCDEF, 0x9E, 0xFD),
    ])
    @pytest.mark.parametrize("address_extension", [0x00, 0x8F, 0xFF])
    def test_validate_ai_consistency_mixed_29bit__redundant_args(self, example_addressing_type, address_extension,
                                                                 can_id, target_address, source_address):
        with pytest.raises(InconsistentArgumentsError):
            CanPacket._CanPacket__validate_ai_consistency_mixed_29bit(addressing=example_addressing_type,
                                                                      can_id=can_id,
                                                                      target_address=target_address,
                                                                      source_address=source_address,
                                                                      address_extension=address_extension)

    @pytest.mark.parametrize("address_extension", [0x00, 0xFF])
    @pytest.mark.parametrize("can_id, target_address, source_address", [
        (None, None, None),
        (None, None, 0x2F),
        (None, 0xBA, None),
    ])
    def test_validate_ai_consistency_mixed_29bit__missing_can_id_args(self, example_addressing_type, address_extension,
                                                                      can_id, target_address, source_address):
        with pytest.raises(InconsistentArgumentsError):
            CanPacket._CanPacket__validate_ai_consistency_mixed_29bit(addressing=example_addressing_type,
                                                                      can_id=can_id,
                                                                      target_address=target_address,
                                                                      source_address=source_address,
                                                                      address_extension=address_extension)

    @pytest.mark.parametrize("target_address", [0x55, 0x82])
    @pytest.mark.parametrize("source_address", [0x0B, 0xAA])
    @pytest.mark.parametrize("address_extension", [0xB3, 0xE7])
    def test_validate_ai_consistency_mixed_29bit__byte_params_validation(self, example_addressing_type,
                                                                         address_extension,
                                                                         target_address, source_address):
        CanPacket._CanPacket__validate_ai_consistency_mixed_29bit(addressing=example_addressing_type,
                                                                  can_id=None,
                                                                  target_address=target_address,
                                                                  source_address=source_address,
                                                                  address_extension=address_extension)
        self.mock_validate_raw_byte.assert_has_calls([call(address_extension),
                                                      call(target_address),
                                                      call(source_address)],
                                                     any_order=True)

    @pytest.mark.parametrize("can_id", [0, "some CAN ID", 0x12343])
    @pytest.mark.parametrize("address_extension", [0xB3, 0xE7])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_mixed_29bit_addressed_can_id")
    def test_validate_ai_consistency_mixed_29bit__invalid_can_id(self, mock_is_mixed_29bit_addressed_can_id,
                                                                 example_addressing_type, can_id, address_extension):
        mock_is_mixed_29bit_addressed_can_id.return_value = False
        with pytest.raises(InconsistentArgumentsError):
            CanPacket._CanPacket__validate_ai_consistency_mixed_29bit(addressing=example_addressing_type,
                                                                      can_id=can_id,
                                                                      target_address=None,
                                                                      source_address=None,
                                                                      address_extension=address_extension)
        self.mock_validate_can_id.assert_called_once_with(can_id)
        mock_is_mixed_29bit_addressed_can_id.assert_called_once_with(can_id=can_id,
                                                                     addressing=example_addressing_type)

    @pytest.mark.parametrize("can_id", [0, "some CAN ID", 0x12343])
    @pytest.mark.parametrize("address_extension", [0xB3, 0xE7])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_mixed_29bit_addressed_can_id")
    def test_validate_ai_consistency_mixed_29bit__valid(self, mock_is_mixed_29bit_addressed_can_id,
                                                        example_addressing_type, can_id, address_extension):
        mock_is_mixed_29bit_addressed_can_id.return_value = True
        CanPacket._CanPacket__validate_ai_consistency_mixed_29bit(addressing=example_addressing_type,
                                                                  can_id=can_id,
                                                                  target_address=None,
                                                                  source_address=None,
                                                                  address_extension=address_extension)
        self.mock_validate_can_id.assert_called_once_with(can_id)
        mock_is_mixed_29bit_addressed_can_id.assert_called_once_with(can_id=can_id,
                                                                     addressing=example_addressing_type)

    # __validate_unambiguous_ai_change

    @pytest.mark.parametrize("new_addressing_format", list(CanAddressingFormat))
    def test_validate_unambiguous_ai_change__none(self, new_addressing_format):
        self.mock_can_packet.addressing_format = None
        CanPacket._CanPacket__validate_unambiguous_ai_change(self=self.mock_can_packet,
                                                             addressing_format=new_addressing_format)
        self.mock_get_data_bytes_used_by_can_addressing_format.assert_not_called()

    @pytest.mark.parametrize("data_bytes_used", [0, 1])
    @pytest.mark.parametrize("new_addressing_format", ["value 1", "value 2"])
    @pytest.mark.parametrize("old_addressing_format", ["other 1", "other 2"])
    def test_validate_unambiguous_ai_change__compatible(self, new_addressing_format, old_addressing_format,
                                                        data_bytes_used):
        self.mock_can_packet.addressing_format = old_addressing_format
        self.mock_get_data_bytes_used_by_can_addressing_format.return_value = data_bytes_used
        CanPacket._CanPacket__validate_unambiguous_ai_change(self=self.mock_can_packet,
                                                             addressing_format=new_addressing_format)
        self.mock_get_data_bytes_used_by_can_addressing_format.assert_has_calls(
            [call(new_addressing_format), call(old_addressing_format)], any_order=True)

    @pytest.mark.parametrize("data_bytes_used", [(0, 1), (1, 0)])
    @pytest.mark.parametrize("new_addressing_format", ["value 1", "value 2"])
    @pytest.mark.parametrize("old_addressing_format", ["other 1", "other 2"])
    def test_validate_unambiguous_ai_change__incompatible(self, new_addressing_format, old_addressing_format,
                                                          data_bytes_used):
        self.mock_can_packet.addressing_format = old_addressing_format
        self.mock_get_data_bytes_used_by_can_addressing_format.side_effect = data_bytes_used
        with pytest.raises(AmbiguityError):
            CanPacket._CanPacket__validate_unambiguous_ai_change(self=self.mock_can_packet,
                                                                 addressing_format=new_addressing_format)
        self.mock_get_data_bytes_used_by_can_addressing_format.assert_has_calls(
            [call(new_addressing_format), call(old_addressing_format)], any_order=True)

    # __validate_data_consistency

    @pytest.mark.parametrize("packet_type", [None, "unknown packet type"])
    @pytest.mark.parametrize("dlc", [None, 8])
    @pytest.mark.parametrize("kwargs", [{}, {"a": "some a value", "b": "some b value"}])
    @patch(f"{SCRIPT_LOCATION}.CanPacketType")
    def test_validate_data_consistency__unknown_packet_type(self, mock_packet_type, packet_type, dlc, kwargs):
        mock_packet_type.return_value = packet_type
        with pytest.raises(NotImplementedError):
            CanPacket._CanPacket__validate_data_consistency(packet_type=packet_type,
                                                            dlc=dlc,
                                                            **kwargs)
        mock_packet_type.assert_called_once_with(packet_type)

    @pytest.mark.parametrize("packet_type", [CanPacketType.SINGLE_FRAME, CanPacketType.SINGLE_FRAME.value])
    @pytest.mark.parametrize("dlc", [None, 8])
    @pytest.mark.parametrize("kwargs", [{}, {"a": "some a value", "b": "some b value"}])
    @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_data_single_frame")
    def test_validate_data_consistency__single_frame(self, mock_validate_data_single_frame, packet_type, dlc, kwargs):
        with pytest.raises(NotImplementedError):
            CanPacket._CanPacket__validate_data_consistency(packet_type=packet_type,
                                                            dlc=dlc,
                                                            **kwargs)
        mock_validate_data_single_frame.assert_called_once_with(dlc=dlc,
                                                                **kwargs)

    @pytest.mark.parametrize("packet_type", [CanPacketType.FIRST_FRAME, CanPacketType.FIRST_FRAME.value])
    @pytest.mark.parametrize("dlc", [None, 8])
    @pytest.mark.parametrize("kwargs", [{}, {"a": "some a value", "b": "some b value"}])
    @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_data_first_frame")
    def test_validate_data_consistency__first_frame(self, mock_validate_data_first_frame, packet_type, dlc, kwargs):
        with pytest.raises(NotImplementedError):
            CanPacket._CanPacket__validate_data_consistency(packet_type=packet_type,
                                                            dlc=dlc,
                                                            **kwargs)
        mock_validate_data_first_frame.assert_called_once_with(dlc=dlc,
                                                               **kwargs)

    @pytest.mark.parametrize("packet_type", [CanPacketType.CONSECUTIVE_FRAME, CanPacketType.CONSECUTIVE_FRAME.value])
    @pytest.mark.parametrize("dlc", [None, 8])
    @pytest.mark.parametrize("kwargs", [{}, {"a": "some a value", "b": "some b value"}])
    @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_data_consecutive_frame")
    def test_validate_data_consistency__consecutive_frame(self, mock_validate_data_consecutive_frame, packet_type, dlc,
                                                          kwargs):
        with pytest.raises(NotImplementedError):
            CanPacket._CanPacket__validate_data_consistency(packet_type=packet_type,
                                                            dlc=dlc,
                                                            **kwargs)
        mock_validate_data_consecutive_frame.assert_called_once_with(dlc=dlc,
                                                                     **kwargs)

    @pytest.mark.parametrize("packet_type", [CanPacketType.FLOW_CONTROL, CanPacketType.FLOW_CONTROL.value])
    @pytest.mark.parametrize("dlc", [None, 8])
    @pytest.mark.parametrize("kwargs", [{}, {"a": "some a value", "b": "some b value"}])
    @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_data_flow_control")
    def test_validate_data_consistency__flow_control(self, mock_validate_data_flow_control, packet_type, dlc,
                                                     kwargs):
        with pytest.raises(NotImplementedError):
            CanPacket._CanPacket__validate_data_consistency(packet_type=packet_type,
                                                            dlc=dlc,
                                                            **kwargs)
        mock_validate_data_flow_control.assert_called_once_with(dlc=dlc,
                                                                **kwargs)

    # __set_address_information_normal_11bit

    @pytest.mark.parametrize("can_id", ["some CAN ID", 0x64A])
    def test_set_address_information_normal_11bit(self, example_addressing_type, can_id):
        CanPacket._CanPacket__set_address_information_normal_11bit(self=self.mock_can_packet,
                                                                   addressing=example_addressing_type,
                                                                   can_id=can_id)
        self.mock_can_packet._CanPacket__validate_unambiguous_ai_change.assert_called_once_with(
            CanAddressingFormat.NORMAL_11BIT_ADDRESSING)
        assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.NORMAL_11BIT_ADDRESSING
        assert self.mock_can_packet._CanPacket__addressing == example_addressing_type
        assert self.mock_can_packet._CanPacket__can_id == can_id
        assert self.mock_can_packet._CanPacket__target_address is None
        assert self.mock_can_packet._CanPacket__address_extension is None

    # __set_address_information_normal_fixed

    @pytest.mark.parametrize("can_id", ["some CAN ID", 0x64A])
    @pytest.mark.parametrize("decoded_target_address", ["value 1", "value 2"])
    def test_set_address_information_normal_11bit__can_id(self, example_addressing_type, can_id,
                                                          decoded_target_address):
        self.mock_decode_normal_fixed_addressed_can_id.return_value = (example_addressing_type, decoded_target_address,
                                                                       "some source adddress")
        CanPacket._CanPacket__set_address_information_normal_fixed(self=self.mock_can_packet,
                                                                   addressing=example_addressing_type,
                                                                   can_id=can_id)
        self.mock_can_packet._CanPacket__validate_unambiguous_ai_change.assert_called_once_with(
            CanAddressingFormat.NORMAL_FIXED_ADDRESSING)
        assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.NORMAL_FIXED_ADDRESSING
        assert self.mock_can_packet._CanPacket__addressing == example_addressing_type
        assert self.mock_can_packet._CanPacket__can_id == can_id
        assert self.mock_can_packet._CanPacket__target_address == decoded_target_address
        assert self.mock_can_packet._CanPacket__address_extension is None
        self.mock_decode_normal_fixed_addressed_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("can_id", ["some CAN ID", 0x64A])
    @pytest.mark.parametrize("target_address, source_address", [
        ("v1", "v2"),
        (0x82, 0xF2),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.get_normal_fixed_addressed_can_id")
    def test_set_address_information_normal_11bit__ta_sa(self, mock_get_normal_fixed_addressed_can_id,
                                                         example_addressing_type, can_id,
                                                         target_address, source_address):
        mock_get_normal_fixed_addressed_can_id.return_value = can_id
        CanPacket._CanPacket__set_address_information_normal_fixed(self=self.mock_can_packet,
                                                                   addressing=example_addressing_type,
                                                                   can_id=None,
                                                                   target_address=target_address,
                                                                   source_address=source_address)
        self.mock_can_packet._CanPacket__validate_unambiguous_ai_change.assert_called_once_with(
            CanAddressingFormat.NORMAL_FIXED_ADDRESSING)
        assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.NORMAL_FIXED_ADDRESSING
        assert self.mock_can_packet._CanPacket__addressing == example_addressing_type
        assert self.mock_can_packet._CanPacket__can_id == can_id
        assert self.mock_can_packet._CanPacket__target_address == target_address
        assert self.mock_can_packet._CanPacket__address_extension is None
        mock_get_normal_fixed_addressed_can_id.assert_called_once_with(addressing_type=example_addressing_type,
                                                                       target_address=target_address,
                                                                       source_address=source_address)

    # __set_address_information_extended

    @pytest.mark.parametrize("can_id", ["some CAN ID", 0x64A])
    @pytest.mark.parametrize("target_address", ["value 1", "value 2"])
    def test_set_address_information_extended(self, example_addressing_type, can_id, target_address):
        CanPacket._CanPacket__set_address_information_extended(self=self.mock_can_packet,
                                                               addressing=example_addressing_type,
                                                               can_id=can_id,
                                                               target_address=target_address)
        self.mock_can_packet._CanPacket__validate_unambiguous_ai_change.assert_called_once_with(
            CanAddressingFormat.EXTENDED_ADDRESSING)
        assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.EXTENDED_ADDRESSING
        assert self.mock_can_packet._CanPacket__addressing == example_addressing_type
        assert self.mock_can_packet._CanPacket__can_id == can_id
        assert self.mock_can_packet._CanPacket__target_address == target_address
        assert self.mock_can_packet._CanPacket__address_extension is None

    # __set_address_information_mixed_11bit

    @pytest.mark.parametrize("can_id", ["some CAN ID", 0x64A])
    @pytest.mark.parametrize("address_extension", ["value 1", "value 2"])
    def test_set_address_information_mixed_11bit(self, example_addressing_type, can_id, address_extension):
        CanPacket._CanPacket__set_address_information_mixed_11bit(self=self.mock_can_packet,
                                                                  addressing=example_addressing_type,
                                                                  can_id=can_id,
                                                                  address_extension=address_extension)
        self.mock_can_packet._CanPacket__validate_unambiguous_ai_change.assert_called_once_with(
            CanAddressingFormat.MIXED_11BIT_ADDRESSING)
        assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.MIXED_11BIT_ADDRESSING
        assert self.mock_can_packet._CanPacket__addressing == example_addressing_type
        assert self.mock_can_packet._CanPacket__can_id == can_id
        assert self.mock_can_packet._CanPacket__target_address is None
        assert self.mock_can_packet._CanPacket__address_extension == address_extension

    # __set_address_information_mixed_29bit

    @pytest.mark.parametrize("can_id", ["some CAN ID", 0x64A])
    @pytest.mark.parametrize("decoded_target_address", ["value 1", "value 2"])
    @pytest.mark.parametrize("address_extension", [0x21, 0x90])
    def test_set_address_information_mixed_29bit__can_id(self, example_addressing_type, can_id, address_extension,
                                                         decoded_target_address):
        self.mock_decode_mixed_addressed_29bit_can_id.return_value = (example_addressing_type, decoded_target_address,
                                                                      "some source adddress")
        CanPacket._CanPacket__set_address_information_mixed_29bit(self=self.mock_can_packet,
                                                                  addressing=example_addressing_type,
                                                                  address_extension=address_extension,
                                                                  can_id=can_id)
        self.mock_can_packet._CanPacket__validate_unambiguous_ai_change.assert_called_once_with(
            CanAddressingFormat.MIXED_29BIT_ADDRESSING)
        assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.MIXED_29BIT_ADDRESSING
        assert self.mock_can_packet._CanPacket__addressing == example_addressing_type
        assert self.mock_can_packet._CanPacket__can_id == can_id
        assert self.mock_can_packet._CanPacket__target_address == decoded_target_address
        assert self.mock_can_packet._CanPacket__address_extension == address_extension
        self.mock_decode_mixed_addressed_29bit_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("can_id", ["some CAN ID", 0x64A])
    @pytest.mark.parametrize("target_address, source_address", [
        ("v1", "v2"),
        (0x82, 0xF2),
    ])
    @pytest.mark.parametrize("address_extension", [0x21, 0x90])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.get_mixed_addressed_29bit_can_id")
    def test_set_address_information_mixed_29bit__ta_sa(self, mock_get_mixed_addressed_29bit_can_id,
                                                        example_addressing_type, can_id,
                                                        target_address, source_address, address_extension):
        mock_get_mixed_addressed_29bit_can_id.return_value = can_id
        CanPacket._CanPacket__set_address_information_mixed_29bit(self=self.mock_can_packet,
                                                                  addressing=example_addressing_type,
                                                                  can_id=None,
                                                                  target_address=target_address,
                                                                  source_address=source_address,
                                                                  address_extension=address_extension)
        self.mock_can_packet._CanPacket__validate_unambiguous_ai_change.assert_called_once_with(
            CanAddressingFormat.MIXED_29BIT_ADDRESSING)
        assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.MIXED_29BIT_ADDRESSING
        assert self.mock_can_packet._CanPacket__addressing == example_addressing_type
        assert self.mock_can_packet._CanPacket__can_id == can_id
        assert self.mock_can_packet._CanPacket__target_address == target_address
        assert self.mock_can_packet._CanPacket__address_extension == address_extension
        mock_get_mixed_addressed_29bit_can_id.assert_called_once_with(addressing_type=example_addressing_type,
                                                                      target_address=target_address,
                                                                      source_address=source_address)

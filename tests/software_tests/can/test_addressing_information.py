import pytest
from mock import patch, MagicMock, Mock

from uds.can.addressing_information import CanAddressingInformation, \
    CanAddressingFormat, InconsistentArgumentsError, UnusedArgumentError, AbstractCanAddressingInformation


class TestCanAddressingInformation:
    """Unit tests for `CanAddressingInformation` class."""

    SCRIPT_LOCATION = "uds.can.addressing_information"

    def setup(self):
        # patching
        self._patcher_can_id_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanIdHandler")
        self.mock_can_id_handler_class = self._patcher_can_id_handler_class.start()
        self._patcher_validate_addressing_format = patch(f"{self.SCRIPT_LOCATION}.CanAddressingFormat.validate_member")
        self.mock_validate_addressing_format = self._patcher_validate_addressing_format.start()
        self._patcher_normal_11bit_ai_class = patch(f"{self.SCRIPT_LOCATION}.Normal11BitCanAddressingInformation")
        self.mock_normal_11bit_ai_class = self._patcher_normal_11bit_ai_class.start()
        self._patcher_normal_fixed_ai_class = patch(f"{self.SCRIPT_LOCATION}.NormalFixedCanAddressingInformation")
        self.mock_normal_fixed_ai_class = self._patcher_normal_fixed_ai_class.start()
        self._patcher_extended_ai_class = patch(f"{self.SCRIPT_LOCATION}.ExtendedCanAddressingInformation")
        self.mock_extended_ai_class = self._patcher_extended_ai_class.start()
        self._patcher_mixed_11bit_ai_class = patch(f"{self.SCRIPT_LOCATION}.Mixed11BitCanAddressingInformation")
        self.mock_mixed_11bit_ai_class = self._patcher_mixed_11bit_ai_class.start()
        self._patcher_mixed_29bit_ai_class = patch(f"{self.SCRIPT_LOCATION}.Mixed29BitCanAddressingInformation")
        self.mock_mixed_29bit_ai_class = self._patcher_mixed_29bit_ai_class.start()
        self._patcher_validate_raw_bytes = patch(f"{self.SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
        self._patcher_validate_raw_byte = patch(f"{self.SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()

    def teardown(self):
        self._patcher_can_id_handler_class.stop()
        self._patcher_validate_addressing_format.stop()
        self._patcher_normal_11bit_ai_class.stop()
        self._patcher_normal_fixed_ai_class.stop()
        self._patcher_extended_ai_class.stop()
        self._patcher_mixed_11bit_ai_class.stop()
        self._patcher_mixed_29bit_ai_class.stop()
        self._patcher_validate_raw_bytes.stop()
        self._patcher_validate_raw_byte.stop()

    # __new__

    @pytest.mark.parametrize("addressing_format", ["addressing_format", Mock()])
    @pytest.mark.parametrize("rx_physical, tx_physical, rx_functional, tx_functional", [
        ("rx_physical", "tx_physical", "rx_functional", "tx_functional"),
        (1, 2, 3, 4),
    ])
    def test_new(self, addressing_format, rx_physical, tx_physical, rx_functional, tx_functional):
        mock_returned_class = Mock()
        mock_getitem = Mock(return_value=mock_returned_class)
        mock_cls = Mock(ADDRESSING_INFORMATION_MAPPING=MagicMock(__getitem__=mock_getitem))
        assert CanAddressingInformation.__new__(cls=mock_cls,
                                                addressing_format=addressing_format,
                                                rx_physical=rx_physical,
                                                tx_physical=tx_physical,
                                                rx_functional=rx_functional,
                                                tx_functional=tx_functional) == mock_returned_class.return_value
        mock_getitem.assert_called_once_with(addressing_format)
        mock_returned_class.assert_called_once_with(rx_physical=rx_physical,
                                                    tx_physical=tx_physical,
                                                    rx_functional=rx_functional,
                                                    tx_functional=tx_functional)

    # validate_packet_ai

    @pytest.mark.parametrize("addressing_format", [None, "unknown addressing format"])
    @pytest.mark.parametrize("addressing_type, can_id, target_address, source_address, address_extension", [
        ("some addressing", "some CAN ID", "TA", "SA", "AE"),
        (Mock(), 0x8213, 0x9A, 0x0B, 0xF1),
    ])
    def test_validate_packet_ai__unknown_addressing_format(self, addressing_format, addressing_type, can_id,
                                                           target_address, source_address, address_extension):
        with pytest.raises(NotImplementedError):
            CanAddressingInformation.validate_packet_ai(addressing_format=addressing_format,
                                                        addressing_type=addressing_type,
                                                        can_id=can_id,
                                                        target_address=target_address,
                                                        source_address=source_address,
                                                        address_extension=address_extension)
        self.mock_validate_addressing_format.assert_called_once_with(addressing_format)

    @pytest.mark.parametrize("addressing_type, can_id", [
        ("some addressing", "some CAN ID"),
        (Mock(), 0x8213),
    ])
    def test_validate_packet_ai__normal_11bit__valid(self, addressing_type, can_id):
        CanAddressingInformation.validate_packet_ai(addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                    addressing_type=addressing_type,
                                                    can_id=can_id)
        self.mock_normal_11bit_ai_class.validate_packet_ai.assert_called_once_with(addressing_type=addressing_type,
                                                                                   can_id=can_id)

    @pytest.mark.parametrize("addressing_type, can_id, target_address, source_address, address_extension", [
        ("some addressing", "some CAN ID", "TA", "SA", "AE"),
        ("some addressing", "some CAN ID", "TA", None, None),
        (Mock(), 0x8213, None, None, 0xF1),
    ])
    def test_validate_packet_ai__normal_11bit__invalid(self, addressing_type, can_id,
                                                       target_address, source_address, address_extension):
        with pytest.raises(UnusedArgumentError):
            CanAddressingInformation.validate_packet_ai(addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                        addressing_type=addressing_type,
                                                        can_id=can_id,
                                                        target_address=target_address,
                                                        source_address=source_address,
                                                        address_extension=address_extension)
        self.mock_normal_11bit_ai_class.assert_not_called()

    @pytest.mark.parametrize("addressing_type, can_id, target_address, source_address", [
        ("some addressing", "some CAN ID", "TA", "SA"),
        (Mock(), 0x8213, 0x9A, 0x0B),
    ])
    def test_validate_packet_ai__normal_fixed__valid(self, addressing_type, can_id, target_address, source_address):
        CanAddressingInformation.validate_packet_ai(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                                    addressing_type=addressing_type,
                                                    can_id=can_id,
                                                    target_address=target_address,
                                                    source_address=source_address)
        self.mock_normal_fixed_ai_class.validate_packet_ai.assert_called_once_with(addressing_type=addressing_type,
                                                                                   can_id=can_id,
                                                                                   target_address=target_address,
                                                                                   source_address=source_address)

    @pytest.mark.parametrize("addressing_type, can_id, target_address, source_address", [
        ("some addressing", "some CAN ID", "TA", "SA"),
        (Mock(), 0x8213, 0x9A, 0x0B),
    ])
    @pytest.mark.parametrize("address_extension", ["AE", 0x9B, 1])
    def test_validate_packet_ai__normal_fixed__invalid(self, addressing_type, can_id,
                                                       target_address, source_address, address_extension):
        with pytest.raises(UnusedArgumentError):
            CanAddressingInformation.validate_packet_ai(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                                        addressing_type=addressing_type,
                                                        can_id=can_id,
                                                        target_address=target_address,
                                                        source_address=source_address,
                                                        address_extension=address_extension)
        self.mock_normal_fixed_ai_class.validate_packet_ai.assert_not_called()

    @pytest.mark.parametrize("addressing_type, can_id, target_address", [
        ("some addressing", "some CAN ID", "TA"),
        (Mock(), 0x8213, 0x9A),
    ])
    def test_validate_packet_ai__extended__valid(self, addressing_type, can_id, target_address):
        CanAddressingInformation.validate_packet_ai(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                                    addressing_type=addressing_type,
                                                    can_id=can_id,
                                                    target_address=target_address)
        self.mock_extended_ai_class.validate_packet_ai.assert_called_once_with(addressing_type=addressing_type,
                                                                               can_id=can_id,
                                                                               target_address=target_address)

    @pytest.mark.parametrize("addressing_type, can_id, target_address", [
        ("some addressing", "some CAN ID", "TA"),
        (Mock(), 0x8213, 0x9A),
    ])
    @pytest.mark.parametrize("source_address, address_extension", [
        ("SA", "AE"),
        ("SA", None),
        (None, "AE"),
        (0x0B, 0xF1),
    ])
    def test_validate_packet_ai__extended__invalid(self, addressing_type, can_id,
                                                   target_address, source_address, address_extension):
        with pytest.raises(UnusedArgumentError):
            CanAddressingInformation.validate_packet_ai(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                                        addressing_type=addressing_type,
                                                        can_id=can_id,
                                                        target_address=target_address,
                                                        source_address=source_address,
                                                        address_extension=address_extension)
        self.mock_extended_ai_class.validate_packet_ai.assert_not_called()

    @pytest.mark.parametrize("addressing_type, can_id, address_extension", [
        ("some addressing", "some CAN ID", "AE"),
        (Mock(), 0x8213, 0xF1),
    ])
    def test_validate_packet_ai__mixed_11bit__valid(self, addressing_type, can_id, address_extension):
        CanAddressingInformation.validate_packet_ai(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                    addressing_type=addressing_type,
                                                    can_id=can_id,
                                                    address_extension=address_extension)
        self.mock_mixed_11bit_ai_class.validate_packet_ai.assert_called_once_with(addressing_type=addressing_type,
                                                                                  can_id=can_id,
                                                                                  address_extension=address_extension)

    @pytest.mark.parametrize("addressing_type, can_id, address_extension", [
        ("some addressing", "some CAN ID", "AE"),
        (Mock(), 0x8213, 0xF1),
    ])
    @pytest.mark.parametrize("target_address, source_address", [
        ("TA", "SA"),
        ("TA", None),
        (None, "SA"),
        (0x0B, 0xF1),
    ])
    def test_validate_packet_ai__mixed_11bit__invalid(self, addressing_type, can_id,
                                                      target_address, source_address, address_extension):
        with pytest.raises(UnusedArgumentError):
            CanAddressingInformation.validate_packet_ai(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                        addressing_type=addressing_type,
                                                        can_id=can_id,
                                                        target_address=target_address,
                                                        source_address=source_address,
                                                        address_extension=address_extension)
        self.mock_mixed_11bit_ai_class.validate_packet_ai.assert_not_called()

    @pytest.mark.parametrize("addressing_type, can_id, target_address, source_address, address_extension", [
        ("some addressing", "some CAN ID", "TA", "SA", "AE"),
        (0, None, None, None, None),
        (Mock(), 0x8213, 0x9A, 0x0B, 0xF1),
    ])
    def test_validate_packet_ai__mixed_29bit(self, addressing_type, can_id,
                                             target_address, source_address, address_extension):
        CanAddressingInformation.validate_packet_ai(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                                    addressing_type=addressing_type,
                                                    can_id=can_id,
                                                    target_address=target_address,
                                                    source_address=source_address,
                                                    address_extension=address_extension)
        self.mock_mixed_29bit_ai_class.validate_packet_ai.assert_called_once_with(addressing_type=addressing_type,
                                                                                  can_id=can_id,
                                                                                  target_address=target_address,
                                                                                  source_address=source_address,
                                                                                  address_extension=address_extension)

    # validate_ai_data_bytes

    @pytest.mark.parametrize("addressing_format", ["Addressing Format", Mock()])
    @pytest.mark.parametrize("ai_data_bytes", [[], (0x12,), [0x9A, 0xD3]])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.get_ai_data_bytes_number")
    def test_validate_ai_data_bytes__invalid(self, mock_get_ai_data_bytes_number, addressing_format, ai_data_bytes):
        mock_get_ai_data_bytes_number.return_value = MagicMock(__eq__=Mock(return_value=False))
        with pytest.raises(InconsistentArgumentsError):
            CanAddressingInformation.validate_ai_data_bytes(addressing_format=addressing_format,
                                                            ai_data_bytes=ai_data_bytes)
        self.mock_validate_addressing_format.assert_called_once_with(addressing_format)
        self.mock_validate_raw_bytes.assert_called_once_with(ai_data_bytes, allow_empty=True)
        mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    @pytest.mark.parametrize("addressing_format", ["Addressing Format", Mock()])
    @pytest.mark.parametrize("ai_data_bytes", [[], (0x12,), [0x9A, 0xD3]])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.get_ai_data_bytes_number")
    def test_validate_ai_data_bytes__valid(self, mock_get_ai_data_bytes_number, addressing_format, ai_data_bytes):
        mock_get_ai_data_bytes_number.return_value = len(ai_data_bytes)
        CanAddressingInformation.validate_ai_data_bytes(addressing_format=addressing_format,
                                                        ai_data_bytes=ai_data_bytes)
        self.mock_validate_addressing_format.assert_called_once_with(addressing_format)
        self.mock_validate_raw_bytes.assert_called_once_with(ai_data_bytes, allow_empty=True)
        mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    # decode_packet_ai

    @pytest.mark.parametrize("addressing_format, can_id, ai_data_bytes", [
        ("Some Format", "CAN ID", "soem AI Data Bytes"),
        ("Another Format", 0x78D, []),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.decode_ai_data_bytes")
    def test_decode_ai(self, mock_decode_ai_data_bytes, addressing_format, can_id, ai_data_bytes):
        ai_values = CanAddressingInformation.decode_packet_ai(addressing_format=addressing_format,
                                                              can_id=can_id,
                                                              ai_data_bytes=ai_data_bytes)
        assert isinstance(ai_values, dict)
        assert set(ai_values.keys()) == {AbstractCanAddressingInformation.ADDRESSING_TYPE_NAME,
                                         AbstractCanAddressingInformation.TARGET_ADDRESS_NAME,
                                         AbstractCanAddressingInformation.SOURCE_ADDRESS_NAME,
                                         AbstractCanAddressingInformation.ADDRESS_EXTENSION_NAME}
        self.mock_can_id_handler_class.decode_can_id.assert_called_once_with(addressing_format=addressing_format,
                                                                             can_id=can_id)
        mock_decode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                          ai_data_bytes=ai_data_bytes)

    # decode_ai_data_bytes

    @pytest.mark.parametrize("addressing_format", [None, "unknown addressing format"])
    @pytest.mark.parametrize("ai_data_bytes", [[], (0xFF,)])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.validate_ai_data_bytes")
    def test_decode_ai_data_bytes__not_implemented(self, mock_validate_ai_data_bytes, addressing_format,
                                                   ai_data_bytes):
        with pytest.raises(NotImplementedError):
            CanAddressingInformation.decode_ai_data_bytes(addressing_format=addressing_format,
                                                          ai_data_bytes=ai_data_bytes)
        mock_validate_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                            ai_data_bytes=ai_data_bytes)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                   CanAddressingFormat.NORMAL_FIXED_ADDRESSING])
    @pytest.mark.parametrize("ai_data_bytes", [[], (0xCF,)])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.validate_ai_data_bytes")
    def test_decode_ai_data_bytes__normal(self, mock_validate_ai_data_bytes, addressing_format, ai_data_bytes):
        decoded_values = CanAddressingInformation.decode_ai_data_bytes(addressing_format=addressing_format,
                                                                       ai_data_bytes=ai_data_bytes)
        assert isinstance(decoded_values, dict)
        assert set(decoded_values.keys()) == {AbstractCanAddressingInformation.ADDRESS_EXTENSION_NAME,
                                              AbstractCanAddressingInformation.TARGET_ADDRESS_NAME}
        assert decoded_values[AbstractCanAddressingInformation.TARGET_ADDRESS_NAME] is None
        assert decoded_values[AbstractCanAddressingInformation.ADDRESS_EXTENSION_NAME] is None
        mock_validate_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                            ai_data_bytes=ai_data_bytes)

    @pytest.mark.parametrize("ai_data_bytes", [[0x0A], (0xCF,)])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.validate_ai_data_bytes")
    def test_decode_ai_data_bytes__extended(self, mock_validate_ai_data_bytes, ai_data_bytes):
        decoded_values = CanAddressingInformation.decode_ai_data_bytes(
            addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING, ai_data_bytes=ai_data_bytes)
        assert isinstance(decoded_values, dict)
        assert set(decoded_values.keys()) == {AbstractCanAddressingInformation.ADDRESS_EXTENSION_NAME,
                                              AbstractCanAddressingInformation.TARGET_ADDRESS_NAME}
        assert decoded_values[AbstractCanAddressingInformation.TARGET_ADDRESS_NAME] == ai_data_bytes[0]
        assert decoded_values[AbstractCanAddressingInformation.ADDRESS_EXTENSION_NAME] is None
        mock_validate_ai_data_bytes.assert_called_once_with(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                                            ai_data_bytes=ai_data_bytes)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                   CanAddressingFormat.MIXED_29BIT_ADDRESSING])
    @pytest.mark.parametrize("ai_data_bytes", [[0x0A], (0xCF,)])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.validate_ai_data_bytes")
    def test_decode_ai_data_bytes__mixed(self, mock_validate_ai_data_bytes, addressing_format, ai_data_bytes):
        decoded_values = CanAddressingInformation.decode_ai_data_bytes(addressing_format=addressing_format,
                                                                       ai_data_bytes=ai_data_bytes)
        assert isinstance(decoded_values, dict)
        assert set(decoded_values.keys()) == {AbstractCanAddressingInformation.ADDRESS_EXTENSION_NAME,
                                              AbstractCanAddressingInformation.TARGET_ADDRESS_NAME}
        assert decoded_values[AbstractCanAddressingInformation.TARGET_ADDRESS_NAME] is None
        assert decoded_values[AbstractCanAddressingInformation.ADDRESS_EXTENSION_NAME] == ai_data_bytes[0]
        mock_validate_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                            ai_data_bytes=ai_data_bytes)

    # encode_ai_data_bytes

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                   CanAddressingFormat.NORMAL_FIXED_ADDRESSING])
    @pytest.mark.parametrize("target_address, address_extension", [
        (None, None),
        (0x5B, 0x9E),
    ])
    def test_encode_ai_data_bytes__normal(self, addressing_format, target_address, address_extension):
        assert CanAddressingInformation.encode_ai_data_bytes(addressing_format=addressing_format,
                                                             address_extension=address_extension,
                                                             target_address=target_address) == []
        self.mock_validate_addressing_format.assert_called_once_with(addressing_format)
        self.mock_validate_raw_byte.assert_not_called()

    @pytest.mark.parametrize("target_address, address_extension", [
        (None, None),
        (0x5B, 0x9E),
    ])
    def test_encode_ai_data_bytes__extended(self, target_address, address_extension):
        assert CanAddressingInformation.encode_ai_data_bytes(
            addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
            address_extension=address_extension,
            target_address=target_address) == [target_address]
        self.mock_validate_addressing_format.assert_called_once_with(CanAddressingFormat.EXTENDED_ADDRESSING)
        self.mock_validate_raw_byte.assert_called_once_with(target_address)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                   CanAddressingFormat.MIXED_29BIT_ADDRESSING])
    @pytest.mark.parametrize("target_address, address_extension", [
        (None, None),
        (0x5B, 0x9E),
    ])
    def test_encode_ai_data_bytes__mixed(self, addressing_format, target_address, address_extension):
        assert CanAddressingInformation.encode_ai_data_bytes(
            addressing_format=addressing_format,
            address_extension=address_extension,
            target_address=target_address) == [address_extension]
        self.mock_validate_addressing_format.assert_called_once_with(addressing_format)
        self.mock_validate_raw_byte.assert_called_once_with(address_extension)

    @pytest.mark.parametrize("addressing_format", [None, "something else"])
    @pytest.mark.parametrize("target_address, address_extension", [
        (None, None),
        (0x5B, 0x9E),
    ])
    def test_encode_ai_data_bytes__unknown(self, addressing_format, target_address, address_extension):
        with pytest.raises(NotImplementedError):
            CanAddressingInformation.encode_ai_data_bytes(addressing_format=addressing_format,
                                                          address_extension=address_extension,
                                                          target_address=target_address)
        self.mock_validate_addressing_format.assert_called_once_with(addressing_format)
        self.mock_validate_raw_byte.assert_not_called()

    # get_ai_data_bytes_number

    @pytest.mark.parametrize("addressing_format", ["some addressing", Mock()])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.ADDRESSING_INFORMATION_MAPPING")
    def test_get_ai_data_bytes_number(self, mock_ai_mapping, addressing_format):
        assert CanAddressingInformation.get_ai_data_bytes_number(addressing_format=addressing_format) \
               == mock_ai_mapping.__getitem__.return_value.AI_DATA_BYTES_NUMBER
        mock_ai_mapping.__getitem__.assert_called_once_with(addressing_format)

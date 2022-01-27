import pytest
from mock import patch, MagicMock, Mock

from uds.can.addressing_information import CanAddressingInformation, \
    CanAddressingFormat, InconsistentArgumentsError, AbstractCanAddressingInformation
from uds.transmission_attributes import AddressingType


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
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.ADDRESSING_INFORMATION_MAPPING")
    def test_validate_packet_ai(self, mock_ai_mapping, addressing_format,
                                addressing_type, can_id, target_address, source_address, address_extension):
        mock_returned_class = Mock()
        mock_getitem = Mock(return_value=mock_returned_class)
        mock_ai_mapping.__getitem__ = mock_getitem
        assert CanAddressingInformation.validate_packet_ai(addressing_format=addressing_format,
                                                           addressing_type=addressing_type,
                                                           can_id=can_id,
                                                           target_address=target_address,
                                                           source_address=source_address,
                                                           address_extension=address_extension) \
               == mock_returned_class.validate_packet_ai.return_value
        mock_getitem.assert_called_once_with(addressing_format)
        mock_returned_class.validate_packet_ai.assert_called_once_with(addressing_type=addressing_type,
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
        assert CanAddressingInformation.decode_ai_data_bytes(addressing_format=addressing_format,
                                                             ai_data_bytes=ai_data_bytes) == {}
        mock_validate_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                            ai_data_bytes=ai_data_bytes)

    @pytest.mark.parametrize("ai_data_bytes", [[0x0A], (0xCF,)])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.validate_ai_data_bytes")
    def test_decode_ai_data_bytes__extended(self, mock_validate_ai_data_bytes, ai_data_bytes):
        assert CanAddressingInformation.decode_ai_data_bytes(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                                             ai_data_bytes=ai_data_bytes) == {
            AbstractCanAddressingInformation.TARGET_ADDRESS_NAME: ai_data_bytes[0]
        }
        mock_validate_ai_data_bytes.assert_called_once_with(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                                            ai_data_bytes=ai_data_bytes)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                   CanAddressingFormat.MIXED_29BIT_ADDRESSING])
    @pytest.mark.parametrize("ai_data_bytes", [[0x0A], (0xCF,)])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.validate_ai_data_bytes")
    def test_decode_ai_data_bytes__mixed(self, mock_validate_ai_data_bytes, addressing_format, ai_data_bytes):
        assert CanAddressingInformation.decode_ai_data_bytes(addressing_format=addressing_format,
                                                             ai_data_bytes=ai_data_bytes) == {
            AbstractCanAddressingInformation.ADDRESS_EXTENSION_NAME: ai_data_bytes[0]
        }
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


class TestCanAddressingInformationIntegration:
    """Integration tests for `CanAddressingInformation` class."""

    @pytest.mark.parametrize("input_params, expected_attributes", [
        ({"addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
          "rx_physical": {"can_id": 0x601},
          "tx_physical": {"can_id": 0x602},
          "rx_functional": {"can_id": 0x6FE},
          "tx_functional": {"can_id": 0x6FF}},
         {"rx_packets_physical_ai": {"addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                     "addressing_type": AddressingType.PHYSICAL,
                                     "can_id": 0x601},
          "tx_packets_physical_ai": {"addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                     "addressing_type": AddressingType.PHYSICAL,
                                     "can_id": 0x602},
          "rx_packets_functional_ai": {"addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                       "addressing_type": AddressingType.FUNCTIONAL,
                                       "can_id": 0x6FE},
          "tx_packets_functional_ai": {"addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                       "addressing_type": AddressingType.FUNCTIONAL,
                                       "can_id": 0x6FF}}),
        ({"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "rx_physical": {"can_id": 0x18DA0E2B},
          "tx_physical": {"target_address": 0x2B, "source_address": 0x0E},
          "rx_functional": {"can_id": 0x18DBFEDC, "target_address": 0xFE},
          "tx_functional": {"can_id": 0x18DBFD92, "target_address": 0xFD, "source_address": 0x92}},
         {"rx_packets_physical_ai": {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                     "addressing_type": AddressingType.PHYSICAL,
                                     "can_id": 0x18DA0E2B,
                                     "target_address": 0x0E,
                                     "source_address": 0x2B},
          "tx_packets_physical_ai": {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                     "addressing_type": AddressingType.PHYSICAL,
                                     "can_id": 0x18DA2B0E,
                                     "target_address": 0x2B,
                                     "source_address": 0x0E},
          "rx_packets_functional_ai": {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                       "addressing_type": AddressingType.FUNCTIONAL,
                                       "can_id": 0x18DBFEDC,
                                       "target_address": 0xFE,
                                       "source_address": 0xDC},
          "tx_packets_functional_ai": {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                       "addressing_type": AddressingType.FUNCTIONAL,
                                       "can_id": 0x18DBFD92,
                                       "target_address": 0xFD,
                                       "source_address": 0x92}}),
        ({"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "rx_physical": {"can_id": 0x621, "target_address": 0x1F},
          "tx_physical": {"can_id": 0x621, "target_address": 0x91},
          "rx_functional": {"can_id": 0x12345, "target_address": 0x82},
          "tx_functional": {"can_id": 0x12346, "target_address": 0x83}},
         {"rx_packets_physical_ai": {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
                                     "addressing_type": AddressingType.PHYSICAL,
                                     "can_id": 0x621,
                                     "target_address": 0x1F},
          "tx_packets_physical_ai": {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
                                     "addressing_type": AddressingType.PHYSICAL,
                                     "can_id": 0x621,
                                     "target_address": 0x91},
          "rx_packets_functional_ai": {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
                                       "addressing_type": AddressingType.FUNCTIONAL,
                                       "can_id": 0x12345,
                                       "target_address": 0x82},
          "tx_packets_functional_ai": {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
                                       "addressing_type": AddressingType.FUNCTIONAL,
                                       "can_id": 0x12346,
                                       "target_address": 0x83}}),
        ({"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
          "rx_physical": {"can_id": 0x641, "address_extension": 0x00},
          "tx_physical": {"can_id": 0x642, "address_extension": 0xFF},
          "rx_functional": {"can_id": 0x6DE, "address_extension": 0xFE},
          "tx_functional": {"can_id": 0x6DF, "address_extension": 0xFF}},
         {"rx_packets_physical_ai": {"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                     "addressing_type": AddressingType.PHYSICAL,
                                     "can_id": 0x641,
                                     "address_extension": 0x00},
          "tx_packets_physical_ai": {"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                     "addressing_type": AddressingType.PHYSICAL,
                                     "can_id": 0x642,
                                     "address_extension": 0xFF},
          "rx_packets_functional_ai": {"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                       "addressing_type": AddressingType.FUNCTIONAL,
                                       "can_id": 0x6DE,
                                       "address_extension": 0xFE},
          "tx_packets_functional_ai": {"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                       "addressing_type": AddressingType.FUNCTIONAL,
                                       "can_id": 0x6DF,
                                       "address_extension": 0xFF}}),
        ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "rx_physical": {"can_id": 0x18CE1234, "target_address": 0x12, "source_address": 0x34, "address_extension": 0x00},
          "tx_physical": {"can_id": 0x18CEFF0F, "target_address": 0xFF, "address_extension": 0x5E},
          "rx_functional": {"can_id": 0x18CDFF00, "address_extension": 0xFE},
          "tx_functional": {"target_address": 0x09, "source_address": 0x23, "address_extension": 0xFF}},
         {"rx_packets_physical_ai": {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                     "addressing_type": AddressingType.PHYSICAL,
                                     "can_id": 0x18CE1234,
                                     "target_address": 0x12,
                                     "source_address": 0x34,
                                     "address_extension": 0x00},
          "tx_packets_physical_ai": {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                     "addressing_type": AddressingType.PHYSICAL,
                                     "can_id": 0x18CEFF0F,
                                     "target_address": 0xFF,
                                     "source_address": 0x0F,
                                     "address_extension": 0x5E},
          "rx_packets_functional_ai": {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                       "addressing_type": AddressingType.FUNCTIONAL,
                                       "can_id": 0x18CDFF00,
                                       "target_address": 0xFF,
                                       "source_address": 0x00,
                                       "address_extension": 0xFE},
          "tx_packets_functional_ai": {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                       "addressing_type": AddressingType.FUNCTIONAL,
                                       "can_id": 0x18CD0923,
                                       "target_address": 0x09,
                                       "source_address": 0x23,
                                       "address_extension": 0xFF}}),
    ])
    def test_new(self, input_params, expected_attributes):
        ai = CanAddressingInformation(**input_params)
        for attr_name, attr_value in expected_attributes.items():
            assert getattr(ai, attr_name) == attr_value

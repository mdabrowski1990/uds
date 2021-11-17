import pytest
from mock import patch, call, MagicMock, Mock

from uds.can.addressing_information import CanAddressingInformationHandler, \
    CanAddressingFormat, AddressingType, InconsistentArgumentsError, UnusedArgumentError


class TestCanAddressingInformationHandler:
    """Unit tests for `CanAddressingInformationHandler` class."""

    SCRIPT_LOCATION = "uds.can.addressing_information"

    def setup(self):
        self._patcher_validate_addressing_format = patch(f"{self.SCRIPT_LOCATION}.CanAddressingFormat.validate_member")
        self.mock_validate_addressing_format = self._patcher_validate_addressing_format.start()
        self._patcher_validate_addressing_type = patch(f"{self.SCRIPT_LOCATION}.AddressingType.validate_member")
        self.mock_validate_addressing_type = self._patcher_validate_addressing_type.start()
        self._patcher_can_id_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanIdHandler")
        self.mock_can_id_handler_class = self._patcher_can_id_handler_class.start()
        self._patcher_validate_raw_byte = patch(f"{self.SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
        self._patcher_validate_raw_bytes = patch(f"{self.SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()

    def teardown(self):
        self._patcher_validate_addressing_format.stop()
        self._patcher_validate_addressing_type.stop()
        self._patcher_can_id_handler_class.stop()
        self._patcher_validate_raw_byte.stop()
        self._patcher_validate_raw_bytes.stop()

    # decode_ai

    @pytest.mark.parametrize("addressing_format, can_id, ai_data_bytes", [
        ("Some Format", "CAN ID", "soem AI Data Bytes"),
        ("Another Format", 0x78D, []),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformationHandler.decode_ai_data_bytes")
    def test_decode_ai(self, mock_decode_ai_data_bytes, addressing_format, can_id, ai_data_bytes):
        ai_values = CanAddressingInformationHandler.decode_ai(addressing_format=addressing_format,
                                                              can_id=can_id,
                                                              ai_data_bytes=ai_data_bytes)
        assert isinstance(ai_values, dict)
        assert set(ai_values.keys()) == {CanAddressingInformationHandler.ADDRESSING_TYPE_NAME,
                                         CanAddressingInformationHandler.TARGET_ADDRESS_NAME,
                                         CanAddressingInformationHandler.SOURCE_ADDRESS_NAME,
                                         CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME}
        self.mock_can_id_handler_class.decode_can_id.assert_called_once_with(addressing_format=addressing_format,
                                                                             can_id=can_id)
        mock_decode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                          ai_data_bytes=ai_data_bytes)

    # decode_ai_data_bytes

    @pytest.mark.parametrize("addressing_format", [None, "unknown addressing format"])
    @pytest.mark.parametrize("ai_data_bytes", [[], (0xFF,)])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformationHandler.validate_ai_data_bytes")
    def test_decode_ai_data_bytes__not_implemented(self, mock_validate_ai_data_bytes, addressing_format,
                                                   ai_data_bytes):
        with pytest.raises(NotImplementedError):
            CanAddressingInformationHandler.decode_ai_data_bytes(addressing_format=addressing_format,
                                                                 ai_data_bytes=ai_data_bytes)
        mock_validate_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                            ai_data_bytes=ai_data_bytes)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                   CanAddressingFormat.NORMAL_FIXED_ADDRESSING])
    @pytest.mark.parametrize("ai_data_bytes", [[], (0xCF,)])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformationHandler.validate_ai_data_bytes")
    def test_decode_ai_data_bytes__normal(self, mock_validate_ai_data_bytes, addressing_format, ai_data_bytes):
        decoded_values = CanAddressingInformationHandler.decode_ai_data_bytes(addressing_format=addressing_format,
                                                                              ai_data_bytes=ai_data_bytes)
        assert isinstance(decoded_values, dict)
        assert set(decoded_values.keys()) == {CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME,
                                              CanAddressingInformationHandler.TARGET_ADDRESS_NAME}
        assert decoded_values[CanAddressingInformationHandler.TARGET_ADDRESS_NAME] is None
        assert decoded_values[CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME] is None
        mock_validate_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                            ai_data_bytes=ai_data_bytes)

    @pytest.mark.parametrize("ai_data_bytes", [[0x0A], (0xCF,)])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformationHandler.validate_ai_data_bytes")
    def test_decode_ai_data_bytes__extended(self, mock_validate_ai_data_bytes, ai_data_bytes):
        decoded_values = CanAddressingInformationHandler.decode_ai_data_bytes(
            addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING, ai_data_bytes=ai_data_bytes)
        assert isinstance(decoded_values, dict)
        assert set(decoded_values.keys()) == {CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME,
                                              CanAddressingInformationHandler.TARGET_ADDRESS_NAME}
        assert decoded_values[CanAddressingInformationHandler.TARGET_ADDRESS_NAME] == ai_data_bytes[0]
        assert decoded_values[CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME] is None
        mock_validate_ai_data_bytes.assert_called_once_with(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                                            ai_data_bytes=ai_data_bytes)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                   CanAddressingFormat.MIXED_29BIT_ADDRESSING])
    @pytest.mark.parametrize("ai_data_bytes", [[0x0A], (0xCF,)])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformationHandler.validate_ai_data_bytes")
    def test_decode_ai_data_bytes__mixed(self, mock_validate_ai_data_bytes, addressing_format, ai_data_bytes):
        decoded_values = CanAddressingInformationHandler.decode_ai_data_bytes(addressing_format=addressing_format,
                                                                              ai_data_bytes=ai_data_bytes)
        assert isinstance(decoded_values, dict)
        assert set(decoded_values.keys()) == {CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME,
                                              CanAddressingInformationHandler.TARGET_ADDRESS_NAME}
        assert decoded_values[CanAddressingInformationHandler.TARGET_ADDRESS_NAME] is None
        assert decoded_values[CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME] == ai_data_bytes[0]
        mock_validate_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                            ai_data_bytes=ai_data_bytes)

    # encode_ai_data_bytes

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                   CanAddressingFormat.NORMAL_FIXED_ADDRESSING])
    @pytest.mark.parametrize("target_address, address_extension", [
        (None, None),
        (0x5B, 0x9E),
    ])
    def test_generate_ai_data_bytes__normal(self, addressing_format, target_address, address_extension):
        assert CanAddressingInformationHandler.encode_ai_data_bytes(addressing_format=addressing_format,
                                                                    address_extension=address_extension,
                                                                    target_address=target_address) == []
        self.mock_validate_addressing_format.assert_called_once_with(addressing_format)
        self.mock_validate_raw_byte.assert_not_called()

    @pytest.mark.parametrize("target_address, address_extension", [
        (None, None),
        (0x5B, 0x9E),
    ])
    def test_generate_ai_data_bytes__extended(self, target_address, address_extension):
        assert CanAddressingInformationHandler.encode_ai_data_bytes(
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
    def test_generate_ai_data_bytes__mixed(self, addressing_format, target_address, address_extension):
        assert CanAddressingInformationHandler.encode_ai_data_bytes(
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
    def test_generate_ai_data_bytes__unknown(self, addressing_format, target_address, address_extension):
        with pytest.raises(NotImplementedError):
            CanAddressingInformationHandler.encode_ai_data_bytes(addressing_format=addressing_format,
                                                                 address_extension=address_extension,
                                                                 target_address=target_address)
        self.mock_validate_addressing_format.assert_called_once_with(addressing_format)
        self.mock_validate_raw_byte.assert_not_called()

    # get_ai_data_bytes_number

    def test_get_ai_data_bytes_number(self, example_can_addressing_format):
        value = CanAddressingInformationHandler.get_ai_data_bytes_number(example_can_addressing_format)
        assert isinstance(value, int)
        assert value >= 0
        self.mock_validate_addressing_format.assert_called_once_with(example_can_addressing_format)

    # validate_ai

    @pytest.mark.parametrize("addressing_format", [None, "unknown addressing format"])
    @pytest.mark.parametrize("addressing_type, can_id, target_address, source_address, address_extension", [
        ("some addressing", "some CAN ID", "TA", "SA", "AE"),
        (AddressingType.PHYSICAL, 0x8213, 0x9A, 0x0B, 0xF1),
    ])
    def test_validate_ai__unknown_addressing_format(self, addressing_format, addressing_type, can_id,
                                                    target_address, source_address, address_extension):
        with pytest.raises(NotImplementedError):
            CanAddressingInformationHandler.validate_ai(addressing_format=addressing_format,
                                                        addressing_type=addressing_type,
                                                        can_id=can_id,
                                                        target_address=target_address,
                                                        source_address=source_address,
                                                        address_extension=address_extension)
        self.mock_validate_addressing_format.assert_called_once_with(addressing_format)

    @pytest.mark.parametrize("addressing_type, can_id", [
        ("some addressing", "some CAN ID"),
        (AddressingType.PHYSICAL, 0x8213),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformationHandler.validate_ai_normal_11bit")
    def test_validate_ai__normal_11bit__valid(self, mock_validate_ai_normal_11bit,
                                              addressing_type, can_id):
        CanAddressingInformationHandler.validate_ai(addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                    addressing_type=addressing_type,
                                                    can_id=can_id)
        mock_validate_ai_normal_11bit.assert_called_once_with(addressing_type=addressing_type,
                                                              can_id=can_id)

    @pytest.mark.parametrize("addressing_type, can_id, target_address, source_address, address_extension", [
        ("some addressing", "some CAN ID", "TA", "SA", "AE"),
        ("some addressing", "some CAN ID", "TA", None, None),
        (AddressingType.PHYSICAL, 0x8213, None, None, 0xF1),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformationHandler.validate_ai_normal_11bit")
    def test_validate_ai__normal_11bit__invalid(self, mock_validate_ai_normal_11bit,
                                                addressing_type, can_id,
                                                target_address, source_address, address_extension):
        with pytest.raises(UnusedArgumentError):
            CanAddressingInformationHandler.validate_ai(addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                        addressing_type=addressing_type,
                                                        can_id=can_id,
                                                        target_address=target_address,
                                                        source_address=source_address,
                                                        address_extension=address_extension)
        mock_validate_ai_normal_11bit.assert_not_called()

    @pytest.mark.parametrize("addressing_type, can_id, target_address, source_address", [
        ("some addressing", "some CAN ID", "TA", "SA"),
        (AddressingType.PHYSICAL, 0x8213, 0x9A, 0x0B),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformationHandler.validate_ai_normal_fixed")
    def test_validate_ai__normal_fixed__valid(self, mock_validate_ai_normal_fixed,
                                              addressing_type, can_id, target_address, source_address):
        CanAddressingInformationHandler.validate_ai(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                                    addressing_type=addressing_type,
                                                    can_id=can_id,
                                                    target_address=target_address,
                                                    source_address=source_address)
        mock_validate_ai_normal_fixed.assert_called_once_with(addressing_type=addressing_type,
                                                              can_id=can_id,
                                                              target_address=target_address,
                                                              source_address=source_address)

    @pytest.mark.parametrize("addressing_type, can_id, target_address, source_address", [
        ("some addressing", "some CAN ID", "TA", "SA"),
        (AddressingType.PHYSICAL, 0x8213, 0x9A, 0x0B),
    ])
    @pytest.mark.parametrize("address_extension", ["AE", 0x9B, 1])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformationHandler.validate_ai_normal_fixed")
    def test_validate_ai__normal_fixed__invalid(self, mock_validate_ai_normal_fixed,
                                                addressing_type, can_id,
                                                target_address, source_address, address_extension):
        with pytest.raises(UnusedArgumentError):
            CanAddressingInformationHandler.validate_ai(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                                        addressing_type=addressing_type,
                                                        can_id=can_id,
                                                        target_address=target_address,
                                                        source_address=source_address,
                                                        address_extension=address_extension)
        mock_validate_ai_normal_fixed.assert_not_called()

    @pytest.mark.parametrize("addressing_type, can_id, target_address", [
        ("some addressing", "some CAN ID", "TA"),
        (AddressingType.PHYSICAL, 0x8213, 0x9A),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformationHandler.validate_ai_extended")
    def test_validate_ai__extended__valid(self, mock_validate_ai_extended,
                                          addressing_type, can_id, target_address):
        CanAddressingInformationHandler.validate_ai(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                                    addressing_type=addressing_type,
                                                    can_id=can_id,
                                                    target_address=target_address)
        mock_validate_ai_extended.assert_called_once_with(addressing_type=addressing_type,
                                                          can_id=can_id,
                                                          target_address=target_address)

    @pytest.mark.parametrize("addressing_type, can_id, target_address", [
        ("some addressing", "some CAN ID", "TA"),
        (AddressingType.PHYSICAL, 0x8213, 0x9A),
    ])
    @pytest.mark.parametrize("source_address, address_extension", [
        ("SA", "AE"),
        ("SA", None),
        (None, "AE"),
        (0x0B, 0xF1),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformationHandler.validate_ai_extended")
    def test_validate_ai__extended__invalid(self, mock_validate_ai_extended,
                                            addressing_type, can_id,
                                            target_address, source_address, address_extension):
        with pytest.raises(UnusedArgumentError):
            CanAddressingInformationHandler.validate_ai(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                                        addressing_type=addressing_type,
                                                        can_id=can_id,
                                                        target_address=target_address,
                                                        source_address=source_address,
                                                        address_extension=address_extension)
        mock_validate_ai_extended.assert_not_called()

    @pytest.mark.parametrize("addressing_type, can_id, address_extension", [
        ("some addressing", "some CAN ID", "AE"),
        (AddressingType.PHYSICAL, 0x8213, 0xF1),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformationHandler.validate_ai_mixed_11bit")
    def test_validate_ai__mixed_11bit__valid(self, mock_validate_ai_mixed_11bit,
                                             addressing_type, can_id, address_extension):
        CanAddressingInformationHandler.validate_ai(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                    addressing_type=addressing_type,
                                                    can_id=can_id,
                                                    address_extension=address_extension)
        mock_validate_ai_mixed_11bit.assert_called_once_with(addressing_type=addressing_type,
                                                             can_id=can_id,
                                                             address_extension=address_extension)

    @pytest.mark.parametrize("addressing_type, can_id, address_extension", [
        ("some addressing", "some CAN ID", "AE"),
        (AddressingType.PHYSICAL, 0x8213, 0xF1),
    ])
    @pytest.mark.parametrize("target_address, source_address", [
        ("TA", "SA"),
        ("TA", None),
        (None, "SA"),
        (0x0B, 0xF1),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformationHandler.validate_ai_mixed_11bit")
    def test_validate_ai__mixed_11bit__invalid(self, mock_validate_ai_mixed_11bit,
                                               addressing_type, can_id,
                                               target_address, source_address, address_extension):
        with pytest.raises(UnusedArgumentError):
            CanAddressingInformationHandler.validate_ai(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                        addressing_type=addressing_type,
                                                        can_id=can_id,
                                                        target_address=target_address,
                                                        source_address=source_address,
                                                        address_extension=address_extension)
        mock_validate_ai_mixed_11bit.assert_not_called()

    @pytest.mark.parametrize("addressing_type, can_id, target_address, source_address, address_extension", [
        ("some addressing", "some CAN ID", "TA", "SA", "AE"),
        (0, None, None, None, None),
        (AddressingType.PHYSICAL, 0x8213, 0x9A, 0x0B, 0xF1),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformationHandler.validate_ai_mixed_29bit")
    def test_validate_ai__mixed_29bit(self, mock_validate_ai_mixed_29bit,
                                      addressing_type, can_id,
                                      target_address, source_address, address_extension):
        CanAddressingInformationHandler.validate_ai(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                                    addressing_type=addressing_type,
                                                    can_id=can_id,
                                                    target_address=target_address,
                                                    source_address=source_address,
                                                    address_extension=address_extension)
        mock_validate_ai_mixed_29bit.assert_called_once_with(addressing_type=addressing_type,
                                                             can_id=can_id,
                                                             target_address=target_address,
                                                             source_address=source_address,
                                                             address_extension=address_extension)

    # validate_ai_normal_11bit

    @pytest.mark.parametrize("addressing_type, can_id", [
        ("some addressing type", "some id"),
        (AddressingType.PHYSICAL, 0x7FF),
    ])
    def test_validate_ai_normal_11bit__invalid_can_id(self, addressing_type, can_id):
        self.mock_can_id_handler_class.is_normal_11bit_addressed_can_id.return_value = False
        with pytest.raises(InconsistentArgumentsError):
            CanAddressingInformationHandler.validate_ai_normal_11bit(addressing_type=addressing_type,
                                                                     can_id=can_id)
        self.mock_can_id_handler_class.validate_can_id.assert_called_once_with(can_id)
        self.mock_can_id_handler_class.is_normal_11bit_addressed_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing_type, can_id", [
        ("some addressing type", "some id"),
        (AddressingType.PHYSICAL, 0x7FF),
    ])
    def test_validate_ai_normal_11bit__valid(self, addressing_type, can_id):
        self.mock_can_id_handler_class.is_normal_11bit_addressed_can_id.return_value = True
        CanAddressingInformationHandler.validate_ai_normal_11bit(addressing_type=addressing_type,
                                                                 can_id=can_id)
        self.mock_can_id_handler_class.validate_can_id.assert_called_once_with(can_id)
        self.mock_can_id_handler_class.is_normal_11bit_addressed_can_id.assert_called_once_with(can_id)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)

    # validate_ai_normal_fixed

    @pytest.mark.parametrize("addressing_type", ["some addressing type", AddressingType.PHYSICAL])
    @pytest.mark.parametrize("can_id, target_address, source_address", [
        (None, None, 0),
        (None, 0x05, None),
        (None, None, None),
    ])
    def test_validate_ai_normal_fixed__missing_info(self, addressing_type, can_id,
                                                    target_address, source_address):
        self.mock_can_id_handler_class.is_normal_fixed_addressed_can_id.return_value = True
        with pytest.raises(InconsistentArgumentsError):
            CanAddressingInformationHandler.validate_ai_normal_fixed(addressing_type=addressing_type,
                                                                     can_id=can_id,
                                                                     target_address=target_address,
                                                                     source_address=source_address)

    @pytest.mark.parametrize("can_id", ["some CAN ID", 0x8FABC])
    @pytest.mark.parametrize("addressing_type, decoded_addressing_type, ta, decoded_ta, sa, decoded_sa", [
        (AddressingType.PHYSICAL, AddressingType.PHYSICAL, None, 0x55, 0x7F, 0x80),
        ("something", "something else", None, 0x55, None, 0x10),
        ("something", "something", 0x56, 0x55, None, 0x10),
        ("something", "something else", 0x56, 0x55, 0x7F, 0x10),
    ])
    def test_validate_ai_normal_fixed__inconsistent_can_id_ta_sa(self, can_id, addressing_type, decoded_addressing_type,
                                                                 ta, decoded_ta, sa, decoded_sa):
        self.mock_can_id_handler_class.decode_normal_fixed_addressed_can_id.return_value = {
            self.mock_can_id_handler_class.ADDRESSING_TYPE_NAME: decoded_addressing_type,
            self.mock_can_id_handler_class.TARGET_ADDRESS_NAME: decoded_ta,
            self.mock_can_id_handler_class.SOURCE_ADDRESS_NAME: decoded_sa
        }
        with pytest.raises(InconsistentArgumentsError):
            CanAddressingInformationHandler.validate_ai_normal_fixed(addressing_type=addressing_type,
                                                                     can_id=can_id,
                                                                     target_address=ta,
                                                                     source_address=sa)
        self.mock_can_id_handler_class.decode_normal_fixed_addressed_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing_type", ["some addressing type", AddressingType.PHYSICAL])
    @pytest.mark.parametrize("target_address, source_address", [
        ("ta", "sa"),
        (0xFA, 0x55),
    ])
    def test_validate_ai_normal_fixed__valid_without_can_id(self, addressing_type, target_address, source_address):
        CanAddressingInformationHandler.validate_ai_normal_fixed(addressing_type=addressing_type,
                                                                 can_id=None,
                                                                 target_address=target_address,
                                                                 source_address=source_address)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
        self.mock_validate_raw_byte.assert_has_calls([call(target_address), call(source_address)], any_order=True)
        self.mock_can_id_handler_class.validate_can_id.assert_not_called()
        self.mock_can_id_handler_class.decode_normal_fixed_addressed_can_id.assert_not_called()

    @pytest.mark.parametrize("addressing_type", ["some addressing type", AddressingType.PHYSICAL])
    @pytest.mark.parametrize("can_id", ["some CAN ID", 0x85421])
    @pytest.mark.parametrize("target_address, source_address", [
        (None, None),
        (0x12, None),
        (None, 0x34),
        ("ta", "sa"),
    ])
    def test_validate_ai_normal_fixed__valid_with_can_id(self, addressing_type, can_id, target_address, source_address):
        self.mock_can_id_handler_class.decode_normal_fixed_addressed_can_id.return_value = {
            self.mock_can_id_handler_class.ADDRESSING_TYPE_NAME: addressing_type,
            self.mock_can_id_handler_class.TARGET_ADDRESS_NAME: target_address or "ta",
            self.mock_can_id_handler_class.SOURCE_ADDRESS_NAME: source_address or "sa",
        }
        CanAddressingInformationHandler.validate_ai_normal_fixed(addressing_type=addressing_type,
                                                                 can_id=can_id,
                                                                 target_address=target_address,
                                                                 source_address=source_address)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
        self.mock_validate_raw_byte.assert_not_called()
        self.mock_can_id_handler_class.decode_normal_fixed_addressed_can_id.assert_called_once_with(can_id)

    # validate_ai_extended

    @pytest.mark.parametrize("addressing_type, can_id", [
        ("some addressing type", "some id"),
        (AddressingType.PHYSICAL, 0x7FF),
    ])
    @pytest.mark.parametrize("target_address", ["some TA", 0x5B])
    def test_validate_ai_extended__invalid_can_id(self, addressing_type, can_id, target_address):
        self.mock_can_id_handler_class.is_extended_addressed_can_id.return_value = False
        with pytest.raises(InconsistentArgumentsError):
            CanAddressingInformationHandler.validate_ai_extended(addressing_type=addressing_type,
                                                                 can_id=can_id,
                                                                 target_address=target_address)
        self.mock_can_id_handler_class.validate_can_id.assert_called_once_with(can_id)
        self.mock_can_id_handler_class.is_extended_addressed_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing_type, can_id", [
        ("some addressing type", "some id"),
        (AddressingType.PHYSICAL, 0x7FF),
    ])
    @pytest.mark.parametrize("target_address", ["some TA", 0x5B])
    def test_validate_ai_extended__valid(self, addressing_type, can_id, target_address):
        self.mock_can_id_handler_class.is_extended_addressed_can_id.return_value = True
        CanAddressingInformationHandler.validate_ai_extended(addressing_type=addressing_type,
                                                             can_id=can_id,
                                                             target_address=target_address)
        self.mock_can_id_handler_class.validate_can_id.assert_called_once_with(can_id)
        self.mock_can_id_handler_class.is_extended_addressed_can_id.assert_called_once_with(can_id)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
        self.mock_validate_raw_byte.assert_called_once_with(target_address)

    # validate_ai_mixed_11bit

    @pytest.mark.parametrize("addressing_type, can_id", [
        ("some addressing type", "some id"),
        (AddressingType.PHYSICAL, 0x7FF),
    ])
    @pytest.mark.parametrize("address_extension", ["some AE", 0x5B])
    def test_validate_ai_mixed_11bit__invalid_can_id(self, addressing_type, can_id, address_extension):
        self.mock_can_id_handler_class.is_mixed_11bit_addressed_can_id.return_value = False
        with pytest.raises(InconsistentArgumentsError):
            CanAddressingInformationHandler.validate_ai_mixed_11bit(addressing_type=addressing_type,
                                                                    can_id=can_id,
                                                                    address_extension=address_extension)
        self.mock_can_id_handler_class.validate_can_id.assert_called_once_with(can_id)
        self.mock_can_id_handler_class.is_mixed_11bit_addressed_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing_type, can_id", [
        ("some addressing type", "some id"),
        (AddressingType.PHYSICAL, 0x7FF),
    ])
    @pytest.mark.parametrize("address_extension", ["some AE", 0x5B])
    def test_validate_ai_mixed_11bit__valid(self, addressing_type, can_id, address_extension):
        self.mock_can_id_handler_class.is_mixed_11bit_addressed_can_id.return_value = True
        CanAddressingInformationHandler.validate_ai_mixed_11bit(addressing_type=addressing_type,
                                                                can_id=can_id,
                                                                address_extension=address_extension)
        self.mock_can_id_handler_class.validate_can_id.assert_called_once_with(can_id)
        self.mock_can_id_handler_class.is_mixed_11bit_addressed_can_id.assert_called_once_with(can_id)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
        self.mock_validate_raw_byte.assert_called_once_with(address_extension)

    # validate_ai_mixed_29bit

    @pytest.mark.parametrize("addressing_type", ["some addressing type", AddressingType.PHYSICAL])
    @pytest.mark.parametrize("can_id, target_address, source_address", [
        (None, None, 0),
        (None, 0x05, None),
        (None, None, None),
    ])
    @pytest.mark.parametrize("address_extension", ["some AE", 0x5B])
    def test_validate_ai_mixed_29bit__missing_info(self, addressing_type, can_id,
                                                   target_address, source_address, address_extension):
        self.mock_can_id_handler_class.is_mixed_29bit_addressed_can_id.return_value = True
        with pytest.raises(InconsistentArgumentsError):
            CanAddressingInformationHandler.validate_ai_mixed_29bit(addressing_type=addressing_type,
                                                                    can_id=can_id,
                                                                    target_address=target_address,
                                                                    source_address=source_address,
                                                                    address_extension=address_extension)

    @pytest.mark.parametrize("can_id", ["some CAN ID", 0x8FABC])
    @pytest.mark.parametrize("addressing_type, decoded_addressing_type, ta, decoded_ta, sa, decoded_sa", [
        (AddressingType.PHYSICAL, AddressingType.PHYSICAL, None, 0x55, 0x7F, 0x80),
        ("something", "something else", None, 0x55, None, 0x10),
        ("something", "something", 0x56, 0x55, None, 0x10),
        ("something", "something else", 0x56, 0x55, 0x7F, 0x10),
    ])
    @pytest.mark.parametrize("address_extension", ["some AE", 0x5B])
    def test_validate_ai_mixed_29bit__inconsistent_can_id_ta_sa(self, can_id, addressing_type, decoded_addressing_type,
                                                                ta, decoded_ta, sa, decoded_sa, address_extension):
        self.mock_can_id_handler_class.decode_mixed_addressed_29bit_can_id.return_value = {
            self.mock_can_id_handler_class.ADDRESSING_TYPE_NAME: decoded_addressing_type,
            self.mock_can_id_handler_class.TARGET_ADDRESS_NAME: decoded_ta,
            self.mock_can_id_handler_class.SOURCE_ADDRESS_NAME: decoded_sa,
        }
        with pytest.raises(InconsistentArgumentsError):
            CanAddressingInformationHandler.validate_ai_mixed_29bit(addressing_type=addressing_type,
                                                                    can_id=can_id,
                                                                    target_address=ta,
                                                                    source_address=sa,
                                                                    address_extension=address_extension)
        self.mock_can_id_handler_class.decode_mixed_addressed_29bit_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing_type", ["some addressing type", AddressingType.PHYSICAL])
    @pytest.mark.parametrize("target_address, source_address", [
        ("ta", "sa"),
        (0, 0),
        (0xFA, 0x55),
    ])
    @pytest.mark.parametrize("address_extension", ["some AE", 0x5B])
    def test_validate_ai_mixed_29bit__valid_without_can_id(self, addressing_type,
                                                           target_address, source_address, address_extension):
        CanAddressingInformationHandler.validate_ai_mixed_29bit(addressing_type=addressing_type,
                                                                can_id=None,
                                                                target_address=target_address,
                                                                source_address=source_address,
                                                                address_extension=address_extension)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
        self.mock_validate_raw_byte.assert_has_calls([call(target_address), call(source_address),
                                                      call(address_extension)], any_order=True)
        self.mock_can_id_handler_class.validate_can_id.assert_not_called()
        self.mock_can_id_handler_class.decode_mixed_addressed_29bit_can_id.assert_not_called()

    @pytest.mark.parametrize("can_id", ["some CAN ID", 0x85421])
    @pytest.mark.parametrize("target_address, source_address, addressing_type", [
        (None, None, "XD"),
        (0x12, None, AddressingType.FUNCTIONAL),
        (None, 0x34, AddressingType.PHYSICAL),
        ("ta", "sa", "some addressing type"),
    ])
    @pytest.mark.parametrize("address_extension", ["some AE", 0x5B])
    def test_validate_ai_mixed_29bit__valid_with_can_id(self, addressing_type, can_id,
                                                        target_address, source_address, address_extension):
        self.mock_can_id_handler_class.decode_mixed_addressed_29bit_can_id.return_value = {
            self.mock_can_id_handler_class.ADDRESSING_TYPE_NAME: addressing_type,
            self.mock_can_id_handler_class.TARGET_ADDRESS_NAME: target_address or "ta",
            self.mock_can_id_handler_class.SOURCE_ADDRESS_NAME: source_address or "sa",
        }
        CanAddressingInformationHandler.validate_ai_mixed_29bit(addressing_type=addressing_type,
                                                                can_id=can_id,
                                                                target_address=target_address,
                                                                source_address=source_address,
                                                                address_extension=address_extension)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
        self.mock_validate_raw_byte.assert_called_once_with(address_extension)
        self.mock_can_id_handler_class.decode_mixed_addressed_29bit_can_id.assert_called_once_with(can_id)

    # validate_ai_data_bytes

    @pytest.mark.parametrize("addressing_format", ["Addressing Format", CanAddressingFormat.NORMAL_FIXED_ADDRESSING])
    @pytest.mark.parametrize("ai_data_bytes", [[], (0x12,), [0x9A, 0xD3]])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformationHandler.get_ai_data_bytes_number")
    def test_validate_ai_data_bytes__invalid(self, mock_get_ai_data_bytes_number, addressing_format, ai_data_bytes):
        mock_get_ai_data_bytes_number.return_value = MagicMock(__eq__=Mock(return_value=False))
        with pytest.raises(InconsistentArgumentsError):
            CanAddressingInformationHandler.validate_ai_data_bytes(addressing_format=addressing_format,
                                                                   ai_data_bytes=ai_data_bytes)
        self.mock_validate_addressing_format.assert_called_once_with(addressing_format)
        self.mock_validate_raw_bytes.assert_called_once_with(ai_data_bytes, allow_empty=True)
        mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    @pytest.mark.parametrize("addressing_format", ["Addressing Format", CanAddressingFormat.NORMAL_FIXED_ADDRESSING])
    @pytest.mark.parametrize("ai_data_bytes", [[], (0x12,), [0x9A, 0xD3]])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformationHandler.get_ai_data_bytes_number")
    def test_validate_ai_data_bytes__valid(self, mock_get_ai_data_bytes_number, addressing_format, ai_data_bytes):
        mock_get_ai_data_bytes_number.return_value = len(ai_data_bytes)
        CanAddressingInformationHandler.validate_ai_data_bytes(addressing_format=addressing_format,
                                                               ai_data_bytes=ai_data_bytes)
        self.mock_validate_addressing_format.assert_called_once_with(addressing_format)
        self.mock_validate_raw_bytes.assert_called_once_with(ai_data_bytes, allow_empty=True)
        mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)


@pytest.mark.integration
class TestCanAddressingInformationHandlerIntegration:

    EMPTY_AI_INFO = {
        CanAddressingInformationHandler.ADDRESSING_TYPE_NAME: None,
        CanAddressingInformationHandler.TARGET_ADDRESS_NAME: None,
        CanAddressingInformationHandler.SOURCE_ADDRESS_NAME: None,
        CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME: None,
    }

    # decode_ai

    @pytest.mark.parametrize("addressing_format, can_id, ai_data_bytes, expected_output", [
        # Normal 11 bit
        (CanAddressingFormat.NORMAL_11BIT_ADDRESSING, 0x620, [], EMPTY_AI_INFO),
        # Normal Fixed
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, 0x18DA1234, [], {
            CanAddressingInformationHandler.ADDRESSING_TYPE_NAME: AddressingType.PHYSICAL,
            CanAddressingInformationHandler.TARGET_ADDRESS_NAME: 0x12,
            CanAddressingInformationHandler.SOURCE_ADDRESS_NAME: 0x34,
            CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME: None,
        }),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, 0x18DBB0C2, [], {
            CanAddressingInformationHandler.ADDRESSING_TYPE_NAME: AddressingType.FUNCTIONAL,
            CanAddressingInformationHandler.TARGET_ADDRESS_NAME: 0xB0,
            CanAddressingInformationHandler.SOURCE_ADDRESS_NAME: 0xC2,
            CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME: None,
        }),
        # Extended
        (CanAddressingFormat.EXTENDED_ADDRESSING, 0x645, [0xE3], {
            CanAddressingInformationHandler.ADDRESSING_TYPE_NAME: None,
            CanAddressingInformationHandler.TARGET_ADDRESS_NAME: 0xE3,
            CanAddressingInformationHandler.SOURCE_ADDRESS_NAME: None,
            CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME: None,
        }),
        (CanAddressingFormat.EXTENDED_ADDRESSING, 0x1A654321, [0xFF], {
            CanAddressingInformationHandler.ADDRESSING_TYPE_NAME: None,
            CanAddressingInformationHandler.TARGET_ADDRESS_NAME: 0xFF,
            CanAddressingInformationHandler.SOURCE_ADDRESS_NAME: None,
            CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME: None,
        }),
        # Mixed 11bit
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, 0x7F3, [0x0B], {
            CanAddressingInformationHandler.ADDRESSING_TYPE_NAME: None,
            CanAddressingInformationHandler.TARGET_ADDRESS_NAME: None,
            CanAddressingInformationHandler.SOURCE_ADDRESS_NAME: None,
            CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME: 0x0B,
        }),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, 0x60A, [0xD9], {
            CanAddressingInformationHandler.ADDRESSING_TYPE_NAME: None,
            CanAddressingInformationHandler.TARGET_ADDRESS_NAME: None,
            CanAddressingInformationHandler.SOURCE_ADDRESS_NAME: None,
            CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME: 0xD9,
        }),
        # Mixed 29bit
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, 0x18CEE009, [0x9A], {
            CanAddressingInformationHandler.ADDRESSING_TYPE_NAME: AddressingType.PHYSICAL,
            CanAddressingInformationHandler.TARGET_ADDRESS_NAME: 0xE0,
            CanAddressingInformationHandler.SOURCE_ADDRESS_NAME: 0x09,
            CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME: 0x9A,
        }),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, 0x18CDE009, [0x9A], {
            CanAddressingInformationHandler.ADDRESSING_TYPE_NAME: AddressingType.FUNCTIONAL,
            CanAddressingInformationHandler.TARGET_ADDRESS_NAME: 0xE0,
            CanAddressingInformationHandler.SOURCE_ADDRESS_NAME: 0x09,
            CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME: 0x9A,
        }),
    ])
    def test_decode_ai(self, addressing_format, can_id, ai_data_bytes, expected_output):
        assert CanAddressingInformationHandler.decode_ai(addressing_format=addressing_format,
                                                         can_id=can_id,
                                                         ai_data_bytes=ai_data_bytes) == expected_output

    # encode_ai_data_bytes

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        (CanAddressingFormat.NORMAL_11BIT_ADDRESSING, None, None),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, 0xFF, None),
        (CanAddressingFormat.EXTENDED_ADDRESSING, 0x8C, None),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, None, 0x08),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, 0x2F, 0xEA),
    ])
    def test_generate_ai_data_bytes(self, addressing_format, target_address, address_extension):
        ai_data_bytes = CanAddressingInformationHandler.encode_ai_data_bytes(addressing_format=addressing_format,
                                                                             target_address=target_address,
                                                                             address_extension=address_extension)
        assert len(ai_data_bytes) == CanAddressingInformationHandler.get_ai_data_bytes_number(addressing_format)

    # validate_ai

    @pytest.mark.parametrize("kwargs", [
        # Normal 11 bit
        {"addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
         "addressing_type": AddressingType.PHYSICAL,
         "can_id": 0x620},
        {"addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
         "addressing_type": AddressingType.FUNCTIONAL,
         "can_id": 0x7FF},
        # Normal Fixed
        {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         "addressing_type": AddressingType.PHYSICAL,
         "can_id": 0x18DA1234},
        {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         "addressing_type": AddressingType.FUNCTIONAL,
         "can_id": 0x18DBB0C2},
        {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         "addressing_type": AddressingType.PHYSICAL,
         "target_address": 0xB0,
         "source_address": 0xC2},
        # Extended
        {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
         "addressing_type": AddressingType.PHYSICAL,
         "can_id": 0x645,
         "target_address": 0xE3},
        {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
         "addressing_type": AddressingType.FUNCTIONAL,
         "can_id": 0x1A654321,
         "target_address": 0xFF},
        # Mixed 11bit
        {"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         "addressing_type": AddressingType.PHYSICAL,
         "can_id": 0x7F3,
         "address_extension": 0x0B},
        {"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         "addressing_type": AddressingType.FUNCTIONAL,
         "can_id": 0x60A,
         "address_extension": 0xD9},
        # Mixed 29bit
        {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         "addressing_type": AddressingType.PHYSICAL,
         "can_id": 0x18CEE009,
         "address_extension": 0x9A},
        {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         "addressing_type": AddressingType.FUNCTIONAL,
         "can_id": 0x18CDE009,
         "address_extension": 0x9A},
        {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         "addressing_type": AddressingType.PHYSICAL,
         "can_id": 0x18CE918B,
         "target_address": 0x91,
         "source_address": 0x8B,
         "address_extension": 0xD9},
        {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         "addressing_type": AddressingType.PHYSICAL,
         "target_address": 0x91,
         "source_address": 0x8B,
         "address_extension": 0xD9},
    ])
    def test_validate_ai__valid(self, kwargs):
        assert CanAddressingInformationHandler.validate_ai(**kwargs) is None

    @pytest.mark.parametrize("kwargs", [
        # Normal 11 bit
        {"addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
         "addressing_type": AddressingType.PHYSICAL,
         "can_id": 0x620,
         "target_address": 0x9F},
        {"addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
         "addressing_type": AddressingType.PHYSICAL,
         "can_id": 0x620,
         "source_address": 0x9F},
        # Normal Fixed
        {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         "addressing_type": AddressingType.PHYSICAL,
         "can_id": 0x18DB1234},
        {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         "addressing_type": AddressingType.FUNCTIONAL,
         "can_id": 0x18DAB0C2},
        {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         "addressing_type": AddressingType.PHYSICAL,
         "target_address": 0xB0},
        {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         "addressing_type": AddressingType.PHYSICAL,
         "target_address": 0xB0,
         "source_address": 0xC2,
         "address_extension": 0xD9},
        # Extended
        {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
         "addressing_type": AddressingType.PHYSICAL,
         "can_id": 0x645,
         "address_extension": 0x01},
        {"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         "addressing_type": AddressingType.PHYSICAL,
         "can_id": 0x7F3,
         "target_address": 0x0B},
        # Mixed 29bit
        {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         "addressing_type": AddressingType.FUNCTIONAL,
         "can_id": 0x18CEE009,
         "address_extension": 0x9A},
        {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         "addressing_type": AddressingType.PHYSICAL,
         "can_id": 0x18CDE009,
         "address_extension": 0x9A},
        {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         "addressing_type": AddressingType.FUNCTIONAL,
         "can_id": 0x18CDE009},
    ])
    def test_validate_ai__invalid(self, kwargs):
        with pytest.raises((ValueError, TypeError)):
            CanAddressingInformationHandler.validate_ai(**kwargs)

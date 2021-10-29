import pytest
from mock import patch, call

from uds.can.addressing_information import CanAddressingInformationHandler, \
    CanAddressingFormat, AddressingType, InconsistentArgumentsError, UnusedArgumentError


class TestCanAddressingInformationHandler:
    """Tests for `CanAddressingInformationHandler` class."""

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

    def teardown(self):
        self._patcher_validate_addressing_format.stop()
        self._patcher_validate_addressing_type.stop()
        self._patcher_can_id_handler_class.stop()
        self._patcher_validate_raw_byte.stop()

    # get_data_bytes_used_for_ai

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                   CanAddressingFormat.NORMAL_FIXED_ADDRESSING.value,
                                                   CanAddressingFormat.EXTENDED_ADDRESSING,
                                                   CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                   CanAddressingFormat.MIXED_11BIT_ADDRESSING.value,
                                                   CanAddressingFormat.MIXED_29BIT_ADDRESSING])
    def test_get_data_bytes_used_for_ai(self, addressing_format):
        value = CanAddressingInformationHandler.get_data_bytes_used_for_ai(addressing_format)
        assert isinstance(value, int)
        assert value >= 0
        self.mock_validate_addressing_format.assert_called_once_with(addressing_format)

    # validate_ai

    @pytest.mark.parametrize("addressing_format", [None, "unknown addressing format"])
    @pytest.mark.parametrize("addressing, can_id, target_address, source_address, address_extension", [
        ("some addressing", "some CAN ID", "TA", "SA", "AE"),
        (AddressingType.PHYSICAL, 0x8213, 0x9A, 0x0B, 0xF1),
    ])
    def test_validate_ai__unknown_addressing_format(self, addressing_format, addressing, can_id,
                                                    target_address, source_address, address_extension):
        with pytest.raises(NotImplementedError):
            CanAddressingInformationHandler.validate_ai(addressing_format=addressing_format,
                                                        addressing=addressing,
                                                        can_id=can_id,
                                                        target_address=target_address,
                                                        source_address=source_address,
                                                        address_extension=address_extension)
        self.mock_validate_addressing_format.assert_called_once_with(addressing_format)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                   CanAddressingFormat.NORMAL_11BIT_ADDRESSING.value])
    @pytest.mark.parametrize("addressing, can_id", [
        ("some addressing", "some CAN ID"),
        (AddressingType.PHYSICAL, 0x8213),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformationHandler.validate_ai_normal_11bit")
    def test_validate_ai__normal_11bit__valid(self, mock_validate_ai_normal_11bit,
                                              addressing_format, addressing, can_id):
        CanAddressingInformationHandler.validate_ai(addressing_format=addressing_format,
                                                    addressing=addressing,
                                                    can_id=can_id)
        mock_validate_ai_normal_11bit.assert_called_once_with(addressing=addressing,
                                                              can_id=can_id)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                   CanAddressingFormat.NORMAL_11BIT_ADDRESSING.value])
    @pytest.mark.parametrize("addressing, can_id, target_address, source_address, address_extension", [
        ("some addressing", "some CAN ID", "TA", "SA", "AE"),
        ("some addressing", "some CAN ID", "TA", None, None),
        (AddressingType.PHYSICAL, 0x8213, None, None, 0xF1),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformationHandler.validate_ai_normal_11bit")
    def test_validate_ai__normal_11bit__invalid(self, mock_validate_ai_normal_11bit,
                                                addressing_format, addressing, can_id,
                                                target_address, source_address, address_extension):
        with pytest.raises(UnusedArgumentError):
            CanAddressingInformationHandler.validate_ai(addressing_format=addressing_format,
                                                        addressing=addressing,
                                                        can_id=can_id,
                                                        target_address=target_address,
                                                        source_address=source_address,
                                                        address_extension=address_extension)
        mock_validate_ai_normal_11bit.assert_not_called()

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                                   CanAddressingFormat.NORMAL_FIXED_ADDRESSING.value])
    @pytest.mark.parametrize("addressing, can_id, target_address, source_address", [
        ("some addressing", "some CAN ID", "TA", "SA"),
        (AddressingType.PHYSICAL, 0x8213, 0x9A, 0x0B),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformationHandler.validate_ai_normal_fixed")
    def test_validate_ai__normal_fixed__valid(self, mock_validate_ai_normal_fixed,
                                              addressing_format, addressing, can_id,
                                              target_address, source_address):
        CanAddressingInformationHandler.validate_ai(addressing_format=addressing_format,
                                                    addressing=addressing,
                                                    can_id=can_id,
                                                    target_address=target_address,
                                                    source_address=source_address)
        mock_validate_ai_normal_fixed.assert_called_once_with(addressing=addressing,
                                                              can_id=can_id,
                                                              target_address=target_address,
                                                              source_address=source_address)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                                   CanAddressingFormat.NORMAL_FIXED_ADDRESSING.value])
    @pytest.mark.parametrize("addressing, can_id, target_address, source_address", [
        ("some addressing", "some CAN ID", "TA", "SA"),
        (AddressingType.PHYSICAL, 0x8213, 0x9A, 0x0B),
    ])
    @pytest.mark.parametrize("address_extension", ["AE", 0x9B, 1])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformationHandler.validate_ai_normal_fixed")
    def test_validate_ai__normal_fixed__invalid(self, mock_validate_ai_normal_fixed,
                                                addressing_format, addressing, can_id,
                                                target_address, source_address, address_extension):
        with pytest.raises(UnusedArgumentError):
            CanAddressingInformationHandler.validate_ai(addressing_format=addressing_format,
                                                        addressing=addressing,
                                                        can_id=can_id,
                                                        target_address=target_address,
                                                        source_address=source_address,
                                                        address_extension=address_extension)
        mock_validate_ai_normal_fixed.assert_not_called()

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.EXTENDED_ADDRESSING,
                                                   CanAddressingFormat.EXTENDED_ADDRESSING.value])
    @pytest.mark.parametrize("addressing, can_id, target_address", [
        ("some addressing", "some CAN ID", "TA"),
        (AddressingType.PHYSICAL, 0x8213, 0x9A),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformationHandler.validate_ai_extended")
    def test_validate_ai__extended__valid(self, mock_validate_ai_extended,
                                          addressing_format, addressing, can_id, target_address):
        CanAddressingInformationHandler.validate_ai(addressing_format=addressing_format,
                                                    addressing=addressing,
                                                    can_id=can_id,
                                                    target_address=target_address)
        mock_validate_ai_extended.assert_called_once_with(addressing=addressing,
                                                          can_id=can_id,
                                                          target_address=target_address)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.EXTENDED_ADDRESSING,
                                                   CanAddressingFormat.EXTENDED_ADDRESSING.value])
    @pytest.mark.parametrize("addressing, can_id, target_address", [
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
                                            addressing_format, addressing, can_id,
                                            target_address, source_address, address_extension):
        with pytest.raises(UnusedArgumentError):
            CanAddressingInformationHandler.validate_ai(addressing_format=addressing_format,
                                                        addressing=addressing,
                                                        can_id=can_id,
                                                        target_address=target_address,
                                                        source_address=source_address,
                                                        address_extension=address_extension)
        mock_validate_ai_extended.assert_not_called()

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                   CanAddressingFormat.MIXED_11BIT_ADDRESSING.value])
    @pytest.mark.parametrize("addressing, can_id, address_extension", [
        ("some addressing", "some CAN ID", "AE"),
        (AddressingType.PHYSICAL, 0x8213, 0xF1),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformationHandler.validate_ai_mixed_11bit")
    def test_validate_ai__mixed_11bit__valid(self, mock_validate_ai_mixed_11bit,
                                             addressing_format, addressing, can_id, address_extension):
        CanAddressingInformationHandler.validate_ai(addressing_format=addressing_format,
                                                    addressing=addressing,
                                                    can_id=can_id,
                                                    address_extension=address_extension)
        mock_validate_ai_mixed_11bit.assert_called_once_with(addressing=addressing,
                                                             can_id=can_id,
                                                             address_extension=address_extension)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                   CanAddressingFormat.MIXED_11BIT_ADDRESSING.value])
    @pytest.mark.parametrize("addressing, can_id, address_extension", [
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
                                               addressing_format, addressing, can_id,
                                               target_address, source_address, address_extension):
        with pytest.raises(UnusedArgumentError):
            CanAddressingInformationHandler.validate_ai(addressing_format=addressing_format,
                                                        addressing=addressing,
                                                        can_id=can_id,
                                                        target_address=target_address,
                                                        source_address=source_address,
                                                        address_extension=address_extension)
        mock_validate_ai_mixed_11bit.assert_not_called()

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                                   CanAddressingFormat.MIXED_29BIT_ADDRESSING.value])
    @pytest.mark.parametrize("addressing, can_id, target_address, source_address, address_extension", [
        ("some addressing", "some CAN ID", "TA", "SA", "AE"),
        (0, None, None, None, None),
        (AddressingType.PHYSICAL, 0x8213, 0x9A, 0x0B, 0xF1),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformationHandler.validate_ai_mixed_29bit")
    def test_validate_ai__mixed_29bit(self, mock_validate_ai_mixed_29bit,
                                      addressing_format, addressing, can_id,
                                      target_address, source_address, address_extension):
        CanAddressingInformationHandler.validate_ai(addressing_format=addressing_format,
                                                    addressing=addressing,
                                                    can_id=can_id,
                                                    target_address=target_address,
                                                    source_address=source_address,
                                                    address_extension=address_extension)
        mock_validate_ai_mixed_29bit.assert_called_once_with(addressing=addressing,
                                                             can_id=can_id,
                                                             target_address=target_address,
                                                             source_address=source_address,
                                                             address_extension=address_extension)

    # validate_ai_normal_11bit

    @pytest.mark.parametrize("addressing, can_id", [
        ("some addressing type", "some id"),
        (AddressingType.PHYSICAL, 0x7FF),
    ])
    def test_validate_ai_normal_11bit__invalid_can_id(self, addressing, can_id):
        self.mock_can_id_handler_class.is_normal_11bit_addressed_can_id.return_value = False
        with pytest.raises(InconsistentArgumentsError):
            CanAddressingInformationHandler.validate_ai_normal_11bit(addressing=addressing,
                                                                     can_id=can_id)
        self.mock_can_id_handler_class.validate_can_id.assert_called_once_with(can_id)
        self.mock_can_id_handler_class.is_normal_11bit_addressed_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing, can_id", [
        ("some addressing type", "some id"),
        (AddressingType.PHYSICAL, 0x7FF),
    ])
    def test_validate_ai_normal_11bit__valid(self, addressing, can_id):
        self.mock_can_id_handler_class.is_normal_11bit_addressed_can_id.return_value = True
        CanAddressingInformationHandler.validate_ai_normal_11bit(addressing=addressing,
                                                                 can_id=can_id)
        self.mock_can_id_handler_class.validate_can_id.assert_called_once_with(can_id)
        self.mock_can_id_handler_class.is_normal_11bit_addressed_can_id.assert_called_once_with(can_id)
        self.mock_validate_addressing_type.assert_called_once_with(addressing)

    # validate_ai_normal_fixed

    @pytest.mark.parametrize("addressing", ["some addressing type", AddressingType.PHYSICAL])
    @pytest.mark.parametrize("can_id, target_address, source_address", [
        (None, None, 0),
        (None, 0x05, None),
        (None, None, None),
    ])
    def test_validate_ai_normal_fixed__missing_info(self, addressing, can_id,
                                                    target_address, source_address):
        self.mock_can_id_handler_class.is_normal_fixed_addressed_can_id.return_value = True
        with pytest.raises(InconsistentArgumentsError):
            CanAddressingInformationHandler.validate_ai_normal_fixed(addressing=addressing,
                                                                     can_id=can_id,
                                                                     target_address=target_address,
                                                                     source_address=source_address)

    @pytest.mark.parametrize("can_id", ["some CAN ID", 0x8FABC])
    @pytest.mark.parametrize("addressing, decoded_addressing, ta, decoded_ta, sa, decoded_sa", [
        (AddressingType.PHYSICAL, AddressingType.PHYSICAL, None, 0x55, 0x7F, 0x80),
        ("something", "something else", None, 0x55, None, 0x10),
        ("something", "something", 0x56, 0x55, None, 0x10),
        ("something", "something else", 0x56, 0x55, 0x7F, 0x10),
    ])
    def test_validate_ai_normal_fixed__inconsistent_can_id_ta_sa(self, can_id, addressing, decoded_addressing,
                                                                 ta, decoded_ta, sa, decoded_sa):
        self.mock_can_id_handler_class.decode_normal_fixed_addressed_can_id.return_value = \
            (decoded_addressing, decoded_ta, decoded_sa)
        with pytest.raises(InconsistentArgumentsError):
            CanAddressingInformationHandler.validate_ai_normal_fixed(addressing=addressing,
                                                                     can_id=can_id,
                                                                     target_address=ta,
                                                                     source_address=sa)
        self.mock_can_id_handler_class.decode_normal_fixed_addressed_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing", ["some addressing type", AddressingType.PHYSICAL])
    @pytest.mark.parametrize("target_address, source_address", [
        ("ta", "sa"),
        (0, 0),
        (0xFA, 0x55),
    ])
    def test_validate_ai_normal_fixed__valid_without_can_id(self, addressing, target_address, source_address):
        CanAddressingInformationHandler.validate_ai_normal_fixed(addressing=addressing,
                                                                 can_id=None,
                                                                 target_address=target_address,
                                                                 source_address=source_address)
        self.mock_validate_addressing_type.assert_called_once_with(addressing)
        self.mock_validate_raw_byte.assert_has_calls([call(target_address), call(source_address)], any_order=True)
        self.mock_can_id_handler_class.validate_can_id.assert_not_called()
        self.mock_can_id_handler_class.decode_normal_fixed_addressed_can_id.assert_not_called()

    @pytest.mark.parametrize("addressing", ["some addressing type", AddressingType.PHYSICAL])
    @pytest.mark.parametrize("can_id", ["some CAN ID", 0x85421])
    @pytest.mark.parametrize("target_address, source_address", [
        (None, None),
        (0x12, None),
        (None, 0x34),
        ("ta", "sa"),
    ])
    def test_validate_ai_normal_fixed__valid_with_can_id(self, addressing, can_id, target_address, source_address):
        self.mock_can_id_handler_class.decode_normal_fixed_addressed_can_id.return_value = \
            (addressing, target_address or "ta", source_address or "sa")
        CanAddressingInformationHandler.validate_ai_normal_fixed(addressing=addressing,
                                                                 can_id=can_id,
                                                                 target_address=target_address,
                                                                 source_address=source_address)
        self.mock_validate_addressing_type.assert_called_once_with(addressing)
        self.mock_validate_raw_byte.assert_not_called()
        self.mock_can_id_handler_class.decode_normal_fixed_addressed_can_id.assert_called_once_with(can_id)

    # validate_ai_extended

    @pytest.mark.parametrize("addressing, can_id", [
        ("some addressing type", "some id"),
        (AddressingType.PHYSICAL, 0x7FF),
    ])
    @pytest.mark.parametrize("target_address", ["some TA", 0x5B])
    def test_validate_ai_extended__invalid_can_id(self, addressing, can_id, target_address):
        self.mock_can_id_handler_class.is_extended_addressed_can_id.return_value = False
        with pytest.raises(InconsistentArgumentsError):
            CanAddressingInformationHandler.validate_ai_extended(addressing=addressing,
                                                                 can_id=can_id,
                                                                 target_address=target_address)
        self.mock_can_id_handler_class.validate_can_id.assert_called_once_with(can_id)
        self.mock_can_id_handler_class.is_extended_addressed_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing, can_id", [
        ("some addressing type", "some id"),
        (AddressingType.PHYSICAL, 0x7FF),
    ])
    @pytest.mark.parametrize("target_address", ["some TA", 0x5B])
    def test_validate_ai_extended__valid(self, addressing, can_id, target_address):
        self.mock_can_id_handler_class.is_extended_addressed_can_id.return_value = True
        CanAddressingInformationHandler.validate_ai_extended(addressing=addressing,
                                                             can_id=can_id,
                                                             target_address=target_address)
        self.mock_can_id_handler_class.validate_can_id.assert_called_once_with(can_id)
        self.mock_can_id_handler_class.is_extended_addressed_can_id.assert_called_once_with(can_id)
        self.mock_validate_addressing_type.assert_called_once_with(addressing)
        self.mock_validate_raw_byte.assert_called_once_with(target_address)

    # validate_ai_mixed_11bit

    @pytest.mark.parametrize("addressing, can_id", [
        ("some addressing type", "some id"),
        (AddressingType.PHYSICAL, 0x7FF),
    ])
    @pytest.mark.parametrize("address_extension", ["some AE", 0x5B])
    def test_validate_ai_mixed_11bit__invalid_can_id(self, addressing, can_id, address_extension):
        self.mock_can_id_handler_class.is_mixed_11bit_addressed_can_id.return_value = False
        with pytest.raises(InconsistentArgumentsError):
            CanAddressingInformationHandler.validate_ai_mixed_11bit(addressing=addressing,
                                                                    can_id=can_id,
                                                                    address_extension=address_extension)
        self.mock_can_id_handler_class.validate_can_id.assert_called_once_with(can_id)
        self.mock_can_id_handler_class.is_mixed_11bit_addressed_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing, can_id", [
        ("some addressing type", "some id"),
        (AddressingType.PHYSICAL, 0x7FF),
    ])
    @pytest.mark.parametrize("address_extension", ["some AE", 0x5B])
    def test_validate_ai_mixed_11bit__valid(self, addressing, can_id, address_extension):
        self.mock_can_id_handler_class.is_mixed_11bit_addressed_can_id.return_value = True
        CanAddressingInformationHandler.validate_ai_mixed_11bit(addressing=addressing,
                                                                can_id=can_id,
                                                                address_extension=address_extension)
        self.mock_can_id_handler_class.validate_can_id.assert_called_once_with(can_id)
        self.mock_can_id_handler_class.is_mixed_11bit_addressed_can_id.assert_called_once_with(can_id)
        self.mock_validate_addressing_type.assert_called_once_with(addressing)
        self.mock_validate_raw_byte.assert_called_once_with(address_extension)

    # validate_ai_mixed_29bit

    @pytest.mark.parametrize("addressing", ["some addressing type", AddressingType.PHYSICAL])
    @pytest.mark.parametrize("can_id, target_address, source_address", [
        (None, None, 0),
        (None, 0x05, None),
        (None, None, None),
    ])
    @pytest.mark.parametrize("address_extension", ["some AE", 0x5B])
    def test_validate_ai_mixed_29bit__missing_info(self, addressing, can_id,
                                                   target_address, source_address, address_extension):
        self.mock_can_id_handler_class.is_mixed_29bit_addressed_can_id.return_value = True
        with pytest.raises(InconsistentArgumentsError):
            CanAddressingInformationHandler.validate_ai_mixed_29bit(addressing=addressing,
                                                                    can_id=can_id,
                                                                    target_address=target_address,
                                                                    source_address=source_address,
                                                                    address_extension=address_extension)

    @pytest.mark.parametrize("can_id", ["some CAN ID", 0x8FABC])
    @pytest.mark.parametrize("addressing, decoded_addressing, ta, decoded_ta, sa, decoded_sa", [
        (AddressingType.PHYSICAL, AddressingType.PHYSICAL, None, 0x55, 0x7F, 0x80),
        ("something", "something else", None, 0x55, None, 0x10),
        ("something", "something", 0x56, 0x55, None, 0x10),
        ("something", "something else", 0x56, 0x55, 0x7F, 0x10),
    ])
    @pytest.mark.parametrize("address_extension", ["some AE", 0x5B])
    def test_validate_ai_mixed_29bit__inconsistent_can_id_ta_sa(self, can_id, addressing, decoded_addressing,
                                                                ta, decoded_ta, sa, decoded_sa, address_extension):
        self.mock_can_id_handler_class.decode_mixed_addressed_29bit_can_id.return_value = \
            (decoded_addressing, decoded_ta, decoded_sa)
        with pytest.raises(InconsistentArgumentsError):
            CanAddressingInformationHandler.validate_ai_mixed_29bit(addressing=addressing,
                                                                    can_id=can_id,
                                                                    target_address=ta,
                                                                    source_address=sa,
                                                                    address_extension=address_extension)
        self.mock_can_id_handler_class.decode_mixed_addressed_29bit_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing", ["some addressing type", AddressingType.PHYSICAL])
    @pytest.mark.parametrize("target_address, source_address", [
        ("ta", "sa"),
        (0, 0),
        (0xFA, 0x55),
    ])
    @pytest.mark.parametrize("address_extension", ["some AE", 0x5B])
    def test_validate_ai_mixed_29bit__valid_without_can_id(self, addressing,
                                                           target_address, source_address, address_extension):
        CanAddressingInformationHandler.validate_ai_mixed_29bit(addressing=addressing,
                                                                can_id=None,
                                                                target_address=target_address,
                                                                source_address=source_address,
                                                                address_extension=address_extension)
        self.mock_validate_addressing_type.assert_called_once_with(addressing)
        self.mock_validate_raw_byte.assert_has_calls([call(target_address), call(source_address),
                                                      call(address_extension)], any_order=True)
        self.mock_can_id_handler_class.validate_can_id.assert_not_called()
        self.mock_can_id_handler_class.decode_mixed_addressed_29bit_can_id.assert_not_called()

    @pytest.mark.parametrize("can_id", ["some CAN ID", 0x85421])
    @pytest.mark.parametrize("target_address, source_address, addressing", [
        (None, None, "XD"),
        (0x12, None, AddressingType.FUNCTIONAL),
        (None, 0x34, AddressingType.PHYSICAL),
        ("ta", "sa", "some addressing type"),
    ])
    @pytest.mark.parametrize("address_extension", ["some AE", 0x5B])
    def test_validate_ai_mixed_29bit__valid_with_can_id(self, addressing, can_id,
                                                        target_address, source_address, address_extension):
        self.mock_can_id_handler_class.decode_mixed_addressed_29bit_can_id.return_value = \
            (addressing, target_address or "ta", source_address or "sa")
        CanAddressingInformationHandler.validate_ai_mixed_29bit(addressing=addressing,
                                                                can_id=can_id,
                                                                target_address=target_address,
                                                                source_address=source_address,
                                                                address_extension=address_extension)
        self.mock_validate_addressing_type.assert_called_once_with(addressing)
        self.mock_validate_raw_byte.assert_called_once_with(address_extension)
        self.mock_can_id_handler_class.decode_mixed_addressed_29bit_can_id.assert_called_once_with(can_id)


@pytest.mark.integration
class TestCanAddressingInformationHandlerIntegration:

    # get_data_bytes_used_for_ai

    def test_get_data_bytes_used_for_ai(self, example_can_addressing_format):
        assert CanAddressingInformationHandler.get_data_bytes_used_for_ai(example_can_addressing_format) == \
               CanAddressingInformationHandler.get_data_bytes_used_for_ai(example_can_addressing_format.value)

    # validate_ai

    @pytest.mark.parametrize("kwargs", [
        # TODO: examples
    ])
    def test_validate_ai__valid(self, kwargs):
        assert CanAddressingInformationHandler.validate_ai(**kwargs) is None

    @pytest.mark.parametrize("kwargs", [
        # TODO: examples
    ])
    def test_validate_ai__invalid(self, kwargs):
        with pytest.raises((ValueError, TypeError)):
            CanAddressingInformationHandler.validate_ai(**kwargs)

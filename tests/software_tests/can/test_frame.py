import pytest
from mock import Mock, call, patch

from uds.can.frame import AddressingType, CanAddressingFormat, CanDlcHandler, CanIdHandler

SCRIPT_LOCATION = "uds.can.frame"


class TestCanIdHandler:
    """Unit tests for `CanIdHandler` class."""

    def setup_method(self):
        self._patcher_validate_raw_byte = patch(f"{SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
        self._patcher_validate_addressing_format = patch(f"{SCRIPT_LOCATION}.CanAddressingFormat.validate_member")
        self.mock_validate_addressing_format = self._patcher_validate_addressing_format.start()
        self._patcher_validate_addressing_type = patch(f"{SCRIPT_LOCATION}.AddressingType.validate_member")
        self.mock_validate_addressing_type = self._patcher_validate_addressing_type.start()

    def teardown_method(self):
        self._patcher_validate_raw_byte.stop()
        self._patcher_validate_addressing_format.stop()
        self._patcher_validate_addressing_type.stop()

    # # decode_can_id
    #
    # @pytest.mark.parametrize("addressing_format", [None, "unknown addressing format"])
    # @pytest.mark.parametrize("can_id", [0, 0x20000])
    # def test_decode_can_id__not_implemented(self, addressing_format, can_id):
    #     with pytest.raises(NotImplementedError):
    #         CanIdHandler.decode_can_id(addressing_format=addressing_format, can_id=can_id)
    #     self.mock_validate_addressing_format.assert_called_once_with(addressing_format)
    #
    # @pytest.mark.parametrize("can_id", [0, 0x20000])
    # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.decode_normal_fixed_addressed_can_id")
    # def test_decode_can_id__normal_fixed(self, mock_decode_normal_fixed_addressed_can_id, can_id):
    #     assert CanIdHandler.decode_can_id(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING, can_id=can_id) \
    #            == mock_decode_normal_fixed_addressed_can_id.return_value
    #     self.mock_validate_addressing_format.assert_called_once_with(CanAddressingFormat.NORMAL_FIXED_ADDRESSING)
    #     mock_decode_normal_fixed_addressed_can_id.assert_called_once_with(can_id)
    #
    # @pytest.mark.parametrize("can_id", [0, 0x20000])
    # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.decode_mixed_addressed_29bit_can_id")
    # def test_decode_can_id__mixed_29bit(self, mock_decode_mixed_addressed_29bit_can_id, can_id):
    #     assert CanIdHandler.decode_can_id(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING, can_id=can_id) \
    #            == mock_decode_mixed_addressed_29bit_can_id.return_value
    #     self.mock_validate_addressing_format.assert_called_once_with(CanAddressingFormat.MIXED_29BIT_ADDRESSING)
    #     mock_decode_mixed_addressed_29bit_can_id.assert_called_once_with(can_id)
    #
    # @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_ADDRESSING,
    #                                                CanAddressingFormat.EXTENDED_ADDRESSING,
    #                                                CanAddressingFormat.MIXED_11BIT_ADDRESSING])
    # @pytest.mark.parametrize("can_id", [0, 0x20000])
    # def test_decode_can_id__other(self, addressing_format, can_id):
    #     decoded_values = CanIdHandler.decode_can_id(addressing_format=addressing_format, can_id=can_id)
    #     assert isinstance(decoded_values, dict)
    #     assert set(decoded_values.keys()) == {CanIdHandler.ADDRESSING_TYPE_NAME, CanIdHandler.TARGET_ADDRESS_NAME,
    #                                           CanIdHandler.SOURCE_ADDRESS_NAME}
    #     assert decoded_values[CanIdHandler.ADDRESSING_TYPE_NAME] is None
    #     assert decoded_values[CanIdHandler.TARGET_ADDRESS_NAME] is None
    #     assert decoded_values[CanIdHandler.SOURCE_ADDRESS_NAME] is None
    #     self.mock_validate_addressing_format.assert_called_once_with(addressing_format)
    #
    #
    # # decode_mixed_addressed_29bit_can_id
    #
    # @pytest.mark.parametrize("can_id", [0, 0x20000])
    # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_mixed_29bit_addressed_can_id")
    # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.validate_can_id")
    # def test_decode_mixed_addressed_29bit_can_id__not_implemented(self, mock_validate_can_id,
    #                                                               mock_is_mixed_29bit_addressed_can_id, can_id):
    #     mock_is_mixed_29bit_addressed_can_id.return_value = True
    #     with pytest.raises(NotImplementedError):
    #         CanIdHandler.decode_mixed_addressed_29bit_can_id(can_id=can_id)
    #     mock_validate_can_id.assert_called_once_with(can_id)
    #     mock_is_mixed_29bit_addressed_can_id.assert_called_once_with(can_id)
    #
    # @pytest.mark.parametrize("value", [0xFFFFFFFFFFFF, "something"])
    # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_mixed_29bit_addressed_can_id")
    # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.validate_can_id")
    # def test_decode_mixed_addressed_29bit_can_id__validation_error(self, mock_validate_can_id,
    #                                                                mock_is_mixed_29bit_addressed_can_id,
    #                                                                value):
    #     mock_is_mixed_29bit_addressed_can_id.return_value = False
    #     with pytest.raises(ValueError):
    #         CanIdHandler.decode_mixed_addressed_29bit_can_id(value)
    #     mock_validate_can_id.assert_called_once_with(value)
    #     mock_is_mixed_29bit_addressed_can_id.assert_called_once_with(value)
    #
    # @pytest.mark.parametrize("addressing_type, target_address, source_address, can_id", [
    #     (AddressingType.PHYSICAL, 0x12, 0x34, 0x18CE1234),
    #     (AddressingType.FUNCTIONAL, 0xFE, 0xDC, 0x18CDFEDC),
    #     (AddressingType.PHYSICAL, 0x00, 0xFF, 0xCE00FF),
    #     (AddressingType.FUNCTIONAL, 0xFF, 0x00, 0x1CCDFF00),
    # ])
    # def test_decode_mixed_addressed_29bit_can_id(self, can_id, addressing_type, target_address, source_address):
    #     decoded_values = CanIdHandler.decode_mixed_addressed_29bit_can_id(can_id=can_id)
    #     assert isinstance(decoded_values, dict)
    #     assert set(decoded_values.keys()) == {CanIdHandler.ADDRESSING_TYPE_NAME,
    #                                           CanIdHandler.TARGET_ADDRESS_NAME,
    #                                           CanIdHandler.SOURCE_ADDRESS_NAME}
    #     assert decoded_values[CanIdHandler.ADDRESSING_TYPE_NAME] == addressing_type
    #     assert decoded_values[CanIdHandler.TARGET_ADDRESS_NAME] == target_address
    #     assert decoded_values[CanIdHandler.SOURCE_ADDRESS_NAME] == source_address
    #
    #
    # # encode_mixed_addressed_29bit_can_id
    #
    # @pytest.mark.parametrize("addressing_type", [None, "some addressing"])
    # @pytest.mark.parametrize("target_address, source_address", [(0, 0), (0xFF, 0xFF), (0xAA, 0x55)])
    # def test_generate_mixed_addressed_29bit_can_id__not_implemented(self, addressing_type, target_address,
    #                                                                 source_address):
    #     with pytest.raises(NotImplementedError):
    #         CanIdHandler.encode_mixed_addressed_29bit_can_id(addressing_type=addressing_type,
    #                                                          target_address=target_address,
    #                                                          source_address=source_address)
    #     self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
    #
    # @pytest.mark.parametrize("addressing_type, target_address, source_address, expected_can_id", [
    #     (AddressingType.PHYSICAL, 0x12, 0x34, 0x18CE1234),
    #     (AddressingType.FUNCTIONAL, 0xFE, 0xDC, 0x18CDFEDC),
    #     (AddressingType.PHYSICAL, 0x00, 0xFF, 0x18CE00FF),
    #     (AddressingType.FUNCTIONAL, 0xFF, 0x00, 0x18CDFF00),
    # ])
    # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.validate_priority")
    # def test_generate_mixed_addressed_29bit_can_id__valid_without_priority(self, mock_validate_priority,
    #                                                                        addressing_type,
    #                                                                        target_address, source_address,
    #                                                                        expected_can_id):
    #     assert CanIdHandler.encode_mixed_addressed_29bit_can_id(addressing_type=addressing_type,
    #                                                             target_address=target_address,
    #                                                             source_address=source_address) == expected_can_id
    #     self.mock_validate_raw_byte.assert_has_calls([call(target_address), call(source_address)], any_order=True)
    #     self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
    #     mock_validate_priority.assert_called_once_with(CanIdHandler.DEFAULT_PRIORITY_VALUE)
    #
    # @pytest.mark.parametrize("addressing_type, priority, target_address, source_address, expected_can_id", [
    #     (AddressingType.PHYSICAL, 0b000, 0x12, 0x34, 0xCE1234),
    #     (AddressingType.FUNCTIONAL, 0b011, 0xFE, 0xDC, 0xCCDFEDC),
    #     (AddressingType.PHYSICAL, 0b101, 0x00, 0xFF, 0x14CE00FF),
    #     (AddressingType.FUNCTIONAL, 0b111, 0xFF, 0x00, 0x1CCDFF00),
    # ])
    # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.validate_priority")
    # def test_generate_mixed_addressed_29bit_can_id__valid_with_priority(self, mock_validate_priority,
    #                                                                     addressing_type, priority,
    #                                                                     target_address, source_address,
    #                                                                     expected_can_id):
    #     assert CanIdHandler.encode_mixed_addressed_29bit_can_id(addressing_type=addressing_type,
    #                                                             target_address=target_address,
    #                                                             source_address=source_address,
    #                                                             priority=priority) == expected_can_id
    #     self.mock_validate_raw_byte.assert_has_calls([call(target_address), call(source_address)], any_order=True)
    #     self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
    #     mock_validate_priority.assert_called_once_with(priority)
    #
    # # is_compatible_can_id
    #
    # @pytest.mark.parametrize("can_addressing_format", [None, "some new addressing format"])
    # @pytest.mark.parametrize("can_id, addressing_type", [
    #     (CanIdHandler.MIN_STANDARD_VALUE, AddressingType.PHYSICAL),
    #     (0x1234, "some addressing"),
    # ])
    # def test_is_compatible_can_id__not_implemented_error(self, can_id, can_addressing_format, addressing_type):
    #     with pytest.raises(NotImplementedError):
    #         CanIdHandler.is_compatible_can_id(can_id=can_id,
    #                                           addressing_format=can_addressing_format,
    #                                           addressing_type=addressing_type)
    #     self.mock_validate_addressing_format.assert_called_once_with(can_addressing_format)
    #
    # @pytest.mark.parametrize("can_id, addressing_type", [
    #     ("some CAN ID", "some addressing"),
    #     (CanIdHandler.MAX_STANDARD_VALUE, AddressingType.PHYSICAL),
    # ])
    # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_addressed_can_id")
    # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.validate_can_id")
    # def test_is_compatible_can_id__normal(self, mock_validate_can_id, mock_is_normal_addressed_can_id,
    #                                       can_id, addressing_type):
    #     assert CanIdHandler.is_compatible_can_id(addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
    #                                              addressing_type=addressing_type,
    #                                              can_id=can_id) == mock_is_normal_addressed_can_id.return_value
    #     mock_is_normal_addressed_can_id.assert_called_once_with(can_id=can_id)
    #     self.mock_validate_addressing_format.assert_called_once_with(CanAddressingFormat.NORMAL_ADDRESSING)
    #     mock_validate_can_id.assert_called_once_with(can_id)
    #
    # @pytest.mark.parametrize("can_id, addressing_type", [
    #     ("some CAN ID", "some addressing"),
    #     (CanIdHandler.MAX_STANDARD_VALUE, AddressingType.PHYSICAL),
    # ])
    # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_fixed_addressed_can_id")
    # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.validate_can_id")
    # def test_is_compatible_can_id__normal_fixed(self, mock_validate_can_id, mock_is_normal_fixed_addressed_can_id,
    #                                             can_id, addressing_type):
    #     assert CanIdHandler.is_compatible_can_id(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
    #                                              addressing_type=addressing_type,
    #                                              can_id=can_id) == mock_is_normal_fixed_addressed_can_id.return_value
    #     mock_is_normal_fixed_addressed_can_id.assert_called_once_with(can_id=can_id, addressing_type=addressing_type)
    #     self.mock_validate_addressing_format.assert_called_once_with(CanAddressingFormat.NORMAL_FIXED_ADDRESSING)
    #     mock_validate_can_id.assert_called_once_with(can_id)
    #
    # @pytest.mark.parametrize("can_id, addressing_type", [
    #     ("some CAN ID", "some addressing"),
    #     (CanIdHandler.MAX_STANDARD_VALUE, AddressingType.PHYSICAL),
    # ])
    # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_extended_addressed_can_id")
    # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.validate_can_id")
    # def test_is_compatible_can_id__extended(self, mock_validate_can_id, mock_is_extended_addressed_can_id,
    #                                         can_id, addressing_type):
    #     assert CanIdHandler.is_compatible_can_id(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
    #                                              addressing_type=addressing_type,
    #                                              can_id=can_id) == mock_is_extended_addressed_can_id.return_value
    #     mock_is_extended_addressed_can_id.assert_called_once_with(can_id=can_id)
    #     self.mock_validate_addressing_format.assert_called_once_with(CanAddressingFormat.EXTENDED_ADDRESSING)
    #     mock_validate_can_id.assert_called_once_with(can_id)
    #
    # @pytest.mark.parametrize("can_id, addressing_type", [
    #     ("some CAN ID", "some addressing"),
    #     (CanIdHandler.MAX_STANDARD_VALUE, AddressingType.PHYSICAL),
    # ])
    # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_mixed_11bit_addressed_can_id")
    # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.validate_can_id")
    # def test_is_compatible_can_id__mixed_11bit(self, mock_validate_can_id, mock_is_mixed_11bit_addressed_can_id,
    #                                            can_id, addressing_type):
    #     assert CanIdHandler.is_compatible_can_id(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
    #                                              addressing_type=addressing_type,
    #                                              can_id=can_id) == mock_is_mixed_11bit_addressed_can_id.return_value
    #     mock_is_mixed_11bit_addressed_can_id.assert_called_once_with(can_id=can_id)
    #     self.mock_validate_addressing_format.assert_called_once_with(CanAddressingFormat.MIXED_11BIT_ADDRESSING)
    #     mock_validate_can_id.assert_called_once_with(can_id)
    #
    # @pytest.mark.parametrize("can_id, addressing_type", [
    #     ("some CAN ID", "some addressing"),
    #     (CanIdHandler.MAX_STANDARD_VALUE, AddressingType.PHYSICAL),
    # ])
    # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_mixed_29bit_addressed_can_id")
    # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.validate_can_id")
    # def test_is_compatible_can_id__mixed_29bit(self, mock_validate_can_id, mock_is_mixed_29bit_addressed_can_id,
    #                                            can_id, addressing_type):
    #     assert CanIdHandler.is_compatible_can_id(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
    #                                              addressing_type=addressing_type,
    #                                              can_id=can_id) == mock_is_mixed_29bit_addressed_can_id.return_value
    #     mock_is_mixed_29bit_addressed_can_id.assert_called_once_with(can_id=can_id, addressing_type=addressing_type)
    #     self.mock_validate_addressing_format.assert_called_once_with(CanAddressingFormat.MIXED_29BIT_ADDRESSING)
    #     mock_validate_can_id.assert_called_once_with(can_id)
    #
    # # is_normal_addressed_can_id
    #
    # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_can_id")
    # def test_is_normal_addressed_can_id(self, mock_is_can_id):
    #     value = Mock()
    #     assert CanIdHandler.is_normal_addressed_can_id(value) == mock_is_can_id.return_value
    #     mock_is_can_id.assert_called_once_with(value)
    #
    #
    # # is_extended_addressed_can_id
    #
    # @pytest.mark.parametrize("value", [0, 0x99999])
    # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_can_id")
    # def test_is_extended_addressed_can_id(self, mock_is_can_id, value):
    #     assert CanIdHandler.is_extended_addressed_can_id(value) == mock_is_can_id.return_value
    #     mock_is_can_id.assert_called_once_with(value)
    #
    # # is_mixed_11bit_addressed_can_id
    #
    # @pytest.mark.parametrize("value", [0, 0x99999])
    # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_standard_can_id")
    # def test_is_mixed_11bit_addressed_can_id(self, mock_is_standard_can_id, value):
    #     assert CanIdHandler.is_mixed_11bit_addressed_can_id(value) == mock_is_standard_can_id.return_value
    #     mock_is_standard_can_id.assert_called_once_with(value)
    #
    # # is_mixed_29bit_addressed_can_id
    #
    # @pytest.mark.parametrize("value", [CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_MASKED_VALUE
    #                                    + (CanIdHandler.MIN_EXTENDED_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
    #                                    CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_MASKED_VALUE + 0x1234
    #                                    + (CanIdHandler.DEFAULT_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
    #                                    CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_MASKED_VALUE + 0xFFFF
    #                                    + (CanIdHandler.MAX_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
    #                                    CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_MASKED_VALUE
    #                                    + (CanIdHandler.MIN_EXTENDED_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
    #                                    CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_MASKED_VALUE + 0xDEBA
    #                                    + (CanIdHandler.DEFAULT_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
    #                                    CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_MASKED_VALUE + 0xFFFF
    #                                    + (CanIdHandler.MAX_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET)])
    # def test_is_mixed_29bit_addressed_can_id__without_addressing__true(self, value):
    #     assert CanIdHandler.is_mixed_29bit_addressed_can_id(value) is True
    #     self.mock_validate_addressing_type.assert_not_called()
    #
    # @pytest.mark.parametrize("value", [CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_MASKED_VALUE
    #                                    + (CanIdHandler.MIN_EXTENDED_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET) - 1,
    #                                    CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_MASKED_VALUE +
    #                                    (CanIdHandler.MAX_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET) + 0x10000])
    # def test_is_mixed_29bit_addressed_can_id__without_addressing__false(self, value):
    #     assert CanIdHandler.is_mixed_29bit_addressed_can_id(value) is False
    #     self.mock_validate_addressing_type.assert_not_called()
    #
    # @pytest.mark.parametrize("value, addressing_type", [
    #     (CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_MASKED_VALUE
    #      + (CanIdHandler.MIN_EXTENDED_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
    #      AddressingType.PHYSICAL),
    #     (CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_MASKED_VALUE + 0x1234
    #      + (CanIdHandler.DEFAULT_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
    #      AddressingType.PHYSICAL),
    #     (CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_MASKED_VALUE + 0xFFFF
    #      + (CanIdHandler.MAX_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
    #      AddressingType.PHYSICAL),
    #     (CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_MASKED_VALUE
    #      + (CanIdHandler.MIN_EXTENDED_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
    #      AddressingType.FUNCTIONAL),
    #     (CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_MASKED_VALUE + 0xDEBA
    #      + (CanIdHandler.DEFAULT_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
    #      AddressingType.FUNCTIONAL),
    #     (CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_MASKED_VALUE + 0xFFFF
    #      + (CanIdHandler.MAX_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
    #      AddressingType.FUNCTIONAL),
    # ])
    # def test_is_mixed_29bit_addressed_can_id__with_addressing__true(self, value, addressing_type):
    #     self.mock_validate_addressing_type.return_value = addressing_type
    #     assert CanIdHandler.is_mixed_29bit_addressed_can_id(value, addressing_type=addressing_type) is True
    #     self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
    #
    # @pytest.mark.parametrize("value, addressing_type", [
    #     (CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_MASKED_VALUE
    #      + (CanIdHandler.MIN_EXTENDED_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET) - 1,
    #      AddressingType.PHYSICAL),
    #     (CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_MASKED_VALUE
    #      + (CanIdHandler.MIN_EXTENDED_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
    #      AddressingType.FUNCTIONAL),
    #     (CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_MASKED_VALUE + 0xFFFF
    #      + (CanIdHandler.MAX_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
    #      AddressingType.FUNCTIONAL),
    #     (CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_MASKED_VALUE
    #      + (CanIdHandler.MIN_EXTENDED_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
    #      AddressingType.PHYSICAL),
    #     (CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_MASKED_VALUE + 0xFFFF
    #      + (CanIdHandler.MAX_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
    #      AddressingType.PHYSICAL),
    #     (CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_MASKED_VALUE + 0x10000
    #      + (CanIdHandler.MAX_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
    #      AddressingType.FUNCTIONAL),
    #     (0, AddressingType.PHYSICAL),
    # ])
    # def test_is_mixed_29bit_addressed_can_id__with_addressing__false(self, value, addressing_type):
    #     self.mock_validate_addressing_type.return_value = addressing_type
    #     assert CanIdHandler.is_normal_fixed_addressed_can_id(value, addressing_type=addressing_type) is False
    #     self.mock_validate_addressing_type.assert_called_once_with(addressing_type)

    # is_can_id

    @pytest.mark.parametrize("is_standard_id, is_extended_id", [
        (True, True),
        (True, False),
        (False, True,),
        (False, False),
    ])
    @pytest.mark.parametrize("value", [5000, 1234567])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_extended_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_standard_can_id")
    def test_is_can_id(self, mock_is_standard_id, mock_is_extended_can_id,
                       value, is_standard_id, is_extended_id):
        mock_is_standard_id.return_value = is_standard_id
        mock_is_extended_can_id.return_value = is_extended_id
        assert CanIdHandler.is_can_id(value) is (is_standard_id or is_extended_id)

    # is_standard_can_id

    @pytest.mark.parametrize("value", [CanIdHandler.MIN_STANDARD_VALUE,
                                       CanIdHandler.MAX_STANDARD_VALUE,
                                       (CanIdHandler.MIN_STANDARD_VALUE + CanIdHandler.MAX_STANDARD_VALUE) // 2])
    def test_is_standard_can_id__true(self, value):
        assert CanIdHandler.is_standard_can_id(value) is True

    @pytest.mark.parametrize("value", [CanIdHandler.MIN_STANDARD_VALUE - 1,
                                       CanIdHandler.MAX_STANDARD_VALUE + 1,
                                       float(CanIdHandler.MIN_STANDARD_VALUE)])
    def test_is_standard_can_id__false(self, value):
        assert CanIdHandler.is_standard_can_id(value) is False

    # is_extended_can_id

    @pytest.mark.parametrize("value", [CanIdHandler.MIN_EXTENDED_VALUE,
                                       CanIdHandler.MAX_EXTENDED_VALUE,
                                       (CanIdHandler.MIN_EXTENDED_VALUE + CanIdHandler.MAX_EXTENDED_VALUE) // 2])
    def test_is_extended_can_id__true(self, value):
        assert CanIdHandler.is_extended_can_id(value) is True

    @pytest.mark.parametrize("value", [CanIdHandler.MIN_EXTENDED_VALUE - 1,
                                       CanIdHandler.MAX_EXTENDED_VALUE + 1,
                                       float(CanIdHandler.MIN_EXTENDED_VALUE)])
    def test_is_extended_can_id__false(self, value):
        assert CanIdHandler.is_extended_can_id(value) is False

    # validate_can_id

    @pytest.mark.parametrize("value", [None, 5., "not a CAN ID"])
    @pytest.mark.parametrize("extended_can_id", [None, True, False])
    def test_validate_can_id__type_error(self, value, extended_can_id):
        with pytest.raises(TypeError):
            CanIdHandler.validate_can_id(value, extended_can_id=extended_can_id)

    @pytest.mark.parametrize("value", [5000, 1234567])
    @pytest.mark.parametrize("extended_can_id", [None, True, False])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_extended_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_standard_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_can_id")
    def test_validate_can_id__value_error(self, mock_is_can_id, mock_is_standard_can_id, mock_is_extended_can_id,
                                          value, extended_can_id):
        mock_is_can_id.return_value = False
        mock_is_standard_can_id.return_value = False
        mock_is_extended_can_id.return_value = False
        with pytest.raises(ValueError):
            CanIdHandler.validate_can_id(value, extended_can_id=extended_can_id)
        if extended_can_id is None:
            mock_is_can_id.assert_called_once_with(value)
            mock_is_standard_can_id.assert_not_called()
            mock_is_extended_can_id.assert_not_called()
        elif extended_can_id:
            mock_is_can_id.assert_not_called()
            mock_is_standard_can_id.assert_not_called()
            mock_is_extended_can_id.assert_called_once_with(value)
        else:
            mock_is_can_id.assert_not_called()
            mock_is_standard_can_id.assert_called_once_with(value)
            mock_is_extended_can_id.assert_not_called()

    @pytest.mark.parametrize("value", [5000, 1234567])
    @pytest.mark.parametrize("extended_can_id", [None, True, False])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_extended_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_standard_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_can_id")
    def test_validate_can_id__valid(self, mock_is_can_id, mock_is_standard_can_id, mock_is_extended_can_id,
                                    value, extended_can_id):
        mock_is_can_id.return_value = True
        mock_is_standard_can_id.return_value = True
        mock_is_extended_can_id.return_value = True
        assert CanIdHandler.validate_can_id(value, extended_can_id=extended_can_id) is None
        if extended_can_id is None:
            mock_is_can_id.assert_called_once_with(value)
            mock_is_standard_can_id.assert_not_called()
            mock_is_extended_can_id.assert_not_called()
        elif extended_can_id:
            mock_is_can_id.assert_not_called()
            mock_is_standard_can_id.assert_not_called()
            mock_is_extended_can_id.assert_called_once_with(value)
        else:
            mock_is_can_id.assert_not_called()
            mock_is_standard_can_id.assert_called_once_with(value)
            mock_is_extended_can_id.assert_not_called()

    # validate_priority

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_validate_priority__type_error(self, mock_isinstance):
        mock_isinstance.return_value = False
        value = Mock()
        with pytest.raises(TypeError):
            CanIdHandler.validate_priority(value)
        mock_isinstance.assert_called_once_with(value, int)

    @pytest.mark.parametrize("value", [CanIdHandler.MIN_PRIORITY_VALUE - 1,
                                       CanIdHandler.MAX_PRIORITY_VALUE + 1])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_validate_priority__value_error(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        with pytest.raises(ValueError):
            CanIdHandler.validate_priority(value)
        mock_isinstance.assert_called_once_with(value, int)

    @pytest.mark.parametrize("value", [CanIdHandler.MIN_PRIORITY_VALUE,
                                       CanIdHandler.DEFAULT_PRIORITY_VALUE - 1,
                                       CanIdHandler.MAX_PRIORITY_VALUE])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_validate_priority__valid(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        assert CanIdHandler.validate_priority(value) is None
        mock_isinstance.assert_called_once_with(value, int)


# @pytest.mark.integration
# class TestCanIdHandlerIntegration:
#     """Integration tests for `TestCanIdHandler` class."""
#
#     @pytest.mark.parametrize("addressing_type", list(AddressingType))
#     @pytest.mark.parametrize("target_address", [0x00, 0x1A, 0xFF])
#     @pytest.mark.parametrize("source_address", [0x9C, 0xB2, 0xFE])
#     def test_encode_decode_normal_fixed_can_id(self, addressing_type, target_address, source_address):
#         can_id = CanIdHandler.encode_normal_fixed_addressed_can_id(addressing_type=addressing_type,
#                                                                    target_address=target_address,
#                                                                    source_address=source_address)
#         assert CanIdHandler.decode_can_id(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
#                                           can_id=can_id) == {
#             CanIdHandler.ADDRESSING_TYPE_NAME: addressing_type,
#             CanIdHandler.TARGET_ADDRESS_NAME: target_address,
#             CanIdHandler.SOURCE_ADDRESS_NAME: source_address
#         }
#
#     @pytest.mark.parametrize("addressing_type", list(AddressingType))
#     @pytest.mark.parametrize("target_address", [0x00, 0x1A, 0xFF])
#     @pytest.mark.parametrize("source_address", [0x9C, 0xB2, 0xFE])
#     def test_encode_decode_mixed_29bit_can_id(self, addressing_type, target_address, source_address):
#         can_id = CanIdHandler.encode_mixed_addressed_29bit_can_id(addressing_type=addressing_type,
#                                                                   target_address=target_address,
#                                                                   source_address=source_address)
#         assert CanIdHandler.decode_can_id(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
#                                           can_id=can_id) == {
#             CanIdHandler.ADDRESSING_TYPE_NAME: addressing_type,
#             CanIdHandler.TARGET_ADDRESS_NAME: target_address,
#             CanIdHandler.SOURCE_ADDRESS_NAME: source_address
#         }
#
#     @pytest.mark.parametrize("addressing_format, can_id, expected_can_id_ai", [
#         # Normal
#         (CanAddressingFormat.NORMAL_ADDRESSING, 0x12345,
#          CanIdHandler.CanIdAIAlias(addressing_type=None, target_address=None, source_address=None)),
#         # Normal Fixed
#         (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, 0xDAFF00,
#          CanIdHandler.CanIdAIAlias(addressing_type=AddressingType.PHYSICAL, target_address=0xFF, source_address=0x00)),
#         (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, 0x1CDBC85A,
#          CanIdHandler.CanIdAIAlias(addressing_type=AddressingType.FUNCTIONAL, target_address=0xC8, source_address=0x5A)),
#         # Extended
#         (CanAddressingFormat.EXTENDED_ADDRESSING, 0xDBC85A,
#          CanIdHandler.CanIdAIAlias(addressing_type=None, target_address=None, source_address=None)),
#         # Mixed 11bit
#         (CanAddressingFormat.MIXED_11BIT_ADDRESSING, 0x6FE,
#          CanIdHandler.CanIdAIAlias(addressing_type=None, target_address=None, source_address=None)),
#         # Mixed 29bit
#         (CanAddressingFormat.MIXED_29BIT_ADDRESSING, 0xCEFF00,
#          CanIdHandler.CanIdAIAlias(addressing_type=AddressingType.PHYSICAL, target_address=0xFF, source_address=0x00)),
#         (CanAddressingFormat.MIXED_29BIT_ADDRESSING, 0x1CCDC85A,
#          CanIdHandler.CanIdAIAlias(addressing_type=AddressingType.FUNCTIONAL, target_address=0xC8, source_address=0x5A)),
#     ])
#     def test_decode_can_id(self, addressing_format, can_id, expected_can_id_ai):
#         assert CanIdHandler.decode_can_id(addressing_format=addressing_format, can_id=can_id) == expected_can_id_ai
#
#     @pytest.mark.parametrize("can_id, addressing_format, addressing_type, expected_result", [
#         # Normal
#         (CanIdHandler.MAX_EXTENDED_VALUE, CanAddressingFormat.NORMAL_ADDRESSING, AddressingType.PHYSICAL, True),
#         (CanIdHandler.MIN_STANDARD_VALUE, CanAddressingFormat.NORMAL_ADDRESSING, AddressingType.FUNCTIONAL, True),
#         # Normal Fixed
#         (0xDA5432, CanAddressingFormat.NORMAL_FIXED_ADDRESSING, AddressingType.PHYSICAL, True),
#         (0x1CDB0000, CanAddressingFormat.NORMAL_FIXED_ADDRESSING, AddressingType.PHYSICAL, False),
#         (0x1DA5432, CanAddressingFormat.NORMAL_FIXED_ADDRESSING, AddressingType.PHYSICAL, False),
#         (0x1CDB0000, CanAddressingFormat.NORMAL_FIXED_ADDRESSING, AddressingType.FUNCTIONAL, True),
#         (0xDA5432, CanAddressingFormat.NORMAL_FIXED_ADDRESSING, AddressingType.FUNCTIONAL, False),
#         (0x2DB0000, CanAddressingFormat.NORMAL_FIXED_ADDRESSING, AddressingType.FUNCTIONAL, False),
#         # Extended
#         (CanIdHandler.MAX_EXTENDED_VALUE, CanAddressingFormat.EXTENDED_ADDRESSING, AddressingType.PHYSICAL, True),
#         (CanIdHandler.MIN_STANDARD_VALUE, CanAddressingFormat.EXTENDED_ADDRESSING, AddressingType.FUNCTIONAL, True),
#         # Mixed 11 bit
#         (CanIdHandler.MIN_STANDARD_VALUE, CanAddressingFormat.MIXED_11BIT_ADDRESSING, AddressingType.PHYSICAL, True),
#         (CanIdHandler.MAX_STANDARD_VALUE, CanAddressingFormat.MIXED_11BIT_ADDRESSING, AddressingType.FUNCTIONAL, True),
#         (CanIdHandler.MIN_EXTENDED_VALUE, CanAddressingFormat.MIXED_11BIT_ADDRESSING, AddressingType.PHYSICAL, False),
#         # Mixed 29 bit
#         (0xCE5432, CanAddressingFormat.MIXED_29BIT_ADDRESSING, AddressingType.PHYSICAL, True),
#         (0x1CCD0000, CanAddressingFormat.MIXED_29BIT_ADDRESSING, AddressingType.PHYSICAL, False),
#         (0x1CE5432, CanAddressingFormat.MIXED_29BIT_ADDRESSING, AddressingType.PHYSICAL, False),
#         (0x1CCD0000, CanAddressingFormat.MIXED_29BIT_ADDRESSING, AddressingType.FUNCTIONAL, True),
#         (0xCE5432, CanAddressingFormat.MIXED_29BIT_ADDRESSING, AddressingType.FUNCTIONAL, False),
#         (0x2CD0000, CanAddressingFormat.MIXED_29BIT_ADDRESSING, AddressingType.FUNCTIONAL, False),
#     ])
#     def test_is_compatible_can_id(self, can_id, addressing_format, addressing_type, expected_result):
#         assert CanIdHandler.is_compatible_can_id(can_id=can_id,
#                                                  addressing_type=addressing_type,
#                                                  addressing_format=addressing_format) == expected_result


class TestCanDlcHandler:
    """Unit tests for `CanDlcHandler` class."""

    # decode_dlc

    @pytest.mark.parametrize("dlc, data_bytes_number", [
        (0, 0),
        (8, 8),
        (9, 12),
        (10, 16),
        (11, 20),
        (12, 24),
        (13, 32),
        (14, 48),
        (15, 64),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanDlcHandler.validate_dlc")
    def test_decode(self, mock_validate_dlc, dlc, data_bytes_number):
        assert CanDlcHandler.decode_dlc(dlc) == data_bytes_number
        mock_validate_dlc.assert_called_once_with(dlc)

    # encode_dlc

    @pytest.mark.parametrize("dlc, data_bytes_number", [
        (0, 0),
        (8, 8),
        (9, 12),
        (10, 16),
        (11, 20),
        (12, 24),
        (13, 32),
        (14, 48),
        (15, 64),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanDlcHandler.validate_data_bytes_number")
    def test_encode(self, mock_validate_data_bytes_number, dlc, data_bytes_number):
        assert CanDlcHandler.encode_dlc(data_bytes_number) == dlc
        mock_validate_data_bytes_number.assert_called_once_with(data_bytes_number, True)

    # get_min_dlc

    @pytest.mark.parametrize("data_bytes_number, min_dlc", [
        (64, 0xF),
        (63, 0xF),
        (49, 0xF),
        (48, 0xE),
        (33, 0xE),
        (32, 0xD),
        (25, 0xD),
        (24, 0xC),
        (21, 0xC),
        (20, 0xB),
        (17, 0xB),
        (16, 0xA),
        (13, 0xA),
        (12, 0x9),
        (9, 0x9),
        (8, 0x8),
        (7, 0x7),
        (6, 0x6),
        (5, 0x5),
        (4, 0x4),
        (3, 0x3),
        (2, 0x2),
        (1, 0x1),
        (0, 0x0),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanDlcHandler.validate_data_bytes_number")
    def test_get_min_dlc(self, mock_validate_data_bytes_number, data_bytes_number, min_dlc):
        assert CanDlcHandler.get_min_dlc(data_bytes_number) == min_dlc
        mock_validate_data_bytes_number.assert_called_once_with(data_bytes_number, False)

    # is_can_fd_specific_value

    @pytest.mark.parametrize("value", range(9, 16))
    def test_is_can_fd_specific_value__true(self, value):
        assert CanDlcHandler.is_can_fd_specific_dlc(value) is True

    @pytest.mark.parametrize("value", range(9))
    def test_is_can_fd_specific_value__false(self, value):
        assert CanDlcHandler.is_can_fd_specific_dlc(value) is False

    # validate_dlc

    @pytest.mark.parametrize("value", [None, 2., "not a DLC"])
    def test_validate_dlc__type_error(self, value):
        with pytest.raises(TypeError):
            CanDlcHandler.validate_dlc(value)

    @pytest.mark.parametrize("value", [-321, -1, 0x10, 99999])
    def test_validate_dlc__value_error(self, value):
        with pytest.raises(ValueError):
            CanDlcHandler.validate_dlc(value)

    @pytest.mark.parametrize("value", range(16))
    def test_validate_dlc__valid(self, value):
        assert CanDlcHandler.validate_dlc(value) is None

    # validate_data_bytes_number

    @pytest.mark.parametrize("value", [None, 2., "not a number of bytes"])
    def test_validate_data_bytes_number__type_error(self, value):
        with pytest.raises(TypeError):
            CanDlcHandler.validate_data_bytes_number(value)

    @pytest.mark.parametrize("value, exact_match", [
        (-1, True),
        (-1, False),
        (9, True),
        (41, True),
        (63, True),
        (128, True),
        (128, False),
    ])
    def test_validate_data_bytes_number__value_error(self, value, exact_match):
        with pytest.raises(ValueError):
            CanDlcHandler.validate_data_bytes_number(value, exact_match)

    @pytest.mark.parametrize("value, exact_match", [
        (0, True),
        (0, False),
        (1, True),
        (1, False),
        (8, True),
        (8, False),
        (9, False),
        (19, False),
        (23, False),
        (41, False),
        (63, False),
        (64, True),
        (64, False),
    ])
    def test_validate_dlc__valid(self, value, exact_match):
        assert CanDlcHandler.validate_data_bytes_number(value, exact_match) is None


@pytest.mark.integration
class TestCanDlcHandlerIntegration:
    """Integration tests for `CanDlcHandler` class."""

    @pytest.mark.parametrize("data_bytes_number", [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 16, 20, 24, 32, 48, 64])
    def test_encode_decode(self, data_bytes_number):
        dlc_value = CanDlcHandler.encode_dlc(data_bytes_number)
        assert CanDlcHandler.decode_dlc(dlc_value) == data_bytes_number

    @pytest.mark.parametrize("dlc", range(0xF))
    def test_decode_encode(self, dlc):
        data_bytes_number = CanDlcHandler.decode_dlc(dlc)
        assert CanDlcHandler.encode_dlc(data_bytes_number) == dlc

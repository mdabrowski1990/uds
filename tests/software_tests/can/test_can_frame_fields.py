import pytest
from mock import patch, call

from uds.can.can_frame_fields import CanIdHandler, \
    AddressingType, CanAddressingFormat


class TestCanIdHandler:
    """Tests for `CanIdHandler` class."""

    SCRIPT_LOCATION = "uds.can.can_frame_fields"

    def setup(self):
        self._patcher_validate_raw_byte = patch(f"{self.SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
        self._patcher_validate_addressing_format = patch(f"{self.SCRIPT_LOCATION}.CanAddressingFormat.validate_member")
        self.mock_validate_addressing_format = self._patcher_validate_addressing_format.start()
        self._patcher_validate_addressing_type = patch(f"{self.SCRIPT_LOCATION}.AddressingType.validate_member")
        self.mock_validate_addressing_type = self._patcher_validate_addressing_type.start()

    def teardown(self):
        self._patcher_validate_raw_byte.stop()
        self._patcher_validate_addressing_format.stop()
        self._patcher_validate_addressing_type.stop()

    # validate_can_id

    @pytest.mark.parametrize("value", [None, 5., "not a CAN ID", (0,)])
    def test_validate_can_id__type_error(self, value):
        with pytest.raises(TypeError):
            CanIdHandler.validate_can_id(value)

    @pytest.mark.parametrize("value", [-100, 1, 5000, 1234567, 9999999999])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_can_id")
    def test_validate_can_id__value_error(self, mock_is_can_id, value):
        mock_is_can_id.return_value = False
        with pytest.raises(ValueError):
            CanIdHandler.validate_can_id(value)
        mock_is_can_id.assert_called_once_with(value)

    @pytest.mark.parametrize("value", [-100, 1, 5000, 1234567, 9999999999])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_can_id")
    def test_validate_can_id__valid(self, mock_is_can_id, value):
        mock_is_can_id.return_value = True
        assert CanIdHandler.validate_can_id(value) is None
        mock_is_can_id.assert_called_once_with(value)

    # is_can_id

    @pytest.mark.parametrize("is_standard_id, is_extended_id, expected_result", [
        (True, True, True),
        (True, False, True),
        (False, True, True),
        (False, False, False),
    ])
    @pytest.mark.parametrize("value", [-100, 1, 5000, 1234567, 9999999999])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_extended_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_standard_can_id")
    def test_is_can_id(self, mock_is_standard_id, mock_is_extended_can_id,
                       value, is_standard_id, is_extended_id, expected_result):
        mock_is_standard_id.return_value = is_standard_id
        mock_is_extended_can_id.return_value = is_extended_id
        assert CanIdHandler.is_can_id(value) is expected_result

    # is_standard_can_id

    @pytest.mark.parametrize("value", [CanIdHandler.MIN_11BIT_VALUE, CanIdHandler.MIN_11BIT_VALUE + 1,
                                       CanIdHandler.MAX_11BIT_VALUE, CanIdHandler.MAX_11BIT_VALUE - 1,
                                       (CanIdHandler.MIN_11BIT_VALUE + CanIdHandler.MAX_11BIT_VALUE) // 2])
    def test_is_standard_can_id__true(self, value):
        assert CanIdHandler.is_standard_can_id(value) is True

    @pytest.mark.parametrize("value", [CanIdHandler.MIN_11BIT_VALUE - 1, CanIdHandler.MAX_11BIT_VALUE + 1,
                                       -1, -CanIdHandler.MAX_11BIT_VALUE,
                                       float(CanIdHandler.MIN_11BIT_VALUE), float(CanIdHandler.MAX_11BIT_VALUE)])
    def test_is_standard_can_id__false(self, value):
        assert CanIdHandler.is_standard_can_id(value) is False

    # is_extended_can_id

    @pytest.mark.parametrize("value", [CanIdHandler.MIN_29BIT_VALUE, CanIdHandler.MIN_29BIT_VALUE + 1,
                                       CanIdHandler.MAX_29BIT_VALUE, CanIdHandler.MAX_29BIT_VALUE - 1,
                                       (CanIdHandler.MIN_29BIT_VALUE + CanIdHandler.MAX_29BIT_VALUE) // 2])
    def test_is_extended_can_id__true(self, value):
        assert CanIdHandler.is_extended_can_id(value) is True

    @pytest.mark.parametrize("value", [CanIdHandler.MIN_29BIT_VALUE - 1, CanIdHandler.MAX_29BIT_VALUE + 1,
                                       -1, -CanIdHandler.MIN_29BIT_VALUE,
                                       float(CanIdHandler.MIN_29BIT_VALUE), float(CanIdHandler.MAX_29BIT_VALUE)])
    def test_is_extended_can_id__false(self, value):
        assert CanIdHandler.is_extended_can_id(value) is False

    # is_compatible_can_id

    @pytest.mark.parametrize("can_addressing_format", [None, "some new addressing format"])
    @pytest.mark.parametrize("can_id", [CanIdHandler. MIN_11BIT_VALUE, CanIdHandler.MAX_29BIT_VALUE])
    @pytest.mark.parametrize("addressing", [None, "some addressing", AddressingType.PHYSICAL])
    def test_is_compatible_can_id__not_implemented_error(self, can_id, can_addressing_format, addressing):
        with pytest.raises(NotImplementedError):
            CanIdHandler.is_compatible_can_id(can_id=can_id,
                                              addressing_format=can_addressing_format,
                                              addressing=addressing)
        self.mock_validate_addressing_format.assert_called_once_with(can_addressing_format)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                   CanAddressingFormat.NORMAL_11BIT_ADDRESSING.value])
    @pytest.mark.parametrize("is_compatible", [True, False])
    @pytest.mark.parametrize("can_id, addressing", [
        ("some CAN ID", "some addressing"),
        (CanIdHandler.MAX_11BIT_VALUE, AddressingType.PHYSICAL),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_11bit_addressed_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.validate_can_id")
    def test_is_compatible_can_id__normal_11bit(self, mock_validate_can_id, mock_is_normal_11bit_addressed_can_id,
                                                can_id, addressing_format, addressing, is_compatible):
        mock_is_normal_11bit_addressed_can_id.return_value = is_compatible
        assert CanIdHandler.is_compatible_can_id(can_id=can_id,
                                                 addressing_format=addressing_format,
                                                 addressing=addressing) is is_compatible
        mock_is_normal_11bit_addressed_can_id.assert_called_once_with(can_id=can_id)
        self.mock_validate_addressing_format.assert_called_once_with(addressing_format)
        mock_validate_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                                   CanAddressingFormat.NORMAL_FIXED_ADDRESSING.value])
    @pytest.mark.parametrize("is_compatible", [True, False])
    @pytest.mark.parametrize("can_id, addressing", [
        ("some CAN ID", "some addressing"),
        (CanIdHandler.MAX_11BIT_VALUE, AddressingType.PHYSICAL),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_fixed_addressed_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.validate_can_id")
    def test_is_compatible_can_id__normal_fixed(self, mock_validate_can_id, mock_is_normal_fixed_addressed_can_id,
                                                can_id, addressing_format, addressing, is_compatible):
        mock_is_normal_fixed_addressed_can_id.return_value = is_compatible
        assert CanIdHandler.is_compatible_can_id(can_id=can_id,
                                                 addressing_format=addressing_format,
                                                 addressing=addressing) is is_compatible
        mock_is_normal_fixed_addressed_can_id.assert_called_once_with(can_id=can_id, addressing=addressing)
        self.mock_validate_addressing_format.assert_called_once_with(addressing_format)
        mock_validate_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.EXTENDED_ADDRESSING,
                                                   CanAddressingFormat.EXTENDED_ADDRESSING.value])
    @pytest.mark.parametrize("is_compatible", [True, False])
    @pytest.mark.parametrize("can_id, addressing", [
        ("some CAN ID", "some addressing"),
        (CanIdHandler.MAX_11BIT_VALUE, AddressingType.PHYSICAL),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_extended_addressed_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.validate_can_id")
    def test_is_compatible_can_id__extended(self, mock_validate_can_id, mock_is_extended_addressed_can_id,
                                            can_id, addressing_format, addressing, is_compatible):
        mock_is_extended_addressed_can_id.return_value = is_compatible
        assert CanIdHandler.is_compatible_can_id(can_id=can_id,
                                                 addressing_format=addressing_format,
                                                 addressing=addressing) is is_compatible
        mock_is_extended_addressed_can_id.assert_called_once_with(can_id=can_id)
        self.mock_validate_addressing_format.assert_called_once_with(addressing_format)
        mock_validate_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                   CanAddressingFormat.MIXED_11BIT_ADDRESSING.value])
    @pytest.mark.parametrize("is_compatible", [True, False])
    @pytest.mark.parametrize("can_id, addressing", [
        ("some CAN ID", "some addressing"),
        (CanIdHandler.MAX_11BIT_VALUE, AddressingType.PHYSICAL),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_mixed_11bit_addressed_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.validate_can_id")
    def test_is_compatible_can_id__mixed_11bit(self, mock_validate_can_id, mock_is_mixed_11bit_addressed_can_id,
                                               can_id, addressing_format, addressing, is_compatible):
        mock_is_mixed_11bit_addressed_can_id.return_value = is_compatible
        assert CanIdHandler.is_compatible_can_id(can_id=can_id,
                                                 addressing_format=addressing_format,
                                                 addressing=addressing) is is_compatible
        mock_is_mixed_11bit_addressed_can_id.assert_called_once_with(can_id=can_id)
        self.mock_validate_addressing_format.assert_called_once_with(addressing_format)
        mock_validate_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                                   CanAddressingFormat.MIXED_29BIT_ADDRESSING.value])
    @pytest.mark.parametrize("is_compatible", [True, False])
    @pytest.mark.parametrize("can_id, addressing", [
        ("some CAN ID", "some addressing"),
        (CanIdHandler.MAX_11BIT_VALUE, AddressingType.PHYSICAL),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_mixed_29bit_addressed_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.validate_can_id")
    def test_is_compatible_can_id__mixed_29bit(self, mock_validate_can_id, mock_is_mixed_29bit_addressed_can_id,
                                               can_id, addressing_format, addressing, is_compatible):
        mock_is_mixed_29bit_addressed_can_id.return_value = is_compatible
        assert CanIdHandler.is_compatible_can_id(can_id=can_id,
                                                 addressing_format=addressing_format,
                                                 addressing=addressing) is is_compatible
        mock_is_mixed_29bit_addressed_can_id.assert_called_once_with(can_id=can_id, addressing=addressing)
        self.mock_validate_addressing_format.assert_called_once_with(addressing_format)
        mock_validate_can_id.assert_called_once_with(can_id)

    # is_normal_11bit_addressed_can_id

    @pytest.mark.parametrize("value", [0, 0x7FF, 0x800, 0x99999])
    @pytest.mark.parametrize("expected_results", [True, False])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_standard_can_id")
    def test_is_normal_11bit_addressed_can_id(self, mock_is_standard_can_id, value, expected_results):
        mock_is_standard_can_id.return_value = expected_results
        assert CanIdHandler.is_normal_11bit_addressed_can_id(value) is expected_results
        mock_is_standard_can_id.assert_called_once_with(value)

    # is_normal_fixed_addressed_can_id

    @pytest.mark.parametrize("value", [CanIdHandler.NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET,
                                       CanIdHandler.NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET + 0x1234,
                                       CanIdHandler.NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET + 0xFFFF,
                                       CanIdHandler.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET,
                                       CanIdHandler.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET + 0xDEBA,
                                       CanIdHandler.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET + 0xFFFF])
    def test_is_normal_fixed_addressed_can_id__without_addressing__true(self, value):
        assert CanIdHandler.is_normal_fixed_addressed_can_id(value) is True
        self.mock_validate_addressing_type.assert_not_called()

    @pytest.mark.parametrize("value", [CanIdHandler.NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET - 1,
                                       CanIdHandler.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET + 0x10000,
                                       0, 0x7FF, 0x620])
    def test_is_normal_fixed_addressed_can_id__without_addressing__false(self, value):
        assert CanIdHandler.is_normal_fixed_addressed_can_id(value) is False
        self.mock_validate_addressing_type.assert_not_called()

    @pytest.mark.parametrize("value, addressing", [
        (CanIdHandler.NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET, AddressingType.PHYSICAL),
        (CanIdHandler.NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET+0x1234, AddressingType.PHYSICAL.value),
        (CanIdHandler.NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET+0xFFFF, AddressingType.PHYSICAL),
        (CanIdHandler.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET, AddressingType.FUNCTIONAL.value),
        (CanIdHandler.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET+0xDEBA, AddressingType.FUNCTIONAL),
        (CanIdHandler.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET+0xFFFF, AddressingType.FUNCTIONAL),
    ])
    def test_is_normal_fixed_addressed_can_id__with_addressing__true(self, value, addressing):
        assert CanIdHandler.is_normal_fixed_addressed_can_id(value, addressing=addressing) is True
        self.mock_validate_addressing_type.assert_called_once_with(addressing)

    @pytest.mark.parametrize("value, addressing", [
        (CanIdHandler.NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET-1, AddressingType.PHYSICAL),
        (CanIdHandler.NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET+0x10000, AddressingType.PHYSICAL),
        (CanIdHandler.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET-1, AddressingType.FUNCTIONAL.value),
        (CanIdHandler.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET+0x10000, AddressingType.FUNCTIONAL.value),
        (CanIdHandler.NORMAL_FIXED_PHYSICAL_ADDRESSING_OFFSET, AddressingType.FUNCTIONAL),
        (CanIdHandler.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_OFFSET, AddressingType.PHYSICAL.value),
        (0, AddressingType.PHYSICAL),
    ])
    def test_is_normal_fixed_addressed_can_id__with_addressing__false(self, value, addressing):
        assert CanIdHandler.is_normal_fixed_addressed_can_id(value, addressing=addressing) is False
        self.mock_validate_addressing_type.assert_called_once_with(addressing)

    # is_normal_11bit_addressed_can_id

    @pytest.mark.parametrize("value", [0, 0x7FF, 0x800, 0x99999])
    @pytest.mark.parametrize("expected_results", [True, False])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_can_id")
    def test_is_extended_addressed_can_id(self, mock_is_can_id, value, expected_results):
        mock_is_can_id.return_value = expected_results
        assert CanIdHandler.is_extended_addressed_can_id(value) is expected_results
        mock_is_can_id.assert_called_once_with(value)

    # is_mixed_11bit_addressed_can_id

    @pytest.mark.parametrize("value", [0, 0x7FF, 0x800, 0x99999])
    @pytest.mark.parametrize("expected_results", [True, False])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_standard_can_id")
    def test_is_mixed_11bit_addressed_can_id(self, mock_is_standard_can_id, value, expected_results):
        mock_is_standard_can_id.return_value = expected_results
        assert CanIdHandler.is_mixed_11bit_addressed_can_id(value) is expected_results
        mock_is_standard_can_id.assert_called_once_with(value)

    # is_mixed_29bit_addressed_can_id

    @pytest.mark.parametrize("value", [CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET,
                                       CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET + 0x1234,
                                       CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET + 0xFFFF,
                                       CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET,
                                       CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET + 0xDEBA,
                                       CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET + 0xFFFF])
    def test_is_mixed_29bit_addressed_can_id__without_addressing__true(self, value):
        assert CanIdHandler.is_mixed_29bit_addressed_can_id(value) is True
        self.mock_validate_addressing_type.assert_not_called()

    @pytest.mark.parametrize("value", [CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET - 1,
                                       CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET + 0x10000,
                                       0, 0x7FF, 0x620])
    def test_is_mixed_29bit_addressed_can_id__without_addressing__false(self, value):
        assert CanIdHandler.is_mixed_29bit_addressed_can_id(value) is False
        self.mock_validate_addressing_type.assert_not_called()

    @pytest.mark.parametrize("value, addressing", [
        (CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET, AddressingType.PHYSICAL),
        (CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET+0x1234, AddressingType.PHYSICAL.value),
        (CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET+0xFFFF, AddressingType.PHYSICAL),
        (CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET, AddressingType.FUNCTIONAL.value),
        (CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET+0xDEBA, AddressingType.FUNCTIONAL),
        (CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET+0xFFFF, AddressingType.FUNCTIONAL),
    ])
    def test_is_mixed_29bit_addressed_can_id__with_addressing__true(self, value, addressing):
        assert CanIdHandler.is_mixed_29bit_addressed_can_id(value, addressing=addressing) is True
        self.mock_validate_addressing_type.assert_called_once_with(addressing)

    @pytest.mark.parametrize("value, addressing", [
        (CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET-1, AddressingType.PHYSICAL),
        (CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET+0x10000, AddressingType.PHYSICAL),
        (CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET-1, AddressingType.FUNCTIONAL.value),
        (CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET+0x10000, AddressingType.FUNCTIONAL.value),
        (CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_OFFSET, AddressingType.FUNCTIONAL),
        (CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_OFFSET, AddressingType.PHYSICAL.value),
        (0, AddressingType.PHYSICAL),
    ])
    def test_is_mixed_29bit_addressed_can_id__with_addressing__false(self, value, addressing):
        assert CanIdHandler.is_mixed_29bit_addressed_can_id(value, addressing=addressing) is False
        self.mock_validate_addressing_type.assert_called_once_with(addressing)

    # get_normal_fixed_addressed_can_id

    @pytest.mark.parametrize("addressing_type", [None, True, "some addressing"])
    @pytest.mark.parametrize("target_address, source_address", [(0, 0), (0xFF, 0xFF), (0xAA, 0x55)])
    def test_get_normal_fixed_addressed_can_id__not_implemented(self, addressing_type, target_address, source_address):
        with pytest.raises(NotImplementedError):
            CanIdHandler.get_normal_fixed_addressed_can_id(addressing_type=addressing_type,
                                                           target_address=target_address,
                                                           source_address=source_address)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)

    @pytest.mark.parametrize("addressing_type, target_address, source_address, expected_can_id", [
        (AddressingType.PHYSICAL, 0x12, 0x34, 0x18DA1234),
        (AddressingType.FUNCTIONAL, 0xFE, 0xDC, 0x18DBFEDC),
        (AddressingType.PHYSICAL.value, 0x00, 0xFF, 0x18DA00FF),
        (AddressingType.FUNCTIONAL.value, 0xFF, 0x00, 0x18DBFF00),
        (AddressingType.PHYSICAL, 0xD2, 0xA3, 0x18DAD2A3),
        (AddressingType.FUNCTIONAL.value, 0xB9, 0xF2, 0x18DBB9F2),
    ])
    def test_get_normal_fixed_addressed_can_id__valid(self, addressing_type, target_address, source_address,
                                                      expected_can_id):
        assert CanIdHandler.get_normal_fixed_addressed_can_id(addressing_type=addressing_type,
                                                              target_address=target_address,
                                                              source_address=source_address) == expected_can_id
        self.mock_validate_raw_byte.assert_has_calls([call(target_address), call(source_address)], any_order=True)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)

    # get_mixed_addressed_29bit_can_id

    @pytest.mark.parametrize("addressing_type", [None, True, "some addressing"])
    @pytest.mark.parametrize("target_address, source_address", [(0, 0), (0xFF, 0xFF), (0xAA, 0x55)])
    def test_get_mixed_addressed_29bit_can_id__not_implemented(self, addressing_type, target_address, source_address):
        with pytest.raises(NotImplementedError):
            CanIdHandler.get_mixed_addressed_29bit_can_id(addressing_type=addressing_type,
                                                          target_address=target_address,
                                                          source_address=source_address)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)

    @pytest.mark.parametrize("addressing_type, target_address, source_address, expected_can_id", [
        (AddressingType.PHYSICAL, 0x12, 0x34, 0x18CE1234),
        (AddressingType.FUNCTIONAL, 0xFE, 0xDC, 0x18CDFEDC),
        (AddressingType.PHYSICAL.value, 0x00, 0xFF, 0x18CE00FF),
        (AddressingType.FUNCTIONAL.value, 0xFF, 0x00, 0x18CDFF00),
        (AddressingType.PHYSICAL.value, 0xD2, 0xA3, 0x18CED2A3),
        (AddressingType.FUNCTIONAL, 0xB9, 0xF2, 0x18CDB9F2),
    ])
    def test_get_mixed_addressed_29bit_can_id__valid(self, addressing_type, target_address, source_address,
                                                     expected_can_id):
        assert CanIdHandler.get_mixed_addressed_29bit_can_id(addressing_type=addressing_type,
                                                             target_address=target_address,
                                                             source_address=source_address) == expected_can_id
        self.mock_validate_raw_byte.assert_has_calls([call(target_address), call(source_address)], any_order=True)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)

    # decode_normal_fixed_addressed_can_id

    @pytest.mark.parametrize("can_id", [0, 0x10000, 0x20000])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_fixed_addressed_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.validate_can_id")
    def test_decode_normal_fixed_addressed_can_id__not_implemented(self, mock_validate_can_id,
                                                                   mock_is_normal_fixed_addressed_can_id, can_id):
        mock_is_normal_fixed_addressed_can_id.return_value = True
        with pytest.raises(NotImplementedError):
            CanIdHandler.decode_normal_fixed_addressed_can_id(can_id=can_id)
        mock_validate_can_id.assert_called_once_with(can_id)
        mock_is_normal_fixed_addressed_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("value", [None, 2.5, 0x10, 0xFFFFFFFFFFFF, "something"])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_fixed_addressed_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.validate_can_id")
    def test_decode_normal_fixed_addressed_can_id__validation_error(self, mock_validate_can_id,
                                                                    mock_is_normal_fixed_addressed_can_id, value):
        mock_is_normal_fixed_addressed_can_id.return_value = False
        with pytest.raises(ValueError):
            CanIdHandler.decode_normal_fixed_addressed_can_id(value)
        mock_validate_can_id.assert_called_once_with(value)
        mock_is_normal_fixed_addressed_can_id.assert_called_once_with(value)

    @pytest.mark.parametrize("addressing_type, target_address, source_address, can_id", [
        (AddressingType.PHYSICAL, 0x12, 0x34, 0x18DA1234),
        (AddressingType.FUNCTIONAL, 0xFE, 0xDC, 0x18DBFEDC),
        (AddressingType.PHYSICAL.value, 0x00, 0xFF, 0x18DA00FF),
        (AddressingType.FUNCTIONAL.value, 0xFF, 0x00, 0x18DBFF00),
        (AddressingType.PHYSICAL, 0xD2, 0xA3, 0x18DAD2A3),
        (AddressingType.FUNCTIONAL.value, 0xB9, 0xF2, 0x18DBB9F2),
    ])
    def test_decode_normal_fixed_addressed_can_id__valid(self, can_id, addressing_type, target_address, source_address):
        assert CanIdHandler.decode_normal_fixed_addressed_can_id(can_id=can_id) \
               == (addressing_type, target_address, source_address)

    # decode_mixed_addressed_29bit_can_id

    @pytest.mark.parametrize("can_id", [0, 0x10000, 0x20000])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_mixed_29bit_addressed_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.validate_can_id")
    def test_decode_mixed_addressed_29bit_can_id__not_implemented(self, mock_validate_can_id,
                                                                  mock_is_mixed_29bit_addressed_can_id, can_id):
        mock_is_mixed_29bit_addressed_can_id.return_value = True
        with pytest.raises(NotImplementedError):
            CanIdHandler.decode_mixed_addressed_29bit_can_id(can_id=can_id)
        mock_validate_can_id.assert_called_once_with(can_id)
        mock_is_mixed_29bit_addressed_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("value", [None, 2.5, 0x10, 0xFFFFFFFFFFFF, "something"])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_mixed_29bit_addressed_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.validate_can_id")
    def test_decode_mixed_addressed_29bit_can_id__validation_error(self, mock_validate_can_id,
                                                                   mock_is_mixed_29bit_addressed_can_id,
                                                                   value):
        mock_is_mixed_29bit_addressed_can_id.return_value = False
        with pytest.raises(ValueError):
            CanIdHandler.decode_mixed_addressed_29bit_can_id(value)
        mock_validate_can_id.assert_called_once_with(value)
        mock_is_mixed_29bit_addressed_can_id.assert_called_once_with(value)

    @pytest.mark.parametrize("addressing_type, target_address, source_address, can_id", [
        (AddressingType.PHYSICAL, 0x12, 0x34, 0x18CE1234),
        (AddressingType.FUNCTIONAL, 0xFE, 0xDC, 0x18CDFEDC),
        (AddressingType.PHYSICAL.value, 0x00, 0xFF, 0x18CE00FF),
        (AddressingType.FUNCTIONAL.value, 0xFF, 0x00, 0x18CDFF00),
        (AddressingType.PHYSICAL.value, 0xD2, 0xA3, 0x18CED2A3),
        (AddressingType.FUNCTIONAL, 0xB9, 0xF2, 0x18CDB9F2),
    ])
    def test_decode_mixed_addressed_29bit_can_id(self, can_id, addressing_type, target_address, source_address):
        assert CanIdHandler.decode_mixed_addressed_29bit_can_id(can_id=can_id) \
               == (addressing_type, target_address, source_address)

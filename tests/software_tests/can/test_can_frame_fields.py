import pytest
from mock import patch, call

from uds.can.can_frame_fields import CanIdHandler, CanDlcHandler, \
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


@pytest.mark.integration
class TestTestCanIdHandlerIntegration:
    """Integration tests for `TestCanIdHandler` class."""

    @pytest.mark.parametrize("target_address", [0x00, 0x1A, 0xFF])
    @pytest.mark.parametrize("source_address", [0x9C, 0xB2, 0xFE])
    def test_encode_decode_normal_fixed_can_id(self, example_addressing_type, target_address, source_address):
        can_id = CanIdHandler.get_normal_fixed_addressed_can_id(addressing_type=example_addressing_type,
                                                                target_address=target_address,
                                                                source_address=source_address)
        assert CanIdHandler.decode_normal_fixed_addressed_can_id(can_id) == \
               (example_addressing_type, target_address, source_address)

    @pytest.mark.parametrize("target_address", [0x00, 0x1A, 0xFF])
    @pytest.mark.parametrize("source_address", [0x9C, 0xB2, 0xFE])
    def test_encode_decode_mixed_29bit_can_id(self, example_addressing_type, target_address, source_address):
        can_id = CanIdHandler.get_mixed_addressed_29bit_can_id(addressing_type=example_addressing_type,
                                                               target_address=target_address,
                                                               source_address=source_address)
        assert CanIdHandler.decode_mixed_addressed_29bit_can_id(can_id) == \
               (example_addressing_type, target_address, source_address)


class TestCanDlcHandler:
    """Tests for `CanDlcHandler` class."""

    SCRIPT_LOCATION = TestCanIdHandler.SCRIPT_LOCATION

    # decode

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
        assert CanDlcHandler.decode(dlc) == data_bytes_number
        mock_validate_dlc.assert_called_once_with(dlc)

    # encode

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
        assert CanDlcHandler.encode(data_bytes_number) == dlc
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
        (19, True),
        (23, True),
        (41, True),
        (63, True),
        (65, True),
        (65, False),
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
        dlc_value = CanDlcHandler.encode(data_bytes_number)
        assert CanDlcHandler.decode(dlc_value) == data_bytes_number

    @pytest.mark.parametrize("dlc", range(0xF))
    def test_decode_encode(self, dlc):
        data_bytes_number = CanDlcHandler.decode(dlc)
        assert CanDlcHandler.encode(data_bytes_number) == dlc

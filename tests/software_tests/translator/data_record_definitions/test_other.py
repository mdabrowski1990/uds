import pytest
from dill.pointers import children
from mock import Mock, call, patch

from uds.translator.data_record_definitions.other import (
    get_decode_float_value_formula,
    get_decode_signed_value_formula,
    get_encode_float_value_formula,
    get_encode_signed_value_formula,
    get_memory_size_and_memory_address,
get_data_records_for_formula_parameters, EXPONENT, MANTISSA, MANTISSA_BIT_LENGTH, EXPONENT_BIT_LENGTH
)

SCRIPT_LOCATION = "uds.translator.data_record_definitions.other"

class TestFormulas:

    def setup_method(self):
        self._patcher_raw_data_record = patch(f"{SCRIPT_LOCATION}.RawDataRecord")
        self.mock_raw_data_record = self._patcher_raw_data_record.start()
        self._patcher_custom_formula_data_record = patch(f"{SCRIPT_LOCATION}.CustomFormulaDataRecord")
        self.mock_custom_formula_data_record = self._patcher_custom_formula_data_record.start()

    def teardown_method(self):
        self._patcher_raw_data_record.stop()
        self._patcher_custom_formula_data_record.stop()

    # get_memory_size_and_memory_address

    @pytest.mark.parametrize("address_and_length_format_identifier", [-1, 0x01, 0xF0, 0x111])
    def test_get_memory_size_and_memory_address__value_error(self, address_and_length_format_identifier):
        with pytest.raises(ValueError):
            get_memory_size_and_memory_address(address_and_length_format_identifier)

    @pytest.mark.parametrize("memory_address_length, memory_size_length", [
        (0x1, 0x1),
        (0xD, 0x3),
        (0xF, 0xF),
    ])
    def test_get_memory_size_and_memory_address(self, memory_address_length, memory_size_length):
        assert (get_memory_size_and_memory_address((memory_size_length << 4) + memory_address_length)
                == (self.mock_raw_data_record.return_value, self.mock_raw_data_record.return_value))
        self.mock_raw_data_record.assert_has_calls([call(name="memoryAddress",
                                                         length=8 * memory_address_length),
                                                    call(name="memorySize",
                                                         length=8 * memory_size_length)],
                                                   any_order=False)

    # get_scaling_byte_extension

    # TODO

    # get_formula_parameters

    @pytest.mark.parametrize("raw_value, physical_value", [
        (0xFF, Mock()),
        (0xAB, "some unknown formula"),
    ])
    @patch(f"{SCRIPT_LOCATION}.FORMULA_IDENTIFIER")
    def test_get_formula_parameters__value_error(self, mock_formula_identifier, raw_value, physical_value):
        mock_formula_identifier.get_physical_value.return_value = physical_value
        with pytest.raises(ValueError):
            get_data_records_for_formula_parameters(raw_value)
        mock_formula_identifier.get_physical_value.assert_called_once_with(raw_value)

    @pytest.mark.parametrize("raw_value, constants_names", [
        (0x00, ("C0", "C1")),
        (0x07, ("C0",)),
        (0x09, ("C0", "C1")),
    ])
    @patch(f"{SCRIPT_LOCATION}.get_decode_float_value_formula")
    @patch(f"{SCRIPT_LOCATION}.get_encode_float_value_formula")
    def test_get_formula_parameters__value_error(self, mock_get_encode_float_value_formula,
                                                 mock_get_decode_float_value_formula,
                                                 raw_value, constants_names):
        assert (get_data_records_for_formula_parameters(raw_value)
                == (self.mock_custom_formula_data_record.return_value,) * len(constants_names))
        self.mock_custom_formula_data_record.assert_has_calls(
            [call(name=constant_name,
                  length=EXPONENT_BIT_LENGTH + MANTISSA_BIT_LENGTH,
                  children=(EXPONENT, MANTISSA),
                  encoding_formula=mock_get_encode_float_value_formula.return_value,
                  decoding_formula=mock_get_decode_float_value_formula.return_value)
             for constant_name in constants_names],
            any_order=False)
        mock_get_encode_float_value_formula.assert_called_once_with(exponent_bit_length=EXPONENT_BIT_LENGTH,
                                                                    mantissa_bit_length=MANTISSA_BIT_LENGTH)
        mock_get_encode_float_value_formula.assert_called_once_with(exponent_bit_length=EXPONENT_BIT_LENGTH,
                                                                    mantissa_bit_length=MANTISSA_BIT_LENGTH)

    # get_decode_signed_value_formula

    @pytest.mark.parametrize("bit_length", [Mock(), "something"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_get_decode_signed_value_formula__type_error(self, mock_isinstance, bit_length):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            get_decode_signed_value_formula(bit_length)
        mock_isinstance.assert_called_once_with(bit_length, int)

    @pytest.mark.parametrize("bit_length", [1, -5])
    def test_get_decode_signed_value_formula__value_error(self, bit_length):
        with pytest.raises(ValueError):
            get_decode_signed_value_formula(bit_length)

    @pytest.mark.parametrize("bit_length, encoding_mapping", [
        (4, {0x0: 0, 0x7: 7, 0x8: -8, 0xF: -1}),
        (12, {0x000: 0, 0x7FF: 2047, 0x800: -2048, 0xFFF: -1}),
    ])
    def test_get_decode_signed_value_formula(self, bit_length, encoding_mapping):
        formula = get_decode_signed_value_formula(bit_length)
        assert all(formula(unsigned_value) == signed_value
                   for unsigned_value, signed_value in encoding_mapping.items())

    # get_encode_signed_value_formula
    
    @pytest.mark.parametrize("bit_length", [Mock(), "something"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_get_encode_signed_value_formula__type_error(self, mock_isinstance, bit_length):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            get_encode_signed_value_formula(bit_length)
        mock_isinstance.assert_called_once_with(bit_length, int)

    @pytest.mark.parametrize("bit_length", [1, -5])
    def test_get_encode_signed_value_formula__value_error(self, bit_length):
        with pytest.raises(ValueError):
            get_encode_signed_value_formula(bit_length)

    @pytest.mark.parametrize("bit_length, encoding_mapping", [
        (4, {0x0: 0, 0x7: 7, 0x8: -8, 0xF: -1}),
        (12, {0x000: 0, 0x7FF: 2047, 0x800: -2048, 0xFFF: -1}),
    ])
    def test_get_encode_signed_value_formula(self, bit_length, encoding_mapping):
        formula = get_encode_signed_value_formula(bit_length)
        assert all(formula(signed_value) == unsigned_value
                   for unsigned_value, signed_value in encoding_mapping.items())

    # get_decode_float_value_formula

    @pytest.mark.parametrize("exponent_bit_length, mantissa_bit_length, exponent_value, mantissa_value, int_value", [
        (4, 12, -1, -1234, 0xFB2E),
        (8, 24, 3, 608, 0x03000260),
    ])
    @patch(f"{SCRIPT_LOCATION}.get_encode_signed_value_formula")
    def test_get_decode_float_value_formula(self, mock_get_encode_signed_value_formula,
                                            exponent_bit_length, mantissa_bit_length,
                                            exponent_value, mantissa_value, int_value):
        mock_exponent_encode_formula = Mock(return_value=exponent_value)
        mock_mantissa_encode_formula = Mock(return_value=mantissa_value)
        mock_get_encode_signed_value_formula.side_effect = [mock_exponent_encode_formula,
                                                            mock_mantissa_encode_formula]
        formula = get_decode_float_value_formula(exponent_bit_length=exponent_bit_length,
                                                 mantissa_bit_length=mantissa_bit_length)
        assert formula(int_value) == mantissa_value * (10 ** exponent_value)
        mock_get_encode_signed_value_formula.assert_has_calls([call(exponent_bit_length), call(mantissa_bit_length)],
                                                              any_order=False)
        mock_exponent_encode_formula.assert_called_once_with(int_value >> mantissa_bit_length)
        mock_mantissa_encode_formula.assert_called_once_with(int_value & ((1 << mantissa_bit_length) - 1))

    # get_encode_float_value_formula

    @pytest.mark.parametrize("exponent_bit_length, mantissa_bit_length, "
                             "exponent_unsigned_value, mantissa_unsigned_value, "
                             "exponent_signed_value, mantissa_signed_value, "
                             "float_value", [
        (4, 12, 0xF, 0x234, -1, 564, 56.4),
        (8, 24, 0xFD, 0xF0E1D2, -3, -990766, -990.766),
    ])
    @patch(f"{SCRIPT_LOCATION}.get_decode_signed_value_formula")
    def test_get_encode_float_value_formula(self, mock_get_decode_signed_value_formula,
                                            exponent_bit_length, mantissa_bit_length,
                                            exponent_unsigned_value, mantissa_unsigned_value,
                                            exponent_signed_value, mantissa_signed_value,
                                            float_value):
        mock_exponent_decode_formula = Mock(return_value=exponent_unsigned_value)
        mock_mantissa_decode_formula = Mock(return_value=mantissa_unsigned_value)
        mock_get_decode_signed_value_formula.side_effect = [mock_exponent_decode_formula,
                                                            mock_mantissa_decode_formula]
        formula = get_encode_float_value_formula(exponent_bit_length=exponent_bit_length,
                                                 mantissa_bit_length=mantissa_bit_length)
        assert formula(float_value) == (exponent_unsigned_value << mantissa_bit_length) + mantissa_unsigned_value
        mock_get_decode_signed_value_formula.assert_has_calls([call(exponent_bit_length), call(mantissa_bit_length)],
                                                              any_order=False)
        mock_exponent_decode_formula.assert_called_once_with(exponent_signed_value)
        mock_mantissa_decode_formula.assert_called_once_with(mantissa_signed_value)

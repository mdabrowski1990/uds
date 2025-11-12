from unittest.mock import MagicMock

import pytest
from mock import Mock, call, patch

from uds.translator.data_record_definitions.other import (
    EXPONENT,
    EXPONENT_BIT_LENGTH,
    FORMULA_IDENTIFIER,
    MANTISSA,
    MANTISSA_BIT_LENGTH,
    STATE_AND_CONNECTION_TYPE,
    UNIT_OR_FORMAT,
    get_data_from_memory,
    get_data_records_for_formula_parameters,
    get_decode_float_value_formula,
    get_decode_signed_value_formula,
    get_encode_float_value_formula,
    get_encode_signed_value_formula,
    get_formula_data_records_for_formula_parameters,
    get_formula_for_raw_data_record_with_length,
    get_memory_size_and_memory_address,
    get_scaling_byte_extension,
)

SCRIPT_LOCATION = "uds.translator.data_record_definitions.other"

class TestFormulas:

    def setup_method(self):
        self._patcher_raw_data_record = patch(f"{SCRIPT_LOCATION}.RawDataRecord")
        self.mock_raw_data_record = self._patcher_raw_data_record.start()
        self._patcher_custom_formula_data_record = patch(f"{SCRIPT_LOCATION}.CustomFormulaDataRecord")
        self.mock_custom_formula_data_record = self._patcher_custom_formula_data_record.start()
        self._patcher_conditional_formula_data_record = patch(f"{SCRIPT_LOCATION}.ConditionalFormulaDataRecord")
        self.mock_conditional_formula_data_record = self._patcher_conditional_formula_data_record.start()

    def teardown_method(self):
        self._patcher_raw_data_record.stop()
        self._patcher_custom_formula_data_record.stop()

    # get_formula_for_raw_data_record_with_length

    @pytest.mark.parametrize("accept_zero_length, length", [
        (True, -1),
        (False, 0),
    ])
    def test_get_formula_for_raw_data_record_with_length__formula_value_error(self, accept_zero_length, length):
        formula = get_formula_for_raw_data_record_with_length(data_record_name=MagicMock(),
                                                              accept_zero_length=accept_zero_length)
        with pytest.raises(ValueError):
            formula(-1)

    def test_get_formula_for_raw_data_record_with_length__empty(self):
        formula = get_formula_for_raw_data_record_with_length(data_record_name=MagicMock(),
                                                              accept_zero_length=True)
        assert formula(0) == ()

    @pytest.mark.parametrize("data_record_name, accept_zero_length, length", [
        ("Some Name", True, 54),
        ("XYZ - abc", False, 1),
    ])
    def test_get_formula_for_raw_data_record_with_length__value(self, data_record_name, accept_zero_length, length):
        formula = get_formula_for_raw_data_record_with_length(data_record_name=data_record_name,
                                                              accept_zero_length=accept_zero_length)
        assert formula(length) == (self.mock_raw_data_record.return_value, )
        self.mock_raw_data_record.assert_called_once_with(name=data_record_name,
                                                          length=8,
                                                          min_occurrences=length,
                                                          max_occurrences=length)

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

    # get_data_from_memory

    @pytest.mark.parametrize("address_and_length_format_identifier", [-1, 0x01, 0xF0, 0x111])
    def test_get_data_from_memory__value_error(self, address_and_length_format_identifier):
        with pytest.raises(ValueError):
            get_data_from_memory(address_and_length_format_identifier)

    @pytest.mark.parametrize("memory_address_length, memory_size_length", [
        (0x1, 0x1),
        (0xD, 0x3),
        (0xF, 0xF),
    ])
    def test_get_data_from_memory(self, memory_address_length, memory_size_length):
        assert (get_data_from_memory((memory_size_length << 4) + memory_address_length)
                == (self.mock_raw_data_record.return_value,))
        self.mock_raw_data_record.assert_has_calls([call(name="memoryAddress",
                                                         length=8 * memory_address_length),
                                                    call(name="memorySize",
                                                         length=8 * memory_size_length),
                                                    call(name="Data from Memory",
                                                         children=(self.mock_raw_data_record.return_value,
                                                                   self.mock_raw_data_record.return_value),
                                                         length=8 * (memory_address_length + memory_size_length),
                                                         min_occurrences=1,
                                                         max_occurrences=None)],
                                                   any_order=True)
    
    # get_scaling_byte_extension

    @pytest.mark.parametrize("scaling_byte", [-1, 0x100])
    def test_get_scaling_byte_extension__value_error(self, scaling_byte):
        with pytest.raises(ValueError):
            get_scaling_byte_extension(scaling_byte, Mock())

    def test_get_scaling_byte_extension__2__inconsistency_Error(self):
        with pytest.raises(ValueError):
            get_scaling_byte_extension(0x20, Mock())

    @pytest.mark.parametrize("number_of_bytes, scaling_byte_number", [
        (1, 23),
        (15, 1)
    ])
    def test_get_scaling_byte_extension__2(self, number_of_bytes, scaling_byte_number):
        assert (get_scaling_byte_extension(0x20 + number_of_bytes, scaling_byte_number)
                == (self.mock_raw_data_record.return_value,))
        self.mock_raw_data_record.assert_called_with(name=f"scalingByteExtension#{scaling_byte_number}",
                                                     length=8 * number_of_bytes,
                                                     children=(self.mock_raw_data_record.return_value,))

    @pytest.mark.parametrize("number_of_bytes, scaling_byte_number", [
        (1, 23),
        (15, 1)
    ])
    @patch(f"{SCRIPT_LOCATION}.get_formula_data_records_for_formula_parameters")
    def test_get_scaling_byte_extension__9(self, mock_get_formula_data_records_for_formula_parameters,
                                           number_of_bytes, scaling_byte_number):
        assert (get_scaling_byte_extension(0x90 + number_of_bytes, scaling_byte_number)
                == (self.mock_raw_data_record.return_value, self.mock_conditional_formula_data_record.return_value))
        self.mock_raw_data_record.assert_called_once_with(name=f"scalingByteExtension#{scaling_byte_number}",
                                                          length=FORMULA_IDENTIFIER.length,
                                                          children=(FORMULA_IDENTIFIER,))
        self.mock_conditional_formula_data_record.assert_called_once_with(
            formula=mock_get_formula_data_records_for_formula_parameters.return_value)
        mock_get_formula_data_records_for_formula_parameters.assert_called_once_with(scaling_byte_number)

    @pytest.mark.parametrize("number_of_bytes, scaling_byte_number", [
        (1, 23),
        (15, 1)
    ])
    def test_get_scaling_byte_extension__A(self, number_of_bytes, scaling_byte_number):
        assert (get_scaling_byte_extension(0xA0 + number_of_bytes, scaling_byte_number)
                == (self.mock_raw_data_record.return_value,))
        self.mock_raw_data_record.assert_called_with(name=f"scalingByteExtension#{scaling_byte_number}",
                                                     length=UNIT_OR_FORMAT.length,
                                                     children=(UNIT_OR_FORMAT,))

    @pytest.mark.parametrize("number_of_bytes, scaling_byte_number", [
        (1, 23),
        (15, 1)
    ])
    def test_get_scaling_byte_extension__B(self, number_of_bytes, scaling_byte_number):
        assert (get_scaling_byte_extension(0xB0 + number_of_bytes, scaling_byte_number)
                == (self.mock_raw_data_record.return_value,))
        self.mock_raw_data_record.assert_called_with(name=f"scalingByteExtension#{scaling_byte_number}",
                                                     length=STATE_AND_CONNECTION_TYPE.length,
                                                     children=(STATE_AND_CONNECTION_TYPE,))

    @pytest.mark.parametrize("scaling_byte", [0x00, 0x15, 0xF1])
    def test_get_scaling_byte_extension__other(self, scaling_byte):
        assert get_scaling_byte_extension(scaling_byte, Mock()) == ()

    # get_formula_parameters

    @pytest.mark.parametrize("raw_value, physical_value", [
        (0xFF, Mock()),
        (0xAB, "some unknown formula"),
    ])
    @patch(f"{SCRIPT_LOCATION}.FORMULA_IDENTIFIER")
    def test_get_formula_parameters__value_error(self, mock_formula_identifier, raw_value, physical_value):
        mock_formula_identifier.get_physical_value.return_value = physical_value
        with pytest.raises(ValueError):
            get_data_records_for_formula_parameters(formula_identifier=raw_value, scaling_byte_number=1)
        mock_formula_identifier.get_physical_value.assert_called_once_with(raw_value)

    @pytest.mark.parametrize("raw_value, scaling_byte_number, constants_names", [
        (0x00, 1, ("C0#1", "C1#1")),
        (0x07, 5, ("C0#5",)),
        (0x09, 12, ("C0#12", "C1#12")),
    ])
    @patch(f"{SCRIPT_LOCATION}.get_decode_float_value_formula")
    @patch(f"{SCRIPT_LOCATION}.get_encode_float_value_formula")
    def test_get_formula_parameters(self, mock_get_encode_float_value_formula,
                                    mock_get_decode_float_value_formula,
                                    raw_value, scaling_byte_number, constants_names):
        assert (get_data_records_for_formula_parameters(formula_identifier=raw_value,
                                                        scaling_byte_number=scaling_byte_number)
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

    # get_formula_data_records_for_formula_parameters

    @pytest.mark.parametrize("scaling_byte_number", [4, 10])
    @patch(f"{SCRIPT_LOCATION}.get_data_records_for_formula_parameters")
    def test_get_formula_data_records_for_formula_parameters(self, mock_get_data_records_for_formula_parameters,
                                                             scaling_byte_number):
        mock_formula_identifier = Mock()
        formula = get_formula_data_records_for_formula_parameters(scaling_byte_number)
        assert formula(mock_formula_identifier) == mock_get_data_records_for_formula_parameters.return_value
        mock_get_data_records_for_formula_parameters.assert_called_once_with(formula_identifier=mock_formula_identifier,
                                                                             scaling_byte_number=scaling_byte_number)

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

    @pytest.mark.parametrize("bit_length, value_out_of_range", [
        (4, -1),
        (12, 4096),
    ])
    def test_get_decode_signed_value_formula__formula_value_error(self, bit_length, value_out_of_range):
        formula = get_decode_signed_value_formula(bit_length)
        with pytest.raises(ValueError):
            formula(value_out_of_range)

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

    @pytest.mark.parametrize("bit_length, value_out_of_range", [
        (4, -9),
        (12, 2048),
    ])
    def test_get_encode_signed_value_formula__formula_value_error(self, bit_length, value_out_of_range):
        formula = get_encode_signed_value_formula(bit_length)
        with pytest.raises(ValueError):
            formula(value_out_of_range)

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

    @pytest.mark.parametrize("exponent_bit_length, mantissa_bit_length, float_value", [
        (4, 12, float("inf")),
        (8, 24, float("inf")),
    ])
    def test_get_encode_float_value_formula__formula_value_error(self, exponent_bit_length, mantissa_bit_length, float_value):
        formula = get_encode_float_value_formula(exponent_bit_length=exponent_bit_length,
                                                 mantissa_bit_length=mantissa_bit_length)
        with pytest.raises(ValueError):
            formula(float_value)

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

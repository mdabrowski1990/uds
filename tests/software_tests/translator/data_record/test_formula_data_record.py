import pytest
from mock import MagicMock, Mock, call, patch

from uds.translator.data_record.formula_data_record import CustomFormulaDataRecord, LinearFormulaDataRecord

SCRIPT_LOCATION = "uds.translator.data_record.formula_data_record"


class TestLinearFormulaDataRecord:
    """Unit tests for `LinearFormulaDataRecord` class."""

    def setup_method(self):
        self.mock_formula_data_record = MagicMock(spec=LinearFormulaDataRecord)
        # patching
        self._patcher_abstract_data_record_init = patch(f"{SCRIPT_LOCATION}.AbstractDataRecord.__init__")
        self.mock_abstract_data_record_init = self._patcher_abstract_data_record_init.start()

    def teardown_method(self):
        self._patcher_abstract_data_record_init.stop()

    # __init__

    @pytest.mark.parametrize("name, length, factor, offset", [
        (Mock(), Mock(), Mock(), Mock()),
        ("Some name", 8, 0.5, -10),
    ])
    def test_init__mandatory_args(self, name, length, factor, offset):
        assert LinearFormulaDataRecord.__init__(self.mock_formula_data_record,
                                                name=name,
                                                length=length,
                                                factor=factor,
                                                offset=offset) is None
        assert self.mock_formula_data_record.factor == factor
        assert self.mock_formula_data_record.offset == offset
        self.mock_abstract_data_record_init.assert_called_once_with(name=name,
                                                                    length=length,
                                                                    children=tuple(),
                                                                    unit=None,
                                                                    min_occurrences=1,
                                                                    max_occurrences=1)

    @pytest.mark.parametrize("name, length, factor, offset, unit, min_occurrences, max_occurrences", [
        (Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()),
        ("Some name", 8, 0.5, -10, "C degrees", 1, 8),
    ])
    def test_init__all_args(self, name, length, factor, offset, unit, min_occurrences, max_occurrences):
        assert LinearFormulaDataRecord.__init__(self.mock_formula_data_record,
                                                name=name,
                                                length=length,
                                                factor=factor,
                                                offset=offset,
                                                unit=unit,
                                                min_occurrences=min_occurrences,
                                                max_occurrences=max_occurrences) is None
        assert self.mock_formula_data_record.factor == factor
        assert self.mock_formula_data_record.offset == offset
        self.mock_abstract_data_record_init.assert_called_once_with(name=name,
                                                                    length=length,
                                                                    children=tuple(),
                                                                    unit=unit,
                                                                    min_occurrences=min_occurrences,
                                                                    max_occurrences=max_occurrences)

    # factor

    def test_factor__get(self):
        self.mock_formula_data_record._LinearFormulaDataRecord__factor = Mock()
        assert (LinearFormulaDataRecord.factor.fget(self.mock_formula_data_record)
                == self.mock_formula_data_record._LinearFormulaDataRecord__factor)

    @pytest.mark.parametrize("value", [Mock(), "Some value"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_factor__set__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            LinearFormulaDataRecord.factor.fset(self.mock_formula_data_record, value)
        mock_isinstance.assert_called_once_with(value, (int, float))

    @pytest.mark.parametrize("value", [0, 0.])
    def test_factor__set__value_error(self, value):
        with pytest.raises(ValueError):
            LinearFormulaDataRecord.factor.fset(self.mock_formula_data_record, value)

    @pytest.mark.parametrize("value", [Mock(), 1])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_factor__set__valid(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        assert LinearFormulaDataRecord.factor.fset(self.mock_formula_data_record, value) is None
        assert self.mock_formula_data_record._LinearFormulaDataRecord__factor == value
        mock_isinstance.assert_called_once_with(value, (int, float))
    
    # offset
    
    def test_offset__get(self):
        self.mock_formula_data_record._LinearFormulaDataRecord__offset = Mock()
        assert (LinearFormulaDataRecord.offset.fget(self.mock_formula_data_record)
                == self.mock_formula_data_record._LinearFormulaDataRecord__offset)

    @pytest.mark.parametrize("value", [Mock(), "Some value"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_offset__set__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            LinearFormulaDataRecord.offset.fset(self.mock_formula_data_record, value)
        mock_isinstance.assert_called_once_with(value, (int, float))

    @pytest.mark.parametrize("value", [Mock(), 0])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_offset__set__valid(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        assert LinearFormulaDataRecord.offset.fset(self.mock_formula_data_record, value) is None
        assert self.mock_formula_data_record._LinearFormulaDataRecord__offset == value
        mock_isinstance.assert_called_once_with(value, (int, float))

    # min_physical_value

    @pytest.mark.parametrize("min_raw_value, max_raw_value, factor, offset", [
        (0, 255, 0.01, -0.5423),
        (0, 65123, -23, 987),
    ])
    def test_min_physical_value(self, min_raw_value, max_raw_value, factor, offset):
        min_physical_value = min((min_raw_value*factor + offset), (max_raw_value*factor + offset))
        self.mock_formula_data_record.min_raw_value = min_raw_value
        self.mock_formula_data_record.max_raw_value = max_raw_value
        self.mock_formula_data_record.factor = factor
        self.mock_formula_data_record.offset = offset
        assert LinearFormulaDataRecord.min_physical_value.fget(self.mock_formula_data_record) == min_physical_value

    # max_physical_value

    @pytest.mark.parametrize("min_raw_value, max_raw_value, factor, offset", [
        (0, 255, -0.01, 0.5423),
        (0, 65123, 23, -987),
    ])
    def test_max_physical_value(self, min_raw_value, max_raw_value, factor, offset):
        max_physical_value = max((min_raw_value*factor + offset), (max_raw_value*factor + offset))
        self.mock_formula_data_record.min_raw_value = min_raw_value
        self.mock_formula_data_record.max_raw_value = max_raw_value
        self.mock_formula_data_record.factor = factor
        self.mock_formula_data_record.offset = offset
        assert LinearFormulaDataRecord.max_physical_value.fget(self.mock_formula_data_record) == max_physical_value

    # get_physical_value

    @pytest.mark.parametrize("raw_value, factor, offset", [
        (0, 0.0004, 765),
        (987321, -52.21, -74.25),
    ])
    def test_get_physical_value(self, raw_value, factor, offset):
        self.mock_formula_data_record.factor = factor
        self.mock_formula_data_record.offset = offset
        assert LinearFormulaDataRecord.get_physical_value(self.mock_formula_data_record,
                                                          raw_value=raw_value) == raw_value*factor + offset
        self.mock_formula_data_record._validate_raw_value.assert_called_once_with(raw_value)

    # get_raw_value

    @pytest.mark.parametrize("physical_value", [Mock(), "Some value"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_get_raw_value__type_error(self, mock_isinstance, physical_value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            LinearFormulaDataRecord.get_raw_value(self.mock_formula_data_record,
                                                  physical_value=physical_value)
        mock_isinstance.assert_called_once_with(physical_value, (int, float))

    @pytest.mark.parametrize("min_raw_value, max_raw_value, physical_value, factor, offset", [
        (0, 255, -41, 1, -40),
        (0, 63, 6.3501, 0.1, 0),
    ])
    def test_get_raw_value__value_error(self, min_raw_value, max_raw_value, physical_value, factor, offset):
        self.mock_formula_data_record.min_raw_value = min_raw_value
        self.mock_formula_data_record.max_raw_value = max_raw_value
        self.mock_formula_data_record.factor = factor
        self.mock_formula_data_record.offset = offset
        with pytest.raises(ValueError):
            LinearFormulaDataRecord.get_raw_value(self.mock_formula_data_record,
                                                  physical_value=physical_value)

    @pytest.mark.parametrize("min_raw_value, max_raw_value, raw_value, physical_value, factor, offset", [
        (0, 255, 0, -40, 1, -40),
        (0, 63, 63, 6.3499, 0.1, 0),
        (0, 15, 7, 2, -0.25, 3.7),
    ])
    def test_get_raw_value__valid(self, min_raw_value, max_raw_value, raw_value, physical_value, factor, offset):
        self.mock_formula_data_record.min_raw_value = min_raw_value
        self.mock_formula_data_record.max_raw_value = max_raw_value
        self.mock_formula_data_record.factor = factor
        self.mock_formula_data_record.offset = offset
        assert LinearFormulaDataRecord.get_raw_value(self.mock_formula_data_record,
                                                     physical_value=physical_value) == raw_value


class TestCustomFormulaDataRecord:
    """Unit tests for `CustomFormulaDataRecord` class."""

    def setup_method(self):
        self.mock_formula_data_record = MagicMock(spec=CustomFormulaDataRecord)
        # patching
        self._patcher_abstract_data_record_init = patch(f"{SCRIPT_LOCATION}.AbstractDataRecord.__init__")
        self.mock_abstract_data_record_init = self._patcher_abstract_data_record_init.start()

    def teardown_method(self):
        self._patcher_abstract_data_record_init.stop()

    # __init__

    @pytest.mark.parametrize("name, length, encoding_formula, decoding_formula", [
        (Mock(), Mock(), Mock(), Mock()),
        ("Some name", 8, MagicMock(), MagicMock()),
    ])
    def test_init__mandatory_args(self, name, length, encoding_formula, decoding_formula):
        assert CustomFormulaDataRecord.__init__(self.mock_formula_data_record,
                                                name=name,
                                                length=length,
                                                encoding_formula=encoding_formula,
                                                decoding_formula=decoding_formula) is None
        assert self.mock_formula_data_record.encoding_formula == encoding_formula
        assert self.mock_formula_data_record.decoding_formula == decoding_formula
        self.mock_abstract_data_record_init.assert_called_once_with(name=name,
                                                                    length=length,
                                                                    children=tuple(),
                                                                    unit=None,
                                                                    min_occurrences=1,
                                                                    max_occurrences=1)

    @pytest.mark.parametrize("name, length, encoding_formula, decoding_formula, unit, min_occurrences, max_occurrences", [
        (Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()),
        ("Some name", 8, MagicMock(), MagicMock(), "m/s^2", 1, 8),
    ])
    def test_init__all_args(self, name, length, encoding_formula, decoding_formula, unit, min_occurrences, max_occurrences):
        assert CustomFormulaDataRecord.__init__(self.mock_formula_data_record,
                                                name=name,
                                                length=length,
                                                encoding_formula=encoding_formula,
                                                decoding_formula=decoding_formula,
                                                unit=unit,
                                                min_occurrences=min_occurrences,
                                                max_occurrences=max_occurrences) is None
        assert self.mock_formula_data_record.encoding_formula == encoding_formula
        assert self.mock_formula_data_record.decoding_formula == decoding_formula
        self.mock_abstract_data_record_init.assert_called_once_with(name=name,
                                                                    length=length,
                                                                    children=tuple(),
                                                                    unit=unit,
                                                                    min_occurrences=min_occurrences,
                                                                    max_occurrences=max_occurrences)
        
    # encoding_formula
    
    def test_encoding_formula__get(self):
        self.mock_formula_data_record._CustomFormulaDataRecord__encoding_formula = Mock()
        assert (CustomFormulaDataRecord.encoding_formula.fget(self.mock_formula_data_record)
                == self.mock_formula_data_record._CustomFormulaDataRecord__encoding_formula)

    @pytest.mark.parametrize("value", [Mock(), "Some value"])
    @patch(f"{SCRIPT_LOCATION}.callable")
    def test_encoding_formula__set__type_error(self, mock_callable, value):
        mock_callable.return_value = False
        with pytest.raises(TypeError):
            CustomFormulaDataRecord.encoding_formula.fset(self.mock_formula_data_record, value)
        mock_callable.assert_called_once_with(value)

    @pytest.mark.parametrize("value", [Mock(), "Some value"])
    @patch(f"{SCRIPT_LOCATION}.callable")
    def test_encoding_formula__set__valid(self, mock_callable, value):
        mock_callable.return_value = True
        assert CustomFormulaDataRecord.encoding_formula.fset(self.mock_formula_data_record, value) is None
        assert self.mock_formula_data_record._CustomFormulaDataRecord__encoding_formula == value
        mock_callable.assert_called_once_with(value)

    # decoding_formula

    def test_decoding_formula__get(self):
        self.mock_formula_data_record._CustomFormulaDataRecord__decoding_formula = Mock()
        assert (CustomFormulaDataRecord.decoding_formula.fget(self.mock_formula_data_record)
                == self.mock_formula_data_record._CustomFormulaDataRecord__decoding_formula)

    @pytest.mark.parametrize("value", [Mock(), "Some value"])
    @patch(f"{SCRIPT_LOCATION}.callable")
    def test_decoding_formula__set__type_error(self, mock_callable, value):
        mock_callable.return_value = False
        with pytest.raises(TypeError):
            CustomFormulaDataRecord.decoding_formula.fset(self.mock_formula_data_record, value)
        mock_callable.assert_called_once_with(value)

    @pytest.mark.parametrize("value", [Mock(), "Some value"])
    @patch(f"{SCRIPT_LOCATION}.callable")
    def test_decoding_formula__set__valid(self, mock_callable, value):
        mock_callable.return_value = True
        assert CustomFormulaDataRecord.decoding_formula.fset(self.mock_formula_data_record, value) is None
        assert self.mock_formula_data_record._CustomFormulaDataRecord__decoding_formula == value
        mock_callable.assert_called_once_with(value)

    # get_physical_value

    @pytest.mark.parametrize("raw_value", [Mock(), "Some value"])
    def test_get_physical_value(self, raw_value):
        assert (CustomFormulaDataRecord.get_physical_value(self.mock_formula_data_record, raw_value=raw_value)
                == self.mock_formula_data_record.decoding_formula.return_value)
        self.mock_formula_data_record._validate_raw_value.assert_called_once_with(raw_value)
        self.mock_formula_data_record.decoding_formula.assert_called_once_with(raw_value)

    # get_raw_value

    @pytest.mark.parametrize("physical_value", [Mock(), "Some value"])
    def test_get_raw_value(self, physical_value):
        assert (CustomFormulaDataRecord.get_raw_value(self.mock_formula_data_record, physical_value=physical_value)
                == self.mock_formula_data_record.encoding_formula.return_value)
        self.mock_formula_data_record.encoding_formula.assert_called_once_with(physical_value)


@pytest.mark.integration
class TestLinearFormulaDataRecordIntegration:
    """Integration tests for `LinearFormulaDataRecord` class."""

    def setup_class(self) -> None:
        self.fahrenheit_to_celsius_data_record = LinearFormulaDataRecord(name="Celsius Temperature",
                                                                         length=16,
                                                                         factor=5 / 9,
                                                                         offset=-160 / 9)

    # get_raw_value

    @pytest.mark.parametrize("physical_value, raw_value", [
        (0, 32),
        (-17.8, 0),
        (36390.6, 0xFFFF),
    ])
    def test_get_raw_value(self, physical_value, raw_value):
        assert self.fahrenheit_to_celsius_data_record.get_raw_value(physical_value) == raw_value

    @pytest.mark.parametrize("physical_value", [-18.1,36390.9,])
    def test_get_raw_value__value_error(self, physical_value):
        with pytest.raises(ValueError):
            self.fahrenheit_to_celsius_data_record.get_raw_value(physical_value)

    # get_physical_value

    @pytest.mark.parametrize("physical_value, raw_value", [
        (0, 32),
        (-17.7777, 0),
        (36390.5555, 0xFFFF),
    ])
    def test_get_raw_value_2(self, physical_value, raw_value):
        assert (round(self.fahrenheit_to_celsius_data_record.get_physical_value(raw_value), 3)
                == round(physical_value, 3))

    # two conversions

    @pytest.mark.parametrize("raw_value", [0, 23546, 65535])
    def test_two_conversions(self, raw_value):
        physical_value = self.fahrenheit_to_celsius_data_record.get_physical_value(raw_value)
        assert self.fahrenheit_to_celsius_data_record.get_raw_value(physical_value) == raw_value


@pytest.mark.integration
class TestCustomFormulaDataRecordIntegration:
    """Integration tests for `CustomFormulaDataRecord` class."""

    def setup_class(self) -> None:
        def encoding_formula(physical_value: float) -> int:
            if physical_value >= 0:
                raw_value = physical_value*100
            else:
                raw_value = 128 + ((physical_value + 1.28) * 100)
            return int(round(raw_value,0))

        def decoding_formula(raw_value: int) -> float:
            physical_value = (raw_value & 0x7F) / 100.
            if raw_value >= 128:
                physical_value -= 1.28
            return physical_value

        self.sensor_entries = CustomFormulaDataRecord(name="Acceleration",
                                                      length=8,
                                                      encoding_formula=encoding_formula,
                                                      decoding_formula=decoding_formula,
                                                      min_occurrences=4,
                                                      max_occurrences=4)

    # get_raw_value

    @pytest.mark.parametrize("physical_value, raw_value", [
        (0, 0),
        (-1.281, 0x80),
        (1.2699, 0x7F)
    ])
    def test_get_raw_value(self, physical_value, raw_value):
        assert self.sensor_entries.get_raw_value(physical_value) == raw_value

    # get_physical_value

    @pytest.mark.parametrize("physical_value, raw_value", [
        (0, 0),
        (-1.28, 0x80),
        (1.27, 0x7F)
    ])
    def test_get_physical_value(self, physical_value, raw_value):
        assert self.sensor_entries.get_physical_value(raw_value) == physical_value

    # two conversions

    @pytest.mark.parametrize("raw_value", [0, 52, 255])
    def test_two_conversions_1(self, raw_value):
        physical_value = self.sensor_entries.get_physical_value(raw_value)
        assert self.sensor_entries.get_raw_value(physical_value) == raw_value
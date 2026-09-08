from unittest.mock import Mock, patch

import pytest

from uds.translator.data_record.raw_data_record import RawDataRecord

SCRIPT_LOCATION = "uds.translator.data_record.raw_data_record"


class TestRawDataRecord:

    def setup_method(self):
        self.mock_data_record = Mock(spec=RawDataRecord)
        # patching
        self._patcher_deepcopy = patch(f"{SCRIPT_LOCATION}.deepcopy")
        self.mock_deepcopy = self._patcher_deepcopy.start()

    def teardown_method(self):
        self._patcher_deepcopy.stop()

    # __init__

    @pytest.mark.parametrize("name, length", [
        ("TestRawDataRecord", 8),
        (Mock(), Mock()),
    ])
    @patch(f"{SCRIPT_LOCATION}.AbstractDataRecord.__init__")
    def test_init__mandatory_args(self, mock_abstract_data_record_class, name, length):
        assert RawDataRecord.__init__(self.mock_data_record, name, length) is None
        mock_abstract_data_record_class.assert_called_once_with(name=name,
                                                                length=length,
                                                                children=tuple(),
                                                                unit=None,
                                                                min_occurrences=1,
                                                                max_occurrences=1,
                                                                enforce_reoccurring=False)

    @pytest.mark.parametrize("name, length, children, unit, min_occurrences, max_occurrences, enforce_reoccurring", [
        ("TestRawDataRecord", 8, [Mock(), Mock()], "km/h", 0, None, True),
        (Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()),
    ])
    @patch(f"{SCRIPT_LOCATION}.AbstractDataRecord.__init__")
    def test_init__all_args(self, mock_abstract_data_record_class,
                            name, length, children, unit, min_occurrences, max_occurrences, enforce_reoccurring):
        assert RawDataRecord.__init__(self.mock_data_record,
                                      name=name,
                                      length=length,
                                      children=children,
                                      unit=unit,
                                      min_occurrences=min_occurrences,
                                      max_occurrences=max_occurrences,
                                      enforce_reoccurring=enforce_reoccurring) is None
        mock_abstract_data_record_class.assert_called_once_with(name=name,
                                                                length=length,
                                                                children=children,
                                                                unit=unit,
                                                                min_occurrences=min_occurrences,
                                                                max_occurrences=max_occurrences,
                                                                enforce_reoccurring=enforce_reoccurring)

    @patch(f"{SCRIPT_LOCATION}.RawDataRecord.__init__")
    def test_deepcopy(self, mock_init):
        memo = {}
        output = RawDataRecord.__deepcopy__(self.mock_data_record, memo)
        assert output == memo[id(self.mock_data_record)]
        mock_init.assert_called_once_with(
            output,
            name=self.mock_data_record.name,
            length=self.mock_data_record.length,
            children=self.mock_deepcopy.return_value,
            min_occurrences=self.mock_data_record.min_occurrences,
            max_occurrences=self.mock_data_record.max_occurrences,
            unit=self.mock_data_record.unit,
            enforce_reoccurring=self.mock_data_record.enforce_reoccurring)
        self.mock_deepcopy.assert_called_once_with(self.mock_data_record.children, memo=memo)

    # get_physical_value

    @pytest.mark.parametrize(
        "value", [0, 0xFF, Mock()]
    )
    def test_get_physical_value(self, value):
        assert RawDataRecord.get_physical_value(self.mock_data_record, value) == value
        self.mock_data_record._validate_raw_value.assert_called_once_with(value)

    # get_raw_value

    @pytest.mark.parametrize(
        "value", [0, 0xFF, Mock()]
    )
    def test_get_raw_value(self, value):
        assert RawDataRecord.get_raw_value(self.mock_data_record, value) == value
        self.mock_data_record._validate_raw_value.assert_called_once_with(value)


@pytest.mark.integration
class TestRawDataRecordIntegration:
    """Integration tests for `RawDataRecord` class."""

    def setup_class(self):
        self.dtc = RawDataRecord(name="DTC",
                                 length=24,
                                 min_occurrences=0,
                                 max_occurrences=1)

    # get_physical_values

    @pytest.mark.parametrize("value", [0, 0xFFFFFF])
    def test_get_physical_values__error(self, value):
        assert self.dtc.is_reoccurring is False
        with pytest.raises(RuntimeError):
            self.dtc.get_physical_values(value)

    # get_physical_value

    @pytest.mark.parametrize("value", [0, 0xFFFFFF, 0xA1B2C3])
    def test_get_physical_value(self, value):
        assert self.dtc.get_physical_value(value) == value

    # get_raw_value

    @pytest.mark.parametrize("value", [0, 0xFFFFFF, 0xA1B2C3])
    def test_get_raw_value(self, value):
        assert self.dtc.get_raw_value(value) == value

    # get_occurrence_info

    @pytest.mark.parametrize("value, expected_output", [
        (0, {
            "name": "DTC",
            "length": 24,
            "raw_value": 0,
            "physical_value": 0,
            "children": tuple(),
            "unit": None,
        }),
        (0xFFFFFF, {
            "name": "DTC",
            "length": 24,
            "raw_value": 0xFFFFFF,
            "physical_value": 0xFFFFFF,
            "children": tuple(),
            "unit": None,
        }),
        (0xA1B2C3, {
            "name": "DTC",
            "length": 24,
            "raw_value": 0xA1B2C3,
            "physical_value": 0xA1B2C3,
            "children": tuple(),
            "unit": None,
        }),
    ])
    def test_get_occurrence_info(self, value, expected_output):
        assert self.dtc.get_occurrence_info(value) == expected_output

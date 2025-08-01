import pytest
from mock import Mock, patch

from uds.database.data_record.raw_data_record import RawDataRecord

SCRIPT_LOCATION = "uds.database.data_record.raw_data_record"


class TestRawDataRecord:

    def setup_method(self):
        self.mock_data_record = Mock(spec=RawDataRecord)

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
                                                                max_occurrences=1)

    @pytest.mark.parametrize("name, length, children, unit, min_occurrences, max_occurrences", [
        ("TestRawDataRecord", 8, [Mock(), Mock()], "km/h", 0, None),
        (Mock(), Mock(), Mock(), Mock(), Mock(), Mock()),
    ])
    @patch(f"{SCRIPT_LOCATION}.AbstractDataRecord.__init__")
    def test_init__all_args(self, mock_abstract_data_record_class,
                            name, length, children, unit, min_occurrences, max_occurrences):
        assert RawDataRecord.__init__(self.mock_data_record,
                                      name=name,
                                      length=length,
                                      children=children,
                                      unit=unit,
                                      min_occurrences=min_occurrences,
                                      max_occurrences=max_occurrences) is None
        mock_abstract_data_record_class.assert_called_once_with(name=name,
                                                                length=length,
                                                                children=children,
                                                                unit=unit,
                                                                min_occurrences=min_occurrences,
                                                                max_occurrences=max_occurrences)

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
    """Integration tests for the RawDataRecord class."""

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
            "raw_value": 0,
            "physical_value": 0,
            "children": tuple()
        }),
        (0xFFFFFF, {
            "name": "DTC",
            "raw_value": 0xFFFFFF,
            "physical_value": 0xFFFFFF,
            "children": tuple()
        }),
        (0xA1B2C3, {
            "name": "DTC",
            "raw_value": 0xA1B2C3,
            "physical_value": 0xA1B2C3,
            "children": tuple()
        }),
    ])
    def test_get_occurrence_info(self, value, expected_output):
        assert self.dtc.get_occurrence_info(value) == expected_output

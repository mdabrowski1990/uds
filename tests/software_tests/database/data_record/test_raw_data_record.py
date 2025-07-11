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
                                                                min_occurrences=1,
                                                                max_occurrences=1)

    @pytest.mark.parametrize("name, length, children, min_occurrences, max_occurrences", [
        ("TestRawDataRecord", 8, [Mock(), Mock()], 0, None),
        (Mock(), Mock(), Mock(), Mock(), Mock()),
    ])
    @patch(f"{SCRIPT_LOCATION}.AbstractDataRecord.__init__")
    def test_init__all_args(self, mock_abstract_data_record_class,
                            name, length, children, min_occurrences, max_occurrences):
        assert RawDataRecord.__init__(self.mock_data_record,
                                      name=name,
                                      length=length,
                                      children=children,
                                      min_occurrences=min_occurrences,
                                      max_occurrences=max_occurrences) is None
        mock_abstract_data_record_class.assert_called_once_with(name=name,
                                                                length=length,
                                                                children=children,
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

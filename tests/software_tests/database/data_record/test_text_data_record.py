import pytest
from mock import Mock, patch

from uds.database.data_record.text_data_record import TextTableDataRecord

SCRIPT_LOCATION = "uds.database.data_record.raw_data_record"

class TestTextTableDataRecord:

    def setup_method(self):
        self.mock_data_record = Mock(spec=TextTableDataRecord)

    @pytest.mark.parametrize(
        "name, length", [
            ("TestTextDataRecord", 32),
            (Mock(), Mock()),
        ]
    )
    @patch(f"{SCRIPT_LOCATION}.RawDataRecord.__init__")
    def test_init__valid(self, mock_raw_data, name, length):
        assert TextTableDataRecord.__init__(self.mock_data_record, name, length) is None
        mock_raw_data.assert_called_once_with(name, length)
        assert self.mock_data_record.length == length

    def test_length_getter(self):
        self.mock_data_record._TextTableDataRecord__length = Mock()
        assert TextTableDataRecord.length.fget(self.mock_data_record) == self.mock_data_record._TextTableDataRecord__length

    @pytest.mark.parametrize(
        "value, expected_value", [("Text", 32), ("Foobar", 48)]
    )
    def test_length_setter_valid(self, value, expected_value):
        TextTableDataRecord.length.fset(self.mock_data_record, value)
        assert self.mock_data_record._TextTableDataRecord__length == expected_value

    @pytest.mark.parametrize(
        "value", [23, None]
    )
    def test_length_setter_type_error(self, value):
        with pytest.raises(AttributeError):
            TextTableDataRecord.length.fset(self.mock_data_record, value)
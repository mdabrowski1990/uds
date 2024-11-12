import pytest
from mock import patch

from uds.database.data_record.raw_data_record import RawDataRecord

SCRIPT_LOCATION = "uds.database.data_record.raw_data_record"


class TestRawDataRecord:

    def setup_method(self):
        self.name = "TestRawDataRecord"
        self.length = 8
        self.raw_data_record = RawDataRecord(self.name, self.length)

    # __init__

    def test_init_valid(self):
        assert self.raw_data_record.name == self.name
        assert self.raw_data_record.length == self.length

    def test_init_type_error_for_name(self):
        with pytest.raises(TypeError):
            RawDataRecord(123, self.length)

    def test_init_value_error_for_length(self):
        with pytest.raises(ValueError):
            RawDataRecord(self.name, -5)

    def test_init_type_error_for_length(self):
        with pytest.raises(TypeError):
            RawDataRecord(self.name, "eight")

    # length

    def test_length_getter(self):
        assert self.raw_data_record.length == self.length

    def test_length_setter_valid(self):
        self.raw_data_record.length = 16
        assert self.raw_data_record.length == 16

    def test_length_setter_type_error(self):
        with pytest.raises(TypeError):
            self.raw_data_record.length = "sixteen"

    def test_length_setter_value_error(self):
        with pytest.raises(ValueError):
            self.raw_data_record.length = -10

    # is_reoccurring

    def test_is_reoccurring(self):
        assert self.raw_data_record.is_reoccurring is False

    # min_occurrences

    def test_min_occurrences(self):
        assert self.raw_data_record.min_occurrences == 1

    # max_occurrences

    def test_max_occurrences(self):
        assert self.raw_data_record.max_occurrences == 1

    # contains

    def test_contains(self):
        assert self.raw_data_record.contains == ()

    # decode

    @patch(f"{SCRIPT_LOCATION}.DecodedDataRecord")
    def test_decode(self, mock_decoded_data_record):
        raw_value = 42
        result = self.raw_data_record.decode(raw_value)
        mock_decoded_data_record.assert_called_once_with(
            name=self.name,
            raw_value=raw_value,
            physical_value=raw_value
        )
        assert result == mock_decoded_data_record.return_value

    # encode

    def test_encode(self):
        physical_value = 42
        assert self.raw_data_record.encode(physical_value) == physical_value

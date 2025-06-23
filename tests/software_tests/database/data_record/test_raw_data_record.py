import pytest
from mock import Mock, patch

from uds.database.data_record.raw_data_record import RawDataRecord

SCRIPT_LOCATION = "uds.database.data_record.raw_data_record"


class TestRawDataRecord:

    def setup_method(self):
        self.mock_data_record = Mock(spec=RawDataRecord)

    # __init__

    @pytest.mark.parametrize(
        "name, length", [
            ("TestRawDataRecord", 8),
            (Mock(), Mock()),
        ]
    )
    @patch(f"{SCRIPT_LOCATION}.AbstractDataRecord.__init__")
    def test_init__valid(self, mock_abstract, name, length):
        assert RawDataRecord.__init__(self.mock_data_record, name, length) is None
        mock_abstract.assert_called_once_with(name)
        assert self.mock_data_record.length == length

    # length

    def test_length_getter(self):
        self.mock_data_record._RawDataRecord__length = Mock()
        assert RawDataRecord.length.fget(self.mock_data_record) == self.mock_data_record._RawDataRecord__length

    @pytest.mark.parametrize(
        "value", [1, 8]
    )
    def test_length_setter_valid(self, value):
        RawDataRecord.length.fset(self.mock_data_record, value)
        assert self.mock_data_record._RawDataRecord__length == value

    @pytest.mark.parametrize(
        "value", ["test", None]
    )
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_length_setter_type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            RawDataRecord.length.fset(self.mock_data_record, value)
        mock_isinstance.assert_called_once_with(value, int)

    @pytest.mark.parametrize(
        "value", [0, -1]
    )
    def test_length_setter_value_error(self, value):
        with pytest.raises(ValueError):
            RawDataRecord.length.fset(self.mock_data_record, value)

    # max_raw_value

    @pytest.mark.parametrize(
        "length, value", [
            (2, 3),
            (5, 31),
            (8, 255),
        ]
    )
    def test_max_raw_value_getter(self, length, value):
        raw_data_record = RawDataRecord("TestRawDataRecord", length)
        assert raw_data_record.max_raw_value == value

    # min_occurrences

    def test_min_occurrences_getter(self):
        assert RawDataRecord.min_occurrences.fget(self.mock_data_record) == 1

    # max_occurrences

    def test_max_occurrences_getter(self):
        assert RawDataRecord.max_occurrences.fget(self.mock_data_record) == 1

    # contains

    def test_contains_getter(self):
        assert RawDataRecord.children.fget(self.mock_data_record) == ()

    # decode

    @pytest.mark.parametrize(
        "value", [1, 4]
    )
    @patch(f"{SCRIPT_LOCATION}.DecodedDataRecord")
    def test_decode(self, mock_decoded_data_record, value):
        self.mock_data_record.max_raw_value = 8
        assert RawDataRecord.decode(self.mock_data_record, value) == mock_decoded_data_record.return_value
        mock_decoded_data_record.assert_called_once_with(
            name=self.mock_data_record.name,
            raw_value=value,
            physical_value=value
        )

    @pytest.mark.parametrize(
        "value", ["test", None]
    )
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_decode_type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            RawDataRecord.decode(self.mock_data_record, value)
        mock_isinstance.assert_called_once_with(value, int)

    @pytest.mark.parametrize(
        "value, max_raw_value", [
            (-1, 2),
            (3, 2),
            (16, 6),
        ]
    )
    def test_decode_value_error(self, value, max_raw_value):
        self.mock_data_record.max_raw_value = max_raw_value
        with pytest.raises(ValueError):
            RawDataRecord.decode(self.mock_data_record, value)

    # encode

    @pytest.mark.parametrize(
        "value, max_raw_value", [
            (0, 2),
            (3, 3),
            (16, 16),
        ]
    )
    def test_encode(self, value, max_raw_value):
        self.mock_data_record.max_raw_value = max_raw_value
        assert RawDataRecord.encode(self.mock_data_record, value) == value

    @pytest.mark.parametrize(
        "value", ["test", None]
    )
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_encode_type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            RawDataRecord.encode(self.mock_data_record, value)
        mock_isinstance.assert_called_once_with(value, int)

    @pytest.mark.parametrize(
        "value, max_raw_value", [
            (-1, 2),
            (3, 2),
            (16, 6),
        ]
    )
    def test_encode_value_error(self, value, max_raw_value):
        self.mock_data_record.max_raw_value = max_raw_value
        with pytest.raises(ValueError):
            RawDataRecord.encode(self.mock_data_record, value)

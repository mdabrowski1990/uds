import pytest
from mock import Mock, patch

from uds.database.data_record.text_data_record import TextTableDataRecord

SCRIPT_LOCATION = "uds.database.data_record.text_data_record"

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

    def test_mapping_getter(self):
        self.mock_data_record._TextTableDataRecord__mapping = Mock()
        assert TextTableDataRecord.mapping.fget(self.mock_data_record) == self.mock_data_record._TextTableDataRecord__mapping

    def test_reversed_mapping_getter(self):
        self.mock_data_record._TextTableDataRecord__reversed_mapping = Mock()
        assert TextTableDataRecord.reversed_mapping.fget(self.mock_data_record) == self.mock_data_record._TextTableDataRecord__reversed_mapping

    @pytest.mark.parametrize(
        "mapping_dict, reversed_dict", [
            ({1: "foo", 2: "bar"}, {"foo": 1, "bar": 2}),
            ({"foo": 1, "bar": 2}, {1: "foo", 2: "bar"}),
            ({1: 1, 2: 2}, {1: 1, 2: 2})
        ]
    )
    def test_mapping_setter_valid(self, mapping_dict, reversed_dict):
        TextTableDataRecord.mapping.fset(self.mock_data_record, mapping_dict)
        assert self.mock_data_record._TextTableDataRecord__mapping == mapping_dict
        assert self.mock_data_record._TextTableDataRecord__reversed_mapping == reversed_dict

    @pytest.mark.parametrize(
        "raw_value, expected_raw_value, mapping_dict", [(1, "foo", {1: "foo"}), (1, 1, {2: "foo"})]
    )
    @patch(f"{SCRIPT_LOCATION}.DecodedDataRecord")
    def test_decode(self, mock_decoded_data_record, raw_value, expected_raw_value, mapping_dict):
        self.mock_data_record.mapping = mapping_dict
        assert TextTableDataRecord.decode(self.mock_data_record, raw_value) == mock_decoded_data_record.return_value
        mock_decoded_data_record.assert_called_once_with(
            name=self.mock_data_record.name,
            raw_value=expected_raw_value,
            physical_value=raw_value
        )

    @pytest.mark.parametrize(
        "physical_value, expected_physical_value", [
            (1, 1), (2, 2), ("foo", 1)
        ]
    )
    def test_encode(self, physical_value, expected_physical_value):
        self.mock_data_record.reversed_mapping = {"foo": 1}
        assert TextTableDataRecord.encode(self.mock_data_record, physical_value) == expected_physical_value

    @pytest.mark.parametrize(
        "physical_value", ["bar", "rab"]
    )
    def test_encode_key_error(self, physical_value):
        self.mock_data_record.reversed_mapping = {"foo": 1}
        with pytest.raises(KeyError):
            TextTableDataRecord.encode(self.mock_data_record, physical_value)

    @pytest.mark.parametrize(
        "physical_value", [[1, 3], 1.34, None]
    )
    def test_encode_type_error(self, physical_value):
        self.mock_data_record.reversed_mapping = {"foo": 1}
        with pytest.raises(TypeError):
            TextTableDataRecord.encode(self.mock_data_record, physical_value)
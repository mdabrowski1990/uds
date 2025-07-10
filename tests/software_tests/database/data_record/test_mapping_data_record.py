import pytest
from mock import Mock, patch

from uds.database.data_record.mapping_data_record import MappingDataRecord

SCRIPT_LOCATION = "uds.database.data_record.mapping_data_record"

class TestTextTableDataRecord:

    def setup_method(self):
        self.mock_data_record = Mock(spec=MappingDataRecord)

    @pytest.mark.parametrize(
        "name, length, mapping", [
            ("TestMappingDataRecord", 32, {1: "foo", 2: "bar"}),
            (Mock(), Mock(), Mock()),
        ]
    )
    @patch(f"{SCRIPT_LOCATION}.RawDataRecord.__init__")
    def test_init__valid(self, mock_raw_data, name, length, mapping):
        assert MappingDataRecord.__init__(self.mock_data_record, name, length, mapping) is None
        mock_raw_data.assert_called_once_with(name, length)
        assert self.mock_data_record.length == length
        assert self.mock_data_record.mapping == mapping

    def test_mapping_getter(self):
        self.mock_data_record._MappingDataRecord__mapping = Mock()
        assert MappingDataRecord.mapping.fget(self.mock_data_record) == self.mock_data_record._MappingDataRecord__mapping

    def test_reversed_mapping_getter(self):
        self.mock_data_record._MappingDataRecord__reversed_mapping = Mock()
        assert MappingDataRecord.reversed_mapping.fget(self.mock_data_record) == self.mock_data_record._MappingDataRecord__reversed_mapping

    @pytest.mark.parametrize(
        "mapping_dict, reversed_dict", [
            ({1: "foo", 2: "bar"}, {"foo": 1, "bar": 2}),
            ({"foo": 1, "bar": 2}, {1: "foo", 2: "bar"}),
            ({1: 1, 2: 2}, {1: 1, 2: 2})
        ]
    )
    def test_mapping_setter_valid(self, mapping_dict, reversed_dict):
        MappingDataRecord.mapping.fset(self.mock_data_record, mapping_dict)
        assert self.mock_data_record._MappingDataRecord__mapping == mapping_dict
        assert self.mock_data_record._MappingDataRecord__reversed_mapping == reversed_dict

    @pytest.mark.parametrize(
        "raw_value, expected_physical_value, mapping_dict", [(1, "foo", {1: "foo"}), (1, 1, {2: "foo"})]
    )
    @patch(f"{SCRIPT_LOCATION}.DecodedDataRecord")
    def test_decode(self, mock_decoded_data_record, raw_value, expected_physical_value, mapping_dict):
        self.mock_data_record.mapping = mapping_dict
        assert MappingDataRecord.decode(self.mock_data_record, raw_value) == mock_decoded_data_record.return_value
        mock_decoded_data_record.assert_called_once_with(
            name=self.mock_data_record.name,
            raw_value=raw_value,
            physical_value=expected_physical_value
        )

    @pytest.mark.parametrize(
        "physical_value, expected_physical_value", [
            (1, 1), (2, 2), ("foo", 1)
        ]
    )
    def test_encode(self, physical_value, expected_physical_value):
        self.mock_data_record.reversed_mapping = {"foo": 1}
        assert MappingDataRecord.encode(self.mock_data_record, physical_value) == expected_physical_value

    @pytest.mark.parametrize(
        "physical_value", ["bar", "rab"]
    )
    def test_encode_key_error(self, physical_value):
        self.mock_data_record.reversed_mapping = {"foo": 1}
        with pytest.raises(KeyError):
            MappingDataRecord.encode(self.mock_data_record, physical_value)

    @pytest.mark.parametrize(
        "physical_value", [[1, 3], 1.34, None]
    )
    def test_encode_type_error(self, physical_value):
        self.mock_data_record.reversed_mapping = {"foo": 1}
        with pytest.raises(TypeError):
            MappingDataRecord.encode(self.mock_data_record, physical_value)
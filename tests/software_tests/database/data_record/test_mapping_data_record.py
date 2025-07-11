import pytest
from mock import Mock, patch

from uds.database.data_record.mapping_data_record import MappingDataRecord, MappingProxyType

SCRIPT_LOCATION = "uds.database.data_record.mapping_data_record"


class TestMappingDataRecord:

    def setup_method(self):
        self.mock_data_record = Mock(spec=MappingDataRecord,
                                     min_raw_value=0)
        self._patcher_warn = patch(f"{SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()

    def teardown_method(self):
        self._patcher_warn.stop()

    # __init__

    @pytest.mark.parametrize("name, length, values_mapping", [
        ("TestRawDataRecord", 8, {1: "A", 2: "B", 3: "C"}),
        (Mock(), Mock(), Mock()),
    ])
    @patch(f"{SCRIPT_LOCATION}.AbstractDataRecord.__init__")
    def test_init__mandatory_args(self, mock_abstract_data_record_class, name, length, values_mapping):
        assert MappingDataRecord.__init__(self.mock_data_record, name, length, values_mapping) is None
        mock_abstract_data_record_class.assert_called_once_with(name=name,
                                                                length=length,
                                                                children=tuple(),
                                                                min_occurrences=1,
                                                                max_occurrences=1)
        assert self.mock_data_record.values_mapping == values_mapping

    @pytest.mark.parametrize("name, length, values_mapping, children, min_occurrences, max_occurrences", [
        ("TestRawDataRecord", 8, {1: "A", 2: "B", 3: "C"}, [Mock(), Mock()], 0, None),
        (Mock(), Mock(), Mock(), Mock(), Mock(), Mock()),
    ])
    @patch(f"{SCRIPT_LOCATION}.AbstractDataRecord.__init__")
    def test_init__all_args(self, mock_abstract_data_record_class,
                            name, length, values_mapping, children, min_occurrences, max_occurrences):
        assert MappingDataRecord.__init__(self.mock_data_record,
                                          name=name,
                                          length=length,
                                          values_mapping=values_mapping,
                                          children=children,
                                          min_occurrences=min_occurrences,
                                          max_occurrences=max_occurrences) is None
        mock_abstract_data_record_class.assert_called_once_with(name=name,
                                                                length=length,
                                                                children=children,
                                                                min_occurrences=min_occurrences,
                                                                max_occurrences=max_occurrences)
        assert self.mock_data_record.values_mapping == values_mapping

    # values_mapping

    def test_values_mapping__get(self):
        self.mock_data_record._MappingDataRecord__values_mapping = Mock()
        assert (MappingDataRecord.values_mapping.fget(self.mock_data_record)
                == self.mock_data_record._MappingDataRecord__values_mapping)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_values_mapping__type_error(self, mock_isinstance):
        mock_isinstance.return_value = False
        mock_value = Mock()
        with pytest.raises(TypeError):
            MappingDataRecord.values_mapping.fset(self.mock_data_record, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, dict)

    @pytest.mark.parametrize("max_raw_value, mapping_value", [
        (1, {0: "No", "1": "Yes"}),
        (3, {4: "ECU#4"}),
    ])
    def test_values_mapping__value_error(self, max_raw_value, mapping_value):
        self.mock_data_record.max_raw_value = max_raw_value
        with pytest.raises(ValueError):
            MappingDataRecord.values_mapping.fset(self.mock_data_record, mapping_value)

    @pytest.mark.parametrize("max_raw_value, mapping_value", [
        (1, {0: "No", 1: "Yes"}),
        (3, {i: f"ECU#{i}" for i in range(4)}),
    ])
    def test_values_mapping__valid(self, max_raw_value, mapping_value):
        self.mock_data_record.max_raw_value = max_raw_value
        assert MappingDataRecord.values_mapping.fset(self.mock_data_record, mapping_value) is None
        assert isinstance(self.mock_data_record._MappingDataRecord__values_mapping, MappingProxyType)
        assert isinstance(self.mock_data_record._MappingDataRecord__labels_mapping, MappingProxyType)
        for key, value in mapping_value.items():
            assert self.mock_data_record._MappingDataRecord__values_mapping[key] == value
            assert self.mock_data_record._MappingDataRecord__labels_mapping[value] == key

    # labels_mapping

    def test_labels_mapping__get(self):
        self.mock_data_record._MappingDataRecord__labels_mapping = Mock()
        assert (MappingDataRecord.labels_mapping.fget(self.mock_data_record)
                == self.mock_data_record._MappingDataRecord__labels_mapping)

    # get_physical_value

    @pytest.mark.parametrize("raw_value, values_mapping", [
        (0, {0: "foo", 1: "bar"}),
        (3, {i: Mock() for i in range(7)})
    ])
    def test_get_physical_value__from_values_mapping(self, raw_value, values_mapping):
        self.mock_data_record.values_mapping = values_mapping
        assert MappingDataRecord.get_physical_value(self.mock_data_record, raw_value) == values_mapping[raw_value]
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("raw_value, values_mapping", [
        (0, {1: "foo", 2: "bar"}),
        (3, {i: Mock() for i in range(4, 13)})
    ])
    @patch(f"{SCRIPT_LOCATION}.RawDataRecord.get_physical_value")
    def test_get_physical_value__not_in_values_mapping(self, mock_get_physical_value, raw_value, values_mapping):
        self.mock_data_record.values_mapping = values_mapping
        assert MappingDataRecord.get_physical_value(self.mock_data_record, raw_value) == mock_get_physical_value.return_value
        mock_get_physical_value.assert_called_once_with(raw_value)
        self.mock_warn.assert_called_once()

    # get_raw_value

    @pytest.mark.parametrize("physical_value, labels_mapping", [
        ("foo", {"foo": 0, "bar": 1}),
        ("ECU#4", {f"ECU#{i}": i for i in range(7)})
    ])
    def test_get_raw_value__from_labels_mapping(self, physical_value, labels_mapping):
        self.mock_data_record.labels_mapping = labels_mapping
        assert MappingDataRecord.get_raw_value(self.mock_data_record, physical_value) == labels_mapping[physical_value]

    @pytest.mark.parametrize("physical_value, labels_mapping", [
        (2, {"foo": 0, "bar": 1}),
        (Mock(), {f"ECU#{i}": i for i in range(7)})
    ])
    @patch(f"{SCRIPT_LOCATION}.RawDataRecord.get_raw_value")
    def test_get_raw_value__not_in_labels_mapping(self, mock_get_raw_value, physical_value, labels_mapping):
        self.mock_data_record.labels_mapping = labels_mapping
        assert MappingDataRecord.get_raw_value(self.mock_data_record, physical_value) == mock_get_raw_value.return_value
        mock_get_raw_value.assert_called_once_with(physical_value)

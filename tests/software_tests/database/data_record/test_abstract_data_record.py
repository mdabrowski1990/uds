import pytest
from mock import Mock, patch

from uds.database.data_record.abstract_data_record import AbstractDataRecord

SCRIPT_LOCATION = "uds.database.data_record.abstract_data_record"


class TestAbstractDataRecord:

    def setup_method(self):
        self.mock_data_record = Mock(spec=AbstractDataRecord)

    # __init__

    @pytest.mark.parametrize("name, length", [
        ("Some Name", 534),
        (Mock(), Mock()),
    ])
    def test_init__mandatory_args(self, name, length):
        AbstractDataRecord.__init__(self.mock_data_record, name, length)
        assert self.mock_data_record.name == name
        assert self.mock_data_record.length == length
        assert self.mock_data_record.children == tuple()

    @pytest.mark.parametrize("name, length, children", [
        ("Some Name", 534, [Mock(), Mock()]),
        (Mock(), Mock(), Mock()),
    ])
    def test_init__all_args(self, name, length, children):
        AbstractDataRecord.__init__(self.mock_data_record, name=name, length=length, children=children)
        assert self.mock_data_record.name == name
        assert self.mock_data_record.length == length
        assert self.mock_data_record.children == children

    # __validate_raw_value

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_validate_raw_value__type_error(self, mock_isinstance):
        mock_isinstance.return_value = False
        mock_value = Mock()
        with pytest.raises(TypeError):
            AbstractDataRecord._AbstractDataRecord__validate_raw_value(self.mock_data_record, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, int)

    @pytest.mark.parametrize("min_value, max_value, value", [
        (0, 10, 11),
        (0, 10, -1),
        (0, 3, 6),
    ])
    def test_validate_raw_value__value_error(self, min_value, max_value, value):
        self.mock_data_record.min_raw_value = min_value
        self.mock_data_record.max_raw_value = max_value
        with pytest.raises(ValueError):
            AbstractDataRecord._AbstractDataRecord__validate_raw_value(self.mock_data_record, value)

    @pytest.mark.parametrize("min_value, max_value, value", [
        (0, 10, 10),
        (0, 10, 6),
        (0, 3, 0),
    ])
    def test_validate_raw_value(self, min_value, max_value, value):
        self.mock_data_record.min_raw_value = min_value
        self.mock_data_record.max_raw_value = max_value
        assert AbstractDataRecord._AbstractDataRecord__validate_raw_value(self.mock_data_record, value) is None

    # name

    def test_name(self):
        self.mock_data_record._AbstractDataRecord__name = Mock()
        assert AbstractDataRecord.name.fget(self.mock_data_record) == self.mock_data_record._AbstractDataRecord__name

    # max_raw_value

    @pytest.mark.parametrize(
        "length, value", [
            (2, 3),
            (5, 31),
            (8, 255),
        ]
    )
    def test_max_raw_value_getter(self, length, value):
        self.mock_data_record.length = length
        assert AbstractDataRecord.max_raw_value.fget(self.mock_data_record) == value

    # is_reoccurring

    @pytest.mark.parametrize("min_occurrences, max_occurrences", [
        (1, 1),
        (5, 5),
        (1, 5),
        (0,1),
    ])
    def test_is_reoccurring(self, min_occurrences, max_occurrences):
        self.mock_data_record.min_occurrences = min_occurrences
        self.mock_data_record.max_occurrences = max_occurrences
        assert AbstractDataRecord.is_reoccurring.fget(self.mock_data_record) is (min_occurrences != max_occurrences)

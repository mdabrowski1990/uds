import pytest
from mock import Mock, patch

from uds.database.data_record.abstract_data_record import (
    AbstractDataRecord,
    InconsistentArgumentsError,
    ReassignmentError,
    Sequence,
OrderedDict
)

SCRIPT_LOCATION = "uds.database.data_record.abstract_data_record"


class TestAbstractDataRecord:

    def setup_method(self):
        self.mock_data_record = Mock(spec=AbstractDataRecord)

    # __init__

    @pytest.mark.parametrize("name, length, children, min_occurrences, max_occurrences", [
        ("Some Name", 534, [Mock(), Mock()], 0, None),
        (Mock(), Mock(), Mock(), Mock(), Mock()),
    ])
    def test_init(self, name, length, children, min_occurrences, max_occurrences):
        AbstractDataRecord.__init__(self.mock_data_record,
                                    name=name,
                                    length=length,
                                    children=children,
                                    min_occurrences=min_occurrences,
                                    max_occurrences=max_occurrences)
        assert self.mock_data_record.name == name
        assert self.mock_data_record.length == length
        assert self.mock_data_record.children == children
        assert self.mock_data_record.min_occurrences == min_occurrences
        assert self.mock_data_record.max_occurrences == max_occurrences

    # _validate_raw_value

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_validate_raw_value__type_error(self, mock_isinstance):
        mock_isinstance.return_value = False
        mock_value = Mock()
        with pytest.raises(TypeError):
            AbstractDataRecord._validate_raw_value(self.mock_data_record, mock_value)
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
            AbstractDataRecord._validate_raw_value(self.mock_data_record, value)

    @pytest.mark.parametrize("min_value, max_value, value", [
        (0, 10, 10),
        (0, 10, 6),
        (0, 3, 0),
    ])
    def test_validate_raw_value(self, min_value, max_value, value):
        self.mock_data_record.min_raw_value = min_value
        self.mock_data_record.max_raw_value = max_value
        assert AbstractDataRecord._validate_raw_value(self.mock_data_record, value) is None

    # name

    def test_name__get(self):
        self.mock_data_record._AbstractDataRecord__name = Mock()
        assert AbstractDataRecord.name.fget(self.mock_data_record) == self.mock_data_record._AbstractDataRecord__name

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_name__set__type_error(self, mock_isinstance):
        mock_isinstance.return_value = False
        mock_value = Mock()
        with pytest.raises(TypeError):
            AbstractDataRecord.name.fset(self.mock_data_record, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, str)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_name__set__value_error(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_value = Mock(strip=Mock(return_value=""))
        with pytest.raises(ValueError):
            AbstractDataRecord.name.fset(self.mock_data_record, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, str)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_name__set__reassignment_error(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_value = Mock()
        self.mock_data_record._AbstractDataRecord__name = Mock()
        with pytest.raises(ReassignmentError):
            AbstractDataRecord.name.fset(self.mock_data_record, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, str)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_name__set__valid(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_value = Mock()
        assert AbstractDataRecord.name.fset(self.mock_data_record, mock_value) is None
        self.mock_data_record._AbstractDataRecord__name = mock_value.strip.return_value
        mock_isinstance.assert_called_once_with(mock_value, str)

    # length

    def test_length__get(self):
        self.mock_data_record._AbstractDataRecord__length = Mock()
        assert AbstractDataRecord.length.fget(self.mock_data_record) == self.mock_data_record._AbstractDataRecord__length

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_length__set__type_error(self, mock_isinstance):
        mock_isinstance.return_value = False
        mock_value = Mock()
        with pytest.raises(TypeError):
            AbstractDataRecord.length.fset(self.mock_data_record, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, int)

    @pytest.mark.parametrize("value", [0, -1, -50])
    def test_length__set__value_error(self, value):
        with pytest.raises(ValueError):
            AbstractDataRecord.length.fset(self.mock_data_record, value)

    @pytest.mark.parametrize("value", [1, 5, 232])
    def test_length__set__reassignment_error(self, value):
        self.mock_data_record._AbstractDataRecord__length = Mock()
        with pytest.raises(ReassignmentError):
            AbstractDataRecord.length.fset(self.mock_data_record, value)

    @pytest.mark.parametrize("value", [1, 5, 232])
    def test_length__set__valid(self, value):
        assert AbstractDataRecord.length.fset(self.mock_data_record, value) is None
        self.mock_data_record._AbstractDataRecord__length = value

    # children

    def test_children__get(self):
        self.mock_data_record._AbstractDataRecord__children = Mock()
        assert AbstractDataRecord.children.fget(self.mock_data_record) == self.mock_data_record._AbstractDataRecord__children

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_children__set__type_error(self, mock_isinstance):
        mock_isinstance.return_value = False
        mock_value = Mock()
        with pytest.raises(TypeError):
            AbstractDataRecord.children.fset(self.mock_data_record, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, Sequence)

    @pytest.mark.parametrize("children", [
        [Mock(is_reoccurring=False, length=4), Mock(spec=AbstractDataRecord, is_reoccurring=False, length=4)],
        [Mock(spec=AbstractDataRecord, is_reoccurring=True, length=1) for _ in range(16)],
    ])
    def test_children__set__value_error(self, children):
        with pytest.raises(ValueError):
            AbstractDataRecord.children.fset(self.mock_data_record, children)

    @pytest.mark.parametrize("length, children", [
        (8, [Mock(spec=AbstractDataRecord, is_reoccurring=False, length=4),
             Mock(spec=AbstractDataRecord, is_reoccurring=False, length=5)]),
        (8, [Mock(spec=AbstractDataRecord, is_reoccurring=False, length=4),
             Mock(spec=AbstractDataRecord, is_reoccurring=False, length=3)]),
        (16, [Mock(spec=AbstractDataRecord, is_reoccurring=False, length=8),
              Mock(spec=AbstractDataRecord, is_reoccurring=False, length=4),
              Mock(spec=AbstractDataRecord, is_reoccurring=False, length=2),
              Mock(spec=AbstractDataRecord, is_reoccurring=False, length=1)]),
    ])
    def test_children__set__inconsistent_error(self, length, children):
        self.mock_data_record.length = length
        with pytest.raises(InconsistentArgumentsError):
            AbstractDataRecord.children.fset(self.mock_data_record, children)

    @pytest.mark.parametrize("length, children", [
        (9, [Mock(spec=AbstractDataRecord, is_reoccurring=False, length=4),
             Mock(spec=AbstractDataRecord, is_reoccurring=False, length=5)]),
        (7, [Mock(spec=AbstractDataRecord, is_reoccurring=False, length=4),
             Mock(spec=AbstractDataRecord, is_reoccurring=False, length=3)]),
        (16, [Mock(spec=AbstractDataRecord, is_reoccurring=False, length=8),
              Mock(spec=AbstractDataRecord, is_reoccurring=False, length=4),
              Mock(spec=AbstractDataRecord, is_reoccurring=False, length=2),
              Mock(spec=AbstractDataRecord, is_reoccurring=False, length=2)]),
    ])
    def test_children__set__valid(self, length, children):
        self.mock_data_record.length = length
        assert AbstractDataRecord.children.fset(self.mock_data_record, children) is None
        self.mock_data_record._AbstractDataRecord__children = tuple(children)

    # min_occurrences
    
    def test_min_occurrences__get(self):
        self.mock_data_record._AbstractDataRecord__min_occurrences = Mock()
        assert AbstractDataRecord.min_occurrences.fget(self.mock_data_record) == self.mock_data_record._AbstractDataRecord__min_occurrences

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_min_occurrences__set__type_error(self, mock_isinstance):
        mock_isinstance.return_value = False
        mock_value = Mock()
        with pytest.raises(TypeError):
            AbstractDataRecord.min_occurrences.fset(self.mock_data_record, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, int)

    @pytest.mark.parametrize("value", [-1, -50])
    def test_min_occurrences__set__value_error(self, value):
        with pytest.raises(ValueError):
            AbstractDataRecord.min_occurrences.fset(self.mock_data_record, value)

    @pytest.mark.parametrize("value", [1, 5, 232])
    def test_min_occurrences__set__reassignment_error(self, value):
        self.mock_data_record._AbstractDataRecord__min_occurrences = Mock()
        with pytest.raises(ReassignmentError):
            AbstractDataRecord.min_occurrences.fset(self.mock_data_record, value)

    @pytest.mark.parametrize("value", [0, 1, 32])
    def test_min_occurrences__set__valid(self, value):
        assert AbstractDataRecord.min_occurrences.fset(self.mock_data_record, value) is None
        self.mock_data_record._AbstractDataRecord__min_occurrences = value

    # max_occurrences

    def test_max_occurrences__get(self):
        self.mock_data_record._AbstractDataRecord__max_occurrences = Mock()
        assert AbstractDataRecord.max_occurrences.fget(
            self.mock_data_record) == self.mock_data_record._AbstractDataRecord__max_occurrences

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_max_occurrences__set__type_error(self, mock_isinstance):
        mock_isinstance.return_value = False
        mock_value = Mock()
        with pytest.raises(TypeError):
            AbstractDataRecord.max_occurrences.fset(self.mock_data_record, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, int)

    @pytest.mark.parametrize("min_occurrences, value", [
        (0, 0),
        (2, 1),
        (10, 9),
    ])
    def test_max_occurrences__set__value_error(self, min_occurrences, value):
        self.mock_data_record.min_occurrences = min_occurrences
        with pytest.raises(ValueError):
            AbstractDataRecord.max_occurrences.fset(self.mock_data_record, value)

    @pytest.mark.parametrize("min_occurrences, value", [
        (0, 1),
        (5, 9),
        (9999, None),
    ])
    def test_max_occurrences__set__reassignment_error(self, min_occurrences, value):
        self.mock_data_record.min_occurrences = min_occurrences
        self.mock_data_record._AbstractDataRecord__max_occurrences = Mock()
        with pytest.raises(ReassignmentError):
            AbstractDataRecord.max_occurrences.fset(self.mock_data_record, value)

    @pytest.mark.parametrize("min_occurrences, value", [
        (0, 1),
        (5, 9),
        (9999, None),
    ])
    def test_max_occurrences__set__valid(self, min_occurrences, value):
        self.mock_data_record.min_occurrences = min_occurrences
        assert AbstractDataRecord.max_occurrences.fset(self.mock_data_record, value) is None
        self.mock_data_record._AbstractDataRecord__max_occurrences = value

    # is_reoccurring

    @pytest.mark.parametrize("max_occurrences", [1, 2, None, 43])
    def test_is_reoccurring(self, max_occurrences):
        self.mock_data_record.max_occurrences = max_occurrences
        if max_occurrences is None:
            assert AbstractDataRecord.is_reoccurring.fget(self.mock_data_record) is True
        else:
            assert AbstractDataRecord.is_reoccurring.fget(self.mock_data_record) is (max_occurrences>1)

    # min_raw_value

    def test_min_raw_value(self):
        assert AbstractDataRecord.min_raw_value.fget(self.mock_data_record) == 0

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

    # get_children_values

    @pytest.mark.parametrize("children, raw_value, expected_children_values", [
        ([Mock(length=4), Mock(length=4)], 0x5A, [0x5, 0xA]),
        ([Mock(length=2), Mock(length=4), Mock(length=10)], 0x55FE, [0b01, 0b0101, 0x1FE]),
        ([Mock(length=1) for _ in range(8)], 0xAA, [1, 0]*4),
    ])
    def test_get_children_values(self, children, raw_value, expected_children_values):
        self.mock_data_record.children = children
        self.mock_data_record.length = sum(child.length for child in children)
        output = AbstractDataRecord.get_children_values(self.mock_data_record, raw_value)
        assert isinstance(output, OrderedDict)
        print(output)
        for i, (name, value) in enumerate(output.items()):
            assert name == children[i].name
            assert value == expected_children_values[i]

    # get_children_occurrence_info

    @pytest.mark.parametrize("raw_value", [0, 0x55])
    @pytest.mark.parametrize("children", [
        (Mock(), Mock(), Mock()),
        (Mock(), Mock()),
    ])
    def test_get_children_occurrence_info(self, raw_value, children):
        self.mock_data_record.children = children
        children_values = {child.name: Mock() for child in children}
        self.mock_data_record.get_children_values = Mock(return_value=children_values)
        output = AbstractDataRecord.get_children_occurrence_info(self.mock_data_record, raw_value=raw_value)
        self.mock_data_record.get_children_values.assert_called_once_with(raw_value)
        assert isinstance(output, tuple)
        assert len(output) == len(children)
        for i, child in enumerate(children):
            assert output[i] == child.get_occurrence_info.return_value
            child.get_occurrence_info.assert_called_with(children_values[child.name])

    # get_occurrence_info
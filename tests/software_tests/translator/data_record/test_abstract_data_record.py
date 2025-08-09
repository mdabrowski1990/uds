import pytest
from mock import MagicMock, Mock, call, patch

from uds.translator.data_record.abstract_data_record import (
    AbstractDataRecord,
    InconsistentArgumentsError,
    Mapping,
    OrderedDict,
    ReassignmentError,
    Sequence,
)

SCRIPT_LOCATION = "uds.translator.data_record.abstract_data_record"


class TestAbstractDataRecord:

    def setup_method(self):
        self.mock_data_record = Mock(spec=AbstractDataRecord)

    # __init__

    @pytest.mark.parametrize("name, length, children, min_occurrences, max_occurrences", [
        ("Some Name", 534, [Mock(), Mock()], 0, None),
        (Mock(), Mock(), Mock(), Mock(), Mock()),
    ])
    def test_init__mandatory_args(self, name, length, children, min_occurrences, max_occurrences):
        assert AbstractDataRecord.__init__(self.mock_data_record,
                                           name=name,
                                           length=length,
                                           children=children,
                                           min_occurrences=min_occurrences,
                                           max_occurrences=max_occurrences) is None
        assert self.mock_data_record.name == name
        assert self.mock_data_record.length == length
        assert self.mock_data_record.children == children
        assert self.mock_data_record.unit == None
        assert self.mock_data_record.min_occurrences == min_occurrences
        assert self.mock_data_record.max_occurrences == max_occurrences

    @pytest.mark.parametrize("name, length, children, unit, min_occurrences, max_occurrences", [
        ("Some Name", 534, [Mock(), Mock()], "km/h", 0, None),
        (Mock(), Mock(), Mock(), Mock(), Mock(), Mock()),
    ])
    def test_init__all_args(self, name, length, children, unit, min_occurrences, max_occurrences):
        assert AbstractDataRecord.__init__(self.mock_data_record,
                                           name=name,
                                           length=length,
                                           children=children,
                                           unit=unit,
                                           min_occurrences=min_occurrences,
                                           max_occurrences=max_occurrences) is None
        assert self.mock_data_record.name == name
        assert self.mock_data_record.length == length
        assert self.mock_data_record.children == children
        assert self.mock_data_record.unit == unit
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
        assert (AbstractDataRecord.children.fget(self.mock_data_record)
                == self.mock_data_record._AbstractDataRecord__children)

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
        (8, [Mock(spec=AbstractDataRecord, is_reoccurring=False, length=4),
             Mock(spec=AbstractDataRecord, is_reoccurring=False, length=4)]),
        (16, [Mock(spec=AbstractDataRecord, is_reoccurring=False, length=8),
              Mock(spec=AbstractDataRecord, is_reoccurring=False, length=4),
              Mock(spec=AbstractDataRecord, is_reoccurring=False, length=2),
              Mock(spec=AbstractDataRecord, is_reoccurring=False, length=2)]),
    ])
    def test_children__set__inconsistent_error__names(self, length, children):
        self.mock_data_record.length = length
        children[-1].name = children[0].name
        with pytest.raises(InconsistentArgumentsError):
            AbstractDataRecord.children.fset(self.mock_data_record, children)

    @pytest.mark.parametrize("length, children", [
        (8, []),
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

    # unit

    def test_unit__get(self):
        self.mock_data_record._AbstractDataRecord__unit = Mock()
        assert AbstractDataRecord.unit.fget(
            self.mock_data_record) == self.mock_data_record._AbstractDataRecord__unit

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_unit__set__type_error(self, mock_isinstance):
        mock_isinstance.return_value = False
        mock_value = Mock()
        with pytest.raises(TypeError):
            AbstractDataRecord.unit.fset(self.mock_data_record, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, str)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_unit__set__valid__none(self, mock_isinstance):
        assert AbstractDataRecord.unit.fset(self.mock_data_record, None) is None
        assert self.mock_data_record._AbstractDataRecord__unit is None
        mock_isinstance.assert_not_called()

    @pytest.mark.parametrize("value", [Mock(), "h"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_unit__set__valid__str(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        assert AbstractDataRecord.unit.fset(self.mock_data_record, value) is None
        assert self.mock_data_record._AbstractDataRecord__unit == value
        mock_isinstance.assert_called_once_with(value, str)

    # is_reoccurring

    @pytest.mark.parametrize("max_occurrences", [1, 2, None, 43])
    def test_is_reoccurring(self, max_occurrences):
        self.mock_data_record.max_occurrences = max_occurrences
        if max_occurrences is None:
            assert AbstractDataRecord.is_reoccurring.fget(self.mock_data_record) is True
        else:
            assert AbstractDataRecord.is_reoccurring.fget(self.mock_data_record) is (max_occurrences>1)

    # fixed_total_length

    @pytest.mark.parametrize("min_occurrences, max_occurrences, expect_value", [
        (1, None, False),
        (3, 3, True),
        (1, 1, True),
        (0, 1, False),
    ])
    def test_fixed_total_length(self, min_occurrences, max_occurrences, expect_value):
        self.mock_data_record.min_occurrences = min_occurrences
        self.mock_data_record.max_occurrences = max_occurrences
        assert AbstractDataRecord.fixed_total_length.fget(self.mock_data_record) is expect_value

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

    def test_get_occurrence_info__value_error__no_values(self):
        with pytest.raises(ValueError):
            AbstractDataRecord.get_occurrence_info(self.mock_data_record)

    def test_get_occurrence_info__value_error__multiple_values_for_single_occurrence(self):
        self.mock_data_record.is_reoccurring = False
        with pytest.raises(ValueError):
            AbstractDataRecord.get_occurrence_info(self.mock_data_record, Mock(), Mock())

    def test_get_occurrence_info__single_occurrence(self):
        mock_raw_value = Mock()
        self.mock_data_record.is_reoccurring = False
        output = AbstractDataRecord.get_occurrence_info(self.mock_data_record, mock_raw_value)
        assert isinstance(output, dict)
        assert output["name"] == self.mock_data_record.name
        assert output["raw_value"] == mock_raw_value
        assert output["physical_value"] == self.mock_data_record.get_physical_value.return_value
        assert output["children"] == self.mock_data_record.get_children_occurrence_info.return_value
        self.mock_data_record.get_physical_value.assert_called_once_with(mock_raw_value)
        self.mock_data_record.get_children_occurrence_info.assert_called_once_with(mock_raw_value)

    @pytest.mark.parametrize("raw_values", [range(10), (Mock(), Mock(), Mock())])
    def test_get_occurrence_info__multiple_occurrences(self, raw_values):
        self.mock_data_record.is_reoccurring = True
        output = AbstractDataRecord.get_occurrence_info(self.mock_data_record, *raw_values)
        assert isinstance(output, dict)
        assert output["name"] == self.mock_data_record.name
        assert output["raw_value"] == list(raw_values)
        assert output["physical_value"] == self.mock_data_record.get_physical_values.return_value
        assert output["children"] == [self.mock_data_record.get_children_occurrence_info.return_value]*len(raw_values)
        self.mock_data_record.get_physical_values.assert_called_once_with(*raw_values)
        self.mock_data_record.get_children_occurrence_info.assert_has_calls([call(raw_value) for raw_value in raw_values])

    # get_physical_values

    def test_get_physical_values__runtime_error(self):
        self.mock_data_record.is_reoccurring = False
        with pytest.raises(RuntimeError):
            AbstractDataRecord.get_physical_values(self.mock_data_record, Mock(), Mock())

    @pytest.mark.parametrize("raw_values, min_occurrences, max_occurrences", [
        (range(11), 0, 10),
        ([Mock()], 2, None),
    ])
    def test_get_physical_values__value_error(self, raw_values, min_occurrences, max_occurrences):
        self.mock_data_record.is_reoccurring = True
        self.mock_data_record.min_occurrences = min_occurrences
        self.mock_data_record.max_occurrences = max_occurrences
        with pytest.raises(ValueError):
            AbstractDataRecord.get_physical_values(self.mock_data_record, *raw_values)

    @pytest.mark.parametrize("raw_values, min_occurrences, max_occurrences", [
        (range(10), 0, 10),
        ([Mock(), Mock()], 2, None),
        (range(10000), 0, None),
    ])
    def test_get_physical_values(self, raw_values, min_occurrences, max_occurrences):
        self.mock_data_record.is_reoccurring = True
        self.mock_data_record.min_occurrences = min_occurrences
        self.mock_data_record.max_occurrences = max_occurrences
        output = AbstractDataRecord.get_physical_values(self.mock_data_record, *raw_values)
        assert isinstance(output, tuple)
        assert output == tuple([self.mock_data_record.get_physical_value.return_value] * len(raw_values))
        self.mock_data_record.get_physical_value.assert_has_calls([call(raw_value) for raw_value in raw_values])

    # get_raw_value_from_children

    def test_get_raw_value_from_children__runtime_error(self):
        self.mock_data_record.children = tuple()
        with pytest.raises(RuntimeError):
            AbstractDataRecord.get_raw_value_from_children(self.mock_data_record, MagicMock())

    @pytest.mark.parametrize("children_values", [Mock(), MagicMock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_get_raw_value_from_children__type_error(self, mock_isinstance, children_values):
        self.mock_data_record.children = [Mock(), Mock()]
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractDataRecord.get_raw_value_from_children(self.mock_data_record, children_values)
        mock_isinstance.assert_called_once_with(children_values, Mapping)

    @pytest.mark.parametrize("children_names, children_values", [
        (["DID#1", "DID#2", "DTC#3"], {"DID#1": 1, "DID#2": 2}),
        (["A B C", "xyz 798"], {"A B C": 1, "xyz 798": 2, "X": 0}),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_get_raw_value_from_children__value_error__children_names(self, mock_isinstance,
                                                                      children_names, children_values):
        self.mock_data_record.children = [Mock() for _ in children_names]
        for i, name in enumerate(children_names):
            self.mock_data_record.children[i].name = name
        mock_isinstance.return_value = True
        with pytest.raises(ValueError):
            AbstractDataRecord.get_raw_value_from_children(self.mock_data_record, children_values)
        mock_isinstance.assert_called_once_with(children_values, Mapping)

    @pytest.mark.parametrize("children, children_values", [
        (
            (Mock(spec=AbstractDataRecord, length=2, name="Parameter A"),
             Mock(spec=AbstractDataRecord, length=2, name="Parameter B"),
             Mock(spec=AbstractDataRecord, length=2, name="Parameter C"),
             Mock(spec=AbstractDataRecord, length=2, name="Parameter D"),),
            {"Parameter A": 0b11, "Parameter B": Mock(), "Parameter C": 0b01, "Parameter D": 0b00},
        ),
        (
            (Mock(spec=AbstractDataRecord, length=8, name="XYZ"),
             Mock(spec=AbstractDataRecord, length=4, name="ABC"),
             Mock(spec=AbstractDataRecord, length=16, name="Some name")),
            {"XYZ": 0xA5, "ABC": 0xD, "Some name": 54.2},
        )
    ])
    def test_get_raw_value_from_children__value_error__children_value_type(self, children, children_values):
        for child in children:
            child.name = child._extract_mock_name()
        self.mock_data_record.children = children
        self.mock_data_record.length = sum([child.length for child in children])
        with pytest.raises(ValueError):
            AbstractDataRecord.get_raw_value_from_children(self.mock_data_record, children_values)

    @pytest.mark.parametrize("children, children_values, raw_value", [
        (
            (Mock(spec=AbstractDataRecord, length=2, name="Parameter A"),
             Mock(spec=AbstractDataRecord, length=2, name="Parameter B"),
             Mock(spec=AbstractDataRecord, length=2, name="Parameter C"),
             Mock(spec=AbstractDataRecord, length=2, name="Parameter D"),),
            {"Parameter A": 0b11, "Parameter B": 0b10, "Parameter C": 0b01, "Parameter D": 0b00},
            0b11100100
        ),
        (
            (Mock(spec=AbstractDataRecord, length=8, name="XYZ"),
             Mock(spec=AbstractDataRecord, length=4, name="ABC"),
             Mock(spec=AbstractDataRecord, length=16, name="Some name")),
            {"XYZ": 0xA5, "ABC": 0xD, "Some name": 0xCAFE},
            0xA5DCAFE
        )
    ])
    def test_get_raw_value_from_children__valid__raw_values(self, children, children_values, raw_value):
        for child in children:
            child.name = child._extract_mock_name()
        self.mock_data_record.children = children
        self.mock_data_record.length = sum([child.length for child in children])
        assert AbstractDataRecord.get_raw_value_from_children(self.mock_data_record,
                                                              children_values) == raw_value

    @pytest.mark.parametrize("children, children_values, children_raw_values_mapping, raw_value", [
        (
            (Mock(spec=AbstractDataRecord, length=2, name="Parameter A"),
             Mock(spec=AbstractDataRecord, length=2, name="Parameter B"),
             Mock(spec=AbstractDataRecord, length=2, name="Parameter C"),
             Mock(spec=AbstractDataRecord, length=2, name="Parameter D"),),
            {"Parameter A": {"a1": 1, "a2": 2},
             "Parameter B": {"xyz": {"a": 0, "b":2}, "abc": 0},
             "Parameter C": {"Parameter C.1": 0, "Parameter C.2": 2, "Parameter C.3": 0xF},
             "Parameter D": {"DTC 1": 0xFEBCDE, "DTC 2": 0x800020}},
            {"Parameter A": 0b11, "Parameter B": 0b10, "Parameter C": 0b01, "Parameter D": 0b00},
            0b11100100
        ),
        (
            (Mock(spec=AbstractDataRecord, length=8, name="XYZ"),
             Mock(spec=AbstractDataRecord, length=4, name="ABC"),
             Mock(spec=AbstractDataRecord, length=16, name="Some name")),
            {"XYZ": {"XYZ#1": 0, "XYZ#2": 1, "XYZ#3": 2, "XYZ#4": 3, "XYZ#5": 0xF},
             "ABC": {"ABC - 1": 0, "ABC - 2": 9},
             "Some name": {"1": 1, "2": 2, "0": 5}},
            {"XYZ": 0xA5, "ABC": 0xD, "Some name": 0xCAFE},
            0xA5DCAFE
        )
    ])
    def test_get_raw_value_from_children__valid__children_values(self, children, children_values,
                                                                 children_raw_values_mapping, raw_value):
        for child in children:
            child.name = child._extract_mock_name()
            child.get_raw_value_from_children.return_value = children_raw_values_mapping[child.name]
        self.mock_data_record.children = children
        self.mock_data_record.length = sum([child.length for child in children])
        assert AbstractDataRecord.get_raw_value_from_children(self.mock_data_record,
                                                              children_values) == raw_value
        for child in children:
            child.get_raw_value_from_children.assert_called_once_with(children_values[child.name])
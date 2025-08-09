from operator import getitem

import pytest
from mock import MagicMock, Mock, call, patch

from uds.translator.data_record import RawDataRecord, TextDataRecord, TextEncoding
from uds.translator.data_record.conditional_data_record import (
    DEFAULT_DIAGNOSTIC_MESSAGE_CONTINUATION,
    AbstractConditionalDataRecord,
    AbstractDataRecord,
    AliasMessageStructure,
    Callable,
    ConditionalFormulaDataRecord,
    ConditionalMappingDataRecord,
    Mapping,
    Sequence,
)
from uds.utilities import InconsistentArgumentsError

SCRIPT_LOCATION = "uds.translator.data_record.conditional_data_record"


class TestAbstractConditionalDataRecord:
    """Unit tests for `AbstractConditionalDataRecord` class"""

    def setup_method(self):
        self.mock_conditional_data_record = MagicMock(spec=AbstractConditionalDataRecord)

    # __init__

    @pytest.mark.parametrize("default_message_continuation", [Mock(), DEFAULT_DIAGNOSTIC_MESSAGE_CONTINUATION])
    def test_init(self, default_message_continuation):
        assert AbstractConditionalDataRecord.__init__(self.mock_conditional_data_record,
                                                      default_message_continuation=default_message_continuation) is None
        assert self.mock_conditional_data_record.default_message_continuation == default_message_continuation

    # default_message_continuation

    def test_default_message_continuation__get(self):
        self.mock_conditional_data_record._AbstractConditionalDataRecord__default_message_continuation = Mock()
        assert (AbstractConditionalDataRecord.default_message_continuation.fget(self.mock_conditional_data_record)
                == self.mock_conditional_data_record._AbstractConditionalDataRecord__default_message_continuation)

    def test_default_message_continuation__set__none(self):
        assert AbstractConditionalDataRecord.default_message_continuation.fset(self.mock_conditional_data_record,
                                                                               None) is None
        assert self.mock_conditional_data_record._AbstractConditionalDataRecord__default_message_continuation is None
        self.mock_conditional_data_record.validate_message_continuation.assert_not_called()

    @pytest.mark.parametrize("value", [MagicMock(), DEFAULT_DIAGNOSTIC_MESSAGE_CONTINUATION])
    def test_default_message_continuation__set__value(self, value):
        assert AbstractConditionalDataRecord.default_message_continuation.fset(self.mock_conditional_data_record,
                                                                               value) is None
        assert (self.mock_conditional_data_record._AbstractConditionalDataRecord__default_message_continuation
                == tuple(value))
        self.mock_conditional_data_record.validate_message_continuation.assert_called_once_with(value)

    # validate_message_continuation

    @pytest.mark.parametrize("value", [Mock(), DEFAULT_DIAGNOSTIC_MESSAGE_CONTINUATION])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_validate_message_continuation__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractConditionalDataRecord.validate_message_continuation(value)
        mock_isinstance.assert_called_once_with(value, Sequence)

    @pytest.mark.parametrize("value", [
        (Mock(spec=AbstractDataRecord, length=8, min_occurrences=1, max_occurrences=1, fixed_total_length=True),
         Mock(length=1, min_occurrences=8, max_occurrences=8, fixed_total_length=True),
         Mock(spec=AbstractConditionalDataRecord, fixed_total_length=True)),
        (Mock(spec=AbstractDataRecord, length=16, min_occurrences=1, max_occurrences=1, fixed_total_length=True),
         Mock(spec=AbstractDataRecord, length=1, min_occurrences=8, max_occurrences=8, fixed_total_length=True),
         Mock(length=2, min_occurrences=4, max_occurrences=None, fixed_total_length=False)),
    ])
    def test_validate_message_continuation__value_error__data_record_type(self, value):
        with pytest.raises(ValueError):
            AbstractConditionalDataRecord.validate_message_continuation(value)

    @pytest.mark.parametrize("value", [
        (Mock(spec=AbstractDataRecord, length=8, min_occurrences=1, max_occurrences=1, fixed_total_length=True),
         Mock(spec=AbstractConditionalDataRecord),
         Mock(spec=AbstractDataRecord, length=1, min_occurrences=8, max_occurrences=8, fixed_total_length=True)),
        (Mock(spec=AbstractConditionalDataRecord),
         Mock(spec=AbstractDataRecord, length=16, min_occurrences=1, max_occurrences=1, fixed_total_length=True),
         Mock(spec=AbstractDataRecord, length=1, min_occurrences=8, max_occurrences=8, fixed_total_length=True),
         Mock(spec=AbstractDataRecord, length=2, min_occurrences=4, max_occurrences=None, fixed_total_length=False)),
        (Mock(spec=AbstractConditionalDataRecord),),
        (Mock(spec=AbstractDataRecord, length=16, min_occurrences=1, max_occurrences=1, fixed_total_length=True),
         Mock(spec=AbstractDataRecord, length=2, min_occurrences=4, max_occurrences=None, fixed_total_length=False),
         Mock(spec=AbstractDataRecord, length=1, min_occurrences=8, max_occurrences=8, fixed_total_length=True)),
        (Mock(spec=AbstractDataRecord, length=2, min_occurrences=4, max_occurrences=None, fixed_total_length=False),
         Mock(spec=AbstractConditionalDataRecord),)
    ])
    def test_validate_message_continuation__value_error__conditional_and_vary_length_data_record_position(self, value):
        with pytest.raises(ValueError):
            AbstractConditionalDataRecord.validate_message_continuation(value)

    @pytest.mark.parametrize("value", [
        (Mock(spec=AbstractDataRecord, length=23, min_occurrences=1, max_occurrences=1, fixed_total_length=True),
         Mock(spec=AbstractDataRecord, length=5, min_occurrences=4, max_occurrences=4, fixed_total_length=True)),
        (Mock(spec=AbstractDataRecord, length=7, min_occurrences=1, max_occurrences=1, fixed_total_length=True),
         Mock(spec=AbstractDataRecord, length=1, min_occurrences=8, max_occurrences=16, fixed_total_length=False)),
        (Mock(spec=AbstractDataRecord, length=16, min_occurrences=1, max_occurrences=1, fixed_total_length=True),
         Mock(spec=AbstractDataRecord, length=2, min_occurrences=4, max_occurrences=4, fixed_total_length=True),
         Mock(spec=AbstractDataRecord, length=1, min_occurrences=8, max_occurrences=14, fixed_total_length=False)),
    ])
    def test_validate_message_continuation__inconsistent__total_length(self, value):
        with pytest.raises(InconsistentArgumentsError):
            AbstractConditionalDataRecord.validate_message_continuation(value)

    @pytest.mark.parametrize("value", [
        (Mock(spec=AbstractDataRecord, length=8, min_occurrences=1, max_occurrences=1, fixed_total_length=True),
         Mock(spec=AbstractDataRecord, length=1, min_occurrences=8, max_occurrences=8, fixed_total_length=True),
         Mock(spec=AbstractConditionalDataRecord, fixed_total_length=False)),
        (Mock(spec=AbstractDataRecord, length=16, min_occurrences=1, max_occurrences=1, fixed_total_length=True),
         Mock(spec=AbstractDataRecord, length=1, min_occurrences=8, max_occurrences=8, fixed_total_length=True),
         Mock(spec=AbstractDataRecord, length=2, min_occurrences=4, max_occurrences=None, fixed_total_length=False)),
    ])
    def test_validate_message_continuation__inconsistent__same_names(self, value):
        for dr in value:
            dr.name = "Common"
        with pytest.raises(InconsistentArgumentsError):
            AbstractConditionalDataRecord.validate_message_continuation(value)

    @pytest.mark.parametrize("value", [
        (Mock(spec=AbstractDataRecord, length=8, min_occurrences=1, max_occurrences=1, fixed_total_length=True),),
        (Mock(spec=AbstractDataRecord, length=8, min_occurrences=0, max_occurrences=None, fixed_total_length=False),),
        (Mock(spec=AbstractDataRecord, length=8, min_occurrences=1, max_occurrences=1, fixed_total_length=True),
         Mock(spec=AbstractDataRecord, length=1, min_occurrences=8, max_occurrences=8, fixed_total_length=True),
         Mock(spec=AbstractConditionalDataRecord, fixed_total_length=False)),
        (Mock(spec=AbstractDataRecord, length=16, min_occurrences=1, max_occurrences=1, fixed_total_length=True),
         Mock(spec=AbstractDataRecord, length=1, min_occurrences=8, max_occurrences=8, fixed_total_length=True),
         Mock(spec=AbstractDataRecord, length=2, min_occurrences=4, max_occurrences=None, fixed_total_length=False)),
    ])
    def test_validate_message_continuation__valid(self, value):
        assert AbstractConditionalDataRecord.validate_message_continuation(value) is None

    # get_message_continuation

    @pytest.mark.parametrize("raw_value", [Mock(), 0])
    def test_get_message_continuation__valid(self, raw_value):
        assert AbstractConditionalDataRecord.get_message_continuation(
            self.mock_conditional_data_record,
            raw_value=raw_value) == self.mock_conditional_data_record.__getitem__.return_value
        self.mock_conditional_data_record.__getitem__.assert_called_once_with(raw_value)

    @pytest.mark.parametrize("raw_value, exception_raised", [
        (Mock(), ValueError),
        (0, KeyError),
    ])
    def test_get_message_continuation__default(self, raw_value, exception_raised):
        self.mock_conditional_data_record.__getitem__.side_effect = exception_raised
        assert AbstractConditionalDataRecord.get_message_continuation(
            self.mock_conditional_data_record,
            raw_value=raw_value) == self.mock_conditional_data_record.default_message_continuation
        self.mock_conditional_data_record.__getitem__.assert_called_once_with(raw_value)

    @pytest.mark.parametrize("raw_value", [Mock(), 0])
    def test_get_message_continuation__value_error(self, raw_value):
        self.mock_conditional_data_record.__getitem__.side_effect = KeyError
        self.mock_conditional_data_record.default_message_continuation = None
        with pytest.raises(ValueError):
            AbstractConditionalDataRecord.get_message_continuation(self.mock_conditional_data_record,
                                                                   raw_value=raw_value)
        self.mock_conditional_data_record.__getitem__.assert_called_once_with(raw_value)


class TestConditionalMappingDataRecord:
    """Unit tests for `ConditionalMappingDataRecord` class"""

    def setup_method(self):
        self.mock_conditional_data_record = MagicMock(spec=ConditionalMappingDataRecord)
        # patching
        self._patcher_abstract_conditional_data_record_init \
            = patch(f"{SCRIPT_LOCATION}.AbstractConditionalDataRecord.__init__")
        self.mock_abstract_conditional_data_record_init = self._patcher_abstract_conditional_data_record_init.start()
        self._patcher_mapping_proxy_type = patch(f"{SCRIPT_LOCATION}.MappingProxyType")
        self.mock_mapping_proxy_type = self._patcher_mapping_proxy_type.start()

    def teardown_method(self):
        self._patcher_abstract_conditional_data_record_init.stop()
        self._patcher_mapping_proxy_type.stop()

    # __init__

    @pytest.mark.parametrize("mapping, default_message_continuation", [
        (Mock(), Mock()),
        ({1: Mock(), 2: []}, DEFAULT_DIAGNOSTIC_MESSAGE_CONTINUATION),
    ])
    def test_init(self, mapping, default_message_continuation):
        assert ConditionalMappingDataRecord.__init__(self.mock_conditional_data_record,
                                                     default_message_continuation=default_message_continuation,
                                                     mapping=mapping) is None
        assert self.mock_conditional_data_record.mapping == mapping
        self.mock_abstract_conditional_data_record_init.assert_called_once_with(
            default_message_continuation=default_message_continuation)

    # __getitem__

    @pytest.mark.parametrize("value", [Mock(), "something"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_getitem__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            ConditionalMappingDataRecord.__getitem__(self.mock_conditional_data_record, value)
        mock_isinstance.assert_called_once_with(value, int)

    @pytest.mark.parametrize("value", [-1, -52])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_getitem__value_error(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        with pytest.raises(ValueError):
            ConditionalMappingDataRecord.__getitem__(self.mock_conditional_data_record, value)
        mock_isinstance.assert_called_once_with(value, int)

    @pytest.mark.parametrize("value", [0, 25])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_getitem__key_error(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        mock_getitem = Mock(side_effect=KeyError)
        self.mock_conditional_data_record.mapping = MagicMock(__getitem__=mock_getitem)
        with pytest.raises(KeyError):
            ConditionalMappingDataRecord.__getitem__(self.mock_conditional_data_record, value)
        mock_isinstance.assert_called_once_with(value, int)
        mock_getitem.assert_called_once_with(value)

    @pytest.mark.parametrize("value", [0, 25])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_getitem__valid(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        mock_getitem = Mock()
        self.mock_conditional_data_record.mapping = MagicMock(__getitem__=mock_getitem)
        assert (ConditionalMappingDataRecord.__getitem__(self.mock_conditional_data_record, value)
                == mock_getitem.return_value)
        mock_isinstance.assert_called_once_with(value, int)
        mock_getitem.assert_called_once_with(value)

    # mapping

    def test_mapping__get(self):
        self.mock_conditional_data_record._ConditionalMappingDataRecord__mapping = Mock()
        assert (ConditionalMappingDataRecord.mapping.fget(self.mock_conditional_data_record)
                == self.mock_conditional_data_record._ConditionalMappingDataRecord__mapping)

    @pytest.mark.parametrize("value", [Mock(), "Some value"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_mapping__set__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            ConditionalMappingDataRecord.mapping.fset(self.mock_conditional_data_record, value)
        mock_isinstance.assert_called_once_with(value, Mapping)

    @pytest.mark.parametrize("value", [{-1: Mock()}, {-50: Mock(), 0: Mock(), 32: Mock()}])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_mapping__set__value_error__value(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        with pytest.raises(ValueError):
            ConditionalMappingDataRecord.mapping.fset(self.mock_conditional_data_record, value)
        mock_isinstance.assert_called()
        self.mock_conditional_data_record.validate_message_continuation.assert_not_called()

    @pytest.mark.parametrize("value", [{1: Mock()}, {0: Mock(), 32: Mock(), 2: Mock(), 3: []}])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_mapping__set__value_error__type(self, mock_isinstance, value):
        mock_isinstance.side_effect = [True, False]
        with pytest.raises(ValueError):
            ConditionalMappingDataRecord.mapping.fset(self.mock_conditional_data_record, value)
        mock_isinstance.assert_called()
        self.mock_conditional_data_record.validate_message_continuation.assert_not_called()

    @pytest.mark.parametrize("value", [{1: Mock()}, {0: Mock(), 32: Mock(), 2: Mock(), 3: []}])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_mapping__set__valid(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        assert ConditionalMappingDataRecord.mapping.fset(self.mock_conditional_data_record, value) is None
        assert (self.mock_conditional_data_record._ConditionalMappingDataRecord__mapping
                == self.mock_mapping_proxy_type.return_value)
        mock_isinstance.assert_has_calls([call(value, Mapping)] + [call(key, int) for key in value.keys()],
                                         any_order=True)
        self.mock_conditional_data_record.validate_message_continuation.assert_has_calls(
            [call(i) for i in value.values()], any_order=True)
        self.mock_mapping_proxy_type.assert_called_once_with(value)


class TestConditionalFormulaDataRecord:
    """Unit tests for `ConditionalFormulaDataRecord` class"""

    def setup_method(self):
        self.mock_conditional_data_record = MagicMock(spec=ConditionalFormulaDataRecord)
        # patching
        self._patcher_abstract_conditional_data_record_init \
            = patch(f"{SCRIPT_LOCATION}.AbstractConditionalDataRecord.__init__")
        self.mock_abstract_conditional_data_record_init = self._patcher_abstract_conditional_data_record_init.start()
        self._patcher_signature = patch(f"{SCRIPT_LOCATION}.signature")
        self.mock_signature = self._patcher_signature.start()

    def teardown_method(self):
        self._patcher_abstract_conditional_data_record_init.stop()
        self._patcher_signature.stop()

    # __init__

    @pytest.mark.parametrize("formula, default_message_continuation", [
        (Mock(), Mock()),
        ({1: Mock(), 2: []}, DEFAULT_DIAGNOSTIC_MESSAGE_CONTINUATION),
    ])
    def test_init(self, formula, default_message_continuation):
        assert ConditionalFormulaDataRecord.__init__(self.mock_conditional_data_record,
                                                     default_message_continuation=default_message_continuation,
                                                     formula=formula) is None
        assert self.mock_conditional_data_record.formula == formula
        self.mock_abstract_conditional_data_record_init.assert_called_once_with(
            default_message_continuation=default_message_continuation)

    # __getitem__

    @pytest.mark.parametrize("value", [Mock(), "something"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_getitem__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            ConditionalFormulaDataRecord.__getitem__(self.mock_conditional_data_record, value)
        mock_isinstance.assert_called_once_with(value, int)

    @pytest.mark.parametrize("value", [-1, -52])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_getitem__value_error(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        with pytest.raises(ValueError):
            ConditionalFormulaDataRecord.__getitem__(self.mock_conditional_data_record, value)
        mock_isinstance.assert_called_once_with(value, int)

    @pytest.mark.parametrize("value", [0, 25])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_getitem__valid(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        assert (ConditionalFormulaDataRecord.__getitem__(self.mock_conditional_data_record, value)
                == self.mock_conditional_data_record.formula.return_value)
        mock_isinstance.assert_called_once_with(value, int)
        self.mock_conditional_data_record.formula.assert_called_once_with(value)

    # formula

    def test_formula__get(self):
        self.mock_conditional_data_record._ConditionalFormulaDataRecord__formula = Mock()
        assert (ConditionalFormulaDataRecord.formula.fget(self.mock_conditional_data_record)
                == self.mock_conditional_data_record._ConditionalFormulaDataRecord__formula)

    @pytest.mark.parametrize("value", [Mock(), "Something"])
    @patch(f"{SCRIPT_LOCATION}.callable")
    def test_formula__set__type_error(self, mock_callable, value):
        mock_callable.return_value = False
        with pytest.raises(TypeError):
            ConditionalFormulaDataRecord.formula.fset(self.mock_conditional_data_record, value)
        mock_callable.assert_called_once_with(value)

    @pytest.mark.parametrize("value, arg_number", [
        (Mock(), 0),
        (Mock(spec=Callable), 2),
    ])
    @patch(f"{SCRIPT_LOCATION}.callable")
    def test_formula__set__value_error__arguments_number(self, mock_callable, value, arg_number):
        mock_callable.return_value = True
        self.mock_signature.return_value = Mock(parameters=[Mock() for _ in range(arg_number)])
        with pytest.raises(ValueError):
            ConditionalFormulaDataRecord.formula.fset(self.mock_conditional_data_record, value)
        mock_callable.assert_called_once_with(value)
        self.mock_signature.assert_called_once_with(value)

    @pytest.mark.parametrize("value, arg_number", [
        (Mock(), 0),
        (Mock(spec=Callable), 2),
    ])
    @patch(f"{SCRIPT_LOCATION}.callable")
    def test_formula__set__value_error__arguments_number(self, mock_callable, value, arg_number):
        mock_callable.return_value = True
        self.mock_signature.return_value = Mock(parameters={Mock(): Mock() for _ in range(arg_number)})
        with pytest.raises(ValueError):
            ConditionalFormulaDataRecord.formula.fset(self.mock_conditional_data_record, value)
        mock_callable.assert_called_once_with(value)
        self.mock_signature.assert_called_once_with(value)

    @pytest.mark.parametrize("value, arg_type", [
        (Mock(), Mock()),
        (Mock(spec=Callable), float),
    ])
    @patch(f"{SCRIPT_LOCATION}.issubclass")
    @patch(f"{SCRIPT_LOCATION}.callable")
    def test_formula__set__value_error__arguments_annotation(self, mock_callable, mock_issubclass, value, arg_type):
        mock_callable.return_value = True
        mock_issubclass.return_value = False
        self.mock_signature.return_value = Mock(parameters={Mock(): Mock(annotation=arg_type)})
        with pytest.raises(ValueError):
            ConditionalFormulaDataRecord.formula.fset(self.mock_conditional_data_record, value)
        mock_callable.assert_called_once_with(value)
        mock_issubclass.assert_called_once_with(arg_type, int)
        self.mock_signature.assert_called_once_with(value)

    @pytest.mark.parametrize("value, arg_type", [
        (Mock(), Mock(spec=int)),
        (Mock(spec=Callable), bool),
    ])
    @patch(f"{SCRIPT_LOCATION}.issubclass")
    @patch(f"{SCRIPT_LOCATION}.callable")
    def test_formula__set__valid_type(self, mock_callable, mock_issubclass, value, arg_type):
        mock_callable.return_value = True
        mock_issubclass.return_value = True
        self.mock_signature.return_value = Mock(parameters={Mock(): Mock(annotation=arg_type)})
        assert ConditionalFormulaDataRecord.formula.fset(self.mock_conditional_data_record, value) is None
        assert self.mock_conditional_data_record._ConditionalFormulaDataRecord__formula == value
        mock_callable.assert_called_once_with(value)
        mock_issubclass.assert_called_once_with(arg_type, int)
        self.mock_signature.assert_called_once_with(value)

    @pytest.mark.parametrize("value", [Mock(), Mock(spec=Callable)])
    @patch(f"{SCRIPT_LOCATION}.issubclass")
    @patch(f"{SCRIPT_LOCATION}.callable")
    def test_formula__set__valid_empty(self, mock_callable, mock_issubclass, value):
        mock_callable.return_value = True
        mock_issubclass.return_value = True
        mock_empty = Mock()
        self.mock_signature.return_value = Mock(parameters={Mock(): Mock(annotation=mock_empty)}, empty=mock_empty)
        assert ConditionalFormulaDataRecord.formula.fset(self.mock_conditional_data_record, value) is None
        assert self.mock_conditional_data_record._ConditionalFormulaDataRecord__formula == value
        mock_callable.assert_called_once_with(value)
        mock_issubclass.assert_not_called()
        self.mock_signature.assert_called_once_with(value)


@pytest.mark.integration
class TestConditionalMappingDataRecordIntegration:
    """Integration tests for `ConditionalMappingDataRecord` class."""

    def setup_class(self):
        self.did_mapping = {
            0x1000: [RawDataRecord(name="Digits Number",
                                   length=8,
                                   min_occurrences=1,
                                   max_occurrences=1),
                     ConditionalFormulaDataRecord(formula=lambda raw_value: [
                         TextDataRecord(name="BCD digits",
                                        encoding=TextEncoding.BCD,
                                        min_occurrences=raw_value,
                                        max_occurrences=raw_value)])],
            0x1234: [RawDataRecord(name="Entry#1",
                                   length=64)],
            0xF186: [TextDataRecord(name="ASCII text",
                                    encoding=TextEncoding.ASCII,
                                    min_occurrences=1,
                                    max_occurrences=None)],
        }
        self.undefined_dids = [0x0000, 0xFFFF]
        self.did_conditional_data_record = ConditionalMappingDataRecord(
            mapping=self.did_mapping,
            default_message_continuation=DEFAULT_DIAGNOSTIC_MESSAGE_CONTINUATION)

    # getitem

    def test_getitem(self):
        for did, did_structure in self.did_mapping.items():
            assert self.did_conditional_data_record[did] == did_structure

    def test_getitem__key_error(self):
        for did in self.undefined_dids:
            with pytest.raises(KeyError):
                self.did_conditional_data_record[did]

    # get_message_continuation

    def test_get_message_continuation(self):
        for did, did_structure in self.did_mapping.items():
            assert self.did_conditional_data_record.get_message_continuation(did) == did_structure

    def test_get_message_continuation__default(self):
        for did in self.undefined_dids:
            assert (self.did_conditional_data_record.get_message_continuation(did)
                    == DEFAULT_DIAGNOSTIC_MESSAGE_CONTINUATION)

@pytest.mark.integration
class TestConditionalFormulaDataRecordIntegration:
    """Integration tests for `ConditionalFormulaDataRecord` class."""

    def setup_class(self):
        def continuation_length_formula(raw_value: int) -> AliasMessageStructure:
            if raw_value <= 0 or raw_value > 20:
                raise ValueError
            return [RawDataRecord(name="Entries",
                                  length=32,
                                  min_occurrences=raw_value,
                                  max_occurrences=raw_value)]

        self.continuation_length_formula_1 = continuation_length_formula
        self.continuation_length_formula_2 = lambda raw_value: [TextDataRecord(name="BCD digits",
                                                                               encoding=TextEncoding.BCD,
                                                                               min_occurrences=raw_value,
                                                                               max_occurrences=raw_value)]
        self.formula_data_record_1 = ConditionalFormulaDataRecord(
            formula=self.continuation_length_formula_1,
            default_message_continuation=DEFAULT_DIAGNOSTIC_MESSAGE_CONTINUATION)
        self.formula_data_record_2 = ConditionalFormulaDataRecord(
            formula=self.continuation_length_formula_2)

    # getitem

    @pytest.mark.parametrize("length", [1, 20])
    def test_getitem_1(self, length):
        continuation = self.formula_data_record_1[length]
        assert len(continuation) == 1
        assert isinstance(continuation[0], RawDataRecord)
        assert continuation[0].min_occurrences == length
        assert continuation[0].max_occurrences == length

    @pytest.mark.parametrize("length", [0, 21])
    def test_getitem_1__value_error(self, length):
        with pytest.raises(ValueError):
            self.formula_data_record_1[length]

    @pytest.mark.parametrize("length", [1, 20])
    def test_getitem_2(self, length):
        continuation = self.formula_data_record_2[length]
        assert len(continuation) == 1
        assert isinstance(continuation[0], TextDataRecord)
        assert continuation[0].min_occurrences == length
        assert continuation[0].max_occurrences == length

    # get_message_continuation

    @pytest.mark.parametrize("length", [0, 21])
    def test_get_message_continuation_1(self, length):
        assert self.formula_data_record_1.get_message_continuation(length) == DEFAULT_DIAGNOSTIC_MESSAGE_CONTINUATION

    @pytest.mark.parametrize("length", [0, -1])
    def test_get_message_continuation_2__value_error(self, length):
        with pytest.raises(ValueError):
            self.formula_data_record_2.get_message_continuation(length)

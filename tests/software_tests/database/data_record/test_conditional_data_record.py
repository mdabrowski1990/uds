import pytest
from mock import MagicMock, Mock, call, patch

from uds.database.data_record.conditional_data_record import (
    DEFAULT_DIAGNOSTIC_MESSAGE_CONTINUATION,
    AbstractConditionalDataRecord,
    AbstractDataRecord,
    ConditionalFormulaDataRecord,
    ConditionalMappingDataRecord,
    InconsistentArgumentsError,
    Mapping,
    Sequence,
)

SCRIPT_LOCATION = "uds.database.data_record.conditional_data_record"


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

    @pytest.mark.parametrize("value", [range(10), DEFAULT_DIAGNOSTIC_MESSAGE_CONTINUATION])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_validate_message_continuation__value_error(self, mock_isinstance, value):
        mock_isinstance.side_effect = [True, False]
        with pytest.raises(ValueError):
            AbstractConditionalDataRecord.validate_message_continuation(value)
        mock_isinstance.assert_has_calls([call(value, Sequence),
                                          call(value[0], AbstractDataRecord)], any_order=False)

    @pytest.mark.parametrize("value", [
        7 * [Mock(length=1)],
        [Mock(length=15)],
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_validate_message_continuation__inconsistent(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        with pytest.raises(InconsistentArgumentsError):
            AbstractConditionalDataRecord.validate_message_continuation(value)
        mock_isinstance.assert_has_calls([call(value, Sequence)] +
                                         [call(element, AbstractDataRecord) for element in value],
                                         any_order=False)

    @pytest.mark.parametrize("value", [
        8 * [Mock(length=1)],
        [Mock(length=16)],
        []
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_validate_message_continuation__valid(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        assert AbstractConditionalDataRecord.validate_message_continuation(value) is None
        mock_isinstance.assert_has_calls([call(value, Sequence)] +
                                         [call(element, AbstractDataRecord) for element in value],
                                         any_order=False)

    # get_message_continuation

    @pytest.mark.parametrize("raw_value", [Mock(), 0])
    def test_get_message_continuation__valid(self, raw_value):
        assert AbstractConditionalDataRecord.get_message_continuation(
            self.mock_conditional_data_record,
            raw_value=raw_value) == self.mock_conditional_data_record.__getitem__.return_value
        self.mock_conditional_data_record.__getitem__.assert_called_once_with(raw_value)

    @pytest.mark.parametrize("raw_value", [Mock(), 0])
    def test_get_message_continuation__default(self, raw_value):
        self.mock_conditional_data_record.__getitem__.side_effect = KeyError
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

    @pytest.mark.parametrize("raw_values_mapping, default_message_continuation", [
        (Mock(), Mock()),
        ({1: Mock(), 2: []}, DEFAULT_DIAGNOSTIC_MESSAGE_CONTINUATION),
    ])
    def test_init(self, raw_values_mapping, default_message_continuation):
        assert ConditionalMappingDataRecord.__init__(self.mock_conditional_data_record,
                                                     default_message_continuation=default_message_continuation,
                                                     raw_values_mapping=raw_values_mapping) is None
        assert self.mock_conditional_data_record.raw_values_mapping == raw_values_mapping
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
    def test_getitem__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        with pytest.raises(ValueError):
            ConditionalMappingDataRecord.__getitem__(self.mock_conditional_data_record, value)
        mock_isinstance.assert_called_once_with(value, int)

    @pytest.mark.parametrize("value", [0, 25])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_getitem__key_error(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        mock_getitem = Mock(side_effect=KeyError)
        self.mock_conditional_data_record.raw_values_mapping = MagicMock(__getitem__=mock_getitem)
        with pytest.raises(KeyError):
            ConditionalMappingDataRecord.__getitem__(self.mock_conditional_data_record, value)
        mock_isinstance.assert_called_once_with(value, int)
        mock_getitem.assert_called_once_with(value)

    @pytest.mark.parametrize("value", [0, 25])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_getitem__valid(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        mock_getitem = Mock()
        self.mock_conditional_data_record.raw_values_mapping = MagicMock(__getitem__=mock_getitem)
        assert (ConditionalMappingDataRecord.__getitem__(self.mock_conditional_data_record, value)
                == mock_getitem.return_value)
        mock_isinstance.assert_called_once_with(value, int)
        mock_getitem.assert_called_once_with(value)

    # raw_values_mapping

    def test_raw_values_mapping__get(self):
        self.mock_conditional_data_record._ConditionalMappingDataRecord__raw_values_mapping = Mock()
        assert (ConditionalMappingDataRecord.raw_values_mapping.fget(self.mock_conditional_data_record)
                == self.mock_conditional_data_record._ConditionalMappingDataRecord__raw_values_mapping)

    @pytest.mark.parametrize("value", [Mock(), "Some value"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_raw_values_mapping__set__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            ConditionalMappingDataRecord.raw_values_mapping.fset(self.mock_conditional_data_record, value)
        mock_isinstance.assert_called_once_with(value, Mapping)

    @pytest.mark.parametrize("value", [{-1: Mock()}, {-50: Mock(), 0: Mock(), 32: Mock()}])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_raw_values_mapping__set__value_error__value(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        with pytest.raises(ValueError):
            ConditionalMappingDataRecord.raw_values_mapping.fset(self.mock_conditional_data_record, value)
        mock_isinstance.assert_called()
        self.mock_conditional_data_record.validate_message_continuation.assert_not_called()

    @pytest.mark.parametrize("value", [{1: Mock()}, {0: Mock(), 32: Mock(), 2: Mock(), 3: []}])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_raw_values_mapping__set__value_error__type(self, mock_isinstance, value):
        mock_isinstance.side_effect = [True, False]
        with pytest.raises(ValueError):
            ConditionalMappingDataRecord.raw_values_mapping.fset(self.mock_conditional_data_record, value)
        mock_isinstance.assert_called()
        self.mock_conditional_data_record.validate_message_continuation.assert_not_called()

    @pytest.mark.parametrize("value", [{1: Mock()}, {0: Mock(), 32: Mock(), 2: Mock(), 3: []}])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_raw_values_mapping__set__valid(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        assert ConditionalMappingDataRecord.raw_values_mapping.fset(self.mock_conditional_data_record, value) is None
        assert (self.mock_conditional_data_record._ConditionalMappingDataRecord__raw_values_mapping
                == self.mock_mapping_proxy_type.return_value)
        mock_isinstance.assert_has_calls([call(value, Mapping)] + [call(key, int) for key in value.keys()],
                                         any_order=True)
        self.mock_conditional_data_record.validate_message_continuation.assert_has_calls(
            [call(i) for i in value.values()], any_order=True)
        self.mock_mapping_proxy_type.assert_called_once_with(value)


class TestConditionalFormulaDataRecord:
    """Unit tests for `ConditionalFormulaDataRecord` class"""


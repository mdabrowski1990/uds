import pytest
from mock import Mock, patch

from uds.translator.data_record_definitions.formula import (
    COMPARE_VALUE,
    COMPARISON_LOGIC,
    DID_2013,
    DID_2020,
    DID_BIT_LENGTH,
    DID_DATA_MAPPING_2013,
    DID_DATA_MAPPING_2020,
    DID_MAPPING_2013,
    DID_MAPPING_2020,
    DTC_STATUS_MASK,
    HYSTERESIS_VALUE,
    LOCALIZATION,
    REPORT_TYPE_2020,
    RESERVED_BIT,
    get_conditional_event_type_record_09_2020,
    get_did_2013,
    get_did_2020,
    get_did_data_2013,
    get_did_data_2020,
    get_did_data_mask_2013,
    get_did_data_mask_2020,
    get_did_records_formula_2013,
    get_did_records_formula_2020,
    get_dids_2013,
    get_dids_2020,
    get_event_type_record_01,
    get_event_type_record_03_2013,
    get_event_type_record_03_2020,
    get_event_type_record_07_2013,
    get_event_type_record_07_2020,
    get_event_type_record_09_2020,
)

SCRIPT_LOCATION = "uds.translator.data_record_definitions.formula"


class TestFunctions:
    """Unit tests for module functions."""

    def setup_method(self):
        self._patcher_raw_data_record = patch(f"{SCRIPT_LOCATION}.RawDataRecord")
        self.mock_raw_data_record = self._patcher_raw_data_record.start()
        self._patcher_mapping_data_record = patch(f"{SCRIPT_LOCATION}.MappingDataRecord")
        self.mock_mapping_data_record = self._patcher_mapping_data_record.start()
        self._patcher_conditional_mapping_data_record = patch(f"{SCRIPT_LOCATION}.ConditionalMappingDataRecord")
        self.mock_conditional_mapping_data_record = self._patcher_conditional_mapping_data_record.start()
        self._patcher_conditional_formula_data_record = patch(f"{SCRIPT_LOCATION}.ConditionalFormulaDataRecord")
        self.mock_conditional_formula_data_record = self._patcher_conditional_formula_data_record.start()

    def teardown_method(self):
        self._patcher_raw_data_record.stop()
        self._patcher_mapping_data_record.stop()
        self._patcher_conditional_mapping_data_record.stop()
        self._patcher_conditional_formula_data_record.stop()

    # get_did_2020

    @pytest.mark.parametrize("name, optional", [
        ("some name", False),
        ("DID#ABC", True),
    ])
    def test_get_did_2020(self, name, optional):
        assert get_did_2020(name=name,
                            optional=optional) == self.mock_mapping_data_record.return_value
        self.mock_mapping_data_record.assert_called_once_with(name=name,
                                                              length=16,
                                                              values_mapping=DID_MAPPING_2020,
                                                              min_occurrences=int(optional) ^ 1,
                                                              max_occurrences=1)

    # get_did_2013

    @pytest.mark.parametrize("name, optional", [
        ("some name", False),
        ("DID#ABC", True),
    ])
    def test_get_did_2013(self, name, optional):
        assert get_did_2013(name=name,
                            optional=optional) == self.mock_mapping_data_record.return_value
        self.mock_mapping_data_record.assert_called_once_with(name=name,
                                                              length=16,
                                                              values_mapping=DID_MAPPING_2013,
                                                              min_occurrences=int(optional) ^ 1,
                                                              max_occurrences=1)

    # get_dids_2020

    @pytest.mark.parametrize("did_count, record_number", [
        (1, None),
        (7, 5),
    ])
    @patch(f"{SCRIPT_LOCATION}.get_did_data_2020")
    @patch(f"{SCRIPT_LOCATION}.get_did_2020")
    def test_get_dids_2020(self, mock_get_did_2020, mock_get_did_data_2020,
                                                  did_count, record_number):
        assert (get_dids_2020(did_count=did_count, record_number=record_number)
                == (mock_get_did_2020.return_value, mock_get_did_data_2020.return_value) * did_count)

    # get_dids_2013

    @pytest.mark.parametrize("did_count, record_number", [
        (1, None),
        (7, 5),
    ])
    @patch(f"{SCRIPT_LOCATION}.get_did_data_2013")
    @patch(f"{SCRIPT_LOCATION}.get_did_2013")
    def test_get_dids_2013(self, mock_get_did_2013, mock_get_did_data_2013,
                                                  did_count, record_number):
        assert (get_dids_2013(did_count=did_count, record_number=record_number)
                == (mock_get_did_2013.return_value, mock_get_did_data_2013.return_value) * did_count)

    # get_did_data_2020

    def test_get_did_data_2020(self):
        assert get_did_data_2020() == self.mock_conditional_formula_data_record.return_value

    def test_get_did_data_2020__formula(self):
        undefined_did = -1
        some_defined_did = tuple(DID_DATA_MAPPING_2020.keys())[0]
        incorrect_did = 0x10000
        DID_DATA_MAPPING_2020[incorrect_did] = [Mock(fixed_total_length=False)]
        input_kwargs = {}
        self.mock_conditional_formula_data_record.side_effect = lambda **kwargs: input_kwargs.update(kwargs)
        get_did_data_2020()
        with pytest.raises(ValueError):
            input_kwargs["formula"](undefined_did)
        with pytest.raises(ValueError):
            input_kwargs["formula"](incorrect_did)
        assert input_kwargs["formula"](some_defined_did) == (self.mock_raw_data_record.return_value, )

    # get_did_data_2013

    def test_get_did_data_2013(self):
        assert get_did_data_2013() == self.mock_conditional_formula_data_record.return_value

    def test_get_did_data_2013__formula(self):
        undefined_did = -1
        some_defined_did = tuple(DID_DATA_MAPPING_2013.keys())[0]
        incorrect_did = 0x10000
        DID_DATA_MAPPING_2013[incorrect_did] = [Mock(fixed_total_length=False)]
        input_kwargs = {}
        self.mock_conditional_formula_data_record.side_effect = lambda **kwargs: input_kwargs.update(kwargs)
        get_did_data_2013()
        with pytest.raises(ValueError):
            input_kwargs["formula"](undefined_did)
        with pytest.raises(ValueError):
            input_kwargs["formula"](incorrect_did)
        assert input_kwargs["formula"](some_defined_did) == (self.mock_raw_data_record.return_value, )

    # get_did_records_formula_2020

    @patch(f"{SCRIPT_LOCATION}.get_dids_2020")
    def test_get_did_records_formula_2020(self, mock_get_dids_2020):
        mock_record_number = Mock()
        mock_did_count = Mock()
        formula = get_did_records_formula_2020(mock_record_number)
        assert callable(formula)
        assert formula(mock_did_count) == mock_get_dids_2020.return_value
        mock_get_dids_2020.assert_called_once_with(did_count=mock_did_count,
                                                   record_number=mock_record_number)

    # get_did_records_formula_2013

    @patch(f"{SCRIPT_LOCATION}.get_dids_2013")
    def test_get_did_records_formula_2013(self, mock_get_dids_2013):
        mock_record_number = Mock()
        mock_did_count = Mock()
        formula = get_did_records_formula_2013(mock_record_number)
        assert callable(formula)
        assert formula(mock_did_count) == mock_get_dids_2013.return_value
        mock_get_dids_2013.assert_called_once_with(did_count=mock_did_count,
                                                   record_number=mock_record_number)

    # get_did_data_mask_2020

    @pytest.mark.parametrize("name, optional", [
        (Mock(), False),
        ("SomeName", True),
    ])
    def test_get_did_data_mask_2020(self, name, optional):
        assert get_did_data_mask_2020(name=name,
                                      optional=optional) == self.mock_conditional_formula_data_record.return_value

    @pytest.mark.parametrize("name, optional", [
        (Mock(), False),
        ("SomeName", True),
    ])
    def test_get_did_data_mask_2020__formula(self, name, optional):
        undefined_did = -1
        some_defined_did = tuple(DID_DATA_MAPPING_2020.keys())[0]
        incorrect_did = 0x10000
        DID_DATA_MAPPING_2020[incorrect_did] = [Mock(fixed_total_length=False)]
        input_kwargs = {}
        self.mock_conditional_formula_data_record.side_effect = lambda **kwargs: input_kwargs.update(kwargs)
        get_did_data_mask_2020(name=name, optional=optional)
        with pytest.raises(ValueError):
            input_kwargs["formula"](undefined_did)
        with pytest.raises(ValueError):
            input_kwargs["formula"](incorrect_did)
        assert input_kwargs["formula"](some_defined_did) == (self.mock_raw_data_record.return_value, )

    # get_did_data_mask_2013

    @pytest.mark.parametrize("name, optional", [
        (Mock(), False),
        ("SomeName", True),
    ])
    def test_get_did_data_mask_2013(self, name, optional):
        assert get_did_data_mask_2013(name=name,
                                      optional=optional) == self.mock_conditional_formula_data_record.return_value

    @pytest.mark.parametrize("name, optional", [
        (Mock(), False),
        ("SomeName", True),
    ])
    def test_get_did_data_mask_2013__formula(self, name, optional):
        undefined_did = -1
        some_defined_did = tuple(DID_DATA_MAPPING_2013.keys())[0]
        incorrect_did = 0x10000
        DID_DATA_MAPPING_2013[incorrect_did] = [Mock(fixed_total_length=False)]
        input_kwargs = {}
        self.mock_conditional_formula_data_record.side_effect = lambda **kwargs: input_kwargs.update(kwargs)
        get_did_data_mask_2013(name=name, optional=optional)
        with pytest.raises(ValueError):
            input_kwargs["formula"](undefined_did)
        with pytest.raises(ValueError):
            input_kwargs["formula"](incorrect_did)
        assert input_kwargs["formula"](some_defined_did) == (self.mock_raw_data_record.return_value, )

    # get_event_type_record_01

    def test_get_event_type_record_01__without_event_number(self):
        assert get_event_type_record_01() == self.mock_raw_data_record.return_value
        self.mock_raw_data_record.assert_called_once_with(name="eventTypeRecord",
                                                          length=8,
                                                          children=(DTC_STATUS_MASK,))

    @pytest.mark.parametrize("event_number", [1, 255])
    def test_get_event_type_record_01__with_event_number(self, event_number):
        assert get_event_type_record_01(event_number) == self.mock_raw_data_record.return_value
        self.mock_raw_data_record.assert_called_once_with(name=f"eventTypeRecord#{event_number}",
                                                          length=8,
                                                          children=(DTC_STATUS_MASK,))

    # get_event_type_record_03_2020

    def test_get_event_type_record_03_2020__without_event_number(self):
        assert get_event_type_record_03_2020() == self.mock_raw_data_record.return_value
        self.mock_raw_data_record.assert_called_once_with(name="eventTypeRecord",
                                                          length=DID_BIT_LENGTH,
                                                          children=(DID_2020,))

    @pytest.mark.parametrize("event_number", [1, 255])
    def test_get_event_type_record_03_2020__with_event_number(self, event_number):
        assert get_event_type_record_03_2020(event_number) == self.mock_raw_data_record.return_value
        self.mock_raw_data_record.assert_called_once_with(name=f"eventTypeRecord#{event_number}",
                                                          length=DID_BIT_LENGTH,
                                                          children=(DID_2020,))

    # get_event_type_record_03_2013

    def test_get_event_type_record_03_2013__without_event_number(self):
        assert get_event_type_record_03_2013() == self.mock_raw_data_record.return_value
        self.mock_raw_data_record.assert_called_once_with(name="eventTypeRecord",
                                                          length=DID_BIT_LENGTH,
                                                          children=(DID_2013,))

    @pytest.mark.parametrize("event_number", [1, 255])
    def test_get_event_type_record_03_2013__with_event_number(self, event_number):
        assert get_event_type_record_03_2013(event_number) == self.mock_raw_data_record.return_value
        self.mock_raw_data_record.assert_called_once_with(name=f"eventTypeRecord#{event_number}",
                                                          length=DID_BIT_LENGTH,
                                                          children=(DID_2013, ))

    # get_event_type_record_07_2020

    def test_get_event_type_record_07_2020__without_event_number(self):
        assert get_event_type_record_07_2020() == self.mock_raw_data_record.return_value
        self.mock_raw_data_record.assert_called_once_with(name="eventTypeRecord",
                                                          length=80,
                                                          children=(DID_2020,
                                                                    COMPARISON_LOGIC,
                                                                    COMPARE_VALUE,
                                                                    HYSTERESIS_VALUE,
                                                                    LOCALIZATION))

    @pytest.mark.parametrize("event_number", [1, 255])
    def test_get_event_type_record_07_2020__with_event_number(self, event_number):
        assert get_event_type_record_07_2020(event_number) == self.mock_raw_data_record.return_value
        self.mock_raw_data_record.assert_called_once_with(name=f"eventTypeRecord#{event_number}",
                                                          length=80,
                                                          children=(DID_2020,
                                                                    COMPARISON_LOGIC,
                                                                    COMPARE_VALUE,
                                                                    HYSTERESIS_VALUE,
                                                                    LOCALIZATION))

    # get_event_type_record_07_2013

    def test_get_event_type_record_07_2013__without_event_number(self):
        assert get_event_type_record_07_2013() == self.mock_raw_data_record.return_value
        self.mock_raw_data_record.assert_called_once_with(name="eventTypeRecord",
                                                          length=80,
                                                          children=(DID_2013,
                                                                    COMPARISON_LOGIC,
                                                                    COMPARE_VALUE,
                                                                    HYSTERESIS_VALUE,
                                                                    LOCALIZATION))

    @pytest.mark.parametrize("event_number", [1, 255])
    def test_get_event_type_record_07_2013__with_event_number(self, event_number):
        assert get_event_type_record_07_2013(event_number) == self.mock_raw_data_record.return_value
        self.mock_raw_data_record.assert_called_once_with(name=f"eventTypeRecord#{event_number}",
                                                          length=80,
                                                          children=(DID_2013,
                                                                    COMPARISON_LOGIC,
                                                                    COMPARE_VALUE,
                                                                    HYSTERESIS_VALUE,
                                                                    LOCALIZATION))

    # get_event_type_record_09_2020

    def test_get_event_type_record_09_2020__without_event_number(self):
        assert get_event_type_record_09_2020() == self.mock_raw_data_record.return_value
        self.mock_raw_data_record.assert_called_once_with(name="eventTypeRecord",
                                                          length=16,
                                                          children=(DTC_STATUS_MASK,
                                                                    RESERVED_BIT,
                                                                    REPORT_TYPE_2020))

    @pytest.mark.parametrize("event_number", [1, 255])
    def test_get_event_type_record_09_2020__with_event_number(self, event_number):
        assert get_event_type_record_09_2020(event_number) == self.mock_raw_data_record.return_value
        self.mock_raw_data_record.assert_called_once_with(name=f"eventTypeRecord#{event_number}",
                                                          length=16,
                                                          children=(DTC_STATUS_MASK,
                                                                    RESERVED_BIT,
                                                                    REPORT_TYPE_2020))

    # get_conditional_event_type_record_09_2020

    @pytest.mark.parametrize("event_number", [None, 1, 255])
    def test_get_conditional_event_type_record_09_2020(self, event_number):
        assert (get_conditional_event_type_record_09_2020(event_number)
                == self.mock_conditional_mapping_data_record.return_value)
        self.mock_conditional_mapping_data_record.assert_called_once()

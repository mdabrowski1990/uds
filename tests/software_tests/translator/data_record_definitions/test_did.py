import pytest
from mock import Mock, patch

from uds.translator.data_record_definitions.did import (
    DID_DATA_MAPPING_2013,
    DID_DATA_MAPPING_2020,
    DID_MAPPING_2013,
    DID_MAPPING_2020,
    get_did_2013,
    get_did_2020,
    get_did_data_2013,
    get_did_data_2020,
    get_did_records_formula_2013,
    get_did_records_formula_2020,
    get_dids_2013,
    get_dids_2020,
)

SCRIPT_LOCATION = "uds.translator.data_record_definitions.did"

class TestFunctions:
    """Unit tests for module functions."""

    def setup_method(self):
        self._patcher_raw_data_record = patch(f"{SCRIPT_LOCATION}.RawDataRecord")
        self.mock_raw_data_record = self._patcher_raw_data_record.start()
        self._patcher_mapping_data_record = patch(f"{SCRIPT_LOCATION}.MappingDataRecord")
        self.mock_mapping_data_record = self._patcher_mapping_data_record.start()
        self._patcher_conditional_formula_data_record = patch(f"{SCRIPT_LOCATION}.ConditionalFormulaDataRecord")
        self.mock_conditional_formula_data_record = self._patcher_conditional_formula_data_record.start()

    def teardown_method(self):
        self._patcher_raw_data_record.stop()
        self._patcher_mapping_data_record.stop()
        self._patcher_conditional_formula_data_record.stop()

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

    # get_did_data_2013

    def test_get_did_data_2013(self):
        undefined_did = -1
        some_defined_did = tuple(DID_DATA_MAPPING_2013.keys())[0]
        incorrect_did = 0x10000
        DID_DATA_MAPPING_2013[incorrect_did] = [Mock(fixed_total_length=False)]
        input_kwargs = {}
        self.mock_conditional_formula_data_record.side_effect = lambda **kwargs: input_kwargs.update(kwargs)
        get_did_data_2013(Mock())
        with pytest.raises(ValueError):
            input_kwargs["formula"](undefined_did)
        with pytest.raises(ValueError):
            input_kwargs["formula"](incorrect_did)
        assert input_kwargs["formula"](some_defined_did) == (self.mock_raw_data_record.return_value, )

    # get_did_data_2020

    def test_get_did_data_2020(self):
        undefined_did = -1
        some_defined_did = tuple(DID_DATA_MAPPING_2020.keys())[0]
        incorrect_did = 0x10000
        DID_DATA_MAPPING_2020[incorrect_did] = [Mock(fixed_total_length=False)]
        input_kwargs = {}
        self.mock_conditional_formula_data_record.side_effect = lambda **kwargs: input_kwargs.update(kwargs)
        get_did_data_2020(Mock())
        with pytest.raises(ValueError):
            input_kwargs["formula"](undefined_did)
        with pytest.raises(ValueError):
            input_kwargs["formula"](incorrect_did)
        assert input_kwargs["formula"](some_defined_did) == (self.mock_raw_data_record.return_value, )

    # get_dids_2013

    @pytest.mark.parametrize("did_count, record_number", [
        (1, None),
        (7, 5),
    ])
    @patch(f"{SCRIPT_LOCATION}.get_did_data_2013")
    @patch(f"{SCRIPT_LOCATION}.get_did_2013")
    def test_get_dids_2013__without_record_number(self, mock_get_did_2013, mock_get_did_data_2013,
                                                  did_count, record_number):
        assert (get_dids_2013(did_count=did_count, record_number=record_number)
                == (mock_get_did_2013.return_value, mock_get_did_data_2013.return_value) * did_count)

    # get_dids_2020

    @pytest.mark.parametrize("did_count, record_number", [
        (1, None),
        (7, 5),
    ])
    @patch(f"{SCRIPT_LOCATION}.get_did_data_2020")
    @patch(f"{SCRIPT_LOCATION}.get_did_2020")
    def test_get_dids_2020__without_record_number(self, mock_get_did_2020, mock_get_did_data_2020,
                                                  did_count, record_number):
        assert (get_dids_2020(did_count=did_count, record_number=record_number)
                == (mock_get_did_2020.return_value, mock_get_did_data_2020.return_value) * did_count)

    # get_did_records_formula_2013

    def test_get_did_records_formula_2013(self):
        assert callable(get_did_records_formula_2013(Mock()))

    # get_did_records_formula_2020

    def test_get_did_records_formula_2020(self):
        assert callable(get_did_records_formula_2020(Mock()))

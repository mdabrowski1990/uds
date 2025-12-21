import pytest
from mock import patch

from uds.translator.data_record_definitions.formula import (
    get_conditional_event_type_record_09_2020,
    get_event_type_record_01,
    get_event_type_record_09_2020,
    DTC_STATUS_MASK,
    REPORT_TYPE_2020,
    RESERVED_BIT,
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

    def teardown_method(self):
        self._patcher_raw_data_record.stop()
        self._patcher_mapping_data_record.stop()
        self._patcher_conditional_mapping_data_record.stop()

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

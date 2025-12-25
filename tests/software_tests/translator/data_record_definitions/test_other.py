import pytest
from mock import patch

from uds.translator.data_record_definitions.other import (
    ANTI_REPLAY_COUNTER,
    EVENT_TYPE_2013,
    EVENT_TYPE_2020,
    INTERNAL_REQUEST_PARAMETERS,
    INTERNAL_RESPONSE_PARAMETERS,
    INTERNAL_RSID,
    INTERNAL_SID,
    REPORT_TYPE_2020,
    RESERVED_BIT,
    TIMER_SCHEDULE,
    get_event_type_of_active_event_2013,
    get_event_type_of_active_event_2020,
    get_event_type_record_02,
    get_event_type_record_08_2020,
    get_event_window_2013,
    get_event_window_2020,
    get_secured_data_transmission_request,
    get_secured_data_transmission_response,
    get_service_to_respond,
)

SCRIPT_LOCATION = "uds.translator.data_record_definitions.other"

class TestFormulas:

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









    # get_secured_data_transmission_request

    def test_get_secured_data_transmission_request__0(self):
        assert get_secured_data_transmission_request(0) == (ANTI_REPLAY_COUNTER,
                                                            INTERNAL_SID,
                                                            INTERNAL_REQUEST_PARAMETERS)

    @pytest.mark.parametrize("signature_length", [1, 0xFFFF])
    def test_get_secured_data_transmission_request(self, signature_length):
        assert get_secured_data_transmission_request(signature_length) == (ANTI_REPLAY_COUNTER,
                                                                           INTERNAL_SID,
                                                                           INTERNAL_REQUEST_PARAMETERS,
                                                                           self.mock_raw_data_record.return_value)
        self.mock_raw_data_record.assert_called_once_with(name="Signature/MAC",
                                                          length=8,
                                                          min_occurrences=signature_length,
                                                          max_occurrences=signature_length,
                                                          enforce_reoccurring=True)

    # get_secured_data_transmission_response

    def test_get_secured_data_transmission_response__0(self):
        assert get_secured_data_transmission_response(0) == (ANTI_REPLAY_COUNTER,
                                                             INTERNAL_RSID,
                                                             INTERNAL_RESPONSE_PARAMETERS)

    @pytest.mark.parametrize("signature_length", [1, 0xFFFF])
    def test_get_secured_data_transmission_response(self, signature_length):
        assert get_secured_data_transmission_response(signature_length) == (ANTI_REPLAY_COUNTER,
                                                                            INTERNAL_RSID,
                                                                            INTERNAL_RESPONSE_PARAMETERS,
                                                                            self.mock_raw_data_record.return_value)
        self.mock_raw_data_record.assert_called_once_with(name="Signature/MAC",
                                                          length=8,
                                                          min_occurrences=signature_length,
                                                          max_occurrences=signature_length,
                                                          enforce_reoccurring=True)

    # get_event_window_2013

    def test_get_event_window_2013__without_event_number(self):
        assert get_event_window_2013() == self.mock_mapping_data_record.return_value
        self.mock_mapping_data_record.assert_called_once_with(name="eventWindowTime",
                                                              length=8,
                                                              values_mapping={  # TODO: replace with a mapping variable (https://github.com/mdabrowski1990/uds/issues/413)
                                                                  0x02: "infiniteTimeToResponse",
                                                              })

    @pytest.mark.parametrize("event_number", [1, 32])
    def test_get_event_window_2013__with_event_number(self, event_number):
        assert get_event_window_2013(event_number) == self.mock_mapping_data_record.return_value
        self.mock_mapping_data_record.assert_called_once_with(name=f"eventWindowTime#{event_number}",
                                                              length=8,
                                                              values_mapping={  # TODO: replace with a mapping variable (https://github.com/mdabrowski1990/uds/issues/413)
                                                                  0x02: "infiniteTimeToResponse",
                                                              })
        
    # get_event_window_2020

    def test_get_event_window_2020__without_event_number(self):
        assert get_event_window_2020() == self.mock_mapping_data_record.return_value
        self.mock_mapping_data_record.assert_called_once_with(name="eventWindowTime",
                                                              length=8,
                                                              values_mapping={  # TODO: replace with a mapping variable (https://github.com/mdabrowski1990/uds/issues/413)
                                                                  0x02: "infiniteTimeToResponse",
                                                                  0x03: "shortEventWindowTime",
                                                                  0x04: "mediumEventWindowTime",
                                                                  0x05: "longEventWindowTime",
                                                                  0x06: "powerWindowTime",
                                                                  0x07: "ignitionWindowTime",
                                                                  0x08: "manufacturerTriggerEventWindowTime",
                                                              })

    @pytest.mark.parametrize("event_number", [1, 32])
    def test_get_event_window_2020__with_event_number(self, event_number):
        assert get_event_window_2020(event_number) == self.mock_mapping_data_record.return_value
        self.mock_mapping_data_record.assert_called_once_with(name=f"eventWindowTime#{event_number}",
                                                              length=8,
                                                              values_mapping={  # TODO: replace with a mapping variable (https://github.com/mdabrowski1990/uds/issues/413)
                                                                  0x02: "infiniteTimeToResponse",
                                                                  0x03: "shortEventWindowTime",
                                                                  0x04: "mediumEventWindowTime",
                                                                  0x05: "longEventWindowTime",
                                                                  0x06: "powerWindowTime",
                                                                  0x07: "ignitionWindowTime",
                                                                  0x08: "manufacturerTriggerEventWindowTime",
                                                              })

    # get_service_to_respond

    def test_get_service_to_respond__without_event_number(self):
        assert get_service_to_respond() == self.mock_raw_data_record.return_value
        self.mock_raw_data_record.assert_called_once_with(name="serviceToRespondToRecord",
                                                          length=8,
                                                          min_occurrences=1,
                                                          max_occurrences=None)

    @pytest.mark.parametrize("event_number", [1, 32])
    def test_get_service_to_respond__with_event_number(self, event_number):
        assert get_service_to_respond(event_number) == self.mock_raw_data_record.return_value
        self.mock_raw_data_record.assert_called_once_with(name=f"serviceToRespondToRecord#{event_number}",
                                                          length=8,
                                                          min_occurrences=1,
                                                          max_occurrences=None)

    # event_type_of_active_event_2013

    @pytest.mark.parametrize("event_number", [1, 32])
    def test_event_type_of_active_event_2013(self, event_number):
        assert get_event_type_of_active_event_2013(event_number) == self.mock_raw_data_record.return_value
        self.mock_raw_data_record.assert_called_once_with(name=f"eventTypeOfActiveEvent#{event_number}",
                                                          length=8,
                                                          children=(RESERVED_BIT,
                                                                    EVENT_TYPE_2013))

    # event_type_of_active_event_2020

    @pytest.mark.parametrize("event_number", [1, 32])
    def test_event_type_of_active_event_2020(self, event_number):
        assert get_event_type_of_active_event_2020(event_number) == self.mock_raw_data_record.return_value
        self.mock_raw_data_record.assert_called_once_with(name=f"eventTypeOfActiveEvent#{event_number}",
                                                          length=8,
                                                          children=(RESERVED_BIT,
                                                                    EVENT_TYPE_2020))

    # get_event_type_record_02

    def test_get_event_type_record_02__without_event_number(self):
        assert get_event_type_record_02() == self.mock_raw_data_record.return_value
        self.mock_raw_data_record.assert_called_once_with(name="eventTypeRecord",
                                                          length=8,
                                                          children=(TIMER_SCHEDULE,))

    @pytest.mark.parametrize("event_number", [1, 32])
    def test_get_event_type_record_02__with_event_number(self, event_number):
        assert get_event_type_record_02(event_number) == self.mock_raw_data_record.return_value
        self.mock_raw_data_record.assert_called_once_with(name=f"eventTypeRecord#{event_number}",
                                                          length=8,
                                                          children=(TIMER_SCHEDULE,))

    # get_event_type_record_08
    
    def test_get_event_type_record_08__without_event_number(self):
        assert get_event_type_record_08_2020() == self.mock_raw_data_record.return_value
        self.mock_raw_data_record.assert_called_once_with(name="eventTypeRecord",
                                                          length=8,
                                                          children=(RESERVED_BIT,
                                                                    REPORT_TYPE_2020))

    @pytest.mark.parametrize("event_number", [1, 32])
    def test_get_event_type_record_08__with_event_number(self, event_number):
        assert get_event_type_record_08_2020(event_number) == self.mock_raw_data_record.return_value
        self.mock_raw_data_record.assert_called_once_with(name=f"eventTypeRecord#{event_number}",
                                                          length=8,
                                                          children=(RESERVED_BIT,
                                                                    REPORT_TYPE_2020))
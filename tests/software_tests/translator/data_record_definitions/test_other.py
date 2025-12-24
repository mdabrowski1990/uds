import pytest
from mock import Mock, call, patch

from uds.translator.data_record_definitions.other import (
    ANTI_REPLAY_COUNTER,
    COMMUNICATION_TYPE,
    EVENT_TYPE_2013,
    EVENT_TYPE_2020,
    EXPONENT,
    EXPONENT_BIT_LENGTH,
    FORMULA_IDENTIFIER,
    INTERNAL_REQUEST_PARAMETERS,
    INTERNAL_RESPONSE_PARAMETERS,
    INTERNAL_RSID,
    INTERNAL_SID,
    MANTISSA,
    MANTISSA_BIT_LENGTH,
    NODE_IDENTIFICATION_NUMBER,
    REPORT_TYPE_2020,
    RESERVED_BIT,
    SECURITY_ACCESS_DATA,
    SECURITY_KEY,
    SECURITY_SEED,
    STATE_AND_CONNECTION_TYPE,
    TIMER_SCHEDULE,
    UNIT_OR_FORMAT,
    TextEncoding,
    get_communication_control_request,
    get_dir_info,
    get_event_type_of_active_event_2013,
    get_event_type_of_active_event_2020,
    get_event_type_record_02,
    get_event_type_record_08_2020,
    get_event_window_2013,
    get_event_window_2020,
    get_file_path_and_name,
    get_file_sizes,
    get_file_sizes_or_dir_info,
    get_secured_data_transmission_request,
    get_secured_data_transmission_response,
    get_security_access_request,
    get_security_access_response,
    get_service_to_respond,
)

SCRIPT_LOCATION = "uds.translator.data_record_definitions.other"

class TestFormulas:

    def setup_method(self):
        self._patcher_raw_data_record = patch(f"{SCRIPT_LOCATION}.RawDataRecord")
        self.mock_raw_data_record = self._patcher_raw_data_record.start()
        self._patcher_mapping_data_record = patch(f"{SCRIPT_LOCATION}.MappingDataRecord")
        self.mock_mapping_data_record = self._patcher_mapping_data_record.start()
        self._patcher_text_data_record = patch(f"{SCRIPT_LOCATION}.TextDataRecord")
        self.mock_text_data_record = self._patcher_text_data_record.start()
        self._patcher_conditional_formula_data_record = patch(f"{SCRIPT_LOCATION}.ConditionalFormulaDataRecord")
        self.mock_conditional_formula_data_record = self._patcher_conditional_formula_data_record.start()

    def teardown_method(self):
        self._patcher_raw_data_record.stop()
        self._patcher_mapping_data_record.stop()
        self._patcher_text_data_record.stop()
        self._patcher_conditional_formula_data_record.stop()


    








    # get_file_path_and_name

    def test_get_file_path_and_name__value_error(self):
        with pytest.raises(ValueError):
            get_file_path_and_name(0x00)

    @pytest.mark.parametrize("file_path_and_name_length", [1, 0xFF])
    def test_get_file_path_and_name(self, file_path_and_name_length):
        assert get_file_path_and_name(file_path_and_name_length) == (self.mock_text_data_record.return_value,)
        self.mock_text_data_record.assert_called_once_with(name="filePathAndName",
                                                           encoding=TextEncoding.ASCII,
                                                           min_occurrences=file_path_and_name_length,
                                                           max_occurrences=file_path_and_name_length,
                                                           enforce_reoccurring=True)

    # get_file_sizes

    def test_get_file_sizes__value_error(self):
        with pytest.raises(ValueError):
            get_file_sizes(0x00)

    @pytest.mark.parametrize("file_size_or_dir_info_parameter_length", [1, 0xFF])
    def test_get_file_sizes(self, file_size_or_dir_info_parameter_length):
        assert (get_file_sizes(file_size_or_dir_info_parameter_length)
                == (self.mock_raw_data_record.return_value, self.mock_raw_data_record.return_value))
        self.mock_raw_data_record.assert_has_calls([call(name="fileSizeUnCompressed",
                                                         length=8 * file_size_or_dir_info_parameter_length,
                                                         unit="bytes"),
                                                    call(name="fileSizeCompressed",
                                                         length=8 * file_size_or_dir_info_parameter_length,
                                                         unit="bytes")],
                                                   any_order=False)

    # get_file_sizes_or_dir_info

    def test_get_file_sizes_or_dir_info__value_error(self):
        with pytest.raises(ValueError):
            get_file_sizes_or_dir_info(0x00)

    @pytest.mark.parametrize("file_size_or_dir_info_parameter_length", [1, 0xFF])
    def test_get_file_sizes_or_dir_info(self, file_size_or_dir_info_parameter_length):
        assert (get_file_sizes_or_dir_info(file_size_or_dir_info_parameter_length)
                == (self.mock_raw_data_record.return_value, self.mock_raw_data_record.return_value))
        self.mock_raw_data_record.assert_has_calls([call(name="fileSizeUncompressedOrDirInfoLength",
                                                         length=8 * file_size_or_dir_info_parameter_length,
                                                         unit="bytes"),
                                                    call(name="fileSizeCompressed",
                                                         length=8 * file_size_or_dir_info_parameter_length,
                                                         unit="bytes")],
                                                   any_order=False)

    # get_dir_info

    def test_get_dir_info__value_error(self):
        with pytest.raises(ValueError):
            get_dir_info(0x00)

    @pytest.mark.parametrize("file_size_or_dir_info_parameter_length", [1, 0xFF])
    def test_get_dir_info(self, file_size_or_dir_info_parameter_length):
        assert get_dir_info(file_size_or_dir_info_parameter_length) == (self.mock_raw_data_record.return_value,)
        self.mock_raw_data_record.assert_called_once_with(name="fileSizeUncompressedOrDirInfoLength",
                                                          length=8 * file_size_or_dir_info_parameter_length,
                                                          unit="bytes")

    # get_security_access_request

    @pytest.mark.parametrize("sub_function", [1, 93, 253])
    def test_get_security_access_request__odd(self, sub_function):
        assert get_security_access_request(sub_function) == (SECURITY_ACCESS_DATA,)

    @pytest.mark.parametrize("sub_function", [2, 48, 254])
    def test_get_security_access_request__even(self, sub_function):
        assert get_security_access_request(sub_function) == (SECURITY_KEY,)

    # get_security_access_response

    @pytest.mark.parametrize("sub_function", [1, 93, 253])
    def test_get_security_access_response__odd(self, sub_function):
        assert get_security_access_response(sub_function) == (SECURITY_SEED,)

    @pytest.mark.parametrize("sub_function", [2, 48, 254])
    def test_get_security_access_response__even(self, sub_function):
        assert get_security_access_response(sub_function) == ()

    # get_communication_control_request

    @pytest.mark.parametrize("sub_function", [0x04, 0x05, 0x84, 0x85])
    def test_get_communication_control_request__special(self, sub_function):
        assert get_communication_control_request(sub_function) == (COMMUNICATION_TYPE, NODE_IDENTIFICATION_NUMBER)

    @pytest.mark.parametrize("sub_function", [0x03, 0x06, 0xB4])
    def test_get_communication_control_request__other(self, sub_function):
        assert get_communication_control_request(sub_function) == (COMMUNICATION_TYPE,)

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
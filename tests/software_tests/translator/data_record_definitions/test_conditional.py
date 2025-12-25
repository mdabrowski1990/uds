from mock import Mock, patch

from uds.translator.data_record_definitions.conditional import (
    INPUT_OUTPUT_CONTROL_PARAMETER,
    get_input_output_control_by_identifier_request_2013,
    get_input_output_control_by_identifier_request_2020,
    get_input_output_control_by_identifier_response_2013,
    get_input_output_control_by_identifier_response_2020,
)

SCRIPT_LOCATION = "uds.translator.data_record_definitions.conditional"

class TestInputOutputControlByIdentifier:
    """Unit tests for `InputOutputControlByIdentifier` service."""

    def setup_method(self):
        self._patcher_conditional_mapping_data_record = patch(f"{SCRIPT_LOCATION}.ConditionalMappingDataRecord")
        self.mock_conditional_mapping_data_record = self._patcher_conditional_mapping_data_record.start()
        self._patcher_conditional_control_state_2013 = patch(f"{SCRIPT_LOCATION}.CONDITIONAL_CONTROL_STATE_2013")
        self.mock_conditional_control_state_2013 = self._patcher_conditional_control_state_2013.start()
        self._patcher_conditional_control_state_2020 = patch(f"{SCRIPT_LOCATION}.CONDITIONAL_CONTROL_STATE_2020")
        self.mock_conditional_control_state_2020 = self._patcher_conditional_control_state_2020.start()
        self._patcher_conditional_control_enable_mask_2013 \
            = patch(f"{SCRIPT_LOCATION}.CONDITIONAL_OPTIONAL_CONTROL_ENABLE_MASK_2013")
        self.mock_conditional_control_enable_mask_2013 = self._patcher_conditional_control_enable_mask_2013.start()
        self._patcher_conditional_control_enable_mask_2020 \
            = patch(f"{SCRIPT_LOCATION}.CONDITIONAL_OPTIONAL_CONTROL_ENABLE_MASK_2020")
        self.mock_conditional_control_enable_mask_2020 = self._patcher_conditional_control_enable_mask_2020.start()

    def teardown_method(self):
        self._patcher_conditional_mapping_data_record.stop()
        self._patcher_conditional_control_state_2013.stop()
        self._patcher_conditional_control_state_2020.stop()
        self._patcher_conditional_control_enable_mask_2013.stop()
        self._patcher_conditional_control_enable_mask_2020.stop()

    # get_input_output_control_by_identifier_request_2013

    def test_get_input_output_control_by_identifier_request_2013(self):
        mock_did = Mock()
        assert (get_input_output_control_by_identifier_request_2013(mock_did)
                == (INPUT_OUTPUT_CONTROL_PARAMETER, self.mock_conditional_mapping_data_record.return_value))
        self.mock_conditional_control_state_2013.get_message_continuation.assert_called_once_with(mock_did)
        self.mock_conditional_control_enable_mask_2013.get_message_continuation.assert_called_once_with(mock_did)


    # get_input_output_control_by_identifier_request_2020

    def test_get_input_output_control_by_identifier_request_2020(self):
        mock_did = Mock()
        assert (get_input_output_control_by_identifier_request_2020(mock_did)
                == (INPUT_OUTPUT_CONTROL_PARAMETER, self.mock_conditional_mapping_data_record.return_value))
        self.mock_conditional_control_state_2020.get_message_continuation.assert_called_once_with(mock_did)
        self.mock_conditional_control_enable_mask_2020.get_message_continuation.assert_called_once_with(mock_did)


    # get_input_output_control_by_identifier_response_2013

    def test_get_input_output_control_by_identifier_response_2013(self):
        mock_did = Mock()
        assert (get_input_output_control_by_identifier_response_2013(mock_did)
                == (INPUT_OUTPUT_CONTROL_PARAMETER, self.mock_conditional_mapping_data_record.return_value))
        self.mock_conditional_control_state_2013.get_message_continuation.assert_called_once_with(mock_did)


    # get_input_output_control_by_identifier_response_2020

    def test_get_input_output_control_by_identifier_response_2020(self):
        mock_did = Mock()
        assert (get_input_output_control_by_identifier_response_2020(mock_did)
                == (INPUT_OUTPUT_CONTROL_PARAMETER, self.mock_conditional_mapping_data_record.return_value))
        self.mock_conditional_control_state_2020.get_message_continuation.assert_called_once_with(mock_did)

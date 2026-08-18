import pytest
from mock import MagicMock, Mock, call, patch

from uds.translator import (
    AUTHENTICATION,
    BASE_TRANSLATOR,
    CLEAR_DIAGNOSTIC_INFORMATION,
    COMMUNICATION_CONTROL,
    CONTROL_DTC_SETTING,
    DIAGNOSTIC_SESSION_CONTROL,
    DYNAMICALLY_DEFINE_DATA_IDENTIFIER,
    ECU_RESET,
    INPUT_OUTPUT_CONTROL_BY_IDENTIFIER,
    LINK_CONTROL,
    READ_DATA_BY_IDENTIFIER,
    READ_DATA_BY_PERIODIC_IDENTIFIER,
    READ_DTC_INFORMATION,
    READ_MEMORY_BY_ADDRESS,
    READ_SCALING_DATA_BY_IDENTIFIER,
    REQUEST_DOWNLOAD,
    REQUEST_FILE_TRANSFER,
    REQUEST_TRANSFER_EXIT,
    REQUEST_UPLOAD,
    RESPONSE_ON_EVENT,
    ROUTINE_CONTROL,
    SECURED_DATA_TRANSMISSION,
    SECURITY_ACCESS,
    TESTER_PRESENT,
    TRANSFER_DATA,
    WRITE_DATA_BY_IDENTIFIER,
    WRITE_MEMORY_BY_ADDRESS,
    RawDataRecord,
)
from uds.translator.configurable_translator import (
    DID_BIT_LENGTH,
    DID_COUNT_RECORDS,
    DTC_AND_STATUS,
    DTC_STORED_DATA_RECORD_NUMBERS_LIST,
    DTCS_AND_STATUSES_LIST,
    INPUT_OUTPUT_CONTROL_PARAMETER,
    MEMORY_SELECTION,
    NUMBER_OF_ACTIVATED_EVENTS,
    OPTIONAL_DTC_SNAPSHOT_RECORDS_NUMBERS_LIST,
    REPEATED_DATA_RECORDS_NUMBER,
    RESERVED_BIT,
    AbstractDataRecord,
    ConfigurableTranslator,
    RequestSID,
    Translator,
)
from uds.translator.data_record_definitions import ACTIVE_DIAGNOSTIC_SESSION
from uds.translator.service_definitions import ACCESS_TIMING_PARAMETER_2013
from uds.utilities.constants import (
    AUTHENTICATION_TASK_MAPPING,
    CONTROL_TYPE_MAPPING,
    DEFINITION_TYPE_MAPPING,
    DIAGNOSTIC_SESSION_TYPE_MAPPING,
    DID_MAPPING_2020,
    DTC_SETTING_TYPE_MAPPING,
    EVENT_MAPPING_2020,
    LINK_CONTROL_TYPE_MAPPING,
    REPORT_TYPE_MAPPING_2020,
    RESET_TYPE_MAPPING,
    ROUTINE_CONTROL_TYPE_MAPPING,
    SECURITY_ACCESS_TYPE_MAPPING,
    ZERO_SUBFUNCTION_MAPPING,
)

SCRIPT_LOCATION = "uds.translator.configurable_translator"


class TestConfigurableTranslator:
    """Unit tests for `ConfigurableTranslator` class."""

    def setup_method(self):
        self.mock_translator = MagicMock(spec=ConfigurableTranslator,
                                         __class__=ConfigurableTranslator,
                                         services_mapping={sid: MagicMock() for sid in list(RequestSID)})
        # patching
        self._patcher_deepcopy = patch(f"{SCRIPT_LOCATION}.deepcopy")
        self.mock_deepcopy = self._patcher_deepcopy.start()
        self._patcher_mapping_proxy_type = patch(f"{SCRIPT_LOCATION}.MappingProxyType")
        self.mock_mapping_proxy_type = self._patcher_mapping_proxy_type.start()
        self._patcher_raw_data_record = patch(f"{SCRIPT_LOCATION}.RawDataRecord")
        self.mock_raw_data_record = self._patcher_raw_data_record.start()
        self._patcher_mapping_data_record = patch(f"{SCRIPT_LOCATION}.MappingDataRecord")
        self.mock_mapping_data_record = self._patcher_mapping_data_record.start()
        self._patcher_conditional_formula_data_record = patch(f"{SCRIPT_LOCATION}.ConditionalFormulaDataRecord")
        self.mock_conditional_formula_data_record = self._patcher_conditional_formula_data_record.start()
        self._patcher_conditional_mapping_data_record = patch(f"{SCRIPT_LOCATION}.ConditionalMappingDataRecord")
        self.mock_conditional_mapping_data_record = self._patcher_conditional_mapping_data_record.start()

    def teardown_method(self):
        self._patcher_deepcopy.stop()
        self._patcher_mapping_proxy_type.stop()
        self._patcher_raw_data_record.stop()
        self._patcher_mapping_data_record.stop()
        self._patcher_conditional_formula_data_record.stop()
        self._patcher_conditional_mapping_data_record.stop()

    # __init__

    @pytest.mark.parametrize("services", [
        [Mock()],
        [Mock(), Mock()],
    ])
    @patch(f"{SCRIPT_LOCATION}.Translator.__init__")
    def test_init__mandatory_args(self, mock_translator_init, services):
        mock_base = Mock(spec=Translator, services=services)
        assert ConfigurableTranslator.__init__(self.mock_translator, mock_base) is None
        assert self.mock_translator._ConfigurableTranslator__did_data_mapping is None
        self.mock_deepcopy.assert_called_once_with(mock_base.services)
        mock_translator_init.assert_called_once_with(services=self.mock_deepcopy.return_value)

    @pytest.mark.parametrize("services, diagnostic_session_type_mapping, reset_type_mapping, report_type_mapping,"
                             "security_access_type_mapping, control_type_type_mapping, authentication_task_mapping,"
                             "definition_type_mapping, routine_control_type_mapping, zero_subfunction_mapping,"
                             "timing_parameter_access_type_mapping, dtc_setting_type_mapping, event_type_mapping,"
                             "link_control_type_mapping, rid_mapping, did_mapping, did_data_mapping", [
        (
            [Mock(request_sid=sid) for sid in list(RequestSID)],
            Mock(),
            Mock(),
            Mock(),
            Mock(),
            Mock(),
            Mock(),
            Mock(),
            Mock(),
            Mock(),
            Mock(),
            Mock(),
            Mock(),
            Mock(),
            Mock(),
            Mock(),
            Mock(),
        )
    ])
    @patch(f"{SCRIPT_LOCATION}.Translator.__init__")
    def test_init__all_args(self,
                            mock_translator_init,
                            services,
                            diagnostic_session_type_mapping, reset_type_mapping, report_type_mapping,
                            security_access_type_mapping, control_type_type_mapping,
                            authentication_task_mapping, definition_type_mapping,
                            routine_control_type_mapping, zero_subfunction_mapping,
                            timing_parameter_access_type_mapping, dtc_setting_type_mapping,
                            event_type_mapping, link_control_type_mapping,
                            rid_mapping, did_mapping, did_data_mapping):
        mock_base = Mock(spec=Translator, services=services)
        assert ConfigurableTranslator.__init__(self.mock_translator,
                                               base=mock_base,
                                               diagnostic_session_type_mapping=diagnostic_session_type_mapping,
                                               reset_type_mapping=reset_type_mapping,
                                               report_type_mapping=report_type_mapping,
                                               security_access_type_mapping=security_access_type_mapping,
                                               control_type_type_mapping=control_type_type_mapping,
                                               authentication_task_mapping=authentication_task_mapping,
                                               definition_type_mapping=definition_type_mapping,
                                               routine_control_type_mapping=routine_control_type_mapping,
                                               zero_subfunction_mapping=zero_subfunction_mapping,
                                               timing_parameter_access_type_mapping=timing_parameter_access_type_mapping,
                                               dtc_setting_type_mapping=dtc_setting_type_mapping,
                                               event_type_mapping=event_type_mapping,
                                               link_control_type_mapping=link_control_type_mapping,
                                               rid_mapping=rid_mapping,
                                               did_mapping=did_mapping,
                                               did_data_mapping=did_data_mapping) is None
        assert self.mock_translator._ConfigurableTranslator__did_data_mapping is None
        assert self.mock_translator.rid_mapping == rid_mapping
        assert self.mock_translator.did_mapping == did_mapping
        assert self.mock_translator.did_data_mapping == did_data_mapping
        assert self.mock_translator.diagnostic_session_type_mapping == diagnostic_session_type_mapping
        assert self.mock_translator.reset_type_mapping == reset_type_mapping
        assert self.mock_translator.report_type_mapping == report_type_mapping
        assert self.mock_translator.security_access_type_mapping == security_access_type_mapping
        assert self.mock_translator.control_type_type_mapping == control_type_type_mapping
        assert self.mock_translator.authentication_task_mapping == authentication_task_mapping
        assert self.mock_translator.routine_control_type_mapping == routine_control_type_mapping
        assert self.mock_translator.definition_type_mapping == definition_type_mapping
        assert self.mock_translator.zero_subfunction_mapping == zero_subfunction_mapping
        assert self.mock_translator.timing_parameter_access_type_mapping == timing_parameter_access_type_mapping
        assert self.mock_translator.dtc_setting_type_mapping == dtc_setting_type_mapping
        assert self.mock_translator.event_type_mapping == event_type_mapping
        assert self.mock_translator.link_control_type_mapping == link_control_type_mapping
        self.mock_deepcopy.assert_called_once_with(mock_base.services)
        mock_translator_init.assert_called_once_with(services=self.mock_deepcopy.return_value)

    # __deepcopy__

    @patch(f"{SCRIPT_LOCATION}.ConfigurableTranslator.__init__")
    def test_deepcopy(self, mock_init):
        memo = {}
        translator_copy = ConfigurableTranslator.__deepcopy__(self.mock_translator, memo)
        assert memo[id(self.mock_translator)] is translator_copy
        mock_init.assert_called_once_with(
            translator_copy,
            base=self.mock_translator,
            diagnostic_session_type_mapping=self.mock_translator.diagnostic_session_type_mapping,
            reset_type_mapping=self.mock_translator.reset_type_mapping,
            report_type_mapping=self.mock_translator.report_type_mapping,
            security_access_type_mapping=self.mock_translator.security_access_type_mapping,
            control_type_type_mapping=self.mock_translator.control_type_type_mapping,
            authentication_task_mapping=self.mock_translator.authentication_task_mapping,
            definition_type_mapping=self.mock_translator.definition_type_mapping,
            routine_control_type_mapping=self.mock_translator.routine_control_type_mapping,
            zero_subfunction_mapping=self.mock_translator.zero_subfunction_mapping,
            timing_parameter_access_type_mapping=self.mock_translator.timing_parameter_access_type_mapping,
            dtc_setting_type_mapping=self.mock_translator.dtc_setting_type_mapping,
            event_type_mapping=self.mock_translator.event_type_mapping,
            link_control_type_mapping=self.mock_translator.link_control_type_mapping,
            rid_mapping=self.mock_translator.rid_mapping,
            did_mapping=self.mock_translator.did_mapping,
            did_data_mapping=self.mock_deepcopy.return_value)
        self.mock_deepcopy.assert_called_once_with(self.mock_translator.did_data_mapping, memo=memo)

    # diagnostic_session_type_mapping

    def test_diagnostic_session_type_mapping_mapping__get(self):
        assert (ConfigurableTranslator.diagnostic_session_type_mapping.fget(self.mock_translator)
                == self.mock_translator.services_mapping[RequestSID.DiagnosticSessionControl].request_structure[0].children[1].values_mapping)

    def test_diagnostic_session_type_mapping_mapping__get__none(self):
        mock_get = Mock(return_value=None)
        self.mock_translator.services_mapping = MagicMock(get=mock_get)
        assert ConfigurableTranslator.diagnostic_session_type_mapping.fget(self.mock_translator) is None
        mock_get.assert_called_once_with(RequestSID.DiagnosticSessionControl, None)

    def test_diagnostic_session_type_mapping_mapping__set(self):
        mock_value = {Mock(): Mock()}
        assert ConfigurableTranslator.diagnostic_session_type_mapping.fset(self.mock_translator, mock_value) is None
        assert (self.mock_translator.services_mapping[RequestSID.DiagnosticSessionControl].request_structure[0].children[1].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.DiagnosticSessionControl].response_structure[0].children[1].values_mapping
                == mock_value)

    # reset_type_mapping

    def test_reset_type_mapping_mapping__get(self):
        assert (ConfigurableTranslator.reset_type_mapping.fget(self.mock_translator)
                == self.mock_translator.services_mapping[RequestSID.ECUReset].request_structure[0].children[1].values_mapping)

    def test_reset_type_mapping_mapping__get__none(self):
        mock_get = Mock(return_value=None)
        self.mock_translator.services_mapping = MagicMock(get=mock_get)
        assert ConfigurableTranslator.reset_type_mapping.fget(self.mock_translator) is None
        mock_get.assert_called_once_with(RequestSID.ECUReset, None)

    def test_reset_type_mapping_mapping__set(self):
        mock_value = {Mock(): Mock()}
        assert ConfigurableTranslator.reset_type_mapping.fset(self.mock_translator, mock_value) is None
        assert (self.mock_translator.services_mapping[RequestSID.ECUReset].request_structure[0].children[1].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.ECUReset].response_structure[0].children[1].values_mapping
                == mock_value)

    # report_type_mapping

    def test_report_type_mapping_mapping__get(self):
        assert (ConfigurableTranslator.report_type_mapping.fget(self.mock_translator)
                == self.mock_translator.services_mapping[RequestSID.ReadDTCInformation].request_structure[0].children[1].values_mapping)

    def test_report_type_mapping_mapping__get__none(self):
        mock_get = Mock(return_value=None)
        self.mock_translator.services_mapping = MagicMock(get=mock_get)
        assert ConfigurableTranslator.report_type_mapping.fget(self.mock_translator) is None
        mock_get.assert_called_once_with(RequestSID.ReadDTCInformation, None)

    def test_report_type_mapping_mapping__set__read_dtc_information_only(self):
        mock_value = {Mock(): Mock()}
        self.mock_translator.services_mapping.pop(RequestSID.ResponseOnEvent)
        assert ConfigurableTranslator.report_type_mapping.fset(self.mock_translator, mock_value) is None
        assert (self.mock_translator.services_mapping[RequestSID.ReadDTCInformation].request_structure[0].children[1].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.ReadDTCInformation].response_structure[0].children[1].values_mapping
                == mock_value)

    def test_report_type_mapping_mapping__set__response_on_event_not_updated(self):
        mock_value = {Mock(): Mock()}
        mock_get_request_continuation = Mock(return_value=None)
        mock_get_response_continuation = Mock(return_value=None)
        self.mock_translator.services_mapping[RequestSID.ResponseOnEvent] = Mock(
            request_structure=(Mock(), Mock(mapping=Mock(get=mock_get_request_continuation))),
            response_structure=(Mock(), Mock(mapping=Mock(get=mock_get_response_continuation))),
        )
        assert ConfigurableTranslator.report_type_mapping.fset(self.mock_translator, mock_value) is None
        assert (self.mock_translator.services_mapping[RequestSID.ReadDTCInformation].request_structure[0].children[1].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.ReadDTCInformation].response_structure[0].children[1].values_mapping
                == mock_value)
        mock_get_request_continuation.assert_has_calls([call(0x08, None), call(0x09, None)], any_order=True)
        mock_get_response_continuation.assert_has_calls([call(0x08, None), call(0x09, None)], any_order=True)

    def test_report_type_mapping_mapping__set__response_on_event_updated(self):
        mock_value = {Mock(): Mock()}
        mock_request_08_continuation = MagicMock()
        mock_request_09_continuation = MagicMock()
        mock_response_08_continuation = MagicMock()
        mock_response_09_continuation = MagicMock()
        self.mock_translator.services_mapping[RequestSID.ResponseOnEvent] = Mock(
            request_structure=(Mock(), Mock(mapping={0x08: mock_request_08_continuation,
                                                     0x09: mock_request_09_continuation})),
            response_structure=(Mock(), Mock(mapping={0x08: mock_response_08_continuation,
                                                      0x09: mock_response_09_continuation})),
        )
        assert ConfigurableTranslator.report_type_mapping.fset(self.mock_translator, mock_value) is None
        assert (self.mock_translator.services_mapping[RequestSID.ReadDTCInformation].request_structure[0].children[1].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.ReadDTCInformation].response_structure[0].children[1].values_mapping
                == mock_value)
        assert mock_request_08_continuation[1].children[1].values_mapping == mock_value
        assert mock_request_09_continuation[1].children[2].values_mapping == mock_value
        assert mock_response_08_continuation[2].children[1].values_mapping == mock_value
        assert mock_response_09_continuation[2].children[2].values_mapping == mock_value

    # security_access_type_mapping

    def test_security_access_type_mapping_mapping__get(self):
        assert (ConfigurableTranslator.security_access_type_mapping.fget(self.mock_translator)
                == self.mock_translator.services_mapping[RequestSID.SecurityAccess].request_structure[0].children[1].values_mapping)

    def test_security_access_type_mapping_mapping__get__none(self):
        mock_get = Mock(return_value=None)
        self.mock_translator.services_mapping = MagicMock(get=mock_get)
        assert ConfigurableTranslator.security_access_type_mapping.fget(self.mock_translator) is None
        mock_get.assert_called_once_with(RequestSID.SecurityAccess, None)

    def test_security_access_type_mapping_mapping__set(self):
        mock_value = {Mock(): Mock()}
        assert ConfigurableTranslator.security_access_type_mapping.fset(self.mock_translator, mock_value) is None
        assert (self.mock_translator.services_mapping[RequestSID.SecurityAccess].request_structure[0].children[1].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.SecurityAccess].response_structure[0].children[1].values_mapping
                == mock_value)
        
    # control_type_type_mapping

    def test_control_type_type_mapping_mapping__get(self):
        assert (ConfigurableTranslator.control_type_type_mapping.fget(self.mock_translator)
                == self.mock_translator.services_mapping[RequestSID.CommunicationControl].request_structure[0].children[1].values_mapping)

    def test_control_type_type_mapping_mapping__get__none(self):
        mock_get = Mock(return_value=None)
        self.mock_translator.services_mapping = MagicMock(get=mock_get)
        assert ConfigurableTranslator.control_type_type_mapping.fget(self.mock_translator) is None
        mock_get.assert_called_once_with(RequestSID.CommunicationControl, None)

    def test_control_type_type_mapping_mapping__set(self):
        mock_value = {Mock(): Mock()}
        assert ConfigurableTranslator.control_type_type_mapping.fset(self.mock_translator, mock_value) is None
        assert (self.mock_translator.services_mapping[RequestSID.CommunicationControl].request_structure[0].children[1].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.CommunicationControl].response_structure[0].children[1].values_mapping
                == mock_value)
        
    # authentication_task_mapping

    def test_authentication_task_mapping_mapping__get(self):
        assert (ConfigurableTranslator.authentication_task_mapping.fget(self.mock_translator)
                == self.mock_translator.services_mapping[RequestSID.Authentication].request_structure[0].children[1].values_mapping)

    def test_authentication_task_mapping_mapping__get__none(self):
        mock_get = Mock(return_value=None)
        self.mock_translator.services_mapping = MagicMock(get=mock_get)
        assert ConfigurableTranslator.authentication_task_mapping.fget(self.mock_translator) is None
        mock_get.assert_called_once_with(RequestSID.Authentication, None)

    def test_authentication_task_mapping_mapping__set(self):
        mock_value = {Mock(): Mock()}
        assert ConfigurableTranslator.authentication_task_mapping.fset(self.mock_translator, mock_value) is None
        assert (self.mock_translator.services_mapping[RequestSID.Authentication].request_structure[0].children[1].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.Authentication].response_structure[0].children[1].values_mapping
                == mock_value)
        
    # definition_type_mapping

    def test_definition_type_mapping_mapping__get(self):
        assert (ConfigurableTranslator.definition_type_mapping.fget(self.mock_translator)
                == self.mock_translator.services_mapping[RequestSID.DynamicallyDefineDataIdentifier].request_structure[0].children[1].values_mapping)

    def test_definition_type_mapping_mapping__get__none(self):
        mock_get = Mock(return_value=None)
        self.mock_translator.services_mapping = MagicMock(get=mock_get)
        assert ConfigurableTranslator.definition_type_mapping.fget(self.mock_translator) is None
        mock_get.assert_called_once_with(RequestSID.DynamicallyDefineDataIdentifier, None)

    def test_definition_type_mapping_mapping__set(self):
        mock_value = {Mock(): Mock()}
        assert ConfigurableTranslator.definition_type_mapping.fset(self.mock_translator, mock_value) is None
        assert (self.mock_translator.services_mapping[RequestSID.DynamicallyDefineDataIdentifier].request_structure[0].children[1].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.DynamicallyDefineDataIdentifier].response_structure[0].children[1].values_mapping
                == mock_value)
        
    # routine_control_type_mapping

    def test_routine_control_type_mapping_mapping__get(self):
        assert (ConfigurableTranslator.routine_control_type_mapping.fget(self.mock_translator)
                == self.mock_translator.services_mapping[RequestSID.RoutineControl].request_structure[0].children[1].values_mapping)

    def test_routine_control_type_mapping_mapping__get__none(self):
        mock_get = Mock(return_value=None)
        self.mock_translator.services_mapping = MagicMock(get=mock_get)
        assert ConfigurableTranslator.routine_control_type_mapping.fget(self.mock_translator) is None
        mock_get.assert_called_once_with(RequestSID.RoutineControl, None)

    def test_routine_control_type_mapping_mapping__set(self):
        mock_value = {Mock(): Mock()}
        assert ConfigurableTranslator.routine_control_type_mapping.fset(self.mock_translator, mock_value) is None
        assert (self.mock_translator.services_mapping[RequestSID.RoutineControl].request_structure[0].children[1].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.RoutineControl].response_structure[0].children[1].values_mapping
                == mock_value)
        
    # zero_subfunction_mapping

    def test_zero_subfunction_mapping_mapping__get(self):
        assert (ConfigurableTranslator.zero_subfunction_mapping.fget(self.mock_translator)
                == self.mock_translator.services_mapping[RequestSID.TesterPresent].request_structure[0].children[1].values_mapping)

    def test_zero_subfunction_mapping_mapping__get__none(self):
        mock_get = Mock(return_value=None)
        self.mock_translator.services_mapping = MagicMock(get=mock_get)
        assert ConfigurableTranslator.zero_subfunction_mapping.fget(self.mock_translator) is None
        mock_get.assert_called_once_with(RequestSID.TesterPresent, None)

    def test_zero_subfunction_mapping_mapping__set(self):
        mock_value = {Mock(): Mock()}
        assert ConfigurableTranslator.zero_subfunction_mapping.fset(self.mock_translator, mock_value) is None
        assert (self.mock_translator.services_mapping[RequestSID.TesterPresent].request_structure[0].children[1].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.TesterPresent].response_structure[0].children[1].values_mapping
                == mock_value)
        
    # timing_parameter_access_type_mapping

    def test_timing_parameter_access_type_mapping_mapping__get(self):
        assert (ConfigurableTranslator.timing_parameter_access_type_mapping.fget(self.mock_translator)
                == self.mock_translator.services_mapping[RequestSID.AccessTimingParameter].request_structure[0].children[1].values_mapping)

    def test_timing_parameter_access_type_mapping_mapping__get__none(self):
        mock_get = Mock(return_value=None)
        self.mock_translator.services_mapping = MagicMock(get=mock_get)
        assert ConfigurableTranslator.timing_parameter_access_type_mapping.fget(self.mock_translator) is None
        mock_get.assert_called_once_with(RequestSID.AccessTimingParameter, None)

    def test_timing_parameter_access_type_mapping_mapping__set(self):
        mock_value = {Mock(): Mock()}
        assert ConfigurableTranslator.timing_parameter_access_type_mapping.fset(self.mock_translator, mock_value) is None
        assert (self.mock_translator.services_mapping[RequestSID.AccessTimingParameter].request_structure[0].children[1].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.AccessTimingParameter].response_structure[0].children[1].values_mapping
                == mock_value)

    # dtc_setting_type_mapping

    def test_dtc_setting_type_mapping_mapping__get(self):
        assert (ConfigurableTranslator.dtc_setting_type_mapping.fget(self.mock_translator)
                == self.mock_translator.services_mapping[RequestSID.ControlDTCSetting].request_structure[0].children[1].values_mapping)

    def test_dtc_setting_type_mapping_mapping__get__none(self):
        mock_get = Mock(return_value=None)
        self.mock_translator.services_mapping = MagicMock(get=mock_get)
        assert ConfigurableTranslator.dtc_setting_type_mapping.fget(self.mock_translator) is None
        mock_get.assert_called_once_with(RequestSID.ControlDTCSetting, None)

    def test_dtc_setting_type_mapping_mapping__set(self):
        mock_value = {Mock(): Mock()}
        assert ConfigurableTranslator.dtc_setting_type_mapping.fset(self.mock_translator,
                                                                                mock_value) is None
        assert (self.mock_translator.services_mapping[RequestSID.ControlDTCSetting].request_structure[0].children[1].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.ControlDTCSetting].response_structure[0].children[1].values_mapping
                == mock_value)
        
    # event_type_mapping

    def test_event_type_mapping_mapping__get(self):
        assert (ConfigurableTranslator.event_type_mapping.fget(self.mock_translator)
                == self.mock_translator.services_mapping[RequestSID.ResponseOnEvent].request_structure[0].children[1].children[1].values_mapping)

    def test_event_type_mapping_mapping__get__none(self):
        mock_get = Mock(return_value=None)
        self.mock_translator.services_mapping = MagicMock(get=mock_get)
        assert ConfigurableTranslator.event_type_mapping.fget(self.mock_translator) is None
        mock_get.assert_called_once_with(RequestSID.ResponseOnEvent, None)

    def test_event_type_mapping_mapping__set(self):
        mock_value = {Mock(): Mock()}
        assert ConfigurableTranslator.event_type_mapping.fset(self.mock_translator,
                                                                                mock_value) is None
        assert (self.mock_translator.services_mapping[RequestSID.ResponseOnEvent].request_structure[0].children[1].children[1].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.ResponseOnEvent].response_structure[0].children[1].children[1].values_mapping
                == mock_value)
        
    # link_control_type_mapping

    def test_link_control_type_mapping_mapping__get(self):
        assert (ConfigurableTranslator.link_control_type_mapping.fget(self.mock_translator)
                == self.mock_translator.services_mapping[RequestSID.LinkControl].request_structure[0].children[1].values_mapping)

    def test_link_control_type_mapping_mapping__get__none(self):
        mock_get = Mock(return_value=None)
        self.mock_translator.services_mapping = MagicMock(get=mock_get)
        assert ConfigurableTranslator.link_control_type_mapping.fget(self.mock_translator) is None
        mock_get.assert_called_once_with(RequestSID.LinkControl, None)

    def test_link_control_type_mapping_mapping__set(self):
        mock_value = {Mock(): Mock()}
        assert ConfigurableTranslator.link_control_type_mapping.fset(self.mock_translator,
                                                                                mock_value) is None
        assert (self.mock_translator.services_mapping[RequestSID.LinkControl].request_structure[0].children[1].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.LinkControl].response_structure[0].children[1].values_mapping
                == mock_value)

    # rid_mapping

    def test_rid_mapping__get(self):
        assert (ConfigurableTranslator.rid_mapping.fget(self.mock_translator)
                == self.mock_translator.services_mapping[RequestSID.RoutineControl].request_structure[1].values_mapping)

    def test_rid_mapping__get__none(self):
        mock_get = Mock(return_value=None)
        self.mock_translator.services_mapping = MagicMock(get=mock_get)
        assert ConfigurableTranslator.rid_mapping.fget(self.mock_translator) is None
        mock_get.assert_called_once_with(RequestSID.RoutineControl, None)

    def test_rid_mapping__set(self):
        mock_value = {Mock(): Mock()}
        assert ConfigurableTranslator.rid_mapping.fset(self.mock_translator, mock_value) is None
        assert (self.mock_translator.services_mapping[RequestSID.RoutineControl].request_structure[1].values_mapping
                == mock_value)

    # did_mapping

    def test_did_mapping__get(self):
        assert (ConfigurableTranslator.did_mapping.fget(self.mock_translator)
                == self.mock_translator.services_mapping[RequestSID.ReadDataByIdentifier].request_structure[0].values_mapping)

    def test_did_mapping__get__none(self):
        mock_get = Mock(return_value=None)
        self.mock_translator.services_mapping = MagicMock(get=mock_get)
        assert ConfigurableTranslator.did_mapping.fget(self.mock_translator) is None
        mock_get.assert_called_once_with(RequestSID.ReadDataByIdentifier, None)

    def test_did_mapping__set__rdbi_only(self):
        self.mock_translator.services_mapping = {
            RequestSID.ReadDataByIdentifier: MagicMock(response_structure = 10 * [Mock()]),
        }
        mock_value = {Mock(): Mock()}
        assert ConfigurableTranslator.did_mapping.fset(self.mock_translator, mock_value) is None
        assert (self.mock_translator.services_mapping[RequestSID.ReadDataByIdentifier].request_structure[0].values_mapping
                == mock_value)
        assert all(did.values_mapping == mock_value
                   for did in self.mock_translator.services_mapping[RequestSID.ReadDataByIdentifier].response_structure[::2])

    def test_did_mapping__set__all(self):
        self.mock_translator.services_mapping = {
            RequestSID.ReadDataByIdentifier: MagicMock(response_structure=100 * [Mock()]),
            RequestSID.WriteDataByIdentifier: MagicMock(),
            RequestSID.ReadScalingDataByIdentifier: MagicMock(),
            RequestSID.DynamicallyDefineDataIdentifier: MagicMock(),
            RequestSID.InputOutputControlByIdentifier: MagicMock(),
            RequestSID.ReadDTCInformation: MagicMock(response_structure=[Mock(), Mock(mapping={})]),
            RequestSID.ResponseOnEvent: MagicMock(
                request_structure=[MagicMock(), MagicMock(mapping={i: 10*[MagicMock()] for i in range(10)})],
                response_structure=[MagicMock(), MagicMock(mapping={i: 10*[MagicMock()] for i in range(10)})]),
        }
        self.mock_translator._ConfigurableTranslator__conditional_read_dtc_information_response = Mock()
        self.mock_translator._ConfigurableTranslator__conditional_response_on_event_response = Mock()
        mock_value = {Mock(): Mock()}
        assert ConfigurableTranslator.did_mapping.fset(self.mock_translator, mock_value) is None
        # ReadDataByIdentifier
        assert (self.mock_translator.services_mapping[RequestSID.ReadDataByIdentifier].request_structure[0].values_mapping
                == mock_value)
        assert all(did.values_mapping == mock_value
                   for did in self.mock_translator.services_mapping[RequestSID.ReadDataByIdentifier].response_structure[::2])
        # WriteDataByIdentifier
        assert (self.mock_translator.services_mapping[RequestSID.WriteDataByIdentifier].request_structure[0].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.WriteDataByIdentifier].response_structure[0].values_mapping
                == mock_value)
        # ReadScalingDataByIdentifier
        assert (self.mock_translator.services_mapping[RequestSID.ReadScalingDataByIdentifier].request_structure[0].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.ReadScalingDataByIdentifier].response_structure[0].values_mapping
                == mock_value)
        # DynamicallyDefineDataIdentifier
        assert (self.mock_translator.services_mapping[RequestSID.DynamicallyDefineDataIdentifier].request_structure[1].mapping[0x01][0].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.DynamicallyDefineDataIdentifier].request_structure[1].mapping[0x01][1].children[0].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.DynamicallyDefineDataIdentifier].request_structure[1].mapping[0x02][0].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.DynamicallyDefineDataIdentifier].request_structure[1].mapping[0x03][0].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.DynamicallyDefineDataIdentifier].response_structure[1].mapping[0x01][0].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.DynamicallyDefineDataIdentifier].response_structure[1].mapping[0x02][0].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.DynamicallyDefineDataIdentifier].response_structure[1].mapping[0x03][0].values_mapping
                == mock_value)
        # InputOutputControlByIdentifier
        assert (self.mock_translator.services_mapping[RequestSID.InputOutputControlByIdentifier].request_structure[0].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.InputOutputControlByIdentifier].response_structure[0].values_mapping
                == mock_value)
        # ReadDTCInformation
        assert (self.mock_translator.services_mapping[RequestSID.ReadDTCInformation].response_structure[1].mapping[0x04]
                == (DTC_AND_STATUS, *self.mock_translator._ConfigurableTranslator__dtc_snapshot_records))
        assert (self.mock_translator.services_mapping[RequestSID.ReadDTCInformation].response_structure[1].mapping[0x05]
                == self.mock_translator._ConfigurableTranslator__dtc_stored_data_records)
        assert (self.mock_translator.services_mapping[RequestSID.ReadDTCInformation].response_structure[1].mapping[0x18]
                == (MEMORY_SELECTION, DTC_AND_STATUS, *self.mock_translator._ConfigurableTranslator__dtc_snapshot_records))
        # ResponseOnEvent
        assert (self.mock_translator.services_mapping[RequestSID.ResponseOnEvent].request_structure[1].mapping[0x03][1].children[0].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.ResponseOnEvent].request_structure[1].mapping[0x07][1].children[0].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.ResponseOnEvent].response_structure[1].mapping[0x03][2].children[0].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.ResponseOnEvent].response_structure[1].mapping[0x04]
                == (NUMBER_OF_ACTIVATED_EVENTS,
                    self.mock_translator._ConfigurableTranslator__conditional_activated_events))
        assert (self.mock_translator.services_mapping[RequestSID.ResponseOnEvent].response_structure[1].mapping[0x07][2].children[0].values_mapping
                == mock_value)

    # did_data_mapping

    def test_did_data_mapping__get(self):
        self.mock_translator._ConfigurableTranslator__did_data_mapping = Mock()
        assert (ConfigurableTranslator.did_data_mapping.fget(self.mock_translator)
                == self.mock_translator._ConfigurableTranslator__did_data_mapping)

    def test_did_data_mapping__set__rdbi_only(self):
        self.mock_translator.services_mapping = {
            RequestSID.ReadDataByIdentifier: MagicMock(response_structure = 10 * [Mock()]),
        }
        mock_rdbi_response_structure = 52 * (Mock(),)
        self.mock_translator._ConfigurableTranslator__get_did_record.side_effect = [
            mock_rdbi_response_structure[:2],
            mock_rdbi_response_structure
        ]
        mock_value = {Mock(): Mock()}
        assert ConfigurableTranslator.did_data_mapping.fset(self.mock_translator, mock_value) is None
        assert self.mock_translator._ConfigurableTranslator__did_data_mapping == self.mock_mapping_proxy_type.return_value
        assert (self.mock_translator.services_mapping[RequestSID.ReadDataByIdentifier].response_structure
                == mock_rdbi_response_structure)
        self.mock_translator._ConfigurableTranslator__get_did_record.assert_has_calls(
            [call(did_count=1, record_number=None, optional=False),
             call(did_count=REPEATED_DATA_RECORDS_NUMBER, record_number=None, optional=True)])
        self.mock_mapping_proxy_type.assert_called_once_with(mock_value)

    def test_did_data_mapping__set__all(self):
        self.mock_translator.services_mapping = {
            RequestSID.ReadDataByIdentifier: MagicMock(),
            RequestSID.WriteDataByIdentifier: MagicMock(),
            RequestSID.InputOutputControlByIdentifier: MagicMock(),
            RequestSID.ReadDTCInformation: MagicMock(response_structure=[Mock(), Mock(mapping={})]),
        }
        mock_rdbi_response_structure = 52 * (Mock(),)
        self.mock_translator._ConfigurableTranslator__get_did_record.side_effect = [
            mock_rdbi_response_structure[:2],
            mock_rdbi_response_structure
        ]
        mock_value = {Mock(): Mock()}
        assert ConfigurableTranslator.did_data_mapping.fset(self.mock_translator, mock_value) is None
        assert self.mock_translator._ConfigurableTranslator__did_data_mapping == self.mock_mapping_proxy_type.return_value
        self.mock_mapping_proxy_type.assert_called_once_with(mock_value)
        # ReadDataByIdentifier
        assert (self.mock_translator.services_mapping[RequestSID.ReadDataByIdentifier].response_structure
                == mock_rdbi_response_structure)
        self.mock_translator._ConfigurableTranslator__get_did_record.assert_has_calls(
            [call(did_count=1, record_number=None, optional=False),
             call(did_count=REPEATED_DATA_RECORDS_NUMBER, record_number=None, optional=True)])
        # WriteDataByIdentifier
        assert self.mock_translator.services_mapping[RequestSID.WriteDataByIdentifier].request_structure == (
            self.mock_translator.services_mapping[RequestSID.WriteDataByIdentifier].request_structure[0],
            self.mock_translator._ConfigurableTranslator__get_did_data.return_value
        )
        self.mock_translator._ConfigurableTranslator__get_did_data.assert_called_once_with()
        # InputOutputControlByIdentifier
        assert (self.mock_translator.services_mapping[RequestSID.InputOutputControlByIdentifier].request_structure[1].formula
                == self.mock_translator._ConfigurableTranslator__get_input_output_control_by_identifier_request)
        assert (self.mock_translator.services_mapping[RequestSID.InputOutputControlByIdentifier].response_structure[1].formula
                == self.mock_translator._ConfigurableTranslator__get_input_output_control_by_identifier_response)
        # ReadDTCInformation
        assert (self.mock_translator.services_mapping[RequestSID.ReadDTCInformation].response_structure[1].mapping[0x04]
                == (DTC_AND_STATUS, *self.mock_translator._ConfigurableTranslator__dtc_snapshot_records))
        assert (self.mock_translator.services_mapping[RequestSID.ReadDTCInformation].response_structure[1].mapping[0x05]
                == self.mock_translator._ConfigurableTranslator__dtc_stored_data_records)
        assert (self.mock_translator.services_mapping[RequestSID.ReadDTCInformation].response_structure[1].mapping[0x18]
                == (MEMORY_SELECTION, DTC_AND_STATUS, *self.mock_translator._ConfigurableTranslator__dtc_snapshot_records))

    # __did_records

    def test_did_records__get(self):
        assert (ConfigurableTranslator._ConfigurableTranslator__did_records.fget(self.mock_translator)
                == REPEATED_DATA_RECORDS_NUMBER * (self.mock_conditional_formula_data_record.return_value, ))
        self.mock_conditional_formula_data_record.assert_called_with(
            formula=self.mock_translator._ConfigurableTranslator__get_did_records_formula.return_value)
        self.mock_translator._ConfigurableTranslator__get_did_records_formula.assert_has_calls(
            [call(record_number+1) for record_number in range(REPEATED_DATA_RECORDS_NUMBER)],
            any_order=False)

    # __dtc_snapshot_records

    def test_dtc_snapshot_records__get(self):
        self.mock_translator._ConfigurableTranslator__did_records = [Mock()] * REPEATED_DATA_RECORDS_NUMBER
        dtc_snapshot_records = ConfigurableTranslator._ConfigurableTranslator__dtc_snapshot_records.fget(self.mock_translator)
        assert isinstance(dtc_snapshot_records, tuple)
        assert all(item == OPTIONAL_DTC_SNAPSHOT_RECORDS_NUMBERS_LIST[i]
                   for i, item in enumerate(dtc_snapshot_records[::3]))
        assert all(item == DID_COUNT_RECORDS[i]
                   for i, item in enumerate(dtc_snapshot_records[1::3]))
        assert all(item == self.mock_translator._ConfigurableTranslator__did_records[i]
                   for i, item in enumerate(dtc_snapshot_records[2::3]))
        
    # __dtc_stored_data_records

    def test_dtc_stored_data_records__get(self):
        self.mock_translator._ConfigurableTranslator__did_records = [Mock()] * REPEATED_DATA_RECORDS_NUMBER
        dtc_stored_data_records = ConfigurableTranslator._ConfigurableTranslator__dtc_stored_data_records.fget(self.mock_translator)
        assert isinstance(dtc_stored_data_records, tuple)
        assert all(item == DTC_STORED_DATA_RECORD_NUMBERS_LIST[i]
                   for i, item in enumerate(dtc_stored_data_records[::4]))
        assert all(item == DTCS_AND_STATUSES_LIST[i]
                   for i, item in enumerate(dtc_stored_data_records[1::4]))
        assert all(item == DID_COUNT_RECORDS[i]
                   for i, item in enumerate(dtc_stored_data_records[2::4]))
        assert all(item == self.mock_translator._ConfigurableTranslator__did_records[i]
                   for i, item in enumerate(dtc_stored_data_records[3::4]))

    # __event_window_time

    def test_event_window_time__get__value_error(self):
        mock_get = Mock(return_value=None)
        self.mock_translator.services_mapping = Mock(get=mock_get)
        with pytest.raises(ValueError):
            ConfigurableTranslator._ConfigurableTranslator__event_window_time.fget(self.mock_translator)
        mock_get.assert_called_once_with(RequestSID.ResponseOnEvent, None)

    def test_event_window_time__get(self):
        mock_service = MagicMock()
        mock_get = Mock(return_value=mock_service)
        self.mock_translator.services_mapping = Mock(get=mock_get)
        assert (ConfigurableTranslator._ConfigurableTranslator__event_window_time.fget(self.mock_translator)
                == mock_service.request_structure[1][0x00][0])

    # __event_type

    def test_event_type__get__value_error(self):
        mock_get = Mock(return_value=None)
        self.mock_translator.services_mapping = Mock(get=mock_get)
        with pytest.raises(ValueError):
            ConfigurableTranslator._ConfigurableTranslator__event_type.fget(self.mock_translator)
        mock_get.assert_called_once_with(RequestSID.ResponseOnEvent, None)

    def test_event_type__get(self):
        mock_service = MagicMock()
        mock_get = Mock(return_value=mock_service)
        self.mock_translator.services_mapping = Mock(get=mock_get)
        assert (ConfigurableTranslator._ConfigurableTranslator__event_type.fget(self.mock_translator)
                == mock_service.request_structure[0].children[1])

    # __conditional_control_state

    def test_conditional_control_state__get(self):
        assert (ConfigurableTranslator._ConfigurableTranslator__conditional_control_state.fget(self.mock_translator)
                == self.mock_translator._ConfigurableTranslator__get_did_data.return_value)
        self.mock_translator._ConfigurableTranslator__get_did_data.assert_called_once_with(name="controlState")

    # __conditional_optional_control_enable_mask

    def test_conditional_optional_control_enable_mask__get(self):
        assert (ConfigurableTranslator._ConfigurableTranslator__conditional_optional_control_enable_mask.fget(
            self.mock_translator) == self.mock_translator._ConfigurableTranslator__get_did_data_mask.return_value)
        self.mock_translator._ConfigurableTranslator__get_did_data_mask.assert_called_once_with(
            name="controlEnableMask", optional=True)

    # __conditional_activated_events

    def test_conditional_activated_events__get(self):
        assert (ConfigurableTranslator._ConfigurableTranslator__conditional_activated_events.fget(self.mock_translator)
                == self.mock_conditional_formula_data_record.return_value)
        self.mock_conditional_formula_data_record.assert_called_once_with(
            formula=self.mock_translator._ConfigurableTranslator__get_activated_events)

    # __get_did

    def test_get_did__value_error(self):
        self.mock_translator.did_mapping = None
        with pytest.raises(ValueError):
            ConfigurableTranslator._ConfigurableTranslator__get_did(self.mock_translator, Mock(), Mock())

    @pytest.mark.parametrize("name, optional", [
        ("SomeName", False),
        ("DID", True),
    ])
    def test_get_did__valid(self, name, optional):
        assert ConfigurableTranslator._ConfigurableTranslator__get_did(
            self.mock_translator, name=name,  optional=optional) == self.mock_mapping_data_record.return_value
        self.mock_mapping_data_record.assert_called_once_with(name=name,
                                                              length=DID_BIT_LENGTH,
                                                              values_mapping=self.mock_translator.did_mapping,
                                                              min_occurrences=0 if optional else 1,
                                                              max_occurrences=1)

    # __get_did_data

    def test_get_did_data(self):
        assert (ConfigurableTranslator._ConfigurableTranslator__get_did_data(self.mock_translator)
                == self.mock_conditional_formula_data_record.return_value)

    def test_get_did_data__formula(self):
        undefined_did = -1
        some_defined_did = 0x1234
        incorrect_did = 0x10000
        self.mock_translator.did_data_mapping = {some_defined_did: [Mock(spec=AbstractDataRecord,
                                                                         fixed_total_length=True,
                                                                         min_occurrences=1,
                                                                         max_occurrences=1,
                                                                         length=16)],
                                                 incorrect_did: [Mock(fixed_total_length=False)]}
        input_kwargs = {}
        self.mock_conditional_formula_data_record.side_effect = lambda **kwargs: input_kwargs.update(kwargs)
        ConfigurableTranslator._ConfigurableTranslator__get_did_data(self.mock_translator)
        with pytest.raises(ValueError):
            input_kwargs["formula"](undefined_did)
        with pytest.raises(ValueError):
            input_kwargs["formula"](incorrect_did)
        assert input_kwargs["formula"](some_defined_did) == (self.mock_raw_data_record.return_value,)

    # __get_did_data_mask

    @pytest.mark.parametrize("name, optional", [
        (Mock(), False),
        ("SomeName", True),
    ])
    def test_get_did_data_mask(self, name, optional):
        assert (ConfigurableTranslator._ConfigurableTranslator__get_did_data_mask(self.mock_translator,
                                                                                  name=name,
                                                                                  optional=optional)
                == self.mock_conditional_formula_data_record.return_value)

    @pytest.mark.parametrize("name, optional", [
        (Mock(), False),
        ("SomeName", True),
    ])
    def test_get_did_data_mask__formula(self, name, optional):
        undefined_did = -1
        some_defined_did = 0x1234
        incorrect_did = 0x10000
        self.mock_translator.did_data_mapping = {some_defined_did: [Mock(spec=AbstractDataRecord,
                                                                         fixed_total_length=True,
                                                                         min_occurrences=1,
                                                                         max_occurrences=1,
                                                                         length=16,
                                                                         children=[])],
                                                 incorrect_did: [Mock(fixed_total_length=False)]}
        input_kwargs = {}
        self.mock_conditional_formula_data_record.side_effect = lambda **kwargs: input_kwargs.update(kwargs)
        ConfigurableTranslator._ConfigurableTranslator__get_did_data_mask(self.mock_translator,
                                                                          name=name,
                                                                          optional=optional)
        with pytest.raises(ValueError):
            input_kwargs["formula"](undefined_did)
        with pytest.raises(ValueError):
            input_kwargs["formula"](incorrect_did)
        assert input_kwargs["formula"](some_defined_did) == (self.mock_raw_data_record.return_value,)

    # __get_did_records_formula

    def test_get_did_records_formula(self):
        mock_record_number = Mock()
        mock_did_count = Mock()
        formula = ConfigurableTranslator._ConfigurableTranslator__get_did_records_formula(self.mock_translator,
                                                                                          mock_record_number)
        assert callable(formula)
        assert formula(mock_did_count) == self.mock_translator._ConfigurableTranslator__get_did_record.return_value
        self.mock_translator._ConfigurableTranslator__get_did_record.assert_called_once_with(
            did_count=mock_did_count, record_number=mock_record_number)

    # __get_did_record

    @pytest.mark.parametrize("did_count, record_number", [
        (1, None),
        (7, 5),
    ])
    def test_get_did_record(self, did_count, record_number):
        assert (ConfigurableTranslator._ConfigurableTranslator__get_did_record(self.mock_translator,
                                                                               did_count=did_count,
                                                                               record_number=record_number)
                == (self.mock_translator._ConfigurableTranslator__get_did.return_value,
                    self.mock_translator._ConfigurableTranslator__get_did_data.return_value, ) * did_count)

    # __get_input_output_control_by_identifier_request

    def test_get_input_output_control_by_identifier_request(self):
        mock_did = Mock()
        assert (ConfigurableTranslator._ConfigurableTranslator__get_input_output_control_by_identifier_request(
            self.mock_translator, mock_did) == (INPUT_OUTPUT_CONTROL_PARAMETER,
                                                self.mock_conditional_mapping_data_record.return_value))
        self.mock_translator._ConfigurableTranslator__conditional_control_state.get_message_continuation.assert_called_once_with(mock_did)
        self.mock_translator._ConfigurableTranslator__conditional_optional_control_enable_mask.get_message_continuation.assert_called_once_with(mock_did)

    # __get_input_output_control_by_identifier_response

    def test_get_input_output_control_by_identifier_response(self):
        mock_did = Mock()
        assert (ConfigurableTranslator._ConfigurableTranslator__get_input_output_control_by_identifier_response(
            self.mock_translator, mock_did) == (INPUT_OUTPUT_CONTROL_PARAMETER,
                                                self.mock_conditional_mapping_data_record.return_value))
        self.mock_translator._ConfigurableTranslator__conditional_control_state.get_message_continuation.assert_called_once_with(mock_did)

    # __get_event_window_time

    @pytest.mark.parametrize("event_number", [1, 32])
    def test_get_event_window_time(self, event_number):
        assert (ConfigurableTranslator._ConfigurableTranslator__get_event_window_time(
            self.mock_translator, event_number) == self.mock_deepcopy.return_value)
        assert self.mock_deepcopy.return_value.name.endswith(f"#{event_number}")
        self.mock_deepcopy.assert_called_once_with(self.mock_translator._ConfigurableTranslator__event_window_time)

    # __get_activated_events

    @patch(f"{SCRIPT_LOCATION}.get_service_to_respond")
    @patch(f"{SCRIPT_LOCATION}.get_event_type_record_01")
    @pytest.mark.parametrize("number_of_activated_events", [0, 1, 5])
    def test_get_activated_events__only_mandatory(self, mock_get_event_type_record_01,
                                                  mock_get_service_to_respond,
                                                  number_of_activated_events):
        self.mock_translator._ConfigurableTranslator__get_event_type_record.return_value = None
        self.mock_translator._ConfigurableTranslator__get_event_type_record_09_continuation.return_value = None
        assert (ConfigurableTranslator._ConfigurableTranslator__get_activated_events(self.mock_translator,
                                                                                     number_of_activated_events) == (
                    self.mock_translator._ConfigurableTranslator__get_event_type_of_active_event.return_value,
                    self.mock_conditional_mapping_data_record.return_value
                ) * number_of_activated_events)
        calls = [call(i + 1) for i in range(number_of_activated_events)]
        self.mock_translator._ConfigurableTranslator__get_event_window_time.assert_has_calls(calls, any_order=False)
        mock_get_event_type_record_01.assert_has_calls(calls, any_order=False)
        mock_get_service_to_respond.assert_has_calls(calls, any_order=False)
        assert self.mock_conditional_mapping_data_record.call_count == number_of_activated_events
        self.mock_conditional_mapping_data_record.assert_has_calls(number_of_activated_events * [
            call(mapping={
                0x01: (self.mock_translator._ConfigurableTranslator__get_event_window_time.return_value,
                       mock_get_event_type_record_01.return_value,
                       mock_get_service_to_respond.return_value)},
                value_mask=0x3F)])

    @patch(f"{SCRIPT_LOCATION}.get_service_to_respond")
    @patch(f"{SCRIPT_LOCATION}.get_event_type_record_01")
    @pytest.mark.parametrize("number_of_activated_events", [0, 1, 5])
    def test_get_activated_events__all(self, mock_get_event_type_record_01,
                                       mock_get_service_to_respond,
                                       number_of_activated_events):
        self.mock_translator._ConfigurableTranslator__get_event_type_record.return_value = Mock()
        self.mock_translator._ConfigurableTranslator__get_event_type_record_09_continuation.return_value = Mock()
        assert (ConfigurableTranslator._ConfigurableTranslator__get_activated_events(self.mock_translator,
                                                                                     number_of_activated_events) == (
                    self.mock_translator._ConfigurableTranslator__get_event_type_of_active_event.return_value,
                    self.mock_conditional_mapping_data_record.return_value
                ) * number_of_activated_events)
        calls = [call(i + 1) for i in range(number_of_activated_events)]
        self.mock_translator._ConfigurableTranslator__get_event_window_time.assert_has_calls(calls, any_order=False)
        mock_get_event_type_record_01.assert_has_calls(calls, any_order=False)
        mock_get_service_to_respond.assert_has_calls(calls, any_order=False)
        assert self.mock_conditional_mapping_data_record.call_count == number_of_activated_events
        self.mock_conditional_mapping_data_record.assert_has_calls(number_of_activated_events * [
            call(mapping={
                0x01: (self.mock_translator._ConfigurableTranslator__get_event_window_time.return_value,
                       mock_get_event_type_record_01.return_value,
                       mock_get_service_to_respond.return_value),
                0x02: (self.mock_translator._ConfigurableTranslator__get_event_window_time.return_value,
                       self.mock_translator._ConfigurableTranslator__get_event_type_record.return_value,
                       mock_get_service_to_respond.return_value),
                0x03: (self.mock_translator._ConfigurableTranslator__get_event_window_time.return_value,
                       self.mock_translator._ConfigurableTranslator__get_event_type_record.return_value,
                       mock_get_service_to_respond.return_value),
                0x07: (self.mock_translator._ConfigurableTranslator__get_event_window_time.return_value,
                       self.mock_translator._ConfigurableTranslator__get_event_type_record.return_value,
                       mock_get_service_to_respond.return_value),
                0x08: (self.mock_translator._ConfigurableTranslator__get_event_window_time.return_value,
                       self.mock_translator._ConfigurableTranslator__get_event_type_record.return_value),
                0x09: (self.mock_translator._ConfigurableTranslator__get_event_window_time.return_value,
                       self.mock_translator._ConfigurableTranslator__get_event_type_record.return_value,
                       self.mock_translator._ConfigurableTranslator__get_event_type_record_09_continuation.return_value,),
            },
                value_mask=0x3F)])

    # __get_event_type_of_active_event

    @pytest.mark.parametrize("event_number", [1, 32])
    def test_get_event_type_of_active_event(self, event_number):
        assert (ConfigurableTranslator._ConfigurableTranslator__get_event_type_of_active_event(
            self.mock_translator, event_number) == self.mock_raw_data_record.return_value)
        self.mock_raw_data_record.assert_called_once_with(
            name=f"eventTypeOfActiveEvent#{event_number}",
            length=8,
            children=(RESERVED_BIT,
                      self.mock_translator._ConfigurableTranslator__event_type))

    # __get_event_type_record

    def test_get_event_type_record__value_error(self):
        mock_get = Mock(return_value=None)
        self.mock_translator.services_mapping = MagicMock(get=mock_get)
        with pytest.raises(ValueError):
            ConfigurableTranslator._ConfigurableTranslator__get_event_type_record(
                self.mock_translator, Mock(), Mock())
        mock_get.assert_called_once_with(RequestSID.ResponseOnEvent, None)

    @pytest.mark.parametrize("event_number", [1, 32])
    @pytest.mark.parametrize("event", [2, 9])
    def test_get_event_type_record__none(self, event, event_number):
        self.mock_translator.services_mapping = {
            RequestSID.ResponseOnEvent: MagicMock(
                response_structure=[MagicMock(), MagicMock(mapping={i: 2*[MagicMock()] for i in range(5)})]),
        }
        assert ConfigurableTranslator._ConfigurableTranslator__get_event_type_record(
            self.mock_translator, event_number=event_number, event=event) is None
        self.mock_deepcopy.assert_not_called()

    @pytest.mark.parametrize("event_number", [1, 32])
    @pytest.mark.parametrize("event", [2, 9])
    def test_get_event_type_record__valid(self, event, event_number):
        self.mock_translator.services_mapping = {
            RequestSID.ResponseOnEvent: MagicMock(
                response_structure=[MagicMock(), MagicMock(mapping={i: 10*[MagicMock()] for i in range(10)})]),
        }
        assert ConfigurableTranslator._ConfigurableTranslator__get_event_type_record(
            self.mock_translator, event_number=event_number, event=event) == self.mock_deepcopy.return_value
        self.mock_deepcopy.return_value.name.endswith(f"#{event_number}")
        self.mock_deepcopy.assert_called_once_with(
            self.mock_translator.services_mapping[RequestSID.ResponseOnEvent].response_structure[1].mapping[event][2])

    # __get_event_type_record_09_continuation

    def test_get_event_type_record_09_continuation__value_error(self):
        mock_get = Mock(return_value=None)
        self.mock_translator.services_mapping = MagicMock(get=mock_get)
        with pytest.raises(ValueError):
            ConfigurableTranslator._ConfigurableTranslator__get_event_type_record_09_continuation(
                self.mock_translator, Mock())
        mock_get.assert_called_once_with(RequestSID.ResponseOnEvent, None)

    @pytest.mark.parametrize("event_number", [1, 32])
    def test_get_event_type_record_09_continuation__none(self, event_number):
        self.mock_translator.services_mapping = {
            RequestSID.ResponseOnEvent: MagicMock(
                response_structure=[MagicMock(), MagicMock(mapping={})]),
        }
        assert ConfigurableTranslator._ConfigurableTranslator__get_event_type_record_09_continuation(
            self.mock_translator, event_number=event_number) is None
        self.mock_deepcopy.assert_not_called()

    @pytest.mark.parametrize("event_number", [1, 32])
    def test_get_event_type_record_09_continuation__valid(self, event_number):
        self.mock_translator.services_mapping = {
            RequestSID.ResponseOnEvent: MagicMock(
                response_structure=[MagicMock(), MagicMock(mapping={
                    0x09: [MagicMock(), MagicMock(), MagicMock(), MagicMock()]
                })]),
        }
        self.mock_deepcopy.return_value = Mock(mapping={
            0x04: [Mock(), Mock()],
            0x09: [Mock()],
            0x12: [Mock(), Mock(), Mock()],
        })
        assert ConfigurableTranslator._ConfigurableTranslator__get_event_type_record_09_continuation(
            self.mock_translator, event_number=event_number) == self.mock_deepcopy.return_value
        self.mock_deepcopy.return_value.name.endswith(f"#{event_number}")
        self.mock_deepcopy.assert_called_once_with(
            self.mock_translator.services_mapping[RequestSID.ResponseOnEvent].response_structure[1].mapping[0x09][3])
        for data_records in self.mock_deepcopy.return_value.mapping.values():
            for data_record in data_records:
                assert data_record.name.endswith(f"#{event_number}")


@pytest.mark.integration
class TestConfigurableTranslatorIntegration:
    """Integration tests for `ConfigurableTranslator` class."""

    diagnostic_session_type_mapping = {
        0x01: "Default",
        0x03: "Extended",
        0x40: "Custom"
    }
    reset_type_mapping = {
        0x03: "Hard",
        0x40: "Custom"
    }
    report_type_mapping = {
        0x01: "reportDTCNumberByStatusMask",
        0x02: "reportDTCByStatusMask",
        0x03: "reportInternalDTCMapping"
    }
    security_access_type_mapping = {
        0x03: "requestSeedForProgramming",
        0x04: "sendKeyForProgramming",
        0x07: "requestSeedForScrapping",
        0x08: "sendKeyForScrapping"
    }
    control_type_type_mapping = {
        0x00: "enableRxAndTx",
        0x03: "disableRxAndTx",
        0x40: "Custom"
    }
    authentication_task_mapping = {
        0x00: "deAuthenticate",
        0x40: "CustomAuthentication"
    }
    definition_type_mapping = {
        0x01: "defineByIdentifier",
        0x03: "clearDynamicallyDefinedDataIdentifier",
        0x40: "CustomDefinition"
    }
    routine_control_type_mapping = {
        0x01: "startRoutine",
        0x02: "stopRoutine",
        0x03: "requestRoutineResults",
        0x40: "block"
    }
    zero_subfunction_mapping = {
        0x00: "default",
        0x41: "till reset"
    }
    timing_parameter_access_type_mapping = {
        0x01: "readExtendedTimingParameterSet",
        0x02: "Custom"
    }
    dtc_setting_type_mapping = {
        0x01: "ON",
        0x02: "OFF",
        0x40: "Custom"
    }
    event_type_mapping = {
        0x00: "stopResponseOnEvent",
        0x01: "onDTCStatusChange",
        0x02: "onTimerInterrupt",
        0x03: "onChangeOfDataIdentifier",
        0x04: "reportActivatedEvents",
        0x05: "startResponseOnEvent",
        0x06: "clearResponseOnEvent",
        0x07: "onComparisonOfValues",
        0x08: "reportMostRecentDtcOnStatusChange",
        0x09: "reportDTCRecordInformationOnDtcStatusChange",
        0x10: "custom",
    }
    link_control_type_mapping = {
        0x01: "verifyModeTransitionWithFixedParameter",
        0x02: "verifyModeTransitionWithSpecificParameter",
        0x03: "transitionMode",
        0x40: "custom",
    }
    rid_mapping = {
        0x1234: "ABC",
        0x5678: "XYZ",
    }
    did_mapping = {
        0x0100: "Custom DID#1",
        0x0101: "Custom DID#2",
        0xF186: "ActiveDiagnosticSessionDataIdentifier",
    }
    did_data_mapping = {
        0x0100: (RawDataRecord(name="Param1", length=8, min_occurrences=2, max_occurrences=2), ),
        0x0101: (RawDataRecord(name="a#1", length=4), RawDataRecord(name="a#2", length=4)),
        0xF186: (RESERVED_BIT, ACTIVE_DIAGNOSTIC_SESSION),
    }

    def setup_class(self):
        self.minimalistic_translator = Translator(services=(DIAGNOSTIC_SESSION_CONTROL,
                                                            TESTER_PRESENT,
                                                            ACCESS_TIMING_PARAMETER_2013,
                                                            READ_DATA_BY_IDENTIFIER))

    @pytest.fixture(scope="class")
    @classmethod
    def configurable_translator_1(cls):
        return ConfigurableTranslator(
            base=cls.minimalistic_translator,
            diagnostic_session_type_mapping=cls.diagnostic_session_type_mapping,
            zero_subfunction_mapping=cls.zero_subfunction_mapping,
            timing_parameter_access_type_mapping=cls.timing_parameter_access_type_mapping,
            did_mapping=cls.did_mapping,
            did_data_mapping=cls.did_data_mapping)

    @pytest.fixture(scope="class")
    @classmethod
    def configurable_translator_2(cls):
        return ConfigurableTranslator(
            base=BASE_TRANSLATOR,
            diagnostic_session_type_mapping=cls.diagnostic_session_type_mapping,
            reset_type_mapping=cls.reset_type_mapping,
            report_type_mapping=cls.report_type_mapping,
            security_access_type_mapping=cls.security_access_type_mapping,
            control_type_type_mapping=cls.control_type_type_mapping,
            authentication_task_mapping=cls.authentication_task_mapping,
            definition_type_mapping=cls.definition_type_mapping,
            routine_control_type_mapping=cls.routine_control_type_mapping,
            zero_subfunction_mapping=cls.zero_subfunction_mapping,
            dtc_setting_type_mapping=cls.dtc_setting_type_mapping,
            event_type_mapping=cls.event_type_mapping,
            link_control_type_mapping=cls.link_control_type_mapping,
            rid_mapping=cls.rid_mapping,
            did_mapping=cls.did_mapping,
            did_data_mapping=cls.did_data_mapping)

    def test_configuration_1(self, configurable_translator_1):
        # defined
        assert configurable_translator_1.diagnostic_session_type_mapping == self.diagnostic_session_type_mapping
        assert configurable_translator_1.zero_subfunction_mapping == self.zero_subfunction_mapping
        assert configurable_translator_1.timing_parameter_access_type_mapping == self.timing_parameter_access_type_mapping
        assert configurable_translator_1.did_mapping == self.did_mapping
        assert configurable_translator_1.did_data_mapping == self.did_data_mapping
        # undefined
        assert configurable_translator_1.reset_type_mapping is None
        assert configurable_translator_1.report_type_mapping is None
        assert configurable_translator_1.security_access_type_mapping is None
        assert configurable_translator_1.control_type_type_mapping is None
        assert configurable_translator_1.authentication_task_mapping is None
        assert configurable_translator_1.definition_type_mapping is None
        assert configurable_translator_1.routine_control_type_mapping is None
        assert configurable_translator_1.dtc_setting_type_mapping is None
        assert configurable_translator_1.event_type_mapping is None
        assert configurable_translator_1.link_control_type_mapping is None
        assert configurable_translator_1.rid_mapping is None
        # unchanged base
        assert self.minimalistic_translator.services_mapping[RequestSID.DiagnosticSessionControl] == DIAGNOSTIC_SESSION_CONTROL
        assert DIAGNOSTIC_SESSION_CONTROL.request_structure[0].children[1].values_mapping != configurable_translator_1.diagnostic_session_type_mapping
        assert DIAGNOSTIC_SESSION_CONTROL.response_structure[0].children[1].values_mapping != configurable_translator_1.diagnostic_session_type_mapping
        assert self.minimalistic_translator.services_mapping[RequestSID.TesterPresent] == TESTER_PRESENT
        assert TESTER_PRESENT.request_structure[0].children[1].values_mapping != configurable_translator_1.zero_subfunction_mapping
        assert TESTER_PRESENT.response_structure[0].children[1].values_mapping != configurable_translator_1.zero_subfunction_mapping
        assert self.minimalistic_translator.services_mapping[RequestSID.AccessTimingParameter] == ACCESS_TIMING_PARAMETER_2013
        assert ACCESS_TIMING_PARAMETER_2013.request_structure[0].children[1].values_mapping != configurable_translator_1.timing_parameter_access_type_mapping
        assert ACCESS_TIMING_PARAMETER_2013.response_structure[0].children[1].values_mapping != configurable_translator_1.timing_parameter_access_type_mapping
        assert self.minimalistic_translator.services_mapping[RequestSID.ReadDataByIdentifier] == READ_DATA_BY_IDENTIFIER
        assert READ_DATA_BY_IDENTIFIER.request_structure[0].values_mapping != configurable_translator_1.did_mapping
        assert READ_DATA_BY_IDENTIFIER.response_structure[0].values_mapping != configurable_translator_1.did_mapping

    def test_configuration_2(self, configurable_translator_2):
        # defined
        assert configurable_translator_2.diagnostic_session_type_mapping == self.diagnostic_session_type_mapping
        assert configurable_translator_2.reset_type_mapping == self.reset_type_mapping
        assert configurable_translator_2.report_type_mapping == self.report_type_mapping
        assert configurable_translator_2.security_access_type_mapping == self.security_access_type_mapping
        assert configurable_translator_2.control_type_type_mapping == self.control_type_type_mapping
        assert configurable_translator_2.authentication_task_mapping == self.authentication_task_mapping
        assert configurable_translator_2.definition_type_mapping == self.definition_type_mapping
        assert configurable_translator_2.routine_control_type_mapping == self.routine_control_type_mapping
        assert configurable_translator_2.zero_subfunction_mapping == self.zero_subfunction_mapping
        assert configurable_translator_2.dtc_setting_type_mapping == self.dtc_setting_type_mapping
        assert configurable_translator_2.event_type_mapping == self.event_type_mapping
        assert configurable_translator_2.link_control_type_mapping == self.link_control_type_mapping
        assert configurable_translator_2.rid_mapping == self.rid_mapping
        assert configurable_translator_2.did_mapping == self.did_mapping
        assert configurable_translator_2.did_data_mapping == self.did_data_mapping
        # undefined
        assert configurable_translator_2.timing_parameter_access_type_mapping is None
        # unchanged base
        assert BASE_TRANSLATOR.services_mapping[RequestSID.DiagnosticSessionControl] == DIAGNOSTIC_SESSION_CONTROL
        assert DIAGNOSTIC_SESSION_CONTROL.request_structure[0].children[1].values_mapping == DIAGNOSTIC_SESSION_TYPE_MAPPING
        assert DIAGNOSTIC_SESSION_CONTROL.response_structure[0].children[1].values_mapping == DIAGNOSTIC_SESSION_TYPE_MAPPING
        assert BASE_TRANSLATOR.services_mapping[RequestSID.ECUReset] == ECU_RESET
        assert ECU_RESET.request_structure[0].children[1].values_mapping == RESET_TYPE_MAPPING
        assert ECU_RESET.response_structure[0].children[1].values_mapping == RESET_TYPE_MAPPING
        assert BASE_TRANSLATOR.services_mapping[RequestSID.ReadDTCInformation] == READ_DTC_INFORMATION
        assert READ_DTC_INFORMATION.request_structure[0].children[1].values_mapping == REPORT_TYPE_MAPPING_2020
        assert READ_DTC_INFORMATION.response_structure[0].children[1].values_mapping == REPORT_TYPE_MAPPING_2020
        assert BASE_TRANSLATOR.services_mapping[RequestSID.SecurityAccess] == SECURITY_ACCESS
        assert SECURITY_ACCESS.request_structure[0].children[1].values_mapping == SECURITY_ACCESS_TYPE_MAPPING
        assert SECURITY_ACCESS.response_structure[0].children[1].values_mapping == SECURITY_ACCESS_TYPE_MAPPING
        assert BASE_TRANSLATOR.services_mapping[RequestSID.CommunicationControl] == COMMUNICATION_CONTROL
        assert COMMUNICATION_CONTROL.request_structure[0].children[1].values_mapping == CONTROL_TYPE_MAPPING
        assert COMMUNICATION_CONTROL.response_structure[0].children[1].values_mapping == CONTROL_TYPE_MAPPING
        assert BASE_TRANSLATOR.services_mapping[RequestSID.Authentication] == AUTHENTICATION
        assert AUTHENTICATION.request_structure[0].children[1].values_mapping == AUTHENTICATION_TASK_MAPPING
        assert AUTHENTICATION.response_structure[0].children[1].values_mapping == AUTHENTICATION_TASK_MAPPING
        assert BASE_TRANSLATOR.services_mapping[RequestSID.DynamicallyDefineDataIdentifier] == DYNAMICALLY_DEFINE_DATA_IDENTIFIER
        assert DYNAMICALLY_DEFINE_DATA_IDENTIFIER.request_structure[0].children[1].values_mapping == DEFINITION_TYPE_MAPPING
        assert DYNAMICALLY_DEFINE_DATA_IDENTIFIER.response_structure[0].children[1].values_mapping == DEFINITION_TYPE_MAPPING
        assert BASE_TRANSLATOR.services_mapping[RequestSID.RoutineControl] == ROUTINE_CONTROL
        assert ROUTINE_CONTROL.request_structure[0].children[1].values_mapping == ROUTINE_CONTROL_TYPE_MAPPING
        assert ROUTINE_CONTROL.response_structure[0].children[1].values_mapping == ROUTINE_CONTROL_TYPE_MAPPING
        assert BASE_TRANSLATOR.services_mapping[RequestSID.TesterPresent] == TESTER_PRESENT
        assert TESTER_PRESENT.request_structure[0].children[1].values_mapping == ZERO_SUBFUNCTION_MAPPING
        assert TESTER_PRESENT.response_structure[0].children[1].values_mapping == ZERO_SUBFUNCTION_MAPPING
        assert BASE_TRANSLATOR.services_mapping[RequestSID.ControlDTCSetting] == CONTROL_DTC_SETTING
        assert CONTROL_DTC_SETTING.request_structure[0].children[1].values_mapping == DTC_SETTING_TYPE_MAPPING
        assert CONTROL_DTC_SETTING.response_structure[0].children[1].values_mapping == DTC_SETTING_TYPE_MAPPING
        assert BASE_TRANSLATOR.services_mapping[RequestSID.ResponseOnEvent] == RESPONSE_ON_EVENT
        assert RESPONSE_ON_EVENT.request_structure[0].children[1].children[1].values_mapping == EVENT_MAPPING_2020
        assert RESPONSE_ON_EVENT.response_structure[0].children[1].children[1].values_mapping == EVENT_MAPPING_2020
        assert BASE_TRANSLATOR.services_mapping[RequestSID.LinkControl] == LINK_CONTROL
        assert LINK_CONTROL.request_structure[0].children[1].values_mapping == LINK_CONTROL_TYPE_MAPPING
        assert LINK_CONTROL.response_structure[0].children[1].values_mapping == LINK_CONTROL_TYPE_MAPPING
        assert BASE_TRANSLATOR.services_mapping[RequestSID.ReadDataByIdentifier] == READ_DATA_BY_IDENTIFIER
        assert READ_DATA_BY_IDENTIFIER.request_structure[0].values_mapping == DID_MAPPING_2020
        assert READ_DATA_BY_IDENTIFIER.response_structure[0].values_mapping == DID_MAPPING_2020
        assert BASE_TRANSLATOR.services_mapping[RequestSID.WriteDataByIdentifier] == WRITE_DATA_BY_IDENTIFIER
        assert WRITE_DATA_BY_IDENTIFIER.request_structure[0].values_mapping == DID_MAPPING_2020
        assert WRITE_DATA_BY_IDENTIFIER.response_structure[0].values_mapping == DID_MAPPING_2020
        assert BASE_TRANSLATOR.services_mapping[RequestSID.ReadScalingDataByIdentifier] == READ_SCALING_DATA_BY_IDENTIFIER
        assert READ_SCALING_DATA_BY_IDENTIFIER.request_structure[0].values_mapping == DID_MAPPING_2020
        assert READ_SCALING_DATA_BY_IDENTIFIER.response_structure[0].values_mapping == DID_MAPPING_2020
        assert BASE_TRANSLATOR.services_mapping[RequestSID.InputOutputControlByIdentifier] == INPUT_OUTPUT_CONTROL_BY_IDENTIFIER
        assert INPUT_OUTPUT_CONTROL_BY_IDENTIFIER.request_structure[0].values_mapping == DID_MAPPING_2020
        assert INPUT_OUTPUT_CONTROL_BY_IDENTIFIER.response_structure[0].values_mapping == DID_MAPPING_2020
        assert BASE_TRANSLATOR.services_mapping[RequestSID.ReadDataByPeriodicIdentifier] == READ_DATA_BY_PERIODIC_IDENTIFIER
        assert BASE_TRANSLATOR.services_mapping[RequestSID.ReadMemoryByAddress] == READ_MEMORY_BY_ADDRESS
        assert BASE_TRANSLATOR.services_mapping[RequestSID.WriteMemoryByAddress] == WRITE_MEMORY_BY_ADDRESS
        assert BASE_TRANSLATOR.services_mapping[RequestSID.SecuredDataTransmission] == SECURED_DATA_TRANSMISSION
        assert BASE_TRANSLATOR.services_mapping[RequestSID.ClearDiagnosticInformation] == CLEAR_DIAGNOSTIC_INFORMATION
        assert BASE_TRANSLATOR.services_mapping[RequestSID.RequestTransferExit] == REQUEST_TRANSFER_EXIT
        assert BASE_TRANSLATOR.services_mapping[RequestSID.RequestFileTransfer] == REQUEST_FILE_TRANSFER
        assert BASE_TRANSLATOR.services_mapping[RequestSID.TransferData] == TRANSFER_DATA
        assert BASE_TRANSLATOR.services_mapping[RequestSID.RequestDownload] == REQUEST_DOWNLOAD
        assert BASE_TRANSLATOR.services_mapping[RequestSID.RequestUpload] == REQUEST_UPLOAD

    @pytest.mark.parametrize("payload, decoded_message", [
        # DiagnosticSessionControl
        (
            [0x10, 0x40],
            (
                {
                    "name": "SID",
                    "length": 8,
                    "raw_value": 0x10,
                    "physical_value": "DiagnosticSessionControl",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x40,
                    "physical_value": 0x40,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 0,
                            "physical_value": "no",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "diagnosticSessionType",
                            "length": 7,
                            "raw_value": 0x40,
                            "physical_value": diagnostic_session_type_mapping.get(0x40, 0x40),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
            )
        ),
        (
            [0x50, 0x82, 0x12, 0x34, 0x56, 0x78],
            (
                {
                    "name": "RSID",
                    "length": 8,
                    "raw_value": 0x50,
                    "physical_value": "DiagnosticSessionControl",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x82,
                    "physical_value": 0x82,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 1,
                            "physical_value": "yes",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "diagnosticSessionType",
                            "length": 7,
                            "raw_value": 0x02,
                            "physical_value": diagnostic_session_type_mapping.get(0x02, 0x02),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 16,
                            'name': 'P2Server_max',
                            'physical_value': 0x1234,
                            'raw_value': 0x1234,
                            'unit': 'ms'
                        },
                        {
                            'children': (),
                            'length': 16,
                            'name': 'P2*Server_max',
                            'physical_value': 221360,
                            'raw_value': 0x5678,
                            'unit': 'ms'
                        }
                    ),
                    'length': 32,
                    'name': 'sessionParameterRecord',
                    'physical_value': 0x12345678,
                    'raw_value': 0x12345678,
                    'unit': None
                }
            )
        ),
        # TesterPresent
        (
            [0x3E, 0x41],
            (
                {
                    "name": "SID",
                    "length": 8,
                    "raw_value": 0x3E,
                    "physical_value": "TesterPresent",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x41,
                    "physical_value": 0x41,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 0,
                            "physical_value": "no",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "zeroSubFunction",
                            "length": 7,
                            "raw_value": 0x41,
                            "physical_value": zero_subfunction_mapping.get(0x41, 0x41),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
            )
        ),
        (
            [0x7E, 0x80],
            (
                {
                    "name": "RSID",
                    "length": 8,
                    "raw_value": 0x7E,
                    "physical_value": "TesterPresent",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x80,
                    "physical_value": 0x80,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 1,
                            "physical_value": "yes",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "zeroSubFunction",
                            "length": 7,
                            "raw_value": 0x00,
                            "physical_value": zero_subfunction_mapping.get(0x00, 0x00),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
            )
        ),
        # AccessTimingParameter
        (
            [0x83, 0x82],
            (
                {
                    "name": "SID",
                    "length": 8,
                    "raw_value": 0x83,
                    "physical_value": "AccessTimingParameter",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x82,
                    "physical_value": 0x82,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 1,
                            "physical_value": "yes",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "timingParameterAccessType",
                            "length": 7,
                            "raw_value": 0x02,
                            "physical_value": timing_parameter_access_type_mapping.get(0x02, 0x02),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
            )
        ),
        (
            [0xC3, 0x04],
            (
                {
                    "name": "RSID",
                    "length": 8,
                    "raw_value": 0xC3,
                    "physical_value": "AccessTimingParameter",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x04,
                    "physical_value": 0x04,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 0,
                            "physical_value": "no",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "timingParameterAccessType",
                            "length": 7,
                            "raw_value": 0x04,
                            "physical_value": timing_parameter_access_type_mapping.get(0x04, 0x04),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
            )
        ),
        # ReadDataByIdentifier
        (
            [0x22, 0x01, 0x00, 0x01, 0x01, 0xF1, 0x85],
            (
                {
                    "name": "SID",
                    "length": 8,
                    "raw_value": 0x22,
                    "physical_value": "ReadDataByIdentifier",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "DID",
                    "length": 16,
                    "raw_value": (0x0100, 0x0101, 0xF185),
                    "physical_value": (did_mapping.get(0x0100, 0x0100),
                                       did_mapping.get(0x0101, 0x0101),
                                       did_mapping.get(0xF185, 0xF185)),
                    "children": ((), (), ()),
                    "unit": None,
                },
            )
        ),
        (
            [0x62, 0x01, 0x00, 0xB4, 0xC5, 0x01, 0x01, 0xFE],
            (
                {
                    "name": "RSID",
                    "length": 8,
                    "raw_value": 0x62,
                    "physical_value": "ReadDataByIdentifier",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "DID#1",
                    "length": 16,
                    "raw_value": 0x0100,
                    "physical_value": did_mapping.get(0x0100, 0x0100),
                    "children": (),
                    "unit": None,
                },
                {
                    'children': (
                        {
                            'children': ((), ()),
                            'length': 8,
                            'name': 'Param1',
                            'physical_value': (0xB4, 0xC5),
                            'raw_value': (0xB4, 0xC5),
                            'unit': None
                        },
                    ),
                    'length': 16,
                    'name': 'DID#1 data',
                    'physical_value': 0xB4C5,
                    'raw_value': 0xB4C5,
                    'unit': None
                },
                {
                    "name": "DID#2",
                    "length": 16,
                    "raw_value": 0x0101,
                    "physical_value": did_mapping.get(0x0101, 0x0101),
                    "children": (),
                    "unit": None,
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'a#1',
                            'physical_value': 0xF,
                            'raw_value': 0xF,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'a#2',
                            'physical_value': 0xE,
                            'raw_value': 0xE,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'DID#2 data',
                    'physical_value': 0xFE,
                    'raw_value': 0xFE,
                    'unit': None
                },
            )
        ),
    ])
    def test_decode_1(self, configurable_translator_1, payload, decoded_message):
        assert configurable_translator_1.decode(payload=payload) == decoded_message

    @pytest.mark.parametrize("payload, decoded_message", [
        # DiagnosticSessionControl
        (
            [0x10, 0x40],
            (
                {
                    "name": "SID",
                    "length": 8,
                    "raw_value": 0x10,
                    "physical_value": "DiagnosticSessionControl",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x40,
                    "physical_value": 0x40,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 0,
                            "physical_value": "no",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "diagnosticSessionType",
                            "length": 7,
                            "raw_value": 0x40,
                            "physical_value": diagnostic_session_type_mapping.get(0x40, 0x40),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
            )
        ),
        (
            [0x50, 0x82, 0x12, 0x34, 0x56, 0x78],
            (
                {
                    "name": "RSID",
                    "length": 8,
                    "raw_value": 0x50,
                    "physical_value": "DiagnosticSessionControl",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x82,
                    "physical_value": 0x82,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 1,
                            "physical_value": "yes",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "diagnosticSessionType",
                            "length": 7,
                            "raw_value": 0x02,
                            "physical_value": diagnostic_session_type_mapping.get(0x02, 0x02),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 16,
                            'name': 'P2Server_max',
                            'physical_value': 0x1234,
                            'raw_value': 0x1234,
                            'unit': 'ms'
                        },
                        {
                            'children': (),
                            'length': 16,
                            'name': 'P2*Server_max',
                            'physical_value': 221360,
                            'raw_value': 0x5678,
                            'unit': 'ms'
                        }
                    ),
                    'length': 32,
                    'name': 'sessionParameterRecord',
                    'physical_value': 0x12345678,
                    'raw_value': 0x12345678,
                    'unit': None
                }
            )
        ),
        # ECUReset
        (
            [0x11, 0x81],
            (
                {
                    "name": "SID",
                    "length": 8,
                    "raw_value": 0x11,
                    "physical_value": "ECUReset",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x81,
                    "physical_value": 0x81,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 1,
                            "physical_value": "yes",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "resetType",
                            "length": 7,
                            "raw_value": 0x01,
                            "physical_value": reset_type_mapping.get(0x01, 0x01),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
            )
        ),
        (
            [0x51, 0x03],
            (
                {
                    "name": "RSID",
                    "length": 8,
                    "raw_value": 0x51,
                    "physical_value": "ECUReset",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x03,
                    "physical_value": 0x03,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 0,
                            "physical_value": "no",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "resetType",
                            "length": 7,
                            "raw_value": 0x03,
                            "physical_value": reset_type_mapping.get(0x03, 0x03),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
            )
        ),
        # SecurityAccess
        (
            [0x27, 0x03],
            (
                {
                    "name": "SID",
                    "length": 8,
                    "raw_value": 0x27,
                    "physical_value": "SecurityAccess",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x03,
                    "physical_value": 0x03,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 0,
                            "physical_value": "no",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "securityAccessType",
                            "length": 7,
                            "raw_value": 0x03,
                            "physical_value": security_access_type_mapping.get(0x03, 0x03),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
            )
        ),
        (
            [0x67, 0x07, 0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0],
            (
                {
                    "name": "RSID",
                    "length": 8,
                    "raw_value": 0x67,
                    "physical_value": "SecurityAccess",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x07,
                    "physical_value": 0x07,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 0,
                            "physical_value": "no",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "securityAccessType",
                            "length": 7,
                            "raw_value": 0x07,
                            "physical_value": security_access_type_mapping.get(0x07, 0x07),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
                {
                    'children': ((), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'securitySeed',
                    'physical_value': (0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0),
                    'raw_value': (0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0),
                    'unit': None
                }
            )
        ),
        # CommunicationControl
        (
            [0x28, 0x81, 0xFF],
            (
                {
                    "name": "SID",
                    "length": 8,
                    "raw_value": 0x28,
                    "physical_value": "CommunicationControl",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x81,
                    "physical_value": 0x81,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 1,
                            "physical_value": "yes",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "controlType",
                            "length": 7,
                            "raw_value": 0x01,
                            "physical_value": control_type_type_mapping.get(0x01, 0x01),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 2,
                            'name': 'messagesType',
                            'physical_value': 'networkManagementCommunicationMessages and normalCommunicationMessages',
                            'raw_value': 0x3,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 2,
                            'name': 'reserved',
                            'physical_value': 3,
                            'raw_value': 0x3,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'networks',
                            'physical_value': 'network on which this request is received',
                            'raw_value': 0xF,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'communicationType',
                    'physical_value': 0xFF,
                    'raw_value': 0xFF,
                    'unit': None
                },
            )
        ),
        (
            [0x68, 0x40],
            (
                {
                    "name": "RSID",
                    "length": 8,
                    "raw_value": 0x68,
                    "physical_value": "CommunicationControl",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x40,
                    "physical_value": 0x40,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 0,
                            "physical_value": "no",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "controlType",
                            "length": 7,
                            "raw_value": 0x40,
                            "physical_value": control_type_type_mapping.get(0x40, 0x40),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
            )
        ),
        # Authentication
        (
            [0x29, 0x00],
            (
                {
                    "name": "SID",
                    "length": 8,
                    "raw_value": 0x29,
                    "physical_value": "Authentication",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x00,
                    "physical_value": 0x00,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 0,
                            "physical_value": "no",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "authenticationTask",
                            "length": 7,
                            "raw_value": 0x00,
                            "physical_value": authentication_task_mapping.get(0x00, 0x00),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
            )
        ),
        (
            [0x69, 0x08, 0x03],
            (
                {
                    "name": "RSID",
                    "length": 8,
                    "raw_value": 0x69,
                    "physical_value": "Authentication",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x08,
                    "physical_value": 0x08,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 0,
                            "physical_value": "no",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "authenticationTask",
                            "length": 7,
                            "raw_value": 0x08,
                            "physical_value": authentication_task_mapping.get(0x08, 0x08),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'authenticationReturnParameter',
                    'physical_value': 'AuthenticationConfiguration ACR with asymmetric cryptography',
                    'raw_value': 0x03,
                    'unit': None
                }
            )
        ),
        # TesterPresent
        (
            [0x3E, 0x41],
            (
                {
                    "name": "SID",
                    "length": 8,
                    "raw_value": 0x3E,
                    "physical_value": "TesterPresent",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x41,
                    "physical_value": 0x41,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 0,
                            "physical_value": "no",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "zeroSubFunction",
                            "length": 7,
                            "raw_value": 0x41,
                            "physical_value": zero_subfunction_mapping.get(0x41, 0x41),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
            )
        ),
        (
            [0x7E, 0x80],
            (
                {
                    "name": "RSID",
                    "length": 8,
                    "raw_value": 0x7E,
                    "physical_value": "TesterPresent",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x80,
                    "physical_value": 0x80,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 1,
                            "physical_value": "yes",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "zeroSubFunction",
                            "length": 7,
                            "raw_value": 0x00,
                            "physical_value": zero_subfunction_mapping.get(0x00, 0x00),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
            )
        ),
        # ControlDTCSetting
        (
            [0x85, 0x01],
            (
                {
                    "name": "SID",
                    "length": 8,
                    "raw_value": 0x85,
                    "physical_value": "ControlDTCSetting",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x01,
                    "physical_value": 0x01,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 0,
                            "physical_value": "no",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "DTCSettingType",
                            "length": 7,
                            "raw_value": 0x01,
                            "physical_value": dtc_setting_type_mapping.get(0x01, 0x01),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
            )
        ),
        (
            [0xC5, 0xC0],
            (
                {
                    "name": "RSID",
                    "length": 8,
                    "raw_value": 0xC5,
                    "physical_value": "ControlDTCSetting",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0xC0,
                    "physical_value": 0xC0,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 1,
                            "physical_value": "yes",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "DTCSettingType",
                            "length": 7,
                            "raw_value": 0x40,
                            "physical_value": dtc_setting_type_mapping.get(0x40, 0x40),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
            )
        ),
        # ResponseOnEvent
        (
            [0x86, 0xC0, 0x02],
            (
                {
                    "name": "SID",
                    "length": 8,
                    "raw_value": 0x86,
                    "physical_value": "ResponseOnEvent",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0xC0,
                    "physical_value": 0xC0,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 1,
                            "physical_value": "yes",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "eventType",
                            "length": 7,
                            "raw_value": 0x40,
                            "physical_value": 0x40,
                            "children": (
                                {
                                    "name": "storageState",
                                    "length": 1,
                                    "raw_value": 1,
                                    "physical_value": "storeEvent",
                                    "children": (),
                                    "unit": None,
                                },
                                {
                                    "name": "event",
                                    "length": 6,
                                    "raw_value": 0x00,
                                    "physical_value": event_type_mapping.get(0x00, 0x00),
                                    "children": (

                                    ),
                                    "unit": None,
                                },
                            ),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
                {
                    "name": "eventWindowTime",
                    "length": 8,
                    "raw_value": 0x02,
                    "physical_value": "infiniteTimeToResponse",
                    "children": (),
                    "unit": None,
                },
            )
        ),
        (
            [0xC6, 0x05, 0x00, 0x08],
            (
                {
                    "name": "RSID",
                    "length": 8,
                    "raw_value": 0xC6,
                    "physical_value": "ResponseOnEvent",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x05,
                    "physical_value": 0x05,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 0,
                            "physical_value": "no",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "eventType",
                            "length": 7,
                            "raw_value": 0x05,
                            "physical_value": 0x05,
                            "children": (
                                {
                                    "name": "storageState",
                                    "length": 1,
                                    "raw_value": 0,
                                    "physical_value": "doNotStoreEvent",
                                    "children": (),
                                    "unit": None,
                                },
                                {
                                    "name": "event",
                                    "length": 6,
                                    "raw_value": 0x05,
                                    "physical_value": event_type_mapping.get(0x05, 0x05),
                                    "children": (

                                    ),
                                    "unit": None,
                                },
                            ),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
                {
                    "name": "numberOfIdentifiedEvents",
                    "length": 8,
                    "raw_value": 0x00,
                    "physical_value": 0,
                    "children": (),
                    "unit": None,
                },                {
                    "name": "eventWindowTime",
                    "length": 8,
                    "raw_value": 0x08,
                    "physical_value": "manufacturerTriggerEventWindowTime",
                    "children": (),
                    "unit": None,
                },
            )
        ),
        # LinkControl
        (
            [0x87, 0x81, 0x05],
            (
                {
                    "name": "SID",
                    "length": 8,
                    "raw_value": 0x87,
                    "physical_value": "LinkControl",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x81,
                    "physical_value": 0x81,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 1,
                            "physical_value": "yes",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "linkControlType",
                            "length": 7,
                            "raw_value": 0x01,
                            "physical_value": link_control_type_mapping.get(0x01, 0x01),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
                {
                    "name": "linkControlModeIdentifier",
                    "length": 8,
                    "raw_value": 0x05,
                    "physical_value": "PC115200Baud",
                    "children": (),
                    "unit": None,
                },
            )
        ),
        (
            [0xC7, 0x40],
            (
                {
                    "name": "RSID",
                    "length": 8,
                    "raw_value": 0xC7,
                    "physical_value": "LinkControl",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x40,
                    "physical_value": 0x40,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 0,
                            "physical_value": "no",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "linkControlType",
                            "length": 7,
                            "raw_value": 0x40,
                            "physical_value": link_control_type_mapping.get(0x40, 0x40),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
            )
        ),
        # ReadDataByIdentifier
        (
            [0x22, 0x01, 0x00, 0x01, 0x01, 0xF1, 0x85],
            (
                {
                    "name": "SID",
                    "length": 8,
                    "raw_value": 0x22,
                    "physical_value": "ReadDataByIdentifier",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "DID",
                    "length": 16,
                    "raw_value": (0x0100, 0x0101, 0xF185),
                    "physical_value": (did_mapping.get(0x0100, 0x0100),
                                       did_mapping.get(0x0101, 0x0101),
                                       did_mapping.get(0xF185, 0xF185)),
                    "children": ((), (), ()),
                    "unit": None,
                },
            )
        ),
        (
            [0x62, 0x01, 0x00, 0xB4, 0xC5, 0x01, 0x01, 0xFE],
            (
                {
                    "name": "RSID",
                    "length": 8,
                    "raw_value": 0x62,
                    "physical_value": "ReadDataByIdentifier",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "DID#1",
                    "length": 16,
                    "raw_value": 0x0100,
                    "physical_value": did_mapping.get(0x0100, 0x0100),
                    "children": (),
                    "unit": None,
                },
                {
                    'children': (
                        {
                            'children': ((), ()),
                            'length': 8,
                            'name': 'Param1',
                            'physical_value': (0xB4, 0xC5),
                            'raw_value': (0xB4, 0xC5),
                            'unit': None
                        },
                    ),
                    'length': 16,
                    'name': 'DID#1 data',
                    'physical_value': 0xB4C5,
                    'raw_value': 0xB4C5,
                    'unit': None
                },
                {
                    "name": "DID#2",
                    "length": 16,
                    "raw_value": 0x0101,
                    "physical_value": did_mapping.get(0x0101, 0x0101),
                    "children": (),
                    "unit": None,
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'a#1',
                            'physical_value': 0xF,
                            'raw_value': 0xF,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'a#2',
                            'physical_value': 0xE,
                            'raw_value': 0xE,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'DID#2 data',
                    'physical_value': 0xFE,
                    'raw_value': 0xFE,
                    'unit': None
                },
            )
        ),
        # ReadScalingDataByIdentifier
        (
            [0x24, 0x01, 0x01],
            (
                {
                    "name": "SID",
                    "length": 8,
                    "raw_value": 0x24,
                    "physical_value": "ReadScalingDataByIdentifier",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "DID",
                    "length": 16,
                    "raw_value": 0x0101,
                    "physical_value": did_mapping.get(0x0101, 0x0101),
                    "children": (),
                    "unit": None,
                },
            )
        ),
        (
            [0x64, 0x00, 0x00, 0x04],
            (
                {
                    "name": "RSID",
                    "length": 8,
                    "raw_value": 0x64,
                    "physical_value": "ReadScalingDataByIdentifier",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "DID",
                    "length": 16,
                    "raw_value": 0x0000,
                    "physical_value": did_mapping.get(0x0000, 0x0000),
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "scalingByte#1",
                    "length": 8,
                    "raw_value": 0x04,
                    "physical_value": 0x04,
                    "children": (
                        {
                            "name": "type",
                            "length": 4,
                            "raw_value": 0x0,
                            "physical_value": "unSignedNumeric",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "numberOfBytesOfParameter",
                            "length": 4,
                            "raw_value": 0x4,
                            "physical_value": 0x4,
                            "children": (),
                            "unit": "bytes",
                        },
                    ),
                    "unit": None,
                },
            )
        ),
        # DynamicallyDefineDataIdentifier
        (
            [0x2C, 0x03],
            (
                {
                    "name": "SID",
                    "length": 8,
                    "raw_value": 0x2C,
                    "physical_value": "DynamicallyDefineDataIdentifier",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x03,
                    "physical_value": 0x03,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 0,
                            "physical_value": "no",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "definitionType",
                            "length": 7,
                            "raw_value": 0x03,
                            "physical_value": definition_type_mapping.get(0x03, 0x03),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
            )
        ),
        (
            [0x6C, 0x81, 0xF1, 0x86],
            (
                {
                    "name": "RSID",
                    "length": 8,
                    "raw_value": 0x6C,
                    "physical_value": "DynamicallyDefineDataIdentifier",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x81,
                    "physical_value": 0x81,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 1,
                            "physical_value": "yes",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "definitionType",
                            "length": 7,
                            "raw_value": 0x01,
                            "physical_value": definition_type_mapping.get(0x01, 0x01),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
                {
                    "name": "dynamicallyDefinedDataIdentifier",
                    "length": 16,
                    "raw_value": 0xF186,
                    "physical_value": did_mapping.get(0xF186, 0xF186),
                    "children": (),
                    "unit": None,
                },
            )
        ),
        # WriteDataByIdentifier
        (
            [0x2E, 0x01, 0x00, 0xF0, 0xE1],
            (
                {
                    "name": "SID",
                    "length": 8,
                    "raw_value": 0x2E,
                    "physical_value": "WriteDataByIdentifier",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "DID",
                    "length": 16,
                    "raw_value": 0x0100,
                    "physical_value": did_mapping.get(0x0100, 0x0100),
                    "children": (),
                    "unit": None,
                },
                {
                    'children': (
                        {
                            'children': ((), ()),
                            'length': 8,
                            'name': 'Param1',
                            'physical_value': (0xF0, 0xE1),
                            'raw_value': (0xF0, 0xE1),
                            'unit': None
                        },
                    ),
                    'length': 16,
                    'name': 'DID data',
                    'physical_value': 0xF0E1,
                    'raw_value': 0xF0E1,
                    'unit': None
                },
            )
        ),
        (
            [0x6E, 0xE0, 0x00],
            (
                {
                    "name": "RSID",
                    "length": 8,
                    "raw_value": 0x6E,
                    "physical_value": "WriteDataByIdentifier",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "DID",
                    "length": 16,
                    "raw_value": 0xE000,
                    "physical_value": did_mapping.get(0xE000, 0xE000),
                    "children": (),
                    "unit": None,
                },
            )
        ),
        # ReadDTCInformation
        (
            [0x19, 0x03],
            (
                {
                    "name": "SID",
                    "length": 8,
                    "raw_value": 0x19,
                    "physical_value": "ReadDTCInformation",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x03,
                    "physical_value": 0x03,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 0,
                            "physical_value": "no",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "reportType",
                            "length": 7,
                            "raw_value": 0x03,
                            "physical_value": report_type_mapping.get(0x03, 0x03),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
            )
        ),
        (
            [0x59, 0x02, 0xFF],
            (
                {
                    "name": "RSID",
                    "length": 8,
                    "raw_value": 0x59,
                    "physical_value": "ReadDTCInformation",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x02,
                    "physical_value": 0x02,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 0,
                            "physical_value": "no",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "reportType",
                            "length": 7,
                            "raw_value": 0x02,
                            "physical_value": report_type_mapping.get(0x02, 0x02),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
                {
                    "name": "DTCStatusAvailabilityMask",
                    "length": 8,
                    "raw_value": 0xFF,
                    "physical_value": 0xFF,
                    "children": (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'warningIndicatorRequested',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testNotCompletedThisOperationCycle',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailedSinceLastClear',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testNotCompletedSinceLastClear',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'confirmedDTC',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'pendingDTC',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailedThisOperationCycle',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailed',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        }
                    ),
                    "unit": None,
                },
            )
        ),
        # InputOutputControlByIdentifier
        (
            [0x2F, 0x01, 0x01, 0x00],
            (
                {
                    "name": "SID",
                    "length": 8,
                    "raw_value": 0x2F,
                    "physical_value": "InputOutputControlByIdentifier",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "DID",
                    "length": 16,
                    "raw_value": 0x0101,
                    "physical_value": did_mapping.get(0x0101, 0x0101),
                    "children": (),
                    "unit": None,
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'inputOutputControlParameter',
                    'physical_value': "returnControlToECU",
                    'raw_value': 0x00,
                    'unit': None
                },
            )
        ),
        (
            [0x6F, 0x01, 0x01, 0x03, 0xA5],
            (
                {
                    "name": "RSID",
                    "length": 8,
                    "raw_value": 0x6F,
                    "physical_value": "InputOutputControlByIdentifier",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "DID",
                    "length": 16,
                    "raw_value": 0x0101,
                    "physical_value": did_mapping.get(0x0101, 0x0101),
                    "children": (),
                    "unit": None,
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'inputOutputControlParameter',
                    'physical_value': "shortTermAdjustment",
                    'raw_value': 0x03,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'a#1',
                            'physical_value': 0xA,
                            'raw_value': 0xA,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'a#2',
                            'physical_value': 0x5,
                            'raw_value': 0x5,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'controlState',
                    'physical_value': 0xA5,
                    'raw_value': 0xA5,
                    'unit': None
                }
            )
        ),
        # RoutineControl
        (
            [0x31, 0x40, 0x12, 0x34],
            (
                {
                    "name": "SID",
                    "length": 8,
                    "raw_value": 0x31,
                    "physical_value": "RoutineControl",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x40,
                    "physical_value": 0x40,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 0,
                            "physical_value": "no",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "routineControlType",
                            "length": 7,
                            "raw_value": 0x40,
                            "physical_value": routine_control_type_mapping.get(0x40, 0x40),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
                {
                    "name": "RID",
                    "length": 16,
                    "raw_value": 0x1234,
                    "physical_value": rid_mapping.get(0x1234, 0x1234),
                    "children": (),
                    "unit": None,
                },
            )
        ),
        (
            [0x71, 0x81, 0xFF, 0x00],
            (
                {
                    "name": "RSID",
                    "length": 8,
                    "raw_value": 0x71,
                    "physical_value": "RoutineControl",
                    "children": (),
                    "unit": None,
                },
                {
                    "name": "SubFunction",
                    "length": 8,
                    "raw_value": 0x81,
                    "physical_value": 0x81,
                    "children": (
                        {
                            "name": "suppressPosRspMsgIndicationBit",
                            "length": 1,
                            "raw_value": 1,
                            "physical_value": "yes",
                            "children": (),
                            "unit": None,
                        },
                        {
                            "name": "routineControlType",
                            "length": 7,
                            "raw_value": 0x01,
                            "physical_value": routine_control_type_mapping.get(0x01, 0x01),
                            "children": (),
                            "unit": None,
                        },
                    ),
                    "unit": None,
                },
                {
                    "name": "RID",
                    "length": 16,
                    "raw_value": 0xFF00,
                    "physical_value": rid_mapping.get(0xFF00, 0xFF00),
                    "children": (),
                    "unit": None,
                },
            )
        ),
    ])
    def test_decode_2(self, configurable_translator_2, payload, decoded_message):
        assert configurable_translator_2.decode(payload=payload) == decoded_message

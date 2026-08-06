import pytest
from mock import call, Mock, MagicMock, patch

from uds.translator.configurable_translator import ConfigurableTranslator, Translator, RequestSID

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

    def teardown_method(self):
        self._patcher_deepcopy.stop()

    # __init__

    @pytest.mark.parametrize("services", [
        [Mock()],
        [Mock(), Mock()],
    ])
    @patch(f"{SCRIPT_LOCATION}.Translator.__init__")
    def test_init__mandatory_args(self, mock_translator_init, services):
        mock_base = Mock(spec=Translator, services=services)
        assert ConfigurableTranslator.__init__(self.mock_translator, mock_base) is None
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
                == self.mock_translator.services_mapping[RequestSID.ResponseOnEvent].request_structure[0].children[1].values_mapping)

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

    def test_did_mapping__set(self):
        self.mock_translator.services_mapping[RequestSID.ReadDataByIdentifier].response_structure = 10 * [Mock()]
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
        assert (self.mock_translator.services_mapping[RequestSID.DynamicallyDefineDataIdentifier].request_structure[1].mapping
                == self.mock_translator._ConfigurableTranslator__conditional_dynamically_define_data_identifier_request)
        assert (self.mock_translator.services_mapping[RequestSID.DynamicallyDefineDataIdentifier].response_structure[1].mapping
                == self.mock_translator._ConfigurableTranslator__conditional_dynamically_define_data_identifier_response)
        # InputOutputControlByIdentifier
        assert (self.mock_translator.services_mapping[RequestSID.InputOutputControlByIdentifier].request_structure[0].values_mapping
                == mock_value)
        assert (self.mock_translator.services_mapping[RequestSID.InputOutputControlByIdentifier].response_structure[0].values_mapping
                == mock_value)
        # ReadDTCInformation
        assert (self.mock_translator.services_mapping[RequestSID.ReadDTCInformation].response_structure[1].mapping
                == self.mock_translator._ConfigurableTranslator__conditional_read_dtc_information_response)
        # ResponseOnEvent
        assert (self.mock_translator.services_mapping[RequestSID.ResponseOnEvent].request_structure[1].mapping
                == self.mock_translator._ConfigurableTranslator__conditional_response_on_event_request)
        assert (self.mock_translator.services_mapping[RequestSID.ResponseOnEvent].response_structure[1].mapping
                == self.mock_translator._ConfigurableTranslator__conditional_response_on_event_response)

    # did_data_mapping

    def test_did_data_mapping__get(self):
        self.mock_translator._ConfigurableTranslator__did_data_mapping = Mock()
        assert (ConfigurableTranslator.did_data_mapping.fget(self.mock_translator)
                == self.mock_translator._ConfigurableTranslator__did_data_mapping)

    def test_did_data_mapping__set(self):
        mock_value = Mock()
        assert ConfigurableTranslator.did_data_mapping.fset(self.mock_translator, mock_value) is None
        assert self.mock_translator._ConfigurableTranslator__did_data_mapping == mock_value
        # TODO: more asserts
        
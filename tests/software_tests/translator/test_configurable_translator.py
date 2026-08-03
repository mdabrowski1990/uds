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

    # rid_mapping

    def test_rid_mapping__get(self):
        assert (ConfigurableTranslator.rid_mapping.fget(self.mock_translator)
                == self.mock_translator.services_mapping[RequestSID.RoutineControl].request_structure[1].values_mapping)

    def test_rid_mapping__set(self):
        mock_value = {Mock(): Mock()}
        assert ConfigurableTranslator.rid_mapping.fset(self.mock_translator, mock_value) is None
        assert (self.mock_translator.services_mapping[RequestSID.RoutineControl].request_structure[1].values_mapping
                == mock_value)

    # did_mapping

    def test_did_mapping__get(self):
        assert (ConfigurableTranslator.did_mapping.fget(self.mock_translator)
                == self.mock_translator.services_mapping[RequestSID.ReadDataByIdentifier].request_structure[0].values_mapping)
        
    def test_did_mapping__set(self):
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

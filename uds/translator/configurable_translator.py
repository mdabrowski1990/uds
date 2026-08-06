"""Implementation of translator configurable through typical diagnostic parameters."""

__all__ = ["ConfigurableTranslator"]

from copy import deepcopy
from typing import Callable, Mapping

from uds.message import RequestSID
from uds.utilities import DID_BIT_LENGTH, REPEATED_DATA_RECORDS_NUMBER

from .data_record import (
    AbstractDataRecord,
    ConditionalFormulaDataRecord,
    ConditionalMappingDataRecord,
    MappingDataRecord,
    MessageStructureAlias,
    RawDataRecord,
)
from .data_record_definitions import (
    ADDRESS_AND_LENGTH_FORMAT_IDENTIFIER,
    CONDITIONAL_DATA_FROM_MEMORY,
    DID_COUNT_RECORDS,
    DID_MEMORY_SIZE,
    DTC_AND_STATUS,
    DTC_STORED_DATA_RECORD_NUMBERS_LIST,
    DTCS_AND_STATUSES_LIST,
    INPUT_OUTPUT_CONTROL_PARAMETER,
    MEMORY_SELECTION,
    OPTIONAL_DTC_SNAPSHOT_RECORDS_NUMBERS_LIST,
    POSITION_IN_DID,NUMBER_OF_ACTIVATED_EVENTS, RESERVED_BIT
)
from .data_record_definitions.formula import get_service_to_respond, get_event_type_record_01
from .service import Service
from .translator import Translator
from .translator_definitions import BASE_TRANSLATOR


class ConfigurableTranslator(Translator):
    """
    Simplified translator for UDS messages that assumes typical messages structures.

    Features:
     - configuration with diagnostic parameters and messages structures
     - building diagnostic messages (requests, positive and negative responses)
     - extracting meaningful information from diagnostic messages payload

    .. note:: It contains core features but in advances cases (where message structure has to be adapted)
        :class:`~uds.translator.translator.Translator` shall be directly used instead.
    """

    def __init__(self,
                 base: Translator = BASE_TRANSLATOR,
                 *,
                 diagnostic_session_type_mapping: None | Mapping[int, str] = None,
                 reset_type_mapping: None | Mapping[int, str] = None,
                 report_type_mapping: None | Mapping[int, str] = None,
                 security_access_type_mapping: None | Mapping[int, str] = None,
                 control_type_type_mapping: None | Mapping[int, str] = None,
                 authentication_task_mapping: None | Mapping[int, str] = None,
                 definition_type_mapping: None | Mapping[int, str] = None,
                 routine_control_type_mapping: None | Mapping[int, str] = None,
                 zero_subfunction_mapping: None | Mapping[int, str] = None,
                 timing_parameter_access_type_mapping: None | Mapping[int, str] = None,
                 dtc_setting_type_mapping: None | Mapping[int, str] = None,
                 event_type_mapping: None | Mapping[int, str] = None,
                 link_control_type_mapping: None | Mapping[int, str] = None,
                 rid_mapping: None | Mapping[int, str] = None,
                 did_mapping: None | Mapping[int, str] = None,
                 did_data_mapping: None | Mapping[int, MessageStructureAlias] = None) -> None:
        """
        Reconfigure a translator.

        :param base: Translator to use as a base.
        :param diagnostic_session_type_mapping: New value mapping for `diagnosticSessionType` DataRecord of
            :ref:`DiagnosticSessionControl <knowledge-base-service-diagnostic-session-control>` service.
            None to keep mapping unchanged.
        :param reset_type_mapping: New value mapping for `resetType` DataRecord of
            :ref:`ECUReset <knowledge-base-service-ecu-reset>` service.
            None to keep mapping unchanged.
        :param report_type_mapping: New value mapping for `reportType` DataRecord of
            :ref:`ReadDTCInformation <knowledge-base-service-read-dtc-information>` service.
            None to keep mapping unchanged.
        :param security_access_type_mapping: New value mapping for `securityAccessType` DataRecord of
            :ref:`SecurityAccess <knowledge-base-service-security-access>` service.
            None to keep mapping unchanged.
        :param control_type_type_mapping: New value mapping for `controlType` DataRecord of
            :ref:`CommunicationControl <knowledge-base-service-communication-control>` service.
            None to keep mapping unchanged.
        :param authentication_task_mapping: New value mapping for `authenticationTask` DataRecord of
            :ref:`Authentication <knowledge-base-service-authentication>` service.
            None to keep mapping unchanged.
        :param definition_type_mapping: New value mapping for `definitionType` DataRecord of
            :ref:`DynamicallyDefineDataIdentifier <knowledge-base-service-dynamically-define-data-identifier>` service.
            None to keep mapping unchanged.
        :param routine_control_type_mapping: New value mapping for `routineControlType` DataRecord of
            :ref:`RoutineControl <knowledge-base-service-routine-control>` service.
            None to keep mapping unchanged.
        :param zero_subfunction_mapping: New value mapping for `zeroSubFunction` DataRecord of
            :ref:`TesterPresent <knowledge-base-service-tester-present>` service.
            None to keep mapping unchanged.
        :param timing_parameter_access_type_mapping: New value mapping for `timingParameterAccessType` DataRecord of
            :ref:`AccessTimingParameter <knowledge-base-service-access-timing-parameter>` service.
            None to keep mapping unchanged.
        :param dtc_setting_type_mapping: New value mapping for `DTCSettingType` DataRecord of
            :ref:`ControlDTCSetting <knowledge-base-service-control-dtc-setting>` service.
            None to keep mapping unchanged.
        :param event_type_mapping: New value mapping for `eventType` DataRecord of
            :ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` service.
            None to keep mapping unchanged.
        :param link_control_type_mapping: New value mapping for `linkControlType` DataRecord of
            :ref:`LinkControl <knowledge-base-service-link-control>` service.
            None to keep mapping unchanged.
        :param rid_mapping: Value to name mapping for :ref:`RIDs <knowledge-base-rid>`.
        :param did_mapping: Value to name mapping for :ref:`DIDs <knowledge-base-did>`.
        :param did_data_mapping: Value to data structure mapping for :ref:`DIDs <knowledge-base-did>`.
        """
        # create copy of base Translator
        super().__init__(services=deepcopy(base.services))
        # adapt SubFunctions
        if diagnostic_session_type_mapping is not None:
            self.diagnostic_session_type_mapping = diagnostic_session_type_mapping
        if reset_type_mapping is not None:
            self.reset_type_mapping = reset_type_mapping
        if report_type_mapping is not None:
            self.report_type_mapping = report_type_mapping
        if security_access_type_mapping is not None:
            self.security_access_type_mapping = security_access_type_mapping
        if control_type_type_mapping is not None:
            self.control_type_type_mapping = control_type_type_mapping
        if authentication_task_mapping is not None:
            self.authentication_task_mapping = authentication_task_mapping
        if routine_control_type_mapping is not None:
            self.routine_control_type_mapping = routine_control_type_mapping
        if definition_type_mapping is not None:
            self.definition_type_mapping = definition_type_mapping
        if zero_subfunction_mapping is not None:
            self.zero_subfunction_mapping = zero_subfunction_mapping
        if timing_parameter_access_type_mapping is not None:
            self.timing_parameter_access_type_mapping = timing_parameter_access_type_mapping
        if dtc_setting_type_mapping is not None:
            self.dtc_setting_type_mapping = dtc_setting_type_mapping
        if event_type_mapping is not None:
            self.event_type_mapping = event_type_mapping
        if link_control_type_mapping is not None:
            self.link_control_type_mapping = link_control_type_mapping
        # adapt RIDs
        if rid_mapping is not None:
            self.rid_mapping = rid_mapping
        # adapt DIDs
        if did_mapping is not None:
            self.did_mapping = did_mapping
        self.did_data_mapping = did_data_mapping

    @property
    def diagnostic_session_type_mapping(self) -> None | Mapping[int, str]:
        """Get diagnosticSessionType (SubFunction of DiagnosticSessionControl) value to name mapping."""
        diagnostic_session_control = self.services_mapping.get(RequestSID.DiagnosticSessionControl, None)
        if diagnostic_session_control is None:
            return None
        sub_function: MappingDataRecord = diagnostic_session_control.request_structure[0].children[1]
        return sub_function.values_mapping

    @diagnostic_session_type_mapping.setter
    def diagnostic_session_type_mapping(self, value: Mapping[int, str]) -> None:
        """
        Set diagnosticSessionType (SubFunction of DiagnosticSessionControl) value to name mapping.

        :param value: Mapping value to set.
        """
        diagnostic_session_control = self.services_mapping[RequestSID.DiagnosticSessionControl]
        diagnostic_session_control.request_structure[0].children[1].values_mapping = value
        diagnostic_session_control.response_structure[0].children[1].values_mapping = value

    @property
    def reset_type_mapping(self) -> None | Mapping[int, str]:
        """Get resetType (SubFunction of ECUReset) value to name mapping."""
        ecu_reset = self.services_mapping.get(RequestSID.ECUReset, None)
        if ecu_reset is None:
            return None
        sub_function: MappingDataRecord = ecu_reset.request_structure[0].children[1]
        return sub_function.values_mapping

    @reset_type_mapping.setter
    def reset_type_mapping(self, value: Mapping[int, str]) -> None:
        """
        Set resetType (SubFunction of ECUReset) value to name mapping.

        :param value: Mapping value to set.
        """
        ecu_reset = self.services_mapping[RequestSID.ECUReset]
        ecu_reset.request_structure[0].children[1].values_mapping = value
        ecu_reset.response_structure[0].children[1].values_mapping = value

    @property
    def report_type_mapping(self) -> None | Mapping[int, str]:
        """Get reportType (SubFunction of ReadDTCInformation) value to name mapping."""
        read_dtc_information = self.services_mapping.get(RequestSID.ReadDTCInformation, None)
        if read_dtc_information is None:
            return None
        sub_function: MappingDataRecord = read_dtc_information.request_structure[0].children[1]
        return sub_function.values_mapping

    @report_type_mapping.setter
    def report_type_mapping(self, value: Mapping[int, str]) -> None:
        """
        Set reportType (SubFunction of ReadDTCInformation) value to name mapping.

        :param value: Mapping value to set.
        """
        read_dtc_information = self.services_mapping[RequestSID.ReadDTCInformation]
        read_dtc_information.request_structure[0].children[1].values_mapping = value
        read_dtc_information.response_structure[0].children[1].values_mapping = value
        response_on_event = self.services_mapping.get(RequestSID.ResponseOnEvent, None)
        if response_on_event is not None:
            subfunction_08_request_continuation = response_on_event.request_structure[1].mapping.get(0x08, None)
            if subfunction_08_request_continuation is not None:
                subfunction_08_request_continuation[1].children[1].values_mapping = value
            subfunction_09_request_continuation = response_on_event.request_structure[1].mapping.get(0x09, None)
            if subfunction_09_request_continuation is not None:
                subfunction_09_request_continuation[1].children[2].values_mapping = value
            subfunction_08_response_continuation = response_on_event.response_structure[1].mapping.get(0x08, None)
            if subfunction_08_response_continuation is not None:
                subfunction_08_response_continuation[2].children[1].values_mapping = value
            subfunction_09_response_continuation = response_on_event.response_structure[1].mapping.get(0x09, None)
            if subfunction_09_response_continuation is not None:
                subfunction_09_response_continuation[2].children[2].values_mapping = value

    @property
    def security_access_type_mapping(self) -> None | Mapping[int, str]:
        """Get securityAccessType (SubFunction of SecurityAccess) value to name mapping."""
        security_access = self.services_mapping.get(RequestSID.SecurityAccess, None)
        if security_access is None:
            return None
        sub_function: MappingDataRecord = security_access.request_structure[0].children[1]
        return sub_function.values_mapping

    @security_access_type_mapping.setter
    def security_access_type_mapping(self, value: Mapping[int, str]) -> None:
        """
        Set securityAccessType (SubFunction of SecurityAccess) value to name mapping.

        :param value: Mapping value to set.
        """
        security_access = self.services_mapping[RequestSID.SecurityAccess]
        security_access.request_structure[0].children[1].values_mapping = value
        security_access.response_structure[0].children[1].values_mapping = value

    @property
    def control_type_type_mapping(self) -> None | Mapping[int, str]:
        """Get controlType (SubFunction of CommunicationControl) value to name mapping."""
        communication_control = self.services_mapping.get(RequestSID.CommunicationControl, None)
        if communication_control is None:
            return None
        sub_function: MappingDataRecord = communication_control.request_structure[0].children[1]
        return sub_function.values_mapping

    @control_type_type_mapping.setter
    def control_type_type_mapping(self, value: Mapping[int, str]) -> None:
        """
        Set controlType (SubFunction of CommunicationControl) value to name mapping.

        :param value: Mapping value to set.
        """
        communication_control = self.services_mapping[RequestSID.CommunicationControl]
        communication_control.request_structure[0].children[1].values_mapping = value
        communication_control.response_structure[0].children[1].values_mapping = value

    @property
    def authentication_task_mapping(self) -> None | Mapping[int, str]:
        """Get authenticationTask (SubFunction of Authentication) value to name mapping."""
        authentication = self.services_mapping.get(RequestSID.Authentication, None)
        if authentication is None:
            return None
        sub_function: MappingDataRecord = authentication.request_structure[0].children[1]
        return sub_function.values_mapping

    @authentication_task_mapping.setter
    def authentication_task_mapping(self, value: Mapping[int, str]) -> None:
        """
        Set authenticationTask (SubFunction of Authentication) value to name mapping.

        :param value: Mapping value to set.
        """
        authentication = self.services_mapping[RequestSID.Authentication]
        authentication.request_structure[0].children[1].values_mapping = value
        authentication.response_structure[0].children[1].values_mapping = value

    @property
    def definition_type_mapping(self) -> None | Mapping[int, str]:
        """Get definitionType (SubFunction of DynamicallyDefineDataIdentifier) value to name mapping."""
        dynamically_define_data_identifier = self.services_mapping.get(RequestSID.DynamicallyDefineDataIdentifier, None)
        if dynamically_define_data_identifier is None:
            return None
        sub_function: MappingDataRecord = dynamically_define_data_identifier.request_structure[0].children[1]
        return sub_function.values_mapping

    @definition_type_mapping.setter
    def definition_type_mapping(self, value: Mapping[int, str]) -> None:
        """
        Set definitionType (SubFunction of DynamicallyDefineDataIdentifier) value to name mapping.

        :param value: Mapping value to set.
        """
        dynamically_define_data_identifier = self.services_mapping[RequestSID.DynamicallyDefineDataIdentifier]
        dynamically_define_data_identifier.request_structure[0].children[1].values_mapping = value
        dynamically_define_data_identifier.response_structure[0].children[1].values_mapping = value

    @property
    def routine_control_type_mapping(self) -> None | Mapping[int, str]:
        """Get routineControlType (SubFunction of RoutineControl) value to name mapping."""
        routine_control = self.services_mapping.get(RequestSID.RoutineControl, None)
        if routine_control is None:
            return None
        sub_function: MappingDataRecord = routine_control.request_structure[0].children[1]
        return sub_function.values_mapping

    @routine_control_type_mapping.setter
    def routine_control_type_mapping(self, value: Mapping[int, str]) -> None:
        """
        Set routineControlType (SubFunction of RoutineControl) value to name mapping.

        :param value: Mapping value to set.
        """
        routine_control = self.services_mapping[RequestSID.RoutineControl]
        routine_control.request_structure[0].children[1].values_mapping = value
        routine_control.response_structure[0].children[1].values_mapping = value

    @property
    def zero_subfunction_mapping(self) -> None | Mapping[int, str]:
        """Get zeroSubFunction (SubFunction of TesterPresent) value to name mapping."""
        tester_present = self.services_mapping.get(RequestSID.TesterPresent, None)
        if tester_present is None:
            return None
        sub_function: MappingDataRecord = tester_present.request_structure[0].children[1]
        return sub_function.values_mapping

    @zero_subfunction_mapping.setter
    def zero_subfunction_mapping(self, value: Mapping[int, str]) -> None:
        """
        Set zeroSubFunction (SubFunction of TesterPresent) value to name mapping.

        :param value: Mapping value to set.
        """
        tester_present = self.services_mapping[RequestSID.TesterPresent]
        tester_present.request_structure[0].children[1].values_mapping = value
        tester_present.response_structure[0].children[1].values_mapping = value

    @property
    def timing_parameter_access_type_mapping(self) -> None | Mapping[int, str]:
        """Get timingParameterAccessType (SubFunction of AccessTimingParameter) value to name mapping."""
        access_timing_parameter = self.services_mapping.get(RequestSID.AccessTimingParameter, None)
        if access_timing_parameter is None:
            return None
        sub_function: MappingDataRecord = access_timing_parameter.request_structure[0].children[1]
        return sub_function.values_mapping

    @timing_parameter_access_type_mapping.setter
    def timing_parameter_access_type_mapping(self, value: Mapping[int, str]) -> None:
        """
        Set timingParameterAccessType (SubFunction of AccessTimingParameter) value to name mapping.

        :param value: Mapping value to set.
        """
        access_timing_parameter = self.services_mapping[RequestSID.AccessTimingParameter]
        access_timing_parameter.request_structure[0].children[1].values_mapping = value
        access_timing_parameter.response_structure[0].children[1].values_mapping = value

    @property
    def dtc_setting_type_mapping(self) -> None | Mapping[int, str]:
        """Get DTCSettingType (SubFunction of ControlDTCSetting) value to name mapping."""
        control_dtc_setting = self.services_mapping.get(RequestSID.ControlDTCSetting, None)
        if control_dtc_setting is None:
            return None
        sub_function: MappingDataRecord = control_dtc_setting.request_structure[0].children[1]
        return sub_function.values_mapping

    @dtc_setting_type_mapping.setter
    def dtc_setting_type_mapping(self, value: Mapping[int, str]) -> None:
        """
        Set DTCSettingType (SubFunction of ControlDTCSetting) value to name mapping.

        :param value: Mapping value to set.
        """
        control_dtc_setting = self.services_mapping[RequestSID.ControlDTCSetting]
        control_dtc_setting.request_structure[0].children[1].values_mapping = value
        control_dtc_setting.response_structure[0].children[1].values_mapping = value

    @property
    def event_type_mapping(self) -> None | Mapping[int, str]:
        """
        Get eventType (SubFunction of ResponseOnEvent) value to name mapping.

        .. warning:: Mapping for `event` (mask 0x3F) part of the `eventType` SubFunction
            (:ref:`ResponseOnEvent <knowledge-base-service-response-on-event>`) is returned.
        """
        response_on_event = self.services_mapping.get(RequestSID.ResponseOnEvent, None)
        if response_on_event is None:
            return None
        sub_function: MappingDataRecord = response_on_event.request_structure[0].children[1]
        return sub_function.values_mapping

    @event_type_mapping.setter
    def event_type_mapping(self, value: Mapping[int, str]) -> None:
        """
        Set eventType (SubFunction of ResponseOnEvent) value to name mapping.

        .. warning:: Mapping for `event` (mask 0x3F) part of the `eventType` SubFunction
            (:ref:`ResponseOnEvent <knowledge-base-service-response-on-event>`) is set.

        :param value: Mapping value to set.
        """
        response_on_event = self.services_mapping[RequestSID.ResponseOnEvent]
        response_on_event.request_structure[0].children[1].children[1].values_mapping = value
        response_on_event.response_structure[0].children[1].children[1].values_mapping = value

    @property
    def link_control_type_mapping(self) -> None | Mapping[int, str]:
        """Get linkControlType (SubFunction of LinkControl) value to name mapping."""
        link_control = self.services_mapping.get(RequestSID.LinkControl, None)
        if link_control is None:
            return None
        sub_function: MappingDataRecord = link_control.request_structure[0].children[1]
        return sub_function.values_mapping

    @link_control_type_mapping.setter
    def link_control_type_mapping(self, value: Mapping[int, str]) -> None:
        """
        Set linkControlType (SubFunction of LinkControl) value to name mapping.

        :param value: Mapping value to set.
        """
        link_control = self.services_mapping[RequestSID.LinkControl]
        link_control.request_structure[0].children[1].values_mapping = value
        link_control.response_structure[0].children[1].values_mapping = value

    @property
    def rid_mapping(self) -> None | Mapping[int, str]:
        """Get :ref:`Routine Identifier (RID) <knowledge-base-rid>` value to name mapping."""
        routine_control = self.services_mapping.get(RequestSID.RoutineControl, None)
        if routine_control is None:
            return None
        rid: MappingDataRecord = routine_control.request_structure[1]
        return rid.values_mapping

    @rid_mapping.setter
    def rid_mapping(self, value: Mapping[int, str]) -> None:
        """
        Set :ref:`Routine Identifier (RID) <knowledge-base-rid>` value to name mapping.

        :param value: Mapping value to set.
        """
        routine_control = self.services_mapping[RequestSID.RoutineControl]
        rid: MappingDataRecord = routine_control.request_structure[1]
        rid.values_mapping = value

    @property
    def did_mapping(self) -> None | Mapping[int, str]:
        """Get :ref:`Data Identifier (DID) <knowledge-base-did>` value to name mapping."""
        read_data_by_identifier = self.services_mapping.get(RequestSID.ReadDataByIdentifier, None)
        if read_data_by_identifier is None:
            return None
        did: MappingDataRecord = read_data_by_identifier.request_structure[0]
        return did.values_mapping

    @did_mapping.setter
    def did_mapping(self, value: Mapping[int, str]) -> None:
        """
        Set :ref:`Data Identifier (DID) <knowledge-base-did>` value to name mapping.

        :param value: Mapping value to set.
        """
        # ReadDataByIdentifier
        read_data_by_identifier = self.services_mapping[RequestSID.ReadDataByIdentifier]
        read_data_by_identifier.request_structure[0].values_mapping = value  # did_mapping value is stored here
        for did in read_data_by_identifier.response_structure[::2]:
            did.values_mapping = value
        # WriteDataByIdentifier
        write_data_by_identifier = self.services_mapping[RequestSID.WriteDataByIdentifier]  # TODO: handle missing services
        write_data_by_identifier.request_structure[0].values_mapping = value
        write_data_by_identifier.response_structure[0].values_mapping = value
        # ReadScalingDataByIdentifier
        read_scaling_data_by_identifier = self.services_mapping[RequestSID.ReadScalingDataByIdentifier]  # TODO: handle missing services
        read_scaling_data_by_identifier.request_structure[0].values_mapping = value
        read_scaling_data_by_identifier.response_structure[0].values_mapping = value
        # DynamicallyDefineDataIdentifier
        dynamically_define_data_identifier = self.services_mapping.get(RequestSID.DynamicallyDefineDataIdentifier, None)
        if dynamically_define_data_identifier is not None:
            dynamically_define_data_identifier.request_structure[1].mapping[0x01][0].values_mapping = value
            dynamically_define_data_identifier.request_structure[1].mapping[0x01][1].children[0].values_mapping = value
            dynamically_define_data_identifier.request_structure[1].mapping[0x02][0].values_mapping = value
            dynamically_define_data_identifier.request_structure[1].mapping[0x03][0].values_mapping = value
            dynamically_define_data_identifier.response_structure[1].mapping[0x01][0].values_mapping = value
            dynamically_define_data_identifier.response_structure[1].mapping[0x02][0].values_mapping = value
            dynamically_define_data_identifier.response_structure[1].mapping[0x03][0].values_mapping = value
        # InputOutputControlByIdentifier
        input_output_control_by_identifier = self.services_mapping[RequestSID.InputOutputControlByIdentifier]  # TODO: handle missing services
        input_output_control_by_identifier.request_structure[0].values_mapping = value
        input_output_control_by_identifier.response_structure[0].values_mapping = value
        # ReadDTCInformation
        read_dtc_information = self.services_mapping[RequestSID.ReadDTCInformation]  # TODO: handle missing services
        read_dtc_information.response_structure[1].mapping = self.__conditional_read_dtc_information_response  # TODO: review
        # ResponseOnEvent
        response_on_event = self.services_mapping[RequestSID.ResponseOnEvent]  # TODO: handle missing services
        response_on_event.request_structure[1].mapping = self.__conditional_response_on_event_request  # TODO: review
        response_on_event.response_structure[1].mapping = self.__conditional_response_on_event_response  # TODO: review

    @property
    def did_data_mapping(self) -> None | Mapping[int, MessageStructureAlias]:
        """
        Get :ref:`Data Identifier (DID) <knowledge-base-did>` value to data structure mapping.

        .. warning:: None value means, it was never set and mapping from base Translator is used.
        """
        return self.__did_data_mapping

    @did_data_mapping.setter
    def did_data_mapping(self, value: Mapping[int, MessageStructureAlias]) -> None:
        """
        Get :ref:`Data Identifier (DID) <knowledge-base-did>` value to data structure mapping.

        :param value: Mapping value to set.
        """
        # TODO: update
        # self.services_mapping[RequestSID.ReadDTCInformation].response_structure[1].mapping \
        #     = self.__conditional_read_dtc_information_response
        # self.services_mapping[RequestSID.DynamicallyDefineDataIdentifier].request_structure[1].mapping \
        #     = self.__conditional_dynamically_define_data_identifier_request
        # self.services_mapping[RequestSID.DynamicallyDefineDataIdentifier].response_structure[1].mapping \
        #     = self.__conditional_dynamically_define_data_identifier_response
        # self.services_mapping[RequestSID.ResponseOnEvent].request_structure[1].mapping \
        #     = self.__conditional_response_on_event_request
        # self.services_mapping[RequestSID.ResponseOnEvent].response_structure[1].mapping \
        #     = self.__conditional_response_on_event_response
        # self.services_mapping[RequestSID.ReadDataByIdentifier].request_structure[0].values_mapping = self.did_mapping
        # self.services_mapping[RequestSID.ReadDataByIdentifier].response_structure = self.__dids
        # self.services_mapping[RequestSID.WriteDataByIdentifier].request_structure = (self.__did, self.__get_did_data())
        # self.services_mapping[RequestSID.WriteDataByIdentifier].response_structure[0].values_mapping = self.did_mapping
        # self.services_mapping[RequestSID.InputOutputControlByIdentifier].request_structure[0].values_mapping \
        #     = self.did_mapping
        # self.services_mapping[RequestSID.InputOutputControlByIdentifier].request_structure[1].formula \
        #     = self.__get_input_output_control_by_identifier_request
        # self.services_mapping[RequestSID.InputOutputControlByIdentifier].response_structure[0].values_mapping \
        #     = self.did_mapping
        # self.services_mapping[RequestSID.InputOutputControlByIdentifier].request_structure[1].formula \
        #     = self.__get_input_output_control_by_identifier_response
        # self.services_mapping[RequestSID.ReadScalingDataByIdentifier].request_structure[0].values_mapping \
        #     = self.did_mapping
        # self.services_mapping[RequestSID.ReadScalingDataByIdentifier].response_structure[0].values_mapping \
        #     = self.did_mapping
        self.__did_data_mapping = value

    # TODO: remove what is not needed

    # @property
    # def __did(self) -> MappingDataRecord:
    #     return MappingDataRecord(name="DID",
    #                              length=DID_BIT_LENGTH,
    #                              values_mapping=self.did_mapping)
    #
    # @property
    # def __dids(self) -> tuple[MappingDataRecord | ConditionalFormulaDataRecord, ...]:
    #     return (*self.__get_did_record(did_count=1, record_number=None, optional=False),
    #             *self.__get_did_record(did_count=REPEATED_DATA_RECORDS_NUMBER, record_number=None, optional=True)[2:])
    #
    # @property
    # def __multiple_did(self) -> MappingDataRecord:
    #     return MappingDataRecord(name="DID",
    #                              length=DID_BIT_LENGTH,
    #                              values_mapping=self.did_mapping,
    #                              min_occurrences=1,
    #                              max_occurrences=None)
    #
    # @property
    # def __dynamically_defined_did(self) -> MappingDataRecord:
    #     return MappingDataRecord(name="dynamicallyDefinedDataIdentifier",
    #                              length=DID_BIT_LENGTH,
    #                              values_mapping=self.did_mapping)
    #
    # @property
    # def __optional_dynamically_defined_did(self) -> MappingDataRecord:
    #     return MappingDataRecord(name="dynamicallyDefinedDataIdentifier",
    #                              length=DID_BIT_LENGTH,
    #                              values_mapping=self.did_mapping,
    #                              min_occurrences=0,
    #                              max_occurrences=1)
    #
    # @property
    # def __source_did(self) -> MappingDataRecord:
    #     return MappingDataRecord(name="sourceDataIdentifier",
    #                              length=DID_BIT_LENGTH,
    #                              values_mapping=self.did_mapping)
    #
    # @property
    # def __data_from_did(self) -> RawDataRecord:
    #     return RawDataRecord(name="Data from DID",
    #                          length=32,
    #                          children=(
    #                              self.__source_did,
    #                              POSITION_IN_DID,
    #                              DID_MEMORY_SIZE
    #                          ),
    #                          min_occurrences=1,
    #                          max_occurrences=None)
    #
    # @property
    # def __event_type(self) -> RawDataRecord:
    #     response_on_event = self.services_mapping[RequestSID.ResponseOnEvent]
    #     return response_on_event.request_structure[0].children[1]
    #
    # @property
    # def __event_window(self) -> MappingDataRecord:
    #     response_on_event = self.services_mapping[RequestSID.ResponseOnEvent]
    #     return response_on_event.request_structure[1][0x00][0]
    #
    # @property
    # def __conditional_control_state(self) -> ConditionalFormulaDataRecord:
    #     return self.__get_did_data(name="controlState")
    #
    # @property
    # def __conditional_optional_control_enable_mask(self) -> ConditionalFormulaDataRecord:
    #     return self.__get_did_data_mask(name="controlEnableMask", optional=True)
    #
    # @property
    # def __did_records(self) -> tuple[ConditionalFormulaDataRecord, ...]:
    #     return tuple(ConditionalFormulaDataRecord(formula=self.__get_did_records_formula(record_number + 1))
    #                  for record_number in range(REPEATED_DATA_RECORDS_NUMBER))
    #
    # @property
    # def __dtc_snapshot_records(self) -> tuple[MappingDataRecord | RawDataRecord | ConditionalFormulaDataRecord, ...]:
    #     return tuple(item
    #                  for snapshot_record in zip(OPTIONAL_DTC_SNAPSHOT_RECORDS_NUMBERS_LIST,
    #                                             DID_COUNT_RECORDS,
    #                                             self.__did_records)
    #                  for item in snapshot_record)
    #
    # @property
    # def __dtc_stored_data_records(self) -> tuple[MappingDataRecord | RawDataRecord | ConditionalFormulaDataRecord, ...]:
    #     return tuple(item
    #                  for stored_data_record in zip(DTC_STORED_DATA_RECORD_NUMBERS_LIST,
    #                                                DTCS_AND_STATUSES_LIST,
    #                                                DID_COUNT_RECORDS,
    #                                                self.__did_records)
    #                  for item in stored_data_record)
    #
    # @property
    # def __conditional_activated_events(self) -> ConditionalFormulaDataRecord:
    #     return ConditionalFormulaDataRecord(formula=self.__get_activated_events)
    #
    # @property
    # def __conditional_read_dtc_information_response(self) -> Mapping[int, MessageStructureAlias]:
    #     read_dtc_information = self.services_mapping[RequestSID.ReadDTCInformation]
    #     conditional_response_mapping = dict(read_dtc_information.response_structure[1].mapping)
    #     conditional_response_mapping[0x04] = (DTC_AND_STATUS, *self.__dtc_snapshot_records)
    #     conditional_response_mapping[0x05] = (DTC_AND_STATUS, *self.__dtc_stored_data_records)
    #     conditional_response_mapping[0x18] = (MEMORY_SELECTION, DTC_AND_STATUS, *self.__dtc_snapshot_records)
    #     return conditional_response_mapping
    #
    #
    # @property
    # def __conditional_response_on_event_request(self) -> Mapping[int, MessageStructureAlias]:
    #     response_on_event = self.services_mapping[RequestSID.ResponseOnEvent]
    #     conditional_request_mapping = dict(response_on_event.request_structure[1].mapping)
    #     conditional_request_mapping[0x03][1].children[0].values_mapping = self.did_mapping
    #     conditional_request_mapping[0x07][1].children[0].values_mapping = self.did_mapping
    #     return conditional_request_mapping
    #
    # @property
    # def __conditional_response_on_event_response(self) -> Mapping[int, MessageStructureAlias]:
    #     response_on_event = self.services_mapping[RequestSID.ResponseOnEvent]
    #     conditional_response_mapping = dict(response_on_event.response_structure[1].mapping)
    #     conditional_response_mapping[0x03][2].children[0].values_mapping = self.did_mapping
    #     conditional_response_mapping[0x04] = (NUMBER_OF_ACTIVATED_EVENTS, self.__conditional_activated_events)
    #     conditional_response_mapping[0x07][2].children[0].values_mapping = self.did_mapping
    #     return conditional_response_mapping
    #
    # @staticmethod
    # def __adapt_subfunction(service: Service, subfunction_mapping: Mapping[int, str]) -> Service:
    #     request_subfunction: MappingDataRecord = service.request_structure[0].children[1]
    #     response_subfunction: MappingDataRecord = service.response_structure[0].children[1]
    #     if service.request_sid == RequestSID.ResponseOnEvent:
    #         # `event` DataRecord is updated instead of `eventType`
    #         request_subfunction.children[1].values_mapping = response_subfunction.children[1].values_mapping = subfunction_mapping
    #     else:
    #         request_subfunction.values_mapping = response_subfunction.values_mapping = subfunction_mapping
    #     return service
    #
    # def __get_did_records_formula(self, record_number: None | int) -> Callable[[int], MessageStructureAlias]:
    #     return lambda did_count: self.__get_did_record(did_count=did_count, record_number=record_number)
    #
    # def __get_did_record(self,
    #                      did_count: int,
    #                      record_number: None | int,
    #                      optional: bool = False) -> tuple[MappingDataRecord | ConditionalFormulaDataRecord, ...]:
    #     data_records: list[MappingDataRecord | ConditionalFormulaDataRecord] = []
    #     for did_number in range(1, did_count + 1):
    #         name = f"DID#{did_number}" if record_number is None else f"DID#{record_number}_{did_number}"
    #         data_records.append(self.__get_did(name=name, optional=optional))
    #         data_records.append(self.__get_did_data(name=f"{name} data"))
    #     return tuple(data_records)
    #
    # def __get_did(self, name: str, optional: bool = False) -> MappingDataRecord:
    #     return MappingDataRecord(name=name,
    #                              length=DID_BIT_LENGTH,
    #                              values_mapping=self.did_mapping,
    #                              min_occurrences=0 if optional else 1,
    #                              max_occurrences=1)
    #
    # def __get_did_data(self, name: str = "DID data") -> ConditionalFormulaDataRecord:
    #     default_did_data = RawDataRecord(name=name,
    #                                      length=8,
    #                                      min_occurrences=1,
    #                                      max_occurrences=None)
    #
    #     def _get_did_data(did: int) -> tuple[RawDataRecord]:
    #         data_records = self.did_data_mapping.get(did, None)
    #         if data_records is None:
    #             raise ValueError(f"No data structure defined for DID 0x{did:04X}.")
    #         total_length = 0
    #         for dr in data_records:
    #             if not isinstance(dr, AbstractDataRecord) or not dr.fixed_total_length:
    #                 raise ValueError(f"Incorrectly defined data structure for DID 0x{did:04X}. "
    #                                  f"Only fixed length data records are supported right now.")
    #             total_length += dr.min_occurrences * dr.length
    #         return (RawDataRecord(name=name,
    #                               children=data_records,
    #                               length=total_length,
    #                               min_occurrences=1,
    #                               max_occurrences=1),)
    #
    #     return ConditionalFormulaDataRecord(formula=_get_did_data,
    #                                         default_message_continuation=[default_did_data])
    #
    # def __get_did_data_mask(self, name: str, optional: bool) -> ConditionalFormulaDataRecord:
    #     default_did_data_mask = RawDataRecord(name=name,
    #                                           length=8,
    #                                           min_occurrences=0 if optional else 1,
    #                                           max_occurrences=None)
    #
    #     def _get_mask_data_record(data_record: AbstractDataRecord) -> RawDataRecord:
    #         return MappingDataRecord(name=f"{data_record.name} (mask)",
    #                                  length=data_record.length,
    #                                  values_mapping={0: "no",
    #                                                  data_record.max_raw_value: "yes"},
    #                                  children=[_get_mask_data_record(child) for child in data_record.children],
    #                                  min_occurrences=data_record.min_occurrences,
    #                                  max_occurrences=data_record.max_occurrences)
    #
    #     def _get_did_data_mask(did: int) -> tuple[RawDataRecord]:
    #         data_records = self.did_data_mapping.get(did, None)
    #         if data_records is None:
    #             raise ValueError(f"No data structure defined for DID 0x{did:04X}.")
    #         total_length = 0
    #         mask_data_records = []
    #         for dr in data_records:
    #             if not isinstance(dr, AbstractDataRecord) or not dr.fixed_total_length:
    #                 raise ValueError(f"Incorrectly defined data structure for DID 0x{did:04X}. "
    #                                  f"Only fixed length data records are supported right now.")
    #             total_length += dr.min_occurrences * dr.length
    #             mask_data_records.append(_get_mask_data_record(dr))
    #         return (RawDataRecord(name=name,
    #                               children=mask_data_records,
    #                               length=total_length,
    #                               min_occurrences=0 if optional else 1,
    #                               max_occurrences=1),)
    #
    #     return ConditionalFormulaDataRecord(formula=_get_did_data_mask,
    #                                         default_message_continuation=[default_did_data_mask])
    #
    # def __get_input_output_control_by_identifier_request(self, did: int) -> MessageStructureAlias:
    #     return (INPUT_OUTPUT_CONTROL_PARAMETER,
    #             ConditionalMappingDataRecord(mapping={
    #                 0x00: (),
    #                 0x01: (),
    #                 0x02: (),
    #                 0x03: (*self.__conditional_control_state.get_message_continuation(did),
    #                        *self.__conditional_optional_control_enable_mask.get_message_continuation(did)),
    #             }))
    #
    # def __get_input_output_control_by_identifier_response(self, did: int) -> MessageStructureAlias:
    #     control_state_data_records = self.__conditional_control_state.get_message_continuation(did)
    #     return (INPUT_OUTPUT_CONTROL_PARAMETER,
    #             ConditionalMappingDataRecord(mapping={
    #                 0x00: control_state_data_records,
    #                 0x01: control_state_data_records,
    #                 0x02: control_state_data_records,
    #                 0x03: control_state_data_records,
    #             }))
    #
    # def __get_event_type_of_active_event(self, event_number: int) -> RawDataRecord:
    #     return RawDataRecord(name=f"eventTypeOfActiveEvent#{event_number}",
    #                          length=8,
    #                          children=(RESERVED_BIT,
    #                                    self.__event_type))
    #
    # def __get_event_window(self, event_number: int) -> MappingDataRecord:
    #     event_window = deepcopy(self.__event_window)
    #     event_window.name = f"{event_window.name}#{event_number}"
    #     return event_window
    #
    # def __get_event_type_record(self, event_type: int, event_number: int) -> None | RawDataRecord:
    #     response_on_event = self.services_mapping[RequestSID.ResponseOnEvent]
    #     conditional_response = response_on_event.response_structure[1].mapping.get(event_type, None)
    #     if conditional_response is None:
    #         return None
    #     event_type_record = deepcopy(conditional_response[2])
    #     event_type_record.name = f"{event_type_record.name}#{event_number}"
    #     return event_type_record
    #
    # def __get_event_type_record_09_continuation(self, event_number: int) -> None | ConditionalMappingDataRecord:
    #     response_on_event = self.services_mapping[RequestSID.ResponseOnEvent]
    #     conditional_response = response_on_event.response_structure[1].mapping.get(0x09, None)
    #     if conditional_response is None:
    #         return None
    #     event_type_record_continuation = deepcopy(conditional_response[3])
    #     for report_type, data_records in event_type_record_continuation.mapping.items():
    #         for data_record in data_records:
    #             data_record.name = f"{data_record.name}#{event_number}"
    #     return event_type_record_continuation
    #
    # def __get_activated_events(self, number_of_activated_events: int) -> tuple[RawDataRecord
    #                                                                            | MappingDataRecord
    #                                                                            | ConditionalMappingDataRecord, ...]:
    #     data_records: list[RawDataRecord | MappingDataRecord | ConditionalMappingDataRecord] = []
    #     for event_number in range(1, number_of_activated_events + 1):
    #         event_window = self.__get_event_window(event_number)
    #         service_to_respond = get_service_to_respond(event_number)
    #         data_records.append(self.__get_event_type_of_active_event(event_number))
    #         mapping = {
    #             0x01: (event_window,
    #                    get_event_type_record_01(event_number),
    #                    service_to_respond),
    #         }
    #         for event_type in {0x02, 0x03, 0x07}:
    #             event_type_record = self.__get_event_type_record(event_type=event_type,
    #                                                              event_number=event_number)
    #             if event_type_record is None:
    #                 continue
    #             mapping[event_type] = (event_window,
    #                                    event_type_record,
    #                                    service_to_respond)
    #
    #         event_type_record_08 = self.__get_event_type_record(event_type=0x08,
    #                                                             event_number=event_number)
    #         if event_type_record_08 is not None:
    #             mapping[0x08] = (event_window, event_type_record_08)
    #         event_type_record_09 = self.__get_event_type_record(event_type=0x09,
    #                                                             event_number=event_number)
    #         event_type_record_09_continuation = self.__get_event_type_record_09_continuation(event_number=event_number)
    #         if event_type_record_09 is not None and event_type_record_09_continuation is not None:
    #             mapping[0x09] = (event_window, event_type_record_09, event_type_record_09_continuation)
    #         data_records.append(ConditionalMappingDataRecord(mapping=mapping, value_mask=0x3F))
    #     return tuple(data_records)

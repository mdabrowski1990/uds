"""Implmentation of translator configurable through typical diagnostic parameters."""

__all__ = ["ConfigurableTranslator"]

from copy import deepcopy
from uds.message import RequestSID
from .translator import Translator
from .translator_definitions import BASE_TRANSLATOR
from .data_record import MessageStructureAlias, MappingDataRecord
from .service import Service


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
                 diagnostic_session_type_mapping: None | dict[int, str] = None,
                 reset_type_mapping: None | dict[int, str] = None,
                 report_type_mapping: None | dict[int, str] = None,
                 security_access_type_mapping: None | dict[int, str] = None,
                 control_type_type_mapping: None | dict[int, str] = None,
                 authentication_task_mapping: None | dict[int, str] = None,
                 definition_type_mapping: None | dict[int, str] = None,
                 routine_control_type_mapping: None | dict[int, str] = None,
                 zero_subfunction_mapping: None | dict[int, str] = None,
                 timing_parameter_access_type_mapping: None | dict[int, str] = None,
                 dtc_setting_type_mapping: None | dict[int, str] = None,
                 event_type_mapping: None | dict[int, str] = None,
                 link_control_type_mapping: None | dict[int, str] = None,
                 rid_mapping: None | dict[int, str] = None,
                 did_mapping: None | dict[int, str] = None,
                 did_structure_mapping: None | dict[int, MessageStructureAlias]) -> None:
        services: list[Service] = []
        # adapt SubFunctions (all except RoutineControl)
        for sid, subfunction_mapping in (
            (RequestSID.DiagnosticSessionControl, diagnostic_session_type_mapping),
            (RequestSID.ECUReset, reset_type_mapping),
            (RequestSID.ReadDTCInformation, report_type_mapping),
            (RequestSID.SecurityAccess, security_access_type_mapping),
            (RequestSID.CommunicationControl, control_type_type_mapping),
            (RequestSID.Authentication, authentication_task_mapping),
            (RequestSID.DynamicallyDefineDataIdentifier, definition_type_mapping),
            (RequestSID.TesterPresent, zero_subfunction_mapping),
            (RequestSID.AccessTimingParameter, timing_parameter_access_type_mapping),
            (RequestSID.ControlDTCSetting, dtc_setting_type_mapping),
            (RequestSID.ResponseOnEvent, event_type_mapping),
            (RequestSID.LinkControl, link_control_type_mapping),
        ):
            service: Service = deepcopy(BASE_TRANSLATOR.services_mapping[sid])
            if subfunction_mapping is not None:
                request_subfunction: MappingDataRecord = service.request_structure[0].children[1]
                response_subfunction: MappingDataRecord = service.response_structure[0].children[1]
                request_subfunction.values_mapping = response_subfunction.values_mapping = subfunction_mapping
            services.append(service)
        # adapt RoutineControl SubFunction and RID names
        routine_control: Service = deepcopy(BASE_TRANSLATOR.services_mapping[RequestSID.RoutineControl])
        if routine_control_type_mapping is not None:
            request_subfunction: MappingDataRecord = routine_control.request_structure[0].children[1]
            response_subfunction: MappingDataRecord = routine_control.response_structure[0].children[1]
            request_subfunction.values_mapping = response_subfunction.values_mapping = subfunction_mapping
        if rid_mapping is not None:
            rid: MappingDataRecord = routine_control.request_structure[1]
            rid.values_mapping = rid_mapping
        # adapt DIDs
        # TODO: adapt DID names
        # TODO: adapt structure of DIDs
        # TODO: propagate DIDs data records to multiple services:
        #  - ReadDTCInformation
        #  - DefineDataIdentifier
        #  - ResponseOnEvent
        #  - ReadDataByIdentifier
        #  - WriteDataByIdentifier
        super().__init__(services=services)

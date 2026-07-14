"""Implmentation of translator configurable through typical diagnostic parameters."""

__all__ = ["ConfigurableTranslator"]

from copy import deepcopy
from uds.message import RequestSID
from .translator import Translator
from .translator_definitions import BASE_TRANSLATOR
from .data_record import MessageStructureAlias, MappingDataRecord
from .service import Service
from uds.utilities import DID_BIT_LENGTH


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
        services_mapping: dict[RequestSID, Service] = {}
        # adapt SubFunctions (all except RoutineControl)
        for sid, subfunction_mapping in (
            (RequestSID.DiagnosticSessionControl, diagnostic_session_type_mapping),
            (RequestSID.ECUReset, reset_type_mapping),
            (RequestSID.ReadDTCInformation, report_type_mapping),
            (RequestSID.SecurityAccess, security_access_type_mapping),
            (RequestSID.CommunicationControl, control_type_type_mapping),
            (RequestSID.Authentication, authentication_task_mapping),
            (RequestSID.RoutineControl, routine_control_type_mapping),
            (RequestSID.DynamicallyDefineDataIdentifier, definition_type_mapping),
            (RequestSID.TesterPresent, zero_subfunction_mapping),
            (RequestSID.AccessTimingParameter, timing_parameter_access_type_mapping),
            (RequestSID.ControlDTCSetting, dtc_setting_type_mapping),
            (RequestSID.ResponseOnEvent, event_type_mapping),
            (RequestSID.LinkControl, link_control_type_mapping),
        ):
            if subfunction_mapping is not None:
                services_mapping[sid] = self.__adapt_subfunction(
                    service=deepcopy(BASE_TRANSLATOR.services_mapping[sid]),
                    subfunction_mapping=subfunction_mapping)
        # adapt RoutineControl SubFunction and RID names
        services_mapping[RequestSID.RoutineControl] = self.__adapt_rid_mapping(
            routine_control=services_mapping.get(RequestSID.RoutineControl,
                                                 deepcopy(BASE_TRANSLATOR.services_mapping[RequestSID.RoutineControl])),
            rid_mapping=rid_mapping)
        # adapt DIDs
        read_data_by_identifier: Service = services_mapping.get(
            RequestSID.ReadDataByIdentifier,
            deepcopy(BASE_TRANSLATOR.services_mapping[RequestSID.ReadDataByIdentifier]))
        # TODO: adapt structure of DIDs
        # TODO: propagate DIDs data records to multiple services:
        #  - ReadDTCInformation
        #  - DefineDataIdentifier
        #  - ResponseOnEvent
        #  - ReadDataByIdentifier
        #  - WriteDataByIdentifier
        if did_mapping is not None:
            ...  # TODO: update names
        if did_structure_mapping is not None:
            ... # TODO: update structures
        services_mapping[RequestSID.ReadDataByIdentifier] = read_data_by_identifier
        super().__init__(services=services_mapping.values())

    @staticmethod
    def __adapt_subfunction(service: Service, subfunction_mapping: dict[int, str]) -> Service:
        request_subfunction: MappingDataRecord = service.request_structure[0].children[1]
        response_subfunction: MappingDataRecord = service.response_structure[0].children[1]
        request_subfunction.values_mapping = response_subfunction.values_mapping = subfunction_mapping
        return service

    @staticmethod
    def __adapt_rid_mapping(routine_control: Service, rid_mapping: dict[int, str]) -> Service:
        rid: MappingDataRecord = routine_control.request_structure[1]
        rid.values_mapping = rid_mapping
        return routine_control


"""Implmentation of translator configurable through typical diagnostic parameters."""

__all__ = ["ConfigurableTranslator"]

from copy import deepcopy
from types import MappingProxyType
from typing import Callable, Mapping

from uds.message import RequestSID
from uds.utilities import DID_BIT_LENGTH, REPEATED_DATA_RECORDS_NUMBER, validate_raw_2byte_value

from .data_record import (
    AbstractDataRecord,
    ConditionalFormulaDataRecord,
    MappingDataRecord,
    MessageStructureAlias,
    RawDataRecord,
)
from .data_record_definitions import DID_COUNT_RECORDS, DTC_AND_STATUS, OPTIONAL_DTC_SNAPSHOT_RECORDS_NUMBERS_LIST
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
                 did_data_mapping: None | Mapping[int, MessageStructureAlias]) -> None:
        # copy services from base Translator
        services_mapping: dict[RequestSID, Service] = {
            service.request_sid: deepcopy(service) for service in base.services
        }
        # adapt SubFunctions
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
                services_mapping[sid] = self.__adapt_subfunction(service=services_mapping[sid],
                                                                 subfunction_mapping=subfunction_mapping)
        # adapt RID names
        if rid_mapping is not None:
            services_mapping[RequestSID.RoutineControl] = self.__adapt_rid_mapping(
                routine_control=services_mapping[RequestSID.RoutineControl],
                rid_mapping=rid_mapping)
        # create new Translator
        super().__init__(services=services_mapping.values())
        # adapt DIDs
        # TODO: adapt structure of DIDs
        # TODO: propagate DIDs data records to multiple services:
        #  - ReadDTCInformation
        #    - 0x04 (resp)
        #    - 0x05 (resp)
        #    - 0x18 (resp)
        #  - DefineDataIdentifier
        #    - 0x01 (req, resp)
        #    - 0x02 (resp)
        #    - 0x03 (req, resp)
        #  - ResponseOnEvent
        #    - 0x03 (req, resp)
        #    - 0x07 (req, resp)
        #  - ReadDataByIdentifier
        #    - * (req, resp)
        #  - WriteDataByIdentifier
        #    - * (req, resp)
        self.did_mapping = did_mapping
        self.did_data_mapping = did_data_mapping

    @property
    def did_mapping(self) -> Mapping[int, str]:
        return self.__did_mapping

    @did_mapping.setter
    def did_mapping(self, value: Mapping[int, str]) -> None:
        for did in value.keys():
            validate_raw_2byte_value(did)
        for name in value.values():
            if not isinstance(name, str):
                raise TypeError("All DID names must be str type.")
            if not name.strip():
                raise ValueError("All DID names must not consist of whitespace only.")
        self.__did_mapping = MappingProxyType(value)
        self.__adapt_did_services()

    @property
    def did_data_mapping(self) -> Mapping[int, MessageStructureAlias]:
        return self.__did_data_mapping

    @did_data_mapping.setter
    def did_data_mapping(self, value: Mapping[int, MessageStructureAlias]) -> None:
        for did in value.keys():
            validate_raw_2byte_value(did)
        self.__did_data_mapping = value
        self.__adapt_did_services()

    @property
    def __did(self) -> MappingDataRecord:
        return MappingDataRecord(name="DID",
                                 length=DID_BIT_LENGTH,
                                 values_mapping=self.did_mapping)

    @property
    def __multiple_did(self) -> MappingDataRecord:
        return MappingDataRecord(name="DID",
                                 length=DID_BIT_LENGTH,
                                 values_mapping=self.did_mapping,
                                 min_occurrences=1,
                                 max_occurrences=None)

    @property
    def __dynamically_defined_did(self) -> MappingDataRecord:
        return MappingDataRecord(name="dynamicallyDefinedDataIdentifier",
                                 length=DID_BIT_LENGTH,
                                 values_mapping=self.did_mapping)

    @property
    def __optional_dynamically_defined_did(self) -> MappingDataRecord:
        return MappingDataRecord(name="dynamicallyDefinedDataIdentifier",
                                 length=DID_BIT_LENGTH,
                                 values_mapping=self.did_mapping,
                                 min_occurrences=0,
                                 max_occurrences=1)

    @property
    def __source_did(self) -> MappingDataRecord:
        return MappingDataRecord(name="sourceDataIdentifier",
                                 length=DID_BIT_LENGTH,
                                 values_mapping=self.did_mapping)

    @property
    def __did_records(self) -> tuple[ConditionalFormulaDataRecord, ...]:
        return tuple(ConditionalFormulaDataRecord(formula=self.__get_did_records_formula(record_number + 1))
                     for record_number in range(REPEATED_DATA_RECORDS_NUMBER))

    @property
    def __dtc_snapshot_records(self) -> tuple[MappingDataRecord | RawDataRecord | ConditionalFormulaDataRecord, ...]:
        return tuple(item
                     for snapshot_record in zip(OPTIONAL_DTC_SNAPSHOT_RECORDS_NUMBERS_LIST,
                                                DID_COUNT_RECORDS,
                                                self.__did_records)
                     for item in snapshot_record)

    @property
    def __conditional_read_dtc_information_response(self) -> Mapping[int, MessageStructureAlias]:
        read_dtc_information = self.services_mapping[RequestSID.ReadDTCInformation]
        conditional_response_mapping = dict(read_dtc_information.response_structure[1].mapping)
        conditional_response_mapping[0x04] = (DTC_AND_STATUS, *self.__dtc_snapshot_records)
        # TODO:0x05
        # TODO:0x18
        return conditional_response_mapping

    @staticmethod
    def __adapt_subfunction(service: Service, subfunction_mapping: Mapping[int, str]) -> Service:
        request_subfunction: MappingDataRecord = service.request_structure[0].children[1]
        response_subfunction: MappingDataRecord = service.response_structure[0].children[1]
        request_subfunction.values_mapping = response_subfunction.values_mapping = subfunction_mapping
        return service

    @staticmethod
    def __adapt_rid_mapping(routine_control: Service, rid_mapping: Mapping[int, str]) -> Service:
        rid: MappingDataRecord = routine_control.request_structure[1]
        rid.values_mapping = rid_mapping
        return routine_control

    def __adapt_did_services(self) -> None:
        self.services_mapping[RequestSID.ReadDTCInformation].response_structure[1].mapping \
            = self.__conditional_read_dtc_information_response
        ...  # TODO: propagate DID related changes

    def __get_did_records_formula(self, record_number: None | int) -> Callable[[int], MessageStructureAlias]:
        return lambda did_count: self.__get_did_record(did_count=did_count, record_number=record_number)

    def __get_did_record(self,
                         did_count: int,
                         record_number: None | int,
                         optional: bool = False) -> tuple[MappingDataRecord | ConditionalFormulaDataRecord, ...]:
        data_records: list[MappingDataRecord | ConditionalFormulaDataRecord] = []
        for did_number in range(1, did_count + 1):
            name = f"DID#{did_number}" if record_number is None else f"DID#{record_number}_{did_number}"
            data_records.append(self.__get_did(name=name, optional=optional))
            data_records.append(self.__get_did_data(name=f"{name} data"))
        return tuple(data_records)

    def __get_did(self, name: str, optional: bool = False) -> MappingDataRecord:
        return MappingDataRecord(name=name,
                                 length=DID_BIT_LENGTH,
                                 values_mapping=self.did_mapping,
                                 min_occurrences=0 if optional else 1,
                                 max_occurrences=1)

    def __get_did_data(self, name: str = "DID data") -> ConditionalFormulaDataRecord:
        default_did_data = RawDataRecord(name=name,
                                         length=8,
                                         min_occurrences=1,
                                         max_occurrences=None)

        def _get_did_data(did: int) -> tuple[RawDataRecord]:
            data_records = self.did_data_mapping.get(did, None)
            if data_records is None:
                raise ValueError(f"No data structure defined for DID 0x{did:04X}.")
            total_length = 0
            for dr in data_records:
                if not isinstance(dr, AbstractDataRecord) or not dr.fixed_total_length:
                    raise ValueError(f"Incorrectly defined data structure for DID 0x{did:04X}. "
                                     f"Only fixed length data records are supported right now.")
                total_length += dr.min_occurrences * dr.length
            return (RawDataRecord(name=name,
                                  children=data_records,
                                  length=total_length,
                                  min_occurrences=1,
                                  max_occurrences=1),)

        return ConditionalFormulaDataRecord(formula=_get_did_data,
                                            default_message_continuation=[default_did_data])

    def __get_did_data_mask(self, name: str, optional: bool) -> ConditionalFormulaDataRecord:
        default_did_data_mask = RawDataRecord(name=name,
                                              length=8,
                                              min_occurrences=0 if optional else 1,
                                              max_occurrences=None)

        def _get_mask_data_record(data_record: AbstractDataRecord) -> RawDataRecord:
            return MappingDataRecord(name=f"{data_record.name} (mask)",
                                     length=data_record.length,
                                     values_mapping={0: "no",
                                                     data_record.max_raw_value: "yes"},
                                     children=[_get_mask_data_record(child) for child in data_record.children],
                                     min_occurrences=data_record.min_occurrences,
                                     max_occurrences=data_record.max_occurrences)

        def _get_did_data_mask(did: int) -> tuple[RawDataRecord]:
            data_records = self.did_data_mapping.get(did, None)
            if data_records is None:
                raise ValueError(f"No data structure defined for DID 0x{did:04X}.")
            total_length = 0
            mask_data_records = []
            for dr in data_records:
                if not isinstance(dr, AbstractDataRecord) or not dr.fixed_total_length:
                    raise ValueError(f"Incorrectly defined data structure for DID 0x{did:04X}. "
                                     f"Only fixed length data records are supported right now.")
                total_length += dr.min_occurrences * dr.length
                mask_data_records.append(_get_mask_data_record(dr))
            return (RawDataRecord(name=name,
                                  children=mask_data_records,
                                  length=total_length,
                                  min_occurrences=0 if optional else 1,
                                  max_occurrences=1),)

        return ConditionalFormulaDataRecord(formula=_get_did_data_mask,
                                            default_message_continuation=[default_did_data_mask])

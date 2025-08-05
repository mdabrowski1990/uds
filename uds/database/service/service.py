"""Definition of UDS Service data encoding and decoding."""

__all__ = ["Service", "DataRecordValuesAlias", "DecodedMessageAlias"]

from typing import Collection, List, Mapping, Optional, OrderedDict, Sequence, Set, Tuple, Union
from warnings import warn
from copy import deepcopy

from uds.message import NRC, RESPONSE_REQUEST_SID_DIFF, RequestSID, ResponseSID
from uds.utilities import InconsistentArgumentsError, RawBytesAlias, validate_raw_bytes, int_to_bytes, Endianness

from ..data_record import (
    DEFAULT_DIAGNOSTIC_MESSAGE_CONTINUATION,
    AbstractConditionalDataRecord,
    AbstractDataRecord,
    AliasMessageStructure,
    DataRecordInfoAlias,
    PhysicalValueAlias,
    SingleOccurrenceInfo,
    ChildrenValuesAlias
)

DataRecordValueAlias = Optional[int, ChildrenValuesAlias, Sequence[Union[int, ChildrenValuesAlias]]]
"""Alias for Data Record value that can be used in the Data Records Mapping.
For a single occurrence Data Records (is_reoccurring=False) it is either a raw value (int type), None (no occurrence)
or a mapping with children values.
For multiple occurrences Data Records (is_reoccurring=True) it is a sequence. Each sequence element represents a single
occurrence and is either a raw value or a mapping with children values.
"""
DataRecordsValuesAlias = Mapping[str, DataRecordValueAlias]
"""Alias for Data Records values mapping.
Mapping keys are Data Records names. 
Mapping values are corresponding Data Records values.
"""

DecodedMessageAlias = Tuple[DataRecordInfoAlias, ...]
"""Alias for decoded information about a Diagnostic Message."""


class Service:
    """
    Translator for a single Diagnostic Service.

    Features:
     - contains structures of diagnostic messages (both request and response) for a single diagnostic service
     - provides tools for decoding meaningful information (physical values) from diagnostic messages
     - provides tools for creating diagnostic messages out of meaningful information (physical values)
    """

    NEGATIVE_RESPONSE_LENGTH = 3

    def __init__(self,
                 request_sid: RequestSID,
                 request_structure: AliasMessageStructure,
                 response_structure: AliasMessageStructure,
                 supported_nrc: Collection[NRC] = tuple(NRC)) -> None:
        """
        Define a translator for a single diagnostic service.

        :param request_sid: Service Identifier for request message.
        :param request_structure: Data Records that contains translation for response message continuation.
        :param response_structure: Data Records that contains translation for diagnostic message continuation.
        :param supported_nrc: NRC codes that are supported by this service.

        .. warning:: Arguments `request_structure` and `response_structure` must not contain Data Records for the first
            byte of respectively request message (SID) and response message (RSID) as those values are passed via
            other parameters.
        """
        self.request_sid = request_sid
        self.request_structure = request_structure
        self.response_structure = response_structure
        self.supported_nrc = supported_nrc

    @property
    def request_sid(self) -> RequestSID:
        """Get Service Identifier (SID) value for this diagnostic service."""
        return self.__request_sid

    @request_sid.setter
    def request_sid(self, request_sid: RequestSID) -> None:
        """
        Set Service Identifier (SID) value for this diagnostic service.

        :param request_sid: SID value to set.

        :raise ValueError: Request SID and Response SID values are incorrectly defined for given value.
        """
        self.__request_sid = RequestSID.validate_member(request_sid)
        self.__response_sid = ResponseSID.validate_member(request_sid + RESPONSE_REQUEST_SID_DIFF)
        if self.__request_sid.name != self.__response_sid.name:
            raise ValueError("Request and Response SID values are not defined for the same Service.")

    @property
    def response_sid(self) -> ResponseSID:
        """Get Response Service Identifier (RSID) value for this diagnostic service."""
        return self.__response_sid

    @property
    def request_structure(self) -> AliasMessageStructure:
        """Get Data Records used for translating request messages for this diagnostic service."""
        return self.__request_structure

    @request_structure.setter
    def request_structure(self, request_structure: AliasMessageStructure) -> None:
        """
        Set Data Records to yse for translating request messages for this diagnostic service.

        :param request_structure: Data Records sequence to set.
        """
        self.validate_message_structure(request_structure)
        self.__request_structure = tuple(request_structure)

    @property
    def response_structure(self) -> AliasMessageStructure:
        """Get Data Records used for translating positive response messages for this diagnostic service."""
        return self.__response_structure

    @response_structure.setter
    def response_structure(self, response_structure: AliasMessageStructure) -> None:
        """
        Set Data Records used for translating positive response messages for this diagnostic service.

        :param response_structure: Data Records sequence to set.
        """
        self.validate_message_structure(response_structure)
        self.__response_structure = tuple(response_structure)

    @property
    def supported_nrc(self) -> Set[NRC]:
        """Get NRC codes that are supported by this diagnostic service."""
        return self.__supported_nrc

    @supported_nrc.setter
    def supported_nrc(self, nrc_container: Collection[NRC]) -> None:
        """
        Set NRC codes that are supported by this diagnostic service.

        :param nrc_container: NRC codes to set as supported.
        """
        for nrc in nrc_container:
            NRC.validate_member(nrc)
        self.__supported_nrc = set(nrc_container)

    @property
    def name(self) -> str:
        """Get name of this service."""
        return self.request_sid.name

    def _get_rsid_info(self) -> SingleOccurrenceInfo:
        """Get detailed information about Response Service Identifier."""
        return SingleOccurrenceInfo(name="RSID",
                                    length=8,
                                    raw_value=self.response_sid.value,
                                    physical_value=self.response_sid.name,
                                    children=tuple())

    def _get_sid_info(self) -> SingleOccurrenceInfo:
        """Get detailed information about Service Identifier."""
        return SingleOccurrenceInfo(name="SID",
                                    length=8,
                                    raw_value=self.request_sid.value,
                                    physical_value=self.request_sid.name,
                                    children=tuple())

    @staticmethod
    def _get_nrc_info(nrc: NRC) -> SingleOccurrenceInfo:
        """
        Get detailed information about Negative Response Code.

        :param nrc: The value of NRC.

        :return: Detailed information for single occurrence of NRC Data Record.
        """
        nrc = NRC.validate_member(nrc)
        return SingleOccurrenceInfo(name="NRC",
                                    length=8,
                                    raw_value=nrc.value,
                                    physical_value=nrc.name,
                                    children=tuple())

    @staticmethod
    def _extract_data_record_occurrences(data_record: AbstractDataRecord,
                                         value: DataRecordValueAlias) -> Sequence[int]:  # TODO
        if data_record.is_reoccurring:
            if not isinstance(data_record_value, Sequence):
                raise ValueError("A sequence of values has to be provided for a reoccurring Data Record. "
                                 f"Data Record name = {data_record.name}.")
            if not data_record.min_occurrences <= len(data_record_value) <= data_record.max_occurrences:
                raise ValueError("A sequence of values has to contain proper number of Data Record occurrences."
                                 f"Data Record name = {data_record.name}. "
                                 f"Data Record min occurrences number = {data_record.min_occurrences}. "
                                 f"Data Record max occurrences number = {data_record.max_occurrences}. "
                                 f"Provided sequence = {data_record_value}.")
            raw_values = []
            for occurrence_value in data_record_value:
                if isinstance(occurrence_value, int):
                    raw_values.append(occurrence_value)
                elif isinstance(occurrence_value, Mapping):
                    raw_values.append(data_record.get_raw_value_from_children(occurrence_value))
                else:
                    raise ValueError("Incorrect value was provided one of Multiple Occurrences Data Record. "
                                     f"Data Record name = {data_record.name}. "
                                     f"Provided values = {data_record_value}. "
                                     f"Faulty occurrence value = {occurrence_value}.")
            for raw_value in raw_values:
                total_raw_value = (total_raw_value << data_record.length) + raw_value
                total_length += data_record.length
        else:
            if isinstance(data_record_value, int):
                raw_value = data_record_value
            elif isinstance(data_record_value, Mapping):
                raw_value = [data_record.get_raw_value_from_children(data_record_value)]
            else:
                raise ValueError(f"Incorrect value was provided for Single Occurrence Data Record. "
                                 f"Data Record name = {data_record.name}. "
                                 f"Provided value = {data_record_value}.")
            total_raw_value = (total_raw_value << data_record.length) + raw_value
            total_length += data_record.length

    @staticmethod
    def _decode_payload(payload: RawBytesAlias,
                        message_continuation: AliasMessageStructure) -> DecodedMessageAlias:
        decoded_message_continuation = []
        remaining_payload = bytearray(payload)
        for data_record in message_continuation:
            if isinstance(data_record, AbstractConditionalDataRecord):
                ...
        # TODO



    @classmethod
    def _encode_message(cls,
                        data_records_values: DataRecordsValuesAlias,
                        message_structure: AliasMessageStructure) -> bytearray:
        """
        Encode payload of a diagnostic message.

        :param data_records_values: Mapping with Data Records values that are part of the message.
            Mapping keys are Data Records names.
            Mapping values are either a single occurrence or multiple occurrences values. Each occurrence can be
            a raw value or a mapping with children names and its corresponding values.
        :param message_structure: Data Records that form the remaining structure of the diagnostic message.

        :raise RuntimeError: An error occurred which was caused by incorrect message structure.
        :raise ValueError: Provided Data Records values are incorrect.
        :raise NotImplementedError: There is missing implementation for at least one Data Record in the provided
            message structure.

        :return: Payload of a diagnostic message created from provided data records values.
        """
        data_records_values = dict(deepcopy(data_records_values))
        total_raw_value = 0
        total_length = 0
        payload_continuation = bytearray()
        for data_record in message_structure:
            raw_value: int
            if isinstance(data_record, AbstractDataRecord):
                data_record_value = data_records_values.pop(data_record.name)
                occurrences = cls._extract_data_record_occurrences(data_record=data_record,
                                                                   value=data_record_value)
                for raw_value in occurrences:
                    total_raw_value = (total_raw_value << data_record.length) + raw_value
                    total_length += data_record.length
            elif isinstance(data_record, AbstractConditionalDataRecord):
                message_continuation = data_record.get_message_continuation(raw_value=raw_value)
                payload_continuation = cls._encode_message(data_records_values=data_records_values,
                                                           message_structure=message_continuation)
                break  # conditional data record must be the last one anyway
            else:
                raise NotImplementedError("Unexpected Data Record type found in the structure.")
        if total_length % 8 != 0:
            raise RuntimeError("Incorrect message structure was provided.")
        return bytearray(int_to_bytes(int_value=total_raw_value,
                                      size=total_length // 8,
                                      endianness=Endianness.BIG_ENDIAN)) + payload_continuation

    @staticmethod
    def validate_message_structure(value: AliasMessageStructure) -> None:
        """
        Validate whether the provided value is a structure of diagnostic message.

        :param value: Value to check.
        """
        AbstractConditionalDataRecord.validate_message_continuation(value)

    def decode_request(self, payload: RawBytesAlias) -> DecodedMessageAlias:
        """
        Decode information carried by a request message for this diagnostic service.

        :param payload: Payload of a request message.

        :raise ValueError: Provided payload does not carry a request to this diagnostic service.

        :return: Decoded information from the provided payload.
        """
        validate_raw_bytes(payload, allow_empty=False)
        if payload[0] != self.request_sid:
            raise ValueError("Provided payload does not start from SID value for this service.")
        decoded_message_continuation = self._decode_payload(payload=payload[1:],
                                                            message_continuation=self.request_structure)
        return self._get_sid_info(), *decoded_message_continuation

    def decode_positive_response(self, payload: RawBytesAlias) -> DecodedMessageAlias:
        """
        Decode information carried by a positive response message for this diagnostic service.

        :param payload: Payload of a positive response message.

        :raise ValueError: Provided payload does not carry a positive response to this diagnostic service.

        :return: Decoded information from the provided payload.
        """
        validate_raw_bytes(payload, allow_empty=False)
        if payload[0] != self.response_sid:
            raise ValueError("Provided payload does not start from RSID value for this service.")
        decoded_message_continuation = self._decode_payload(payload=payload[1:],
                                                            message_continuation=self.request_structure)
        return self._get_rsid_info(), *decoded_message_continuation

    def decode_negative_response(self, payload: RawBytesAlias) -> DecodedMessageAlias:
        """
        Decode information carried by a negative response message for this diagnostic service.

        :param payload: Payload of a negative response message.

        :raise ValueError: Provided payload does not carry a negative response to this diagnostic service.

        :return: Decoded information from the provided payload.
        """
        validate_raw_bytes(payload, allow_empty=False)
        if len(payload) != self.NEGATIVE_RESPONSE_LENGTH:
            raise ValueError(f"Negative Response Message must be exactly {self.NEGATIVE_RESPONSE_LENGTH}-bytes long.")
        rsid = payload[0]
        sid = payload[1]
        nrc = payload[2]
        if rsid != ResponseSID.NegativeResponse:
            raise ValueError("Provided payload does not start from Negative Response SID value.")
        if sid != self.request_sid:
            raise ValueError(f"Provided payload contains Negative Response for another service with SID=0x{sid:02X}.")
        if nrc not in self.supported_nrc:
            warn(message=f"Received NRC code `0x{nrc:02X}` that is not supported by {self.name} service.",
                 category=UserWarning)
        return self._get_rsid_info(), self._get_sid_info(), self._get_nrc_info(NRC(nrc))

    def decode(self, payload: RawBytesAlias) -> DecodedMessageAlias:
        """
        Decode information carried by a diagnostic message for this diagnostic service.

        :param payload: Payload of a diagnostic message.

        :raise ValueError: Provided message payload does not start from a SID value for this service.

        :return: Decoded information from the provided payload.
        """
        if payload[0] == self.request_sid:
            return self.decode_request(payload)
        if payload[0] == self.response_sid:
            return self.decode_positive_response(payload)
        if payload[0] == ResponseSID.NegativeResponse:
            return self.decode_negative_response(payload)
        raise ValueError("Provided message does not belong to this diagnostic message")

    def encode_request(self, data_records_values: DataRecordsValuesAlias) -> bytearray:
        """
        Encode request message payload for this service.

        :param data_records_values: Mapping with Data Records values that are part of the message.
            Mapping keys are Data Records names.
            Mapping values are either a single occurrence or multiple occurrences values. Each occurrence can be
            a raw value or a mapping with children names and its corresponding values.

        :return: Payload of a request message.
        """
        return (bytearray([self.request_sid])
                + self._encode_message(data_records_values=data_records_values,
                                       message_structure=self.response_structure))

    def encode_positive_response(self, data_records_values: DataRecordsValuesAlias) -> bytearray:
        """
        Encode positive response message payload for this service.

        :param data_records_values: Mapping with Data Records values that are part of the message.
            Mapping keys are Data Records names.
            Mapping values are either a single occurrence or multiple occurrences values. Each occurrence can be
            a raw value or a mapping with children names and its corresponding values.

        :return: Payload of a positive response message.
        """
        return (bytearray([self.response_sid])
                + self._encode_message(data_records_values=data_records_values,
                                       message_structure=self.response_structure))

    def encode_negative_response(self, nrc: NRC) -> bytearray:
        """
        Encode negative response message payload for this service.

        :param nrc: NRC value to use.

        :return: Payload of a negative response message for this service.
        """
        NRC.validate_member(nrc)
        if nrc not in self.supported_nrc:
            warn(message=f"NRC code {nrc} is not supported by service {self.name}.")
        return bytearray([ResponseSID.NegativeResponse, self.request_sid, nrc])

    def encode(self,
               sid: Union[int, RequestSID, ResponseSID],
               data_records_values: DataRecordsValuesAlias) -> bytearray:
        """
        Encode diagnostic message payload for this service.

        :param sid: Value of Service Identifier.
            It should be either equal to either to `request_sid`, `response_sid` or NegativeResponseSID (0x7F).
        :param data_records_values: Mapping with Data Records values that are part of the message.
            Mapping keys are Data Records names.
            Mapping values are either a single occurrence or multiple occurrences values. Each occurrence can be
            a raw value or a mapping with children names and its corresponding values.

        :raise ValueError: Provided SID value cannot be handled by this service.

        :return: Payload of a diagnostic message created from provided data records values.
        """
        if sid == self.request_sid:
            return self.encode_request(data_records_values=data_records_values)
        if sid == self.response_sid:
            return self.encode_positive_response(data_records_values=data_records_values)
        if sid == ResponseSID.NegativeResponse:
            return self.encode_negative_response(**data_records_values)
        raise ValueError("Provided SID value is neither request or response SID value for this service.")

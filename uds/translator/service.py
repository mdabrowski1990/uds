"""Definition of diagnostic services data encoding and decoding."""

__all__ = ["Service", "DecodedMessageAlias", "DataRecordsValuesAlias",
           "DataRecordValueAlias", "MultipleDataRecordValueAlias", "SingleDataRecordValueAlias"]

from copy import deepcopy
from typing import Collection, Dict, List, Mapping, Optional, Sequence, Set, Tuple, Union
from warnings import warn

from uds.message import NRC, RESPONSE_REQUEST_SID_DIFF, RequestSID, ResponseSID
from uds.utilities import Endianness, InconsistencyError, RawBytesAlias, bytes_to_int, int_to_bytes, validate_raw_bytes

from .data_record import (
    AbstractConditionalDataRecord,
    AbstractDataRecord,
    AliasMessageStructure,
    ChildrenValuesAlias,
    DataRecordInfoAlias,
    SingleOccurrenceInfo,
)

SingleDataRecordValueAlias = Optional[Union[int, ChildrenValuesAlias]]
"""Alias for a single occurrence Data Record. Either:
 - int type - a single raw value
 - mapping type - children values
 - None - no occurrence"""
MultipleDataRecordValueAlias = Sequence[Union[int, ChildrenValuesAlias]]
"""Alias for a multiple occurrences Data Record. It is a sequence where each element represents a single occurrence.
Each element is either raw value (int type) or children values (mapping type)."""
DataRecordValueAlias = Union[SingleDataRecordValueAlias, MultipleDataRecordValueAlias]
"""Alias for a Data Record value that can be used in the Data Records Mapping."""
DataRecordsValuesAlias = Mapping[str, DataRecordValueAlias]
"""Alias for Data Records values mapping.
Mapping keys are Data Records names.
Mapping values are corresponding Data Records values.
"""

DecodedMessageAlias = Tuple[DataRecordInfoAlias, ...]
"""Alias for decoded information about a Diagnostic Message."""


class Service:
    """
    Translator for a diagnostic service.

    Interactions via UDS protocol with servers (ECUs) are possible via
    :ref:`diagnostic services <knowledge-base-service>` which are basically functions that you can request as a client.

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
        self.__request_sid: RequestSID = RequestSID.validate_member(request_sid)
        self.__response_sid: ResponseSID = ResponseSID.validate_member(request_sid + RESPONSE_REQUEST_SID_DIFF)
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
        Set Data Records to use for translating request messages for this diagnostic service.

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
        return self.request_sid.name  # type: ignore

    def _get_rsid_info(self, positive: bool = True) -> SingleOccurrenceInfo:
        """
        Get detailed information about Response Service Identifier.

        :param positive: RSID is for positive or negative response message.

        :return: Detailed information about RSID value.
        """
        rsid = self.response_sid if positive else ResponseSID.NegativeResponse
        return SingleOccurrenceInfo(name="RSID",
                                    length=8,
                                    raw_value=rsid.value,
                                    physical_value=rsid.name,
                                    children=tuple(),
                                    unit=None)

    def _get_sid_info(self) -> SingleOccurrenceInfo:
        """Get detailed information about Service Identifier."""
        return SingleOccurrenceInfo(name="SID",
                                    length=8,
                                    raw_value=self.request_sid.value,
                                    physical_value=self.request_sid.name,
                                    children=tuple(),
                                    unit=None)

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
                                    children=tuple(),
                                    unit=None)

    @staticmethod
    def _get_single_data_record_occurrence(data_record: AbstractDataRecord,
                                           value: SingleDataRecordValueAlias) -> List[int]:
        """
        Get occurrence value for a single occurrence Data Record.

        :param data_record: Data Record object.
        :param value: Data Record value. Either:

            - None - no value (valid for Data Records with min_occurrences=0)
            - int type - raw value
            - mapping type - children values

        :raise TypeError: Provided value has incorrect type that cannot be handled for the provided Data Record.
        :raise ValueError: Provided value is incorrect.

        :return: List with either 1 or 0 raw values for this Data Record.
        """
        if value is None and data_record.min_occurrences == 0:
            return []
        if isinstance(value, int):
            if not data_record.min_raw_value <= value <= data_record.max_raw_value:
                raise ValueError("Provided occurrence value is out of range. "
                                 f"Data Record name = {data_record.name!r}. "
                                 f"Data Record min raw value = {data_record.min_raw_value}. "
                                 f"Data Record max raw value = {data_record.max_raw_value}. "
                                 f"Provided sequence = {value}. Occurrence value = {value}.")
            return [value]
        if isinstance(value, Mapping):
            return [data_record.get_raw_value_from_children(value)]
        raise TypeError(f"Incorrect value was provided for a Single Occurrence Data Record. "
                        f"Data Record name = {data_record.name!r}. Provided value = {value}.")

    @staticmethod
    def _get_reoccurring_data_record_occurrences(data_record: AbstractDataRecord,
                                                 value: MultipleDataRecordValueAlias) -> List[int]:
        """
        Get occurrences values for multiple occurrences Data Record.

        :param data_record: Data Record object.
        :param value: Sequence with Data Record values (either int or mapping type).

        :raise TypeError: Provided value has incorrect type that cannot be handled for the provided Data Record.
        :raise ValueError: Provided value is incorrect.

        :return: List with raw values for this Data Record.
        """
        if not isinstance(value, Sequence):
            raise TypeError("A sequence of values has to be provided for a reoccurring Data Record. "
                            f"Data Record name = {data_record.name!r}.")
        if len(value) < data_record.min_occurrences or len(value) > (data_record.max_occurrences or float("inf")):
            raise ValueError("A sequence of values has to contain proper number of Data Record occurrences."
                             f"Data Record name = {data_record.name!r}. "
                             f"Data Record min occurrences number = {data_record.min_occurrences}. "
                             f"Data Record max occurrences number = {data_record.max_occurrences}. "
                             f"Provided sequence = {value}.")
        raw_values: List[int] = []
        for occurrence_value in value:
            if isinstance(occurrence_value, int):
                if not data_record.min_raw_value <= occurrence_value <= data_record.max_raw_value:
                    raise ValueError("Provided occurrence value is out of range. "
                                     f"Data Record name = {data_record.name!r}. "
                                     f"Data Record min raw value = {data_record.min_raw_value}. "
                                     f"Data Record max raw value = {data_record.max_raw_value}. "
                                     f"Provided sequence = {value}. Occurrence value = {occurrence_value}.")
                raw_values.append(occurrence_value)
            elif isinstance(occurrence_value, Mapping):
                raw_values.append(data_record.get_raw_value_from_children(occurrence_value))
            else:
                raise ValueError("Incorrect value was provided for at least one occurrence of a Multi Occurrences "
                                 f"Data Record. Data Record name = {data_record.name!r}. "
                                 f"Provided values = {value}. Incorrect occurrence = {occurrence_value}.")
        return raw_values

    @classmethod
    def _get_data_record_occurrences(cls,
                                     data_record: AbstractDataRecord,
                                     value: DataRecordValueAlias) -> List[int]:
        """
        Get raw values of all occurrences provided as value.

        :param data_record: Data Record object.
        :param value: Data Record values. Either for a single occurrence or multiple occurrences.
            Each occurrence might be a raw value or mapping with children values.

        :return: Raw values for following Data Record occurrences.
        """
        if data_record.is_reoccurring:
            return cls._get_reoccurring_data_record_occurrences(data_record=data_record, value=value)  # type: ignore
        return cls._get_single_data_record_occurrence(data_record=data_record, value=value)  # type: ignore

    @classmethod
    def _decode_payload(cls,
                        payload: RawBytesAlias,
                        message_structure: AliasMessageStructure,
                        check_remaining_length: bool = True) -> DecodedMessageAlias:
        """
        Decode information for given message structure and payload.

        :param payload: Payload to decode.
        :param message_structure: Defined structure of a diagnostic message.
        :param check_remaining_length: Whether to raise an exception when only part of the message was decoded.

        :raise ValueError: Provided message payload was too short.
        :raise RuntimeError: An error occurred which was caused by incorrect message structure.
        :raise NotImplementedError: There is missing implementation for at least one Data Record in the provided
            message structure.

        :return: Decoded information from the provided payload.
        """
        decoded_message_continuation = []
        remaining_length = 8 * len(payload)
        payload_int = bytes_to_int(bytes_list=payload, endianness=Endianness.BIG_ENDIAN) if payload else 0
        raw_values: List[int] = []
        for data_record in message_structure:
            if isinstance(data_record, AbstractDataRecord):
                max_occurrences_number = remaining_length // data_record.length
                occurrences_number = int(min(max_occurrences_number, data_record.max_occurrences or float("inf")))
                if occurrences_number < data_record.min_occurrences:
                    raise ValueError("Too short payload was provided.")
                raw_values = []
                for _ in range(occurrences_number):
                    remaining_length -= data_record.length
                    mask = (1 << data_record.length) - 1
                    occurrence_value = (payload_int >> remaining_length) & mask
                    raw_values.append(occurrence_value)
                if data_record.min_occurrences == 0 and not raw_values:
                    # an information that this is the end of the message
                    break
                decoded_message_continuation.append(data_record.get_occurrence_info(*raw_values))
            elif isinstance(data_record, AbstractConditionalDataRecord):
                if remaining_length % 8 != 0:
                    raise RuntimeError("Incorrect Data Records structure.")
                bytes_number = remaining_length // 8
                conditional_message_continuation = data_record.get_message_continuation(raw_value=raw_values[-1])
                remaining_payload = int_to_bytes(int_value=payload_int & ((1 << remaining_length) - 1),
                                                 endianness=Endianness.BIG_ENDIAN,
                                                 size=bytes_number)
                decoded_conditional_message_continuation = cls._decode_payload(
                    payload=remaining_payload,
                    message_structure=conditional_message_continuation,
                    check_remaining_length=False)
                for data_record_info in decoded_conditional_message_continuation:
                    occurrences_number = 1 if isinstance(data_record_info["raw_value"], int) \
                        else len(data_record_info["raw_value"])
                    remaining_length -= occurrences_number * data_record_info["length"]
                    decoded_message_continuation.append(data_record_info)
                    raw_values.append(data_record_info["raw_value"])
            else:
                raise NotImplementedError("Unexpected Data Record type found in the structure.")
        if check_remaining_length and remaining_length != 0:
            raise RuntimeError("Incorrect message structure was defined.")
        return tuple(decoded_message_continuation)

    @classmethod
    def _encode_message(cls,
                        data_records_values: Dict[str, DataRecordValueAlias],
                        message_structure: AliasMessageStructure,
                        check_unused_data_record_values: bool = True) -> bytearray:
        """
        Encode payload of a diagnostic message.

        :param data_records_values: Mapping with Data Records values that are part of the message.
            Mapping keys are Data Records names.
            Mapping values are either a single occurrence or multiple occurrences values. Each occurrence can be
            a raw value or a mapping with children names and its corresponding values.
        :param message_structure: Data Records that form the remaining structure of the diagnostic message.
        :param check_unused_data_record_values: Whether to raise an exception when unused Data Record value found.

        :raise RuntimeError: An error occurred which was caused by incorrect message structure.
        :raise ValueError: Value for at least one Data Record that is no part of the message, was provided.
        :raise NotImplementedError: There is missing implementation for at least one Data Record in the provided
            message structure.

        :return: Payload of a diagnostic message created from provided data records values.
        """
        total_raw_value = 0
        total_length = 0
        occurrences = []
        for data_record in message_structure:
            if isinstance(data_record, AbstractDataRecord):
                if data_record.name in data_records_values:
                    data_record_value = data_records_values.pop(data_record.name)
                    occurrences = cls._get_data_record_occurrences(data_record=data_record,
                                                                   value=data_record_value)
                elif data_record.min_occurrences == 0:
                    occurrences = []
                else:
                    raise InconsistencyError(f"Value for Data Record {data_record.name!r} was not provided.")
                for raw_value in occurrences:
                    total_raw_value = (total_raw_value << data_record.length) + raw_value
                    total_length += data_record.length
            elif isinstance(data_record, AbstractConditionalDataRecord):
                message_continuation = data_record.get_message_continuation(raw_value=raw_value)
                if message_continuation:
                    payload_continuation = cls._encode_message(data_records_values=data_records_values,
                                                               message_structure=message_continuation,
                                                               check_unused_data_record_values=False)
                    _length = 8 * len(payload_continuation)
                    total_length += _length
                    continuation_raw_value = bytes_to_int(payload_continuation, endianness=Endianness.BIG_ENDIAN)
                    total_raw_value = ((total_raw_value << _length) + continuation_raw_value)
                    # calculate raw_value of the last Data Record (in the message_continuation)
                    # in case it is followed by another ConditionalDataRecord
                    last_data_record_mask = (1 << message_continuation[-1].length) - 1
                    raw_value = continuation_raw_value & last_data_record_mask
            else:
                raise NotImplementedError("Unexpected Data Record type found in the structure.")
            # stop processing if the proceeding Data Record was empty (that means message is over)
            if not occurrences:
                break
        if total_length % 8 != 0:
            raise RuntimeError("Incorrect message structure was provided.")
        if check_unused_data_record_values and data_records_values:
            raise ValueError(f"Unused Data Record values were provided: {data_records_values}.")
        return bytearray(int_to_bytes(int_value=total_raw_value,
                                      size=total_length // 8,
                                      endianness=Endianness.BIG_ENDIAN))

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
                                                            message_structure=self.request_structure)
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
                                                            message_structure=self.response_structure)
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
            warn(message=f"Received NRC code `0x{nrc:02X}` that is not supported by {self.name!r} service.",
                 category=UserWarning)
        return self._get_rsid_info(positive=False), self._get_sid_info(), self._get_nrc_info(NRC(nrc))

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
                + self._encode_message(data_records_values=deepcopy(dict(data_records_values)),
                                       message_structure=self.request_structure))

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
                + self._encode_message(data_records_values=deepcopy(dict(data_records_values)),
                                       message_structure=self.response_structure))

    def encode_negative_response(self, nrc: NRC) -> bytearray:
        """
        Encode negative response message payload for this service.

        :param nrc: NRC value to use.

        :return: Payload of a negative response message for this service.
        """
        NRC.validate_member(nrc)
        if nrc not in self.supported_nrc:
            warn(message=f"NRC code {nrc} is not supported by service {self.name!r}.",
                 category=UserWarning)
        return bytearray([ResponseSID.NegativeResponse, self.request_sid, nrc])

    def encode(self,
               data_records_values: DataRecordsValuesAlias,
               sid: Optional[RequestSID] = None,
               rsid: Optional[ResponseSID] = None) -> bytearray:
        """
        Encode diagnostic message payload for this service.

        :param data_records_values: Mapping with Data Records values that are part of the message.
            Mapping keys are Data Records names.
            Mapping values are either a single occurrence or multiple occurrences values. Each occurrence can be
            a raw value or a mapping with children names and its corresponding values.
        :param sid: Request SID value.
            Used by request message (first byte) and negative response message (second byte).
        :param rsid: Response SID value.
            Used by response messages only (first byte).

        :raise ValueError: Missing or provided SID/RSID value cannot be handled by this service.
        :raise InconsistencyError: Value only for `NRC`

        :return: Payload of a diagnostic message created from provided data records values.
        """
        if rsid == ResponseSID.NegativeResponse and sid in {None, self.request_sid}:
            if set(data_records_values.keys()) != {"NRC"}:
                raise InconsistencyError("Value only for `NRC` Data Record shall be provided in case of "
                                         "negative response message. "
                                         f"Actual values: {data_records_values}")
            return self.encode_negative_response(nrc=data_records_values["NRC"])  # type: ignore
        if rsid == self.response_sid and sid is None:
            return self.encode_positive_response(data_records_values=data_records_values)
        if sid == self.request_sid and rsid is None:
            return self.encode_request(data_records_values=data_records_values)
        raise ValueError("Either SID or RSID value is missing or incorrect. Provided values: "
                         f"SID = {sid}. RSID = {rsid}.")

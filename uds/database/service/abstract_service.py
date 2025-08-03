"""Definition of UDS Service data encoding and decoding."""

__all__ = ["Service", "DataRecordOccurrencesValuesAlias", "DecodedMessageAlias"]

from typing import List, Sequence, Union, Set, Collection
from warnings import warn

from uds.message import RequestSID, ResponseSID, NRC
from uds.utilities import RawBytesAlias, validate_raw_bytes, InconsistentArgumentsError

from ..data_record import PhysicalValueAlias, AliasMessageStructure, AbstractConditionalDataRecord, DEFAULT_DIAGNOSTIC_MESSAGE_CONTINUATION, AbstractDataRecord

DecodedMessageAlias = List[PhysicalValueAlias]  # TODO
"""Alias for decoded information about a Diagnostic Message."""

DataRecordOccurrencesValuesAlias = Union[int, Sequence[int]]  # TODO
"""Alias for raw values of Data Records occurrences."""


class Service:
    """
    Translator for a single Diagnostic Service.

    Features:
     - contains structures of diagnostic messages (both request and response) for a single diagnostic service
     - provides tools for decoding meaningful information (physical values) from diagnostic messages
     - provides tools for creating diagnostic messages out of meaningful information (physical values)
    """

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
    def name(self) -> str:
        """Get name of this service."""
        return self.request_sid.name

    @property
    def request_sid(self) -> RequestSID:
        """Get Service Identifier (SID) value for this diagnostic service."""
        return self.__request_sid

    @request_sid.setter
    def request_sid(self, request_sid: RequestSID) -> None:
        """
        Set Service Identifier (SID) value for this diagnostic service.

        :param request_sid: SID value to set.
        """
        self.__request_sid = RequestSID.validate_member(request_sid)
        self.__response_sid = ResponseSID.validate_member(request_sid + 0x40)
        if self.__response_sid.name != self.__response_sid.name:
            raise InconsistentArgumentsError

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
        self.validate_message_continuation(request_structure)
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
        self.validate_message_continuation(response_structure)
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

    @staticmethod
    def _encode_message_continuation(structure, data_records_raw_values) -> bytearray:
        # TODO
        for data_record in structure:
            if isinstance(data_record, AbstractDataRecord):
                if data_record.is_reoccurring:
                    raw_values = data_records_raw_values.pop(data_record.name)
        # TODO

    @staticmethod
    def validate_message_continuation(value: AliasMessageStructure) -> None:
        """
        Validate whether the provided value is a structure of diagnostic message continuation.

        :param value: Value to check.
        """
        AbstractConditionalDataRecord.validate_message_continuation(value)

    def encode_request(self, data_records_raw_values) -> bytearray:  # TODO: annotation
        """
        Encode diagnostic message payload for this service's request message.

        :param data_records_raw_values: Raw value for each data record that is part of a service message.
            Use sequences to provide multiple raw values for each occurrence of a Data Record.

        :return: Payload of a request diagnostic message.
        """
        return (bytearray([self.request_sid]) +
                self._encode_message_continuation(structure=self.request_structure,
                                                  data_records_raw_values=data_records_raw_values))

    def encode_positive_response(self, data_records_raw_values) -> bytearray:  # TODO
        """
        Encode diagnostic message payload for this service's response message.

        :param data_records_raw_values: Raw value for each data record that is part of a service message.
            Use sequences to provide multiple raw values for each occurrence of a Data Record.

        :return: Payload of a response diagnostic message.
        """
        return (bytearray([self.response_sid])
                + self._encode_message_continuation(structure=self.response_structure,
                                                    data_records_raw_values=data_records_raw_values))

    def encode_negative_response(self, nrc: NRC) -> bytearray:
        # TODO
        if nrc not in self.supported_nrc:
            NRC.validate_member(nrc)
            warn(message=f"NRC code {nrc} is not supported by service {self.name}.")
        return bytearray([ResponseSID.NegativeResponse, self.request_sid, nrc])

    def decode_positive_response(self, payload: bytearray) -> DecodedMessageAlias:
        ...

    def decode_negative_response(self, payload) -> DecodedMessageAlias:
        ...




    def decode(self, payload: RawBytesAlias) -> DecodedMessageAlias:
        """
        Decode information carried by a diagnostic message for this diagnostic service.

        :param payload: Payload of a diagnostic message.

        :raise ValueError: Provided message payload does not start from a SID value for this service.

        :return: Decoded information from the provided diagnostic message payload.
        """
        if payload[0] == self.request_sid:
            return self.decode_request(payload)
        if payload[0] == self.response_sid:
            return self.decode_positive_response(payload)
        if payload[0] == ResponseSID.NegativeResponse:
            return self.decode_negative_response(payload)
        raise ValueError("Provided message does not belong to this diagnostic message")

    def encode(self,
               sid: Union[int, RequestSID, ResponseSID],
               data_records_raw_values) -> bytearray:  # TODO
        """
        Encode diagnostic message payload for this service.

        :param sid: Value of Service Identifier.
            It should be either equal to either to `request_sid`, `response_sid` or NegativeResponseSID (0x7F).
        :param data_records_raw_values: TODO

        :raise ValueError: Provided `sid` value is neither equal to request SID value nor response SID value for this
            diagnostic service.

        :return: Payload of a diagnostic message created from provided data records values.
        """
        if sid == self.request_sid:
            return self.encode_request(data_records_raw_values)
        if sid == self.response_sid:
            return self.encode_positive_response(data_records_raw_values)
        if sid == ResponseSID.NegativeResponse:
            return self.encode_negative_response(data_records_raw_values)
        raise ValueError("Provided SID value is neither request or response SID value for this service.")

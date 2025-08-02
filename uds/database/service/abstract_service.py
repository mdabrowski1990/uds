"""Definition of UDS Service data encoding and decoding."""

__all__ = ["AbstractService", "DataRecordOccurrencesValuesAlias", "DecodedMessageAlias"]

from abc import ABC, abstractmethod
from typing import List, Sequence, Union, Container, Set

from uds.message import RequestSID, ResponseSID, NRC
from uds.utilities import RawBytesAlias

from ..data_record import PhysicalValueAlias, AliasMessageStructure

DecodedMessageAlias = List[PhysicalValueAlias]
"""Alias for decoded information about a Diagnostic Message."""

DataRecordOccurrencesValuesAlias = Union[int, Sequence[int]]
"""Alias for raw values of Data Records occurrences."""


class Service:
    """Common interface for all diagnostic services."""

    def __init__(self,
                 request_sid: RequestSID,
                 response_sid: ResponseSID,
                 request_structure: AliasMessageStructure,
                 response_structure: AliasMessageStructure,
                 supported_nrc: Container[NRC] = set(NRC)) -> None:
        self.request_sid = request_sid
        self.response_sid = response_sid
        self.request_structure = request_structure
        self.response_structure = response_structure
        self.supported_nrc = supported_nrc

    @property
    def request_sid(self) -> RequestSID:
        """Service Identifier in request messages."""
        return self.__request_sid

    @request_sid.setter
    def request_sid(self, request_sid: RequestSID) -> None:
        self.__request_sid = RequestSID.validate_member(request_sid)

    @property
    def response_sid(self) -> ResponseSID:
        """Service Identifier in (positive) response messages."""
        return self.__response_sid

    @response_sid.setter
    def response_sid(self, response_sid: ResponseSID) -> None:
        self.__response_sid = ResponseSID.validate_member(response_sid)

    @property
    def request_structure(self) -> AliasMessageStructure:
        return self.__request_structure

    @request_structure.setter
    def request_structure(self, request_structure: AliasMessageStructure) -> None:
        self.validate_message_continuation(request_structure)
        self.__request_structure = request_structure

    @property
    def response_structure(self) -> AliasMessageStructure:
        return self.__response_structure

    @response_structure.setter
    def response_structure(self, response_structure: AliasMessageStructure) -> None:
        self.validate_message_continuation(response_structure)
        self.__response_structure = response_structure

    @property
    def supported_nrc(self) -> Set[NRC]:
        return self.__supported_nrc

    @supported_nrc.setter
    def supported_nrc(self, value: Container[NRC]) -> None:
        for nrc in value:
            NRC.validate_member(nrc)
        self.__supported_nrc = set(value)





    @staticmethod
    def validate_message_continuation(value: AliasMessageStructure) -> None:
        """
        Validate whether the provided value is structure of diagnostic message continuation.

        :param value: Value to check

        :raise TypeError: Provided value is not a sequence.
        :raise ValueError: At least one element of the provided sequence is not an instance of AbstractDataRecord
            or AbstractConditionalDataRecord class.
        """
        if not isinstance(value, Sequence):
            raise TypeError("Provided value is not a sequence")
        if not all(isinstance(element, (AbstractDataRecord, AbstractConditionalDataRecord)) for element in value):
            raise ValueError("At least one element is not an instance of AbstractDataRecord class.")


    def decode(self, payload: RawBytesAlias) -> DecodedMessageAlias:
        """
        Decode physical values carried in payload of a diagnostic message.

        :param payload: Payload of a diagnostic message.

        :return: Decoded Data Records values from provided diagnostic message.
        """

    def encode(self,
               sid: Union[int, RequestSID, ResponseSID],
               **data_records_raw_values: DataRecordOccurrencesValuesAlias) -> bytearray:
        """
        Encode diagnostic message payload for this service.

        :param sid: Value of Service Identifier. It should be either equal to either `request_sid` or `response_sid`.
        :param data_records_raw_values: Raw value for each data record that is part of a service message.
            Use sequences to provide multiple raw values for each occurrence of a Data Record.

        :raise ValueError: Provided `sid` value is neither equal to request SID value nor response SID value for this
            diagnostic service.

        :return: Payload of a diagnostic message.
        """
        if sid == self.request_sid:
            return self.encode_request(**data_records_raw_values)
        if sid == self.response_sid:
            return self.encode_response(**data_records_raw_values)
        raise ValueError("Provided SID value is neither request or response SID value for this service.")

    def encode_request(self, **data_records_raw_values: DataRecordOccurrencesValuesAlias) -> bytearray:
        """
        Encode diagnostic message payload for this service's request message.

        :param data_records_raw_values: Raw value for each data record that is part of a service message.
            Use sequences to provide multiple raw values for each occurrence of a Data Record.

        :return: Payload of a request diagnostic message.
        """

    def encode_response(self, **data_records_raw_values: DataRecordOccurrencesValuesAlias) -> bytearray:
        """
        Encode diagnostic message payload for this service's response message.

        :param data_records_raw_values: Raw value for each data record that is part of a service message.
            Use sequences to provide multiple raw values for each occurrence of a Data Record.

        :return: Payload of a response diagnostic message.
        """

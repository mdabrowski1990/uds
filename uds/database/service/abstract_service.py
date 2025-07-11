"""Definition of UDS Service data encoding and decoding."""

__all__ = ["AbstractService", "DataRecordOccurrencesValuesAlias", "DecodedMessageAlias"]

from abc import ABC, abstractmethod
from typing import List, Union, Sequence

from uds.message import RequestSID, ResponseSID
from uds.utilities import RawBytesAlias

from ..data_record import SingleOccurrenceInfo, MultipleOccurrencesInfo

DecodedMessageAlias = List[Union[SingleOccurrenceInfo, MultipleOccurrencesInfo]]
"""Alias for decoded information about a Diagnostic Message."""

DataRecordOccurrencesValuesAlias = Union[int, Sequence[int]]
"""Alias for raw values of Data Records occurrences."""


class AbstractService(ABC):
    """Common interface for all diagnostic services."""

    @property  # noqa: F841
    @abstractmethod
    def request_sid(self) -> RequestSID:
        """Service Identifier in request messages."""

    @property  # noqa: F841
    @abstractmethod
    def response_sid(self) -> ResponseSID:
        """Service Identifier in (positive) response messages."""

    @abstractmethod
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

    @abstractmethod
    def encode_request(self, **data_records_raw_values: DataRecordOccurrencesValuesAlias) -> bytearray:
        """
        Encode diagnostic message payload for this service's request message.

        :param data_records_raw_values: Raw value for each data record that is part of a service message.
            Use sequences to provide multiple raw values for each occurrence of a Data Record.

        :return: Payload of a request diagnostic message.
        """

    @abstractmethod
    def encode_response(self, **data_records_raw_values: DataRecordOccurrencesValuesAlias) -> bytearray:
        """
        Encode diagnostic message payload for this service's response message.

        :param data_records_raw_values: Raw value for each data record that is part of a service message.
            Use sequences to provide multiple raw values for each occurrence of a Data Record.

        :return: Payload of a response diagnostic message.
        """

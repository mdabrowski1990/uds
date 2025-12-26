"""Implementation of UDS messages translator for data encoding and decoding."""

__all__ = ["Translator"]

from types import MappingProxyType
from typing import Collection, Dict, FrozenSet, Mapping, Optional, Union

from uds.message import RequestSID, ResponseSID, UdsMessage, UdsMessageRecord
from uds.utilities import InconsistencyError

from .service import DataRecordsValuesAlias, DecodedMessageAlias, Service


class Translator:
    """
    Translator for UDS messages.

    Features:
     - configuration with Services Translators that are ECU/OEM specific
     - building diagnostic messages (requests, positive and negative responses)
     - extracting meaningful information from diagnostic messages payload
    """

    def __init__(self, services: Collection[Service]) -> None:
        """
        Configure Translator.

        :param services: Services translators to use.
        """
        self.services = services

    @property
    def services(self) -> FrozenSet[Service]:
        """Get diagnostic services translators."""
        return self.__services

    @services.setter
    def services(self, value: Collection[Service]) -> None:
        """
        Set diagnostic services translators.

        :param value: Diagnostic services translators to set.

        :raise TypeError: Provided value is not a collection.
        :raise ValueError: Provided value does not contain collection of Service instances only.
        :raise InconsistencyError: Multiple translators were provided for at least one Service.
        """
        if not isinstance(value, Collection):
            raise TypeError(f"Provided value is not a collection. Actual type: {type(value)}.")
        services_mapping: Dict[Union[RequestSID, ResponseSID], Service] = {}
        for service in value:
            if not isinstance(service, Service):
                raise ValueError("At least one collection element is not instance of Service class.")
            if service.request_sid in services_mapping or service.response_sid in services_mapping:
                raise InconsistencyError("Multiple translators were provided for Service with "
                                         f"SID = {service.request_sid} or RSID = {service.response_sid}.")
            services_mapping[service.request_sid] = service
            services_mapping[service.response_sid] = service
        self.__services = frozenset(value)
        self.__services_mapping = MappingProxyType(services_mapping)

    @property
    def services_mapping(self) -> Mapping[Union[int, RequestSID, ResponseSID], Service]:
        """Get mapping from SID/RSID values to corresponding Service Translators."""
        return self.__services_mapping  # type: ignore

    def encode(self,
               data_records_values: DataRecordsValuesAlias,
               sid: Optional[RequestSID] = None,
               rsid: Optional[ResponseSID] = None) -> bytearray:
        """
        Encode diagnostic message payload from data records values.

        :param data_records_values: Mapping with Data Records values that are part of the message.
            Mapping keys are Data Records names.
            Mapping values are either a single occurrence or multiple occurrences values. Each occurrence can be
            a raw value or a mapping with children names and its corresponding values.
        :param sid: Request SID value.
            Used by request message (first byte) and negative response message (second byte).
        :param rsid: Response SID value.
            Used by response messages only (first byte).

        :return: Payload of a diagnostic message.
        """
        if rsid == ResponseSID.NegativeResponse and sid in self.services_mapping:
            return self.services_mapping[sid].encode_negative_response(nrc=data_records_values["NRC"])  # type: ignore
        if rsid in self.services_mapping and sid is None:
            return self.services_mapping[rsid].encode_positive_response(  # type: ignore
                data_records_values=data_records_values)
        if sid in self.services_mapping and rsid is None:
            return self.services_mapping[sid].encode_request(data_records_values=data_records_values)  # type: ignore
        raise ValueError("Either SID or RSID value is missing or incorrect. "
                         f"Provided values: SID = {sid}. RSID = {rsid}.")

    def decode(self, message: Union[UdsMessage, UdsMessageRecord]) -> DecodedMessageAlias:
        """
        Decode physical values carried in payload of a diagnostic message.

        :param message: A diagnostic message that is carrying payload to decode.

        :raise ValueError: This translator has no service implementation for provided diagnostic message SID.

        :return: Decoded Data Records values from provided diagnostic message.
        """
        if message.payload[0] == ResponseSID.NegativeResponse:
            sid = message.payload[1]
            return self.services_mapping[sid].decode_negative_response(message.payload)
        sid = message.payload[0]
        if sid not in self.services_mapping:
            raise ValueError("Database has no decoding defined for SID/RSID value of the provided message.")
        return self.services_mapping[sid].decode(message.payload)

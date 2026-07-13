"""Implementation of UDS messages translator for data encoding and decoding."""

__all__ = ["Translator"]

from collections.abc import Collection, Mapping
from copy import deepcopy
from types import MappingProxyType
from typing import Any

from uds.message import NEGATIVE_RESPONSE_MESSAGE_LENGTH, RequestSID, ResponseSID, SidAlias
from uds.utilities import InconsistencyError, RawBytesAlias, bytes_to_hex, validate_raw_bytes

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

    def __deepcopy__(self, memo: dict[int, Any]) -> Translator:
        """Get deep copy of the translator."""
        cls = self.__class__
        self_copy = cls.__new__(cls)
        memo[id(self)] = self_copy
        Translator.__init__(self_copy, ([deepcopy(service, memo=memo) for service in self.services]))
        return self_copy

    @property
    def services(self) -> frozenset[Service]:
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
        services_mapping: dict[SidAlias, Service] = {}
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
    def services_mapping(self) -> Mapping[SidAlias, Service]:
        """Get mapping from SID/RSID values to corresponding Service Translators."""
        return self.__services_mapping

    def encode(self,
               data_records_values: DataRecordsValuesAlias,
               sid: None | RequestSID = None,
               rsid: None | ResponseSID = None) -> bytearray:
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

    def decode(self, payload: RawBytesAlias) -> DecodedMessageAlias:
        """
        Decode physical values carried by given payload of a diagnostic message.

        :param payload: Payload of a diagnostic message.

        :raise ValueError: This translator has no service implementation for provided diagnostic message SID.

        :return: Decoded Data Records values.
        """
        validate_raw_bytes(payload, allow_empty=False)
        if payload[0] == ResponseSID.NegativeResponse:
            if len(payload) != NEGATIVE_RESPONSE_MESSAGE_LENGTH:
                raise ValueError(f"Negative response message payload has unexpected length. "
                                 f"Expected length: {NEGATIVE_RESPONSE_MESSAGE_LENGTH}. "
                                 f"Actual length: {len(payload)}. "
                                 f"Payload: {bytes_to_hex(payload)}.")
            sid = payload[1]
            if sid not in self.services_mapping:
                raise ValueError("Database has no decoding defined for SID/RSID value of the provided message.")
            return self.services_mapping[sid].decode_negative_response(payload)
        sid = payload[0]
        if sid not in self.services_mapping:
            raise ValueError("Database has no decoding defined for SID/RSID value of the provided message.")
        return self.services_mapping[sid].decode(payload)

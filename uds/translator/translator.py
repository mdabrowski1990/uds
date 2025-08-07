"""Definition of UDS messages translator for data encoding and decoding."""

__all__ = ["Translator"]

from typing import Dict, Union, Sequence, Mapping
from types import MappingProxyType

from uds.message import RequestSID, ResponseSID, UdsMessage, UdsMessageRecord

from .service import Service, DataRecordsValuesAlias, DecodedMessageAlias


class Translator:
    """Common interface and implementation for UDS message databases."""

    def __init__(self, services: Sequence[Service]) -> None:
        self.services = services

    @property
    def services(self) -> Sequence[Service]:
        return self.__services

    @services.setter
    def services(self, value: Sequence[Service]) -> None:
        # TODO: error handling
        self.__services = tuple(value)
        services_mapping = {}
        for service in self.__services:
            services_mapping[service.request_sid] = service
            services_mapping[service.response_sid] = service
        self.__services_mapping = MappingProxyType(services_mapping)

    @property
    def services_mapping(self) -> Mapping[int, Service]:
        return self.__services_mapping

    def encode(self, data_records_values: DataRecordsValuesAlias) -> bytearray:
        """
        Encode diagnostic message payload from data records values.

        :param data_records_values: Mapping with Data Records values that are part of the message.
            Mapping keys are Data Records names.
            Mapping values are either a single occurrence or multiple occurrences values. Each occurrence can be
            a raw value or a mapping with children names and its corresponding values.

        :return: Payload of a diagnostic message.
        """
        data_records_values_dict = dict(data_records_values)
        sid = data_records_values_dict.pop("SID", None)
        rsid = data_records_values_dict.pop("RSID", None)
        if rsid == ResponseSID.NegativeResponse:
            return self.services_mapping[sid].encode_negative_response(
                nrc=data_records_values_dict["NRC"])  # type: ignore
        if rsid is None:
            return self.services_mapping[sid].encode_request(data_records_values=data_records_values_dict)
        if sid is None:
            return self.services_mapping[rsid].encode_positive_response(data_records_values=data_records_values_dict)
        raise ValueError("Either SID or RSID value is missing or incorrect. Provided values: "
                         f"SID = {sid}. RSID = {rsid}.")

    def decode(self, message: Union[UdsMessage, UdsMessageRecord]) -> DecodedMessageAlias:
        """
        Decode physical values carried in payload of a diagnostic message.

        :param message: A diagnostic message that is carrying payload to decode.

        :raise ValueError: This translator has no service implementation for provided diagnostic message SID.

        :return: Decoded Data Records values from provided diagnostic message.
        """
        if message.payload[0] == ResponseSID.NegativeResponse:
            sid = message.payload[1]
            return self.services[sid].decode_negative_response(message.payload)
        sid = message.payload[0]
        if sid not in self.services:
            raise ValueError("Database has no decoding defined for SID/RSID value of the provided message.")
        return self.services[sid].decode(message.payload)

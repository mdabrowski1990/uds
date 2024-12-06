"""Definition of UDS Service data encoding and decoding."""

__all__ = ["AbstractService", "DataRecordValueAlias"]

from abc import ABC, abstractmethod
from typing import Dict, Sequence, List, Union

from uds.message import RequestSID, ResponseSID
from uds.utilities import RawBytesAlias, RawBytesListAlias

from ..data_record import DecodedDataRecord

DataRecordValueAlias = Union[
    int,  # raw value
    float,  # physical value calculated through formula
    str,  # text value decoded either through raw value mapping or text encoding
    Dict[str, "DataRecordValueAlias"],  # value of container's children
    Sequence[Dict[str, "DataRecordValueAlias"]],  # multiple records' values
]
"Alias of input with Data Records values."


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
    def decode(self, payload: RawBytesAlias) -> List[DecodedDataRecord]:
        """
        Decode physical values carried in payload of a diagnostic message.

        :param payload: Payload of a diagnostic message.

        :return: Decoded Data Records values from provided diagnostic message.
        """

    def encode(self, sid: int, **data_records_values: DataRecordValueAlias) -> RawBytesListAlias:
        # TODO
        if sid == self.request_sid:
            return self.encode_request(**data_records_values)
        if sid == self.response_sid:
            return self.encode_response(**data_records_values)
        raise ValueError

    @abstractmethod
    def encode_request(self, **data_records_values: DataRecordValueAlias) -> RawBytesListAlias:
        """
        Encode diagnostic message payload from data records values.

        :param data_records_values: Value for each Data Record that is part a service message.

            Each type represent other data:

            - int type - raw value of a Data Record
            - float type - physical value of a Data Record
            - str type - text value of a Data Record
            - sequence - contains values for children Data Records
            - dict type - values of children Data Records

            .. warning:: Providing physical value as float might sometime cause issues due
                `floating-point precision <https://docs.python.org/3/tutorial/floatingpoint.html>`_.
                The closest raw value would be evaluated and put into a payload.

                To avoid rounding, provide raw value (int type).

        :return: Payload of a diagnostic message.
        """

    @abstractmethod
    def encode_response(self, **data_records_values: DataRecordValueAlias) -> RawBytesListAlias:
        """
        Encode diagnostic message payload from data records values.

        :param data_records_values: Value for each Data Record that is part a service message.

            Each type represent other data:

            - int type - raw value of a Data Record
            - float type - physical value of a Data Record
            - str type - text value of a Data Record
            - sequence - contains values for children Data Records
            - dict type - values of children Data Records

            .. warning:: Providing physical value as float might sometime cause issues due
                `floating-point precision <https://docs.python.org/3/tutorial/floatingpoint.html>`_.
                The closest raw value would be evaluated and put into a payload.

                To avoid rounding, provide raw value (int type).

        :return: Payload of a diagnostic message.
        """

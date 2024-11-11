"""Definition of UDS Service data encoding and decoding."""

__all__ = ["AbstractService"]

from abc import ABC, abstractmethod
from typing import Dict, Iterable, List, Union

from uds.message import RequestSID, ResponseSID
from uds.utilities import RawBytesAlias, RawBytesListAlias

from ..abstract_data_record import DecodedDataRecord

DataRecordValueAlias = Union[int, float, str, Iterable[Dict[str, "DataRecordValueAlias"]]]
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
        Decode physical values carried by a diagnostic message.

        :param payload: Payload of a diagnostic message.

        :return: Decoded values for all Data Records.
        """

    @abstractmethod
    def encode(self, **data_records_values: DataRecordValueAlias) -> RawBytesListAlias:  # noqa: F841
        """
        Encode diagnostic message from data records values.

        :param data_records_values: Value for each Data Record that is part a service message.
            Each type represent other data:
                - int type - raw value of a Data Record
                - float type - physical value of a Data Record
                - str type - text value of a Data Record
                - iterable type - contains values for children Data Records

            .. warning:: Providing physical value as float might sometime cause issues due
                :ref:`floating-point precision <https://docs.python.org/3/tutorial/floatingpoint.html>`.
                The closest raw value would be evaluated and put into a payload.

                To avoid rounding, provide raw value (int type).

        :return: Payload of a diagnostic message.
        """

"""Definition of UDS messages database for data encoding and decoding."""

__all__ = ["AbstractService"]

from abc import ABC, abstractmethod
from typing import Dict, List, Union

from uds.message import RequestSID, ResponseSID, UdsMessage, UdsMessageRecord
from uds.utilities import RawBytesListAlias

from .services import AbstractService

from .abstract_data_record import DecodedDataRecord


class AbstractDatabase(ABC):
    """Common interface and implementation for UDS message databases."""

    @property
    @abstractmethod
    def services(self) -> Dict[int, AbstractService]:
        """
        Get mapping of diagnostic services.

        Keys are SID (int) values.
        Values are diagnostic services with dedicated decoding and encoding implementation.
        """

    def encode(self,
               sid: Union[int, RequestSID, ResponseSID],
               **data_records_values: DataRecordValueAlias) -> RawBytesListAlias:
        """
        Encode diagnostic message payload from data records values.

        :param sid: Service Identifier of a diagnostic message.
        :param data_records_values: Value for each Data Record that is part a service message.
            Each type represent other data:
                - int type - raw value of a Data Record
                - float type - physical value of a Data Record
                - str type - text value of a Data Record
                - iterable type - contains values for children Data Records
                - dict type - values of children Data Records

            .. warning:: Providing physical value as float might sometime cause issues due
                :ref:`floating-point precision <https://docs.python.org/3/tutorial/floatingpoint.html>`.
                The closest raw value would be evaluated and put into a payload.

                To avoid rounding, provide raw value (int type).

        :raise TypeError: Provided SID value is neither int, RequestSID nor ResponseSID type.
        :raise ValueError: This database has no implementation for provided SID value.

        :return: Payload of a diagnostic message.
        """
        if isinstance(sid, (RequestSID, ResponseSID)):
            sid_int = sid.value
        elif isinstance(sid, int):
            sid_int = sid
        else:
            raise TypeError
        if sid_int not in self.services:
            raise ValueError
        return self.services[sid_int].encode(**data_records_values)

    def decode(self, message: Union[UdsMessage, UdsMessageRecord]) -> List[DecodedDataRecord]:
        """
        Decode physical values carried in payload of a diagnostic message.

        :param message: A diagnostic message that is carrying payload to decode.

        :return: Decoded Data Records values from provided diagnostic message.
        """
        sid_int = message.payload[0]
        return self.services[sid_int].decode(message.payload)

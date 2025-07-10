"""Definition of UDS messages database for data encoding and decoding."""

__all__ = ["AbstractDatabase"]

from abc import ABC, abstractmethod
from typing import Dict, List, Union

from uds.message import RequestSID, ResponseSID, UdsMessage, UdsMessageRecord

from .data_record import DataRecordValueAlias, DecodedDataRecord
from .service import AbstractService


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
               **data_records_values: DataRecordValueAlias) -> bytearray:
        """
        Encode diagnostic message payload from data records values.

        :param sid: Service Identifier of a diagnostic message.
        :param data_records_values: Value for each Data Record that is part a service message.

        :raise TypeError: Provided SID value is neither int, RequestSID nor ResponseSID type.
        :raise ValueError: This database has no implementation for provided SID value.

        :return: Payload of a diagnostic message.
        """
        if not isinstance(sid, int):
            raise TypeError("Provided SID value is not int type.")
        if sid not in self.services:
            raise ValueError("Database has no encoding defined for provided SID value.")
        return self.services[sid].encode(sid=sid, **data_records_values)

    def decode(self, message: Union[UdsMessage, UdsMessageRecord]) -> List[DecodedDataRecord]:
        """
        Decode physical values carried in payload of a diagnostic message.

        :param message: A diagnostic message that is carrying payload to decode.

        :raise ValueError: This database has no service implementation for provided diagnostic message SID.

        :return: Decoded Data Records values from provided diagnostic message.
        """
        sid = message.payload[0]
        if sid not in self.services:
            raise ValueError("Database has no decoding defined for SID value of provided message.")
        return self.services[sid].decode(message.payload)

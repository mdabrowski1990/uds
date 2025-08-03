# """Definition of UDS messages database for data encoding and decoding."""
#
# __all__ = ["Database"]
#
# from typing import Dict, Union, Sequence
#
# from uds.message import RequestSID, ResponseSID, UdsMessage, UdsMessageRecord
#
# from .service import AbstractService, DataRecordOccurrencesValuesAlias, DecodedMessageAlias
#
#
# class Database:
#     """Common interface and implementation for UDS message databases."""
#
#     def __init__(self, services: Sequence[]) -> None:
#
#     @property
#     @abstractmethod
#     def services(self) -> Dict[int, AbstractService]:
#         """
#         Get mapping of diagnostic services.
#
#         Keys are SID (int) values.
#         Values are diagnostic services with dedicated decoding and encoding implementation.
#         """
#
#     def encode(self,
#                sid: Union[int, RequestSID, ResponseSID],
#                **data_records_raw_values: DataRecordOccurrencesValuesAlias) -> bytearray:
#         """
#         Encode diagnostic message payload from data records values.
#
#         :param sid: Service Identifier of a diagnostic message.
#         :param data_records_raw_values: Raw value for each data record that is part of a service message.
#             Use sequences to provide multiple raw values for each occurrence of a Data Record.
#
#         :raise TypeError: Provided SID value is neither int, RequestSID nor ResponseSID type.
#         :raise ValueError: This database has no implementation for provided SID value.
#
#         :return: Payload of a diagnostic message.
#         """
#         if not isinstance(sid, int):
#             raise TypeError("Provided SID value is not int type.")
#         if sid not in self.services:
#             raise ValueError("Database has no encoding defined for provided SID value.")
#         return self.services[sid].encode(sid=sid, **data_records_raw_values)
#
#     def decode(self, message: Union[UdsMessage, UdsMessageRecord]) -> DecodedMessageAlias:
#         """
#         Decode physical values carried in payload of a diagnostic message.
#
#         :param message: A diagnostic message that is carrying payload to decode.
#
#         :raise ValueError: This database has no service implementation for provided diagnostic message SID.
#
#         :return: Decoded Data Records values from provided diagnostic message.
#         """
#         sid = message.payload[0]
#         if sid not in self.services:
#             raise ValueError("Database has no decoding defined for SID value of provided message.")
#         return self.services[sid].decode(message.payload)

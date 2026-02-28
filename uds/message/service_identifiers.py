"""
Service Identifier (SID) data parameter implementation.

.. note:: :ref:`Service Identifiers <knowledge-base-sid>` values and their meanings are defined by ISO 14229-1
    and SAE J1979 standards.
"""

__all__ = [
    "ALL_REQUEST_SIDS", "ALL_RESPONSE_SIDS",
    "SERVICES_WITH_SUBFUNCTION",
    "RESPONSE_REQUEST_SID_DIFF",
    "RequestSID", "ResponseSID",
    "UnrecognizedSIDWarning",
    "add_sid",
]

from typing import Tuple
from warnings import warn

from aenum import unique

from uds.utilities import ByteEnum, ExtendableEnum, InconsistencyError, RawBytesSetAlias, ValidatedEnum

RESPONSE_REQUEST_SID_DIFF: int = 0x40
"""Difference between request and response SID values (SID = RSID + 0x40)."""

# reserved SID values
_REQUEST_SIDS_DEFINED_BY_SAEJ1979 = set(range(0x01, 0x10))
_RESPONSE_SIDS_DEFINED_BY_SAEJ1979 = set(range(0x41, 0x50))
_REQUEST_SIDS_DEFINED_BY_ISO_14229 = set(range(0x10, 0x3F)).union(set(range(0x83, 0x89)), set(range(0xBA, 0xBF)))
_RESPONSE_SIDS_DEFINED_BY_ISO_14229 = set(range(0x50, 0x80)).union(set(range(0xC3, 0xC9)), set(range(0xFA, 0xFF)))

# all supported SID values according to UDS
ALL_REQUEST_SIDS: RawBytesSetAlias = _REQUEST_SIDS_DEFINED_BY_SAEJ1979.union(_REQUEST_SIDS_DEFINED_BY_ISO_14229)
"""Set with all possible values of Request SID data parameter according to SAE J1979 and ISO 14229 standards."""
ALL_RESPONSE_SIDS: RawBytesSetAlias = _RESPONSE_SIDS_DEFINED_BY_SAEJ1979.union(_RESPONSE_SIDS_DEFINED_BY_ISO_14229)
"""Set with all possible values of Response SID data parameter according to SAE J1979 and ISO 14229 standards."""


class UnrecognizedSIDWarning(Warning):
    """
    Warning about SID value that is legit but not recognized by the package.

    .. note:: If you want to register a SID value, you need to define members (for this SID) manually using
        :meth:`~uds.utilities.enums.ExtendableEnum.add_member` method
        (on :class:`~uds.message.service_identifiers.RequestSID` and
        :class:`~uds.message.service_identifiers.ResponseSID` classes).

        You can also create feature request in the UDS project
        `issues management system <https://github.com/mdabrowski1990/uds/issues/new/choose>`_ to register
        a SID value (for which this warning was raised).
    """


@unique
class RequestSID(ValidatedEnum, ExtendableEnum, ByteEnum):
    """
    Request Service Identifier values.

    .. note:: Request :ref:`SID <knowledge-base-sid>` is always the first payload byte of all request message.
    """

    # pylint: disable=invalid-name

    @classmethod
    def is_request_sid(cls, value: int) -> bool:
        """
        Check whether given value is Service Identifier (SID).

        :param value: Value to check.

        :return: True if value is valid SID, else False.
        """
        if value in ALL_REQUEST_SIDS:
            if not cls.is_member(value):
                warn(message=f"SID 0x{value:X} is not recognized by this version of the package. "
                             "Define it manually using `add_member` method.",
                     category=UnrecognizedSIDWarning)
            return True
        return False

    # Diagnostic and communication management - more information in ISO 14229-1:2013 (obsolete), chapter 9
    AccessTimingParameter: "RequestSID" = 0x83  # type: ignore
    # Diagnostic and communication management - more information in ISO 14229-1:2020, chapter 10
    DiagnosticSessionControl: "RequestSID" = 0x10  # type: ignore
    ECUReset: "RequestSID" = 0x11  # type: ignore
    SecurityAccess: "RequestSID" = 0x27  # type: ignore
    CommunicationControl: "RequestSID" = 0x28  # type: ignore
    Authentication: "RequestSID" = 0x29  # type: ignore
    TesterPresent: "RequestSID" = 0x3E  # type: ignore
    ControlDTCSetting: "RequestSID" = 0x85  # type: ignore
    ResponseOnEvent: "RequestSID" = 0x86  # type: ignore
    LinkControl: "RequestSID" = 0x87  # type: ignore
    # Data transmission - more information in ISO 14229-1:2020, chapter 11
    ReadDataByIdentifier: "RequestSID" = 0x22  # type: ignore
    ReadMemoryByAddress: "RequestSID" = 0x23  # type: ignore
    ReadScalingDataByIdentifier: "RequestSID" = 0x24  # type: ignore
    ReadDataByPeriodicIdentifier: "RequestSID" = 0x2A  # type: ignore
    DynamicallyDefineDataIdentifier: "RequestSID" = 0x2C  # type: ignore
    WriteDataByIdentifier: "RequestSID" = 0x2E  # type: ignore
    WriteMemoryByAddress: "RequestSID" = 0x3D  # type: ignore
    # Stored data transmission - more information in ISO 14229-1:2020, chapter 12
    ClearDiagnosticInformation: "RequestSID" = 0x14  # type: ignore
    ReadDTCInformation: "RequestSID" = 0x19  # type: ignore
    # InputOutput control - more information in ISO 14229-1:2020, chapter 13
    InputOutputControlByIdentifier: "RequestSID" = 0x2F  # type: ignore
    # Routine - more information in ISO 14229-1:2020, chapter 14
    RoutineControl: "RequestSID" = 0x31  # type: ignore
    # Upload download - more information in ISO 14229-1:2020, chapter 15
    RequestDownload: "RequestSID" = 0x34  # type: ignore
    RequestUpload: "RequestSID" = 0x35  # type: ignore
    TransferData: "RequestSID" = 0x36  # type: ignore
    RequestTransferExit: "RequestSID" = 0x37  # type: ignore
    RequestFileTransfer: "RequestSID" = 0x38  # type: ignore
    # Security sub-layer - more information in ISO 14229-1:2020, chapter 16
    SecuredDataTransmission: "RequestSID" = 0x84  # type: ignore


@unique
class ResponseSID(ValidatedEnum, ExtendableEnum, ByteEnum):
    """
    Response Service Identifier values.

    .. note:: Response :ref:`SID <knowledge-base-sid>` is always the first payload byte of all request message.

    .. warning:: This enum contains multiple members (for all the services as
        :class:`~uds.message.service_identifiers.RequestSID`), but most of them are dynamically (implicitly) added and
        invisible in the documentation.
    """

    # pylint: disable=invalid-name

    NegativeResponse: "ResponseSID" = 0x7F  # type: ignore
    # Diagnostic and communication management - more information in ISO 14229-1:2013 (obsolete), chapter 9
    AccessTimingParameter: "ResponseSID" = RequestSID.AccessTimingParameter + RESPONSE_REQUEST_SID_DIFF
    # Diagnostic and communication management - more information in ISO 14229-1:2020, chapter 10
    DiagnosticSessionControl: "ResponseSID" = RequestSID.DiagnosticSessionControl + RESPONSE_REQUEST_SID_DIFF
    ECUReset: "ResponseSID" = RequestSID.ECUReset + RESPONSE_REQUEST_SID_DIFF
    SecurityAccess: "ResponseSID" = RequestSID.SecurityAccess + RESPONSE_REQUEST_SID_DIFF
    CommunicationControl: "ResponseSID" = RequestSID.CommunicationControl + RESPONSE_REQUEST_SID_DIFF
    Authentication: "ResponseSID" = RequestSID.Authentication + RESPONSE_REQUEST_SID_DIFF
    TesterPresent: "ResponseSID" = RequestSID.TesterPresent + RESPONSE_REQUEST_SID_DIFF
    ControlDTCSetting: "ResponseSID" = RequestSID.ControlDTCSetting + RESPONSE_REQUEST_SID_DIFF
    ResponseOnEvent: "ResponseSID" = RequestSID.ResponseOnEvent + RESPONSE_REQUEST_SID_DIFF
    LinkControl: "ResponseSID" = RequestSID.LinkControl + RESPONSE_REQUEST_SID_DIFF
    # Data transmission - more information in ISO 14229-1:2020, chapter 11
    ReadDataByIdentifier: "ResponseSID" = RequestSID.ReadDataByIdentifier + RESPONSE_REQUEST_SID_DIFF
    ReadMemoryByAddress: "ResponseSID" = RequestSID.ReadMemoryByAddress + RESPONSE_REQUEST_SID_DIFF
    ReadScalingDataByIdentifier: "ResponseSID" = RequestSID.ReadScalingDataByIdentifier + RESPONSE_REQUEST_SID_DIFF
    ReadDataByPeriodicIdentifier: "ResponseSID" = RequestSID.ReadDataByPeriodicIdentifier + RESPONSE_REQUEST_SID_DIFF
    DynamicallyDefineDataIdentifier: "ResponseSID" = (RequestSID.DynamicallyDefineDataIdentifier
                                                      + RESPONSE_REQUEST_SID_DIFF)
    WriteDataByIdentifier: "ResponseSID" = RequestSID.WriteDataByIdentifier + RESPONSE_REQUEST_SID_DIFF
    WriteMemoryByAddress: "ResponseSID" = RequestSID.WriteMemoryByAddress + RESPONSE_REQUEST_SID_DIFF
    # Stored data transmission - more information in ISO 14229-1:2020, chapter 12
    ClearDiagnosticInformation: "ResponseSID" = RequestSID.ClearDiagnosticInformation + RESPONSE_REQUEST_SID_DIFF
    ReadDTCInformation: "ResponseSID" = RequestSID.ReadDTCInformation + RESPONSE_REQUEST_SID_DIFF
    # InputOutput control - more information in ISO 14229-1:2020, chapter 13
    InputOutputControlByIdentifier: "ResponseSID" = (RequestSID.InputOutputControlByIdentifier
                                                     + RESPONSE_REQUEST_SID_DIFF)
    # Routine - more information in ISO 14229-1:2020, chapter 14
    RoutineControl: "ResponseSID" = RequestSID.RoutineControl + RESPONSE_REQUEST_SID_DIFF
    # Upload download - more information in ISO 14229-1:2020, chapter 15
    RequestDownload: "ResponseSID" = RequestSID.RequestDownload + RESPONSE_REQUEST_SID_DIFF
    RequestUpload: "ResponseSID" = RequestSID.RequestUpload + RESPONSE_REQUEST_SID_DIFF
    TransferData: "ResponseSID" = RequestSID.TransferData + RESPONSE_REQUEST_SID_DIFF
    RequestTransferExit: "ResponseSID" = RequestSID.RequestTransferExit + RESPONSE_REQUEST_SID_DIFF
    RequestFileTransfer: "ResponseSID" = RequestSID.RequestFileTransfer + RESPONSE_REQUEST_SID_DIFF
    # Security sub-layer - more information in ISO 14229-1:2020, chapter 16
    SecuredDataTransmission: "ResponseSID" = RequestSID.SecuredDataTransmission + RESPONSE_REQUEST_SID_DIFF

    @classmethod
    def is_response_sid(cls, value: int) -> bool:
        """
        Check whether given value is Response Service Identifier (RSID).

        :param value: Value to check.

        :return: True if value is valid RSID, else False.
        """
        if value in ALL_RESPONSE_SIDS:
            if not cls.is_member(value):
                warn(message=f"RSID 0x{value:X} is not recognized by this version of the package. "
                             "Define it manually using `add_member` method.",
                     category=UnrecognizedSIDWarning)
            return True
        return False


SERVICES_WITH_SUBFUNCTION = {
    RequestSID.DiagnosticSessionControl,
    ResponseSID.DiagnosticSessionControl,
    RequestSID.ECUReset,
    ResponseSID.ECUReset,
    RequestSID.ReadDTCInformation,
    ResponseSID.ReadDTCInformation,
    RequestSID.SecurityAccess,
    ResponseSID.SecurityAccess,
    RequestSID.CommunicationControl,
    ResponseSID.CommunicationControl,
    RequestSID.Authentication,
    ResponseSID.Authentication,
    RequestSID.DynamicallyDefineDataIdentifier,
    ResponseSID.DynamicallyDefineDataIdentifier,
    RequestSID.RoutineControl,
    ResponseSID.RoutineControl,
    RequestSID.TesterPresent,
    ResponseSID.TesterPresent,
    RequestSID.AccessTimingParameter,
    ResponseSID.AccessTimingParameter,
    RequestSID.ControlDTCSetting,
    ResponseSID.ControlDTCSetting,
    RequestSID.ResponseOnEvent,
    ResponseSID.ResponseOnEvent,
    RequestSID.LinkControl,
    ResponseSID.LinkControl,
}
"""SID and RSID values for services that contain sub-function in their message format."""


def add_sid(sid: int, name: str) -> Tuple[RequestSID, ResponseSID]:
    """
    Define a new SID.

    :param sid: Service Identifier value.
    :param name: Name of the Service.

    :raise TypeError: Incorrect value type provided.
    :raise ValueError: Incorrect value provided.
    :raise InconsistencyError: Member for provided SID is already defined.

    :return: Defined RequestSID and ResponseSID members.
    """
    if not isinstance(sid, int):
        raise TypeError(f"Provided sid value is not int type. Actual type: {type(sid)}.")
    if not isinstance(name, str):
        raise TypeError(f"Provided name value is not str type. Actual type: {type(name)}.")
    if sid not in ALL_REQUEST_SIDS:
        raise ValueError(f"Provided sid value is not a SID value. Actual value: 0x{sid:02X}")
    if RequestSID.is_member(sid):
        raise InconsistencyError(f"Member for SID 0x{sid:02X} is already defined.")
    rsid = sid + RESPONSE_REQUEST_SID_DIFF
    if ResponseSID.is_member(rsid):
        raise InconsistencyError(f"Member for RSID 0x{rsid:02X} is already defined.")
    return RequestSID.add_member(name=name, value=sid), ResponseSID.add_member(name=name, value=rsid)

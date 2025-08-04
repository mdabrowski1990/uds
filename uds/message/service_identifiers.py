"""
Service Identifier (SID) data parameter implementation.

.. note:: :ref:`Service Identifiers <knowledge-base-sid>` values and their meanings are defined by ISO 14229-1
    and SAE J1979 standards.
"""

__all__ = ["RESPONSE_REQUEST_SID_DIFF","ALL_REQUEST_SIDS", "ALL_RESPONSE_SIDS",
           "RequestSID", "ResponseSID", "UnrecognizedSIDWarning"]

from warnings import warn

from aenum import unique

from uds.utilities import ByteEnum, ExtendableEnum, RawBytesSetAlias, ValidatedEnum

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

    @classmethod
    def is_request_sid(cls, value: int) -> bool:
        """
        Check whether given value is Service Identifier (SID).

        :param value: Value to check.

        :return: True if value is valid SID, else False.
        """
        if value in ALL_REQUEST_SIDS:
            if not cls.is_member(value):
                warn(message=f"SID 0x{value:X} is not recognized by this version of the package.",
                     category=UnrecognizedSIDWarning)
            return True
        return False

    # Diagnostic and communication management - more information in ISO 14229-1:2020, chapter 10
    DiagnosticSessionControl: "RequestSID" = 0x10  # type: ignore  # noqa: F841
    ECUReset: "RequestSID" = 0x11  # type: ignore  # noqa: F841
    SecurityAccess: "RequestSID" = 0x27  # type: ignore  # noqa: F841
    CommunicationControl: "RequestSID" = 0x28  # type: ignore  # noqa: F841
    Authentication: "RequestSID" = 0x29  # type: ignore  # noqa: F841
    TesterPresent: "RequestSID" = 0x3E  # type: ignore  # noqa: F841
    ControlDTCSetting: "RequestSID" = 0x85  # type: ignore  # noqa: F841
    ResponseOnEvent: "RequestSID" = 0x86  # type: ignore  # noqa: F841
    LinkControl: "RequestSID" = 0x87  # type: ignore  # noqa: F841
    # Data transmission - more information in ISO 14229-1:2020, chapter 11
    ReadDataByIdentifier: "RequestSID" = 0x22  # type: ignore  # noqa: F841
    ReadMemoryByAddress: "RequestSID" = 0x23  # type: ignore  # noqa: F841
    ReadScalingDataByIdentifier: "RequestSID" = 0x24  # type: ignore  # noqa: F841
    ReadDataByPeriodicIdentifier: "RequestSID" = 0x2A  # type: ignore  # noqa: F841
    DynamicallyDefineDataIdentifier: "RequestSID" = 0x2C  # type: ignore  # noqa: F841
    WriteDataByIdentifier: "RequestSID" = 0x2E  # type: ignore  # noqa: F841
    WriteMemoryByAddress: "RequestSID" = 0x3D  # type: ignore  # noqa: F841
    # Stored data transmission - more information in ISO 14229-1:2020, chapter 12
    ClearDiagnosticInformation: "RequestSID" = 0x14  # type: ignore  # noqa: F841
    ReadDTCInformation: "RequestSID" = 0x19  # type: ignore  # noqa: F841
    # InputOutput control - more information in ISO 14229-1:2020, chapter 13
    InputOutputControlByIdentifier: "RequestSID" = 0x2F  # type: ignore  # noqa: F841
    # Routine - more information in ISO 14229-1:2020, chapter 14
    RoutineControl: "RequestSID" = 0x31  # type: ignore  # noqa: F841
    # Upload download - more information in ISO 14229-1:2020, chapter 15
    RequestDownload: "RequestSID" = 0x34  # type: ignore  # noqa: F841
    RequestUpload: "RequestSID" = 0x35  # type: ignore  # noqa: F841
    TransferData: "RequestSID" = 0x36  # type: ignore  # noqa: F841
    RequestTransferExit: "RequestSID" = 0x37  # type: ignore  # noqa: F841
    RequestFileTransfer: "RequestSID" = 0x38  # type: ignore  # noqa: F841
    SecuredDataTransmission: "RequestSID" = 0x84  # type: ignore  # noqa: F841


@unique
class ResponseSID(ValidatedEnum, ExtendableEnum, ByteEnum):
    """
    Response Service Identifier values.

    .. note:: Response :ref:`SID <knowledge-base-sid>` is always the first payload byte of all request message.

    .. warning:: This enum contains multiple members (for all the services as
        :class:`~uds.message.service_identifiers.RequestSID`), but most of them are dynamically (implicitly) added and
        invisible in the documentation.
    """

    NegativeResponse: "ResponseSID" = 0x7F  # type: ignore  # noqa: F841

    @classmethod
    def is_response_sid(cls, value: int) -> bool:
        """
        Check whether given value is Response Service Identifier (RSID).

        :param value: Value to check.

        :return: True if value is valid RSID, else False.
        """
        if value in ALL_RESPONSE_SIDS:
            if not cls.is_member(value):
                warn(message=f"RSID 0x{value:X} is not recognized by this version of the package",
                     category=UnrecognizedSIDWarning)
            return True
        return False


# extend 'ResponseSID' with members that were defined in RequestSID
for request_sid_member in RequestSID:
    ResponseSID.add_member(request_sid_member.name, request_sid_member.value + RESPONSE_REQUEST_SID_DIFF)

"""
Service Identifier (SID) data parameter implementation.

.. note:: :ref:`Service Identifiers <knowledge-base-sid>` values and their meanings are defined by ISO 14229-1
    and SAE J1979 standards.
"""

__all__ = ["RESPONSE_REQUEST_SID_DIFF", "ALL_REQUEST_SIDS", "ALL_RESPONSE_SIDS",
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
        Return True if `value` is a valid request Service Identifier (SID) value.
        
        A value is considered a request SID if it belongs to the module-wide ALL_REQUEST_SIDS set.
        If the value is in that set but not a defined enum member of this class, an
        UnrecognizedSIDWarning is emitted to indicate the SID is legitimate but not registered here.
        
        Parameters:
            value (int): SID value (byte) to check.
        
        Returns:
            bool: True when `value` is a request SID, False otherwise.
        """
        if value in ALL_REQUEST_SIDS:
            if not cls.is_member(value):
                warn(message=f"SID 0x{value:X} is not recognized by this version of the package.",
                     category=UnrecognizedSIDWarning)
            return True
        return False

    # Diagnostic and communication management - more information in ISO 14229-1:2020, chapter 10
    DiagnosticSessionControl: "RequestSID" = 0x10  # type: ignore  # noqa: vulture
    ECUReset: "RequestSID" = 0x11  # type: ignore  # noqa: vulture
    SecurityAccess: "RequestSID" = 0x27  # type: ignore  # noqa: vulture
    CommunicationControl: "RequestSID" = 0x28  # type: ignore  # noqa: vulture
    Authentication: "RequestSID" = 0x29  # type: ignore  # noqa: vulture
    TesterPresent: "RequestSID" = 0x3E  # type: ignore  # noqa: vulture
    ControlDTCSetting: "RequestSID" = 0x85  # type: ignore  # noqa: vulture
    ResponseOnEvent: "RequestSID" = 0x86  # type: ignore  # noqa: vulture
    LinkControl: "RequestSID" = 0x87  # type: ignore  # noqa: vulture
    # Data transmission - more information in ISO 14229-1:2020, chapter 11
    ReadDataByIdentifier: "RequestSID" = 0x22  # type: ignore  # noqa: vulture
    ReadMemoryByAddress: "RequestSID" = 0x23  # type: ignore  # noqa: vulture
    ReadScalingDataByIdentifier: "RequestSID" = 0x24  # type: ignore  # noqa: vulture
    ReadDataByPeriodicIdentifier: "RequestSID" = 0x2A  # type: ignore  # noqa: vulture
    DynamicallyDefineDataIdentifier: "RequestSID" = 0x2C  # type: ignore  # noqa: vulture
    WriteDataByIdentifier: "RequestSID" = 0x2E  # type: ignore  # noqa: vulture
    WriteMemoryByAddress: "RequestSID" = 0x3D  # type: ignore  # noqa: vulture
    # Stored data transmission - more information in ISO 14229-1:2020, chapter 12
    ClearDiagnosticInformation: "RequestSID" = 0x14  # type: ignore  # noqa: vulture
    ReadDTCInformation: "RequestSID" = 0x19  # type: ignore  # noqa: vulture
    # InputOutput control - more information in ISO 14229-1:2020, chapter 13
    InputOutputControlByIdentifier: "RequestSID" = 0x2F  # type: ignore  # noqa: vulture
    # Routine - more information in ISO 14229-1:2020, chapter 14
    RoutineControl: "RequestSID" = 0x31  # type: ignore  # noqa: vulture
    # Upload download - more information in ISO 14229-1:2020, chapter 15
    RequestDownload: "RequestSID" = 0x34  # type: ignore  # noqa: vulture
    RequestUpload: "RequestSID" = 0x35  # type: ignore  # noqa: vulture
    TransferData: "RequestSID" = 0x36  # type: ignore  # noqa: vulture
    RequestTransferExit: "RequestSID" = 0x37  # type: ignore  # noqa: vulture
    RequestFileTransfer: "RequestSID" = 0x38  # type: ignore  # noqa: vulture
    SecuredDataTransmission: "RequestSID" = 0x84  # type: ignore  # noqa: vulture


@unique
class ResponseSID(ValidatedEnum, ExtendableEnum, ByteEnum):
    """
    Response Service Identifier values.

    .. note:: Response :ref:`SID <knowledge-base-sid>` is always the first payload byte of all request message.

    .. warning:: This enum contains multiple members (for all the services as
        :class:`~uds.message.service_identifiers.RequestSID`), but most of them are dynamically (implicitly) added and
        invisible in the documentation.
    """

    NegativeResponse: "ResponseSID" = 0x7F  # type: ignore

    @classmethod
    def is_response_sid(cls, value: int) -> bool:
        """
        Return whether the given integer is a Response Service Identifier (RSID).
        
        Checks membership against ALL_RESPONSE_SIDS. If the value is within the allowed RSID set but not defined as a ResponseSID enum member, emits UnrecognizedSIDWarning.
        
        Parameters:
            value (int): RSID byte value to check (0–255).
        
        Returns:
            bool: True if value is a valid RSID (defined or recognized but not listed in the enum), False otherwise.
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

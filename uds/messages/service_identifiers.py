"""Module with data and implementation related to Service Identifiers (SID)."""

__all__ = ["RequestSID", "ResponseSID", "POSSIBLE_REQUEST_SIDS", "POSSIBLE_RESPONSE_SIDS"]

from warnings import warn

from aenum import unique

from uds.utilities import RawByte, ByteEnum, ValidatedEnum, ExtendableEnum

# reserved SID values
_REQUEST_SIDS_DEFINED_BY_SAEJ1979 = set(range(0x01, 0x10))
_RESPONSE_SIDS_DEFINED_BY_SAEJ1979 = set(range(0x41, 0x50))
_REQUEST_SIDS_DEFINED_BY_ISO_14229 = set(range(0x10, 0x3F)).union(set(range(0x83, 0x89)), set(range(0xBA, 0xBF)))
_RESPONSE_SIDS_DEFINED_BY_ISO_14229 = set(range(0x50, 0x80)).union(set(range(0xC3, 0xC9)), set(range(0xFA, 0xFF)))

# all supported SID values according to UDS
POSSIBLE_REQUEST_SIDS = _REQUEST_SIDS_DEFINED_BY_SAEJ1979.union(_REQUEST_SIDS_DEFINED_BY_ISO_14229)
POSSIBLE_RESPONSE_SIDS = _RESPONSE_SIDS_DEFINED_BY_SAEJ1979.union(_RESPONSE_SIDS_DEFINED_BY_ISO_14229)


class UnsupportedSID(Warning):
    """
    Warning about SID that is legit but currently not supported by the package.

    You can either define member for this SID manually or raise `feature request` on webpage
    https://github.com/mdabrowski1990/uds/issues/new/choose to have support (for this SID) implemented in the package.
    """


@unique
class RequestSID(ByteEnum, ValidatedEnum):
    """
    Storage for all known Service Identifiers (SID).

    SID is always the first byte of the request messages. In this enum, only the valid values are defined.
    """

    @classmethod
    def is_request_sid(cls, value: RawByte) -> bool:
        """
        Check whether given value is Service Identifier (SID).

        :param value: Value to check.

        :return: True if value is int of known SID, else False.
        """
        if not cls.is_member(value):
            if value not in POSSIBLE_REQUEST_SIDS:
                return False
            warn(message=f"SID 0x{value:X} is not supported by this version of the package", category=UnsupportedSID)
        return True

    # Diagnostic and communication management - more information in ISO 14229-1:2020, chapter 10
    DiagnosticSessionControl = 0x10  # noqa: F841
    ECUReset = 0x11  # noqa: F841
    SecurityAccess = 0x27  # noqa: F841
    CommunicationControl = 0x28  # noqa: F841
    Authentication = 0x29  # noqa: F841
    TesterPresent = 0x3E  # noqa: F841
    ControlDTCSetting = 0x85  # noqa: F841
    ResponseOnEvent = 0x86  # noqa: F841
    LinkControl = 0x87  # noqa: F841
    # Data transmission - more information in ISO 14229-1:2020, chapter 11
    ReadDataByIdentifier = 0x22  # noqa: F841
    ReadMemoryByAddress = 0x23  # noqa: F841
    ReadScalingDataByIdentifier = 0x24  # noqa: F841
    ReadDataByPeriodicIdentifier = 0x2A  # noqa: F841
    DynamicallyDefineDataIdentifier = 0x2C  # noqa: F841
    WriteDataByIdentifier = 0x2E  # noqa: F841
    WriteMemoryByAddress = 0x3D  # noqa: F841
    # Stored data transmission - more information in ISO 14229-1:2020, chapter 12
    ClearDiagnosticInformation = 0x14  # noqa: F841
    ReadDTCInformation = 0x19  # noqa: F841
    # InputOutput control - more information in ISO 14229-1:2020, chapter 13
    InputOutputControlByIdentifier = 0x2F  # noqa: F841
    # Routine - more information in ISO 14229-1:2020, chapter 14
    RoutineControl = 0x31  # noqa: F841
    # Upload download - more information in ISO 14229-1:2020, chapter 15
    RequestDownload = 0x34  # noqa: F841
    RequestUpload = 0x35  # noqa: F841
    TransferData = 0x36  # noqa: F841
    RequestTransferExit = 0x37  # noqa: F841
    RequestFileTransfer = 0x38  # noqa: F841
    SecuredDataTransmission = 0x84  # noqa: F841


@unique
class ResponseSID(ByteEnum, ValidatedEnum, ExtendableEnum):  # pylint: disable=too-many-ancestors
    """
    Storage for all known Response Service Identifiers (RSID).

    RSID is always the first byte of the response messages. In this enum, only the valid values are defined.
    """

    @classmethod
    def is_response_sid(cls, value: RawByte) -> bool:
        """
        Check whether given value is Response Service Identifier (RSID).

        :param value: Value to check.

        :return: True if value is int of known RSID, else False.
        """
        if not cls.is_member(value):
            if value not in POSSIBLE_RESPONSE_SIDS:
                return False
            warn(message=f"RSID 0x{value:X} is not supported by this version of the package", category=UnsupportedSID)
        return True

    NegativeResponse = 0x7F  # noqa: F841


# extend 'ResponseSID' with members that were defined in RequestSID
for request_sid_member in RequestSID:  # type: ignore
    ResponseSID.add_member(request_sid_member.name, request_sid_member.value + 0x40)

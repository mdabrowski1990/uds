"""Module with data and implementation related to Service Identifiers (SID)."""

__all__ = ["RequestSID", "ResponseSID"]

from aenum import IntEnum, unique, extend_enum

from .types import RawByte


@unique
class RequestSID(IntEnum):
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
        try:
            cls(value)
            return True
        except ValueError:
            return False

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
class ResponseSID(IntEnum):
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
        try:
            cls(value)
            return True
        except ValueError:
            return False

    NegativeResponse = 0x7F


# extend 'ResponseSID' with members that were defined in RequestSID
for request_name, request_enum_member in RequestSID.__members__.items():
    extend_enum(ResponseSID, request_name, request_enum_member.value + 0x40)

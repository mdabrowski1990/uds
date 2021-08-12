"""Definition of Negative Response Codes (NRC)."""

__all__ = ["NRC"]

from aenum import unique

from ..utilities import ByteEnum


@unique
class NRC(ByteEnum):
    """
    Storage for all known Negative Response Codes (NRC).

    Explanation when each of NRC shall be used can be found in appendix A1 of ISO 14229-1.
    """

    # PositiveResponse = 0x00
    # This NRC shall not be used in a negative response message as positiveResponse parameter value is reserved
    # for server internal implementation. Refer to 8.7.5 of ISO 14229-1 for more details.
    GeneralReject = 0x10  # noqa: F841
    ServiceNotSupported = 0x11
    SubFunctionNotSupported = 0x12  # noqa: F841
    IncorrectMessageLengthOrInvalidFormat = 0x13  # noqa: F841
    ResponseTooLong = 0x14  # noqa: F841
    BusyRepeatRequest = 0x21  # noqa: F841
    ConditionsNotCorrect = 0x22  # noqa: F841
    RequestSequenceError = 0x24  # noqa: F841
    NoResponseFromSubnetComponent = 0x25  # noqa: F841
    FailurePreventsExecutionOfRequestedAction = 0x26  # noqa: F841
    RequestOutOfRange = 0x31  # noqa: F841
    SecurityAccessDenied = 0x33  # noqa: F841
    AuthenticationRequired = 0x34  # noqa: F841
    InvalidKey = 0x35  # noqa: F841
    ExceedNumberOfAttempts = 0x36  # noqa: F841
    RequiredTimeDelayNotExpired = 0x37  # noqa: F841
    SecureDataTransmissionRequired = 0x38  # noqa: F841
    SecureDataTransmissionNotAllowed = 0x39  # noqa: F841
    SecureDataVerificationFailed = 0x3A  # noqa: F841
    CertificateVerificationFailed_InvalidTimePeriod = 0x50  # noqa: F841
    CertificateVerificationFailed_InvalidSignature = 0x51  # noqa: F841
    CertificateVerificationFailed_InvalidChainOfTrust = 0x52  # noqa: F841
    CertificateVerificationFailed_InvalidType = 0x53  # noqa: F841
    CertificateVerificationFailed_InvalidFormat = 0x54  # noqa: F841
    CertificateVerificationFailed_InvalidContent = 0x55  # noqa: F841
    CertificateVerificationFailed_InvalidScope = 0x56  # noqa: F841
    CertificateVerificationFailed_InvalidCertificate = 0x57  # noqa: F841
    OwnershipVerificationFailed = 0x58  # noqa: F841
    ChallengeCalculationFailed = 0x59  # noqa: F841
    SettingAccessRightsFailed = 0x5A  # noqa: F841
    SessionKeyCreationOrDerivationFailed = 0x5B  # noqa: F841
    ConfigurationDataUsageFailed = 0x5C  # noqa: F841
    DeAuthenticationFailed = 0x5D  # noqa: F841
    UploadDownloadNotAccepted = 0x70  # noqa: F841
    TransferDataSuspended = 0x71  # noqa: F841
    GeneralProgrammingFailure = 0x72  # noqa: F841
    WrongBlockSequenceCounter = 0x73  # noqa: F841
    RequestCorrectlyReceived_ResponsePending = 0x78  # noqa: F841
    SubFunctionNotSupportedInActiveSession = 0x7E  # noqa: F841
    ServiceNotSupportedInActiveSession = 0x7F  # noqa: F841
    RpmTooHigh = 0x81  # noqa: F841
    RpmTooLow = 0x82  # noqa: F841
    EngineIsRunning = 0x83  # noqa: F841
    EngineIsNotRunning = 0x84  # noqa: F841
    EngineRunTimeTooLow = 0x85  # noqa: F841
    TemperatureTooHigh = 0x86  # noqa: F841
    TemperatureTooLow = 0x87  # noqa: F841
    VehicleSpeedTooHigh = 0x88  # noqa: F841
    VehicleSpeedTooLow = 0x89  # noqa: F841
    ThrottleOrPedalTooHigh = 0x8A  # noqa: F841
    ThrottleOrPedalTooLow = 0x8B  # noqa: F841
    TransmissionRangeNotInNeutral = 0x8C  # noqa: F841
    TransmissionRangeNotInGear = 0x8D  # noqa: F841
    BrakeSwitchOrSwitchesNotClosed = 0x8F  # noqa: F841
    ShifterLeverNotInPark = 0x90  # noqa: F841
    TorqueConvertClutchLocked = 0x91  # noqa: F841
    VoltageTooHigh = 0x92  # noqa: F841
    VoltageTooLow = 0x93  # noqa: F841
    ResourceTemporarilyNotAvailable = 0x94  # noqa: F841

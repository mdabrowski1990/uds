"""Definition of Negative Response Codes (NRC)."""

__all__ = ["NRC"]

from aenum import IntEnum, unique


@unique
class NRC(IntEnum):
    """
    Storage for all known Negative Response Codes (NRC).

    Explanation when each of NRC shall be used can be found in appendix A1 of ISO 14229-1.
    """

    # PositiveResponse = 0x00
    # This NRC shall not be used in a negative response message. This positiveResponse parameter value is reserved
    # for server internal implementation. Refer to 8.7.5 of ISO 14229-1.
    GeneralReject = 0x10
    ServiceNotSupported = 0x11
    SubFunctionNotSupported = 0x12
    IncorrectMessageLengthOrInvalidFormat = 0x13
    ResponseTooLong = 0x14
    BusyRepeatRequest = 0x21
    ConditionsNotCorrect = 0x22
    RequestSequenceError = 0x24
    NoResponseFromSubnetComponent = 0x25
    FailurePreventsExecutionOfRequestedAction = 0x26
    RequestOutOfRange = 0x31
    SecurityAccessDenied = 0x33
    AuthenticationRequired = 0x34
    InvalidKey = 0x35
    ExceedNumberOfAttempts = 0x36
    RequiredTimeDelayNotExpired = 0x37
    SecureDataTransmissionRequired = 0x38
    SecureDataTransmissionNotAllowed = 0x39
    SecureDataVerificationFailed = 0x3A
    CertificateVerificationFailed_InvalidTimePeriod = 0x50
    CertificateVerificationFailed_InvalidSignature = 0x51
    CertificateVerificationFailed_InvalidChainOfTrust = 0x52
    CertificateVerificationFailed_InvalidType = 0x53
    CertificateVerificationFailed_InvalidFormat = 0x54
    CertificateVerificationFailed_InvalidContent = 0x55
    CertificateVerificationFailed_InvalidScope = 0x56
    CertificateVerificationFailed_InvalidCertificate = 0x57
    OwnershipVerificationFailed = 0x58
    ChallengeCalculationFailed = 0x59
    SettingAccessRightsFailed = 0x5A
    SessionKeyCreationOrDerivationFailed = 0x5B
    ConfigurationDataUsageFailed = 0x5C
    DeAuthenticationFailed = 0x5D
    UploadDownloadNotAccepted = 0x70
    TransferDataSuspended = 0x71
    GeneralProgrammingFailure = 0x72
    WrongBlockSequenceCounter = 0x73
    RequestCorrectlyReceived_ResponsePending = 0x78
    SubFunctionNotSupportedInActiveSession = 0x7E
    ServiceNotSupportedInActiveSession = 0x7F
    RpmTooHigh = 0x81
    RpmTooLow = 0x82
    EngineIsRunning = 0x83
    EngineIsNotRunning = 0x84
    EngineRunTimeTooLow = 0x85
    TemperatureTooHigh = 0x86
    TemperatureTooLow = 0x87
    VehicleSpeedTooHigh = 0x88
    VehicleSpeedTooLow = 0x89
    ThrottleOrPedalTooHigh = 0x8A
    ThrottleOrPedalTooLow = 0x8B
    TransmissionRangeNotInNeutral = 0x8C
    TransmissionRangeNotInGear = 0x8D
    BrakeSwitchOrSwitchesNotClosed = 0x8F
    ShifterLeverNotInPark = 0x90
    TorqueConvertClutchLocked = 0x91
    VoltageTooHigh = 0x92
    VoltageTooLow = 0x93
    ResourceTemporarilyNotAvailable = 0x94

"""
Module with an entire Negative Response Code (NRC) data parameters implementation.

.. note:: Explanation of :ref:`NRC <knowledge-base-nrc>` values meaning is located in appendix A1 of
    ISO 14229-1 standard.
"""

__all__ = ["NRC"]

from aenum import unique

from uds.utilities import ByteEnum, ExtendableEnum, ValidatedEnum


@unique
class NRC(ValidatedEnum, ExtendableEnum, ByteEnum):
    """
    Negative Response Codes (NRC) values.

    `Negative Response Code <knowledge-base-nrc>` is a data parameter located in the last byte of a negative response
    message. NRC informs why a server is not sending a positive response message.
    """

    # PositiveResponse: "NRC" = 0x00
    # This NRC shall not be used in a negative response message as positiveResponse parameter value is reserved
    # for server internal implementation. Refer to 8.7.5 of ISO 14229-1 for more details.
    GeneralReject: "NRC" = 0x10  # type: ignore  # noqa: F841
    """GeneralReject (0x10) NRC indicates that the requested action has been rejected by the server."""
    ServiceNotSupported: "NRC" = 0x11  # type: ignore  # noqa: F841
    """ServiceNotSupported (0x11) NRC indicates that the requested action will not be taken because the server does not
    support the requested service."""
    SubFunctionNotSupported: "NRC" = 0x12  # type: ignore  # noqa: F841
    """SubFunctionNotSupported (0x12) NRC indicates that the requested action will not be taken because the server
    does not support the service specific parameters of the request message."""
    IncorrectMessageLengthOrInvalidFormat: "NRC" = 0x13  # type: ignore  # noqa: F841
    """IncorrectMessageLengthOrInvalidFormat (0x13) NRC indicates that the requested action will not be taken because
    the length of the received request message does not match the prescribed length for the specified service or
    the format of the parameters do not match the prescribed format for the specified service."""
    ResponseTooLong: "NRC" = 0x14  # type: ignore  # noqa: F841
    """ResponseTooLong (0x14) NRC shall be reported by the server if the response to be generated exceeds the maximum
    number of bytes available by the underlying network layer. This could occur if the response message exceeds
    the maximum size allowed by the underlying transport protocol or if the response message exceeds the server buffer
    size allocated for that purpose."""
    BusyRepeatRequest: "NRC" = 0x21  # type: ignore  # noqa: F841
    """BusyRepeatRequest (0x21) NRC indicates that the server is temporarily too busy to perform the requested
    operation. In this circumstance the client shall perform repetition of the “identical request message”
    or “another request message”. The repetition of the request shall be delayed by a time specified in the respective
    implementation documents."""
    ConditionsNotCorrect: "NRC" = 0x22  # type: ignore  # noqa: F841
    """ConditionsNotCorrect (0x22) NRC indicates that the requested action will not be taken because the server
    prerequisite conditions are not met."""
    RequestSequenceError: "NRC" = 0x24  # type: ignore  # noqa: F841
    """RequestSequenceError (0x24) NRC indicates that the requested action will not be taken because the server
    expects a different sequence of request messages or message as sent by the client. This may occur when sequence
    sensitive requests are issued in the wrong order."""
    NoResponseFromSubnetComponent: "NRC" = 0x25  # type: ignore  # noqa: F841
    """NoResponseFromSubnetComponent (0x25) NRC indicates that the server has received the request but the requested
    action could not be performed by the server as a subnet component which is necessary to supply the requested
    information did not respond within the specified time."""
    FailurePreventsExecutionOfRequestedAction: "NRC" = 0x26  # type: ignore  # noqa: F841
    """FailurePreventsExecutionOfRequestedAction (0x26) NRC indicates that the requested action will not be taken
    because a failure condition, identified by a DTC (with at least one DTC status bit for TestFailed, Pending,
    Confirmed or TestFailedSinceLastClear set to 1), has occurred and that this failure condition prevents
    the server from performing the requested action."""
    RequestOutOfRange: "NRC" = 0x31  # type: ignore  # noqa: F841
    """RequestOutOfRange (0x31) NRC indicates that the requested action will not be taken because the server has
    detected that the request message contains a parameter which attempts to substitute a value beyond its range of
    authority (e.g. attempting to substitute a data byte of 111 when the data is only defined to 100), or which
    attempts to access a DataIdentifier/RoutineIdentifer that is not supported or not supported in active session."""
    SecurityAccessDenied: "NRC" = 0x33  # type: ignore  # noqa: F841
    """SecurityAccessDenied (0x33) NRC indicates that the requested action will not be taken because the server’s
    security strategy has not been satisfied by the client."""
    AuthenticationRequired: "NRC" = 0x34  # type: ignore  # noqa: F841
    """AuthenticationRequired (0x34) NRC indicates that the requested service will not be taken because the client
    has insufficient rights based on its Authentication state."""
    InvalidKey: "NRC" = 0x35  # type: ignore  # noqa: F841
    """InvalidKey (0x35) NRC indicates that the server has not given security access because the key sent by
    the client did not match with the key in the server’s memory. This counts as an attempt to gain security."""
    ExceedNumberOfAttempts: "NRC" = 0x36  # type: ignore  # noqa: F841
    """ExceedNumberOfAttempts (0x36) NRC indicates that the requested action will not be taken because the client
    has unsuccessfully attempted to gain security access more times than the server’s security strategy will allow."""
    RequiredTimeDelayNotExpired: "NRC" = 0x37  # type: ignore  # noqa: F841
    """RequiredTimeDelayNotExpired (0x37) NRC indicates that the requested action will not be taken because
    the client’s latest attempt to gain security access was initiated before the server’s required timeout period had
    elapsed."""
    SecureDataTransmissionRequired: "NRC" = 0x38  # type: ignore  # noqa: F841
    """SecureDataTransmissionRequired (0x38) NRC indicates that the requested service will not be taken because
    the requested action is required to be sent using a secured communication channel."""
    SecureDataTransmissionNotAllowed: "NRC" = 0x39  # type: ignore  # noqa: F841
    """SecureDataTransmissionNotAllowed (0x39) NRC indicates that this message was received using
    the SecuredDataTransmission (SID 0x84) service. However, the requested action is not allowed to be sent using
    the SecuredDataTransmission (0x84) service."""
    SecureDataVerificationFailed: "NRC" = 0x3A  # type: ignore  # noqa: F841
    """SecureDataVerificationFailed (0x3A) NRC indicates that the message failed in the security sub-layer."""
    CertificateVerificationFailed_InvalidTimePeriod: "NRC" = 0x50  # type: ignore  # noqa: F841
    """CertificateVerificationFailed_InvalidTimePeriod (0x50) NRC indicates that date and time of the server does not
    match the validity period of the Certificate."""
    CertificateVerificationFailed_InvalidSignature: "NRC" = 0x51  # type: ignore  # noqa: F841
    """CertificateVerificationFailed_InvalidSignature (0x51) NRC indicates that signature of the Certificate could
    not be verified."""
    CertificateVerificationFailed_InvalidChainOfTrust: "NRC" = 0x52  # type: ignore  # noqa: F841
    """CertificateVerificationFailed_InvalidChainOfTrust (0x52) NRC indicates that The Certificate could not be
    verified against stored information about the issuing authority."""
    CertificateVerificationFailed_InvalidType: "NRC" = 0x53  # type: ignore  # noqa: F841
    """CertificateVerificationFailed_InvalidType (0x53) NRC indicates that the Certificate does not match the current
    requested use case."""
    CertificateVerificationFailed_InvalidFormat: "NRC" = 0x54  # type: ignore  # noqa: F841
    """CertificateVerificationFailed_InvalidFormat (0x54) NRC indicates that the Certificate could not be evaluated
    because the format requirement has not been met."""
    CertificateVerificationFailed_InvalidContent: "NRC" = 0x55  # type: ignore  # noqa: F841
    """CertificateVerificationFailed_InvalidContent (0x55) NRC indicates that the Certificate could not be verified
    because the content does not match."""
    CertificateVerificationFailed_InvalidScope: "NRC" = 0x56  # type: ignore  # noqa: F841
    """CertificateVerificationFailed_InvalidScope (0x56) NRC indicates that the scope of the Certificate does not match
    the contents of the server."""
    CertificateVerificationFailed_InvalidCertificate: "NRC" = 0x57  # type: ignore  # noqa: F841
    """CertificateVerificationFailed_InvalidCertificate (0x57) NRC indicates that the Certificate received from client
    is invalid, because the server has revoked access for some reason."""
    OwnershipVerificationFailed: "NRC" = 0x58  # type: ignore  # noqa: F841
    """OwnershipVerificationFailed (0x58) NRC indicates that delivered Ownership does not match the provided challenge
    or could not verified with the own private key."""
    ChallengeCalculationFailed: "NRC" = 0x59  # type: ignore  # noqa: F841
    """ChallengeCalculationFailed (0x59) NRC indicates that the challenge could not be calculated on the server side."""
    SettingAccessRightsFailed: "NRC" = 0x5A  # type: ignore  # noqa: F841
    """SettingAccessRightsFailed (0x5A) NRC indicates that the server could not set the access rights."""
    SessionKeyCreationOrDerivationFailed: "NRC" = 0x5B  # type: ignore  # noqa: F841
    """SessionKeyCreationOrDerivationFailed (0x5B) NRC indicates that the server could not create or derive
    a session key."""
    ConfigurationDataUsageFailed: "NRC" = 0x5C  # type: ignore  # noqa: F841
    """ConfigurationDataUsageFailed (0x5C) NRC indicates that the server could not work with the provided
    configuration data."""
    DeAuthenticationFailed: "NRC" = 0x5D  # type: ignore  # noqa: F841
    """DeAuthenticationFailed (0x5D) NRC indicates that DeAuthentication was not successful, server could still be
    unprotected."""
    UploadDownloadNotAccepted: "NRC" = 0x70  # type: ignore  # noqa: F841
    """UploadDownloadNotAccepted (0x70) NRC indicates that an attempt to upload/download to a server’s memory cannot
    be accomplished due to some fault conditions."""
    TransferDataSuspended: "NRC" = 0x71  # type: ignore  # noqa: F841
    """TransferDataSuspended (0x71) NRC indicates that a data transfer operation was halted due to some fault.
    The active transferData sequence shall be aborted."""
    GeneralProgrammingFailure: "NRC" = 0x72  # type: ignore  # noqa: F841
    """GeneralProgrammingFailure (0x72) NRC indicates that the server detected an error when erasing or programming
    a memory location in the permanent memory device (e.g. Flash Memory)."""
    WrongBlockSequenceCounter: "NRC" = 0x73  # type: ignore  # noqa: F841
    """WrongBlockSequenceCounter (0x73) NRC indicates that  the server detected an error in the sequence of
    blockSequenceCounter values. Note that the repetition of a TransferData request message with a blockSequenceCounter
    equal to the one included in the previous TransferData request message shall be accepted by the server."""
    RequestCorrectlyReceived_ResponsePending: "NRC" = 0x78  # type: ignore  # noqa: F841
    """RequestCorrectlyReceived_ResponsePending (0x78) NRC indicates that the request message was received correctly,
    and that all parameters in the request message were valid (these checks can be delayed until after sending this NRC
    if executing the boot software), but the action to be performed is not yet completed and the server is not yet
    ready to receive another request. As soon as the requested service has been completed, the server shall send
    a positive response message or negative response message with a response code different from this."""
    SubFunctionNotSupportedInActiveSession: "NRC" = 0x7E  # type: ignore  # noqa: F841
    """SubFunctionNotSupportedInActiveSession (0x7E) NRC indicates that the requested action will not be taken because
    the server does not support the requested SubFunction in the session currently active. This NRC shall only be used
    when the requested SubFunction is known to be supported in another session, otherwise response code
    SubFunctionNotSupported shall be used."""
    ServiceNotSupportedInActiveSession: "NRC" = 0x7F  # type: ignore  # noqa: F841
    """ServiceNotSupportedInActiveSession (0x7F) NRC indicates that the requested action will not be taken because
    the server does not support the requested service in the session currently active. This NRC shall only be used when
    the requested service is known to be supported in another session, otherwise response code serviceNotSupported
    shall be used."""
    RpmTooHigh: "NRC" = 0x81  # type: ignore  # noqa: F841
    """RpmTooHigh (0x81) NRC indicates that the requested action will not be taken because the server prerequisite
    condition for RPM is not met (current RPM is above a preprogrammed maximum threshold)."""
    RpmTooLow: "NRC" = 0x82  # type: ignore  # noqa: F841
    """RpmTooLow (0x82) NRC indicates that the requested action will not be taken because the server prerequisite
    condition for RPM is not met (current RPM is below a preprogrammed minimum threshold)."""
    EngineIsRunning: "NRC" = 0x83  # type: ignore  # noqa: F841
    """EngineIsRunning (0x83) NRC is required for those actuator tests which cannot be actuated while the Engine
    is running. This is different from RPM too high negative response, and shall be allowed."""
    EngineIsNotRunning: "NRC" = 0x84  # type: ignore  # noqa: F841
    """EngineIsNotRunning (0x84) NRC is required for those actuator tests which cannot be actuated unless the Engine
    is running. This is different from RPM too low negative response, and shall be allowed."""
    EngineRunTimeTooLow: "NRC" = 0x85  # type: ignore  # noqa: F841
    """EngineRunTimeTooLow (0x85)  NRC indicates that the requested action will not be taken because the server
    prerequisite condition for engine run time is not met (current engine run time is below a preprogrammed limit)."""
    TemperatureTooHigh: "NRC" = 0x86  # type: ignore  # noqa: F841
    """TemperatureTooHigh (0x86) NRC indicates that the requested action will not be taken because the serve
    prerequisite condition for temperature is not met (current temperature is above a preprogrammed maximum
    threshold)."""
    TemperatureTooLow: "NRC" = 0x87  # type: ignore  # noqa: F841
    """TemperatureTooLow (0x87) NRC indicates that the requested action will not be taken because the server
    prerequisite condition for temperature is not met (current temperature is below a preprogrammed minimum
    threshold)."""
    VehicleSpeedTooHigh: "NRC" = 0x88  # type: ignore  # noqa: F841
    """VehicleSpeedTooHigh (0x88) NRC indicates that the requested action will not be taken because the server
    prerequisite condition for vehicle speed is not met (current VS is above a preprogrammed maximum threshold)."""
    VehicleSpeedTooLow: "NRC" = 0x89  # type: ignore  # noqa: F841
    """VehicleSpeedTooLow (0x89) NRC indicates that the requested action will not be taken because the server
    prerequisite condition for vehicle speed is not met (current VS is below a preprogrammed minimum threshold)."""
    ThrottleOrPedalTooHigh: "NRC" = 0x8A  # type: ignore  # noqa: F841
    """ThrottleOrPedalTooHigh (0x8A) NRC indicates that the requested action will not be taken because the server
    prerequisite condition for throttle/pedal position is not met (current throttle/pedal position is above
    a preprogrammed maximum threshold)."""
    ThrottleOrPedalTooLow: "NRC" = 0x8B  # type: ignore  # noqa: F841
    """ThrottleOrPedalTooLow (0x8B) NRC indicates that the requested action will not be taken because the server
    prerequisite condition for throttle/pedal position is not met (current throttle/pedal position is below
    a preprogrammed minimum threshold)."""
    TransmissionRangeNotInNeutral: "NRC" = 0x8C  # type: ignore  # noqa: F841
    """TransmissionRangeNotInNeutral (0x8C) NRC indicates that the requested action will not be taken because
    the server prerequisite condition for being in neutral is not met (current transmission range is not in neutral)."""
    TransmissionRangeNotInGear: "NRC" = 0x8D  # type: ignore  # noqa: F841
    """TransmissionRangeNotInGear (0x8D) NRC indicates that the requested action will not be taken because
    the server prerequisite condition for being in gear is not met (current transmission range is not in gear)."""
    BrakeSwitchOrSwitchesNotClosed: "NRC" = 0x8F  # type: ignore  # noqa: F841
    """BrakeSwitchOrSwitchesNotClosed (0x8F) NRC indicates that for safety reasons, this is required for certain
    tests before it begins, and shall be maintained for the entire duration of the test."""
    ShifterLeverNotInPark: "NRC" = 0x90  # type: ignore  # noqa: F841
    """ShifterLeverNotInPark (0x90) NRC indicates that for safety reasons, this is required for certain tests before
    it begins, and shall be maintained for the entire duration of the test."""
    TorqueConvertClutchLocked: "NRC" = 0x91  # type: ignore  # noqa: F841
    """TorqueConvertClutchLocked (0x91) RC indicates that the requested action will not be taken because the server
    prerequisite condition for torque converter clutch is not met (current torque converter clutch status above
    a preprogrammed limit or locked)."""
    VoltageTooHigh: "NRC" = 0x92  # type: ignore  # noqa: F841
    """VoltageTooHigh (0x92) NRC indicates that the requested action will not be taken because the server prerequisite
    condition for voltage at the primary pin of the server (ECU) is not met (current voltage is above a preprogrammed
    maximum threshold)."""
    VoltageTooLow: "NRC" = 0x93  # type: ignore  # noqa: F841
    """VoltageTooLow (0x93) NRC indicates that the requested action will not be taken because the server prerequisite
    condition for voltage at the primary pin of the server (ECU) is not met (current voltage is below a preprogrammed
    minimum threshold)."""
    ResourceTemporarilyNotAvailable: "NRC" = 0x94  # type: ignore  # noqa: F841
    """ResourceTemporarilyNotAvailable (0x94) NRC indicates that the server has received the request but the requested
    action could not be performed by the server because an application which is necessary to supply the requested
    information is temporality not available. This NRC is in general supported by each diagnostic service, as not
    otherwise stated in the data link specific implementation document, therefore it is not listed in the list of
    applicable response codes of the diagnostic services."""

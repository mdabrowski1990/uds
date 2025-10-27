"""Various helper functions, classes and variables that are shared and reused within the project."""

from .common_types import (
    RawBytesAlias,
    RawBytesListAlias,
    RawBytesSetAlias,
    RawBytesTupleAlias,
    TimeMillisecondsAlias,
    TimestampAlias,
    validate_nibble,
    validate_raw_byte,
    validate_raw_bytes,
)
from .constants import (
    BITS_TO_DTC_CHARACTER_MAPPING,
    DTC_CHARACTERS_MAPPING,
    EXPONENT_BIT_LENGTH,
    MANTISSA_BIT_LENGTH,
    MAX_DTC_VALUE,
    MIN_DTC_VALUE,
    REPEATED_DATA_RECORDS_NUMBER,
)
from .conversions import bytes_to_hex, bytes_to_int, int_to_bytes, int_to_obd_dtc, obd_dtc_to_int
from .custom_exceptions import (
    AmbiguityError,
    InconsistencyError,
    MessageTransmissionNotStartedError,
    ReassignmentError,
    UnusedArgumentError,
)
from .custom_warnings import (
    NewMessageReceptionWarning,
    UnexpectedPacketReceptionWarning,
    UnusedArgumentWarning,
    ValueWarning,
)
from .enums import ByteEnum, Endianness, ExtendableEnum, NibbleEnum, ValidatedEnum

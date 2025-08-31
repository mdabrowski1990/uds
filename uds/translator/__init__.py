"""
Implementation for diagnostic messages databases.

Tools for decoding and encoding information from/to diagnostic messages.
"""

from .data_record import (
    AbstractDataRecord,
    ConditionalFormulaDataRecord,
    ConditionalMappingDataRecord,
    CustomFormulaDataRecord,
    LinearFormulaDataRecord,
    MappingDataRecord,
    RawDataRecord,
    TextDataRecord,
    TextEncoding,
)
from .service import DecodedMessageAlias, Service, TESTER_PRESENT
from .translator import Translator
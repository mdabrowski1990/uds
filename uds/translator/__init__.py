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
from .service import TESTER_PRESENT, DecodedMessageAlias, Service
from .translator import Translator

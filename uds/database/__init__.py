"""
Implementation for diagnostic messages databases.

Tools for decoding and encoding information from/to diagnostic messages.
"""

# from .abstract_database import AbstractDatabase
from .data_record import (
    AbstractDataRecord,
    ConditionalFormulaDataRecord,
    ConditionalMappingDataRecord,
    MappingDataRecord,
    RawDataRecord,
    TextDataRecord,
    TextEncoding,
)
# from .service import AbstractService

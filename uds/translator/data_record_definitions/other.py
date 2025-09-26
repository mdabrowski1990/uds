"""Remaining Data Records definitions."""

__all__ = [
    # SID 0x10
    "P2_SERVER_MAX", "P2EXT_SERVER_MAX", "SESSION_PARAMETER_RECORD"
]

from uds.translator.data_record.formula_data_record import LinearFormulaDataRecord
from uds.translator.data_record.raw_data_record import RawDataRecord

# SID 0x10
P2_SERVER_MAX = LinearFormulaDataRecord(name="P2Server_max",
                                        length=16,
                                        factor=1,
                                        offset=0,
                                        unit="ms")
P2EXT_SERVER_MAX = LinearFormulaDataRecord(name="P2*Server_max",
                                           length=16,
                                           factor=10,
                                           offset=0,
                                           unit="ms")
SESSION_PARAMETER_RECORD = RawDataRecord(name="sessionParameterRecord",
                                         length=32,
                                         children=(P2_SERVER_MAX, P2EXT_SERVER_MAX))

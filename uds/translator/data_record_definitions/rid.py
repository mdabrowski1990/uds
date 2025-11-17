"""Data Records definitions for Routines and :ref:`Routine Identifiers <knowledge-base-rid>`."""

__all__ = ["RID",
           "ROUTINE_CONTROL_OPTION", "ROUTINE_INFO",
           "ROUTINE_STATUS", "OPTIONAL_ROUTINE_STATUS"]

from ..data_record import MappingDataRecord, RawDataRecord

RID_MAPPING = {
    0xE200 : "Execute SPL",
    0xE201 : "Execute DeployLoopRoutineID",
    0xFF00 : "eraseMemory",
    0xFF01 : "checkProgrammingDependencies",
}
""":ref:`:Routine Identifiers mapping according to ISO 14229-1 <knowledge-base-rid>`."""

RID = MappingDataRecord(name="RID",
                        length=16,
                        values_mapping=RID_MAPPING)

ROUTINE_CONTROL_OPTION = RawDataRecord(name="routineControlOption",
                                       length=8,
                                       min_occurrences=0,
                                       max_occurrences=None)

ROUTINE_INFO = RawDataRecord(name="routineInfo",
                             length=8,
                             min_occurrences=0,
                             max_occurrences=1)

ROUTINE_STATUS = RawDataRecord(name="routineStatus",
                               length=8,
                               min_occurrences=1,
                               max_occurrences=None)
OPTIONAL_ROUTINE_STATUS = RawDataRecord(name="routineStatus",
                                        length=8,
                                        min_occurrences=0,
                                        max_occurrences=None)

"""Data Records definitions for Routines and :ref:`Routine Identifiers <knowledge-base-rid>`."""

__all__ = [
    "RID",
    "ROUTINE_CONTROL_OPTION",
    "ROUTINE_STATUS", "OPTIONAL_ROUTINE_STATUS"
]

from uds.utilities import RID_BIT_LENGTH, RID_MAPPING

from ..data_record import MappingDataRecord, RawDataRecord

RID = MappingDataRecord(name="RID",
                        length=RID_BIT_LENGTH,
                        values_mapping=RID_MAPPING)
"""Definition of :ref:`RoutineIdentifier (RID) <knowledge-base-rid>` Data Record."""

ROUTINE_CONTROL_OPTION = RawDataRecord(name="routineControlOption",
                                       length=8,
                                       min_occurrences=0,
                                       max_occurrences=None)
"""Definition of `routineControlOption` Data Record."""

ROUTINE_STATUS = RawDataRecord(name="routineStatus",
                               length=8,
                               min_occurrences=1,
                               max_occurrences=None)
"""Definition of `routineStatus` Data Record."""
OPTIONAL_ROUTINE_STATUS = RawDataRecord(name="routineStatus",
                                        length=8,
                                        min_occurrences=0,
                                        max_occurrences=None)
"""Definition of optional `routineStatus` Data Record."""

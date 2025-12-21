"""Definitions for Conditional Data Records."""

__all__ = [
    # SID 0x86
    "EVENT_TYPE_RECORD_01",
    "EVENT_TYPE_RECORD_09_2020", "CONDITIONAL_EVENT_TYPE_RECORD_09_2020"
]

from .formula import get_event_type_record_01, get_event_type_record_09_2020, get_conditional_event_type_record_09_2020


# SID 0x86
EVENT_TYPE_RECORD_01 = get_event_type_record_01()
"""Definition of `eventTypeRecord` Data Record for `event` equal to 0x01."""
EVENT_TYPE_RECORD_09_2020 = get_event_type_record_09_2020()
"""Definition of `eventTypeRecord` Data Record (compatible with ISO 14229-1:2020) for `event` equal to 0x09."""
CONDITIONAL_EVENT_TYPE_RECORD_09_2020 = get_conditional_event_type_record_09_2020()
"""Continuation of `eventTypeRecord` Data Record (compatible with ISO 14229-1:2020) for `event` equal to 0x09."""

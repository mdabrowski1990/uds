""":ref:`DTC <knowledge-base-dtc>` related constants."""

__all__ = [
    "MIN_DTC_VALUE", "MAX_DTC_VALUE",
    "DTC_CHARACTERS_MAPPING", "BITS_TO_DTC_CHARACTER_MAPPING",
    "DTC_SNAPSHOT_RECORD_NUMBER_MAPPING",
    "DTC_EXTENDED_DATA_RECORD_NUMBER_MAPPING",
    "DTC_STORED_DATA_RECORD_NUMBER_MAPPING",
    "GROUP_OF_DTC_MAPPING",
    "DTC_FORMAT_IDENTIFIER_MAPPING",
    "DTC_FUNCTIONAL_GROUP_IDENTIFIER_MAPPING",
]

from typing import Dict

MIN_DTC_VALUE = 0x000000
"""Minimum DTC value."""
MAX_DTC_VALUE = 0xFFFFFF
"""Maximum DTC value."""

DTC_CHARACTERS_MAPPING: Dict[str, int] = {
    "P": 0b00,  # Powertrain
    "C": 0b01,  # Chassis
    "B": 0b10,  # Body
    "U": 0b11,  # Network Communication
}
"""Mapping of the first DTC character in :ref:`OBD format <knowledge-base-dtc-obd-format>` to bits."""

BITS_TO_DTC_CHARACTER_MAPPING: Dict[int, str] = {
    value: key for key, value in DTC_CHARACTERS_MAPPING.items()
}
"""Mapping of the first two DTC bits to :ref:`OBD format <knowledge-base-dtc-obd-format>` character."""

DTC_SNAPSHOT_RECORD_NUMBER_MAPPING: Dict[int, str] = {
    0xFF: "all"
}
"""Values mapping for `DTCSnapshotRecordNumber` Data Record."""

DTC_EXTENDED_DATA_RECORD_NUMBER_MAPPING: Dict[int, str] = {
    0xFE: "all regulated emissions data",
    0xFF: "all",
}
"""Values mapping for `DTCExtDataRecordNumber` Data Record."""

DTC_STORED_DATA_RECORD_NUMBER_MAPPING: Dict[int, str] = {
    0xFF: "all",
}
"""Values mapping for `DTCStoredDataRecordNumber` Data Record."""

GROUP_OF_DTC_MAPPING: Dict[int, str] = {
    0xFFFF33: "Emissions-system group",
    0xFFFFD0: "Safety-system group",
    0xFFFFFE: "VOBD system group",
    0xFFFFFF: "all",
}
"""Values mapping for `groupOfDTC` Data Record."""

DTC_FORMAT_IDENTIFIER_MAPPING: Dict[int, str] = {
    0x00: "SAE J2012-DA DTC Format 00",
    0x01: "ISO 14229-1 DTC Format",
    0x02: "SAE J1939-73 DTC Format",
    0x03: "ISO 11992-4 DTC Format",
    0x04: "SAE J2012-DA DTC Format 04"
}
"""Values mapping for `DTCFormatIdentifier` Data Record."""

DTC_FUNCTIONAL_GROUP_IDENTIFIER_MAPPING = {
    0x33: "Emissions-system group",
    0xD0: "Safety-system group",
    0xFE: "VOBD system",
    0xFF: "all"
}
"""Values mapping for `FunctionalGroupIdentifier` Data Record."""

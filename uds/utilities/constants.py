"""Constants used within the project."""

__all__ = [
    "DTC_CHARACTERS_MAPPING", "BITS_TO_DTC_CHARACTER_MAPPING", "MIN_DTC_VALUE", "MAX_DTC_VALUE",
    "EXPONENT_BIT_LENGTH", "MANTISSA_BIT_LENGTH",
    "REPEATED_DATA_RECORDS_NUMBER",
]

from typing import Dict

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

MIN_DTC_VALUE = 0x000000
MAX_DTC_VALUE = 0xFFFFFF

EXPONENT_BIT_LENGTH: int = 4
"""Number of bits used for constant's exponent value by
:ref:`ReadScalingDataByIdentifier service <knowledge-base-service-read-scaling-data-by-identifier>`"""
MANTISSA_BIT_LENGTH: int = 12
"""Number of bits used for constant's mantissa value by
:ref:`ReadScalingDataByIdentifier service <knowledge-base-service-read-scaling-data-by-identifier>`"""

REPEATED_DATA_RECORDS_NUMBER: int = 100

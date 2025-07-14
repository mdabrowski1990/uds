from aenum import StrEnum

from uds.utilities.transmission_direction import TransmissionDirection
from uds.utilities import ValidatedEnum


class TestTransmissionDirection:
    """Unit tests for 'TransmissionDirection' class."""

    def test_inheritance__enum_str(self):
        assert issubclass(TransmissionDirection, StrEnum)

    def test_inheritance__validated_enum(self):
        assert issubclass(TransmissionDirection, ValidatedEnum)

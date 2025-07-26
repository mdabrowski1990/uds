from aenum import StrEnum

from uds.can.addressing import CanAddressingFormat
from uds.utilities import ValidatedEnum


class TestCanAddressingFormat:
    """Unit tests for `CanAddressingFormat` class."""

    # inheritance

    def test_inheritance__validated_enum(self):
        assert issubclass(CanAddressingFormat, ValidatedEnum)

    def test_inheritance__str_enum(self):
        assert issubclass(CanAddressingFormat, StrEnum)

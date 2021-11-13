from uds.can.addressing_format import CanAddressingFormat
from uds.utilities import ValidatedEnum
from aenum import StrEnum


class TestCanAddressingFormat:
    """Unit tests for `CanAddressingFormat` class."""

    # inheritance

    def test_inheritance__validated_enum(self):
        assert issubclass(CanAddressingFormat, ValidatedEnum)

    def test_inheritance__str_enum(self):
        assert issubclass(CanAddressingFormat, StrEnum)

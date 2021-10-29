from uds.can.addressing_format import CanAddressingFormat
from uds.utilities import ValidatedEnum


class TestCanAddressingFormat:
    """Tests for `CanAddressingFormat` class."""

    # inheritance

    def test_inheritance__validated_enum(self):
        assert issubclass(CanAddressingFormat, ValidatedEnum)

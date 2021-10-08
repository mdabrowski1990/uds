from aenum import StrEnum

from uds.message.addressing import AddressingType
from uds.utilities import ValidatedEnum


class TestAddressingType:
    """Tests for 'AddressingType' class."""

    def test_inheritance__enum_str(self):
        assert issubclass(AddressingType, StrEnum)

    def test_inheritance__validated_enum(self):
        assert issubclass(AddressingType, ValidatedEnum)

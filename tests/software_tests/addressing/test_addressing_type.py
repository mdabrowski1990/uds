from aenum import StrEnum

from uds.addressing.addressing_type import AddressingType
from uds.utilities import ValidatedEnum


class TestAddressingType:
    """Unit tests for 'AddressingType' class."""

    def test_inheritance__enum_str(self):
        assert issubclass(AddressingType, StrEnum)

    def test_inheritance__validated_enum(self):
        assert issubclass(AddressingType, ValidatedEnum)

from aenum import StrEnum

from uds.messages.transmission_attributes import AddressingType, TransmissionDirection
from uds.utilities import ValidatedEnum


class TestAddressingType:
    """Tests for 'AddressingType' class."""

    def test_inheritance__enum_str(self):
        assert issubclass(AddressingType, StrEnum)

    def test_inheritance__validated_enum(self):
        assert issubclass(AddressingType, ValidatedEnum)


class TestTransmissionDirection:
    """Tests for 'TransmissionDirection' class."""

    def test_inheritance__enum_str(self):
        assert issubclass(TransmissionDirection, StrEnum)

    def test_inheritance__validated_enum(self):
        assert issubclass(TransmissionDirection, ValidatedEnum)

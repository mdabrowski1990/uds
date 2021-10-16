import pytest

from uds.message.nrc import NRC, \
    ByteEnum, ValidatedEnum, ExtendableEnum


class TestNRC:
    """Tests for 'NRC' enum"""

    def test_inheritance__byte_enum(self):
        assert issubclass(NRC, ByteEnum)

    def test_inheritance__validated_enum(self):
        assert issubclass(NRC, ValidatedEnum)

    def test_inheritance__extendable_enum(self):
        assert issubclass(NRC, ExtendableEnum)


@pytest.mark.functional
class TestNRCFunctional:
    """Functional tests for NRC class."""

    SPECIFIC_CONDITIONS_NOT_CORRECT_VALUES = range(0x95, 0xF0)
    SYSTEM_SPECIFIC_VALUES = range(0xF0, 0xFF)

    @pytest.mark.parametrize("undefined_value", list(SPECIFIC_CONDITIONS_NOT_CORRECT_VALUES) + list(SYSTEM_SPECIFIC_VALUES))
    def test_undefined_value(self, undefined_value):
        assert NRC.is_member(undefined_value) is False

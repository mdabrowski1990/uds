from uds.messages.nrc import NRC, \
    ByteEnum, ValidatedEnum, ExtendableEnum


class TestNRC:
    """Tests for 'NRC' enum"""

    def test_inheritance__byte_enum(self):
        assert issubclass(NRC, ByteEnum)

    def test_inheritance__validated_enum(self):
        assert issubclass(NRC, ValidatedEnum)

    def test_inheritance__extendable_enum(self):
        assert issubclass(NRC, ExtendableEnum)

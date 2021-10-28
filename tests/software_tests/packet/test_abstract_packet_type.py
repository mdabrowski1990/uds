from uds.packet.abstract_packet_type import AbstractUdsPacketType
from uds.utilities import NibbleEnum, ValidatedEnum, ExtendableEnum


class TestAbstractPacketType:
    """Tests for 'AbstractPacketType' class."""

    SCRIPT_LOCATION = "uds.packet.abstract_packet"

    def test_inheritance__nibble_enum(self):
        assert issubclass(AbstractUdsPacketType, NibbleEnum)

    def test_inheritance__validated_enum(self):
        assert issubclass(AbstractUdsPacketType, ValidatedEnum)

    def test_inheritance__extendable_enum(self):
        assert issubclass(AbstractUdsPacketType, ExtendableEnum)

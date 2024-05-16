from uds.packet.abstract_packet_type import AbstractUdsPacketType
from uds.utilities import ExtendableEnum, NibbleEnum, ValidatedEnum

SCRIPT_LOCATION = "uds.packet.abstract_packet"


class TestAbstractPacketType:
    """Unit tests for 'AbstractPacketType' class."""

    def test_inheritance__nibble_enum(self):
        assert issubclass(AbstractUdsPacketType, NibbleEnum)

    def test_inheritance__validated_enum(self):
        assert issubclass(AbstractUdsPacketType, ValidatedEnum)

    def test_inheritance__extendable_enum(self):
        assert issubclass(AbstractUdsPacketType, ExtendableEnum)

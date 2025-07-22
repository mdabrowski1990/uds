import pytest
from mock import patch

from uds.can.packet.can_packet_type import CanPacketType
from uds.packet import AbstractPacketType

SCRIPT_LOCATION = "uds.can.packet.can_packet_type"


class TestCanPacketType:
    """Unit tests for `CanPacketType` class."""

    # inheritance

    def test_inheritance__abstract_packet_type(self):
        assert issubclass(CanPacketType, AbstractPacketType)

    # is_initial_packet_type

    @pytest.mark.parametrize("value", [CanPacketType.CONSECUTIVE_FRAME, CanPacketType.FLOW_CONTROL])
    @patch(f"{SCRIPT_LOCATION}.CanPacketType.validate_member")
    def test_is_initial_packet_type__false(self, mock_validate_member, value):
        mock_validate_member.side_effect = lambda arg: arg
        assert CanPacketType.is_initial_packet_type(value) is False
        mock_validate_member.assert_called_once_with(value)

    @pytest.mark.parametrize("value", [CanPacketType.FIRST_FRAME, CanPacketType.SINGLE_FRAME])
    @patch(f"{SCRIPT_LOCATION}.CanPacketType.validate_member")
    def test_is_initial_packet_type__true(self, mock_validate_member, value):
        mock_validate_member.side_effect = lambda arg: arg
        assert CanPacketType.is_initial_packet_type(value) is True
        mock_validate_member.assert_called_once_with(value)

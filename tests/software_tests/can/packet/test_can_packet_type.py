import pytest
from mock import patch

from uds.packet import AbstractPacketType
from uds.packet.can import CanPacketType


class TestCanPacketType:
    """Unit tests for `CanPacketType` class."""

    def setup_method(self):
        self._patcher_validate_member = patch("uds.utilities.ValidatedEnum.validate_member")
        self.mock_validate_member = self._patcher_validate_member.start()

    def teardown_method(self):
        self._patcher_validate_member.stop()

    # inheritance

    def test_inheritance__abstract_packet_type(self):
        assert issubclass(CanPacketType, AbstractPacketType)

    # is_initial_packet_type

    @pytest.mark.parametrize("value", [2, 3, CanPacketType.CONSECUTIVE_FRAME, CanPacketType.FLOW_CONTROL])
    def test_is_initial_packet_type__false(self, value):
        self.mock_validate_member.side_effect = lambda arg: arg
        assert CanPacketType.is_initial_packet_type(value) is False
        self.mock_validate_member.assert_called_once_with(value)

    @pytest.mark.parametrize("value", [0, 1, CanPacketType.FIRST_FRAME, CanPacketType.SINGLE_FRAME])
    def test_is_initial_packet_type__true(self, value):
        self.mock_validate_member.side_effect = lambda arg: arg
        assert CanPacketType.is_initial_packet_type(value) is True
        self.mock_validate_member.assert_called_once_with(value)

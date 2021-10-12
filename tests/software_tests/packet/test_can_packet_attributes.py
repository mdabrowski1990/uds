import pytest

from mock import patch

from uds.packet.can_packet_attributes import CanIdHandler, CanPacketType, CanAddressingFormat
from uds.packet.abstract_packet import AbstractUdsPacketType
from uds.utilities import ValidatedEnum


class TestCanIdHandler:
    """Tests for `CanIdHandler` class."""

    SCRIPT_LOCATION = "uds.packet.can_packet_attributes"

    # is_standard_can_id

    @pytest.mark.parametrize("value", [CanIdHandler.MIN_11BIT_VALUE, CanIdHandler.MIN_11BIT_VALUE+1,
                                       CanIdHandler.MAX_11BIT_VALUE, CanIdHandler.MAX_11BIT_VALUE-1,
                                       (CanIdHandler.MIN_11BIT_VALUE + CanIdHandler.MAX_11BIT_VALUE) // 2])
    def test_is_standard_can_id__true(self, value):
        assert CanIdHandler.is_standard_can_id(value) is True

    @pytest.mark.parametrize("value", [CanIdHandler.MIN_11BIT_VALUE-1, CanIdHandler.MAX_11BIT_VALUE+1,
                                       -1, -CanIdHandler.MAX_11BIT_VALUE])
    def test_is_standard_can_id__false(self, value):
        assert CanIdHandler.is_standard_can_id(value) is False

    # is_extended_can_id

    @pytest.mark.parametrize("value", [CanIdHandler.MIN_29BIT_VALUE, CanIdHandler.MIN_29BIT_VALUE+1,
                                       CanIdHandler.MAX_29BIT_VALUE, CanIdHandler.MAX_29BIT_VALUE-1,
                                       (CanIdHandler.MIN_29BIT_VALUE + CanIdHandler.MAX_29BIT_VALUE) // 2])
    def test_is_extended_can_id__true(self, value):
        assert CanIdHandler.is_extended_can_id(value) is True

    @pytest.mark.parametrize("value", [CanIdHandler.MIN_29BIT_VALUE-1, CanIdHandler.MAX_29BIT_VALUE+1,
                                       -CanIdHandler.MIN_29BIT_VALUE])
    def test_is_extended_can_id__false(self, value):
        assert CanIdHandler.is_extended_can_id(value) is False

    # is_can_id

    @pytest.mark.parametrize("is_standard_id, is_extended_id, expected_result", [
        (True, True, True),
        (True, False, True),
        (False, True, True),
        (False, False, False),
    ])
    @pytest.mark.parametrize("value", [-100, 1, 5000, 1234567, 9999999999])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_extended_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_standard_can_id")
    def test_is_can_id(self, mock_is_standard_id, mock_is_extended_can_id,
                       value, is_standard_id, is_extended_id, expected_result):
        mock_is_standard_id.return_value = is_standard_id
        mock_is_extended_can_id.return_value = is_extended_id
        assert CanIdHandler.is_can_id(value) is expected_result

    # validate_can_id

    @pytest.mark.parametrize("value", [None, 5., "not a CAN ID", (0,)])
    def test_validate_can_id__type_error(self, value):
        with pytest.raises(TypeError):
            CanIdHandler.validate_can_id(value)

    @pytest.mark.parametrize("value", [-100, 1, 5000, 1234567, 9999999999])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_can_id")
    def test_validate_can_id__value_error(self, mock_is_can_id, value):
        mock_is_can_id.return_value = False
        with pytest.raises(ValueError):
            CanIdHandler.validate_can_id(value)
        mock_is_can_id.assert_called_once_with(value)

    @pytest.mark.parametrize("value", [-100, 1, 5000, 1234567, 9999999999])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_can_id")
    def test_validate_can_id__valid(self, mock_is_can_id, value):
        mock_is_can_id.return_value = True
        assert CanIdHandler.validate_can_id(value) is None
        mock_is_can_id.assert_called_once_with(value)


class TestCanPacketType:
    """Tests for `CanPacketType` class."""

    def setup(self):
        self._patcher_validate_member = patch("uds.utilities.ValidatedEnum.validate_member")
        self.mock_validate_member = self._patcher_validate_member.start()

    def teardown(self):
        self._patcher_validate_member.stop()

    def test_inheritance__abstract_packet_type(self):
        assert issubclass(CanPacketType, AbstractUdsPacketType)

    @pytest.mark.parametrize("value", [2, 3, CanPacketType.CONSECUTIVE_FRAME, CanPacketType.FLOW_CONTROL])
    def test_is_initial_packet_type__false(self, value):
        assert CanPacketType.is_initial_packet_type(value) is False
        self.mock_validate_member.assert_called_once_with(value)

    @pytest.mark.parametrize("value", [0, 1, CanPacketType.FIRST_FRAME, CanPacketType.SINGLE_FRAME])
    def test_is_initial_packet_type__true(self, value):
        assert CanPacketType.is_initial_packet_type(value) is True
        self.mock_validate_member.assert_called_once_with(value)


class TestCanAddressingFormat:
    """Tests for `CanAddressingFormat` class."""

    def test_inheritance__validated_enum(self):
        assert issubclass(CanAddressingFormat, ValidatedEnum)

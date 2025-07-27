import pytest
from mock import Mock, patch

from uds.can.frame import CanDlcHandler, CanIdHandler

SCRIPT_LOCATION = "uds.can.frame"


class TestCanIdHandler:
    """Unit tests for `CanIdHandler` class."""

    # is_can_id

    @pytest.mark.parametrize("is_standard_id, is_extended_id", [
        (True, True),
        (True, False),
        (False, True,),
        (False, False),
    ])
    @pytest.mark.parametrize("value", [5000, 1234567])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_extended_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_standard_can_id")
    def test_is_can_id(self, mock_is_standard_id, mock_is_extended_can_id,
                       value, is_standard_id, is_extended_id):
        mock_is_standard_id.return_value = is_standard_id
        mock_is_extended_can_id.return_value = is_extended_id
        assert CanIdHandler.is_can_id(value) is (is_standard_id or is_extended_id)

    # is_standard_can_id

    @pytest.mark.parametrize("value", [CanIdHandler.MIN_STANDARD_VALUE,
                                       CanIdHandler.MAX_STANDARD_VALUE,
                                       (CanIdHandler.MIN_STANDARD_VALUE + CanIdHandler.MAX_STANDARD_VALUE) // 2])
    def test_is_standard_can_id__true(self, value):
        assert CanIdHandler.is_standard_can_id(value) is True

    @pytest.mark.parametrize("value", [CanIdHandler.MIN_STANDARD_VALUE - 1,
                                       CanIdHandler.MAX_STANDARD_VALUE + 1,
                                       float(CanIdHandler.MIN_STANDARD_VALUE)])
    def test_is_standard_can_id__false(self, value):
        assert CanIdHandler.is_standard_can_id(value) is False

    # is_extended_can_id

    @pytest.mark.parametrize("value", [CanIdHandler.MIN_EXTENDED_VALUE,
                                       CanIdHandler.MAX_EXTENDED_VALUE,
                                       (CanIdHandler.MIN_EXTENDED_VALUE + CanIdHandler.MAX_EXTENDED_VALUE) // 2])
    def test_is_extended_can_id__true(self, value):
        assert CanIdHandler.is_extended_can_id(value) is True

    @pytest.mark.parametrize("value", [CanIdHandler.MIN_EXTENDED_VALUE - 1,
                                       CanIdHandler.MAX_EXTENDED_VALUE + 1,
                                       float(CanIdHandler.MIN_EXTENDED_VALUE)])
    def test_is_extended_can_id__false(self, value):
        assert CanIdHandler.is_extended_can_id(value) is False

    # validate_can_id

    @pytest.mark.parametrize("value", [None, 5., "not a CAN ID"])
    @pytest.mark.parametrize("extended_can_id", [None, True, False])
    def test_validate_can_id__type_error(self, value, extended_can_id):
        with pytest.raises(TypeError):
            CanIdHandler.validate_can_id(value, extended_can_id=extended_can_id)

    @pytest.mark.parametrize("value", [5000, 1234567])
    @pytest.mark.parametrize("extended_can_id", [None, True, False])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_extended_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_standard_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_can_id")
    def test_validate_can_id__value_error(self, mock_is_can_id, mock_is_standard_can_id, mock_is_extended_can_id,
                                          value, extended_can_id):
        mock_is_can_id.return_value = False
        mock_is_standard_can_id.return_value = False
        mock_is_extended_can_id.return_value = False
        with pytest.raises(ValueError):
            CanIdHandler.validate_can_id(value, extended_can_id=extended_can_id)
        if extended_can_id is None:
            mock_is_can_id.assert_called_once_with(value)
            mock_is_standard_can_id.assert_not_called()
            mock_is_extended_can_id.assert_not_called()
        elif extended_can_id:
            mock_is_can_id.assert_not_called()
            mock_is_standard_can_id.assert_not_called()
            mock_is_extended_can_id.assert_called_once_with(value)
        else:
            mock_is_can_id.assert_not_called()
            mock_is_standard_can_id.assert_called_once_with(value)
            mock_is_extended_can_id.assert_not_called()

    @pytest.mark.parametrize("value", [5000, 1234567])
    @pytest.mark.parametrize("extended_can_id", [None, True, False])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_extended_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_standard_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_can_id")
    def test_validate_can_id__valid(self, mock_is_can_id, mock_is_standard_can_id, mock_is_extended_can_id,
                                    value, extended_can_id):
        mock_is_can_id.return_value = True
        mock_is_standard_can_id.return_value = True
        mock_is_extended_can_id.return_value = True
        assert CanIdHandler.validate_can_id(value, extended_can_id=extended_can_id) is None
        if extended_can_id is None:
            mock_is_can_id.assert_called_once_with(value)
            mock_is_standard_can_id.assert_not_called()
            mock_is_extended_can_id.assert_not_called()
        elif extended_can_id:
            mock_is_can_id.assert_not_called()
            mock_is_standard_can_id.assert_not_called()
            mock_is_extended_can_id.assert_called_once_with(value)
        else:
            mock_is_can_id.assert_not_called()
            mock_is_standard_can_id.assert_called_once_with(value)
            mock_is_extended_can_id.assert_not_called()

    # validate_priority

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_validate_priority__type_error(self, mock_isinstance):
        mock_isinstance.return_value = False
        value = Mock()
        with pytest.raises(TypeError):
            CanIdHandler.validate_priority(value)
        mock_isinstance.assert_called_once_with(value, int)

    @pytest.mark.parametrize("value", [CanIdHandler.MIN_PRIORITY_VALUE - 1,
                                       CanIdHandler.MAX_PRIORITY_VALUE + 1])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_validate_priority__value_error(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        with pytest.raises(ValueError):
            CanIdHandler.validate_priority(value)
        mock_isinstance.assert_called_once_with(value, int)

    @pytest.mark.parametrize("value", [CanIdHandler.MIN_PRIORITY_VALUE,
                                       CanIdHandler.DEFAULT_PRIORITY_VALUE - 1,
                                       CanIdHandler.MAX_PRIORITY_VALUE])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_validate_priority__valid(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        assert CanIdHandler.validate_priority(value) is None
        mock_isinstance.assert_called_once_with(value, int)


class TestCanDlcHandler:
    """Unit tests for `CanDlcHandler` class."""

    # decode_dlc

    @pytest.mark.parametrize("dlc, data_bytes_number", [
        (0, 0),
        (8, 8),
        (9, 12),
        (10, 16),
        (11, 20),
        (12, 24),
        (13, 32),
        (14, 48),
        (15, 64),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanDlcHandler.validate_dlc")
    def test_decode(self, mock_validate_dlc, dlc, data_bytes_number):
        assert CanDlcHandler.decode_dlc(dlc) == data_bytes_number
        mock_validate_dlc.assert_called_once_with(dlc)

    # encode_dlc

    @pytest.mark.parametrize("dlc, data_bytes_number", [
        (0, 0),
        (8, 8),
        (9, 12),
        (10, 16),
        (11, 20),
        (12, 24),
        (13, 32),
        (14, 48),
        (15, 64),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanDlcHandler.validate_data_bytes_number")
    def test_encode(self, mock_validate_data_bytes_number, dlc, data_bytes_number):
        assert CanDlcHandler.encode_dlc(data_bytes_number) == dlc
        mock_validate_data_bytes_number.assert_called_once_with(data_bytes_number, True)

    # get_min_dlc

    @pytest.mark.parametrize("data_bytes_number, min_dlc", [
        (64, 0xF),
        (33, 0xE),
        (32, 0xD),
        (12, 0x9),
        (9, 0x9),
        (8, 0x8),
        (6, 0x6),
        (1, 0x1),
        (0, 0x0),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanDlcHandler.validate_data_bytes_number")
    def test_get_min_dlc(self, mock_validate_data_bytes_number, data_bytes_number, min_dlc):
        assert CanDlcHandler.get_min_dlc(data_bytes_number) == min_dlc
        mock_validate_data_bytes_number.assert_called_once_with(data_bytes_number, False)

    # is_can_fd_specific_value

    @pytest.mark.parametrize("value", [CanDlcHandler.MIN_BASE_UDS_DLC + 1, CanDlcHandler.MAX_DLC_VALUE])
    def test_is_can_fd_specific_value__true(self, value):
        assert CanDlcHandler.is_can_fd_specific_dlc(value) is True

    @pytest.mark.parametrize("value", [CanDlcHandler.MIN_DLC_VALUE, CanDlcHandler.MIN_BASE_UDS_DLC])
    def test_is_can_fd_specific_value__false(self, value):
        assert CanDlcHandler.is_can_fd_specific_dlc(value) is False

    # validate_dlc

    @pytest.mark.parametrize("value", [Mock(), "not a DLC"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_validate_dlc__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            CanDlcHandler.validate_dlc(value)
        mock_isinstance.assert_called_once_with(value, int)

    @pytest.mark.parametrize("value", [CanDlcHandler.MIN_DLC_VALUE - 1, CanDlcHandler.MAX_DLC_VALUE + 1])
    def test_validate_dlc__value_error(self, value):
        with pytest.raises(ValueError):
            CanDlcHandler.validate_dlc(value)

    @pytest.mark.parametrize("value", [CanDlcHandler.MIN_DLC_VALUE, 8, CanDlcHandler.MAX_DLC_VALUE])
    def test_validate_dlc__valid(self, value):
        assert CanDlcHandler.validate_dlc(value) is None

    # validate_data_bytes_number

    @pytest.mark.parametrize("value", [None, 2., "not a number of bytes"])
    def test_validate_data_bytes_number__type_error(self, value):
        with pytest.raises(TypeError):
            CanDlcHandler.validate_data_bytes_number(value)

    @pytest.mark.parametrize("value, exact_match", [
        (CanDlcHandler.MIN_DATA_BYTES_NUMBER - 1, False),
        (41, True),
        (CanDlcHandler.MAX_DATA_BYTES_NUMBER + 1, False),
    ])
    def test_validate_data_bytes_number__value_error(self, value, exact_match):
        with pytest.raises(ValueError):
            CanDlcHandler.validate_data_bytes_number(value, exact_match)

    @pytest.mark.parametrize("value, exact_match", [
        (CanDlcHandler.MIN_DATA_BYTES_NUMBER, True),
        (CanDlcHandler.MAX_DATA_BYTES_NUMBER - 1, False),
        (CanDlcHandler.MAX_DATA_BYTES_NUMBER, True),
    ])
    def test_validate_data_bytes_number__valid(self, value, exact_match):
        assert CanDlcHandler.validate_data_bytes_number(value, exact_match) is None


@pytest.mark.integration
class TestCanDlcHandlerIntegration:
    """Integration tests for `CanDlcHandler` class."""

    @pytest.mark.parametrize("data_bytes_number", [CanDlcHandler.MIN_DATA_BYTES_NUMBER,
                                                   8,
                                                   CanDlcHandler.MAX_DATA_BYTES_NUMBER])
    def test_encode_decode(self, data_bytes_number):
        dlc_value = CanDlcHandler.encode_dlc(data_bytes_number)
        assert CanDlcHandler.decode_dlc(dlc_value) == data_bytes_number

    @pytest.mark.parametrize("dlc", range(CanDlcHandler.MIN_DLC_VALUE, CanDlcHandler.MAX_DLC_VALUE + 1))
    def test_decode_encode(self, dlc):
        data_bytes_number = CanDlcHandler.decode_dlc(dlc)
        assert CanDlcHandler.encode_dlc(data_bytes_number) == dlc

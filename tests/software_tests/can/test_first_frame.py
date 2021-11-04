import pytest
from mock import patch

from uds.can.first_frame import CanFirstFrameHandler


class TestCanFirstFrameHandler:
    """Tests for `CanFirstFrameHandler` class."""

    SCRIPT_LOCATION = "uds.can.first_frame"

    # is_first_frame

    @pytest.mark.parametrize("addressing_format, raw_frame_data, ff_dl_data_bytes", [
        ("some addressing", "some raw frame", [0x10, 0x06]),
        ("some other addressing", "some other raw frame", [0x10, 0x00, 0x12, 0x34, 0x56]),
        ("Mixed", range(20), [0x1F, 0xED]),
        ("Extended", [0x10, 0x20, 0x30], [0x10]),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanFirstFrameHandler._CanFirstFrameHandler__extract_ff_dl_data_bytes")
    def test_is_first_frame__true(self, mock_extract_ff_dl_data_bytes,
                                  addressing_format, raw_frame_data, ff_dl_data_bytes):
        mock_extract_ff_dl_data_bytes.return_value = ff_dl_data_bytes
        assert CanFirstFrameHandler.is_first_frame(addressing_format=addressing_format,
                                                   raw_frame_data=raw_frame_data) is True
        mock_extract_ff_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)

    @pytest.mark.parametrize("addressing_format, raw_frame_data, ff_dl_data_bytes", [
        ("some addressing", "some raw frame", [0x80, 0x06]),
        ("some other addressing", "some other raw frame", [0x40, 0x00, 0x12, 0x34, 0x56]),
        ("Mixed", range(20), [0x2F, 0xED]),
        ("Extended", [0x10, 0x20, 0x30], [0xF0]),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanFirstFrameHandler._CanFirstFrameHandler__extract_ff_dl_data_bytes")
    def test_is_first_frame__false(self, mock_extract_ff_dl_data_bytes,
                                   addressing_format, raw_frame_data, ff_dl_data_bytes):
        mock_extract_ff_dl_data_bytes.return_value = ff_dl_data_bytes
        assert CanFirstFrameHandler.is_first_frame(addressing_format=addressing_format,
                                                   raw_frame_data=raw_frame_data) is False
        mock_extract_ff_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)

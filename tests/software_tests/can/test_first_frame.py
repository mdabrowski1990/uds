import pytest
from mock import patch

from uds.can.first_frame import CanFirstFrameHandler, \
    InconsistentArgumentsError


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

    # __create_ff_dl_data_bytes

    @pytest.mark.parametrize("ff_dl, long_ff_dl_format, expected_ff_dl_bytes", [
        (0x0, False, [0x10, 0x00]),
        (0x0, True, [0x10, 0x00, 0x00, 0x00, 0x00, 0x00]),
        (0xFFF, False, [0x1F, 0xFF]),
        (0xFFFFFFFF, True, [0x10, 0x00, 0xFF, 0xFF, 0xFF, 0xFF]),
        (0xF4A, False, [0x1F, 0x4A]),
        (0x9BE08721, True, [0x10, 0x00, 0x9B, 0xE0, 0x87, 0x21]),
    ])
    def test_create_ff_dl_data_bytes__valid(self, ff_dl, long_ff_dl_format, expected_ff_dl_bytes):
        assert CanFirstFrameHandler._CanFirstFrameHandler__create_ff_dl_data_bytes(long_ff_dl_format=long_ff_dl_format,
                                                                                   ff_dl=ff_dl) == expected_ff_dl_bytes

    @pytest.mark.parametrize("ff_dl", [None, 2., "something not right"])
    @pytest.mark.parametrize("long_ff_dl_format", [True, False])
    def test_create_ff_dl_data_bytes__type_error(self, ff_dl, long_ff_dl_format):
        with pytest.raises(TypeError):
            CanFirstFrameHandler._CanFirstFrameHandler__create_ff_dl_data_bytes(long_ff_dl_format=long_ff_dl_format,
                                                                                ff_dl=ff_dl)

    @pytest.mark.parametrize("ff_dl", [-1, CanFirstFrameHandler.MAX_LONG_FF_DL_VALUE + 1])
    @pytest.mark.parametrize("long_ff_dl_format", [True, False])
    def test_create_ff_dl_data_bytes__value_error(self, ff_dl, long_ff_dl_format):
        with pytest.raises(ValueError):
            CanFirstFrameHandler._CanFirstFrameHandler__create_ff_dl_data_bytes(long_ff_dl_format=long_ff_dl_format,
                                                                                ff_dl=ff_dl)

    @pytest.mark.parametrize("ff_dl", [CanFirstFrameHandler.MAX_LONG_FF_DL_VALUE,
                                       CanFirstFrameHandler.MAX_SHORT_FF_DL_VALUE + 1])
    def test_create_ff_dl_data_bytes__inconsistent_value(self, ff_dl):
        with pytest.raises(InconsistentArgumentsError):
            CanFirstFrameHandler._CanFirstFrameHandler__create_ff_dl_data_bytes(long_ff_dl_format=False,
                                                                                ff_dl=ff_dl)

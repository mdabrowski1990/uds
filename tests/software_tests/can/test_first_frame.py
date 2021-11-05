import pytest
from mock import patch

from uds.can.first_frame import CanFirstFrameHandler, \
    InconsistentArgumentsError


class TestCanFirstFrameHandler:
    """Tests for `CanFirstFrameHandler` class."""

    SCRIPT_LOCATION = "uds.can.first_frame"

    def setup(self):
        self._patcher_get_ai_data_bytes_number = \
            patch(f"{self.SCRIPT_LOCATION}.CanAddressingInformationHandler.get_ai_data_bytes_number")
        self.mock_get_ai_data_bytes_number = self._patcher_get_ai_data_bytes_number.start()
        self._patcher_get_max_sf_dl = patch(f"{self.SCRIPT_LOCATION}.CanSingleFrameHandler.get_max_payload_size")
        self.mock_get_max_sf_dl = self._patcher_get_max_sf_dl.start()

    def teardown(self):
        self._patcher_get_ai_data_bytes_number.stop()
        self._patcher_get_max_sf_dl.stop()

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

    # validate_frame_data

    @pytest.mark.parametrize("addressing_format", ["any format", "another format"])
    @pytest.mark.parametrize("raw_frame_data", [range(10), list(range(20, 25))])
    @patch(f"{SCRIPT_LOCATION}.CanFirstFrameHandler.is_first_frame")
    def test_validate_frame_data__value_error(self, mock_is_first_frame,
                                              addressing_format, raw_frame_data):
        mock_is_first_frame.return_value = False
        with pytest.raises(ValueError):
            CanFirstFrameHandler.validate_frame_data(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
        mock_is_first_frame.assert_called_once_with(addressing_format=addressing_format, raw_frame_data=raw_frame_data)

    # validate_ff_dl

    @pytest.mark.parametrize("ff_dl", [None, "something", 2.])
    @pytest.mark.parametrize("dlc", [None, "anything"])
    @pytest.mark.parametrize("addressing_format", [None, "any format"])
    def test_validate_ff_dl__type_error(self, ff_dl, dlc, addressing_format):
        with pytest.raises(TypeError):
            CanFirstFrameHandler.validate_ff_dl(ff_dl=ff_dl, dlc=dlc, addressing_format=addressing_format)

    @pytest.mark.parametrize("ff_dl", [-1, 0, CanFirstFrameHandler.MAX_LONG_FF_DL_VALUE + 1])
    @pytest.mark.parametrize("dlc", [None, "anything"])
    @pytest.mark.parametrize("addressing_format", [None, "any format"])
    def test_validate_ff_dl__value_error(self, ff_dl, dlc, addressing_format):
        with pytest.raises(ValueError):
            CanFirstFrameHandler.validate_ff_dl(ff_dl=ff_dl, dlc=dlc, addressing_format=addressing_format)

    @pytest.mark.parametrize("ff_dl, sf_dl", [
        (5, 5),
        (2, 5),
        (100, 100),
    ])
    @pytest.mark.parametrize("dlc", ["anything", "something else"])
    @pytest.mark.parametrize("addressing_format", ["any format", "another format"])
    def test_validate_ff_dl__inconsistent_sf(self, ff_dl, dlc, addressing_format, sf_dl):
        self.mock_get_max_sf_dl.return_value = sf_dl
        with pytest.raises(InconsistentArgumentsError):
            CanFirstFrameHandler.validate_ff_dl(ff_dl=ff_dl, dlc=dlc, addressing_format=addressing_format)
        self.mock_get_max_sf_dl.assert_called_once_with(dlc=dlc, addressing_format=addressing_format)

    @pytest.mark.parametrize("ff_dl, long_ff_dl_format", [
        (CanFirstFrameHandler.MAX_SHORT_FF_DL_VALUE - 1, True),
        (CanFirstFrameHandler.MAX_SHORT_FF_DL_VALUE, True),
        (CanFirstFrameHandler.MAX_SHORT_FF_DL_VALUE + 1, False),
        (CanFirstFrameHandler.MAX_LONG_FF_DL_VALUE, False),
    ])
    def test_validate_ff_dl__inconsistent_format(self, ff_dl, long_ff_dl_format):
        with pytest.raises(InconsistentArgumentsError):
            CanFirstFrameHandler.validate_ff_dl(ff_dl=ff_dl, long_ff_dl_format=long_ff_dl_format)

    @pytest.mark.parametrize("ff_dl, sf_dl, long_ff_dl_format", [
        (6, 5, False),
        (25, 5, False),
        (101, 100, False),
        (CanFirstFrameHandler.MAX_SHORT_FF_DL_VALUE + 1, 100, True),
        (CanFirstFrameHandler.MAX_LONG_FF_DL_VALUE, 100, True),
    ])
    @pytest.mark.parametrize("dlc", ["anything", "something else"])
    @pytest.mark.parametrize("addressing_format", ["any format", "another format"])
    def test_validate_ff_dl__valid_with_args(self, ff_dl, long_ff_dl_format, dlc, addressing_format, sf_dl):
        self.mock_get_max_sf_dl.return_value = sf_dl
        CanFirstFrameHandler.validate_ff_dl(ff_dl=ff_dl,
                                            dlc=dlc,
                                            addressing_format=addressing_format,
                                            long_ff_dl_format=long_ff_dl_format)
        self.mock_get_max_sf_dl.assert_called_once_with(dlc=dlc, addressing_format=addressing_format)

    @pytest.mark.parametrize("ff_dl", [1, 100, CanFirstFrameHandler.MAX_LONG_FF_DL_VALUE])
    def test_validate_ff_dl__valid_without_args(self, ff_dl):
        CanFirstFrameHandler.validate_ff_dl(ff_dl=ff_dl)
        self.mock_get_max_sf_dl.assert_not_called()

    # __extract_ff_dl_data_bytes

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("raw_frame_data, ai_data_bytes, ff_dl_bytes", [
        ((0x10, 0x01), 0, [0x10, 0x01]),
        ([0x11, 0x11, 0x23, 0xEF, 0xCD, 0xAB, 0x89], 1, [0x11, 0x23]),
        ((0xFE, 0x1F, 0xFF, 0xEF, 0xCD, 0xAB, 0x89, 0x67), 1, [0x1F, 0xFF]),
        ([0x10, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0x89, 0x67], 0, [0x10, 0x00, 0xFF, 0xFF, 0xFF, 0xFF]),
        ([0x10, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x89, 0x67] + list(range(50)), 1, [0x10, 0x00, 0x00, 0x00, 0x00, 0x00]),
        ([0x10, 0x10, 0x00, 0xF0, 0xE1, 0xD2, 0xC3, 0x89, 0x67], 1, [0x10, 0x00, 0xF0, 0xE1, 0xD2, 0xC3]),
    ])
    def test_extract_ff_dl_data_bytes(self, addressing_format, raw_frame_data,
                                      ai_data_bytes, ff_dl_bytes):
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes
        assert CanFirstFrameHandler._CanFirstFrameHandler__extract_ff_dl_data_bytes(
            addressing_format=addressing_format, raw_frame_data=raw_frame_data) == ff_dl_bytes
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    # __encode_valid_ff_dl

    @pytest.mark.parametrize("ff_dl, long_format", [
        (CanFirstFrameHandler.MAX_SHORT_FF_DL_VALUE - 99999, False),
        (CanFirstFrameHandler.MAX_SHORT_FF_DL_VALUE - 1, False),
        (CanFirstFrameHandler.MAX_SHORT_FF_DL_VALUE, False),
        (CanFirstFrameHandler.MAX_SHORT_FF_DL_VALUE + 1, True),
        (CanFirstFrameHandler.MAX_SHORT_FF_DL_VALUE + 100, True),
        (CanFirstFrameHandler.MAX_LONG_FF_DL_VALUE, True),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanFirstFrameHandler._CanFirstFrameHandler__encode_any_ff_dl")
    def test_encode_valid_ff_dl(self, mock_encode_any_ff_dl, ff_dl, long_format):
        assert CanFirstFrameHandler._CanFirstFrameHandler__encode_valid_ff_dl(ff_dl=ff_dl) \
               == mock_encode_any_ff_dl.return_value
        mock_encode_any_ff_dl.assert_called_once_with(ff_dl=ff_dl, long_ff_dl_format=long_format)

    # __encode_any_ff_dl

    @pytest.mark.parametrize("ff_dl, long_ff_dl_format, expected_ff_dl_bytes", [
        (0x0, False, [0x10, 0x00]),
        (0x0, True, [0x10, 0x00, 0x00, 0x00, 0x00, 0x00]),
        (0xFFF, False, [0x1F, 0xFF]),
        (0xFFFFFFFF, True, [0x10, 0x00, 0xFF, 0xFF, 0xFF, 0xFF]),
        (0xF4A, False, [0x1F, 0x4A]),
        (0x9BE08721, True, [0x10, 0x00, 0x9B, 0xE0, 0x87, 0x21]),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanFirstFrameHandler.validate_ff_dl")
    def test_encode_any_ff_dl__valid(self, mock_validate_ff_dl,
                                     ff_dl, long_ff_dl_format, expected_ff_dl_bytes):
        assert CanFirstFrameHandler._CanFirstFrameHandler__encode_any_ff_dl(
            long_ff_dl_format=long_ff_dl_format, ff_dl=ff_dl) == expected_ff_dl_bytes == expected_ff_dl_bytes
        mock_validate_ff_dl.assert_called_once_with(ff_dl=ff_dl)

    @pytest.mark.parametrize("ff_dl", [CanFirstFrameHandler.MAX_LONG_FF_DL_VALUE,
                                       CanFirstFrameHandler.MAX_SHORT_FF_DL_VALUE + 1])
    @patch(f"{SCRIPT_LOCATION}.CanFirstFrameHandler.validate_ff_dl")
    def test_encode_any_ff_dl__inconsistent_value(self, mock_validate_ff_dl, ff_dl):
        with pytest.raises(InconsistentArgumentsError):
            CanFirstFrameHandler._CanFirstFrameHandler__encode_any_ff_dl(long_ff_dl_format=False,
                                                                         ff_dl=ff_dl)
        mock_validate_ff_dl.assert_called_once_with(ff_dl=ff_dl)

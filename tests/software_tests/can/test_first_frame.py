import pytest
from mock import patch

from uds.can.first_frame import CanFirstFrameHandler, \
    InconsistentArgumentsError, CanAddressingFormat, CanPacketType


class TestCanFirstFrameHandler:
    """Unit tests for `CanFirstFrameHandler` class."""

    SCRIPT_LOCATION = "uds.can.first_frame"

    def setup(self):
        self._patcher_validate_raw_bytes = patch(f"{self.SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
        self._patcher_bytes_list_to_int = patch(f"{self.SCRIPT_LOCATION}.bytes_list_to_int")
        self.mock_bytes_list_to_int = self._patcher_bytes_list_to_int.start()
        self._patcher_get_ai_data_bytes_number = \
            patch(f"{self.SCRIPT_LOCATION}.CanAddressingInformationHandler.get_ai_data_bytes_number")
        self.mock_get_ai_data_bytes_number = self._patcher_get_ai_data_bytes_number.start()
        self._patcher_encode_ai_data_bytes = \
            patch(f"{self.SCRIPT_LOCATION}.CanAddressingInformationHandler.encode_ai_data_bytes")
        self.mock_encode_ai_data_bytes = self._patcher_encode_ai_data_bytes.start()
        self._patcher_decode_dlc = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler.decode_dlc")
        self.mock_decode_dlc = self._patcher_decode_dlc.start()
        self._patcher_encode_dlc = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler.encode_dlc")
        self.mock_encode_dlc = self._patcher_encode_dlc.start()
        self._patcher_get_max_sf_dl = patch(f"{self.SCRIPT_LOCATION}.CanSingleFrameHandler.get_max_payload_size")
        self.mock_get_max_sf_dl = self._patcher_get_max_sf_dl.start()

    def teardown(self):
        self._patcher_bytes_list_to_int.stop()
        self._patcher_validate_raw_bytes.stop()
        self._patcher_get_ai_data_bytes_number.stop()
        self._patcher_encode_ai_data_bytes.stop()
        self._patcher_decode_dlc.stop()
        self._patcher_encode_dlc.stop()
        self._patcher_get_max_sf_dl.stop()

    # create_valid_frame_data

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, ff_dl", [
        ("some DLC", "some FF_DL"),
        (8, 9876543),
    ])
    @pytest.mark.parametrize("ai_data_bytes, ff_dl_data_bytes, payload", [
        ([], [0x12, 0x34], range(6)),
        ([0x9F], [0x10, 0x00, 0xFE, 0xDC, 0xBA, 0x98], list(range(90, 142))),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanFirstFrameHandler._CanFirstFrameHandler__encode_valid_ff_dl")
    def test_create_valid_frame_data__valid(self, mock_encode_valid_ff_dl,
                                            addressing_format, target_address, address_extension,
                                            payload, dlc, ff_dl,
                                            ai_data_bytes, ff_dl_data_bytes):
        self.mock_encode_ai_data_bytes.return_value = ai_data_bytes
        mock_encode_valid_ff_dl.return_value = ff_dl_data_bytes
        self.mock_decode_dlc.return_value = len(ai_data_bytes) + len(ff_dl_data_bytes) + len(payload)
        ff_data_bytes = CanFirstFrameHandler.create_valid_frame_data(addressing_format=addressing_format,
                                                                     target_address=target_address,
                                                                     address_extension=address_extension,
                                                                     payload=payload,
                                                                     dlc=dlc,
                                                                     ff_dl=ff_dl)
        self.mock_validate_raw_bytes.assert_called_once_with(payload)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        mock_encode_valid_ff_dl.assert_called_once_with(ff_dl=ff_dl, dlc=dlc, addressing_format=addressing_format)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        assert isinstance(ff_data_bytes, list)
        assert ff_data_bytes == list(ai_data_bytes) + list(ff_dl_data_bytes) + list(payload)

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, ff_dl", [
        ("some DLC", "some FF_DL"),
        (8, 9876543),
    ])
    @pytest.mark.parametrize("ai_data_bytes, ff_dl_data_bytes, payload, expected_frame_length", [
        ([], [0x12, 0x34], range(6), 7),
        ([0x9F], [0x10, 0x00, 0xFE, 0xDC, 0xBA, 0x98], list(range(90, 142)), 64),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanFirstFrameHandler._CanFirstFrameHandler__encode_valid_ff_dl")
    def test_create_valid_frame_data__inconsistent_length(self, mock_encode_valid_ff_dl,
                                                          addressing_format, target_address, address_extension,
                                                          payload, dlc, ff_dl,
                                                          ai_data_bytes, ff_dl_data_bytes, expected_frame_length):
        self.mock_encode_ai_data_bytes.return_value = ai_data_bytes
        mock_encode_valid_ff_dl.return_value = ff_dl_data_bytes
        self.mock_decode_dlc.return_value = expected_frame_length
        with pytest.raises(InconsistentArgumentsError):
            CanFirstFrameHandler.create_valid_frame_data(addressing_format=addressing_format,
                                                         target_address=target_address,
                                                         address_extension=address_extension,
                                                         payload=payload,
                                                         dlc=dlc,
                                                         ff_dl=ff_dl)
        self.mock_validate_raw_bytes.assert_called_once_with(payload)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        mock_encode_valid_ff_dl.assert_called_once_with(ff_dl=ff_dl, dlc=dlc, addressing_format=addressing_format)
        self.mock_decode_dlc.assert_called_once_with(dlc)

    # create_any_frame_data

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, ff_dl, long_ff_dl_format", [
        ("some DLC", "some FF_DL", True),
        (8, 9876543, False),
    ])
    @pytest.mark.parametrize("ai_data_bytes, ff_dl_data_bytes, payload", [
        ([], [0x12, 0x34], range(6)),
        ([0x9F], [0x10, 0x00, 0xFE, 0xDC, 0xBA, 0x98], list(range(90, 142))),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanFirstFrameHandler._CanFirstFrameHandler__encode_any_ff_dl")
    def test_create_any_frame_data__valid(self, mock_encode_any_ff_dl,
                                          addressing_format, target_address, address_extension,
                                          payload, dlc, ff_dl, long_ff_dl_format,
                                          ai_data_bytes, ff_dl_data_bytes):
        self.mock_encode_ai_data_bytes.return_value = ai_data_bytes
        mock_encode_any_ff_dl.return_value = ff_dl_data_bytes
        self.mock_decode_dlc.return_value = len(ai_data_bytes) + len(ff_dl_data_bytes) + len(payload)
        ff_data_bytes = CanFirstFrameHandler.create_any_frame_data(addressing_format=addressing_format,
                                                                   target_address=target_address,
                                                                   address_extension=address_extension,
                                                                   payload=payload,
                                                                   dlc=dlc,
                                                                   ff_dl=ff_dl,
                                                                   long_ff_dl_format=long_ff_dl_format)
        self.mock_validate_raw_bytes.assert_called_once_with(payload)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        mock_encode_any_ff_dl.assert_called_once_with(ff_dl=ff_dl, long_ff_dl_format=long_ff_dl_format)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        assert isinstance(ff_data_bytes, list)
        assert ff_data_bytes == list(ai_data_bytes) + list(ff_dl_data_bytes) + list(payload)

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, ff_dl, long_ff_dl_format", [
        ("some DLC", "some FF_DL", True),
        (8, 9876543, False),
    ])
    @pytest.mark.parametrize("ai_data_bytes, ff_dl_data_bytes, payload, expected_frame_length", [
        ([], [0x12, 0x34], range(6), 7),
        ([0x9F], [0x10, 0x00, 0xFE, 0xDC, 0xBA, 0x98], list(range(90, 142)), 64),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanFirstFrameHandler._CanFirstFrameHandler__encode_any_ff_dl")
    def test_create_any_frame_data__inconsistent_length(self, mock_encode_any_ff_dl,
                                                        addressing_format, target_address, address_extension,
                                                        payload, dlc, ff_dl, long_ff_dl_format,
                                                        ai_data_bytes, ff_dl_data_bytes, expected_frame_length):
        self.mock_encode_ai_data_bytes.return_value = ai_data_bytes
        mock_encode_any_ff_dl.return_value = ff_dl_data_bytes
        self.mock_decode_dlc.return_value = expected_frame_length
        with pytest.raises(InconsistentArgumentsError):
            CanFirstFrameHandler.create_any_frame_data(addressing_format=addressing_format,
                                                       target_address=target_address,
                                                       address_extension=address_extension,
                                                       payload=payload,
                                                       dlc=dlc,
                                                       ff_dl=ff_dl,
                                                       long_ff_dl_format=long_ff_dl_format)
        self.mock_validate_raw_bytes.assert_called_once_with(payload)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        mock_encode_any_ff_dl.assert_called_once_with(ff_dl=ff_dl, long_ff_dl_format=long_ff_dl_format)
        self.mock_decode_dlc.assert_called_once_with(dlc)

    # is_first_frame

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("raw_frame_data, ai_bytes_number", [
        ([0x10, 0xFE, 0xDC], 0),
        ([0xFE, 0x1F, 0xDC, 0xBA, 0x98, 0x76, 0x54], 1),
        ([0x1F, 0xFF, 0xFF, 0xFF] + list(range(20)), 0),
        ([0xFF, 0x1F, 0xFF, 0xFF] + list(range(60)), 1),
    ])
    def test_is_first_frame__true(self, addressing_format, raw_frame_data, ai_bytes_number):
        self.mock_get_ai_data_bytes_number.return_value = ai_bytes_number
        assert CanFirstFrameHandler.is_first_frame(addressing_format=addressing_format,
                                                   raw_frame_data=raw_frame_data) is True
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("raw_frame_data, ai_bytes_number", [
        ([0x20, 0xFE, 0xDC], 0),
        ([0xFE, 0x4F, 0xDC, 0xBA, 0x98, 0x76, 0x54], 1),
        ([0x8F, 0xFF, 0xFF, 0xFF] + list(range(20)), 0),
        ([0xFF, 0xFF, 0xFF, 0xFF] + list(range(60)), 1),
    ])
    def test_is_first_frame__false(self, addressing_format, raw_frame_data, ai_bytes_number):
        self.mock_get_ai_data_bytes_number.return_value = ai_bytes_number
        assert CanFirstFrameHandler.is_first_frame(addressing_format=addressing_format,
                                                   raw_frame_data=raw_frame_data) is False
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    # decode_payload

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        ("some addressing", tuple(range(20, 84))),
        ("another addressing", range(8)),
    ])
    @pytest.mark.parametrize("ff_dl_data_bytes", [[0x10], [0x1F, 0xFF], (0x10, 0x20, 0x30, 0xF2, 0xE7)])
    @pytest.mark.parametrize("ai_bytes_number", [0, 1])
    @patch(f"{SCRIPT_LOCATION}.CanFirstFrameHandler._CanFirstFrameHandler__extract_ff_dl_data_bytes")
    def test_decode_payload(self, mock_extract_ff_dl_data_bytes,
                            addressing_format, raw_frame_data,
                            ai_bytes_number, ff_dl_data_bytes):
        self.mock_get_ai_data_bytes_number.return_value = ai_bytes_number
        mock_extract_ff_dl_data_bytes.return_value = ff_dl_data_bytes
        payload = CanFirstFrameHandler.decode_payload(addressing_format=addressing_format,
                                                      raw_frame_data=raw_frame_data)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        mock_extract_ff_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)
        assert isinstance(payload, list)
        assert payload == list(raw_frame_data)[ai_bytes_number + len(ff_dl_data_bytes):]

    # decode_ff_dl

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        ("some addressing", "some data"),
        ("another addressing", range(8)),
    ])
    @pytest.mark.parametrize("ff_dl_data_bytes", [
        [0x10, 0x06],
        [0x1F, 0xFF],
        [0x15, 0x65],
    ])
    @patch(f"{SCRIPT_LOCATION}.CanFirstFrameHandler._CanFirstFrameHandler__extract_ff_dl_data_bytes")
    def test_decode_ff_dl__short(self, mock_extract_ff_dl_data_bytes,
                                 addressing_format, raw_frame_data, ff_dl_data_bytes):
        mock_extract_ff_dl_data_bytes.return_value = ff_dl_data_bytes
        assert CanFirstFrameHandler.decode_ff_dl(addressing_format=addressing_format,
                                                 raw_frame_data=raw_frame_data) == self.mock_bytes_list_to_int.return_value
        mock_extract_ff_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)
        ff_dl_data_bytes_without_npci = list(ff_dl_data_bytes)
        ff_dl_data_bytes_without_npci[0] = ff_dl_data_bytes[0] & 0xF
        self.mock_bytes_list_to_int.assert_called_once_with(ff_dl_data_bytes_without_npci)

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        ("some addressing", "some data"),
        ("another addressing", range(8)),
    ])
    @pytest.mark.parametrize("ff_dl_data_bytes", [
        [0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC],
        [0x10, 0x00, 0xFF, 0XFF, 0xFF, 0xFF],
    ])
    @patch(f"{SCRIPT_LOCATION}.CanFirstFrameHandler._CanFirstFrameHandler__extract_ff_dl_data_bytes")
    def test_decode_ff_dl__long(self, mock_extract_ff_dl_data_bytes,
                                addressing_format, raw_frame_data, ff_dl_data_bytes):
        mock_extract_ff_dl_data_bytes.return_value = ff_dl_data_bytes
        assert CanFirstFrameHandler.decode_ff_dl(addressing_format=addressing_format,
                                                 raw_frame_data=raw_frame_data) == self.mock_bytes_list_to_int.return_value
        mock_extract_ff_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)
        self.mock_bytes_list_to_int.assert_called_once_with(ff_dl_data_bytes[-4:])

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        ("some addressing", "some data"),
        ("another addressing", range(8)),
    ])
    @pytest.mark.parametrize("ff_dl_data_bytes", [
        [0x12, 0x34, 0x56],
        [0x10],
    ])
    @patch(f"{SCRIPT_LOCATION}.CanFirstFrameHandler._CanFirstFrameHandler__extract_ff_dl_data_bytes")
    def test_decode_ff_dl__unknown(self, mock_extract_ff_dl_data_bytes,
                                   addressing_format, raw_frame_data, ff_dl_data_bytes):
        mock_extract_ff_dl_data_bytes.return_value = ff_dl_data_bytes
        with pytest.raises(NotImplementedError):
            CanFirstFrameHandler.decode_ff_dl(addressing_format=addressing_format,
                                              raw_frame_data=raw_frame_data)
        mock_extract_ff_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)

    # get_payload_size

    @pytest.mark.parametrize("addressing_format", ["any format", "another format"])
    @pytest.mark.parametrize("dlc", [CanFirstFrameHandler.MIN_DLC_VALUE_FF-1, CanFirstFrameHandler.MIN_DLC_VALUE_FF-2])
    @pytest.mark.parametrize("long_ff_dl_format", [True, False])
    def test_get_payload_size__too_short_dlc(self, addressing_format, dlc, long_ff_dl_format):
        with pytest.raises(ValueError):
            CanFirstFrameHandler.get_payload_size(addressing_format=addressing_format,
                                                  dlc=dlc,
                                                  long_ff_dl_format=long_ff_dl_format)
        self.mock_decode_dlc.assert_not_called()
        self.mock_get_ai_data_bytes_number.assert_not_called()

    @pytest.mark.parametrize("addressing_format", ["any format", "another format"])
    @pytest.mark.parametrize("dlc", [CanFirstFrameHandler.MIN_DLC_VALUE_FF, CanFirstFrameHandler.MIN_DLC_VALUE_FF+1])
    @pytest.mark.parametrize("data_bytes_number, ai_bytes_number", [
        (8, 0),
        (8, 1),
        (48, 0),
        (64, 1),
    ])
    def test_get_payload_size__short(self, addressing_format, dlc,
                                     data_bytes_number, ai_bytes_number):
        self.mock_decode_dlc.return_value = data_bytes_number
        self.mock_get_ai_data_bytes_number.return_value = ai_bytes_number
        payload_size = CanFirstFrameHandler.get_payload_size(addressing_format=addressing_format,
                                                             dlc=dlc,
                                                             long_ff_dl_format=False)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        assert isinstance(payload_size, int)
        assert payload_size == data_bytes_number - ai_bytes_number - CanFirstFrameHandler.SHORT_FF_DL_BYTES_USED

    @pytest.mark.parametrize("addressing_format", ["any format", "another format"])
    @pytest.mark.parametrize("dlc", [CanFirstFrameHandler.MIN_DLC_VALUE_FF, CanFirstFrameHandler.MIN_DLC_VALUE_FF+1])
    @pytest.mark.parametrize("data_bytes_number, ai_bytes_number", [
        (8, 0),
        (8, 1),
        (48, 0),
        (64, 1),
    ])
    def test_get_payload_size__long(self, addressing_format, dlc,
                                    data_bytes_number, ai_bytes_number):
        self.mock_decode_dlc.return_value = data_bytes_number
        self.mock_get_ai_data_bytes_number.return_value = ai_bytes_number
        payload_size = CanFirstFrameHandler.get_payload_size(addressing_format=addressing_format,
                                                             dlc=dlc,
                                                             long_ff_dl_format=True)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        assert isinstance(payload_size, int)
        assert payload_size == data_bytes_number - ai_bytes_number - CanFirstFrameHandler.LONG_FF_DL_BYTES_USED

    # validate_frame_data

    @pytest.mark.parametrize("addressing_format", ["any format", "another format"])
    @pytest.mark.parametrize("raw_frame_data", [range(10), list(range(20, 25))])
    @patch(f"{SCRIPT_LOCATION}.CanFirstFrameHandler.is_first_frame")
    def test_validate_frame_data__value_error(self, mock_is_first_frame,
                                              addressing_format, raw_frame_data):
        mock_is_first_frame.return_value = False
        with pytest.raises(ValueError):
            CanFirstFrameHandler.validate_frame_data(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
        self.mock_validate_raw_bytes.assert_called_once_with(raw_frame_data)
        mock_is_first_frame.assert_called_once_with(addressing_format=addressing_format, raw_frame_data=raw_frame_data)

    @pytest.mark.parametrize("addressing_format", ["any format", "another format"])
    @pytest.mark.parametrize("raw_frame_data", [range(10), list(range(20, 25))])
    @pytest.mark.parametrize("ff_dl_data_bytes, long_ff_dl_format", [
        ([0x10, 0x3E], False),
        ([0x10, 0x00, 0xFE, 0xDC, 0xBA, 0x98], True),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanFirstFrameHandler._CanFirstFrameHandler__extract_ff_dl_data_bytes")
    @patch(f"{SCRIPT_LOCATION}.CanFirstFrameHandler.validate_ff_dl")
    @patch(f"{SCRIPT_LOCATION}.CanFirstFrameHandler.decode_ff_dl")
    @patch(f"{SCRIPT_LOCATION}.CanFirstFrameHandler.is_first_frame")
    def test_validate_frame_data__valid(self, mock_is_first_frame, mock_decode_ff_dl, mock_validate_ff_dl,
                                        mock_extract_ff_dl_data_bytes,
                                        addressing_format, raw_frame_data, ff_dl_data_bytes, long_ff_dl_format):
        mock_is_first_frame.return_value = True
        mock_extract_ff_dl_data_bytes.return_value = ff_dl_data_bytes
        CanFirstFrameHandler.validate_frame_data(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
        self.mock_validate_raw_bytes.assert_called_once_with(raw_frame_data)
        mock_is_first_frame.assert_called_once_with(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
        mock_decode_ff_dl.assert_called_once_with(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
        self.mock_encode_dlc.assert_called_once_with(len(raw_frame_data))
        mock_extract_ff_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)
        mock_validate_ff_dl.assert_called_once_with(ff_dl=mock_decode_ff_dl.return_value,
                                                    dlc=self.mock_encode_dlc.return_value,
                                                    long_ff_dl_format=long_ff_dl_format,
                                                    addressing_format=addressing_format)

    # validate_ff_dl

    @pytest.mark.parametrize("ff_dl", [None, "something", 2.])
    @pytest.mark.parametrize("dlc", [None, "anything"])
    @pytest.mark.parametrize("addressing_format", [None, "any format"])
    def test_validate_ff_dl__type_error(self, ff_dl, dlc, addressing_format):
        with pytest.raises(TypeError):
            CanFirstFrameHandler.validate_ff_dl(ff_dl=ff_dl, dlc=dlc, addressing_format=addressing_format)

    @pytest.mark.parametrize("ff_dl", [-1, CanFirstFrameHandler.MAX_LONG_FF_DL_VALUE + 1])
    @pytest.mark.parametrize("dlc", [None, "anything"])
    @pytest.mark.parametrize("addressing_format", [None, "any format"])
    def test_validate_ff_dl__value_error(self, ff_dl, dlc, addressing_format):
        with pytest.raises(ValueError):
            CanFirstFrameHandler.validate_ff_dl(ff_dl=ff_dl, dlc=dlc, addressing_format=addressing_format)

    @pytest.mark.parametrize("ff_dl", [0,
                                       CanFirstFrameHandler.MAX_SHORT_FF_DL_VALUE,
                                       CanFirstFrameHandler.MAX_LONG_FF_DL_VALUE])
    @pytest.mark.parametrize("dlc", [0, CanFirstFrameHandler.MIN_DLC_VALUE_FF - 1])
    @pytest.mark.parametrize("addressing_format", ["any format", "something else"])
    def test_validate_ff_dl__value_error__dlc(self, ff_dl, dlc, addressing_format):
        with pytest.raises(ValueError):
            CanFirstFrameHandler.validate_ff_dl(ff_dl=ff_dl, dlc=dlc, addressing_format=addressing_format)

    @pytest.mark.parametrize("ff_dl, sf_dl", [
        (5, 5),
        (2, 5),
        (100, 100),
    ])
    @pytest.mark.parametrize("dlc", [CanFirstFrameHandler.MIN_DLC_VALUE_FF, CanFirstFrameHandler.MIN_DLC_VALUE_FF + 2])
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
    @pytest.mark.parametrize("dlc", [CanFirstFrameHandler.MIN_DLC_VALUE_FF, CanFirstFrameHandler.MIN_DLC_VALUE_FF + 2])
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
        ([0x10, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x89, 0x67] + list(range(50)), 1,
         [0x10, 0x00, 0x00, 0x00, 0x00, 0x00]),
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
    @pytest.mark.parametrize("dlc, addressing_format", [
        ("any DLC", "some addressing format"),
        (12, "another addressing format"),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanFirstFrameHandler.validate_ff_dl")
    @patch(f"{SCRIPT_LOCATION}.CanFirstFrameHandler._CanFirstFrameHandler__encode_any_ff_dl")
    def test_encode_valid_ff_dl(self, mock_encode_any_ff_dl, mock_validate_ff_dl,
                                ff_dl, dlc, addressing_format, long_format):
        assert CanFirstFrameHandler._CanFirstFrameHandler__encode_valid_ff_dl(ff_dl=ff_dl,
                                                                              dlc=dlc,
                                                                              addressing_format=addressing_format) \
               == mock_encode_any_ff_dl.return_value
        mock_validate_ff_dl.assert_called_once_with(ff_dl=ff_dl, dlc=dlc, addressing_format=addressing_format)
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


@pytest.mark.integration
class TestCanFirstFrameHandlerIntegration:
    """Integrations tests for `CanFirstFrameHandler` class."""

    # create_valid_frame_data

    @pytest.mark.parametrize("kwargs, expected_raw_frame_data", [
        ({"addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
          "dlc": 8,
          "ff_dl": 0xFED,
          "payload": [0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC]}, [0x1F, 0xED, 0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC]),
        ({"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "dlc": 9,
          "ff_dl": 0x12345678,
          "payload": [0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5],
          "target_address": 0xC0}, [0x10, 0x00, 0x12, 0x34, 0x56, 0x78, 0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5]),
        ({"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "dlc": 0xF,
          "ff_dl": 62,
          "payload": tuple(range(120, 181)),
          "target_address": 0xC0}, [0xC0, 0x10, 0x3E] + list(range(120, 181))),
        ({"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
          "dlc": 0xA,
          "ff_dl": 0x1000,
          "payload": list(range(9)),
          "address_extension": 0x0B}, [0x0B, 0x10, 0x00, 0x00, 0x00, 0x10, 0x00] + list(range(9))),
        ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "dlc": 8,
          "ff_dl": 0xFFF,
          "payload": [0x9A, 0x8B, 0x7C, 0x6D, 0x5E],
          "target_address": 0x9E,
          "address_extension": 0x61}, [0x61, 0x1F, 0xFF, 0x9A, 0x8B, 0x7C, 0x6D, 0x5E]),
    ])
    def test_create_valid_frame_data__valid(self, kwargs, expected_raw_frame_data):
        assert CanFirstFrameHandler.create_valid_frame_data(**kwargs) == expected_raw_frame_data

    @pytest.mark.parametrize("kwargs", [
        {"addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
         "dlc": 7,
         "ff_dl": 0xFED,
         "payload": [0x12, 0x34, 0x56, 0x78, 0x9A]},
        {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         "dlc": 9,
         "ff_dl": 0x12345678,
         "payload": [0xF0, 0xE1, 0xD2, 0xC3, 0xB4],
         "target_address": 0xC0},
        {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
         "dlc": 0xF,
         "ff_dl": 61,
         "payload": tuple(range(120, 181)),
         "target_address": 0xC0},
        {"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         "dlc": 0xA,
         "ff_dl": 0x100000000,
         "payload": list(range(9)),
         "address_extension": 0x0B},
        {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         "dlc": 8,
         "ff_dl": 0x6,
         "payload": [0x9A, 0x8B, 0x7C, 0x6D, 0x5E],
         "target_address": 0x9E,
         "address_extension": 0x61}
    ])
    def test_create_valid_frame_data__invalid(self, kwargs):
        with pytest.raises(ValueError):
            CanFirstFrameHandler.create_valid_frame_data(**kwargs)

    # create_any_frame_data

    @pytest.mark.parametrize("kwargs, expected_raw_frame_data", [
        ({"addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
          "dlc": 7,
          "ff_dl": 0xFED,
          "long_ff_dl_format": False,
          "payload": [0x12, 0x34, 0x56, 0x78, 0x9A]}, [0x1F, 0xED, 0x12, 0x34, 0x56, 0x78, 0x9A]),
        ({"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "dlc": 8,
          "ff_dl": 0xFED,
          "long_ff_dl_format": True,
          "payload": [0x78, 0x9A],
          "target_address": 0xC0}, [0x10, 0x00, 0x00, 0x00, 0x0F, 0xED, 0x78, 0x9A]),
        ({"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "dlc": 0xF,
          "ff_dl": 61,
          "long_ff_dl_format": False,
          "payload": tuple(range(120, 181)),
          "target_address": 0xC0}, [0xC0, 0x10, 0x3D] + list(range(120, 181))),
        ({"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
          "dlc": 0xA,
          "ff_dl": 0,
          "long_ff_dl_format": True,
          "payload": list(range(9)),
          "address_extension": 0x0B}, [0x0B, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00] + list(range(9))),
        ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "dlc": 8,
          "ff_dl": 0x6,
          "long_ff_dl_format": False,
          "payload": [0x9A, 0x8B, 0x7C, 0x6D, 0x5E],
          "target_address": 0x9E,
          "address_extension": 0x61}, [0x61, 0x10, 0x06, 0x9A, 0x8B, 0x7C, 0x6D, 0x5E])
    ])
    def test_create_any_frame_data__valid(self, kwargs, expected_raw_frame_data):
        assert CanFirstFrameHandler.create_any_frame_data(**kwargs) == expected_raw_frame_data

    @pytest.mark.parametrize("kwargs", [
        {"addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
         "dlc": 7,
         "ff_dl": 0x1000,
         "long_ff_dl_format": False,
         "payload": [0x12, 0x34, 0x56, 0x78, 0x9A]},
        {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         "dlc": 9,
         "ff_dl": 0x12345678,
         "long_ff_dl_format": True,
         "payload": [0xF0, 0xE1, 0xD2, 0xC3, 0xB4],
         "target_address": 0xC0},
        {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
         "dlc": 0xF,
         "ff_dl": 610,
         "long_ff_dl_format": False,
         "payload": tuple(range(120, 182)),
         "target_address": 0xC0},
        {"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         "dlc": 0xA,
         "ff_dl": 0x100000000,
         "long_ff_dl_format": True,
         "payload": list(range(9)),
         "address_extension": 0x0B},
        {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         "dlc": 8,
         "ff_dl": -1,
         "long_ff_dl_format": False,
         "payload": [0x9A, 0x8B, 0x7C, 0x6D, 0x5E],
         "target_address": 0x9E,
         "address_extension": 0x61}
    ])
    def test_create_any_frame_data__invalid(self, kwargs):
        with pytest.raises(ValueError):
            CanFirstFrameHandler.create_any_frame_data(**kwargs)

    # decode_ff_dl

    @pytest.mark.parametrize("addressing_format, raw_frame_data, expected_ff_dl", [
        (CanAddressingFormat.NORMAL_11BIT_ADDRESSING, (0x10, 0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE), 0x12),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, [0x1F, 0xED] + list(range(62)), 0xFED),
        (CanAddressingFormat.EXTENDED_ADDRESSING, [0x10, 0x10, 0x00, 0xF0, 0xD1, 0xE2, 0xC3] + list(range(50, 92)), 0xF0D1E2C3),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, [0xC4, 0x10, 0x00, 0xF0, 0xD1, 0xE2, 0xC3, 0xD4], 0xF0D1E2C3),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, [0x83, 0x1F, 0xFF] + list(range(100, 121)), 0xFFF),
    ])
    def test_decode_ff_dl(self, addressing_format, raw_frame_data, expected_ff_dl):
        assert CanFirstFrameHandler.decode_ff_dl(addressing_format=addressing_format,
                                                 raw_frame_data=raw_frame_data) == expected_ff_dl

    # validate_frame_data

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        (CanAddressingFormat.NORMAL_11BIT_ADDRESSING, (0x10, 0x08, 0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54)),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, [0x10, 0x00, 0x00, 0x00, 0x10, 0x00] + list(range(58))),
        (CanAddressingFormat.EXTENDED_ADDRESSING, [0x10, 0x1F, 0xFF] + list(range(100, 121))),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, (0x0F, 0x10, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF)),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, [0x0F, 0x10, 0x3E] + list(range(50, 111))),
    ])
    def test_validate_frame_data__valid(self, addressing_format, raw_frame_data):
        assert CanFirstFrameHandler.validate_frame_data(addressing_format=addressing_format,
                                                        raw_frame_data=raw_frame_data) is None

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        (CanAddressingFormat.NORMAL_11BIT_ADDRESSING, (0x10, 0x07, 0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54)),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, [0x10, 0x00, 0x00, 0x00, 0x0F, 0xFF] + list(range(58))),
        (CanAddressingFormat.EXTENDED_ADDRESSING, [0x10, 0x10, 0x15] + list(range(100, 121))),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, (0x0F, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, [0x0F, 0x10, 0x3D] + list(range(50, 111))),
    ])
    def test_validate_frame_data__invalid(self, addressing_format, raw_frame_data):
        with pytest.raises(ValueError):
            CanFirstFrameHandler.validate_frame_data(addressing_format=addressing_format,
                                                     raw_frame_data=raw_frame_data)



















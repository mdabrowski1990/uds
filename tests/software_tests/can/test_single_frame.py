import pytest
from mock import patch

from uds.can.single_frame import CanSingleFrameHandler, \
    CanPacketType, CanAddressingFormat, InconsistentArgumentsError, CanDlcHandler, DEFAULT_FILLER_BYTE


class TestCanSingleFrameHandler:
    """Tests for `CanSingleFrameHandler` class."""

    SCRIPT_LOCATION = "uds.can.single_frame"

    def setup(self):
        self._patcher_validate_nibble = patch(f"{self.SCRIPT_LOCATION}.validate_nibble")
        self.mock_validate_nibble = self._patcher_validate_nibble.start()
        self._patcher_validate_raw_byte = patch(f"{self.SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
        self._patcher_validate_raw_bytes = patch(f"{self.SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
        self._patcher_encode_dlc = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler.encode_dlc")
        self.mock_encode_dlc = self._patcher_encode_dlc.start()
        self._patcher_decode_dlc = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler.decode_dlc")
        self.mock_decode_dlc = self._patcher_decode_dlc.start()
        self._patcher_get_min_dlc = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler.get_min_dlc")
        self.mock_get_min_dlc = self._patcher_get_min_dlc.start()
        self._patcher_validate_dlc = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler.validate_dlc")
        self.mock_validate_dlc = self._patcher_validate_dlc.start()
        self._patcher_encode_ai_data_bytes = \
            patch(f"{self.SCRIPT_LOCATION}.CanAddressingInformationHandler.encode_ai_data_bytes")
        self.mock_encode_ai_data_bytes = self._patcher_encode_ai_data_bytes.start()
        self._patcher_get_ai_data_bytes_number = \
            patch(f"{self.SCRIPT_LOCATION}.CanAddressingInformationHandler.get_ai_data_bytes_number")
        self.mock_get_ai_data_bytes_number = self._patcher_get_ai_data_bytes_number.start()

    def teardown(self):
        self._patcher_validate_nibble.stop()
        self._patcher_validate_raw_byte.stop()
        self._patcher_validate_raw_bytes.stop()
        self._patcher_encode_dlc.stop()
        self._patcher_decode_dlc.stop()
        self._patcher_get_min_dlc.stop()
        self._patcher_validate_dlc.stop()
        self._patcher_encode_ai_data_bytes.stop()
        self._patcher_get_ai_data_bytes_number.stop()

    # create_can_frame_data

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, filler_byte", [
        ("some DLC", 0x66),
        (8, 0x99),
    ])
    @pytest.mark.parametrize("payload, data_bytes_number, ai_bytes, sf_dl_bytes", [
        ([0x54], 2, [], [0xFA]),
        ([0x3E], 8, [], [0x0C]),
        (range(50, 110), 64, [0x98], [0x12, 0x34]),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.encode_sf_dl")
    def test_generate_can_frame_data__with_dlc(self, mock_encode_sf_dl,
                                               addressing_format, target_address, address_extension,
                                               payload, dlc, filler_byte, data_bytes_number, ai_bytes, sf_dl_bytes):
        self.mock_encode_ai_data_bytes.return_value = ai_bytes
        self.mock_decode_dlc.return_value = data_bytes_number
        mock_encode_sf_dl.return_value = sf_dl_bytes
        sf_frame_data = CanSingleFrameHandler.create_can_frame_data(addressing_format=addressing_format,
                                                                    payload=payload,
                                                                    dlc=dlc,
                                                                    filler_byte=filler_byte,
                                                                    target_address=target_address,
                                                                    address_extension=address_extension)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=True)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        mock_encode_sf_dl.assert_called_once_with(sf_dl=len(payload),
                                                  dlc=dlc,
                                                  addressing_format=addressing_format)
        assert isinstance(sf_frame_data, list)
        assert len(sf_frame_data) == data_bytes_number

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, filler_byte", [
        ("some DLC", 0x66),
        (8, 0x99),
    ])
    @pytest.mark.parametrize("payload, data_bytes_number, ai_bytes, sf_dl_bytes", [
        ([0x54], 2, [], [0xFA]),
        ([0x3E], 8, [], [0x0C]),
        (range(50, 110), 64, [0x98], [0x12, 0x34]),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.get_dlc")
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.encode_sf_dl")
    def test_generate_can_frame_data__without_dlc(self, mock_encode_sf_dl, mock_get_dlc,
                                                  addressing_format, target_address, address_extension,
                                                  payload, dlc, filler_byte, data_bytes_number, ai_bytes, sf_dl_bytes):
        self.mock_encode_ai_data_bytes.return_value = ai_bytes
        self.mock_decode_dlc.return_value = data_bytes_number
        mock_encode_sf_dl.return_value = sf_dl_bytes
        mock_get_dlc.return_value = dlc
        sf_frame_data = CanSingleFrameHandler.create_can_frame_data(addressing_format=addressing_format,
                                                                    payload=payload,
                                                                    dlc=None,
                                                                    filler_byte=filler_byte,
                                                                    target_address=target_address,
                                                                    address_extension=address_extension)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=True)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        mock_get_dlc.assert_called_once_with(addressing_format=addressing_format,
                                             payload_length=len(payload))
        self.mock_decode_dlc.assert_called_once_with(dlc)
        mock_encode_sf_dl.assert_called_once_with(sf_dl=len(payload),
                                                  dlc=dlc,
                                                  addressing_format=addressing_format)
        assert isinstance(sf_frame_data, list)
        assert len(sf_frame_data) == data_bytes_number

    # is_single_frame

    @pytest.mark.parametrize("addressing_format, raw_frame_data, sf_dl_data_bytes", [
        ("some addressing", "some raw frame", [0x00]),
        ("some other addressing", "some other raw frame", [0x06]),
        ("Mixed", range(20), [0x00, 0x12]),
        ("Extended", [0x10, 0x20, 0x30], [0x0F, 0xED]),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.extract_sf_dl_data_bytes")
    def test_is_single_frame__true(self, mock_extract_sf_dl_data_bytes,
                                   addressing_format, raw_frame_data, sf_dl_data_bytes):
        mock_extract_sf_dl_data_bytes.return_value = sf_dl_data_bytes
        assert CanSingleFrameHandler.is_single_frame(addressing_format=addressing_format,
                                                     raw_frame_data=raw_frame_data) is True
        mock_extract_sf_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)

    @pytest.mark.parametrize("addressing_format, raw_frame_data, sf_dl_data_bytes", [
        ("some addressing", "some raw frame", [0x10]),
        ("some other addressing", "some other raw frame", [0x26]),
        ("Mixed", range(20), [0xF0, 0x12]),
        ("Extended", [0x10, 0x20, 0x30], [0x8F, 0xED]),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.extract_sf_dl_data_bytes")
    def test_is_single_frame__false(self, mock_extract_sf_dl_data_bytes,
                                    addressing_format, raw_frame_data, sf_dl_data_bytes):
        mock_extract_sf_dl_data_bytes.return_value = sf_dl_data_bytes
        assert CanSingleFrameHandler.is_single_frame(addressing_format=addressing_format,
                                                     raw_frame_data=raw_frame_data) is False
        mock_extract_sf_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)

    # get_dlc

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
    @pytest.mark.parametrize("ai_data_bytes, payload_length", [
        (0, 0),
        (1, 7),
        (0, 15),
        (0, 62),
    ])
    @pytest.mark.parametrize("decoded_dlc", [CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL,
                                             CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL - 2])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__validate_payload_length")
    def test_get_can_frame_dlc_single_frame__short_dlc(self, mock_validate_payload_length,
                                                       addressing_format, payload_length, ai_data_bytes,
                                                       decoded_dlc):
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes
        self.mock_get_min_dlc.return_value = decoded_dlc
        assert CanSingleFrameHandler.get_dlc(addressing_format=addressing_format,
                                             payload_length=payload_length) == self.mock_get_min_dlc.return_value
        data_bytes_number = payload_length + CanSingleFrameHandler.SHORT_SF_DL_BYTES_USED + ai_data_bytes
        self.mock_get_min_dlc.assert_called_once_with(data_bytes_number)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        mock_validate_payload_length.assert_called_once_with(ai_data_bytes_number=ai_data_bytes,
                                                             payload_length=payload_length)

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
    @pytest.mark.parametrize("ai_data_bytes, payload_length", [
        (0, 0),
        (1, 7),
        (0, 15),
        (0, 62),
    ])
    @pytest.mark.parametrize("decoded_dlc", [CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL + 1,
                                             CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL + 5])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__validate_payload_length")
    def test_get_can_frame_dlc_single_frame__long_dlc(self, mock_validate_payload_length,
                                                      addressing_format, payload_length, ai_data_bytes,
                                                      decoded_dlc):
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes
        self.mock_get_min_dlc.return_value = decoded_dlc
        assert CanSingleFrameHandler.get_dlc(addressing_format=addressing_format,
                                             payload_length=payload_length) == self.mock_get_min_dlc.return_value
        data_bytes_number = payload_length + CanSingleFrameHandler.LONG_SF_DL_BYTES_USED + ai_data_bytes
        self.mock_get_min_dlc.assert_called_with(data_bytes_number)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        mock_validate_payload_length.assert_called_once_with(ai_data_bytes_number=ai_data_bytes,
                                                             payload_length=payload_length)

    # encode_sf_dl

    @pytest.mark.parametrize("sf_dl", [0, 8, 0xF])
    @pytest.mark.parametrize("dlc", [CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL,
                                     CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL - 1])
    @pytest.mark.parametrize("addressing_format", [None, "some addressing format"])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.create_sf_dl_data_bytes")
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.validate_sf_dl")
    def test_encode_sf_dl__short(self, mock_validate_sf_dl, mock_generate_sf_dl_data_bytes,
                                 sf_dl, dlc, addressing_format):
        assert CanSingleFrameHandler.encode_sf_dl(sf_dl=sf_dl,
                                                  addressing_format=addressing_format,
                                                  dlc=dlc) == mock_generate_sf_dl_data_bytes.return_value
        mock_validate_sf_dl.assert_called_once_with(sf_dl=sf_dl,
                                                    dlc=dlc,
                                                    addressing_format=addressing_format)
        mock_generate_sf_dl_data_bytes.assert_called_once_with(sf_dl_short=sf_dl)

    @pytest.mark.parametrize("sf_dl", [0, 8, 0xF])
    @pytest.mark.parametrize("dlc", [CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL + 1,
                                     CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL + 2])
    @pytest.mark.parametrize("addressing_format", [None, "some addressing format"])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.create_sf_dl_data_bytes")
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.validate_sf_dl")
    def test_encode_sf_dl__long(self, mock_validate_sf_dl, mock_generate_sf_dl_data_bytes,
                                sf_dl, dlc, addressing_format):
        assert CanSingleFrameHandler.encode_sf_dl(sf_dl=sf_dl,
                                                  addressing_format=addressing_format,
                                                  dlc=dlc) == mock_generate_sf_dl_data_bytes.return_value
        mock_validate_sf_dl.assert_called_once_with(sf_dl=sf_dl,
                                                    dlc=dlc,
                                                    addressing_format=addressing_format)
        mock_generate_sf_dl_data_bytes.assert_called_once_with(sf_dl_long=sf_dl)

    # create_sf_dl_data_bytes

    @pytest.mark.parametrize("sf_dl_short", [0, 7, 0xF])
    def test_create_sf_dl_data_bytes__short(self, sf_dl_short):
        assert CanSingleFrameHandler.create_sf_dl_data_bytes(sf_dl_short=sf_dl_short) \
               == [(CanPacketType.SINGLE_FRAME.value << 4) + sf_dl_short]
        self.mock_validate_nibble.assert_called_once_with(sf_dl_short)
        self.mock_validate_raw_byte.assert_not_called()

    @pytest.mark.parametrize("sf_dl_short", [0, 7, 0xF])
    @pytest.mark.parametrize("sf_dl_long", [0, 7, 0xF])
    def test_create_sf_dl_data_bytes__long(self, sf_dl_short, sf_dl_long):
        assert CanSingleFrameHandler.create_sf_dl_data_bytes(sf_dl_short=sf_dl_short, sf_dl_long=sf_dl_long) \
               == [(CanPacketType.SINGLE_FRAME.value << 4) + sf_dl_short, sf_dl_long]
        self.mock_validate_nibble.assert_called_once_with(sf_dl_short)
        self.mock_validate_raw_byte.assert_called_once_with(sf_dl_long)

    # decode_sf_dl

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("raw_frame_data", [list(range(64)), (0x12, 0x34, 0x56)])
    @pytest.mark.parametrize("expected_sf_dl", [1, 4, 7])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.extract_sf_dl_data_bytes")
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.validate_frame_data")
    def test_decode_sf_dl__valid_short(self, mock_validate_frame_data, mock_extract_sf_dl_data_bytes,
                                       addressing_format, raw_frame_data, expected_sf_dl):
        mock_extract_sf_dl_data_bytes.return_value = [(CanPacketType.SINGLE_FRAME.value << 4) ^ expected_sf_dl]
        assert CanSingleFrameHandler.decode_sf_dl(addressing_format=addressing_format,
                                                  raw_frame_data=raw_frame_data) == expected_sf_dl
        mock_validate_frame_data.assert_called_once_with(addressing_format=addressing_format,
                                                         raw_frame_data=raw_frame_data)
        mock_extract_sf_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("raw_frame_data", [list(range(64)), (0x12, 0x34, 0x56)])
    @pytest.mark.parametrize("expected_sf_dl", [8, 0x15, 0x3E])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.extract_sf_dl_data_bytes")
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.validate_frame_data")
    def test_decode_sf_dl__valid_long(self, mock_validate_frame_data, mock_extract_sf_dl_data_bytes,
                                      addressing_format, raw_frame_data, expected_sf_dl):
        mock_extract_sf_dl_data_bytes.return_value = [(CanPacketType.SINGLE_FRAME.value << 4), expected_sf_dl]
        assert CanSingleFrameHandler.decode_sf_dl(addressing_format=addressing_format,
                                                  raw_frame_data=raw_frame_data) == expected_sf_dl
        mock_validate_frame_data.assert_called_once_with(addressing_format=addressing_format,
                                                         raw_frame_data=raw_frame_data)
        mock_extract_sf_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("raw_frame_data", [list(range(64)), (0x12, 0x34, 0x56)])
    @pytest.mark.parametrize("sf_dl_data_bytes", [[], [0x00, 0x00, 0x01]])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.extract_sf_dl_data_bytes")
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.validate_frame_data")
    def test_decode_sf_dl__not_implemented(self, mock_validate_frame_data, mock_extract_sf_dl_data_bytes,
                                           addressing_format, raw_frame_data, sf_dl_data_bytes):
        mock_extract_sf_dl_data_bytes.return_value = sf_dl_data_bytes
        with pytest.raises(NotImplementedError):
            CanSingleFrameHandler.decode_sf_dl(addressing_format=addressing_format,
                                               raw_frame_data=raw_frame_data)
        mock_validate_frame_data.assert_called_once_with(addressing_format=addressing_format,
                                                         raw_frame_data=raw_frame_data)
        mock_extract_sf_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)

    # extract_sf_dl_data_bytes

    @pytest.mark.parametrize("addressing_format, ai_data_bytes", [
        ("some addressing format", 0),
        ("another format", 1),
    ])
    @pytest.mark.parametrize("raw_frame_data", [range(10), range(10, 16)])
    @pytest.mark.parametrize("sf_dl_bytes_number", [1, 2])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.get_sf_dl_bytes_number")
    def test_extract_sf_dl_data_bytes__short(self, mock_get_sf_dl_bytes_number,
                                             addressing_format, raw_frame_data, sf_dl_bytes_number, ai_data_bytes):
        mock_get_sf_dl_bytes_number.return_value = sf_dl_bytes_number
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes
        sf_dl_bytes = CanSingleFrameHandler.extract_sf_dl_data_bytes(addressing_format=addressing_format,
                                                                     raw_frame_data=raw_frame_data)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        self.mock_encode_dlc.assert_called_once_with(len(raw_frame_data))
        mock_get_sf_dl_bytes_number.assert_called_once_with(self.mock_encode_dlc.return_value)
        assert isinstance(sf_dl_bytes, list)
        assert len(sf_dl_bytes) == sf_dl_bytes_number
        assert sf_dl_bytes == list(raw_frame_data)[ai_data_bytes:][:sf_dl_bytes_number]

    # get_sf_dl_bytes_number

    @pytest.mark.parametrize("dlc, expected_sf_dl_bytes_number", [
        (CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL - 100, CanSingleFrameHandler.SHORT_SF_DL_BYTES_USED),
        (CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL, CanSingleFrameHandler.SHORT_SF_DL_BYTES_USED),
        (CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL + 1, CanSingleFrameHandler.LONG_SF_DL_BYTES_USED),
        (CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL + 100, CanSingleFrameHandler.LONG_SF_DL_BYTES_USED),
    ])
    def test_get_sf_dl_bytes_number__short(self, dlc, expected_sf_dl_bytes_number):
        assert CanSingleFrameHandler.get_sf_dl_bytes_number(dlc) == expected_sf_dl_bytes_number
        self.mock_validate_dlc.assert_called_once_with(dlc)

    # validate_frame_data

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
    @pytest.mark.parametrize("raw_frame_data", ["some raw bbytes", range(6)])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.decode_sf_dl")
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.validate_sf_dl")
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.is_single_frame")
    def test_validate_frame_data__valid(self, mock_is_single_frame, mock_validate_sf_dl, mock_decode_sf_dl,
                                        addressing_format, raw_frame_data):
        mock_is_single_frame.return_value = True
        CanSingleFrameHandler.validate_frame_data(addressing_format=addressing_format,
                                                  raw_frame_data=raw_frame_data)
        mock_is_single_frame.assert_called_once_with(addressing_format=addressing_format,
                                                     raw_frame_data=raw_frame_data)
        self.mock_encode_dlc.assert_called_once_with(len(raw_frame_data))
        mock_decode_sf_dl.assert_called_once_with(addressing_format=addressing_format,
                                                  raw_frame_data=raw_frame_data)
        mock_validate_sf_dl.assert_called_once_with(sf_dl=mock_decode_sf_dl.return_value,
                                                    dlc=self.mock_encode_dlc.return_value,
                                                    addressing_format=addressing_format)

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
    @pytest.mark.parametrize("raw_frame_data", ["some raw bbytes", range(6)])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.is_single_frame")
    def test_validate_frame_data__invalid(self, mock_is_single_frame, addressing_format, raw_frame_data):
        mock_is_single_frame.return_value = False
        with pytest.raises(ValueError):
            CanSingleFrameHandler.validate_frame_data(addressing_format=addressing_format,
                                                      raw_frame_data=raw_frame_data)

    # validate_sf_dl

    @pytest.mark.parametrize("sf_dl", ["some SF_DL", None, 5.])
    @pytest.mark.parametrize("dlc, addressing_format", [
        ("dlc", "some addressing"),
        (8, None),
    ])
    def test_validate_sf_dl__type_error(self, sf_dl, dlc, addressing_format):
        with pytest.raises(TypeError):
            CanSingleFrameHandler.validate_sf_dl(sf_dl=sf_dl, dlc=dlc, addressing_format=addressing_format)

    @pytest.mark.parametrize("sf_dl", [0, -1, -6])
    @pytest.mark.parametrize("dlc, addressing_format", [
        ("dlc", "some addressing"),
        (8, None),
    ])
    def test_validate_sf_dl__value_error(self, sf_dl, dlc, addressing_format):
        with pytest.raises(ValueError):
            CanSingleFrameHandler.validate_sf_dl(sf_dl=sf_dl, dlc=dlc, addressing_format=addressing_format)

    @pytest.mark.parametrize("sf_dl, data_bytes_number, sf_dl_bytes_number", [
        (8, 8, 1),
        (6, 5, 1),
        (24, 16, 2),
        (63, 64, 2),
    ])
    @pytest.mark.parametrize("dlc", [8, 0xF])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.get_sf_dl_bytes_number")
    def test_validate_sf_dl__inconsistent_without_addressing(self, mock_get_sf_dl_bytes_number,
                                                             sf_dl, dlc, data_bytes_number, sf_dl_bytes_number):
        self.mock_decode_dlc.return_value = data_bytes_number
        mock_get_sf_dl_bytes_number.return_value = sf_dl_bytes_number
        with pytest.raises(InconsistentArgumentsError):
            CanSingleFrameHandler.validate_sf_dl(sf_dl=sf_dl, dlc=dlc)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        mock_get_sf_dl_bytes_number.assert_called_once_with(dlc)

    @pytest.mark.parametrize("sf_dl, data_bytes_number, ai_data_bytes_number, sf_dl_bytes_number", [
        (7, 8, 1, 1),
        (5, 5, 0, 1),
        (24, 16, 0, 2),
        (62, 64, 1, 2),
    ])
    @pytest.mark.parametrize("dlc, addressing_format", [
        ("dlc", "some addressing"),
        (8, "something else"),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.get_sf_dl_bytes_number")
    def test_validate_sf_dl__inconsistent_with_addressing(self, mock_get_sf_dl_bytes_number,
                                                          sf_dl, dlc, addressing_format,
                                                          data_bytes_number, sf_dl_bytes_number, ai_data_bytes_number):
        self.mock_decode_dlc.return_value = data_bytes_number
        mock_get_sf_dl_bytes_number.return_value = sf_dl_bytes_number
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes_number
        with pytest.raises(InconsistentArgumentsError):
            CanSingleFrameHandler.validate_sf_dl(sf_dl=sf_dl, dlc=dlc, addressing_format=addressing_format)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        mock_get_sf_dl_bytes_number.assert_called_once_with(dlc)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    @pytest.mark.parametrize("sf_dl, data_bytes_number, sf_dl_bytes_number", [
        (7, 8, 1),
        (2, 5, 1),
        (10, 16, 2),
        (62, 64, 2),
    ])
    @pytest.mark.parametrize("dlc", [8, 0xF])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.get_sf_dl_bytes_number")
    def test_validate_sf_dl__valid_without_addressing(self, mock_get_sf_dl_bytes_number,
                                                      sf_dl, dlc, data_bytes_number, sf_dl_bytes_number):
        self.mock_decode_dlc.return_value = data_bytes_number
        mock_get_sf_dl_bytes_number.return_value = sf_dl_bytes_number
        CanSingleFrameHandler.validate_sf_dl(sf_dl=sf_dl, dlc=dlc)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        mock_get_sf_dl_bytes_number.assert_called_once_with(dlc)

    @pytest.mark.parametrize("sf_dl, data_bytes_number, ai_data_bytes_number, sf_dl_bytes_number", [
        (6, 8, 1, 1),
        (2, 5, 0, 1),
        (10, 16, 1, 2),
        (61, 64, 1, 2),
    ])
    @pytest.mark.parametrize("dlc, addressing_format", [
        ("dlc", "some addressing"),
        (8, "something else"),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.get_sf_dl_bytes_number")
    def test_validate_sf_dl__valid_with_addressing(self, mock_get_sf_dl_bytes_number,
                                                   sf_dl, dlc, addressing_format,
                                                   data_bytes_number, sf_dl_bytes_number, ai_data_bytes_number):
        self.mock_decode_dlc.return_value = data_bytes_number
        mock_get_sf_dl_bytes_number.return_value = sf_dl_bytes_number
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes_number
        CanSingleFrameHandler.validate_sf_dl(sf_dl=sf_dl, dlc=dlc, addressing_format=addressing_format)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        mock_get_sf_dl_bytes_number.assert_called_once_with(dlc)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    # validate_sf_dl_data_bytes

    @pytest.mark.parametrize("sf_dl_bytes, sf_dl", [
        ([0x01], 1),
        ([0x06], 6),
        ([0x00, 0x12], 0x12),
        ([0x00, 0x3A], 0x3A),
    ])
    @pytest.mark.parametrize("dlc", ["some DLC", 8])
    @pytest.mark.parametrize("addressing_format", [None, "some addressing format"])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.get_sf_dl_bytes_number")
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.validate_sf_dl")
    def test_validate_sf_dl_data_bytes__valid(self, mock_validate_sf_dl, mock_get_sf_dl_bytes_number,
                                              sf_dl_bytes, sf_dl, dlc, addressing_format):
        mock_get_sf_dl_bytes_number.return_value = len(sf_dl_bytes)
        CanSingleFrameHandler.validate_sf_dl_data_bytes(sf_dl_bytes=sf_dl_bytes,
                                                        dlc=dlc,
                                                        addressing_format=addressing_format)
        self.mock_validate_raw_bytes.assert_called_once_with(sf_dl_bytes)
        mock_get_sf_dl_bytes_number.assert_called_once_with(dlc)
        mock_validate_sf_dl.assert_called_once_with(sf_dl=sf_dl, dlc=dlc, addressing_format=addressing_format)

    @pytest.mark.parametrize("sf_dl_bytes, expected_sf_dl_bytes_number", [
        ([0x00, 0x12], 1),
        ([0x00, 0x06], 3),
        ([0x0F], 2),
    ])
    @pytest.mark.parametrize("dlc", ["some DLC", 8])
    @pytest.mark.parametrize("addressing_format", [None, "some addressing format"])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.get_sf_dl_bytes_number")
    def test_validate_sf_dl_data_bytes__invalid_length(self, mock_get_sf_dl_bytes_number, expected_sf_dl_bytes_number,
                                                       sf_dl_bytes, dlc, addressing_format):
        mock_get_sf_dl_bytes_number.return_value = expected_sf_dl_bytes_number
        with pytest.raises(InconsistentArgumentsError):
            CanSingleFrameHandler.validate_sf_dl_data_bytes(sf_dl_bytes=sf_dl_bytes,
                                                            dlc=dlc,
                                                            addressing_format=addressing_format)
        self.mock_validate_raw_bytes.assert_called_once_with(sf_dl_bytes)
        mock_get_sf_dl_bytes_number.assert_called_once_with(dlc)

    @pytest.mark.parametrize("dlc, sf_dl_bytes", [
        (9, [0x01, 0x3E]),
        (0x10, [0x0A, 0x12]),
        (0xF, [0x0F, 0x02]),
    ])
    @pytest.mark.parametrize("addressing_format", [None, "some addressing format"])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.get_sf_dl_bytes_number")
    def test_validate_sf_dl_data_bytes__invalid_byte_zero(self, mock_get_sf_dl_bytes_number,
                                                          sf_dl_bytes, dlc, addressing_format):
        mock_get_sf_dl_bytes_number.return_value = len(sf_dl_bytes)
        with pytest.raises(ValueError):
            CanSingleFrameHandler.validate_sf_dl_data_bytes(sf_dl_bytes=sf_dl_bytes,
                                                            dlc=dlc,
                                                            addressing_format=addressing_format)
        self.mock_validate_raw_bytes.assert_called_once_with(sf_dl_bytes)
        mock_get_sf_dl_bytes_number.assert_called_once_with(dlc)

    @pytest.mark.parametrize("sf_dl_bytes", [[0x00, 0x00, 0xFF], range(4)])
    @pytest.mark.parametrize("dlc", ["some DLC", 8])
    @pytest.mark.parametrize("addressing_format", [None, "some addressing format"])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.get_sf_dl_bytes_number")
    def test_validate_sf_dl_data_bytes__not_implemented(self, mock_get_sf_dl_bytes_number,
                                                        sf_dl_bytes, dlc, addressing_format):
        mock_get_sf_dl_bytes_number.return_value = len(sf_dl_bytes)
        with pytest.raises(NotImplementedError):
            CanSingleFrameHandler.validate_sf_dl_data_bytes(sf_dl_bytes=sf_dl_bytes,
                                                            dlc=dlc,
                                                            addressing_format=addressing_format)
        self.mock_validate_raw_bytes.assert_called_once_with(sf_dl_bytes)
        mock_get_sf_dl_bytes_number.assert_called_once_with(dlc)


@pytest.mark.integration
class TestCanSingleFrameHandlerIntegration:
    """Integration tests for `CanSingleFrameHandler` class."""

    @pytest.mark.parametrize("kwargs, expected_raw_frame_data", [
        ({"addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
          "payload": [0x3E]},
         [0x01, 0x3E]),
        ({"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "payload": [0x3E],
          "dlc": 8,
          "target_address": 0xFF},
         [0x01, 0x3E] + ([DEFAULT_FILLER_BYTE] * 6)),
        ({"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "payload": list(range(54)),
          "filler_byte": 0x66,
          "target_address": 0xF2},
         [0xF2, 0x00, 0x36] + list(range(54)) + ([0x66] * 7)),
        ({"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
          "payload": [0x9A, 0xB8, 0xC4, 0x67, 0x10, 0x00],
          "dlc": 8,
          "filler_byte": 0x66,
          "address_extension": 0x12},
         [0x12, 0x06, 0x9A, 0xB8, 0xC4, 0x67, 0x10, 0x00]),
        ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "payload": [0x9A, 0xB8, 0xC4, 0x67, 0x10, 0x00, 0x01],
          "filler_byte": 0x99,
          "target_address": 0xF2,
          "address_extension": 0x12},
         [0x12, 0x00, 0x07, 0x9A, 0xB8, 0xC4, 0x67, 0x10, 0x00, 0x01, 0x99, 0x99]),
    ])
    def test_generate_can_frame_data(self, kwargs, expected_raw_frame_data):
        assert CanSingleFrameHandler.create_can_frame_data(**kwargs) == expected_raw_frame_data


# @pytest.mark.integration
# class _TestCanSingleFrameDataLengthHandlerIntegration:
#     """Integration tests for `CanSingleFrameDataLengthHandler` class."""
#
#     # encode_sf_dl
#
#     @pytest.mark.parametrize("sf_dl, dlc, expected_sf_dl_data_bytes", [
#         # short
#         (0x0, 1, [0x00]),
#         (0x8, 2, [0x08]),
#         (0x9, 6, [0x09]),
#         (0xF, 8, [0x0F]),
#         # long
#         (0x0, 0x9, [0x00, 0x00]),
#         (0x8, 0xA, [0x00, 0x08]),
#         (0x12, 0xD, [0x00, 0x12]),
#         (0x3E, 0xF, [0x00, 0x3E]),
#         (0xFF, 0xF, [0x00, 0xFF]),
#     ])
#     def test_encode_sf_dl(self, sf_dl, dlc, expected_sf_dl_data_bytes):
#         assert _CanSingleFrameDataLengthHandler.encode_sf_dl(sf_dl=sf_dl, dlc=dlc, valid_sf_dl=False) == expected_sf_dl_data_bytes
#
#     # decode_sf_dl
#
#     @pytest.mark.parametrize("addressing_format, raw_frame_data, expected_sf_dl", [
#         (CanAddressingFormat.NORMAL_11BIT_ADDRESSING, (0x01, 0x23), 1),
#         (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, [0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF], 1),
#         (CanAddressingFormat.EXTENDED_ADDRESSING, [0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B], 5),
#         (CanAddressingFormat.MIXED_11BIT_ADDRESSING, [0x0A, 0x00, 0x3D] + list(range(100, 161)), 0x3D),
#         (CanAddressingFormat.MIXED_29BIT_ADDRESSING, [0xF0, 0x00, 0x0B] + list(range(50, 95)), 0xB),
#     ])
#     def test_decode_sf_dl(self, addressing_format, raw_frame_data, expected_sf_dl):
#         assert _CanSingleFrameDataLengthHandler.decode_sf_dl(addressing_format=addressing_format,
#                                                              raw_frame_data=raw_frame_data) == expected_sf_dl

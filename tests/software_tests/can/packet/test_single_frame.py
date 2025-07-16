from unittest.mock import MagicMock

import pytest
from mock import Mock, call, patch

from uds.can.packet.single_frame import (
    DEFAULT_FILLER_BYTE,
    LONG_SF_DL_BYTES_USED,
    MAX_DLC_VALUE_SHORT_SF_DL,
    SHORT_SF_DL_BYTES_USED,
    SINGLE_FRAME_N_PCI,
    CanAddressingFormat,
    CanDlcHandler,
    InconsistentArgumentsError,
    encode_single_frame_data,
    encode_sf_dl,
    extract_sf_dl,
    extract_sf_dl_data_bytes,
    extract_single_frame_payload,
    generate_sf_dl_bytes,
    get_sf_dl_bytes_number,
    get_single_frame_max_payload_size,
    get_single_frame_min_dlc,
    is_single_frame,
    validate_sf_dl,
generate_single_frame_data
)

SCRIPT_LOCATION = "uds.can.packet.single_frame"


class TestFunctions:
    """Unit tests for module functions."""

    def setup_method(self):
        self._patcher_validate_nibble = patch(f"{SCRIPT_LOCATION}.validate_nibble")
        self.mock_validate_nibble = self._patcher_validate_nibble.start()
        self._patcher_validate_raw_byte = patch(f"{SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
        self._patcher_validate_raw_bytes = patch(f"{SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
        self._patcher_can_dlc_handler = patch(f"{SCRIPT_LOCATION}.CanDlcHandler",
                                              Mock(MIN_BASE_UDS_DLC=CanDlcHandler.MIN_BASE_UDS_DLC))
        self.mock_can_dlc_handler = self._patcher_can_dlc_handler.start()
        self._patcher_get_ai_data_bytes_number = (
            patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.get_ai_data_bytes_number"))
        self.mock_get_ai_data_bytes_number = self._patcher_get_ai_data_bytes_number.start()
        self._patcher_encode_ai_data_bytes = \
            patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.encode_ai_data_bytes")
        self.mock_encode_ai_data_bytes = self._patcher_encode_ai_data_bytes.start()

    def teardown_method(self):
        # self._patcher_validate_nibble.stop()
        self._patcher_validate_raw_byte.stop()
        self._patcher_validate_raw_bytes.stop()
        self._patcher_can_dlc_handler.stop()
        self._patcher_get_ai_data_bytes_number.stop()
        self._patcher_encode_ai_data_bytes.stop()

    # is_single_frame

    @pytest.mark.parametrize("addressing_format, raw_frame_data, ai_data_bytes_number, expected_output", [
        (Mock(), [SINGLE_FRAME_N_PCI << 4, *range(7)], 0, True),
        (Mock(), [SINGLE_FRAME_N_PCI << 4 + 0xF, 0xFF, 0xFF], 0, True),
        (Mock(), [SINGLE_FRAME_N_PCI << 4 + 0xF, 0xFF, 0xFF], 1, False),
        (CanAddressingFormat.EXTENDED_ADDRESSING, [0xFF, SINGLE_FRAME_N_PCI << 4 + 0x5, 0xFF], 1, True),
    ])
    def test_is_single_frame(self, addressing_format, raw_frame_data, ai_data_bytes_number, expected_output):
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes_number
        assert is_single_frame(addressing_format=addressing_format, raw_frame_data=raw_frame_data) is expected_output
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    # extract_single_frame_payload

    @pytest.mark.parametrize("addressing_format, raw_frame_data, ai_data_bytes_number, sf_dl_bytes_number, sf_dl", [
        (Mock(), list(range(8)), 0, 1, 1),
        (CanAddressingFormat.NORMAL_ADDRESSING, b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87", 0, 1, 7),
        (CanAddressingFormat.EXTENDED_ADDRESSING, list(range(64)), 1, 2, 45),
        (CanAddressingFormat.EXTENDED_ADDRESSING, list(range(64))[::-1], 0, 1, 63),
    ])
    @patch(f"{SCRIPT_LOCATION}.get_sf_dl_bytes_number")
    @patch(f"{SCRIPT_LOCATION}.extract_sf_dl")
    def test_extract_single_frame_payload(self, mock_extract_sf_dl, mock_get_sf_dl_bytes_number,
                                          addressing_format, raw_frame_data, ai_data_bytes_number, sf_dl_bytes_number,
                                          sf_dl):
        mock_extract_sf_dl.return_value = sf_dl
        mock_get_sf_dl_bytes_number.return_value = sf_dl_bytes_number
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes_number
        assert (extract_single_frame_payload(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
                == bytearray(raw_frame_data)[ai_data_bytes_number + sf_dl_bytes_number:][:sf_dl])
        mock_extract_sf_dl.assert_called_once_with(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        mock_get_sf_dl_bytes_number.assert_called_once_with(self.mock_can_dlc_handler.encode_dlc.return_value)
        self.mock_can_dlc_handler.encode_dlc.assert_called_once_with(len(raw_frame_data))

    # create_single_frame_data

    @pytest.mark.parametrize("addressing_format, payload, ai_data_bytes, data_bytes_number, sf_dl_bytes", [
        (Mock(), [0x12, 0x34, 0x56], bytearray(), 8, bytearray([0x03])),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, range(43), bytearray([0xFF]), 64, bytearray([0xA5, 0x5A])),
    ])
    @patch(f"{SCRIPT_LOCATION}.encode_sf_dl")
    @patch(f"{SCRIPT_LOCATION}.get_single_frame_min_dlc")
    def test_create_single_frame_data__mandatory_args(self, mock_get_single_frame_min_dlc, mock_encode_sf_dl,
                                                      addressing_format, payload,
                                                      ai_data_bytes, data_bytes_number, sf_dl_bytes):
        mock_encode_sf_dl.return_value = sf_dl_bytes
        self.mock_encode_ai_data_bytes.return_value = ai_data_bytes
        self.mock_can_dlc_handler.decode_dlc.return_value = data_bytes_number
        expected_output = ai_data_bytes + sf_dl_bytes + bytearray(payload)
        while len(expected_output) < data_bytes_number:
            expected_output.append(DEFAULT_FILLER_BYTE)
        assert encode_single_frame_data(addressing_format=addressing_format,
                                        payload=payload) == expected_output
        mock_get_single_frame_min_dlc.assert_called_once_with(addressing_format=addressing_format,
                                                              payload_length=len(payload))
        mock_encode_sf_dl.assert_called_once_with(sf_dl=len(payload),
                                                  dlc=mock_get_single_frame_min_dlc.return_value,
                                                  addressing_format=addressing_format)
        self.mock_can_dlc_handler.decode_dlc.assert_called_once_with(mock_get_single_frame_min_dlc.return_value)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=None,
                                                               address_extension=None)
        self.mock_validate_raw_byte.assert_called_once_with(DEFAULT_FILLER_BYTE)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=False)

    @pytest.mark.parametrize("addressing_format, payload, dlc, filler_byte, target_address, address_extension, "
                             "ai_data_bytes, data_bytes_number, sf_dl_bytes", [
        (Mock(), [0x12, 0x34, 0x56, 0x78], 8, 0xA5, Mock(), Mock(), bytearray(), 8, bytearray([0x03])),
        (Mock(), [0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE], Mock(), 0xA5, Mock(), Mock(), bytearray(), 8, bytearray([0x03])),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, range(43), 0xF, 0x00, 0x64, 0x9A, bytearray([0xFF]), 64, bytearray([0xA5, 0x5A])),
    ])
    @patch(f"{SCRIPT_LOCATION}.encode_sf_dl")
    @patch(f"{SCRIPT_LOCATION}.get_single_frame_min_dlc")
    def test_create_single_frame_data__all_args(self, mock_get_single_frame_min_dlc, mock_encode_sf_dl,
                                                addressing_format, payload, dlc, filler_byte,
                                                target_address, address_extension,
                                                ai_data_bytes, data_bytes_number, sf_dl_bytes):
        mock_encode_sf_dl.return_value = sf_dl_bytes
        self.mock_encode_ai_data_bytes.return_value = ai_data_bytes
        self.mock_can_dlc_handler.decode_dlc.return_value = data_bytes_number
        expected_output = ai_data_bytes + sf_dl_bytes + bytearray(payload)
        while len(expected_output) < data_bytes_number:
            expected_output.append(filler_byte)
        assert encode_single_frame_data(addressing_format=addressing_format,
                                        payload=payload,
                                        dlc=dlc,
                                        filler_byte=filler_byte,
                                        target_address=target_address,
                                        address_extension=address_extension) == expected_output
        mock_get_single_frame_min_dlc.assert_not_called()
        mock_encode_sf_dl.assert_called_once_with(sf_dl=len(payload),
                                                  dlc=dlc,
                                                  addressing_format=addressing_format)
        self.mock_can_dlc_handler.decode_dlc.assert_called_once_with(dlc)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=False)

    @pytest.mark.parametrize("addressing_format, payload, dlc, filler_byte, target_address, address_extension, "
                             "ai_data_bytes, data_bytes_number, sf_dl_bytes", [
        (Mock(), [0x12, 0x34, 0x56, 0x78], 7, 0xA5, Mock(), Mock(), bytearray(), 7, bytearray([0x03])),
        (Mock(), [0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0, 0xFF], Mock(), 0xA5, Mock(), Mock(), bytearray(), 8, bytearray()),
    ])
    @patch(f"{SCRIPT_LOCATION}.encode_sf_dl")
    @patch(f"{SCRIPT_LOCATION}.get_single_frame_min_dlc")
    def test_create_single_frame_data__inconsistent(self, mock_get_single_frame_min_dlc, mock_encode_sf_dl,
                                                addressing_format, payload, dlc, filler_byte,
                                                target_address, address_extension,
                                                ai_data_bytes, data_bytes_number, sf_dl_bytes):
        mock_encode_sf_dl.return_value = sf_dl_bytes
        self.mock_encode_ai_data_bytes.return_value = ai_data_bytes
        self.mock_can_dlc_handler.decode_dlc.return_value = data_bytes_number
        with pytest.raises(InconsistentArgumentsError):
            encode_single_frame_data(addressing_format=addressing_format,
                                     payload=payload,
                                     dlc=dlc,
                                     filler_byte=filler_byte,
                                     target_address=target_address,
                                     address_extension=address_extension)
        mock_get_single_frame_min_dlc.assert_not_called()
        mock_encode_sf_dl.assert_called_once_with(sf_dl=len(payload),
                                                  dlc=dlc,
                                                  addressing_format=addressing_format)
        self.mock_can_dlc_handler.decode_dlc.assert_called_once_with(dlc)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=False)

    # generate_single_frame_data

    @pytest.mark.parametrize("addressing_format, payload, dlc, sf_dl_short, ai_data_bytes, data_bytes_number, sf_dl_bytes", [
        (Mock(), [], 6, 0, bytearray([0xA5]), 6, bytearray([0x00])),
        (Mock(), range(8), 0xA, 0xF, bytearray(), 10, bytearray([0xFF])),
        (CanAddressingFormat.NORMAL_ADDRESSING, [0x12, 0x34, 0x56], 0xF, 0x3, bytearray(), 64, bytearray([0xAC])),
    ])
    @patch(f"{SCRIPT_LOCATION}.generate_sf_dl_bytes")
    def test_generate_single_frame_data__mandatory_args(self, mock_generate_sf_dl_bytes,
                                                        addressing_format, payload, dlc, sf_dl_short,
                                                        ai_data_bytes, data_bytes_number, sf_dl_bytes):
        self.mock_encode_ai_data_bytes.return_value = ai_data_bytes
        self.mock_can_dlc_handler.decode_dlc.return_value = data_bytes_number
        mock_generate_sf_dl_bytes.return_value = sf_dl_bytes
        expected_output = ai_data_bytes + sf_dl_bytes + bytearray(payload)
        while len(expected_output) < data_bytes_number:
            expected_output.append(DEFAULT_FILLER_BYTE)
        assert generate_single_frame_data(addressing_format=addressing_format,
                                          payload=payload,
                                          dlc=dlc,
                                          sf_dl_short=sf_dl_short) == expected_output
        mock_generate_sf_dl_bytes.assert_called_once_with(sf_dl_short=sf_dl_short, sf_dl_long=None)
        self.mock_can_dlc_handler.decode_dlc.assert_called_once_with(dlc)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=None,
                                                               address_extension=None)
        self.mock_validate_raw_byte.assert_called_once_with(DEFAULT_FILLER_BYTE)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=True)

    @pytest.mark.parametrize("addressing_format, payload, dlc, sf_dl_short, sf_dl_long, filler_byte, target_address, "
                             "address_extension, ai_data_bytes, data_bytes_number, sf_dl_bytes", [
        (Mock(), [], 4, 0xF, 0xFF, 0x00, Mock(), Mock(), bytearray(), 4, bytearray([0x0F, 0xFF])),
        (CanAddressingFormat.NORMAL_ADDRESSING, range(100,150), 0xF, 0x0, 0x00, 0xFF, 0x5A, 0x3C, bytearray([0x98]), 64, bytearray([0x0, 0x00])),
    ])
    @patch(f"{SCRIPT_LOCATION}.generate_sf_dl_bytes")
    def test_generate_single_frame_data__all_args(self, mock_generate_sf_dl_bytes,
                                                  addressing_format, payload, dlc, sf_dl_short, sf_dl_long,
                                                  filler_byte, target_address, address_extension,
                                                  ai_data_bytes, data_bytes_number, sf_dl_bytes):
        self.mock_encode_ai_data_bytes.return_value = ai_data_bytes
        self.mock_can_dlc_handler.decode_dlc.return_value = data_bytes_number
        mock_generate_sf_dl_bytes.return_value = sf_dl_bytes
        expected_output = ai_data_bytes + sf_dl_bytes + bytearray(payload)
        while len(expected_output) < data_bytes_number:
            expected_output.append(filler_byte)
        assert generate_single_frame_data(addressing_format=addressing_format,
                                          payload=payload,
                                          dlc=dlc,
                                          sf_dl_short=sf_dl_short,
                                          sf_dl_long=sf_dl_long,
                                          filler_byte=filler_byte,
                                          target_address=target_address,
                                          address_extension=address_extension) == expected_output
        mock_generate_sf_dl_bytes.assert_called_once_with(sf_dl_short=sf_dl_short, sf_dl_long=sf_dl_long)
        self.mock_can_dlc_handler.decode_dlc.assert_called_once_with(dlc)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=True)

    # extract_sf_dl

    @pytest.mark.parametrize("addressing_format, raw_frame_data, sf_dl_data_bytes, sf_dl", [
        (Mock(), Mock(), [0x08], 8),
        (CanAddressingFormat.EXTENDED_ADDRESSING, b"\x12\x34\x56\x78", [0x02], 2),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, list(range(64)), [0x00, 0x32], 50),
        (CanAddressingFormat.NORMAL_ADDRESSING, list(range(64)), [0x0F, 0x23], 35),
    ])
    @patch(f"{SCRIPT_LOCATION}.extract_sf_dl_data_bytes")
    def test_get_sf_dl__valid(self, mock_extract_sf_dl_data_bytes,
                              addressing_format, raw_frame_data, sf_dl_data_bytes, sf_dl):
        mock_extract_sf_dl_data_bytes.return_value = sf_dl_data_bytes
        assert extract_sf_dl(addressing_format=addressing_format, raw_frame_data=raw_frame_data) == sf_dl
        mock_extract_sf_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)

    @pytest.mark.parametrize("addressing_format, raw_frame_data, sf_dl_data_bytes", [
        (Mock(), Mock(), []),
        (CanAddressingFormat.EXTENDED_ADDRESSING, b"\x12\x34\x56\x78", [0x00, 0x00, 0x23]),
    ])
    @patch(f"{SCRIPT_LOCATION}.extract_sf_dl_data_bytes")
    def test_get_sf_dl__not_implemented(self, mock_extract_sf_dl_data_bytes,
                                        addressing_format, raw_frame_data, sf_dl_data_bytes):
        mock_extract_sf_dl_data_bytes.return_value = sf_dl_data_bytes
        with pytest.raises(NotImplementedError):
            extract_sf_dl(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
        mock_extract_sf_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)

    # get_sf_dl_bytes_number

    @pytest.mark.parametrize("dlc, expected_sf_dl_bytes_number", [
        (MAX_DLC_VALUE_SHORT_SF_DL - 1, SHORT_SF_DL_BYTES_USED),
        (MAX_DLC_VALUE_SHORT_SF_DL, SHORT_SF_DL_BYTES_USED),
        (MAX_DLC_VALUE_SHORT_SF_DL + 1, LONG_SF_DL_BYTES_USED),
        (MAX_DLC_VALUE_SHORT_SF_DL + 100, LONG_SF_DL_BYTES_USED),
    ])
    def test_get_sf_dl_bytes_number(self, dlc, expected_sf_dl_bytes_number):
        assert get_sf_dl_bytes_number(dlc) == expected_sf_dl_bytes_number
        self.mock_can_dlc_handler.validate_dlc.assert_called_once_with(dlc)

    # get_single_frame_min_dlc

    @pytest.mark.parametrize("addressing_format, payload_length, ai_data_bytes, decoded_dlc", [
        (Mock(), MAX_DLC_VALUE_SHORT_SF_DL - 2, 1, MAX_DLC_VALUE_SHORT_SF_DL),
        (CanAddressingFormat.NORMAL_ADDRESSING, 1, 0, MAX_DLC_VALUE_SHORT_SF_DL - 1),
    ])
    def test_get_single_frame_min_dlc__short_dlc(self, addressing_format, payload_length, ai_data_bytes, decoded_dlc):
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes
        self.mock_can_dlc_handler.get_min_dlc.return_value = decoded_dlc
        assert get_single_frame_min_dlc(addressing_format=addressing_format,
                                        payload_length=payload_length) == self.mock_can_dlc_handler.get_min_dlc.return_value
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        data_bytes_number = payload_length + SHORT_SF_DL_BYTES_USED + ai_data_bytes
        self.mock_can_dlc_handler.get_min_dlc.assert_called_once_with(data_bytes_number)

    @pytest.mark.parametrize("addressing_format, payload_length, ai_data_bytes, decoded_dlc", [
        (Mock(), MAX_DLC_VALUE_SHORT_SF_DL, 1, MAX_DLC_VALUE_SHORT_SF_DL + 1),
        (CanAddressingFormat.NORMAL_ADDRESSING, 1, 0, MAX_DLC_VALUE_SHORT_SF_DL + 2),
    ])
    def test_get_single_frame_min_dlc__long_dlc(self, addressing_format, payload_length, ai_data_bytes, decoded_dlc):
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes
        self.mock_can_dlc_handler.get_min_dlc.return_value = decoded_dlc
        assert get_single_frame_min_dlc(addressing_format=addressing_format,
                                        payload_length=payload_length) == self.mock_can_dlc_handler.get_min_dlc.return_value
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        data_bytes_number_1 = payload_length + SHORT_SF_DL_BYTES_USED + ai_data_bytes
        data_bytes_number_2 = payload_length + LONG_SF_DL_BYTES_USED + ai_data_bytes
        self.mock_can_dlc_handler.get_min_dlc.assert_has_calls([call(data_bytes_number_1), call(data_bytes_number_2)],
                                                               any_order=False)

    # get_single_frame_max_payload_size

    @pytest.mark.parametrize(
        "addressing_format, dlc, frame_data_bytes_number, ai_data_bytes_number, sf_dl_bytes_number", [
            (Mock(), Mock(), 8, 0, 1),
            (CanAddressingFormat.MIXED_29BIT_ADDRESSING, 0xF, 64, 1, 2),
            (CanAddressingFormat.NORMAL_ADDRESSING, 0x6, 6, 0, 1),
        ])
    @patch(f"{SCRIPT_LOCATION}.get_sf_dl_bytes_number")
    def test_get_single_frame_max_payload_size__with_dlc(self, mock_get_sf_dl_bytes_number,
                                                         addressing_format, dlc,
                                                         frame_data_bytes_number, ai_data_bytes_number,
                                                         sf_dl_bytes_number):
        self.mock_can_dlc_handler.decode_dlc.return_value = frame_data_bytes_number
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes_number
        mock_get_sf_dl_bytes_number.return_value = sf_dl_bytes_number
        assert (get_single_frame_max_payload_size(addressing_format=addressing_format, dlc=dlc)
                == frame_data_bytes_number - ai_data_bytes_number - sf_dl_bytes_number)
        self.mock_can_dlc_handler.decode_dlc.assert_called_once_with(dlc)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        mock_get_sf_dl_bytes_number.assert_called_once_with(dlc)

    @pytest.mark.parametrize("addressing_format, frame_data_bytes_number, ai_data_bytes_number", [
        (Mock(), 8, 0),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, 64, 1),
        (CanAddressingFormat.NORMAL_ADDRESSING, 6, 0),
    ])
    @patch(f"{SCRIPT_LOCATION}.get_sf_dl_bytes_number")
    def test_get_single_frame_max_payload_size__without_dlc(self, mock_get_sf_dl_bytes_number,
                                                            addressing_format, frame_data_bytes_number,
                                                            ai_data_bytes_number):
        self.mock_can_dlc_handler.MAX_DATA_BYTES_NUMBER = frame_data_bytes_number
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes_number
        assert (get_single_frame_max_payload_size(addressing_format=addressing_format)
                == frame_data_bytes_number - ai_data_bytes_number - LONG_SF_DL_BYTES_USED)
        self.mock_can_dlc_handler.decode_dlc.assert_not_called()
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        mock_get_sf_dl_bytes_number.assert_not_called()

    @pytest.mark.parametrize(
        "addressing_format, dlc, frame_data_bytes_number, ai_data_bytes_number, sf_dl_bytes_number", [
            (Mock(), Mock(), 2, 1, 1),
            (CanAddressingFormat.MIXED_29BIT_ADDRESSING, 0xF, 1, 0, 1),
        ])
    @patch(f"{SCRIPT_LOCATION}.get_sf_dl_bytes_number")
    def test_get_single_frame_max_payload_size__too_short(self, mock_get_sf_dl_bytes_number,
                                                          addressing_format, dlc,
                                                          frame_data_bytes_number, ai_data_bytes_number,
                                                          sf_dl_bytes_number):
        self.mock_can_dlc_handler.decode_dlc.return_value = frame_data_bytes_number
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes_number
        mock_get_sf_dl_bytes_number.return_value = sf_dl_bytes_number
        with pytest.raises(InconsistentArgumentsError):
            get_single_frame_max_payload_size(addressing_format=addressing_format, dlc=dlc)
        self.mock_can_dlc_handler.decode_dlc.assert_called_once_with(dlc)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        mock_get_sf_dl_bytes_number.assert_called_once_with(dlc)

    # extract_sf_dl_data_bytes

    @pytest.mark.parametrize("addressing_format, raw_frame_data, sf_dl_bytes_number, ai_data_bytes_number", [
        (Mock(), (0x78, 0x69, 0x5A, 0x4B, 0x3C, 0x2D, 0x1E, 0x0F), 1, 0),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87", 1, 1),
        (CanAddressingFormat.EXTENDED_ADDRESSING, list(range(64)), 2, 1),
        (CanAddressingFormat.NORMAL_ADDRESSING, list(range(64))[::-1], 2, 0),
    ])
    @patch(f"{SCRIPT_LOCATION}.get_sf_dl_bytes_number")
    def test_extract_sf_dl_data_bytes(self, mock_get_sf_dl_bytes_number,
                                      addressing_format, raw_frame_data, sf_dl_bytes_number, ai_data_bytes_number):
        mock_get_sf_dl_bytes_number.return_value = sf_dl_bytes_number
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes_number
        assert (extract_sf_dl_data_bytes(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
                == bytearray(raw_frame_data)[ai_data_bytes_number:][:sf_dl_bytes_number])
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        self.mock_can_dlc_handler.encode_dlc.assert_called_once_with(len(raw_frame_data))
        mock_get_sf_dl_bytes_number.assert_called_once_with(self.mock_can_dlc_handler.encode_dlc.return_value)

    # encode_sf_dl

    @pytest.mark.parametrize("sf_dl, dlc, addressing_format", [
        (1, MAX_DLC_VALUE_SHORT_SF_DL - 1, Mock()),
        (5, MAX_DLC_VALUE_SHORT_SF_DL, CanAddressingFormat.NORMAL_ADDRESSING),
    ])
    @patch(f"{SCRIPT_LOCATION}.generate_sf_dl_bytes")
    @patch(f"{SCRIPT_LOCATION}.validate_sf_dl")
    def test_encode_sf_dl__short(self, mock_validate_sf_dl, mock_generate_sf_dl_bytes,
                                 sf_dl, dlc, addressing_format):
        assert (encode_sf_dl(sf_dl=sf_dl, dlc=dlc, addressing_format=addressing_format)
                == mock_generate_sf_dl_bytes.return_value)
        mock_generate_sf_dl_bytes.assert_called_once_with(sf_dl_short=sf_dl)
        mock_validate_sf_dl.assert_called_once_with(sf_dl=sf_dl, dlc=dlc, addressing_format=addressing_format)

    @pytest.mark.parametrize("sf_dl, dlc, addressing_format", [
        (1, MAX_DLC_VALUE_SHORT_SF_DL + 1, Mock()),
        (26, MAX_DLC_VALUE_SHORT_SF_DL + 5, CanAddressingFormat.NORMAL_ADDRESSING),
    ])
    @patch(f"{SCRIPT_LOCATION}.generate_sf_dl_bytes")
    @patch(f"{SCRIPT_LOCATION}.validate_sf_dl")
    def test_encode_sf_dl__long(self, mock_validate_sf_dl, mock_generate_sf_dl_bytes,
                                sf_dl, dlc, addressing_format):
        assert (encode_sf_dl(sf_dl=sf_dl, dlc=dlc, addressing_format=addressing_format)
                == mock_generate_sf_dl_bytes.return_value)
        mock_generate_sf_dl_bytes.assert_called_once_with(sf_dl_long=sf_dl)
        mock_validate_sf_dl.assert_called_once_with(sf_dl=sf_dl, dlc=dlc, addressing_format=addressing_format)

    # generate_sf_dl_bytes

    @pytest.mark.parametrize("sf_dl_short, expected_output", [
        (0, bytearray([0x00])),
        (7, bytearray([0x07])),
        (0xF, bytearray([0x0F])),
    ])
    def test_generate_sf_dl_bytes__short(self, sf_dl_short, expected_output):
        assert generate_sf_dl_bytes(sf_dl_short=sf_dl_short) == expected_output
        self.mock_validate_nibble.assert_called_once_with(sf_dl_short)

    @pytest.mark.parametrize("sf_dl_short, sf_dl_long, expected_output", [
        (0x0, 0x00, bytearray([0x00, 0x00])),
        (0x0, 0x12, bytearray([0x00, 0x12])),
        (0x0, 63, bytearray([0x00, 63])),
        (0xF, 0xFF, bytearray([0x0F, 0xFF])),
    ])
    def test_generate_sf_dl_bytes__long(self, sf_dl_short, sf_dl_long, expected_output):
        assert generate_sf_dl_bytes(sf_dl_short=sf_dl_short, sf_dl_long=sf_dl_long) == expected_output
        self.mock_validate_nibble.assert_called_once_with(sf_dl_short)
        self.mock_validate_raw_byte.assert_called_once_with(sf_dl_long)

    # validate_sf_dl

    @pytest.mark.parametrize("sf_dl", [Mock(), "not an int"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_validate_sf_dl__type_error(self, mock_isinstance, sf_dl):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            validate_sf_dl(sf_dl=sf_dl, dlc=Mock(), addressing_format=Mock())
        mock_isinstance.assert_called_once_with(sf_dl, int)

    @pytest.mark.parametrize("sf_dl", [0, -1, -6])
    def test_validate_sf_dl__value_error(self, sf_dl):
        with pytest.raises(ValueError):
            validate_sf_dl(sf_dl=sf_dl, dlc=Mock(), addressing_format=Mock())

    @pytest.mark.parametrize("sf_dl, max_sf, dlc, addressing_format", [
        [54, 53, Mock(), Mock()],
        [63, 62, 15, CanAddressingFormat.MIXED_29BIT_ADDRESSING],
        [8, 7, 8, CanAddressingFormat.NORMAL_ADDRESSING],
    ])
    @patch(f"{SCRIPT_LOCATION}.get_single_frame_max_payload_size")
    def test_validate_sf_dl__inconsistent(self, mock_get_single_frame_max_payload_size,
                                          sf_dl, max_sf, dlc, addressing_format):
        mock_get_single_frame_max_payload_size.return_value = max_sf
        with pytest.raises(InconsistentArgumentsError):
            validate_sf_dl(sf_dl=sf_dl, dlc=dlc, addressing_format=addressing_format)
        mock_get_single_frame_max_payload_size.assert_called_once_with(addressing_format=addressing_format, dlc=dlc)

    @pytest.mark.parametrize("sf_dl, max_sf, dlc, addressing_format", [
        [54, 54, Mock(), Mock()],
        [63, 63, 15, CanAddressingFormat.MIXED_29BIT_ADDRESSING],
        [7, 7, 8, CanAddressingFormat.NORMAL_ADDRESSING],
    ])
    @patch(f"{SCRIPT_LOCATION}.get_single_frame_max_payload_size")
    def test_validate_sf_dl__valid(self, mock_get_single_frame_max_payload_size,
                                   sf_dl, max_sf, dlc, addressing_format):
        mock_get_single_frame_max_payload_size.return_value = max_sf
        assert validate_sf_dl(sf_dl=sf_dl, dlc=dlc, addressing_format=addressing_format) is None
        mock_get_single_frame_max_payload_size.assert_called_once_with(addressing_format=addressing_format, dlc=dlc)

# class TestCanSingleFrameHandler:
#     """Unit tests for `CanSingleFrameHandler` class."""
#
#     def setup_method(self):
#         self._patcher_validate_nibble = patch(f"{SCRIPT_LOCATION}.validate_nibble")
#         self.mock_validate_nibble = self._patcher_validate_nibble.start()
#         self._patcher_validate_raw_byte = patch(f"{SCRIPT_LOCATION}.validate_raw_byte")
#         self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
#         self._patcher_validate_raw_bytes = patch(f"{SCRIPT_LOCATION}.validate_raw_bytes")
#         self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
#         self._patcher_encode_dlc = patch(f"{SCRIPT_LOCATION}.CanDlcHandler.encode_dlc")
#         self.mock_encode_dlc = self._patcher_encode_dlc.start()
#         self._patcher_decode_dlc = patch(f"{SCRIPT_LOCATION}.CanDlcHandler.decode_dlc")
#         self.mock_decode_dlc = self._patcher_decode_dlc.start()
#         self._patcher_get_min_dlc = patch(f"{SCRIPT_LOCATION}.CanDlcHandler.get_min_dlc")
#         self.mock_get_min_dlc = self._patcher_get_min_dlc.start()
#         self._patcher_validate_dlc = patch(f"{SCRIPT_LOCATION}.CanDlcHandler.validate_dlc")
#         self.mock_validate_dlc = self._patcher_validate_dlc.start()
#         self._patcher_encode_ai_data_bytes = \
#             patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.encode_ai_data_bytes")
#         self.mock_encode_ai_data_bytes = self._patcher_encode_ai_data_bytes.start()
#         self._patcher_get_ai_data_bytes_number = \
#             patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.get_ai_data_bytes_number")
#         self.mock_get_ai_data_bytes_number = self._patcher_get_ai_data_bytes_number.start()
#
#     def teardown_method(self):
#         self._patcher_validate_nibble.stop()
#         self._patcher_validate_raw_byte.stop()
#         self._patcher_validate_raw_bytes.stop()
#         self._patcher_encode_dlc.stop()
#         self._patcher_decode_dlc.stop()
#         self._patcher_get_min_dlc.stop()
#         self._patcher_validate_dlc.stop()
#         self._patcher_encode_ai_data_bytes.stop()
#         self._patcher_get_ai_data_bytes_number.stop()
#

#
#     @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
#         ("some format", "TA", "SA"),
#         ("another format", None, None),
#     ])
#     @pytest.mark.parametrize("dlc, filler_byte", [
#         ("some DLC", 0x66),
#         (8, 0x99),
#     ])
#     @pytest.mark.parametrize("payload, data_bytes_number, ai_bytes, sf_dl_bytes", [
#         ([0x54], 2, bytearray(), bytearray([0xFA])),
#         (range(50, 110), 64, bytearray([0x98]), bytearray([0x12, 0x34])),
#     ])
#     @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.get_min_dlc")
#     @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__encode_valid_sf_dl")
#     def test_create_valid_frame_data__valid_without_dlc(self, mock_encode_sf_dl, mock_get_min_dlc,
#                                                         addressing_format, target_address, address_extension,
#                                                         payload, dlc, filler_byte, data_bytes_number, ai_bytes,
#                                                         sf_dl_bytes):
#         self.mock_encode_ai_data_bytes.return_value = ai_bytes
#         self.mock_decode_dlc.return_value = data_bytes_number
#         mock_encode_sf_dl.return_value = sf_dl_bytes
#         mock_get_min_dlc.return_value = dlc
#         sf_frame_data = CanSingleFrameHandler.create_valid_frame_data(addressing_format=addressing_format,
#                                                                       payload=payload,
#                                                                       dlc=None,
#                                                                       filler_byte=filler_byte,
#                                                                       target_address=target_address,
#                                                                       address_extension=address_extension)
#         self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=False)
#         self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
#         self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
#                                                                target_address=target_address,
#                                                                address_extension=address_extension)
#         mock_get_min_dlc.assert_called_once_with(addressing_format=addressing_format,
#                                                  payload_length=len(payload))
#         self.mock_decode_dlc.assert_called_once_with(dlc)
#         mock_encode_sf_dl.assert_called_once_with(sf_dl=len(payload),
#                                                   dlc=dlc,
#                                                   addressing_format=addressing_format)
#         assert isinstance(sf_frame_data, bytearray)
#         assert len(sf_frame_data) == data_bytes_number
#
#     @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
#         ("some format", "TA", "SA"),
#         ("another format", None, None),
#     ])
#     @pytest.mark.parametrize("filler_byte", [0x66, 0x99])
#     @pytest.mark.parametrize("dlc, payload, data_bytes_number, ai_bytes, sf_dl_bytes", [
#         (CanDlcHandler.MIN_BASE_UDS_DLC - 1, range(60), 100, bytearray([0xFF]), bytearray([0x00, 0xFA])),
#         (CanDlcHandler.MIN_BASE_UDS_DLC, [0x20, 0x30, 0x44], 3, bytearray(), bytearray([0x03])),
#         (CanDlcHandler.MIN_BASE_UDS_DLC + 1, range(20), 21, bytearray([0xAA]), bytearray([0x03])),
#     ])
#     @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__encode_valid_sf_dl")
#     def test_create_valid_frame_data__inconsistent_args(self, mock_encode_sf_dl,
#                                                         addressing_format, target_address, address_extension,
#                                                         payload, dlc, filler_byte,
#                                                         data_bytes_number, ai_bytes, sf_dl_bytes):
#         self.mock_encode_ai_data_bytes.return_value = ai_bytes
#         self.mock_decode_dlc.return_value = data_bytes_number
#         mock_encode_sf_dl.return_value = sf_dl_bytes
#         with pytest.raises(InconsistentArgumentsError):
#             CanSingleFrameHandler.create_valid_frame_data(addressing_format=addressing_format,
#                                                           payload=payload,
#                                                           dlc=dlc,
#                                                           filler_byte=filler_byte,
#                                                           target_address=target_address,
#                                                           address_extension=address_extension)
#         self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=False)
#         self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
#         self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
#                                                                target_address=target_address,
#                                                                address_extension=address_extension)
#         self.mock_decode_dlc.assert_called_once_with(dlc)
#         mock_encode_sf_dl.assert_called_once_with(sf_dl=len(payload),
#                                                   dlc=dlc,
#                                                   addressing_format=addressing_format)
#

#
#

#

#
#
#
#
#     # validate_frame_data
#
#     @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
#     @pytest.mark.parametrize("raw_frame_data, dlc, ai_bytes_number, sf_dl_data_bytes", [
#         (list(range(8)), 8, 0, [0x07]),
#         (list(range(64)), 10, 0, [0x00, 0x3E]),
#     ])
#     @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__extract_sf_dl_data_bytes")
#     @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.is_single_frame")
#     def test_validate_frame_data__valid(self, mock_is_single_frame, mock_extract_sf_dl_data_bytes,
#                                         addressing_format, raw_frame_data,
#                                         ai_bytes_number, sf_dl_data_bytes, dlc):
#         mock_is_single_frame.return_value = True
#         self.mock_get_ai_data_bytes_number.return_value = ai_bytes_number
#         mock_extract_sf_dl_data_bytes.return_value = sf_dl_data_bytes
#         self.mock_encode_dlc.return_value = dlc
#         CanSingleFrameHandler.validate_frame_data(addressing_format=addressing_format,
#                                                   raw_frame_data=raw_frame_data)
#         self.mock_validate_raw_bytes.assert_called_once_with(raw_frame_data)
#         mock_is_single_frame.assert_called_once_with(addressing_format=addressing_format,
#                                                      raw_frame_data=raw_frame_data)
#         self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
#         mock_extract_sf_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
#                                                               raw_frame_data=raw_frame_data)
#         self.mock_encode_dlc.assert_called_once_with(len(raw_frame_data))
#
#     @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
#     @pytest.mark.parametrize("raw_frame_data", ["some raw bbytes", range(6)])
#     @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.is_single_frame")
#     def test_validate_frame_data__invalid_type(self, mock_is_single_frame, addressing_format, raw_frame_data):
#         mock_is_single_frame.return_value = False
#         with pytest.raises(ValueError):
#             CanSingleFrameHandler.validate_frame_data(addressing_format=addressing_format,
#                                                       raw_frame_data=raw_frame_data)
#         self.mock_validate_raw_bytes.assert_called_once_with(raw_frame_data)
#         mock_is_single_frame.assert_called_once_with(addressing_format=addressing_format,
#                                                      raw_frame_data=raw_frame_data)
#
#     @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
#     @pytest.mark.parametrize("raw_frame_data, dlc, ai_bytes_number, sf_dl_data_bytes", [
#         (list(range(7)), 8, 0, [0x07]),
#         (list(range(9)), 9, 1, [0x00, 0x08]),
#         (list(range(64)), 10, 0, [0x0A, 0x3F]),
#     ])
#     @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__extract_sf_dl_data_bytes")
#     @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.is_single_frame")
#     def test_validate_frame_data__sf_dl_bytes(self, mock_is_single_frame, mock_extract_sf_dl_data_bytes,
#                                               addressing_format, raw_frame_data,
#                                               ai_bytes_number, sf_dl_data_bytes, dlc):
#         mock_is_single_frame.return_value = True
#         self.mock_get_ai_data_bytes_number.return_value = ai_bytes_number
#         mock_extract_sf_dl_data_bytes.return_value = sf_dl_data_bytes
#         self.mock_encode_dlc.return_value = dlc
#         with pytest.raises(InconsistentArgumentsError):
#             CanSingleFrameHandler.validate_frame_data(addressing_format=addressing_format,
#                                                       raw_frame_data=raw_frame_data)
#         self.mock_validate_raw_bytes.assert_called_once_with(raw_frame_data)
#         mock_is_single_frame.assert_called_once_with(addressing_format=addressing_format,
#                                                      raw_frame_data=raw_frame_data)
#         self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
#         mock_extract_sf_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
#                                                               raw_frame_data=raw_frame_data)
#         self.mock_encode_dlc.assert_called_once_with(len(raw_frame_data))
#

#
#     # __validate_payload_length
#
#     @pytest.mark.parametrize("payload_length", [None, 6.5, "not a payload length"])
#     @pytest.mark.parametrize("ai_data_bytes_number", [0, 1])
#     def test_validate_payload_length__type_error(self, payload_length, ai_data_bytes_number):
#         with pytest.raises(TypeError):
#             CanSingleFrameHandler._CanSingleFrameHandler__validate_payload_length(payload_length=payload_length,
#                                                                                   ai_data_bytes_number=ai_data_bytes_number)
#
#     @pytest.mark.parametrize("payload_length", [0, -1])
#     @pytest.mark.parametrize("ai_data_bytes_number", [0, 1])
#     def test_validate_payload_length__value_error(self, payload_length, ai_data_bytes_number):
#         with pytest.raises(ValueError):
#             CanSingleFrameHandler._CanSingleFrameHandler__validate_payload_length(payload_length=payload_length,
#                                                                                   ai_data_bytes_number=ai_data_bytes_number)
#
#     @pytest.mark.parametrize("payload_length, ai_data_bytes_number", [
#         (CanDlcHandler.MAX_DATA_BYTES_NUMBER - CanSingleFrameHandler.LONG_SF_DL_BYTES_USED, 1),
#         (CanDlcHandler.MAX_DATA_BYTES_NUMBER - CanSingleFrameHandler.LONG_SF_DL_BYTES_USED + 42, 1),
#         (CanDlcHandler.MAX_DATA_BYTES_NUMBER - CanSingleFrameHandler.LONG_SF_DL_BYTES_USED + 1, 0),
#         (CanDlcHandler.MAX_DATA_BYTES_NUMBER - CanSingleFrameHandler.LONG_SF_DL_BYTES_USED + 5, 0),
#     ])
#     def test_validate_payload_length__inconsistency_error(self, payload_length, ai_data_bytes_number):
#         with pytest.raises(InconsistentArgumentsError):
#             CanSingleFrameHandler._CanSingleFrameHandler__validate_payload_length(payload_length=payload_length,
#                                                                                   ai_data_bytes_number=ai_data_bytes_number)
#
#     @pytest.mark.parametrize("payload_length, ai_data_bytes_number", [
#         (CanDlcHandler.MAX_DATA_BYTES_NUMBER - CanSingleFrameHandler.LONG_SF_DL_BYTES_USED - 1, 1),
#         (CanDlcHandler.MAX_DATA_BYTES_NUMBER - CanSingleFrameHandler.LONG_SF_DL_BYTES_USED, 0),
#         (1, 0),
#     ])
#     def test_validate_payload_length__valid(self, payload_length, ai_data_bytes_number):
#         CanSingleFrameHandler._CanSingleFrameHandler__validate_payload_length(payload_length=payload_length,
#                                                                               ai_data_bytes_number=ai_data_bytes_number)
#
#
#     # __encode_valid_sf_dl
#
#     @pytest.mark.parametrize("sf_dl", [0, 8, 0xF])
#     @pytest.mark.parametrize("dlc", [CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL,
#                                      CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL - 1])
#     @pytest.mark.parametrize("addressing_format", [None, "some addressing format"])
#     @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__encode_any_sf_dl")
#     @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.validate_sf_dl")
#     def test_encode_valid_sf_dl__short(self, mock_validate_sf_dl, mock_encode_any_sf_dl,
#                                  sf_dl, dlc, addressing_format):
#         assert CanSingleFrameHandler._CanSingleFrameHandler__encode_valid_sf_dl(
#             sf_dl=sf_dl,
#             addressing_format=addressing_format,
#             dlc=dlc) == mock_encode_any_sf_dl.return_value
#         mock_validate_sf_dl.assert_called_once_with(sf_dl=sf_dl,
#                                                     dlc=dlc,
#                                                     addressing_format=addressing_format)
#         mock_encode_any_sf_dl.assert_called_once_with(sf_dl_short=sf_dl)
#
#     @pytest.mark.parametrize("sf_dl", [0, 8, 0xF])
#     @pytest.mark.parametrize("dlc", [CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL + 1,
#                                      CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL + 2])
#     @pytest.mark.parametrize("addressing_format", [None, "some addressing format"])
#     @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__encode_any_sf_dl")
#     @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.validate_sf_dl")
#     def test_encode_valid_sf_dl__long(self, mock_validate_sf_dl, mock_encode_any_sf_dl,
#                                 sf_dl, dlc, addressing_format):
#         assert CanSingleFrameHandler._CanSingleFrameHandler__encode_valid_sf_dl(
#             sf_dl=sf_dl,
#             addressing_format=addressing_format,
#             dlc=dlc) == mock_encode_any_sf_dl.return_value
#         mock_validate_sf_dl.assert_called_once_with(sf_dl=sf_dl,
#                                                     dlc=dlc,
#                                                     addressing_format=addressing_format)
#         mock_encode_any_sf_dl.assert_called_once_with(sf_dl_long=sf_dl)
#
#     # __encode_any_sf_dl
#
#     @pytest.mark.parametrize("sf_dl_short", [0, 7, 0xF])
#     def test_encode_any_sf_dl__short(self, sf_dl_short):
#         assert (CanSingleFrameHandler._CanSingleFrameHandler__encode_any_sf_dl(sf_dl_short=sf_dl_short)
#                 == bytearray([(CanSingleFrameHandler.SINGLE_FRAME_N_PCI << 4) + sf_dl_short]))
#         self.mock_validate_nibble.assert_called_once_with(sf_dl_short)
#         self.mock_validate_raw_byte.assert_not_called()
#
#     @pytest.mark.parametrize("sf_dl_short", [0, 5, 0xF])
#     @pytest.mark.parametrize("sf_dl_long", [0, 7, 0xF])
#     def test_encode_any_sf_dl__long(self, sf_dl_short, sf_dl_long):
#         assert (CanSingleFrameHandler._CanSingleFrameHandler__encode_any_sf_dl(sf_dl_short=sf_dl_short,
#                                                                               sf_dl_long=sf_dl_long)
#                 == bytearray([(CanSingleFrameHandler.SINGLE_FRAME_N_PCI << 4) + sf_dl_short, sf_dl_long]))
#         self.mock_validate_nibble.assert_called_once_with(sf_dl_short)
#         self.mock_validate_raw_byte.assert_called_once_with(sf_dl_long)
#
#
# @pytest.mark.integration
# class TestCanSingleFrameHandlerIntegration:
#     """Integration tests for `CanSingleFrameHandler` class."""
#
#     # create_valid_frame_data
#
#     @pytest.mark.parametrize("kwargs, expected_raw_frame_data", [
#         ({"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
#           "payload": [0x3E]}, bytearray([0x01, 0x3E])),
#         ({"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
#           "payload": [0x3E],
#           "dlc": 8,
#           "target_address": 0xFF}, bytearray([0x01, 0x3E] + ([DEFAULT_FILLER_BYTE] * 6))),
#         ({"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
#           "payload": list(range(54)),
#           "filler_byte": 0x66,
#           "target_address": 0xF2}, bytearray([0xF2, 0x00, 0x36] + list(range(54)) + ([0x66] * 7))),
#         ({"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
#           "payload": [0x9A, 0xB8, 0xC4, 0x67, 0x10, 0x00],
#           "dlc": 8,
#           "filler_byte": 0x66,
#           "address_extension": 0x12}, bytearray([0x12, 0x06, 0x9A, 0xB8, 0xC4, 0x67, 0x10, 0x00])),
#         ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
#           "payload": [0x9A, 0xB8, 0xC4, 0x67, 0x10, 0x00, 0x01],
#           "filler_byte": 0x99,
#           "target_address": 0xF2,
#           "address_extension": 0x12}, bytearray([0x12, 0x00, 0x07, 0x9A, 0xB8, 0xC4, 0x67, 0x10, 0x00, 0x01, 0x99, 0x99])),
#     ])
#     def test_create_valid_frame_data__valid(self, kwargs, expected_raw_frame_data):
#         assert CanSingleFrameHandler.create_valid_frame_data(**kwargs) == expected_raw_frame_data
#
#     @pytest.mark.parametrize("kwargs", [
#         {"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
#          "payload": b"\x3E",
#          "dlc": 1},
#         {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
#          "payload": bytes(range(63))},
#         {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
#          "payload": bytes(range(50, 112)),
#          "target_address": 0xF2},
#         {"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
#          "payload": b"\xAB",
#          "dlc": 7,
#          "address_extension": 0x12},
#         {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
#          "payload": [],
#          "target_address": 0xF2,
#          "address_extension": 0x12},
#     ])
#     def test_create_valid_frame_data__invalid(self, kwargs):
#         with pytest.raises(ValueError):
#             CanSingleFrameHandler.create_valid_frame_data(**kwargs)
#
#     # create_any_frame_data
#
#     @pytest.mark.parametrize("kwargs, expected_raw_frame_data", [
#         ({"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
#           "payload": [0x3E],
#           "dlc": 2,
#           "sf_dl_short": 0xF}, bytearray([0x0F, 0x3E])),
#         ({"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
#           "payload": [0x3E],
#           "dlc": 8,
#           "target_address": 0xFF,
#           "sf_dl_short": 0x0,
#           "sf_dl_long": 0xAB}, bytearray([0x00, 0xAB, 0x3E] + ([DEFAULT_FILLER_BYTE] * 5))),
#         ({"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
#           "payload": [],
#           "dlc": 0xF,
#           "filler_byte": 0x66,
#           "target_address": 0xF2,
#           "sf_dl_short": 0xE}, bytearray([0xF2, 0x0E] + ([0x66] * 62))),
#         ({"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
#           "payload": [0x9A, 0xB8, 0xC4, 0x67, 0x10, 0x00],
#           "dlc": 8,
#           "filler_byte": 0x66,
#           "address_extension": 0x12,
#           "sf_dl_short": 0x5}, bytearray([0x12, 0x05, 0x9A, 0xB8, 0xC4, 0x67, 0x10, 0x00])),
#         ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
#           "payload": [0x9A, 0xB8],
#           "dlc": 7,
#           "filler_byte": 0x99,
#           "target_address": 0xF2,
#           "address_extension": 0x12,
#           "sf_dl_short": 0x2}, bytearray([0x12, 0x02, 0x9A, 0xB8, 0x99, 0x99, 0x99])),
#     ])
#     def test_create_any_frame_data__valid(self, kwargs, expected_raw_frame_data):
#         assert CanSingleFrameHandler.create_any_frame_data(**kwargs) == expected_raw_frame_data
#
#     @pytest.mark.parametrize("kwargs", [
#         {"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
#          "payload": [0x3E],
#          "dlc": 1,
#          "sf_dl_short": 0xF},
#         {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
#          "payload": list(range(63)),
#          "dlc": 0xF,
#          "sf_dl_short": 0x0,
#          "sf_dl_long": 0xAB},
#         {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
#          "payload": [],
#          "dlc": 0xF,
#          "target_address": 0xF2,
#          "sf_dl_short": 0x10},
#         {"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
#          "payload": list(range(5)),
#          "dlc": 8,
#          "address_extension": 0x12,
#          "sf_dl_short": 0,
#          "sf_dl_long": 0x100},
#     ])
#     def test_create_any_frame_data__invalid(self, kwargs):
#         with pytest.raises(ValueError):
#             CanSingleFrameHandler.create_any_frame_data(**kwargs)
#
#     # extract_sf_dl
#
#     @pytest.mark.parametrize("addressing_format, raw_frame_data, expected_sf_dl", [
#         (CanAddressingFormat.NORMAL_ADDRESSING, (0x01, 0x3E), 1),
#         (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, [0x00, 0x32] + list(range(20, 82)), 0x32),
#         (CanAddressingFormat.EXTENDED_ADDRESSING, [0x05, 0x04, 0x03, 0x02, 0x01, 0x00, 0xFF, 0xFE], 4),
#         (CanAddressingFormat.MIXED_11BIT_ADDRESSING, [0x0A, 0x00, 0x3D] + list(range(100, 161)), 0x3D),
#         (CanAddressingFormat.MIXED_29BIT_ADDRESSING, [0xDA, 0x00, 0x10] + list(range(21)), 0x10)
#     ])
#     def test_extract_sf_dl(self, addressing_format, raw_frame_data, expected_sf_dl):
#         assert CanSingleFrameHandler.extract_sf_dl(addressing_format=addressing_format,
#                                                   raw_frame_data=raw_frame_data) == expected_sf_dl
#
#     # validate_frame_data
#
#     @pytest.mark.parametrize("addressing_format, raw_frame_data", [
#         (CanAddressingFormat.NORMAL_ADDRESSING, (0x07, 0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32)),
#         (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, [0x00, 0x3E] + list(range(0x10, 0x4E))),
#         (CanAddressingFormat.EXTENDED_ADDRESSING, [0x00, 0x00, 0x01] + list(range(0x10, 0x4D))),
#         (CanAddressingFormat.MIXED_11BIT_ADDRESSING, (0x02, 0x01, 0xFF)),
#         (CanAddressingFormat.MIXED_29BIT_ADDRESSING, [0x04, 0x00, 0x05] + list(range(100, 113))),
#     ])
#     def test_validate_frame_data__valid(self, addressing_format, raw_frame_data):
#         assert CanSingleFrameHandler.validate_frame_data(addressing_format=addressing_format,
#                                                          raw_frame_data=raw_frame_data) is None
#
#     @pytest.mark.parametrize("addressing_format, raw_frame_data", [
#         (CanAddressingFormat.NORMAL_ADDRESSING, (0x05, 0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54)),
#         (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, [0x00, 0x3F] + list(range(0x10, 0x4E))),
#         (CanAddressingFormat.EXTENDED_ADDRESSING, [0x00, 0x01, 0x01] + list(range(0x10, 0x4D))),
#         (CanAddressingFormat.MIXED_11BIT_ADDRESSING, (0x02, 0x07, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF)),
#         (CanAddressingFormat.MIXED_29BIT_ADDRESSING, [0xB0, 0x09] + list(range(100, 114))),
#     ])
#     def test_validate_frame_data__invalid(self, addressing_format, raw_frame_data):
#         with pytest.raises(ValueError):
#             CanSingleFrameHandler.validate_frame_data(addressing_format=addressing_format,
#                                                       raw_frame_data=raw_frame_data)

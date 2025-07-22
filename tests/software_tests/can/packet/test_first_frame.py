import pytest
from mock import Mock, patch

from uds.can.packet.first_frame import (
    FIRST_FRAME_N_PCI,
    LONG_FF_DL_BYTES_USED,
    MAX_LONG_FF_DL_VALUE,
    MAX_SHORT_FF_DL_VALUE,
    SHORT_FF_DL_BYTES_USED,
    CanAddressingFormat,
    CanDlcHandler,
    InconsistentArgumentsError,
    create_first_frame_data,
    encode_ff_dl,
    extract_ff_dl,
    extract_ff_dl_data_bytes,
    extract_first_frame_payload,
    generate_ff_dl_bytes,
    generate_first_frame_data,
    get_first_frame_payload_size,
    is_first_frame,
    validate_ff_dl,
    validate_first_frame_data,
)

SCRIPT_LOCATION = "uds.can.packet.first_frame"


class TestCanFirstFrame:
    """Unit tests for functions in CAN First Frame module."""

    def setup_method(self):
        self._patcher_validate_raw_bytes = patch(f"{SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
        self._patcher_can_addressing_information = patch(f"{SCRIPT_LOCATION}.CanAddressingInformation")
        self.mock_can_addressing_information = self._patcher_can_addressing_information.start()
        self._patcher_dlc_handler = patch(f"{SCRIPT_LOCATION}.CanDlcHandler",
                                          Mock(MIN_BASE_UDS_DLC=CanDlcHandler.MIN_BASE_UDS_DLC))
        self.mock_dlc_handler = self._patcher_dlc_handler.start()
        self._patcher_get_max_sf_dl = patch(f"{SCRIPT_LOCATION}.get_max_sf_dl")
        self.mock_get_max_sf_dl = self._patcher_get_max_sf_dl.start()

    def teardown_method(self):
        self._patcher_validate_raw_bytes.stop()
        self._patcher_can_addressing_information.stop()
        self._patcher_dlc_handler.stop()
        self._patcher_get_max_sf_dl.stop()

    # is_single_frame

    @pytest.mark.parametrize("addressing_format, raw_frame_data, ai_data_bytes_number, expected_output", [
        (Mock(), [FIRST_FRAME_N_PCI << 4, 0] + list(range(100, 162)), 0, True),
        (Mock(), [(FIRST_FRAME_N_PCI << 4) + 0xF, 0xFF] + list(range(6)), 0, True),
        (Mock(), [(FIRST_FRAME_N_PCI << 4) + 0xF, 0xFF, 0x0F, 0x1E, 0x2D, 0x3C, 0x4B, 0x5A], 1, False),
        (CanAddressingFormat.EXTENDED_ADDRESSING, [0xFF, (FIRST_FRAME_N_PCI << 4) + 0x5, 0xFF], 1, True),
    ])
    def test_is_first_frame(self, addressing_format, raw_frame_data, ai_data_bytes_number, expected_output):
        self.mock_can_addressing_information.get_ai_data_bytes_number.return_value = ai_data_bytes_number
        assert is_first_frame(addressing_format=addressing_format, raw_frame_data=raw_frame_data) is expected_output
        self.mock_can_addressing_information.get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    # validate_first_frame_data

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        (Mock(), Mock()),
        (CanAddressingFormat.NORMAL_ADDRESSING, list(range(8))),
    ])
    @patch(f"{SCRIPT_LOCATION}.is_first_frame")
    def test_validate_first_frame_data__value_error(self, mock_is_first_frame,
                                              addressing_format, raw_frame_data):
        mock_is_first_frame.return_value = False
        with pytest.raises(ValueError):
            validate_first_frame_data(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
        self.mock_validate_raw_bytes.assert_called_once_with(raw_frame_data, allow_empty=False)
        mock_is_first_frame.assert_called_once_with(addressing_format=addressing_format, raw_frame_data=raw_frame_data)

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        (Mock(), range(64)),
        (CanAddressingFormat.NORMAL_ADDRESSING, list(range(8))),
    ])
    @patch(f"{SCRIPT_LOCATION}.validate_ff_dl")
    @patch(f"{SCRIPT_LOCATION}.extract_ff_dl_data_bytes")
    @patch(f"{SCRIPT_LOCATION}.extract_ff_dl")
    @patch(f"{SCRIPT_LOCATION}.is_first_frame")
    def test_validate_frame_data__valid(self, mock_is_first_frame, mock_extract_ff_dl, mock_extract_ff_dl_data_bytes,
                                        mock_validate_ff_dl,
                                        addressing_format, raw_frame_data):
        mock_is_first_frame.return_value = True
        assert validate_first_frame_data(addressing_format=addressing_format, raw_frame_data=raw_frame_data) is None
        self.mock_validate_raw_bytes.assert_called_once_with(raw_frame_data, allow_empty=False)
        mock_is_first_frame.assert_called_once_with(addressing_format=addressing_format,
                                                    raw_frame_data=raw_frame_data)
        mock_extract_ff_dl.assert_called_once_with(addressing_format=addressing_format,
                                                   raw_frame_data=raw_frame_data)
        mock_extract_ff_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)
        self.mock_dlc_handler.encode_dlc.assert_called_once_with(len(raw_frame_data))
        mock_validate_ff_dl.assert_called_once_with(
            addressing_format=addressing_format,
            dlc=self.mock_dlc_handler.encode_dlc.return_value,
            ff_dl=mock_extract_ff_dl.return_value,
            ff_dl_bytes_number=mock_extract_ff_dl_data_bytes.return_value.__len__.return_value)

    # create_first_frame_data

    @pytest.mark.parametrize("addressing_format, payload, dlc, data_length, target_address, address_extension, "
                             "ai_data_bytes, ff_dl_data_bytes", [
        (Mock(), [0x12, 0x34, 0x56, 0x78], 8, 13, Mock(), Mock(), bytearray([0x23]), bytearray([0x12, 0x34])),
        (CanAddressingFormat.NORMAL_ADDRESSING, range(58), 0xF, 0x98765434, 0x76, 0x65, bytearray(),
         bytearray([0x10, 0x00, 0xFE, 0xDC, 0xBA, 0x98])),
    ])
    @patch(f"{SCRIPT_LOCATION}.encode_ff_dl")
    def test_create_first_frame_data__valid(self, mock_encode_ff_dl,
                                            addressing_format, payload, dlc, data_length, target_address,
                                            address_extension,
                                            ai_data_bytes, ff_dl_data_bytes):
        expected_output = bytearray(ai_data_bytes) + bytearray(ff_dl_data_bytes) + bytearray(payload)
        self.mock_can_addressing_information.encode_ai_data_bytes.return_value = ai_data_bytes
        mock_encode_ff_dl.return_value = ff_dl_data_bytes
        self.mock_dlc_handler.decode_dlc.return_value = len(expected_output)
        assert create_first_frame_data(addressing_format=addressing_format,
                                       payload=payload,
                                       dlc=dlc,
                                       data_length=data_length,
                                       target_address=target_address,
                                       address_extension=address_extension) == expected_output
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=False)
        self.mock_can_addressing_information.encode_ai_data_bytes.assert_called_once_with(
            addressing_format=addressing_format,
            target_address=target_address,
            address_extension=address_extension)
        mock_encode_ff_dl.assert_called_once_with(addressing_format=addressing_format, dlc=dlc, ff_dl=data_length)
        self.mock_dlc_handler.decode_dlc.assert_called_once_with(dlc)

    @pytest.mark.parametrize("addressing_format, payload, dlc, data_length, target_address, address_extension, "
                             "ai_data_bytes, ff_dl_data_bytes, frame_data_length", [
        (Mock(), [0x12, 0x34, 0x56, 0x78], 8, 13, Mock(), Mock(), bytearray([0x23]), bytearray([0x12, 0x34]), 8),
        (CanAddressingFormat.NORMAL_ADDRESSING, range(58), 0xF, 0x98765434, 0x76, 0x65, bytearray(),
         bytearray([0x10, 0x00, 0xFE, 0xDC, 0xBA, 0x98]), 63),
    ])
    @patch(f"{SCRIPT_LOCATION}.encode_ff_dl")
    def test_create_first_frame_data__inconsistent(self, mock_encode_ff_dl,
                                                   addressing_format, payload, dlc, data_length, target_address,
                                                   address_extension,
                                                   ai_data_bytes, ff_dl_data_bytes, frame_data_length):
        self.mock_can_addressing_information.encode_ai_data_bytes.return_value = ai_data_bytes
        mock_encode_ff_dl.return_value = ff_dl_data_bytes
        self.mock_dlc_handler.decode_dlc.return_value = frame_data_length
        with pytest.raises(InconsistentArgumentsError):
            create_first_frame_data(addressing_format=addressing_format,
                                    payload=payload,
                                    dlc=dlc,
                                    data_length=data_length,
                                    target_address=target_address,
                                    address_extension=address_extension)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=False)
        self.mock_can_addressing_information.encode_ai_data_bytes.assert_called_once_with(
            addressing_format=addressing_format,
            target_address=target_address,
            address_extension=address_extension)
        mock_encode_ff_dl.assert_called_once_with(addressing_format=addressing_format, dlc=dlc, ff_dl=data_length)
        self.mock_dlc_handler.decode_dlc.assert_called_once_with(dlc)
        
    # generate_first_frame_data

    @pytest.mark.parametrize("addressing_format, payload, dlc, ff_dl, long_ff_dl_format, target_address, "
                             "address_extension, ai_data_bytes, ff_dl_data_bytes", [
        (Mock(), [0x12, 0x34, 0x56, 0x78], 8, 13, True, Mock(), Mock(), bytearray([0x23]), bytearray([0x12, 0x34])),
        (CanAddressingFormat.NORMAL_ADDRESSING, range(58), 0xF, 0x98765434, False, 0x76, 0x65, bytearray(),
         bytearray([0x10, 0x00, 0xFE, 0xDC, 0xBA, 0x98])),
    ])
    @patch(f"{SCRIPT_LOCATION}.generate_ff_dl_bytes")
    def test_generate_first_frame_data__valid(self, mock_generate_ff_dl_bytes,
                                              addressing_format, payload, dlc, ff_dl, long_ff_dl_format,
                                              target_address, address_extension,
                                              ai_data_bytes, ff_dl_data_bytes):
        expected_output = ai_data_bytes + ff_dl_data_bytes + bytearray(payload)
        self.mock_can_addressing_information.encode_ai_data_bytes.return_value = ai_data_bytes
        mock_generate_ff_dl_bytes.return_value = ff_dl_data_bytes
        self.mock_dlc_handler.decode_dlc.return_value = len(expected_output)
        assert generate_first_frame_data(addressing_format=addressing_format,
                                         payload=payload,
                                         dlc=dlc,
                                         ff_dl=ff_dl,
                                         long_ff_dl_format=long_ff_dl_format,
                                         target_address=target_address,
                                         address_extension=address_extension) == expected_output
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=True)
        self.mock_can_addressing_information.encode_ai_data_bytes.assert_called_once_with(
            addressing_format=addressing_format,
            target_address=target_address,
            address_extension=address_extension)
        mock_generate_ff_dl_bytes.assert_called_once_with(ff_dl=ff_dl, long_ff_dl_format=long_ff_dl_format)
        self.mock_dlc_handler.decode_dlc.assert_called_once_with(dlc)

    @pytest.mark.parametrize("addressing_format, payload, dlc, ff_dl, long_ff_dl_format, target_address, "
                             "address_extension, ai_data_bytes, ff_dl_data_bytes, data_length", [
        (Mock(), [0x12, 0x34, 0x56, 0x78], 8, 13, False, Mock(), Mock(), bytearray([0x23]), bytearray([0x12, 0x34]), 8),
        (CanAddressingFormat.NORMAL_ADDRESSING, range(58), 0xF, 0x98765434, True, 0x76, 0x65, bytearray(),
         bytearray([0x10, 0x00, 0xFE, 0xDC, 0xBA, 0x98]), 63),
    ])
    @patch(f"{SCRIPT_LOCATION}.generate_ff_dl_bytes")
    def test_generate_first_frame_data__inconsistent(self, mock_generate_ff_dl_bytes,
                                                     addressing_format, payload, dlc, ff_dl, long_ff_dl_format,
                                                     target_address, address_extension,
                                                     ai_data_bytes, ff_dl_data_bytes, data_length):
        self.mock_can_addressing_information.encode_ai_data_bytes.return_value = ai_data_bytes
        mock_generate_ff_dl_bytes.return_value = ff_dl_data_bytes
        self.mock_dlc_handler.decode_dlc.return_value = data_length
        with pytest.raises(InconsistentArgumentsError):
            generate_first_frame_data(addressing_format=addressing_format,
                                      payload=payload,
                                      dlc=dlc,
                                      ff_dl=ff_dl,
                                      long_ff_dl_format=long_ff_dl_format,
                                      target_address=target_address,
                                      address_extension=address_extension)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=True)
        self.mock_can_addressing_information.encode_ai_data_bytes.assert_called_once_with(
            addressing_format=addressing_format,
            target_address=target_address,
            address_extension=address_extension)
        mock_generate_ff_dl_bytes.assert_called_once_with(ff_dl=ff_dl, long_ff_dl_format=long_ff_dl_format)
        self.mock_dlc_handler.decode_dlc.assert_called_once_with(dlc)

    # extract_first_frame_payload

    @pytest.mark.parametrize("addressing_format, raw_frame_data, ai_bytes_number, ff_dl_data_bytes_number", [
        (Mock(), range(64), 1, SHORT_FF_DL_BYTES_USED),
        (CanAddressingFormat.NORMAL_ADDRESSING, [0x1F, 0x2E, 0x3D, 0x4C, 0x5B, 0x6A, 0x79, 0x80], 0,
         LONG_FF_DL_BYTES_USED),
    ])
    @patch(f"{SCRIPT_LOCATION}.extract_ff_dl_data_bytes")
    def test_extract_first_frame_payload(self, mock_extract_ff_dl_data_bytes,
                                        addressing_format, raw_frame_data,
                                        ai_bytes_number, ff_dl_data_bytes_number):
        self.mock_can_addressing_information.get_ai_data_bytes_number.return_value = ai_bytes_number
        mock_extract_ff_dl_data_bytes.return_value.__len__.return_value = ff_dl_data_bytes_number
        assert (extract_first_frame_payload(addressing_format=addressing_format,
                                            raw_frame_data=raw_frame_data)
                == bytearray(raw_frame_data)[ai_bytes_number + ff_dl_data_bytes_number:])
        self.mock_can_addressing_information.get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        mock_extract_ff_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)

    # extract_ff_dl

    @pytest.mark.parametrize("addressing_format, raw_frame_data, ff_dl_data_bytes, expected_output", [
        (Mock(), Mock(), [0x12, 0x34], 0x234),
        (CanAddressingFormat.NORMAL_ADDRESSING, list(range(64)), [0x10, 0xF0], 0x0F0),
        (CanAddressingFormat.EXTENDED_ADDRESSING, list(range(8)), [0x10, 0x00, 0xFE, 0xDC, 0xBA, 0x98], 0xFEDCBA98),
        (Mock(), Mock(), [0x10, 0x00, 0x00, 0x00, 0x23, 0xBD], 0x000023BD),
    ])
    @patch(f"{SCRIPT_LOCATION}.extract_ff_dl_data_bytes")
    def test_extract_ff_dl__valid(self, mock_extract_ff_dl_data_bytes,
                                 addressing_format, raw_frame_data, ff_dl_data_bytes, expected_output):
        mock_extract_ff_dl_data_bytes.return_value = ff_dl_data_bytes
        assert extract_ff_dl(addressing_format=addressing_format, raw_frame_data=raw_frame_data) == expected_output
        mock_extract_ff_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)

    @pytest.mark.parametrize("addressing_format, raw_frame_data, ff_dl_data_bytes", [
        (Mock(), Mock(), [0x12]),
        (CanAddressingFormat.EXTENDED_ADDRESSING, list(range(8)), [0x10, 0x00, 0x00, 0x23, 0xBD]),
    ])
    @patch(f"{SCRIPT_LOCATION}.extract_ff_dl_data_bytes")
    def test_extract_ff_dl__not_implemented(self, mock_extract_ff_dl_data_bytes,
                                   addressing_format, raw_frame_data, ff_dl_data_bytes):
        mock_extract_ff_dl_data_bytes.return_value = ff_dl_data_bytes
        with pytest.raises(NotImplementedError):
            extract_ff_dl(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
        mock_extract_ff_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)

    # extract_ff_dl_data_bytes

    @pytest.mark.parametrize("addressing_format, raw_frame_data, ai_data_bytes_number, expected_output", [
        (Mock(), [0x10, 0x01, 0xFF, 0xAB, 0xCD], 0, bytearray([0x10, 0x01])),
        (Mock(), (0x10, 0x10, 0x01, 0xFF, 0xAB, 0xCD), 1, bytearray([0x10, 0x01])),
        (Mock(), [0x10, 0x00, 0x01, 0xFF, 0xAB, 0xCD, 0xFF, 0xFF], 0, bytearray([0x10, 0x00, 0x01, 0xFF, 0xAB, 0xCD])),
        (Mock(), [0x00, 0x10, 0x00, 0x01, 0xFF, 0xAB, 0xCD, 0xFF], 1, bytearray([0x10, 0x00, 0x01, 0xFF, 0xAB, 0xCD])),
    ])
    def test_extract_ff_dl_data_bytes(self, addressing_format, raw_frame_data, ai_data_bytes_number, expected_output):
        self.mock_can_addressing_information.get_ai_data_bytes_number.return_value = ai_data_bytes_number
        assert (extract_ff_dl_data_bytes(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
                == expected_output)
        self.mock_can_addressing_information.get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    # encode_ff_dl

    @pytest.mark.parametrize("addressing_format, dlc, ff_dl", [
        (Mock(), Mock(), MAX_SHORT_FF_DL_VALUE),
        (Mock(), Mock(), MAX_SHORT_FF_DL_VALUE + 1),
    ])
    @patch(f"{SCRIPT_LOCATION}.generate_ff_dl_bytes")
    @patch(f"{SCRIPT_LOCATION}.validate_ff_dl")
    def test_encode_valid_ff_dl(self, mock_validate_ff_dl, mock_generate_ff_dl_bytes,
                                addressing_format, dlc, ff_dl):
        assert encode_ff_dl(addressing_format=addressing_format,
                            dlc=dlc,
                            ff_dl=ff_dl) == mock_generate_ff_dl_bytes.return_value
        mock_validate_ff_dl.assert_called_once_with(addressing_format=addressing_format,
                                                    dlc=dlc,
                                                    ff_dl=ff_dl)
        if ff_dl > MAX_SHORT_FF_DL_VALUE:
            mock_generate_ff_dl_bytes.assert_called_once_with(ff_dl=ff_dl, long_ff_dl_format=True)
        else:
            mock_generate_ff_dl_bytes.assert_called_once_with(ff_dl=ff_dl, long_ff_dl_format=False)

    # get_first_frame_payload_size

    @pytest.mark.parametrize("addressing_format, dlc, long_ff_dl_format", [
        (Mock(), CanDlcHandler.MIN_BASE_UDS_DLC - 1, False),
        (Mock(), 0, True),
    ])
    def test_get_first_frame_payload_size__value_error(self, addressing_format, dlc, long_ff_dl_format):
        with pytest.raises(ValueError):
            get_first_frame_payload_size(addressing_format=addressing_format,
                                         dlc=dlc,
                                         long_ff_dl_format=long_ff_dl_format)

    @pytest.mark.parametrize("addressing_format, dlc, long_ff_dl_format, data_bytes_number, ai_data_bytes_number", [
        (Mock(), CanDlcHandler.MIN_BASE_UDS_DLC, False, 8, 0),
        (CanAddressingFormat.NORMAL_ADDRESSING, CanDlcHandler.MIN_BASE_UDS_DLC + 1, False, 12, 1),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, CanDlcHandler.MIN_BASE_UDS_DLC, True, 8, 1),
        (CanAddressingFormat.EXTENDED_ADDRESSING, CanDlcHandler.MAX_DLC_VALUE, True, 64, 0),
    ])
    def test_get_first_frame_payload_size__valid(self, addressing_format, dlc, long_ff_dl_format,
                                     data_bytes_number, ai_data_bytes_number):
        self.mock_dlc_handler.decode_dlc.return_value = data_bytes_number
        self.mock_can_addressing_information.get_ai_data_bytes_number.return_value = ai_data_bytes_number
        if long_ff_dl_format:
            expected_output = data_bytes_number - ai_data_bytes_number - LONG_FF_DL_BYTES_USED
        else:
            expected_output = data_bytes_number - ai_data_bytes_number - SHORT_FF_DL_BYTES_USED
        assert get_first_frame_payload_size(addressing_format=addressing_format,
                                            dlc=dlc,
                                            long_ff_dl_format=long_ff_dl_format) == expected_output
        self.mock_dlc_handler.decode_dlc.assert_called_once_with(dlc)
        self.mock_can_addressing_information.get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    # generate_ff_dl_bytes

    @pytest.mark.parametrize("ff_dl, long_ff_dl_format, expected_ff_dl_bytes", [
        (MAX_SHORT_FF_DL_VALUE + 1, False, bytearray([0x10, 0x00])),
        (MAX_LONG_FF_DL_VALUE + 1, True, bytearray([0x10, 0x00, 0x00, 0x00, 0x00, 0x00])),
        (MAX_LONG_FF_DL_VALUE, False, bytearray([0x1F, 0x4A])),
        (MAX_LONG_FF_DL_VALUE + MAX_SHORT_FF_DL_VALUE, True, bytearray([0x10, 0x00, 0x9B, 0xE0, 0x87, 0x21])),
    ])
    def test_generate_ff_dl_bytes__value_error(self, ff_dl, long_ff_dl_format, expected_ff_dl_bytes):
        with pytest.raises(ValueError):
            generate_ff_dl_bytes(long_ff_dl_format=long_ff_dl_format, ff_dl=ff_dl)

    @pytest.mark.parametrize("ff_dl, long_ff_dl_format, expected_ff_dl_bytes", [
        (0x0, False, bytearray([0x10, 0x00])),
        (0x0, True, bytearray([0x10, 0x00, 0x00, 0x00, 0x00, 0x00])),
        (0xF4A, False, bytearray([0x1F, 0x4A])),
        (0x9BE08721, True, bytearray([0x10, 0x00, 0x9B, 0xE0, 0x87, 0x21])),
    ])
    def test_generate_ff_dl_bytes__valid(self, ff_dl, long_ff_dl_format, expected_ff_dl_bytes):
        assert generate_ff_dl_bytes(long_ff_dl_format=long_ff_dl_format, ff_dl=ff_dl) == expected_ff_dl_bytes

    # validate_ff_dl

    @pytest.mark.parametrize("ff_dl", [Mock(), 654])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_validate_ff_dl__type_error(self, mock_isinstance, ff_dl):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            validate_ff_dl(ff_dl=ff_dl)
        mock_isinstance.assert_called_once_with(ff_dl, int)

    @pytest.mark.parametrize("ff_dl", [-1, MAX_LONG_FF_DL_VALUE +1])
    def test_validate_ff_dl__value_error(self, ff_dl):
        with pytest.raises(ValueError):
            validate_ff_dl(ff_dl=ff_dl)

    @pytest.mark.parametrize("ff_dl, dlc, addressing_format", [
        (MAX_LONG_FF_DL_VALUE, CanDlcHandler.MIN_BASE_UDS_DLC - 1, CanAddressingFormat.NORMAL_ADDRESSING),
        (MAX_SHORT_FF_DL_VALUE, CanDlcHandler.MIN_BASE_UDS_DLC - 2, CanAddressingFormat.EXTENDED_ADDRESSING),
    ])
    def test_validate_ff_dl__value_error__dlc(self, ff_dl, dlc, addressing_format):
        with pytest.raises(ValueError):
            validate_ff_dl(ff_dl=ff_dl, dlc=dlc, addressing_format=addressing_format)

    @pytest.mark.parametrize("ff_dl, ff_dl_bytes_number", [
        (MAX_SHORT_FF_DL_VALUE-1, 0),
        (MAX_SHORT_FF_DL_VALUE, SHORT_FF_DL_BYTES_USED -1),
        (MAX_LONG_FF_DL_VALUE, LONG_FF_DL_BYTES_USED +1),
        (MAX_LONG_FF_DL_VALUE, Mock()),
    ])
    def test_validate_ff_dl__value_error__ff_dl_bytes_number(self, ff_dl, ff_dl_bytes_number):
        with pytest.raises(ValueError):
            validate_ff_dl(ff_dl=ff_dl, ff_dl_bytes_number=ff_dl_bytes_number)

    @pytest.mark.parametrize("ff_dl, dlc, addressing_format, sf_dl", [
        (5, CanDlcHandler.MIN_BASE_UDS_DLC, Mock(), 5),
        (50, CanDlcHandler.MIN_BASE_UDS_DLC+1, CanAddressingFormat.EXTENDED_ADDRESSING, 61),
    ])
    def test_validate_ff_dl__inconsistent_sf(self, ff_dl, dlc, addressing_format, sf_dl):
        self.mock_get_max_sf_dl.return_value = sf_dl
        with pytest.raises(InconsistentArgumentsError):
            validate_ff_dl(ff_dl=ff_dl, dlc=dlc, addressing_format=addressing_format)
        self.mock_get_max_sf_dl.assert_called_once_with(dlc=dlc, addressing_format=addressing_format)

    @pytest.mark.parametrize("ff_dl, dlc, addressing_format, ff_dl_bytes_number", [
        (MAX_SHORT_FF_DL_VALUE+1, CanDlcHandler.MIN_BASE_UDS_DLC, Mock(), SHORT_FF_DL_BYTES_USED),
        (MAX_SHORT_FF_DL_VALUE, CanDlcHandler.MIN_BASE_UDS_DLC+1, CanAddressingFormat.EXTENDED_ADDRESSING,
         LONG_FF_DL_BYTES_USED),
    ])
    def test_validate_ff_dl__inconsistent_format(self, ff_dl, dlc, addressing_format, ff_dl_bytes_number):
        self.mock_get_max_sf_dl.return_value = 0
        with pytest.raises(InconsistentArgumentsError):
            validate_ff_dl(ff_dl=ff_dl,
                           dlc=dlc,
                           addressing_format=addressing_format,
                           ff_dl_bytes_number=ff_dl_bytes_number)
        self.mock_get_max_sf_dl.assert_called_once_with(dlc=dlc, addressing_format=addressing_format)

    @pytest.mark.parametrize("ff_dl, dlc, addressing_format, ff_dl_bytes_number", [
        (5, CanDlcHandler.MIN_BASE_UDS_DLC, Mock(), SHORT_FF_DL_BYTES_USED),
        (MAX_SHORT_FF_DL_VALUE, CanDlcHandler.MIN_BASE_UDS_DLC + 1, Mock(), SHORT_FF_DL_BYTES_USED),
        (MAX_SHORT_FF_DL_VALUE+1, CanDlcHandler.MIN_BASE_UDS_DLC + 2, CanAddressingFormat.EXTENDED_ADDRESSING,
         LONG_FF_DL_BYTES_USED),
        (MAX_LONG_FF_DL_VALUE, CanDlcHandler.MAX_DLC_VALUE, CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         LONG_FF_DL_BYTES_USED),
    ])
    def test_validate_ff_dl__valid(self, ff_dl, dlc, addressing_format, ff_dl_bytes_number):
        self.mock_get_max_sf_dl.return_value = 0
        assert validate_ff_dl(ff_dl=ff_dl,
                              dlc=dlc,
                              addressing_format=addressing_format,
                              ff_dl_bytes_number=ff_dl_bytes_number) is None
        self.mock_get_max_sf_dl.assert_called_once_with(dlc=dlc, addressing_format=addressing_format)


@pytest.mark.integration
class TestCanFirstFrameIntegration:
    """Integration tests for CAN First Frame module."""

    # validate_first_frame_data

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        (CanAddressingFormat.NORMAL_ADDRESSING, (0x10, 0x08, 0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54)),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, [0x10, 0x00, 0x00, 0x00, 0x10, 0x00] + list(range(58))),
        (CanAddressingFormat.EXTENDED_ADDRESSING, [0x10, 0x1F, 0xFF] + list(range(100, 121))),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, (0x0F, 0x10, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF)),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, [0x0F, 0x10, 0x3E] + list(range(50, 111))),
    ])
    def test_validate_first_frame_data(self, addressing_format, raw_frame_data):
        assert validate_first_frame_data(addressing_format=addressing_format,
                                         raw_frame_data=raw_frame_data) is None

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        (CanAddressingFormat.NORMAL_ADDRESSING, (0x10, 0x07, 0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54)),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, [0x10, 0x00, 0x00, 0x00, 0x0F, 0xFF] + list(range(58))),
        (CanAddressingFormat.EXTENDED_ADDRESSING, [0x10, 0x10, 0x15] + list(range(100, 121))),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, (0x0F, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, [0x0F, 0x10, 0x3D] + list(range(50, 111))),
    ])
    def test_validate_first_frame_data__value_error(self, addressing_format, raw_frame_data):
        with pytest.raises(ValueError):
            validate_first_frame_data(addressing_format=addressing_format,
                                      raw_frame_data=raw_frame_data)

    # create_first_frame_data

    @pytest.mark.parametrize("kwargs, expected_raw_frame_data", [
        ({"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
          "dlc": 8,
          "data_length": 0xFED,
          "payload": [0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC]}, bytearray([0x1F, 0xED, 0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC])),
        ({"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "dlc": 9,
          "data_length": 0xFFFFFFFF,
          "payload": b"\xF0\xE1\xD2\xC3\xB4\xA5",
          "target_address": 0xC0}, bytearray([0x10, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5])),
        ({"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "dlc": 0xF,
          "data_length": 62,
          "payload": tuple(range(120, 181)),
          "target_address": 0xC0}, bytearray([0xC0, 0x10, 0x3E] + list(range(120, 181)))),
        ({"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
          "dlc": 0xA,
          "data_length": 0x1000,
          "payload": list(range(9)),
          "address_extension": 0x0B}, bytearray([0x0B, 0x10, 0x00, 0x00, 0x00, 0x10, 0x00] + list(range(9)))),
        ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "dlc": 8,
          "data_length": 0xFFF,
          "payload": bytearray([0x9A, 0x8B, 0x7C, 0x6D, 0x5E]),
          "target_address": 0x9E,
          "address_extension": 0x61}, bytearray([0x61, 0x1F, 0xFF, 0x9A, 0x8B, 0x7C, 0x6D, 0x5E])),
    ])
    def test_create_first_frame_data(self, kwargs, expected_raw_frame_data):
        assert create_first_frame_data(**kwargs) == expected_raw_frame_data

    @pytest.mark.parametrize("kwargs", [
        {"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
         "dlc": 7,
         "data_length": 0xFED,
         "payload": [0x12, 0x34, 0x56, 0x78, 0x9A]},
        {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         "dlc": 9,
         "data_length": 0x12345678,
         "payload": [0xF0, 0xE1, 0xD2, 0xC3, 0xB4],
         "target_address": 0xC0},
        {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
         "dlc": 0xF,
         "data_length": 61,
         "payload": tuple(range(120, 181)),
         "target_address": 0xC0},
        {"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         "dlc": 0xA,
         "data_length": 0x100000000,
         "payload": list(range(9)),
         "address_extension": 0x0B},
        {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         "dlc": 8,
         "data_length": 0x6,
         "payload": [0x9A, 0x8B, 0x7C, 0x6D, 0x5E],
         "target_address": 0x9E,
         "address_extension": 0x61}
    ])
    def test_create_first_frame_data__value_error(self, kwargs):
        with pytest.raises(ValueError):
            create_first_frame_data(**kwargs)

    # generate_first_frame_data

    @pytest.mark.parametrize("kwargs, expected_raw_frame_data", [
        ({"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
          "dlc": 7,
          "ff_dl": 0xFED,
          "long_ff_dl_format": False,
          "payload": [0x12, 0x34, 0x56, 0x78, 0x9A]}, bytearray([0x1F, 0xED, 0x12, 0x34, 0x56, 0x78, 0x9A])),
        ({"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "dlc": 8,
          "ff_dl": 0xFED,
          "long_ff_dl_format": True,
          "payload": [0x78, 0x9A],
          "target_address": 0xC0}, bytearray([0x10, 0x00, 0x00, 0x00, 0x0F, 0xED, 0x78, 0x9A])),
        ({"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "dlc": 0xF,
          "ff_dl": 61,
          "long_ff_dl_format": False,
          "payload": tuple(range(120, 181)),
          "target_address": 0xC0}, bytearray([0xC0, 0x10, 0x3D]) + bytearray(range(120, 181))),
        ({"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
          "dlc": 0xA,
          "ff_dl": 0,
          "long_ff_dl_format": True,
          "payload": list(range(100, 109)),
          "address_extension": 0x0B}, bytearray([0x0B, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00]) + bytearray(range(100, 109))),
        ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "dlc": 8,
          "ff_dl": 0x4,
          "long_ff_dl_format": False,
          "payload": [0x9A, 0x8B, 0x7C, 0x6D, 0x5E],
          "target_address": 0x9E,
          "address_extension": 0x61}, bytearray([0x61, 0x10, 0x04, 0x9A, 0x8B, 0x7C, 0x6D, 0x5E]))
    ])
    def test_generate_first_frame_data(self, kwargs, expected_raw_frame_data):
        assert generate_first_frame_data(**kwargs) == expected_raw_frame_data

    @pytest.mark.parametrize("kwargs", [
        {"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
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
    def test_generate_first_frame_data__value_error(self, kwargs):
        with pytest.raises(ValueError):
            generate_first_frame_data(**kwargs)

    # extract_first_frame_payload

    @pytest.mark.parametrize("addressing_format, raw_frame_data, payload_i", [
        (CanAddressingFormat.NORMAL_ADDRESSING, (0x10, 0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE), 2),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, [0x10, 0x00, 0xF0, 0xD1, 0xE2, 0xC3] + list(range(58)), 6),
        (CanAddressingFormat.EXTENDED_ADDRESSING, [0x10, 0x10, 0xF0] + list(range(50, 96)), 3),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, [0xC4, 0x10, 0x00, 0xF0, 0xD1, 0xE2, 0xC3, 0xD4], 7),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, [0x83, 0x1F, 0xFF] + list(range(100, 121)), 3),
    ])
    def test_extract_first_frame_payload(self, addressing_format, raw_frame_data, payload_i):
        assert extract_first_frame_payload(addressing_format=addressing_format,
                                           raw_frame_data=raw_frame_data) == bytearray(raw_frame_data)[payload_i:]

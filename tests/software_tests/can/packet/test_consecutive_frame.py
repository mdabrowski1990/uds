import pytest
from mock import MagicMock, Mock, patch

from uds.can.packet.consecutive_frame import (
    CONSECUTIVE_FRAME_N_PCI,
    DEFAULT_FILLER_BYTE,
    SN_BYTES_USED,
    CanAddressingFormat,
    CanDlcHandler,
    InconsistencyError,
    create_consecutive_frame_data,
    encode_sequence_number,
    extract_consecutive_frame_payload,
    extract_sequence_number,
    generate_consecutive_frame_data,
    get_consecutive_frame_max_payload_size,
    get_consecutive_frame_min_dlc,
    is_consecutive_frame,
    validate_consecutive_frame_data,
)

SCRIPT_LOCATION = "uds.can.packet.consecutive_frame"


class TestCanConsecutiveFrame:
    """Unit tests for functions in CAN Consecutive Frame module."""

    def setup_method(self):
        self._patcher_validate_nibble = patch(f"{SCRIPT_LOCATION}.validate_nibble")
        self.mock_validate_nibble = self._patcher_validate_nibble.start()
        self._patcher_validate_raw_byte = patch(f"{SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
        self._patcher_validate_raw_bytes = patch(f"{SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
        self._patcher_can_dlc_handler = patch(f"{SCRIPT_LOCATION}.CanDlcHandler",
                                              Mock(MAX_DATA_BYTES_NUMBER=CanDlcHandler.MAX_DATA_BYTES_NUMBER,
                                                   MIN_BASE_UDS_DLC=CanDlcHandler.MIN_BASE_UDS_DLC))
        self.mock_can_dlc_handler = self._patcher_can_dlc_handler.start()
        self._patcher_can_addressing_information = patch(f"{SCRIPT_LOCATION}.CanAddressingInformation")
        self.mock_can_addressing_information = self._patcher_can_addressing_information.start()

    def teardown_method(self):
        self._patcher_validate_nibble.stop()
        self._patcher_validate_raw_byte.stop()
        self._patcher_validate_raw_bytes.stop()
        self._patcher_can_dlc_handler.stop()
        self._patcher_can_addressing_information.stop()

    # is_consecutive_frame

    @pytest.mark.parametrize("addressing_format, raw_frame_data, ai_data_bytes_number, expected_output", [
        (Mock(), [CONSECUTIVE_FRAME_N_PCI << 4, *range(100, 163)], 0, True),
        (Mock(), [(CONSECUTIVE_FRAME_N_PCI << 4) + 0xF, *range(7)], 0, True),
        (Mock(), [(CONSECUTIVE_FRAME_N_PCI << 4) + 0xF, 0xFF, 0x0F, 0x1E, 0x2D, 0x3C, 0x4B, 0x5A], 1, False),
        (CanAddressingFormat.EXTENDED_ADDRESSING, [0xFF, (CONSECUTIVE_FRAME_N_PCI << 4) + 0x5, 0xFF], 1, True),
    ])
    def test_is_consecutive_frame(self, addressing_format, raw_frame_data, ai_data_bytes_number, expected_output):
        self.mock_can_addressing_information.get_ai_data_bytes_number.return_value = ai_data_bytes_number
        assert is_consecutive_frame(addressing_format=addressing_format, raw_frame_data=raw_frame_data) is expected_output
        self.mock_can_addressing_information.get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    # validate_consecutive_frame_data

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        (Mock(), Mock()),
        (CanAddressingFormat.NORMAL_ADDRESSING, range(8)),
    ])
    @patch(f"{SCRIPT_LOCATION}.get_consecutive_frame_min_dlc")
    @patch(f"{SCRIPT_LOCATION}.is_consecutive_frame")
    def test_validate_consecutive_frame_data__value_error(self, mock_is_consecutive_frame,
                                                          mock_get_consecutive_frame_min_dlc,
                                                          addressing_format, raw_frame_data):
        mock_is_consecutive_frame.return_value = False
        with pytest.raises(ValueError):
            validate_consecutive_frame_data(addressing_format=addressing_format,
                                                           raw_frame_data=raw_frame_data)
        mock_is_consecutive_frame.assert_called_once_with(addressing_format=addressing_format,
                                                          raw_frame_data=raw_frame_data)
        mock_get_consecutive_frame_min_dlc.assert_not_called()
        self.mock_can_dlc_handler.encode_dlc.assert_not_called()

    @pytest.mark.parametrize("addressing_format, raw_frame_data, decoded_dlc, min_dlc", [
        (Mock(), MagicMock(), 4, 5),
        (CanAddressingFormat.NORMAL_ADDRESSING, range(8), 1, 2),
    ])
    @patch(f"{SCRIPT_LOCATION}.get_consecutive_frame_min_dlc")
    @patch(f"{SCRIPT_LOCATION}.is_consecutive_frame")
    def test_validate_consecutive_frame_data__inconsistent(self, mock_is_consecutive_frame,
                                                           mock_get_consecutive_frame_min_dlc,
                                                           addressing_format, raw_frame_data,
                                                           decoded_dlc, min_dlc):
        mock_is_consecutive_frame.return_value = True
        mock_get_consecutive_frame_min_dlc.return_value = min_dlc
        self.mock_can_dlc_handler.encode_dlc.return_value = decoded_dlc
        with pytest.raises(InconsistencyError):
            validate_consecutive_frame_data(addressing_format=addressing_format,
                                            raw_frame_data=raw_frame_data)
        mock_is_consecutive_frame.assert_called_once_with(addressing_format=addressing_format,
                                                          raw_frame_data=raw_frame_data)
        mock_get_consecutive_frame_min_dlc.assert_called_once_with(addressing_format)
        self.mock_can_dlc_handler.encode_dlc.assert_called_once_with(len(raw_frame_data))

    @pytest.mark.parametrize("addressing_format, raw_frame_data, decoded_dlc, min_dlc", [
        (Mock(), MagicMock(), 5, 5),
        (CanAddressingFormat.NORMAL_ADDRESSING, range(8), 1, 1),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, bytearray([0xBC, 0x2F, *range(100, 162)]), 64, 2),
    ])
    @patch(f"{SCRIPT_LOCATION}.get_consecutive_frame_min_dlc")
    @patch(f"{SCRIPT_LOCATION}.is_consecutive_frame")
    def test_validate_consecutive_frame_data__valid(self, mock_is_consecutive_frame,
                                                           mock_get_consecutive_frame_min_dlc,
                                                           addressing_format, raw_frame_data,
                                                           decoded_dlc, min_dlc):
        mock_is_consecutive_frame.return_value = True
        mock_get_consecutive_frame_min_dlc.return_value = min_dlc
        self.mock_can_dlc_handler.encode_dlc.return_value = decoded_dlc
        assert validate_consecutive_frame_data(addressing_format=addressing_format,
                                               raw_frame_data=raw_frame_data) is None
        mock_is_consecutive_frame.assert_called_once_with(addressing_format=addressing_format,
                                                          raw_frame_data=raw_frame_data)
        mock_get_consecutive_frame_min_dlc.assert_called_once_with(addressing_format)
        self.mock_can_dlc_handler.encode_dlc.assert_called_once_with(len(raw_frame_data))

    # create_consecutive_frame_data

    @pytest.mark.parametrize("addressing_format, payload, sequence_number, ai_data_bytes, sn_bytes", [
        (Mock(), [0x0F, 0x1E, 0x2D, 0x3C, 0x4B, 0x5A, 0x69, 0x78], 0, bytearray(), bytearray([0x20])),
        (Mock(), [0x5A], 0xF, bytearray([0xD0]), bytearray([0x2F])),
        (CanAddressingFormat.NORMAL_ADDRESSING, tuple(range(62)), 0x5, bytearray([0xC2]), bytearray([0xBD])),
    ])
    @patch(f"{SCRIPT_LOCATION}.get_consecutive_frame_min_dlc")
    @patch(f"{SCRIPT_LOCATION}.encode_sequence_number")
    def test_create_consecutive_frame_data__valid_mandatory_args(self, mock_encode_sequence_number,
                                                                 mock_get_consecutive_frame_min_dlc,
                                                                 addressing_format, payload, sequence_number,
                                                                 ai_data_bytes, sn_bytes):
        expected_output = ai_data_bytes + sn_bytes + bytearray(payload)
        self.mock_can_addressing_information.encode_ai_data_bytes.return_value = ai_data_bytes
        self.mock_can_dlc_handler.decode_dlc.return_value = len(expected_output)
        mock_encode_sequence_number.return_value = sn_bytes
        assert create_consecutive_frame_data(addressing_format=addressing_format,
                                             payload=payload,
                                             sequence_number=sequence_number) == expected_output
        mock_get_consecutive_frame_min_dlc.assert_called_once_with(addressing_format=addressing_format,
                                                                   payload_length=len(payload))
        self.mock_can_addressing_information.encode_ai_data_bytes.assert_called_once_with(
            addressing_format=addressing_format,
            target_address=None,
            address_extension=None)
        self.mock_can_dlc_handler.decode_dlc.assert_called_once_with(mock_get_consecutive_frame_min_dlc.return_value)

    @pytest.mark.parametrize("addressing_format, payload, sequence_number, dlc, filler_byte, target_address, "
                             "address_extension, ai_data_bytes, sn_bytes, data_bytes_number", [
        (Mock(), [0x0F, 0x1E, 0x2D, 0x3C], 0, 6, 0xAA, 0xBA, 0xC9, bytearray([0xC9]), bytearray([0x20]), 6),
        (Mock(), [0xE9], 0xF, 2, 0xAA, 0x55, 0xAA, bytearray(), bytearray([0x2F]), 2),
        (CanAddressingFormat.NORMAL_ADDRESSING, tuple(range(20)), 0x5, 0xF, 0x3C, 0x60, 0x71, bytearray([0xC2]),
         bytearray([0xBD]), 48),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, bytearray(range(100, 182, 2)), 0x7, 0xF, 0x13, Mock(), Mock(),
         bytearray([0xFE]), bytearray([0x27]), 64),
    ])
    @patch(f"{SCRIPT_LOCATION}.get_consecutive_frame_min_dlc")
    @patch(f"{SCRIPT_LOCATION}.encode_sequence_number")
    def test_create_consecutive_frame_data__valid_all_args(self, mock_encode_sequence_number,
                                                           mock_get_consecutive_frame_min_dlc,
                                                           addressing_format, payload, sequence_number, dlc,
                                                           filler_byte, target_address, address_extension,
                                                           ai_data_bytes, sn_bytes, data_bytes_number):
        self.mock_can_addressing_information.encode_ai_data_bytes.return_value = ai_data_bytes
        self.mock_can_dlc_handler.decode_dlc.return_value = data_bytes_number
        mock_encode_sequence_number.return_value = sn_bytes
        expected_output = ai_data_bytes + sn_bytes + bytearray(payload)
        while len(expected_output) < data_bytes_number:
            expected_output.append(filler_byte)
        assert create_consecutive_frame_data(addressing_format=addressing_format,
                                             payload=payload,
                                             sequence_number=sequence_number,
                                             dlc=dlc,
                                             filler_byte=filler_byte,
                                             target_address=target_address,
                                             address_extension=address_extension) == expected_output
        mock_get_consecutive_frame_min_dlc.assert_not_called()
        self.mock_can_addressing_information.encode_ai_data_bytes.assert_called_once_with(
            addressing_format=addressing_format,
            target_address=target_address,
            address_extension=address_extension)
        self.mock_can_dlc_handler.decode_dlc.assert_called_once_with(dlc)

    @pytest.mark.parametrize("addressing_format, payload, sequence_number, dlc, filler_byte, target_address, "
                             "address_extension, ai_data_bytes, sn_bytes, data_bytes_number", [
        (Mock(), [0xE9], 0xF, CanDlcHandler.MIN_BASE_UDS_DLC - 1, 0xAA, Mock(), Mock(), bytearray(), bytearray([0x2F]), 8),
        (CanAddressingFormat.NORMAL_ADDRESSING, tuple(range(63)), 0x0, 0xF, 0x3C, 0x60, 0x71, bytearray([0xC2]),
         bytearray([0xBD]), 64),
    ])
    @patch(f"{SCRIPT_LOCATION}.get_consecutive_frame_min_dlc")
    @patch(f"{SCRIPT_LOCATION}.encode_sequence_number")
    def test_create_consecutive_frame_data__inconsistent(self, mock_encode_sequence_number,
                                                           mock_get_consecutive_frame_min_dlc,
                                                           addressing_format, payload, sequence_number, dlc,
                                                           filler_byte, target_address, address_extension,
                                                           ai_data_bytes, sn_bytes, data_bytes_number):
        self.mock_can_addressing_information.encode_ai_data_bytes.return_value = ai_data_bytes
        self.mock_can_dlc_handler.decode_dlc.return_value = data_bytes_number
        mock_encode_sequence_number.return_value = sn_bytes
        with pytest.raises(InconsistencyError):
            create_consecutive_frame_data(addressing_format=addressing_format,
                                          payload=payload,
                                          sequence_number=sequence_number,
                                          dlc=dlc,
                                          filler_byte=filler_byte,
                                          target_address=target_address,
                                          address_extension=address_extension)
        mock_get_consecutive_frame_min_dlc.assert_not_called()
        self.mock_can_addressing_information.encode_ai_data_bytes.assert_called_once_with(
            addressing_format=addressing_format,
            target_address=target_address,
            address_extension=address_extension)
        self.mock_can_dlc_handler.decode_dlc.assert_called_once_with(dlc)

    # generate_consecutive_frame_data

    @pytest.mark.parametrize("addressing_format, payload, sequence_number, dlc, ai_data_bytes, sn_bytes, "
                             "data_bytes_number", [
        (Mock(), [0x0F, 0x1E, 0x2D, 0x3C, 0x4B, 0x5A, 0x69, 0x78], 5, CanDlcHandler.MIN_BASE_UDS_DLC - 1, bytearray(),
         bytearray([0x20]), 12),
        (Mock(), [], 0x0, 1, bytearray(), bytearray([0x2F]), 1),
        (CanAddressingFormat.NORMAL_ADDRESSING, (0xF5, 0x6E), 0xF, CanDlcHandler.MIN_BASE_UDS_DLC - 2,
         bytearray([0xC2]), bytearray([0x2D]), 6),
    ])
    @patch(f"{SCRIPT_LOCATION}.encode_sequence_number")
    def test_generate_consecutive_frame_data__valid_mandatory_args(self, mock_encode_sequence_number,
                                                                 addressing_format, payload, sequence_number, dlc,
                                                                 ai_data_bytes, sn_bytes, data_bytes_number):

        self.mock_can_addressing_information.encode_ai_data_bytes.return_value = ai_data_bytes
        self.mock_can_dlc_handler.decode_dlc.return_value = data_bytes_number
        mock_encode_sequence_number.return_value = sn_bytes
        expected_output = ai_data_bytes + sn_bytes + bytearray(payload)
        while len(expected_output) < data_bytes_number:
            expected_output.append(DEFAULT_FILLER_BYTE)
        assert generate_consecutive_frame_data(addressing_format=addressing_format,
                                               payload=payload,
                                               sequence_number=sequence_number,
                                               dlc=dlc) == expected_output
        self.mock_can_addressing_information.encode_ai_data_bytes.assert_called_once_with(
            addressing_format=addressing_format,
            target_address=None,
            address_extension=None)
        self.mock_can_dlc_handler.decode_dlc.assert_called_once_with(dlc)

    @pytest.mark.parametrize("addressing_format, payload, sequence_number, dlc, filler_byte, target_address, "
                             "address_extension, ai_data_bytes, sn_bytes, data_bytes_number", [
        (Mock(), [0x0F, 0x1E, 0x2D, 0x3C, 0x4B, 0x5A, 0x69, 0x78], 5, CanDlcHandler.MIN_BASE_UDS_DLC - 1, 0x5A,
         Mock(), Mock(), bytearray(), bytearray([0x20]), 12),
        (Mock(), [], 0x0, 1, 0xFF, 0x21, 0x31, bytearray(), bytearray([0x2F]), 1),
        (CanAddressingFormat.NORMAL_ADDRESSING, (0xF5, 0x6E), 0xF, CanDlcHandler.MIN_BASE_UDS_DLC - 2, 0xC3, 0xD2, 0x2D,
         bytearray([0xC2]), bytearray([0x2D]), 6),
    ])
    @patch(f"{SCRIPT_LOCATION}.encode_sequence_number")
    def test_generate_consecutive_frame_data__valid_all_args(self, mock_encode_sequence_number,
                                                             addressing_format, payload, sequence_number, dlc,
                                                             filler_byte, target_address, address_extension,
                                                             ai_data_bytes, sn_bytes, data_bytes_number):

        self.mock_can_addressing_information.encode_ai_data_bytes.return_value = ai_data_bytes
        self.mock_can_dlc_handler.decode_dlc.return_value = data_bytes_number
        mock_encode_sequence_number.return_value = sn_bytes
        expected_output = ai_data_bytes + sn_bytes + bytearray(payload)
        while len(expected_output) < data_bytes_number:
            expected_output.append(filler_byte)
        assert generate_consecutive_frame_data(addressing_format=addressing_format,
                                               payload=payload,
                                               sequence_number=sequence_number,
                                               dlc=dlc,
                                               filler_byte=filler_byte,
                                               target_address=target_address,
                                               address_extension=address_extension) == expected_output
        self.mock_can_addressing_information.encode_ai_data_bytes.assert_called_once_with(
            addressing_format=addressing_format,
            target_address=target_address,
            address_extension=address_extension)
        self.mock_can_dlc_handler.decode_dlc.assert_called_once_with(dlc)

    @pytest.mark.parametrize("addressing_format, payload, sequence_number, dlc, filler_byte, target_address, "
                             "address_extension, ai_data_bytes, sn_bytes, data_bytes_number", [
        (Mock(), [0x0F, 0x1E, 0x2D, 0x3C, 0x4B, 0x5A, 0x69, 0x78], 5, CanDlcHandler.MIN_BASE_UDS_DLC - 1, 0x5A,
         Mock(), Mock(), bytearray(), bytearray([0x20]), 8),
        (Mock(), [], 0x0, 1, 0xFF, 0x21, 0x31, bytearray(), bytearray([0x2F]), 0),
        (CanAddressingFormat.NORMAL_ADDRESSING, (0xF5, 0x6E), 0xF, CanDlcHandler.MIN_BASE_UDS_DLC - 2, 0xC3, 0xD2, 0x2D,
         bytearray([0xC2]), bytearray([0x2D]), 2),
    ])
    @patch(f"{SCRIPT_LOCATION}.encode_sequence_number")
    def test_generate_consecutive_frame_data__inconsistent(self, mock_encode_sequence_number,
                                                             addressing_format, payload, sequence_number, dlc,
                                                             filler_byte, target_address, address_extension,
                                                             ai_data_bytes, sn_bytes, data_bytes_number):
        self.mock_can_addressing_information.encode_ai_data_bytes.return_value = ai_data_bytes
        self.mock_can_dlc_handler.decode_dlc.return_value = data_bytes_number
        mock_encode_sequence_number.return_value = sn_bytes
        with pytest.raises(InconsistencyError):
            generate_consecutive_frame_data(addressing_format=addressing_format,
                                            payload=payload,
                                            sequence_number=sequence_number,
                                            dlc=dlc,
                                            filler_byte=filler_byte,
                                            target_address=target_address,
                                            address_extension=address_extension)
        self.mock_can_addressing_information.encode_ai_data_bytes.assert_called_once_with(
            addressing_format=addressing_format,
            target_address=target_address,
            address_extension=address_extension)
        self.mock_can_dlc_handler.decode_dlc.assert_called_once_with(dlc)

    # extract_consecutive_frame_payload

    @pytest.mark.parametrize("addressing_format, raw_frame_data, ai_bytes_number", [
        (Mock(), [0x2F, *range(63)], 0),
        (Mock(), bytearray([0xFF, 0x20, 0x0F, 0x1E, 0x2D, 0x3C, 0x4B, 0x5A, 0x69, 0x78, 0x87, 0x96, 0xA5, 0xB4]), 1),
    ])
    def test_extract_consecutive_frame_payload(self, addressing_format, raw_frame_data,
                                              ai_bytes_number):
        self.mock_can_addressing_information.get_ai_data_bytes_number.return_value = ai_bytes_number
        assert (extract_consecutive_frame_payload(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
                == bytearray(raw_frame_data)[ai_bytes_number+SN_BYTES_USED:])
        self.mock_can_addressing_information.get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    # get_consecutive_frame_min_dlc

    @pytest.mark.parametrize("addressing_format, payload_length, ai_data_bytes_number", [
        (Mock(), 1, 1),
        (Mock(), 1, 0),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, 62, 1),
        (CanAddressingFormat.NORMAL_ADDRESSING, 63, 0),
    ])
    def test_get_min_consecutive_frame_dlc__valid(self, addressing_format, payload_length, ai_data_bytes_number):
        self.mock_can_addressing_information.get_ai_data_bytes_number.return_value = ai_data_bytes_number
        assert (get_consecutive_frame_min_dlc(addressing_format=addressing_format, payload_length=payload_length)
                == self.mock_can_dlc_handler.get_min_dlc.return_value)
        self.mock_can_addressing_information.get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        self.mock_can_dlc_handler.get_min_dlc.assert_called_once_with(
            ai_data_bytes_number + SN_BYTES_USED + payload_length)

    @pytest.mark.parametrize("addressing_format, payload_length", [
        (Mock(), Mock()),
        (CanAddressingFormat.NORMAL_ADDRESSING, 63),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_get_min_consecutive_frame_dlc__type_error(self, mock_isinstance,
                                                       addressing_format, payload_length):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            get_consecutive_frame_min_dlc(addressing_format=addressing_format, payload_length=payload_length)
        mock_isinstance.assert_called_once_with(payload_length, int)
        self.mock_can_addressing_information.get_ai_data_bytes_number.assert_not_called()
        self.mock_can_dlc_handler.get_min_dlc.assert_not_called()

    @pytest.mark.parametrize("addressing_format, payload_length, ai_data_bytes_number", [
        (Mock(), 0, 1),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, 63, 1),
        (CanAddressingFormat.NORMAL_ADDRESSING, 64, 0),
    ])
    def test_get_min_consecutive_frame_dlc__value_error(self, addressing_format, payload_length, ai_data_bytes_number):
        self.mock_can_addressing_information.get_ai_data_bytes_number.return_value = ai_data_bytes_number
        with pytest.raises(ValueError):
            get_consecutive_frame_min_dlc(addressing_format=addressing_format, payload_length=payload_length)
        self.mock_can_addressing_information.get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        self.mock_can_dlc_handler.get_min_dlc.assert_not_called()

    # get_consecutive_frame_max_payload_size

    @pytest.mark.parametrize("addressing_format, dlc, ai_data_bytes_number, data_bytes_number", [
        (Mock(), Mock(), 1, 2),
        (Mock(), Mock(), 0, 0),
        (CanAddressingFormat.NORMAL_ADDRESSING, 1, 0, 1),
    ])
    def test_get_consecutive_frame_max_payload_size__inconsistent(self, addressing_format, dlc,
                                                                  ai_data_bytes_number, data_bytes_number):
        self.mock_can_dlc_handler.decode_dlc.return_value = data_bytes_number
        self.mock_can_addressing_information.get_ai_data_bytes_number.return_value = ai_data_bytes_number
        with pytest.raises(InconsistencyError):
            get_consecutive_frame_max_payload_size(addressing_format=addressing_format, dlc=dlc)
        self.mock_can_dlc_handler.decode_dlc.assert_called_once_with(dlc)
        self.mock_can_addressing_information.get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    @pytest.mark.parametrize("addressing_format, dlc, ai_data_bytes_number, data_bytes_number", [
        (Mock(), Mock(), 1, 3),
        (Mock(), Mock(), 0, 2),
        (CanAddressingFormat.NORMAL_ADDRESSING, 2, 0, 2),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, 0xF, 1, 64),
    ])
    def test_get_consecutive_frame_max_payload_size__valid_with_dlc(self, addressing_format, dlc,
                                                                    ai_data_bytes_number, data_bytes_number):
        self.mock_can_dlc_handler.decode_dlc.return_value = data_bytes_number
        self.mock_can_addressing_information.get_ai_data_bytes_number.return_value = ai_data_bytes_number
        assert get_consecutive_frame_max_payload_size(
            addressing_format=addressing_format,
            dlc=dlc) == data_bytes_number - ai_data_bytes_number - SN_BYTES_USED
        self.mock_can_dlc_handler.decode_dlc.assert_called_once_with(dlc)
        self.mock_can_addressing_information.get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    @pytest.mark.parametrize("addressing_format, ai_data_bytes_number", [
        (Mock(), 0),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, 1),
    ])
    def test_get_consecutive_frame_max_payload_size__valid_without_dlc(self, addressing_format,
                                                                       ai_data_bytes_number):
        self.mock_can_addressing_information.get_ai_data_bytes_number.return_value = ai_data_bytes_number
        assert (get_consecutive_frame_max_payload_size(addressing_format=addressing_format)
                == CanDlcHandler.MAX_DATA_BYTES_NUMBER - ai_data_bytes_number - SN_BYTES_USED)
        self.mock_can_addressing_information.get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        self.mock_can_dlc_handler.decode_dlc.assert_not_called()

    # extract_sequence_number

    @pytest.mark.parametrize("addressing_format, raw_frame_data, ai_bytes_number, expected_sn", [
        (Mock(), bytearray([0x20, 0xEF, 0xCD]), 0, 0x0),
        (Mock(), list(range(0x2A, 0x6A)), 1, 0xB),
        (CanAddressingFormat.NORMAL_ADDRESSING, (0x2F, 0xED, 0xCB, 0xA9, 0x87, 0x65, 0x43, 0x21), 0, 0xF),
    ])
    def test_extract_sequence_number(self, addressing_format, raw_frame_data,
                                    ai_bytes_number, expected_sn):
        self.mock_can_addressing_information.get_ai_data_bytes_number.return_value = ai_bytes_number
        assert extract_sequence_number(addressing_format=addressing_format,
                                       raw_frame_data=raw_frame_data) == expected_sn
        self.mock_can_addressing_information.get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    # encode_sequence_number

    @pytest.mark.parametrize("sequence_number", [0, 1, 0xF])
    def test_encode_sequence_number(self, sequence_number):
        output = encode_sequence_number(sequence_number)
        self.mock_validate_nibble.assert_called_once_with(sequence_number)
        assert isinstance(output, bytearray)
        assert len(output) == SN_BYTES_USED
        assert output[0] >> 4 == CONSECUTIVE_FRAME_N_PCI
        assert output[0] & 0xF == sequence_number


@pytest.mark.integration
class TestCanConsecutiveFrameIntegration:
    """Integration tests for CAN Consecutive Frame module."""

    # validate_consecutive_frame_data

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        (CanAddressingFormat.NORMAL_ADDRESSING, (0x20, 0x12, 0x34, 0x45, 0x67, 0x89, 0x9A, 0xBC)),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, (0x2F, 0x2F)),
        (CanAddressingFormat.EXTENDED_ADDRESSING, (0xF0, 0x26, 0x00)),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, [0x30, 0x21] + (46 * [0xFF])),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, (0x8B, 0x2E, 0x9B)),
    ])
    def test_validate_frame_data(self, addressing_format, raw_frame_data):
        assert validate_consecutive_frame_data(addressing_format=addressing_format,
                                               raw_frame_data=raw_frame_data) is None

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        (CanAddressingFormat.NORMAL_ADDRESSING, [0x20]),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, tuple([0x2F] + ([0xFF] * 64))),
        (CanAddressingFormat.EXTENDED_ADDRESSING, [0x2F, 0x30, 0x54]),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, (0x8B, 0x2E)),
    ])
    def test_validate_frame_data__value_error(self, addressing_format, raw_frame_data):
        with pytest.raises(ValueError):
            validate_consecutive_frame_data(addressing_format=addressing_format,
                                            raw_frame_data=raw_frame_data)

    # create_consecutive_frame_data

    @pytest.mark.parametrize("kwargs, expected_raw_frame_data", [
        ({"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
          "payload": b"\x9A",
          "sequence_number": 0}, bytearray([0x20, 0x9A])),
        ({"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "payload": bytes(range(48)),
          "sequence_number": 0xF}, bytearray([0x2F, *range(48)] + (15 * [DEFAULT_FILLER_BYTE]))),
        ({"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "target_address": 0xF1,
          "dlc": 8,
          "payload": b"\x92\xB8",
          "sequence_number": 0x5,
          "filler_byte": 0xD9}, bytearray([0xF1, 0x25, 0x92, 0xB8, 0xD9, 0xD9, 0xD9, 0xD9])),
        ({"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
          "address_extension": 0xE8,
          "dlc": 9,
          "payload": bytes(range(10, 20)),
          "sequence_number": 0xB,
          "filler_byte": 0x99}, bytearray([0xE8, 0x2B, *range(10, 20)])),
        ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "target_address": 0xFE,
          "address_extension": 0xDC,
          "payload": bytes(range(50, 96)),
          "sequence_number": 0x1,
          "filler_byte": 0xD9}, bytearray([0xDC, 0x21, *range(50, 96)])),
    ])
    def test_create_consecutive_frame_data(self, kwargs, expected_raw_frame_data):
        assert create_consecutive_frame_data(**kwargs) == expected_raw_frame_data

    @pytest.mark.parametrize("kwargs", [
        {"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
         "payload": b"\x9A",
         "dlc": 1,
         "sequence_number": 5},
        {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         "payload": bytearray(),
         "sequence_number": 0xF},
        {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
         "target_address": 0xF1,
         "payload": b"\x9A",
         "dlc": 8,
         "sequence_number": 0x10},
        {"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         "address_extension": 0xE8,
         "payload": list(range(7)),
         "dlc": 8,
         "sequence_number": 0x0},
        {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         "target_address": 0xFE,
         "address_extension": 0xE8,
         "payload": tuple(range(50, 96)),
         "sequence_number": -1,
         "filler_byte": 0xD9}
    ])
    def test_create_consecutive_frame_data__error(self, kwargs):
        with pytest.raises((TypeError, ValueError)):
            create_consecutive_frame_data(**kwargs)

    # generate_consecutive_frame_data

    @pytest.mark.parametrize("kwargs, expected_raw_frame_data", [
        ({"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
          "payload": [],
          "dlc": 1,
          "sequence_number": 0}, bytearray([0x20])),
        ({"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "payload": (0xFE, 0xDC),
          "dlc": 5,
          "sequence_number": 0xF}, bytearray([0x2F, 0xFE, 0xDC, DEFAULT_FILLER_BYTE, DEFAULT_FILLER_BYTE])),
        ({"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "target_address": 0xF1,
          "payload": [],
          "dlc": 2,
          "sequence_number": 0xE,
          "filler_byte": 0xD9}, bytearray([0xF1, 0x2E])),
        ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "address_extension": 0xE8,
          "payload": [],
          "dlc": 2,
          "sequence_number": 0x1}, bytearray([0xE8, 0x21])),
    ])
    def test_generate_consecutive_frame_data(self, kwargs, expected_raw_frame_data):
        assert generate_consecutive_frame_data(**kwargs) == expected_raw_frame_data

    @pytest.mark.parametrize("kwargs", [
        {"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
         "payload": [0x9A],
         "dlc": 1,
         "sequence_number": 0},
        {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         "payload": [],
         "dlc": 8,
         "sequence_number": -1},
        {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
         "target_address": 0xF1,
         "payload": [0x9A],
         "dlc": 8,
         "sequence_number": 0x10},
        {"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         "address_extension": 0xE8,
         "payload": list(range(7)),
         "dlc": 8,
         "sequence_number": 0xE},
    ])
    def test_generate_consecutive_frame_data__value_error(self, kwargs):
        with pytest.raises(ValueError):
            generate_consecutive_frame_data(**kwargs)

    # extract_consecutive_frame_payload

    @pytest.mark.parametrize("addressing_format, raw_frame_data, payload", [
        (CanAddressingFormat.NORMAL_ADDRESSING, b"\x2F\x12\x34\x56\x78\x9A\xBC\xDE",
         bytearray(b"\x12\x34\x56\x78\x9A\xBC\xDE")),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, [0x20, *range(63)], bytearray(range(63))),
        (CanAddressingFormat.EXTENDED_ADDRESSING, [0x20, 0x20, *range(100, 107)], bytearray(range(100, 107))),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, [0x3F] + [0x2F] * 5, bytearray([0x2F] * 4)),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, [0x20, 0x20, 0x20], bytearray([0x20])),
    ])
    def test_extract_consecutive_frame_payload(self, addressing_format, raw_frame_data, payload):
        assert extract_consecutive_frame_payload(addressing_format=addressing_format,
                                                 raw_frame_data=raw_frame_data) == payload

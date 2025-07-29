import pytest
from mock import Mock, call, patch

from uds.can.addressing.mixed_addressing import (
    AddressingType,
    CanAddressingFormat,
    CanIdHandler,
    InconsistentArgumentsError,
    Mixed11BitCanAddressingInformation,
    Mixed29BitCanAddressingInformation,
    UnusedArgumentError,
)

SCRIPT_LOCATION = "uds.can.addressing.mixed_addressing"


class TestMixed11BitCanAddressingInformation:
    """Unit tests for `Mixed11BitCanAddressingInformation` class."""

    def setup_method(self):
        self.mock_addressing_information = Mock(spec=Mixed11BitCanAddressingInformation)
        # patching
        self._patcher_validate_raw_byte = patch(f"{SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
        self._patcher_validate_raw_bytes = patch(f"{SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
        self._patcher_validate_addressing_type = patch(f"{SCRIPT_LOCATION}.AddressingType.validate_member")
        self.mock_validate_addressing_type = self._patcher_validate_addressing_type.start()
        self._patcher_can_id_handler_class = patch(f"{SCRIPT_LOCATION}.CanIdHandler")
        self.mock_can_id_handler_class = self._patcher_can_id_handler_class.start()

    def teardown_method(self):
        self._patcher_validate_raw_byte.stop()
        self._patcher_validate_raw_bytes.stop()
        self._patcher_validate_addressing_type.stop()
        self._patcher_can_id_handler_class.stop()

    # ADDRESSING_FORMAT

    def test_addressing_format(self):
        assert Mixed11BitCanAddressingInformation.ADDRESSING_FORMAT == CanAddressingFormat.MIXED_11BIT_ADDRESSING

    # AI_DATA_BYTES_NUMBER

    def test_ai_data_bytes_number(self):
        assert Mixed11BitCanAddressingInformation.AI_DATA_BYTES_NUMBER == 1

    # _validate_addressing_information

    @pytest.mark.parametrize("rx_physical_params, tx_physical_params, rx_functional_params, tx_functional_params", [
        (
            {"can_id": 1, "address_extension": 1},
            {"can_id": 2, "address_extension": 2},
            {"can_id": 3, "address_extension": 4},
            {"can_id": 4, "address_extension": 4},
        ),
        (
            {"can_id": 0x4321, "address_extension": 0xFF},
            {"can_id": 0x4322, "address_extension": 0xFF},
            {"can_id": 0x4321, "address_extension": 0xFE},
            {"can_id": 0x4322, "address_extension": 0xF1},
        ),
        (
            {"can_id": 0xABC, "address_extension": 0xFF},
            {"can_id": 0xDEF, "address_extension": 0xFF},
            {"can_id": 0xADD, "address_extension": 0xFF},
            {"can_id": 0xABC, "address_extension": 0xFF},
        ),
        (
            {"can_id": 0xABC, "address_extension": 0x00},
            {"can_id": 0xDEF, "address_extension": 0x00},
            {"can_id": 0xDEF, "address_extension": 0xFF},
            {"can_id": 0xABD, "address_extension": 0xFF},
        ),
    ])
    def test_validate_node_ai__inconsistent(self, rx_physical_params, tx_physical_params,
                                            rx_functional_params, tx_functional_params):
        self.mock_addressing_information.rx_physical_params = rx_physical_params
        self.mock_addressing_information.tx_physical_params = tx_physical_params
        self.mock_addressing_information.rx_functional_params = rx_functional_params
        self.mock_addressing_information.tx_functional_params = tx_functional_params
        with pytest.raises(InconsistentArgumentsError):
            Mixed11BitCanAddressingInformation._validate_addressing_information(self.mock_addressing_information)

    @pytest.mark.parametrize("rx_physical_params, tx_physical_params, rx_functional_params, tx_functional_params", [
        (
            {"can_id": 1, "address_extension": 1},
            {"can_id": 2, "address_extension": 1},
            {"can_id": 3, "address_extension": 4},
            {"can_id": 4, "address_extension": 4},
        ),
        (
            {"can_id": 0x4321, "address_extension": 0xFF},
            {"can_id": 0x4322, "address_extension": 0xFF},
            {"can_id": 0x4321, "address_extension": 0xFE},
            {"can_id": 0x4322, "address_extension": 0xFE},
        ),
        (
            {"can_id": 0xABC, "address_extension": 0x5A},
            {"can_id": 0xDEF, "address_extension": 0x5A},
            {"can_id": 0xABC, "address_extension": 0x5A},
            {"can_id": 0xDEF, "address_extension": 0x5A},
        ),
    ])
    def test_validate_node_ai__valid(self, rx_physical_params, tx_physical_params,
                                     rx_functional_params, tx_functional_params):
        self.mock_addressing_information.rx_physical_params = rx_physical_params
        self.mock_addressing_information.tx_physical_params = tx_physical_params
        self.mock_addressing_information.rx_functional_params = rx_functional_params
        self.mock_addressing_information.tx_functional_params = tx_functional_params
        assert Mixed11BitCanAddressingInformation._validate_addressing_information(
            self.mock_addressing_information) is None

    # validate_addressing_params

    @pytest.mark.parametrize("addressing_format", [
        Mock(),
        CanAddressingFormat.NORMAL_ADDRESSING,
    ])
    def test_validate_addressing_params__value_error(self, addressing_format):
        with pytest.raises(ValueError):
            Mixed11BitCanAddressingInformation.validate_addressing_params(addressing_type=Mock(),
                                                                        can_id=Mock(),
                                                                        addressing_format=addressing_format)

    @pytest.mark.parametrize("unsupported_args", [
        {"target_address": 0x2C},
        {"source_address": 0x96},
        {"target_address": Mock(), "source_address": Mock()}
    ])
    def test_validate_addressing_params__inconsistent_arg(self, unsupported_args):
        with pytest.raises(UnusedArgumentError):
            Mixed11BitCanAddressingInformation.validate_addressing_params(addressing_type=Mock(),
                                                                  can_id=Mock(),
                                                                  address_extension=Mock(),
                                                                  **unsupported_args)

    @pytest.mark.parametrize("addressing_type, can_id, address_extension", [
        (Mock(), Mock(), Mock()),
        (AddressingType.PHYSICAL, 0x7FF, 0x5A),
    ])
    @patch(f"{SCRIPT_LOCATION}.Mixed11BitCanAddressingInformation.is_compatible_can_id")
    def test_validate_addressing_params__inconsistent(self, mock_is_compatible_can_id,
                                                      addressing_type, can_id, address_extension):
        mock_is_compatible_can_id.return_value = False
        with pytest.raises(InconsistentArgumentsError):
            Mixed11BitCanAddressingInformation.validate_addressing_params(addressing_type=addressing_type,
                                                                          can_id=can_id,
                                                                          address_extension=address_extension)
        mock_is_compatible_can_id.assert_called_once_with(can_id=can_id,
                                                          addressing_type=self.mock_validate_addressing_type.return_value)

    @pytest.mark.parametrize("addressing_type, can_id, address_extension", [
        (Mock(), Mock(), Mock()),
        (AddressingType.PHYSICAL, 0x7FF, 0x5A),
    ])
    @patch(f"{SCRIPT_LOCATION}.Mixed11BitCanAddressingInformation.is_compatible_can_id")
    def test_validate_addressing_params__valid(self, mock_is_compatible_can_id,
                                               addressing_type, can_id, address_extension):
        mock_is_compatible_can_id.return_value = True
        assert Mixed11BitCanAddressingInformation.validate_addressing_params(addressing_type=addressing_type,
                                                                             can_id=can_id,
                                                                             address_extension=address_extension) == {
                   "addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                   "addressing_type": self.mock_validate_addressing_type.return_value,
                   "can_id": can_id,
                   "target_address": None,
                   "source_address": None,
                   "address_extension": address_extension,
               }
        mock_is_compatible_can_id.assert_called_once_with(can_id=can_id,
                                                          addressing_type=self.mock_validate_addressing_type.return_value)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)

    # is_compatible_can_id

    @pytest.mark.parametrize("can_id, addressing_type", [
        (Mock(), Mock()),
        (0x12345, AddressingType.PHYSICAL),
    ])
    def test_is_compatible_can_id(self, can_id, addressing_type):
        assert (Mixed11BitCanAddressingInformation.is_compatible_can_id(can_id, addressing_type)
                == self.mock_can_id_handler_class.is_standard_can_id.return_value)

    # decode_can_id_ai_params

    @pytest.mark.parametrize("can_id", [Mock(), 0x1234])
    def test_decode_can_id_ai_params(self, can_id):
        assert Mixed11BitCanAddressingInformation.decode_can_id_ai_params(can_id) == {
            "addressing_type": None,
            "target_address": None,
            "source_address": None,
            "priority": None
        }

    # decode_data_bytes_ai_params

    @pytest.mark.parametrize("value", [b"\xFF", [0x5A, 0xB0]])
    def test_decode_data_bytes_ai_params(self, value):
        assert Mixed11BitCanAddressingInformation.decode_data_bytes_ai_params(value) == {"address_extension": value[0]}
        self.mock_validate_raw_bytes.assert_called_once_with(value, allow_empty=False)

    # encode_ai_data_bytes

    @pytest.mark.parametrize("target_address, address_extension", [
        (None, 0x0F),
        (Mock(), 0x98),
    ])
    def test_encode_ai_data_bytes(self, target_address, address_extension):
        assert Mixed11BitCanAddressingInformation.encode_ai_data_bytes(
            target_address=target_address, address_extension=address_extension) == bytearray([address_extension])
        self.mock_validate_raw_byte.assert_called_once_with(address_extension)


class TestMixed29BitCanAddressingInformation:
    """Unit tests for `Mixed29BitCanAddressingInformation` class."""

    def setup_method(self):
        self.mock_addressing_information = Mock(spec=Mixed29BitCanAddressingInformation)
        # patching
        self._patcher_validate_raw_byte = patch(f"{SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
        self._patcher_validate_raw_bytes = patch(f"{SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
        self._patcher_validate_addressing_type = patch(f"{SCRIPT_LOCATION}.AddressingType.validate_member")
        self.mock_validate_addressing_type = self._patcher_validate_addressing_type.start()

    def teardown_method(self):
        self._patcher_validate_raw_byte.stop()
        self._patcher_validate_addressing_type.stop()

    # ADDRESSING_FORMAT

    def test_addressing_format(self):
        assert Mixed29BitCanAddressingInformation.ADDRESSING_FORMAT == CanAddressingFormat.MIXED_29BIT_ADDRESSING

    # AI_DATA_BYTES_NUMBER

    def test_ai_data_bytes_number(self):
        assert Mixed29BitCanAddressingInformation.AI_DATA_BYTES_NUMBER == 1

    # _validate_addressing_information

    @pytest.mark.parametrize("rx_physical_params, tx_physical_params, "
                             "rx_functional_params, tx_functional_params", [
        (
            {"can_id": 0xCE1234, "target_address": 0x12, "source_address": 0x34, "address_extension": 0x01},
            {"can_id": 0xCE3413, "target_address": 0x34, "source_address": 0x13, "address_extension": 0x01},
            {"can_id": 0xCD01FF, "target_address": 0x01, "source_address": 0xFF, "address_extension": 0xFF},
            {"can_id": 0xCDFF01, "target_address": 0xFF, "source_address": 0x01, "address_extension": 0xFF},
        ),
        (
            {"can_id": 0x18CEFEDC, "target_address": 0xFE, "source_address": 0xDC, "address_extension": 0x00},
            {"can_id": 0x18CEDCDE, "target_address": 0xDC, "source_address": 0xFE, "address_extension": 0x00},
            {"can_id": 0x18CD543F, "target_address": 0x54, "source_address": 0x3F, "address_extension": 0xFF},
            {"can_id": 0x18CD543F, "target_address": 0x54, "source_address": 0x3F, "address_extension": 0xFF},
        ),
        (
            {"can_id": 0x1CCEFEDC, "target_address": 0xFE, "source_address": 0xDC, "address_extension": 0xCD},
            {"can_id": 0x1CCEDCDE, "target_address": 0xDC, "source_address": 0xFE, "address_extension": 0xCD},
            {"can_id": 0x10CD543F, "target_address": 0x54, "source_address": 0x3F, "address_extension": 0xCD},
            {"can_id": 0x10CD3F54, "target_address": 0x3F, "source_address": 0x54, "address_extension": 0x01},
        ),
        (
            {"can_id": 0xCCE00FF, "target_address": 0x00, "source_address": 0xFF, "address_extension": 0x43},
            {"can_id": 0xCCEFF00, "target_address": 0xFF, "source_address": 0x00, "address_extension": 0x65},
            {"can_id": 0x8CDFF00, "target_address": 0xFF, "source_address": 0x00, "address_extension": 0x43},
            {"can_id": 0x8CD00FF, "target_address": 0x00, "source_address": 0xFF, "address_extension": 0x65},
        ),
    ])
    def test_validate_addressing_information__inconsistent(self, rx_physical_params, tx_physical_params,
                                                           rx_functional_params, tx_functional_params):
        self.mock_addressing_information.rx_physical_params = rx_physical_params
        self.mock_addressing_information.tx_physical_params = tx_physical_params
        self.mock_addressing_information.rx_functional_params = rx_functional_params
        self.mock_addressing_information.tx_functional_params = tx_functional_params
        with pytest.raises(InconsistentArgumentsError):
            Mixed29BitCanAddressingInformation._validate_addressing_information(self.mock_addressing_information)

    @pytest.mark.parametrize("rx_physical_params, tx_physical_params, "
                             "rx_functional_params, tx_functional_params", [
        (
            {"can_id": 0xCE1234, "target_address": 0x12, "source_address": 0x34, "address_extension": 0x01},
            {"can_id": 0xCE3413, "target_address": 0x34, "source_address": 0x12, "address_extension": 0x01},
            {"can_id": 0xCD01FF, "target_address": 0x01, "source_address": 0xFF, "address_extension": 0xFF},
            {"can_id": 0xCDFF01, "target_address": 0xFF, "source_address": 0x01, "address_extension": 0xFF},
        ),
        (
            {"can_id": 0x18CEFEDC, "target_address": 0xFE, "source_address": 0xDC, "address_extension": 0x00},
            {"can_id": 0x18CEDCDE, "target_address": 0xDC, "source_address": 0xFE, "address_extension": 0x00},
            {"can_id": 0x18CD543F, "target_address": 0x54, "source_address": 0x3F, "address_extension": 0xFF},
            {"can_id": 0x18CD3F54, "target_address": 0x3F, "source_address": 0x54, "address_extension": 0xFF},
        ),
        (
            {"can_id": 0x1CCEFEDC, "target_address": 0xFE, "source_address": 0xDC, "address_extension": 0xCD},
            {"can_id": 0x1CCEDCDE, "target_address": 0xDC, "source_address": 0xFE, "address_extension": 0xCD},
            {"can_id": 0x10CD543F, "target_address": 0x54, "source_address": 0x3F, "address_extension": 0xCD},
            {"can_id": 0x10CD3F54, "target_address": 0x3F, "source_address": 0x54, "address_extension": 0xCD},
        ),
    ])
    def test_validate_addressing_information__valid(self, rx_physical_params, tx_physical_params,
                                                           rx_functional_params, tx_functional_params):
        self.mock_addressing_information.rx_physical_params = rx_physical_params
        self.mock_addressing_information.tx_physical_params = tx_physical_params
        self.mock_addressing_information.rx_functional_params = rx_functional_params
        self.mock_addressing_information.tx_functional_params = tx_functional_params
        assert Mixed29BitCanAddressingInformation._validate_addressing_information(
            self.mock_addressing_information) is None

    # validate_addressing_params

    @pytest.mark.parametrize("addressing_format", [
        Mock(),
        CanAddressingFormat.NORMAL_ADDRESSING,
    ])
    def test_validate_addressing_params__value_error(self, addressing_format):
        with pytest.raises(ValueError):
            Mixed29BitCanAddressingInformation.validate_addressing_params(addressing_type=Mock(),
                                                                          can_id=Mock(),
                                                                          addressing_format=addressing_format)

    @pytest.mark.parametrize("addressing_type, can_id, target_address, source_address, address_extension", [
        (Mock(), None, None, None, Mock()),
        (AddressingType.PHYSICAL, None, 0x05, None, 0x5A),
        (AddressingType.FUNCTIONAL, None, None, 0x50, 0xFF),
    ])
    def test_validate_addressing_params__inconsistent__missing_info(self, addressing_type, can_id,
                                                                    target_address, source_address, address_extension):
        self.mock_validate_addressing_type.return_value = addressing_type
        with pytest.raises(InconsistentArgumentsError):
            Mixed29BitCanAddressingInformation.validate_addressing_params(addressing_type=addressing_type,
                                                                  can_id=can_id,
                                                                  target_address=target_address,
                                                                  source_address=source_address,
                                                                  address_extension=address_extension)

    @pytest.mark.parametrize("addressing_type, decoded_addressing_type, ta, decoded_ta, sa, decoded_sa, can_id, address_extension", [
        (AddressingType.FUNCTIONAL, AddressingType.FUNCTIONAL, 0x56, 0x55, None, 0x10, Mock(), Mock()),
        (AddressingType.PHYSICAL, AddressingType.PHYSICAL, None, 0x55, 0x9F, 0x10, 0x123456, 0x12),
        ("something", "something else", 0x01, 0x01, 0xF0, 0xF0, 0x556677, 0x6A),
    ])
    @patch(f"{SCRIPT_LOCATION}.Mixed29BitCanAddressingInformation.decode_can_id_ai_params")
    def test_validate_addressing_params__inconsistent(self, mock_decode_can_id_ai_params,
                                                      addressing_type, decoded_addressing_type,
                                                      ta, decoded_ta, sa, decoded_sa, can_id, address_extension):
        self.mock_validate_addressing_type.return_value = addressing_type
        mock_decode_can_id_ai_params.return_value = {
            "addressing_type": decoded_addressing_type,
            "target_address": decoded_ta,
            "source_address": decoded_sa
        }
        with pytest.raises(InconsistentArgumentsError):
            Mixed29BitCanAddressingInformation.validate_addressing_params(addressing_type=addressing_type,
                                                                  can_id=can_id,
                                                                  target_address=ta,
                                                                  source_address=sa,
                                                                  address_extension=address_extension)
        mock_decode_can_id_ai_params.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing_type, target_address, source_address, address_extension", [
        (Mock(), Mock(), Mock(), Mock()),
        (AddressingType.PHYSICAL, 0xAA, 0x55, 0x00),
    ])
    @patch(f"{SCRIPT_LOCATION}.Mixed29BitCanAddressingInformation.encode_can_id")
    def test_validate_addressing_params__valid_without_can_id(self, mock_encode_can_id,
                                                              addressing_type, target_address, source_address,
                                                              address_extension):
        assert Mixed29BitCanAddressingInformation.validate_addressing_params(addressing_type=addressing_type,
                                                                     can_id=None,
                                                                     target_address=target_address,
                                                                     source_address=source_address,
                                                                     address_extension=address_extension) == {
            "addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
            "addressing_type": self.mock_validate_addressing_type.return_value,
            "can_id": mock_encode_can_id.return_value,
            "target_address": target_address,
            "source_address": source_address,
            "address_extension": address_extension,
        }
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
        self.mock_validate_raw_byte.assert_has_calls(
            [call(target_address), call(source_address), call(address_extension)], any_order=True)
        mock_encode_can_id.assert_called_once_with(addressing_type=self.mock_validate_addressing_type.return_value,
                                                   target_address=target_address,
                                                   source_address=source_address)

    @pytest.mark.parametrize("addressing_type, target_address, source_address, can_id, address_extension", [
        [Mock(), Mock(), Mock(), Mock(), Mock()],
        [AddressingType.PHYSICAL, None, None, 0x67234, 0x12],
        [AddressingType.FUNCTIONAL, 0x00, None, 0x67234, 0x34],
        [AddressingType.FUNCTIONAL, None, 0xFF, 0x67234, 0xE2],
    ])
    @patch(f"{SCRIPT_LOCATION}.Mixed29BitCanAddressingInformation.decode_can_id_ai_params")
    def test_validate_addressing_params__valid_with_can_id(self, mock_decode_can_id_ai_params,
                                                           addressing_type, target_address, source_address,
                                                           can_id, address_extension):
        decoded_target_address = target_address if target_address is not None else Mock()
        decoded_source_address = source_address if source_address is not None else Mock()
        mock_decode_can_id_ai_params.return_value = {
            "addressing_type": self.mock_validate_addressing_type.return_value,
            "target_address": decoded_target_address,
            "source_address": decoded_source_address
        }
        assert Mixed29BitCanAddressingInformation.validate_addressing_params(addressing_type=addressing_type,
                                                                             can_id=can_id,
                                                                             target_address=target_address,
                                                                             source_address=source_address,
                                                                             address_extension=address_extension) == {
                   "addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                   "addressing_type": self.mock_validate_addressing_type.return_value,
                   "can_id": can_id,
                   "target_address": decoded_target_address,
                   "source_address": decoded_source_address,
                   "address_extension": address_extension,
               }
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
        self.mock_validate_raw_byte.assert_called_once_with(address_extension)
        mock_decode_can_id_ai_params.assert_called_once_with(can_id)

    # is_compatible_can_id

    @pytest.mark.parametrize("value", [CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_MASKED_VALUE
                                       + (CanIdHandler.MIN_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
                                       CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_MASKED_VALUE + 0x1234
                                       + (CanIdHandler.DEFAULT_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
                                       CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_MASKED_VALUE + 0xFFFF
                                       + (CanIdHandler.MAX_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
                                       CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_MASKED_VALUE
                                       + (CanIdHandler.MIN_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
                                       CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_MASKED_VALUE + 0xDEBA
                                       + (CanIdHandler.DEFAULT_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
                                       CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_MASKED_VALUE + 0xFFFF
                                       + (CanIdHandler.MAX_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET)])
    def test_is_compatible_can_id__without_addressing__true(self, value):
        assert Mixed29BitCanAddressingInformation.is_compatible_can_id(value) is True
        self.mock_validate_addressing_type.assert_not_called()

    @pytest.mark.parametrize("value", [CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_MASKED_VALUE
                                       + (CanIdHandler.MIN_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET) +  0x10000,
                                       CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_MASKED_VALUE +
                                       (CanIdHandler.MAX_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET) - 1])
    def test_is_compatible_can_id__without_addressing__false(self, value):
        assert Mixed29BitCanAddressingInformation.is_compatible_can_id(value) is False
        self.mock_validate_addressing_type.assert_not_called()

    @pytest.mark.parametrize("value, addressing_type", [
        (CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_MASKED_VALUE
         + (CanIdHandler.MIN_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
         AddressingType.PHYSICAL),
        (CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_MASKED_VALUE + 0x1234
         + (CanIdHandler.DEFAULT_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
         AddressingType.PHYSICAL),
        (CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_MASKED_VALUE + 0xFFFF
         + (CanIdHandler.MAX_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
         AddressingType.PHYSICAL),
        (CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_MASKED_VALUE
         + (CanIdHandler.MIN_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
         AddressingType.FUNCTIONAL),
        (CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_MASKED_VALUE + 0xDEBA
         + (CanIdHandler.DEFAULT_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
         AddressingType.FUNCTIONAL),
        (CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_MASKED_VALUE + 0xFFFF
         + (CanIdHandler.MAX_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
         AddressingType.FUNCTIONAL),
    ])
    def test_is_compatible_can_id__with_addressing__true(self, value, addressing_type):
        self.mock_validate_addressing_type.return_value = addressing_type
        assert Mixed29BitCanAddressingInformation.is_compatible_can_id(value, addressing_type=addressing_type) is True
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)

    @pytest.mark.parametrize("value, addressing_type", [
        (CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_MASKED_VALUE
         + (CanIdHandler.MIN_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET) - 1,
         AddressingType.PHYSICAL),
        (CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_MASKED_VALUE
         + (CanIdHandler.DEFAULT_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
         AddressingType.FUNCTIONAL),
        (CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_MASKED_VALUE + 0xFFFF
         + (CanIdHandler.MAX_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
         AddressingType.FUNCTIONAL),
        (CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_MASKED_VALUE
         + (CanIdHandler.MIN_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
         AddressingType.PHYSICAL),
        (CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_MASKED_VALUE + 0xFFFF
         + (CanIdHandler.DEFAULT_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
         AddressingType.PHYSICAL),
        (CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_MASKED_VALUE + 0x10000
         + (CanIdHandler.MAX_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
         AddressingType.FUNCTIONAL),
        (0, AddressingType.PHYSICAL),
    ])
    def test_is_compatible_can_id__with_addressing__false(self, value, addressing_type):
        self.mock_validate_addressing_type.return_value = addressing_type
        assert Mixed29BitCanAddressingInformation.is_compatible_can_id(value, addressing_type=addressing_type) is False
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)

    # decode_can_id_ai_params

    @pytest.mark.parametrize("can_id", [0, 0x20000])
    @patch(f"{SCRIPT_LOCATION}.Mixed29BitCanAddressingInformation.is_compatible_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.validate_can_id")
    def test_decode_can_id_ai_params__not_implemented(self, mock_validate_can_id, mock_is_compatible_can_id, can_id):
        mock_is_compatible_can_id.return_value = True
        with pytest.raises(NotImplementedError):
            Mixed29BitCanAddressingInformation.decode_can_id_ai_params(can_id=can_id)
        mock_validate_can_id.assert_called_once_with(can_id)
        mock_is_compatible_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("can_id", [0xFFFFFFFFFFFF, "something"])
    @patch(f"{SCRIPT_LOCATION}.Mixed29BitCanAddressingInformation.is_compatible_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.validate_can_id")
    def test_decode_can_id_ai_params__value_error(self, mock_validate_can_id, mock_is_compatible_can_id, can_id):
        mock_is_compatible_can_id.return_value = False
        with pytest.raises(ValueError):
            Mixed29BitCanAddressingInformation.decode_can_id_ai_params(can_id=can_id)
        mock_validate_can_id.assert_called_once_with(can_id)
        mock_is_compatible_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing_type, target_address, source_address, priority, can_id", [
        (AddressingType.PHYSICAL, 0x12, 0x34, 0b110, 0x18CE1234),
        (AddressingType.FUNCTIONAL, 0xFE, 0xDC, 0b110, 0x18CDFEDC),
        (AddressingType.PHYSICAL, 0x00, 0xFF, 0b000, 0xCE00FF),
        (AddressingType.FUNCTIONAL, 0xFF, 0x00, 0b111, 0x1CCDFF00),
    ])
    def test_decode_can_id_ai_params__valid(self, addressing_type, target_address, source_address, priority, can_id):
        assert Mixed29BitCanAddressingInformation.decode_can_id_ai_params(can_id=can_id) == {
            "addressing_type": addressing_type,
            "target_address": target_address,
            "source_address": source_address,
            "priority": priority,
        }

    # decode_data_bytes_ai_params

    @pytest.mark.parametrize("value", [b"\xFF", [0x5A, 0xB0]])
    def test_decode_data_bytes_ai_params(self, value):
        assert Mixed29BitCanAddressingInformation.decode_data_bytes_ai_params(value) == {"address_extension": value[0]}
        self.mock_validate_raw_bytes.assert_called_once_with(value, allow_empty=False)

    # encode_can_id

    @pytest.mark.parametrize("addressing_type, target_address, source_address", [
        (Mock(), 0x55, 0xAA),
        ("something not handled", 0x00, 0xFF)
    ])
    def test_encode_can_id__not_implemented(self, addressing_type, target_address, source_address):
        self.mock_validate_addressing_type.return_value = addressing_type
        with pytest.raises(NotImplementedError):
            Mixed29BitCanAddressingInformation.encode_can_id(addressing_type=addressing_type,
                                                              target_address=target_address,
                                                              source_address=source_address)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)

    @pytest.mark.parametrize("addressing_type, target_address, source_address, expected_can_id", [
        (AddressingType.PHYSICAL, 0x12, 0x34, 0x18CE1234),
        (AddressingType.FUNCTIONAL, 0xFE, 0xDC, 0x18CDFEDC),
        (AddressingType.PHYSICAL, 0x00, 0xFF, 0x18CE00FF),
        (AddressingType.FUNCTIONAL, 0xFF, 0x00, 0x18CDFF00),
    ])
    def test_encode_can_id__valid_without_priority(self, addressing_type, target_address, source_address,
                                                   expected_can_id):
        self.mock_validate_addressing_type.return_value = addressing_type
        assert Mixed29BitCanAddressingInformation.encode_can_id(addressing_type=addressing_type,
                                                                target_address=target_address,
                                                                source_address=source_address) == expected_can_id
        self.mock_validate_raw_byte.assert_has_calls([call(target_address), call(source_address)], any_order=True)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)

    @pytest.mark.parametrize("addressing_type, priority, target_address, source_address, expected_can_id", [
        (AddressingType.PHYSICAL, 0b000, 0x12, 0x34, 0xCE1234),
        (AddressingType.FUNCTIONAL, 0b011, 0xFE, 0xDC, 0xCCDFEDC),
        (AddressingType.PHYSICAL, 0b101, 0x00, 0xFF, 0x14CE00FF),
        (AddressingType.FUNCTIONAL, 0b111, 0xFF, 0x00, 0x1CCDFF00),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.validate_priority")
    def test_encode_can_id__valid_with_priority(self, mock_validate_priority,
                                                addressing_type, priority, target_address, source_address,
                                                expected_can_id):
        self.mock_validate_addressing_type.return_value = addressing_type
        assert Mixed29BitCanAddressingInformation.encode_can_id(addressing_type=addressing_type,
                                                                 target_address=target_address,
                                                                 source_address=source_address,
                                                                 priority=priority) == expected_can_id
        self.mock_validate_raw_byte.assert_has_calls([call(target_address), call(source_address)], any_order=True)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
        mock_validate_priority.assert_called_once_with(priority)

    # encode_ai_data_bytes

    @pytest.mark.parametrize("target_address, address_extension", [
        (None, 0x0F),
        (Mock(), 0x98),
    ])
    def test_encode_ai_data_bytes(self, target_address, address_extension):
        assert Mixed29BitCanAddressingInformation.encode_ai_data_bytes(
            target_address=target_address, address_extension=address_extension) == bytearray([address_extension])
        self.mock_validate_raw_byte.assert_called_once_with(address_extension)

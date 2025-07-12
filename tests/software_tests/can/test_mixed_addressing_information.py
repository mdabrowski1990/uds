import pytest
from mock import Mock, call, patch

from uds.can.mixed_addressing_information import (
    AbstractCanAddressingInformation,
    CanAddressingFormat,
    InconsistentArgumentsError,
    Mixed11BitCanAddressingInformation,
    Mixed29BitCanAddressingInformation,
    UnusedArgumentError,
)

SCRIPT_LOCATION = "uds.can.mixed_addressing_information"


class TestMixed11BitCanAddressingInformation:
    """Unit tests for `Mixed11BitCanAddressingInformation` class."""

    def setup_method(self):
        self.mock_addressing_information = Mock(spec=Mixed11BitCanAddressingInformation)
        # patching
        self._patcher_validate_raw_byte = patch(f"{SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
        self._patcher_validate_addressing_type = patch(f"{SCRIPT_LOCATION}.AddressingType.validate_member")
        self.mock_validate_addressing_type = self._patcher_validate_addressing_type.start()
        self._patcher_can_id_handler_class = patch(f"{SCRIPT_LOCATION}.CanIdHandler")
        self.mock_can_id_handler_class = self._patcher_can_id_handler_class.start()

    def teardown_method(self):
        self._patcher_validate_raw_byte.stop()
        self._patcher_validate_addressing_type.stop()
        self._patcher_can_id_handler_class.stop()

    # addressing_format

    def test_addressing_format(self):
        assert Mixed11BitCanAddressingInformation.addressing_format.fget(self.mock_addressing_information) \
               == CanAddressingFormat.MIXED_11BIT_ADDRESSING

    # validate_packet_ai

    @pytest.mark.parametrize("unsupported_args", [
        {"target_address": "something"},
        {"source_address": Mock()},
        {"target_address": Mock(), "source_address": Mock()}
    ])
    def test_validate_packet_ai__inconsistent_arg(self, unsupported_args):
        with pytest.raises(UnusedArgumentError):
            Mixed11BitCanAddressingInformation.validate_packet_ai(addressing_type=Mock(),
                                                                  can_id=Mock(),
                                                                  address_extension=Mock(),
                                                                  **unsupported_args)

    @pytest.mark.parametrize("addressing_type, can_id", [
        ("some addressing type", "some id"),
        (Mock(), 0x7FF),
    ])
    @pytest.mark.parametrize("address_extension", ["some AE", 0x5B])
    def test_validate_ai_mixed_11bit__invalid_can_id(self, addressing_type, can_id, address_extension):
        self.mock_can_id_handler_class.is_mixed_11bit_addressed_can_id.return_value = False
        with pytest.raises(InconsistentArgumentsError):
            Mixed11BitCanAddressingInformation.validate_packet_ai(addressing_type=addressing_type,
                                                                  can_id=can_id,
                                                                  address_extension=address_extension)
        self.mock_can_id_handler_class.validate_can_id.assert_called_once_with(can_id)
        self.mock_can_id_handler_class.is_mixed_11bit_addressed_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing_type, can_id", [
        ("some addressing type", "some id"),
        (Mock(), 0x7FF),
    ])
    @pytest.mark.parametrize("address_extension", ["some AE", 0x5B])
    def test_validate_ai_mixed_11bit__valid(self, addressing_type, can_id, address_extension):
        self.mock_can_id_handler_class.is_mixed_11bit_addressed_can_id.return_value = True
        assert Mixed11BitCanAddressingInformation.validate_packet_ai(addressing_type=addressing_type,
                                                                     can_id=can_id,
                                                                     address_extension=address_extension) == {
            AbstractCanAddressingInformation.ADDRESSING_FORMAT_NAME: CanAddressingFormat.MIXED_11BIT_ADDRESSING,
            AbstractCanAddressingInformation.ADDRESSING_TYPE_NAME: addressing_type,
            AbstractCanAddressingInformation.CAN_ID_NAME: can_id,
            AbstractCanAddressingInformation.ADDRESS_EXTENSION_NAME: address_extension,
            AbstractCanAddressingInformation.TARGET_ADDRESS_NAME: None,
            AbstractCanAddressingInformation.SOURCE_ADDRESS_NAME: None,
        }
        self.mock_can_id_handler_class.validate_can_id.assert_called_once_with(can_id)
        self.mock_can_id_handler_class.is_mixed_11bit_addressed_can_id.assert_called_once_with(can_id)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
        self.mock_validate_raw_byte.assert_called_once_with(address_extension)

    # _validate_node_ai

    @pytest.mark.parametrize("rx_packets_physical_ai, tx_packets_physical_ai, "
                             "rx_packets_functional_ai, tx_packets_functional_ai", [
        (
            {"can_id": 1, "address_extension": 1},
            {"can_id": 2, "address_extension": 1},
            {"can_id": 3, "address_extension": 4},
            {"can_id": 3, "address_extension": 4},
        ),
        (
            {"can_id": 0x4321, "address_extension": 0xFF},
            {"can_id": 0x4321, "address_extension": 0xFF},
            {"can_id": 0x4321, "address_extension": 0xFE},
            {"can_id": 0x4321, "address_extension": 0xFE},
        ),
        (
            {"can_id": 0xABC, "address_extension": 0xFF},
            {"can_id": 0xDEF, "address_extension": 0xFF},
            {"can_id": 0xADD, "address_extension": 0xFE},
            {"can_id": 0xFEE, "address_extension": 0xF1},
        ),
        (
            {"can_id": 0xABC, "address_extension": 0x4E},
            {"can_id": 0xDEF, "address_extension": 0x4E},
            {"can_id": 0xDEF, "address_extension": 0x4E},
            {"can_id": 0xABC, "address_extension": 0x4E},
        ),
    ])
    def test_validate_node_ai__inconsistent(self, rx_packets_physical_ai, tx_packets_physical_ai,
                                            rx_packets_functional_ai, tx_packets_functional_ai):
        with pytest.raises(InconsistentArgumentsError):
            Mixed11BitCanAddressingInformation._validate_node_ai(rx_packets_physical_ai=rx_packets_physical_ai,
                                                                 tx_packets_physical_ai=tx_packets_physical_ai,
                                                                 rx_packets_functional_ai=rx_packets_functional_ai,
                                                                 tx_packets_functional_ai=tx_packets_functional_ai)

    @pytest.mark.parametrize("rx_packets_physical_ai, tx_packets_physical_ai, "
                             "rx_packets_functional_ai, tx_packets_functional_ai", [
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
            {"can_id": 0xABC, "address_extension": 0xFF},
            {"can_id": 0xDEF, "address_extension": 0xFF},
            {"can_id": 0xADD, "address_extension": 0xF1},
            {"can_id": 0xFEE, "address_extension": 0xF1},
        ),
        (
            {"can_id": 0xABC, "address_extension": 0x43},
            {"can_id": 0xDEF, "address_extension": 0x43},
            {"can_id": 0xABC, "address_extension": 0x70},
            {"can_id": 0xDEF, "address_extension": 0x70},
        ),
    ])
    def test_validate_node_ai__valid(self, rx_packets_physical_ai, tx_packets_physical_ai,
                                     rx_packets_functional_ai, tx_packets_functional_ai):
        assert Mixed11BitCanAddressingInformation._validate_node_ai(
            rx_packets_physical_ai=rx_packets_physical_ai,
            tx_packets_physical_ai=tx_packets_physical_ai,
            rx_packets_functional_ai=rx_packets_functional_ai,
            tx_packets_functional_ai=tx_packets_functional_ai) is None


class TestMixed29BitCanAddressingInformation:
    """Unit tests for `Mixed29BitCanAddressingInformation` class."""

    def setup_method(self):
        self.mock_addressing_information = Mock(spec=Mixed29BitCanAddressingInformation)
        # patching
        self._patcher_validate_raw_byte = patch(f"{SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
        self._patcher_validate_addressing_type = patch(f"{SCRIPT_LOCATION}.AddressingType.validate_member")
        self.mock_validate_addressing_type = self._patcher_validate_addressing_type.start()
        self._patcher_can_id_handler_class = patch(f"{SCRIPT_LOCATION}.CanIdHandler")
        self.mock_can_id_handler_class = self._patcher_can_id_handler_class.start()

    def teardown_method(self):
        self._patcher_validate_raw_byte.stop()
        self._patcher_validate_addressing_type.stop()
        self._patcher_can_id_handler_class.stop()

    # addressing_format

    def test_addressing_format(self):
        assert Mixed29BitCanAddressingInformation.addressing_format.fget(self.mock_addressing_information) \
               == CanAddressingFormat.MIXED_29BIT_ADDRESSING

    # validate_packet_ai

    @pytest.mark.parametrize("addressing_type", ["some addressing type", Mock()])
    @pytest.mark.parametrize("can_id, target_address, source_address", [
        (None, None, 0),
        (None, 0x05, None),
        (None, None, None),
    ])
    @pytest.mark.parametrize("address_extension", ["some AE", 0x5B])
    def test_validate_packet_ai__missing_info(self, addressing_type, can_id,
                                              target_address, source_address, address_extension):
        self.mock_can_id_handler_class.is_mixed_29bit_addressed_can_id.return_value = True
        with pytest.raises(InconsistentArgumentsError):
            Mixed29BitCanAddressingInformation.validate_packet_ai(addressing_type=addressing_type,
                                                                  can_id=can_id,
                                                                  target_address=target_address,
                                                                  source_address=source_address,
                                                                  address_extension=address_extension)

    @pytest.mark.parametrize("can_id", ["some CAN ID", 0x8FABC])
    @pytest.mark.parametrize("addressing_type, decoded_addressing_type, ta, decoded_ta, sa, decoded_sa", [
        (Mock(), Mock(), None, 0x55, None, 0x80),
        ("something", "something", 0x56, 0x55, None, 0x10),
        ("abc", "abc", None, 0x55, 0x9F, 0x10),
        ("something", "something else", 0x1, 0x2, 0xF0, 0x10),
    ])
    @pytest.mark.parametrize("address_extension", ["some AE", 0x5B])
    def test_validate_packet_ai__inconsistent_can_id_ta_sa(self, can_id, addressing_type, decoded_addressing_type,
                                                           ta, decoded_ta, sa, decoded_sa, address_extension):
        self.mock_validate_addressing_type.return_value = addressing_type
        self.mock_can_id_handler_class.decode_mixed_addressed_29bit_can_id.return_value = {
            self.mock_can_id_handler_class.ADDRESSING_TYPE_NAME: decoded_addressing_type,
            self.mock_can_id_handler_class.TARGET_ADDRESS_NAME: decoded_ta,
            self.mock_can_id_handler_class.SOURCE_ADDRESS_NAME: decoded_sa,
        }
        with pytest.raises(InconsistentArgumentsError):
            Mixed29BitCanAddressingInformation.validate_packet_ai(addressing_type=addressing_type,
                                                                  can_id=can_id,
                                                                  target_address=ta,
                                                                  source_address=sa,
                                                                  address_extension=address_extension)
        self.mock_can_id_handler_class.decode_mixed_addressed_29bit_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing_type", ["some addressing type", Mock()])
    @pytest.mark.parametrize("target_address, source_address", [
        ("ta", "sa"),
        (0, 0),
        (0xFA, 0x55),
    ])
    @pytest.mark.parametrize("address_extension", ["some AE", 0x5B])
    def test_validate_packet_ai__valid_without_can_id(self, addressing_type,
                                                      target_address, source_address, address_extension):
        assert Mixed29BitCanAddressingInformation.validate_packet_ai(addressing_type=addressing_type,
                                                                     can_id=None,
                                                                     target_address=target_address,
                                                                     source_address=source_address,
                                                                     address_extension=address_extension) == {
            AbstractCanAddressingInformation.ADDRESSING_FORMAT_NAME: CanAddressingFormat.MIXED_29BIT_ADDRESSING,
            AbstractCanAddressingInformation.ADDRESSING_TYPE_NAME: self.mock_validate_addressing_type.return_value,
            AbstractCanAddressingInformation.CAN_ID_NAME: self.mock_can_id_handler_class.encode_mixed_addressed_29bit_can_id.return_value,
            AbstractCanAddressingInformation.TARGET_ADDRESS_NAME: target_address,
            AbstractCanAddressingInformation.SOURCE_ADDRESS_NAME: source_address,
            AbstractCanAddressingInformation.ADDRESS_EXTENSION_NAME: address_extension,
        }
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
        self.mock_validate_raw_byte.assert_has_calls([call(target_address), call(source_address),
                                                      call(address_extension)], any_order=True)
        self.mock_can_id_handler_class.validate_can_id.assert_not_called()
        self.mock_can_id_handler_class.decode_mixed_addressed_29bit_can_id.assert_not_called()
        self.mock_can_id_handler_class.encode_mixed_addressed_29bit_can_id.assert_called_once_with(
            addressing_type=self.mock_validate_addressing_type.return_value,
            target_address=target_address,
            source_address=source_address)

    @pytest.mark.parametrize("can_id", ["some CAN ID", 0x85421])
    @pytest.mark.parametrize("target_address, source_address, addressing_type", [
        (None, None, "XD"),
        (0x12, None, Mock()),
        (None, 0x34, Mock()),
        ("ta", "sa", "some addressing type"),
    ])
    @pytest.mark.parametrize("address_extension", ["some AE", 0x5B])
    def test_validate_packet_ai__valid_with_can_id(self, addressing_type, can_id,
                                                   target_address, source_address, address_extension):
        decoded_target_address = target_address or "ta"
        decoded_source_address = source_address or "sa"
        self.mock_can_id_handler_class.decode_mixed_addressed_29bit_can_id.return_value = {
            self.mock_can_id_handler_class.ADDRESSING_TYPE_NAME: self.mock_validate_addressing_type.return_value,
            self.mock_can_id_handler_class.TARGET_ADDRESS_NAME: decoded_target_address,
            self.mock_can_id_handler_class.SOURCE_ADDRESS_NAME: decoded_source_address,
        }
        assert Mixed29BitCanAddressingInformation.validate_packet_ai(addressing_type=addressing_type,
                                                                     can_id=can_id,
                                                                     target_address=target_address,
                                                                     source_address=source_address,
                                                                     address_extension=address_extension) == {
            AbstractCanAddressingInformation.ADDRESSING_FORMAT_NAME: CanAddressingFormat.MIXED_29BIT_ADDRESSING,
            AbstractCanAddressingInformation.ADDRESSING_TYPE_NAME: self.mock_validate_addressing_type.return_value,
            AbstractCanAddressingInformation.CAN_ID_NAME: can_id,
            AbstractCanAddressingInformation.TARGET_ADDRESS_NAME: decoded_target_address,
            AbstractCanAddressingInformation.SOURCE_ADDRESS_NAME: decoded_source_address,
            AbstractCanAddressingInformation.ADDRESS_EXTENSION_NAME: address_extension,
        }
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
        self.mock_validate_raw_byte.assert_called_once_with(address_extension)
        self.mock_can_id_handler_class.decode_mixed_addressed_29bit_can_id.assert_called_once_with(can_id)

    # _validate_node_ai

    @pytest.mark.parametrize("rx_packets_physical_ai, tx_packets_physical_ai, "
                             "rx_packets_functional_ai, tx_packets_functional_ai", [
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
    def test_validate_node_ai__inconsistent(self, rx_packets_physical_ai, tx_packets_physical_ai,
                                            rx_packets_functional_ai, tx_packets_functional_ai):
        with pytest.raises(InconsistentArgumentsError):
            Mixed29BitCanAddressingInformation._validate_node_ai(rx_packets_physical_ai=rx_packets_physical_ai,
                                                                 tx_packets_physical_ai=tx_packets_physical_ai,
                                                                 rx_packets_functional_ai=rx_packets_functional_ai,
                                                                 tx_packets_functional_ai=tx_packets_functional_ai)

    @pytest.mark.parametrize("rx_packets_physical_ai, tx_packets_physical_ai, "
                             "rx_packets_functional_ai, tx_packets_functional_ai", [
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
    def test_validate_node_ai__valid(self, rx_packets_physical_ai, tx_packets_physical_ai,
                                     rx_packets_functional_ai, tx_packets_functional_ai):
        assert Mixed29BitCanAddressingInformation._validate_node_ai(
            rx_packets_physical_ai=rx_packets_physical_ai,
            tx_packets_physical_ai=tx_packets_physical_ai,
            rx_packets_functional_ai=rx_packets_functional_ai,
            tx_packets_functional_ai=tx_packets_functional_ai) is None

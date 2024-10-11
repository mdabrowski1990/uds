import pytest
from mock import Mock, call, patch

from uds.can.normal_addressing_information import (
    AbstractCanAddressingInformation,
    CanAddressingFormat,
    InconsistentArgumentsError,
    NormalCanAddressingInformation,
    NormalFixedCanAddressingInformation,
    UnusedArgumentError,
)

SCRIPT_LOCATION = "uds.can.normal_addressing_information"


class TestNormalCanAddressingInformation:
    """Unit tests for `NormalCanAddressingInformation` class."""

    def setup_method(self):
        self.mock_addressing_information = Mock(spec=NormalCanAddressingInformation)
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
        assert NormalCanAddressingInformation.addressing_format.fget(self.mock_addressing_information) \
               == CanAddressingFormat.NORMAL_ADDRESSING

    # validate_packet_ai

    @pytest.mark.parametrize("unsupported_args", [
        {"target_address": 1},
        {"source_address": "something"},
        {"address_extension": Mock()},
        {"target_address": Mock(), "source_address": Mock(), "address_extension": Mock()}
    ])
    def test_validate_packet_ai__inconsistent_arg(self, unsupported_args):
        with pytest.raises(UnusedArgumentError):
            NormalCanAddressingInformation.validate_packet_ai(addressing_type=Mock(),
                                                              can_id=Mock(),
                                                              **unsupported_args)

    @pytest.mark.parametrize("addressing_type, can_id", [
        ("some addressing type", "some id"),
        (Mock(), 0x7FF),
    ])
    def test_validate_packet_ai__invalid_can_id(self, addressing_type, can_id):
        self.mock_can_id_handler_class.is_normal_addressed_can_id.return_value = False
        with pytest.raises(InconsistentArgumentsError):
            NormalCanAddressingInformation.validate_packet_ai(addressing_type=addressing_type, can_id=can_id)
        self.mock_can_id_handler_class.validate_can_id.assert_called_once_with(can_id)
        self.mock_can_id_handler_class.is_normal_addressed_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing_type, can_id", [
        ("some addressing type", "some id"),
        (Mock(), 0x7FF),
    ])
    def test_validate_packet_ai__valid(self, addressing_type, can_id):
        self.mock_can_id_handler_class.is_normal_addressed_can_id.return_value = True
        assert NormalCanAddressingInformation.validate_packet_ai(addressing_type=addressing_type,
                                                                 can_id=can_id) == {
                   AbstractCanAddressingInformation.ADDRESSING_FORMAT_NAME: CanAddressingFormat.NORMAL_ADDRESSING,
                   AbstractCanAddressingInformation.ADDRESSING_TYPE_NAME: self.mock_validate_addressing_type.return_value,
                   AbstractCanAddressingInformation.CAN_ID_NAME: can_id,
                   AbstractCanAddressingInformation.TARGET_ADDRESS_NAME: None,
                   AbstractCanAddressingInformation.SOURCE_ADDRESS_NAME: None,
                   AbstractCanAddressingInformation.ADDRESS_EXTENSION_NAME: None,
               }
        self.mock_can_id_handler_class.validate_can_id.assert_called_once_with(can_id)
        self.mock_can_id_handler_class.is_normal_addressed_can_id.assert_called_once_with(can_id)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)

    # _validate_node_ai

    @pytest.mark.parametrize("rx_packets_physical_ai, tx_packets_physical_ai, "
                             "rx_packets_functional_ai, tx_packets_functional_ai", [
        (
            {"can_id": 1},
            {"can_id": 2},
            {"can_id": 3},
            {"can_id": 3},
        ),
        (
            {"can_id": 0x4321},
            {"can_id": 0x4321},
            {"can_id": 0x4321},
            {"can_id": 0x4321},
        ),
    ])
    def test_validate_node_ai__inconsistent(self, rx_packets_physical_ai, tx_packets_physical_ai,
                                            rx_packets_functional_ai, tx_packets_functional_ai):
        with pytest.raises(InconsistentArgumentsError):
            NormalCanAddressingInformation._validate_node_ai(rx_packets_physical_ai=rx_packets_physical_ai,
                                                               tx_packets_physical_ai=tx_packets_physical_ai,
                                                               rx_packets_functional_ai=rx_packets_functional_ai,
                                                               tx_packets_functional_ai=tx_packets_functional_ai)

    @pytest.mark.parametrize("rx_packets_physical_ai, tx_packets_physical_ai, "
                             "rx_packets_functional_ai, tx_packets_functional_ai", [
        (
            {"can_id": 1},
            {"can_id": 2},
            {"can_id": 3},
            {"can_id": 4},
        ),
        (
            {"can_id": 0x711},
            {"can_id": 0x712},
            {"can_id": 0x6FE},
            {"can_id": 0x6FF},
        ),
        (
            {"can_id": 0xABC1},
            {"can_id": 0xABC2},
            {"can_id": 0xABC3},
            {"can_id": 0xABC4},
        ),
    ])
    def test_validate_node_ai__valid(self, rx_packets_physical_ai, tx_packets_physical_ai,
                                            rx_packets_functional_ai, tx_packets_functional_ai):
        assert NormalCanAddressingInformation._validate_node_ai(
            rx_packets_physical_ai=rx_packets_physical_ai,
            tx_packets_physical_ai=tx_packets_physical_ai,
            rx_packets_functional_ai=rx_packets_functional_ai,
            tx_packets_functional_ai=tx_packets_functional_ai) is None


class TestNormalFixedCanAddressingInformation:
    """Unit tests for `NormalFixedCanAddressingInformation` class."""

    def setup_method(self):
        self.mock_addressing_information = Mock(spec=NormalFixedCanAddressingInformation)
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
        assert NormalFixedCanAddressingInformation.addressing_format.fget(self.mock_addressing_information) \
               == CanAddressingFormat.NORMAL_FIXED_ADDRESSING

    # validate_packet_ai

    @pytest.mark.parametrize("unsupported_args", [
        {"address_extension": Mock()},
    ])
    def test_validate_packet_ai__inconsistent_arg(self, unsupported_args):
        with pytest.raises(UnusedArgumentError):
            NormalFixedCanAddressingInformation.validate_packet_ai(addressing_type=Mock(),
                                                                   can_id=Mock(),
                                                                   **unsupported_args)

    @pytest.mark.parametrize("addressing_type", ["some addressing type", Mock()])
    @pytest.mark.parametrize("can_id, target_address, source_address", [
        (None, None, 0),
        (None, 0x05, None),
        (None, None, None),
    ])
    def test_validate_packet_ai__missing_info(self, addressing_type, can_id,
                                              target_address, source_address):
        self.mock_can_id_handler_class.is_normal_fixed_addressed_can_id.return_value = True
        with pytest.raises(InconsistentArgumentsError):
            NormalFixedCanAddressingInformation.validate_packet_ai(addressing_type=addressing_type,
                                                                   can_id=can_id,
                                                                   target_address=target_address,
                                                                   source_address=source_address)

    @pytest.mark.parametrize("can_id", ["some CAN ID", 0x8FABC])
    @pytest.mark.parametrize("addressing_type, decoded_addressing_type, ta, decoded_ta, sa, decoded_sa", [
        (Mock(), Mock(), None, 0x55, None, 0x80),
        ("something", "something", 0x56, 0x55, None, 0x10),
        ("abc", "abc", None, 0x55, 0x9F, 0x10),
        ("something", "something else", 0x1, 0x2, 0xF0, 0x10),
    ])
    def test_validate_packet_ai__inconsistent_can_id_ta_sa(self, can_id, addressing_type, decoded_addressing_type,
                                                           ta, decoded_ta, sa, decoded_sa):
        self.mock_validate_addressing_type.return_value = addressing_type
        self.mock_can_id_handler_class.decode_normal_fixed_addressed_can_id.return_value = {
            self.mock_can_id_handler_class.ADDRESSING_TYPE_NAME: decoded_addressing_type,
            self.mock_can_id_handler_class.TARGET_ADDRESS_NAME: decoded_ta,
            self.mock_can_id_handler_class.SOURCE_ADDRESS_NAME: decoded_sa
        }
        with pytest.raises(InconsistentArgumentsError):
            NormalFixedCanAddressingInformation.validate_packet_ai(addressing_type=addressing_type,
                                                                   can_id=can_id,
                                                                   target_address=ta,
                                                                   source_address=sa)
        self.mock_can_id_handler_class.decode_normal_fixed_addressed_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing_type", ["some addressing type", Mock()])
    @pytest.mark.parametrize("target_address, source_address", [
        ("ta", "sa"),
        (0xFA, 0x55),
    ])
    def test_validate_packet_ai__valid_without_can_id(self, addressing_type, target_address, source_address):
        assert NormalFixedCanAddressingInformation.validate_packet_ai(addressing_type=addressing_type,
                                                                      can_id=None,
                                                                      target_address=target_address,
                                                                      source_address=source_address) == {
            AbstractCanAddressingInformation.ADDRESSING_FORMAT_NAME: CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
            AbstractCanAddressingInformation.ADDRESSING_TYPE_NAME: self.mock_validate_addressing_type.return_value,
            AbstractCanAddressingInformation.CAN_ID_NAME: self.mock_can_id_handler_class.encode_normal_fixed_addressed_can_id.return_value,
            AbstractCanAddressingInformation.TARGET_ADDRESS_NAME: target_address,
            AbstractCanAddressingInformation.SOURCE_ADDRESS_NAME: source_address,
            AbstractCanAddressingInformation.ADDRESS_EXTENSION_NAME: None,
        }
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
        self.mock_validate_raw_byte.assert_has_calls([call(target_address), call(source_address)], any_order=True)
        self.mock_can_id_handler_class.validate_can_id.assert_not_called()
        self.mock_can_id_handler_class.decode_normal_fixed_addressed_can_id.assert_not_called()
        self.mock_can_id_handler_class.encode_normal_fixed_addressed_can_id.assert_called_once_with(
            addressing_type=self.mock_validate_addressing_type.return_value,
            target_address=target_address,
            source_address=source_address
        )

    @pytest.mark.parametrize("addressing_type", ["some addressing type", Mock()])
    @pytest.mark.parametrize("can_id", ["some CAN ID", 0x85421])
    @pytest.mark.parametrize("target_address, source_address", [
        (None, None),
        (0x12, None),
        (None, 0x34),
        ("ta", "sa"),
    ])
    def test_validate_packet_ai__valid_with_can_id(self, addressing_type, can_id, target_address, source_address):
        decoded_target_address = target_address or "ta"
        decoded_source_address = source_address or "sa"
        self.mock_can_id_handler_class.decode_normal_fixed_addressed_can_id.return_value = {
            self.mock_can_id_handler_class.ADDRESSING_TYPE_NAME: self.mock_validate_addressing_type.return_value,
            self.mock_can_id_handler_class.TARGET_ADDRESS_NAME: decoded_target_address,
            self.mock_can_id_handler_class.SOURCE_ADDRESS_NAME: decoded_source_address,
        }
        assert NormalFixedCanAddressingInformation.validate_packet_ai(addressing_type=addressing_type,
                                                                      can_id=can_id,
                                                                      target_address=target_address,
                                                                      source_address=source_address) == {
            AbstractCanAddressingInformation.ADDRESSING_FORMAT_NAME: CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
            AbstractCanAddressingInformation.ADDRESSING_TYPE_NAME: self.mock_validate_addressing_type.return_value,
            AbstractCanAddressingInformation.CAN_ID_NAME: can_id,
            AbstractCanAddressingInformation.TARGET_ADDRESS_NAME: decoded_target_address,
            AbstractCanAddressingInformation.SOURCE_ADDRESS_NAME: decoded_source_address,
            AbstractCanAddressingInformation.ADDRESS_EXTENSION_NAME: None,
        }
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
        self.mock_validate_raw_byte.assert_not_called()
        self.mock_can_id_handler_class.decode_normal_fixed_addressed_can_id.assert_called_once_with(can_id)

    # _validate_node_ai

    @pytest.mark.parametrize("rx_packets_physical_ai, tx_packets_physical_ai, "
                             "rx_packets_functional_ai, tx_packets_functional_ai", [
        (
            {"can_id": 0xDA1234, "target_address": 0x12, "source_address": 0x34},
            {"can_id": 0xDA3413, "target_address": 0x34, "source_address": 0x13},
            {"can_id": 0xDB01FF, "target_address": 0x01, "source_address": 0xFF},
            {"can_id": 0xDBFF01, "target_address": 0xFF, "source_address": 0x01},
        ),
        (
            {"can_id": 0x18DAFEDC, "target_address": 0xFE, "source_address": 0xDC},
            {"can_id": 0x18DADCDE, "target_address": 0xDC, "source_address": 0xFE},
            {"can_id": 0x18DB543F, "target_address": 0x54, "source_address": 0x3F},
            {"can_id": 0x18DB543F, "target_address": 0x54, "source_address": 0x3F},
        ),
    ])
    def test_validate_node_ai__inconsistent(self, rx_packets_physical_ai, tx_packets_physical_ai,
                                            rx_packets_functional_ai, tx_packets_functional_ai):
        with pytest.raises(InconsistentArgumentsError):
            NormalFixedCanAddressingInformation._validate_node_ai(rx_packets_physical_ai=rx_packets_physical_ai,
                                                                  tx_packets_physical_ai=tx_packets_physical_ai,
                                                                  rx_packets_functional_ai=rx_packets_functional_ai,
                                                                  tx_packets_functional_ai=tx_packets_functional_ai)

    @pytest.mark.parametrize("rx_packets_physical_ai, tx_packets_physical_ai, "
                             "rx_packets_functional_ai, tx_packets_functional_ai", [
        (
            {"can_id": 0xDA1234, "target_address": 0x12, "source_address": 0x34},
            {"can_id": 0xDA3412, "target_address": 0x34, "source_address": 0x12},
            {"can_id": 0xDB01FF, "target_address": 0x01, "source_address": 0xFF},
            {"can_id": 0xDBFF01, "target_address": 0xFF, "source_address": 0x01},
        ),
        (
            {"can_id": 0x18DAFEDC, "target_address": 0xFE, "source_address": 0xDC},
            {"can_id": 0x18DADCDE, "target_address": 0xDC, "source_address": 0xFE},
            {"can_id": 0x18DB543F, "target_address": 0x54, "source_address": 0x3F},
            {"can_id": 0x18DB3F54, "target_address": 0x3F, "source_address": 0x54},
        ),
        (
            {"can_id": 0x1CDA2F71, "target_address": 0x2F, "source_address": 0x71},
            {"can_id": 0x1CDA712F, "target_address": 0x71, "source_address": 0x2F},
            {"can_id": 0x8DB5580, "target_address": 0x55, "source_address": 0x80},
            {"can_id": 0x8DB8055, "target_address": 0x80, "source_address": 0x55},
        ),
    ])
    def test_validate_node_ai__valid(self, rx_packets_physical_ai, tx_packets_physical_ai,
                                            rx_packets_functional_ai, tx_packets_functional_ai):
        assert NormalFixedCanAddressingInformation._validate_node_ai(
            rx_packets_physical_ai=rx_packets_physical_ai,
            tx_packets_physical_ai=tx_packets_physical_ai,
            rx_packets_functional_ai=rx_packets_functional_ai,
            tx_packets_functional_ai=tx_packets_functional_ai) is None

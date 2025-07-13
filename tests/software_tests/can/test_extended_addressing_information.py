import pytest
from mock import Mock, patch

from uds.can.addressing import (
    AbstractCanAddressingInformation,
    CanAddressingFormat,
    ExtendedCanAddressingInformation,
    InconsistentArgumentsError,
    UnusedArgumentError,
)

SCRIPT_LOCATION = "uds.addressing.extended_addressing_information"


class TestExtendedCanAddressingInformation:
    """Unit tests for `ExtendedCanAddressingInformation` class."""

    def setup_method(self):
        self.mock_addressing_information = Mock(spec=ExtendedCanAddressingInformation)
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
        assert ExtendedCanAddressingInformation.addressing_format.fget(self.mock_addressing_information) \
               == CanAddressingFormat.EXTENDED_ADDRESSING

    # validate_packet_ai

    @pytest.mark.parametrize("unsupported_args", [
        {"source_address": "something"},
        {"address_extension": Mock()},
        {"source_address": Mock(), "address_extension": Mock()}
    ])
    def test_validate_packet_ai__inconsistent_arg(self, unsupported_args):
        with pytest.raises(UnusedArgumentError):
            ExtendedCanAddressingInformation.validate_packet_ai(addressing_type=Mock(),
                                                                can_id=Mock(),
                                                                target_address=Mock(),
                                                                **unsupported_args)

    @pytest.mark.parametrize("addressing_type, can_id", [
        ("some addressing type", "some id"),
        (Mock(), 0x7FF),
    ])
    @pytest.mark.parametrize("target_address", ["some TA", 0x5B])
    def test_validate_packet_ai__invalid_can_id(self, addressing_type, can_id, target_address):
        self.mock_can_id_handler_class.is_extended_addressed_can_id.return_value = False
        with pytest.raises(InconsistentArgumentsError):
            ExtendedCanAddressingInformation.validate_packet_ai(addressing_type=addressing_type,
                                                                can_id=can_id,
                                                                target_address=target_address)
        self.mock_can_id_handler_class.validate_can_id.assert_called_once_with(can_id)
        self.mock_can_id_handler_class.is_extended_addressed_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing_type, can_id", [
        ("some addressing type", "some id"),
        (Mock(), 0x7FF),
    ])
    @pytest.mark.parametrize("target_address", ["some TA", 0x5B])
    def test_validate_packet_ai__valid(self, addressing_type, can_id, target_address):
        self.mock_can_id_handler_class.is_extended_addressed_can_id.return_value = True
        assert ExtendedCanAddressingInformation.validate_packet_ai(addressing_type=addressing_type,
                                                                   can_id=can_id,
                                                                   target_address=target_address) == {
            AbstractCanAddressingInformation.ADDRESSING_FORMAT_NAME: CanAddressingFormat.EXTENDED_ADDRESSING,
            AbstractCanAddressingInformation.ADDRESSING_TYPE_NAME: self.mock_validate_addressing_type.return_value,
            AbstractCanAddressingInformation.CAN_ID_NAME: can_id,
            AbstractCanAddressingInformation.TARGET_ADDRESS_NAME: target_address,
            AbstractCanAddressingInformation.SOURCE_ADDRESS_NAME: None,
            AbstractCanAddressingInformation.ADDRESS_EXTENSION_NAME: None,
        }
        self.mock_can_id_handler_class.validate_can_id.assert_called_once_with(can_id)
        self.mock_can_id_handler_class.is_extended_addressed_can_id.assert_called_once_with(can_id)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
        self.mock_validate_raw_byte.assert_called_once_with(target_address)

    # _validate_node_ai

    @pytest.mark.parametrize("rx_packets_physical_ai, tx_packets_physical_ai, "
                             "rx_packets_functional_ai, tx_packets_functional_ai", [
        (
            {"can_id": 1, "target_address": 2},
            {"can_id": 2, "target_address": 1},
            {"can_id": 3, "target_address": 4},
            {"can_id": 3, "target_address": 4},
        ),
        (
            {"can_id": 0x4321, "target_address": 0xFF},
            {"can_id": 0x4321, "target_address": 0xFE},
            {"can_id": 0x4321, "target_address": 0xFD},
            {"can_id": 0x4321, "target_address": 0xFF},
        ),
    ])
    def test_validate_node_ai__inconsistent(self, rx_packets_physical_ai, tx_packets_physical_ai,
                                            rx_packets_functional_ai, tx_packets_functional_ai):
        with pytest.raises(InconsistentArgumentsError):
            ExtendedCanAddressingInformation._validate_node_ai(rx_packets_physical_ai=rx_packets_physical_ai,
                                                               tx_packets_physical_ai=tx_packets_physical_ai,
                                                               rx_packets_functional_ai=rx_packets_functional_ai,
                                                               tx_packets_functional_ai=tx_packets_functional_ai)

    @pytest.mark.parametrize("rx_packets_physical_ai, tx_packets_physical_ai, "
                             "rx_packets_functional_ai, tx_packets_functional_ai", [
        (
            {"can_id": 1, "target_address": 2},
            {"can_id": 2, "target_address": 1},
            {"can_id": 3, "target_address": 4},
            {"can_id": 4, "target_address": 3},
        ),
        (
            {"can_id": 0x4321, "target_address": 0xFF},
            {"can_id": 0x4321, "target_address": 0x00},
            {"can_id": 0x4321, "target_address": 0xFF},
            {"can_id": 0x4321, "target_address": 0x00},
        ),
        (
            {"can_id": 0xABC1, "target_address": 0xFF},
            {"can_id": 0xABC2, "target_address": 0xFF},
            {"can_id": 0xABC3, "target_address": 0xFF},
            {"can_id": 0xABC4, "target_address": 0xFF},
        ),
    ])
    def test_validate_node_ai__valid(self, rx_packets_physical_ai, tx_packets_physical_ai,
                                            rx_packets_functional_ai, tx_packets_functional_ai):
        assert ExtendedCanAddressingInformation._validate_node_ai(
            rx_packets_physical_ai=rx_packets_physical_ai,
            tx_packets_physical_ai=tx_packets_physical_ai,
            rx_packets_functional_ai=rx_packets_functional_ai,
            tx_packets_functional_ai=tx_packets_functional_ai) is None

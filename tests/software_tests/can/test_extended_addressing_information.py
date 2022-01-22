import pytest
from mock import Mock, patch

from uds.can.extended_addressing_information import ExtendedAddressingInformation, \
    CanAddressingFormat, InconsistentArgumentsError, AddressingType


class TestExtendedAddressingInformation:
    """Unit tests for `ExtendedAddressingInformation` class."""

    SCRIPT_LOCATION = "uds.can.extended_addressing_information"

    def setup(self):
        self.mock_addressing_information = Mock(spec=ExtendedAddressingInformation,
                                                ADDRESSING_FORMAT_NAME="addressing_format",
                                                ADDRESSING_TYPE_NAME="addressing_type",
                                                TARGET_ADDRESS_NAME="target_address",
                                                SOURCE_ADDRESS_NAME="source_address",
                                                ADDRESS_EXTENSION_NAME="address_extension")
        # patching
        self._patcher_validate_raw_byte = patch(f"{self.SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
        self._patcher_validate_addressing_type = patch(f"{self.SCRIPT_LOCATION}.AddressingType.validate_member")
        self.mock_validate_addressing_type = self._patcher_validate_addressing_type.start()
        self._patcher_can_id_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanIdHandler")
        self.mock_can_id_handler_class = self._patcher_can_id_handler_class.start()

    def teardown(self):
        self._patcher_validate_raw_byte.stop()
        self._patcher_validate_addressing_type.stop()
        self._patcher_can_id_handler_class.stop()

    # addressing_format

    def test_addressing_format(self):
        assert ExtendedAddressingInformation.addressing_format.fget(self.mock_addressing_information) \
               == CanAddressingFormat.EXTENDED_ADDRESSING
        
    # ai_data_bytes_number

    def test_ai_data_bytes_number(self):
        assert ExtendedAddressingInformation.ai_data_bytes_number.fget(self.mock_addressing_information) == 1

    # rx_packets_physical_ai

    @pytest.mark.parametrize("value", ["any value", Mock()])
    def test_rx_packets_physical_ai__get(self, value):
        self.mock_addressing_information._ExtendedAddressingInformation__rx_packets_physical_ai = value
        assert ExtendedAddressingInformation.rx_packets_physical_ai.fget(self.mock_addressing_information) == value

    @pytest.mark.parametrize("value", [{"a": 1, "b": 2}, {"argument_1": None, "argument_2": Mock()}])
    def test_rx_packets_physical_ai__set(self, value):
        ExtendedAddressingInformation.rx_packets_physical_ai.fset(self.mock_addressing_information, value)
        self.mock_addressing_information.validate_packet_ai(addressing_type=AddressingType.PHYSICAL, **value)
        assert self.mock_addressing_information._ExtendedAddressingInformation__rx_packets_physical_ai == {
            self.mock_addressing_information.ADDRESSING_FORMAT_NAME: self.mock_addressing_information.addressing_format,
            self.mock_addressing_information.ADDRESSING_TYPE_NAME: AddressingType.PHYSICAL,
            self.mock_addressing_information.SOURCE_ADDRESS_NAME: None,
            self.mock_addressing_information.ADDRESS_EXTENSION_NAME: None,
            **value
        }
        
    # tx_packets_physical_ai

    @pytest.mark.parametrize("value", ["any value", Mock()])
    def test_tx_packets_physical_ai__get(self, value):
        self.mock_addressing_information._ExtendedAddressingInformation__tx_packets_physical_ai = value
        assert ExtendedAddressingInformation.tx_packets_physical_ai.fget(self.mock_addressing_information) == value

    @pytest.mark.parametrize("value", [{"a": 1, "b": 2}, {"argument_1": None, "argument_2": Mock()}])
    def test_tx_packets_physical_ai__set(self, value):
        ExtendedAddressingInformation.tx_packets_physical_ai.fset(self.mock_addressing_information, value)
        self.mock_addressing_information.validate_packet_ai(addressing_type=AddressingType.PHYSICAL, **value)
        assert self.mock_addressing_information._ExtendedAddressingInformation__tx_packets_physical_ai == {
            self.mock_addressing_information.ADDRESSING_FORMAT_NAME: self.mock_addressing_information.addressing_format,
            self.mock_addressing_information.ADDRESSING_TYPE_NAME: AddressingType.PHYSICAL,
            self.mock_addressing_information.SOURCE_ADDRESS_NAME: None,
            self.mock_addressing_information.ADDRESS_EXTENSION_NAME: None,
            **value
        }
        
    # rx_packets_functional_ai

    @pytest.mark.parametrize("value", ["any value", Mock()])
    def test_rx_packets_functional_ai__get(self, value):
        self.mock_addressing_information._ExtendedAddressingInformation__rx_packets_functional_ai = value
        assert ExtendedAddressingInformation.rx_packets_functional_ai.fget(self.mock_addressing_information) == value

    @pytest.mark.parametrize("value", [{"a": 1, "b": 2}, {"argument_1": None, "argument_2": Mock()}])
    def test_rx_packets_functional_ai__set(self, value):
        ExtendedAddressingInformation.rx_packets_functional_ai.fset(self.mock_addressing_information, value)
        self.mock_addressing_information.validate_packet_ai(addressing_type=AddressingType.FUNCTIONAL, **value)
        assert self.mock_addressing_information._ExtendedAddressingInformation__rx_packets_functional_ai == {
            self.mock_addressing_information.ADDRESSING_FORMAT_NAME: self.mock_addressing_information.addressing_format,
            self.mock_addressing_information.ADDRESSING_TYPE_NAME: AddressingType.FUNCTIONAL,
            self.mock_addressing_information.SOURCE_ADDRESS_NAME: None,
            self.mock_addressing_information.ADDRESS_EXTENSION_NAME: None,
            **value
        }
        
    # tx_packets_functional_ai

    @pytest.mark.parametrize("value", ["any value", Mock()])
    def test_tx_packets_functional_ai__get(self, value):
        self.mock_addressing_information._ExtendedAddressingInformation__tx_packets_functional_ai = value
        assert ExtendedAddressingInformation.tx_packets_functional_ai.fget(self.mock_addressing_information) == value

    @pytest.mark.parametrize("value", [{"a": 1, "b": 2}, {"argument_1": None, "argument_2": Mock()}])
    def test_tx_packets_functional_ai__set(self, value):
        ExtendedAddressingInformation.tx_packets_functional_ai.fset(self.mock_addressing_information, value)
        self.mock_addressing_information.validate_packet_ai(addressing_type=AddressingType.FUNCTIONAL, **value)
        assert self.mock_addressing_information._ExtendedAddressingInformation__tx_packets_functional_ai == {
            self.mock_addressing_information.ADDRESSING_FORMAT_NAME: self.mock_addressing_information.addressing_format,
            self.mock_addressing_information.ADDRESSING_TYPE_NAME: AddressingType.FUNCTIONAL,
            self.mock_addressing_information.SOURCE_ADDRESS_NAME: None,
            self.mock_addressing_information.ADDRESS_EXTENSION_NAME: None,
            **value
        }

    # validate_packet_ai

    @pytest.mark.parametrize("addressing_type, can_id", [
        ("some addressing type", "some id"),
        (Mock(), 0x7FF),
    ])
    @pytest.mark.parametrize("target_address", ["some TA", 0x5B])
    def test_validate_packet_ai__invalid_can_id(self, addressing_type, can_id, target_address):
        self.mock_can_id_handler_class.is_extended_addressed_can_id.return_value = False
        with pytest.raises(InconsistentArgumentsError):
            ExtendedAddressingInformation.validate_packet_ai(addressing_type=addressing_type,
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
        ExtendedAddressingInformation.validate_packet_ai(addressing_type=addressing_type,
                                                         can_id=can_id,
                                                         target_address=target_address)
        self.mock_can_id_handler_class.validate_can_id.assert_called_once_with(can_id)
        self.mock_can_id_handler_class.is_extended_addressed_can_id.assert_called_once_with(can_id)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
        self.mock_validate_raw_byte.assert_called_once_with(target_address)

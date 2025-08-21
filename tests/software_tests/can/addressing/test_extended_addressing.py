import pytest
from mock import Mock, patch

from uds.can.addressing.extended_addressing import (
    AddressingType,
    CanAddressingFormat,
    ExtendedCanAddressingInformation,
    InconsistencyError,
    UnusedArgumentError,
)

SCRIPT_LOCATION = "uds.can.addressing.extended_addressing"


class TestExtendedCanAddressingInformation:
    """Unit tests for `ExtendedCanAddressingInformation` class."""

    def setup_method(self):
        self.mock_addressing_information = Mock(spec=ExtendedCanAddressingInformation)
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
        assert ExtendedCanAddressingInformation.ADDRESSING_FORMAT == CanAddressingFormat.EXTENDED_ADDRESSING

    # AI_DATA_BYTES_NUMBER

    def test_ai_data_bytes_number(self):
        assert ExtendedCanAddressingInformation.AI_DATA_BYTES_NUMBER == 1

    # _validate_addressing_information

    @pytest.mark.parametrize("rx_physical_params, tx_physical_params, rx_functional_params, tx_functional_params", [
        (
                {"can_id": 1, "target_address": 0xAA},
                {"can_id": 2, "target_address": 0xAA},
                {"can_id": 3, "target_address": 0x12},
                {"can_id": 3, "target_address": 0xFF},
        ),
        (
                {"can_id": 0x4321, "target_address": 0x00},
                {"can_id": 0x4322, "target_address": 0xFF},
                {"can_id": 0x4323, "target_address": 0x00},
                {"can_id": 0x4321, "target_address": 0xFF},
        ),
    ])
    def test_validate_node_ai__inconsistent(self, rx_physical_params, tx_physical_params,
                                            rx_functional_params, tx_functional_params):
        self.mock_addressing_information.rx_physical_params = rx_physical_params
        self.mock_addressing_information.tx_physical_params = tx_physical_params
        self.mock_addressing_information.rx_functional_params = rx_functional_params
        self.mock_addressing_information.tx_functional_params = tx_functional_params
        with pytest.raises(InconsistencyError):
            ExtendedCanAddressingInformation._validate_addressing_information(self.mock_addressing_information)

    @pytest.mark.parametrize("rx_physical_params, tx_physical_params, rx_functional_params, tx_functional_params", [
        (
                {"can_id": 1, "target_address": 0x11},
                {"can_id": 2, "target_address": 0x22},
                {"can_id": 1, "target_address": 0x33},
                {"can_id": 2, "target_address": 0x44},
        ),
        (
                {"can_id": 1, "target_address": 0x5F},
                {"can_id": 2, "target_address": 0x5F},
                {"can_id": 3, "target_address": 0x5F},
                {"can_id": 4, "target_address": 0x5F},
        ),
        (
                {"can_id": 0x4321, "target_address": 0xD2},
                {"can_id": 0x4322, "target_address": 0xD2},
                {"can_id": 0x4321, "target_address": 0xD2},
                {"can_id": 0x4323, "target_address": 0xD2},
        ),
        (
                {"can_id": 0x700, "target_address": 0xFF},
                {"can_id": 0x7DF, "target_address": 0x00},
                {"can_id": 0x700, "target_address": 0xE0},
                {"can_id": 0x7DF, "target_address": 0xDB},
        ),
    ])
    def test_validate_node_ai__valid(self, rx_physical_params, tx_physical_params,
                                     rx_functional_params, tx_functional_params):
        self.mock_addressing_information.rx_physical_params = rx_physical_params
        self.mock_addressing_information.tx_physical_params = tx_physical_params
        self.mock_addressing_information.rx_functional_params = rx_functional_params
        self.mock_addressing_information.tx_functional_params = tx_functional_params
        assert ExtendedCanAddressingInformation._validate_addressing_information(
            self.mock_addressing_information) is None

    # validate_addressing_params

    @pytest.mark.parametrize("addressing_format", [
        Mock(),
        CanAddressingFormat.NORMAL_ADDRESSING,
    ])
    def test_validate_addressing_params__value_error(self, addressing_format):
        with pytest.raises(ValueError):
            ExtendedCanAddressingInformation.validate_addressing_params(addressing_type=Mock(),
                                                                        can_id=Mock(),
                                                                        addressing_format=addressing_format)

    @pytest.mark.parametrize("unsupported_args", [
        {"source_address": 0x5F},
        {"address_extension": 0xA0},
        {"source_address": Mock(), "address_extension": Mock()}
    ])
    def test_validate_addressing_params__unused_args(self, unsupported_args):
        with pytest.raises(UnusedArgumentError):
            ExtendedCanAddressingInformation.validate_addressing_params(addressing_type=Mock(),
                                                                        can_id=Mock(),
                                                                        target_address=Mock(),
                                                                        **unsupported_args)

    @pytest.mark.parametrize("addressing_type, can_id", [
        (Mock(), Mock()),
        (AddressingType.PHYSICAL, 0x7FF),
    ])
    @patch(f"{SCRIPT_LOCATION}.ExtendedCanAddressingInformation.is_compatible_can_id")
    def test_validate_addressing_params__inconsistent(self, mock_is_compatible_can_id, addressing_type, can_id):
        mock_is_compatible_can_id.return_value = False
        with pytest.raises(InconsistencyError):
            ExtendedCanAddressingInformation.validate_addressing_params(addressing_type=addressing_type,
                                                                        can_id=can_id)
        mock_is_compatible_can_id.assert_called_once_with(can_id=can_id,
                                                          addressing_type=self.mock_validate_addressing_type.return_value)

    @pytest.mark.parametrize("addressing_type, can_id, target_address", [
        (Mock(), Mock(), Mock()),
        (AddressingType.PHYSICAL, 0x7FF, 0x5A),
    ])
    @patch(f"{SCRIPT_LOCATION}.ExtendedCanAddressingInformation.is_compatible_can_id")
    def test_validate_addressing_params__valid(self, mock_is_compatible_can_id, addressing_type, can_id,
                                               target_address):
        mock_is_compatible_can_id.return_value = True
        assert ExtendedCanAddressingInformation.validate_addressing_params(addressing_type=addressing_type,
                                                                           can_id=can_id,
                                                                           target_address=target_address) == {
                   "addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
                   "addressing_type": self.mock_validate_addressing_type.return_value,
                   "can_id": can_id,
                   "target_address": target_address,
                   "source_address": None,
                   "address_extension": None,
               }
        mock_is_compatible_can_id.assert_called_once_with(can_id=can_id,
                                                          addressing_type=self.mock_validate_addressing_type.return_value)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
        self.mock_validate_raw_byte.assert_called_once_with(target_address)

    # is_compatible_can_id

    @pytest.mark.parametrize("can_id, addressing_type", [
        (Mock(), Mock()),
        (0x500, AddressingType.PHYSICAL),
    ])
    def test_is_compatible_can_id(self, can_id, addressing_type):
        assert (ExtendedCanAddressingInformation.is_compatible_can_id(can_id, addressing_type)
                == self.mock_can_id_handler_class.is_can_id.return_value)

    # decode_can_id_ai_params

    @pytest.mark.parametrize("can_id", [Mock(), 0x1234])
    def test_decode_can_id_ai_params(self, can_id):
        assert ExtendedCanAddressingInformation.decode_can_id_ai_params(can_id) == {
            "addressing_type": None,
            "target_address": None,
            "source_address": None,
            "priority": None
        }

    # decode_data_bytes_ai_params

    @pytest.mark.parametrize("value", [b"\xFF", [0x5A, 0xB0]])
    def test_decode_data_bytes_ai_params(self, value):
        assert ExtendedCanAddressingInformation.decode_data_bytes_ai_params(value) == {"target_address": value[0]}
        self.mock_validate_raw_bytes.assert_called_once_with(value, allow_empty=False)

    # encode_ai_data_bytes

    @pytest.mark.parametrize("target_address, address_extension", [
        (0x0F, None),
        (0x98, Mock()),
    ])
    def test_encode_ai_data_bytes(self, target_address, address_extension):
        assert ExtendedCanAddressingInformation.encode_ai_data_bytes(
            target_address=target_address, address_extension=address_extension) == bytearray([target_address])
        self.mock_validate_raw_byte.assert_called_once_with(target_address)
import pytest
from mock import Mock, call, patch

from uds.can.addressing.normal_addressing import (
    AddressingType,
    CanAddressingFormat,
    CanIdHandler,
    InconsistentArgumentsError,
    NormalCanAddressingInformation,
    NormalFixedCanAddressingInformation,
    UnusedArgumentError,
)

SCRIPT_LOCATION = "uds.can.addressing.normal_addressing"


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
        assert NormalCanAddressingInformation.ADDRESSING_FORMAT == CanAddressingFormat.NORMAL_ADDRESSING

    # ai_data_bytes_number

    def test_ai_data_bytes_number(self):
        assert NormalCanAddressingInformation.AI_DATA_BYTES_NUMBER == 0

    # is_compatible_can_id

    @pytest.mark.parametrize("can_id, addressing_type", [
        (Mock(), Mock()),
        (0x12345, AddressingType.PHYSICAL),
    ])
    def test_is_compatible_can_id(self, can_id, addressing_type):
        assert (NormalCanAddressingInformation.is_compatible_can_id(can_id, addressing_type)
                == self.mock_can_id_handler_class.is_can_id.return_value)

    # decode_can_id

    @pytest.mark.parametrize("can_id", [Mock(), 0x1234])
    def test_decode_can_id(self, can_id):
        assert NormalCanAddressingInformation.decode_can_id(can_id) == {
            "addressing_type": None,
            "target_address": None,
            "source_address": None,
            "priority": None
        }

    # validate_addressing_params

    @pytest.mark.parametrize("addressing_format", [
        Mock(),
        CanAddressingFormat.EXTENDED_ADDRESSING,
    ])
    def test_validate_addressing_params__value_error(self, addressing_format):
        with pytest.raises(ValueError):
            NormalCanAddressingInformation.validate_addressing_params(addressing_type=Mock(),
                                                                      can_id=Mock(),
                                                                      addressing_format=addressing_format)

    @pytest.mark.parametrize("unsupported_args", [
        {"target_address": 0x2C},
        {"source_address": 0x96},
        {"address_extension": 0x02},
        {"target_address": Mock(), "source_address": Mock(), "address_extension": Mock()}
    ])
    def test_validate_addressing_params__unused_args(self, unsupported_args):
        with pytest.raises(UnusedArgumentError):
            NormalCanAddressingInformation.validate_addressing_params(addressing_type=Mock(),
                                                                      can_id=Mock(),
                                                                      **unsupported_args)

    @pytest.mark.parametrize("addressing_type, can_id", [
        (Mock(), Mock()),
        (AddressingType.PHYSICAL, 0x7FF),
    ])
    @patch(f"{SCRIPT_LOCATION}.NormalCanAddressingInformation.is_compatible_can_id")
    def test_validate_addressing_params__inconsistent(self, mock_is_compatible_can_id, addressing_type, can_id):
        mock_is_compatible_can_id.return_value = False
        with pytest.raises(InconsistentArgumentsError):
            NormalCanAddressingInformation.validate_addressing_params(addressing_type=addressing_type, can_id=can_id)
        mock_is_compatible_can_id.assert_called_once_with(can_id=can_id,
                                                          addressing_type=self.mock_validate_addressing_type.return_value)

    @pytest.mark.parametrize("addressing_type, can_id", [
        (Mock(), Mock()),
        (AddressingType.PHYSICAL, 0x7FF),
    ])
    @patch(f"{SCRIPT_LOCATION}.NormalCanAddressingInformation.is_compatible_can_id")
    def test_validate_addressing_params__valid(self, mock_is_compatible_can_id, addressing_type, can_id):
        mock_is_compatible_can_id.return_value = True
        assert NormalCanAddressingInformation.validate_addressing_params(addressing_type=addressing_type,
                                                                         can_id=can_id) == {
                   "addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
                   "addressing_type": self.mock_validate_addressing_type.return_value,
                   "can_id": can_id,
                   "target_address": None,
                   "source_address": None,
                   "address_extension": None,
               }
        mock_is_compatible_can_id.assert_called_once_with(can_id=can_id,
                                                          addressing_type=self.mock_validate_addressing_type.return_value)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)

    # _validate_addressing_information

    @pytest.mark.parametrize("rx_physical_params, tx_physical_params, rx_functional_params, tx_functional_params", [
        (
            {"can_id": 1},
            {"can_id": 2},
            {"can_id": 3},
            {"can_id": 3},
        ),
        (
            {"can_id": 0x4321},
            {"can_id": 0x4322},
            {"can_id": 0x4323},
            {"can_id": 0x4321},
        ),
    ])
    def test_validate_node_ai__inconsistent(self, rx_physical_params, tx_physical_params,
                                            rx_functional_params, tx_functional_params):
        self.mock_addressing_information.rx_physical_params = rx_physical_params
        self.mock_addressing_information.tx_physical_params = tx_physical_params
        self.mock_addressing_information.rx_functional_params = rx_functional_params
        self.mock_addressing_information.tx_functional_params = tx_functional_params
        with pytest.raises(InconsistentArgumentsError):
            NormalCanAddressingInformation._validate_addressing_information(self.mock_addressing_information)

    @pytest.mark.parametrize("rx_physical_params, tx_physical_params, rx_functional_params, tx_functional_params", [
        (
            {"can_id": 1},
            {"can_id": 2},
            {"can_id": 3},
            {"can_id": 4},
        ),
        (
            {"can_id": 1},
            {"can_id": 4},
            {"can_id": 3},
            {"can_id": 4},
        ),
        (
            {"can_id": 0x4321},
            {"can_id": 0x4322},
            {"can_id": 0x4321},
            {"can_id": 0x4323},
        ),
        (
            {"can_id": 0x700},
            {"can_id": 0x7DF},
            {"can_id": 0x700},
            {"can_id": 0x7DF},
        ),
    ])
    def test_validate_node_ai__valid(self, rx_physical_params, tx_physical_params,
                                            rx_functional_params, tx_functional_params):
        self.mock_addressing_information.rx_physical_params = rx_physical_params
        self.mock_addressing_information.tx_physical_params = tx_physical_params
        self.mock_addressing_information.rx_functional_params = rx_functional_params
        self.mock_addressing_information.tx_functional_params = tx_functional_params
        assert NormalCanAddressingInformation._validate_addressing_information(self.mock_addressing_information) is None


class TestNormalFixedCanAddressingInformation:
    """Unit tests for `NormalFixedCanAddressingInformation` class."""

    def setup_method(self):
        self.mock_addressing_information = Mock(spec=NormalFixedCanAddressingInformation)
        # patching
        self._patcher_validate_raw_byte = patch(f"{SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
        self._patcher_validate_addressing_type = patch(f"{SCRIPT_LOCATION}.AddressingType.validate_member")
        self.mock_validate_addressing_type = self._patcher_validate_addressing_type.start()

    def teardown_method(self):
        self._patcher_validate_raw_byte.stop()
        self._patcher_validate_addressing_type.stop()

    # addressing_format

    def test_addressing_format(self):
        assert NormalFixedCanAddressingInformation.ADDRESSING_FORMAT == CanAddressingFormat.NORMAL_FIXED_ADDRESSING

    # ai_data_bytes_number

    def test_ai_data_bytes_number(self):
        assert NormalFixedCanAddressingInformation.AI_DATA_BYTES_NUMBER == 0

    # is_compatible_can_id

    @pytest.mark.parametrize("value", [CanIdHandler.NORMAL_FIXED_PHYSICAL_ADDRESSING_MASKED_VALUE
                                       + (CanIdHandler.MIN_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
                                       CanIdHandler.NORMAL_FIXED_PHYSICAL_ADDRESSING_MASKED_VALUE + 0x1234
                                       + (CanIdHandler.DEFAULT_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
                                       CanIdHandler.NORMAL_FIXED_PHYSICAL_ADDRESSING_MASKED_VALUE + 0xFFFF
                                       + (CanIdHandler.MAX_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
                                       CanIdHandler.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_MASKED_VALUE
                                       + (CanIdHandler.MIN_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
                                       CanIdHandler.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_MASKED_VALUE + 0xDEBA
                                       + (CanIdHandler.DEFAULT_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
                                       CanIdHandler.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_MASKED_VALUE + 0xFFFF
                                       + (CanIdHandler.MAX_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET)])
    def test_is_compatible_can_id__without_addressing__true(self, value):
        assert NormalFixedCanAddressingInformation.is_compatible_can_id(value) is True
        self.mock_validate_addressing_type.assert_not_called()

    @pytest.mark.parametrize("value", [CanIdHandler.NORMAL_FIXED_PHYSICAL_ADDRESSING_MASKED_VALUE
                                       + (CanIdHandler.MIN_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET) - 1,
                                       CanIdHandler.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_MASKED_VALUE +
                                       (CanIdHandler.MAX_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET) + 0x10000])
    def test_is_compatible_can_id__without_addressing__false(self, value):
        assert NormalFixedCanAddressingInformation.is_compatible_can_id(value) is False
        self.mock_validate_addressing_type.assert_not_called()

    @pytest.mark.parametrize("value, addressing_type", [
        (CanIdHandler.NORMAL_FIXED_PHYSICAL_ADDRESSING_MASKED_VALUE
         + (CanIdHandler.MIN_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
         AddressingType.PHYSICAL),
        (CanIdHandler.NORMAL_FIXED_PHYSICAL_ADDRESSING_MASKED_VALUE + 0x1234
         + (CanIdHandler.DEFAULT_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
         AddressingType.PHYSICAL),
        (CanIdHandler.NORMAL_FIXED_PHYSICAL_ADDRESSING_MASKED_VALUE + 0xFFFF
         + (CanIdHandler.MAX_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
         AddressingType.PHYSICAL),
        (CanIdHandler.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_MASKED_VALUE
         + (CanIdHandler.MIN_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
         AddressingType.FUNCTIONAL),
        (CanIdHandler.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_MASKED_VALUE + 0xDEBA
         + (CanIdHandler.DEFAULT_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
         AddressingType.FUNCTIONAL),
        (CanIdHandler.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_MASKED_VALUE + 0xFFFF
         + (CanIdHandler.MAX_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
         AddressingType.FUNCTIONAL),
    ])
    def test_is_compatible_can_id__with_addressing__true(self, value, addressing_type):
        self.mock_validate_addressing_type.return_value = addressing_type
        assert NormalFixedCanAddressingInformation.is_compatible_can_id(value, addressing_type=addressing_type) is True
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)

    @pytest.mark.parametrize("value, addressing_type", [
        (CanIdHandler.NORMAL_FIXED_PHYSICAL_ADDRESSING_MASKED_VALUE
         + (CanIdHandler.MIN_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET) - 1,
         AddressingType.PHYSICAL),
        (CanIdHandler.NORMAL_FIXED_PHYSICAL_ADDRESSING_MASKED_VALUE
         + (CanIdHandler.DEFAULT_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
         AddressingType.FUNCTIONAL),
        (CanIdHandler.NORMAL_FIXED_PHYSICAL_ADDRESSING_MASKED_VALUE + 0xFFFF
         + (CanIdHandler.MAX_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
         AddressingType.FUNCTIONAL),
        (CanIdHandler.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_MASKED_VALUE
         + (CanIdHandler.MIN_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
         AddressingType.PHYSICAL),
        (CanIdHandler.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_MASKED_VALUE + 0xFFFF
         + (CanIdHandler.DEFAULT_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
         AddressingType.PHYSICAL),
        (CanIdHandler.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_MASKED_VALUE + 0x10000
         + (CanIdHandler.MAX_PRIORITY_VALUE << CanIdHandler.PRIORITY_BIT_OFFSET),
         AddressingType.FUNCTIONAL),
        (0, AddressingType.PHYSICAL),
    ])
    def test_is_compatible_can_id__with_addressing__false(self, value, addressing_type):
        self.mock_validate_addressing_type.return_value = addressing_type
        assert NormalFixedCanAddressingInformation.is_compatible_can_id(value, addressing_type=addressing_type) is False
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)

    # decode_can_id

    @pytest.mark.parametrize("can_id", [0, 0x20000])
    @patch(f"{SCRIPT_LOCATION}.NormalFixedCanAddressingInformation.is_compatible_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.validate_can_id")
    def test_decode_can_id__not_implemented(self, mock_validate_can_id, mock_is_compatible_can_id, can_id):
        mock_is_compatible_can_id.return_value = True
        with pytest.raises(NotImplementedError):
            NormalFixedCanAddressingInformation.decode_can_id(can_id=can_id)
        mock_validate_can_id.assert_called_once_with(can_id)
        mock_is_compatible_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("can_id", [0xFFFFFFFFFFFF, "something"])
    @patch(f"{SCRIPT_LOCATION}.NormalFixedCanAddressingInformation.is_compatible_can_id")
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.validate_can_id")
    def test_decode_can_id__value_error(self, mock_validate_can_id, mock_is_compatible_can_id, can_id):
        mock_is_compatible_can_id.return_value = False
        with pytest.raises(ValueError):
            NormalFixedCanAddressingInformation.decode_can_id(can_id=can_id)
        mock_validate_can_id.assert_called_once_with(can_id)
        mock_is_compatible_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing_type, target_address, source_address, priority, can_id", [
        (AddressingType.PHYSICAL, 0x12, 0x34, 0b110, 0x18DA1234),
        (AddressingType.FUNCTIONAL, 0xFE, 0xDC, 0b110, 0x18DBFEDC),
        (AddressingType.PHYSICAL, 0x00, 0xFF, 0b000, 0xDA00FF),
        (AddressingType.FUNCTIONAL, 0xFF, 0x00, 0b111, 0x1CDBFF00),
    ])
    def test_decode_can_id__valid(self, addressing_type, target_address, source_address, priority, can_id):
        assert NormalFixedCanAddressingInformation.decode_can_id(can_id=can_id) == {
            "addressing_type": addressing_type,
            "target_address": target_address,
            "source_address": source_address,
            "priority": priority,
        }

    # encode_can_id

    @pytest.mark.parametrize("addressing_type, target_address, source_address", [
        (Mock(), 0x55, 0xAA),
        ("something not handled", 0x00, 0xFF)
    ])
    def test_encode_can_id__not_implemented(self, addressing_type, target_address, source_address):
        self.mock_validate_addressing_type.return_value = addressing_type
        with pytest.raises(NotImplementedError):
            NormalFixedCanAddressingInformation.encode_can_id(addressing_type=addressing_type,
                                                              target_address=target_address,
                                                              source_address=source_address)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)

    @pytest.mark.parametrize("addressing_type, target_address, source_address, expected_can_id", [
        (AddressingType.PHYSICAL, 0x12, 0x34, 0x18DA1234),
        (AddressingType.FUNCTIONAL, 0xFE, 0xDC, 0x18DBFEDC),
        (AddressingType.PHYSICAL, 0x00, 0xFF, 0x18DA00FF),
        (AddressingType.FUNCTIONAL, 0xFF, 0x00, 0x18DBFF00),
    ])
    def test_encode_can_id__valid_without_priority(self, addressing_type, target_address, source_address,
                                                   expected_can_id):
        self.mock_validate_addressing_type.return_value = addressing_type
        assert NormalFixedCanAddressingInformation.encode_can_id(addressing_type=addressing_type,
                                                                 target_address=target_address,
                                                                 source_address=source_address) == expected_can_id
        self.mock_validate_raw_byte.assert_has_calls([call(target_address), call(source_address)], any_order=True)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)

    @pytest.mark.parametrize("addressing_type, priority, target_address, source_address, expected_can_id", [
        (AddressingType.PHYSICAL, 0b000, 0x12, 0x34, 0xDA1234),
        (AddressingType.FUNCTIONAL, 0b011, 0xFE, 0xDC, 0xCDBFEDC),
        (AddressingType.PHYSICAL, 0b101, 0x00, 0xFF, 0x14DA00FF),
        (AddressingType.FUNCTIONAL, 0b111, 0xFF, 0x00, 0x1CDBFF00),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanIdHandler.validate_priority")
    def test_encode_can_id__valid_with_priority(self, mock_validate_priority,
                                                addressing_type, priority, target_address, source_address,
                                                expected_can_id):
        self.mock_validate_addressing_type.return_value = addressing_type
        assert NormalFixedCanAddressingInformation.encode_can_id(addressing_type=addressing_type,
                                                                 target_address=target_address,
                                                                 source_address=source_address,
                                                                 priority=priority) == expected_can_id
        self.mock_validate_raw_byte.assert_has_calls([call(target_address), call(source_address)], any_order=True)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
        mock_validate_priority.assert_called_once_with(priority)

    # validate_addressing_params

    @pytest.mark.parametrize("addressing_format", [
        Mock(),
        CanAddressingFormat.EXTENDED_ADDRESSING,
    ])
    def test_validate_addressing_params__value_error(self, addressing_format):
        with pytest.raises(ValueError):
            NormalFixedCanAddressingInformation.validate_addressing_params(addressing_type=Mock(),
                                                                           can_id=Mock(),
                                                                           addressing_format=addressing_format)

    @pytest.mark.parametrize("unsupported_args", [
        {"address_extension": Mock()},
    ])
    def test_validate_addressing_params__unused_args(self, unsupported_args):
        with pytest.raises(UnusedArgumentError):
            NormalFixedCanAddressingInformation.validate_addressing_params(addressing_type=Mock(),
                                                                           can_id=Mock(),
                                                                           **unsupported_args)

    @pytest.mark.parametrize("addressing_type, can_id, target_address, source_address", [
        (Mock(), None, None, 0),
        (AddressingType.PHYSICAL, None, 0x05, None),
        (AddressingType.FUNCTIONAL, None, None, None),
    ])
    def test_validate_addressing_params__inconsistent__missing_info(self, addressing_type, can_id, target_address, source_address):
        self.mock_validate_addressing_type.return_value = addressing_type
        with pytest.raises(InconsistentArgumentsError):
            NormalFixedCanAddressingInformation.validate_addressing_params(addressing_type=addressing_type,
                                                                           can_id=can_id,
                                                                           target_address=target_address,
                                                                           source_address=source_address)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)

    @pytest.mark.parametrize("addressing_type, decoded_addressing_type, ta, decoded_ta, sa, decoded_sa, can_id", [
        (AddressingType.FUNCTIONAL, AddressingType.FUNCTIONAL, 0x56, 0x55, None, 0x10, Mock()),
        (AddressingType.PHYSICAL, AddressingType.PHYSICAL, None, 0x55, 0x9F, 0x10, 0x123456),
        ("something", "something else", 0x01, 0x01, 0xF0, 0xF0, 0x556677),
    ])
    @patch(f"{SCRIPT_LOCATION}.NormalFixedCanAddressingInformation.decode_can_id")
    def test_validate_addressing_params__inconsistent(self, mock_decode_can_id,
                                                      addressing_type, decoded_addressing_type,
                                                      ta, decoded_ta, sa, decoded_sa, can_id):
        self.mock_validate_addressing_type.return_value = addressing_type
        mock_decode_can_id.return_value = {
            "addressing_type": decoded_addressing_type,
            "target_address": decoded_ta,
            "source_address": decoded_sa
        }
        with pytest.raises(InconsistentArgumentsError):
            NormalFixedCanAddressingInformation.validate_addressing_params(addressing_type=addressing_type,
                                                                           can_id=can_id,
                                                                           target_address=ta,
                                                                           source_address=sa)
        mock_decode_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing_type, target_address, source_address", [
        (Mock(), Mock(), Mock()),
        (AddressingType.PHYSICAL, 0xAA, 0x55),
    ])
    @patch(f"{SCRIPT_LOCATION}.NormalFixedCanAddressingInformation.encode_can_id")
    def test_validate_addressing_params__valid_without_can_id(self, mock_encode_can_id,
                                                              addressing_type, target_address, source_address):
        assert NormalFixedCanAddressingInformation.validate_addressing_params(addressing_type=addressing_type,
                                                                              can_id=None,
                                                                              target_address=target_address,
                                                                              source_address=source_address) == {
            "addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
            "addressing_type": self.mock_validate_addressing_type.return_value,
            "can_id": mock_encode_can_id.return_value,
            "target_address": target_address,
            "source_address": source_address,
            "address_extension": None,
        }
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
        self.mock_validate_raw_byte.assert_has_calls([call(target_address), call(source_address)], any_order=True)
        mock_encode_can_id.assert_called_once_with(addressing_type=self.mock_validate_addressing_type.return_value,
                                                   target_address=target_address,
                                                   source_address=source_address)

    @pytest.mark.parametrize("addressing_type, target_address, source_address, can_id", [
        [Mock(), Mock(), Mock(), Mock()],
        [AddressingType.PHYSICAL, None, None, 0x67234],
        [AddressingType.FUNCTIONAL, 0x00, None, 0x67234],
        [AddressingType.FUNCTIONAL, None, 0xFF, 0x67234],
    ])
    @patch(f"{SCRIPT_LOCATION}.NormalFixedCanAddressingInformation.decode_can_id")
    def test_validate_addressing_params__valid_with_can_id(self, mock_decode_can_id,
                                                           addressing_type, target_address, source_address, can_id):
        decoded_target_address = target_address if target_address is not None else Mock()
        decoded_source_address = source_address if source_address is not None else Mock()
        mock_decode_can_id.return_value = {
            "addressing_type": self.mock_validate_addressing_type.return_value,
            "target_address": decoded_target_address,
            "source_address": decoded_source_address
        }
        assert NormalFixedCanAddressingInformation.validate_addressing_params(addressing_type=addressing_type,
                                                                              can_id=can_id,
                                                                              target_address=target_address,
                                                                              source_address=source_address) == {
                   "addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                   "addressing_type": self.mock_validate_addressing_type.return_value,
                   "can_id": can_id,
                   "target_address": decoded_target_address,
                   "source_address": decoded_source_address,
                   "address_extension": None,
               }
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
        self.mock_validate_raw_byte.assert_not_called()
        mock_decode_can_id.assert_called_once_with(can_id)

    # _validate_addressing_information

    @pytest.mark.parametrize("rx_physical_params, tx_physical_params, "
                             "rx_functional_params, tx_functional_params", [
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
    def test_validate_addressing_information__inconsistent(self, rx_physical_params, tx_physical_params,
                                                           rx_functional_params, tx_functional_params):
        self.mock_addressing_information.rx_physical_params = rx_physical_params
        self.mock_addressing_information.tx_physical_params = tx_physical_params
        self.mock_addressing_information.rx_functional_params = rx_functional_params
        self.mock_addressing_information.tx_functional_params = tx_functional_params
        with pytest.raises(InconsistentArgumentsError):
            NormalFixedCanAddressingInformation._validate_addressing_information(self.mock_addressing_information)

    @pytest.mark.parametrize("rx_physical_params, tx_physical_params, "
                             "rx_functional_params, tx_functional_params", [
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
            {"can_id": 0x8DB5580, "target_address": 0x2F, "source_address": 0x71},
            {"can_id": 0x8DB8055, "target_address": 0x71, "source_address": 0x2F},
        ),
    ])
    def test_validate_addressing_information__valid(self, rx_physical_params, tx_physical_params,
                                                           rx_functional_params, tx_functional_params):
        self.mock_addressing_information.rx_physical_params = rx_physical_params
        self.mock_addressing_information.tx_physical_params = tx_physical_params
        self.mock_addressing_information.rx_functional_params = rx_functional_params
        self.mock_addressing_information.tx_functional_params = tx_functional_params
        assert NormalFixedCanAddressingInformation._validate_addressing_information(
            self.mock_addressing_information) is None

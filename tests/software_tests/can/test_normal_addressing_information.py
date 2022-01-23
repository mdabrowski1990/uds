import pytest
from mock import Mock, patch, call

from uds.can.normal_addressing_information import Normal11BitCanAddressingInformation, NormalFixedCanAddressingInformation, \
    CanAddressingFormat, InconsistentArgumentsError


class TestNormal11BitCanAddressingInformation:
    """Unit tests for `Normal11BitCanAddressingInformation` class."""

    SCRIPT_LOCATION = "uds.can.normal_addressing_information"

    def setup(self):
        self.mock_addressing_information = Mock(spec=Normal11BitCanAddressingInformation)
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
        assert Normal11BitCanAddressingInformation.addressing_format.fget(self.mock_addressing_information) \
               == CanAddressingFormat.NORMAL_11BIT_ADDRESSING

    # validate_packet_ai

    @pytest.mark.parametrize("addressing_type, can_id", [
        ("some addressing type", "some id"),
        (Mock(), 0x7FF),
    ])
    def test_validate_packet_ai__invalid_can_id(self, addressing_type, can_id):
        self.mock_can_id_handler_class.is_normal_11bit_addressed_can_id.return_value = False
        with pytest.raises(InconsistentArgumentsError):
            Normal11BitCanAddressingInformation.validate_packet_ai(addressing_type=addressing_type,
                                                                   can_id=can_id)
        self.mock_can_id_handler_class.validate_can_id.assert_called_once_with(can_id)
        self.mock_can_id_handler_class.is_normal_11bit_addressed_can_id.assert_called_once_with(can_id)

    @pytest.mark.parametrize("addressing_type, can_id", [
        ("some addressing type", "some id"),
        (Mock(), 0x7FF),
    ])
    def test_validate_packet_ai__valid(self, addressing_type, can_id):
        self.mock_can_id_handler_class.is_normal_11bit_addressed_can_id.return_value = True
        Normal11BitCanAddressingInformation.validate_packet_ai(addressing_type=addressing_type,
                                                               can_id=can_id)
        self.mock_can_id_handler_class.validate_can_id.assert_called_once_with(can_id)
        self.mock_can_id_handler_class.is_normal_11bit_addressed_can_id.assert_called_once_with(can_id)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)


class TestNormalFixedCanAddressingInformation:
    """Unit tests for `NormalFixedCanAddressingInformation` class."""

    SCRIPT_LOCATION = TestNormal11BitCanAddressingInformation.SCRIPT_LOCATION

    def setup(self):
        self.mock_addressing_information = Mock(spec=NormalFixedCanAddressingInformation)
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
        assert NormalFixedCanAddressingInformation.addressing_format.fget(self.mock_addressing_information) \
               == CanAddressingFormat.NORMAL_FIXED_ADDRESSING

    # validate_packet_ai

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
        (Mock(), Mock(), None, 0x55, 0x7F, 0x80),
        ("something", "something else", None, 0x55, None, 0x10),
        ("something", "something", 0x56, 0x55, None, 0x10),
        ("something", "something else", 0x56, 0x55, 0x7F, 0x10),
    ])
    def test_validate_packet_ai__inconsistent_can_id_ta_sa(self, can_id, addressing_type, decoded_addressing_type,
                                                           ta, decoded_ta, sa, decoded_sa):
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
        NormalFixedCanAddressingInformation.validate_packet_ai(addressing_type=addressing_type,
                                                               can_id=None,
                                                               target_address=target_address,
                                                               source_address=source_address)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
        self.mock_validate_raw_byte.assert_has_calls([call(target_address), call(source_address)], any_order=True)
        self.mock_can_id_handler_class.validate_can_id.assert_not_called()
        self.mock_can_id_handler_class.decode_normal_fixed_addressed_can_id.assert_not_called()

    @pytest.mark.parametrize("addressing_type", ["some addressing type", Mock()])
    @pytest.mark.parametrize("can_id", ["some CAN ID", 0x85421])
    @pytest.mark.parametrize("target_address, source_address", [
        (None, None),
        (0x12, None),
        (None, 0x34),
        ("ta", "sa"),
    ])
    def test_validate_packet_ai__valid_with_can_id(self, addressing_type, can_id, target_address, source_address):
        self.mock_can_id_handler_class.decode_normal_fixed_addressed_can_id.return_value = {
            self.mock_can_id_handler_class.ADDRESSING_TYPE_NAME: addressing_type,
            self.mock_can_id_handler_class.TARGET_ADDRESS_NAME: target_address or "ta",
            self.mock_can_id_handler_class.SOURCE_ADDRESS_NAME: source_address or "sa",
        }
        NormalFixedCanAddressingInformation.validate_packet_ai(addressing_type=addressing_type,
                                                               can_id=can_id,
                                                               target_address=target_address,
                                                               source_address=source_address)
        self.mock_validate_addressing_type.assert_called_once_with(addressing_type)
        self.mock_validate_raw_byte.assert_not_called()
        self.mock_can_id_handler_class.decode_normal_fixed_addressed_can_id.assert_called_once_with(can_id)

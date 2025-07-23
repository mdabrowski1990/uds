import pytest
from mock import MagicMock, Mock, patch

from uds.can.addressing.addressing_information import (
    AddressingType,
    CanAddressingFormat,
    CanAddressingInformation,
    CanIdHandler,
    InconsistentArgumentsError,
)

SCRIPT_LOCATION = "uds.can.addressing.addressing_information"


class TestCanAddressingInformation:
    """Unit tests for `CanAddressingInformation` class."""

    def setup_method(self):
        # patching
        self._patcher_validate_addressing_format = patch(f"{SCRIPT_LOCATION}.CanAddressingFormat.validate_member")
        self.mock_validate_addressing_format = self._patcher_validate_addressing_format.start()
        self._patcher_validate_raw_bytes = patch(f"{SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
        self._patcher_validate_raw_byte = patch(f"{SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()

    def teardown_method(self):
        self._patcher_validate_addressing_format.stop()
        self._patcher_validate_raw_bytes.stop()
        self._patcher_validate_raw_byte.stop()

    # __new__

    @pytest.mark.parametrize("addressing_format, "
                             "rx_physical_params, tx_physical_params, rx_functional_params, tx_functional_params", [
        (Mock(), Mock(), Mock(), Mock(), Mock()),
        (CanAddressingFormat.NORMAL_ADDRESSING, {"can_id": 1}, {"can_id": 2}, {"can_id": 3}, {"can_id": 4}),
    ])
    def test_new(self, addressing_format, rx_physical_params, tx_physical_params, rx_functional_params, tx_functional_params):
        mock_returned_class = Mock()
        mock_getitem = Mock(return_value=mock_returned_class)
        mock_cls = Mock(ADDRESSING_INFORMATION_MAPPING=MagicMock(__getitem__=mock_getitem))
        assert CanAddressingInformation.__new__(cls=mock_cls,
                                                addressing_format=addressing_format,
                                                rx_physical_params=rx_physical_params,
                                                tx_physical_params=tx_physical_params,
                                                rx_functional_params=rx_functional_params,
                                                tx_functional_params=tx_functional_params) == mock_returned_class.return_value
        mock_getitem.assert_called_once_with(addressing_format)
        mock_returned_class.assert_called_once_with(rx_physical_params=rx_physical_params,
                                                    tx_physical_params=tx_physical_params,
                                                    rx_functional_params=rx_functional_params,
                                                    tx_functional_params=tx_functional_params)

    # get_ai_data_bytes_number

    @pytest.mark.parametrize("addressing_format", [Mock(), AddressingType.PHYSICAL])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.ADDRESSING_INFORMATION_MAPPING")
    def test_get_ai_data_bytes_number(self, mock_ai_mapping, addressing_format):
        assert CanAddressingInformation.get_ai_data_bytes_number(addressing_format=addressing_format) \
               == mock_ai_mapping.__getitem__.return_value.AI_DATA_BYTES_NUMBER
        mock_ai_mapping.__getitem__.assert_called_once_with(addressing_format)

    # is_compatible_can_id

    @pytest.mark.parametrize("addressing_format, can_id, addressing_type", [
        (Mock(), Mock(), Mock()),
        (CanAddressingFormat.NORMAL_ADDRESSING, 0x7DF, AddressingType.PHYSICAL),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.ADDRESSING_INFORMATION_MAPPING")
    def test_is_compatible_can_id__with_addressing_type(self, mock_ai_mapping,
                                                        addressing_format, can_id, addressing_type):
        assert (CanAddressingInformation.is_compatible_can_id(addressing_format=addressing_format,
                                                             can_id=can_id,
                                                             addressing_type=addressing_type)
                == mock_ai_mapping.__getitem__.return_value.is_compatible_can_id.return_value)
        mock_ai_mapping.__getitem__.assert_called_once_with(addressing_format)
        mock_ai_mapping.__getitem__.return_value.is_compatible_can_id.assert_called_once_with(
            can_id=can_id, addressing_type=addressing_type)

    @pytest.mark.parametrize("addressing_format, can_id", [
        (Mock(), Mock()),
        (CanAddressingFormat.NORMAL_ADDRESSING, 0x7DF),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.ADDRESSING_INFORMATION_MAPPING")
    def test_is_compatible_can_id__without_addressing_type(self, mock_ai_mapping,
                                                        addressing_format, can_id):
        assert (CanAddressingInformation.is_compatible_can_id(addressing_format=addressing_format,
                                                             can_id=can_id)
                == mock_ai_mapping.__getitem__.return_value.is_compatible_can_id.return_value)
        mock_ai_mapping.__getitem__.assert_called_once_with(addressing_format)
        mock_ai_mapping.__getitem__.return_value.is_compatible_can_id.assert_called_once_with(
            can_id=can_id, addressing_type=None)

    # decode_can_id_ai_params

    @pytest.mark.parametrize("addressing_format, can_id", [
        (Mock(), Mock()),
        (AddressingType.PHYSICAL, 0x85431),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.ADDRESSING_INFORMATION_MAPPING")
    def test_decode_can_id_ai_params(self, mock_ai_mapping, addressing_format, can_id):
        assert (CanAddressingInformation.decode_can_id_ai_params(addressing_format=addressing_format, can_id=can_id)
                == mock_ai_mapping.__getitem__.return_value.decode_can_id_ai_params.return_value)
        mock_ai_mapping.__getitem__.assert_called_once_with(addressing_format)
        mock_ai_mapping.__getitem__.return_value.decode_can_id_ai_params.assert_called_once_with(can_id)

    # decode_data_bytes_ai_params

    @pytest.mark.parametrize("addressing_format, ai_data_bytes", [
        (Mock(), Mock()),
        (AddressingType.PHYSICAL, [0xB9]),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.ADDRESSING_INFORMATION_MAPPING")
    def test_decode_data_bytes_ai_params(self, mock_ai_mapping, addressing_format, ai_data_bytes):
        assert (CanAddressingInformation.decode_data_bytes_ai_params(addressing_format=addressing_format,
                                                                     ai_data_bytes=ai_data_bytes)
                == mock_ai_mapping.__getitem__.return_value.decode_data_bytes_ai_params.return_value)
        mock_ai_mapping.__getitem__.assert_called_once_with(addressing_format)
        mock_ai_mapping.__getitem__.return_value.decode_data_bytes_ai_params.assert_called_once_with(ai_data_bytes)

    # decode_frame_ai_params

    @pytest.mark.parametrize("addressing_format, can_id, ai_data_bytes", [
        (Mock(), Mock(), Mock()),
        (AddressingType.PHYSICAL, 0x123, [0xB9]),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.ADDRESSING_INFORMATION_MAPPING")
    def test_decode_frame_ai_params(self, mock_ai_mapping, addressing_format, can_id, ai_data_bytes):
        assert (CanAddressingInformation.decode_frame_ai_params(addressing_format=addressing_format,
                                                                can_id=can_id,
                                                                ai_data_bytes=ai_data_bytes)
                == mock_ai_mapping.__getitem__.return_value.decode_frame_ai_params.return_value)
        mock_ai_mapping.__getitem__.assert_called_once_with(addressing_format)
        mock_ai_mapping.__getitem__.return_value.decode_frame_ai_params.assert_called_once_with(
            can_id=can_id, ai_data_bytes=ai_data_bytes)

    # encode_can_id

    @pytest.mark.parametrize("params", [
        {"addressing_type": Mock(), "target_address": Mock(), "source_address": Mock(), "priority": Mock()},
        {"addressing_type": AddressingType.PHYSICAL, "target_address": 0x00, "source_address": 0xFF},
    ])
    @patch(f"{SCRIPT_LOCATION}.NormalFixedCanAddressingInformation.encode_can_id")
    def test_encode_can_id__normal_fixed(self, mock_encode_normal_fixed_can_id, params):
        assert CanAddressingInformation.encode_can_id(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                                      **params) == mock_encode_normal_fixed_can_id.return_value
        if "priority" in params:
            mock_encode_normal_fixed_can_id.assert_called_once_with(**params)
        else:
            mock_encode_normal_fixed_can_id.assert_called_once_with(**params,
                                                                    priority=CanIdHandler.DEFAULT_PRIORITY_VALUE)

    @pytest.mark.parametrize("params", [
        {"addressing_type": Mock(), "target_address": Mock(), "source_address": Mock(), "priority": Mock()},
        {"addressing_type": AddressingType.PHYSICAL, "target_address": 0x00, "source_address": 0xFF},
    ])
    @patch(f"{SCRIPT_LOCATION}.Mixed29BitCanAddressingInformation.encode_can_id")
    def test_encode_can_id__mixed_29bit(self, mock_encode_normal_fixed_can_id, params):
        assert CanAddressingInformation.encode_can_id(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                                      **params) == mock_encode_normal_fixed_can_id.return_value
        if "priority" in params:
            mock_encode_normal_fixed_can_id.assert_called_once_with(**params)
        else:
            mock_encode_normal_fixed_can_id.assert_called_once_with(**params,
                                                                    priority=CanIdHandler.DEFAULT_PRIORITY_VALUE)

    @pytest.mark.parametrize("addressing_format", [
        CanAddressingFormat.NORMAL_ADDRESSING,
        CanAddressingFormat.EXTENDED_ADDRESSING,
        CanAddressingFormat.MIXED_11BIT_ADDRESSING,
        Mock()
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.ADDRESSING_INFORMATION_MAPPING")
    def test_encode_can_id__value_error(self, mock_ai_mapping, addressing_format):
        with pytest.raises(ValueError):
            CanAddressingInformation.encode_can_id(addressing_format=addressing_format,
                                                   addressing_type=Mock(),
                                                   target_address=Mock(),
                                                   source_address=Mock())
        mock_ai_mapping.__getitem__.assert_not_called()

    # validate_addressing_params

    @pytest.mark.parametrize("params", [
        {
            "addressing_format": Mock(),
            "addressing_type": Mock(),
            "can_id": Mock(),
            "target_address": Mock(),
            "source_address": Mock(),
            "address_extension": Mock(),
        },
        {
            "addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
            "addressing_type": AddressingType.PHYSICAL,
            "can_id": 0x123,
        },
        {
            "addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
            "addressing_type": AddressingType.FUNCTIONAL,
            "target_address": 0xF0,
            "source_address": 0x1E,
            "address_extension": 0x8C,
        },
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.ADDRESSING_INFORMATION_MAPPING")
    def test_validate_addressing_params(self, mock_ai_mapping, params):
        mock_returned_class = Mock()
        mock_getitem = Mock(return_value=mock_returned_class)
        mock_ai_mapping.__getitem__ = mock_getitem
        assert CanAddressingInformation.validate_addressing_params(**params) \
               == mock_returned_class.validate_addressing_params.return_value
        mock_getitem.assert_called_once_with(params["addressing_format"])
        passed_params = {
            "addressing_format": params["addressing_format"],
            "addressing_type": params["addressing_type"],
            "can_id": params.get("can_id", None),
            "target_address": params.get("target_address", None),
            "source_address": params.get("source_address", None),
            "address_extension": params.get("address_extension", None),
        }
        mock_returned_class.validate_addressing_params.assert_called_once_with(**passed_params)
        self.mock_validate_addressing_format.assert_called_once_with(params["addressing_format"])

    # validate_ai_data_bytes

    @pytest.mark.parametrize("addressing_format, ai_data_bytes", [
        (Mock(), MagicMock()),
        (CanAddressingFormat.EXTENDED_ADDRESSING, b"\x01"),
        (CanAddressingFormat.NORMAL_ADDRESSING, []),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.get_ai_data_bytes_number")
    def test_validate_ai_data_bytes__valid(self, mock_get_ai_data_bytes_number, addressing_format, ai_data_bytes):
        mock_get_ai_data_bytes_number.return_value = len(ai_data_bytes)
        assert CanAddressingInformation.validate_ai_data_bytes(addressing_format=addressing_format,
                                                               ai_data_bytes=ai_data_bytes) is None
        mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        self.mock_validate_raw_bytes.assert_called_once_with(ai_data_bytes, allow_empty=True)
        self.mock_validate_addressing_format.assert_called_once_with(addressing_format)

    @pytest.mark.parametrize("addressing_format, ai_data_bytes, expected_ai_bytes_number", [
        (CanAddressingFormat.EXTENDED_ADDRESSING, b"\x01", 0),
        (CanAddressingFormat.NORMAL_ADDRESSING, [], 1),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.get_ai_data_bytes_number")
    def test_validate_ai_data_bytes__inconsistent(self, mock_get_ai_data_bytes_number,
                                                  addressing_format, ai_data_bytes, expected_ai_bytes_number):
        mock_get_ai_data_bytes_number.return_value = expected_ai_bytes_number
        with pytest.raises(InconsistentArgumentsError):
            CanAddressingInformation.validate_ai_data_bytes(addressing_format=addressing_format,
                                                            ai_data_bytes=ai_data_bytes)
        mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        self.mock_validate_raw_bytes.assert_called_once_with(ai_data_bytes, allow_empty=True)
        self.mock_validate_addressing_format.assert_called_once_with(addressing_format)

    # decode_packet_ai

    @pytest.mark.parametrize("addressing_format, can_id, ai_data_bytes, from_data_bytes, from_can_id", [
        (Mock(), Mock(), Mock(), MagicMock(), MagicMock()),
        (CanAddressingFormat.NORMAL_ADDRESSING, 0x543, b"\x22",
         {"addressing_type": "some crap", "source_address": "some crap"}, {"address_extension": "some crap"}),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, 0x18CD8523, b"\x92", {"address_extension": 0xFE},
         {"addressing_type": AddressingType.PHYSICAL, "target_address": 0xBB}),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, 0xED8523, [], {"target_address": 0x54}, {"source_address": 0xA1}),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.decode_ai_data_bytes")
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.decode_can_id_ai_params")
    def test_decode_ai(self, mock_decode_can_id_ai_params, mock_decode_ai_data_bytes,
                       addressing_format, can_id, ai_data_bytes, from_data_bytes, from_can_id):
        mock_decode_ai_data_bytes.return_value = from_data_bytes
        mock_decode_can_id_ai_params.return_value = from_can_id
        assert (CanAddressingInformation.decode_packet_ai(addressing_format=addressing_format,
                                                          can_id=can_id,
                                                          ai_data_bytes=ai_data_bytes)
                == CanAddressingInformation.DecodedAIParamsAlias(
                    addressing_type=from_can_id.get("addressing_type", None),
                    target_address=from_data_bytes.get("target_address", from_can_id.get("target_address", None)),
                    source_address=from_can_id.get("source_address"),
                    address_extension=from_data_bytes.get("address_extension")))
        mock_decode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                          ai_data_bytes=ai_data_bytes)
        mock_decode_can_id_ai_params.assert_called_once_with(addressing_format=addressing_format,
                                                   can_id=can_id)

    # decode_ai_data_bytes

    @pytest.mark.parametrize("addressing_format, ai_data_bytes", [
        (Mock(), Mock()),
        ("Unknown", []),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.validate_ai_data_bytes")
    def test_decode_ai_data_bytes__not_implemented(self, mock_validate_ai_data_bytes,
                                                   addressing_format, ai_data_bytes):
        with pytest.raises(NotImplementedError):
            CanAddressingInformation.decode_ai_data_bytes(addressing_format=addressing_format,
                                                          ai_data_bytes=ai_data_bytes)
        mock_validate_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                            ai_data_bytes=ai_data_bytes)

    @pytest.mark.parametrize("addressing_format, ai_data_bytes", [
        (CanAddressingFormat.NORMAL_ADDRESSING, Mock()),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, []),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.validate_ai_data_bytes")
    def test_decode_ai_data_bytes__normal(self, mock_validate_ai_data_bytes, addressing_format, ai_data_bytes):
        assert CanAddressingInformation.decode_ai_data_bytes(addressing_format=addressing_format,
                                                             ai_data_bytes=ai_data_bytes) == {}
        mock_validate_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                            ai_data_bytes=ai_data_bytes)

    @pytest.mark.parametrize("ai_data_bytes", [[0x0A], b"\xCF"])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.validate_ai_data_bytes")
    def test_decode_ai_data_bytes__extended(self, mock_validate_ai_data_bytes, ai_data_bytes):
        assert CanAddressingInformation.decode_ai_data_bytes(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                                             ai_data_bytes=ai_data_bytes) == {
            "target_address": ai_data_bytes[0]
        }
        mock_validate_ai_data_bytes.assert_called_once_with(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                                            ai_data_bytes=ai_data_bytes)

    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                                   CanAddressingFormat.MIXED_29BIT_ADDRESSING])
    @pytest.mark.parametrize("ai_data_bytes", [[0x0A], b"\xCF"])
    @patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.validate_ai_data_bytes")
    def test_decode_ai_data_bytes__mixed(self, mock_validate_ai_data_bytes, addressing_format, ai_data_bytes):
        assert CanAddressingInformation.decode_ai_data_bytes(addressing_format=addressing_format,
                                                             ai_data_bytes=ai_data_bytes) == {
            "address_extension": ai_data_bytes[0]
        }
        mock_validate_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                            ai_data_bytes=ai_data_bytes)

    # encode_ai_data_bytes

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        (CanAddressingFormat.NORMAL_ADDRESSING, None, None),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, 0x5B, 0x9E)
    ])
    def test_encode_ai_data_bytes__normal(self, addressing_format, target_address, address_extension):
        assert CanAddressingInformation.encode_ai_data_bytes(addressing_format=addressing_format,
                                                             address_extension=address_extension,
                                                             target_address=target_address) == bytearray()
        self.mock_validate_addressing_format.assert_called_once_with(addressing_format)
        self.mock_validate_raw_byte.assert_not_called()

    @pytest.mark.parametrize("target_address, address_extension", [
        (0xFF, 0x00),
        (0x5B, None),
    ])
    def test_encode_ai_data_bytes__extended(self, target_address, address_extension):
        assert CanAddressingInformation.encode_ai_data_bytes(
            addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
            address_extension=address_extension,
            target_address=target_address) == bytearray([target_address])
        self.mock_validate_addressing_format.assert_called_once_with(CanAddressingFormat.EXTENDED_ADDRESSING)
        self.mock_validate_raw_byte.assert_called_once_with(target_address)

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, None, 0xFF),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, 0x5B, 0x9E),
    ])
    def test_encode_ai_data_bytes__mixed(self, addressing_format, target_address, address_extension):
        assert CanAddressingInformation.encode_ai_data_bytes(
            addressing_format=addressing_format,
            address_extension=address_extension,
            target_address=target_address) == bytearray([address_extension])
        self.mock_validate_addressing_format.assert_called_once_with(addressing_format)
        self.mock_validate_raw_byte.assert_called_once_with(address_extension)

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        (Mock(), Mock(), Mock()),
        ("Unknown", 0x53, 0x43),
    ])
    def test_encode_ai_data_bytes__unknown(self, addressing_format, target_address, address_extension):
        with pytest.raises(NotImplementedError):
            CanAddressingInformation.encode_ai_data_bytes(addressing_format=addressing_format,
                                                          address_extension=address_extension,
                                                          target_address=target_address)
        self.mock_validate_addressing_format.assert_called_once_with(addressing_format)
        self.mock_validate_raw_byte.assert_not_called()


@pytest.mark.integration
class TestCanAddressingInformationIntegration:
    """Integration tests for `CanAddressingInformation` class."""

    @pytest.mark.parametrize("input_params, expected_attributes", [
        # Normal
        ({"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
          "rx_physical_params": {"can_id": 0x601},
          "tx_physical_params": {"can_id": 0x602},
          "rx_functional_params": {"can_id": 0x6FE},
          "tx_functional_params": {"can_id": 0x6FF}},
         {"rx_physical_params": {"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
                                 "addressing_type": AddressingType.PHYSICAL,
                                 "can_id": 0x601,
                                 "target_address": None,
                                 "source_address": None,
                                 "address_extension": None},
          "tx_physical_params": {"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
                                 "addressing_type": AddressingType.PHYSICAL,
                                 "can_id": 0x602,
                                 "target_address": None,
                                 "source_address": None,
                                 "address_extension": None},
          "rx_functional_params": {"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
                                   "addressing_type": AddressingType.FUNCTIONAL,
                                   "can_id": 0x6FE,
                                   "target_address": None,
                                   "source_address": None,
                                   "address_extension": None},
          "tx_functional_params": {"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
                                   "addressing_type": AddressingType.FUNCTIONAL,
                                   "can_id": 0x6FF,
                                   "target_address": None,
                                   "source_address": None,
                                   "address_extension": None}}),
        ({"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
          "rx_physical_params": {"can_id": 0x1},
          "tx_physical_params": {"can_id": 0x2},
          "rx_functional_params": {"can_id": 0x1FFFFFFE},
          "tx_functional_params": {"can_id": 0x1FFFFFFF}},
         {"rx_physical_params": {"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
                                 "addressing_type": AddressingType.PHYSICAL,
                                 "can_id": 0x1,
                                 "target_address": None,
                                 "source_address": None,
                                 "address_extension": None},
          "tx_physical_params": {"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
                                 "addressing_type": AddressingType.PHYSICAL,
                                 "can_id": 0x2,
                                 "target_address": None,
                                 "source_address": None,
                                 "address_extension": None},
          "rx_functional_params": {"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
                                   "addressing_type": AddressingType.FUNCTIONAL,
                                   "can_id": 0x1FFFFFFE,
                                   "target_address": None,
                                   "source_address": None,
                                   "address_extension": None},
          "tx_functional_params": {"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
                                   "addressing_type": AddressingType.FUNCTIONAL,
                                   "can_id": 0x1FFFFFFF,
                                   "target_address": None,
                                   "source_address": None,
                                   "address_extension": None}}),
        # Normal Fixed
        ({"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "rx_physical_params": {"can_id": 0x18DA0E2B},
          "tx_physical_params": {"target_address": 0x2B, "source_address": 0x0E},
          "rx_functional_params": {"can_id": 0x18DBFEDC, "target_address": 0xFE},
          "tx_functional_params": {"can_id": 0x18DBDCFE, "target_address": 0xDC, "source_address": 0xFE}},
         {"rx_physical_params": {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                 "addressing_type": AddressingType.PHYSICAL,
                                 "can_id": 0x18DA0E2B,
                                 "target_address": 0x0E,
                                 "source_address": 0x2B,
                                 "address_extension": None},
          "tx_physical_params": {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                 "addressing_type": AddressingType.PHYSICAL,
                                 "can_id": 0x18DA2B0E,
                                 "target_address": 0x2B,
                                 "source_address": 0x0E,
                                 "address_extension": None},
          "rx_functional_params": {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                   "addressing_type": AddressingType.FUNCTIONAL,
                                   "can_id": 0x18DBFEDC,
                                   "target_address": 0xFE,
                                   "source_address": 0xDC,
                                   "address_extension": None},
          "tx_functional_params": {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                   "addressing_type": AddressingType.FUNCTIONAL,
                                   "can_id": 0x18DBDCFE,
                                   "target_address": 0xDC,
                                   "source_address": 0xFE,
                                   "address_extension": None}}),
        ({"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "rx_physical_params": {"can_id": 0xDA00FF},
          "tx_physical_params": {"can_id": 0xDAFF00},
          "rx_functional_params": {"can_id": 0x1CDBFF00},
          "tx_functional_params": {"can_id": 0x1CDB00FF, "target_address": 0x00, "source_address": 0xFF}},
         {"rx_physical_params": {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                 "addressing_type": AddressingType.PHYSICAL,
                                 "can_id": 0xDA00FF,
                                 "target_address": 0x00,
                                 "source_address": 0xFF,
                                 "address_extension": None},
          "tx_physical_params": {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                 "addressing_type": AddressingType.PHYSICAL,
                                 "can_id": 0xDAFF00,
                                 "target_address": 0xFF,
                                 "source_address": 0x00,
                                 "address_extension": None},
          "rx_functional_params": {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                   "addressing_type": AddressingType.FUNCTIONAL,
                                   "can_id": 0x1CDBFF00,
                                   "target_address": 0xFF,
                                   "source_address": 0x00,
                                   "address_extension": None},
          "tx_functional_params": {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                   "addressing_type": AddressingType.FUNCTIONAL,
                                   "can_id": 0x1CDB00FF,
                                   "target_address": 0x00,
                                   "source_address": 0xFF,
                                   "address_extension": None}}),
        # Extended
        ({"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "rx_physical_params": {"can_id": 0x621, "target_address": 0x1F},
          "tx_physical_params": {"can_id": 0x1, "target_address": 0x91},
          "rx_functional_params": {"can_id": 0x12345, "target_address": 0x82},
          "tx_functional_params": {"can_id": 0x12346, "target_address": 0x83}},
         {"rx_physical_params": {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
                                 "addressing_type": AddressingType.PHYSICAL,
                                 "can_id": 0x621,
                                 "target_address": 0x1F,
                                 "source_address": None,
                                 "address_extension": None},
          "tx_physical_params": {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
                                 "addressing_type": AddressingType.PHYSICAL,
                                 "can_id": 0x1,
                                 "target_address": 0x91,
                                 "source_address": None,
                                 "address_extension": None},
          "rx_functional_params": {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
                                   "addressing_type": AddressingType.FUNCTIONAL,
                                   "can_id": 0x12345,
                                   "target_address": 0x82,
                                   "source_address": None,
                                   "address_extension": None},
          "tx_functional_params": {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
                                   "addressing_type": AddressingType.FUNCTIONAL,
                                   "can_id": 0x12346,
                                   "target_address": 0x83,
                                   "source_address": None,
                                   "address_extension": None}}),
        # Mixed 11-bit
        ({"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
          "rx_physical_params": {"can_id": 0x641, "address_extension": 0x00},
          "tx_physical_params": {"can_id": 0x642, "address_extension": 0x00},
          "rx_functional_params": {"can_id": 0x6DE, "address_extension": 0xFE},
          "tx_functional_params": {"can_id": 0x6DF, "address_extension": 0xFE}},
         {"rx_physical_params": {"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                 "addressing_type": AddressingType.PHYSICAL,
                                 "can_id": 0x641,
                                 "address_extension": 0x00,
                                 "target_address": None,
                                 "source_address": None},
          "tx_physical_params": {"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                 "addressing_type": AddressingType.PHYSICAL,
                                 "can_id": 0x642,
                                 "address_extension": 0x00,
                                 "target_address": None,
                                 "source_address": None},
          "rx_functional_params": {"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                   "addressing_type": AddressingType.FUNCTIONAL,
                                   "can_id": 0x6DE,
                                   "address_extension": 0xFE,
                                   "target_address": None,
                                   "source_address": None},
          "tx_functional_params": {"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                   "addressing_type": AddressingType.FUNCTIONAL,
                                   "can_id": 0x6DF,
                                   "address_extension": 0xFE,
                                   "target_address": None,
                                   "source_address": None}}),
        # Mixed 29-bit
        ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "rx_physical_params": {"can_id": 0x18CE1234, "target_address": 0x12, "source_address": 0x34,
                                 "address_extension": 0x00},
          "tx_physical_params": {"can_id": 0x18CE3412, "source_address": 0x12, "address_extension": 0x00},
          "rx_functional_params": {"can_id": 0x18CDBD87, "target_address": 0xBD, "address_extension": 0xFF},
          "tx_functional_params": {"target_address": 0x87, "source_address": 0xBD, "address_extension": 0xFF}},
         {"rx_physical_params": {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                 "addressing_type": AddressingType.PHYSICAL,
                                 "can_id": 0x18CE1234,
                                 "target_address": 0x12,
                                 "source_address": 0x34,
                                 "address_extension": 0x00},
          "tx_physical_params": {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                 "addressing_type": AddressingType.PHYSICAL,
                                 "can_id": 0x18CE3412,
                                 "target_address": 0x34,
                                 "source_address": 0x12,
                                 "address_extension": 0x00},
          "rx_functional_params": {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                   "addressing_type": AddressingType.FUNCTIONAL,
                                   "can_id": 0x18CDBD87,
                                   "target_address": 0xBD,
                                   "source_address": 0x87,
                                   "address_extension": 0xFF},
          "tx_functional_params": {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                   "addressing_type": AddressingType.FUNCTIONAL,
                                   "can_id": 0x18CD87BD,
                                   "target_address": 0x87,
                                   "source_address": 0xBD,
                                   "address_extension": 0xFF}}),
        ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "rx_physical_params": {"can_id": 0xCE00FF, "address_extension": 0x32},
          "tx_physical_params": {"can_id": 0xCEFF00, "address_extension": 0x32},
          "rx_functional_params": {"can_id": 0x1CCDFF00, "address_extension": 0xA1},
          "tx_functional_params": {"can_id": 0x1CCD00FF, "address_extension": 0xA1}},
         {"rx_physical_params": {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                 "addressing_type": AddressingType.PHYSICAL,
                                 "can_id": 0xCE00FF,
                                 "target_address": 0x00,
                                 "source_address": 0xFF,
                                 "address_extension": 0x32},
          "tx_physical_params": {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                 "addressing_type": AddressingType.PHYSICAL,
                                 "can_id": 0xCEFF00,
                                 "target_address": 0xFF,
                                 "source_address": 0x00,
                                 "address_extension": 0x32},
          "rx_functional_params": {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                   "addressing_type": AddressingType.FUNCTIONAL,
                                   "can_id": 0x1CCDFF00,
                                   "target_address": 0xFF,
                                   "source_address": 0x00,
                                   "address_extension": 0xA1},
          "tx_functional_params": {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                   "addressing_type": AddressingType.FUNCTIONAL,
                                   "can_id": 0x1CCD00FF,
                                   "target_address": 0x00,
                                   "source_address": 0xFF,
                                   "address_extension": 0xA1}}),
    ])
    def test_new_and_other_end(self, input_params, expected_attributes):
        ai = CanAddressingInformation(**input_params)
        for attr_name, attr_value in expected_attributes.items():
            assert getattr(ai, attr_name) == attr_value
        ai_other_end = ai.get_other_end()
        assert ai.rx_physical_params == ai_other_end.tx_physical_params
        assert ai.tx_physical_params == ai_other_end.rx_physical_params
        assert ai.rx_functional_params == ai_other_end.tx_functional_params
        assert ai.tx_functional_params == ai_other_end.rx_functional_params

import pytest
from mock import Mock, patch

from uds.addressing import AbstractAddressingInformation, AddressingType
from uds.can.addressing.abstract_addressing_information import AbstractCanAddressingInformation

SCRIPT_LOCATION = "uds.can.addressing.abstract_addressing_information"


class TestAbstractCanAddressingInformation:
    """Unit tests for `AbstractCanAddressingInformation` class."""

    def setup_method(self):
        self.mock_addressing_information = Mock(spec=AbstractCanAddressingInformation)

    def test_inheritance__abstract_addressing_information(self):
        assert issubclass(AbstractCanAddressingInformation, AbstractAddressingInformation)

    # __init__

    @pytest.mark.parametrize("rx_physical_params, tx_physical_params, rx_functional_params, tx_functional_params", [
        (Mock(), Mock(), Mock(), Mock()),
        ("rx_physical", "tx_physical", "rx_functional", "tx_functional"),
    ])
    @patch(f"{SCRIPT_LOCATION}.AbstractAddressingInformation.__init__")
    def test_init(self, mock_abstract_ai_init, rx_physical_params, tx_physical_params, rx_functional_params, tx_functional_params):
        assert AbstractCanAddressingInformation.__init__(self=self.mock_addressing_information,
                                                         rx_physical_params=rx_physical_params,
                                                         tx_physical_params=tx_physical_params,
                                                         rx_functional_params=rx_functional_params,
                                                         tx_functional_params=tx_functional_params) is None
        mock_abstract_ai_init.assert_called_once_with(rx_physical_params=rx_physical_params,
                                                      tx_physical_params=tx_physical_params,
                                                      rx_functional_params=rx_functional_params,
                                                      tx_functional_params=tx_functional_params)

    # decode_frame_ai_params

    @pytest.mark.parametrize("can_id, raw_frame_data, ai_data_bytes_number, "
                             "decoded_can_id_params, decoded_data_ai_params, expected_output", [
        (Mock(), b"\xFE\xDC\xBA\x98\x76\x54\x32\x10"[::-1], 0,
         {
             "addressing_type": None,
             "target_address": None,
             "source_address": None,
             "priority": None,
         },
         {
         },
         {
             "addressing_type": None,
             "target_address": None,
             "source_address": None,
             "address_extension": None,
         }),
        (Mock(), b"\xFE\xDC\xBA\x98\x76\x54\x32\x10", 1,
         {
             "addressing_type": AddressingType.PHYSICAL,
             "target_address": 0x5A,
             "source_address": 0xA5,
             "priority": 0b111,
         },
         {
             "address_extension": 0xBC
         },
         {
             "addressing_type": AddressingType.PHYSICAL,
             "target_address": 0x5A,
             "source_address": 0xA5,
             "address_extension": 0xBC,
         }),
        (0x6FF, list(range(8)), 2,
         {
             "addressing_type": AddressingType.FUNCTIONAL,
             "target_address": None,
             "source_address": 0x00,
             "priority": 0,
         },
         {
             "target_address": 0xE9
         },
         {
             "addressing_type": AddressingType.FUNCTIONAL,
             "target_address": 0xE9,
             "source_address": 0x00,
             "address_extension": None,
         }),
    ])
    @patch(f"{SCRIPT_LOCATION}.AbstractCanAddressingInformation.decode_data_bytes_ai_params")
    @patch(f"{SCRIPT_LOCATION}.AbstractCanAddressingInformation.decode_can_id_ai_params")
    def test_decode_frame_ai_params(self, mock_decode_can_id_ai_params, mock_decode_data_bytes_ai_params,
                                    can_id, raw_frame_data,
                                    ai_data_bytes_number, decoded_can_id_params, decoded_data_ai_params, expected_output):
        mock_decode_can_id_ai_params.return_value = decoded_can_id_params
        mock_decode_data_bytes_ai_params.return_value = decoded_data_ai_params
        AbstractCanAddressingInformation.AI_DATA_BYTES_NUMBER = ai_data_bytes_number
        assert AbstractCanAddressingInformation.decode_frame_ai_params(can_id=can_id,
                                                                       raw_frame_data=raw_frame_data) == expected_output
        mock_decode_can_id_ai_params.assert_called_once_with(can_id)
        mock_decode_data_bytes_ai_params.assert_called_once_with(raw_frame_data[:ai_data_bytes_number])

    # is_input_packet

    @pytest.mark.parametrize("can_id, raw_frame_data, "
                             "decoded_frame_ai_params, rx_physical_params, rx_functional_params", [
        (Mock(), b"\xFE\xDC\xBA\x98\x76\x54\x32\x10",
         {
             "addressing_type": None,
             "target_address": None,
             "source_address": None,
             "address_extension": None,
         },
         {
             "addressing_type": AddressingType.PHYSICAL,
             "can_id": 0x123,
             "target_address": None,
             "source_address": None,
             "address_extension": None,
         },
         {
             "addressing_type": AddressingType.FUNCTIONAL,
             "can_id": 0x86FF,
             "target_address": None,
             "source_address": None,
             "address_extension": None,
         }),
        (0x123, b"\xFE\xDC\xBA\x98\x76\x54\x32\x10"[::-1],
         {
             "addressing_type": AddressingType.PHYSICAL,
             "target_address": 0x54,
             "source_address": 0x32,
             "address_extension": None,
         },
         {
             "addressing_type": AddressingType.PHYSICAL,
             "can_id": 0x123,
             "target_address": 0x54,
             "source_address": 0xFF,
             "address_extension": None,
         },
         {
             "addressing_type": AddressingType.FUNCTIONAL,
             "can_id": 0x123,
             "target_address": 0xFF,
             "source_address": 0x32,
             "address_extension": None,
         }),
        (0x18C6FF, list(range(100, 164)),
         {
             "addressing_type": AddressingType.FUNCTIONAL,
             "target_address": None,
             "source_address": None,
             "address_extension": 0x55,
         },
         {
             "addressing_type": AddressingType.PHYSICAL,
             "can_id": 0x18C6FF,
             "target_address": None,
             "source_address": None,
             "address_extension": 0x55,
         },
         {
             "addressing_type": AddressingType.FUNCTIONAL,
             "can_id": 0x18C6FF,
             "target_address": None,
             "source_address": None,
             "address_extension": 0xFF,
         }),
    ])
    def test_is_input_packet__none(self, can_id, raw_frame_data,
                                   decoded_frame_ai_params, rx_physical_params, rx_functional_params):
        self.mock_addressing_information.rx_physical_params = rx_physical_params
        self.mock_addressing_information.rx_functional_params = rx_functional_params
        self.mock_addressing_information.decode_frame_ai_params.return_value = decoded_frame_ai_params
        assert AbstractCanAddressingInformation.is_input_packet(self.mock_addressing_information,
                                                                can_id=can_id,
                                                                raw_frame_data=raw_frame_data) is None
        self.mock_addressing_information.decode_frame_ai_params.assert_called_once_with(
            can_id=can_id, raw_frame_data=raw_frame_data)

    @pytest.mark.parametrize("can_id, raw_frame_data, "
                             "decoded_frame_ai_params, rx_physical_params, rx_functional_params", [
        (0x123, b"\xFE\xDC\xBA\x98\x76\x54\x32\x10",
         {
             "addressing_type": None,
             "target_address": None,
             "source_address": None,
             "address_extension": None,
         },
         {
             "addressing_type": AddressingType.PHYSICAL,
             "can_id": 0x123,
             "target_address": None,
             "source_address": None,
             "address_extension": None,
         },
         {
             "addressing_type": AddressingType.FUNCTIONAL,
             "can_id": 0x86FF,
             "target_address": None,
             "source_address": None,
             "address_extension": None,
         }),
        (0x123, b"\xFE\xDC\xBA\x98\x76\x54\x32\x10"[::-1],
         {
             "addressing_type": AddressingType.PHYSICAL,
             "target_address": 0x54,
             "source_address": 0xFF,
             "address_extension": None,
         },
         {
             "addressing_type": AddressingType.PHYSICAL,
             "can_id": 0x123,
             "target_address": 0x54,
             "source_address": 0xFF,
             "address_extension": None,
         },
         {
             "addressing_type": AddressingType.FUNCTIONAL,
             "can_id": 0x123,
             "target_address": 0xFF,
             "source_address": 0x32,
             "address_extension": None,
         }),
        (0x18C6FF, list(range(100, 164)),
         {
             "addressing_type": None,
             "target_address": None,
             "source_address": None,
             "address_extension": 0x55,
         },
         {
             "addressing_type": AddressingType.PHYSICAL,
             "can_id": 0x18C6FF,
             "target_address": None,
             "source_address": None,
             "address_extension": 0x55,
         },
         {
             "addressing_type": AddressingType.FUNCTIONAL,
             "can_id": 0x18C6FF,
             "target_address": None,
             "source_address": None,
             "address_extension": 0xFF,
         }),
    ])
    def test_is_input_packet__physical(self, can_id, raw_frame_data,
                                       decoded_frame_ai_params, rx_physical_params, rx_functional_params):
        self.mock_addressing_information.rx_physical_params = rx_physical_params
        self.mock_addressing_information.rx_functional_params = rx_functional_params
        self.mock_addressing_information.decode_frame_ai_params.return_value = decoded_frame_ai_params
        assert AbstractCanAddressingInformation.is_input_packet(
            self.mock_addressing_information,
            can_id=can_id,
            raw_frame_data=raw_frame_data) is AddressingType.PHYSICAL
        self.mock_addressing_information.decode_frame_ai_params.assert_called_once_with(
            can_id=can_id, raw_frame_data=raw_frame_data)

    @pytest.mark.parametrize("can_id, raw_frame_data, "
                             "decoded_frame_ai_params, rx_physical_params, rx_functional_params", [
        (0x86FF, b"\xFE\xDC\xBA\x98\x76\x54\x32\x10",
         {
             "addressing_type": None,
             "target_address": None,
             "source_address": None,
             "address_extension": None,
         },
         {
             "addressing_type": AddressingType.PHYSICAL,
             "can_id": 0x123,
             "target_address": None,
             "source_address": None,
             "address_extension": None,
         },
         {
             "addressing_type": AddressingType.FUNCTIONAL,
             "can_id": 0x86FF,
             "target_address": None,
             "source_address": None,
             "address_extension": None,
         }),
        (0x123, b"\xFE\xDC\xBA\x98\x76\x54\x32\x10"[::-1],
         {
             "addressing_type": AddressingType.FUNCTIONAL,
             "target_address": 0xFF,
             "source_address": 0x32,
             "address_extension": None,
         },
         {
             "addressing_type": AddressingType.PHYSICAL,
             "can_id": 0x123,
             "target_address": 0x54,
             "source_address": 0xFF,
             "address_extension": None,
         },
         {
             "addressing_type": AddressingType.FUNCTIONAL,
             "can_id": 0x123,
             "target_address": 0xFF,
             "source_address": 0x32,
             "address_extension": None,
         }),
        (0x18C6FF, list(range(100, 164)),
         {
             "addressing_type": None,
             "target_address": None,
             "source_address": None,
             "address_extension": 0xFF,
         },
         {
             "addressing_type": AddressingType.PHYSICAL,
             "can_id": 0x18C6FF,
             "target_address": None,
             "source_address": None,
             "address_extension": 0x55,
         },
         {
             "addressing_type": AddressingType.FUNCTIONAL,
             "can_id": 0x18C6FF,
             "target_address": None,
             "source_address": None,
             "address_extension": 0xFF,
         }),
    ])
    def test_is_input_packet__functional(self, can_id, raw_frame_data,
                                         decoded_frame_ai_params, rx_physical_params, rx_functional_params):
        self.mock_addressing_information.rx_physical_params = rx_physical_params
        self.mock_addressing_information.rx_functional_params = rx_functional_params
        self.mock_addressing_information.decode_frame_ai_params.return_value = decoded_frame_ai_params
        assert AbstractCanAddressingInformation.is_input_packet(
            self.mock_addressing_information,
            can_id=can_id,
            raw_frame_data=raw_frame_data) is AddressingType.FUNCTIONAL
        self.mock_addressing_information.decode_frame_ai_params.assert_called_once_with(
            can_id=can_id, raw_frame_data=raw_frame_data)

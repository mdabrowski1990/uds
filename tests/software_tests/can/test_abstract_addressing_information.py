import pytest
from mock import Mock, MagicMock, patch

from uds.can.abstract_addressing_information import AbstractCanAddressingInformation, AddressingType

SCRIPT_LOCATION = "uds.can.abstract_addressing_information"


class TestAbstractCanAddressingInformation:
    """Unit tests for `AbstractCanAddressingInformation` class."""

    def setup_method(self):
        self.mock_addressing_information = Mock(spec=AbstractCanAddressingInformation,
                                                ADDRESSING_FORMAT_NAME="addressing_format",
                                                ADDRESSING_TYPE_NAME="addressing_type",
                                                TARGET_ADDRESS_NAME="target_address",
                                                SOURCE_ADDRESS_NAME="source_address",
                                                ADDRESS_EXTENSION_NAME="address_extension",
                                                tx_packets_physical_ai=MagicMock(),
                                                rx_packets_physical_ai=MagicMock(),
                                                tx_packets_functional_ai=MagicMock(),
                                                rx_packets_functional_ai=MagicMock())
        # patching
        self._patcher_deepcopy = patch(f"{SCRIPT_LOCATION}.deepcopy")
        self.mock_deepcopy = self._patcher_deepcopy.start()

    def teardown_method(self):
        self._patcher_deepcopy.stop()

    # __init__

    @pytest.mark.parametrize("rx_physical, tx_physical, rx_functional, tx_functional", [
        (1, 2, 3, 4),
        ("rx_physical", "tx_physical", "rx_functional", "tx_functional"),
    ])
    def test_init(self, rx_physical, tx_physical, rx_functional, tx_functional):
        assert AbstractCanAddressingInformation.__init__(self=self.mock_addressing_information,
                                                         rx_physical=rx_physical,
                                                         tx_physical=tx_physical,
                                                         rx_functional=rx_functional,
                                                         tx_functional=tx_functional) is None
        assert self.mock_addressing_information.rx_packets_physical_ai == rx_physical
        assert self.mock_addressing_information.tx_packets_physical_ai == tx_physical
        assert self.mock_addressing_information.rx_packets_functional_ai == rx_functional
        assert self.mock_addressing_information.tx_packets_functional_ai == tx_functional
        self.mock_addressing_information._validate_node_ai.assert_called_once_with(
            rx_packets_physical_ai=self.mock_addressing_information.rx_packets_physical_ai,
            tx_packets_physical_ai=self.mock_addressing_information.tx_packets_physical_ai,
            rx_packets_functional_ai=self.mock_addressing_information.rx_packets_functional_ai,
            tx_packets_functional_ai=self.mock_addressing_information.tx_packets_functional_ai)

    # rx_packets_physical_ai

    @pytest.mark.parametrize("value", ["any value", Mock()])
    def test_rx_packets_physical_ai__get(self, value):
        self.mock_addressing_information._AbstractCanAddressingInformation__rx_packets_physical_ai = value
        assert AbstractCanAddressingInformation.rx_packets_physical_ai.fget(self.mock_addressing_information) \
               == self.mock_deepcopy.return_value
        self.mock_deepcopy.assert_called_once_with(value)

    @pytest.mark.parametrize("value", [{"a": 1, "b": 2}, {"argument_1": None, "argument_2": Mock()}])
    def test_rx_packets_physical_ai__set(self, value):
        AbstractCanAddressingInformation.rx_packets_physical_ai.fset(self.mock_addressing_information, value)
        self.mock_addressing_information.validate_packet_ai(addressing_type=AddressingType.PHYSICAL, **value)
        assert self.mock_addressing_information._AbstractCanAddressingInformation__rx_packets_physical_ai \
               == self.mock_addressing_information.validate_packet_ai.return_value

    # tx_packets_physical_ai

    @pytest.mark.parametrize("value", ["any value", Mock()])
    def test_tx_packets_physical_ai__get(self, value):
        self.mock_addressing_information._AbstractCanAddressingInformation__tx_packets_physical_ai = value
        assert AbstractCanAddressingInformation.tx_packets_physical_ai.fget(self.mock_addressing_information) \
               == self.mock_deepcopy.return_value
        self.mock_deepcopy.assert_called_once_with(value)

    @pytest.mark.parametrize("value", [{"a": 1, "b": 2}, {"argument_1": None, "argument_2": Mock()}])
    def test_tx_packets_physical_ai__set(self, value):
        AbstractCanAddressingInformation.tx_packets_physical_ai.fset(self.mock_addressing_information, value)
        self.mock_addressing_information.validate_packet_ai(addressing_type=AddressingType.PHYSICAL, **value)
        assert self.mock_addressing_information._AbstractCanAddressingInformation__tx_packets_physical_ai \
               == self.mock_addressing_information.validate_packet_ai.return_value

    # rx_packets_functional_ai

    @pytest.mark.parametrize("value", ["any value", Mock()])
    def test_rx_packets_functional_ai__get(self, value):
        self.mock_addressing_information._AbstractCanAddressingInformation__rx_packets_functional_ai = value
        assert AbstractCanAddressingInformation.rx_packets_functional_ai.fget(self.mock_addressing_information) \
               == self.mock_deepcopy.return_value
        self.mock_deepcopy.assert_called_once_with(value)

    @pytest.mark.parametrize("value", [{"a": 1, "b": 2}, {"argument_1": None, "argument_2": Mock()}])
    def test_rx_packets_functional_ai__set(self, value):
        AbstractCanAddressingInformation.rx_packets_functional_ai.fset(self.mock_addressing_information, value)
        self.mock_addressing_information.validate_packet_ai(addressing_type=AddressingType.FUNCTIONAL, **value)
        assert self.mock_addressing_information._AbstractCanAddressingInformation__rx_packets_functional_ai \
               == self.mock_addressing_information.validate_packet_ai.return_value

    # tx_packets_functional_ai

    @pytest.mark.parametrize("value", ["any value", Mock()])
    def test_tx_packets_functional_ai__get(self, value):
        self.mock_addressing_information._AbstractCanAddressingInformation__tx_packets_functional_ai = value
        assert AbstractCanAddressingInformation.tx_packets_functional_ai.fget(self.mock_addressing_information) \
               == self.mock_deepcopy.return_value
        self.mock_deepcopy.assert_called_once_with(value)

    @pytest.mark.parametrize("value", [{"a": 1, "b": 2}, {"argument_1": None, "argument_2": Mock()}])
    def test_tx_packets_functional_ai__set(self, value):
        AbstractCanAddressingInformation.tx_packets_functional_ai.fset(self.mock_addressing_information, value)
        self.mock_addressing_information.validate_packet_ai(addressing_type=AddressingType.FUNCTIONAL, **value)
        assert self.mock_addressing_information._AbstractCanAddressingInformation__tx_packets_functional_ai \
               == self.mock_addressing_information.validate_packet_ai.return_value

    # get_other_end

    def test_get_other_end(self):
        assert (AbstractCanAddressingInformation.get_other_end(self.mock_addressing_information)
                == self.mock_deepcopy.return_value)
        self.mock_deepcopy.assert_called_once_with(self.mock_addressing_information)

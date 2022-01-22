import pytest
from mock import Mock, patch

from uds.can.abstract_addressing_information import AbstractAddressingInformation


class TestAbstractAddressingInformation:
    """Unit tests for `AbstractAddressingInformation` class."""

    SCRIPT_LOCATION = "uds.can.extended_addressing_information"

    def setup(self):
        self.mock_addressing_information = Mock(spec=AbstractAddressingInformation)

    # __init__

    @pytest.mark.parametrize("rx_physical, tx_physical, rx_functional, tx_functional", [
        (1, 2, 3, 4),
        ("rx_physical", "tx_physical", "rx_functional", "tx_functional"),
    ])
    def test_init(self, rx_physical, tx_physical, rx_functional, tx_functional):
        assert AbstractAddressingInformation.__init__(self=self.mock_addressing_information,
                                                      rx_physical=rx_physical,
                                                      tx_physical=tx_physical,
                                                      rx_functional=rx_functional,
                                                      tx_functional=tx_functional) is None
        assert self.mock_addressing_information.rx_packets_physical_ai == rx_physical
        assert self.mock_addressing_information.tx_packets_physical_ai == tx_physical
        assert self.mock_addressing_information.rx_packets_functional_ai == rx_functional
        assert self.mock_addressing_information.tx_packets_functional_ai == tx_functional

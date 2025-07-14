import pytest
from mock import Mock, patch

from uds.can.addressing.abstract_addressing_information import AbstractCanAddressingInformation
from uds.addressing import AbstractAddressingInformation

SCRIPT_LOCATION = "uds.addressing.abstract_addressing_information"


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

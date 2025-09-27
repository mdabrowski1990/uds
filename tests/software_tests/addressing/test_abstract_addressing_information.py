import pytest
from mock import MagicMock, Mock, patch

from uds.addressing.abstract_addressing_information import (
    AbstractAddressingInformation,
    AddressingType,
    ReassignmentError,
)

SCRIPT_LOCATION = "uds.addressing.abstract_addressing_information"


class TestAbstractAddressingInformation:
    """Unit tests for `AbstractAddressingInformation` class."""

    def setup_method(self):
        self.mock_ai = MagicMock(spec=AbstractAddressingInformation,
                                 ADDRESSING_TYPE_NAME=AbstractAddressingInformation.ADDRESSING_TYPE_NAME)
        # patching
        self._patcher_mapping_proxy_type = patch(f"{SCRIPT_LOCATION}.MappingProxyType")
        self.mock_mapping_proxy_type = self._patcher_mapping_proxy_type.start()

    def teardown_method(self):
        self._patcher_mapping_proxy_type.stop()

    # __init__

    @pytest.mark.parametrize("rx_physical_params, tx_physical_params, rx_functional_params, tx_functional_params", [
        ({"a": 1}, {"b": 2}, {"c": 3}, {"d": 4}),
        (Mock(), Mock(), Mock(), Mock()),
    ])
    def test_init(self, rx_physical_params, tx_physical_params, rx_functional_params, tx_functional_params):
        assert AbstractAddressingInformation.__init__(self.mock_ai,
                                                      rx_physical_params,
                                                      tx_physical_params,
                                                      rx_functional_params,
                                                      tx_functional_params) is None
        assert self.mock_ai.rx_physical_params == rx_physical_params
        assert self.mock_ai.tx_physical_params == tx_physical_params
        assert self.mock_ai.rx_functional_params == rx_functional_params
        assert self.mock_ai.tx_functional_params == tx_functional_params
        self.mock_ai._validate_addressing_information.assert_called_once_with()

    # __eq__

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_eq__other_type(self, mock_isinstance):
        mock_isinstance.return_value = False
        assert AbstractAddressingInformation.__eq__(self.mock_ai, self.mock_ai) is False
        mock_isinstance.assert_called_once_with(self.mock_ai, AbstractAddressingInformation)

    def test_eq__true(self):
        assert AbstractAddressingInformation.__eq__(self.mock_ai, self.mock_ai) is True

    def test_eq__false(self):
        mock_ai = Mock(spec=AbstractAddressingInformation)
        assert AbstractAddressingInformation.__eq__(self.mock_ai, mock_ai) is False

    # rx_physical_params

    def test_rx_physical_params__get(self):
        self.mock_ai._AbstractAddressingInformation__rx_physical_params = Mock()
        assert (AbstractAddressingInformation.rx_physical_params.fget(self.mock_ai)
                == self.mock_ai._AbstractAddressingInformation__rx_physical_params)

    @pytest.mark.parametrize("params", [
        {},
        {"a": 1, "b": 2, "c": None},
        {AbstractAddressingInformation.ADDRESSING_TYPE_NAME: None, "xyz": 43.2, "abc": "some value"},
    ])
    def test_rx_physical_params__set__valid(self, params):
        assert AbstractAddressingInformation.rx_physical_params.fset(self.mock_ai, params) is None
        assert self.mock_ai._AbstractAddressingInformation__rx_physical_params is self.mock_mapping_proxy_type.return_value
        self.mock_mapping_proxy_type.assert_called_once_with(self.mock_ai.validate_addressing_params.return_value)
        params[AbstractAddressingInformation.ADDRESSING_TYPE_NAME] = AddressingType.PHYSICAL
        self.mock_ai.validate_addressing_params.assert_called_once_with(**params)

    def test_rx_physical_params__set__reassignment_error(self):
        self.mock_ai._AbstractAddressingInformation__rx_physical_params = Mock()
        with pytest.raises(ReassignmentError):
            AbstractAddressingInformation.rx_physical_params.fset(self.mock_ai, {})

    # tx_physical_params

    def test_tx_physical_params__get(self):
        self.mock_ai._AbstractAddressingInformation__tx_physical_params = Mock()
        assert (AbstractAddressingInformation.tx_physical_params.fget(self.mock_ai)
                == self.mock_ai._AbstractAddressingInformation__tx_physical_params)

    @pytest.mark.parametrize("params", [
        {},
        {"a": 1, "b": 2, "c": None},
        {AbstractAddressingInformation.ADDRESSING_TYPE_NAME: None, "xyz": 43.2, "abc": "some value"},
    ])
    def test_tx_physical_params__set__valid(self, params):
        assert AbstractAddressingInformation.tx_physical_params.fset(self.mock_ai, params) is None
        assert self.mock_ai._AbstractAddressingInformation__tx_physical_params is self.mock_mapping_proxy_type.return_value
        self.mock_mapping_proxy_type.assert_called_once_with(self.mock_ai.validate_addressing_params.return_value)
        params[AbstractAddressingInformation.ADDRESSING_TYPE_NAME] = AddressingType.PHYSICAL
        self.mock_ai.validate_addressing_params.assert_called_once_with(**params)

    def test_tx_physical_params__set__reassignment_error(self):
        self.mock_ai._AbstractAddressingInformation__tx_physical_params = Mock()
        with pytest.raises(ReassignmentError):
            AbstractAddressingInformation.tx_physical_params.fset(self.mock_ai, {})
            
    # rx_functional_params

    def test_rx_functional_params__get(self):
        self.mock_ai._AbstractAddressingInformation__rx_functional_params = Mock()
        assert (AbstractAddressingInformation.rx_functional_params.fget(self.mock_ai)
                == self.mock_ai._AbstractAddressingInformation__rx_functional_params)

    @pytest.mark.parametrize("params", [
        {},
        {"a": 1, "b": 2, "c": None},
        {AbstractAddressingInformation.ADDRESSING_TYPE_NAME: None, "xyz": 43.2, "abc": "some value"},
    ])
    def test_rx_functional_params__set__valid(self, params):
        assert AbstractAddressingInformation.rx_functional_params.fset(self.mock_ai, params) is None
        assert self.mock_ai._AbstractAddressingInformation__rx_functional_params is self.mock_mapping_proxy_type.return_value
        self.mock_mapping_proxy_type.assert_called_once_with(self.mock_ai.validate_addressing_params.return_value)
        params[AbstractAddressingInformation.ADDRESSING_TYPE_NAME] = AddressingType.FUNCTIONAL
        self.mock_ai.validate_addressing_params.assert_called_once_with(**params)

    def test_rx_functional_params__set__reassignment_error(self):
        self.mock_ai._AbstractAddressingInformation__rx_functional_params = Mock()
        with pytest.raises(ReassignmentError):
            AbstractAddressingInformation.rx_functional_params.fset(self.mock_ai, {})
            
    # tx_functional_params

    def test_tx_functional_params__get(self):
        self.mock_ai._AbstractAddressingInformation__tx_functional_params = Mock()
        assert (AbstractAddressingInformation.tx_functional_params.fget(self.mock_ai)
                == self.mock_ai._AbstractAddressingInformation__tx_functional_params)

    @pytest.mark.parametrize("params", [
        {},
        {"a": 1, "b": 2, "c": None},
        {AbstractAddressingInformation.ADDRESSING_TYPE_NAME: None, "xyz": 43.2, "abc": "some value"},
    ])
    def test_tx_functional_params__set__valid(self, params):
        assert AbstractAddressingInformation.tx_functional_params.fset(self.mock_ai, params) is None
        assert self.mock_ai._AbstractAddressingInformation__tx_functional_params is self.mock_mapping_proxy_type.return_value
        self.mock_mapping_proxy_type.assert_called_once_with(self.mock_ai.validate_addressing_params.return_value)
        params[AbstractAddressingInformation.ADDRESSING_TYPE_NAME] = AddressingType.FUNCTIONAL
        self.mock_ai.validate_addressing_params.assert_called_once_with(**params)

    def test_tx_functional_params__set__reassignment_error(self):
        self.mock_ai._AbstractAddressingInformation__tx_functional_params = Mock()
        with pytest.raises(ReassignmentError):
            AbstractAddressingInformation.tx_functional_params.fset(self.mock_ai, {})

    # get_other_end

    def test_get_other_end(self):
        mock_class = Mock()
        self.mock_ai.__class__ = mock_class
        assert AbstractAddressingInformation.get_other_end(self.mock_ai) == mock_class.return_value
        mock_class.assert_called_once_with(rx_physical_params=self.mock_ai.tx_physical_params,
                                           tx_physical_params=self.mock_ai.rx_physical_params,
                                           rx_functional_params=self.mock_ai.tx_functional_params,
                                           tx_functional_params=self.mock_ai.rx_functional_params)

@pytest.mark.integration
class TestAbstractCanAddressingInformationIntegration:
    """Integration tests for `AbstractCanAddressingInformation` class."""

    def test_get_other_end(self, example_can_addressing_information):
        other = example_can_addressing_information.get_other_end()
        assert other.rx_physical_params == example_can_addressing_information.tx_physical_params
        assert other.tx_physical_params == example_can_addressing_information.rx_physical_params
        assert other.rx_functional_params == example_can_addressing_information.tx_functional_params
        assert other.tx_functional_params == example_can_addressing_information.rx_functional_params

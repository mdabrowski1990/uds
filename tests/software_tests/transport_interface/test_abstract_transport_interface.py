import pytest
from mock import Mock

from uds.transport_interface.abstract_transport_interface import AbstractTransportInterface, ReassignmentError

SCRIPT_LOCATION = "uds.transport_interface.abstract_transport_interface"


class TestAbstractTransportInterface:
    """Unit tests for `AbstractTransportInterface` class."""

    def setup_method(self):
        self.mock_transport_interface = Mock(spec=AbstractTransportInterface)

    # __init__

    @pytest.mark.parametrize("network_manager", [Mock(), "some network manager"])
    def test_init__valid(self, network_manager):
        assert AbstractTransportInterface.__init__(self=self.mock_transport_interface,
                                                   network_manager=network_manager) is None
        assert self.mock_transport_interface.network_manager == network_manager

    # addressing_information

    def test_addressing_information__get(self):
        assert (AbstractTransportInterface.addressing_information.fget(self.mock_transport_interface)
                == self.mock_transport_interface.segmenter.addressing_information)

    @pytest.mark.parametrize("value", [Mock(), "some addressing information"])
    def test_addressing_information__set(self, value):
        assert (AbstractTransportInterface.addressing_information.fset(self.mock_transport_interface, value) is None)
        assert self.mock_transport_interface.segmenter.addressing_information == value

    # network_manager

    def test_network_manager__get(self):
        self.mock_transport_interface._AbstractTransportInterface__network_manager = Mock()
        assert (AbstractTransportInterface.network_manager.fget(self.mock_transport_interface)
                == self.mock_transport_interface._AbstractTransportInterface__network_manager)

    @pytest.mark.parametrize("value", [Mock(), "some network manager"])
    def test_network_manager__set(self, value):
        self.mock_transport_interface.is_supported_network_manager.return_value = True
        AbstractTransportInterface.network_manager.fset(self.mock_transport_interface, value)
        assert self.mock_transport_interface._AbstractTransportInterface__network_manager == value
        self.mock_transport_interface.is_supported_network_manager.assert_called_with(value)

    @pytest.mark.parametrize("value", [Mock(), "some network manager"])
    def test_network_manager__set__value_error(self, value):
        self.mock_transport_interface._AbstractTransportInterface__network_manager = Mock()
        self.mock_transport_interface.is_supported_network_manager.return_value = True
        with pytest.raises(ReassignmentError):
            AbstractTransportInterface.network_manager.fset(self.mock_transport_interface, value)
        self.mock_transport_interface.is_supported_network_manager.assert_called_with(value)

    @pytest.mark.parametrize("value", [Mock(), "some network manager"])
    def test_network_manager__set__value_error(self, value):
        self.mock_transport_interface.is_supported_network_manager.return_value = False
        with pytest.raises(ValueError):
            AbstractTransportInterface.network_manager.fset(self.mock_transport_interface, value)
        self.mock_transport_interface.is_supported_network_manager.assert_called_with(value)

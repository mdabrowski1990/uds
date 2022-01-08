import pytest
from mock import Mock, patch

from uds.transport_interface.abstract_transport_interface import AbstractTransportInterface


class TestAbstractTransportInterface:
    """Unit tests for `AbstractTransportInterface` class."""

    SCRIPT_LOCATION = "uds.transport_interface.abstract_transport_interface"

    def setup(self):
        self.mock_transport_interface = Mock(spec=AbstractTransportInterface)

    # __init__

    @pytest.mark.parametrize("bus_manager", [Mock(), "something"])
    def test_init__value_error__bus_manager(self, bus_manager):
        self.mock_transport_interface.is_supported_bus_manager.return_value = False
        with pytest.raises(ValueError):
            AbstractTransportInterface.__init__(self=self.mock_transport_interface, bus_manager=bus_manager)
        self.mock_transport_interface.is_supported_bus_manager.assert_called_once_with(bus_manager)

    @pytest.mark.parametrize("kwargs", [
        {"bus_manager": Mock()},
        {"bus_manager": "something", "max_packet_records_stored": 1, "max_message_records_stored": 1},
    ])
    def test_init__valid(self, kwargs):
        self.mock_transport_interface.is_supported_bus_manager.return_value = True
        AbstractTransportInterface.__init__(self=self.mock_transport_interface, **kwargs)
        self.mock_transport_interface.is_supported_bus_manager.assert_called_once_with(kwargs["bus_manager"])
        assert self.mock_transport_interface._AbstractTransportInterface__bus_manager == kwargs["bus_manager"]
        # TODO: make sure max_packet_records_stored and max_message_records_stored passed properly

    # bus_manager

    @pytest.mark.parametrize("value", [None, "some value"])
    def test_bus_manager(self, value):
        self.mock_transport_interface._AbstractTransportInterface__bus_manager = value
        assert AbstractTransportInterface.bus_manager.fget(self.mock_transport_interface) == value

    # packet_records

    def test_packet_records(self):
        with pytest.raises(NotImplementedError):
            AbstractTransportInterface.packet_records.fget(self.mock_transport_interface)

    # message_records

    def test_message_records(self):
        with pytest.raises(NotImplementedError):
            AbstractTransportInterface.message_records.fget(self.mock_transport_interface)

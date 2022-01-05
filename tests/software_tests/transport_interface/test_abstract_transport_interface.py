import pytest
from mock import Mock

from uds.transport_interface.abstract_transport_interface import AbstractTransportInterface


class TestAbstractTransportInterface:
    """Unit tests for `AbstractTransportInterface` class."""

    def setup(self):
        self.mock_transport_interface = Mock(spec=AbstractTransportInterface)

    # __init__

    def test_init(self):
        with pytest.raises(NotImplementedError):
            AbstractTransportInterface.__init__(self=self.mock_transport_interface,
                                                bus_manager=Mock(),
                                                max_message_records_stored=Mock(),
                                                max_packet_records_stored=Mock())

    # bus_manager

    def test_bus_handler(self):
        with pytest.raises(NotImplementedError):
            AbstractTransportInterface.bus_manager.fget(self.mock_transport_interface)

    # packet_records

    def test_packet_records(self):
        with pytest.raises(NotImplementedError):
            AbstractTransportInterface.packet_records.fget(self.mock_transport_interface)

    # message_records

    def test_message_records(self):
        with pytest.raises(NotImplementedError):
            AbstractTransportInterface.message_records.fget(self.mock_transport_interface)

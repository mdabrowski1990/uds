import pytest
from mock import Mock

from uds.transport_interface.abstract_transport_interface import AbstractTransportInterface


class TestAbstractTransportInterface:
    """Unit tests for `AbstractTransportInterface` class."""

    def setup(self):
        self.mock_transport_interface = Mock(spec=AbstractTransportInterface)

    # __init__

    def test_init__value_error(self):
        self.mock_transport_interface.is_supported_bus_manager.return_value = False
        with pytest.raises(ValueError):
            AbstractTransportInterface.__init__(self=self.mock_transport_interface,
                                                bus_manager=Mock(),
                                                message_records_number=Mock(),
                                                packet_records_number=Mock())
        self.mock_transport_interface.is_supported_bus_manager.assert_called_once()

    @pytest.mark.parametrize("bus_manager, message_records_number, packet_records_number", [
        ("bus_manager", "message_records_number", "packet_records_number"),
        (Mock(), Mock(), Mock()),
    ])
    def test_init__valid(self, bus_manager, message_records_number, packet_records_number):
        self.mock_transport_interface.is_supported_bus_manager.return_value = True
        AbstractTransportInterface.__init__(self=self.mock_transport_interface,
                                            bus_manager=bus_manager,
                                            message_records_number=message_records_number,
                                            packet_records_number=packet_records_number)
        self.mock_transport_interface.is_supported_bus_manager.assert_called_once_with(bus_manager)
        assert self.mock_transport_interface._AbstractTransportInterface__bus_manager == bus_manager
        # TODO: utilize message_records_number
        # TODO: utilize packet_records_number

    # bus_manager

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_bus_manager(self, value):
        self.mock_transport_interface._AbstractTransportInterface__bus_manager = value
        assert AbstractTransportInterface.bus_manager.fget(self.mock_transport_interface) \
               == self.mock_transport_interface._AbstractTransportInterface__bus_manager

    # packet_records_queue

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_packet_records_queue(self, value):
        self.mock_transport_interface._AbstractTransportInterface__packet_records_queue = value
        assert AbstractTransportInterface.packet_records_queue.fget(self.mock_transport_interface) \
               == self.mock_transport_interface._AbstractTransportInterface__packet_records_queue

    # message_records_queue

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_message_records_queue(self, value):
        self.mock_transport_interface._AbstractTransportInterface__message_records_queue = value
        assert AbstractTransportInterface.message_records_queue.fget(self.mock_transport_interface) \
               == self.mock_transport_interface._AbstractTransportInterface__message_records_queue

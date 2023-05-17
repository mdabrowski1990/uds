import pytest
from mock import Mock

from uds.transport_interface.abstract_transport_interface import AbstractTransportInterface, AbstractUdsPacket


@pytest.mark.skip
class TestAbstractTransportInterface:
    """Unit tests for `AbstractTransportInterface` class."""

    SCRIPT_LOCATION = "uds.transport_interface.abstract_transport_interface"

    def setup(self):
        self.mock_transport_interface = Mock(spec=AbstractTransportInterface)

    # __init__

    def test_init__value_error(self):
        self.mock_transport_interface.is_supported_bus_manager.return_value = False
        with pytest.raises(ValueError):
            AbstractTransportInterface.__init__(self=self.mock_transport_interface,
                                                bus_manager=Mock())
        self.mock_transport_interface.is_supported_bus_manager.assert_called_once()

    @pytest.mark.parametrize("bus_manager, message_records_number, packet_records_number", [
        ("bus_manager", "message_records_number", "packet_records_number"),
        (Mock(), Mock(), Mock()),
    ])
    def test_init__valid(self, bus_manager, message_records_number, packet_records_number):
        self.mock_transport_interface.is_supported_bus_manager.return_value = True
        AbstractTransportInterface.__init__(self=self.mock_transport_interface,
                                            bus_manager=bus_manager)
        self.mock_transport_interface.is_supported_bus_manager.assert_called_once_with(bus_manager)
        assert self.mock_transport_interface._AbstractTransportInterface__bus_manager == bus_manager

    # bus_manager

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_bus_manager(self, value):
        self.mock_transport_interface._AbstractTransportInterface__bus_manager = value
        assert AbstractTransportInterface.bus_manager.fget(self.mock_transport_interface) == value

    # send_packet

    @pytest.mark.asyncio
    async def test_send_packet(self):
        with pytest.raises(NotImplementedError):
            await AbstractTransportInterface.send_packet(self=self.mock_transport_interface,
                                                         packet=Mock(spec=AbstractUdsPacket))

    # receive_packet

    @pytest.mark.asyncio
    async def test_receive_packet(self):
        with pytest.raises(NotImplementedError):
            await AbstractTransportInterface.receive_packet(self=self.mock_transport_interface)

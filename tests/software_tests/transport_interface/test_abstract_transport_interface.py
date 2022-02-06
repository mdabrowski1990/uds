import pytest
from mock import Mock, patch

from uds.transport_interface.abstract_transport_interface import AbstractTransportInterface, \
    UdsMessageRecord, UdsMessage


class TestAbstractTransportInterface:
    """Unit tests for `AbstractTransportInterface` class."""

    SCRIPT_LOCATION = "uds.transport_interface.abstract_transport_interface"

    def setup(self):
        self.mock_transport_interface = Mock(spec=AbstractTransportInterface)
        # patching
        self._patcher_records_queue_class = patch(f"{self.SCRIPT_LOCATION}.RecordsQueue")
        self.mock_records_queue_class = self._patcher_records_queue_class.start()
        self._patcher_transmission_queue_class = patch(f"{self.SCRIPT_LOCATION}.TransmissionQueue")
        self.mock_transmission_queue_class = self._patcher_transmission_queue_class.start()

    def teardown(self):
        self._patcher_records_queue_class.stop()
        self._patcher_transmission_queue_class.stop()

    # __init__

    def test_init__value_error(self):
        self.mock_transport_interface.is_supported_bus_manager.return_value = False
        with pytest.raises(ValueError):
            AbstractTransportInterface.__init__(self=self.mock_transport_interface,
                                                bus_manager=Mock(),
                                                message_records_number=Mock())
        self.mock_transport_interface.is_supported_bus_manager.assert_called_once()

    @pytest.mark.parametrize("bus_manager, message_records_number, packet_records_number", [
        ("bus_manager", "message_records_number", "packet_records_number"),
        (Mock(), Mock(), Mock()),
    ])
    def test_init__valid(self, bus_manager, message_records_number, packet_records_number):
        self.mock_transport_interface.is_supported_bus_manager.return_value = True
        AbstractTransportInterface.__init__(self=self.mock_transport_interface,
                                            bus_manager=bus_manager,
                                            message_records_number=message_records_number)
        self.mock_transport_interface.is_supported_bus_manager.assert_called_once_with(bus_manager)
        self.mock_records_queue_class.assert_called_once_with(records_type=UdsMessageRecord,
                                                              history_size=message_records_number)
        self.mock_transmission_queue_class.assert_called_once_with(pdu_type=UdsMessage)
        assert self.mock_transport_interface._AbstractTransportInterface__bus_manager == bus_manager
        assert self.mock_transport_interface._AbstractTransportInterface__message_records_queue \
               == self.mock_records_queue_class.return_value
        assert self.mock_transport_interface._AbstractTransportInterface__message_transmission_queue \
               == self.mock_transmission_queue_class.return_value

    # _message_records_queue

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_message_records_queue__get(self, value):
        self.mock_transport_interface._AbstractTransportInterface__message_records_queue = value
        assert AbstractTransportInterface._message_records_queue.fget(self.mock_transport_interface) == value

    # _message_transmission_queue
    
    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_message_transmission_queue__get(self, value):
        self.mock_transport_interface._AbstractTransportInterface__message_transmission_queue = value
        assert AbstractTransportInterface._message_transmission_queue.fget(self.mock_transport_interface) == value

    # bus_manager

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_bus_manager(self, value):
        self.mock_transport_interface._AbstractTransportInterface__bus_manager = value
        assert AbstractTransportInterface.bus_manager.fget(self.mock_transport_interface) == value

    # message_records_history

    def test_message_records_history__get(self):
        assert AbstractTransportInterface.message_records_history.fget(self.mock_transport_interface) \
               == self.mock_transport_interface._message_records_queue.records_history

    # packet_records_history

    def test_packet_records_history__get(self):
        assert AbstractTransportInterface.packet_records_history.fget(self.mock_transport_interface) \
               == self.mock_transport_interface._packet_records_queue.records_history

    # await_packet_received

    @pytest.mark.asyncio
    async def test_await_packet_received(self):
        with pytest.raises(NotImplementedError):
            await AbstractTransportInterface.await_packet_received(self=self.mock_transport_interface)

    # await_packet_transmitted

    @pytest.mark.asyncio
    async def test_await_packet_transmitted(self):
        with pytest.raises(NotImplementedError):
            await AbstractTransportInterface.await_packet_transmitted(self=self.mock_transport_interface)

    # await_message_received

    @pytest.mark.asyncio
    async def test_await_message_received(self):
        with pytest.raises(NotImplementedError):
            await AbstractTransportInterface.await_message_received(self=self.mock_transport_interface)
            
    # await_message_transmitted

    @pytest.mark.asyncio
    async def test_await_message_transmitted(self):
        with pytest.raises(NotImplementedError):
            await AbstractTransportInterface.await_message_transmitted(self=self.mock_transport_interface)
            
    # schedule_packet

    def test_schedule_packet(self):
        with pytest.raises(NotImplementedError):
            AbstractTransportInterface.schedule_packet(self=self.mock_transport_interface, packet=Mock())
            
    # schedule_message

    def test_schedule_message(self):
        with pytest.raises(NotImplementedError):
            AbstractTransportInterface.schedule_message(self=self.mock_transport_interface, message=Mock())

import pytest
from mock import Mock

from uds.transport_interface.python_can_transport_interface import PyCanTransportInterface


class TestPyCanTransportInterface:
    """Unit tests for `PyCanTransportInterface` class."""

    def setup(self):
        self.mock_can_transport_interface = Mock(spec=PyCanTransportInterface)

    # n_as_measured

    def test_n_as_measured(self):
        with pytest.raises(NotImplementedError):
            PyCanTransportInterface.n_as_measured.fget(self.mock_can_transport_interface)

    # n_ar_measured

    def test_n_ar_measured(self):
        with pytest.raises(NotImplementedError):
            PyCanTransportInterface.n_ar_measured.fget(self.mock_can_transport_interface)
            
    # n_bs_measured

    def test_n_bs_measured(self):
        with pytest.raises(NotImplementedError):
            PyCanTransportInterface.n_bs_measured.fget(self.mock_can_transport_interface)
            
    # n_cr_measured

    def test_n_cr_measured(self):
        with pytest.raises(NotImplementedError):
            PyCanTransportInterface.n_cr_measured.fget(self.mock_can_transport_interface)
            
    # dlc

    def test_dlc__set(self):
        with pytest.raises(NotImplementedError):
            PyCanTransportInterface.dlc.fset(self.mock_can_transport_interface, Mock())
            
    # is_supported_bus_manager

    def test_is_supported_bus_manager(self):
        with pytest.raises(NotImplementedError):
            PyCanTransportInterface.is_supported_bus_manager(Mock())

    # await_packet_received

    @pytest.mark.asyncio
    async def test_await_packet_received(self):
        with pytest.raises(NotImplementedError):
            await PyCanTransportInterface.await_packet_received(self.mock_can_transport_interface)
            
    # await_packet_transmitted

    @pytest.mark.asyncio
    async def test_await_packet_transmitted(self):
        with pytest.raises(NotImplementedError):
            await PyCanTransportInterface.await_packet_transmitted(self.mock_can_transport_interface)

    # await_message_received

    @pytest.mark.asyncio
    async def test_await_message_received(self):
        with pytest.raises(NotImplementedError):
            await PyCanTransportInterface.await_message_received(self.mock_can_transport_interface)

    # await_message_transmitted

    @pytest.mark.asyncio
    async def test_await_message_transmitted(self):
        with pytest.raises(NotImplementedError):
            await PyCanTransportInterface.await_message_transmitted(self.mock_can_transport_interface)

    # send_packet

    def test_send_packet(self):
        with pytest.raises(NotImplementedError):
            PyCanTransportInterface.send_packet(self.mock_can_transport_interface, Mock())

    # send_message

    def test_send_message(self):
        with pytest.raises(NotImplementedError):
            PyCanTransportInterface.send_message(self.mock_can_transport_interface, Mock())

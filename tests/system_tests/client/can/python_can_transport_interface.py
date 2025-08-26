from random import choice

from tests.conftest import make_can_addressing_information

from can import Bus
from uds.can import CanAddressingFormat, PyCanTransportInterface

from ..test_client import AbstractClientTests


class TestClientWithPythonCanKvaser(AbstractClientTests):
    """Client tests for UDS over CAN with python-can package as network manager."""

    def _define_transport_interfaces(self):
        """Configure Transport Interfaces."""
        self.can_addressing_format: CanAddressingFormat = choice(list(CanAddressingFormat))
        self.addressing_information = make_can_addressing_information(self.can_addressing_format)
        self.can_interface_1 = Bus(interface="kvaser",
                                   channel=0,
                                   fd=True,
                                   receive_own_messages=True)
        self.can_interface_2 = Bus(interface="kvaser",
                                   channel=1,
                                   fd=True,
                                   receive_own_messages=True)
        self.transport_interface_1 = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=self.addressing_information)
        self.transport_interface_2 = PyCanTransportInterface(
            network_manager=self.can_interface_2,
            addressing_information=self.addressing_information.get_other_end())

    def teardown_method(self):
        """Clean up all tasks that were opened during test and close all connections."""
        self.can_interface_1.flush_tx_buffer()
        self.can_interface_2.flush_tx_buffer()
        super().teardown_method()
        self.can_interface_1.shutdown()
        self.can_interface_2.shutdown()

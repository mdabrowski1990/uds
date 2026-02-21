from random import choice
from time import sleep

from tests.conftest import make_can_addressing_information

from can import Bus
from uds.can import CanAddressingFormat, DefaultFlowControlParametersGenerator, PyCanTransportInterface
from uds.utilities import TimeMillisecondsAlias

from ..client import (
    AbstractBaseClientFunctionalityTests,
    AbstractClientErrorGuessing,
    AbstractClientTests,
    AbstractClientTimeoutsTests,
)


class PythonCanKvaserConfig(AbstractClientTests):
    """Client tests for UDS over CAN with python-can package as network manager."""

    transport_interface_1: PyCanTransportInterface
    transport_interface_2: PyCanTransportInterface

    TIMESTAMP_TOLERANCE: TimeMillisecondsAlias = 2  # python-can has low accuracy

    def _define_transport_interfaces(self):
        """Configure Transport Interfaces."""
        can_addressing_format: CanAddressingFormat = choice(list(CanAddressingFormat))
        addressing_information = make_can_addressing_information(can_addressing_format)
        self.can_interface_1 = Bus(interface="kvaser",
                                   channel=0,
                                   fd=True)
        self.can_interface_2 = Bus(interface="kvaser",
                                   channel=1,
                                   fd=True)
        transport_interface_1 = PyCanTransportInterface(
            network_manager=self.can_interface_1,
            addressing_information=addressing_information)
        self.transport_interface_1 = self.transport_logger(transport_interface_1)
        self.transport_interface_2 = PyCanTransportInterface(
            network_manager=self.can_interface_2,
            addressing_information=addressing_information.get_other_end())

    def teardown_method(self):
        """Clean up all tasks that were opened during test and close all connections."""
        self.can_interface_1.flush_tx_buffer()
        self.can_interface_2.flush_tx_buffer()
        super().teardown_method()
        self.can_interface_1.shutdown()
        self.can_interface_2.shutdown()
        sleep(0.1)

    def configure_slow_message_reception(self):
        """Change configuration of Transport Interfaces to reach timeouts easily."""
        self.transport_interface_1.flow_control_parameters_generator = DefaultFlowControlParametersGenerator(
            block_size=5,
            st_min=127)


class TestBaseClientFunctionalityTests(AbstractBaseClientFunctionalityTests, PythonCanKvaserConfig):
    """Base Client tests related to Client Functionalities for python-can Transport Interface with Kvaser interface."""


class TestClientTimeoutsTests(AbstractClientTimeoutsTests, PythonCanKvaserConfig):
    """Client tests related to timeout for python-can Transport Interface with Kvaser interface."""


class TestClientErrorGuessing(AbstractClientErrorGuessing, PythonCanKvaserConfig):
    """Error-guessing tests for Client."""

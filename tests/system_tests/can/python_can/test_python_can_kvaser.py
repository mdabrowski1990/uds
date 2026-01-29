from can import Bus

from .python_can import (
    AbstractCanPacketTests,
    AbstractErrorGuessingTests,
    AbstractFullDuplexTests,
    AbstractPythonCanTests,
    AbstractSegmentedMessageTests,
    AbstractUnsegmentedMessageTests,
    AbstractUseCaseTests,
)

# Config

class KvaserConfig(AbstractPythonCanTests):
    """Configuration for python-can Transport Interface tests with Kvaser CAN interfaces."""

    MAKE_TIMING_CHECKS = True

    def _define_interfaces(self):
        """Configure CAN bus objects that manage CAN interfaces."""
        self.can_interface_1 = Bus(interface="kvaser",
                                   channel=0,
                                   fd=True)
        self.can_interface_2 = Bus(interface="kvaser",
                                   channel=1,
                                   fd=True)


# Can Packets Transmission and Reception

class TestKvaserCanPacket(AbstractCanPacketTests, KvaserConfig):
    """CAN packets related system tests for python-can Transport Interface."""
    # TODO: remove - passing


# Messages Transmission and Reception

class TestKvaserUnsegmentedMessage(AbstractUnsegmentedMessageTests, KvaserConfig):
    """Unsegmented UDS message related system tests for python-can Transport Interface."""
    # TODO: remove - passing



class TestKvaserSegmentedMessage(AbstractSegmentedMessageTests, KvaserConfig):
    """Segmented UDS message related system tests for python-can Transport Interface."""
    # TODO: remove - passing


# Full Duplex

class TestKvaserFullDuplex(AbstractFullDuplexTests, KvaserConfig):
    """Full-Duplex related system tests for python-can Transport Interface."""
    # TODO: failing


# Use-Cases

class TestKvaserUseCase(AbstractUseCaseTests, KvaserConfig):
    """Use case based system tests for python-can Transport Interface."""
    # TODO: test_async_send_message_on_one_receive_on_other_interface failing



# Error Guessing

class TestKvaserErrorGuessing(AbstractErrorGuessingTests, KvaserConfig):
    """Error guessing system tests for python-can Transport Interface."""
    # TODO: remove - passing

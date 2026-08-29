from can import Bus
from uds.utilities import TimeMillisecondsAlias

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

class VectorConfig(AbstractPythonCanTests):
    """Configuration for python-can Transport Interface tests with Vector CAN interfaces."""

    MAKE_TIMING_CHECKS: bool = True

    def _define_interfaces(self):
        """Configure CAN bus objects that manage CAN interfaces."""
        self.can_interface_1 = Bus(interface="vector",
                                   app_name="python-can",
                                   channel=0,
                                   fd=True,
                                   receive_own_messages=True)
        self.can_interface_2 = Bus(interface="vector",
                                   app_name="python-can",
                                   channel=1,
                                   fd=True,
                                   receive_own_messages=True)


# Can Packets Transmission and Reception

class TestVectorCanPacket(AbstractCanPacketTests, VectorConfig):
    """CAN packets related system tests for python-can Transport Interface."""


# Messages Transmission and Reception

class TestVectorUnsegmentedMessage(AbstractUnsegmentedMessageTests, VectorConfig):
    """Unsegmented UDS message related system tests for python-can Transport Interface."""


class TestVectorSegmentedMessage(AbstractSegmentedMessageTests, VectorConfig):
    """Segmented UDS message related system tests for python-can Transport Interface."""


# Full Duplex

class TestVectorFullDuplex(AbstractFullDuplexTests, VectorConfig):
    """Full-Duplex related system tests for python-can Transport Interface."""


# Use-Cases

class TestVectorUseCase(AbstractUseCaseTests, VectorConfig):
    """Use case based system tests for python-can Transport Interface."""


# Error Guessing

class TestVectorErrorGuessing(AbstractErrorGuessingTests, VectorConfig):
    """Error guessing system tests for python-can Transport Interface."""

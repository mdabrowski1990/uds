from can import Bus

from .python_can import (
    AbstractCanPacketTests,
    AbstractErrorGuessingTests,
    AbstractMessageTests,
    AbstractPythonCanTests,
    AbstractUseCaseTests,
)

# Configs

class KvaserConfig(AbstractPythonCanTests):
    """
    Configuration for Python CAN Transport Interface tests with Kvaser CAN interfaces.

    Interfaces receive own CAN Frames.
    """

    def _define_interfaces(self):
        """Configure CAN bus objects that manage CAN interfaces."""
        self.can_interface_1 = Bus(interface="kvaser",
                                   channel=0,
                                   fd=True)
        self.can_interface_2 = Bus(interface="kvaser",
                                   channel=1,
                                   fd=True)

# Can Packet

class TestKvaserCanPacket(AbstractCanPacketTests, KvaserConfig):
    """CAN packets related system tests for Python CAN Transport Interface."""

# Message

class TestKvaserMessage(AbstractMessageTests, KvaserConfig):
    """UDS message related system tests for Python CAN Transport Interface."""

# Use-Cases

class TestKvaserUseCase(AbstractUseCaseTests, KvaserConfig):
    """Use case based system tests for Python CAN Transport Interface."""

# Error Guessing

class TestKvaserErrorGuessing(AbstractErrorGuessingTests, KvaserConfig):
    """Error guessing system tests for Python CAN Transport Interface."""

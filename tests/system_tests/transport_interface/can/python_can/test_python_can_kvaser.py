from can import Bus

from .python_can import (
    AbstractCanPacketTests,
    AbstractErrorGuessingTests,
    AbstractMessageTests,
    AbstractPythonCanTests,
    AbstractUseCaseTests,
)


class KvaserConfig(AbstractPythonCanTests):
    """Configuration for Python CAN Transport Interface tests with Kvaser CAN interfaces."""

    def setup_class(self):
        self.can_interface_1 = Bus(interface="kvaser", channel=0, fd=True, receive_own_messages=True)
        self.can_interface_2 = Bus(interface="kvaser", channel=1, fd=True, receive_own_messages=True)


class TestKvaserCanPacket(AbstractCanPacketTests, KvaserConfig):
    """CAN packets related system tests for Python CAN Transport Interface."""

    MAKE_TIMING_CHECKS: bool = False


class TestKvaserMessage(AbstractMessageTests, KvaserConfig):
    """UDS message related system tests for Python CAN Transport Interface."""

    MAKE_TIMING_CHECKS: bool = False


class TestKvaserUseCase(AbstractUseCaseTests, KvaserConfig):
    """Use case based system tests for Python CAN Transport Interface."""

    MAKE_TIMING_CHECKS: bool = True


class TestKvaserErrorGuessing(AbstractErrorGuessingTests, KvaserConfig):
    """Error guessing system tests for Python CAN Transport Interface."""

    MAKE_TIMING_CHECKS: bool = False

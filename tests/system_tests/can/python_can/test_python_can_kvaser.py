from can import Bus

from .python_can import (
    AbstractCanPacketTests,
    AbstractErrorGuessingTests,
    AbstractMessageTests,
    AbstractPythonCanTests,
    AbstractUseCaseTests,
)


# Receive Own Frames


class KvaserConfig_ReceiveOwnFrames(AbstractPythonCanTests):
    """
    Configuration for Python CAN Transport Interface tests with Kvaser CAN interfaces.

    Interfaces receive own CAN Frames.
    """

    RECEIVE_OWN_FRAMES = True

    def _define_interfaces(self):
        """Configure CAN bus objects that manage CAN interfaces."""
        self.can_interface_1 = Bus(interface="kvaser",
                                   channel=0,
                                   fd=True,
                                   receive_own_messages=True)
        self.can_interface_2 = Bus(interface="kvaser",
                                   channel=1,
                                   fd=True,
                                   receive_own_messages=True)

class TestKvaserCanPacket_ReceiveOwnFrames(AbstractCanPacketTests, KvaserConfig_ReceiveOwnFrames):
    """CAN packets related system tests for Python CAN Transport Interface."""

    # TODO: https://github.com/mdabrowski1990/uds/issues/228 - set MAKE_TIMING_CHECKS to true when resolved
    MAKE_TIMING_CHECKS: bool = False


class TestKvaserMessage_ReceiveOwnFrames(AbstractMessageTests, KvaserConfig_ReceiveOwnFrames):
    """UDS message related system tests for Python CAN Transport Interface."""

    # TODO: https://github.com/mdabrowski1990/uds/issues/228 - set MAKE_TIMING_CHECKS to true when resolved
    MAKE_TIMING_CHECKS: bool = False


class TestKvaserUseCase_ReceiveOwnFrames(AbstractUseCaseTests, KvaserConfig_ReceiveOwnFrames):
    """Use case based system tests for Python CAN Transport Interface."""


class TestKvaserErrorGuessing_ReceiveOwnFrames(AbstractErrorGuessingTests, KvaserConfig_ReceiveOwnFrames):
    """Error guessing system tests for Python CAN Transport Interface."""

    # TODO: https://github.com/mdabrowski1990/uds/issues/228 - set MAKE_TIMING_CHECKS to true when resolved
    MAKE_TIMING_CHECKS: bool = False


# Do Not Receive Own Frames


class KvaserConfig_DoNotReceiveOwnFrames(AbstractPythonCanTests):
    """
    Configuration for Python CAN Transport Interface tests with Kvaser CAN interfaces.

    Interfaces do not receive own CAN Frames.
    """

    RECEIVE_OWN_FRAMES = False

    def _define_interfaces(self):
        """Configure CAN bus objects that manage CAN interfaces."""
        self.can_interface_1 = Bus(interface="kvaser",
                                   channel=0,
                                   fd=True,
                                   receive_own_messages=False)
        self.can_interface_2 = Bus(interface="kvaser",
                                   channel=1,
                                   fd=True,
                                   receive_own_messages=False)

class TestKvaserCanPacket_DoNotReceiveOwnFrames(AbstractCanPacketTests, KvaserConfig_DoNotReceiveOwnFrames):
    """CAN packets related system tests for Python CAN Transport Interface."""


class TestKvaserMessage_DoNotReceiveOwnFrames(AbstractMessageTests, KvaserConfig_DoNotReceiveOwnFrames):
    """UDS message related system tests for Python CAN Transport Interface."""


class TestKvaserUseCase_DoNotReceiveOwnFrames(AbstractUseCaseTests, KvaserConfig_DoNotReceiveOwnFrames):
    """Use case based system tests for Python CAN Transport Interface."""


class TestKvaserErrorGuessing_DoNotReceiveOwnFrames(AbstractErrorGuessingTests, KvaserConfig_DoNotReceiveOwnFrames):
    """Error guessing system tests for Python CAN Transport Interface."""

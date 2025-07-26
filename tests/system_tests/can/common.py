from abc import ABC, abstractmethod

from uds.utilities import TimeMillisecondsAlias


class AbstractCanTests(ABC):
    """Abstract class for system tests (with hardware) for Diagnostic over CAN (DoCAN)."""

    TASK_TIMING_TOLERANCE: TimeMillisecondsAlias = 30.
    WAIT_AFTER_TEST_CASE: TimeMillisecondsAlias

    @abstractmethod
    def setup_class(self):
        """Configure CAN bus connections."""

    @abstractmethod
    def teardown_class(self):
        """Safely close CAN bus connections."""

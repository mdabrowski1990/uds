from abc import ABC, abstractmethod

from uds.utilities import TimeMillisecondsAlias


class AbstractCanTests(ABC):
    """Abstract class for system tests (with hardware) for Diagnostic over CAN (DoCAN)."""

    TASK_TIMING_TOLERANCE: TimeMillisecondsAlias = 30.  # ms
    DELAY_AFTER_RECEIVING_FRAME: TimeMillisecondsAlias  # ms
    DELAY_AFTER_RECEIVING_MESSAGE: TimeMillisecondsAlias  # ms

    @abstractmethod
    def setup_class(self):
        """Configure CAN bus connections."""

    @abstractmethod
    def teardown_class(self):
        """Safely close CAN bus connections."""

    @property
    @abstractmethod
    def DELAY_AFTER_RECEIVING_FRAME(self) -> TimeMillisecondsAlias:
        ...

    @property
    @abstractmethod
    def DELAY_AFTER_RECEIVING_MESSAGE(self) -> TimeMillisecondsAlias:
        ...

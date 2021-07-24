"""Container with all constant values used by the module."""

from .types import TimeMilliseconds

DEFAULT_P2_SERVER_MAX: TimeMilliseconds = 50  # ISO 14229-2 recommended value
DEFAULT_P2EXT_SERVER_MAX: TimeMilliseconds = 5000  # ISO 14229-2 recommended value
DEFAULT_P4_SERVER_MAX: TimeMilliseconds = 10000  # Vehicle manufacturer specific value

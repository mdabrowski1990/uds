"""Custom exception used within the project."""


class ReassignmentError(Exception):
    """Attempt to set a new value of an attribute that cannot be changed after the initial value was already set."""

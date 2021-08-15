"""Custom exception used within the project."""


class ReassignmentError(Exception):
    """Trying to set a new value to a variable or an attribute which cannot be changed."""

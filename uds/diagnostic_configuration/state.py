"""Implementation for diagnostic communication state."""

__all__ = ["State"]

from typing import Any, Collection, FrozenSet, Optional
from warnings import warn


class State:
    """
    States relevant for diagnostic communication.

    Typical states:
    - diagnostic session
    - unlocked Security Access level
    - Authentication status
    - vehicle speed
    - engine status (ON/OFF)
    """

    def __init__(self, name: str, possible_values: Collection[Any]) -> None:
        """
        Define a state.

        :param name: Name of the state.
        :param possible_values: All potential values that can be assigned to a state.
        """
        self.name = name
        self.possible_values = possible_values
        self.__current_value: Optional[Any] = None

    @property
    def name(self) -> str:
        """Get state name."""
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """
        Set state name.

        :param name: Value to set (whitespaces will be stripped).

        :raise TypeError: Value must be a string.
        :raise ValueError: Value must not consist of whitespaces only.
        """
        if not isinstance(name, str):
            raise TypeError(f"Provided name is not str type. Actual type: {type(name)}.")
        stripped_name = name.strip()
        if not stripped_name:
            raise ValueError("Name must not consist of whitespace characters only.")
        if stripped_name != name:
            warn(category=UserWarning,
                 message="Given name was containing whitespaces as suffix or prefix. "
                         f"They were removed and {stripped_name!r} is assigned instead.",
                 stacklevel=2)
        self.__name = stripped_name

    @property
    def possible_values(self) -> FrozenSet[Any]:
        """Get set with all values that can be assigned to this state."""
        return self.__possible_values

    @possible_values.setter
    def possible_values(self, values: Collection[Any]) -> None:
        """Set all potential values that can be assigned to a state."""
        self.__possible_values = frozenset(values)
        self.__current_value = None  # if possible values are change, then the current state is also affected

    @property
    def current_value(self) -> Optional[Any]:
        """Get currently assigned value."""
        return self.__current_value

    @current_value.setter
    def current_value(self, value: Optional[Any]) -> None:
        """
        Set currently assigned value.

        :param value: Value to set.

        :raise ValueError: Given value is not a valid state.
        """
        if value is not None and value not in self.possible_values:
            raise ValueError(f"Value {value!r} is not a correct state for {self.name}.")
        self.__current_value = value

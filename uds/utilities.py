"""Module with various helper function that are used within the package."""

__all__ = ["RepeatedCall"]

from typing import Union, Callable, Iterable, Optional
from threading import Timer
from warnings import warn

from .common_types import TimeSeconds


class RepeatedCall:
    """Class for cyclically calling function in another thread."""

    def __init__(self,
                 interval: TimeSeconds,
                 function: Callable,
                 function_args: Optional[Iterable] = None,  # pylint: disable=unsubscriptable-object
                 function_kwargs: Optional[dict] = None,  # pylint: disable=unsubscriptable-object
                 number_of_calls: Union[int, float] = float("inf")) -> None:  # pylint: disable=unsubscriptable-object
        """
        Configure thread for cyclically calling a function with provided arguments.

        :param interval: Time in seconds describing the interval with which the function to be executed.
        :param function: Function to be called.
        :param number_of_calls: Number of calls the function to be executed.
            Use float("inf") if you do not want to provide precise number of calls to execute.
        :param function_args: Arguments to pass to the function at every call.
        :param function_kwargs: Keyword arguments to pass to the function at every call.
        """
        self._timer: Optional[Timer] = None  # pylint: disable=unsubscriptable-object
        self.interval = interval
        self.function = function
        self.function_args = function_args if function_args else ()
        self.function_kwargs = function_kwargs if function_kwargs else {}
        self.is_running = False
        self.calls_left = number_of_calls

    def start(self, delay: TimeSeconds = 0) -> None:
        """
        Start to call the function cyclically.

        :param delay: Time in seconds after which the first call to be executed.
        """
        if not self.is_running:
            self.is_running = True
            if delay > 0:
                self._timer = Timer(interval=delay, function=self._execute)
                self._timer.start()
            else:
                self._execute()
        else:
            warn(message="Cyclical calling of the function was already started.", category=RuntimeWarning)

    def stop(self):
        """Stop cyclical calling of the function."""
        if self.is_running:
            self._timer.cancel()
            self.is_running = False
        else:
            warn(message="Cyclical calling of the function was already stopped.", category=RuntimeWarning)

    def _execute(self):
        """Execute the function and schedule another call if not finished."""
        self.function(*self.function_args, **self.function_kwargs)
        self.calls_left -= 1
        if self.calls_left > 0 and self.is_running:
            self._timer = Timer(interval=self.interval, function=self._execute)
            self._timer.start()
        else:
            self.is_running = False

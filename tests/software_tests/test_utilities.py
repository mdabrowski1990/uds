import pytest
from mock import Mock, patch

from uds.utilities import RepeatedCall


class TestRepeatedCall:

    SOURCE_SCRIPT_LOCATION = "uds.utilities"

    def setup(self):
        self.mock_repeated_call = Mock(spec=RepeatedCall, interval=Mock(), _timer=Mock(), function=Mock())
        # patching
        self._patcher_warn = patch(f"{self.SOURCE_SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()
        self._patcher_timer = patch(f"{self.SOURCE_SCRIPT_LOCATION}.Timer")
        self.mock_timer = self._patcher_timer.start()

    def teardown(self):
        self._patcher_warn.stop()
        self._patcher_timer.stop()

    # __init__

    @pytest.mark.parametrize("interval", [0.01, 2])
    @pytest.mark.parametrize("function", [abs, print])
    @pytest.mark.parametrize("args", [range(10), "abc"])
    @pytest.mark.parametrize("kwargs", [dict(a=1, b=2), dict(p1="value 1", p2="value 2")])
    @pytest.mark.parametrize("number_of_calls", [1, float("inf")])
    def test_init(self, interval, function, args, kwargs, number_of_calls):
        RepeatedCall.__init__(self=self.mock_repeated_call, interval=interval, function=function, function_args=args,
                              function_kwargs=kwargs, number_of_calls=number_of_calls)
        assert self.mock_repeated_call.interval == interval
        assert self.mock_repeated_call.function == function
        assert self.mock_repeated_call.function_args == args
        assert self.mock_repeated_call.function_kwargs == kwargs
        assert self.mock_repeated_call.calls_left == number_of_calls

    @pytest.mark.parametrize("interval", [0.01, 2])
    @pytest.mark.parametrize("function", [abs, print])
    def test_init__no_optional_params(self, interval, function):
        RepeatedCall.__init__(self=self.mock_repeated_call, interval=interval, function=function)
        assert self.mock_repeated_call.interval == interval
        assert self.mock_repeated_call.function == function
        assert self.mock_repeated_call.function_args == ()
        assert self.mock_repeated_call.function_kwargs == {}
        assert self.mock_repeated_call.calls_left == float("inf")

    # start

    @pytest.mark.parametrize("delay", [0, 1.1, 5])
    def test_start__already_running(self, delay):
        self.mock_repeated_call.is_running = True
        assert RepeatedCall.start(self=self.mock_repeated_call, delay=delay) is None
        self.mock_timer.assert_not_called()
        self.mock_repeated_call._execute.assert_not_called()
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("delay", [1.1, 5])
    def test_start__with_delay(self, delay):
        self.mock_repeated_call.is_running = False
        assert RepeatedCall.start(self=self.mock_repeated_call, delay=delay) is None
        assert self.mock_repeated_call.is_running is True
        self.mock_timer.assert_called_once_with(interval=delay, function=self.mock_repeated_call._execute)
        self.mock_timer.return_value.start.assert_called_once()
        self.mock_warn.assert_not_called()

    def test_start__without_delay(self):
        self.mock_repeated_call.is_running = False
        assert RepeatedCall.start(self=self.mock_repeated_call) is None
        assert self.mock_repeated_call.is_running is True
        self.mock_repeated_call._execute.assert_called_once()
        self.mock_warn.assert_not_called()

    # stop

    def test_stop__already_stopped(self):
        self.mock_repeated_call.is_running = False
        assert RepeatedCall.stop(self=self.mock_repeated_call) is None
        self.mock_repeated_call._timer.cancel.assert_not_called()
        assert self.mock_repeated_call.is_running is False
        self.mock_warn.assert_called_once()

    def test_stop__to_be_stopped(self):
        self.mock_repeated_call.is_running = True
        assert RepeatedCall.stop(self=self.mock_repeated_call) is None
        self.mock_repeated_call._timer.cancel.assert_called_once()
        assert self.mock_repeated_call.is_running is False
        self.mock_warn.assert_not_called()

    # _execute

    @pytest.mark.parametrize("calls_left", [1, 2, float("inf")])
    @pytest.mark.parametrize("args", [range(10), "abc"])
    @pytest.mark.parametrize("kwargs", [dict(a=1, b=2), dict(p1="value 1", p2="value 2")])
    @pytest.mark.parametrize("is_running", [True, False])
    def test_execute__always(self, calls_left, args, kwargs, is_running):
        self.mock_repeated_call.calls_left = calls_left
        self.mock_repeated_call.function_args = args
        self.mock_repeated_call.function_kwargs = kwargs
        self.mock_repeated_call.is_running = is_running
        assert RepeatedCall._execute(self=self.mock_repeated_call) is None
        self.mock_repeated_call.function.assert_called_once_with(*args, **kwargs)
        assert self.mock_repeated_call.calls_left == calls_left-1

    @pytest.mark.parametrize("calls_left", [1, 2, float("inf")])
    @pytest.mark.parametrize("args", [range(10), "abc"])
    @pytest.mark.parametrize("kwargs", [dict(a=1, b=2), dict(p1="value 1", p2="value 2")])
    def test_execute__not_running(self, calls_left, args, kwargs):
        self.mock_repeated_call.calls_left = calls_left
        self.mock_repeated_call.function_args = args
        self.mock_repeated_call.function_kwargs = kwargs
        self.mock_repeated_call.is_running = False
        assert RepeatedCall._execute(self=self.mock_repeated_call) is None
        self.mock_repeated_call._timer.start.assert_not_called()

    @pytest.mark.parametrize("calls_left", [1, 0, 0.5, -0.5])
    @pytest.mark.parametrize("args", [range(10), "abc"])
    @pytest.mark.parametrize("kwargs", [dict(a=1, b=2), dict(p1="value 1", p2="value 2")])
    @pytest.mark.parametrize("is_running", [True, False])
    def test_execute__last_call(self, calls_left, args, kwargs, is_running):
        self.mock_repeated_call.calls_left = calls_left
        self.mock_repeated_call.function_args = args
        self.mock_repeated_call.function_kwargs = kwargs
        self.mock_repeated_call.is_running = False
        assert RepeatedCall._execute(self=self.mock_repeated_call) is None
        assert self.mock_repeated_call.is_running is False
        self.mock_repeated_call._timer.start.assert_not_called()

    @pytest.mark.parametrize("calls_left", [2, 43, float("inf")])
    @pytest.mark.parametrize("args", [range(10), "abc"])
    @pytest.mark.parametrize("kwargs", [dict(a=1, b=2), dict(p1="value 1", p2="value 2")])
    def test_execute__call_again(self, calls_left, args, kwargs):
        self.mock_repeated_call.calls_left = calls_left
        self.mock_repeated_call.function_args = args
        self.mock_repeated_call.function_kwargs = kwargs
        self.mock_repeated_call.is_running = True
        assert RepeatedCall._execute(self=self.mock_repeated_call) is None
        assert self.mock_repeated_call.is_running is True
        self.mock_repeated_call.function.assert_called_once_with(*args, **kwargs)
        self.mock_repeated_call._timer.start.assert_called_once()

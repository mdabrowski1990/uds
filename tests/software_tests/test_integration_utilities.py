import pytest
from mock import Mock
from time import sleep

from uds.utilities import RepeatedCall


@pytest.mark.integration
class TestRepeatedCallIntegration:

    @pytest.mark.parametrize("delay", [0.5, 1])
    def test_delayed_call(self, delay):
        """Check that function is called with proper delay."""
        # preparation
        function_to_call = Mock()
        caller = RepeatedCall(interval=0.0000001, function=function_to_call, number_of_calls=1)
        function_to_call.assert_not_called()
        # start caller
        caller.start(delay=delay)
        # wait less than call delay
        sleep(0.9*delay)
        # verify that not called
        function_to_call.assert_not_called()
        # wait for the first call
        sleep(0.2*delay)
        # verify that called once
        function_to_call.assert_called_once()

    @pytest.mark.parametrize("interval", [0.1, 0.25])
    def test_few_calls(self, interval):
        """Check that function is called with proper interval."""
        # preparation
        function_to_call = Mock()
        caller = RepeatedCall(interval=interval, function=function_to_call, number_of_calls=3)
        function_to_call.assert_not_called()
        # start caller
        caller.start()
        function_to_call.assert_called_once()
        # wait less than call delay
        sleep(0.5 * interval)
        # verify that not called again
        function_to_call.assert_called_once()
        # wait for the second call
        sleep(interval)
        # verify that called twice
        assert function_to_call.call_count == 2
        # wait for the third call
        sleep(interval)
        # verify that called three time
        assert function_to_call.call_count == 3
        assert caller.is_running is False
        # wait another interval
        sleep(interval)
        # verify that there are no other calls
        assert function_to_call.call_count == 3
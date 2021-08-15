from uds.messages.request import UdsMessage, UdsRequest


class TestsUdsRequest:
    """Tests for UdsRequest class."""

    # inheritance

    def test_inherits_after_uds_message(self):
        assert issubclass(UdsRequest, UdsMessage)

import pytest

from uds.transport_interface.client import TransportInterfaceClient, TransportInterface


class TestsTransportInterfaceClient:
    """Tests for TransportInterfaceClient class."""

    # inheritance

    def test_inherits_after_uds_message(self):
        assert issubclass(TransportInterfaceClient, TransportInterface)

import pytest

from uds.transport_interface.server import TransportInterfaceServer, TransportInterface


class TestsTransportInterfaceServer:
    """Tests for TransportInterfaceServer class."""

    # inheritance

    def test_inherits_after_uds_message(self):
        assert issubclass(TransportInterfaceServer, TransportInterface)

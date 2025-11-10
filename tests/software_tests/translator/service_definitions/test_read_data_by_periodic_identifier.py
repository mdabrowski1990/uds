import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.read_data_by_periodic_identifier import READ_DATA_BY_PERIODIC_IDENTIFIER

class TestReadDataByPeriodicIdentifier:
    """Unit tests for `ReadDataByPeriodicIdentifier` service."""

    def test_request_sid(self):
        assert READ_DATA_BY_PERIODIC_IDENTIFIER.request_sid == RequestSID.ReadDataByPeriodicIdentifier

    def test_response_sid(self):
        assert READ_DATA_BY_PERIODIC_IDENTIFIER.response_sid == ResponseSID.ReadDataByPeriodicIdentifier

# TODO: more tests
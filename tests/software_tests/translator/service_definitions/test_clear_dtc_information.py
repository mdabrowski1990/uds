import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.clear_diagnostic_information import (
    CLEAR_DIAGNOSTIC_INFORMATION,
    CLEAR_DIAGNOSTIC_INFORMATION_2013,
    CLEAR_DIAGNOSTIC_INFORMATION_2020,
)


class TestClearDiagnosticInformation:
    """Unit tests for `ClearDiagnosticInformation` service."""

    def test_request_sid(self):
        assert CLEAR_DIAGNOSTIC_INFORMATION_2013.request_sid == RequestSID.ClearDiagnosticInformation
        assert CLEAR_DIAGNOSTIC_INFORMATION_2020.request_sid == RequestSID.ClearDiagnosticInformation

    def test_response_sid(self):
        assert CLEAR_DIAGNOSTIC_INFORMATION_2013.response_sid == ResponseSID.ClearDiagnosticInformation
        assert CLEAR_DIAGNOSTIC_INFORMATION_2020.response_sid == ResponseSID.ClearDiagnosticInformation

    def test_default_translator(self):
        assert CLEAR_DIAGNOSTIC_INFORMATION is CLEAR_DIAGNOSTIC_INFORMATION_2020


@pytest.mark.integration
class TestClearDiagnosticInformation2020Integration:
    """Integration tests for `ClearDiagnosticInformation` service."""

    @pytest.mark.parametrize("payload, decoded_message", [
        (
            [0x14, 0xFF, 0xFF, 0xFF],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'ClearDiagnosticInformation',
                    'raw_value': 0x14,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 24,
                    'name': 'groupOfDTC',
                    'physical_value': 0xFFFFFF,
                    'raw_value': 0xFFFFFF,
                    'unit': None
                },
            )
        ),
        (
            [0x14, 0x12, 0x34, 0x56, 0xA5],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'ClearDiagnosticInformation',
                    'raw_value': 0x14,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 24,
                    'name': 'groupOfDTC',
                    'physical_value': 0x123456,
                    'raw_value': 0x123456,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'MemorySelection',
                    'physical_value': 0xA5,
                    'raw_value': 0xA5,
                    'unit': None
                },
            )
        ),
        (
            [0x54],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'ClearDiagnosticInformation',
                    'raw_value': 0x54,
                    'unit': None
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert CLEAR_DIAGNOSTIC_INFORMATION_2020.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        (
            {
                "groupOfDTC": 0xF0E1D2,
                "MemorySelection": None,
            },
            RequestSID.ClearDiagnosticInformation,
            None,
            bytearray([0x14, 0xF0, 0xE1, 0xD2])
        ),
        (
            {
                "groupOfDTC": 0xFFFFFF,
                "MemorySelection": 0x5A,
            },
            RequestSID.ClearDiagnosticInformation,
            None,
            bytearray([0x14, 0xFF, 0xFF, 0xFF, 0x5A])
        ),
        (
            {},
            None,
            ResponseSID.ClearDiagnosticInformation,
            bytearray([0x54])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert CLEAR_DIAGNOSTIC_INFORMATION_2020.encode(data_records_values=data_records_values,
                                                        sid=sid,
                                                        rsid=rsid) == payload

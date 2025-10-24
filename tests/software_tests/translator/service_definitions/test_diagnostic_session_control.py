import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.diagnostic_session_control import DIAGNOSTIC_SESSION_CONTROL


class TestDiagnosticSessionControl:
    """Unit tests for `DiagnosticSessionControl` service."""

    def test_request_sid(self):
        assert DIAGNOSTIC_SESSION_CONTROL.request_sid == RequestSID.DiagnosticSessionControl

    def test_response_sid(self):
        assert DIAGNOSTIC_SESSION_CONTROL.response_sid == ResponseSID.DiagnosticSessionControl


@pytest.mark.integration
class TestDiagnosticSessionControlIntegration:
    """Integration tests for `DiagnosticSessionControl` service."""

    @pytest.mark.parametrize("payload, decoded_message", [
        (
            [0x10, 0x01],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'DiagnosticSessionControl',
                    'raw_value': 0x10,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'suppressPosRspMsgIndicationBit',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'diagnosticSessionType',
                            'physical_value': 'defaultSession',
                            'raw_value': 1,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 1,
                    'raw_value': 1,
                    'unit': None
                },
            )
        ),
        (
            [0x50, 0x03, 0xF1, 0xE2, 0xD3, 0xC4],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'DiagnosticSessionControl',
                    'raw_value': 0x50,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'suppressPosRspMsgIndicationBit',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'diagnosticSessionType',
                            'physical_value': 'extendedDiagnosticSession',
                            'raw_value': 3,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 3,
                    'raw_value': 3,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 16,
                            'name': 'P2Server_max',
                            'physical_value': 0xF1E2,
                            'raw_value': 0xF1E2,
                            'unit': 'ms'
                        },
                        {
                            'children': (),
                            'length': 16,
                            'name': 'P2*Server_max',
                            'physical_value': 542120,
                            'raw_value': 0xD3C4,
                            'unit': 'ms'
                        },
                    ),
                    'length': 32,
                    'name': 'sessionParameterRecord',
                    'physical_value': 0xF1E2D3C4,
                    'raw_value': 0xF1E2D3C4,
                    'unit': None
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert DIAGNOSTIC_SESSION_CONTROL.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": True,
                    "diagnosticSessionType": 0x02
                }
            },
            RequestSID.DiagnosticSessionControl,
            None,
            bytearray([0x10, 0x82])
        ),
        (
            {
                "SubFunction": 0x04,
                "sessionParameterRecord": {
                    "P2Server_max": 0xA1B2,
                    "P2*Server_max": 0xC3D4,
                }
            },
            None,
            ResponseSID.DiagnosticSessionControl,
            bytearray([0x50, 0x04, 0xA1, 0xB2, 0xC3, 0xD4])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert DIAGNOSTIC_SESSION_CONTROL.encode(data_records_values=data_records_values,
                                                 sid=sid,
                                                 rsid=rsid) == payload

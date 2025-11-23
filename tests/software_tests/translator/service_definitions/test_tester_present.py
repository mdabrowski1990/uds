import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.tester_present import TESTER_PRESENT


class TestTesterPresent:
    """Unit tests for `TesterPresent` service."""

    def test_request_sid(self):
        assert TESTER_PRESENT.request_sid == RequestSID.TesterPresent

    def test_response_sid(self):
        assert TESTER_PRESENT.response_sid == ResponseSID.TesterPresent


@pytest.mark.integration
class TestTesterPresentIntegration:
    """Integration tests for `TesterPresent` service."""

    @pytest.mark.parametrize("payload, decoded_message", [
        (
            [0x3E, 0x00],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'TesterPresent',
                    'raw_value': 0x3E,
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
                            'name': 'zeroSubFunction',
                            'physical_value': 'zeroSubFunction',
                            'raw_value': 0x00,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x00,
                    'raw_value': 0x00,
                    'unit': None
                },
            )
        ),
        (
            [0x3E, 0xFF],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'TesterPresent',
                    'raw_value': 0x3E,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'suppressPosRspMsgIndicationBit',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'zeroSubFunction',
                            'physical_value': 0x7F,
                            'raw_value': 0x7F,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0xFF,
                    'raw_value': 0xFF,
                    'unit': None
                },
            )
        ),
        (
            [0x7E, 0x40],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'TesterPresent',
                    'raw_value': 0x7E,
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
                            'name': 'zeroSubFunction',
                            'physical_value': 0x40,
                            'raw_value': 0x40,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x40,
                    'raw_value': 0x40,
                    'unit': None
                },
            )
        ),
        (
            [0x7E, 0x80],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'TesterPresent',
                    'raw_value': 0x7E,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'suppressPosRspMsgIndicationBit',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'zeroSubFunction',
                            'physical_value': 'zeroSubFunction',
                            'raw_value': 0x00,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x80,
                    'raw_value': 0x80,
                    'unit': None
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert TESTER_PRESENT.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        (
            {
                "SubFunction": 0x00,
            },
            RequestSID.TesterPresent,
            None,
            bytearray([0x3E, 0x00])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "zeroSubFunction": 0x23,
                },
            },
            None,
            ResponseSID.TesterPresent,
            bytearray([0x7E, 0xA3])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert TESTER_PRESENT.encode(data_records_values=data_records_values,
                                      sid=sid,
                                      rsid=rsid) == payload

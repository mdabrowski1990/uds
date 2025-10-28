import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.security_access import SECURITY_ACCESS


class TestSecurityAccess:
    """Unit tests for `SecurityAccess` service."""

    def test_request_sid(self):
        assert SECURITY_ACCESS.request_sid == RequestSID.SecurityAccess

    def test_response_sid(self):
        assert SECURITY_ACCESS.response_sid == ResponseSID.SecurityAccess


@pytest.mark.integration
class TestSecurityAccessIntegration:
    """Integration tests for `SecurityAccess` service."""

    @pytest.mark.parametrize("payload, decoded_message", [
        (
            [0x27, 0x01],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'SecurityAccess',
                    'raw_value': 0x27,
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
                            'name': 'securityAccessType',
                            'physical_value': 'Request Seed - level 1 (vehicle manufacturer specific)',
                            'raw_value': 0x01,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': None
                },
            )
        ),
        (
            [0x27, 0xDF, 0xFB, 0x85, 0xA1],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'SecurityAccess',
                    'raw_value': 0x27,
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
                            'name': 'securityAccessType',
                            'physical_value': 'Request Seed - level 95, end of life (ISO 26021-2)',
                            'raw_value': 0x5F,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0xDF,
                    'raw_value': 0xDF,
                    'unit': None
                },
                {
                    'children': ((), (), ()),
                    'length': 8,
                    'name': 'securityAccessData',
                    'physical_value': (0xFB, 0x85, 0xA1),
                    'raw_value': (0xFB, 0x85, 0xA1),
                    'unit': None
                },
            )
        ),
        (
            [0x27, 0x82, 0xAE, 0xDB, 0xD6, 0x6F, 0x19, 0x3F, 0xAB, 0xBC, 0x54],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'SecurityAccess',
                    'raw_value': 0x27,
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
                            'name': 'securityAccessType',
                            'physical_value': 'Send Key - level 1 (vehicle manufacturer specific)',
                            'raw_value': 0x02,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x82,
                    'raw_value': 0x82,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'securityKey',
                    'physical_value': (0xAE, 0xDB, 0xD6, 0x6F, 0x19, 0x3F, 0xAB, 0xBC, 0x54),
                    'raw_value': (0xAE, 0xDB, 0xD6, 0x6F, 0x19, 0x3F, 0xAB, 0xBC, 0x54),
                    'unit': None
                },
            )
        ),
        (
            [0x67, 0x19, 0x2D],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'SecurityAccess',
                    'raw_value': 0x67,
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
                            'name': 'securityAccessType',
                            'physical_value': 'Request Seed - level 25 (vehicle manufacturer specific)',
                            'raw_value': 0x19,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x19,
                    'raw_value': 0x19,
                    'unit': None
                },
                {
                    'children': ((),),
                    'length': 8,
                    'name': 'securitySeed',
                    'physical_value': (0x2D, ),
                    'raw_value': (0x2D, ),
                    'unit': None
                },
            )
        ),
        (
            [0x67, 0x82],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'SecurityAccess',
                    'raw_value': 0x67,
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
                            'name': 'securityAccessType',
                            'physical_value': 'Send Key - level 1 (vehicle manufacturer specific)',
                            'raw_value': 0x02,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x82,
                    'raw_value': 0x82,
                    'unit': None
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert SECURITY_ACCESS.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": True,
                    "securityAccessType": 0x03
                },
            },
            RequestSID.SecurityAccess,
            None,
            bytearray([0x27, 0x83])
        ),
        (
            {
                "SubFunction": 0x41,
                "securityAccessData": (0x90, 0x50, 0x68, 0xDE, 0x6B, 0xA1, 0x47),
            },
            RequestSID.SecurityAccess,
            None,
            bytearray([0x27, 0x41, 0x90, 0x50, 0x68, 0xDE, 0x6B, 0xA1, 0x47])
        ),
        (
            {
                "SubFunction": 0x7E,
                "securityKey": (0xA8, 0xEF),
            },
            RequestSID.SecurityAccess,
            None,
            bytearray([0x27, 0x7E, 0xA8, 0xEF])
        ),
        (
            {
                "SubFunction": 0xF1,
                "securitySeed": (0x01, 0x7D),
            },
            None,
            ResponseSID.SecurityAccess,
            bytearray([0x67, 0xF1, 0x01, 0x7D])
        ),
        (
            {
                "SubFunction": 0x60,
            },
            None,
            ResponseSID.SecurityAccess,
            bytearray([0x67, 0x60])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert SECURITY_ACCESS.encode(data_records_values=data_records_values,
                                      sid=sid,
                                      rsid=rsid) == payload

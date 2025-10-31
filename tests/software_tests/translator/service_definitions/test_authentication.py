import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.authentication import AUTHENTICATION


class TestAuthentication:
    """Unit tests for `Authentication` service."""

    def test_request_sid(self):
        assert AUTHENTICATION.request_sid == RequestSID.Authentication

    def test_response_sid(self):
        assert AUTHENTICATION.response_sid == ResponseSID.Authentication


@pytest.mark.integration
class TestAuthenticationIntegration:
    """Integration tests for `Authentication` service."""

    @pytest.mark.parametrize("payload, decoded_message", [
        # deAuthenticate
        (
            [0x29, 0x00],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'Authentication',
                    'raw_value': 0x29,
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
                            'name': 'authenticationTask',
                            'physical_value': 'deAuthenticate',
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
            [0x69, 0x80, 0x10],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'Authentication',
                    'raw_value': 0x69,
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
                            'name': 'authenticationTask',
                            'physical_value': 'deAuthenticate',
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
                {
                    'children': (),
                    'length': 8,
                    'name': 'authenticationReturnParameter',
                    'physical_value': "DeAuthentication successful",
                    'raw_value': 0x10,
                    'unit': None
                },
            )
        ),
        # verifyCertificateUnidirectional
        (
            [0x29, 0x81, 0x5A,
             0x00, 0x01, 0xD8,
             0x00, 0x00],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'Authentication',
                    'raw_value': 0x29,
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
                            'name': 'authenticationTask',
                            'physical_value': 'verifyCertificateUnidirectional',
                            'raw_value': 0x01,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x81,
                    'raw_value': 0x81,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'communicationConfiguration',
                    'physical_value': 0x5A,
                    'raw_value': 0x5A,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfCertificateClient',
                    'physical_value': 0x0001,
                    'raw_value': 0x0001,
                    'unit': 'bytes'
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'certificateClient',
                    'physical_value': 0xD8,
                    'raw_value': 0xD8,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfChallengeClient',
                    'physical_value': 0x0000,
                    'raw_value': 0x0000,
                    'unit': 'bytes'
                },
            )
        ),
        (
            [0x29, 0x01, 0xA5,
             0x00, 0x06, 0x99, 0xD3, 0x75, 0x38, 0x60, 0x17,
             0x00, 0x03, 0xB7, 0x3E, 0x39],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'Authentication',
                    'raw_value': 0x29,
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
                            'name': 'authenticationTask',
                            'physical_value': 'verifyCertificateUnidirectional',
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
                {
                    'children': (),
                    'length': 8,
                    'name': 'communicationConfiguration',
                    'physical_value': 0xA5,
                    'raw_value': 0xA5,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfCertificateClient',
                    'physical_value': 0x0006,
                    'raw_value': 0x0006,
                    'unit': 'bytes'
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'certificateClient',
                    'physical_value': 0x99D375386017,
                    'raw_value': 0x99D375386017,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfChallengeClient',
                    'physical_value': 0x0000,
                    'raw_value': 0x0000,
                    'unit': 'bytes'
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'challengeClient',
                    'physical_value': 0xB73E39,
                    'raw_value': 0xB73E39,
                    'unit': None
                },
            )
        ),
        (
            [0x69, 0x01, 0x00,
             0x00, 0x04, 0x86, 0xCC, 0x26, 0x75,
             0x00, 0x00],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'Authentication',
                    'raw_value': 0x69,
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
                            'name': 'authenticationTask',
                            'physical_value': 'verifyCertificateUnidirectional',
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
                {
                    'children': (),
                    'length': 8,
                    'name': 'authenticationReturnParameter',
                    'physical_value': "RequestAccepted",
                    'raw_value': 0x00,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfChallengeServer',
                    'physical_value': 0x0004,
                    'raw_value': 0x0004,
                    'unit': 'bytes',
                },
                {
                    'children': (),
                    'length': 32,
                    'name': 'challengeServer',
                    'physical_value': 0x86CC2675,
                    'raw_value': 0x86CC2675,
                    'unit': None,
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfEphemeralPublicKeyServer',
                    'physical_value': 0x0000,
                    'raw_value': 0x0000,
                    'unit': 'bytes',
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert AUTHENTICATION.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": True,
                    "diagnosticSessionType": 0x02
                }
            },
            RequestSID.Authentication,
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
            ResponseSID.Authentication,
            bytearray([0x50, 0x04, 0xA1, 0xB2, 0xC3, 0xD4])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert AUTHENTICATION.encode(data_records_values=data_records_values,
                                                 sid=sid,
                                                 rsid=rsid) == payload

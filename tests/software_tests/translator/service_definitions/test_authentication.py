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
        # deAuthenticate (0x00)
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
        # verifyCertificateUnidirectional (0x01)
        (
            [0x29, 0x81, 0x5A, 0x00, 0x01, 0xD8, 0x00, 0x00],
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
            [0x29, 0x01, 0xA5, 0x00, 0x06, 0x99, 0xD3, 0x75, 0x38, 0x60, 0x17, 0x00, 0x03, 0xB7, 0x3E, 0x39],
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
                    'children': ((), (), (), (), (), ()),
                    'length': 8,
                    'name': 'certificateClient',
                    'physical_value': (0x99, 0xD3, 0x75, 0x38, 0x60, 0x17),
                    'raw_value': (0x99, 0xD3, 0x75, 0x38, 0x60, 0x17),
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfChallengeClient',
                    'physical_value': 0x0003,
                    'raw_value': 0x0003,
                    'unit': 'bytes'
                },
                {
                    'children': ((), (), ()),
                    'length': 8,
                    'name': 'challengeClient',
                    'physical_value': (0xB7, 0x3E, 0x39),
                    'raw_value': (0xB7, 0x3E, 0x39),
                    'unit': None
                },
            )
        ),
        (
            [0x69, 0x81, 0x01, 0x00, 0x02, 0x27, 0xB6, 0x00, 0x04, 0x53, 0xC6, 0xA1, 0x84],
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
                    'name': 'authenticationReturnParameter',
                    'physical_value': "GeneralReject",
                    'raw_value': 0x01,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfChallengeServer',
                    'physical_value': 0x0002,
                    'raw_value': 0x0002,
                    'unit': 'bytes',
                },
                {
                    'children': ((), ()),
                    'length': 8,
                    'name': 'challengeServer',
                    'physical_value': (0x27, 0xB6),
                    'raw_value': (0x27, 0xB6),
                    'unit': None,
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfEphemeralPublicKeyServer',
                    'physical_value': 0x0004,
                    'raw_value': 0x0004,
                    'unit': 'bytes',
                },
                {
                    'children': ((), (), (), ()),
                    'length': 8,
                    'name': 'ephemeralPublicKeyServer',
                    'physical_value': (0x53, 0xC6, 0xA1, 0x84),
                    'raw_value': (0x53, 0xC6, 0xA1, 0x84),
                    'unit': None,
                },
            )
        ),
        (
            [0x69, 0x01, 0x00, 0x00, 0x04, 0x86, 0xCC, 0x26, 0x75, 0x00, 0x00],
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
                    'children': ((), (), (), ()),
                    'length': 8,
                    'name': 'challengeServer',
                    'physical_value': (0x86, 0xCC, 0x26, 0x75),
                    'raw_value': (0x86, 0xCC, 0x26, 0x75),
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
        # verifyCertificateBidirectional (0x02)
        (
            [0x29, 0x82, 0x50, 0x00, 0x02, 0xC4, 0xA7, 0x00, 0x04, 0x0C, 0xF6, 0xE9, 0x51],
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
                            'physical_value': 'verifyCertificateBidirectional',
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
                    'children': (),
                    'length': 8,
                    'name': 'communicationConfiguration',
                    'physical_value': 0x50,
                    'raw_value': 0x50,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfCertificateClient',
                    'physical_value': 0x0002,
                    'raw_value': 0x0002,
                    'unit': 'bytes'
                },
                {
                    'children': ((), ()),
                    'length': 8,
                    'name': 'certificateClient',
                    'physical_value': (0xC4, 0xA7),
                    'raw_value': (0xC4, 0xA7),
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfChallengeClient',
                    'physical_value': 0x0004,
                    'raw_value': 0x0004,
                    'unit': 'bytes'
                },
                {
                    'children': ((), (), (), ()),
                    'length': 8,
                    'name': 'challengeClient',
                    'physical_value': (0x0C, 0xF6, 0xE9, 0x51),
                    'raw_value': (0x0C, 0xF6, 0xE9, 0x51),
                    'unit': None
                },
            )
        ),
        (
            [0x69, 0x02, 0x13, 0x00, 0x01, 0xA9, 0x00, 0x05, 0x7D, 0x20, 0x9B, 0x76, 0x56, 0x00, 0x01, 0x5B, 0x00, 0x00],
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
                            'physical_value': 'verifyCertificateBidirectional',
                            'raw_value': 0x02,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x02,
                    'raw_value': 0x02,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'authenticationReturnParameter',
                    'physical_value': "CertificateVerified",
                    'raw_value': 0x13,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfChallengeServer',
                    'physical_value': 0x0001,
                    'raw_value': 0x0001,
                    'unit': 'bytes',
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'challengeServer',
                    'physical_value': 0xA9,
                    'raw_value': 0xA9,
                    'unit': None,
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfCertificateServer',
                    'physical_value': 0x0005,
                    'raw_value': 0x0005,
                    'unit': 'bytes',
                },
                {
                    'children': ((), (), (), (), ()),
                    'length': 8,
                    'name': 'certificateServer',
                    'physical_value': (0x7D, 0x20, 0x9B, 0x76, 0x56),
                    'raw_value': (0x7D, 0x20, 0x9B, 0x76, 0x56),
                    'unit': None,
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfProofOfOwnershipServer',
                    'physical_value': 0x0001,
                    'raw_value': 0x0001,
                    'unit': 'bytes',
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'proofOfOwnershipServer',
                    'physical_value': 0x5B,
                    'raw_value': 0x5B,
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
        # proofOfOwnership (0x03)
        (
            [0x29, 0x83, 0x00, 0x03, 0xDF, 0xE6, 0x90, 0x00, 0x0A, 0xB4, 0xB2, 0xD1, 0x0F, 0x8A, 0x22, 0xE1, 0x4E, 0x30, 0x90],
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
                            'physical_value': 'proofOfOwnership',
                            'raw_value': 0x03,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x83,
                    'raw_value': 0x83,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfProofOfOwnershipClient',
                    'physical_value': 0x0003,
                    'raw_value': 0x0003,
                    'unit': 'bytes'
                },
                {
                    'children': ((), (), ()),
                    'length': 8,
                    'name': 'proofOfOwnershipClient',
                    'physical_value': (0xDF, 0xE6, 0x90),
                    'raw_value': (0xDF, 0xE6, 0x90),
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfEphemeralPublicKeyClient',
                    'physical_value': 0x000A,
                    'raw_value': 0x000A,
                    'unit': 'bytes'
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'ephemeralPublicKeyClient',
                    'physical_value': (0xB4, 0xB2, 0xD1, 0x0F, 0x8A, 0x22, 0xE1, 0x4E, 0x30, 0x90),
                    'raw_value': (0xB4, 0xB2, 0xD1, 0x0F, 0x8A, 0x22, 0xE1, 0x4E, 0x30, 0x90),
                    'unit': None
                },
            )
        ),
        (
            [0x69, 0x03, 0x78, 0x00, 0x00],
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
                            'physical_value': 'proofOfOwnership',
                            'raw_value': 0x03,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x03,
                    'raw_value': 0x03,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'authenticationReturnParameter',
                    'physical_value': 0x78,
                    'raw_value': 0x78,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfSessionKeyInfo',
                    'physical_value': 0x0000,
                    'raw_value': 0x0000,
                    'unit': 'bytes',
                },
            )
        ),
        (
            [0x69, 0x83, 0x12, 0x00, 0x07, 0xA4, 0x54, 0x69, 0xDE, 0x0E, 0x24, 0xDE],
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
                            'physical_value': 'proofOfOwnership',
                            'raw_value': 0x03,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x83,
                    'raw_value': 0x83,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'authenticationReturnParameter',
                    'physical_value': 'OwnershipVerified, AuthenticationComplete',
                    'raw_value': 0x12,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfSessionKeyInfo',
                    'physical_value': 0x0007,
                    'raw_value': 0x0007,
                    'unit': 'bytes',
                },
                {
                    'children': ((), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'sessionKeyInfo',
                    'physical_value': (0xA4, 0x54, 0x69, 0xDE, 0x0E, 0x24, 0xDE),
                    'raw_value': (0xA4, 0x54, 0x69, 0xDE, 0x0E, 0x24, 0xDE),
                    'unit': None
                },
            )
        ),
        # transmitCertificate (0x04)
        (
            [0x29, 0x04, 0xAB, 0x00, 0x10, 0xCC, 0x4B, 0xFF, 0x64, 0x7D, 0x06, 0x50, 0xE5, 0x12, 0xDF, 0x57, 0x9F, 0x16, 0x7E, 0xFE, 0x33],
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
                            'physical_value': 'transmitCertificate',
                            'raw_value': 0x04,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x04,
                    'raw_value': 0x04,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'certificateEvaluationId',
                    'physical_value': 0xAB,
                    'raw_value': 0xAB,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfCertificateData',
                    'physical_value': 0x0010,
                    'raw_value': 0x0010,
                    'unit': 'bytes'
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'certificateData',
                    'physical_value': (0xCC, 0x4B, 0xFF, 0x64, 0x7D, 0x06, 0x50, 0xE5, 0x12, 0xDF, 0x57, 0x9F, 0x16, 0x7E, 0xFE, 0x33),
                    'raw_value': (0xCC, 0x4B, 0xFF, 0x64, 0x7D, 0x06, 0x50, 0xE5, 0x12, 0xDF, 0x57, 0x9F, 0x16, 0x7E, 0xFE, 0x33),
                    'unit': None
                },
            )
        ),
        (
            [0x69, 0x04, 0x13],
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
                            'physical_value': 'transmitCertificate',
                            'raw_value': 0x04,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x04,
                    'raw_value': 0x04,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'authenticationReturnParameter',
                    'physical_value': 'CertificateVerified',
                    'raw_value': 0x13,
                    'unit': None
                },
            )
        ),
        # requestChallengeForAuthentication (0x05)
        (
            [0x29, 0x85, 0x9C, 0x49, 0xB8, 0xA7, 0x0A, 0x6B, 0xB2, 0x39, 0x81, 0x23, 0x9E, 0xAD, 0x18, 0x36, 0x04, 0x58, 0xE2],
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
                            'physical_value': 'requestChallengeForAuthentication',
                            'raw_value': 0x05,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x85,
                    'raw_value': 0x85,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'communicationConfiguration',
                    'physical_value': 0x9C,
                    'raw_value': 0x9C,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'algorithmIndicator',
                    'physical_value': (0x49, 0xB8, 0xA7, 0x0A, 0x6B, 0xB2, 0x39, 0x81, 0x23, 0x9E, 0xAD, 0x18, 0x36, 0x04, 0x58, 0xE2),
                    'raw_value': (0x49, 0xB8, 0xA7, 0x0A, 0x6B, 0xB2, 0x39, 0x81, 0x23, 0x9E, 0xAD, 0x18, 0x36, 0x04, 0x58, 0xE2),
                    'unit': None
                },
            )
        ),
        (
            [0x69, 0x05, 0x0B, 0x17, 0xC0, 0x27, 0xAE, 0x24, 0x8D, 0x5D, 0x58, 0xED, 0x8E, 0x95, 0x00, 0x37, 0x53, 0x92, 0x19, 0x00, 0x02, 0x81, 0x3A, 0x00, 0x00],
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
                            'physical_value': 'requestChallengeForAuthentication',
                            'raw_value': 0x05,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x05,
                    'raw_value': 0x05,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'authenticationReturnParameter',
                    'physical_value': 0x0B,
                    'raw_value': 0x0B,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'algorithmIndicator',
                    'physical_value': (0x17, 0xC0, 0x27, 0xAE, 0x24, 0x8D, 0x5D, 0x58, 0xED, 0x8E, 0x95, 0x00, 0x37, 0x53, 0x92, 0x19),
                    'raw_value': (0x17, 0xC0, 0x27, 0xAE, 0x24, 0x8D, 0x5D, 0x58, 0xED, 0x8E, 0x95, 0x00, 0x37, 0x53, 0x92, 0x19),
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfChallengeServer',
                    'physical_value': 0x0002,
                    'raw_value': 0x0002,
                    'unit': 'bytes'
                },
                {
                    'children': ((), ()),
                    'length': 8,
                    'name': 'challengeServer',
                    'physical_value': (0x81, 0x3A),
                    'raw_value': (0x81, 0x3A),
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfNeededAdditionalParameter',
                    'physical_value': 0x0000,
                    'raw_value': 0x0000,
                    'unit': 'bytes'
                },
            )
        ),
        (
            [0x69, 0x85, 0x04, 0x6E, 0xCE, 0x27, 0x2C, 0xA7, 0xDB, 0x2E, 0x08, 0x43, 0x38, 0xDB, 0x9C, 0x69, 0x24, 0x00, 0x00, 0x00, 0x03, 0x3B, 0x27, 0x3B, 0x00, 0x05, 0xE2, 0x05, 0x56, 0x3D, 0x94],
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
                            'physical_value': 'requestChallengeForAuthentication',
                            'raw_value': 0x05,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x85,
                    'raw_value': 0x85,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'authenticationReturnParameter',
                    'physical_value': 'AuthenticationConfiguration ACR with symmetric cryptography',
                    'raw_value': 0x04,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'algorithmIndicator',
                    'physical_value': (0x6E, 0xCE, 0x27, 0x2C, 0xA7, 0xDB, 0x2E, 0x08, 0x43, 0x38, 0xDB, 0x9C, 0x69, 0x24, 0x00, 0x00),
                    'raw_value': (0x6E, 0xCE, 0x27, 0x2C, 0xA7, 0xDB, 0x2E, 0x08, 0x43, 0x38, 0xDB, 0x9C, 0x69, 0x24, 0x00, 0x00),
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfChallengeServer',
                    'physical_value': 0x0003,
                    'raw_value': 0x0003,
                    'unit': 'bytes'
                },
                {
                    'children': ((), (), ()),
                    'length': 8,
                    'name': 'challengeServer',
                    'physical_value': (0x3B, 0x27, 0x3B),
                    'raw_value': (0x3B, 0x27, 0x3B),
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfNeededAdditionalParameter',
                    'physical_value': 0x0005,
                    'raw_value': 0x0005,
                    'unit': 'bytes'
                },
                {
                    'children': ((), (), (), (), ()),
                    'length': 8,
                    'name': 'neededAdditionalParameter',
                    'physical_value': (0xE2, 0x05, 0x56, 0x3D, 0x94),
                    'raw_value': (0xE2, 0x05, 0x56, 0x3D, 0x94),
                    'unit': None
                },
            )
        ),
        # verifyProofOfOwnershipUnidirectional (0x06)
        (
            [0x29, 0x06, 0xCB, 0x15, 0x34, 0xE5, 0x53, 0x0B, 0x23, 0x04, 0x30, 0xAE, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
             0x00, 0x0A, 0x15, 0x88, 0xA2, 0xDA, 0x01, 0x98, 0xC0, 0xFC, 0x21, 0x12,
             0x00, 0x00, 0x00, 0x00],
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
                            'physical_value': 'verifyProofOfOwnershipUnidirectional',
                            'raw_value': 0x06,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x06,
                    'raw_value': 0x06,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'algorithmIndicator',
                    'physical_value': (0xCB, 0x15, 0x34, 0xE5, 0x53, 0x0B, 0x23, 0x04, 0x30, 0xAE, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
                    'raw_value': (0xCB, 0x15, 0x34, 0xE5, 0x53, 0x0B, 0x23, 0x04, 0x30, 0xAE, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfProofOfOwnershipClient',
                    'physical_value': 0x000A,
                    'raw_value': 0x000A,
                    'unit': 'bytes'
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'proofOfOwnershipClient',
                    'physical_value': (0x15, 0x88, 0xA2, 0xDA, 0x01, 0x98, 0xC0, 0xFC, 0x21, 0x12),
                    'raw_value': (0x15, 0x88, 0xA2, 0xDA, 0x01, 0x98, 0xC0, 0xFC, 0x21, 0x12),
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
                    'length': 16,
                    'name': 'lengthOfAdditionalParameter',
                    'physical_value': 0x0000,
                    'raw_value': 0x0000,
                    'unit': 'bytes'
                },
            )
        ),
        (
            [0x29, 0x86, 0x3B, 0x39, 0x2F, 0x7A, 0x97, 0x2D, 0xFB, 0x1D, 0xD7, 0xCB, 0xAB, 0x32, 0xE1, 0x61, 0xA8, 0xD6,
             0x00, 0x03, 0x9C, 0xB2, 0xB1,
             0x00, 0x04, 0xF0, 0x11, 0x08, 0x4F,
             0x00, 0x04, 0xB3, 0x17, 0x14, 0x8D],
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
                            'physical_value': 'verifyProofOfOwnershipUnidirectional',
                            'raw_value': 0x06,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x86,
                    'raw_value': 0x86,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'algorithmIndicator',
                    'physical_value': (0x3B, 0x39, 0x2F, 0x7A, 0x97, 0x2D, 0xFB, 0x1D, 0xD7, 0xCB, 0xAB, 0x32, 0xE1, 0x61, 0xA8, 0xD6),
                    'raw_value': (0x3B, 0x39, 0x2F, 0x7A, 0x97, 0x2D, 0xFB, 0x1D, 0xD7, 0xCB, 0xAB, 0x32, 0xE1, 0x61, 0xA8, 0xD6),
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfProofOfOwnershipClient',
                    'physical_value': 0x0003,
                    'raw_value': 0x0003,
                    'unit': 'bytes'
                },
                {
                    'children': ((), (), ()),
                    'length': 8,
                    'name': 'proofOfOwnershipClient',
                    'physical_value': (0x9C, 0xB2, 0xB1),
                    'raw_value': (0x9C, 0xB2, 0xB1),
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfChallengeClient',
                    'physical_value': 0x0004,
                    'raw_value': 0x0004,
                    'unit': 'bytes'
                },
                {
                    'children': ((), (), (), ()),
                    'length': 8,
                    'name': 'challengeClient',
                    'physical_value': (0xF0, 0x11, 0x08, 0x4F),
                    'raw_value': (0xF0, 0x11, 0x08, 0x4F),
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfAdditionalParameter',
                    'physical_value': 0x0004,
                    'raw_value': 0x0004,
                    'unit': 'bytes'
                },
                {
                    'children': ((), (), (), ()),
                    'length': 8,
                    'name': 'additionalParameter',
                    'physical_value': (0xB3, 0x17, 0x14, 0x8D),
                    'raw_value': (0xB3, 0x17, 0x14, 0x8D),
                    'unit': None
                },
            )
        ),
        (
            [0x69, 0x06, 0xCB, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
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
                            'physical_value': 'verifyProofOfOwnershipUnidirectional',
                            'raw_value': 0x06,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x06,
                    'raw_value': 0x06,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'authenticationReturnParameter',
                    'physical_value': 0xCB,
                    'raw_value': 0xCB,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'algorithmIndicator',
                    'physical_value': (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
                    'raw_value': (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfSessionKeyInfo',
                    'physical_value': 0x0000,
                    'raw_value': 0x0000,
                    'unit': 'bytes'
                },
            )
        ),
        (
            [0x69, 0x86, 0x00, 0x07, 0x39, 0x0A, 0xAE, 0xAC, 0x1F, 0xA0, 0x1F, 0xE1, 0xED, 0x6C, 0xB1, 0xA9, 0x91, 0x4A, 0xC3,
             0x00, 0x06, 0xD6, 0x31, 0xDB, 0x8E, 0x7F, 0x61],
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
                            'physical_value': 'verifyProofOfOwnershipUnidirectional',
                            'raw_value': 0x06,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x86,
                    'raw_value': 0x86,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'authenticationReturnParameter',
                    'physical_value': 'RequestAccepted',
                    'raw_value': 0x00,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'algorithmIndicator',
                    'physical_value': (0x07, 0x39, 0x0A, 0xAE, 0xAC, 0x1F, 0xA0, 0x1F, 0xE1, 0xED, 0x6C, 0xB1, 0xA9, 0x91, 0x4A, 0xC3),
                    'raw_value': (0x07, 0x39, 0x0A, 0xAE, 0xAC, 0x1F, 0xA0, 0x1F, 0xE1, 0xED, 0x6C, 0xB1, 0xA9, 0x91, 0x4A, 0xC3),
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfSessionKeyInfo',
                    'physical_value': 0x0006,
                    'raw_value': 0x0006,
                    'unit': 'bytes'
                },
                {
                    'children': ((), (), (), (), (), ()),
                    'length': 8,
                    'name': 'sessionKeyInfo',
                    'physical_value': (0xD6, 0x31, 0xDB, 0x8E, 0x7F, 0x61),
                    'raw_value': (0xD6, 0x31, 0xDB, 0x8E, 0x7F, 0x61),
                    'unit': None
                },
            )
        ),
        # verifyProofOfOwnershipBidirectional (0x07)
        (
            [0x29, 0x87, 0x11, 0x22, 0x66, 0x62, 0x13, 0x1A, 0x36, 0x64, 0x18, 0xD4, 0x72, 0x22, 0x09, 0x35, 0xB0, 0x5A,
             0x00, 0x02, 0x2A, 0xE3,
             0x00, 0x04, 0x6F, 0xD5, 0xAC, 0x05,
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
                            'physical_value': 'verifyProofOfOwnershipBidirectional',
                            'raw_value': 0x07,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x87,
                    'raw_value': 0x87,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'algorithmIndicator',
                    'physical_value': (0x11, 0x22, 0x66, 0x62, 0x13, 0x1A, 0x36, 0x64, 0x18, 0xD4, 0x72, 0x22, 0x09, 0x35, 0xB0, 0x5A),
                    'raw_value': (0x11, 0x22, 0x66, 0x62, 0x13, 0x1A, 0x36, 0x64, 0x18, 0xD4, 0x72, 0x22, 0x09, 0x35, 0xB0, 0x5A),
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfProofOfOwnershipClient',
                    'physical_value': 0x0002,
                    'raw_value': 0x0002,
                    'unit': 'bytes'
                },
                {
                    'children': ((), ()),
                    'length': 8,
                    'name': 'proofOfOwnershipClient',
                    'physical_value': (0x2A, 0xE3),
                    'raw_value': (0x2A, 0xE3),
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfChallengeClient',
                    'physical_value': 0x0004,
                    'raw_value': 0x0004,
                    'unit': 'bytes'
                },
                {
                    'children': ((), (), (), ()),
                    'length': 8,
                    'name': 'challengeClient',
                    'physical_value': (0x6F, 0xD5, 0xAC, 0x05),
                    'raw_value': (0x6F, 0xD5, 0xAC, 0x05),
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfAdditionalParameter',
                    'physical_value': 0x0000,
                    'raw_value': 0x0000,
                    'unit': 'bytes'
                },
            )
        ),
        (
            [0x29, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
             0x00, 0x01, 0x48,
             0x00, 0x01, 0x05,
             0x00, 0x07, 0xED, 0x27, 0x9D, 0x1B, 0xD4, 0x19, 0x3E],
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
                            'physical_value': 'verifyProofOfOwnershipBidirectional',
                            'raw_value': 0x07,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x07,
                    'raw_value': 0x07,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'algorithmIndicator',
                    'physical_value': (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
                    'raw_value': (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfProofOfOwnershipClient',
                    'physical_value': 0x0001,
                    'raw_value': 0x0001,
                    'unit': 'bytes'
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'proofOfOwnershipClient',
                    'physical_value': 0x48,
                    'raw_value': 0x48,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfChallengeClient',
                    'physical_value': 0x0001,
                    'raw_value': 0x0001,
                    'unit': 'bytes'
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'challengeClient',
                    'physical_value': 0x05,
                    'raw_value': 0x05,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfAdditionalParameter',
                    'physical_value': 0x0007,
                    'raw_value': 0x0007,
                    'unit': 'bytes'
                },
                {
                    'children': ((), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'additionalParameter',
                    'physical_value': (0xED, 0x27, 0x9D, 0x1B, 0xD4, 0x19, 0x3E),
                    'raw_value': (0xED, 0x27, 0x9D, 0x1B, 0xD4, 0x19, 0x3E),
                    'unit': None
                },
            )
        ),
        (
            [0x69, 0x07, 0x03, 0xB9, 0x72, 0xB1, 0x58, 0x7C, 0xCD, 0xE0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
             0x00, 0x02, 0x68, 0x20,
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
                            'physical_value': 'verifyProofOfOwnershipBidirectional',
                            'raw_value': 0x07,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x07,
                    'raw_value': 0x07,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'authenticationReturnParameter',
                    'physical_value': 'AuthenticationConfiguration ACR with asymmetric cryptography',
                    'raw_value': 0x03,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'algorithmIndicator',
                    'physical_value': (0xB9, 0x72, 0xB1, 0x58, 0x7C, 0xCD, 0xE0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
                    'raw_value': (0xB9, 0x72, 0xB1, 0x58, 0x7C, 0xCD, 0xE0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfProofOfOwnershipServer',
                    'physical_value': 0x0002,
                    'raw_value': 0x0002,
                    'unit': 'bytes'
                },
                {
                    'children': ((), ()),
                    'length': 8,
                    'name': 'proofOfOwnershipServer',
                    'physical_value': (0x68, 0x20),
                    'raw_value': (0x68, 0x20),
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfSessionKeyInfo',
                    'physical_value': 0x0000,
                    'raw_value': 0x0000,
                    'unit': 'bytes'
                },
            )
        ),
        (
            [0x69, 0x87, 0xC9, 0xA3, 0x43, 0x19, 0x95, 0xA7, 0xD3, 0xA7, 0xA9, 0xB1, 0xE1, 0x91, 0x64, 0x8C, 0x67, 0x62, 0xDF,
             0x00, 0x01, 0x7A,
             0x00, 0x09, 0x5A, 0xD8, 0x7F, 0x44, 0x48, 0x74, 0x59, 0x19, 0xD6],
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
                            'physical_value': 'verifyProofOfOwnershipBidirectional',
                            'raw_value': 0x07,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x87,
                    'raw_value': 0x87,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'authenticationReturnParameter',
                    'physical_value': 0xC9,
                    'raw_value': 0xC9,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'algorithmIndicator',
                    'physical_value': (0xA3, 0x43, 0x19, 0x95, 0xA7, 0xD3, 0xA7, 0xA9, 0xB1, 0xE1, 0x91, 0x64, 0x8C, 0x67, 0x62, 0xDF),
                    'raw_value': (0xA3, 0x43, 0x19, 0x95, 0xA7, 0xD3, 0xA7, 0xA9, 0xB1, 0xE1, 0x91, 0x64, 0x8C, 0x67, 0x62, 0xDF),
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfProofOfOwnershipServer',
                    'physical_value': 0x0001,
                    'raw_value': 0x0001,
                    'unit': 'bytes'
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'proofOfOwnershipServer',
                    'physical_value': 0x7A,
                    'raw_value': 0x7A,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'lengthOfSessionKeyInfo',
                    'physical_value': 0x0009,
                    'raw_value': 0x0009,
                    'unit': 'bytes'
                },
                {
                    'children': ((), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'sessionKeyInfo',
                    'physical_value': (0x5A, 0xD8, 0x7F, 0x44, 0x48, 0x74, 0x59, 0x19, 0xD6),
                    'raw_value': (0x5A, 0xD8, 0x7F, 0x44, 0x48, 0x74, 0x59, 0x19, 0xD6),
                    'unit': None
                },
            )
        ),
        # authenticationConfiguration (0x08)
        (
            [0x29, 0x88],
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
                            'physical_value': 'authenticationConfiguration',
                            'raw_value': 0x08,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x88,
                    'raw_value': 0x88,
                    'unit': None
                },
            )
        ),
        (
            [0x69, 0x08, 0x11],
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
                            'physical_value': 'authenticationConfiguration',
                            'raw_value': 0x08,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x08,
                    'raw_value': 0x08,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'authenticationReturnParameter',
                    'physical_value': 'CertificateVerified, OwnershipVerificationNecessary',
                    'raw_value': 0x11,
                    'unit': None
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

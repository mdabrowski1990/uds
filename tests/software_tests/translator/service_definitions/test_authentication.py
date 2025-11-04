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
        # deAuthenticate (0x00)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": True,
                    "authenticationTask": 0x00
                }
            },
            RequestSID.Authentication,
            None,
            bytearray([0x29, 0x80])
        ),
        (
            {
                "SubFunction": 0x00,
                "authenticationReturnParameter": 0xFF
            },
            None,
            ResponseSID.Authentication,
            bytearray([0x69, 0x00, 0xFF])
        ),
        # verifyCertificateUnidirectional (0x01)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": False,
                    "authenticationTask": 0x01
                },
                "communicationConfiguration": 0x04,
                "lengthOfCertificateClient": 0x0100,
                "certificateClient": b'\xc4\xa7\xdf\xf7\xdb\x05\xefr\xe7\xc2Q\xd8\xf1z^\x0e\xa3\xf2\xfdQl\x125NT\x93'
                                     b'\xe0\x97W\x1b\xdc\xbeK\x1a]\x07Z/\xc8\xd8=\x0b\xc8{\xb7\x87\xb3\xba6\x8d7\x03>:'
                                     b'\xf4\xb3nK\xc3\x1a??W\xe0\x1be\x174[\xfaj\xe4\xf0\x9eD\xe9\x07\x07J+\xb0\x0c\xad'
                                     b'\x00\x88\x87k\x17\xfb+J\xfc\x90\xa9\x06G,^\xce\xf1T\xe1\xf6h\xd4\xc2\xd5\xce'
                                     b'\x912\x19\xab;\xed]\xad\x02\xf5z%\x8cz\x93\t\xce\xb8\x89\xfcv\x9cMmw\x9fX\x80'
                                     b'\x8a#&\xce\xff\x14\x93\r\x18w\xc8\xcc\x02Xi\xb2I;\x84.\xbf\xf6w\xa4\xe2\xf8\xe7'
                                     b'y\x9ciV\xf4\xe2\'\xf3R7\xb6\x8b\xd3\xfd\xf9\x8dNh%\xf3?w~\x11\xf5\x18\xd9A*#\rF'
                                     b'\xb6\x01\xae\x8b\x9d\x11Qb\xfb/<o"c\x83\xd4\xb2\x87\n]jz\x03\x97\xc4\\v\x8et'
                                     b'\x97\xcb\xa3\xc2R\xfcT\x1c}\xa5\x1b5\xf3u>\xed\x85\x0e\xd5\x8a\x17\xb8\xa4.\xae '
                                     b'Q\x8a\xcd\x95\xf3d',
                "lengthOfChallengeClient": 0x0001,
                "challengeClient": 0x55,
            },
            RequestSID.Authentication,
            None,
            bytearray([0x29, 0x01, 0x04,
                       0x01, 0x00, 0xC4, 0xA7, 0xDF, 0xF7, 0xDB, 0x05, 0xEF, 0x72, 0xE7, 0xC2, 0x51, 0xD8, 0xF1, 0x7A,
                       0x5E, 0x0E, 0xA3, 0xF2, 0xFD, 0x51, 0x6C, 0x12, 0x35, 0x4E, 0x54, 0x93, 0xE0, 0x97, 0x57, 0x1B,
                       0xDC, 0xBE, 0x4B, 0x1A, 0x5D, 0x07, 0x5A, 0x2F, 0xC8, 0xD8, 0x3D, 0x0B, 0xC8, 0x7B, 0xB7, 0x87,
                       0xB3, 0xBA, 0x36, 0x8D, 0x37, 0x03, 0x3E, 0x3A, 0xF4, 0xB3, 0x6E, 0x4B, 0xC3, 0x1A, 0x3F, 0x3F,
                       0x57, 0xE0, 0x1B, 0x65, 0x17, 0x34, 0x5B, 0xFA, 0x6A, 0xE4, 0xF0, 0x9E, 0x44, 0xE9, 0x07, 0x07,
                       0x4A, 0x2B, 0xB0, 0x0C, 0xAD, 0x00, 0x88, 0x87, 0x6B, 0x17, 0xFB, 0x2B, 0x4A, 0xFC, 0x90, 0xA9,
                       0x06, 0x47, 0x2C, 0x5E, 0xCE, 0xF1, 0x54, 0xE1, 0xF6, 0x68, 0xD4, 0xC2, 0xD5, 0xCE, 0x91, 0x32,
                       0x19, 0xAB, 0x3B, 0xED, 0x5D, 0xAD, 0x02, 0xF5, 0x7A, 0x25, 0x8C, 0x7A, 0x93, 0x09, 0xCE, 0xB8,
                       0x89, 0xFC, 0x76, 0x9C, 0x4D, 0x6D, 0x77, 0x9F, 0x58, 0x80, 0x8A, 0x23, 0x26, 0xCE, 0xFF, 0x14,
                       0x93, 0x0D, 0x18, 0x77, 0xC8, 0xCC, 0x02, 0x58, 0x69, 0xB2, 0x49, 0x3B, 0x84, 0x2E, 0xBF, 0xF6,
                       0x77, 0xA4, 0xE2, 0xF8, 0xE7, 0x79, 0x9C, 0x69, 0x56, 0xF4, 0xE2, 0x27, 0xF3, 0x52, 0x37, 0xB6,
                       0x8B, 0xD3, 0xFD, 0xF9, 0x8D, 0x4E, 0x68, 0x25, 0xF3, 0x3F, 0x77, 0x7E, 0x11, 0xF5, 0x18, 0xD9,
                       0x41, 0x2A, 0x23, 0x0D, 0x46, 0xB6, 0x01, 0xAE, 0x8B, 0x9D, 0x11, 0x51, 0x62, 0xFB, 0x2F, 0x3C,
                       0x6F, 0x22, 0x63, 0x83, 0xD4, 0xB2, 0x87, 0x0A, 0x5D, 0x6A, 0x7A, 0x03, 0x97, 0xC4, 0x5C, 0x76,
                       0x8E, 0x74, 0x97, 0xCB, 0xA3, 0xC2, 0x52, 0xFC, 0x54, 0x1C, 0x7D, 0xA5, 0x1B, 0x35, 0xF3, 0x75,
                       0x3E, 0xED, 0x85, 0x0E, 0xD5, 0x8A, 0x17, 0xB8, 0xA4, 0x2E, 0xAE, 0x20, 0x51, 0x8A, 0xCD, 0x95,
                       0xF3, 0x64,
                       0x00, 0x01, 0x55])
        ),
        (
            {
                "SubFunction": 0x81,
                "authenticationReturnParameter": 0xFF,
                "lengthOfChallengeServer": 0x0011,
                "challengeServer": (0xF3, 0x46, 0x14, 0xEF, 0x40, 0x23, 0xED, 0x50, 0x15, 0x6F, 0xC5, 0xAF, 0xE6, 0x6D,
                                    0xB8, 0xD1, 0x72),
                "lengthOfEphemeralPublicKeyServer": 0x0005,
                "ephemeralPublicKeyServer": (0xB9, 0x35, 0xB7, 0x43, 0x39),
            },
            None,
            ResponseSID.Authentication,
            bytearray([0x69, 0x81, 0xFF,
                       0x00, 0x11, 0xF3, 0x46, 0x14, 0xEF, 0x40, 0x23, 0xED, 0x50, 0x15, 0x6F, 0xC5, 0xAF, 0xE6, 0x6D,
                       0xB8, 0xD1, 0x72,
                       0x00, 0x05, 0xB9, 0x35, 0xB7, 0x43, 0x39])
        ),
        # verifyCertificateBidirectional (0x02)
        (
            {
                "SubFunction": 0x82,
                "communicationConfiguration": 0x3C,
                "lengthOfCertificateClient": 0x0005,
                "certificateClient": (0x38, 0x0A, 0xF0, 0x20, 0x5A),
                "lengthOfChallengeClient": 0x0026,
                "challengeClient": (0x16, 0x04, 0x8E, 0x6D, 0x85, 0x50, 0xD2, 0xD6, 0xFC, 0x1A, 0x0C, 0x07, 0x2B, 0x2D,
                                    0x9A, 0x18, 0x51, 0x9A, 0xC9, 0x69, 0xF1, 0xAA, 0x3A, 0x48, 0x30, 0x19, 0xA7, 0xD3,
                                    0x1D, 0x99, 0x8D, 0x1D, 0x86, 0xA1, 0x39, 0x46, 0x15, 0xF5),
            },
            RequestSID.Authentication,
            None,
            bytearray([0x29, 0x82, 0x3C,
                       0x00, 0x05, 0x38, 0x0A, 0xF0, 0x20, 0x5A,
                       0x00, 0x26, 0x16, 0x04, 0x8E, 0x6D, 0x85, 0x50, 0xD2, 0xD6, 0xFC, 0x1A, 0x0C, 0x07, 0x2B, 0x2D,
                       0x9A, 0x18, 0x51, 0x9A, 0xC9, 0x69, 0xF1, 0xAA, 0x3A, 0x48, 0x30, 0x19, 0xA7, 0xD3, 0x1D, 0x99,
                       0x8D, 0x1D, 0x86, 0xA1, 0x39, 0x46, 0x15, 0xF5])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": False,
                    "authenticationTask": 0x02
                },
                "authenticationReturnParameter": 0xB3,
                "lengthOfChallengeServer": 0x0008,
                "challengeServer": (0x77, 0x02, 0xB7, 0xD4, 0x40, 0xD6, 0x16, 0x49),
                "lengthOfCertificateServer": 0x0008,
                "certificateServer": (0x30, 0x7E, 0x49, 0xA3, 0xE2, 0xE4, 0xF4, 0x12),
                "lengthOfProofOfOwnershipServer": 0x0012,
                "proofOfOwnershipServer": (0x75, 0xEE, 0xB2, 0xCB, 0xE5, 0x39, 0xFC, 0x12, 0xA6, 0xE2, 0x7C, 0xCC, 0xFA,
                                           0x3A, 0xEE, 0x22, 0x22, 0x32),
                "lengthOfEphemeralPublicKeyServer": 0x0000,
            },
            None,
            ResponseSID.Authentication,
            bytearray([0x69, 0x02, 0xB3,
                       0x00, 0x08, 0x77, 0x02, 0xB7, 0xD4, 0x40, 0xD6, 0x16, 0x49,
                       0x00, 0x08, 0x30, 0x7E, 0x49, 0xA3, 0xE2, 0xE4, 0xF4, 0x12,
                       0x00, 0x12, 0x75, 0xEE, 0xB2, 0xCB, 0xE5, 0x39, 0xFC, 0x12, 0xA6, 0xE2, 0x7C, 0xCC, 0xFA, 0x3A,
                       0xEE, 0x22, 0x22, 0x32,
                       0x00, 0x00])
        ),
        # proofOfOwnership (0x03)
        (
            {
                "SubFunction": 0x03,
                "lengthOfProofOfOwnershipClient": 0x000A,
                "proofOfOwnershipClient": (0x3C, 0x03, 0x80, 0x10, 0x5E, 0x3A, 0x42, 0x20, 0x7F, 0x3A),
                "lengthOfEphemeralPublicKeyClient": 0x0008,
                "ephemeralPublicKeyClient": (0x61, 0xB8, 0x2D, 0x0D, 0xA9, 0x15, 0x5E, 0x53),
            },
            RequestSID.Authentication,
            None,
            bytearray([0x29, 0x03,
                       0x00, 0x0A, 0x3C, 0x03, 0x80, 0x10, 0x5E, 0x3A, 0x42, 0x20, 0x7F, 0x3A,
                       0x00, 0x08, 0x61, 0xB8, 0x2D, 0x0D, 0xA9, 0x15, 0x5E, 0x53])
        ),
        (
            {
                "SubFunction": 0x83,
                "authenticationReturnParameter": 0x17,
                "lengthOfSessionKeyInfo": 0x000A,
                "sessionKeyInfo": (0x28, 0x4D, 0x67, 0xE8, 0x81, 0x0E, 0xC6, 0x7F, 0xB6, 0x8C),
            },
            None,
            ResponseSID.Authentication,
            bytearray([0x69, 0x83, 0x17,
                       0x00, 0x0A, 0x28, 0x4D, 0x67, 0xE8, 0x81, 0x0E, 0xC6, 0x7F, 0xB6, 0x8C])
        ),
        # transmitCertificate (0x04)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": True,
                    "authenticationTask": 0x04
                },
                "certificateEvaluationId": 0xBE,
                "lengthOfCertificateData": 0x0023,
                "certificateData": (0x59, 0x23, 0xA6, 0xD8, 0x22, 0x42, 0x65, 0x3E, 0x9A, 0x04, 0xA4, 0x07, 0x64, 0x30,
                                    0x45, 0x9E, 0x7D, 0x48, 0x64, 0x4F, 0x81, 0xD5, 0x21, 0x29, 0xA6, 0x2E, 0x1C, 0x81,
                                    0x4C, 0x18, 0x32, 0xD0, 0x08, 0x77, 0x9C),
            },
            RequestSID.Authentication,
            None,
            bytearray([0x29, 0x84, 0xBE,
                       0x00, 0x23, 0x59, 0x23, 0xA6, 0xD8, 0x22, 0x42, 0x65, 0x3E, 0x9A, 0x04, 0xA4, 0x07, 0x64, 0x30,
                       0x45, 0x9E, 0x7D, 0x48, 0x64, 0x4F, 0x81, 0xD5, 0x21, 0x29, 0xA6, 0x2E, 0x1C, 0x81, 0x4C, 0x18,
                       0x32, 0xD0, 0x08, 0x77, 0x9C])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": False,
                    "authenticationTask": 0x04
                },
                "authenticationReturnParameter": 0x80,
            },
            None,
            ResponseSID.Authentication,
            bytearray([0x69, 0x04, 0x80])
        ),
        # requestChallengeForAuthentication (0x05)
        (
            {
                "SubFunction": 0x05,
                "communicationConfiguration": 0xF2,
                "algorithmIndicator": (0xA0, 0x5C, 0x18, 0x48, 0xEB, 0x30, 0xD3, 0x5A, 0x40, 0x9A, 0xB0, 0xC4, 0x70,
                                       0xBF, 0x68, 0xC0),
            },
            RequestSID.Authentication,
            None,
            bytearray([0x29, 0x05, 0xF2,
                       0xA0, 0x5C, 0x18, 0x48, 0xEB, 0x30, 0xD3, 0x5A, 0x40, 0x9A, 0xB0, 0xC4, 0x70, 0xBF, 0x68, 0xC0])
        ),
        (
            {
                "SubFunction": 0x85,
                "authenticationReturnParameter": 0xFE,
                "algorithmIndicator": (0x02, 0xA2, 0xE2, 0x9E, 0x68, 0xDB, 0x64, 0xE6, 0x6D, 0xC5, 0x7C, 0x47, 0x53,
                                       0x32, 0xBB, 0x3D),
                "lengthOfChallengeServer": 0x0010,
                "challengeServer": (0x8C, 0xF4, 0x0C, 0x41, 0xB6, 0x5F, 0x22, 0xF6, 0xA5, 0xD7, 0x57, 0xB4, 0x35, 0x10,
                                    0x53, 0x00),
                "lengthOfNeededAdditionalParameter": 0x0000,
            },
            None,
            ResponseSID.Authentication,
            bytearray([0x69, 0x85, 0xFE,
                       0x02, 0xA2, 0xE2, 0x9E, 0x68, 0xDB, 0x64, 0xE6, 0x6D, 0xC5, 0x7C, 0x47, 0x53, 0x32, 0xBB, 0x3D,
                       0x00, 0x10, 0x8C, 0xF4, 0x0C, 0x41, 0xB6, 0x5F, 0x22, 0xF6, 0xA5, 0xD7, 0x57, 0xB4, 0x35, 0x10,
                       0x53, 0x00,
                       0x00, 0x00,])
        ),
        # verifyProofOfOwnershipUnidirectional (0x06)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": True,
                    "authenticationTask": 0x06
                },
                "algorithmIndicator": (0x03, 0x8E, 0x4C, 0x87, 0x51, 0x24, 0xCB, 0x49, 0xC7, 0x56, 0x9F, 0x88, 0xCD,
                                       0xA6, 0x1D, 0x30),
                "lengthOfProofOfOwnershipClient": 0x0005,
                "proofOfOwnershipClient": (0x56, 0xEF, 0x7A, 0x95, 0x7D),
                "lengthOfChallengeClient": 0x0008,
                "challengeClient": (0x70, 0x15, 0xDC, 0x29, 0x0B, 0xF3, 0xC5, 0x23),
                "lengthOfAdditionalParameter": 0x0000,
            },
            RequestSID.Authentication,
            None,
            bytearray([0x29, 0x86,
                       0x03, 0x8E, 0x4C, 0x87, 0x51, 0x24, 0xCB, 0x49, 0xC7, 0x56, 0x9F, 0x88, 0xCD, 0xA6, 0x1D, 0x30,
                       0x00, 0x05, 0x56, 0xEF, 0x7A, 0x95, 0x7D,
                       0x00, 0x08, 0x70, 0x15, 0xDC, 0x29, 0x0B, 0xF3, 0xC5, 0x23,
                       0x00, 0x00])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": False,
                    "authenticationTask": 0x06
                },
                "authenticationReturnParameter": 0xA2,
                "algorithmIndicator": (0x87, 0xFA, 0x1D, 0xAB, 0x9C, 0xE6, 0xC6, 0xEE, 0x26, 0xD3, 0x7C, 0x59, 0x68,
                                       0xA8, 0x2C, 0xF0),
                "lengthOfSessionKeyInfo": 0x0000,
            },
            None,
            ResponseSID.Authentication,
            bytearray([0x69, 0x06, 0xA2,
                       0x87, 0xFA, 0x1D, 0xAB, 0x9C, 0xE6, 0xC6, 0xEE, 0x26, 0xD3, 0x7C, 0x59, 0x68, 0xA8, 0x2C, 0xF0,
                       0x00, 0x00])
        ),
        # verifyProofOfOwnershipBidirectional (0x07)
        (
            {
                "SubFunction": 0x07,
                "algorithmIndicator": (0xA0, 0x5C, 0x18, 0x48, 0xEB, 0x30, 0xD3, 0x5A, 0x40, 0x9A, 0xB0, 0xC4, 0x70,
                                       0xBF, 0x68, 0xC0),
                "lengthOfProofOfOwnershipClient": 0x0001,
                "proofOfOwnershipClient": 0x60,
                "lengthOfChallengeClient": 0x000A,
                "challengeClient": (0x9A, 0xD7, 0x34, 0x45, 0x5B, 0x66, 0x03, 0x09, 0x7A, 0x3D),
                "lengthOfAdditionalParameter": 0x000F,
                "additionalParameter": (0x6F, 0x32, 0x9B, 0xC6, 0xCA, 0x99, 0xC5, 0x35, 0x01, 0x43, 0x96, 0xB1, 0xEC,
                                        0xE7, 0xCF),
            },
            RequestSID.Authentication,
            None,
            bytearray([0x29, 0x07,
                       0xA0, 0x5C, 0x18, 0x48, 0xEB, 0x30, 0xD3, 0x5A, 0x40, 0x9A, 0xB0, 0xC4, 0x70, 0xBF, 0x68, 0xC0,
                       0x00, 0x01, 0x60,
                       0x00, 0x0A, 0x9A, 0xD7, 0x34, 0x45, 0x5B, 0x66, 0x03, 0x09, 0x7A, 0x3D,
                       0x00, 0x0F, 0x6F, 0x32, 0x9B, 0xC6, 0xCA, 0x99, 0xC5, 0x35, 0x01, 0x43, 0x96, 0xB1, 0xEC, 0xE7,
                       0xCF])
        ),
        (
            {
                "SubFunction": 0x87,
                "authenticationReturnParameter": 0x41,
                "algorithmIndicator": (0xF9, 0x3D, 0xC5, 0x87, 0x67, 0xE9, 0xB9, 0x35, 0x19, 0x1B, 0x34, 0x40, 0x9D,
                                       0x58, 0x1B, 0xB1),
                "lengthOfProofOfOwnershipServer": 0x0014,
                "proofOfOwnershipServer": (0x12, 0xC8, 0x2E, 0x7B, 0xC1, 0x24, 0x15, 0xE3, 0xA1, 0xBE, 0xB9, 0x94, 0x58,
                                           0x7B, 0x5E, 0xED, 0x6F, 0xB2, 0x87, 0x4E),
                "lengthOfSessionKeyInfo": 0x0018,
                "sessionKeyInfo": (0xE4, 0x4B, 0xBE, 0x79, 0x26, 0x57, 0xB5, 0x70, 0xE6, 0xF9, 0xDC, 0xFC, 0x48, 0x09,
                                   0xDC, 0x71, 0xA3, 0x68, 0x9E, 0xFD, 0xFB, 0x1C, 0xEF, 0x5B),
            },
            None,
            ResponseSID.Authentication,
            bytearray([0x69, 0x87, 0x41,
                       0xF9, 0x3D, 0xC5, 0x87, 0x67, 0xE9, 0xB9, 0x35, 0x19, 0x1B, 0x34, 0x40, 0x9D, 0x58, 0x1B, 0xB1,
                       0x00, 0x14, 0x12, 0xC8, 0x2E, 0x7B, 0xC1, 0x24, 0x15, 0xE3, 0xA1, 0xBE, 0xB9, 0x94, 0x58, 0x7B,
                       0x5E, 0xED, 0x6F, 0xB2, 0x87, 0x4E,
                       0x00, 0x18, 0xE4, 0x4B, 0xBE, 0x79, 0x26, 0x57, 0xB5, 0x70, 0xE6, 0xF9, 0xDC, 0xFC, 0x48, 0x09,
                       0xDC, 0x71, 0xA3, 0x68, 0x9E, 0xFD, 0xFB, 0x1C, 0xEF, 0x5B])
        ),
        # authenticationConfiguration (0x08)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": True,
                    "authenticationTask": 0x08
                },
            },
            RequestSID.Authentication,
            None,
            bytearray([0x29, 0x88])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": False,
                    "authenticationTask": 0x08
                },
                "authenticationReturnParameter": 0x11,
            },
            None,
            ResponseSID.Authentication,
            bytearray([0x69, 0x08, 0x11])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert AUTHENTICATION.encode(data_records_values=data_records_values,
                                                 sid=sid,
                                                 rsid=rsid) == payload

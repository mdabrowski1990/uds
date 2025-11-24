import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.secured_data_transmission import (
    SECURED_DATA_TRANSMISSION,
    SECURED_DATA_TRANSMISSION_2013,
    SECURED_DATA_TRANSMISSION_2020,
)


class TestSecuredDataTransmission:
    """Unit tests for `SecuredDataTransmission` service."""

    def test_request_sid(self):
        assert SECURED_DATA_TRANSMISSION_2013.request_sid == RequestSID.SecuredDataTransmission
        assert SECURED_DATA_TRANSMISSION_2020.request_sid == RequestSID.SecuredDataTransmission

    def test_response_sid(self):
        assert SECURED_DATA_TRANSMISSION_2013.response_sid == ResponseSID.SecuredDataTransmission
        assert SECURED_DATA_TRANSMISSION_2020.response_sid == ResponseSID.SecuredDataTransmission

    def test_default_translator(self):
        assert SECURED_DATA_TRANSMISSION is SECURED_DATA_TRANSMISSION_2020


@pytest.mark.integration
class TestSecuredDataTransmission2013Integration:
    """Integration tests for `SecuredDataTransmission` service version 2013."""

    @pytest.mark.parametrize("payload, decoded_message", [
        (
            [0x84, 0x8B],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'SecuredDataTransmission',
                    'raw_value': 0x84,
                    'unit': None
                },
                {
                    'children': ((), ),
                    'length': 8,
                    'name': 'securityDataRequestRecord',
                    'physical_value': (0x8B,),
                    'raw_value': (0x8B,),
                    'unit': None
                },
            )
        ),
        (
            [0x84, 0xB6, 0x80, 0x02, 0x91, 0x7C, 0x91, 0xD6, 0xAD, 0x18, 0x26, 0x12, 0xE8, 0x6E, 0xFF, 0xF6, 0x78, 0x77, 0x69],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'SecuredDataTransmission',
                    'raw_value': 0x84,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'securityDataRequestRecord',
                    'physical_value': (0xB6, 0x80, 0x02, 0x91, 0x7C, 0x91, 0xD6, 0xAD, 0x18, 0x26, 0x12, 0xE8, 0x6E,
                                       0xFF, 0xF6, 0x78, 0x77, 0x69),
                    'raw_value': (0xB6, 0x80, 0x02, 0x91, 0x7C, 0x91, 0xD6, 0xAD, 0x18, 0x26, 0x12, 0xE8, 0x6E,
                                  0xFF, 0xF6, 0x78, 0x77, 0x69),
                    'unit': None
                },
            )
        ),
        (
            [0xC4, 0x00],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'SecuredDataTransmission',
                    'raw_value': 0xC4,
                    'unit': None
                },
                {
                    'children': ((),),
                    'length': 8,
                    'name': 'securityDataResponseRecord',
                    'physical_value': (0x00,),
                    'raw_value': (0x00,),
                    'unit': None
                },
            )
        ),
        (
            [0xC4, 0x8C, 0x02, 0x27, 0x70, 0xD8, 0xF9, 0xA4, 0x99, 0xC8, 0xC3, 0x1F, 0xE2, 0xF3, 0xEC, 0x07, 0x18, 0x5C],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'SecuredDataTransmission',
                    'raw_value': 0xC4,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'securityDataResponseRecord',
                    'physical_value': (0x8C, 0x02, 0x27, 0x70, 0xD8, 0xF9, 0xA4, 0x99, 0xC8, 0xC3, 0x1F, 0xE2, 0xF3,
                                       0xEC, 0x07, 0x18, 0x5C),
                    'raw_value': (0x8C, 0x02, 0x27, 0x70, 0xD8, 0xF9, 0xA4, 0x99, 0xC8, 0xC3, 0x1F, 0xE2, 0xF3,
                                  0xEC, 0x07, 0x18, 0x5C),
                    'unit': None
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert SECURED_DATA_TRANSMISSION_2013.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        (
            {
                "securityDataRequestRecord": (0xFF,),
            },
            RequestSID.SecuredDataTransmission,
            None,
            bytearray([0x84, 0xFF])
        ),
        (
            {
                "securityDataResponseRecord": (0xCB, 0x12, 0xDC, 0xFF, 0x8D, 0x69, 0x69, 0x1E, 0xC7, 0x34, 0x61, 0x0B),
            },
            None,
            ResponseSID.SecuredDataTransmission,
            bytearray([0xC4, 0xCB, 0x12, 0xDC, 0xFF, 0x8D, 0x69, 0x69, 0x1E, 0xC7, 0x34, 0x61, 0x0B])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert SECURED_DATA_TRANSMISSION_2013.encode(data_records_values=data_records_values,
                                                sid=sid,
                                                rsid=rsid) == payload


@pytest.mark.integration
class TestSecuredDataTransmission2020Integration:
    """Integration tests for `SecuredDataTransmission` service version 2020."""

    @pytest.mark.parametrize("payload, decoded_message", [
        (
            [0x84,
             0x00, 0x19,
             0x00,
             0x00, 0x00,
             0xFE, 0xDC,
             0x7D],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'SecuredDataTransmission',
                    'raw_value': 0x84,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 9,
                            'name': 'reserved-9bits',
                            'physical_value': 0x000,
                            'raw_value': 0x000,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'Signature on the response is requested.',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'Message is signed.',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'Message is encrypted.',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'A pre-established key is used.',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 2,
                            'name': 'reserved',
                            'physical_value': 0x0,
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'Message is request message.',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                    ),
                    'length': 16,
                    'name': 'Administrative Parameter',
                    'physical_value': 0x0019,
                    'raw_value': 0x0019,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'Signature/Encryption Calculation',
                    'physical_value': 0x00,
                    'raw_value': 0x00,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'Signature Length',
                    'physical_value': 0x0000,
                    'raw_value': 0x0000,
                    'unit': 'bytes'
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'Anti-replay Counter',
                    'physical_value': 0xFEDC,
                    'raw_value': 0xFEDC,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'Internal Message Service Request ID',
                    'physical_value': 0x7D,
                    'raw_value': 0x7D,
                    'unit': None
                },
            )
        ),
        (
            [0x84,
             0xFF, 0xFF,
             0xE4,
             0x00, 0x10,
             0x00, 0x00,
             0xB4, 0x6C,
             0xF2, 0xDD, 0x30, 0xD7, 0xB7, 0x6F, 0x07, 0xD0, 0xA0, 0x72, 0x4F, 0x08, 0xBC, 0x3E, 0xA1, 0xCC],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'SecuredDataTransmission',
                    'raw_value': 0x84,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 9,
                            'name': 'reserved-9bits',
                            'physical_value': 0x1FF,
                            'raw_value': 0x1FF,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'Signature on the response is requested.',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'Message is signed.',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'Message is encrypted.',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'A pre-established key is used.',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 2,
                            'name': 'reserved',
                            'physical_value': 0x3,
                            'raw_value': 0x3,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'Message is request message.',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                    ),
                    'length': 16,
                    'name': 'Administrative Parameter',
                    'physical_value': 0xFFFF,
                    'raw_value': 0xFFFF,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'Signature/Encryption Calculation',
                    'physical_value': 0xE4,
                    'raw_value': 0xE4,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'Signature Length',
                    'physical_value': 0x0010,
                    'raw_value': 0x0010,
                    'unit': 'bytes'
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'Anti-replay Counter',
                    'physical_value': 0x0000,
                    'raw_value': 0x0000,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'Internal Message Service Request ID',
                    'physical_value': 0xB4,
                    'raw_value': 0xB4,
                    'unit': None
                },
                {
                    'children': ((),),
                    'length': 8,
                    'name': 'Service Specific Parameters',
                    'physical_value': (0x6C,),
                    'raw_value': (0x6C,),
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'Signature/MAC',
                    'physical_value': (0xF2, 0xDD, 0x30, 0xD7, 0xB7, 0x6F, 0x07, 0xD0, 0xA0, 0x72, 0x4F, 0x08, 0xBC,
                                       0x3E, 0xA1, 0xCC),
                    'raw_value': (0xF2, 0xDD, 0x30, 0xD7, 0xB7, 0x6F, 0x07, 0xD0, 0xA0, 0x72, 0x4F, 0x08, 0xBC,
                                  0x3E, 0xA1, 0xCC),
                    'unit': None
                },
            )
        ),
        (
            [0xC4,
             0x00, 0x00,
             0xFF,
             0x00, 0x05,
             0x15, 0x9D,
             0x3F,
             0xBF, 0xCE, 0xB7, 0xE4, 0xEE],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'SecuredDataTransmission',
                    'raw_value': 0xC4,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 9,
                            'name': 'reserved-9bits',
                            'physical_value': 0x000,
                            'raw_value': 0x000,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'Signature on the response is requested.',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'Message is signed.',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'Message is encrypted.',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'A pre-established key is used.',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 2,
                            'name': 'reserved',
                            'physical_value': 0x0,
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'Message is request message.',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                    ),
                    'length': 16,
                    'name': 'Administrative Parameter',
                    'physical_value': 0x0000,
                    'raw_value': 0x0000,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'Signature/Encryption Calculation',
                    'physical_value': 0xFF,
                    'raw_value': 0xFF,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'Signature Length',
                    'physical_value': 0x0005,
                    'raw_value': 0x0005,
                    'unit': 'bytes'
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'Anti-replay Counter',
                    'physical_value': 0x159D,
                    'raw_value': 0x159D,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'Internal Message Service Response ID',
                    'physical_value': 0x3F,
                    'raw_value': 0x3F,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), ()),
                    'length': 8,
                    'name': 'Signature/MAC',
                    'physical_value': (0xBF, 0xCE, 0xB7, 0xE4, 0xEE),
                    'raw_value': (0xBF, 0xCE, 0xB7, 0xE4, 0xEE),
                    'unit': None
                },
            )
        ),
        (
            [0xC4,
             0x7F, 0xFA,
             0xD4,
             0x00, 0x00,
             0x89, 0x58,
             0x04, 0xC7, 0x56, 0x63, 0x65, 0xFE, 0x0C, 0xFC],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'SecuredDataTransmission',
                    'raw_value': 0xC4,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 9,
                            'name': 'reserved-9bits',
                            'physical_value': 0x0FF,
                            'raw_value': 0x0FF,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'Signature on the response is requested.',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'Message is signed.',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'Message is encrypted.',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'A pre-established key is used.',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 2,
                            'name': 'reserved',
                            'physical_value': 0x1,
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'Message is request message.',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                    ),
                    'length': 16,
                    'name': 'Administrative Parameter',
                    'physical_value': 0x7FFA,
                    'raw_value': 0x7FFA,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'Signature/Encryption Calculation',
                    'physical_value': 0xD4,
                    'raw_value': 0xD4,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'Signature Length',
                    'physical_value': 0x0000,
                    'raw_value': 0x0000,
                    'unit': 'bytes'
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'Anti-replay Counter',
                    'physical_value': 0x8958,
                    'raw_value': 0x8958,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'Internal Message Service Response ID',
                    'physical_value': 0x04,
                    'raw_value': 0x04,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'Response Specific Parameters',
                    'physical_value': (0xC7, 0x56, 0x63, 0x65, 0xFE, 0x0C, 0xFC),
                    'raw_value': (0xC7, 0x56, 0x63, 0x65, 0xFE, 0x0C, 0xFC),
                    'unit': None
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert SECURED_DATA_TRANSMISSION_2020.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        (
            {
                "Administrative Parameter": {
                    "reserved-9bits": 0x000,
                    "Signature on the response is requested.": True,
                    "Message is signed.": True,
                    "Message is encrypted.": True,
                    "A pre-established key is used.": True,
                    "reserved": 0x0,
                    "Message is request message.": True,
                },
                "Signature/Encryption Calculation": 0x5A,
                "Signature Length": 0x0002,
                "Anti-replay Counter": 0xF0B8,
                "Internal Message Service Request ID": 0x16,
                "Service Specific Parameters": (0x27, 0xEC, 0x1E, 0x54, 0x1A, 0xD6, 0xA4, 0x31, 0x6D),
                "Signature/MAC": (0x2C, 0x04),
            },
            RequestSID.SecuredDataTransmission,
            None,
            bytearray([0x84, 0x00, 0x79, 0x5A, 0x00, 0x02, 0xF0, 0xB8,
                       0x16, 0x27, 0xEC, 0x1E, 0x54, 0x1A, 0xD6, 0xA4, 0x31, 0x6D,
                       0x2C, 0x04])
        ),
        (
            {
                "Administrative Parameter": 0x0001,
                "Signature/Encryption Calculation": 0x3A,
                "Signature Length": 0x0000,
                "Anti-replay Counter": 0x4AA4,
                "Internal Message Service Request ID": 0x7B,
            },
            RequestSID.SecuredDataTransmission,
            None,
            bytearray([0x84, 0x00, 0x01, 0x3A, 0x00, 0x00, 0x4A, 0xA4,
                       0x7B])
        ),
        (
            {
                "Administrative Parameter": 0xAC54,
                "Signature/Encryption Calculation": 0x63,
                "Signature Length": 0x0000,
                "Anti-replay Counter": 0x3041,
                "Internal Message Service Response ID": 0x97,
                "Response Specific Parameters": (0x76,),
            },
            None,
            ResponseSID.SecuredDataTransmission,
            bytearray([0xC4, 0xAC, 0x54, 0x63, 0x00, 0x00, 0x30, 0x41,
                       0x97, 0x76])
        ),
        (
            {
                "Administrative Parameter": 0x5940,
                "Signature/Encryption Calculation": 0x03,
                "Signature Length": 0x000D,
                "Anti-replay Counter": 0x83F8,
                "Internal Message Service Response ID": 0x76,
                "Signature/MAC": (0x85, 0x3E, 0x98, 0x3C, 0xC0, 0xB0, 0x9F, 0x11, 0xDE, 0x4F, 0x12, 0x02, 0x2A),
            },
            None,
            ResponseSID.SecuredDataTransmission,
            bytearray([0xC4, 0x59, 0x40, 0x03, 0x00, 0x0D, 0x83, 0xF8,
                       0x76,
                       0x85, 0x3E, 0x98, 0x3C, 0xC0, 0xB0, 0x9F, 0x11, 0xDE, 0x4F, 0x12, 0x02, 0x2A])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert SECURED_DATA_TRANSMISSION_2020.encode(data_records_values=data_records_values,
                                                sid=sid,
                                                rsid=rsid) == payload

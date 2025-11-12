import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.dynamically_define_data_identifier import (
    DYNAMICALLY_DEFINE_DATA_IDENTIFIER,
    DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2013,
    DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2020,
)


class TestDynamicallyDefineDataIdentifier:
    """Unit tests for `DynamicallyDefineDataIdentifier` service."""

    def test_request_sid(self):
        assert DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2013.request_sid == RequestSID.DynamicallyDefineDataIdentifier
        assert DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2020.request_sid == RequestSID.DynamicallyDefineDataIdentifier

    def test_response_sid(self):
        assert DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2013.response_sid == ResponseSID.DynamicallyDefineDataIdentifier
        assert DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2020.response_sid == ResponseSID.DynamicallyDefineDataIdentifier

    def test_default_translator(self):
        assert DYNAMICALLY_DEFINE_DATA_IDENTIFIER is DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2020


@pytest.mark.integration
class TestDynamicallyDefineDataIdentifier2013Integration:
    """Integration tests for `DynamicallyDefineDataIdentifier` service version 2013."""

    @pytest.mark.parametrize("payload, decoded_message", [
        # defineByIdentifier (0x01)
        (
            [0x2C, 0x81, 0xF3, 0xFF,
             0xF1, 0x97, 0x6A, 0x83],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'DynamicallyDefineDataIdentifier',
                    'raw_value': 0x2C,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': "suppressPosRspMsgIndicationBit",
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "definitionType",
                            'physical_value': 'defineByIdentifier',
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
                    'length': 16,
                    'name': 'dynamicallyDefinedDataIdentifier',
                    'physical_value': 0xF3FF,
                    'raw_value': 0xF3FF,
                    'unit': None
                },
                {
                    'children': (
                        (
                            {
                                'children': (),
                                'length': 16,
                                'name': 'sourceDataIdentifier',
                                'physical_value': "systemNameOrEngineTypeDataIdentifier",
                                'raw_value': 0xF197,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'positionInSourceDataRecord',
                                'physical_value': 0x6A,
                                'raw_value': 0x6A,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'memorySize',
                                'physical_value': 0x83,
                                'raw_value': 0x83,
                                'unit': None
                            },
                        ),
                    ),
                    'length': 32,
                    'name': 'Data from DID',
                    "physical_value": (0xF1976A83,),
                    "raw_value": (0xF1976A83,),
                    'unit': None
                },
            )
        ),
        (
            [0x6C, 0x01, 0xF2, 0x45],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'DynamicallyDefineDataIdentifier',
                    'raw_value': 0x6C,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': "suppressPosRspMsgIndicationBit",
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "definitionType",
                            'physical_value': 'defineByIdentifier',
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
                    'length': 16,
                    'name': 'dynamicallyDefinedDataIdentifier',
                    'physical_value': 0xF245,
                    'raw_value': 0xF245,
                    'unit': None
                },
            )
        ),
        # defineByMemoryAddress (0x02)
        (
            [0x2C, 0x02, 0xF2, 0x00, 0x14,
             0xD7, 0xCD, 0xEA, 0x54, 0xC2,
             0x62, 0x54, 0x41, 0xBA, 0xDA,
             0x54, 0x80, 0x91, 0xCA, 0xDE,
             0x43, 0x7D, 0x4C, 0xAA, 0xA1],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'DynamicallyDefineDataIdentifier',
                    'raw_value': 0x2C,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': "suppressPosRspMsgIndicationBit",
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "definitionType",
                            'physical_value': 'defineByMemoryAddress',
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
                    'length': 16,
                    'name': 'dynamicallyDefinedDataIdentifier',
                    'physical_value': 0xF200,
                    'raw_value': 0xF200,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'memorySizeLength',
                            'physical_value': 0x1,
                            'raw_value': 0x1,
                            'unit': 'bytes',
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'memoryAddressLength',
                            'physical_value': 0x4,
                            'raw_value': 0x4,
                            'unit': 'bytes',
                        },
                    ),
                    'length': 8,
                    'name': 'addressAndLengthFormatIdentifier',
                    'physical_value': 0x14,
                    'raw_value': 0x14,
                    'unit': None
                },
                {
                    'children': (
                        (
                            {
                                'children': (),
                                'length': 32,
                                'name': 'memoryAddress',
                                'physical_value': 0xD7CDEA54,
                                'raw_value': 0xD7CDEA54,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'memorySize',
                                'physical_value': 0xC2,
                                'raw_value': 0xC2,
                                'unit': None
                            },
                        ),
                        (
                            {
                                'children': (),
                                'length': 32,
                                'name': 'memoryAddress',
                                'physical_value': 0x625441BA,
                                'raw_value': 0x625441BA,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'memorySize',
                                'physical_value': 0xDA,
                                'raw_value': 0xDA,
                                'unit': None
                            },
                        ),
                        (
                            {
                                'children': (),
                                'length': 32,
                                'name': 'memoryAddress',
                                'physical_value': 0x548091CA,
                                'raw_value': 0x548091CA,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'memorySize',
                                'physical_value': 0xDE,
                                'raw_value': 0xDE,
                                'unit': None
                            },
                        ),
                        (
                            {
                                'children': (),
                                'length': 32,
                                'name': 'memoryAddress',
                                'physical_value': 0x437D4CAA,
                                'raw_value': 0x437D4CAA,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'memorySize',
                                'physical_value': 0xA1,
                                'raw_value': 0xA1,
                                'unit': None
                            },
                        ),
                    ),
                    'length': 40,
                    'name': 'Data from Memory',
                    "physical_value": (0xD7CDEA54C2, 0x625441BADA, 0x548091CADE, 0x437D4CAAA1),
                    "raw_value": (0xD7CDEA54C2, 0x625441BADA, 0x548091CADE, 0x437D4CAAA1),
                    'unit': None
                },
            )
        ),
        (
            [0x6C, 0x82, 0xF3, 0xE0],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'DynamicallyDefineDataIdentifier',
                    'raw_value': 0x6C,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': "suppressPosRspMsgIndicationBit",
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "definitionType",
                            'physical_value': 'defineByMemoryAddress',
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
                    'length': 16,
                    'name': 'dynamicallyDefinedDataIdentifier',
                    'physical_value': 0xF3E0,
                    'raw_value': 0xF3E0,
                    'unit': None
                },
            )
        ),
        # clearDynamicallyDefinedDataIdentifier (0x03)
        (
            [0x2C, 0x83],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'DynamicallyDefineDataIdentifier',
                    'raw_value': 0x2C,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': "suppressPosRspMsgIndicationBit",
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "definitionType",
                            'physical_value': 'clearDynamicallyDefinedDataIdentifier',
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
            )
        ),
        (
            [0x6C, 0x03, 0xF3, 0xDB],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'DynamicallyDefineDataIdentifier',
                    'raw_value': 0x6C,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': "suppressPosRspMsgIndicationBit",
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "definitionType",
                            'physical_value': 'clearDynamicallyDefinedDataIdentifier',
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
                    'length': 16,
                    'name': 'dynamicallyDefinedDataIdentifier',
                    'physical_value': 0xF3DB,
                    'raw_value': 0xF3DB,
                    'unit': None
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2013.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        # defineByMemoryAddress (0x01)
        (
            {
                "SubFunction": 0x01,
                "dynamicallyDefinedDataIdentifier": 0xF345,
                "Data from DID": (
                    {
                        "sourceDataIdentifier": 0x4321,
                        "positionInSourceDataRecord": 0x01,
                        "memorySize": 0x2B,
                    },
                    {
                        "sourceDataIdentifier": 0xF19A,
                        "positionInSourceDataRecord": 0x1E,
                        "memorySize": 0xD0,
                    },
                ),
            },
            RequestSID.DynamicallyDefineDataIdentifier,
            None,
            bytearray([0x2C, 0x01, 0xF3, 0x45,
                       0x43, 0x21, 0x01, 0x2B,
                       0xF1, 0x9A, 0x1E, 0xD0])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "definitionType": 0x01,
                },
                "dynamicallyDefinedDataIdentifier": 0xF2FF,
            },
            None,
            ResponseSID.DynamicallyDefineDataIdentifier,
            bytearray([0x6C, 0x81, 0xF2, 0xFF])
        ),
        # defineByMemoryAddress (0x02)
        (
            {
                "SubFunction": 0x82,
                "dynamicallyDefinedDataIdentifier": 0xF2FE,
                "addressAndLengthFormatIdentifier": 0xFF,
                "Data from Memory": (0x7F2FFC8B743D080FEC4CC76DDD594DFA932806E2FE948357E869C91E4255,),
            },
            RequestSID.DynamicallyDefineDataIdentifier,
            None,
            bytearray([0x2C, 0x82, 0xF2, 0xFE, 0xFF,
                       0x7F, 0x2F, 0xFC, 0x8B, 0x74, 0x3D, 0x08, 0x0F, 0xEC, 0x4C, 0xC7, 0x6D, 0xDD, 0x59, 0x4D,
                       0xFA, 0x93, 0x28, 0x06, 0xE2, 0xFE, 0x94, 0x83, 0x57, 0xE8, 0x69, 0xC9, 0x1E, 0x42, 0x55])
        ),
        (
            {
                "SubFunction": 0x02,
                "dynamicallyDefinedDataIdentifier": 0xF2FF,
            },
            None,
            ResponseSID.DynamicallyDefineDataIdentifier,
            bytearray([0x6C, 0x02, 0xF2, 0xFF])
        ),
        # clearDynamicallyDefinedDataIdentifier (0x03)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 0,
                    "definitionType": 0x03,
                },
                "dynamicallyDefinedDataIdentifier": 0xF269,
            },
            RequestSID.DynamicallyDefineDataIdentifier,
            None,
            bytearray([0x2C, 0x03, 0xF2, 0x69])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "definitionType": 0x03,
                },
            },
            None,
            ResponseSID.DynamicallyDefineDataIdentifier,
            bytearray([0x6C, 0x83])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2013.encode(data_records_values=data_records_values,
                                                              sid=sid,
                                                              rsid=rsid) == payload


@pytest.mark.integration
class TestDynamicallyDefineDataIdentifier2020Integration:
    """Integration tests for `DynamicallyDefineDataIdentifier` service version 2020."""

    @pytest.mark.parametrize("payload, decoded_message", [
        # defineByIdentifier (0x01)
        (
            [0x2C, 0x01, 0xF2, 0x00,
             0xFF, 0x01, 0x3C, 0x19,
             0xF2, 0xC9, 0xE2, 0x30,
             0xB7, 0x33, 0x54, 0x47,
             0x67, 0xD3, 0x3E, 0xBD],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'DynamicallyDefineDataIdentifier',
                    'raw_value': 0x2C,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': "suppressPosRspMsgIndicationBit",
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "definitionType",
                            'physical_value': 'defineByIdentifier',
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
                    'length': 16,
                    'name': 'dynamicallyDefinedDataIdentifier',
                    'physical_value': 0xF200,
                    'raw_value': 0xF200,
                    'unit': None
                },
                {
                    'children': (
                        (
                            {
                                'children': (),
                                'length': 16,
                                'name': 'sourceDataIdentifier',
                                'physical_value': "ReservedForISO15765-5",
                                'raw_value': 0xFF01,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'positionInSourceDataRecord',
                                'physical_value': 0x3C,
                                'raw_value': 0x3C,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'memorySize',
                                'physical_value': 0x19,
                                'raw_value': 0x19,
                                'unit': None
                            },
                        ),
                        (
                            {
                                'children': (),
                                'length': 16,
                                'name': 'sourceDataIdentifier',
                                'physical_value': 0xF2C9,
                                'raw_value': 0xF2C9,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'positionInSourceDataRecord',
                                'physical_value': 0xE2,
                                'raw_value': 0xE2,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'memorySize',
                                'physical_value': 0x30,
                                'raw_value': 0x30,
                                'unit': None
                            },
                        ),
                        (
                            {
                                'children': (),
                                'length': 16,
                                'name': 'sourceDataIdentifier',
                                'physical_value': 0xB733,
                                'raw_value': 0xB733,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'positionInSourceDataRecord',
                                'physical_value': 0x54,
                                'raw_value': 0x54,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'memorySize',
                                'physical_value': 0x47,
                                'raw_value': 0x47,
                                'unit': None
                            },
                        ),
                        (
                            {
                                'children': (),
                                'length': 16,
                                'name': 'sourceDataIdentifier',
                                'physical_value': 0x67D3,
                                'raw_value': 0x67D3,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'positionInSourceDataRecord',
                                'physical_value': 0x3E,
                                'raw_value': 0x3E,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'memorySize',
                                'physical_value': 0xBD,
                                'raw_value': 0xBD,
                                'unit': None
                            },
                        ),
                    ),
                    'length': 32,
                    'name': 'Data from DID',
                    "physical_value": (0xFF013C19, 0xF2C9E230, 0xB7335447, 0x67D33EBD),
                    "raw_value": (0xFF013C19, 0xF2C9E230, 0xB7335447, 0x67D33EBD),
                    'unit': None
                },
            )
        ),
        (
            [0x6C, 0x81, 0xF3, 0x80],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'DynamicallyDefineDataIdentifier',
                    'raw_value': 0x6C,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': "suppressPosRspMsgIndicationBit",
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "definitionType",
                            'physical_value': 'defineByIdentifier',
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
                    'length': 16,
                    'name': 'dynamicallyDefinedDataIdentifier',
                    'physical_value': 0xF380,
                    'raw_value': 0xF380,
                    'unit': None
                },
            )
        ),
        # defineByMemoryAddress (0x02)
        (
            [0x2C, 0x82, 0xF3, 0xFF, 0x25,
             0x92, 0x86, 0x7D, 0xA5, 0xA4, 0x17, 0xCF],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'DynamicallyDefineDataIdentifier',
                    'raw_value': 0x2C,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': "suppressPosRspMsgIndicationBit",
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "definitionType",
                            'physical_value': 'defineByMemoryAddress',
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
                    'length': 16,
                    'name': 'dynamicallyDefinedDataIdentifier',
                    'physical_value': 0xF3FF,
                    'raw_value': 0xF3FF,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'memorySizeLength',
                            'physical_value': 0x2,
                            'raw_value': 0x2,
                            'unit': 'bytes',
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'memoryAddressLength',
                            'physical_value': 0x5,
                            'raw_value': 0x5,
                            'unit': 'bytes',
                        },
                    ),
                    'length': 8,
                    'name': 'addressAndLengthFormatIdentifier',
                    'physical_value': 0x25,
                    'raw_value': 0x25,
                    'unit': None
                },
                {
                    'children': (
                        (
                            {
                                'children': (),
                                'length': 40,
                                'name': 'memoryAddress',
                                'physical_value': 0x92867DA5A4,
                                'raw_value': 0x92867DA5A4,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 16,
                                'name': 'memorySize',
                                'physical_value': 0x17CF,
                                'raw_value': 0x17CF,
                                'unit': None
                            },
                        ),
                    ),
                    'length': 56,
                    'name': 'Data from Memory',
                    "physical_value": (0x92867DA5A417CF,),
                    "raw_value": (0x92867DA5A417CF,),
                    'unit': None
                },
            )
        ),
        (
            [0x6C, 0x02, 0xF2, 0x2C],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'DynamicallyDefineDataIdentifier',
                    'raw_value': 0x6C,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': "suppressPosRspMsgIndicationBit",
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "definitionType",
                            'physical_value': 'defineByMemoryAddress',
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
                    'length': 16,
                    'name': 'dynamicallyDefinedDataIdentifier',
                    'physical_value': 0xF22C,
                    'raw_value': 0xF22C,
                    'unit': None
                },
            )
        ),
        # clearDynamicallyDefinedDataIdentifier (0x03)
        (
            [0x2C, 0x03, 0xF3, 0x51],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'DynamicallyDefineDataIdentifier',
                    'raw_value': 0x2C,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': "suppressPosRspMsgIndicationBit",
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "definitionType",
                            'physical_value': 'clearDynamicallyDefinedDataIdentifier',
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
                    'length': 16,
                    'name': 'dynamicallyDefinedDataIdentifier',
                    'physical_value': 0xF351,
                    'raw_value': 0xF351,
                    'unit': None
                },
            )
        ),
        (
            [0x6C, 0x83],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'DynamicallyDefineDataIdentifier',
                    'raw_value': 0x6C,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': "suppressPosRspMsgIndicationBit",
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "definitionType",
                            'physical_value': 'clearDynamicallyDefinedDataIdentifier',
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
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2020.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        # defineByMemoryAddress (0x01)
        (
            {
                "SubFunction": 0x81,
                "dynamicallyDefinedDataIdentifier": 0xF200,
                "Data from DID": (
                    {
                        "sourceDataIdentifier": 0xFFFF,
                        "positionInSourceDataRecord": 0xFF,
                        "memorySize": 0x01,
                    },
                ),
            },
            RequestSID.DynamicallyDefineDataIdentifier,
            None,
            bytearray([0x2C, 0x81, 0xF2, 0x00,
                       0xFF, 0xFF, 0xFF, 0x01])
        ),
        (
            {
                "SubFunction": 0x01,
                "dynamicallyDefinedDataIdentifier": 0xF3FF,
            },
            None,
            ResponseSID.DynamicallyDefineDataIdentifier,
            bytearray([0x6C, 0x01, 0xF3, 0xFF])
        ),
        # defineByMemoryAddress (0x02)
        (
            {
                "SubFunction": 0x02,
                "dynamicallyDefinedDataIdentifier": 0xF2D2,
                "addressAndLengthFormatIdentifier": 0x12,
                "Data from Memory": (
                    {
                        "memoryAddress": 0x9189,
                        "memorySize": 0x1E,
                    },
                    {
                        "memoryAddress": 0xE112,
                        "memorySize": 0x80,
                    },
                    {
                        "memoryAddress": 0x89CD,
                        "memorySize": 0xD4,
                    },
                    {
                        "memoryAddress": 0x79EC,
                        "memorySize": 0x81,
                    },
                    {
                        "memoryAddress": 0x6B69,
                        "memorySize": 0x2E,
                    },
                ),
            },
            RequestSID.DynamicallyDefineDataIdentifier,
            None,
            bytearray([0x2C, 0x02, 0xF2, 0xD2, 0x12,
                       0x91, 0x89, 0x1E,
                       0xE1, 0x12, 0x80,
                       0x89, 0xCD, 0xD4,
                       0x79, 0xEC, 0x81,
                       0x6B, 0x69, 0x2E])
        ),
        (
            {
                "SubFunction": 0x82,
                "dynamicallyDefinedDataIdentifier": 0xF300,
            },
            None,
            ResponseSID.DynamicallyDefineDataIdentifier,
            bytearray([0x6C, 0x82, 0xF3, 0x00])
        ),
        # clearDynamicallyDefinedDataIdentifier (0x03)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "definitionType": 0x03,
                },
            },
            RequestSID.DynamicallyDefineDataIdentifier,
            None,
            bytearray([0x2C, 0x83])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 0,
                    "definitionType": 0x03,
                },
                "dynamicallyDefinedDataIdentifier": 0xF369,
            },
            None,
            ResponseSID.DynamicallyDefineDataIdentifier,
            bytearray([0x6C, 0x03, 0xF3, 0x69])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2020.encode(data_records_values=data_records_values,
                                                              sid=sid,
                                                              rsid=rsid) == payload

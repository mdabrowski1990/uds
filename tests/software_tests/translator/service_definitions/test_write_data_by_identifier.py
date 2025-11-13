import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.write_data_by_identifier import (
    WRITE_DATA_BY_IDENTIFIER,
    WRITE_DATA_BY_IDENTIFIER_2013,
    WRITE_DATA_BY_IDENTIFIER_2020,
)


class TestWriteDataByIdentifier:
    """Unit tests for `WriteDataByIdentifier` service."""

    def test_request_sid(self):
        assert WRITE_DATA_BY_IDENTIFIER_2013.request_sid == RequestSID.WriteDataByIdentifier
        assert WRITE_DATA_BY_IDENTIFIER_2020.request_sid == RequestSID.WriteDataByIdentifier

    def test_response_sid(self):
        assert WRITE_DATA_BY_IDENTIFIER_2013.response_sid == ResponseSID.WriteDataByIdentifier
        assert WRITE_DATA_BY_IDENTIFIER_2020.response_sid == ResponseSID.WriteDataByIdentifier

    def test_default_translator(self):
        assert WRITE_DATA_BY_IDENTIFIER is WRITE_DATA_BY_IDENTIFIER_2020


@pytest.mark.integration
class TestWriteDataByIdentifier2013Integration:
    """Integration tests for `WriteDataByIdentifier` service version 2013."""

    @pytest.mark.parametrize("payload, decoded_message", [
        (
            [0x2E, 0xF1, 0x86, 0x03],  # it is the only DID that has defined length by ISO 14229
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'WriteDataByIdentifier',
                    'raw_value': 0x2E,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DID',
                    'physical_value': "ActiveDiagnosticSessionDataIdentifier",
                    'raw_value': 0xF186,
                    'unit': None
                },
                {
                    'children': (
                            {
                                'children': (),
                                'length': 1,
                                'name': 'reserved',
                                'physical_value': 0,
                                'raw_value': 0,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 7,
                                'name': 'ActiveDiagnosticSession',
                                'physical_value': "extendedDiagnosticSession",
                                'raw_value': 0x03,
                                'unit': None
                            }
                    ),
                    'length': 8,
                    'name': 'DID data',
                    'physical_value': 0x03,
                    'raw_value': 0x03,
                    'unit': None
                },
            )
        ),
        (
            [0x6E, 0xFA, 0x10],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'WriteDataByIdentifier',
                    'raw_value': 0x6E,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DID',
                    'physical_value': "NumberOfEDRDevices",
                    'raw_value': 0xFA10,
                    'unit': None
                },
            )
        ),
        (
            [0x6E, 0x12, 0x34],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'WriteDataByIdentifier',
                    'raw_value': 0x6E,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DID',
                    'physical_value': 0x1234,
                    'raw_value': 0x1234,
                    'unit': None
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert WRITE_DATA_BY_IDENTIFIER_2013.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        (
            {
                "DID": 0x928A,
                "DID data": (0xA7, 0xBB, 0x3E, 0x0B, 0x1C, 0xBD, 0x6D, 0x76, 0xDC, 0x3A, 0xB9, 0xE8, 0x45, 0x4D),
            },
            RequestSID.WriteDataByIdentifier,
            None,
            bytearray([0x2E, 0x92, 0x8A,
                       0xA7, 0xBB, 0x3E, 0x0B, 0x1C, 0xBD, 0x6D, 0x76, 0xDC, 0x3A, 0xB9, 0xE8, 0x45, 0x4D])
        ),
        (
            {
                "DID": 0x2468,
            },
            None,
            ResponseSID.WriteDataByIdentifier,
            bytearray([0x6E, 0x24, 0x68])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert WRITE_DATA_BY_IDENTIFIER_2013.encode(data_records_values=data_records_values,
                                                   sid=sid,
                                                   rsid=rsid) == payload


@pytest.mark.integration
class TestWriteDataByIdentifier2020Integration:
    """Integration tests for `WriteDataByIdentifier` service version 2020."""

    @pytest.mark.parametrize("payload, decoded_message", [
        (
            [0x2E, 0xF1, 0x86, 0x01],  # it is the only DID that has defined length by ISO 14229
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'WriteDataByIdentifier',
                    'raw_value': 0x2E,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DID',
                    'physical_value': "ActiveDiagnosticSessionDataIdentifier",
                    'raw_value': 0xF186,
                    'unit': None
                },
                {
                    'children': (
                            {
                                'children': (),
                                'length': 1,
                                'name': 'reserved',
                                'physical_value': 0,
                                'raw_value': 0,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 7,
                                'name': 'ActiveDiagnosticSession',
                                'physical_value': "defaultSession",
                                'raw_value': 0x01,
                                'unit': None
                            }
                    ),
                    'length': 8,
                    'name': 'DID data',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': None
                },
            )
        ),
        (
            [0x6E, 0xFF, 0x01],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'WriteDataByIdentifier',
                    'raw_value': 0x6E,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DID',
                    'physical_value': "ReservedForISO15765-5",
                    'raw_value': 0xFF01,
                    'unit': None
                },
            )
        ),
        (
            [0x6E, 0x60, 0xFB],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'WriteDataByIdentifier',
                    'raw_value': 0x6E,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DID',
                    'physical_value': 0x60FB,
                    'raw_value': 0x60FB,
                    'unit': None
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert WRITE_DATA_BY_IDENTIFIER_2020.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        (
            {
                "DID": 0x59DF,
                "DID data": (0x7E, 0xFB, 0x44, 0x26, 0x3B, 0xE0, 0xA8, 0x19, 0xC4, 0x83, 0x61, 0x06, 0x0A, 0x87, 0x19,
                             0x38, 0xB1, 0x87, 0x87, 0xC4, 0x01, 0x4F, 0x91, 0xA3, 0x05, 0x14, 0x4E, 0xDB, 0xAF, 0xD9,
                             0xB3, 0x2D, 0xDB, 0x90, 0x6A, 0x71, 0x12, 0x9D, 0x0D, 0x0A, 0xF8, 0x6F, 0x11, 0xCF, 0x24),
            },
            RequestSID.WriteDataByIdentifier,
            None,
            bytearray([0x2E, 0x59, 0xDF,
                       0x7E, 0xFB, 0x44, 0x26, 0x3B, 0xE0, 0xA8, 0x19, 0xC4, 0x83, 0x61, 0x06, 0x0A, 0x87, 0x19,
                       0x38, 0xB1, 0x87, 0x87, 0xC4, 0x01, 0x4F, 0x91, 0xA3, 0x05, 0x14, 0x4E, 0xDB, 0xAF, 0xD9,
                       0xB3, 0x2D, 0xDB, 0x90, 0x6A, 0x71, 0x12, 0x9D, 0x0D, 0x0A, 0xF8, 0x6F, 0x11, 0xCF, 0x24])
        ),
        (
            {
                "DID": 0x0D76,
            },
            None,
            ResponseSID.WriteDataByIdentifier,
            bytearray([0x6E, 0x0D, 0x76])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert WRITE_DATA_BY_IDENTIFIER_2020.encode(data_records_values=data_records_values,
                                                   sid=sid,
                                                   rsid=rsid) == payload

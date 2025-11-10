import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.read_data_by_periodic_identifier import READ_DATA_BY_PERIODIC_IDENTIFIER


class TestReadDataByPeriodicIdentifier:
    """Unit tests for `ReadDataByPeriodicIdentifier` service."""

    def test_request_sid(self):
        assert READ_DATA_BY_PERIODIC_IDENTIFIER.request_sid == RequestSID.ReadDataByPeriodicIdentifier

    def test_response_sid(self):
        assert READ_DATA_BY_PERIODIC_IDENTIFIER.response_sid == ResponseSID.ReadDataByPeriodicIdentifier


@pytest.mark.integration
class TestReadDataByPeriodicIdentifierIntegration:
    """Integration tests for `ReadDataByPeriodicIdentifier` service version 2013."""

    @pytest.mark.parametrize("payload, decoded_message", [
        (
            [0x2A, 0x01, 0xFF],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'ReadDataByPeriodicIdentifier',
                    'raw_value': 0x2A,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'transmissionMode',
                    'physical_value': "sendAtSlowRate",
                    'raw_value': 0x01,
                    'unit': None
                },
                {
                    'children': ((),),
                    'length': 8,
                    'name': 'Periodic DID',
                    'physical_value': (0xF2FF,),
                    'raw_value': (0xFF,),
                    'unit': None
                },
            )
        ),
        (
            [0x2A, 0x02, 0x00, 0x12, 0xFF],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'ReadDataByPeriodicIdentifier',
                    'raw_value': 0x2A,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'transmissionMode',
                    'physical_value': "sendAtMediumRate",
                    'raw_value': 0x02,
                    'unit': None
                },
                {
                    'children': ((), (), ()),
                    'length': 8,
                    'name': 'Periodic DID',
                    'physical_value': (0xF200, 0xF212, 0xF2FF),
                    'raw_value': (0x00, 0x12, 0xFF),
                    'unit': None
                },
            )
        ),
        (
            [0x2A, 0x04],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'ReadDataByPeriodicIdentifier',
                    'raw_value': 0x2A,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'transmissionMode',
                    'physical_value': "stopSending",
                    'raw_value': 0x04,
                    'unit': None
                },
            )
        ),
        (
            [0x2A, 0x04, 0x52, 0x6D, 0x4F, 0x02],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'ReadDataByPeriodicIdentifier',
                    'raw_value': 0x2A,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'transmissionMode',
                    'physical_value': "stopSending",
                    'raw_value': 0x04,
                    'unit': None
                },
                {
                    'children': ((), (), (), ()),
                    'length': 8,
                    'name': 'Periodic DID',
                    'physical_value': (0xF252, 0xF26D, 0xF24F, 0xF202),
                    'raw_value': (0x52, 0x6D, 0x4F, 0x02),
                    'unit': None
                },
            )
        ),
        (
            [0x6A],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'ReadDataByPeriodicIdentifier',
                    'raw_value': 0x6A,
                    'unit': None
                },
            )
        ),
        (
            [0x6A, 0x00, 0x23],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'ReadDataByPeriodicIdentifier',
                    'raw_value': 0x6A,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'Periodic DID',
                    'physical_value': 0xF200,
                    'raw_value': 0x00,
                    'unit': None
                },
                {
                    'children': ((),),
                    'length': 8,
                    'name': 'data',
                    'physical_value': (0x23,),
                    'raw_value': (0x23,),
                    'unit': None
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert READ_DATA_BY_PERIODIC_IDENTIFIER.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        (
                {
                    "transmissionMode": 0x03,
                    "Periodic DID": (0xFF, 0x00, 0x5A),
                },
                RequestSID.ReadDataByPeriodicIdentifier,
                None,
                bytearray([0x2A, 0x03, 0xFF, 0x00, 0x5A])
        ),
        (
                {
                    "transmissionMode": 0x04,
                },
                RequestSID.ReadDataByPeriodicIdentifier,
                None,
                bytearray([0x2A, 0x04])
        ),
        (
                {},
                None,
                ResponseSID.ReadDataByPeriodicIdentifier,
                bytearray([0x6A])
        ),
        (
                {
                    "Periodic DID": 0xC8,
                    "data": (0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5, 0x96, 0x87)
                },
                None,
                ResponseSID.ReadDataByPeriodicIdentifier,
                bytearray([0x6A, 0xC8, 0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5, 0x96, 0x87])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert READ_DATA_BY_PERIODIC_IDENTIFIER.encode(data_records_values=data_records_values,
                                                       sid=sid,
                                                       rsid=rsid) == payload

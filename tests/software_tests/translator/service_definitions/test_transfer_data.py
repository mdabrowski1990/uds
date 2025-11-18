import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.transfer_data import TRANSFER_DATA


class TestTransferData:
    """Unit tests for `TransferData` service."""

    def test_request_sid(self):
        assert TRANSFER_DATA.request_sid == RequestSID.TransferData

    def test_response_sid(self):
        assert TRANSFER_DATA.response_sid == ResponseSID.TransferData


@pytest.mark.integration
class TestTransferDataIntegration:
    """Integration tests for `TransferData` service."""

    @pytest.mark.parametrize("payload, decoded_message", [
        (
            [0x36, 0x01],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'TransferData',
                    'raw_value': 0x36,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'blockSequenceCounter',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': None
                },
            )
        ),
        (
            [0x36, 0xFF, 0xBF, 0xD1, 0x84, 0x1D, 0xE4, 0x9A, 0xFB, 0xDA, 0xD7, 0x13, 0x54, 0x3C, 0xDC, 0x2C],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'TransferData',
                    'raw_value': 0x36,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'blockSequenceCounter',
                    'physical_value': 0xFF,
                    'raw_value': 0xFF,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'transferRequestParameter',
                    'physical_value': (0xBF, 0xD1, 0x84, 0x1D, 0xE4, 0x9A, 0xFB, 0xDA, 0xD7, 0x13, 0x54, 0x3C, 0xDC, 0x2C),
                    'raw_value': (0xBF, 0xD1, 0x84, 0x1D, 0xE4, 0x9A, 0xFB, 0xDA, 0xD7, 0x13, 0x54, 0x3C, 0xDC, 0x2C),
                    'unit': None
                },
            )
        ),
        (
            [0x76, 0x00],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'TransferData',
                    'raw_value': 0x76,
                    'unit': None
                },                {
                    'children': (),
                    'length': 8,
                    'name': 'blockSequenceCounter',
                    'physical_value': 0x00,
                    'raw_value': 0x00,
                    'unit': None
                },
            )
        ),
        (
            [0x76, 0x5F, 0x6D],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'TransferData',
                    'raw_value': 0x76,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'blockSequenceCounter',
                    'physical_value': 0x5F,
                    'raw_value': 0x5F,
                    'unit': None
                },
                {
                    'children': ((),),
                    'length': 8,
                    'name': 'transferResponseParameter',
                    'physical_value': (0x6D,),
                    'raw_value': (0x6D,),
                    'unit': None
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert TRANSFER_DATA.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        (
            {
                "blockSequenceCounter": 0x00,
            },
            RequestSID.TransferData,
            None,
            bytearray([0x36, 0x00])
        ),
        (
            {
                "blockSequenceCounter": 0x92,
                "transferRequestParameter": (0x88, 0x26, 0x62, 0x63, 0x01, 0x58, 0x52, 0x90, 0x1E, 0xD5, 0xEE, 0x63,
                                             0xBC, 0xED, 0x30, 0xD0, 0x71, 0x63),
            },
            RequestSID.TransferData,
            None,
            bytearray([0x36, 0x92, 0x88, 0x26, 0x62, 0x63, 0x01, 0x58, 0x52, 0x90, 0x1E, 0xD5, 0xEE, 0x63, 0xBC, 0xED,
                       0x30, 0xD0, 0x71, 0x63])
        ),
        (
            {
                "blockSequenceCounter": 0x20,
            },
            None,
            ResponseSID.TransferData,
            bytearray([0x76, 0x20])
        ),
        (
            {
                "blockSequenceCounter": 0xFF,
                "transferResponseParameter": (0xCB, 0x9F, 0xDE, 0xB8, 0xA0, 0x76, 0x5B, 0x6D),
            },
            None,
            ResponseSID.TransferData,
            bytearray([0x76, 0xFF, 0xCB, 0x9F, 0xDE, 0xB8, 0xA0, 0x76, 0x5B, 0x6D])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert TRANSFER_DATA.encode(data_records_values=data_records_values,
                                      sid=sid,
                                      rsid=rsid) == payload

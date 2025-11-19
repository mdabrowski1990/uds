import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.request_transfer_exit import REQUEST_TRANSFER_EXIT


class TestRequestTransferExit:
    """Unit tests for `RequestTransferExit` service."""

    def test_request_sid(self):
        assert REQUEST_TRANSFER_EXIT.request_sid == RequestSID.RequestTransferExit

    def test_response_sid(self):
        assert REQUEST_TRANSFER_EXIT.response_sid == ResponseSID.RequestTransferExit


@pytest.mark.integration
class TestRequestTransferExitIntegration:
    """Integration tests for `RequestTransferExit` service."""

    @pytest.mark.parametrize("payload, decoded_message", [
        (
            [0x37],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'RequestTransferExit',
                    'raw_value': 0x37,
                    'unit': None
                },
            )
        ),
        (
            [0x37, 0xBF, 0xD1, 0x84],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'RequestTransferExit',
                    'raw_value': 0x37,
                    'unit': None
                },
                {
                    'children': ((), (), ()),
                    'length': 8,
                    'name': 'transferRequestParameter',
                    'physical_value': (0xBF, 0xD1, 0x84),
                    'raw_value': (0xBF, 0xD1, 0x84),
                    'unit': None
                },
            )
        ),
        (
            [0x77],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'RequestTransferExit',
                    'raw_value': 0x77,
                    'unit': None
                },
            )
        ),
        (
            [0x77, 0xFF],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'RequestTransferExit',
                    'raw_value': 0x77,
                    'unit': None
                },
                {
                    'children': ((),),
                    'length': 8,
                    'name': 'transferResponseParameter',
                    'physical_value': (0xFF,),
                    'raw_value': (0xFF,),
                    'unit': None
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert REQUEST_TRANSFER_EXIT.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        (
            {},
            RequestSID.RequestTransferExit,
            None,
            bytearray([0x37])
        ),
        (
            {
                "transferRequestParameter": (0x00,),
            },
            RequestSID.RequestTransferExit,
            None,
            bytearray([0x37, 0x00])
        ),
        (
            {},
            None,
            ResponseSID.RequestTransferExit,
            bytearray([0x77])
        ),
        (
            {
                "transferResponseParameter": (0x00, 0x69, 0xBF, 0x0E, 0x7B, 0xEF, 0x08, 0x01, 0x29, 0xDC, 0x85),
            },
            None,
            ResponseSID.RequestTransferExit,
            bytearray([0x77, 0x00, 0x69, 0xBF, 0x0E, 0x7B, 0xEF, 0x08, 0x01, 0x29, 0xDC, 0x85])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert REQUEST_TRANSFER_EXIT.encode(data_records_values=data_records_values,
                                            sid=sid,
                                            rsid=rsid) == payload

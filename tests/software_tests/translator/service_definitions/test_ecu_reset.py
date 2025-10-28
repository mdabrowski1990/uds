import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.ecu_reset import ECU_RESET


class TestECUReset:
    """Unit tests for `ECUReset` service."""

    def test_request_sid(self):
        assert ECU_RESET.request_sid == RequestSID.ECUReset

    def test_response_sid(self):
        assert ECU_RESET.response_sid == ResponseSID.ECUReset


@pytest.mark.integration
class TestECUResetIntegration:
    """Integration tests for `ECUReset` service."""

    @pytest.mark.parametrize("payload, decoded_message", [
        (
            [0x11, 0x81],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'ECUReset',
                    'raw_value': 0x11,
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
                            'name': 'resetType',
                            'physical_value': 'hardReset',
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
            )
        ),
        (
            [0x51, 0x04, 0xFF],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'ECUReset',
                    'raw_value': 0x51,
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
                            'name': 'resetType',
                            'physical_value': 'enableRapidPowerShutDown',
                            'raw_value': 0x04,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 4,
                    'raw_value': 0x04,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'powerDownTime',
                    'physical_value': 'failure or time unavailable',
                    'raw_value': 0xFF,
                    'unit': 's'
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert ECU_RESET.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": True,
                    "resetType": 0x02
                }
            },
            RequestSID.ECUReset,
            None,
            bytearray([0x11, 0x82])
        ),
        (
            {
                "SubFunction": 0x04,
                "powerDownTime": 0x5A,
            },
            None,
            ResponseSID.ECUReset,
            bytearray([0x51, 0x04, 0x5A])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert ECU_RESET.encode(data_records_values=data_records_values,
                                sid=sid,
                                rsid=rsid) == payload

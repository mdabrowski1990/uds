import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.ecu_reset import ECU_RESET, ECU_RESET_2013, ECU_RESET_2020


class TestECUReset:
    """Unit tests for `ECUReset` service."""

    def test_request_sid(self):
        assert ECU_RESET_2013.request_sid == RequestSID.ECUReset
        assert ECU_RESET_2020.request_sid == RequestSID.ECUReset

    def test_response_sid(self):
        assert ECU_RESET_2013.response_sid == ResponseSID.ECUReset
        assert ECU_RESET_2020.response_sid == ResponseSID.ECUReset

    def test_default_translator(self):
        assert ECU_RESET is ECU_RESET_2020


@pytest.mark.integration
class TestECUReset2013Integration:
    """Integration tests for `ECUReset` service version 2013."""

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
            [0x51, 0x04],
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
                            'physical_value': 0x04,
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
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert ECU_RESET_2013.decode(payload) == decoded_message

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
            },
            None,
            ResponseSID.ECUReset,
            bytearray([0x51, 0x04])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert ECU_RESET_2013.encode(data_records_values=data_records_values,
                                     sid=sid,
                                     rsid=rsid) == payload


@pytest.mark.integration
class TestECUReset2020Integration:
    """Integration tests for `ECUReset` service version 2020."""

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
                    'physical_value': 'ERROR',
                    'raw_value': 0xFF,
                    'unit': 's'
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert ECU_RESET_2020.decode(payload) == decoded_message

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
        assert ECU_RESET_2020.encode(data_records_values=data_records_values,
                                     sid=sid,
                                     rsid=rsid) == payload

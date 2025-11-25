import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.control_dtc_setting import CONTROL_DTC_SETTING


class TestControlDTCSetting:
    """Unit tests for `ControlDTCSetting` service."""

    def test_request_sid(self):
        assert CONTROL_DTC_SETTING.request_sid == RequestSID.ControlDTCSetting

    def test_response_sid(self):
        assert CONTROL_DTC_SETTING.response_sid == ResponseSID.ControlDTCSetting


@pytest.mark.integration
class TestControlDTCSettingIntegration:
    """Integration tests for `ControlDTCSetting` service."""

    @pytest.mark.parametrize("payload, decoded_message", [
        (
            [0x85, 0x01],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'ControlDTCSetting',
                    'raw_value': 0x85,
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
                            'name': 'DTCSettingType',
                            'physical_value': 'on',
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
            )
        ),
        (
            [0x85, 0xC0, 0x7D, 0x9D, 0xA8, 0x9B, 0x15, 0x8D, 0xAE, 0x10, 0x2C, 0xBA, 0x0F],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'ControlDTCSetting',
                    'raw_value': 0x85,
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
                            'name': 'DTCSettingType',
                            'physical_value': 0x40,
                            'raw_value': 0x40,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0xC0,
                    'raw_value': 0xC0,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (),),
                    'length': 8,
                    'name': 'DTCSettingControlOptionRecord',
                    'physical_value': (0x7D, 0x9D, 0xA8, 0x9B, 0x15, 0x8D, 0xAE, 0x10, 0x2C, 0xBA, 0x0F),
                    'raw_value': (0x7D, 0x9D, 0xA8, 0x9B, 0x15, 0x8D, 0xAE, 0x10, 0x2C, 0xBA, 0x0F),
                    'unit': None
                },
            )
        ),
        (
            [0xC5, 0x02],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'ControlDTCSetting',
                    'raw_value': 0xC5,
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
                            'name': 'DTCSettingType',
                            'physical_value': 'off',
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
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert CONTROL_DTC_SETTING.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": True,
                    "DTCSettingType": 0x02
                }
            },
            RequestSID.ControlDTCSetting,
            None,
            bytearray([0x85, 0x82])
        ),
        (
            {
                "SubFunction": 0x01,
                "DTCSettingControlOptionRecord": [0x00],
            },
            RequestSID.ControlDTCSetting,
            None,
            bytearray([0x85, 0x01, 0x00])
        ),
        (
            {
                "SubFunction": 0x5A,
            },
            None,
            ResponseSID.ControlDTCSetting,
            bytearray([0xC5, 0x5A])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert CONTROL_DTC_SETTING.encode(data_records_values=data_records_values,
                                                 sid=sid,
                                                 rsid=rsid) == payload

import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.link_control import LINK_CONTROL


class TestLinkControl:
    """Unit tests for `LinkControl` service."""

    def test_request_sid(self):
        assert LINK_CONTROL.request_sid == RequestSID.LinkControl

    def test_response_sid(self):
        assert LINK_CONTROL.response_sid == ResponseSID.LinkControl


@pytest.mark.integration
class TestLinkControlIntegration:
    """Integration tests for `LinkControl` service."""

    @pytest.mark.parametrize("payload, decoded_message", [
        # verifyModeTransitionWithFixedParameter (0x01)
        (
            [0x87, 0x01, 0x11],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'LinkControl',
                    'raw_value': 0x87,
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
                            'name': 'linkControlType',
                            'physical_value': 'verifyModeTransitionWithFixedParameter',
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
                    'name': 'linkControlModeIdentifier',
                    'physical_value': 'CAN250000Baud',
                    'raw_value': 0x11,
                    'unit': None
                },
            )
        ),
        (
            [0xC7, 0x81],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'LinkControl',
                    'raw_value': 0xC7,
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
                            'name': 'linkControlType',
                            'physical_value': 'verifyModeTransitionWithFixedParameter',
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
        # verifyModeTransitionWithSpecificParameter (0x02)
        (
            [0x87, 0x82, 0xF0, 0xE1, 0xD2],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'LinkControl',
                    'raw_value': 0x87,
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
                            'name': 'linkControlType',
                            'physical_value': 'verifyModeTransitionWithSpecificParameter',
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
                    'length': 24,
                    'name': 'linkRecord',
                    'physical_value': 0xF0E1D2,
                    'raw_value': 0xF0E1D2,
                    'unit': None
                },
            )
        ),
        (
            [0xC7, 0x02],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'LinkControl',
                    'raw_value': 0xC7,
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
                            'name': 'linkControlType',
                            'physical_value': 'verifyModeTransitionWithSpecificParameter',
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
        # transitionMode (0x03)
        (
            [0x87, 0x03],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'LinkControl',
                    'raw_value': 0x87,
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
                            'name': 'linkControlType',
                            'physical_value': 'transitionMode',
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
            )
        ),
        (
            [0xC7, 0x83],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'LinkControl',
                    'raw_value': 0xC7,
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
                            'name': 'linkControlType',
                            'physical_value': 'transitionMode',
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
        assert LINK_CONTROL.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        # verifyModeTransitionWithFixedParameter (0x01)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": True,
                    "linkControlType": 0x01
                },
                "linkControlModeIdentifier": 0x00
            },
            RequestSID.LinkControl,
            None,
            bytearray([0x87, 0x81, 0x00])
        ),
        (
            {
                "SubFunction": 0x01,
            },
            None,
            ResponseSID.LinkControl,
            bytearray([0xC7, 0x01])
        ),
        # verifyModeTransitionWithSpecificParameter (0x02)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": False,
                    "linkControlType": 0x02
                },
                "linkRecord": 0x012345
            },
            RequestSID.LinkControl,
            None,
            bytearray([0x87, 0x02, 0x01, 0x23, 0x45])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": True,
                    "linkControlType": 0x02
                },
            },
            None,
            ResponseSID.LinkControl,
            bytearray([0xC7, 0x82])
        ),
        # transitionMode (0x03)
        (
            {
                "SubFunction": 0x83,
            },
            RequestSID.LinkControl,
            None,
            bytearray([0x87, 0x83])
        ),
        (
            {
                "SubFunction": 0x03,
            },
            None,
            ResponseSID.LinkControl,
            bytearray([0xC7, 0x03])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert LINK_CONTROL.encode(data_records_values=data_records_values,
                                                 sid=sid,
                                                 rsid=rsid) == payload

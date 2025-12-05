import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.response_on_event import (
    RESPONSE_ON_EVENT,
    RESPONSE_ON_EVENT_2013,
    RESPONSE_ON_EVENT_2020,
)


class TestResponseOnEvent:
    """Unit tests for `ResponseOnEvent` service."""

    def test_request_sid(self):
        assert RESPONSE_ON_EVENT_2013.request_sid == RequestSID.ResponseOnEvent
        assert RESPONSE_ON_EVENT_2020.request_sid == RequestSID.ResponseOnEvent

    def test_response_sid(self):
        assert RESPONSE_ON_EVENT_2013.response_sid == ResponseSID.ResponseOnEvent
        assert RESPONSE_ON_EVENT_2020.response_sid == ResponseSID.ResponseOnEvent

    def test_default_translator(self):
        assert RESPONSE_ON_EVENT is RESPONSE_ON_EVENT_2020


@pytest.mark.integration
class TestResponseOnEvent2013Integration:
    """Integration tests for `ResponseOnEvent` service version 2013."""

    @pytest.mark.parametrize("payload, decoded_message", [
        # stopResponseOnEvent (0x00)
        (
            [0x86, 0x00, 0x03],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'ResponseOnEvent',
                    'raw_value': 0x86,
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
                            'children': (
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': "storageState",
                                    'physical_value': 'doNotStoreEvent',
                                    'raw_value': 0,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 6,
                                    'name': "event",
                                    'physical_value': 'stopResponseOnEvent',
                                    'raw_value': 0x00,
                                    'unit': None
                                },
                            ),
                            'length': 7,
                            'name': "eventType",
                            'physical_value': 0x00,
                            'raw_value': 0x00,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x00,
                    'raw_value': 0x00,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'eventWindowTime',
                    'physical_value': 0x03,
                    'raw_value': 0x03,
                    'unit': None
                }
            )
        ),
        (
            [0xC6, 0xC0, 0xFF, 0x00],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'ResponseOnEvent',
                    'raw_value': 0xC6,
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
                            'children': (
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': "storageState",
                                    'physical_value': 'storeEvent',
                                    'raw_value': 1,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 6,
                                    'name': "event",
                                    'physical_value': 'stopResponseOnEvent',
                                    'raw_value': 0x00,
                                    'unit': None
                                },
                            ),
                            'length': 7,
                            'name': "eventType",
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
                    'children': (),
                    'length': 8,
                    'name': 'numberOfIdentifiedEvents',
                    'physical_value': 0xFF,
                    'raw_value': 0xFF,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'eventWindowTime',
                    'physical_value': 0x00,
                    'raw_value': 0x00,
                    'unit': None
                },
            ),
        ),
        # onDTCStatusChange (0x01)
        # onTimerInterrupt (0x02)
        # onChangeOfDataIdentifier (0x03)
        # reportActivatedEvents (0x04)
        # startResponseOnEvent (0x05)
        # clearResponseOnEvent (0x06)
        # onComparisonOfValues (0x07)
    ])
    def test_decode(self, payload, decoded_message):
        assert RESPONSE_ON_EVENT_2013.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        # stopResponseOnEvent (0x00)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": True,
                    "eventType": {
                        "storageState": False,
                        "event": 0x00,
                    },
                },
                "eventWindowTime": 0x2D,
            },
            RequestSID.ResponseOnEvent,
            None,
            bytearray([0x86, 0x80, 0x2D])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": False,
                    "eventType": {
                        "storageState": True,
                        "event": 0x00,
                    },
                },
                "numberOfIdentifiedEvents": 0x01,
                "eventWindowTime": 0x8C,
            },
            None,
            ResponseSID.ResponseOnEvent,
            bytearray([0xC6, 0x40, 0x01, 0x8C])
        ),
        # onDTCStatusChange (0x01)
        # onTimerInterrupt (0x02)
        # onChangeOfDataIdentifier (0x03)
        # reportActivatedEvents (0x04)
        # startResponseOnEvent (0x05)
        # clearResponseOnEvent (0x06)
        # onComparisonOfValues (0x07)
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert RESPONSE_ON_EVENT_2013.encode(data_records_values=data_records_values,
                                                sid=sid,
                                                rsid=rsid) == payload


@pytest.mark.integration
class TestResponseOnEvent2020Integration:
    """Integration tests for `ResponseOnEvent` service version 2020."""

    @pytest.mark.parametrize("payload, decoded_message", [
        # TODO
    ])
    def test_decode(self, payload, decoded_message):
        assert RESPONSE_ON_EVENT_2020.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        # TODO
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert RESPONSE_ON_EVENT_2020.encode(data_records_values=data_records_values,
                                                sid=sid,
                                                rsid=rsid) == payload

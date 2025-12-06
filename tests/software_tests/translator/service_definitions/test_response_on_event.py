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
        (
            [0x86, 0x81, 0x02, 0xFF, 0x19, 0x02, 0xFF],
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
                                    'physical_value': 'doNotStoreEvent',
                                    'raw_value': 0,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 6,
                                    'name': "event",
                                    'physical_value': 'onDTCStatusChange',
                                    'raw_value': 0x01,
                                    'unit': None
                                },
                            ),
                            'length': 7,
                            'name': "eventType",
                            'physical_value': 0x01,
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
                    'length': 8,
                    'name': 'eventWindowTime',
                    'physical_value': "infiniteTimeToResponse",
                    'raw_value': 0x02,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'warningIndicatorRequested',
                                    'physical_value': 'yes',
                                    'raw_value': 1,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'testNotCompletedThisOperationCycle',
                                    'physical_value': 'yes',
                                    'raw_value': 1,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'testFailedSinceLastClear',
                                    'physical_value': 'yes',
                                    'raw_value': 1,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'testNotCompletedSinceLastClear',
                                    'physical_value': 'yes',
                                    'raw_value': 1,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'confirmedDTC',
                                    'physical_value': 'yes',
                                    'raw_value': 1,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'pendingDTC',
                                    'physical_value': 'yes',
                                    'raw_value': 1,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'testFailedThisOperationCycle',
                                    'physical_value': 'yes',
                                    'raw_value': 1,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'testFailed',
                                    'physical_value': 'yes',
                                    'raw_value': 1,
                                    'unit': None
                                },
                            ),
                            'length': 8,
                            'name': 'DTCStatusMask',
                            'physical_value': 0xFF,
                            'raw_value': 0xFF,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'eventTypeRecord',
                    'physical_value': 0xFF,
                    'raw_value': 0xFF,
                    'unit': None
                },
                {
                    'children': ((), (), ()),
                    'length': 8,
                    'name': 'serviceToRespondToRecord',
                    'physical_value': (0x19, 0x02, 0xFF),
                    'raw_value': (0x19, 0x02, 0xFF),
                    'unit': None
                }
            )
        ),
        (
            [0xC6, 0x41, 0x01, 0x2C, 0x5A, 0x22, 0x01, 0x00, 0x01, 0x01],
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
                                    'physical_value': 'storeEvent',
                                    'raw_value': 1,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 6,
                                    'name': "event",
                                    'physical_value': 'onDTCStatusChange',
                                    'raw_value': 0x01,
                                    'unit': None
                                },
                            ),
                            'length': 7,
                            'name': "eventType",
                            'physical_value': 0x41,
                            'raw_value': 0x41,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x41,
                    'raw_value': 0x41,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'numberOfIdentifiedEvents',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'eventWindowTime',
                    'physical_value': 0x2C,
                    'raw_value': 0x2C,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'warningIndicatorRequested',
                                    'physical_value': 'no',
                                    'raw_value': 0,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'testNotCompletedThisOperationCycle',
                                    'physical_value': 'yes',
                                    'raw_value': 1,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'testFailedSinceLastClear',
                                    'physical_value': 'no',
                                    'raw_value': 0,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'testNotCompletedSinceLastClear',
                                    'physical_value': 'yes',
                                    'raw_value': 1,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'confirmedDTC',
                                    'physical_value': 'yes',
                                    'raw_value': 1,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'pendingDTC',
                                    'physical_value': 'no',
                                    'raw_value': 0,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'testFailedThisOperationCycle',
                                    'physical_value': 'yes',
                                    'raw_value': 1,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'testFailed',
                                    'physical_value': 'no',
                                    'raw_value': 0,
                                    'unit': None
                                },
                            ),
                            'length': 8,
                            'name': 'DTCStatusMask',
                            'physical_value': 0x5A,
                            'raw_value': 0x5A,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'eventTypeRecord',
                    'physical_value': 0x5A,
                    'raw_value': 0x5A,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), ()),
                    'length': 8,
                    'name': 'serviceToRespondToRecord',
                    'physical_value': (0x22, 0x01, 0x00, 0x01, 0x01),
                    'raw_value': (0x22, 0x01, 0x00, 0x01, 0x01),
                    'unit': None
                }
            ),
        ),
        # onTimerInterrupt (0x02)
        (
            [0x86, 0x42, 0x6E, 0x03, 0x19, 0x04, 0x12, 0x34, 0x56, 0x78],
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
                                    'physical_value': 'storeEvent',
                                    'raw_value': 1,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 6,
                                    'name': "event",
                                    'physical_value': 'onTimerInterrupt',
                                    'raw_value': 0x02,
                                    'unit': None
                                },
                            ),
                            'length': 7,
                            'name': "eventType",
                            'physical_value': 0x42,
                            'raw_value': 0x42,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x42,
                    'raw_value': 0x42,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'eventWindowTime',
                    'physical_value': 0x6E,
                    'raw_value': 0x6E,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 8,
                            'name': 'Timer schedule',
                            'physical_value': "Fast rate",
                            'raw_value': 0x03,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'eventTypeRecord',
                    'physical_value': 0x03,
                    'raw_value': 0x03,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), ()),
                    'length': 8,
                    'name': 'serviceToRespondToRecord',
                    'physical_value': (0x19, 0x04, 0x12, 0x34, 0x56, 0x78),
                    'raw_value': (0x19, 0x04, 0x12, 0x34, 0x56, 0x78),
                    'unit': None
                }
            )
        ),
        (
            [0xC6, 0x82, 0x01, 0x90, 0x01, 0x50],
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
                                    'physical_value': 'doNotStoreEvent',
                                    'raw_value': 0,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 6,
                                    'name': "event",
                                    'physical_value': 'onTimerInterrupt',
                                    'raw_value': 0x02,
                                    'unit': None
                                },
                            ),
                            'length': 7,
                            'name': "eventType",
                            'physical_value': 0x02,
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
                    'length': 8,
                    'name': 'numberOfIdentifiedEvents',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'eventWindowTime',
                    'physical_value': 0x90,
                    'raw_value': 0x90,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 8,
                            'name': 'Timer schedule',
                            'physical_value': "Slow rate",
                            'raw_value': 0x01,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'eventTypeRecord',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': None
                },
                {
                    'children': ((),),
                    'length': 8,
                    'name': 'serviceToRespondToRecord',
                    'physical_value': (0x50,),
                    'raw_value': (0x50,),
                    'unit': None
                }
            ),
        ),
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
        (
            {
                "SubFunction": 0x41,
                "eventWindowTime": 0xBE,
                "eventTypeRecord": {
                    "DTCStatusMask": {
                        "warningIndicatorRequested": True,
                        "testNotCompletedThisOperationCycle": True,
                        "testFailedSinceLastClear": False,
                        "testNotCompletedSinceLastClear": True,
                        "confirmedDTC": True,
                        "pendingDTC": True,
                        "testFailedThisOperationCycle": False,
                        "testFailed": False,
                    },
                },
                "serviceToRespondToRecord": (0x00,),
            },
            RequestSID.ResponseOnEvent,
            None,
            bytearray([0x86, 0x41, 0xBE, 0xDC, 0x00])
        ),
        (
            {
                "SubFunction": 0x81,
                "numberOfIdentifiedEvents": 0x05,
                "eventWindowTime": 0x00,
                "eventTypeRecord": 0x1F,
                "serviceToRespondToRecord": (0xFF, 0xED, 0xCB, 0xA9, 0x87, 0x65, 0x43, 0x21, 0x00),
            },
            None,
            ResponseSID.ResponseOnEvent,
            bytearray([0xC6, 0x81, 0x05, 0x00, 0x1F, 0xFF, 0xED, 0xCB, 0xA9, 0x87, 0x65, 0x43, 0x21, 0x00])
        ),
        # onTimerInterrupt (0x02)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": True,
                    "eventType": 0x02,
                },
                "eventWindowTime": 0xDD,
                "eventTypeRecord": 0xFF,
                "serviceToRespondToRecord": (0xFF,),
            },
            RequestSID.ResponseOnEvent,
            None,
            bytearray([0x86, 0x82, 0xDD, 0xFF, 0xFF])
        ),
        (
            {
                "SubFunction": 0x02,
                "numberOfIdentifiedEvents": 0x0F,
                "eventWindowTime": 0xC1,
                "eventTypeRecord": {
                    "Timer schedule": 0x6E,
                },
                "serviceToRespondToRecord": (0xB5, 0x8F, 0x1A, 0x79, 0xD2, 0x43, 0x41, 0x54, 0x7D, 0x6C, 0x57),
            },
            None,
            ResponseSID.ResponseOnEvent,
            bytearray([0xC6, 0x02, 0x0F, 0xC1, 0x6E, 0xB5, 0x8F, 0x1A, 0x79, 0xD2, 0x43, 0x41, 0x54, 0x7D, 0x6C, 0x57])
        ),
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

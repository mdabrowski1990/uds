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
        (
            [0x86, 0xC3, 0x01, 0xFF, 0x01, 0x23, 0x11, 0x23, 0x45],
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
                                    'physical_value': 'storeEvent',
                                    'raw_value': 1,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 6,
                                    'name': "event",
                                    'physical_value': 'onChangeOfDataIdentifier',
                                    'raw_value': 0x03,
                                    'unit': None
                                },
                            ),
                            'length': 7,
                            'name': "eventType",
                            'physical_value': 0x43,
                            'raw_value': 0x43,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0xC3,
                    'raw_value': 0xC3,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'eventWindowTime',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 16,
                            'name': 'DID',
                            'physical_value': 0xFF01,
                            'raw_value': 0xFF01,
                            'unit': None
                        },
                    ),
                    'length': 16,
                    'name': 'eventTypeRecord',
                    'physical_value': 0xFF01,
                    'raw_value': 0xFF01,
                    'unit': None
                },
                {
                    'children': ((), (), (), ()),
                    'length': 8,
                    'name': 'serviceToRespondToRecord',
                    'physical_value': (0x23, 0x11, 0x23, 0x45),
                    'raw_value': (0x23, 0x11, 0x23, 0x45),
                    'unit': None
                }
            )
        ),
        (
            [0xC6, 0x03, 0x10, 0x03, 0xF1, 0x8A, 0x10, 0x03],
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
                                    'physical_value': 'doNotStoreEvent',
                                    'raw_value': 0,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 6,
                                    'name': "event",
                                    'physical_value': 'onChangeOfDataIdentifier',
                                    'raw_value': 0x03,
                                    'unit': None
                                },
                            ),
                            'length': 7,
                            'name': "eventType",
                            'physical_value': 0x03,
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
                {
                    'children': (),
                    'length': 8,
                    'name': 'numberOfIdentifiedEvents',
                    'physical_value': 0x10,
                    'raw_value': 0x10,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'eventWindowTime',
                    'physical_value': 0x03,
                    'raw_value': 0x03,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 16,
                            'name': 'DID',
                            'physical_value': "systemSupplierIdentifierDataIdentifier",
                            'raw_value': 0xF18A,
                            'unit': None
                        },
                    ),
                    'length': 16,
                    'name': 'eventTypeRecord',
                    'physical_value': 0xF18A,
                    'raw_value': 0xF18A,
                    'unit': None
                },
                {
                    'children': ((), ()),
                    'length': 8,
                    'name': 'serviceToRespondToRecord',
                    'physical_value': (0x10, 0x03),
                    'raw_value': (0x10, 0x03),
                    'unit': None
                }
            ),
        ),
        # reportActivatedEvents (0x04)
        (
            [0x86, 0x04, 0x06],
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
                                    'physical_value': 'reportActivatedEvents',
                                    'raw_value': 0x04,
                                    'unit': None
                                },
                            ),
                            'length': 7,
                            'name': "eventType",
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
                {
                    'children': (),
                    'length': 8,
                    'name': 'eventWindowTime',
                    'physical_value': 0x06,
                    'raw_value': 0x06,
                    'unit': None
                },
            )
        ),
        (
            [0xC6, 0x84, 0x01, 0x01, 0x00, 0xFF, 0x00],
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
                                    'physical_value': 'reportActivatedEvents',
                                    'raw_value': 0x04,
                                    'unit': None
                                },
                            ),
                            'length': 7,
                            'name': "eventType",
                            'physical_value': 0x04,
                            'raw_value': 0x04,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x84,
                    'raw_value': 0x84,
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
                            'children': (
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'storageState',
                                    'physical_value': 'doNotStoreEvent',
                                    'raw_value': 0,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 6,
                                    'name': 'event',
                                    'physical_value': 'onDTCStatusChange',
                                    'raw_value': 0x01,
                                    'unit': None
                                }
                            ),
                            'length': 7,
                            'name': 'eventType',
                            'physical_value': 0x01,
                            'raw_value': 0x01,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'eventTypeOfActiveEvent#1',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'eventWindowTime#1',
                    'physical_value': 0x00,
                    'raw_value': 0x00,
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
                                }
                            ),
                            'length': 8,
                            'name': 'DTCStatusMask',
                            'physical_value': 0xFF,
                            'raw_value': 0xFF,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'eventTypeRecord#1',
                    'physical_value': 0xFF,
                    'raw_value': 0xFF,
                    'unit': None
                },
                {
                    'children': ((),),
                    'length': 8,
                    'name': 'serviceToRespondToRecord#1',
                    'physical_value': (0x00,),
                    'raw_value': (0x00,),
                    'unit': None
                },
            ),
        ),
        (
            [0xC6, 0x04, 0x01, 0x42, 0x02, 0x02, 0x7B, 0x64, 0x4F, 0x43, 0x21, 0x27, 0xB0, 0xE9],
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
                                    'physical_value': 'doNotStoreEvent',
                                    'raw_value': 0,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 6,
                                    'name': "event",
                                    'physical_value': 'reportActivatedEvents',
                                    'raw_value': 0x04,
                                    'unit': None
                                },
                            ),
                            'length': 7,
                            'name': "eventType",
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
                {
                    'children': (),
                    'length': 8,
                    'name': 'numberOfIdentifiedEvents',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
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
                            'children': (
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'storageState',
                                    'physical_value': 'storeEvent',
                                    'raw_value': 1,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 6,
                                    'name': 'event',
                                    'physical_value': 'onTimerInterrupt',
                                    'raw_value': 0x02,
                                    'unit': None
                                }
                            ),
                            'length': 7,
                            'name': 'eventType',
                            'physical_value': 0x42,
                            'raw_value': 0x42,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'eventTypeOfActiveEvent#1',
                    'physical_value': 0x42,
                    'raw_value': 0x42,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'eventWindowTime#1',
                    'physical_value': "infiniteTimeToResponse",
                    'raw_value': 0x02,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 8,
                            'name': 'Timer schedule',
                            'physical_value': "Medium rate",
                            'raw_value': 0x02,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'eventTypeRecord#1',
                    'physical_value': 0x02,
                    'raw_value': 0x02,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'serviceToRespondToRecord#1',
                    'physical_value': (0x7B, 0x64, 0x4F, 0x43, 0x21, 0x27, 0xB0, 0xE9),
                    'raw_value': (0x7B, 0x64, 0x4F, 0x43, 0x21, 0x27, 0xB0, 0xE9),
                    'unit': None
                },
            ),
        ),
        (
            [0xC6, 0x44, 0x01, 0x03, 0x01, 0xF1, 0x80, 0x80, 0xC5, 0x79, 0x69, 0xBA, 0xFC, 0x90],
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
                                    'physical_value': 'reportActivatedEvents',
                                    'raw_value': 0x04,
                                    'unit': None
                                },
                            ),
                            'length': 7,
                            'name': "eventType",
                            'physical_value': 0x44,
                            'raw_value': 0x44,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x44,
                    'raw_value': 0x44,
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
                            'children': (
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'storageState',
                                    'physical_value': 'doNotStoreEvent',
                                    'raw_value': 0,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 6,
                                    'name': 'event',
                                    'physical_value': 'onChangeOfDataIdentifier',
                                    'raw_value': 0x03,
                                    'unit': None
                                }
                            ),
                            'length': 7,
                            'name': 'eventType',
                            'physical_value': 0x03,
                            'raw_value': 0x03,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'eventTypeOfActiveEvent#1',
                    'physical_value': 0x03,
                    'raw_value': 0x03,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'eventWindowTime#1',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 16,
                            'name': 'DID',
                            'physical_value': "BootSoftwareIdentificationDataIdentifier",
                            'raw_value': 0xF180,
                            'unit': None
                        },
                    ),
                    'length': 16,
                    'name': 'eventTypeRecord#1',
                    'physical_value': 0xF180,
                    'raw_value': 0xF180,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'serviceToRespondToRecord#1',
                    'physical_value': (0x80, 0xC5, 0x79, 0x69, 0xBA, 0xFC, 0x90),
                    'raw_value': (0x80, 0xC5, 0x79, 0x69, 0xBA, 0xFC, 0x90),
                    'unit': None
                },
            ),
        ),
        (
            [0xC6, 0x44, 0x01,
             0x47, 0x04, 0x01, 0x00, 0x04, 0xE9, 0x6B, 0x06, 0xBB, 0x7F, 0x00, 0x08,
             0xBB, 0x4F, 0xF2, 0xFE],
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
                                    'physical_value': 'reportActivatedEvents',
                                    'raw_value': 0x04,
                                    'unit': None
                                },
                            ),
                            'length': 7,
                            'name': "eventType",
                            'physical_value': 0x44,
                            'raw_value': 0x44,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x44,
                    'raw_value': 0x44,
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
                            'children': (
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'storageState',
                                    'physical_value': 'storeEvent',
                                    'raw_value': 1,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 6,
                                    'name': 'event',
                                    'physical_value': 'onComparisonOfValues',
                                    'raw_value': 0x07,
                                    'unit': None
                                }
                            ),
                            'length': 7,
                            'name': 'eventType',
                            'physical_value': 0x47,
                            'raw_value': 0x47,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'eventTypeOfActiveEvent#1',
                    'physical_value': 0x47,
                    'raw_value': 0x47,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'eventWindowTime#1',
                    'physical_value': 0x04,
                    'raw_value': 0x04,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 16,
                            'name': 'DID',
                            'physical_value': 0x0100,
                            'raw_value': 0x0100,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 8,
                            'name': 'Comparison logic',
                            'physical_value': "<>",
                            'raw_value': 0x04,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 32,
                            'name': 'Compare Value',
                            'physical_value': 0xE96B06BB,
                            'raw_value': 0xE96B06BB,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 8,
                            'name': 'Hysteresis Value',
                            'physical_value': 100 / 255 * 0x7F,
                            'raw_value': 0x7F,
                            'unit': "%"
                        },
                        {
                            'children': (
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'Compare Sign',
                                    'physical_value': "Comparison without sign",
                                    'raw_value': 0,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 5,
                                    'name': 'Bits Number',
                                    'physical_value': 32,
                                    'raw_value': 0x00,
                                    'unit': "bits"
                                },
                                {
                                    'children': (),
                                    'length': 10,
                                    'name': 'Bit Offset',
                                    'physical_value': 0x008,
                                    'raw_value': 0x008,
                                    'unit': "bits"
                                },
                            ),
                            'length': 16,
                            'name': 'Localization',
                            'physical_value': 0x0008,
                            'raw_value': 0x0008,
                            'unit': None
                        },
                    ),
                    'length': 80,
                    'name': 'eventTypeRecord#1',
                    'physical_value': 0x010004E96B06BB7F0008,
                    'raw_value': 0x010004E96B06BB7F0008,
                    'unit': None
                },
                {
                    'children': ((), (), (), ()),
                    'length': 8,
                    'name': 'serviceToRespondToRecord#1',
                    'physical_value': (0xBB, 0x4F, 0xF2, 0xFE),
                    'raw_value': (0xBB, 0x4F, 0xF2, 0xFE),
                    'unit': None
                },
            ),
        ),
        # startResponseOnEvent (0x05)
        (
            [0x86, 0x85, 0x07],
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
                                    'physical_value': 'startResponseOnEvent',
                                    'raw_value': 0x05,
                                    'unit': None
                                },
                            ),
                            'length': 7,
                            'name': "eventType",
                            'physical_value': 0x05,
                            'raw_value': 0x05,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x85,
                    'raw_value': 0x85,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'eventWindowTime',
                    'physical_value': 0x07,
                    'raw_value': 0x07,
                    'unit': None
                },
            )
        ),
        (
            [0xC6, 0x45, 0x00, 0x05],
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
                                    'physical_value': 'startResponseOnEvent',
                                    'raw_value': 0x05,
                                    'unit': None
                                },
                            ),
                            'length': 7,
                            'name': "eventType",
                            'physical_value': 0x45,
                            'raw_value': 0x45,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x45,
                    'raw_value': 0x45,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'numberOfIdentifiedEvents',
                    'physical_value': 0x00,
                    'raw_value': 0x00,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'eventWindowTime',
                    'physical_value': 0x05,
                    'raw_value': 0x05,
                    'unit': None
                },
            ),
        ),
        # clearResponseOnEvent (0x06)
        (
            [0x86, 0x06, 0x04],
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
                                    'physical_value': 'clearResponseOnEvent',
                                    'raw_value': 0x06,
                                    'unit': None
                                },
                            ),
                            'length': 7,
                            'name': "eventType",
                            'physical_value': 0x06,
                            'raw_value': 0x06,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x06,
                    'raw_value': 0x06,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'eventWindowTime',
                    'physical_value': 0x04,
                    'raw_value': 0x04,
                    'unit': None
                },
            )
        ),
        (
            [0xC6, 0xC6, 0x2A, 0x0A],
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
                                    'physical_value': 'clearResponseOnEvent',
                                    'raw_value': 0x06,
                                    'unit': None
                                },
                            ),
                            'length': 7,
                            'name': "eventType",
                            'physical_value': 0x46,
                            'raw_value': 0x46,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0xC6,
                    'raw_value': 0xC6,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'numberOfIdentifiedEvents',
                    'physical_value': 0x2A,
                    'raw_value': 0x2A,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'eventWindowTime',
                    'physical_value': 0x0A,
                    'raw_value': 0x0A,
                    'unit': None
                },
            ),
        ),
        # onComparisonOfValues (0x07)
        (
            [0x86, 0xC7, 0x2F, 0xF1, 0x9C, 0x03, 0xD4, 0xB3, 0xE2, 0xB8, 0x10, 0xC8, 0x00, 0x54],
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
                                    'physical_value': 'storeEvent',
                                    'raw_value': 1,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 6,
                                    'name': "event",
                                    'physical_value': 'onComparisonOfValues',
                                    'raw_value': 0x07,
                                    'unit': None
                                },
                            ),
                            'length': 7,
                            'name': "eventType",
                            'physical_value': 0x47,
                            'raw_value': 0x47,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0xC7,
                    'raw_value': 0xC7,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'eventWindowTime',
                    'physical_value': 0x2F,
                    'raw_value': 0x2F,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 16,
                            'name': 'DID',
                            'physical_value': "calibrationEquipmentSoftwareNumberDataIdentifier",
                            'raw_value': 0xF19C,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 8,
                            'name': 'Comparison logic',
                            'physical_value': "=",
                            'raw_value': 0x03,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 32,
                            'name': 'Compare Value',
                            'physical_value': 0xD4B3E2B8,
                            'raw_value': 0xD4B3E2B8,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 8,
                            'name': 'Hysteresis Value',
                            'physical_value': 100 / 255 * 0x10,
                            'raw_value': 0x10,
                            'unit': "%"
                        },
                        {
                            'children': (
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'Compare Sign',
                                    'physical_value': "Comparison with sign",
                                    'raw_value': 1,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 5,
                                    'name': 'Bits Number',
                                    'physical_value': 0x12,
                                    'raw_value': 0x12,
                                    'unit': "bits"
                                },
                                {
                                    'children': (),
                                    'length': 10,
                                    'name': 'Bit Offset',
                                    'physical_value': 0x000,
                                    'raw_value': 0x000,
                                    'unit': "bits"
                                },
                            ),
                            'length': 16,
                            'name': 'Localization',
                            'physical_value': 0xC800,
                            'raw_value': 0xC800,
                            'unit': None
                        },
                    ),
                    'length': 80,
                    'name': 'eventTypeRecord',
                    'physical_value': 0xF19C03D4B3E2B810C800,
                    'raw_value': 0xF19C03D4B3E2B810C800,
                    'unit': None
                },
                {
                    'children': ((),),
                    'length': 8,
                    'name': 'serviceToRespondToRecord',
                    'physical_value': (0x54,),
                    'raw_value': (0x54,),
                    'unit': None
                }
            )
        ),
        (
            [0xC6, 0x07, 0xE0, 0x0C, 0x5E, 0x12, 0x6C, 0x8C, 0x27, 0xA8, 0x3A, 0x20, 0xE6, 0x4A,
             0x3C, 0x38, 0xE7, 0xE2, 0x5E, 0xF4],
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
                                    'physical_value': 'doNotStoreEvent',
                                    'raw_value': 0,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 6,
                                    'name': "event",
                                    'physical_value': 'onComparisonOfValues',
                                    'raw_value': 0x07,
                                    'unit': None
                                },
                            ),
                            'length': 7,
                            'name': "eventType",
                            'physical_value': 0x07,
                            'raw_value': 0x07,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x07,
                    'raw_value': 0x07,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'numberOfIdentifiedEvents',
                    'physical_value': 0xE0,
                    'raw_value': 0xE0,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'eventWindowTime',
                    'physical_value': 0x0C,
                    'raw_value': 0x0C,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 16,
                            'name': 'DID',
                            'physical_value': 0x5E12,
                            'raw_value': 0x5E12,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 8,
                            'name': 'Comparison logic',
                            'physical_value': 0x6C,
                            'raw_value': 0x6C,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 32,
                            'name': 'Compare Value',
                            'physical_value': 0x8C27A83A,
                            'raw_value': 0x8C27A83A,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 8,
                            'name': 'Hysteresis Value',
                            'physical_value': 100 / 255 * 0x20,
                            'raw_value': 0x20,
                            'unit': "%"
                        },
                        {
                            'children': (
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'Compare Sign',
                                    'physical_value': "Comparison with sign",
                                    'raw_value': 1,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 5,
                                    'name': 'Bits Number',
                                    'physical_value': 0x19,
                                    'raw_value': 0x19,
                                    'unit': "bits"
                                },
                                {
                                    'children': (),
                                    'length': 10,
                                    'name': 'Bit Offset',
                                    'physical_value': 0x24A,
                                    'raw_value': 0x24A,
                                    'unit': "bits"
                                },
                            ),
                            'length': 16,
                            'name': 'Localization',
                            'physical_value': 0xE64A,
                            'raw_value': 0xE64A,
                            'unit': None
                        },
                    ),
                    'length': 80,
                    'name': 'eventTypeRecord',
                    'physical_value': 0x5E126C8C27A83A20E64A,
                    'raw_value': 0x5E126C8C27A83A20E64A,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), ()),
                    'length': 8,
                    'name': 'serviceToRespondToRecord',
                    'physical_value': (0x3C, 0x38, 0xE7, 0xE2, 0x5E, 0xF4),
                    'raw_value': (0x3C, 0x38, 0xE7, 0xE2, 0x5E, 0xF4),
                    'unit': None
                }
            ),
        ),
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
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": False,
                    "eventType": 0x03
                },
                "eventWindowTime": 0xFE,
                "eventTypeRecord": {
                    "DID": 0x0123,
                },
                "serviceToRespondToRecord": (0x22, 0xFE, 0xDC, 0xBA, 0x98),
            },
            RequestSID.ResponseOnEvent,
            None,
            bytearray([0x86, 0x03, 0xFE, 0x01, 0x23, 0x22, 0xFE, 0xDC, 0xBA, 0x98])
        ),
        (
            {
                "SubFunction": 0xC3,
                "numberOfIdentifiedEvents": 0x01,
                "eventWindowTime": 0x0D,
                "eventTypeRecord": 0xF0E1,
                "serviceToRespondToRecord": (0x54, 0x35, 0x3B, 0x72, 0x29, 0x63),
            },
            None,
            ResponseSID.ResponseOnEvent,
            bytearray([0xC6, 0xC3, 0x01, 0x0D, 0xF0, 0xE1, 0x54, 0x35, 0x3B, 0x72, 0x29, 0x63])
        ),
        # reportActivatedEvents (0x04)
        (
            {
                "SubFunction": 0xC4,
                "eventWindowTime": 0xE8,
            },
            RequestSID.ResponseOnEvent,
            None,
            bytearray([0x86, 0xC4, 0xE8])
        ),
        (
            {
                "SubFunction": 0x04,
                "numberOfIdentifiedEvents": 0x04,
                "eventTypeOfActiveEvent#1": 0x01,
                "eventWindowTime#1": 0x01,
                "eventTypeRecord#1": 0x32,
                "serviceToRespondToRecord#1": (0x10, 0x02),
                "eventTypeOfActiveEvent#2": 0x02,
                "eventWindowTime#2": 0xFF,
                "eventTypeRecord#2": {
                    "Timer schedule": 0x50
                },
                "serviceToRespondToRecord#2": (0x22, 0xA2, 0xEE),
                "eventTypeOfActiveEvent#3": 0x03,
                "eventWindowTime#3": 0x2B,
                "eventTypeRecord#3": {
                    "DID": 0x1234
                },
                "serviceToRespondToRecord#3": (0x11, 0x02),
                "eventTypeOfActiveEvent#4": 0x47,
                "eventWindowTime#4": 0x00,
                "eventTypeRecord#4": {
                    "DID": 0x5927,
                    "Comparison logic": 0x01,
                    "Compare Value": 0x000789AB,
                    "Hysteresis Value": 0x00,
                    "Localization": {
                        "Compare Sign": True,
                        "Bits Number": 16,
                        "Bit Offset": 512,
                    }
                },
                "serviceToRespondToRecord#4": (0x50, 0x78, 0xD7, 0x86, 0xB0, 0x44, 0x8B, 0xBA, 0x9B, 0xBD),
            },
            None,
            ResponseSID.ResponseOnEvent,
            bytearray([0xC6, 0x04, 0x04,
                       0x01, 0x01, 0x32, 0x10, 0x02,
                       0x02, 0xFF, 0x50, 0x22, 0xA2, 0xEE,
                       0x03, 0x2B, 0x12, 0x34, 0x11, 0x02,
                       0x47, 0x00, 0x59, 0x27, 0x01, 0x00, 0x07, 0x89, 0xAB, 0x00, 0xC2, 0x00, 0x50, 0x78, 0xD7, 0x86, 0xB0, 0x44, 0x8B, 0xBA, 0x9B, 0xBD])
        ),
        # startResponseOnEvent (0x05)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": False,
                    "eventType": 0x45
                },
                "eventWindowTime": 0x90,
            },
            RequestSID.ResponseOnEvent,
            None,
            bytearray([0x86, 0x45, 0x90])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": True,
                    "eventType": {
                        "storageState": False,
                        "event": 0x05,
                    }
                },
                "numberOfIdentifiedEvents": 0x61,
                "eventWindowTime": 0x6E,
            },
            None,
            ResponseSID.ResponseOnEvent,
            bytearray([0xC6, 0x85, 0x61, 0x6E])
        ),
        # clearResponseOnEvent (0x06)
        (
            {
                "SubFunction": 0x86,
                "eventWindowTime": 0x02,
            },
            RequestSID.ResponseOnEvent,
            None,
            bytearray([0x86, 0x86, 0x02])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": False,
                    "eventType": 0x46
                },
                "numberOfIdentifiedEvents": 0x00,
                "eventWindowTime": 0xD5,
            },
            None,
            ResponseSID.ResponseOnEvent,
            bytearray([0xC6, 0x46, 0x00, 0xD5])
        ),
        # onComparisonOfValues (0x07)
        (
            {
                "SubFunction": 0x47,
                "eventWindowTime": 0xF1,
                "eventTypeRecord": {
                    "DID": 0xA9B7,
                    "Comparison logic": 0x02,
                    "Compare Value": 0x3D7E52C5,
                    "Hysteresis Value": 0xFF,
                    "Localization": {
                        "Compare Sign": False,
                        "Bits Number": 0x1F,
                        "Bit Offset": 0x001,
                    }
                },
                "serviceToRespondToRecord": (0xEC, 0xAD, 0x25, 0x72),
            },
            RequestSID.ResponseOnEvent,
            None,
            bytearray([0x86, 0x47, 0xF1, 0xA9, 0xB7, 0x02, 0x3D, 0x7E, 0x52, 0xC5, 0xFF,
                       0x7C, 0x01, 0xEC, 0xAD, 0x25, 0x72])
        ),
        (
            {
                "SubFunction": 0x87,
                "numberOfIdentifiedEvents": 0xEB,
                "eventWindowTime": 0xB4,
                "eventTypeRecord": 0x6DC91B40DCA884EEA101,
                "serviceToRespondToRecord": (0x22, 0x52, 0xA0),
            },
            None,
            ResponseSID.ResponseOnEvent,
            bytearray([0xC6, 0x87, 0xEB, 0xB4, 0x6D, 0xC9, 0x1B, 0x40, 0xDC, 0xA8, 0x84, 0xEE, 0xA1, 0x01, 0x22, 0x52, 0xA0])
        ),
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

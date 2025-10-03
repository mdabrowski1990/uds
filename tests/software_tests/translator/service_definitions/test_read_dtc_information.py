import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.read_dtc_information import READ_DTC_INFORMATION, READ_DTC_INFORMATION_2013, READ_DTC_INFORMATION_2020


class TestReadDTCInformation:
    """Unit tests for `ReadDTCInformation` service."""

    def test_request_sid(self):
        assert READ_DTC_INFORMATION_2013.request_sid == RequestSID.ReadDTCInformation
        assert READ_DTC_INFORMATION_2020.request_sid == RequestSID.ReadDTCInformation

    def test_response_sid(self):
        assert READ_DTC_INFORMATION_2013.response_sid == ResponseSID.ReadDTCInformation
        assert READ_DTC_INFORMATION_2020.response_sid == ResponseSID.ReadDTCInformation

    def test_default_translator(self):
        assert READ_DTC_INFORMATION is READ_DTC_INFORMATION_2020


@pytest.mark.integration
class TestReadDTCInformation2013Integration:
    """Integration tests for `ReadDTCInformation` service version 2013."""

    @pytest.mark.parametrize("payload, decoded_message", [
        # reportNumberOfDTCByStatusMask
        (
            [0x19, 0x81, 0xFF],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'ReadDTCInformation',
                    'raw_value': 0x19,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': "suppressPosRspMsgIndicationBit",
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportNumberOfDTCByStatusMask',
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
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'warningIndicatorRequested',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testNotCompletedThisOperationCycle',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailedSinceLastClear',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testNotCompletedSinceLastClear',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'confirmedDTC',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'pendingDTC',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailedThisOperationCycle',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailed',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'DTCStatusMask',
                    'physical_value': 0xFF,
                    'raw_value': 0xFF,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x01, 0xCF, 0x03, 0x0F, 0x1E],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'ReadDTCInformation',
                    'raw_value': 0x59,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'suppressPosRspMsgIndicationBit',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportNumberOfDTCByStatusMask',
                            'raw_value': 0x1,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'warningIndicatorRequested',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testNotCompletedThisOperationCycle',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailedSinceLastClear',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testNotCompletedSinceLastClear',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'confirmedDTC',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'pendingDTC',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailedThisOperationCycle',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailed',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0xCF,
                    'raw_value': 0xCF,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCFormatIdentifier',
                    'physical_value': 'ISO 11992-4 DTC Format',
                    'raw_value': 0x03,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DTCCount',
                    'physical_value': 0x0F1E,
                    'raw_value': 0x0F1E,
                    'unit': 'DTCs'
                },

            ),
        ),
        # reportDTCByStatusMask
        (
            [0x19, 0x82, 0xFF],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'ReadDTCInformation',
                    'raw_value': 0x19,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': "suppressPosRspMsgIndicationBit",
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportDTCByStatusMask',
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
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'warningIndicatorRequested',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testNotCompletedThisOperationCycle',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailedSinceLastClear',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testNotCompletedSinceLastClear',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'confirmedDTC',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'pendingDTC',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailedThisOperationCycle',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailed',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'DTCStatusMask',
                    'physical_value': 0xFF,
                    'raw_value': 0xFF,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x02, 0xCF, 0x12, 0x45, 0x56, 0x55, 0xF0, 0xE1, 0xD2, 0xAA],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'ReadDTCInformation',
                    'raw_value': 0x59,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'suppressPosRspMsgIndicationBit',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportDTCByStatusMask',
                            'raw_value': 0x02,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x02,
                    'raw_value': 0x02,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'warningIndicatorRequested',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testNotCompletedThisOperationCycle',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailedSinceLastClear',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testNotCompletedSinceLastClear',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'confirmedDTC',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'pendingDTC',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailedThisOperationCycle',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailed',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0xCF,
                    'raw_value': 0xCF,
                    'unit': None
                },
                {
                    'children': [
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 0x124556,
                                'raw_value': 0x124556,
                                'unit': None,
                            },
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                'name': 'DTC Status',
                                'physical_value': 0x55,
                                'raw_value': 0x55,
                                'unit': None,
                            }
                        ),
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 0xF0E1D2,
                                'raw_value': 0xF0E1D2,
                                'unit': None,
                            },
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                     }
                                ),
                                'length': 8,
                                'name': 'DTC Status',
                                'physical_value': 0xAA,
                                'raw_value': 0xAA,
                                'unit': None,
                            }
                        ),
                    ],
                    'length': 32,
                    'name': 'DTC and Status',
                    'physical_value': (0x12455655, 0xF0E1D2AA),
                    'raw_value': [0x12455655, 0xF0E1D2AA],
                    'unit': None
                },
            ),
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert READ_DTC_INFORMATION_2013.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        # reportNumberOfDTCByStatusMask
        (
            {
                "SubFunction": 0x01,
                "DTCStatusMask": 0xAA,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x01, 0xAA])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x01,
                },
                "DTCStatusAvailabilityMask": {
                    "warningIndicatorRequested": 0,
                    "testNotCompletedThisOperationCycle": 1,
                    "testFailedSinceLastClear": 0,
                    "testNotCompletedSinceLastClear": 1,
                    "confirmedDTC": 0,
                    "pendingDTC": 1,
                    "testFailedThisOperationCycle": 0,
                    "testFailed": 1,
                },
                "DTCFormatIdentifier": 0x04,
                "DTCCount": 0x1234,
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x81, 0x55, 0x04, 0x12, 0x34])
        ),
        # reportDTCByStatusMask
        (
            {
                "SubFunction": 0x02,
                "DTCStatusMask": 0xAA,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x02, 0xAA])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x02,
                },
                "DTCStatusAvailabilityMask": {
                    "warningIndicatorRequested": 0,
                    "testNotCompletedThisOperationCycle": 1,
                    "testFailedSinceLastClear": 0,
                    "testNotCompletedSinceLastClear": 1,
                    "confirmedDTC": 0,
                    "pendingDTC": 1,
                    "testFailedThisOperationCycle": 0,
                    "testFailed": 1,
                },
                "DTCFormatIdentifier": 0x04,
                "DTC and Status": [],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x82, 0x55])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert READ_DTC_INFORMATION_2013.encode(data_records_values=data_records_values,
                                                        sid=sid,
                                                        rsid=rsid) == payload

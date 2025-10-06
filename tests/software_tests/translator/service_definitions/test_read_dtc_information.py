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
        # reportDTCSnapshotIdentification
        (
            [0x19, 0x83],
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
                            'physical_value': 'reportDTCSnapshotIdentification',
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
        (
            [0x59, 0x03, 0x12, 0x34, 0x56, 0x01, 0x12, 0x34, 0x56, 0xBD, 0xF1, 0xE2, 0xD3, 0xCC],
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
                            'physical_value': 'reportDTCSnapshotIdentification',
                            'raw_value': 0x03,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x03,
                    'raw_value': 0x03,
                    'unit': None
                },
                {
                    'children': [
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 0x123456,
                                'raw_value': 0x123456,
                                'unit': None,
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'DTCSnapshotRecordNumber',
                                'physical_value': 0x01,
                                'raw_value': 0x01,
                                'unit': None,
                            }
                        ),
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 0x123456,
                                'raw_value': 0x123456,
                                'unit': None,
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'DTCSnapshotRecordNumber',
                                'physical_value': 0xBD,
                                'raw_value': 0xBD,
                                'unit': None,
                            }
                        ),
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 0xF1E2D3,
                                'raw_value': 0xF1E2D3,
                                'unit': None,
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'DTCSnapshotRecordNumber',
                                'physical_value': 0xCC,
                                'raw_value': 0xCC,
                                'unit': None,
                            }
                        ),
                    ],
                    'length': 32,
                    'name': 'DTC and Snapshot Record Number',
                    'physical_value': (0x12345601, 0x123456BD, 0xF1E2D3CC),
                    'raw_value': [0x12345601, 0x123456BD, 0xF1E2D3CC],
                    'unit': None
                },
            ),
        ),
        # reportDTCSnapshotRecordByDTCNumber
        (
            [0x19, 0x84, 0xFF, 0x5A],
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
                            'physical_value': 'reportDTCSnapshotRecordByDTCNumber',
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
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCSnapshotRecordNumber',
                    'physical_value': 0x5A,
                    'raw_value': 0x5A,
                    'unit': None
                }
            )
        ),
        # (
        #     [0x59, 0x04, 0x12, 0x34, 0x56, 0x89, 0x25, 0x01, 0x01, 0x00, 0x7E],
        #     (
        #         {
        #             'children': (),
        #             'length': 8,
        #             'name': 'RSID',
        #             'physical_value': 'ReadDTCInformation',
        #             'raw_value': 0x59,
        #             'unit': None
        #         },
        #         {
        #             'children': (
        #                 {
        #                     'children': (),
        #                     'length': 1,
        #                     'name': 'suppressPosRspMsgIndicationBit',
        #                     'physical_value': 'no',
        #                     'raw_value': 0x0,
        #                     'unit': None
        #                 },
        #                 {
        #                     'children': (),
        #                     'length': 7,
        #                     'name': 'reportType',
        #                     'physical_value': 'reportDTCSnapshotIdentification',
        #                     'raw_value': 0x04,
        #                     'unit': None
        #                 }
        #             ),
        #             'length': 8,
        #             'name': 'SubFunction',
        #             'physical_value': 0x04,
        #             'raw_value': 0x04,
        #             'unit': None
        #         },
        #         {
        #             'children': (),
        #             'length': 24,
        #             'name': 'DTC',
        #             'physical_value': 0x123456,
        #             'raw_value': 0x123456,
        #             'unit': None,
        #         },
        #         {
        #             'children': (
        #                 {
        #                     'children': (),
        #                     'length': 1,
        #                     'name': 'warningIndicatorRequested',
        #                     'physical_value': 'yes',
        #                     'raw_value': 0x1,
        #                     'unit': None
        #                 },
        #                 {
        #                     'children': (),
        #                     'length': 1,
        #                     'name': 'testNotCompletedThisOperationCycle',
        #                     'physical_value': 'no',
        #                     'raw_value': 0x0,
        #                     'unit': None
        #                 },
        #                 {
        #                     'children': (),
        #                     'length': 1,
        #                     'name': 'testFailedSinceLastClear',
        #                     'physical_value': 'no',
        #                     'raw_value': 0x0,
        #                     'unit': None
        #                 },
        #                 {
        #                     'children': (),
        #                     'length': 1,
        #                     'name': 'testNotCompletedSinceLastClear',
        #                     'physical_value': 'no',
        #                     'raw_value': 0x0,
        #                     'unit': None
        #                 },
        #                 {
        #                     'children': (),
        #                     'length': 1,
        #                     'name': 'confirmedDTC',
        #                     'physical_value': 'yes',
        #                     'raw_value': 0x1,
        #                     'unit': None
        #                 },
        #                 {
        #                     'children': (),
        #                     'length': 1,
        #                     'name': 'pendingDTC',
        #                     'physical_value': 'no',
        #                     'raw_value': 0x0,
        #                     'unit': None
        #                 },
        #                 {
        #                     'children': (),
        #                     'length': 1,
        #                     'name': 'testFailedThisOperationCycle',
        #                     'physical_value': 'no',
        #                     'raw_value': 0x0,
        #                     'unit': None
        #                 },
        #                 {
        #                     'children': (),
        #                     'length': 1,
        #                     'name': 'testFailed',
        #                     'physical_value': 'yes',
        #                     'raw_value': 0x1,
        #                     'unit': None
        #                 },
        #             ),
        #             'length': 8,
        #             'name': 'DTC Status',
        #             'physical_value': 0x89,
        #             'raw_value': 0x89,
        #             'unit': None,
        #         },
        #         {
        #             'children': (),
        #             'length': 8,
        #             'name': 'DTCSnapshotRecordNumber#1',
        #             'physical_value': 0x25,
        #             'raw_value': 0x25,
        #             'unit': None,
        #         },
        #         {
        #             'children': (),
        #             'length': 8,
        #             'name': 'DIDCount#1',
        #             'physical_value': 0x01,
        #             'raw_value': 0x01,
        #             'unit': 'DIDs',
        #         },
        #         {
        #             'children': (),
        #             'length': 16,
        #             'name': 'DID#1_1',
        #             'physical_value': 0x0100,
        #             'raw_value': 0x0100,
        #             'unit': None,
        #         },
        #         {
        #             'children': (),
        #             'length': 8,
        #             'name': 'DID#1_1 data',
        #             'physical_value': (0x7E,),
        #             'raw_value': [0x7E],
        #             'unit': None,
        #         },
        #     ),
        # ),
    ])
    def test_decode(self, payload, decoded_message):
        assert READ_DTC_INFORMATION_2013.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        # reportNumberOfDTCByStatusMask (0x01)
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
        # reportDTCByStatusMask (0x02)
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
        # reportDTCSnapshotIdentification (0x03)
        (
            {
                "SubFunction": 0x03,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x03])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x03,
                },
                "DTC and Snapshot Record Number": [
                    {
                        "DTC": 0x5A6B7C,
                        "DTCSnapshotRecordNumber": 0x20
                    },
                    {
                        "DTC": 0xCAFFEE,
                        "DTCSnapshotRecordNumber": 0xC2
                    },
                ]
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x83, 0x5A, 0x6B, 0x7C, 0x20, 0xCA, 0xFF, 0xEE, 0xC2])
        ),
        # reportDTCSnapshotRecordByDTCNumber (0x04)
        (
            {
                "SubFunction": 0x04,
                "DTCStatusMask": 0x24,
                "DTCSnapshotRecordNumber": 0x90,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x04, 0x24, 0x90])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x04,
                },
                "DTC": 0xBEEF02,
                "DTC Status": {
                    "warningIndicatorRequested": 1,
                    "testNotCompletedThisOperationCycle": 0,
                    "testFailedSinceLastClear": 1,
                    "testNotCompletedSinceLastClear": 0,
                    "confirmedDTC": 1,
                    "pendingDTC": 0,
                    "testFailedThisOperationCycle": 1,
                    "testFailed": 1,
                },
                "DTCSnapshotRecordNumber#1": 0x3C,
                "DIDCount#1": 2,
                "DID#1_1": 0x0100,
                "DID#1_1 data": [0xF1, 0xE2],
                "DID#1_2": 0x0101,
                "DID#1_2 data": [0xD3],
                "DTCSnapshotRecordNumber#2": 0x40,
                "DIDCount#2": 1,
                "DID#2_1": 0x0102,
                "DID#2_1 data": [0xC4, 0xB5, 0xA6, 0x97, 0x88],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x84,
                       0xBE, 0xEF, 0x02, 0xAB,  # DTC and Status
                       0x3C, 0x02, 0x01, 0x00, 0xF1, 0xE2, 0x01, 0x01, 0xD3,  # DTCSnapshotRecord#1
                       0x40, 0x01, 0x01, 0x02, 0xC4, 0xB5, 0xA6, 0x97, 0x88]), # DTCSnapshotRecord#2
        ),
        # reportDTCStoredDataByRecordNumber (0x05)
        (
            {
                "SubFunction": 0x05,
                "DTCStoredDataRecordNumber": 0xFE
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x05, 0xFE])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x05,
                },
                "DTCStoredDataRecordNumber#1": 0x2E,
                "DTC#1": 0x987654,
                "DTC Status#1": {
                    "warningIndicatorRequested": 1,
                    "testNotCompletedThisOperationCycle": 0,
                    "testFailedSinceLastClear": 1,
                    "testNotCompletedSinceLastClear": 0,
                    "confirmedDTC": 1,
                    "pendingDTC": 0,
                    "testFailedThisOperationCycle": 1,
                    "testFailed": 1,
                },
                "DIDCount#1": 2,
                "DID#1_1": 0x0100,
                "DID#1_1 data": [0x68, 0x79],
                "DID#1_2": 0x0101,
                "DID#1_2 data": [0xD3],
                "DTCStoredDataRecordNumber#2": 0xF4,
                "DTC#2": 0x1F2E3D,
                "DTC Status#2": {
                    "warningIndicatorRequested": 0,
                    "testNotCompletedThisOperationCycle": 1,
                    "testFailedSinceLastClear": 0,
                    "testNotCompletedSinceLastClear": 1,
                    "confirmedDTC": 1,
                    "pendingDTC": 1,
                    "testFailedThisOperationCycle": 0,
                    "testFailed": 0,
                },
                "DIDCount#2": 1,
                "DID#2_1": 0x0102,
                "DID#2_1 data": [0xCA, 0xFF, 0xEE, 0x00, 0xBE, 0xEF],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x85,
                       0x2E, 0x98, 0x76, 0x54, 0xAB, 0x02, 0x01, 0x00, 0x68, 0x79, 0x01, 0x01, 0xD3,  # DTCStoredDataRecord#1
                       0xF4, 0x1F, 0x2E, 0x3D, 0x6C, 0x01, 0x01, 0x02, 0xCA, 0xFF, 0xEE, 0x00, 0xBE, 0xEF])  # DTCStoredDataRecord#2
        ),
        # reportDTCExtDataRecordByDTCNumber (0x06)
        (
            {
                "SubFunction": 0x06,
                "DTC": 0xF0E1D2,
                "DTCExtDataRecordNumber": 0xFF
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x06, 0xF0, 0xE1, 0xD2, 0xFF])
        ),
        (
            {
                "SubFunction": 0x06,
                "DTC": 0x896C3B,
                "DTC Status": 0x5A,
                "DTCExtDataRecordNumber#1": 0x01,
                "DTCExtDataRecord#1": [0x12, 0x34],
                "DTCExtDataRecordNumber#2": 0x02,
                "DTCExtDataRecord#2": [0x34, 0x56],
                "DTCExtDataRecordNumber#3": 0x43,
                "DTCExtDataRecord#3": [0x78, 0x9A, 0xBC, 0xDE, 0xF0],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x06,
                       0x89, 0x6C, 0x3B, 0x5A,  # DTC and Status
                       0x01, 0x12, 0x34,  # DTCExtendedDataRecord#1
                       0x02, 0x34, 0x56,  # DTCExtendedDataRecord#2
                       0x43, 0x78, 0x9A, 0xBC, 0xDE, 0xF0])  # DTCExtendedDataRecord#3
        ),
        # reportNumberOfDTCBySeverityMaskRecord (0x07)
        (
            {
                "SubFunction": 0x07,
                "DTCSeverityMask": 0x2A,
                "DTCStatusMask": 0x4B,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x07, 0x2A, 0x4B])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x07,
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
                "DTCFormatIdentifier": 0x03,
                "DTCCount": 0xFEDC,
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x87, 0x55, 0x03, 0xFE, 0xDC])
        ),
        # reportDTCBySeverityMaskRecord (0x08)
        (
            {
                "SubFunction": 0x08,
                "DTCSeverityMask": 0xC7,
                "DTCStatusMask": 0xD8,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x08, 0xC7, 0xD8])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x08,
                },
                "DTCStatusAvailabilityMask": {
                    "warningIndicatorRequested": 1,
                    "testNotCompletedThisOperationCycle": 1,
                    "testFailedSinceLastClear": 0,
                    "testNotCompletedSinceLastClear": 0,
                    "confirmedDTC": 1,
                    "pendingDTC": 1,
                    "testFailedThisOperationCycle": 0,
                    "testFailed": 0,
                },
                "DTC Severity, DTC Functional Unit, DTC and DTC Status": [
                    {
                        "DTC Severity": 0xF0,
                        "FunctionalGroupIdentifier": 0xE1,
                        "DTC": 0xD2C3B4,
                        "DTC Status": 0xA5
                    },
                    0x123456789ABC,
                    {
                        "DTC Severity": 0x5A,
                        "FunctionalGroupIdentifier": 0x69,
                        "DTC": 0x987654,
                        "DTC Status": 0x89
                    },
                ]
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x88, 0xCC,
                       0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5,  # DTC Severity, DTC Functional Unit, DTC and DTC Status # 1
                       0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC,  # DTC Severity, DTC Functional Unit, DTC and DTC Status # 2
                       0x5A, 0x69, 0x98, 0x76, 0x54, 0x89])  # DTC Severity, DTC Functional Unit, DTC and DTC Status # 3
        ),
        # reportSeverityInformationOfDTC (0x09)
        (
            {
                "SubFunction": 0x09,
                "DTC": 0xFEDCBA,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x09, 0xFE, 0xDC, 0xBA])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x09,
                },
                "DTCStatusAvailabilityMask": {
                    "warningIndicatorRequested": 0,
                    "testNotCompletedThisOperationCycle": 0,
                    "testFailedSinceLastClear": 1,
                    "testNotCompletedSinceLastClear": 1,
                    "confirmedDTC": 0,
                    "pendingDTC": 0,
                    "testFailedThisOperationCycle": 1,
                    "testFailed": 1,
                },
                "DTC Severity, DTC Functional Unit, DTC and DTC Status": {
                        "DTC Severity": 0xF0,
                        "FunctionalGroupIdentifier": 0xE1,
                        "DTC": 0xD2C3B4,
                        "DTC Status": 0xA5
                },
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x89, 0x33, 0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5])
        ),
        # reportSupportedDTC (0x0A)
        (
            {
                "SubFunction": 0x0A,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x0A])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x0A,
                },
                "DTCStatusAvailabilityMask": {
                    "warningIndicatorRequested": 1,
                    "testNotCompletedThisOperationCycle": 1,
                    "testFailedSinceLastClear": 1,
                    "testNotCompletedSinceLastClear": 1,
                    "confirmedDTC": 1,
                    "pendingDTC": 1,
                    "testFailedThisOperationCycle": 1,
                    "testFailed": 1,
                },
                "DTC and Status": [
                    {
                        "DTC": 0x012345,
                        "DTC Status": 0x67,
                    },
                    0x89ABCDEF,
                    {
                        "DTC": 0xF1E2D3,
                        "DTC Status": 0xFF,
                    },
                    {
                        "DTC": 0xC4B5A6,
                        "DTC Status": 0x00,
                    },
                    0x9788796A,
                    0x5B4C3D2E,
                ]
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x8A, 0xFF,
                       0x01, 0x23, 0x45, 0x67,
                       0x89, 0xAB, 0xCD, 0xEF,
                       0xF1, 0xE2, 0xD3, 0xFF,
                       0xC4, 0xB5, 0xA6, 0x00,
                       0x97, 0x88, 0x79, 0x6A,
                       0x5B, 0x4C, 0x3D, 0x2E])
        ),
        # reportFirstTestFailedDTC (0x0B)
        (
                {
                    "SubFunction": 0x0B,
                },
                RequestSID.ReadDTCInformation,
                None,
                bytearray([0x19, 0x0B])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x0B,
                },
                "DTCStatusAvailabilityMask": {
                    "warningIndicatorRequested": 1,
                    "testNotCompletedThisOperationCycle": 1,
                    "testFailedSinceLastClear": 1,
                    "testNotCompletedSinceLastClear": 1,
                    "confirmedDTC": 1,
                    "pendingDTC": 1,
                    "testFailedThisOperationCycle": 1,
                    "testFailed": 1,
                },
                "DTC and Status": {
                        "DTC": 0xF1E2D3,
                        "DTC Status": 0x89,
                },
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x8B, 0xFF,
                       0xF1, 0xE2, 0xD3, 0x89])
        ),
        # reportFirstConfirmedDTC (0x0C)
        (
                {
                    "SubFunction": 0x0C,
                },
                RequestSID.ReadDTCInformation,
                None,
                bytearray([0x19, 0x0C])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x0C,
                },
                "DTCStatusAvailabilityMask": {
                    "warningIndicatorRequested": 0,
                    "testNotCompletedThisOperationCycle": 0,
                    "testFailedSinceLastClear": 0,
                    "testNotCompletedSinceLastClear": 0,
                    "confirmedDTC": 1,
                    "pendingDTC": 0,
                    "testFailedThisOperationCycle": 1,
                    "testFailed": 1,
                },
                "DTC and Status": None
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x8C, 0x0B])
        ),
        # reportMostRecentTestFailedDTC (0x0D)
        (
                {
                    "SubFunction": 0x0D,
                },
                RequestSID.ReadDTCInformation,
                None,
                bytearray([0x19, 0x0D])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x0D,
                },
                "DTCStatusAvailabilityMask": {
                    "warningIndicatorRequested": 1,
                    "testNotCompletedThisOperationCycle": 0,
                    "testFailedSinceLastClear": 1,
                    "testNotCompletedSinceLastClear": 0,
                    "confirmedDTC": 1,
                    "pendingDTC": 1,
                    "testFailedThisOperationCycle": 1,
                    "testFailed": 1,
                },
                "DTC and Status": {
                        "DTC": 0x5A6B7C,
                        "DTC Status": 0x2B,
                },
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x8D, 0xAF,
                       0x5A, 0x6B, 0x7C, 0x2B])
        ),
        # reportMostRecentConfirmedDTC (0x0E)
        (
                {
                    "SubFunction": 0x0E,
                },
                RequestSID.ReadDTCInformation,
                None,
                bytearray([0x19, 0x0E])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x0E,
                },
                "DTCStatusAvailabilityMask": {
                    "warningIndicatorRequested": 0,
                    "testNotCompletedThisOperationCycle": 0,
                    "testFailedSinceLastClear": 1,
                    "testNotCompletedSinceLastClear": 0,
                    "confirmedDTC": 1,
                    "pendingDTC": 1,
                    "testFailedThisOperationCycle": 1,
                    "testFailed": 1,
                },
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x8E, 0x2F])
        ),
        # reportMirrorMemoryDTCByStatusMask (0x0F)
        (
                {
                    "SubFunction": 0x0F,
                    "DTCStatusMask": 0x85
                },
                RequestSID.ReadDTCInformation,
                None,
                bytearray([0x19, 0x0F, 0x85])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x0F,
                },
                "DTCStatusAvailabilityMask": 0xFF,
                "DTC and Status": [
                    {
                        "DTC": 0x012345,
                        "DTC Status": 0x67,
                    },
                    0x89ABCDEF,
                ]
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x8F, 0xFF,
                       0x01, 0x23, 0x45, 0x67,
                       0x89, 0xAB, 0xCD, 0xEF])
        ),
        # reportMirrorMemoryDTCExtDataRecordByDTCNumber (0x10)
        # TODO
        # reportNumberOfMirrorMemoryDTCByStatusMask (0x11)
        # TODO
        # reportNumberOfEmissionsOBDDTCByStatusMask (0x12)
        # TODO
        # reportEmissionsOBDDTCByStatusMask (0x13)
        # TODO
        # reportDTCFaultDetectionCounter (0x14)
        # TODO
        # reportDTCWithPermanentStatus (0x15)
        # TODO
        # reportDTCExtDataRecordByRecordNumber (0x16)
        # TODO
        # reportUserDefMemoryDTCByStatusMask (0x17)
        # TODO
        # reportUserDefMemoryDTCSnapshotRecordByDTCNumber (0x18)
        # TODO
        # reportUserDefMemoryDTCExtDataRecordByDTCNumber (0x19)
        # TODO
        # reportWWHOBDDTCByMaskRecord (0x42)
        # TODO
        # reportWWHOBDDTCWithPermanentStatus (0x55)
        # TODO
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert READ_DTC_INFORMATION_2013.encode(data_records_values=data_records_values,
                                                sid=sid,
                                                rsid=rsid) == payload

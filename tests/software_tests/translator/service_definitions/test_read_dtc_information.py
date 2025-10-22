import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.read_dtc_information import (
    READ_DTC_INFORMATION,
    READ_DTC_INFORMATION_2013,
    READ_DTC_INFORMATION_2020,
)
from uds.utilities import bytes_to_hex


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
        # reportNumberOfDTCByStatusMask (0x01)
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
        # reportDTCByStatusMask (0x02)
        (
            [0x19, 0x02, 0x12],
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testNotCompletedThisOperationCycle',
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'confirmedDTC',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'pendingDTC',
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'DTCStatusMask',
                    'physical_value': 0x12,
                    'raw_value': 0x12,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x82, 0xCF, 0x12, 0x45, 0x56, 0x55, 0xF0, 0xE1, 0xD2, 0xAA],
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
                            'physical_value': 'yes',
                            'raw_value': 0x1,
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
                    'children': (
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'P1245-56',
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
                                'name': 'DTCStatus',
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
                                'physical_value': 'U30E1-D2',
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
                                'name': 'DTCStatus',
                                'physical_value': 0xAA,
                                'raw_value': 0xAA,
                                'unit': None,
                            }
                        ),
                    ),
                    'length': 32,
                    'name': 'DTC and Status',
                    'physical_value': (0x12455655, 0xF0E1D2AA),
                    'raw_value': (0x12455655, 0xF0E1D2AA),
                    'unit': None
                },
            ),
        ),
        # reportDTCSnapshotIdentification (0x03)
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
                    'children': (
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'P1234-56',
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
                                'physical_value': 'P1234-56',
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
                                'physical_value': 'U31E2-D3',
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
                    ),
                    'length': 32,
                    'name': 'DTC and Snapshot Record Number',
                    'physical_value': (0x12345601, 0x123456BD, 0xF1E2D3CC),
                    'raw_value': (0x12345601, 0x123456BD, 0xF1E2D3CC),
                    'unit': None
                },
            ),
        ),
        # reportDTCSnapshotRecordByDTCNumber (0x04)
        (
            [0x19, 0x04, 0x50, 0x6F, 0x7E, 0x88],
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                    'physical_value': 0x04,
                    'raw_value': 0x04,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 24,
                    'name': 'DTC',
                    'physical_value': 'C106F-7E',
                    'raw_value': 0x506F7E,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCSnapshotRecordNumber',
                    'physical_value': 0x88,
                    'raw_value': 0x88,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x84, 0x12, 0x34, 0x56, 0x89, 0x25, 0x01, 0x01, 0x00, 0x7E, 0x8F, 0x90, 0xA1, 0xB2, 0xC3, 0xD4, 0xE5],
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
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportDTCSnapshotRecordByDTCNumber',
                            'raw_value': 0x04,
                            'unit': None
                        }
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
                            'length': 24,
                            'name': 'DTC',
                            'physical_value': 'P1234-56',
                            'raw_value': 0x123456,
                            'unit': None,
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
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
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
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'testFailedThisOperationCycle',
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
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
                            'name': 'DTCStatus',
                            'physical_value': 0x89,
                            'raw_value': 0x89,
                            'unit': None,
                        },
                    ),
                    'length': 32,
                    'name': 'DTC and Status',
                    'physical_value': 0x12345689,
                    'raw_value': 0x12345689,
                    'unit': None,
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCSnapshotRecordNumber#1',
                    'physical_value': 0x25,
                    'raw_value': 0x25,
                    'unit': None,
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DIDCount#1',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': 'DIDs',
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DID#1_1',
                    'physical_value': 0x0100,
                    'raw_value': 0x0100,
                    'unit': None,
                },
                {
                    'children': ((), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'DID#1_1 data',
                    'physical_value': (0x7E, 0x8F, 0x90, 0xA1, 0xB2, 0xC3, 0xD4, 0xE5),
                    'raw_value': (0x7E, 0x8F, 0x90, 0xA1, 0xB2, 0xC3, 0xD4, 0xE5),
                    'unit': None,
                },
            ),
        ),
        # reportDTCStoredDataByRecordNumber (0x05)
        (
            [0x19, 0x85, 0x00],
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
                            'physical_value': 'reportDTCStoredDataByRecordNumber',
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
                    'name': 'DTCStoredDataRecordNumber',
                    'physical_value': 0x00,
                    'raw_value': 0x00,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x05, 0xFE, 0xEF, 0xCD, 0xAB, 0x03, 0x01, 0x64, 0x23, 0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5, 0x96],
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
                            'physical_value': 'reportDTCStoredDataByRecordNumber',
                            'raw_value': 0x05,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x05,
                    'raw_value': 0x05,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCStoredDataRecordNumber#1',
                    'physical_value': 0xFE,
                    'raw_value': 0xFE,
                    'unit': None,
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 24,
                            'name': 'DTC',
                            'physical_value': 'U2FCD-AB',
                            'raw_value': 0xEFCDAB,
                            'unit': None,
                        },
                        {
                            'children': (
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'warningIndicatorRequested',
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'testNotCompletedThisOperationCycle',
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
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
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'pendingDTC',
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
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
                            'name': 'DTCStatus',
                            'physical_value': 0x03,
                            'raw_value': 0x03,
                            'unit': None,
                        },
                    ),
                    'length': 32,
                    'name': 'DTC and Status#1',
                    'physical_value': 0xEFCDAB03,
                    'raw_value': 0xEFCDAB03,
                    'unit': None,
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DIDCount#1',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': 'DIDs',
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DID#1_1',
                    'physical_value': 0x6423,
                    'raw_value': 0x6423,
                    'unit': None,
                },
                {
                    'children': ((), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'DID#1_1 data',
                    'physical_value': (0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5, 0x96),
                    'raw_value': (0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5, 0x96),
                    'unit': None,
                },
            ),
        ),
        # reportDTCExtDataRecordByDTCNumber (0x06)
        (
            [0x19, 0x06, 0xAB, 0x89, 0x67, 0xFF],
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportDTCExtDataRecordByDTCNumber',
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
                    'length': 24,
                    'name': 'DTC',
                    'physical_value': 'B2B89-67',
                    'raw_value': 0xAB8967,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCExtDataRecordNumber',
                    'physical_value': 'all',
                    'raw_value': 0xFF,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x86, 0xFE, 0xDC, 0xBA, 0x76, 0x00, 0x01, 0x01, 0xA1, 0xB2, 0xC3, 0xD4, 0xE5],
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
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportDTCExtDataRecordByDTCNumber',
                            'raw_value': 0x06,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x86,
                    'raw_value': 0x86,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 24,
                            'name': 'DTC',
                            'physical_value': 'U3EDC-BA',
                            'raw_value': 0xFEDCBA,
                            'unit': None,
                        },
                        {
                            'children': (
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'warningIndicatorRequested',
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
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
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
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
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
                                    'unit': None
                                },
                            ),
                            'length': 8,
                            'name': 'DTCStatus',
                            'physical_value': 0x76,
                            'raw_value': 0x76,
                            'unit': None,
                        },
                    ),
                    'length': 32,
                    'name': 'DTC and Status',
                    'physical_value': 0xFEDCBA76,
                    'raw_value': 0xFEDCBA76,
                    'unit': None,
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCExtDataRecordNumber#1',
                    'physical_value': 0x00,
                    'raw_value': 0x00,
                    'unit': None,
                },
                {
                    'children': ((), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'DTCExtDataRecord#1',
                    'physical_value': (0x01, 0x01, 0xA1, 0xB2, 0xC3, 0xD4, 0xE5),
                    'raw_value': (0x01, 0x01, 0xA1, 0xB2, 0xC3, 0xD4, 0xE5),
                    'unit': None,
                },
            ),
        ),
        # reportNumberOfDTCBySeverityMaskRecord (0x07)
        (
            [0x19, 0x87, 0xD2, 0x3C],
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
                            'physical_value': 'reportNumberOfDTCBySeverityMaskRecord',
                            'raw_value': 0x07,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x87,
                    'raw_value': 0x87,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'checkImmediately',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'checkAtNextHalt',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'maintenanceOnly',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_4',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_3',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_2',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_1',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_0',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'DTCSeverityMask',
                    'physical_value': 0xD2,
                    'raw_value': 0xD2,
                    'unit': None
                },
{
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'warningIndicatorRequested',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testNotCompletedThisOperationCycle',
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailed',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'DTCStatusMask',
                    'physical_value': 0x3C,
                    'raw_value': 0x3C,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x07, 0xBE, 0x00, 0x00, 0x00],
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
                            'physical_value': 'reportNumberOfDTCBySeverityMaskRecord',
                            'raw_value': 0x07,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x07,
                    'raw_value': 0x07,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0xBE,
                    'raw_value': 0xBE,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCFormatIdentifier',
                    'physical_value': 'SAE J2012-DA DTC Format 00',
                    'raw_value': 0x00,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DTCCount',
                    'physical_value': 0x0000,
                    'raw_value': 0x0000,
                    'unit': 'DTCs'
                },

            ),
        ),
        # reportDTCBySeverityMaskRecord (0x08)
        (
            [0x19, 0x08, 0x0F, 0xF0],
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportDTCBySeverityMaskRecord',
                            'raw_value': 0x08,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x08,
                    'raw_value': 0x08,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'checkImmediately',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'checkAtNextHalt',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'maintenanceOnly',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_4',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_3',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_2',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_1',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_0',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'DTCSeverityMask',
                    'physical_value': 0x0F,
                    'raw_value': 0x0F,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'pendingDTC',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailedThisOperationCycle',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailed',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'DTCStatusMask',
                    'physical_value': 0xF0,
                    'raw_value': 0xF0,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x88, 0x1B, 0x00, 0x01, 0x23, 0x34, 0x56, 0x1B, 0xFF, 0x33, 0x78, 0x9A, 0xBC, 0x01, 0xC0, 0xFF, 0xFF, 0xFF, 0xFF, 0x00],
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
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportDTCBySeverityMaskRecord',
                            'raw_value': 0x08,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x88,
                    'raw_value': 0x88,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'warningIndicatorRequested',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testNotCompletedThisOperationCycle',
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                    'physical_value': 0x1B,
                    'raw_value': 0x1B,
                    'unit': None
                },
                {
                    'children': (
                        (
                            {
                                'children': (
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'checkImmediately',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'checkAtNextHalt',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'maintenanceOnly',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_4',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_3',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_2',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_1',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_0',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    }
                                ),
                                'length': 8,
                                'name': 'DTCSeverity',
                                'physical_value': 0x00,
                                'raw_value': 0x00,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'FunctionalGroupIdentifier',
                                'physical_value': 0x01,
                                'raw_value': 0x01,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'P2334-56',
                                'raw_value': 0x233456,
                                'unit': None
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                    }
                                ),
                                'length': 8,
                                'name': 'DTCStatus',
                                'physical_value': 0x1B,
                                'raw_value': 0x1B,
                                'unit': None
                            }
                        ),
                        (
                            {
                                'children': (
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'checkImmediately',
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'checkAtNextHalt',
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'maintenanceOnly',
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_4',
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_3',
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_2',
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_1',
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_0',
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                    },
                                ),
                                'length': 8,
                                'name': 'DTCSeverity',
                                'physical_value': 0xFF,
                                'raw_value': 0xFF,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'FunctionalGroupIdentifier',
                                'physical_value': 'Emissions-system group',
                                'raw_value': 0x33,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'C389A-BC',
                                'raw_value': 0x789ABC,
                                'unit': None
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None},
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                'name': 'DTCStatus',
                                'physical_value': 0x01,
                                'raw_value': 0x01,
                                'unit': None
                            }
                        ),
                        (
                            {
                                'children': (
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'checkImmediately',
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'checkAtNextHalt',
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'maintenanceOnly',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_4',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_3',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_2',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_1',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_0',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    }
                                ),
                                'length': 8,
                                'name': 'DTCSeverity',
                                'physical_value': 0xC0,
                                'raw_value': 0xC0,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'FunctionalGroupIdentifier',
                                'physical_value': 'all',
                                'raw_value': 0xFF,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'U3FFF-FF',
                                'raw_value': 0xFFFFFF,
                                'unit': None
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    }
                                ),
                                'length': 8,
                                'name': 'DTCStatus',
                                'physical_value': 0x00,
                                'raw_value': 0x00,
                                'unit': None
                            }
                        )
            ),
                    'length': 48,
                    'name': 'Severity, Functional Unit, DTC and Status',
                    'physical_value': (0x00012334561B, 0xFF33789ABC01, 0xC0FFFFFFFF00),
                    'raw_value': (0x00012334561B, 0xFF33789ABC01, 0xC0FFFFFFFF00),
                    'unit': None
                }
            ),
        ),
        # reportSeverityInformationOfDTC (0x09)
        (
            [0x19, 0x89, 0x82, 0x3B, 0x95],
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
                            'physical_value': 'reportSeverityInformationOfDTC',
                            'raw_value': 0x09,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x89,
                    'raw_value': 0x89,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 24,
                    'name': 'DTC',
                    'physical_value': 'B023B-95',
                    'raw_value': 0x823B95,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x09, 0xFF],
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
                            'physical_value': 'reportSeverityInformationOfDTC',
                            'raw_value': 0x09,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x09,
                    'raw_value': 0x09,
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
                        }
                    ),
                    'length': 8,
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0xFF,
                    'raw_value': 0xFF,
                    'unit': None
                },
            ),
        ),
        # reportSupportedDTC (0x0A)
        (
            [0x19, 0x0A],
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportSupportedDTC',
                            'raw_value': 0x0A,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x0A,
                    'raw_value': 0x0A,
                    'unit': None
                },
            )
        ),
        (
            [0x59, 0x8A, 0xEF, 0x65, 0x87, 0xA9, 0xCB, 0xF0, 0xE1, 0xD2, 0xAA, 0x4A, 0x5B, 0x6C, 0x7D, 0xBF, 0xAE, 0x9D, 0x8C],
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
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportSupportedDTC',
                            'raw_value': 0x0A,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x8A,
                    'raw_value': 0x8A,
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
                    'physical_value': 0xEF,
                    'raw_value': 0xEF,
                    'unit': None
                },
                {
                    'children': (
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'C2587-A9',
                                'raw_value': 0x6587A9,
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
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                     }
                                ),
                                'length': 8,
                                'name': 'DTCStatus',
                                'physical_value': 0xCB,
                                'raw_value': 0xCB,
                                'unit': None,
                            }
                        ),
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'U30E1-D2',
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
                                'name': 'DTCStatus',
                                'physical_value': 0xAA,
                                'raw_value': 0xAA,
                                'unit': None,
                            }
                        ),
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'C0A5B-6C',
                                'raw_value': 0x4A5B6C,
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
                                'name': 'DTCStatus',
                                'physical_value': 0x7D,
                                'raw_value': 0x7D,
                                'unit': None,
                            }
                        ),
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'B3FAE-9D',
                                'raw_value': 0xBFAE9D,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                     }
                                ),
                                'length': 8,
                                'name': 'DTCStatus',
                                'physical_value': 0x8C,
                                'raw_value': 0x8C,
                                'unit': None,
                            }
                        ),
            ),
                    'length': 32,
                    'name': 'DTC and Status',
                    'physical_value': (0x6587A9CB, 0xF0E1D2AA, 0x4A5B6C7D, 0xBFAE9D8C),
                    'raw_value': (0x6587A9CB, 0xF0E1D2AA, 0x4A5B6C7D, 0xBFAE9D8C),
                    'unit': None
                },
            ),
        ),
        # reportFirstTestFailedDTC (0x0B)
        (
            [0x19, 0x8B],
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
                            'physical_value': 'reportFirstTestFailedDTC',
                            'raw_value': 0x0B,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x8B,
                    'raw_value': 0x8B,
                    'unit': None
                },
            )
        ),
        (
            [0x59, 0x0B, 0x89, 0x73, 0x94, 0xB5, 0x01],
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
                            'physical_value': 'reportFirstTestFailedDTC',
                            'raw_value': 0x0B,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x0B,
                    'raw_value': 0x0B,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailedThisOperationCycle',
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                    'physical_value': 0x89,
                    'raw_value': 0x89,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 24,
                            'name': 'DTC',
                            'physical_value': 'C3394-B5',
                            'raw_value': 0x7394B5,
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
                                    'physical_value': 'no',
                                    'raw_value': 0,
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
                                    'physical_value': 'no',
                                    'raw_value': 0,
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
                                    'physical_value': 'no',
                                    'raw_value': 0,
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
                            'name': 'DTCStatus',
                            'physical_value': 0x01,
                            'raw_value': 0x01,
                            'unit': None,
                        }
                    ),
                    'length': 32,
                    'name': 'DTC and Status',
                    'physical_value': 0x7394B501,
                    'raw_value': 0x7394B501,
                    'unit': None
                },
            ),
        ),
        # reportFirstConfirmedDTC (0x0C)
        (
            [0x19, 0x0C],
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportFirstConfirmedDTC',
                            'raw_value': 0x0C,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x0C,
                    'raw_value': 0x0C,
                    'unit': None
                },
            )
        ),
        (
            [0x59, 0x8C, 0x01],
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
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportFirstConfirmedDTC',
                            'raw_value': 0x0C,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x8C,
                    'raw_value': 0x8C,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'warningIndicatorRequested',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testNotCompletedThisOperationCycle',
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'pendingDTC',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailedThisOperationCycle',
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': None
                },
            ),
        ),
        # reportMostRecentTestFailedDTC (0x0D)
        (
            [0x19, 0x8D],
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
                            'physical_value': 'reportMostRecentTestFailedDTC',
                            'raw_value': 0x0D,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x8D,
                    'raw_value': 0x8D,
                    'unit': None
                },
            )
        ),
        (
            [0x59, 0x0D, 0x7F, 0xC8, 0xD7, 0xE6, 0x5F],
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
                            'physical_value': 'reportMostRecentTestFailedDTC',
                            'raw_value': 0x0D,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x0D,
                    'raw_value': 0x0D,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'warningIndicatorRequested',
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                        }
                    ),
                    'length': 8,
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0x7F,
                    'raw_value': 0x7F,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 24,
                            'name': 'DTC',
                            'physical_value': 'U08D7-E6',
                            'raw_value': 0xC8D7E6,
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
                                    'raw_value': 0x1,
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
                                 }
                            ),
                            'length': 8,
                            'name': 'DTCStatus',
                            'physical_value': 0x5F,
                            'raw_value': 0x5F,
                            'unit': None,
                        }
                    ),
                    'length': 32,
                    'name': 'DTC and Status',
                    'physical_value': 0xC8D7E65F,
                    'raw_value': 0xC8D7E65F,
                    'unit': None
                },
            ),
        ),
        # reportMostRecentConfirmedDTC (0x0E)
        (
            [0x19, 0x0E],
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportMostRecentConfirmedDTC',
                            'raw_value': 0x0E,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x0E,
                    'raw_value': 0x0E,
                    'unit': None
                },
            )
        ),
        (
            [0x59, 0x8E, 0x94, 0xB7, 0xD6, 0xF5, 0x14],
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
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportMostRecentConfirmedDTC',
                            'raw_value': 0x0E,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x8E,
                    'raw_value': 0x8E,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'confirmedDTC',
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailed',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0x94,
                    'raw_value': 0x94,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 24,
                            'name': 'DTC',
                            'physical_value': 'B37D6-F5',
                            'raw_value': 0xB7D6F5,
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
                                    'physical_value': 'no',
                                    'raw_value': 0,
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
                                    'raw_value': 0x1,
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
                                    'raw_value': 0x1,
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
                                    'physical_value': 'no',
                                    'raw_value': 0,
                                    'unit': None
                                 }
                            ),
                            'length': 8,
                            'name': 'DTCStatus',
                            'physical_value': 0x14,
                            'raw_value': 0x14,
                            'unit': None,
                        }
                    ),
                    'length': 32,
                    'name': 'DTC and Status',
                    'physical_value': 0xB7D6F514,
                    'raw_value': 0xB7D6F514,
                    'unit': None
                },
            ),
        ),
        # reportMirrorMemoryDTCByStatusMask (0x0F)
        (
            [0x19, 0x8F, 0x00],
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
                            'physical_value': 'reportMirrorMemoryDTCByStatusMask',
                            'raw_value': 0x0F,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x8F,
                    'raw_value': 0x8F,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'warningIndicatorRequested',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testNotCompletedThisOperationCycle',
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'pendingDTC',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailedThisOperationCycle',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailed',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'DTCStatusMask',
                    'physical_value': 0x00,
                    'raw_value': 0x00,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x0F, 0x22, 0x62, 0x85, 0xA8, 0x02, 0xAF, 0x81, 0x62, 0x20],
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
                            'physical_value': 'reportMirrorMemoryDTCByStatusMask',
                            'raw_value': 0x0F,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x0F,
                    'raw_value': 0x0F,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'warningIndicatorRequested',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testNotCompletedThisOperationCycle',
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'confirmedDTC',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'pendingDTC',
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0x22,
                    'raw_value': 0x22,
                    'unit': None
                },
                {
                    'children': (
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'C2285-A8',
                                'raw_value': 0x6285A8,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                'name': 'DTCStatus',
                                'physical_value': 0x02,
                                'raw_value': 0x02,
                                'unit': None,
                            }
                        ),
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'B2F81-62',
                                'raw_value': 0xAF8162,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                'name': 'DTCStatus',
                                'physical_value': 0x20,
                                'raw_value': 0x20,
                                'unit': None,
                            }
                        ),
            ),
                    'length': 32,
                    'name': 'DTC and Status',
                    'physical_value': (0x6285A802, 0xAF816220),
                    'raw_value': (0x6285A802, 0xAF816220),
                    'unit': None
                },
            ),
        ),
        # reportMirrorMemoryDTCExtDataRecordByDTCNumber (0x10)
        (
            [0x19, 0x10, 0x56, 0x43, 0x21, 0x30],
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportMirrorMemoryDTCExtDataRecordByDTCNumber',
                            'raw_value': 0x10,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x10,
                    'raw_value': 0x10,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 24,
                    'name': 'DTC',
                    'physical_value': 'C1643-21',
                    'raw_value': 0x564321,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCExtDataRecordNumber',
                    'physical_value': 0x30,
                    'raw_value': 0x30,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x90, 0x70, 0xF2, 0x44, 0x54, 0x25, 0xE2, 0x0D, 0x6A, 0x02, 0x50, 0xF4, 0xFE, 0x33],
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
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportMirrorMemoryDTCExtDataRecordByDTCNumber',
                            'raw_value': 0x10,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x90,
                    'raw_value': 0x90,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 24,
                            'name': 'DTC',
                            'physical_value': 'C30F2-44',
                            'raw_value': 0x70F244,
                            'unit': None,
                        },
                        {
                            'children': (
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'warningIndicatorRequested',
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
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
                                    'physical_value': 'yes',
                                    'raw_value': 0x1,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'confirmedDTC',
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
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
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'testFailed',
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
                                    'unit': None
                                },
                            ),
                            'length': 8,
                            'name': 'DTCStatus',
                            'physical_value': 0x54,
                            'raw_value': 0x54,
                            'unit': None,
                        },
                    ),
                    'length': 32,
                    'name': 'DTC and Status',
                    'physical_value': 0x70F24454,
                    'raw_value': 0x70F24454,
                    'unit': None,
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCExtDataRecordNumber#1',
                    'physical_value': 0x25,
                    'raw_value': 0x25,
                    'unit': None,
                },
                {
                    'children': ((), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'DTCExtDataRecord#1',
                    'physical_value': (0xE2, 0x0D, 0x6A, 0x02, 0x50, 0xF4, 0xFE, 0x33),
                    'raw_value': (0xE2, 0x0D, 0x6A, 0x02, 0x50, 0xF4, 0xFE, 0x33),
                    'unit': None,
                },
            ),
        ),
        # reportNumberOfMirrorMemoryDTCByStatusMask (0x11)
        (
            [0x19, 0x91, 0xA7],
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
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportNumberOfMirrorMemoryDTCByStatusMask',
                            'raw_value': 0x11,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x91,
                    'raw_value': 0x91,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'confirmedDTC',
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                    'physical_value': 0xA7,
                    'raw_value': 0xA7,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x11, 0xD2, 0x01, 0x80, 0x83],
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
                            'physical_value': 'reportNumberOfMirrorMemoryDTCByStatusMask',
                            'raw_value': 0x11,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x11,
                    'raw_value': 0x11,
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
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'confirmedDTC',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'pendingDTC',
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0xD2,
                    'raw_value': 0xD2,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCFormatIdentifier',
                    'physical_value': 'ISO 14229-1 DTC Format',
                    'raw_value': 0x01,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DTCCount',
                    'physical_value': 0x8083,
                    'raw_value': 0x8083,
                    'unit': 'DTCs'
                },

            ),
        ),
        # reportNumberOfEmissionsOBDDTCByStatusMask (0x12)
        (
            [0x19, 0x12, 0xAF],
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
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportNumberOfEmissionsOBDDTCByStatusMask',
                            'raw_value': 0x12,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x12,
                    'raw_value': 0x12,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                        },
                    ),
                    'length': 8,
                    'name': 'DTCStatusMask',
                    'physical_value': 0xAF,
                    'raw_value': 0xAF,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x92, 0xDD, 0x04, 0x82, 0x0C],
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
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportNumberOfEmissionsOBDDTCByStatusMask',
                            'raw_value': 0x12,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x92,
                    'raw_value': 0x92,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                    'physical_value': 0xDD,
                    'raw_value': 0xDD,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCFormatIdentifier',
                    'physical_value': "SAE J2012-DA DTC Format 04",
                    'raw_value': 0x04,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DTCCount',
                    'physical_value': 0x820C,
                    'raw_value': 0x820C,
                    'unit': 'DTCs'
                },

            ),
        ),
        # reportEmissionsOBDDTCByStatusMask (0x13)
        (
            [0x19, 0x93, 0xFB],
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
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportEmissionsOBDDTCByStatusMask',
                            'raw_value': 0x13,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x93,
                    'raw_value': 0x93,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                    'physical_value': 0xFB,
                    'raw_value': 0xFB,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x13, 0x5A, 0x2D, 0x68, 0x7F, 0x2B, 0x26, 0xE6, 0xC0, 0xCB, 0x33, 0xA6, 0x1E, 0x05, 0xD9, 0x2A, 0x02, 0xB5],
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
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportEmissionsOBDDTCByStatusMask',
                            'raw_value': 0x13,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x13,
                    'raw_value': 0x13,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'warningIndicatorRequested',
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0x5A,
                    'raw_value': 0x5A,
                    'unit': None
                },
                {
                    'children': (
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'P2D68-7F',
                                'raw_value': 0x2D687F,
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
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                     }
                                ),
                                'length': 8,
                                'name': 'DTCStatus',
                                'physical_value': 0x2B,
                                'raw_value': 0x2B,
                                'unit': None,
                            }
                        ),
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'P26E6-C0',
                                'raw_value': 0x26E6C0,
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
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                     }
                                ),
                                'length': 8,
                                'name': 'DTCStatus',
                                'physical_value': 0xCB,
                                'raw_value': 0xCB,
                                'unit': None,
                            }
                        ),
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'P33A6-1E',
                                'raw_value': 0x33A61E,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                'name': 'DTCStatus',
                                'physical_value': 0x05,
                                'raw_value': 0x05,
                                'unit': None,
                            }
                        ),
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'U192A-02',
                                'raw_value': 0xD92A02,
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
                                'name': 'DTCStatus',
                                'physical_value': 0xB5,
                                'raw_value': 0xB5,
                                'unit': None,
                            }
                        ),
            ),
                    'length': 32,
                    'name': 'DTC and Status',
                    'physical_value': (0x2D687F2B, 0x26E6C0CB, 0x33A61E05, 0xD92A02B5),
                    'raw_value': (0x2D687F2B, 0x26E6C0CB, 0x33A61E05, 0xD92A02B5),
                    'unit': None
                },
            ),
        ),
        # reportDTCFaultDetectionCounter (0x14)
        (
            [0x19, 0x14],
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportDTCFaultDetectionCounter',
                            'raw_value': 0x14,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x14,
                    'raw_value': 0x14,
                    'unit': None
                },
            )
        ),
        (
            [0x59, 0x94, 0x7B, 0x2B, 0x57, 0x73, 0x70, 0xED, 0xC4, 0xBC],
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
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportDTCFaultDetectionCounter',
                            'raw_value': 0x14,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x94,
                    'raw_value': 0x94,
                    'unit': None
                },
                {
                    'children': (
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'C3B2B-57',
                                'raw_value': 0x7B2B57,
                                'unit': None,
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'FaultDetectionCounter',
                                'physical_value': 0x73,
                                'raw_value': 0x73,
                                'unit': None,
                            }
                        ),
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'C30ED-C4',
                                'raw_value': 0x70EDC4,
                                'unit': None,
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'FaultDetectionCounter',
                                'physical_value': 0xBC,
                                'raw_value': 0xBC,
                                'unit': None,
                            }
                        ),
            ),
                    'length': 32,
                    'name': 'DTC and Fault Detection Counter',
                    'physical_value': (0x7B2B5773, 0x70EDC4BC),
                    'raw_value': (0x7B2B5773, 0x70EDC4BC),
                    'unit': None
                },
            ),
        ),
        # reportDTCWithPermanentStatus (0x15)
        (
            [0x19, 0x95],
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
                            'physical_value': 'reportDTCWithPermanentStatus',
                            'raw_value': 0x15,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x95,
                    'raw_value': 0x95,
                    'unit': None
                },
            )
        ),
        (
            [0x59, 0x15, 0xE6],
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
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportDTCWithPermanentStatus',
                            'raw_value': 0x15,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x15,
                    'raw_value': 0x15,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'confirmedDTC',
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0xE6,
                    'raw_value': 0xE6,
                    'unit': None
                },
            ),
        ),
        # reportDTCExtDataRecordByRecordNumber (0x16)
        (
            [0x19, 0x16, 0x54],
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportDTCExtDataRecordByRecordNumber',
                            'raw_value': 0x16,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x16,
                    'raw_value': 0x16,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCExtDataRecordNumber',
                    'physical_value': 0x54,
                    'raw_value': 0x54,
                    'unit': None
                },
            )
        ),
        (
            [0x59, 0x96, 0x6C, 0x1C, 0x54, 0x30, 0x09, 0xBD],
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
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportDTCExtDataRecordByRecordNumber',
                            'raw_value': 0x16,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x96,
                    'raw_value': 0x96,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCExtDataRecordNumber',
                    'physical_value': 0x6C,
                    'raw_value': 0x6C,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 24,
                            'name': 'DTC',
                            'physical_value': 'P1C54-30',
                            'raw_value': 0x1C5430,
                            'unit': None,
                        },
                        {
                            'children': (
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'warningIndicatorRequested',
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'testNotCompletedThisOperationCycle',
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
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
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'testFailedThisOperationCycle',
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
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
                            'name': 'DTCStatus',
                            'physical_value': 0x09,
                            'raw_value': 0x09,
                            'unit': None,
                        },
                    ),
                    'length': 32,
                    'name': 'DTC and Status#1',
                    'physical_value': 0x1C543009,
                    'raw_value': 0x1C543009,
                    'unit': None,
                },
                {
                    'children': ((),),
                    'length': 8,
                    'name': 'DTCExtDataRecord#1',
                    'physical_value': (0xBD,),
                    'raw_value': (0xBD,),
                    'unit': None,
                },
            ),
        ),
        # reportUserDefMemoryDTCByStatusMask (0x17)
        (
            [0x19, 0x97, 0xCB, 0xDB],
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
                            'physical_value': 'reportUserDefMemoryDTCByStatusMask',
                            'raw_value': 0x17,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x97,
                    'raw_value': 0x97,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                    'physical_value': 0xCB,
                    'raw_value': 0xCB,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'MemorySelection',
                    'physical_value': 0xDB,
                    'raw_value': 0xDB,
                    'unit': None
                },
            )
        ),
        (
            [0x59, 0x17, 0xC8, 0x01],
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
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportUserDefMemoryDTCByStatusMask',
                            'raw_value': 0x17,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x17,
                    'raw_value': 0x17,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'MemorySelection',
                    'physical_value': 0xC8,
                    'raw_value': 0xC8,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'warningIndicatorRequested',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testNotCompletedThisOperationCycle',
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'pendingDTC',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailedThisOperationCycle',
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': None
                },
            ),
        ),
        # reportUserDefMemoryDTCSnapshotRecordByDTCNumber (0x18)
        (
            [0x19, 0x18, 0xC3, 0x4A, 0xD8, 0xDF, 0xFD],
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportUserDefMemoryDTCSnapshotRecordByDTCNumber',
                            'raw_value': 0x18,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x18,
                    'raw_value': 0x18,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 24,
                    'name': 'DTC',
                    'physical_value': 'U034A-D8',
                    'raw_value': 0xC34AD8,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCSnapshotRecordNumber',
                    'physical_value': 0xDF,
                    'raw_value': 0xDF,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'MemorySelection',
                    'physical_value': 0xFD,
                    'raw_value': 0xFD,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x98, 0xED, 0xC6, 0x45, 0x03, 0x5A, 0xFE, 0x01, 0x28, 0x86, 0x23, 0x24, 0x8A],
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
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportUserDefMemoryDTCSnapshotRecordByDTCNumber',
                            'raw_value': 0x18,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x98,
                    'raw_value': 0x98,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'MemorySelection',
                    'physical_value': 0xED,
                    'raw_value': 0xED,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 24,
                            'name': 'DTC',
                            'physical_value': 'U0645-03',
                            'raw_value': 0xC64503,
                            'unit': None,
                        },
                        {
                            'children': (
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'warningIndicatorRequested',
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
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
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
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
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
                                    'unit': None
                                },
                            ),
                            'length': 8,
                            'name': 'DTCStatus',
                            'physical_value': 0x5A,
                            'raw_value': 0x5A,
                            'unit': None,
                        },
                    ),
                    'length': 32,
                    'name': 'DTC and Status',
                    'physical_value': 0xC645035A,
                    'raw_value': 0xC645035A,
                    'unit': None,
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCSnapshotRecordNumber#1',
                    'physical_value': 0xFE,
                    'raw_value': 0xFE,
                    'unit': None,
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DIDCount#1',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': 'DIDs',
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DID#1_1',
                    'physical_value': 0x2886,
                    'raw_value': 0x2886,
                    'unit': None,
                },
                {
                    'children': ((), (), ()),
                    'length': 8,
                    'name': 'DID#1_1 data',
                    'physical_value': (0x23, 0x24, 0x8A),
                    'raw_value': (0x23, 0x24, 0x8A),
                    'unit': None,
                },
            ),
        ),
        # reportUserDefMemoryDTCExtDataRecordByDTCNumber (0x19)
        (
            [0x19, 0x99, 0x7A, 0xE5, 0xF6, 0x6C, 0xD6],
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
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportUserDefMemoryDTCExtDataRecordByDTCNumber',
                            'raw_value': 0x19,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x99,
                    'raw_value': 0x99,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 24,
                    'name': 'DTC',
                    'physical_value': 'C3AE5-F6',
                    'raw_value': 0x7AE5F6,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCExtDataRecordNumber',
                    'physical_value': 0x6C,
                    'raw_value': 0x6C,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'MemorySelection',
                    'physical_value': 0xD6,
                    'raw_value': 0xD6,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x19, 0x88, 0xA8, 0x86, 0xA7, 0xA4, 0xD3, 0x6F, 0x14, 0x92, 0x01],
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
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportUserDefMemoryDTCExtDataRecordByDTCNumber',
                            'raw_value': 0x19,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x19,
                    'raw_value': 0x19,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'MemorySelection',
                    'physical_value': 0x88,
                    'raw_value': 0x88,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 24,
                            'name': 'DTC',
                            'physical_value': 'B2886-A7',
                            'raw_value': 0xA886A7,
                            'unit': None,
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
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
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
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'confirmedDTC',
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
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
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'testFailed',
                                    'physical_value': 'no',
                                    'raw_value': 0x0,
                                    'unit': None
                                },
                            ),
                            'length': 8,
                            'name': 'DTCStatus',
                            'physical_value': 0xA4,
                            'raw_value': 0xA4,
                            'unit': None,
                        },
                    ),
                    'length': 32,
                    'name': 'DTC and Status',
                    'physical_value': 0xA886A7A4,
                    'raw_value': 0xA886A7A4,
                    'unit': None,
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCExtDataRecordNumber',
                    'physical_value': 0xD3,
                    'raw_value': 0xD3,
                    'unit': None
                },
                {
                    'children': ((), (), (), ()),
                    'length': 8,
                    'name': 'DTCExtDataRecord#1',
                    'physical_value': (0x6F, 0x14, 0x92, 0x01),
                    'raw_value': (0x6F, 0x14, 0x92, 0x01),
                    'unit': None,
                },
            ),
        ),
        # reportWWHOBDDTCByMaskRecord (0x42)
        (
            [0x19, 0x42, 0xFF, 0x4D, 0xDD],
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportWWHOBDDTCByMaskRecord',
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
                    'name': 'FunctionalGroupIdentifier',
                    'physical_value': 'all',
                    'raw_value': 0xFF,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'warningIndicatorRequested',
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                    'physical_value': 0x4D,
                    'raw_value': 0x4D,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'checkImmediately',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'checkAtNextHalt',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'maintenanceOnly',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_4',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_3',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_2',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_1',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_0',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'DTCSeverityMask',
                    'physical_value': 0xDD,
                    'raw_value': 0xDD,
                    'unit': None
                },
            )
        ),
        (
            [0x59, 0xC2, 0xFE, 0x14, 0x06, 0x9C, 0x05, 0x11, 0x94, 0x59, 0xC6, 0xC0, 0x2C, 0x17, 0xD6, 0x6F, 0xD7, 0xB8, 0xB7, 0x9F, 0xC0],
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
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportWWHOBDDTCByMaskRecord',
                            'raw_value': 0x42,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0xC2,
                    'raw_value': 0xC2,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'FunctionalGroupIdentifier',
                    'physical_value': "VOBD system",
                    'raw_value': 0xFE,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'warningIndicatorRequested',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testNotCompletedThisOperationCycle',
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'confirmedDTC',
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'testFailed',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0x14,
                    'raw_value': 0x14,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'checkImmediately',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'checkAtNextHalt',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'maintenanceOnly',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_4',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_3',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_2',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_1',
                            'physical_value': 'yes',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_0',
                            'physical_value': 'no',
                            'raw_value': 0x0,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'DTCSeverityAvailabilityMask',
                    'physical_value': 0x06,
                    'raw_value': 0x06,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCFormatIdentifier',
                    'physical_value': 0x9C,
                    'raw_value': 0x9C,
                    'unit': None
                },
                {
                    'children': (
                        (
                            {
                                'children': (
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'checkImmediately',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'checkAtNextHalt',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'maintenanceOnly',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_4',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_3',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_2',
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_1',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_0',
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                    }
                                ),
                                'length': 8,
                                'name': 'DTCSeverity',
                                'physical_value': 0x05,
                                'raw_value': 0x05,
                                'unit': None,
                            },
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'P1194-59',
                                'raw_value': 0x119459,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                'name': 'DTCStatus',
                                'physical_value': 0xC6,
                                'raw_value': 0xC6,
                                'unit': None,
                            },
                        ),
                        (
                            {
                                'children': (
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'checkImmediately',
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'checkAtNextHalt',
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'maintenanceOnly',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_4',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_3',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_2',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_1',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_0',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    }
                                ),
                                'length': 8,
                                'name': 'DTCSeverity',
                                'physical_value': 0xC0,
                                'raw_value': 0xC0,
                                'unit': None,
                            },
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'P2C17-D6',
                                'raw_value': 0x2C17D6,
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
                                'name': 'DTCStatus',
                                'physical_value': 0x6F,
                                'raw_value': 0x6F,
                                'unit': None,
                            },
                        ),
                        (
                            {
                                'children': (
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'checkImmediately',
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'checkAtNextHalt',
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'maintenanceOnly',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_4',
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_3',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_2',
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_1',
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_0',
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                    }
                                ),
                                'length': 8,
                                'name': 'DTCSeverity',
                                'physical_value': 0xD7,
                                'raw_value': 0xD7,
                                'unit': None,
                            },
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'B38B7-9F',
                                'raw_value': 0xB8B79F,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                     }
                                ),
                                'length': 8,
                                'name': 'DTCStatus',
                                'physical_value': 0xC0,
                                'raw_value': 0xC0,
                                'unit': None,
                            },
                        ),
                    ),
                    'length': 40,
                    'name': 'Severity, DTC and DTC Status',
                    'physical_value': (0x05119459C6, 0xC02C17D66F, 0xD7B8B79FC0),
                    'raw_value': (0x05119459C6, 0xC02C17D66F, 0xD7B8B79FC0),
                    'unit': None
                },
            ),
        ),
        # reportWWHOBDDTCWithPermanentStatus (0x55)
        (
            [0x19, 0xD5, 0xD0],
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
                            'physical_value': 'reportWWHOBDDTCWithPermanentStatus',
                            'raw_value': 0x55,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0xD5,
                    'raw_value': 0xD5,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'FunctionalGroupIdentifier',
                    'physical_value': "Safety-system group",
                    'raw_value': 0xD0,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x55, 0xC6, 0xAD, 0xBB, 0x69, 0x2E, 0x89, 0xB9],
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
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportWWHOBDDTCWithPermanentStatus',
                            'raw_value': 0x55,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x55,
                    'raw_value': 0x55,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'FunctionalGroupIdentifier',
                    'physical_value': 0xC6,
                    'raw_value': 0xC6,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                            'physical_value': 'no',
                            'raw_value': 0x0,
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
                    'physical_value': 0xAD,
                    'raw_value': 0xAD,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCFormatIdentifier',
                    'physical_value': 0xBB,
                    'raw_value': 0xBB,
                    'unit': None
                },
                {
                    'children': (
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'C292E-89',
                                'raw_value': 0x692E89,
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
                                'name': 'DTCStatus',
                                'physical_value': 0xB9,
                                'raw_value': 0xB9,
                                'unit': None,
                            }
                        ),
                    ),
                    'length': 32,
                    'name': 'DTC and Status',
                    'physical_value': (0x692E89B9,),
                    'raw_value': (0x692E89B9,),
                    'unit': None
                },
            ),
        ),
    ])
    def test_decode(self, payload, decoded_message):
        print(f"payload = {bytes_to_hex(payload)}")
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
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 0,
                    "reportType": 0x02,
                },
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
                "SubFunction": 0x83,
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
                "DTC": 0x8090A0,
                "DTCSnapshotRecordNumber": 0x91,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x04, 0x80, 0x90, 0xA0, 0x91])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x04,
                },
                "DTC and Status": {
                    "DTC": 0xBEEF02,
                    "DTCStatus": {
                        "warningIndicatorRequested": 1,
                        "testNotCompletedThisOperationCycle": 0,
                        "testFailedSinceLastClear": 1,
                        "testNotCompletedSinceLastClear": 0,
                        "confirmedDTC": 1,
                        "pendingDTC": 0,
                        "testFailedThisOperationCycle": 1,
                        "testFailed": 1,
                    },
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
                "SubFunction": 0x05,
                "DTCStoredDataRecordNumber#1": 0x2E,
                "DTC and Status#1": {
                    "DTC": 0x987654,
                    "DTCStatus": {
                    "warningIndicatorRequested": 1,
                    "testNotCompletedThisOperationCycle": 0,
                    "testFailedSinceLastClear": 1,
                    "testNotCompletedSinceLastClear": 0,
                    "confirmedDTC": 1,
                    "pendingDTC": 0,
                    "testFailedThisOperationCycle": 1,
                    "testFailed": 1,
                    },
                },
                "DIDCount#1": 2,
                "DID#1_1": 0x0100,
                "DID#1_1 data": [0x68, 0x79],
                "DID#1_2": 0x0101,
                "DID#1_2 data": [0xD3],
                "DTCStoredDataRecordNumber#2": 0xF4,
                "DTC and Status#2": {
                    "DTC": 0x1F2E3D,
                    "DTCStatus": 0x6C,
                },
                "DIDCount#2": 1,
                "DID#2_1": 0x0102,
                "DID#2_1 data": [0xCA, 0xFF, 0xEE, 0x00, 0xBE, 0xEF],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x05,
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
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x06,
                },
                "DTC and Status": {
                    "DTC": 0x896C3B,
                    "DTCStatus": 0x5A,
                },
                "DTCExtDataRecordNumber#1": 0x01,
                "DTCExtDataRecord#1": [0x12, 0x34],
                "DTCExtDataRecordNumber#2": 0x02,
                "DTCExtDataRecord#2": [0x34, 0x56],
                "DTCExtDataRecordNumber#3": 0x43,
                "DTCExtDataRecord#3": [0x78, 0x9A, 0xBC, 0xDE, 0xF0],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x86,
                       0x89, 0x6C, 0x3B, 0x5A,  # DTC and Status
                       0x01, 0x12, 0x34,  # DTCExtendedDataRecord#1
                       0x02, 0x34, 0x56,  # DTCExtendedDataRecord#2
                       0x43, 0x78, 0x9A, 0xBC, 0xDE, 0xF0])  # DTCExtendedDataRecord#3
        ),
        # reportNumberOfDTCBySeverityMaskRecord (0x07)
        (
            {
                "SubFunction": 0x87,
                "DTCSeverityMask": {
                    "checkImmediately": 0,
                    "checkAtNextHalt": 0,
                    "maintenanceOnly": 1,
                    "DTCClass_4": 0,
                    "DTCClass_3": 1,
                    "DTCClass_2": 0,
                    "DTCClass_1": 1,
                    "DTCClass_0": 0,
                },
                "DTCStatusMask": 0x4B,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x87, 0x2A, 0x4B])
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
                "Severity, Functional Unit, DTC and Status": [
                    {
                        "DTCSeverity": 0xF0,
                        "FunctionalGroupIdentifier": 0xE1,
                        "DTC": 0xD2C3B4,
                        "DTCStatus": 0xA5
                    },
                    0x123456789ABC,
                    {
                        "DTCSeverity": 0x5A,
                        "FunctionalGroupIdentifier": 0x69,
                        "DTC": 0x987654,
                        "DTCStatus": 0x89
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
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 0,
                    "reportType": 0x09,
                },
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
                "Severity, Functional Unit, DTC and Status": {
                        "DTCSeverity": 0xF0,
                        "FunctionalGroupIdentifier": 0xE1,
                        "DTC": 0xD2C3B4,
                        "DTCStatus": 0xA5
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
                        "DTCStatus": 0x67,
                    },
                    0x89ABCDEF,
                    {
                        "DTC": 0xF1E2D3,
                        "DTCStatus": 0xFF,
                    },
                    {
                        "DTC": 0xC4B5A6,
                        "DTCStatus": 0x00,
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
                        "DTCStatus": 0x89,
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
                        "DTCStatus": 0x2B,
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
                        "DTCStatus": 0x67,
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
        (
            {
                "SubFunction": 0x10,
                "DTC": 0x0F1E2D,
                "DTCExtDataRecordNumber": 0x20
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x10, 0x0F, 0x1E, 0x2D, 0x20])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x10,
                },
                "DTC and Status": 0x123456AB,
                "DTCExtDataRecordNumber#1": 0x50,
                "DTCExtDataRecord#1": [0xF6],
                "DTCExtDataRecordNumber#2": 0x6D,
                "DTCExtDataRecord#2": [0xBE, 0xEF],
                "DTCExtDataRecordNumber#3": 0xC2,
                "DTCExtDataRecord#3": [0x73, 0x84, 0x95, 0xA6, 0xB7, 0xC8, 0xD9, 0xEA, 0xFB],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x90,
                       0x12, 0x34, 0x56, 0xAB,  # DTC and Status
                       0x50, 0xF6,  # DTCExtendedDataRecord#1
                       0x6D, 0xBE, 0xEF,  # DTCExtendedDataRecord#2
                       0xC2, 0x73, 0x84, 0x95, 0xA6, 0xB7, 0xC8, 0xD9, 0xEA, 0xFB])  # DTCExtendedDataRecord#3
        ),
        # reportNumberOfMirrorMemoryDTCByStatusMask (0x11)
        (
            {
                "SubFunction": 0x11,
                "DTCStatusMask": 0xB4,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x11, 0xB4])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 0,
                    "reportType": 0x12,
                },
                "DTCStatusAvailabilityMask": 0x00,
                "DTCFormatIdentifier": 0xFF,
                "DTCCount": 0xFFFF,
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x12, 0x00, 0xFF, 0xFF, 0xFF])
        ),
        # reportNumberOfEmissionsOBDDTCByStatusMask (0x12)
        (
            {
                "SubFunction": 0x12,
                "DTCStatusMask": 0xFB,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x12, 0xFB])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x12,
                },
                "DTCStatusAvailabilityMask": {
                    "warningIndicatorRequested": 1,
                    "testNotCompletedThisOperationCycle": 1,
                    "testFailedSinceLastClear": 1,
                    "testNotCompletedSinceLastClear": 0,
                    "confirmedDTC": 1,
                    "pendingDTC": 1,
                    "testFailedThisOperationCycle": 1,
                    "testFailed": 1,
                },
                "DTCFormatIdentifier": 0xA3,
                "DTCCount": 0x0000,
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x92, 0xEF, 0xA3, 0x00, 0x00])
        ),
        # reportEmissionsOBDDTCByStatusMask (0x13)
        (
            {
                "SubFunction": 0x13,
                "DTCStatusMask": 0xEA,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x13, 0xEA])
        ),
        (
            {
                "SubFunction": 0x93,
                "DTCStatusAvailabilityMask": 0xFF,
                "DTC and Status": [
                    {
                        "DTC": 0x102030,
                        "DTCStatus": {
                            "warningIndicatorRequested": 0,
                            "testNotCompletedThisOperationCycle": 0,
                            "testFailedSinceLastClear": 0,
                            "testNotCompletedSinceLastClear": 0,
                            "confirmedDTC": 0,
                            "pendingDTC": 0,
                            "testFailedThisOperationCycle": 0,
                            "testFailed": 0,
                        },
                    },
                    {
                        "DTC": 0x000001,
                        "DTCStatus": 0xFF,
                    },
                    0xF21D0CBF
                ],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x93, 0xFF,
                       0x10, 0x20, 0x30, 0x00,  # DTC and Status #1
                       0x00, 0x00, 0x01, 0xFF,  # DTC and Status #2
                       0xF2, 0x1D, 0x0C, 0xBF])  # DTC and Status #3
        ),
        # reportDTCFaultDetectionCounter (0x14)
        (
            {
                "SubFunction": 0x94,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x94])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 0,
                    "reportType": 0x14,
                },
                "DTC and Fault Detection Counter": [
                    {
                        "DTC": 0x000000,
                        "FaultDetectionCounter": 0x00,
                    },
                    {
                        "DTC": 0x896745,
                        "FaultDetectionCounter": 0x23,
                    },
                    0xFFFFFFFF
                ],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x14,
                       0x00, 0x00, 0x00, 0x00,  # DTC and Fault Detection Counter #1
                       0x89, 0x67, 0x45, 0x23,  # DTC and Fault Detection Counter #2
                       0xFF, 0xFF, 0xFF, 0xFF])  # DTC and Fault Detection Counter #3
        ),
        # reportDTCWithPermanentStatus (0x15)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x15,
                },
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x95])
        ),
        (
            {
                "SubFunction": 0x15,
                "DTCStatusAvailabilityMask": 0xED,
                "DTC and Status": [
                    {
                        "DTC": 0x000000,
                        "DTCStatus": {
                            "warningIndicatorRequested": 0,
                            "testNotCompletedThisOperationCycle": 0,
                            "testFailedSinceLastClear": 0,
                            "testNotCompletedSinceLastClear": 0,
                            "confirmedDTC": 0,
                            "pendingDTC": 0,
                            "testFailedThisOperationCycle": 0,
                            "testFailed": 0,
                        },
                    },
                    {
                        "DTC": 0x5A5A5A,
                        "DTCStatus": 0x6B,
                    },
                    0xFFFFFFFF
                ],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x15, 0xED,
                       0x00, 0x00, 0x00, 0x00,  # DTC and Status #1
                       0x5A, 0x5A, 0x5A, 0x6B,  # DTC and Status #2
                       0xFF, 0xFF, 0xFF, 0xFF])  # DTC and Status #3
        ),
        # reportDTCExtDataRecordByRecordNumber (0x16)
        (
            {
                "SubFunction": 0x16,
                "DTCExtDataRecordNumber": 0xFE,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x16, 0xFE])
        ),
        (
            {
                "SubFunction": 0x96,
                "DTCExtDataRecordNumber": 0xE2,
                "DTC and Status#1": {
                    "DTC": 0x3B896C,
                    "DTCStatus": 0xA5,
                },
                "DTCExtDataRecord#1": [0x21, 0x43, 0x68],
                "DTC and Status#2": 0xFECB9864,
                "DTCExtDataRecord#2": [0xCA, 0xFF, 0xEE],
                "DTC and Status#3":{
                    "DTC": 0x765432,
                    "DTCStatus": {
                        "warningIndicatorRequested": 0,
                        "testNotCompletedThisOperationCycle": 1,
                        "testFailedSinceLastClear": 0,
                        "testNotCompletedSinceLastClear": 1,
                        "confirmedDTC": 0,
                        "pendingDTC": 1,
                        "testFailedThisOperationCycle": 0,
                        "testFailed": 0,
                    },
                },
                "DTCExtDataRecord#3": [0xDA, 0xD0, 0x03],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x96, 0xE2,
                       0x3B, 0x89, 0x6C, 0xA5, 0x21, 0x43, 0x68,  # DTC, Status and ExtendedDataRecord #1
                       0xFE, 0xCB, 0x98, 0x64, 0xCA, 0xFF, 0xEE,  # DTC, Status and ExtendedDataRecord #2
                       0x76, 0x54, 0x32, 0x54, 0xDA, 0xD0, 0x03])  # DTC, Status and ExtendedDataRecord #3
        ),
        # reportUserDefMemoryDTCByStatusMask (0x17)
        (
            {
                "SubFunction": 0x17,
                "DTCStatusMask": 0x7D,
                "MemorySelection": 0x2D,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x17, 0x7D, 0x2D])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 0,
                    "reportType": 0x17,
                },
                "MemorySelection": 0x01,
                "DTCStatusAvailabilityMask": 0xEF,
                "DTC and Status": [
                    {
                        "DTC": 0xDADDEE,
                        "DTCStatus": {
                            "warningIndicatorRequested": 0,
                            "testNotCompletedThisOperationCycle": 1,
                            "testFailedSinceLastClear": 0,
                            "testNotCompletedSinceLastClear": 1,
                            "confirmedDTC": 0,
                            "pendingDTC": 1,
                            "testFailedThisOperationCycle": 0,
                            "testFailed": 0,
                        }
                    },
                    {
                        "DTC": 0xFBBEEF,
                        "DTCStatus": 0xC6,
                    },
                    0x9E8D7C6B,
                ],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x17, 0x01, 0xEF,
                       0xDA, 0xDD, 0xEE, 0x54,  # DTC and Status #1
                       0xFB, 0xBE, 0xEF, 0xC6, # DTC and Status #2
                       0x9E, 0x8D, 0x7C, 0x6B])  # DTC and Status #3
        ),
        # reportUserDefMemoryDTCSnapshotRecordByDTCNumber (0x18)
        (
            {
                "SubFunction": 0x18,
                "DTC": 0x103254,
                "DTCSnapshotRecordNumber": 0xE6,
                "MemorySelection": 0x1B,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x18, 0x10, 0x32, 0x54, 0xE6, 0x1B])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x18,
                },
                "MemorySelection": 0x7D,
                "DTC and Status": {
                    "DTC": 0xDEEDEE,
                    "DTCStatus": {
                        "warningIndicatorRequested": 0,
                        "testNotCompletedThisOperationCycle": 0,
                        "testFailedSinceLastClear": 0,
                        "testNotCompletedSinceLastClear": 0,
                        "confirmedDTC": 0,
                        "pendingDTC": 1,
                        "testFailedThisOperationCycle": 0,
                        "testFailed": 0,
                    },
                },
                "DTCSnapshotRecordNumber#1": 0x12,
                "DIDCount#1": 2,
                "DID#1_1": 0x210F,
                "DID#1_1 data": [0x00],
                "DID#1_2": 0x12E1,
                "DID#1_2 data": [0x51, 0x52, 0x53, 0x54],
                "DTCSnapshotRecordNumber#2": 0x00,
                "DIDCount#2": 1,
                "DID#2_1": 0x0123,
                "DID#2_1 data": [0x33, 0x44, 0x55],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x98, 0x7D,
                       0xDE, 0xED, 0xEE, 0x04,  # DTC and Status
                       0x12, 0x02, 0x21, 0x0F, 0x00, 0x12, 0xE1, 0x51, 0x52, 0x53, 0x54,  # DTCSnapshotRecord#1
                       0x00, 0x01, 0x01, 0x23, 0x33, 0x44, 0x55]), # DTCSnapshotRecord#2
        ),
        # reportUserDefMemoryDTCExtDataRecordByDTCNumber (0x19)
        (
            {
                "SubFunction": 0x19,
                "DTC": 0x65789A,
                "DTCExtDataRecordNumber": 0xFF,
                "MemorySelection": 0x01,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x19, 0x65, 0x78, 0x9A, 0xFF, 0x01])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x19,
                },
                "MemorySelection": 0x6E,
                "DTC and Status": {
                    "DTC": 0x3B896C,
                    "DTCStatus": 0xA5,
                },
                "DTCExtDataRecordNumber": 0x41,
                "DTCExtDataRecord#1": [0x21, 0x43],
                "DTCExtDataRecord#2": [0xF0, 0x0F],
                "DTCExtDataRecord#3": [0x78, 0x9A, 0xBC, 0xDE, 0xF0],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x99, 0x6E,
                       0x3B, 0x89, 0x6C, 0xA5,  # DTC and Status
                       0x41,  # DTCExtDataRecordNumber
                       0x21, 0x43,  # DTCExtendedDataRecord#1
                       0xF0, 0x0F,  # DTCExtendedDataRecord#2
                       0x78, 0x9A, 0xBC, 0xDE, 0xF0])  # DTCExtendedDataRecord#3
        ),
        # reportWWHOBDDTCByMaskRecord (0x42)
        (
            {
                "SubFunction": 0x42,
                "FunctionalGroupIdentifier": 0x25,
                "DTCStatusMask": 0xA3,
                "DTCSeverityMask": 0xBE,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x42, 0x25, 0xA3, 0xBE])
        ),
        (
            {
                "SubFunction": 0xC2,
                "FunctionalGroupIdentifier": 0xD0,
                "DTCStatusAvailabilityMask": {
                    "warningIndicatorRequested": 1,
                    "testNotCompletedThisOperationCycle": 0,
                    "testFailedSinceLastClear": 0,
                    "testNotCompletedSinceLastClear": 1,
                    "confirmedDTC": 1,
                    "pendingDTC": 1,
                    "testFailedThisOperationCycle": 1,
                    "testFailed": 1,
                },
                "DTCSeverityAvailabilityMask": {
                    "checkImmediately": 1,
                    "checkAtNextHalt": 1,
                    "maintenanceOnly": 1,
                    "DTCClass_4": 0,
                    "DTCClass_3": 0,
                    "DTCClass_2": 0,
                    "DTCClass_1": 1,
                    "DTCClass_0": 1,
                },
                "DTCFormatIdentifier": 0x54,
                "Severity, DTC and DTC Status": [
                    {
                        "DTCSeverity": {
                            "checkImmediately": 1,
                            "checkAtNextHalt": 0,
                            "maintenanceOnly": 0,
                            "DTCClass_4": 0,
                            "DTCClass_3": 0,
                            "DTCClass_2": 0,
                            "DTCClass_1": 1,
                            "DTCClass_0": 0,
                        },
                        "DTC": 0xCAFFEE,
                        "DTCStatus": {
                            "warningIndicatorRequested": 1,
                            "testNotCompletedThisOperationCycle": 0,
                            "testFailedSinceLastClear": 1,
                            "testNotCompletedSinceLastClear": 0,
                            "confirmedDTC": 1,
                            "pendingDTC": 0,
                            "testFailedThisOperationCycle": 1,
                            "testFailed": 1,
                        },
                    },
                    {
                        "DTCSeverity": 0x01,
                        "DTC": 0xBADDAD,
                        "DTCStatus": 0x03,
                    },
                    0x0FE12DC34B,
                ]
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0xC2, 0xD0, 0x9F, 0xE3, 0x54,
                       0x82, 0xCA, 0xFF, 0xEE, 0xAB,  # Severity, DTC and Status #1
                       0x01, 0xBA, 0xDD, 0xAD, 0x03,  # Severity, DTC and Status #2
                       0x0F, 0xE1, 0x2D, 0xC3, 0x4B])  # Severity, DTC and Status #3
        ),
        # reportWWHOBDDTCWithPermanentStatus (0x55)
        (
            {
                "SubFunction": 0x55,
                "FunctionalGroupIdentifier": 0xE0,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x55, 0xE0])
        ),
        (
            {
                "SubFunction": 0x55,
                "FunctionalGroupIdentifier": 0x33,
                "DTCStatusAvailabilityMask": 0xAB,
                "DTCFormatIdentifier": 0x02,
                "DTC and Status": [
                    {
                        "DTC": 0x214365,
                        "DTCStatus": 0x87,
                    },
                    0xEFCDAB89,
                    {
                        "DTC": 0x0F1E2D,
                        "DTCStatus": {
                            "warningIndicatorRequested": 0,
                            "testNotCompletedThisOperationCycle": 0,
                            "testFailedSinceLastClear": 1,
                            "testNotCompletedSinceLastClear": 1,
                            "confirmedDTC": 0,
                            "pendingDTC": 1,
                            "testFailedThisOperationCycle": 0,
                            "testFailed": 1,
                        },
                    },
                ],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x55, 0x33, 0xAB, 0x02,
                       0x21, 0x43, 0x65, 0x87,  # DTC and Status #1
                       0xEF, 0xCD, 0xAB, 0x89,  # DTC and Status #2
                       0x0F, 0x1E, 0x2D, 0x35])  # DTC and Status #3
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        print(f"SID = {sid}\nRSID = {rsid}\npayload = {bytes_to_hex(payload)}")
        assert READ_DTC_INFORMATION_2013.encode(data_records_values=data_records_values,
                                                sid=sid,
                                                rsid=rsid) == payload


@pytest.mark.integration
class TestReadDTCInformation2020Integration:
    """Integration tests for `ReadDTCInformation` service version 2020."""

    @pytest.mark.parametrize("payload, decoded_message", [
        # reportNumberOfDTCByStatusMask (0x01)
        (
            [0x19, 0x01, 0x00],
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
                            'physical_value': 'no',
                            'raw_value': 0,
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
                            'physical_value': 'no',
                            'raw_value': 0,
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
                            'physical_value': 'no',
                            'raw_value': 0,
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
                            'physical_value': 'no',
                            'raw_value': 0,
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
                            'physical_value': 'no',
                            'raw_value': 0,
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
                    'physical_value': 0x00,
                    'raw_value': 0x00,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x81, 0x13, 0x00, 0xB9, 0x10],
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
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportNumberOfDTCByStatusMask',
                            'raw_value': 0x01,
                            'unit': None
                        }
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
                            'physical_value': 'no',
                            'raw_value': 0,
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
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0x13,
                    'raw_value': 0x13,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCFormatIdentifier',
                    'physical_value': 'SAE J2012-DA DTC Format 00',
                    'raw_value': 0x00,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DTCCount',
                    'physical_value': 0xB910,
                    'raw_value': 0xB910,
                    'unit': 'DTCs'
                },

            ),
        ),
        # reportDTCByStatusMask (0x02)
        (
            [0x19, 0x82, 0x7E],
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
                            'raw_value': 1,
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
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'DTCStatusMask',
                    'physical_value': 0x7E,
                    'raw_value': 0x7E,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x02, 0x17],
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
                            'raw_value': 0,
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
                            'physical_value': 'no',
                            'raw_value': 0,
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
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0x17,
                    'raw_value': 0x17,
                    'unit': None
                },
            ),
        ),
        # reportDTCSnapshotIdentification (0x03)
        (
            [0x19, 0x03],
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
                            'physical_value': 'no',
                            'raw_value': 0,
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
                    'physical_value': 0x03,
                    'raw_value': 0x03,
                    'unit': None
                },
            )
        ),
        (
            [0x59, 0x83, 0x5D, 0xBB, 0xC9, 0x6A, 0xA6, 0x33, 0x1E, 0x84, 0x38, 0x11, 0x5F, 0x57, 0x66, 0x9D, 0xC4, 0xEA, 0x0A, 0xBA, 0x04, 0x45],
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
                            'physical_value': 'yes',
                            'raw_value': 1,
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
                    'physical_value': 0x83,
                    'raw_value': 0x83,
                    'unit': None
                },
                {
                    'children': (
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'C1DBB-C9',
                                'raw_value': 0x5DBBC9,
                                'unit': None,
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'DTCSnapshotRecordNumber',
                                'physical_value': 0x6A,
                                'raw_value': 0x6A,
                                'unit': None,
                            }
                        ),
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'B2633-1E',
                                'raw_value': 0xA6331E,
                                'unit': None,
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'DTCSnapshotRecordNumber',
                                'physical_value': 0x84,
                                'raw_value': 0x84,
                                'unit': None,
                            }
                        ),
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'P3811-5F',
                                'raw_value': 0x38115F,
                                'unit': None,
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'DTCSnapshotRecordNumber',
                                'physical_value': 0x57,
                                'raw_value': 0x57,
                                'unit': None,
                            }
                        ),
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'C269D-C4',
                                'raw_value': 0x669DC4,
                                'unit': None,
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'DTCSnapshotRecordNumber',
                                'physical_value': 0xEA,
                                'raw_value': 0xEA,
                                'unit': None,
                            }
                        ),
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'P0ABA-04',
                                'raw_value': 0x0ABA04,
                                'unit': None,
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'DTCSnapshotRecordNumber',
                                'physical_value': 0x45,
                                'raw_value': 0x45,
                                'unit': None,
                            }
                        ),
                    ),
                    'length': 32,
                    'name': 'DTC and Snapshot Record Number',
                    'physical_value': (0x5DBBC96A, 0xA6331E84, 0x38115F57, 0x669DC4EA, 0x0ABA0445),
                    'raw_value': (0x5DBBC96A, 0xA6331E84, 0x38115F57, 0x669DC4EA, 0x0ABA0445),
                    'unit': None
                },
            ),
        ),
        # reportDTCSnapshotRecordByDTCNumber (0x04)
        (
            [0x19, 0x84, 0xAC, 0x08, 0xA5, 0xFF],
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
                            'raw_value': 1,
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
                    'children': (),
                    'length': 24,
                    'name': 'DTC',
                    'physical_value': 'B2C08-A5',
                    'raw_value': 0xAC08A5,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCSnapshotRecordNumber',
                    'physical_value': 'all',
                    'raw_value': 0xFF,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x04, 0x73, 0xF7, 0xCF, 0x1F, 0x29, 0x01, 0x90, 0x11, 0xCF],
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
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportDTCSnapshotRecordByDTCNumber',
                            'raw_value': 0x04,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x04,
                    'raw_value': 0x04,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 24,
                            'name': 'DTC',
                            'physical_value': 'C33F7-CF',
                            'raw_value': 0x73F7CF,
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
                                    'physical_value': 'no',
                                    'raw_value': 0,
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
                            'name': 'DTCStatus',
                            'physical_value': 0x1F,
                            'raw_value': 0x1F,
                            'unit': None,
                        },
                    ),
                    'length': 32,
                    'name': 'DTC and Status',
                    'physical_value': 0x73F7CF1F,
                    'raw_value': 0x73F7CF1F,
                    'unit': None,
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCSnapshotRecordNumber#1',
                    'physical_value': 0x29,
                    'raw_value': 0x29,
                    'unit': None,
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DIDCount#1',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': 'DIDs',
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DID#1_1',
                    'physical_value': 0x9011,
                    'raw_value': 0x9011,
                    'unit': None,
                },
                {
                    'children': ((),),
                    'length': 8,
                    'name': 'DID#1_1 data',
                    'physical_value': (0xCF,),
                    'raw_value': (0xCF,),
                    'unit': None,
                },
            ),
        ),
        # reportDTCStoredDataByRecordNumber (0x05)
        (
            [0x19, 0x05, 0xFF],
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
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportDTCStoredDataByRecordNumber',
                            'raw_value': 0x05,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x05,
                    'raw_value': 0x05,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCStoredDataRecordNumber',
                    'physical_value': 'all',
                    'raw_value': 0xFF,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x85, 0xF6, 0x5A, 0x06, 0x99, 0xF0, 0x01, 0x7F, 0x1A, 0x1A, 0xE9, 0xBD, 0x63, 0xED, 0x42, 0x90],
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
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportDTCStoredDataByRecordNumber',
                            'raw_value': 0x05,
                            'unit': None
                        }
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
                    'name': 'DTCStoredDataRecordNumber#1',
                    'physical_value': 0xF6,
                    'raw_value': 0xF6,
                    'unit': None,
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 24,
                            'name': 'DTC',
                            'physical_value': 'C1A06-99',
                            'raw_value': 0x5A0699,
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
                                    'physical_value': 'no',
                                    'raw_value': 0,
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
                                    'physical_value': 'no',
                                    'raw_value': 0,
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
                            'name': 'DTCStatus',
                            'physical_value': 0xF0,
                            'raw_value': 0xF0,
                            'unit': None,
                        },
                    ),
                    'length': 32,
                    'name': 'DTC and Status#1',
                    'physical_value': 0x5A0699F0,
                    'raw_value': 0x5A0699F0,
                    'unit': None,
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DIDCount#1',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': 'DIDs',
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DID#1_1',
                    'physical_value': 0x7F1A,
                    'raw_value': 0x7F1A,
                    'unit': None,
                },
                {
                    'children': ((), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'DID#1_1 data',
                    'physical_value': (0x1A, 0xE9, 0xBD, 0x63, 0xED, 0x42, 0x90),
                    'raw_value': (0x1A, 0xE9, 0xBD, 0x63, 0xED, 0x42, 0x90),
                    'unit': None,
                },
            ),
        ),
        # reportDTCExtDataRecordByDTCNumber (0x06)
        (
            [0x19, 0x86, 0xDF, 0xAD, 0x70, 0x0B],
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
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportDTCExtDataRecordByDTCNumber',
                            'raw_value': 0x06,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x86,
                    'raw_value': 0x86,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 24,
                    'name': 'DTC',
                    'physical_value': 'U1FAD-70',
                    'raw_value': 0xDFAD70,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCExtDataRecordNumber',
                    'physical_value': 0x0B,
                    'raw_value': 0x0B,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x06, 0x4E, 0x78, 0x03, 0x0F, 0xA4, 0xA1],
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
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportDTCExtDataRecordByDTCNumber',
                            'raw_value': 0x06,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x06,
                    'raw_value': 0x06,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 24,
                            'name': 'DTC',
                            'physical_value': 'C0E78-03',
                            'raw_value': 0x4E7803,
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
                                    'physical_value': 'no',
                                    'raw_value': 0,
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
                            'name': 'DTCStatus',
                            'physical_value': 0x0F,
                            'raw_value': 0x0F,
                            'unit': None,
                        },
                    ),
                    'length': 32,
                    'name': 'DTC and Status',
                    'physical_value': 0x4E78030F,
                    'raw_value': 0x4E78030F,
                    'unit': None,
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCExtDataRecordNumber#1',
                    'physical_value': 0xA4,
                    'raw_value': 0xA4,
                    'unit': None,
                },
                {
                    'children': ((),),
                    'length': 8,
                    'name': 'DTCExtDataRecord#1',
                    'physical_value': (0xA1,),
                    'raw_value': (0xA1,),
                    'unit': None,
                },
            ),
        ),
        # reportNumberOfDTCBySeverityMaskRecord (0x07)
        (
            [0x19, 0x07, 0x99, 0xEB],
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
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportNumberOfDTCBySeverityMaskRecord',
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
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'checkImmediately',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'checkAtNextHalt',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'maintenanceOnly',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_4',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_3',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_2',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_1',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_0',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'DTCSeverityMask',
                    'physical_value': 0x99,
                    'raw_value': 0x99,
                    'unit': None
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
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'DTCStatusMask',
                    'physical_value': 0xEB,
                    'raw_value': 0xEB,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x87, 0x69, 0x01, 0x00, 0x2A],
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
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportNumberOfDTCBySeverityMaskRecord',
                            'raw_value': 0x07,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x87,
                    'raw_value': 0x87,
                    'unit': None
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
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0x69,
                    'raw_value': 0x69,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCFormatIdentifier',
                    'physical_value': 'ISO 14229-1 DTC Format',
                    'raw_value': 0x01,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DTCCount',
                    'physical_value': 0x002A,
                    'raw_value': 0x002A,
                    'unit': 'DTCs'
                },
            ),
        ),
        # reportDTCBySeverityMaskRecord (0x08)
        (
            [0x19, 0x88, 0x1D, 0xCB],
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
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportDTCBySeverityMaskRecord',
                            'raw_value': 0x08,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x88,
                    'raw_value': 0x88,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'checkImmediately',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'checkAtNextHalt',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'maintenanceOnly',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_4',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_3',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_2',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_1',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_0',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'DTCSeverityMask',
                    'physical_value': 0x1D,
                    'raw_value': 0x1D,
                    'unit': None
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
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'DTCStatusMask',
                    'physical_value': 0xCB,
                    'raw_value': 0xCB,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x08, 0x3C],
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
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportDTCBySeverityMaskRecord',
                            'raw_value': 0x08,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x08,
                    'raw_value': 0x08,
                    'unit': None
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
                            'physical_value': 'no',
                            'raw_value': 0,
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
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0x3C,
                    'raw_value': 0x3C,
                    'unit': None
                },
            ),
        ),
        # reportSeverityInformationOfDTC (0x09)
        (
            [0x19, 0x09, 0xF9, 0xFA, 0x2A],
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
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportSeverityInformationOfDTC',
                            'raw_value': 0x09,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x09,
                    'raw_value': 0x09,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 24,
                    'name': 'DTC',
                    'physical_value': 'U39FA-2A',
                    'raw_value': 0xF9FA2A,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x89, 0x7F, 0x0E, 0xD0, 0xBD, 0xBA, 0x0E, 0x58],
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
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportSeverityInformationOfDTC',
                            'raw_value': 0x09,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x89,
                    'raw_value': 0x89,
                    'unit': None
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
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0x7F,
                    'raw_value': 0x7F,
                    'unit': None
                },
                {
                    'children': (
                            {
                                'children': (
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'checkImmediately',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'checkAtNextHalt',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'maintenanceOnly',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_4',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_3',
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_2',
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_1',
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                    },
                                    {
                                        'children': (),
                                        'length': 1,
                                        'name': 'DTCClass_0',
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                    }
                                ),
                                'length': 8,
                                'name': 'DTCSeverity',
                                'physical_value': 0x0E,
                                'raw_value': 0x0E,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 8,
                                'name': 'FunctionalGroupIdentifier',
                                'physical_value': 'Safety-system group',
                                'raw_value': 0xD0,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'B3DBA-0E',
                                'raw_value': 0xBDBA0E,
                                'unit': None
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                'name': 'DTCStatus',
                                'physical_value': 0x58,
                                'raw_value': 0x58,
                                'unit': None
                            }
                    ),
                    'length': 48,
                    'name': 'Severity, Functional Unit, DTC and Status',
                    'physical_value': 0x0ED0BDBA0E58,
                    'raw_value': 0x0ED0BDBA0E58,
                    'unit': None
                }
            ),
        ),
        # reportSupportedDTC (0x0A)
        (
            [0x19, 0x8A],
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
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportSupportedDTC',
                            'raw_value': 0x0A,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x8A,
                    'raw_value': 0x8A,
                    'unit': None
                },
            )
        ),
        (
            [0x59, 0x0A, 0x3C, 0x0F, 0x54, 0x60, 0x06],
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
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportSupportedDTC',
                            'raw_value': 0x0A,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x0A,
                    'raw_value': 0x0A,
                    'unit': None
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
                            'physical_value': 'no',
                            'raw_value': 0,
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
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0x3C,
                    'raw_value': 0x3C,
                    'unit': None
                },
                {
                    'children': (
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'P0F54-60',
                                'raw_value': 0x0F5460,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                'name': 'DTCStatus',
                                'physical_value': 0x06,
                                'raw_value': 0x06,
                                'unit': None,
                            }
                        ),
                    ),
                    'length': 32,
                    'name': 'DTC and Status',
                    'physical_value': (0x0F546006,),
                    'raw_value': (0x0F546006,),
                    'unit': None
                },
            ),
        ),
        # reportFirstTestFailedDTC (0x0B)
        (
            [0x19, 0x0B],
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
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportFirstTestFailedDTC',
                            'raw_value': 0x0B,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x0B,
                    'raw_value': 0x0B,
                    'unit': None
                },
            )
        ),
        (
            [0x59, 0x8B, 0x9F, 0xEB, 0xC5, 0xF3, 0x04],
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
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportFirstTestFailedDTC',
                            'raw_value': 0x0B,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x8B,
                    'raw_value': 0x8B,
                    'unit': None
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
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0x9F,
                    'raw_value': 0x9F,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 24,
                            'name': 'DTC',
                            'physical_value': 'U2BC5-F3',
                            'raw_value': 0xEBC5F3,
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
                                    'physical_value': 'no',
                                    'raw_value': 0,
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
                                    'physical_value': 'no',
                                    'raw_value': 0,
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
                                    'physical_value': 'no',
                                    'raw_value': 0,
                                    'unit': None
                                 }
                            ),
                            'length': 8,
                            'name': 'DTCStatus',
                            'physical_value': 0x04,
                            'raw_value': 0x04,
                            'unit': None,
                        }
                    ),
                    'length': 32,
                    'name': 'DTC and Status',
                    'physical_value': 0xEBC5F304,
                    'raw_value': 0xEBC5F304,
                    'unit': None
                },
            ),
        ),
        # reportFirstConfirmedDTC (0x0C)
        (
            [0x19, 0x8C],
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
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportFirstConfirmedDTC',
                            'raw_value': 0x0C,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x8C,
                    'raw_value': 0x8C,
                    'unit': None
                },
            )
        ),
        (
            [0x59, 0x0C, 0xD7, 0xF4, 0x82, 0xFB, 0x05],
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
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportFirstConfirmedDTC',
                            'raw_value': 0x0C,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x0C,
                    'raw_value': 0x0C,
                    'unit': None
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
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0xD7,
                    'raw_value': 0xD7,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 24,
                            'name': 'DTC',
                            'physical_value': 'U3482-FB',
                            'raw_value': 0xF482FB,
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
                                    'physical_value': 'no',
                                    'raw_value': 0,
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
                                    'physical_value': 'no',
                                    'raw_value': 0,
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
                            'name': 'DTCStatus',
                            'physical_value': 0x05,
                            'raw_value': 0x05,
                            'unit': None,
                        }
                    ),
                    'length': 32,
                    'name': 'DTC and Status',
                    'physical_value': 0xF482FB05,
                    'raw_value': 0xF482FB05,
                    'unit': None
                },
            ),
        ),
        # reportMostRecentTestFailedDTC (0x0D)
        (
            [0x19, 0x0D],
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
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportMostRecentTestFailedDTC',
                            'raw_value': 0x0D,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x0D,
                    'raw_value': 0x0D,
                    'unit': None
                },
            )
        ),
        (
            [0x59, 0x8D, 0x14],
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
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportMostRecentTestFailedDTC',
                            'raw_value': 0x0D,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x8D,
                    'raw_value': 0x8D,
                    'unit': None
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
                            'physical_value': 'no',
                            'raw_value': 0,
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
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0x14,
                    'raw_value': 0x14,
                    'unit': None
                },
            ),
        ),
        # reportMostRecentConfirmedDTC (0x0E)
        (
            [0x19, 0x8E],
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
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportMostRecentConfirmedDTC',
                            'raw_value': 0x0E,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x8E,
                    'raw_value': 0x8E,
                    'unit': None
                },
            )
        ),
        (
            [0x59, 0x0E, 0xF1],
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
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportMostRecentConfirmedDTC',
                            'raw_value': 0x0E,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x0E,
                    'raw_value': 0x0E,
                    'unit': None
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
                            'physical_value': 'no',
                            'raw_value': 0,
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
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0xF1,
                    'raw_value': 0xF1,
                    'unit': None
                },
            ),
        ),
        # reportDTCFaultDetectionCounter (0x14)
        (
            [0x19, 0x94],
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
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportDTCFaultDetectionCounter',
                            'raw_value': 0x14,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x94,
                    'raw_value': 0x94,
                    'unit': None
                },
            )
        ),
        (
            [0x59, 0x14],
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
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportDTCFaultDetectionCounter',
                            'raw_value': 0x14,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x14,
                    'raw_value': 0x14,
                    'unit': None
                },
            ),
        ),
        # reportDTCWithPermanentStatus (0x15)
        (
            [0x19, 0x15],
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
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportDTCWithPermanentStatus',
                            'raw_value': 0x15,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x15,
                    'raw_value': 0x15,
                    'unit': None
                },
            )
        ),
        (
            [0x59, 0x95, 0x6C, 0xA7, 0xB5, 0x1C, 0x53, 0x02, 0x9C, 0xA4, 0x9C, 0xB2, 0x8B, 0x82, 0xAB],
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
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportDTCWithPermanentStatus',
                            'raw_value': 0x15,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x95,
                    'raw_value': 0x95,
                    'unit': None
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
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0x6C,
                    'raw_value': 0x6C,
                    'unit': None
                },
                {
                    'children': (
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'B27B5-1C',
                                'raw_value': 0xA7B51C,
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
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                     }
                                ),
                                'length': 8,
                                'name': 'DTCStatus',
                                'physical_value': 0x53,
                                'raw_value': 0x53,
                                'unit': None,
                            }
                        ),
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'P029C-A4',
                                'raw_value': 0x029CA4,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
                                        'unit': None
                                     }
                                ),
                                'length': 8,
                                'name': 'DTCStatus',
                                'physical_value': 0x9C,
                                'raw_value': 0x9C,
                                'unit': None,
                            }
                        ),
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'B328B-82',
                                'raw_value': 0xB28B82,
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
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                     }
                                ),
                                'length': 8,
                                'name': 'DTCStatus',
                                'physical_value': 0xAB,
                                'raw_value': 0xAB,
                                'unit': None,
                            }
                        ),
                    ),
                    'length': 32,
                    'name': 'DTC and Status',
                    'physical_value': (0xA7B51C53, 0x029CA49C, 0xB28B82AB),
                    'raw_value': (0xA7B51C53, 0x029CA49C, 0xB28B82AB),
                    'unit': None
                },
            ),
        ),
        # reportDTCExtDataRecordByRecordNumber (0x16)
        (
            [0x19, 0x96, 0xE2],
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
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportDTCExtDataRecordByRecordNumber',
                            'raw_value': 0x16,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x96,
                    'raw_value': 0x96,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCExtDataRecordNumber',
                    'physical_value': 0xE2,
                    'raw_value': 0xE2,
                    'unit': None
                },
            )
        ),
        (
            [0x59, 0x16, 0x19, 0xC2, 0x2F, 0x29, 0x7C, 0x35, 0x03, 0xAB, 0x14, 0x91, 0xF7, 0xA1, 0x09, 0x88, 0x70, 0xA1],
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
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportDTCExtDataRecordByRecordNumber',
                            'raw_value': 0x16,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x16,
                    'raw_value': 0x16,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCExtDataRecordNumber',
                    'physical_value': 0x19,
                    'raw_value': 0x19,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 24,
                            'name': 'DTC',
                            'physical_value': 'U022F-29',
                            'raw_value': 0xC22F29,
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
                                    'physical_value': 'no',
                                    'raw_value': 0,
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
                            'name': 'DTCStatus',
                            'physical_value': 0x7C,
                            'raw_value': 0x7C,
                            'unit': None,
                        },
                    ),
                    'length': 32,
                    'name': 'DTC and Status#1',
                    'physical_value': 0xC22F297C,
                    'raw_value': 0xC22F297C,
                    'unit': None,
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'DTCExtDataRecord#1',
                    'physical_value': (0x35, 0x03, 0xAB, 0x14, 0x91, 0xF7, 0xA1, 0x09, 0x88, 0x70, 0xA1),
                    'raw_value': (0x35, 0x03, 0xAB, 0x14, 0x91, 0xF7, 0xA1, 0x09, 0x88, 0x70, 0xA1),
                    'unit': None,
                },
            ),
        ),
        # reportUserDefMemoryDTCByStatusMask (0x17)
        (
            [0x19, 0x17, 0x2B, 0x69],
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
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportUserDefMemoryDTCByStatusMask',
                            'raw_value': 0x17,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x17,
                    'raw_value': 0x17,
                    'unit': None
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
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'DTCStatusMask',
                    'physical_value': 0x2B,
                    'raw_value': 0x2B,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'MemorySelection',
                    'physical_value': 0x69,
                    'raw_value': 0x69,
                    'unit': None
                },
            )
        ),
        (
            [0x59, 0x97, 0x24 ,0x19],
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
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportUserDefMemoryDTCByStatusMask',
                            'raw_value': 0x17,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x97,
                    'raw_value': 0x97,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'MemorySelection',
                    'physical_value': 0x24,
                    'raw_value': 0x24,
                    'unit': None
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
                            'physical_value': 'no',
                            'raw_value': 0,
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
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0x19,
                    'raw_value': 0x19,
                    'unit': None
                },
            ),
        ),
        # reportUserDefMemoryDTCSnapshotRecordByDTCNumber (0x18)
        (
            [0x19, 0x98, 0xCE, 0xD3, 0x11, 0xFF, 0xC2],
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
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportUserDefMemoryDTCSnapshotRecordByDTCNumber',
                            'raw_value': 0x18,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x98,
                    'raw_value': 0x98,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 24,
                    'name': 'DTC',
                    'physical_value': 'U0ED3-11',
                    'raw_value': 0xCED311,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCSnapshotRecordNumber',
                    'physical_value': 'all',
                    'raw_value': 0xFF,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'MemorySelection',
                    'physical_value': 0xC2,
                    'raw_value': 0xC2,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x18, 0x1B, 0x49, 0x2F, 0x60, 0x4F, 0x90, 0x01, 0x03, 0x74, 0x4B, 0xEB, 0xDB, 0x8E, 0x35],
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
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportUserDefMemoryDTCSnapshotRecordByDTCNumber',
                            'raw_value': 0x18,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x18,
                    'raw_value': 0x18,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'MemorySelection',
                    'physical_value': 0x1B,
                    'raw_value': 0x1B,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 24,
                            'name': 'DTC',
                            'physical_value': 'C092F-60',
                            'raw_value': 0x492F60,
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
                            'name': 'DTCStatus',
                            'physical_value': 0x4F,
                            'raw_value': 0x4F,
                            'unit': None,
                        },
                    ),
                    'length': 32,
                    'name': 'DTC and Status',
                    'physical_value': 0x492F604F,
                    'raw_value': 0x492F604F,
                    'unit': None,
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCSnapshotRecordNumber#1',
                    'physical_value': 0x90,
                    'raw_value': 0x90,
                    'unit': None,
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DIDCount#1',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': 'DIDs',
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DID#1_1',
                    'physical_value': 0x0374,
                    'raw_value': 0x0374,
                    'unit': None,
                },
                {
                    'children': ((), (), (), (), ()),
                    'length': 8,
                    'name': 'DID#1_1 data',
                    'physical_value': (0x4B, 0xEB, 0xDB, 0x8E, 0x35),
                    'raw_value': (0x4B, 0xEB, 0xDB, 0x8E, 0x35),
                    'unit': None,
                },
            ),
        ),
        # reportUserDefMemoryDTCExtDataRecordByDTCNumber (0x19)
        (
            [0x19, 0x19, 0xC9, 0x09, 0xB6, 0x24, 0xF4],
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
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportUserDefMemoryDTCExtDataRecordByDTCNumber',
                            'raw_value': 0x19,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x19,
                    'raw_value': 0x19,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 24,
                    'name': 'DTC',
                    'physical_value': 'U0909-B6',
                    'raw_value': 0xC909B6,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCExtDataRecordNumber',
                    'physical_value': 0x24,
                    'raw_value': 0x24,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'MemorySelection',
                    'physical_value': 0xF4,
                    'raw_value': 0xF4,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0x99, 0xD5, 0x0F, 0xEF, 0x53, 0xD3, 0x00, 0x7F, 0x81, 0xB6, 0x94, 0x27, 0x8E, 0x57, 0x1A, 0xE1, 0xB8],
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
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportUserDefMemoryDTCExtDataRecordByDTCNumber',
                            'raw_value': 0x19,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x99,
                    'raw_value': 0x99,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'MemorySelection',
                    'physical_value': 0xD5,
                    'raw_value': 0xD5,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 24,
                            'name': 'DTC',
                            'physical_value': 'P0FEF-53',
                            'raw_value': 0x0FEF53,
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
                                    'physical_value': 'yes',
                                    'raw_value': 1,
                                    'unit': None
                                },
                            ),
                            'length': 8,
                            'name': 'DTCStatus',
                            'physical_value': 0xD3,
                            'raw_value': 0xD3,
                            'unit': None,
                        },
                    ),
                    'length': 32,
                    'name': 'DTC and Status',
                    'physical_value': 0x0FEF53D3,
                    'raw_value': 0x0FEF53D3,
                    'unit': None,
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCExtDataRecordNumber',
                    'physical_value': 0x00,
                    'raw_value': 0x00,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'DTCExtDataRecord#1',
                    'physical_value': (0x7F, 0x81, 0xB6, 0x94, 0x27, 0x8E, 0x57, 0x1A, 0xE1, 0xB8),
                    'raw_value': (0x7F, 0x81, 0xB6, 0x94, 0x27, 0x8E, 0x57, 0x1A, 0xE1, 0xB8),
                    'unit': None,
                },
            ),
        ),
        # reportSupportedDTCExtDataRecord (0x1A)
        (
            [0x19, 0x9A, 0xD7],
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
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportSupportedDTCExtDataRecord',
                            'raw_value': 0x1A,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x9A,
                    'raw_value': 0x9A,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCExtDataRecordNumber',
                    'physical_value': 0xD7,
                    'raw_value': 0xD7,
                    'unit': None
                },
            )
        ),
        (
            [0x59, 0x1A, 0x91, 0xF1, 0x8F, 0x46, 0xD6, 0x85, 0xE4, 0x0D, 0x69, 0xC5, 0x41, 0x14, 0xDB, 0xBB],
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
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportSupportedDTCExtDataRecord',
                            'raw_value': 0x1A,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x1A,
                    'raw_value': 0x1A,
                    'unit': None
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
                            'physical_value': 'no',
                            'raw_value': 0,
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
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0x91,
                    'raw_value': 0x91,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCExtDataRecordNumber',
                    'physical_value': 0xF1,
                    'raw_value': 0xF1,
                    'unit': None
                },
                {
                    'children': (
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'B0F46-D6',
                                'raw_value': 0x8F46D6,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                'name': 'DTCStatus',
                                'physical_value': 0x85,
                                'raw_value': 0x85,
                                'unit': None,
                            }
                        ),
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'U240D-69',
                                'raw_value': 0xE40D69,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                'name': 'DTCStatus',
                                'physical_value': 0xC5,
                                'raw_value': 0xC5,
                                'unit': None,
                            }
                        ),
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'C0114-DB',
                                'raw_value': 0x4114DB,
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
                                        'physical_value': 'yes',
                                        'raw_value': 1,
                                        'unit': None
                                     }
                                ),
                                'length': 8,
                                'name': 'DTCStatus',
                                'physical_value': 0xBB,
                                'raw_value': 0xBB,
                                'unit': None,
                            }
                        ),
                    ),
                    'length': 32,
                    'name': 'DTC and Status',
                    'physical_value': (0x8F46D685, 0xE40D69C5, 0x4114DBBB),
                    'raw_value': (0x8F46D685, 0xE40D69C5, 0x4114DBBB),
                    'unit': None
                },
            ),
        ),
        # reportWWHOBDDTCByMaskRecord (0x42)
        (
            [0x19, 0xC2, 0xEC, 0xFE, 0x72],
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
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportWWHOBDDTCByMaskRecord',
                            'raw_value': 0x42,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0xC2,
                    'raw_value': 0xC2,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'FunctionalGroupIdentifier',
                    'physical_value': 0xEC,
                    'raw_value': 0xEC,
                    'unit': None
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
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'DTCStatusMask',
                    'physical_value': 0xFE,
                    'raw_value': 0xFE,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'checkImmediately',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'checkAtNextHalt',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'maintenanceOnly',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_4',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_3',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_2',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_1',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_0',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'DTCSeverityMask',
                    'physical_value': 0x72,
                    'raw_value': 0x72,
                    'unit': None
                },
            )
        ),
        (
            [0x59, 0x42, 0x92, 0xB1, 0x08, 0xE5],
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
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportWWHOBDDTCByMaskRecord',
                            'raw_value': 0x42,
                            'unit': None
                        }
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
                    'name': 'FunctionalGroupIdentifier',
                    'physical_value': 0x92,
                    'raw_value': 0x92,
                    'unit': None
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
                            'physical_value': 'no',
                            'raw_value': 0,
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
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0xB1,
                    'raw_value': 0xB1,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'checkImmediately',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'checkAtNextHalt',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'maintenanceOnly',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_4',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_3',
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_2',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_1',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 1,
                            'name': 'DTCClass_0',
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'DTCSeverityAvailabilityMask',
                    'physical_value': 0x08,
                    'raw_value': 0x08,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCFormatIdentifier',
                    'physical_value': 0xE5,
                    'raw_value': 0xE5,
                    'unit': None
                },
            ),
        ),
        # reportWWHOBDDTCWithPermanentStatus (0x55)
        (
            [0x19, 0x55, 0xEA],
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
                            'physical_value': 'no',
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportWWHOBDDTCWithPermanentStatus',
                            'raw_value': 0x55,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x55,
                    'raw_value': 0x55,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'FunctionalGroupIdentifier',
                    'physical_value': 0xEA,
                    'raw_value': 0xEA,
                    'unit': None
                }
            )
        ),
        (
            [0x59, 0xD5, 0x48, 0xAF, 0xF9],
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
                            'physical_value': 'yes',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportWWHOBDDTCWithPermanentStatus',
                            'raw_value': 0x55,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0xD5,
                    'raw_value': 0xD5,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'FunctionalGroupIdentifier',
                    'physical_value': 0x48,
                    'raw_value': 0x48,
                    'unit': None
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
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0xAF,
                    'raw_value': 0xAF,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCFormatIdentifier',
                    'physical_value': 0xF9,
                    'raw_value': 0xF9,
                    'unit': None
                },
            ),
        ),
        # reportDTCInformationByDTCReadinessGroupIdentifier (0x56)
        (
            [0x19, 0xD6, 0x94, 0x27],
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
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': "reportType",
                            'physical_value': 'reportDTCInformationByDTCReadinessGroupIdentifier',
                            'raw_value': 0x56,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0xD6,
                    'raw_value': 0xD6,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'FunctionalGroupIdentifier',
                    'physical_value': 0x94,
                    'raw_value': 0x94,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCReadinessGroupIdentifier',
                    'physical_value': 0x27,
                    'raw_value': 0x27,
                    'unit': None
                },
            )
        ),
        (
            [0x59, 0x56, 0x21, 0x32, 0x59, 0x59, 0x89, 0x79, 0xBA, 0x85, 0xEB, 0xC9, 0xEE, 0xC1, 0xF9, 0xD8, 0xEA, 0x86],
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
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'reportType',
                            'physical_value': 'reportDTCInformationByDTCReadinessGroupIdentifier',
                            'raw_value': 0x56,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x56,
                    'raw_value': 0x56,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'FunctionalGroupIdentifier',
                    'physical_value': 0x21,
                    'raw_value': 0x21,
                    'unit': None
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
                    'name': 'DTCStatusAvailabilityMask',
                    'physical_value': 0x32,
                    'raw_value': 0x32,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCFormatIdentifier',
                    'physical_value': 0x59,
                    'raw_value': 0x59,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'DTCReadinessGroupIdentifier',
                    'physical_value': 0x59,
                    'raw_value': 0x59,
                    'unit': None
                },
                {
                    'children': (
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'B0979-BA',
                                'raw_value': 0x8979BA,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                'name': 'DTCStatus',
                                'physical_value': 0x85,
                                'raw_value': 0x85,
                                'unit': None,
                            }
                        ),
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'U2BC9-EE',
                                'raw_value': 0xEBC9EE,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                'name': 'DTCStatus',
                                'physical_value': 0xC1,
                                'raw_value': 0xC1,
                                'unit': None,
                            }
                        ),
                        (
                            {
                                'children': (),
                                'length': 24,
                                'name': 'DTC',
                                'physical_value': 'U39D8-EA',
                                'raw_value': 0xF9D8EA,
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
                                        'physical_value': 'no',
                                        'raw_value': 0,
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
                                'name': 'DTCStatus',
                                'physical_value': 0x86,
                                'raw_value': 0x86,
                                'unit': None,
                            }
                        ),
                    ),
                    'length': 32,
                    'name': 'DTC and Status',
                    'physical_value': (0x8979BA85, 0xEBC9EEC1, 0xF9D8EA86),
                    'raw_value': (0x8979BA85, 0xEBC9EEC1, 0xF9D8EA86),
                    'unit': None
                },
            ),
        ),
    ])
    def test_decode(self, payload, decoded_message):
        print(f"payload = {bytes_to_hex(payload)}")
        assert READ_DTC_INFORMATION_2020.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        # reportNumberOfDTCByStatusMask (0x01)
        (
            {
                "SubFunction": 0x01,
                "DTCStatusMask": 0xFF,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x01, 0xFF])
        ),
        (
            {
                "SubFunction": 0x81,
                "DTCStatusAvailabilityMask": 0x00,
                "DTCFormatIdentifier": 0x00,
                "DTCCount": 0x0000,
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x81, 0x00, 0x00, 0x00, 0x00])
        ),
        # reportDTCByStatusMask (0x02)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x02,
                },
                "DTCStatusMask": 0x5A,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x82, 0x5A])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 0,
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
                "DTC and Status": [],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x02, 0x55])
        ),
        # reportDTCSnapshotIdentification (0x03)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x03,
                },
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x83])
        ),
        (
            {
                "SubFunction": 0x03,
                "DTC and Snapshot Record Number": [
                    {
                        "DTC": 0xA5B6C7,
                        "DTCSnapshotRecordNumber": 0x00
                    },
                    {
                        "DTC": 0xCAFFEE,
                        "DTCSnapshotRecordNumber": 0xFF
                    },
                ]
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x03, 0xA5, 0xB6, 0xC7, 0x00, 0xCA, 0xFF, 0xEE, 0xFF])
        ),
        # reportDTCSnapshotRecordByDTCNumber (0x04)
        (
            {
                "SubFunction": 0x04,
                "DTC": 0xB7A846,
                "DTCSnapshotRecordNumber": 0xFE,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x04, 0xB7, 0xA8, 0x46, 0xFE])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x04,
                },
                "DTC and Status": {
                    "DTC": 0xBEEF02,
                    "DTCStatus": {
                        "warningIndicatorRequested": 1,
                        "testNotCompletedThisOperationCycle": 0,
                        "testFailedSinceLastClear": 1,
                        "testNotCompletedSinceLastClear": 0,
                        "confirmedDTC": 1,
                        "pendingDTC": 0,
                        "testFailedThisOperationCycle": 1,
                        "testFailed": 1,
                    },
                },
                "DTCSnapshotRecordNumber#1": 0x3C,
                "DIDCount#1": 2,
                "DID#1_1": 0x0121,
                "DID#1_1 data": [0xF1, 0xE2],
                "DID#1_2": 0x0162,
                "DID#1_2 data": [0xD3],
                "DTCSnapshotRecordNumber#2": 0x40,
                "DIDCount#2": 1,
                "DID#2_1": 0x0183,
                "DID#2_1 data": [0xC4, 0xB5, 0xA6, 0x97, 0x88],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x84,
                       0xBE, 0xEF, 0x02, 0xAB,  # DTC and Status
                       0x3C, 0x02, 0x01, 0x21, 0xF1, 0xE2, 0x01, 0x62, 0xD3,  # DTCSnapshotRecord#1
                       0x40, 0x01, 0x01, 0x83, 0xC4, 0xB5, 0xA6, 0x97, 0x88]), # DTCSnapshotRecord#2
        ),
        # reportDTCStoredDataByRecordNumber (0x05)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x05,
                },
                "DTCStoredDataRecordNumber": 0x01
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x85, 0x01])
        ),
        (
            {
                "SubFunction": 0x05,
                "DTCStoredDataRecordNumber#1": 0xFF,
                "DTC and Status#1": {
                    "DTC": 0x987654,
                    "DTCStatus": {
                        "warningIndicatorRequested": 1,
                        "testNotCompletedThisOperationCycle": 1,
                        "testFailedSinceLastClear": 1,
                        "testNotCompletedSinceLastClear": 1,
                        "confirmedDTC": 1,
                        "pendingDTC": 1,
                        "testFailedThisOperationCycle": 1,
                        "testFailed": 1,
                    },
                },
                "DIDCount#1": 0x02,
                "DID#1_1": 0x0000,
                "DID#1_1 data": [0x68, 0x79],
                "DID#1_2": 0xFFFF,
                "DID#1_2 data": [0xD3],
                "DTCStoredDataRecordNumber#2": 0x00,
                "DTC and Status#2": 0xF1E2D3C4,
                "DIDCount#2": 0x01,
                "DID#2_1": 0x0102,
                "DID#2_1 data": [0xCA, 0xFF, 0xEE, 0x00, 0xBE, 0xEF],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x05,
                       0xFF, 0x98, 0x76, 0x54, 0xFF, 0x02, 0x00, 0x00, 0x68, 0x79, 0xFF, 0xFF, 0xD3,  # DTCStoredDataRecord#1
                       0x00, 0xF1, 0xE2, 0xD3, 0xC4, 0x01, 0x01, 0x02, 0xCA, 0xFF, 0xEE, 0x00, 0xBE, 0xEF])  # DTCStoredDataRecord#2
        ),
        # reportDTCExtDataRecordByDTCNumber (0x06)
        (
            {
                "SubFunction": 0x86,
                "DTC": 0x0000D0,
                "DTCExtDataRecordNumber": 0xFF
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x86, 0x00, 0x00, 0xD0, 0xFF])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 0,
                    "reportType": 0x06,
                },
                "DTC and Status": {
                    "DTC": 0x987654,
                    "DTCStatus": 0x00,
                },
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
                       0x98, 0x76, 0x54, 0x00,  # DTC and Status
                       0x01, 0x12, 0x34,  # DTCExtendedDataRecord#1
                       0x02, 0x34, 0x56,  # DTCExtendedDataRecord#2
                       0x43, 0x78, 0x9A, 0xBC, 0xDE, 0xF0])  # DTCExtendedDataRecord#3
        ),
        # reportNumberOfDTCBySeverityMaskRecord (0x07)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 0,
                    "reportType": 0x07,
                },
                "DTCSeverityMask": {
                    "checkImmediately": 1,
                    "checkAtNextHalt": 1,
                    "maintenanceOnly": 0,
                    "DTCClass_4": 1,
                    "DTCClass_3": 0,
                    "DTCClass_2": 1,
                    "DTCClass_1": 0,
                    "DTCClass_0": 1,
                },
                "DTCStatusMask": {
                    "warningIndicatorRequested": 1,
                    "testNotCompletedThisOperationCycle": 1,
                    "testFailedSinceLastClear": 0,
                    "testNotCompletedSinceLastClear": 1,
                    "confirmedDTC": 1,
                    "pendingDTC": 1,
                    "testFailedThisOperationCycle": 0,
                    "testFailed": 0,
                },
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x07, 0xD5, 0xDC])
        ),
        (
            {
                "SubFunction": 0x87,
                "DTCStatusAvailabilityMask": {
                    "warningIndicatorRequested": 0,
                    "testNotCompletedThisOperationCycle": 0,
                    "testFailedSinceLastClear": 0,
                    "testNotCompletedSinceLastClear": 0,
                    "confirmedDTC": 0,
                    "pendingDTC": 0,
                    "testFailedThisOperationCycle": 0,
                    "testFailed": 0,
                },
                "DTCFormatIdentifier": 0xFF,
                "DTCCount": 0xF01E,
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x87, 0x00, 0xFF, 0xF0, 0x1E])
        ),
        # reportDTCBySeverityMaskRecord (0x08)
        (
            {
                "SubFunction": 0x88,
                "DTCSeverityMask": 0x2E,
                "DTCStatusMask": 0xD3,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x88, 0x2E, 0xD3])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 0,
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
                "Severity, Functional Unit, DTC and Status": [
                    {
                        "DTCSeverity": {
                            "checkImmediately": 1,
                            "checkAtNextHalt": 1,
                            "maintenanceOnly": 1,
                            "DTCClass_4": 1,
                            "DTCClass_3": 0,
                            "DTCClass_2": 0,
                            "DTCClass_1": 0,
                            "DTCClass_0": 0,
                        },
                        "FunctionalGroupIdentifier": 0xE1,
                        "DTC": 0xD2C3B4,
                        "DTCStatus": {
                            "warningIndicatorRequested": 1,
                            "testNotCompletedThisOperationCycle": 0,
                            "testFailedSinceLastClear": 1,
                            "testNotCompletedSinceLastClear": 0,
                            "confirmedDTC": 0,
                            "pendingDTC": 1,
                            "testFailedThisOperationCycle": 0,
                            "testFailed": 1,
                        }
                    },
                    0x123456789ABC,
                    {
                        "DTCSeverity": 0x00,
                        "FunctionalGroupIdentifier": 0x00,
                        "DTC": 0x00FFFF,
                        "DTCStatus": 0xFF
                    },
                ]
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x08, 0xCC,
                       0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5,  # DTC Severity, DTC Functional Unit, DTC and DTC Status # 1
                       0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC,  # DTC Severity, DTC Functional Unit, DTC and DTC Status # 2
                       0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF])  # DTC Severity, DTC Functional Unit, DTC and DTC Status # 3
        ),
        # reportSeverityInformationOfDTC (0x09)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 0,
                    "reportType": 0x09,
                },
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
                    "warningIndicatorRequested": 1,
                    "testNotCompletedThisOperationCycle": 1,
                    "testFailedSinceLastClear": 0,
                    "testNotCompletedSinceLastClear": 0,
                    "confirmedDTC": 0,
                    "pendingDTC": 0,
                    "testFailedThisOperationCycle": 1,
                    "testFailed": 1,
                },
                "Severity, Functional Unit, DTC and Status": {
                        "DTCSeverity": 0xD9,
                        "FunctionalGroupIdentifier": 0xE2,
                        "DTC": 0x00FF00,
                        "DTCStatus": 0x01
                },
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x89, 0xC3, 0xD9, 0xE2, 0x00, 0xFF, 0x00, 0x01])
        ),
        # reportSupportedDTC (0x0A)
        (
            {
                "SubFunction": 0x8A,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x8A])
        ),
        (
            {
                "SubFunction": 0x0A,
                "DTCStatusAvailabilityMask": 0xB7,
                "DTC and Status": [
                    {
                        "DTC": 0x012345,
                        "DTCStatus": 0x67,
                    },
                    {
                        "DTC": 0xC4B5A6,
                        "DTCStatus": {
                            "warningIndicatorRequested": 0,
                            "testNotCompletedThisOperationCycle": 0,
                            "testFailedSinceLastClear": 0,
                            "testNotCompletedSinceLastClear": 0,
                            "confirmedDTC": 0,
                            "pendingDTC": 1,
                            "testFailedThisOperationCycle": 0,
                            "testFailed": 0,
                        },
                    },
                    0x9788796A,
                ]
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x0A, 0xB7,
                       0x01, 0x23, 0x45, 0x67,
                       0xC4, 0xB5, 0xA6, 0x04,
                       0x97, 0x88, 0x79, 0x6A])
        ),
        # reportFirstTestFailedDTC (0x0B)
        (
                {
                    "SubFunction": {
                        "suppressPosRspMsgIndicationBit": 0,
                        "reportType": 0x0B,
                    },
                },
                RequestSID.ReadDTCInformation,
                None,
                bytearray([0x19, 0x0B])
        ),
        (
            {
                "SubFunction": 0x8B,
                "DTCStatusAvailabilityMask": {
                    "warningIndicatorRequested": 1,
                    "testNotCompletedThisOperationCycle": 1,
                    "testFailedSinceLastClear": 1,
                    "testNotCompletedSinceLastClear": 1,
                    "confirmedDTC": 1,
                    "pendingDTC": 1,
                    "testFailedThisOperationCycle": 1,
                    "testFailed": 0,
                },
                "DTC and Status": {
                        "DTC": 0xF1E2D3,
                        "DTCStatus": 0x88,
                },
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x8B, 0xFE,
                       0xF1, 0xE2, 0xD3, 0x88])
        ),
        # reportFirstConfirmedDTC (0x0C)
        (
                {
                    "SubFunction": {
                        "suppressPosRspMsgIndicationBit": 1,
                        "reportType": 0x0C,
                    },
                },
                RequestSID.ReadDTCInformation,
                None,
                bytearray([0x19, 0x8C])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 0,
                    "reportType": 0x0C,
                },
                "DTCStatusAvailabilityMask": 0x25,
                "DTC and Status": None
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x0C, 0x25])
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
                    "testNotCompletedSinceLastClear": 1,
                    "confirmedDTC": 1,
                    "pendingDTC": 0,
                    "testFailedThisOperationCycle": 1,
                    "testFailed": 1,
                },
                "DTC and Status": {
                        "DTC": 0x5A6B7C,
                        "DTCStatus": 0x8F,
                },
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x8D, 0xBB,
                       0x5A, 0x6B, 0x7C, 0x8F])
        ),
        # reportMostRecentConfirmedDTC (0x0E)
        (
                {
                    "SubFunction": 0x8E,
                },
                RequestSID.ReadDTCInformation,
                None,
                bytearray([0x19, 0x8E])
        ),
        (
            {
                "SubFunction": 0x0E,
                "DTCStatusAvailabilityMask": 0xFF,
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x0E, 0xFF])
        ),
        # reportDTCFaultDetectionCounter (0x14)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 0,
                    "reportType": 0x14,
                },
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x14])
        ),
        (
            {
                "SubFunction": 0x94,
                "DTC and Fault Detection Counter": [
                    {
                        "DTC": 0x000000,
                        "FaultDetectionCounter": 0x00,
                    },
                    {
                        "DTC": 0xFFFFFF,
                        "FaultDetectionCounter": 0xFF,
                    },
                    0x12345678
                ],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x94,
                       0x00, 0x00, 0x00, 0x00,  # DTC and Fault Detection Counter #1
                       0xFF, 0xFF, 0xFF, 0xFF,  # DTC and Fault Detection Counter #2
                       0x12, 0x34, 0x56, 0x78])  # DTC and Fault Detection Counter #3
        ),
        # reportDTCWithPermanentStatus (0x15)
        (
            {
                "SubFunction": 0x95,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x95])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 0,
                    "reportType": 0x15,
                },
                "DTCStatusAvailabilityMask": 0xEF,
                "DTC and Status": [
                    {
                        "DTC": 0x000000,
                        "DTCStatus": {
                            "warningIndicatorRequested": 0,
                            "testNotCompletedThisOperationCycle": 0,
                            "testFailedSinceLastClear": 0,
                            "testNotCompletedSinceLastClear": 0,
                            "confirmedDTC": 0,
                            "pendingDTC": 0,
                            "testFailedThisOperationCycle": 0,
                            "testFailed": 0,
                        },
                    },
                    {
                        "DTC": 0x1AB630,
                        "DTCStatus": 0x96,
                    },
                    0xFFFFFFFF
                ],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x15, 0xEF,
                       0x00, 0x00, 0x00, 0x00,  # DTC and Status #1
                       0x1A, 0xB6, 0x30, 0x96,  # DTC and Status #2
                       0xFF, 0xFF, 0xFF, 0xFF])  # DTC and Status #3
        ),
        # reportDTCExtDataRecordByRecordNumber (0x16)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 0,
                    "reportType": 0x16,
                },
                "DTCExtDataRecordNumber": 0xFF,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x16, 0xFF])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x16,
                },
                "DTCExtDataRecordNumber": 0xFF,
                "DTC and Status#1": 0x3B896CA5,
                "DTCExtDataRecord#1": [0x21, 0x43, 0x68],
                "DTC and Status#2": {
                    "DTC": 0xFECB98,
                    "DTCStatus": 0x64,
                },
                "DTCExtDataRecord#2": [0xCA, 0xFF, 0xEE],
                "DTC and Status#3": {
                    "DTC": 0x765432,
                    "DTCStatus": {
                        "warningIndicatorRequested": 0,
                        "testNotCompletedThisOperationCycle": 1,
                        "testFailedSinceLastClear": 0,
                        "testNotCompletedSinceLastClear": 1,
                        "confirmedDTC": 0,
                        "pendingDTC": 1,
                        "testFailedThisOperationCycle": 0,
                        "testFailed": 0,
                    },
                },
                "DTCExtDataRecord#3": [0xDA],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x96, 0xFF,
                       0x3B, 0x89, 0x6C, 0xA5, 0x21, 0x43, 0x68,  # DTC, Status and ExtendedDataRecord #1
                       0xFE, 0xCB, 0x98, 0x64, 0xCA, 0xFF, 0xEE,  # DTC, Status and ExtendedDataRecord #2
                       0x76, 0x54, 0x32, 0x54, 0xDA])  # DTC, Status and ExtendedDataRecord #3
        ),
        # reportUserDefMemoryDTCByStatusMask (0x17)
        (
            {
                "SubFunction": 0x97,
                "DTCStatusMask": 0x01,
                "MemorySelection": 0xB0,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x97, 0x01, 0xB0])
        ),
        (
            {
                "SubFunction": 0x17,
                "MemorySelection": 0x0B,
                "DTCStatusAvailabilityMask": 0xFC,
                "DTC and Status": [
                    {
                        "DTC": 0xDADDEE,
                        "DTCStatus": {
                            "warningIndicatorRequested": 0,
                            "testNotCompletedThisOperationCycle": 1,
                            "testFailedSinceLastClear": 0,
                            "testNotCompletedSinceLastClear": 1,
                            "confirmedDTC": 0,
                            "pendingDTC": 1,
                            "testFailedThisOperationCycle": 0,
                            "testFailed": 0,
                        }
                    },
                    {
                        "DTC": 0xFBBEEF,
                        "DTCStatus": 0x58,
                    },
                    0x9E8D7C6B,
                ],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x17, 0x0B, 0xFC,
                       0xDA, 0xDD, 0xEE, 0x54,  # DTC and Status #1
                       0xFB, 0xBE, 0xEF, 0x58,  # DTC and Status #2
                       0x9E, 0x8D, 0x7C, 0x6B])  # DTC and Status #3
        ),
        # reportUserDefMemoryDTCSnapshotRecordByDTCNumber (0x18)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 0,
                    "reportType": 0x18,
                },
                "DTC": 0x325410,
                "DTCSnapshotRecordNumber": 0x4F,
                "MemorySelection": 0x1C,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x18, 0x32, 0x54, 0x10, 0x4F, 0x1C])
        ),
        (
            {
                "SubFunction": 0x98,
                "MemorySelection": 0x80,
                "DTC and Status": {
                    "DTC": 0xDEEDEE,
                    "DTCStatus": {
                        "warningIndicatorRequested": 0,
                        "testNotCompletedThisOperationCycle": 0,
                        "testFailedSinceLastClear": 0,
                        "testNotCompletedSinceLastClear": 0,
                        "confirmedDTC": 0,
                        "pendingDTC": 1,
                        "testFailedThisOperationCycle": 0,
                        "testFailed": 0,
                    },
                },
                "DTCSnapshotRecordNumber#1": 0xE1,
                "DIDCount#1": 2,
                "DID#1_1": 0x210F,
                "DID#1_1 data": [0x00],
                "DID#1_2": 0x12E1,
                "DID#1_2 data": [0x51, 0x52, 0x53, 0x54],
                "DTCSnapshotRecordNumber#2": 0x00,
                "DIDCount#2": 1,
                "DID#2_1": 0x0123,
                "DID#2_1 data": [0x33, 0x44, 0x55],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x98, 0x80,
                       0xDE, 0xED, 0xEE, 0x04,  # DTC and Status
                       0xE1, 0x02, 0x21, 0x0F, 0x00, 0x12, 0xE1, 0x51, 0x52, 0x53, 0x54,  # DTCSnapshotRecord#1
                       0x00, 0x01, 0x01, 0x23, 0x33, 0x44, 0x55]), # DTCSnapshotRecord#2
        ),
        # reportUserDefMemoryDTCExtDataRecordByDTCNumber (0x19)
        (
            {
                "SubFunction": 0x99,
                "DTC": 0x65789A,
                "DTCExtDataRecordNumber": 0xFE,
                "MemorySelection": 0xFF,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x99, 0x65, 0x78, 0x9A, 0xFE, 0xFF])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 0,
                    "reportType": 0x19,
                },
                "MemorySelection": 0x0F,
                "DTC and Status": {
                    "DTC": 0xB398C6,
                    "DTCStatus": 0x5A,
                },
                "DTCExtDataRecordNumber": 0x41,
                "DTCExtDataRecord#1": [0x21, 0x43],
                "DTCExtDataRecord#2": [0x78, 0x9A, 0xBC, 0xDE, 0xF0],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x19, 0x0F,
                       0xB3, 0x98, 0xC6, 0x5A,  # DTC and Status
                       0x41,
                       0x21, 0x43,  # DTCExtendedDataRecord#1
                       0x78, 0x9A, 0xBC, 0xDE, 0xF0])  # DTCExtendedDataRecord#2
        ),
        # reportSupportedDTCExtDataRecord
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x1A,
                },
                "DTCExtDataRecordNumber": 0x01,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x9A, 0x01])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 0,
                    "reportType": 0x1A,
                },
                "DTCStatusAvailabilityMask": 0xFF,
                "DTCExtDataRecordNumber": 0xFD,
                "DTC and Status": [
                    {
                        "DTC": 0xBADDAD,
                        "DTCStatus": {
                            "warningIndicatorRequested": 0,
                            "testNotCompletedThisOperationCycle": 0,
                            "testFailedSinceLastClear": 0,
                            "testNotCompletedSinceLastClear": 0,
                            "confirmedDTC": 0,
                            "pendingDTC": 0,
                            "testFailedThisOperationCycle": 0,
                            "testFailed": 0,
                        },
                    },
                    {
                        "DTC": 0xDADDEE,
                        "DTCStatus": 0xFF,
                    },
                    0xFEDCBA98,
                ],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x1A, 0xFF, 0xFD,
                       0xBA, 0xDD, 0xAD, 0x00,  # DTC and Status #1
                       0xDA, 0xDD, 0xEE, 0xFF,  # DTC and Status #2
                       0xFE, 0xDC, 0xBA, 0x98])  # DTC and Status #3
        ),
        # reportWWHOBDDTCByMaskRecord (0x42)
        (
            {
                "SubFunction": 0xC2,
                "FunctionalGroupIdentifier": 0xFE,
                "DTCStatusMask": {
                    "warningIndicatorRequested": 0,
                    "testNotCompletedThisOperationCycle": 0,
                    "testFailedSinceLastClear": 0,
                    "testNotCompletedSinceLastClear": 0,
                    "confirmedDTC": 0,
                    "pendingDTC": 0,
                    "testFailedThisOperationCycle": 0,
                    "testFailed": 1,
                },
                "DTCSeverityMask": {
                    "checkImmediately": 1,
                    "checkAtNextHalt": 0,
                    "maintenanceOnly": 0,
                    "DTCClass_4": 0,
                    "DTCClass_3": 0,
                    "DTCClass_2": 0,
                    "DTCClass_1": 0,
                    "DTCClass_0": 0,
                },
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0xC2, 0xFE, 0x01, 0x80])
        ),
        (
            {
                "SubFunction": 0x42,
                "FunctionalGroupIdentifier": 0xD0,
                "DTCStatusAvailabilityMask": {
                    "warningIndicatorRequested": 1,
                    "testNotCompletedThisOperationCycle": 0,
                    "testFailedSinceLastClear": 0,
                    "testNotCompletedSinceLastClear": 1,
                    "confirmedDTC": 1,
                    "pendingDTC": 1,
                    "testFailedThisOperationCycle": 1,
                    "testFailed": 1,
                },
                "DTCSeverityAvailabilityMask": {
                    "checkImmediately": 0,
                    "checkAtNextHalt": 1,
                    "maintenanceOnly": 1,
                    "DTCClass_4": 1,
                    "DTCClass_3": 1,
                    "DTCClass_2": 1,
                    "DTCClass_1": 1,
                    "DTCClass_0": 1,
                },
                "DTCFormatIdentifier": 0x02,
                "Severity, DTC and DTC Status": [
                    {
                        "DTCSeverity": {
                            "checkImmediately": 1,
                            "checkAtNextHalt": 0,
                            "maintenanceOnly": 0,
                            "DTCClass_4": 1,
                            "DTCClass_3": 0,
                            "DTCClass_2": 0,
                            "DTCClass_1": 0,
                            "DTCClass_0": 0,
                        },
                        "DTC": 0xCAFFEE,
                        "DTCStatus": {
                            "warningIndicatorRequested": 1,
                            "testNotCompletedThisOperationCycle": 0,
                            "testFailedSinceLastClear": 1,
                            "testNotCompletedSinceLastClear": 0,
                            "confirmedDTC": 1,
                            "pendingDTC": 0,
                            "testFailedThisOperationCycle": 1,
                            "testFailed": 1,
                        },
                    },
                    {
                        "DTCSeverity": 0x2D,
                        "DTC": 0xF01ED2,
                        "DTCStatus": 0x3C,
                    },
                    0xB45A967878,
                ]
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x42, 0xD0, 0x9F, 0x7F, 0x02,
                       0x90, 0xCA, 0xFF, 0xEE, 0xAB,  # Severity, DTC and Status #1
                       0x2D, 0xF0, 0x1E, 0xD2, 0x3C,  # Severity, DTC and Status #2
                       0xB4, 0x5A, 0x96, 0x78, 0x78])  # Severity, DTC and Status #3
        ),
        # reportWWHOBDDTCWithPermanentStatus (0x55)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x55,
                },
                "FunctionalGroupIdentifier": 0xFE,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0xD5, 0xFE])
        ),
        (
            {
                "SubFunction": 0x55,
                "FunctionalGroupIdentifier": 0x33,
                "DTCStatusAvailabilityMask": 0x7E,
                "DTCFormatIdentifier": 0x04,
                "DTC and Status": [
                    {
                        "DTC": 0x214365,
                        "DTCStatus": 0x87,
                    },
                    0xEFCDAB89,
                    {
                        "DTC": 0x0F1E2D,
                        "DTCStatus": {
                            "warningIndicatorRequested": 0,
                            "testNotCompletedThisOperationCycle": 0,
                            "testFailedSinceLastClear": 1,
                            "testNotCompletedSinceLastClear": 1,
                            "confirmedDTC": 0,
                            "pendingDTC": 1,
                            "testFailedThisOperationCycle": 0,
                            "testFailed": 1,
                        },
                    },
                ],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0x55, 0x33, 0x7E, 0x04,
                       0x21, 0x43, 0x65, 0x87,  # DTC and Status #1
                       0xEF, 0xCD, 0xAB, 0x89,  # DTC and Status #2
                       0x0F, 0x1E, 0x2D, 0x35])  # DTC and Status #3
        ),
        # reportDTCInformationByDTCReadinessGroupIdentifier (0x56)
        (
            {
                "SubFunction": 0x56,
                "FunctionalGroupIdentifier": 0x00,
                "DTCReadinessGroupIdentifier": 0xD7,
            },
            RequestSID.ReadDTCInformation,
            None,
            bytearray([0x19, 0x56, 0x00, 0xD7])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": 1,
                    "reportType": 0x56,
                },
                "FunctionalGroupIdentifier": 0x00,
                "DTCStatusAvailabilityMask":0xFF,
                "DTCFormatIdentifier": 0x2D,
                "DTCReadinessGroupIdentifier": 0x16,
                "DTC and Status": [
                    0x192A3B4D,
                    {
                        "DTC": 0x0ECFE0,
                        "DTCStatus": 0x58,
                    }
                ],
            },
            None,
            ResponseSID.ReadDTCInformation,
            bytearray([0x59, 0xD6, 0x00, 0xFF, 0x2D, 0x16,
                       0x19, 0x2A, 0x3B, 0x4D,  # DTC and Status #1
                       0x0E, 0xCF, 0xE0, 0x58])  # DTC and Status #2
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        print(f"SID = {sid}\nRSID = {rsid}\npayload = {bytes_to_hex(payload)}")
        assert READ_DTC_INFORMATION_2020.encode(data_records_values=data_records_values,
                                                sid=sid,
                                                rsid=rsid) == payload

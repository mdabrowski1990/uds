import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.read_scaling_data_by_identifier import (
    READ_SCALING_DATA_BY_IDENTIFIER,
    READ_SCALING_DATA_BY_IDENTIFIER_2013,
    READ_SCALING_DATA_BY_IDENTIFIER_2020,
)


class TestReadScalingDataByIdentifier:
    """Unit tests for `ReadScalingDataByIdentifier` service."""

    def test_request_sid(self):
        assert READ_SCALING_DATA_BY_IDENTIFIER_2013.request_sid == RequestSID.ReadScalingDataByIdentifier
        assert READ_SCALING_DATA_BY_IDENTIFIER_2020.request_sid == RequestSID.ReadScalingDataByIdentifier

    def test_response_sid(self):
        assert READ_SCALING_DATA_BY_IDENTIFIER_2013.response_sid == ResponseSID.ReadScalingDataByIdentifier
        assert READ_SCALING_DATA_BY_IDENTIFIER_2020.response_sid == ResponseSID.ReadScalingDataByIdentifier

    def test_default_translator(self):
        assert READ_SCALING_DATA_BY_IDENTIFIER is READ_SCALING_DATA_BY_IDENTIFIER_2020


@pytest.mark.integration
class TestReadScalingDataByIdentifier2013Integration:
    """Integration tests for `ReadScalingDataByIdentifier` service version 2013."""

    @pytest.mark.parametrize("payload, decoded_message", [
        (
            [0x24, 0xF1, 0x88],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'ReadScalingDataByIdentifier',
                    'raw_value': 0x24,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DID',
                    'physical_value': "vehicleManufacturerECUSoftwareNumberDataIdentifier",
                    'raw_value': 0xF188,
                    'unit': None
                },
            )
        ),
        (
            [0x64, 0x42, 0xA8,
             0x04,
             0x11,
             0x23, 0xA5, 0xFE, 0xFF,
             0x3F,
             0x42,
             0x51,
             0x6A,
             0x74,
             0x8C,
             0x91, 0x08, 0x10, 0x01,
             0xA0, 0x43,
             0xB1, 0x23],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'ReadScalingDataByIdentifier',
                    'raw_value': 0x64,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DID',
                    'physical_value': 0x42A8,
                    'raw_value': 0x42A8,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'Type',
                            'physical_value': 'UnSignedNumeric',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'NumberOfBytes',
                            'physical_value': 4,
                            'raw_value': 0x4,
                            'unit': "bytes",
                        },
                    ),
                    'length': 8,
                    'name': 'scalingByte#1',
                    'physical_value': 0x04,
                    'raw_value': 0x04,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'Type',
                            'physical_value': 'SignedNumeric',
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'NumberOfBytes',
                            'physical_value': 1,
                            'raw_value': 0x1,
                            'unit': "bytes",
                        },
                    ),
                    'length': 8,
                    'name': 'scalingByte#2',
                    'physical_value': 0x11,
                    'raw_value': 0x11,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'Type',
                            'physical_value': 'BitMappedReportedWithOutMask',
                            'raw_value': 0x2,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'NumberOfBytes',
                            'physical_value': 3,
                            'raw_value': 0x3,
                            'unit': "bytes",
                        },
                    ),
                    'length': 8,
                    'name': 'scalingByte#3',
                    'physical_value': 0x23,
                    'raw_value': 0x23,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 24,
                            'name': 'ValidityMask',
                            'physical_value': 0xA5FEFF,
                            'raw_value': 0xA5FEFF,
                            'unit': None
                        },
                    ),
                    'length': 24,
                    'name': 'scalingByteExtension#3',
                    'physical_value': 0xA5FEFF,
                    'raw_value': 0xA5FEFF,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'Type',
                            'physical_value': 'BitMappedReportedWithMask',
                            'raw_value': 0x3,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'NumberOfBytes',
                            'physical_value': 15,
                            'raw_value': 0xF,
                            'unit': "bytes",
                        },
                    ),
                    'length': 8,
                    'name': 'scalingByte#4',
                    'physical_value': 0x3F,
                    'raw_value': 0x3F,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'Type',
                            'physical_value': 'BinaryCodedDecimal',
                            'raw_value': 0x4,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'NumberOfBytes',
                            'physical_value': 2,
                            'raw_value': 0x2,
                            'unit': "bytes",
                        },
                    ),
                    'length': 8,
                    'name': 'scalingByte#5',
                    'physical_value': 0x42,
                    'raw_value': 0x42,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'Type',
                            'physical_value': 'StateEncodedVariable',
                            'raw_value': 0x5,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'NumberOfBytes',
                            'physical_value': 1,
                            'raw_value': 0x1,
                            'unit': "bytes",
                        },
                    ),
                    'length': 8,
                    'name': 'scalingByte#6',
                    'physical_value': 0x51,
                    'raw_value': 0x51,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'Type',
                            'physical_value': 'ASCII',
                            'raw_value': 0x6,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'NumberOfBytes',
                            'physical_value': 10,
                            'raw_value': 0xA,
                            'unit': "bytes",
                        },
                    ),
                    'length': 8,
                    'name': 'scalingByte#7',
                    'physical_value': 0x6A,
                    'raw_value': 0x6A,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'Type',
                            'physical_value': 'SignedFloatingPoint',
                            'raw_value': 0x7,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'NumberOfBytes',
                            'physical_value': 4,
                            'raw_value': 0x4,
                            'unit': "bytes",
                        },
                    ),
                    'length': 8,
                    'name': 'scalingByte#8',
                    'physical_value': 0x74,
                    'raw_value': 0x74,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'Type',
                            'physical_value': 'Packet',
                            'raw_value': 0x8,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'NumberOfBytes',
                            'physical_value': 12,
                            'raw_value': 0xC,
                            'unit': "bytes",
                        },
                    ),
                    'length': 8,
                    'name': 'scalingByte#9',
                    'physical_value': 0x8C,
                    'raw_value': 0x8C,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'Type',
                            'physical_value': 'Formula',
                            'raw_value': 0x9,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'NumberOfBytes',
                            'physical_value': 1,
                            'raw_value': 0x1,
                            'unit': "bytes",
                        },
                    ),
                    'length': 8,
                    'name': 'scalingByte#10',
                    'physical_value': 0x91,
                    'raw_value': 0x91,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 8,
                            'name': 'FormulaIdentifier',
                            'physical_value': "y = x + C0",
                            'raw_value': 0x08,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'scalingByteExtension#10',
                    'physical_value': 0x08,
                    'raw_value': 0x08,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'Exponent',
                            'physical_value': 1,
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 12,
                            'name': 'Mantissa',
                            'physical_value': 1,
                            'raw_value': 0x001,
                            'unit': None
                        },
                    ),
                    'length': 16,
                    'name': 'C0#10',
                    'physical_value': 10,
                    'raw_value': 0x1001,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'Type',
                            'physical_value': 'Unit/Format',
                            'raw_value': 0xA,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'NumberOfBytes',
                            'physical_value': 0,
                            'raw_value': 0x0,
                            'unit': "bytes",
                        },
                    ),
                    'length': 8,
                    'name': 'scalingByte#11',
                    'physical_value': 0xA0,
                    'raw_value': 0xA0,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 8,
                            'name': 'Unit/Format',
                            'physical_value': "Giga (prefix) [G] - 10^9",
                            'raw_value': 0x43,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'scalingByteExtension#11',
                    'physical_value': 0x43,
                    'raw_value': 0x43,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'Type',
                            'physical_value': 'StateAndConnectionType',
                            'raw_value': 0xB,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'NumberOfBytes',
                            'physical_value': 1,
                            'raw_value': 0x1,
                            'unit': "bytes",
                        },
                    ),
                    'length': 8,
                    'name': 'scalingByte#12',
                    'physical_value': 0xB1,
                    'raw_value': 0xB1,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (
                                {
                                    'children': (),
                                    'length': 2,
                                    'name': 'SignalAccess',
                                    'physical_value': "Internal signal",
                                    'raw_value': 0x0,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 1,
                                    'name': 'SignalType',
                                    'physical_value': "Output signal",
                                    'raw_value': 0x1,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 2,
                                    'name': 'Signal',
                                    'physical_value': "Signal at low level (ground)",
                                    'raw_value': 0x0,
                                    'unit': None
                                },
                                {
                                    'children': (),
                                    'length': 3,
                                    'name': 'State',
                                    'physical_value': "Not available",
                                    'raw_value': 0x3,
                                    'unit': None
                                },
                            ),
                            'length': 8,
                            'name': 'StateAndConnectionType',
                            'physical_value': 0x23,
                            'raw_value': 0x23,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'scalingByteExtension#12',
                    'physical_value': 0x23,
                    'raw_value': 0x23,
                    'unit': None
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert READ_SCALING_DATA_BY_IDENTIFIER_2013.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        (
            {
                "DID": 0xF0E1,
            },
            RequestSID.ReadScalingDataByIdentifier,
            None,
            bytearray([0x24, 0xF0, 0xE1])
        ),
        (
            {
                "DID": 0xB9D3,
                "scalingByte#1": 0xB1,
                "scalingByteExtension#1": {
                    "StateAndConnectionType": {
                        "SignalAccess": 0x3,
                        "SignalType": 0x0,
                        "Signal": 0x1,
                        "State": 0x4,
                    },
                },
                "scalingByte#2": 0xA1,
                "scalingByteExtension#2": {
                    "Unit/Format": 0x02,
                },
                "scalingByte#3": 0x92,
                "scalingByteExtension#3": {
                    "FormulaIdentifier": 0x03
                },
                "C0#3": 0x2345,
                "C1#3": 0xFEDC,
                "scalingByte#4": 0x8C,
                "scalingByte#5": 0x78,
                "scalingByte#6": 0x6D,
                "scalingByte#7": 0x51,
                "scalingByte#8": 0x4E,
                "scalingByte#9": 0x31,
                "scalingByte#10": 0x21,
                "scalingByteExtension#10": {
                    "ValidityMask": 0x2F,
                },
                "scalingByte#11": 0x12,
                "scalingByte#12": 0x03,
            },
            None,
            ResponseSID.ReadScalingDataByIdentifier,
            bytearray([0x64, 0xB9, 0xD3,
                       0xB1, 0xCC,
                       0xA1, 0x02,
                       0x92, 0x03, 0x23, 0x45, 0xFE, 0xDC,
                       0x8C,
                       0x78,
                       0x6D,
                       0x51,
                       0x4E,
                       0x31,
                       0x21, 0x2F,
                       0x12,
                       0x03])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert READ_SCALING_DATA_BY_IDENTIFIER_2013.encode(data_records_values=data_records_values,
                                                           sid=sid,
                                                           rsid=rsid) == payload


@pytest.mark.integration
class TestReadScalingDataByIdentifier2020Integration:
    """Integration tests for `ClearDiagnosticInformation` service version 2020."""

    @pytest.mark.parametrize("payload, decoded_message", [
        (
            [0x24, 0xFF, 0x01],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'ReadScalingDataByIdentifier',
                    'raw_value': 0x24,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DID',
                    'physical_value': "ReservedForISO15765-5",
                    'raw_value': 0xFF01,
                    'unit': None
                },
            )
        ),
        (
            [0x64, 0x01, 0x00,
             0xA0, 0x4A,
             0xA0, 0x0E,
             0x92, 0x00, 0x00, 0x02, 0x10, 0x05],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'ReadScalingDataByIdentifier',
                    'raw_value': 0x64,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DID',
                    'physical_value': 0x0100,
                    'raw_value': 0x0100,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'Type',
                            'physical_value': 'Unit/Format',
                            'raw_value': 0xA,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'NumberOfBytes',
                            'physical_value': 0,
                            'raw_value': 0x0,
                            'unit': "bytes",
                        },
                    ),
                    'length': 8,
                    'name': 'scalingByte#1',
                    'physical_value': 0xA0,
                    'raw_value': 0xA0,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 8,
                            'name': 'Unit/Format',
                            'physical_value': "Milli (prefix) [m] - 10^-3",
                            'raw_value': 0x4A,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'scalingByteExtension#1',
                    'physical_value': 0x4A,
                    'raw_value': 0x4A,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'Type',
                            'physical_value': 'Unit/Format',
                            'raw_value': 0xA,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'NumberOfBytes',
                            'physical_value': 0,
                            'raw_value': 0x0,
                            'unit': "bytes",
                        },
                    ),
                    'length': 8,
                    'name': 'scalingByte#2',
                    'physical_value': 0xA0,
                    'raw_value': 0xA0,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 8,
                            'name': 'Unit/Format',
                            'physical_value': "Volt [V] - voltage",
                            'raw_value': 0x0E,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'scalingByteExtension#2',
                    'physical_value': 0x0E,
                    'raw_value': 0x0E,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'Type',
                            'physical_value': 'Formula',
                            'raw_value': 0x9,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'NumberOfBytes',
                            'physical_value': 2,
                            'raw_value': 0x2,
                            'unit': "bytes",
                        },
                    ),
                    'length': 8,
                    'name': 'scalingByte#3',
                    'physical_value': 0x92,
                    'raw_value': 0x92,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 8,
                            'name': 'FormulaIdentifier',
                            'physical_value': "y = C0 * x + C1",
                            'raw_value': 0x00,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'scalingByteExtension#3',
                    'physical_value': 0x00,
                    'raw_value': 0x00,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'Exponent',
                            'physical_value': 0,
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 12,
                            'name': 'Mantissa',
                            'physical_value': 2,
                            'raw_value': 0x002,
                            'unit': None
                        },
                    ),
                    'length': 16,
                    'name': 'C0#3',
                    'physical_value': 2,
                    'raw_value': 0x0002,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'Exponent',
                            'physical_value': 1,
                            'raw_value': 0x1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 12,
                            'name': 'Mantissa',
                            'physical_value': 5,
                            'raw_value': 0x005,
                            'unit': None
                        },
                    ),
                    'length': 16,
                    'name': 'C1#3',
                    'physical_value': 50,
                    'raw_value': 0x1005,
                    'unit': None
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert READ_SCALING_DATA_BY_IDENTIFIER_2020.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        (
            {
                "DID": 0xB6E9,
            },
            RequestSID.ReadScalingDataByIdentifier,
            None,
            bytearray([0x24, 0xB6, 0xE9])
        ),
        (
            {
                "DID": 0x306F,
                "scalingByte#1": 0xB1,
                "scalingByteExtension#1": {
                    "StateAndConnectionType": {
                        "SignalAccess": 0x1,
                        "SignalType": 0x1,
                        "Signal": 0x2,
                        "State": 0x0,
                    },
                },
                "scalingByte#2": 0xA3,
                "scalingByteExtension#2": {
                    "Unit/Format": 0x55,
                },
                "scalingByte#3": 0x91,
                "scalingByteExtension#3": {
                    "FormulaIdentifier": 0x06,
                },
                "C0#3": 0xF1E3,
                "scalingByte#4": 0x8B,
                "scalingByte#5": 0x74,
                "scalingByte#6": 0x6F,
                "scalingByte#7": 0x51,
                "scalingByte#8": 0x42,
                "scalingByte#9": 0x31,
                "scalingByte#10": 0x22,
                "scalingByteExtension#10": {
                    "ValidityMask": 0x2FFF,
                },
                "scalingByte#11": 0x11,
                "scalingByte#12": 0x02,
            },
            None,
            ResponseSID.ReadScalingDataByIdentifier,
            bytearray([0x64, 0x30, 0x6F,
                       0xB1, 0x70,
                       0xA3, 0x55,
                       0x91, 0x06, 0xF1, 0xE3,
                       0x8B,
                       0x74,
                       0x6F,
                       0x51,
                       0x42,
                       0x31,
                       0x22, 0x2F, 0xFF,
                       0x11,
                       0x02])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert READ_SCALING_DATA_BY_IDENTIFIER_2020.encode(data_records_values=data_records_values,
                                                           sid=sid,
                                                           rsid=rsid) == payload

import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.request_download import REQUEST_DOWNLOAD


class TestRequestDownload:
    """Unit tests for `RequestDownload` service."""

    def test_request_sid(self):
        assert REQUEST_DOWNLOAD.request_sid == RequestSID.RequestDownload

    def test_response_sid(self):
        assert REQUEST_DOWNLOAD.response_sid == ResponseSID.RequestDownload


@pytest.mark.integration
class TestRequestDownloadIntegration:
    """Integration tests for `RequestDownload` service."""

    @pytest.mark.parametrize("payload, decoded_message", [
        (
            [0x34, 0x00, 0x11, 0x23, 0x45],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'RequestDownload',
                    'raw_value': 0x34,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'compressionMethod',
                            'physical_value': "no compression",
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'encryptingMethod',
                            'physical_value': "no encryption",
                            'raw_value': 0x0,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'dataFormatIdentifier',
                    'physical_value': 0x00,
                    'raw_value': 0x00,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'memorySizeLength',
                            'physical_value': 0x1,
                            'raw_value': 0x1,
                            'unit': "bytes"
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'memoryAddressLength',
                            'physical_value': 0x1,
                            'raw_value': 0x1,
                            'unit': "bytes"
                        },
                    ),
                    'length': 8,
                    'name': 'addressAndLengthFormatIdentifier',
                    'physical_value': 0x11,
                    'raw_value': 0x11,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'memoryAddress',
                    'physical_value': 0x23,
                    'raw_value': 0x23,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'memorySize',
                    'physical_value': 0x45,
                    'raw_value': 0x45,
                    'unit': "bytes"
                },
            )
        ),
        (
            [0x34, 0xF1, 0x24, 0x80, 0x3C, 0x57, 0x7D, 0x97, 0xB1],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'RequestDownload',
                    'raw_value': 0x34,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'compressionMethod',
                            'physical_value': "compression #15",
                            'raw_value': 0xF,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'encryptingMethod',
                            'physical_value': "encryption #1",
                            'raw_value': 0x1,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'dataFormatIdentifier',
                    'physical_value': 0xF1,
                    'raw_value': 0xF1,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'memorySizeLength',
                            'physical_value': 0x2,
                            'raw_value': 0x2,
                            'unit': "bytes"
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'memoryAddressLength',
                            'physical_value': 0x4,
                            'raw_value': 0x4,
                            'unit': "bytes"
                        },
                    ),
                    'length': 8,
                    'name': 'addressAndLengthFormatIdentifier',
                    'physical_value': 0x24,
                    'raw_value': 0x24,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 32,
                    'name': 'memoryAddress',
                    'physical_value': 0x803C577D,
                    'raw_value': 0x803C577D,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'memorySize',
                    'physical_value': 0x97B1,
                    'raw_value': 0x97B1,
                    'unit': "bytes"
                },
            )
        ),
        (
            [0x74, 0x10, 0x08],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'RequestDownload',
                    'raw_value': 0x74,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'maxNumberOfBlockLengthBytesNumber',
                            'physical_value': 0x1,
                            'raw_value': 0x1,
                            'unit': "bytes"
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'reserved',
                            'physical_value': 0x0,
                            'raw_value': 0x0,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'lengthFormatIdentifier',
                    'physical_value': 0x10,
                    'raw_value': 0x10,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'maxNumberOfBlockLength',
                    'physical_value': 0x08,
                    'raw_value': 0x08,
                    'unit': "bytes"
                },
            )
        ),
        (
            [0x74, 0x3F, 0x1A, 0x0E, 0x3D],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'RequestDownload',
                    'raw_value': 0x74,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'maxNumberOfBlockLengthBytesNumber',
                            'physical_value': 0x3,
                            'raw_value': 0x3,
                            'unit': "bytes"
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'reserved',
                            'physical_value': 0xF,
                            'raw_value': 0xF,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'lengthFormatIdentifier',
                    'physical_value': 0x3F,
                    'raw_value': 0x3F,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 24,
                    'name': 'maxNumberOfBlockLength',
                    'physical_value': 0x1A0E3D,
                    'raw_value': 0x1A0E3D,
                    'unit': "bytes"
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert REQUEST_DOWNLOAD.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        (
            {
                "dataFormatIdentifier": 0x00,
                "addressAndLengthFormatIdentifier": 0x12,
                "memoryAddress": 0xFFFF,
                "memorySize": 0xED,
            },
            RequestSID.RequestDownload,
            None,
            bytearray([0x34, 0x00, 0x12, 0xFF, 0xFF, 0xED])
        ),
        (
            {
                "dataFormatIdentifier": {
                    "compressionMethod": 0xD,
                    "encryptingMethod": 0xE,
                },
                "addressAndLengthFormatIdentifier": {
                    "memorySizeLength": 0x6,
                    "memoryAddressLength": 0x5,
                },
                "memoryAddress": 0x1E0510888A,
                "memorySize": 0x0A959E715806,
            },
            RequestSID.RequestDownload,
            None,
            bytearray([0x34, 0xDE, 0x65, 0x1E, 0x05, 0x10, 0x88, 0x8A, 0x0A, 0x95, 0x9E, 0x71, 0x58, 0x06])
        ),
        (
            {
                "lengthFormatIdentifier": 0x20,
                "maxNumberOfBlockLength": 0x2344,
            },
            None,
            ResponseSID.RequestDownload,
            bytearray([0x74, 0x20, 0x23, 0x44])
        ),
        (
            {
                "lengthFormatIdentifier": {
                    "maxNumberOfBlockLengthBytesNumber": 0xA,
                    "reserved": 0x1,
                },
                "maxNumberOfBlockLength": 0x00B5A0027177757821DF,
            },
            None,
            ResponseSID.RequestDownload,
            bytearray([0x74, 0xA1, 0x00, 0xB5, 0xA0, 0x02, 0x71, 0x77, 0x75, 0x78, 0x21, 0xDF])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert REQUEST_DOWNLOAD.encode(data_records_values=data_records_values,
                                      sid=sid,
                                      rsid=rsid) == payload

import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.request_upload import REQUEST_UPLOAD


class TestRequestUpload:
    """Unit tests for `RequestUpload` service."""

    def test_request_sid(self):
        assert REQUEST_UPLOAD.request_sid == RequestSID.RequestUpload

    def test_response_sid(self):
        assert REQUEST_UPLOAD.response_sid == ResponseSID.RequestUpload


@pytest.mark.integration
class TestRequestUploadIntegration:
    """Integration tests for `RequestUpload` service."""

    @pytest.mark.parametrize("payload, decoded_message", [
        (
            [0x35, 0x00, 0x11, 0x5C, 0xAB],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'RequestUpload',
                    'raw_value': 0x35,
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
                    'physical_value': 0x5C,
                    'raw_value': 0x5C,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'memorySize',
                    'physical_value': 0xAB,
                    'raw_value': 0xAB,
                    'unit': "bytes"
                },
            )
        ),
        (
            [0x35, 0x2F, 0x24, 0x3F, 0x57, 0x8A, 0xE9, 0x11, 0xC0],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'RequestUpload',
                    'raw_value': 0x35,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'compressionMethod',
                            'physical_value': "compression #2",
                            'raw_value': 0x2,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'encryptingMethod',
                            'physical_value': "encryption #15",
                            'raw_value': 0xF,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'dataFormatIdentifier',
                    'physical_value': 0x2F,
                    'raw_value': 0x2F,
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
                    'physical_value': 0x3F578AE9,
                    'raw_value': 0x3F578AE9,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'memorySize',
                    'physical_value': 0x11C0,
                    'raw_value': 0x11C0,
                    'unit': "bytes"
                },
            )
        ),
        (
            [0x75, 0x10, 0x40],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'RequestUpload',
                    'raw_value': 0x75,
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
                    'physical_value': 0x40,
                    'raw_value': 0x40,
                    'unit': "bytes"
                },
            )
        ),
        (
            [0x75, 0x5F, 0x04, 0x36, 0xAC, 0x75, 0x1C],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'RequestUpload',
                    'raw_value': 0x75,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'maxNumberOfBlockLengthBytesNumber',
                            'physical_value': 0x5,
                            'raw_value': 0x5,
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
                    'physical_value': 0x5F,
                    'raw_value': 0x5F,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 40,
                    'name': 'maxNumberOfBlockLength',
                    'physical_value': 0x0436AC751C,
                    'raw_value': 0x0436AC751C,
                    'unit': "bytes"
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert REQUEST_UPLOAD.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        (
            {
                "dataFormatIdentifier": 0x00,
                "addressAndLengthFormatIdentifier": 0x12,
                "memoryAddress": 0x0000,
                "memorySize": 0xFF,
            },
            RequestSID.RequestUpload,
            None,
            bytearray([0x35, 0x00, 0x12, 0x00, 0x00, 0xFF])
        ),
        (
            {
                "dataFormatIdentifier": {
                    "compressionMethod": 0xC,
                    "encryptingMethod": 0x4,
                },
                "addressAndLengthFormatIdentifier": {
                    "memorySizeLength": 0x2,
                    "memoryAddressLength": 0x8,
                },
                "memoryAddress": 0x8E6703EA4A751A14,
                "memorySize": 0x63B0,
            },
            RequestSID.RequestUpload,
            None,
            bytearray([0x35, 0xC4, 0x28, 0x8E, 0x67, 0x03, 0xEA, 0x4A, 0x75, 0x1A, 0x14, 0x63, 0xB0])
        ),
        (
            {
                "lengthFormatIdentifier": 0x20,
                "maxNumberOfBlockLength": 0xAF7D,
            },
            None,
            ResponseSID.RequestUpload,
            bytearray([0x75, 0x20, 0xAF, 0x7D])
        ),
        (
            {
                "lengthFormatIdentifier": {
                    "maxNumberOfBlockLengthBytesNumber": 0x2,
                    "reserved": 0x8,
                },
                "maxNumberOfBlockLength": 0x0075,
            },
            None,
            ResponseSID.RequestUpload,
            bytearray([0x75, 0x28, 0x00, 0x75])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert REQUEST_UPLOAD.encode(data_records_values=data_records_values,
                                      sid=sid,
                                      rsid=rsid) == payload

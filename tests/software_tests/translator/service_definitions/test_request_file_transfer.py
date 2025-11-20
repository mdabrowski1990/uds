import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.request_file_transfer import (
    REQUEST_FILE_TRANSFER,
    REQUEST_FILE_TRANSFER_2013,
    REQUEST_FILE_TRANSFER_2020,
)


class TestRequestFileTransfer:
    """Unit tests for `RequestFileTransfer` service."""

    def test_request_sid(self):
        assert REQUEST_FILE_TRANSFER_2013.request_sid == RequestSID.RequestFileTransfer
        assert REQUEST_FILE_TRANSFER_2020.request_sid == RequestSID.RequestFileTransfer

    def test_response_sid(self):
        assert REQUEST_FILE_TRANSFER_2013.response_sid == ResponseSID.RequestFileTransfer
        assert REQUEST_FILE_TRANSFER_2020.response_sid == ResponseSID.RequestFileTransfer

    def test_default_translator(self):
        assert REQUEST_FILE_TRANSFER is REQUEST_FILE_TRANSFER_2020


@pytest.mark.integration
class TestRequestFileTransfer2013Integration:
    """Integration tests for `RequestFileTransfer` service version 2013."""

    @pytest.mark.parametrize("payload, decoded_message", [
        # AddFile (0x01)
        (
            [0x38, 0x01,
             0x00, 0x15, 0x63, 0x3A, 0x5C, 0x64, 0x69, 0x72, 0x65, 0x63, 0x74, 0x6F, 0x72, 0x79, 0x5C, 0x66, 0x69, 0x6C, 0x65, 0x2E, 0x74, 0x78, 0x74,
             0x00,
             0x02, 0x9E, 0x4D, 0x07, 0xEE],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'RequestFileTransfer',
                    'raw_value': 0x38,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'modeOfOperation',
                    'physical_value': "AddFile",
                    'raw_value': 0x01,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'filePathAndNameLength',
                    'physical_value': 0x0015,
                    'raw_value': 0x0015,
                    'unit': "bytes"
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'filePathAndName',
                    'physical_value': r"c:\directory\file.txt",
                    'raw_value': (0x63, 0x3A, 0x5C, 0x64, 0x69, 0x72, 0x65, 0x63, 0x74, 0x6F, 0x72, 0x79, 0x5C, 0x66, 0x69, 0x6C, 0x65, 0x2E, 0x74, 0x78, 0x74),
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'compressionMethod',
                            'physical_value': 'no compression',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'encryptingMethod',
                            'physical_value': 'no encryption',
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
                    'children': (),
                    'length': 8,
                    'name': 'fileSizeParameterLength',
                    'physical_value': 0x02,
                    'raw_value': 0x02,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'fileSizeUnCompressed',
                    'physical_value': 0x9E4D,
                    'raw_value': 0x9E4D,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'fileSizeCompressed',
                    'physical_value': 0x07EE,
                    'raw_value': 0x07EE,
                    'unit': "bytes"
                },
            )
        ),
        (
            [0x78, 0x01,
             0x02, 0xFD, 0x48,
             0xF1],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'RequestFileTransfer',
                    'raw_value': 0x78,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'modeOfOperation',
                    'physical_value': "AddFile",
                    'raw_value': 0x01,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'lengthFormatIdentifier',
                    'physical_value': 0x02,
                    'raw_value': 0x02,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'maxNumberOfBlockLength',
                    'physical_value': 0xFD48,
                    'raw_value': 0xFD48,
                    'unit': "bytes"
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'compressionMethod',
                            'physical_value': 'compression #15',
                            'raw_value': 0xF,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'encryptingMethod',
                            'physical_value': 'encryption #1',
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
            ),
        ),
        # DeleteFile (0x02)
        (
            [0x38, 0x02,
             0x00, 0x03, 0x41, 0x42, 0x43],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'RequestFileTransfer',
                    'raw_value': 0x38,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'modeOfOperation',
                    'physical_value': "DeleteFile",
                    'raw_value': 0x02,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'filePathAndNameLength',
                    'physical_value': 0x0003,
                    'raw_value': 0x0003,
                    'unit': "bytes"
                },
                {
                    'children': ((), (), ()),
                    'length': 8,
                    'name': 'filePathAndName',
                    'physical_value': r"ABC",
                    'raw_value': (0x41, 0x42, 0x43),
                    'unit': None
                },
            )
        ),
        (
            [0x78, 0x02],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'RequestFileTransfer',
                    'raw_value': 0x78,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'modeOfOperation',
                    'physical_value': "DeleteFile",
                    'raw_value': 0x02,
                    'unit': None
                },
            ),
        ),
        # ReplaceFile (0x03)
        (
            [0x38, 0x03,
             0x00, 0x1A, 0x2F, 0x75, 0x73, 0x72, 0x2F, 0x6C, 0x6F, 0x63, 0x61, 0x6C, 0x2F, 0x62, 0x69, 0x6E, 0x2F, 0x63, 0x6F, 0x6E, 0x66, 0x69, 0x67, 0x2E, 0x6A, 0x73, 0x6F, 0x6E,
             0x62,
             0x04, 0xFB, 0x2F, 0x3E, 0xB1, 0x70, 0xC5, 0x0F, 0x09],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'RequestFileTransfer',
                    'raw_value': 0x38,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'modeOfOperation',
                    'physical_value': "ReplaceFile",
                    'raw_value': 0x03,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'filePathAndNameLength',
                    'physical_value': 0x001A,
                    'raw_value': 0x001A,
                    'unit': "bytes"
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (),
                                 (), (), (), (), ()),
                    'length': 8,
                    'name': 'filePathAndName',
                    'physical_value': r"/usr/local/bin/config.json",
                    'raw_value': (0x2F, 0x75, 0x73, 0x72, 0x2F, 0x6C, 0x6F, 0x63, 0x61, 0x6C, 0x2F, 0x62, 0x69, 0x6E,
                                  0x2F, 0x63, 0x6F, 0x6E, 0x66, 0x69, 0x67, 0x2E, 0x6A, 0x73, 0x6F, 0x6E),
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'compressionMethod',
                            'physical_value': 'compression #6',
                            'raw_value': 0x6,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'encryptingMethod',
                            'physical_value': 'encryption #2',
                            'raw_value': 0x2,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'dataFormatIdentifier',
                    'physical_value': 0x62,
                    'raw_value': 0x62,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'fileSizeParameterLength',
                    'physical_value': 0x04,
                    'raw_value': 0x04,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 32,
                    'name': 'fileSizeUnCompressed',
                    'physical_value': 0xFB2F3EB1,
                    'raw_value': 0xFB2F3EB1,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 32,
                    'name': 'fileSizeCompressed',
                    'physical_value': 0x70C50F09,
                    'raw_value': 0x70C50F09,
                    'unit': "bytes"
                },
            )
        ),
        (
            [0x78, 0x03,
             0x01, 0xFF,
             0x00],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'RequestFileTransfer',
                    'raw_value': 0x78,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'modeOfOperation',
                    'physical_value': "ReplaceFile",
                    'raw_value': 0x03,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'lengthFormatIdentifier',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'maxNumberOfBlockLength',
                    'physical_value': 0xFF,
                    'raw_value': 0xFF,
                    'unit': "bytes"
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'compressionMethod',
                            'physical_value': 'no compression',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'encryptingMethod',
                            'physical_value': 'no encryption',
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
            ),
        ),
        # ReadFile (0x04)
        (
            [0x38, 0x04,
             0x00, 0x08, 0x66, 0x69, 0x6C, 0x65, 0x2E, 0x78, 0x79, 0x7A,
             0x00],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'RequestFileTransfer',
                    'raw_value': 0x38,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'modeOfOperation',
                    'physical_value': "ReadFile",
                    'raw_value': 0x04,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'filePathAndNameLength',
                    'physical_value': 0x0008,
                    'raw_value': 0x0008,
                    'unit': "bytes"
                },
                {
                    'children': ((), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'filePathAndName',
                    'physical_value': r"file.xyz",
                    'raw_value': (0x66, 0x69, 0x6C, 0x65, 0x2E, 0x78, 0x79, 0x7A),
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'compressionMethod',
                            'physical_value': 'no compression',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'encryptingMethod',
                            'physical_value': 'no encryption',
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
            )
        ),
        (
            [0x78, 0x04,
             0x04, 0x77, 0x2B, 0xC3, 0xA1,
             0x55,
             0x00, 0x01, 0xD6, 0x1B],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'RequestFileTransfer',
                    'raw_value': 0x78,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'modeOfOperation',
                    'physical_value': "ReadFile",
                    'raw_value': 0x04,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'lengthFormatIdentifier',
                    'physical_value': 0x04,
                    'raw_value': 0x04,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 32,
                    'name': 'maxNumberOfBlockLength',
                    'physical_value': 0x772BC3A1,
                    'raw_value': 0x772BC3A1,
                    'unit': "bytes"
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'compressionMethod',
                            'physical_value': 'compression #5',
                            'raw_value': 0x5,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'encryptingMethod',
                            'physical_value': 'encryption #5',
                            'raw_value': 0x5,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'dataFormatIdentifier',
                    'physical_value': 0x55,
                    'raw_value': 0x55,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'fileSizeOrDirInfoParameterLength',
                    'physical_value': 0x0001,
                    'raw_value': 0x0001,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'fileSizeUncompressedOrDirInfoLength',
                    'physical_value': 0xD6,
                    'raw_value': 0xD6,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'fileSizeCompressed',
                    'physical_value': 0x1B,
                    'raw_value': 0x1B,
                    'unit': "bytes"
                },
            ),
        ),
        # ReadDir (0x05)
        (
            [0x38, 0x05,
             0x00, 0x0A, 0x2F, 0x73, 0x6F, 0x6D, 0x65, 0x5F, 0x64, 0x69, 0x72, 0x2F],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'RequestFileTransfer',
                    'raw_value': 0x38,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'modeOfOperation',
                    'physical_value': "ReadDir",
                    'raw_value': 0x05,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'filePathAndNameLength',
                    'physical_value': 0x000A,
                    'raw_value': 0x000A,
                    'unit': "bytes"
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'filePathAndName',
                    'physical_value': r"/some_dir/",
                    'raw_value': (0x2F, 0x73, 0x6F, 0x6D, 0x65, 0x5F, 0x64, 0x69, 0x72, 0x2F),
                    'unit': None
                }
            )
        ),
        (
            [0x78, 0x05,
             0x02, 0x01, 0x00,
             0x00,
             0x00, 0x10, 0xC4, 0x8C, 0x57, 0x4A, 0x27, 0xF8, 0xFC, 0x7C, 0xD0, 0xD5, 0xF5, 0xD4, 0x9C, 0xEB, 0x93, 0x8B],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'RequestFileTransfer',
                    'raw_value': 0x78,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'modeOfOperation',
                    'physical_value': "ReadDir",
                    'raw_value': 0x05,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'lengthFormatIdentifier',
                    'physical_value': 0x02,
                    'raw_value': 0x02,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'maxNumberOfBlockLength',
                    'physical_value': 0x0100,
                    'raw_value': 0x0100,
                    'unit': "bytes"
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'compressionMethod',
                            'physical_value': 'no compression',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'encryptingMethod',
                            'physical_value': 'no encryption',
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
                    'children': (),
                    'length': 16,
                    'name': 'fileSizeOrDirInfoParameterLength',
                    'physical_value': 0x0010,
                    'raw_value': 0x0010,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 128,
                    'name': 'fileSizeUncompressedOrDirInfoLength',
                    'physical_value': 0xC48C574A27F8FC7CD0D5F5D49CEB938B,
                    'raw_value': 0xC48C574A27F8FC7CD0D5F5D49CEB938B,
                    'unit': "bytes"
                },
            ),
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert REQUEST_FILE_TRANSFER_2013.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        # AddFile (0x01)
        (
            {
                "modeOfOperation": 0x01,
                "filePathAndNameLength": 0x0001,
                "filePathAndName": 0x54,
                "dataFormatIdentifier": 0x39,
                "fileSizeParameterLength": 0x01,
                "fileSizeUnCompressed": 0x01,
                "fileSizeCompressed": 0x02,
            },
            RequestSID.RequestFileTransfer,
            None,
            bytearray([0x38, 0x01, 0x00, 0x01, 0x54, 0x39, 0x01, 0x01, 0x02])
        ),
        (
            {
                "modeOfOperation": 0x01,
                "lengthFormatIdentifier": 0x02,
                "maxNumberOfBlockLength": 0xFFFF,
                "dataFormatIdentifier": 0x00,
            },
            None,
            ResponseSID.RequestFileTransfer,
            bytearray([0x78, 0x01, 0x02, 0xFF, 0xFF, 0x00])
        ),
        # DeleteFile (0x02)
        (
            {
                "modeOfOperation": 0x02,
                "filePathAndNameLength": 0x0009,
                "filePathAndName": (0x73, 0x6F, 0x6D, 0x65, 0x5F, 0x70, 0x61, 0x74, 0x68),
            },
            RequestSID.RequestFileTransfer,
            None,
            bytearray([0x38, 0x02, 0x00, 0x09, 0x73, 0x6F, 0x6D, 0x65, 0x5F, 0x70, 0x61, 0x74, 0x68])
        ),
        (
            {
                "modeOfOperation": 0x02,
            },
            None,
            ResponseSID.RequestFileTransfer,
            bytearray([0x78, 0x02])
        ),
        # ReplaceFile (0x03)
        (
            {
                "modeOfOperation": 0x03,
                "filePathAndNameLength": 0x0010,
                "filePathAndName": (0x41, 0x52, 0x55, 0x5E, 0x59, 0x0C, 0x20, 0x54, 0x06, 0x46, 0x11, 0x39, 0x42, 0x13, 0x4A, 0x36),
                "dataFormatIdentifier": 0x00,
                "fileSizeParameterLength": 0x03,
                "fileSizeUnCompressed": 0x66F93A,
                "fileSizeCompressed": 0x9785,
            },
            RequestSID.RequestFileTransfer,
            None,
            bytearray([0x38, 0x03, 0x00, 0x10, 0x41, 0x52, 0x55, 0x5E, 0x59, 0x0C, 0x20, 0x54, 0x06, 0x46, 0x11, 0x39,
                       0x42, 0x13, 0x4A, 0x36, 0x00, 0x03, 0x66, 0xF9, 0x3A, 0x00, 0x97, 0x85])
        ),
        (
            {
                "modeOfOperation": 0x03,
                "lengthFormatIdentifier": 0x01,
                "maxNumberOfBlockLength": 0x58,
                "dataFormatIdentifier": 0x15,
            },
            None,
            ResponseSID.RequestFileTransfer,
            bytearray([0x78, 0x03, 0x01, 0x58, 0x15])
        ),
        # ReadFile (0x04)
        (
            {
                "modeOfOperation": 0x04,
                "filePathAndNameLength": 0x0004,
                "filePathAndName": (0x0D, 0x34, 0x1A, 0x6D),
                "dataFormatIdentifier": 0xDB,
            },
            RequestSID.RequestFileTransfer,
            None,
            bytearray([0x38, 0x04, 0x00, 0x04, 0x0D, 0x34, 0x1A, 0x6D, 0xDB])
        ),
        (
            {
                "modeOfOperation": 0x04,
                "lengthFormatIdentifier": 0x02,
                "maxNumberOfBlockLength": 0x56A5,
                "dataFormatIdentifier": 0xF3,
                "fileSizeOrDirInfoParameterLength": 0x0002,
                "fileSizeUncompressedOrDirInfoLength": 0x1F9D,
                "fileSizeCompressed": 0x50E5,
            },
            None,
            ResponseSID.RequestFileTransfer,
            bytearray([0x78, 0x04, 0x02, 0x56, 0xA5, 0xF3, 0x00, 0x02, 0x1F, 0x9D, 0x50, 0xE5])
        ),
        # ReadDir (0x05)
        (
            {
                "modeOfOperation": 0x05,
                "filePathAndNameLength": 0x0021,
                "filePathAndName": (0x41, 0x79, 0x33, 0x5A, 0x6A, 0x59, 0x67, 0x70, 0x5A, 0x5B, 0x37, 0x6E, 0x33, 0x58,
                                    0x5D, 0x7B, 0x77, 0x4E, 0x77, 0x3C, 0x37, 0x16, 0x54, 0x26, 0x5E, 0x71, 0x10, 0x25,
                                    0x43, 0x20, 0x12, 0x13, 0x37),
            },
            RequestSID.RequestFileTransfer,
            None,
            bytearray([0x38, 0x05, 0x00, 0x21, 0x41, 0x79, 0x33, 0x5A, 0x6A, 0x59, 0x67, 0x70, 0x5A, 0x5B, 0x37, 0x6E,
                       0x33, 0x58, 0x5D, 0x7B, 0x77, 0x4E, 0x77, 0x3C, 0x37, 0x16, 0x54, 0x26, 0x5E, 0x71, 0x10, 0x25,
                       0x43, 0x20, 0x12, 0x13, 0x37])
        ),
        (
            {
                "modeOfOperation": 0x05,
                "lengthFormatIdentifier": 0x01,
                "maxNumberOfBlockLength": 0xE5,
                "dataFormatIdentifier": 0x00,
                "fileSizeOrDirInfoParameterLength": 0x0003,
                "fileSizeUncompressedOrDirInfoLength": 0x699C18,
            },
            None,
            ResponseSID.RequestFileTransfer,
            bytearray([0x78, 0x05, 0x01, 0xE5, 0x00, 0x00, 0x03, 0x69, 0x9C, 0x18])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert REQUEST_FILE_TRANSFER_2013.encode(data_records_values=data_records_values,
                                                sid=sid,
                                                rsid=rsid) == payload


@pytest.mark.integration
class TestRequestFileTransfer2020Integration:
    """Integration tests for `RequestFileTransfer` service version 2020."""

    @pytest.mark.parametrize("payload, decoded_message", [
        # AddFile (0x01)
        (
            [0x38, 0x01,
             0x00, 0x06, 0x2F, 0x66, 0x2E, 0x31, 0x32, 0x33,
             0x8C,
             0x01, 0xB0, 0x2C],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'RequestFileTransfer',
                    'raw_value': 0x38,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'modeOfOperation',
                    'physical_value': "AddFile",
                    'raw_value': 0x01,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'filePathAndNameLength',
                    'physical_value': 0x0006,
                    'raw_value': 0x0006,
                    'unit': "bytes"
                },
                {
                    'children': ((), (), (), (), (), ()),
                    'length': 8,
                    'name': 'filePathAndName',
                    'physical_value': r"/f.123",
                    'raw_value': (0x2F, 0x66, 0x2E, 0x31, 0x32, 0x33),
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'compressionMethod',
                            'physical_value': 'compression #8',
                            'raw_value': 0x8,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'encryptingMethod',
                            'physical_value': 'encryption #12',
                            'raw_value': 0xC,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'dataFormatIdentifier',
                    'physical_value': 0x8C,
                    'raw_value': 0x8C,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'fileSizeParameterLength',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'fileSizeUnCompressed',
                    'physical_value': 0xB0,
                    'raw_value': 0xB0,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'fileSizeCompressed',
                    'physical_value': 0x2C,
                    'raw_value': 0x2C,
                    'unit': "bytes"
                },
            )
        ),
        (
            [0x78, 0x01,
             0x01, 0x08,
             0x00],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'RequestFileTransfer',
                    'raw_value': 0x78,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'modeOfOperation',
                    'physical_value': "AddFile",
                    'raw_value': 0x01,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'lengthFormatIdentifier',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'maxNumberOfBlockLength',
                    'physical_value': 0x08,
                    'raw_value': 0x08,
                    'unit': "bytes"
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'compressionMethod',
                            'physical_value': 'no compression',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'encryptingMethod',
                            'physical_value': 'no encryption',
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
            ),
        ),
        # DeleteFile (0x02)
        (
            [0x38, 0x02,
             0x00, 0x1F, 0x2F, 0x6F, 0x70, 0x74, 0x2F, 0x6D, 0x79, 0x61, 0x70, 0x70, 0x2F, 0x63, 0x6F, 0x6E, 0x66, 0x69,
             0x67, 0x2F, 0x73, 0x65, 0x74, 0x74, 0x69, 0x6E, 0x67, 0x73, 0x2E, 0x79, 0x61, 0x6D, 0x6C],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'RequestFileTransfer',
                    'raw_value': 0x38,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'modeOfOperation',
                    'physical_value': "DeleteFile",
                    'raw_value': 0x02,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'filePathAndNameLength',
                    'physical_value': 0x001F,
                    'raw_value': 0x001F,
                    'unit': "bytes"
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (),
                                 (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'filePathAndName',
                    'physical_value': r"/opt/myapp/config/settings.yaml",
                    'raw_value': (0x2F, 0x6F, 0x70, 0x74, 0x2F, 0x6D, 0x79, 0x61, 0x70, 0x70, 0x2F, 0x63, 0x6F, 0x6E,
                                  0x66, 0x69, 0x67, 0x2F, 0x73, 0x65, 0x74, 0x74, 0x69, 0x6E, 0x67, 0x73, 0x2E, 0x79,
                                  0x61, 0x6D, 0x6C),
                    'unit': None
                },
            )
        ),
        (
            [0x78, 0x02],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'RequestFileTransfer',
                    'raw_value': 0x78,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'modeOfOperation',
                    'physical_value': "DeleteFile",
                    'raw_value': 0x02,
                    'unit': None
                },
            ),
        ),
        # ReplaceFile (0x03)
        (
            [0x38, 0x03,
             0x00, 0x01, 0x2E,
             0x00,
             0x01, 0x4F, 0x5B],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'RequestFileTransfer',
                    'raw_value': 0x38,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'modeOfOperation',
                    'physical_value': "ReplaceFile",
                    'raw_value': 0x03,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'filePathAndNameLength',
                    'physical_value': 0x0001,
                    'raw_value': 0x0001,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'filePathAndName',
                    'physical_value': r".",
                    'raw_value': 0x2E,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'compressionMethod',
                            'physical_value': 'no compression',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'encryptingMethod',
                            'physical_value': 'no encryption',
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
                    'children': (),
                    'length': 8,
                    'name': 'fileSizeParameterLength',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'fileSizeUnCompressed',
                    'physical_value': 0x4F,
                    'raw_value': 0x4F,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'fileSizeCompressed',
                    'physical_value': 0x5B,
                    'raw_value': 0x5B,
                    'unit': "bytes"
                },
            )
        ),
        (
            [0x78, 0x03,
             0x06, 0x00, 0x00, 0xB6, 0x70, 0xB2, 0x71,
             0xB2],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'RequestFileTransfer',
                    'raw_value': 0x78,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'modeOfOperation',
                    'physical_value': "ReplaceFile",
                    'raw_value': 0x03,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'lengthFormatIdentifier',
                    'physical_value': 0x06,
                    'raw_value': 0x06,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 48,
                    'name': 'maxNumberOfBlockLength',
                    'physical_value': 0x0000B670B271,
                    'raw_value': 0x0000B670B271,
                    'unit': "bytes"
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'compressionMethod',
                            'physical_value': 'compression #11',
                            'raw_value': 0xB,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'encryptingMethod',
                            'physical_value': 'encryption #2',
                            'raw_value': 0x2,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'dataFormatIdentifier',
                    'physical_value': 0xB2,
                    'raw_value': 0xB2,
                    'unit': None
                },
            ),
        ),
        # ReadFile (0x04)
        (
            [0x38, 0x04,
             0x00, 0x09, 0x2F, 0x66, 0x69, 0x6C, 0x65, 0x2E, 0x61, 0x62, 0x63,
             0x73],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'RequestFileTransfer',
                    'raw_value': 0x38,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'modeOfOperation',
                    'physical_value': "ReadFile",
                    'raw_value': 0x04,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'filePathAndNameLength',
                    'physical_value': 0x0009,
                    'raw_value': 0x0009,
                    'unit': "bytes"
                },
                {
                    'children': ((), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'filePathAndName',
                    'physical_value': r"/file.abc",
                    'raw_value': (0x2F, 0x66, 0x69, 0x6C, 0x65, 0x2E, 0x61, 0x62, 0x63),
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'compressionMethod',
                            'physical_value': 'compression #7',
                            'raw_value': 0x7,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'encryptingMethod',
                            'physical_value': 'encryption #3',
                            'raw_value': 0x3,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'dataFormatIdentifier',
                    'physical_value': 0x73,
                    'raw_value': 0x73,
                    'unit': None
                },
            )
        ),
        (
            [0x78, 0x04,
             0x01, 0x40,
             0x02,
             0x00, 0x02, 0x83, 0x0B, 0x06, 0x97],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'RequestFileTransfer',
                    'raw_value': 0x78,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'modeOfOperation',
                    'physical_value': "ReadFile",
                    'raw_value': 0x04,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'lengthFormatIdentifier',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'maxNumberOfBlockLength',
                    'physical_value': 0x40,
                    'raw_value': 0x40,
                    'unit': "bytes"
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'compressionMethod',
                            'physical_value': 'no compression',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'encryptingMethod',
                            'physical_value': 'encryption #2',
                            'raw_value': 0x2,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'dataFormatIdentifier',
                    'physical_value': 0x02,
                    'raw_value': 0x02,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'fileSizeOrDirInfoParameterLength',
                    'physical_value': 0x0002,
                    'raw_value': 0x0002,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'fileSizeUncompressedOrDirInfoLength',
                    'physical_value': 0x830B,
                    'raw_value': 0x830B,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'fileSizeCompressed',
                    'physical_value': 0x0697,
                    'raw_value': 0x0697,
                    'unit': "bytes"
                },
            ),
        ),
        # ReadDir (0x05)
        (
            [0x38, 0x05,
             0x00, 0x02, 0x2F, 0x78],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'RequestFileTransfer',
                    'raw_value': 0x38,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'modeOfOperation',
                    'physical_value': "ReadDir",
                    'raw_value': 0x05,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'filePathAndNameLength',
                    'physical_value': 0x0002,
                    'raw_value': 0x0002,
                    'unit': "bytes"
                },
                {
                    'children': ((), ()),
                    'length': 8,
                    'name': 'filePathAndName',
                    'physical_value': r"/x",
                    'raw_value': (0x2F, 0x78),
                    'unit': None
                }
            )
        ),
        (
            [0x78, 0x05,
             0x02, 0xF0, 0x00,
             0xE0,
             0x00, 0x02, 0xFE, 0xDC],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'RequestFileTransfer',
                    'raw_value': 0x78,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'modeOfOperation',
                    'physical_value': "ReadDir",
                    'raw_value': 0x05,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'lengthFormatIdentifier',
                    'physical_value': 0x02,
                    'raw_value': 0x02,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'maxNumberOfBlockLength',
                    'physical_value': 0xF000,
                    'raw_value': 0xF000,
                    'unit': "bytes"
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'compressionMethod',
                            'physical_value': 'compression #14',
                            'raw_value': 0xE,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'encryptingMethod',
                            'physical_value': 'no encryption',
                            'raw_value': 0x0,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'dataFormatIdentifier',
                    'physical_value': 0xE0,
                    'raw_value': 0xE0,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'fileSizeOrDirInfoParameterLength',
                    'physical_value': 0x0002,
                    'raw_value': 0x0002,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'fileSizeUncompressedOrDirInfoLength',
                    'physical_value': 0xFEDC,
                    'raw_value': 0xFEDC,
                    'unit': "bytes"
                },
            ),
        ),
        # ResumeFile (0x06)
        (
            [0x38, 0x06,
             0x00, 0x05, 0x2F, 0x66, 0x69, 0x6C, 0x65,
             0x00,
             0x02, 0x36, 0x3A, 0xBB, 0x6D],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'RequestFileTransfer',
                    'raw_value': 0x38,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'modeOfOperation',
                    'physical_value': "ResumeFile",
                    'raw_value': 0x06,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'filePathAndNameLength',
                    'physical_value': 0x0005,
                    'raw_value': 0x0005,
                    'unit': "bytes"
                },
                {
                    'children': ((), (), (), (), ()),
                    'length': 8,
                    'name': 'filePathAndName',
                    'physical_value': r"/file",
                    'raw_value': (0x2F, 0x66, 0x69, 0x6C, 0x65),
                    'unit': None
                },
                {
                    'children': (
                            {
                                'children': (),
                                'length': 4,
                                'name': 'compressionMethod',
                                'physical_value': 'no compression',
                                'raw_value': 0x0,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 4,
                                'name': 'encryptingMethod',
                                'physical_value': 'no encryption',
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
                    'children': (),
                    'length': 8,
                    'name': 'fileSizeParameterLength',
                    'physical_value': 0x02,
                    'raw_value': 0x02,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'fileSizeUnCompressed',
                    'physical_value': 0x363A,
                    'raw_value': 0x363A,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'fileSizeCompressed',
                    'physical_value': 0xBB6D,
                    'raw_value': 0xBB6D,
                    'unit': "bytes"
                },
            )
        ),
        (
            [0x78, 0x06,
             0x01, 0xD2,
             0x00,
             0x4E, 0x7D, 0x5C, 0x2D, 0xA9, 0xBC, 0xB1, 0x91],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'RequestFileTransfer',
                    'raw_value': 0x78,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'modeOfOperation',
                    'physical_value': "ResumeFile",
                    'raw_value': 0x06,
                    'unit': None
                },

                {
                    'children': (),
                    'length': 8,
                    'name': 'lengthFormatIdentifier',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': "bytes"
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'maxNumberOfBlockLength',
                    'physical_value': 0xD2,
                    'raw_value': 0xD2,
                    'unit': "bytes"
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'compressionMethod',
                            'physical_value': 'no compression',
                            'raw_value': 0x0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'encryptingMethod',
                            'physical_value': 'no encryption',
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
                    'children': (),
                    'length': 64,
                    'name': 'filePosition',
                    'physical_value': 0x4E7D5C2DA9BCB191,
                    'raw_value': 0x4E7D5C2DA9BCB191,
                    'unit': None
                },
            ),
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert REQUEST_FILE_TRANSFER_2020.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        # AddFile (0x01)
        (
            {
                "modeOfOperation": 0x01,
                "filePathAndNameLength": 0x0002,
                "filePathAndName": (0x30, 0x31),
                "dataFormatIdentifier": 0x01,
                "fileSizeParameterLength": 0x02,
                "fileSizeUnCompressed": 0x0100,
                "fileSizeCompressed": 0x00D2,
            },
            RequestSID.RequestFileTransfer,
            None,
            bytearray([0x38, 0x01, 0x00, 0x02, 0x30, 0x31, 0x01, 0x02, 0x01, 0x00, 0x00, 0xD2])
        ),
        (
            {
                "modeOfOperation": 0x01,
                "lengthFormatIdentifier": 0x02,
                "maxNumberOfBlockLength": 0xE000,
                "dataFormatIdentifier": 0x5D,
            },
            None,
            ResponseSID.RequestFileTransfer,
            bytearray([0x78, 0x01, 0x02, 0xE0, 0x00, 0x5D])
        ),
        # DeleteFile (0x02)
        (
            {
                "modeOfOperation": 0x02,
                "filePathAndNameLength": 0x0005,
                "filePathAndName": (0x68, 0x2C, 0x62, 0x28, 0x5A),
            },
            RequestSID.RequestFileTransfer,
            None,
            bytearray([0x38, 0x02, 0x00, 0x05, 0x68, 0x2C, 0x62, 0x28, 0x5A])
        ),
        (
            {
                "modeOfOperation": 0x02,
            },
            None,
            ResponseSID.RequestFileTransfer,
            bytearray([0x78, 0x02])
        ),
        # TODO
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert REQUEST_FILE_TRANSFER_2020.encode(data_records_values=data_records_values,
                                                sid=sid,
                                                rsid=rsid) == payload

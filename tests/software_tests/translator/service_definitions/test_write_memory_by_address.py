import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.write_memory_by_address import WRITE_MEMORY_BY_ADDRESS


class TestWriteMemoryByAddress:
    """Unit tests for `WriteMemoryByAddress` service."""

    def test_request_sid(self):
        assert WRITE_MEMORY_BY_ADDRESS.request_sid == RequestSID.WriteMemoryByAddress

    def test_response_sid(self):
        assert WRITE_MEMORY_BY_ADDRESS.response_sid == ResponseSID.WriteMemoryByAddress


@pytest.mark.integration
class TestWriteMemoryByAddressIntegration:
    """Integration tests for `WriteMemoryByAddress` service."""

    @pytest.mark.parametrize("payload, decoded_message", [
        (
            [0x3D, 0x12,
             0x3A, 0x83,
             0x10,
             0x1E, 0xC7, 0x93, 0xC4, 0xC7, 0x1D, 0x70, 0x0D, 0x25, 0xFA, 0xFC, 0x38, 0x32, 0x38, 0x9E, 0x9E],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'WriteMemoryByAddress',
                    'raw_value': 0x3D,
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
                            'unit': 'bytes',
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'memoryAddressLength',
                            'physical_value': 0x2,
                            'raw_value': 0x2,
                            'unit': 'bytes',
                        },
                    ),
                    'length': 8,
                    'name': 'addressAndLengthFormatIdentifier',
                    'physical_value': 0x12,
                    'raw_value': 0x12,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'memoryAddress',
                    'physical_value': 0x3A83,
                    'raw_value': 0x3A83,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'memorySize',
                    'physical_value': 0x10,
                    'raw_value': 0x10,
                    'unit': "bytes"
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'data',
                    'physical_value': (0x1E, 0xC7, 0x93, 0xC4, 0xC7, 0x1D, 0x70, 0x0D, 0x25, 0xFA, 0xFC, 0x38, 0x32, 0x38, 0x9E, 0x9E),
                    'raw_value': (0x1E, 0xC7, 0x93, 0xC4, 0xC7, 0x1D, 0x70, 0x0D, 0x25, 0xFA, 0xFC, 0x38, 0x32, 0x38, 0x9E, 0x9E),
                    'unit': None
                },
            )
        ),
        (
            [0x3D, 0x24,
             0x80, 0x5D, 0x20, 0xA9,
             0x00, 0x05,
             0xAF, 0x31, 0xD3, 0xBB, 0x31],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'WriteMemoryByAddress',
                    'raw_value': 0x3D,
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
                            'unit': 'bytes',
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'memoryAddressLength',
                            'physical_value': 0x4,
                            'raw_value': 0x4,
                            'unit': 'bytes',
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
                    'physical_value': 0x805D20A9,
                    'raw_value': 0x805D20A9,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'memorySize',
                    'physical_value': 0x0005,
                    'raw_value': 0x0005,
                    'unit': "bytes"
                },
                {
                    'children': ((), (), (), (), ()),
                    'length': 8,
                    'name': 'data',
                    'physical_value': (0xAF, 0x31, 0xD3, 0xBB, 0x31),
                    'raw_value': (0xAF, 0x31, 0xD3, 0xBB, 0x31),
                    'unit': None
                },
            )
        ),
        (
            [0x7D, 0xFF,
             0xD7, 0x10, 0xA5, 0x81, 0xF8, 0x2E, 0x9E, 0xA6, 0x61, 0x3B, 0xEA, 0x76, 0xA3, 0x7E, 0x1D,
             0xAB, 0x5B, 0x14, 0xF1, 0x50, 0x47, 0x03, 0x9B, 0xA0, 0x40, 0xEF, 0x5C, 0x28, 0x99, 0xB0],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'WriteMemoryByAddress',
                    'raw_value': 0x7D,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 4,
                            'name': 'memorySizeLength',
                            'physical_value': 0xF,
                            'raw_value': 0xF,
                            'unit': 'bytes',
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'memoryAddressLength',
                            'physical_value': 0xF,
                            'raw_value': 0xF,
                            'unit': 'bytes',
                        },
                    ),
                    'length': 8,
                    'name': 'addressAndLengthFormatIdentifier',
                    'physical_value': 0xFF,
                    'raw_value': 0xFF,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 120,
                    'name': 'memoryAddress',
                    'physical_value': 0xD710A581F82E9EA6613BEA76A37E1D,
                    'raw_value': 0xD710A581F82E9EA6613BEA76A37E1D,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 120,
                    'name': 'memorySize',
                    'physical_value': 0xAB5B14F15047039BA040EF5C2899B0,
                    'raw_value': 0xAB5B14F15047039BA040EF5C2899B0,
                    'unit': "bytes"
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert WRITE_MEMORY_BY_ADDRESS.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        (
            {
                "addressAndLengthFormatIdentifier": {
                    "memorySizeLength": 2,
                    "memoryAddressLength": 3,
                },
                "memoryAddress": 0xF00012,
                "memorySize": 0x000A,
                "data": (0xEC, 0xFA, 0xC9, 0x27, 0xA3, 0xEC, 0x46, 0x1C, 0xC7, 0x72),
            },
            RequestSID.WriteMemoryByAddress,
            None,
            bytearray([0x3D, 0x23, 0xF0, 0x00, 0x12,
                       0x00, 0x0A,
                       0xEC, 0xFA, 0xC9, 0x27, 0xA3, 0xEC, 0x46, 0x1C, 0xC7, 0x72])
        ),
        (
            {
                "addressAndLengthFormatIdentifier": 0xDE,
                "memoryAddress": 0xC11370C78D3C7090B3B3ADAA8E4F,
                "memorySize": 0xEBF2C1076771568F956597C8C3,
            },
            None,
            ResponseSID.WriteMemoryByAddress,
            bytearray([0x7D, 0xDE,
                       0xC1, 0x13, 0x70, 0xC7, 0x8D, 0x3C, 0x70, 0x90, 0xB3, 0xB3, 0xAD, 0xAA, 0x8E, 0x4F,
                       0xEB, 0xF2, 0xC1, 0x07, 0x67, 0x71, 0x56, 0x8F, 0x95, 0x65, 0x97, 0xC8, 0xC3])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert WRITE_MEMORY_BY_ADDRESS.encode(data_records_values=data_records_values,
                                                 sid=sid,
                                                 rsid=rsid) == payload

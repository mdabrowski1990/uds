import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.read_memory_by_address import READ_MEMORY_BY_ADDRESS
from uds.utilities import bytes_to_hex


class TestReadMemoryByAddress:
    """Unit tests for `ReadMemoryByAddress` service."""

    def test_request_sid(self):
        assert READ_MEMORY_BY_ADDRESS.request_sid == RequestSID.ReadMemoryByAddress

    def test_response_sid(self):
        assert READ_MEMORY_BY_ADDRESS.response_sid == ResponseSID.ReadMemoryByAddress


@pytest.mark.integration
class TestReadMemoryByAddressIntegration:
    """Integration tests for `ReadMemoryByAddress` service."""

    @pytest.mark.parametrize("payload, decoded_message", [
        (
            [0x23, 0xFF,
             0xB3, 0x4D, 0xB0, 0x75, 0xC3, 0xCB, 0x50, 0x86, 0x28, 0xB1, 0x6F, 0x52, 0x97, 0x06, 0x3B,
             0x2C, 0xE7, 0x43, 0x3D, 0x85, 0x33, 0xEE, 0x4C, 0xB1, 0x05, 0xBB, 0x07, 0x9A, 0xC5, 0xA0],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'ReadMemoryByAddress',
                    'raw_value': 0x23,
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
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'memoryAddressLength',
                            'physical_value': 0xF,
                            'raw_value': 0xF,
                            'unit': None
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
                    'physical_value': 0xB34DB075C3CB508628B16F5297063B,
                    'raw_value': 0xB34DB075C3CB508628B16F5297063B,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 120,
                    'name': 'memorySize',
                    'physical_value': 0x2CE7433D8533EE4CB105BB079AC5A0,
                    'raw_value': 0x2CE7433D8533EE4CB105BB079AC5A0,
                    'unit': None
                },
            )
        ),
        (
            [0x23, 0x14, 0x88, 0xD6, 0x4D, 0xB3, 0xF1],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'ReadMemoryByAddress',
                    'raw_value': 0x23,
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
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'memoryAddressLength',
                            'physical_value': 0x4,
                            'raw_value': 0x4,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'addressAndLengthFormatIdentifier',
                    'physical_value': 0x14,
                    'raw_value': 0x14,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 32,
                    'name': 'memoryAddress',
                    'physical_value': 0x88D64DB3,
                    'raw_value': 0x88D64DB3,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'memorySize',
                    'physical_value': 0xF1,
                    'raw_value': 0xF1,
                    'unit': None
                },
            )
        ),
        (
            [0x63, 0xFB, 0x3E, 0xA7, 0x47, 0x67, 0x82, 0xAF, 0x2C, 0xB4, 0x7A, 0xA5, 0xC4, 0x32],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'ReadMemoryByAddress',
                    'raw_value': 0x63,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'Data',
                    'physical_value': (0xFB, 0x3E, 0xA7, 0x47, 0x67, 0x82, 0xAF, 0x2C, 0xB4, 0x7A, 0xA5, 0xC4, 0x32),
                    'raw_value': (0xFB, 0x3E, 0xA7, 0x47, 0x67, 0x82, 0xAF, 0x2C, 0xB4, 0x7A, 0xA5, 0xC4, 0x32),
                    'unit': None
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        print(f"payload = {bytes_to_hex(payload)}")
        assert READ_MEMORY_BY_ADDRESS.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        (
            {
                "addressAndLengthFormatIdentifier": {
                    "memoryAddressLength": 3,
                    "memorySizeLength": 2,
                },
                "memoryAddress": 0xF00012,
                "memorySize": 0x0100,
            },
            RequestSID.ReadMemoryByAddress,
            None,
            bytearray([0x23, 0x23, 0xF0, 0x00, 0x12, 0x01, 0x00])
        ),
        (
            {
                "Data": (0x29, 0x88, 0xDA, 0xB0),
            },
            None,
            ResponseSID.ReadMemoryByAddress,
            bytearray([0x63, 0x29, 0x88, 0xDA, 0xB0])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        print(f"SID = {sid}\nRSID = {rsid}\npayload = {bytes_to_hex(payload)}")
        assert READ_MEMORY_BY_ADDRESS.encode(data_records_values=data_records_values,
                                                 sid=sid,
                                                 rsid=rsid) == payload

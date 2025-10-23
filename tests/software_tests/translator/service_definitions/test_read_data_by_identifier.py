import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.read_data_by_identifier import (
    READ_DATA_BY_IDENTIFIER,
    READ_DATA_BY_IDENTIFIER_2013,
    READ_DATA_BY_IDENTIFIER_2020,
)
from uds.utilities import bytes_to_hex


class TestReadDataByIdentifier:
    """Unit tests for `ReadDataByIdentifier` service."""

    def test_request_sid(self):
        assert READ_DATA_BY_IDENTIFIER_2013.request_sid == RequestSID.ReadDataByIdentifier
        assert READ_DATA_BY_IDENTIFIER_2020.request_sid == RequestSID.ReadDataByIdentifier

    def test_response_sid(self):
        assert READ_DATA_BY_IDENTIFIER_2013.response_sid == ResponseSID.ReadDataByIdentifier
        assert READ_DATA_BY_IDENTIFIER_2020.response_sid == ResponseSID.ReadDataByIdentifier

    def test_default_translator(self):
        assert READ_DATA_BY_IDENTIFIER is READ_DATA_BY_IDENTIFIER_2020


@pytest.mark.integration
class TestReadDataByIdentifier2013Integration:
    """Integration tests for `ReadDataByIdentifier` service version 2013."""

    @pytest.mark.parametrize("payload, decoded_message", [
        (
            [0x22, 0xF1, 0x86],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'ReadDataByIdentifier',
                    'raw_value': 0x22,
                    'unit': None
                },
                {
                    'children': ((),),
                    'length': 16,
                    'name': 'DID',
                    'physical_value': ("ActiveDiagnosticSessionDataIdentifier",),
                    'raw_value': (0xF186,),
                    'unit': None
                },
            )
        ),
        (
            [0x22, 0xF1, 0x80, 0xFF, 0x00, 0x00, 0x00, 0xF1, 0x90, 0x12, 0x34, 0xFF, 0xFF],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'ReadDataByIdentifier',
                    'raw_value': 0x22,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), ()),
                    'length': 16,
                    'name': 'DID',
                    'physical_value': ("BootSoftwareIdentificationDataIdentifier",
                                       "UDSVersionDataIdentifier",
                                       0x0000,
                                       "VINDataIdentifier",
                                       0x1234,
                                       0xFFFF),
                    'raw_value': (0xF180, 0xFF00, 0x0000,  0xF190, 0x1234, 0xFFFF),
                    'unit': None
                },
            )
        ),

        (
            [0x62, 0xF1, 0x86, 0x03, 0xF1, 0x90, 0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5, 0x96, 0x87],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'ReadDataByIdentifier',
                    'raw_value': 0x62,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DID#1',
                    'physical_value': "ActiveDiagnosticSessionDataIdentifier",
                    'raw_value': 0xF186,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'Reserved',
                            'physical_value': 0,
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'ActiveDiagnosticSession',
                            'physical_value': 'extendedDiagnosticSession',
                            'raw_value': 0x03,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'DID#1 data',
                    'physical_value': 0x03,
                    'raw_value': 0x03,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DID#2',
                    'physical_value': "VINDataIdentifier",
                    'raw_value': 0xF190,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'DID#2 data',
                    'physical_value': (0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5, 0x96, 0x87),
                    'raw_value': (0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5, 0x96, 0x87),
                    'unit': None
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        print(f"payload = {bytes_to_hex(payload)}")
        assert READ_DATA_BY_IDENTIFIER_2013.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        (
                {
                    "DID": [0xFA12],
                },
                RequestSID.ReadDataByIdentifier,
                None,
                bytearray([0x22, 0xFA, 0x12])
        ),
        (
                {
                    "DID": (0x0000, 0x1234, 0x58BE, 0xFFFF),
                },
                RequestSID.ReadDataByIdentifier,
                None,
                bytearray([0x22, 0x00, 0x00, 0x12, 0x34, 0x58, 0xBE, 0xFF, 0xFF])
        ),
        (
                {
                    "DID#1": 0x2468,
                    "DID#1 data": [0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE],
                    "DID#2": 0xF195,
                    "DID#2 data": [0x13, 0x57, 0x9C, 0xDF],
                    "DID#3": 0xF195,
                    "DID#3 data": [0x00, 0xFF],
                },
                None,
                ResponseSID.ReadDataByIdentifier,
                bytearray([0x62,
                           0x24, 0x68, 0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE,
                           0xF1, 0x95, 0x13, 0x57, 0x9C, 0xDF,
                           0xF1, 0x95, 0x00, 0xFF])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        print(f"SID = {sid}\nRSID = {rsid}\npayload = {bytes_to_hex(payload)}")
        assert READ_DATA_BY_IDENTIFIER_2013.encode(data_records_values=data_records_values,
                                                   sid=sid,
                                                   rsid=rsid) == payload


@pytest.mark.integration
class TestReadDataByIdentifier2020Integration:
    """Integration tests for `ReadDataByIdentifier` service version 2020."""

    @pytest.mark.parametrize("payload, decoded_message", [
        (
            [0x22, 0xFF, 0x01],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'ReadDataByIdentifier',
                    'raw_value': 0x22,
                    'unit': None
                },
                {
                    'children': ((),),
                    'length': 16,
                    'name': 'DID',
                    'physical_value': ("ReservedForISO15765-5",),
                    'raw_value': (0xFF01,),
                    'unit': None
                },
            )
        ),
        (
            [0x22, 0xFA, 0x12, 0xFA, 0x10, 0x00, 0x00, 0xFF, 0xFF],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'ReadDataByIdentifier',
                    'raw_value': 0x22,
                    'unit': None
                },
                {
                    'children': ((), (), (), ()),
                    'length': 16,
                    'name': 'DID',
                    'physical_value': ("EDRDeviceAddressInformation",
                                       "NumberOfEDRDevices",
                                       0x0000,
                                       0xFFFF),
                    'raw_value': (0xFA12, 0xFA10, 0x0000, 0xFFFF),
                    'unit': None
                },
            )
        ),

        (
            [0x62, 0xF1, 0x86, 0x01, 0xF1, 0x8B, 0x00, 0xFF, 0x11, 0xEE],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'ReadDataByIdentifier',
                    'raw_value': 0x62,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DID#1',
                    'physical_value': "ActiveDiagnosticSessionDataIdentifier",
                    'raw_value': 0xF186,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'Reserved',
                            'physical_value': 0,
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'ActiveDiagnosticSession',
                            'physical_value': 'defaultSession',
                            'raw_value': 0x01,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'DID#1 data',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DID#2',
                    'physical_value': "ECUManufacturingDateDataIdentifier",
                    'raw_value': 0xF18B,
                    'unit': None
                },
                {
                    'children': ((), (), (), ()),
                    'length': 8,
                    'name': 'DID#2 data',
                    'physical_value': (0x00, 0xFF, 0x11, 0xEE),
                    'raw_value': (0x00, 0xFF, 0x11, 0xEE),
                    'unit': None
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        print(f"payload = {bytes_to_hex(payload)}")
        assert READ_DATA_BY_IDENTIFIER_2020.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        (
                {
                    "DID": [0x53B8],
                },
                RequestSID.ReadDataByIdentifier,
                None,
                bytearray([0x22, 0x53, 0xB8])
        ),
        (
                {
                    "DID": (0x0000, 0xF184, 0xFFFF),
                },
                RequestSID.ReadDataByIdentifier,
                None,
                bytearray([0x22, 0x00, 0x00, 0xF1, 0x84, 0xFF, 0xFF])
        ),
        (
                {
                    "DID#1": 0x0000,
                    "DID#1 data": [0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5, 0x96, 0x87, 0x78, 0x69, 0x5A, 0x4B, 0x3C, 0x2D, 0x1E, 0x0F],
                    "DID#2": 0xFFFF,
                    "DID#2 data": [0x5A],
                },
                None,
                ResponseSID.ReadDataByIdentifier,
                bytearray([0x62,
                           0x00, 0x00, 0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5, 0x96, 0x87, 0x78, 0x69, 0x5A, 0x4B, 0x3C, 0x2D, 0x1E, 0x0F,
                           0xFF, 0xFF, 0x5A])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        print(f"SID = {sid}\nRSID = {rsid}\npayload = {bytes_to_hex(payload)}")
        assert READ_DATA_BY_IDENTIFIER_2020.encode(data_records_values=data_records_values,
                                                   sid=sid,
                                                   rsid=rsid) == payload

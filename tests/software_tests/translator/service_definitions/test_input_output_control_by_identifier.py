import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.input_output_control_by_identifier import (
    INPUT_OUTPUT_CONTROL_BY_IDENTIFIER,
    INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2013,
    INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2020,
)


class TestInputOutputControlByIdentifier:
    """Unit tests for `InputOutputControlByIdentifier` service."""

    def test_request_sid(self):
        assert INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2013.request_sid == RequestSID.InputOutputControlByIdentifier
        assert INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2020.request_sid == RequestSID.InputOutputControlByIdentifier

    def test_response_sid(self):
        assert INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2013.response_sid == ResponseSID.InputOutputControlByIdentifier
        assert INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2020.response_sid == ResponseSID.InputOutputControlByIdentifier

    def test_default_translator(self):
        assert INPUT_OUTPUT_CONTROL_BY_IDENTIFIER is INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2020


@pytest.mark.integration
class TestInputOutputControlByIdentifier2013Integration:
    """Integration tests for `InputOutputControlByIdentifier` service version 2013."""

    @pytest.mark.parametrize("payload, decoded_message", [
        # returnControlToECU (0x00)
        (
            [0x2F, 0xF1, 0x8D, 0x00],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'InputOutputControlByIdentifier',
                    'raw_value': 0x2F,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DID',
                    'physical_value': "supportedFunctionalUnitsDataIdentifier",
                    'raw_value': 0xF18D,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'inputOutputControlParameter',
                    'physical_value': "returnControlToECU",
                    'raw_value': 0x00,
                    'unit': None
                },
            )
        ),
        (
            [0x6F, 0xF1, 0x80, 0x00, 0xFF],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'InputOutputControlByIdentifier',
                    'raw_value': 0x6F,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'DID',
                    'physical_value': "BootSoftwareIdentificationDataIdentifier",
                    'raw_value': 0xF180,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'inputOutputControlParameter',
                    'physical_value': "returnControlToECU",
                    'raw_value': 0x00,
                    'unit': None
                },
                {
                    'children': ((),),
                    'length': 8,
                    'name': 'controlState',
                    'physical_value': (0xFF,),
                    'raw_value': (0xFF,),
                    'unit': None
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2013.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        # returnControlToECU (0x00)
        (
            {
                "DID": 0xF0E1,
                "inputOutputControlParameter": 0x00,
            },
            RequestSID.InputOutputControlByIdentifier,
            None,
            bytearray([0x2F, 0xF0, 0xE1, 0x00])
        ),
        (
            {
                "DID": 0x0123,
                "inputOutputControlParameter": 0x00,
                "controlState": (0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5, 0x96, 0x87, 0x78, 0x69, 0x5A, 0x4B, 0x3C, 0x2D,
                                 0x1E, 0x0F)
            },
            None,
            ResponseSID.InputOutputControlByIdentifier,
            bytearray([0x6F, 0x01, 0x23, 0x00,
                       0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5, 0x96, 0x87, 0x78, 0x69, 0x5A, 0x4B, 0x3C, 0x2D, 0x1E, 0x0F])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2013.encode(data_records_values=data_records_values,
                                                        sid=sid,
                                                        rsid=rsid) == payload


@pytest.mark.integration
class TestInputOutputControlByIdentifier2020Integration:
    """Integration tests for `InputOutputControlByIdentifier` service version 2020."""

    @pytest.mark.parametrize("payload, decoded_message", [
    ])
    def test_decode(self, payload, decoded_message):
        assert INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2020.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2020.encode(data_records_values=data_records_values,
                                                        sid=sid,
                                                        rsid=rsid) == payload

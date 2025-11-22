import pytest
from mock import Mock, patch

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.input_output_control_by_identifier import (
    INPUT_OUTPUT_CONTROL_BY_IDENTIFIER,
    INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2013,
    INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2020,
    INPUT_OUTPUT_CONTROL_PARAMETER,
    get_request_continuation_2013,
    get_request_continuation_2020,
    get_response_continuation_2013,
    get_response_continuation_2020,
)

SCRIPT_LOCATION = "uds.translator.service_definitions.input_output_control_by_identifier"

class TestInputOutputControlByIdentifier:
    """Unit tests for `InputOutputControlByIdentifier` service."""

    def setup_method(self):
        self._patcher_conditional_mapping_data_record = patch(f"{SCRIPT_LOCATION}.ConditionalMappingDataRecord")
        self.mock_conditional_mapping_data_record = self._patcher_conditional_mapping_data_record.start()
        self._patcher_conditional_control_state_2013 = patch(f"{SCRIPT_LOCATION}.CONDITIONAL_CONTROL_STATE_2013")
        self.mock_conditional_control_state_2013 = self._patcher_conditional_control_state_2013.start()
        self._patcher_conditional_control_state_2020 = patch(f"{SCRIPT_LOCATION}.CONDITIONAL_CONTROL_STATE_2020")
        self.mock_conditional_control_state_2020 = self._patcher_conditional_control_state_2020.start()
        self._patcher_conditional_control_enable_mask_2013 = patch(f"{SCRIPT_LOCATION}.CONDITIONAL_CONTROL_ENABLE_MASK_2013")
        self.mock_conditional_control_enable_mask_2013 = self._patcher_conditional_control_enable_mask_2013.start()
        self._patcher_conditional_control_enable_mask_2020 = patch(f"{SCRIPT_LOCATION}.CONDITIONAL_CONTROL_ENABLE_MASK_2020")
        self.mock_conditional_control_enable_mask_2020 = self._patcher_conditional_control_enable_mask_2020.start()

    def teardown_method(self):
        self._patcher_conditional_mapping_data_record.stop()
        self._patcher_conditional_control_state_2013.stop()
        self._patcher_conditional_control_state_2020.stop()
        self._patcher_conditional_control_enable_mask_2013.stop()
        self._patcher_conditional_control_enable_mask_2020.stop()

    def test_request_sid(self):
        assert INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2013.request_sid == RequestSID.InputOutputControlByIdentifier
        assert INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2020.request_sid == RequestSID.InputOutputControlByIdentifier

    def test_response_sid(self):
        assert INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2013.response_sid == ResponseSID.InputOutputControlByIdentifier
        assert INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2020.response_sid == ResponseSID.InputOutputControlByIdentifier

    def test_default_translator(self):
        assert INPUT_OUTPUT_CONTROL_BY_IDENTIFIER is INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2020

    # get_request_continuation_2013

    def test_get_request_continuation_2013(self):
        mock_did = Mock()
        assert (get_request_continuation_2013(mock_did)
                == (INPUT_OUTPUT_CONTROL_PARAMETER, self.mock_conditional_mapping_data_record.return_value))
        self.mock_conditional_control_state_2013.get_message_continuation.assert_called_once_with(mock_did)
        self.mock_conditional_control_enable_mask_2013.get_message_continuation.assert_called_once_with(mock_did)

    # get_request_continuation_2020

    def test_get_request_continuation_2020(self):
        mock_did = Mock()
        assert (get_request_continuation_2020(mock_did)
                == (INPUT_OUTPUT_CONTROL_PARAMETER, self.mock_conditional_mapping_data_record.return_value))
        self.mock_conditional_control_state_2020.get_message_continuation.assert_called_once_with(mock_did)
        self.mock_conditional_control_enable_mask_2020.get_message_continuation.assert_called_once_with(mock_did)

    # get_response_continuation_2013

    def test_get_response_continuation_2013(self):
        mock_did = Mock()
        assert (get_response_continuation_2013(mock_did)
                == (INPUT_OUTPUT_CONTROL_PARAMETER, self.mock_conditional_mapping_data_record.return_value))
        self.mock_conditional_control_state_2013.get_message_continuation.assert_called_once_with(mock_did)

    # get_response_continuation_2020

    def test_get_response_continuation_2020(self):
        mock_did = Mock()
        assert (get_response_continuation_2020(mock_did)
                == (INPUT_OUTPUT_CONTROL_PARAMETER, self.mock_conditional_mapping_data_record.return_value))
        self.mock_conditional_control_state_2020.get_message_continuation.assert_called_once_with(mock_did)


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
        # resetToDefault (0x01)
        (
            [0x2F, 0xFF, 0x01, 0x01],
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
                    'physical_value': 0xFF01,
                    'raw_value': 0xFF01,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'inputOutputControlParameter',
                    'physical_value': "resetToDefault",
                    'raw_value': 0x01,
                    'unit': None
                },
            )
        ),
        (
            [0x6F, 0x40, 0x5F, 0x01, 0x54, 0x76, 0x98, 0xBA],
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
                    'physical_value': 0x405F,
                    'raw_value': 0x405F,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'inputOutputControlParameter',
                    'physical_value': "resetToDefault",
                    'raw_value': 0x01,
                    'unit': None
                },
                {
                    'children': ((), (), (), ()),
                    'length': 8,
                    'name': 'controlState',
                    'physical_value': (0x54, 0x76, 0x98, 0xBA),
                    'raw_value': (0x54, 0x76, 0x98, 0xBA),
                    'unit': None
                },
            )
        ),
        # freezeCurrentState (0x02)
        (
            [0x2F, 0x12, 0x34, 0x02],
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
                    'physical_value': 0x1234,
                    'raw_value': 0x1234,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'inputOutputControlParameter',
                    'physical_value': "freezeCurrentState",
                    'raw_value': 0x02,
                    'unit': None
                },
            )
        ),
        (
            [0x6F, 0xCF, 0x40, 0x02, 0x73, 0xA5, 0xAB, 0x16, 0xE4, 0xC8, 0x8E, 0x33],
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
                    'physical_value': 0xCF40,
                    'raw_value': 0xCF40,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'inputOutputControlParameter',
                    'physical_value': "freezeCurrentState",
                    'raw_value': 0x02,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'controlState',
                    'physical_value': (0x73, 0xA5, 0xAB, 0x16, 0xE4, 0xC8, 0x8E, 0x33),
                    'raw_value': (0x73, 0xA5, 0xAB, 0x16, 0xE4, 0xC8, 0x8E, 0x33),
                    'unit': None
                },
            )
        ),
        # shortTermAdjustment (0x03)
        (
            [0x2F, 0xF1, 0x86, 0x03, 0x01, 0x7F],
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
                    'physical_value': 'ActiveDiagnosticSessionDataIdentifier',
                    'raw_value': 0xF186,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'inputOutputControlParameter',
                    'physical_value': "shortTermAdjustment",
                    'raw_value': 0x03,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'reserved',
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
                        },
                    ),
                    'length': 8,
                    'name': 'controlState',
                    'physical_value': 0x01,
                    'raw_value': 0x01,
                    'unit': None
                },
                {
                    'children': (
                        (
                            {
                                'children': (),
                                'length': 1,
                                'name': 'reserved (mask)',
                                'physical_value': 'no',
                                'raw_value': 0,
                                'unit': None
                            },
                            {
                                'children': (),
                                'length': 7,
                                'name': 'ActiveDiagnosticSession (mask)',
                                'physical_value': 'yes',
                                'raw_value': 0x7F,
                                'unit': None
                            },
                        ),
                    ),
                    'length': 8,
                    'name': 'controlEnableMask',
                    'physical_value': (0x7F,),
                    'raw_value': (0x7F,),
                    'unit': None
                }
            )
        ),
        (
            [0x2F, 0x0A, 0x73, 0x03, 0xA0, 0x02, 0x78, 0x0D],
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
                    'physical_value': 0x0A73,
                    'raw_value': 0x0A73,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'inputOutputControlParameter',
                    'physical_value': "shortTermAdjustment",
                    'raw_value': 0x03,
                    'unit': None
                },
                {
                    'children': ((), (), (), ()),
                    'length': 8,
                    'name': 'controlState',
                    'physical_value': (0xA0, 0x02, 0x78, 0x0D),
                    'raw_value': (0xA0, 0x02, 0x78, 0x0D),
                    'unit': None
                },
            )
        ),
        (
            [0x6F, 0x4D, 0xCE, 0x03, 0x17, 0x7C, 0xC8, 0x5E, 0x5D, 0x21, 0x51, 0x98, 0x56, 0xFB, 0x67, 0x0C, 0x4B, 0x77],
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
                    'physical_value': 0x4DCE,
                    'raw_value': 0x4DCE,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'inputOutputControlParameter',
                    'physical_value': "shortTermAdjustment",
                    'raw_value': 0x03,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'controlState',
                    'physical_value': (0x17, 0x7C, 0xC8, 0x5E, 0x5D, 0x21, 0x51, 0x98, 0x56, 0xFB, 0x67, 0x0C, 0x4B, 0x77),
                    'raw_value': (0x17, 0x7C, 0xC8, 0x5E, 0x5D, 0x21, 0x51, 0x98, 0x56, 0xFB, 0x67, 0x0C, 0x4B, 0x77),
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
        # resetToDefault (0x01)
        (
            {
                "DID": 0xDAA5,
                "inputOutputControlParameter": 0x01,
            },
            RequestSID.InputOutputControlByIdentifier,
            None,
            bytearray([0x2F, 0xDA, 0xA5, 0x01])
        ),
        (
            {
                "DID": 0xBDA2,
                "inputOutputControlParameter": 0x01,
                "controlState": (0x11, 0x18, 0xB9, 0x44, 0x10, 0xE8)
            },
            None,
            ResponseSID.InputOutputControlByIdentifier,
            bytearray([0x6F, 0xBD, 0xA2, 0x01,
                       0x11, 0x18, 0xB9, 0x44, 0x10, 0xE8])
        ),
        # freezeCurrentState (0x02)
        (
            {
                "DID": 0xB715,
                "inputOutputControlParameter": 0x02,
            },
            RequestSID.InputOutputControlByIdentifier,
            None,
            bytearray([0x2F, 0xB7, 0x15, 0x02])
        ),
        (
            {
                "DID": 0xE0FA,
                "inputOutputControlParameter": 0x02,
                "controlState": (0x85, 0x4B, 0xBE, 0xBE, 0x81, 0x34, 0x62, 0xA2, 0x10, 0x1B, 0xEF, 0x67),
            },
            None,
            ResponseSID.InputOutputControlByIdentifier,
            bytearray([0x6F,0xE0, 0xFA, 0x02,
                       0x85, 0x4B, 0xBE, 0xBE, 0x81, 0x34, 0x62, 0xA2, 0x10, 0x1B, 0xEF, 0x67])
        ),
        # shortTermAdjustment (0x03)
        (
            {
                "DID": 0x3AD3,
                "inputOutputControlParameter": 0x03,
                "controlState": (0x1C, 0xCB, 0x9A, 0x7A, 0xC1, 0x66, 0xD6, 0xAE, 0xB8, 0x9F, 0x22, 0x1B, 0xC2, 0x79),
                "controlEnableMask": (0x96, 0x47, 0xE0, 0xC8, 0xE3, 0xE8, 0x09, 0x92, 0x97, 0xC4, 0x87, 0xA7, 0xB1, 0x11),
            },
            RequestSID.InputOutputControlByIdentifier,
            None,
            bytearray([0x2F, 0x3A, 0xD3, 0x03,
                       0x1C, 0xCB, 0x9A, 0x7A, 0xC1, 0x66, 0xD6, 0xAE, 0xB8, 0x9F, 0x22, 0x1B, 0xC2, 0x79,
                       0x96, 0x47, 0xE0, 0xC8, 0xE3, 0xE8, 0x09, 0x92, 0x97, 0xC4, 0x87, 0xA7, 0xB1, 0x11])
        ),
        (
            {
                "DID": 0xF186,
                "inputOutputControlParameter": 0x03,
                "controlState": 0x40,
            },
            RequestSID.InputOutputControlByIdentifier,
            None,
            bytearray([0x2F, 0xF1, 0x86, 0x03,
                       0x40])
        ),
        (
            {
                "DID": 0xBA8B,
                "inputOutputControlParameter": 0x03,
                "controlState": (0x90,),
            },
            None,
            ResponseSID.InputOutputControlByIdentifier,
            bytearray([0x6F, 0xBA, 0x8B, 0x03,
                       0x90])
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
        # returnControlToECU (0x00)
        (
            [0x2F, 0xFF, 0x01, 0x00],
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
                    'physical_value': "ReservedForISO15765-5",
                    'raw_value': 0xFF01,
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
            [0x6F, 0x04, 0x63, 0x00, 0x64, 0x4D, 0x4E, 0xA7, 0xA5, 0xE3, 0x84, 0x1F],
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
                    'physical_value': 0x0463,
                    'raw_value': 0x0463,
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
                    'children': ((), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'controlState',
                    'physical_value': (0x64, 0x4D, 0x4E, 0xA7, 0xA5, 0xE3, 0x84, 0x1F),
                    'raw_value': (0x64, 0x4D, 0x4E, 0xA7, 0xA5, 0xE3, 0x84, 0x1F),
                    'unit': None
                },
            )
        ),
        # resetToDefault (0x01)
        (
            [0x2F, 0x6B, 0xC0, 0x01],
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
                    'physical_value': 0x6BC0,
                    'raw_value': 0x6BC0,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'inputOutputControlParameter',
                    'physical_value': "resetToDefault",
                    'raw_value': 0x01,
                    'unit': None
                },
            )
        ),
        (
            [0x6F, 0x92, 0xDD, 0x01, 0x53, 0x4B, 0xC2, 0xA4, 0xD8, 0x41, 0x2F, 0x72, 0x24],
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
                    'physical_value': 0x92DD,
                    'raw_value': 0x92DD,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'inputOutputControlParameter',
                    'physical_value': "resetToDefault",
                    'raw_value': 0x01,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'controlState',
                    'physical_value': (0x53, 0x4B, 0xC2, 0xA4, 0xD8, 0x41, 0x2F, 0x72, 0x24),
                    'raw_value': (0x53, 0x4B, 0xC2, 0xA4, 0xD8, 0x41, 0x2F, 0x72, 0x24),
                    'unit': None
                },
            )
        ),
        # freezeCurrentState (0x02)
        (
            [0x2F, 0xAE, 0xE7, 0x02],
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
                    'physical_value': 0xAEE7,
                    'raw_value': 0xAEE7,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'inputOutputControlParameter',
                    'physical_value': "freezeCurrentState",
                    'raw_value': 0x02,
                    'unit': None
                },
            )
        ),
        (
            [0x6F, 0x93, 0x85, 0x02, 0x61, 0x39, 0x8E, 0xDF, 0xA7, 0x80, 0x4A, 0x9B, 0x26, 0xB6, 0x4A, 0x9D, 0x46,
             0x95, 0xFA, 0x56, 0xEC, 0xAD, 0x3E, 0xD4],
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
                    'physical_value': 0x9385,
                    'raw_value': 0x9385,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'inputOutputControlParameter',
                    'physical_value': "freezeCurrentState",
                    'raw_value': 0x02,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'controlState',
                    'physical_value': (0x61, 0x39, 0x8E, 0xDF, 0xA7, 0x80, 0x4A, 0x9B, 0x26, 0xB6, 0x4A, 0x9D, 0x46,
                                       0x95, 0xFA, 0x56, 0xEC, 0xAD, 0x3E, 0xD4),
                    'raw_value': (0x61, 0x39, 0x8E, 0xDF, 0xA7, 0x80, 0x4A, 0x9B, 0x26, 0xB6, 0x4A, 0x9D, 0x46,
                                  0x95, 0xFA, 0x56, 0xEC, 0xAD, 0x3E, 0xD4),
                    'unit': None
                },
            )
        ),
        # shortTermAdjustment (0x03)
        (
            [0x2F, 0xF1, 0x86, 0x03, 0x02],
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
                    'physical_value': 'ActiveDiagnosticSessionDataIdentifier',
                    'raw_value': 0xF186,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'inputOutputControlParameter',
                    'physical_value': "shortTermAdjustment",
                    'raw_value': 0x03,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 1,
                            'name': 'reserved',
                            'physical_value': 0,
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 7,
                            'name': 'ActiveDiagnosticSession',
                            'physical_value': 'programmingSession',
                            'raw_value': 0x02,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'controlState',
                    'physical_value': 0x02,
                    'raw_value': 0x02,
                    'unit': None
                },
            )
        ),
        (
            [0x6F, 0xE1, 0x66, 0x03, 0xBD],
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
                    'physical_value': 0xE166,
                    'raw_value': 0xE166,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'inputOutputControlParameter',
                    'physical_value': "shortTermAdjustment",
                    'raw_value': 0x03,
                    'unit': None
                },
                {
                    'children': ((),),
                    'length': 8,
                    'name': 'controlState',
                    'physical_value': (0xBD,),
                    'raw_value': (0xBD,),
                    'unit': None
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2020.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        # returnControlToECU (0x00)
        (
            {
                "DID": 0x9F0A,
                "inputOutputControlParameter": 0x00,
            },
            RequestSID.InputOutputControlByIdentifier,
            None,
            bytearray([0x2F, 0x9F, 0x0A, 0x00])
        ),
        (
            {
                "DID": 0x9328,
                "inputOutputControlParameter": 0x00,
                "controlState": (0x22, 0x36, 0x1D, 0x28, 0x8D, 0x4D, 0x74, 0x13, 0x3B, 0x4F, 0x1A, 0x77, 0x9F, 0x1F,
                                 0xBB, 0x9B)
            },
            None,
            ResponseSID.InputOutputControlByIdentifier,
            bytearray([0x6F, 0x93, 0x28, 0x00,
                       0x22, 0x36, 0x1D, 0x28, 0x8D, 0x4D, 0x74, 0x13, 0x3B, 0x4F, 0x1A, 0x77, 0x9F, 0x1F, 0xBB, 0x9B])
        ),
        # resetToDefault (0x01)
        (
            {
                "DID": 0x6AB3,
                "inputOutputControlParameter": 0x01,
            },
            RequestSID.InputOutputControlByIdentifier,
            None,
            bytearray([0x2F, 0x6A, 0xB3, 0x01])
        ),
        (
            {
                "DID": 0xAF1A,
                "inputOutputControlParameter": 0x01,
                "controlState": (0xEF,)
            },
            None,
            ResponseSID.InputOutputControlByIdentifier,
            bytearray([0x6F, 0xAF, 0x1A, 0x01,
                       0xEF])
        ),
        # freezeCurrentState (0x02)
        (
            {
                "DID": 0xDC64,
                "inputOutputControlParameter": 0x02,
            },
            RequestSID.InputOutputControlByIdentifier,
            None,
            bytearray([0x2F, 0xDC, 0x64, 0x02])
        ),
        (
            {
                "DID": 0xE9ED,
                "inputOutputControlParameter": 0x02,
                "controlState": (0xAB, 0x7C, 0xC9, 0x26, 0x98, 0x3E, 0x4B, 0x6E, 0x69, 0x4D, 0x37, 0xD2, 0x2D, 0x70,
                                 0xD3, 0xC8),
            },
            None,
            ResponseSID.InputOutputControlByIdentifier,
            bytearray([0x6F, 0xE9, 0xED, 0x02,
                       0xAB, 0x7C, 0xC9, 0x26, 0x98, 0x3E, 0x4B, 0x6E, 0x69, 0x4D, 0x37, 0xD2, 0x2D, 0x70, 0xD3, 0xC8])
        ),
        # shortTermAdjustment (0x03)
        (
            {
                "DID": 0x32CB,
                "inputOutputControlParameter": 0x03,
                "controlState": (0x6B, 0x65, 0x01, 0xAD),
            },
            RequestSID.InputOutputControlByIdentifier,
            None,
            bytearray([0x2F, 0x32, 0xCB, 0x03,
                       0x6B, 0x65, 0x01, 0xAD])
        ),
        (
            {
                "DID": 0xF186,
                "inputOutputControlParameter": 0x03,
                "controlState": (0x60,),
                "controlEnableMask": (0x7F,),
            },
            RequestSID.InputOutputControlByIdentifier,
            None,
            bytearray([0x2F, 0xF1, 0x86, 0x03,
                       0x60,
                       0x7F])
        ),
        (
            {
                "DID": 0xCDEA,
                "inputOutputControlParameter": 0x03,
                "controlState": (0x1E, 0xD7, 0x04, 0xF2),
            },
            None,
            ResponseSID.InputOutputControlByIdentifier,
            bytearray([0x6F, 0xCD, 0xEA, 0x03,
                       0x1E, 0xD7, 0x04, 0xF2])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2020.encode(data_records_values=data_records_values,
                                                        sid=sid,
                                                        rsid=rsid) == payload

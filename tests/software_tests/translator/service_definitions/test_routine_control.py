import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.routine_control import ROUTINE_CONTROL


class TestRoutineControl:
    """Unit tests for `RoutineControl` service."""

    def test_request_sid(self):
        assert ROUTINE_CONTROL.request_sid == RequestSID.RoutineControl

    def test_response_sid(self):
        assert ROUTINE_CONTROL.response_sid == ResponseSID.RoutineControl


@pytest.mark.integration
class TestRoutineControlIntegration:
    """Integration tests for `RoutineControl` service."""

    @pytest.mark.parametrize("payload, decoded_message", [
        # startRoutine (0x01)
        (
            [0x31, 0x81, 0xE2, 0x00, 0x12, 0x34, 0x56, 0x78],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'RoutineControl',
                    'raw_value': 0x31,
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
                            'name': 'routineControlType',
                            'physical_value': 'startRoutine',
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
                    'children': (),
                    'length': 16,
                    'name': 'RID',
                    'physical_value': 'Execute SPL',
                    'raw_value': 0xE200,
                    'unit': None
                },
                {
                    'children': ((), (), (), ()),
                    'length': 8,
                    'name': 'routineControlOption',
                    'physical_value': (0x12, 0x34, 0x56, 0x78),
                    'raw_value': (0x12, 0x34, 0x56, 0x78),
                    'unit': None
                },
            )
        ),
        (
            [0x71, 0x01, 0x47, 0xE1],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'RoutineControl',
                    'raw_value': 0x71,
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
                            'name': 'routineControlType',
                            'physical_value': 'startRoutine',
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
                    'children': (),
                    'length': 16,
                    'name': 'RID',
                    'physical_value': 0x47E1,
                    'raw_value': 0x47E1,
                    'unit': None
                },
            )
        ),
        # stopRoutine (0x02)
        (
            [0x31, 0x02, 0xFB, 0xE5],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'RoutineControl',
                    'raw_value': 0x31,
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
                            'name': 'routineControlType',
                            'physical_value': 'stopRoutine',
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
                    'children': (),
                    'length': 16,
                    'name': 'RID',
                    'physical_value': 0xFBE5,
                    'raw_value': 0xFBE5,
                    'unit': None
                },
            )
        ),
        (
            [0x71, 0x82, 0xFF, 0x01, 0x05, 0x48, 0xBD, 0x74, 0x52, 0xF8, 0x7E, 0xFD, 0x4D, 0xC8, 0x76, 0x12, 0x63],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'RoutineControl',
                    'raw_value': 0x71,
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
                            'name': 'routineControlType',
                            'physical_value': 'stopRoutine',
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
                    'children': (),
                    'length': 16,
                    'name': 'RID',
                    'physical_value': "checkProgrammingDependencies",
                    'raw_value': 0xFF01,
                    'unit': None
                },
                {
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'routineStatus',
                    'physical_value': (0x05, 0x48, 0xBD, 0x74, 0x52, 0xF8, 0x7E, 0xFD, 0x4D, 0xC8, 0x76, 0x12, 0x63),
                    'raw_value': (0x05, 0x48, 0xBD, 0x74, 0x52, 0xF8, 0x7E, 0xFD, 0x4D, 0xC8, 0x76, 0x12, 0x63),
                    'unit': None
                },
            )
        ),
        # requestRoutineResults (0x03)
        (
            [0x31, 0x83, 0xFF, 0x00],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'RoutineControl',
                    'raw_value': 0x31,
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
                            'name': 'routineControlType',
                            'physical_value': 'requestRoutineResults',
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
                {
                    'children': (),
                    'length': 16,
                    'name': 'RID',
                    'physical_value': 'eraseMemory',
                    'raw_value': 0xFF00,
                    'unit': None
                },
            )
        ),
        (
            [0x71, 0x03, 0x00, 0x00, 0xFF],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'RoutineControl',
                    'raw_value': 0x71,
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
                            'name': 'routineControlType',
                            'physical_value': 'requestRoutineResults',
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
                {
                    'children': (),
                    'length': 16,
                    'name': 'RID',
                    'physical_value': 0x0000,
                    'raw_value': 0x0000,
                    'unit': None
                },
                {
                    'children': ((),),
                    'length': 8,
                    'name': 'routineStatus',
                    'physical_value': (0xFF, ),
                    'raw_value': (0xFF, ),
                    'unit': None
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert ROUTINE_CONTROL.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        # startRoutine (0x01)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": False,
                    "routineControlType": 0x01
                },
                "RID": 0xF0E1
            },
            RequestSID.RoutineControl,
            None,
            bytearray([0x31, 0x01, 0xF0, 0xE1])
        ),
        (
            {
                "SubFunction": 0x81,
                "RID": 0xFFFF,
                "routineStatus": (0x00,),
            },
            None,
            ResponseSID.RoutineControl,
            bytearray([0x71, 0x81, 0xFF, 0xFF, 0x00])
        ),
        # stopRoutine (0x02)
        (
            {
                "SubFunction": 0x82,
                "RID": 0xB97F,
                "routineControlOption": (0x93,),
            },
            RequestSID.RoutineControl,
            None,
            bytearray([0x31, 0x82, 0xB9, 0x7F, 0x93])
        ),
        (
            {
                "SubFunction": 0x02,
                "RID": 0x969F,
            },
            None,
            ResponseSID.RoutineControl,
            bytearray([0x71, 0x02, 0x96, 0x9F])
        ),
        # requestRoutineResults (0x03)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": False,
                    "routineControlType": 0x03
                },
                "RID": 0xB12C,
                "routineControlOption": (0xE5, 0xD1, 0x12, 0x2C, 0xE0, 0xD9, 0x9C, 0x13, 0x4C),
            },
            RequestSID.RoutineControl,
            None,
            bytearray([0x31, 0x03, 0xB1, 0x2C, 0xE5, 0xD1, 0x12, 0x2C, 0xE0, 0xD9, 0x9C, 0x13, 0x4C])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": True,
                    "routineControlType": 0x03
                },
                "RID": 0xD07C,
                "routineStatus": (0x25, 0x81, 0xF8, 0x43, 0x23, 0x3D, 0x5E, 0x9B, 0x5F, 0x1E),
            },
            None,
            ResponseSID.RoutineControl,
            bytearray([0x71, 0x83, 0xD0, 0x7C, 0x25, 0x81, 0xF8, 0x43, 0x23, 0x3D, 0x5E, 0x9B, 0x5F, 0x1E])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert ROUTINE_CONTROL.encode(data_records_values=data_records_values,
                                      sid=sid,
                                      rsid=rsid) == payload

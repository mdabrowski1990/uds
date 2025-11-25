import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.access_timing_parameter import ACCESS_TIMING_PARAMETER_2013


class TestAccessTimingParameter:
    """Unit tests for `AccessTimingParameter` service."""

    def test_request_sid(self):
        assert ACCESS_TIMING_PARAMETER_2013.request_sid == RequestSID.AccessTimingParameter

    def test_response_sid(self):
        assert ACCESS_TIMING_PARAMETER_2013.response_sid == ResponseSID.AccessTimingParameter


@pytest.mark.integration
class TestAccessTimingParameter2013Integration:
    """Integration tests for `AccessTimingParameter` service version 2013."""

    @pytest.mark.parametrize("payload, decoded_message", [
        # readExtendedTimingParameterSet (0x01)
        (
            [0x83, 0x01],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'AccessTimingParameter',
                    'raw_value': 0x83,
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
                            'name': 'timingParameterAccessType',
                            'physical_value': 'readExtendedTimingParameterSet',
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
            )
        ),
        (
            [0xC3, 0x81, 0x00],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'AccessTimingParameter',
                    'raw_value': 0xC3,
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
                            'name': 'timingParameterAccessType',
                            'physical_value': 'readExtendedTimingParameterSet',
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
                    'children': ((),),
                    'length': 8,
                    'name': 'TimingParameterResponseRecord',
                    'physical_value': (0x00,),
                    'raw_value': (0x00,),
                    'unit': None
                },
            )
        ),
        # setTimingParametersToDefaultValues (0x02)
        (
            [0x83, 0x82],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'AccessTimingParameter',
                    'raw_value': 0x83,
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
                            'name': 'timingParameterAccessType',
                            'physical_value': 'setTimingParametersToDefaultValues',
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
            )
        ),
        (
            [0xC3, 0x02],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'AccessTimingParameter',
                    'raw_value': 0xC3,
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
                            'name': 'timingParameterAccessType',
                            'physical_value': 'setTimingParametersToDefaultValues',
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
            )
        ),
        # readCurrentlyActiveTimingParameters (0x03)
        (
            [0x83, 0x03],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'AccessTimingParameter',
                    'raw_value': 0x83,
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
                            'name': 'timingParameterAccessType',
                            'physical_value': 'readCurrentlyActiveTimingParameters',
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
            )
        ),
        (
            [0xC3, 0x83, 0x87, 0x5B, 0xFF, 0x5C, 0x7B, 0x8F, 0xE7, 0x54, 0x3D, 0xA3, 0xAF, 0xA3, 0x98, 0xE2],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'AccessTimingParameter',
                    'raw_value': 0xC3,
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
                            'name': 'timingParameterAccessType',
                            'physical_value': 'readCurrentlyActiveTimingParameters',
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
                    'children': ((), (), (), (), (), (), (), (), (), (), (), (), (), ()),
                    'length': 8,
                    'name': 'TimingParameterResponseRecord',
                    'physical_value': (0x87, 0x5B, 0xFF, 0x5C, 0x7B, 0x8F, 0xE7, 0x54, 0x3D, 0xA3, 0xAF, 0xA3, 0x98, 0xE2),
                    'raw_value': (0x87, 0x5B, 0xFF, 0x5C, 0x7B, 0x8F, 0xE7, 0x54, 0x3D, 0xA3, 0xAF, 0xA3, 0x98, 0xE2),
                    'unit': None
                },
            )
        ),
        # setTimingParametersToGivenValues (0x04)
        (
            [0x83, 0x84, 0xA3],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'AccessTimingParameter',
                    'raw_value': 0x83,
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
                            'name': 'timingParameterAccessType',
                            'physical_value': 'setTimingParametersToGivenValues',
                            'raw_value': 0x04,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x84,
                    'raw_value': 0x84,
                    'unit': None
                },
                {
                    'children': ((),),
                    'length': 8,
                    'name': 'TimingParameterRequestRecord',
                    'physical_value': (0xA3,),
                    'raw_value': (0xA3,),
                    'unit': None
                },
            )
        ),
        (
            [0xC3, 0x04],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'AccessTimingParameter',
                    'raw_value': 0xC3,
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
                            'name': 'timingParameterAccessType',
                            'physical_value': 'setTimingParametersToGivenValues',
                            'raw_value': 0x04,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x04,
                    'raw_value': 0x04,
                    'unit': None
                },
            )
        ),
    ])
    def test_decode(self, payload, decoded_message):
        assert ACCESS_TIMING_PARAMETER_2013.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        # readExtendedTimingParameterSet (0x01)
        (
            {
                "SubFunction": 0x81,
            },
            RequestSID.AccessTimingParameter,
            None,
            bytearray([0x83, 0x81])
        ),
        (
            {
                "SubFunction": 0x01,
                "TimingParameterResponseRecord": (0x14, 0x67, 0x82, 0x13, 0x7F, 0x1C, 0x92, 0x5A, 0x5C, 0x03, 0x74,
                                                  0x92, 0x7F, 0x42, 0x98, 0xB9),
            },
            None,
            ResponseSID.AccessTimingParameter,
            bytearray([0xC3, 0x01, 0x14, 0x67, 0x82, 0x13, 0x7F, 0x1C, 0x92, 0x5A, 0x5C, 0x03, 0x74, 0x92, 0x7F, 0x42,
                       0x98, 0xB9])
        ),
        # setTimingParametersToDefaultValues (0x02)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": False,
                    "timingParameterAccessType": 0x02,
                },
            },
            RequestSID.AccessTimingParameter,
            None,
            bytearray([0x83, 0x02])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": True,
                    "timingParameterAccessType": 0x02,
                },
            },
            None,
            ResponseSID.AccessTimingParameter,
            bytearray([0xC3, 0x82])
        ),
        # readCurrentlyActiveTimingParameters (0x03)
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": True,
                    "timingParameterAccessType": 0x03,
                },
            },
            RequestSID.AccessTimingParameter,
            None,
            bytearray([0x83, 0x83])
        ),
        (
            {
                "SubFunction": 0x03,
                "TimingParameterResponseRecord": (0xE3,),
            },
            None,
            ResponseSID.AccessTimingParameter,
            bytearray([0xC3, 0x03, 0xE3])
        ),
        # setTimingParametersToGivenValues (0x04)
        (
            {
                "SubFunction": 0x04,
                "TimingParameterRequestRecord": (0x5D, 0x23, 0x8D, 0x79, 0x07, 0x9A, 0xC3, 0x76, 0x4D, 0x9F, 0x7B, 0x12,
                                                 0x8F, 0xB9, 0x56, 0x4F, 0xF2, 0x54),
            },
            RequestSID.AccessTimingParameter,
            None,
            bytearray([0x83, 0x04, 0x5D, 0x23, 0x8D, 0x79, 0x07, 0x9A, 0xC3, 0x76, 0x4D, 0x9F, 0x7B, 0x12, 0x8F, 0xB9,
                       0x56, 0x4F, 0xF2, 0x54])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": True,
                    "timingParameterAccessType": 0x04,
                },
            },
            None,
            ResponseSID.AccessTimingParameter,
            bytearray([0xC3, 0x84])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert ACCESS_TIMING_PARAMETER_2013.encode(data_records_values=data_records_values,
                                                        sid=sid,
                                                        rsid=rsid) == payload

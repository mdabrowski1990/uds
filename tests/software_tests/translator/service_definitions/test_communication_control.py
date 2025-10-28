import pytest

from uds.message import RequestSID, ResponseSID
from uds.translator.service_definitions.communication_control import COMMUNICATION_CONTROL


class TestCommunicationControl:
    """Unit tests for `CommunicationControl` service."""

    def test_request_sid(self):
        assert COMMUNICATION_CONTROL.request_sid == RequestSID.CommunicationControl

    def test_response_sid(self):
        assert COMMUNICATION_CONTROL.response_sid == ResponseSID.CommunicationControl


@pytest.mark.integration
class TestCommunicationControlIntegration:
    """Integration tests for `CommunicationControl` service."""

    @pytest.mark.parametrize("payload, decoded_message", [
        (
            [0x28, 0x00, 0x40],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'CommunicationControl',
                    'raw_value': 0x28,
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
                            'name': 'controlType',
                            'physical_value': 'enableRxAndTx',
                            'raw_value': 0x00,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x00,
                    'raw_value': 0x00,
                    'unit': None
                },
                {
                    'children': (
                        {
                            'children': (),
                            'length': 2,
                            'name': 'messagesType',
                            'physical_value': 'normalCommunicationMessages',
                            'raw_value': 1,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 2,
                            'name': 'reserved',
                            'physical_value': 0,
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'networks',
                            'physical_value': 'all connected networks',
                            'raw_value': 0x0,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'communicationType',
                    'physical_value': 0x40,
                    'raw_value': 0x40,
                    'unit': None
                },
            )
        ),
        (
            [0x28, 0x84, 0xCF, 0xF1, 0xDE],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'CommunicationControl',
                    'raw_value': 0x28,
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
                            'name': 'controlType',
                            'physical_value': 'enableRxAndDisableTxWithEnhancedAddressInformation',
                            'raw_value': 0x4,
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
                    'children': (
                        {
                            'children': (),
                            'length': 2,
                            'name': 'messagesType',
                            'physical_value': 'networkManagementCommunicationMessages and normalCommunicationMessages',
                            'raw_value': 3,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 2,
                            'name': 'reserved',
                            'physical_value': 0,
                            'raw_value': 0,
                            'unit': None
                        },
                        {
                            'children': (),
                            'length': 4,
                            'name': 'networks',
                            'physical_value': 'network on which this request is received',
                            'raw_value': 0xF,
                            'unit': None
                        },
                    ),
                    'length': 8,
                    'name': 'communicationType',
                    'physical_value': 0xCF,
                    'raw_value': 0xCF,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 16,
                    'name': 'nodeIdentificationNumber',
                    'physical_value': 0xF1DE,
                    'raw_value': 0xF1DE,
                    'unit': None
                },
            )
        ),
        (
            [0x68, 0x01],
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'CommunicationControl',
                    'raw_value': 0x68,
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
                            'name': 'controlType',
                            'physical_value': 'enableRxAndDisableTx',
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
    ])
    def test_decode(self, payload, decoded_message):
        assert COMMUNICATION_CONTROL.decode(payload) == decoded_message

    @pytest.mark.parametrize("data_records_values, sid, rsid, payload", [
        (
            {
                "SubFunction": 0x03,
                "communicationType": 0x31,
            },
            RequestSID.CommunicationControl,
            None,
            bytearray([0x28, 0x03, 0x31])
        ),
        (
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": True,
                    "controlType": 0x05
                },
                "communicationType": {
                    "messagesType": 2,
                    "reserved": 0,
                    "networks": 0xA,
                },
                "nodeIdentificationNumber": 0x0005
            },
            RequestSID.CommunicationControl,
            None,
            bytearray([0x28, 0x85, 0x8A, 0x00, 0x05])
        ),
        (
            {
                "SubFunction": 0x85,
            },
            None,
            ResponseSID.CommunicationControl,
            bytearray([0x68, 0x85])
        ),
    ])
    def test_encode(self, data_records_values, sid, rsid, payload):
        assert COMMUNICATION_CONTROL.encode(data_records_values=data_records_values,
                                                 sid=sid,
                                                 rsid=rsid) == payload

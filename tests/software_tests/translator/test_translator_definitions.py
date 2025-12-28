import pytest

import uds.translator.service_definitions
from uds.addressing import AddressingType
from uds.message import NRC, RequestSID, ResponseSID, UdsMessage
from uds.translator import BASE_TRANSLATOR, BASE_TRANSLATOR_2013, BASE_TRANSLATOR_2020


class TestTranslatorDefinitions:
    """Unit tests for translator definitions."""

    @staticmethod
    def _get_services_definitions_names():
        return (service_def_name
                for service_def_name in vars(uds.translator.service_definitions).keys()
                if service_def_name.isupper() and not service_def_name.startswith("_"))

    def test_services_definition(self):
        """Make sure that all services definition are used in translators."""
        for service_def_name in self._get_services_definitions_names():
            service_def = getattr(uds.translator.service_definitions, service_def_name)
            if service_def_name.endswith("2013"):
                assert service_def in BASE_TRANSLATOR_2013.services
            elif service_def_name.endswith("2020"):
                assert service_def in BASE_TRANSLATOR_2020.services
            else:
                assert service_def in BASE_TRANSLATOR.services

    def test_default_translator(self):
        assert BASE_TRANSLATOR is BASE_TRANSLATOR_2020

    @pytest.mark.parametrize("translator", [BASE_TRANSLATOR_2020, BASE_TRANSLATOR_2013])
    @pytest.mark.parametrize("sid, rsid, data_records_values, payload", [
        (
            RequestSID.DiagnosticSessionControl,
            None,
            {
                "SubFunction": 0x81,
            },
            bytearray([0x10, 0x81])
        ),
        (
            None,
            ResponseSID.DiagnosticSessionControl,
            {
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": False,
                    "diagnosticSessionType": 0x03,
                },
                "sessionParameterRecord": {
                    "P2Server_max": 0x1234,
                    "P2*Server_max": 0x5678
                }
            },
            bytearray([0x50, 0x03, 0x12, 0x34, 0x56, 0x78])
        ),
        (
            RequestSID.DiagnosticSessionControl,
            ResponseSID.NegativeResponse,
            {
                "NRC": NRC.ConditionsNotCorrect,
            },
            bytearray([0x7F, 0x10, 0x22])
        ),
    ])
    def test_encode(self, translator, sid, rsid, data_records_values, payload):
        assert translator.encode(sid=sid,
                                 rsid=rsid,
                                 data_records_values=data_records_values) == payload

    @pytest.mark.parametrize("translator", [BASE_TRANSLATOR_2020, BASE_TRANSLATOR_2013])
    @pytest.mark.parametrize("message, decoded_message", [
        (
            UdsMessage(payload=[0x10, 0x81], addressing_type=AddressingType.PHYSICAL),
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'DiagnosticSessionControl',
                    'raw_value': 0x10,
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
                            'name': 'diagnosticSessionType',
                            'physical_value': 'defaultSession',
                            'raw_value': 0x01,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x81,
                    'raw_value': 0x81,
                    'unit': None
                }
            )
        ),
        (
            UdsMessage(payload=[0x50, 0x03, 0x12, 0x34, 0x56, 0x78], addressing_type=AddressingType.FUNCTIONAL),
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'DiagnosticSessionControl',
                    'raw_value': 0x50,
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
                            'unit': None},
                        {
                            'children': (),
                            'length': 7,
                            'name': 'diagnosticSessionType',
                            'physical_value': 'extendedDiagnosticSession',
                            'raw_value': 0x03,
                            'unit': None
                        }
                    ),
                    'length': 8,
                    'name': 'SubFunction',
                    'physical_value': 0x03,
                    'raw_value': 0x03,
                    'unit': None},
                {
                    'children': (
                        {
                            'children': (),
                            'length': 16,
                            'name': 'P2Server_max',
                            'physical_value': 0x1234,
                            'raw_value': 0x1234,
                            'unit': 'ms'
                        },
                        {
                            'children': (),
                            'length': 16,
                            'name': 'P2*Server_max',
                            'physical_value': 0x5678 * 10,
                            'raw_value': 0x5678,
                            'unit': 'ms'
                        }
                    ),
                    'length': 32,
                    'name': 'sessionParameterRecord',
                    'physical_value': 0x12345678,
                    'raw_value': 0x12345678,
                    'unit': None
                }
            )
        ),
        (
            UdsMessage(payload=[0x7F, 0x10, 0x22], addressing_type=AddressingType.PHYSICAL),
            (
                {
                    'children': (),
                    'length': 8,
                    'name': 'RSID',
                    'physical_value': 'NegativeResponse',
                    'raw_value': 0x7F,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'SID',
                    'physical_value': 'DiagnosticSessionControl',
                    'raw_value': 0x10,
                    'unit': None
                },
                {
                    'children': (),
                    'length': 8,
                    'name': 'NRC',
                    'physical_value': 'ConditionsNotCorrect',
                    'raw_value': 0x22,
                    'unit': None
                }
            )
        ),
    ])
    def test_decode(self, translator, message, decoded_message):
        assert translator.decode(message=message) == decoded_message
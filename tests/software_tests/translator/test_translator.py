import pytest
from mock import MagicMock, Mock, patch

from uds.addressing import AddressingType
from uds.message import NRC, UdsMessage
from uds.translator.data_record import (
    DEFAULT_DIAGNOSTIC_MESSAGE_CONTINUATION,
    ConditionalFormulaDataRecord,
    ConditionalMappingDataRecord,
    LinearFormulaDataRecord,
    MappingDataRecord,
    MultipleOccurrencesInfo,
    RawDataRecord,
    SingleOccurrenceInfo,
    TextDataRecord,
    TextEncoding,
)
from uds.translator.translator import (
    Collection,
    MappingProxyType,
    RequestSID,
    ResponseSID,
    Service,
    Translator,
    UdsMessage,
    UdsMessageRecord,
)

SCRIPT_LOCATION = "uds.translator.translator"


class TestTranslator:
    """Unit tests for `Translator` class."""

    def setup_method(self):
        self.mock_translator = Mock(spec=Translator)

    # __init__

    @pytest.mark.parametrize("services", [Mock(), [Mock(), Mock()]])
    def test_init(self, services):
        Translator.__init__(self.mock_translator, services=services)
        assert self.mock_translator.services == services

    # services

    def test_services__get(self):
        self.mock_translator._Translator__services = Mock()
        assert Translator.services.fget(self.mock_translator) == self.mock_translator._Translator__services

    @pytest.mark.parametrize("services", [Mock(), [Mock(), Mock()]])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_services__set__type_error(self, mock_isinstance, services):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            Translator.services.fset(self.mock_translator, services)
        mock_isinstance.assert_called_once_with(services, Collection)

    @pytest.mark.parametrize("services", [
        {Mock(spec=Service), Mock(spec=Service), Mock()},
        [Mock(spec=Service, request_sid=1, response_sid=2),
         Mock(spec=Service, request_sid=4, response_sid=5),
         Mock(spec=Service, request_sid=3, response_sid=4)],
    ])
    def test_services__set__value_error(self, services):
        with pytest.raises(ValueError):
            Translator.services.fset(self.mock_translator, services)

    @pytest.mark.parametrize("services", [
        {Mock(spec=Service), Mock(spec=Service), Mock(spec=Service)},
        [Mock(spec=Service, request_sid=1, response_sid=2),
         Mock(spec=Service, request_sid=4, response_sid=5),
         Mock(spec=Service, request_sid=3, response_sid=6)],
    ])
    def test_services__set__valid(self, services):
        services_dict = {}
        for service in services:
            services_dict[service.request_sid] = service
            services_dict[service.response_sid] = service
        Translator.services.fset(self.mock_translator, services)
        assert self.mock_translator._Translator__services == frozenset(services)
        assert self.mock_translator._Translator__services_mapping == MappingProxyType(services_dict)

    # services_mapping

    def test_services_mapping__get(self):
        self.mock_translator._Translator__services_mapping = Mock()
        assert (Translator.services_mapping.fget(self.mock_translator)
                == self.mock_translator._Translator__services_mapping)

    # encode

    @pytest.mark.parametrize("sid", [0x10, 0x3E])
    def test_encode__encode_request(self, sid):
        mock_service = Mock()
        mock_getitem = MagicMock(return_value=mock_service)
        mock_contains = Mock(return_value=True)
        self.mock_translator.services_mapping = MagicMock(__getitem__=mock_getitem, __contains__=mock_contains)
        mock_data_records_values = MagicMock()
        assert (Translator.encode(self.mock_translator, sid=sid, data_records_values=mock_data_records_values)
                == mock_service.encode_request.return_value)
        mock_getitem.assert_called_once_with(sid)
        mock_service.encode_request.assert_called_once_with(data_records_values=mock_data_records_values)

    @pytest.mark.parametrize("rsid", [0x50, 0x7E])
    def test_encode__encode_positive_response(self, rsid):
        mock_service = Mock()
        mock_getitem = MagicMock(return_value=mock_service)
        mock_contains = Mock(return_value=True)
        self.mock_translator.services_mapping = MagicMock(__getitem__=mock_getitem, __contains__=mock_contains)
        mock_data_records_values = MagicMock()
        assert (Translator.encode(self.mock_translator, rsid=rsid, data_records_values=mock_data_records_values)
                == mock_service.encode_positive_response.return_value)
        mock_getitem.assert_called_once_with(rsid)
        mock_service.encode_positive_response.assert_called_once_with(data_records_values=mock_data_records_values)

    @pytest.mark.parametrize("rsid, sid", [
        (0x7F, 0x10),
        (ResponseSID.NegativeResponse, 0x2E),
    ])
    def test_encode__encode_negative_response(self, rsid, sid):
        mock_service = Mock()
        mock_getitem = MagicMock(return_value=mock_service)
        mock_contains = Mock(return_value=True)
        self.mock_translator.services_mapping = MagicMock(__getitem__=mock_getitem, __contains__=mock_contains)
        mock_data_records_values = MagicMock()
        assert (Translator.encode(self.mock_translator, rsid=rsid, sid=sid, data_records_values=mock_data_records_values)
                == mock_service.encode_negative_response.return_value)
        mock_getitem.assert_called_once_with(sid)
        mock_service.encode_negative_response.assert_called_once_with(nrc=mock_data_records_values["NRC"])

    @pytest.mark.parametrize("sid, rsid, services_mapping", [
        (None, None, {}),
        (0x10, 0x7F, {0x7F: Mock()}),
        (0x10, 0x50, {0x10: Mock(), 0x50: Mock()}),
        (0x10, None, {0x11: Mock(), 0x0F: Mock()}),
        (None, 0x50, {0x4F: Mock(), 0x51: Mock()}),
    ])
    def test_encode__value_error(self, sid, rsid, services_mapping):
        self.mock_translator.services_mapping = services_mapping
        with pytest.raises(ValueError):
            Translator.encode(self.mock_translator, sid=sid, rsid=rsid, data_records_values=MagicMock())

    # decode

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x10, 0x03], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessageRecord, payload=[0x62, *range(255)])
    ])
    def test_decode__value_error(self, message):
        self.mock_translator.services_mapping = {}
        with pytest.raises(ValueError):
            Translator.decode(self.mock_translator, message)

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x10, 0x03], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessageRecord, payload=[0x62, *range(255)])
    ])
    def test_decode(self, message):
        mock_service = Mock()
        self.mock_translator.services_mapping = {message.payload[0]: mock_service}
        assert Translator.decode(self.mock_translator, message) == mock_service.decode.return_value
        mock_service.decode.assert_called_once_with(message.payload)

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x7F, 0x10, 0x65], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessageRecord, payload=[0x7F, 0x3E, 0xAB])
    ])
    def test_decode__negative_response(self, message):
        mock_service = Mock()
        self.mock_translator.services_mapping = {message.payload[1]: mock_service}
        assert Translator.decode(self.mock_translator, message) == mock_service.decode_negative_response.return_value
        mock_service.decode_negative_response.assert_called_once_with(message.payload)


@pytest.mark.integration
class TestTranslatorIntegration:
    """Integration tests for `Translator` class."""

    def setup_class(self):
        did_mapping = {
            0xF186: [MappingDataRecord(name="diagnosticSessionType",
                                       length=8,
                                       values_mapping={1: "Default",
                                                       2: "Programming",
                                                       3: "Extended"})],
            0xF187: [TextDataRecord(name="Spare Part Number",
                                    encoding=TextEncoding.ASCII,
                                    min_occurrences=1,
                                    max_occurrences=None)],
            0xF188: [TextDataRecord(name="ECU Software Number",
                                    encoding=TextEncoding.BCD,
                                    min_occurrences=2,
                                    max_occurrences=None)],
            0xF191: [TextDataRecord(name="ECU Hardware Number",
                                    encoding=TextEncoding.BCD,
                                    min_occurrences=2,
                                    max_occurrences=None)],
        }
        did_2 = MappingDataRecord(name="DID #2",
                                  length=16,
                                  values_mapping={
                                      0xF186: "ActiveDiagnosticSessionDataIdentifier",
                                      0xF187: "vehicleManufacturerSparePartNumberDataIdentifier",
                                      0xF188: "vehicleManufacturerECUSoftwareNumberDataIdentifier",
                                      0xF191: "vehicleManufacturerECUHardwareNumberDataIdentifier",
                                  },
                                  min_occurrences=0,
                                  max_occurrences=1)
        conditional_mapping = ConditionalMappingDataRecord(
            default_message_continuation=DEFAULT_DIAGNOSTIC_MESSAGE_CONTINUATION,
            mapping=did_mapping)
        diagnostic_session_control = Service(
            request_sid=RequestSID.DiagnosticSessionControl,
            request_structure=[
                RawDataRecord(name="subFunction",
                              length=8,
                              children=[
                                  MappingDataRecord(name="SPRMIB",
                                                    length=1,
                                                    values_mapping={0: "no", 1: "yes"}),
                                  MappingDataRecord(name="diagnosticSessionType",
                                                    length=7,
                                                    values_mapping={1: "Default",
                                                                    2: "Programming",
                                                                    3: "Extended"})
                              ])
            ],
            response_structure=[
                RawDataRecord(name="subFunction",
                              length=8,
                              children=[
                                  MappingDataRecord(name="SPRMIB",
                                                    length=1,
                                                    values_mapping={0: "no", 1: "yes"}),
                                  MappingDataRecord(name="diagnosticSessionType",
                                                    length=7,
                                                    values_mapping={1: "Default",
                                                                    2: "Programming",
                                                                    3: "Extended"})
                              ]),
                RawDataRecord(name="sessionParameterRecord",
                              length=32,
                              children=[
                                  LinearFormulaDataRecord(name="P2Server_max",
                                                          length=16,
                                                          factor=1,
                                                          offset=0,
                                                          unit="ms"),
                                  LinearFormulaDataRecord(name="P2*Server_max",
                                                          length=16,
                                                          factor=10,
                                                          offset=0,
                                                          unit="ms")
                              ])
            ]
        )
        read_memory_by_address = Service(
            request_sid=RequestSID.ReadMemoryByAddress,
            request_structure=[
                RawDataRecord(name="addressAndLengthFormatIdentifier",
                              length=8,
                              children=[
                                  RawDataRecord(name="memorySizeLength",
                                                length=4),
                                  RawDataRecord(name="memoryAddressLength",
                                                length=4)
                              ]),
                ConditionalFormulaDataRecord(
                    formula=lambda addressAndLengthFormatIdentifier: [
                        RawDataRecord(name="memoryAddress", length=8*(addressAndLengthFormatIdentifier & 0xF)),
                        RawDataRecord(name="memorySize", length=8*(addressAndLengthFormatIdentifier >> 4))
                    ]
                )
            ],
            response_structure=[
                RawDataRecord(name="data",
                              length=8,
                              min_occurrences=1,
                              max_occurrences=None)
            ]
        )
        read_data_by_identifier = Service(
            request_sid=RequestSID.ReadDataByIdentifier,
            request_structure=[
                MappingDataRecord(name="DID",
                                  length=16,
                                  values_mapping={
                                      0xF186: "ActiveDiagnosticSessionDataIdentifier",
                                      0xF187: "vehicleManufacturerSparePartNumberDataIdentifier",
                                      0xF188: "vehicleManufacturerECUSoftwareNumberDataIdentifier",
                                      0xF191: "vehicleManufacturerECUHardwareNumberDataIdentifier",
                                  },
                                  min_occurrences=1,
                                  max_occurrences=None)
            ],
            response_structure=[  # Simplified
                MappingDataRecord(name="DID #1",
                                  length=16,
                                  values_mapping={
                                      0xF186: "ActiveDiagnosticSessionDataIdentifier",
                                      0xF187: "vehicleManufacturerSparePartNumberDataIdentifier",
                                      0xF188: "vehicleManufacturerECUSoftwareNumberDataIdentifier",
                                      0xF191: "vehicleManufacturerECUHardwareNumberDataIdentifier",
                                  }),
                ConditionalMappingDataRecord(default_message_continuation=DEFAULT_DIAGNOSTIC_MESSAGE_CONTINUATION,
                                             mapping={
                                                 did: did_structure + [did_2, conditional_mapping] if did == 0xF186 else did_structure
                                                 for did, did_structure in did_mapping.items()
                                             })
            ],
        )
        self.translator = Translator(services={diagnostic_session_control,
                                               read_memory_by_address,
                                               read_data_by_identifier})

    # services_mapping

    def test_services_mapping(self):
        for service in self.translator.services:
            assert self.translator.services_mapping[service.request_sid] == service
            assert self.translator.services_mapping[service.response_sid] == service

    # encode

    @pytest.mark.parametrize("sid, rsid, data_records_values, payload", [
        # Diagnostic Session Control
        (
            0x10,
            None,
            {"subFunction": 0x03},
            bytearray([0x10, 0x03])
        ),
        (
            None,
            0x50,
            {
                "subFunction": {"SPRMIB": 1, "diagnosticSessionType": 3},
                "sessionParameterRecord": {"P2Server_max": 0x1234, "P2*Server_max": 0x5678}
            },
            bytearray([0x50, 0x83, 0x12, 0x34, 0x56, 0x78])
        ),
        (
            0x10,
            0x7F,
            {"NRC": 0x84},
            bytearray([0x7F, 0x10, 0x84])
        ),
        # Read Data By Identifier
        (
            RequestSID.ReadDataByIdentifier,
            None,
            {
                "DID": [0x1234, 0xF186, 0xF191]
            },
            bytearray([0x22, 0x12, 0x34, 0xF1, 0x86, 0xF1, 0x91])
        ),
        (
            None,
            ResponseSID.ReadDataByIdentifier,
            {
                "DID #1": 0xF186,
                "diagnosticSessionType": 0x01,
                "DID #2": 0xF188,
                "ECU Software Number": [9, 0, 8, 1, 7, 2]
            },
            bytearray(b"\x62\xF1\x86\x01\xF1\x88\x90\x81\x72")
        ),
        (
            RequestSID.ReadDataByIdentifier,
            ResponseSID.NegativeResponse,
            {
                "NRC": NRC.GeneralReject
            },
            bytearray([0x7F, 0x22, 0x10])
        ),
        # Read Memory By Address
        (
            RequestSID.ReadMemoryByAddress,
            None,
            {
                "addressAndLengthFormatIdentifier": 0x24,
                "memoryAddress": 0x20481392,
                "memorySize": 0x0103
            },
            bytearray([0x23, 0x24, 0x20, 0x48, 0x13, 0x92, 0x01, 0x03])
        ),
        (
            None,
            ResponseSID.ReadMemoryByAddress,
            {
                "addressAndLengthFormatIdentifier": 0x24,
                "data": [0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5, 0x96, 0x87, 0x78, 0x69, 0x5A, 0x4B, 0x3C, 0x2D, 0x1E, 0x0F],
            },
            bytearray(b"\x63\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87\x78\x69\x5A\x4B\x3C\x2D\x1E\x0F")
        ),
        (
            RequestSID.ReadMemoryByAddress,
            ResponseSID.NegativeResponse,
            {
                "NRC": NRC.ServiceNotSupportedInActiveSession
            },
            bytearray([0x7F, 0x23, 0x7F])
        )
    ])
    def test_encode(self, sid, rsid, data_records_values, payload):
        assert self.translator.encode(sid=sid,
                                      rsid=rsid,
                                      data_records_values=data_records_values) == payload

    # decode

    @pytest.mark.parametrize("message, decoded_message", [
        (
            # Diagnostic Session Control
            UdsMessage(payload=[0x10, 0x40], addressing_type=AddressingType.FUNCTIONAL),
            (
                SingleOccurrenceInfo(name="SID",
                                     length=8,
                                     raw_value=0x10,
                                     physical_value="DiagnosticSessionControl",
                                     children=tuple(),
                                     unit=None),
                SingleOccurrenceInfo(name="subFunction",
                                     length=8,
                                     raw_value=0x40,
                                     physical_value=0x40,
                                     children=(
                                         SingleOccurrenceInfo(name="SPRMIB",
                                                              length=1,
                                                              raw_value=0,
                                                              physical_value="no",
                                                              children=tuple(),
                                                              unit=None),
                                         SingleOccurrenceInfo(name="diagnosticSessionType",
                                                              length=7,
                                                              raw_value=0x40,
                                                              physical_value=0x40,
                                                              children=tuple(),
                                                              unit=None),
                                     ),
                                     unit=None),
            )
        ),
        (
            UdsMessage(payload=[0x50, 0x83, 0x12, 0x34, 0x56, 0x78], addressing_type=AddressingType.FUNCTIONAL),
            (
                SingleOccurrenceInfo(name="RSID",
                                     length=8,
                                     raw_value=0x50,
                                     physical_value="DiagnosticSessionControl",
                                     children=tuple(),
                                     unit=None),
                SingleOccurrenceInfo(name="subFunction",
                                     length=8,
                                     raw_value=0x83,
                                     physical_value=0x83,
                                     children=(
                                             SingleOccurrenceInfo(name="SPRMIB",
                                                                  length=1,
                                                                  raw_value=1,
                                                                  physical_value="yes",
                                                                  children=tuple(),
                                                                  unit=None),
                                             SingleOccurrenceInfo(name="diagnosticSessionType",
                                                                  length=7,
                                                                  raw_value=0x03,
                                                                  physical_value="Extended",
                                                                  children=tuple(),
                                                                  unit=None),
                                     ),
                                     unit=None),
                SingleOccurrenceInfo(name="sessionParameterRecord",
                                     length=32,
                                     raw_value=0x12345678,
                                     physical_value=0x12345678,
                                     children=(
                                             SingleOccurrenceInfo(name="P2Server_max",
                                                                  length=16,
                                                                  raw_value=0x1234,
                                                                  physical_value=0x1234,
                                                                  children=tuple(),
                                                                  unit="ms"),
                                             SingleOccurrenceInfo(name="P2*Server_max",
                                                                  length=16,
                                                                  raw_value=0x5678,
                                                                  physical_value=0x5678 * 10,
                                                                  children=tuple(),
                                                                  unit="ms"),
                                     ),
                                     unit=None)
            )
        ),
        (
            Mock(spec=UdsMessageRecord, payload=b"\x7F\x10\x84"),
            (
                SingleOccurrenceInfo(name="RSID",
                                     length=8,
                                     raw_value=0x7F,
                                     physical_value="NegativeResponse",
                                     children=tuple(),
                                     unit=None),
                SingleOccurrenceInfo(name="SID",
                                     length=8,
                                     raw_value=0x10,
                                     physical_value="DiagnosticSessionControl",
                                     children=tuple(),
                                     unit=None),
                SingleOccurrenceInfo(name="NRC",
                                     length=8,
                                     raw_value=0x84,
                                     physical_value="EngineIsNotRunning",
                                     children=tuple(),
                                     unit=None),
            )
        ),
        # Read Data By Identifier
        (
            UdsMessage(payload=[0x22, 0x12, 0x34, 0xF1, 0x86, 0xF1, 0x91], addressing_type=AddressingType.PHYSICAL),
            (
                SingleOccurrenceInfo(name="SID",
                                     length=8,
                                     raw_value=0x22,
                                     physical_value="ReadDataByIdentifier",
                                     children=tuple(),
                                     unit=None),
                MultipleOccurrencesInfo(name="DID",
                                        length=16,
                                        raw_value=[0x1234, 0xF186, 0xF191],
                                        physical_value=(0x1234,
                                                        "ActiveDiagnosticSessionDataIdentifier",
                                                        "vehicleManufacturerECUHardwareNumberDataIdentifier"),
                                        children=[(), (), ()],
                                        unit=None),
            )
        ),
        (
            UdsMessage(payload=b"\x62\xF1\x86\x01\xF1\x88\x90\x81\x72", addressing_type=AddressingType.FUNCTIONAL),
            (
                SingleOccurrenceInfo(name="RSID",
                                     length=8,
                                     raw_value=0x62,
                                     physical_value="ReadDataByIdentifier",
                                     children=tuple(),
                                     unit=None),
                SingleOccurrenceInfo(name="DID #1",
                                     length=16,
                                     raw_value=0xF186,
                                     physical_value="ActiveDiagnosticSessionDataIdentifier",
                                     children=tuple(),
                                     unit=None),
                SingleOccurrenceInfo(name="diagnosticSessionType",
                                     length=8,
                                     raw_value=0x01,
                                     physical_value="Default",
                                     children=tuple(),
                                     unit=None),
                SingleOccurrenceInfo(name="DID #2",
                                     length=16,
                                     raw_value=0xF188,
                                     physical_value="vehicleManufacturerECUSoftwareNumberDataIdentifier",
                                     children=tuple(),
                                     unit=None),
                MultipleOccurrencesInfo(name="ECU Software Number",
                                        length=4,
                                        raw_value=[9, 0, 8, 1, 7, 2],
                                        physical_value="908172",
                                        children=[tuple()] * 6,
                                        unit=None),
            )
        ),
        (
            Mock(spec=UdsMessageRecord, payload=b"\x7F\x22\x10"),
            (
                SingleOccurrenceInfo(name="RSID",
                                     length=8,
                                     raw_value=0x7F,
                                     physical_value="NegativeResponse",
                                     children=tuple(),
                                     unit=None),
                SingleOccurrenceInfo(name="SID",
                                     length=8,
                                     raw_value=0x22,
                                     physical_value="ReadDataByIdentifier",
                                     children=tuple(),
                                     unit=None),
                SingleOccurrenceInfo(name="NRC",
                                     length=8,
                                     raw_value=0x10,
                                     physical_value="GeneralReject",
                                     children=tuple(),
                                     unit=None),
            )
        ),
        # Read Memory By Address
        (
            UdsMessage(payload=[0x23, 0x24, 0x20, 0x48, 0x13, 0x92, 0x01, 0x03],
                       addressing_type=AddressingType.FUNCTIONAL),
            (
                SingleOccurrenceInfo(name="SID",
                                     length=8,
                                     raw_value=0x23,
                                     physical_value="ReadMemoryByAddress",
                                     children=tuple(),
                                     unit=None),
                SingleOccurrenceInfo(name="addressAndLengthFormatIdentifier",
                                     length=8,
                                     raw_value=0x24,
                                     physical_value=0x24,
                                     children=(
                                             SingleOccurrenceInfo(name="memorySizeLength",
                                                                  length=4,
                                                                  raw_value=0x2,
                                                                  physical_value=0x2,
                                                                  children=tuple(),
                                                                  unit=None),
                                             SingleOccurrenceInfo(name="memoryAddressLength",
                                                                  length=4,
                                                                  raw_value=0x4,
                                                                  physical_value=0x4,
                                                                  children=tuple(),
                                                                  unit=None),
                                     ),
                                     unit=None),
                SingleOccurrenceInfo(name="memoryAddress",
                                     length=32,
                                     raw_value=0x20481392,
                                     physical_value=0x20481392,
                                     children=tuple(),
                                     unit=None),
                SingleOccurrenceInfo(name="memorySize",
                                     length=16,
                                     raw_value=0x0103,
                                     physical_value=0x0103,
                                     children=tuple(),
                                     unit=None),
            )
        ),
        (
            UdsMessage(payload=b"\x63\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87\x78\x69\x5A\x4B\x3C\x2D\x1E\x0F",
                       addressing_type=AddressingType.FUNCTIONAL),
            (
                SingleOccurrenceInfo(name="RSID",
                                     length=8,
                                     raw_value=0x63,
                                     physical_value="ReadMemoryByAddress",
                                     children=tuple(),
                                     unit=None),
                MultipleOccurrencesInfo(name="data",
                                        length=8,
                                        raw_value=[0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5, 0x96, 0x87, 0x78, 0x69,
                                                   0x5A, 0x4B, 0x3C, 0x2D, 0x1E, 0x0F],
                                        physical_value=(0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5, 0x96, 0x87, 0x78, 0x69,
                                                        0x5A, 0x4B, 0x3C, 0x2D, 0x1E, 0x0F),
                                        children=[tuple()] * 16,
                                        unit=None),
            )
        ),
        (
            Mock(spec=UdsMessageRecord, payload=b"\x7F\x23\x7F"),
            (
                SingleOccurrenceInfo(name="RSID",
                                     length=8,
                                     raw_value=0x7F,
                                     physical_value="NegativeResponse",
                                     children=tuple(),
                                     unit=None),
                SingleOccurrenceInfo(name="SID",
                                     length=8,
                                     raw_value=0x23,
                                     physical_value="ReadMemoryByAddress",
                                     children=tuple(),
                                     unit=None),
                SingleOccurrenceInfo(name="NRC",
                                     length=8,
                                     raw_value=0x7F,
                                     physical_value="ServiceNotSupportedInActiveSession",
                                     children=tuple(),
                                     unit=None),
            )
        ),
    ])
    def test_decode(self, message, decoded_message):
        assert self.translator.decode(message=message) == decoded_message

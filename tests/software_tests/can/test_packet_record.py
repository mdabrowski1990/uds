import pytest
from mock import Mock, patch

from uds.can.packet_record import CanPacketRecord, \
    PythonCanMessage, CanAddressingInformationHandler, InconsistentArgumentsError


class TestCanPacketRecord:
    """Unit tests for `CanPacketRecord` class."""

    SCRIPT_LOCATION = "uds.can.packet_record"

    def setup(self):
        self.mock_can_packet_record = Mock(spec=CanPacketRecord)
        mock_ai = Mock(spec=CanAddressingInformationHandler,
                       TARGET_ADDRESS_NAME=CanAddressingInformationHandler.TARGET_ADDRESS_NAME,
                       SOURCE_ADDRESS_NAME=CanAddressingInformationHandler.SOURCE_ADDRESS_NAME,
                       ADDRESS_EXTENSION_NAME=CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME,
                       ADDRESSING_TYPE_NAME=CanAddressingInformationHandler.ADDRESSING_TYPE_NAME)
        # patching
        self._patcher_addressing_type_class = patch(f"{self.SCRIPT_LOCATION}.AddressingType")
        self.mock_addressing_type_class = self._patcher_addressing_type_class.start()
        self._patcher_can_addressing_format_class = patch(f"{self.SCRIPT_LOCATION}.CanAddressingFormat")
        self.mock_can_addressing_format_class = self._patcher_can_addressing_format_class.start()
        self._patcher_can_ai_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanAddressingInformationHandler", mock_ai)
        self.mock_can_ai_handler_class = self._patcher_can_ai_handler_class.start()
        self._patcher_can_packet_class = patch(f"{self.SCRIPT_LOCATION}.CanPacket")
        self.mock_can_packet_class = self._patcher_can_packet_class.start()
        self._patcher_can_packet_type_class = patch(f"{self.SCRIPT_LOCATION}.CanPacketType")
        self.mock_can_packet_type_class = self._patcher_can_packet_type_class.start()
        self._patcher_can_id_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanIdHandler")
        self.mock_can_id_handler_class = self._patcher_can_id_handler_class.start()
        self._patcher_can_dlc_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler")
        self.mock_can_dlc_handler_class = self._patcher_can_dlc_handler_class.start()
        self._patcher_abstract_uds_packet_record_init = patch(f"{self.SCRIPT_LOCATION}.AbstractUdsPacketRecord.__init__")
        self.mock_abstract_uds_packet_record_init = self._patcher_abstract_uds_packet_record_init.start()

    def teardown(self):
        self._patcher_addressing_type_class.stop()
        self._patcher_can_addressing_format_class.stop()
        self._patcher_can_ai_handler_class.stop()
        self._patcher_can_packet_class.stop()
        self._patcher_can_packet_type_class.stop()
        self._patcher_can_id_handler_class.stop()
        self._patcher_can_dlc_handler_class.stop()
        self._patcher_abstract_uds_packet_record_init.stop()

    # __init__

    @pytest.mark.parametrize("frame, direction", [
        ("some frame", "some direction"),
        (Mock(spec=PythonCanMessage), "TX"),
    ])
    @pytest.mark.parametrize("addressing_type, addressing_format, transmission_time", [
        ("some addressing type", "some format", "some timestamp"),
        ("Another type", "another format", 9.543),
    ])
    def test_init(self, frame, direction, addressing_type, addressing_format, transmission_time):
        CanPacketRecord.__init__(self=self.mock_can_packet_record,
                                 frame=frame,
                                 direction=direction,
                                 addressing_type=addressing_type,
                                 addressing_format=addressing_format,
                                 transmission_time=transmission_time)
        assert self.mock_can_packet_record._CanPacketRecord__addressing_type \
               == self.mock_addressing_type_class.return_value
        assert self.mock_can_packet_record._CanPacketRecord__addressing_format \
               == self.mock_can_addressing_format_class.return_value
        self.mock_abstract_uds_packet_record_init.assert_called_once_with(frame=frame,
                                                                          direction=direction,
                                                                          transmission_time=transmission_time)
        self.mock_can_packet_record._CanPacketRecord__assess_packet_type.assert_called_once_with()
        self.mock_can_packet_record._CanPacketRecord__assess_ai_attributes.assert_called_once_with()
        self.mock_addressing_type_class.validate_member.assert_called_once_with(addressing_type)
        self.mock_addressing_type_class.assert_called_once_with(addressing_type)
        self.mock_can_addressing_format_class.validate_member.assert_called_once_with(addressing_format)
        self.mock_can_addressing_format_class.assert_called_once_with(addressing_format)

    # raw_frame_data

    def test_raw_frame_data__python_can(self):
        self.mock_can_packet_record.frame = Mock(spec=PythonCanMessage)
        assert CanPacketRecord.raw_frame_data.fget(self=self.mock_can_packet_record) \
               == self.mock_can_packet_record.frame.data

    def test_raw_frame_data__not_implemented(self):
        self.mock_can_packet_record.frame = None
        with pytest.raises(NotImplementedError):
            CanPacketRecord.raw_frame_data.fget(self=self.mock_can_packet_record)

    # addressing_type

    @pytest.mark.parametrize("value", [None, "something", 1])
    def test_addressing_type(self, value):
        self.mock_can_packet_record._CanPacketRecord__addressing_type = value
        assert CanPacketRecord.addressing_type.fget(self=self.mock_can_packet_record) == value
        
    # addressing_format

    @pytest.mark.parametrize("value", [None, "something", 1])
    def test_addressing_format(self, value):
        self.mock_can_packet_record._CanPacketRecord__addressing_format = value
        assert CanPacketRecord.addressing_format.fget(self=self.mock_can_packet_record) == value

    # packet_type

    @pytest.mark.parametrize("value", [None, "something", 1])
    def test_packet_type(self, value):
        self.mock_can_packet_record._CanPacketRecord__packet_type = value
        assert CanPacketRecord.packet_type.fget(self=self.mock_can_packet_record) == value

    # payload

    def test_payload(self):
        assert CanPacketRecord.payload.fget(self=self.mock_can_packet_record) \
               == self.mock_can_packet_class.payload.fget.return_value
        self.mock_can_packet_class.payload.fget.assert_called_once_with(self.mock_can_packet_record)
        
    # data_length

    def test_data_length(self):
        assert CanPacketRecord.data_length.fget(self=self.mock_can_packet_record) \
               == self.mock_can_packet_class.data_length.fget.return_value
        self.mock_can_packet_class.data_length.fget.assert_called_once_with(self.mock_can_packet_record)

    # can_id

    def test_can_id__python_can(self):
        self.mock_can_packet_record.frame = Mock(spec=PythonCanMessage)
        assert CanPacketRecord.can_id.fget(self=self.mock_can_packet_record) \
               == self.mock_can_packet_record.frame.arbitration_id

    def test_can_id__not_implemented(self):
        self.mock_can_packet_record.frame = None
        with pytest.raises(NotImplementedError):
            CanPacketRecord.can_id.fget(self=self.mock_can_packet_record)

    # dlc

    @pytest.mark.parametrize("raw_frame_data", [range(10), [0xFF, 0xEE, 0xDD]])
    def test_dlc(self, raw_frame_data):
        self.mock_can_packet_record.raw_frame_data = raw_frame_data
        assert CanPacketRecord.dlc.fget(self=self.mock_can_packet_record) \
               == self.mock_can_dlc_handler_class.encode_dlc.return_value
        self.mock_can_dlc_handler_class.encode_dlc.assert_called_once_with(len(self.mock_can_packet_record.raw_frame_data))
        
    # target_address

    @pytest.mark.parametrize("value", [None, "something", 1])
    def test_target_address(self, value):
        self.mock_can_packet_record._CanPacketRecord__target_address = value
        assert CanPacketRecord.target_address.fget(self=self.mock_can_packet_record) == value
        
    # source_address

    @pytest.mark.parametrize("value", [None, "something", 1])
    def test_source_address(self, value):
        self.mock_can_packet_record._CanPacketRecord__source_address = value
        assert CanPacketRecord.source_address.fget(self=self.mock_can_packet_record) == value
        
    # address_extension

    @pytest.mark.parametrize("value", [None, "something", 1])
    def test_address_extension(self, value):
        self.mock_can_packet_record._CanPacketRecord__address_extension = value
        assert CanPacketRecord.address_extension.fget(self=self.mock_can_packet_record) == value

    # sequence_number

    def test_sequence_number(self):
        assert CanPacketRecord.sequence_number.fget(self=self.mock_can_packet_record) \
               == self.mock_can_packet_class.sequence_number.fget.return_value
        self.mock_can_packet_class.sequence_number.fget.assert_called_once_with(self.mock_can_packet_record)

    # flow_status
    
    def test_flow_status(self):
        assert CanPacketRecord.flow_status.fget(self=self.mock_can_packet_record) \
               == self.mock_can_packet_class.flow_status.fget.return_value
        self.mock_can_packet_class.flow_status.fget.assert_called_once_with(self.mock_can_packet_record)

    # block_size

    def test_block_size(self):
        assert CanPacketRecord.block_size.fget(self=self.mock_can_packet_record) \
               == self.mock_can_packet_class.block_size.fget.return_value
        self.mock_can_packet_class.block_size.fget.assert_called_once_with(self.mock_can_packet_record)

    # st_min

    def test_st_min(self):
        assert CanPacketRecord.st_min.fget(self=self.mock_can_packet_record) \
               == self.mock_can_packet_class.st_min.fget.return_value
        self.mock_can_packet_class.st_min.fget.assert_called_once_with(self.mock_can_packet_record)

    # _validate_frame

    @pytest.mark.parametrize("frame", [None, "not a frame"])
    def test_validate_frame__invalid_type(self, frame):
        with pytest.raises(TypeError):
            CanPacketRecord._validate_frame(frame)

    def test_validate_frame__valid_python_can(self, example_python_can_message):
        assert CanPacketRecord._validate_frame(example_python_can_message) is None
        self.mock_can_id_handler_class.validate_can_id.assert_called_once_with(
            example_python_can_message.arbitration_id, extended_can_id=example_python_can_message.is_extended_id)
        self.mock_can_dlc_handler_class.validate_data_bytes_number.assert_called_once_with(
            len(example_python_can_message.data))

    # __assess_packet_type

    @pytest.mark.parametrize("raw_frame_data", [range(10), [0xFE, 0xDC, 0xBA, 0x98]])
    @pytest.mark.parametrize("ai_data_bytes_number", [0, 1])
    def test_assess_packet_type(self, raw_frame_data, ai_data_bytes_number):
        self.mock_can_packet_record.raw_frame_data = raw_frame_data
        self.mock_can_ai_handler_class.get_ai_data_bytes_number.return_value = ai_data_bytes_number
        assert CanPacketRecord._CanPacketRecord__assess_packet_type(self=self.mock_can_packet_record) is None
        assert self.mock_can_packet_record._CanPacketRecord__packet_type == self.mock_can_packet_type_class.return_value
        n_pci_value = raw_frame_data[ai_data_bytes_number] >> 4
        self.mock_can_ai_handler_class.get_ai_data_bytes_number.assert_called_once_with(
            self.mock_can_packet_record.addressing_format)
        self.mock_can_packet_type_class.validate_member.assert_called_once_with(n_pci_value)
        self.mock_can_packet_type_class.assert_called_once_with(n_pci_value)

    # __assess_ai_attributes

    @pytest.mark.parametrize("addressing_format, can_id, raw_frame_data", [
        ("some fortmat", "some id", range(10)),
        ("some other fortmat", 0x98765, [0xFE, 0xDC, 0xBA, 0x98, 0x76]),
    ])
    @pytest.mark.parametrize("decoded_ai", [
        {CanAddressingInformationHandler.TARGET_ADDRESS_NAME: "TA",
         CanAddressingInformationHandler.SOURCE_ADDRESS_NAME: "SA",
         CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME: "AE",
         CanAddressingInformationHandler.ADDRESSING_TYPE_NAME: "Some Addressing"},
        {CanAddressingInformationHandler.TARGET_ADDRESS_NAME: 0x12,
         CanAddressingInformationHandler.SOURCE_ADDRESS_NAME: 0x34,
         CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME: 0x56,
         CanAddressingInformationHandler.ADDRESSING_TYPE_NAME: None},
    ])
    @pytest.mark.parametrize("ai_data_bytes_number", [0, 1])
    def test_assess_ai_attributes(self, addressing_format, can_id, raw_frame_data,
                                  ai_data_bytes_number, decoded_ai):
        self.mock_can_packet_record.addressing_format = addressing_format
        self.mock_can_packet_record.can_id = can_id
        self.mock_can_packet_record.raw_frame_data = raw_frame_data
        self.mock_can_packet_record.addressing_type = "Some Addressing"
        self.mock_can_ai_handler_class.get_ai_data_bytes_number.return_value = ai_data_bytes_number
        self.mock_can_ai_handler_class.decode_ai.return_value = decoded_ai
        assert CanPacketRecord._CanPacketRecord__assess_ai_attributes(self=self.mock_can_packet_record) is None
        self.mock_can_ai_handler_class.get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        self.mock_can_ai_handler_class.decode_ai.assert_called_once_with(addressing_format=addressing_format,
                                                                         can_id=can_id,
                                                                         ai_data_bytes=raw_frame_data[:ai_data_bytes_number])
        assert self.mock_can_packet_record._CanPacketRecord__target_address == decoded_ai["target_address"]
        assert self.mock_can_packet_record._CanPacketRecord__source_address == decoded_ai["source_address"]
        assert self.mock_can_packet_record._CanPacketRecord__address_extension == decoded_ai["address_extension"]

    @pytest.mark.parametrize("addressing_format, can_id, raw_frame_data", [
        ("some fortmat", "some id", range(10)),
        ("some other fortmat", 0x98765, [0xFE, 0xDC, 0xBA, 0x98, 0x76]),
    ])
    @pytest.mark.parametrize("decoded_ai", [
        {CanAddressingInformationHandler.TARGET_ADDRESS_NAME: "TA",
         CanAddressingInformationHandler.SOURCE_ADDRESS_NAME: "SA",
         CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME: "AE",
         CanAddressingInformationHandler.ADDRESSING_TYPE_NAME: "Some Addressing"},
        {CanAddressingInformationHandler.TARGET_ADDRESS_NAME: 0x12,
         CanAddressingInformationHandler.SOURCE_ADDRESS_NAME: 0x34,
         CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME: 0x56,
         CanAddressingInformationHandler.ADDRESSING_TYPE_NAME: "Some Other Addressing"},
    ])
    @pytest.mark.parametrize("ai_data_bytes_number", [0, 1])
    def test_assess_ai_attributes__inconsistent_addressing(self, addressing_format, can_id, raw_frame_data,
                                                           ai_data_bytes_number, decoded_ai):
        self.mock_can_packet_record.addressing_format = addressing_format
        self.mock_can_packet_record.can_id = can_id
        self.mock_can_packet_record.raw_frame_data = raw_frame_data
        self.mock_can_ai_handler_class.get_ai_data_bytes_number.return_value = ai_data_bytes_number
        self.mock_can_ai_handler_class.decode_ai.return_value = decoded_ai
        with pytest.raises(InconsistentArgumentsError):
            CanPacketRecord._CanPacketRecord__assess_ai_attributes(self=self.mock_can_packet_record)
        self.mock_can_ai_handler_class.get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        self.mock_can_ai_handler_class.decode_ai.assert_called_once_with(addressing_format=addressing_format,
                                                                         can_id=can_id,
                                                                         ai_data_bytes=raw_frame_data[:ai_data_bytes_number])

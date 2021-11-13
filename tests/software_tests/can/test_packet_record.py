import pytest
from mock import Mock, patch

from uds.can.packet_record import CanPacketRecord, \
    PythonCanMessage


class TestCanPacketRecord:
    """Unit tests for `CanPacketRecord` class."""

    SCRIPT_LOCATION = "uds.can.packet_record"

    def setup(self):
        self.mock_can_packet_record = Mock(spec=CanPacketRecord)
        # patching
        self._patcher_can_packet_class = patch(f"{self.SCRIPT_LOCATION}.CanPacket")
        self.mock_can_packet_class = self._patcher_can_packet_class.start()
        self._patcher_can_id_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanIdHandler")
        self.mock_can_id_handler_class = self._patcher_can_id_handler_class.start()
        self._patcher_can_dlc_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler")
        self.mock_can_dlc_handler_class = self._patcher_can_dlc_handler_class.start()

    def teardown(self):
        self._patcher_can_packet_class.stop()
        self._patcher_can_id_handler_class.stop()
        self._patcher_can_dlc_handler_class.stop()

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

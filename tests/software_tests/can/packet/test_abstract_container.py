import pytest
from mock import MagicMock, Mock, patch

from uds.can.packet.abstract_container import AbstractCanPacketContainer, AddressingType, CanPacketType

SCRIPT_LOCATION = "uds.can.packet.abstract_container"


class TestAbstractCanPacketContainer:
    """Unit tests for 'AbstractCanPacketContainer' class."""

    def setup_method(self):
        self.mock_can_packet_container = Mock(spec=AbstractCanPacketContainer)
        mock_can_packet_type_class = Mock(SINGLE_FRAME=CanPacketType.SINGLE_FRAME,
                                          FIRST_FRAME=CanPacketType.FIRST_FRAME,
                                          CONSECUTIVE_FRAME=CanPacketType.CONSECUTIVE_FRAME,
                                          FLOW_CONTROL=CanPacketType.FLOW_CONTROL)
        # patching
        self._patcher_can_dlc_handler_class = patch(f"{SCRIPT_LOCATION}.CanDlcHandler")
        self.mock_can_dlc_handler_class = self._patcher_can_dlc_handler_class.start()
        self._patcher_can_ai_class = patch(f"{SCRIPT_LOCATION}.CanAddressingInformation")
        self.mock_can_ai_class = self._patcher_can_ai_class.start()
        self._patcher_can_packet_type_class = patch(f"{SCRIPT_LOCATION}.CanPacketType", mock_can_packet_type_class)
        self.mock_can_packet_type_class = self._patcher_can_packet_type_class.start()
        self._patcher_extract_single_frame_payload = patch(f"{SCRIPT_LOCATION}.extract_single_frame_payload")
        self.mock_extract_single_frame_payload = self._patcher_extract_single_frame_payload.start()
        self._patcher_extract_sf_dl = patch(f"{SCRIPT_LOCATION}.extract_sf_dl")
        self.mock_extract_sf_dl = self._patcher_extract_sf_dl.start()
        self._patcher_extract_first_frame_payload = patch(f"{SCRIPT_LOCATION}.extract_first_frame_payload")
        self.mock_extract_first_frame_payload = self._patcher_extract_first_frame_payload.start()
        self._patcher_extract_ff_dl = patch(f"{SCRIPT_LOCATION}.extract_ff_dl")
        self.mock_extract_ff_dl = self._patcher_extract_ff_dl.start()
        self._patcher_extract_consecutive_frame_payload = patch(f"{SCRIPT_LOCATION}.extract_consecutive_frame_payload")
        self.mock_extract_consecutive_frame_payload = self._patcher_extract_consecutive_frame_payload.start()
        self._patcher_extract_sequence_number = patch(f"{SCRIPT_LOCATION}.extract_sequence_number")
        self.mock_extract_sequence_number = self._patcher_extract_sequence_number.start()
        self._patcher_flow_status = patch(f"{SCRIPT_LOCATION}.CanFlowStatus")
        self.mock_flow_status = self._patcher_flow_status.start()
        self._patcher_extract_block_size = patch(f"{SCRIPT_LOCATION}.extract_block_size")
        self.mock_extract_block_size = self._patcher_extract_block_size.start()
        self._patcher_extract_flow_status = patch(f"{SCRIPT_LOCATION}.extract_flow_status")
        self.mock_extract_flow_status = self._patcher_extract_flow_status.start()
        self._patcher_extract_st_min = patch(f"{SCRIPT_LOCATION}.extract_st_min")
        self.mock_extract_st_min = self._patcher_extract_st_min.start()

    def teardown_method(self):
        self._patcher_can_dlc_handler_class.stop()
        self._patcher_can_ai_class.stop()
        self._patcher_can_packet_type_class.stop()
        self._patcher_extract_single_frame_payload.stop()
        self._patcher_extract_sf_dl.stop()
        self._patcher_extract_first_frame_payload.stop()
        self._patcher_extract_ff_dl.stop()
        self._patcher_extract_consecutive_frame_payload.stop()
        self._patcher_extract_sequence_number.stop()
        self._patcher_flow_status.stop()
        self._patcher_extract_block_size.stop()
        self._patcher_extract_flow_status.stop()
        self._patcher_extract_st_min.stop()

    # dlc

    @pytest.mark.parametrize("raw_frame_data", [MagicMock(), range(64)])
    def test_dlc__get(self, raw_frame_data):
        self.mock_can_packet_container.raw_frame_data = raw_frame_data
        assert AbstractCanPacketContainer.dlc.fget(self.mock_can_packet_container) \
               == self.mock_can_dlc_handler_class.encode_dlc.return_value
        self.mock_can_dlc_handler_class.encode_dlc.assert_called_once_with(len(raw_frame_data))

    # target_address

    @pytest.mark.parametrize("ai_info", [
        {
            "target_address": Mock(),
            "source_address": Mock(),
            "address_extension": Mock(),
            "addressing_type": AddressingType.FUNCTIONAL,
        },
        {
            "target_address": 0xF9,
            "source_address": 0xE8,
            "address_extension": None,
            "addressing_type": AddressingType.FUNCTIONAL,
        }
    ])
    def test_target_address__get(self, ai_info):
        self.mock_can_ai_class.decode_frame_ai_params.return_value = ai_info
        assert AbstractCanPacketContainer.target_address.fget(self.mock_can_packet_container) \
               == ai_info["target_address"]
        self.mock_can_ai_class.decode_frame_ai_params.assert_called_once_with(
            addressing_format=self.mock_can_packet_container.addressing_format,
            can_id=self.mock_can_packet_container.can_id,
            raw_frame_data=self.mock_can_packet_container.raw_frame_data)

    # source_address

    @pytest.mark.parametrize("ai_info", [
        {
            "target_address": Mock(),
            "source_address": Mock(),
            "address_extension": Mock(),
            "addressing_type": AddressingType.FUNCTIONAL,
        },
        {
            "target_address": 0xF9,
            "source_address": 0xE8,
            "address_extension": None,
            "addressing_type": AddressingType.FUNCTIONAL,
        }
    ])
    def test_source_address__get(self, ai_info):
        self.mock_can_ai_class.decode_frame_ai_params.return_value = ai_info
        assert AbstractCanPacketContainer.source_address.fget(self.mock_can_packet_container) \
               == ai_info["source_address"]
        self.mock_can_ai_class.decode_frame_ai_params.assert_called_once_with(
            addressing_format=self.mock_can_packet_container.addressing_format,
            can_id=self.mock_can_packet_container.can_id,
            raw_frame_data=self.mock_can_packet_container.raw_frame_data)

    # address_extension

    @pytest.mark.parametrize("ai_info", [
        {
            "target_address": Mock(),
            "source_address": Mock(),
            "address_extension": Mock(),
            "addressing_type": AddressingType.FUNCTIONAL,
        },
        {
            "target_address": 0xF9,
            "source_address": 0xE8,
            "address_extension": None,
            "addressing_type": AddressingType.FUNCTIONAL,
        }
    ])
    def test_address_extension__get(self, ai_info):
        self.mock_can_ai_class.decode_frame_ai_params.return_value = ai_info
        assert AbstractCanPacketContainer.address_extension.fget(self.mock_can_packet_container) \
               == ai_info["address_extension"]
        self.mock_can_ai_class.decode_frame_ai_params.assert_called_once_with(
            addressing_format=self.mock_can_packet_container.addressing_format,
            can_id=self.mock_can_packet_container.can_id,
            raw_frame_data=self.mock_can_packet_container.raw_frame_data)

    # packet_type

    @pytest.mark.parametrize("ai_data_bytes_number, raw_frame_data", [
        (0, [0x2F]),
        (1, [0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10]),
    ])
    def test_packet_type__get(self, ai_data_bytes_number, raw_frame_data):
        self.mock_can_ai_class.get_ai_data_bytes_number.return_value = ai_data_bytes_number
        self.mock_can_packet_container.raw_frame_data = raw_frame_data
        assert (AbstractCanPacketContainer.packet_type.fget(self.mock_can_packet_container)
                == self.mock_can_packet_type_class.return_value)
        self.mock_can_ai_class.get_ai_data_bytes_number.assert_called_once_with(
            self.mock_can_packet_container.addressing_format)
        self.mock_can_packet_type_class.assert_called_once_with(raw_frame_data[ai_data_bytes_number] >> 4)

    # data_length

    def test_data_length__single_frame(self):
        self.mock_can_packet_container.packet_type = CanPacketType.SINGLE_FRAME
        assert (AbstractCanPacketContainer.data_length.fget(self.mock_can_packet_container)
                == self.mock_extract_sf_dl.return_value)
        self.mock_extract_sf_dl.assert_called_once_with(
            addressing_format=self.mock_can_packet_container.addressing_format,
            raw_frame_data=self.mock_can_packet_container.raw_frame_data)

    def test_data_length__first_frame(self):
        self.mock_can_packet_container.packet_type = CanPacketType.FIRST_FRAME
        assert (AbstractCanPacketContainer.data_length.fget(self.mock_can_packet_container)
                == self.mock_extract_ff_dl.return_value)
        self.mock_extract_ff_dl.assert_called_once_with(
            addressing_format=self.mock_can_packet_container.addressing_format,
            raw_frame_data=self.mock_can_packet_container.raw_frame_data)

    @pytest.mark.parametrize("packet_type", [CanPacketType.CONSECUTIVE_FRAME, CanPacketType.FLOW_CONTROL])
    def test_data_length__none(self, packet_type):
        self.mock_can_packet_container.packet_type = packet_type
        assert AbstractCanPacketContainer.data_length.fget(self.mock_can_packet_container) is None

    def test_data_length__not_implemented(self):
        self.mock_can_packet_container.packet_type = Mock()
        with pytest.raises(NotImplementedError):
            AbstractCanPacketContainer.data_length.fget(self.mock_can_packet_container)

    # sequence_number

    def test_sequence_number__consecutive_frame(self):
        self.mock_can_packet_container.packet_type = CanPacketType.CONSECUTIVE_FRAME
        assert (AbstractCanPacketContainer.sequence_number.fget(self.mock_can_packet_container)
                == self.mock_extract_sequence_number.return_value)
        self.mock_extract_sequence_number.assert_called_once_with(
            addressing_format=self.mock_can_packet_container.addressing_format,
            raw_frame_data=self.mock_can_packet_container.raw_frame_data)

    @pytest.mark.parametrize("packet_type", [CanPacketType.SINGLE_FRAME,
                                             CanPacketType.FIRST_FRAME,
                                             CanPacketType.FLOW_CONTROL])
    def test_sequence_number__none(self, packet_type):
        self.mock_can_packet_container.packet_type = packet_type
        assert AbstractCanPacketContainer.sequence_number.fget(self.mock_can_packet_container) is None

    def test_sequence_number__not_implemented(self):
        self.mock_can_packet_container.packet_type = Mock()
        with pytest.raises(NotImplementedError):
            AbstractCanPacketContainer.sequence_number.fget(self.mock_can_packet_container)

    # flow_status

    def test_flow_status__flow_control(self):
        self.mock_can_packet_container.packet_type = CanPacketType.FLOW_CONTROL
        assert (AbstractCanPacketContainer.flow_status.fget(self.mock_can_packet_container)
                == self.mock_extract_flow_status.return_value)
        self.mock_extract_flow_status.assert_called_once_with(
            addressing_format=self.mock_can_packet_container.addressing_format,
            raw_frame_data=self.mock_can_packet_container.raw_frame_data)

    @pytest.mark.parametrize("packet_type", [CanPacketType.SINGLE_FRAME,
                                             CanPacketType.FIRST_FRAME,
                                             CanPacketType.CONSECUTIVE_FRAME])
    def test_flow_status__none(self, packet_type):
        self.mock_can_packet_container.packet_type = packet_type
        assert AbstractCanPacketContainer.flow_status.fget(self.mock_can_packet_container) is None

    def test_flow_status__not_implemented(self):
        self.mock_can_packet_container.packet_type = Mock()
        with pytest.raises(NotImplementedError):
            AbstractCanPacketContainer.flow_status.fget(self.mock_can_packet_container)

    # block_size

    def test_block_size__flow_control(self):
        self.mock_can_packet_container.packet_type = CanPacketType.FLOW_CONTROL
        assert (AbstractCanPacketContainer.block_size.fget(self.mock_can_packet_container)
                == self.mock_extract_block_size.return_value)
        self.mock_extract_block_size.assert_called_once_with(
            addressing_format=self.mock_can_packet_container.addressing_format,
            raw_frame_data=self.mock_can_packet_container.raw_frame_data)

    @pytest.mark.parametrize("packet_type", [CanPacketType.SINGLE_FRAME,
                                             CanPacketType.FIRST_FRAME,
                                             CanPacketType.CONSECUTIVE_FRAME])
    def test_block_size__none(self, packet_type):
        self.mock_can_packet_container.packet_type = packet_type
        assert AbstractCanPacketContainer.block_size.fget(self.mock_can_packet_container) is None

    def test_block_size__not_implemented(self):
        self.mock_can_packet_container.packet_type = Mock()
        with pytest.raises(NotImplementedError):
            AbstractCanPacketContainer.block_size.fget(self.mock_can_packet_container)

    # st_min

    def test_st_min__flow_control(self):
        self.mock_can_packet_container.packet_type = CanPacketType.FLOW_CONTROL
        assert (AbstractCanPacketContainer.st_min.fget(self.mock_can_packet_container)
                == self.mock_extract_st_min.return_value)
        self.mock_extract_st_min.assert_called_once_with(
            addressing_format=self.mock_can_packet_container.addressing_format,
            raw_frame_data=self.mock_can_packet_container.raw_frame_data)

    @pytest.mark.parametrize("packet_type", [CanPacketType.SINGLE_FRAME,
                                             CanPacketType.FIRST_FRAME,
                                             CanPacketType.CONSECUTIVE_FRAME])
    def test_st_min__none(self, packet_type):
        self.mock_can_packet_container.packet_type = packet_type
        assert AbstractCanPacketContainer.st_min.fget(self.mock_can_packet_container) is None

    def test_st_min__not_implemented(self):
        self.mock_can_packet_container.packet_type = Mock()
        with pytest.raises(NotImplementedError):
            AbstractCanPacketContainer.st_min.fget(self.mock_can_packet_container)

    # payload

    @pytest.mark.parametrize("payload", [range(10), [0xFE, 0xDC]])
    def test_payload__single_frame(self, payload):
        self.mock_can_packet_container.packet_type = CanPacketType.SINGLE_FRAME
        self.mock_extract_single_frame_payload.return_value = payload
        assert AbstractCanPacketContainer.payload.fget(self.mock_can_packet_container) == bytes(payload)
        self.mock_extract_single_frame_payload.assert_called_once_with(
            addressing_format=self.mock_can_packet_container.addressing_format,
            raw_frame_data=self.mock_can_packet_container.raw_frame_data)

    @pytest.mark.parametrize("payload", [range(10), [0xFE, 0xDC]])
    def test_payload__first_frame(self, payload):
        self.mock_can_packet_container.packet_type = CanPacketType.FIRST_FRAME
        self.mock_extract_first_frame_payload.return_value = payload
        assert AbstractCanPacketContainer.payload.fget(self.mock_can_packet_container) == bytes(payload)
        self.mock_extract_first_frame_payload.assert_called_once_with(
            addressing_format=self.mock_can_packet_container.addressing_format,
            raw_frame_data=self.mock_can_packet_container.raw_frame_data)

    @pytest.mark.parametrize("payload", [range(10), [0xFE, 0xDC]])
    def test_payload__consecutive_frame(self, payload):
        self.mock_can_packet_container.packet_type = CanPacketType.CONSECUTIVE_FRAME
        self.mock_extract_consecutive_frame_payload.return_value = payload
        assert AbstractCanPacketContainer.payload.fget(self.mock_can_packet_container) == bytes(payload)
        self.mock_extract_consecutive_frame_payload.assert_called_once_with(
            addressing_format=self.mock_can_packet_container.addressing_format,
            raw_frame_data=self.mock_can_packet_container.raw_frame_data)

    def test_payload__flow_control(self):
        self.mock_can_packet_container.packet_type = CanPacketType.FLOW_CONTROL
        assert AbstractCanPacketContainer.payload.fget(self.mock_can_packet_container) is None

    def test_payload__not_implemented(self):
        self.mock_can_packet_container.packet_type = Mock()
        with pytest.raises(NotImplementedError):
            AbstractCanPacketContainer.payload.fget(self.mock_can_packet_container)

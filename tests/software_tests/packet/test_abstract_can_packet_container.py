import pytest
from mock import Mock, patch

from uds.packet.abstract_can_packet_container import AbstractCanPacketContainer, \
    CanAddressingInformationHandler, CanPacketType
from uds.transmission_attributes import AddressingType


class TestAbstractCanPacketContainer:
    """Unit tests for 'AbstractCanPacketContainer' class."""

    SCRIPT_LOCATION = "uds.packet.abstract_can_packet_container"

    def setup(self):
        self.mock_can_packet_container = Mock(spec=AbstractCanPacketContainer)
        mock_ai_handler_class = Mock(ADDRESSING_TYPE_NAME=CanAddressingInformationHandler.ADDRESSING_TYPE_NAME,
                                     TARGET_ADDRESS_NAME=CanAddressingInformationHandler.TARGET_ADDRESS_NAME,
                                     SOURCE_ADDRESS_NAME=CanAddressingInformationHandler.SOURCE_ADDRESS_NAME,
                                     ADDRESS_EXTENSION_NAME=CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME)
        mock_can_packet_type_class = Mock(SINGLE_FRAME=CanPacketType.SINGLE_FRAME,
                                          FIRST_FRAME=CanPacketType.FIRST_FRAME,
                                          CONSECUTIVE_FRAME=CanPacketType.CONSECUTIVE_FRAME,
                                          FLOW_CONTROL=CanPacketType.FLOW_CONTROL)
        # patching
        self._patcher_ai_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanAddressingInformationHandler",
                                               mock_ai_handler_class)
        self.mock_ai_handler_class = self._patcher_ai_handler_class.start()
        self._patcher_can_dlc_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler")
        self.mock_can_dlc_handler_class = self._patcher_can_dlc_handler_class.start()
        self._patcher_single_frame_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanSingleFrameHandler")
        self.mock_single_frame_handler_class = self._patcher_single_frame_handler_class.start()
        self._patcher_first_frame_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanFirstFrameHandler")
        self.mock_first_frame_handler_class = self._patcher_first_frame_handler_class.start()
        self._patcher_consecutive_frame_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanConsecutiveFrameHandler")
        self.mock_consecutive_frame_handler_class = self._patcher_consecutive_frame_handler_class.start()
        self._patcher_flow_control_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanFlowControlHandler")
        self.mock_flow_control_handler_class = self._patcher_flow_control_handler_class.start()
        self._patcher_can_packet_type_class = patch(f"{self.SCRIPT_LOCATION}.CanPacketType", mock_can_packet_type_class)
        self.mock_can_packet_type_class = self._patcher_can_packet_type_class.start()

    def teardown(self):
        self._patcher_ai_handler_class.stop()
        self._patcher_can_dlc_handler_class.stop()
        self._patcher_single_frame_handler_class.stop()
        self._patcher_first_frame_handler_class.stop()
        self._patcher_consecutive_frame_handler_class.stop()
        self._patcher_flow_control_handler_class.stop()
        self._patcher_can_packet_type_class.stop()

    # dlc

    @pytest.mark.parametrize("raw_frame_data", ["some raw data", list(range(2))])
    def test_dlc__get(self, raw_frame_data):
        self.mock_can_packet_container.raw_frame_data = raw_frame_data
        assert AbstractCanPacketContainer.dlc.fget(self.mock_can_packet_container) \
               == self.mock_can_dlc_handler_class.encode_dlc.return_value
        self.mock_can_dlc_handler_class.encode_dlc.assert_called_once_with(len(raw_frame_data))

    # packet_type

    @pytest.mark.parametrize("ai_data_bytes_number, raw_frame_data", [
        (0, [0x2F]),
        (1, [0x12, 0x34, 0x45]),
    ])
    def test_packet_type__get(self, ai_data_bytes_number, raw_frame_data):
        self.mock_ai_handler_class.get_ai_data_bytes_number.return_value = ai_data_bytes_number
        self.mock_can_packet_container.raw_frame_data = raw_frame_data
        assert AbstractCanPacketContainer.packet_type.fget(self.mock_can_packet_container) \
               == self.mock_can_packet_type_class.return_value
        self.mock_ai_handler_class.get_ai_data_bytes_number.assert_called_once_with(
            self.mock_can_packet_container.addressing_format)
        self.mock_can_packet_type_class.assert_called_once_with(raw_frame_data[ai_data_bytes_number] >> 4)

    # target_address

    @pytest.mark.parametrize("ai_info", [
        {
            CanAddressingInformationHandler.TARGET_ADDRESS_NAME: "TA",
            CanAddressingInformationHandler.SOURCE_ADDRESS_NAME: "SA",
            CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME: "AE",
            CanAddressingInformationHandler.ADDRESSING_TYPE_NAME: "Addressing",
        },
        {
            CanAddressingInformationHandler.TARGET_ADDRESS_NAME: 0xF9,
            CanAddressingInformationHandler.SOURCE_ADDRESS_NAME: 0xE8,
            CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME: None,
            CanAddressingInformationHandler.ADDRESSING_TYPE_NAME: AddressingType.FUNCTIONAL,
        }
    ])
    def test_target_address__get(self, ai_info):
        self.mock_can_packet_container.get_addressing_information.return_value = ai_info
        assert AbstractCanPacketContainer.target_address.fget(self.mock_can_packet_container) \
               == ai_info[CanAddressingInformationHandler.TARGET_ADDRESS_NAME]
        self.mock_can_packet_container.get_addressing_information.assert_called_once_with()

    # source_address

    @pytest.mark.parametrize("ai_info", [
        {
            CanAddressingInformationHandler.TARGET_ADDRESS_NAME: "TA",
            CanAddressingInformationHandler.SOURCE_ADDRESS_NAME: "SA",
            CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME: "AE",
            CanAddressingInformationHandler.ADDRESSING_TYPE_NAME: "Addressing",
        },
        {
            CanAddressingInformationHandler.TARGET_ADDRESS_NAME: 0xF9,
            CanAddressingInformationHandler.SOURCE_ADDRESS_NAME: 0xE8,
            CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME: None,
            CanAddressingInformationHandler.ADDRESSING_TYPE_NAME: AddressingType.FUNCTIONAL,
        }
    ])
    def test_source_address__get(self, ai_info):
        self.mock_can_packet_container.get_addressing_information.return_value = ai_info
        assert AbstractCanPacketContainer.source_address.fget(self.mock_can_packet_container) \
               == ai_info[CanAddressingInformationHandler.SOURCE_ADDRESS_NAME]
        self.mock_can_packet_container.get_addressing_information.assert_called_once_with()

    # address_extension

    @pytest.mark.parametrize("ai_info", [
        {
            CanAddressingInformationHandler.TARGET_ADDRESS_NAME: "TA",
            CanAddressingInformationHandler.SOURCE_ADDRESS_NAME: "SA",
            CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME: "AE",
            CanAddressingInformationHandler.ADDRESSING_TYPE_NAME: "Addressing",
        },
        {
            CanAddressingInformationHandler.TARGET_ADDRESS_NAME: 0xF9,
            CanAddressingInformationHandler.SOURCE_ADDRESS_NAME: 0xE8,
            CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME: None,
            CanAddressingInformationHandler.ADDRESSING_TYPE_NAME: AddressingType.FUNCTIONAL,
        }
    ])
    def test_address_extension__get(self, ai_info):
        self.mock_can_packet_container.get_addressing_information.return_value = ai_info
        assert AbstractCanPacketContainer.address_extension.fget(self.mock_can_packet_container) \
               == ai_info[CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME]
        self.mock_can_packet_container.get_addressing_information.assert_called_once_with()

    # data_length

    @pytest.mark.parametrize("packet_type", [None, CanPacketType.CONSECUTIVE_FRAME, CanPacketType.FLOW_CONTROL, "x"])
    def test_data_length__none(self, packet_type):
        self.mock_can_packet_container.packet_type = packet_type
        assert AbstractCanPacketContainer.data_length.fget(self.mock_can_packet_container) is None

    def test_data_length__single_frame(self):
        self.mock_can_packet_container.packet_type = CanPacketType.SINGLE_FRAME
        assert AbstractCanPacketContainer.data_length.fget(self.mock_can_packet_container) \
               == self.mock_single_frame_handler_class.decode_sf_dl.return_value
        self.mock_single_frame_handler_class.decode_sf_dl.assert_called_once_with(
            addressing_format=self.mock_can_packet_container.addressing_format,
            raw_frame_data=self.mock_can_packet_container.raw_frame_data)

    def test_data_length__first_frame(self):
        self.mock_can_packet_container.packet_type = CanPacketType.FIRST_FRAME
        assert AbstractCanPacketContainer.data_length.fget(self.mock_can_packet_container) \
               == self.mock_first_frame_handler_class.decode_ff_dl.return_value
        self.mock_first_frame_handler_class.decode_ff_dl.assert_called_once_with(
            addressing_format=self.mock_can_packet_container.addressing_format,
            raw_frame_data=self.mock_can_packet_container.raw_frame_data)

    # sequence_number

    @pytest.mark.parametrize("packet_type", [None,
                                             CanPacketType.SINGLE_FRAME,
                                             CanPacketType.FIRST_FRAME,
                                             CanPacketType.FLOW_CONTROL,
                                             "something new"])
    def test_sequence_number__none(self, packet_type):
        self.mock_can_packet_container.packet_type = packet_type
        assert AbstractCanPacketContainer.sequence_number.fget(self.mock_can_packet_container) is None

    def test_sequence_number__consecutive_frame(self):
        self.mock_can_packet_container.packet_type = CanPacketType.CONSECUTIVE_FRAME
        assert AbstractCanPacketContainer.sequence_number.fget(self.mock_can_packet_container) \
               == self.mock_consecutive_frame_handler_class.decode_sequence_number.return_value
        self.mock_consecutive_frame_handler_class.decode_sequence_number.assert_called_once_with(
            addressing_format=self.mock_can_packet_container.addressing_format,
            raw_frame_data=self.mock_can_packet_container.raw_frame_data)

    # payload

    @pytest.mark.parametrize("packet_type", [None, CanPacketType.FLOW_CONTROL, "something new"])
    def test_payload__none(self, packet_type):
        self.mock_can_packet_container.packet_type = packet_type
        assert AbstractCanPacketContainer.payload.fget(self.mock_can_packet_container) is None

    @pytest.mark.parametrize("payload", [range(10), [0xFE, 0xDC]])
    def test_payload__single_frame(self, payload):
        self.mock_can_packet_container.packet_type = CanPacketType.SINGLE_FRAME
        self.mock_single_frame_handler_class.decode_payload.return_value = payload
        assert AbstractCanPacketContainer.payload.fget(self.mock_can_packet_container) == tuple(payload)
        self.mock_single_frame_handler_class.decode_payload.assert_called_once_with(
            addressing_format=self.mock_can_packet_container.addressing_format,
            raw_frame_data=self.mock_can_packet_container.raw_frame_data)

    @pytest.mark.parametrize("payload", [range(10), [0xFE, 0xDC]])
    def test_payload__first_frame(self, payload):
        self.mock_can_packet_container.packet_type = CanPacketType.FIRST_FRAME
        self.mock_first_frame_handler_class.decode_payload.return_value = payload
        assert AbstractCanPacketContainer.payload.fget(self.mock_can_packet_container) == tuple(payload)
        self.mock_first_frame_handler_class.decode_payload.assert_called_once_with(
            addressing_format=self.mock_can_packet_container.addressing_format,
            raw_frame_data=self.mock_can_packet_container.raw_frame_data)

    @pytest.mark.parametrize("payload", [range(10), [0xFE, 0xDC]])
    def test_payload__consecutive_frame(self, payload):
        self.mock_can_packet_container.packet_type = CanPacketType.CONSECUTIVE_FRAME
        self.mock_consecutive_frame_handler_class.decode_payload.return_value = payload
        assert AbstractCanPacketContainer.payload.fget(self.mock_can_packet_container) == tuple(payload)
        self.mock_consecutive_frame_handler_class.decode_payload.assert_called_once_with(
            addressing_format=self.mock_can_packet_container.addressing_format,
            raw_frame_data=self.mock_can_packet_container.raw_frame_data)

    # flow_status

    @pytest.mark.parametrize("packet_type", [None,
                                             CanPacketType.SINGLE_FRAME,
                                             CanPacketType.FIRST_FRAME,
                                             CanPacketType.CONSECUTIVE_FRAME,
                                             "something new"])
    def test_flow_status__none(self, packet_type):
        self.mock_can_packet_container.packet_type = packet_type
        assert AbstractCanPacketContainer.flow_status.fget(self.mock_can_packet_container) is None

    def test_flow_status__flow_control(self):
        self.mock_can_packet_container.packet_type = CanPacketType.FLOW_CONTROL
        assert AbstractCanPacketContainer.flow_status.fget(self.mock_can_packet_container) \
               == self.mock_flow_control_handler_class.decode_flow_status.return_value
        self.mock_flow_control_handler_class.decode_flow_status.assert_called_once_with(
            addressing_format=self.mock_can_packet_container.addressing_format,
            raw_frame_data=self.mock_can_packet_container.raw_frame_data)

    # block_size

    @pytest.mark.parametrize("packet_type", [None,
                                             CanPacketType.SINGLE_FRAME,
                                             CanPacketType.FIRST_FRAME,
                                             CanPacketType.CONSECUTIVE_FRAME,
                                             "something new"])
    def test_block_size__none(self, packet_type):
        self.mock_can_packet_container.packet_type = packet_type
        assert AbstractCanPacketContainer.block_size.fget(self.mock_can_packet_container) is None

    def test_block_size__flow_control(self):
        self.mock_can_packet_container.packet_type = CanPacketType.FLOW_CONTROL
        assert AbstractCanPacketContainer.block_size.fget(self.mock_can_packet_container) \
               == self.mock_flow_control_handler_class.decode_block_size.return_value
        self.mock_flow_control_handler_class.decode_block_size.assert_called_once_with(
            addressing_format=self.mock_can_packet_container.addressing_format,
            raw_frame_data=self.mock_can_packet_container.raw_frame_data)

    # st_min

    @pytest.mark.parametrize("packet_type", [None,
                                             CanPacketType.SINGLE_FRAME,
                                             CanPacketType.FIRST_FRAME,
                                             CanPacketType.CONSECUTIVE_FRAME,
                                             "something new"])
    def test_st_min__none(self, packet_type):
        self.mock_can_packet_container.packet_type = packet_type
        assert AbstractCanPacketContainer.st_min.fget(self.mock_can_packet_container) is None

    def test_st_min__flow_control(self):
        self.mock_can_packet_container.packet_type = CanPacketType.FLOW_CONTROL
        assert AbstractCanPacketContainer.st_min.fget(self.mock_can_packet_container) \
               == self.mock_flow_control_handler_class.decode_st_min.return_value
        self.mock_flow_control_handler_class.decode_st_min.assert_called_once_with(
            addressing_format=self.mock_can_packet_container.addressing_format,
            raw_frame_data=self.mock_can_packet_container.raw_frame_data)

    # get_addressing_information

    @pytest.mark.parametrize("raw_frame_data, ai_data_bytes_number", [
        ([0x12, 0xFE], 0),
        ((0xF9, 0xE8, 0xD7, 0xC6, 0xB5), 1),
    ])
    def test_get_addressing_information(self, raw_frame_data, ai_data_bytes_number):
        self.mock_can_packet_container.raw_frame_data = raw_frame_data
        self.mock_ai_handler_class.get_ai_data_bytes_number.return_value = ai_data_bytes_number
        assert AbstractCanPacketContainer.get_addressing_information(self=self.mock_can_packet_container) \
               == self.mock_ai_handler_class.decode_ai.return_value
        self.mock_ai_handler_class.get_ai_data_bytes_number.assert_called_once_with(
            self.mock_can_packet_container.addressing_format)
        self.mock_ai_handler_class.decode_ai.assert_called_once_with(
            addressing_format=self.mock_can_packet_container.addressing_format,
            can_id=self.mock_can_packet_container.can_id,
            ai_data_bytes=self.mock_can_packet_container.raw_frame_data[:ai_data_bytes_number])

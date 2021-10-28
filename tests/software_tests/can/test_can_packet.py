# import pytest
# from mock import patch, Mock, call
#
# from uds.can.packet import CanPacket, \
#     AddressingType, CanAddressingFormat, CanPacketType, CanFlowStatus, \
#     InconsistentArgumentsError, UnusedArgumentError, DEFAULT_FILLER_BYTE
#
#
# class TestCanPacketClassMethods:
#     """Tests for classmethods in 'CanPacket' class."""
#
#     SCRIPT_LOCATION = "uds.packet.can_packet"
#
#     def setup(self):
#         # patching
#         self._patcher_validate_raw_byte = patch(f"{self.SCRIPT_LOCATION}.validate_raw_byte")
#         self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
#         self._patcher_validate_raw_bytes = patch(f"{self.SCRIPT_LOCATION}.validate_raw_bytes")
#         self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
#         self._patcher_validate_addressing_type = patch(f"{self.SCRIPT_LOCATION}.AddressingType.validate_member")
#         self.mock_validate_addressing_type = self._patcher_validate_addressing_type.start()
#         self._patcher_validate_can_addressing_format = \
#             patch(f"{self.SCRIPT_LOCATION}.CanAddressingFormat.validate_member")
#         self.mock_validate_can_addressing_format = self._patcher_validate_can_addressing_format.start()
#         self._patcher_get_data_bytes_used_by_can_addressing_format = \
#             patch(f"{self.SCRIPT_LOCATION}.CanAddressingFormat.get_number_of_data_bytes_used")
#         self.mock_get_data_bytes_used_by_can_addressing_format = \
#             self._patcher_get_data_bytes_used_by_can_addressing_format.start()
#
#     def teardown(self):
#         self._patcher_validate_raw_bytes.stop()
#         self._patcher_validate_addressing_type.stop()
#         self._patcher_validate_can_addressing_format.stop()
#         self._patcher_get_data_bytes_used_by_can_addressing_format.stop()
#
#     # get_can_frame_dlc
#
#     @pytest.mark.parametrize("packet_type", [None, "unknown"])
#     @pytest.mark.parametrize("payload_length", [1, 5])
#     @patch(f"{SCRIPT_LOCATION}.CanPacketType")
#     def test_get_can_frame_dlc__unknown_packet_type(self, mock_packet_type_class,
#                                                     example_can_addressing_format, packet_type, payload_length):
#         with pytest.raises(NotImplementedError):
#             CanPacket.get_can_frame_dlc(packet_type=packet_type,
#                                         addressing_format=example_can_addressing_format,
#                                         payload_length=payload_length)
#         mock_packet_type_class.validate_member.assert_called_once_with(packet_type)
#         mock_packet_type_class.assert_called_once_with(packet_type)
#
#     @pytest.mark.parametrize("packet_type", [CanPacketType.SINGLE_FRAME, CanPacketType.SINGLE_FRAME.value])
#     @pytest.mark.parametrize("payload_length", [1, 5])
#     @patch(f"{SCRIPT_LOCATION}.CanPacket.get_can_frame_dlc_single_frame")
#     def test_get_can_frame_dlc__single_frame(self, mock_get_can_frame_dlc_single_frame,
#                                              example_can_addressing_format, packet_type, payload_length):
#         assert CanPacket.get_can_frame_dlc(packet_type=packet_type,
#                                            addressing_format=example_can_addressing_format,
#                                            payload_length=payload_length) == mock_get_can_frame_dlc_single_frame.return_value
#         mock_get_can_frame_dlc_single_frame.assert_called_once_with(addressing_format=example_can_addressing_format,
#                                                                     payload_length=payload_length)
#
#     @pytest.mark.parametrize("packet_type", [CanPacketType.FIRST_FRAME, CanPacketType.FIRST_FRAME.value])
#     @pytest.mark.parametrize("payload_length", [1, 5])
#     @pytest.mark.parametrize("data_length", [12345, 0xFEDCBA])
#     @patch(f"{SCRIPT_LOCATION}.CanPacket.get_can_frame_dlc_first_frame")
#     def test_get_can_frame_dlc__first_frame(self, mock_get_can_frame_dlc_first_frame,
#                                             example_can_addressing_format, packet_type, payload_length, data_length):
#         assert CanPacket.get_can_frame_dlc(packet_type=packet_type,
#                                            addressing_format=example_can_addressing_format,
#                                            payload_length=payload_length,
#                                            data_length=data_length) is mock_get_can_frame_dlc_first_frame.return_value
#         mock_get_can_frame_dlc_first_frame.assert_called_once_with(addressing_format=example_can_addressing_format,
#                                                                    payload_length=payload_length,
#                                                                    data_length=data_length)
#
#     @pytest.mark.parametrize("packet_type", [CanPacketType.CONSECUTIVE_FRAME, CanPacketType.CONSECUTIVE_FRAME.value])
#     @pytest.mark.parametrize("payload_length", [1, 5])
#     @patch(f"{SCRIPT_LOCATION}.CanPacket.get_can_frame_dlc_consecutive_frame")
#     def test_get_can_frame_dlc__consecutive_frame(self, mock_get_can_frame_dlc_consecutive_frame,
#                                                   example_can_addressing_format, packet_type, payload_length):
#         assert CanPacket.get_can_frame_dlc(packet_type=packet_type,
#                                            addressing_format=example_can_addressing_format,
#                                            payload_length=payload_length) is mock_get_can_frame_dlc_consecutive_frame.return_value
#         mock_get_can_frame_dlc_consecutive_frame.assert_called_once_with(
#             addressing_format=example_can_addressing_format,
#             payload_length=payload_length)
#
#     @pytest.mark.parametrize("packet_type", [CanPacketType.FLOW_CONTROL, CanPacketType.FLOW_CONTROL.value])
#     @patch(f"{SCRIPT_LOCATION}.CanPacket.get_can_frame_dlc_flow_control")
#     def test_get_can_frame_dlc__flow_control(self, mock_get_can_frame_dlc_flow_control,
#                                              example_can_addressing_format, packet_type):
#         assert CanPacket.get_can_frame_dlc(addressing_format=example_can_addressing_format,
#                                            packet_type=packet_type) is mock_get_can_frame_dlc_flow_control.return_value
#         mock_get_can_frame_dlc_flow_control.assert_called_once_with(addressing_format=example_can_addressing_format)
#
#     # create_can_frame_data
#
#     @pytest.mark.parametrize("packet_type", [None, "unknown"])
#     @pytest.mark.parametrize("addressing_format, target_address, address_extension, dlc, filler_byte", [
#         ("some addressing format", "TA", "AE", "DLC", "filler"),
#         (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, 0x58, 0xA4, 8, 0x9C),
#     ])
#     @pytest.mark.parametrize("kwargs", [{}, {"a1": "var 1", "b2": None}])
#     @patch(f"{SCRIPT_LOCATION}.CanPacketType")
#     def test_create_can_frame_data__unknown_packet_type(self, mock_packet_type_class,
#                                                         packet_type, dlc, filler_byte,
#                                                         addressing_format, target_address, address_extension, kwargs):
#         with pytest.raises(NotImplementedError):
#             CanPacket.create_can_frame_data(packet_type=packet_type,
#                                             addressing_format=addressing_format,
#                                             dlc=dlc,
#                                             filler_byte=filler_byte,
#                                             target_address=target_address,
#                                             address_extension=address_extension,
#                                             **kwargs)
#         mock_packet_type_class.validate_member.assert_called_once_with(packet_type)
#         mock_packet_type_class.assert_called_once_with(packet_type)
#
#     @pytest.mark.parametrize("packet_type", [CanPacketType.SINGLE_FRAME, CanPacketType.SINGLE_FRAME.value])
#     @pytest.mark.parametrize("addressing_format, target_address, address_extension, dlc, filler_byte", [
#         ("some addressing format", "TA", "AE", "DLC", "filler"),
#         (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, 0x58, 0xA4, 8, 0x9C),
#     ])
#     @pytest.mark.parametrize("kwargs", [{}, {"a1": "var 1", "b2": None}])
#     @patch(f"{SCRIPT_LOCATION}.CanPacket.create_can_frame_data_single_frame")
#     def test_create_can_frame_data__single_frame(self, mock_create_can_frame_data_single_frame,
#                                                  packet_type, dlc, filler_byte,
#                                                  addressing_format, target_address, address_extension, kwargs):
#         assert CanPacket.create_can_frame_data(packet_type=packet_type,
#                                                addressing_format=addressing_format,
#                                                dlc=dlc,
#                                                filler_byte=filler_byte,
#                                                target_address=target_address,
#                                                address_extension=address_extension,
#                                                **kwargs) == mock_create_can_frame_data_single_frame.return_value
#         mock_create_can_frame_data_single_frame.assert_called_once_with(addressing_format=addressing_format,
#                                                                         dlc=dlc,
#                                                                         filler_byte=filler_byte,
#                                                                         target_address=target_address,
#                                                                         address_extension=address_extension,
#                                                                         **kwargs)
#
#     @pytest.mark.parametrize("packet_type", [CanPacketType.FIRST_FRAME, CanPacketType.FIRST_FRAME.value])
#     @pytest.mark.parametrize("addressing_format, target_address, address_extension, dlc, filler_byte", [
#         ("some addressing format", "TA", "AE", "DLC", "filler"),
#         (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, 0x58, 0xA4, 8, 0x9C),
#     ])
#     @pytest.mark.parametrize("kwargs", [{}, {"a1": "var 1", "b2": None}])
#     @patch(f"{SCRIPT_LOCATION}.CanPacket.create_can_frame_data_first_frame")
#     def test_create_can_frame_data__first_frame(self, mock_create_can_frame_data_first_frame,
#                                                 packet_type, dlc, filler_byte,
#                                                 addressing_format, target_address, address_extension, kwargs):
#         assert CanPacket.create_can_frame_data(packet_type=packet_type,
#                                                addressing_format=addressing_format,
#                                                dlc=dlc,
#                                                filler_byte=filler_byte,
#                                                target_address=target_address,
#                                                address_extension=address_extension,
#                                                **kwargs) == mock_create_can_frame_data_first_frame.return_value
#         mock_create_can_frame_data_first_frame.assert_called_once_with(addressing_format=addressing_format,
#                                                                        dlc=dlc,
#                                                                        target_address=target_address,
#                                                                        address_extension=address_extension,
#                                                                        **kwargs)
#
#     @pytest.mark.parametrize("packet_type", [CanPacketType.CONSECUTIVE_FRAME, CanPacketType.CONSECUTIVE_FRAME.value])
#     @pytest.mark.parametrize("addressing_format, target_address, address_extension, dlc, filler_byte", [
#         ("some addressing format", "TA", "AE", "DLC", "filler"),
#         (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, 0x58, 0xA4, 8, 0x9C),
#     ])
#     @pytest.mark.parametrize("kwargs", [{}, {"a1": "var 1", "b2": None}])
#     @patch(f"{SCRIPT_LOCATION}.CanPacket.create_can_frame_data_consecutive_frame")
#     def test_create_can_frame_data__consecutive_frame(self, mock_create_can_frame_data_consecutive_frame,
#                                                       packet_type, dlc, filler_byte,
#                                                       addressing_format, target_address, address_extension, kwargs):
#         assert CanPacket.create_can_frame_data(packet_type=packet_type,
#                                                addressing_format=addressing_format,
#                                                dlc=dlc,
#                                                filler_byte=filler_byte,
#                                                target_address=target_address,
#                                                address_extension=address_extension,
#                                                **kwargs) == mock_create_can_frame_data_consecutive_frame.return_value
#         mock_create_can_frame_data_consecutive_frame.assert_called_once_with(addressing_format=addressing_format,
#                                                                              dlc=dlc,
#                                                                              filler_byte=filler_byte,
#                                                                              target_address=target_address,
#                                                                              address_extension=address_extension,
#                                                                              **kwargs)
#
#     @pytest.mark.parametrize("packet_type", [CanPacketType.FLOW_CONTROL, CanPacketType.FLOW_CONTROL.value])
#     @pytest.mark.parametrize("addressing_format, target_address, address_extension, dlc, filler_byte", [
#         ("some addressing format", "TA", "AE", "DLC", "filler"),
#         (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, 0x58, 0xA4, 8, 0x9C),
#     ])
#     @pytest.mark.parametrize("kwargs", [{}, {"a1": "var 1", "b2": None}])
#     @patch(f"{SCRIPT_LOCATION}.CanPacket.create_can_frame_data_flow_control")
#     def test_create_can_frame_data__flow_control(self, mock_create_can_frame_data_flow_control,
#                                                  packet_type, dlc, filler_byte,
#                                                  addressing_format, target_address, address_extension, kwargs):
#         assert CanPacket.create_can_frame_data(packet_type=packet_type,
#                                                addressing_format=addressing_format,
#                                                dlc=dlc,
#                                                filler_byte=filler_byte,
#                                                target_address=target_address,
#                                                address_extension=address_extension,
#                                                **kwargs) == mock_create_can_frame_data_flow_control.return_value
#         mock_create_can_frame_data_flow_control.assert_called_once_with(addressing_format=addressing_format,
#                                                                         dlc=dlc,
#                                                                         filler_byte=filler_byte,
#                                                                         target_address=target_address,
#                                                                         address_extension=address_extension,
#                                                                         **kwargs)
#
#     # validate_address_information
#
#     @pytest.mark.parametrize("addressing_format", [None, "unknown addressing format"])
#     @pytest.mark.parametrize("addressing, can_id, target_address, source_address, address_extension", [
#         ("some addressing", "some CAN ID", "TA", "SA", "AE"),
#         (0, None, None, None, None),
#         (AddressingType.PHYSICAL, 0x8213, 0x9A, 0x0B, 0xF1),
#     ])
#     @patch(f"{SCRIPT_LOCATION}.CanAddressingFormat")
#     def test_validate_address_information__unknown_addressing_format(self, mock_can_addressing_format_class,
#                                                                      addressing_format, addressing, can_id,
#                                                                      target_address, source_address, address_extension):
#         with pytest.raises(NotImplementedError):
#             CanPacket.validate_address_information(addressing_format=addressing_format,
#                                                    addressing=addressing,
#                                                    can_id=can_id,
#                                                    target_address=target_address,
#                                                    source_address=source_address,
#                                                    address_extension=address_extension)
#         mock_can_addressing_format_class.validate_member.assert_called_once_with(addressing_format)
#         mock_can_addressing_format_class.assert_called_once_with(addressing_format)
#
#     @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
#                                                    CanAddressingFormat.NORMAL_11BIT_ADDRESSING.value])
#     @pytest.mark.parametrize("addressing, can_id, target_address, source_address, address_extension", [
#         ("some addressing", "some CAN ID", "TA", "SA", "AE"),
#         (0, None, None, None, None),
#         (AddressingType.PHYSICAL, 0x8213, 0x9A, 0x0B, 0xF1),
#     ])
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_ai_normal_11bit")
#     def test_validate_address_information__normal_11bit(self, mock_validate_ai_normal_11bit,
#                                                         addressing_format, addressing, can_id,
#                                                         target_address, source_address, address_extension):
#         CanPacket.validate_address_information(addressing_format=addressing_format,
#                                                addressing=addressing,
#                                                can_id=can_id,
#                                                target_address=target_address,
#                                                source_address=source_address,
#                                                address_extension=address_extension)
#         mock_validate_ai_normal_11bit.assert_called_once_with(addressing=addressing,
#                                                               can_id=can_id,
#                                                               target_address=target_address,
#                                                               source_address=source_address,
#                                                               address_extension=address_extension)
#
#     @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
#                                                    CanAddressingFormat.NORMAL_FIXED_ADDRESSING.value])
#     @pytest.mark.parametrize("addressing, can_id, target_address, source_address, address_extension", [
#         ("some addressing", "some CAN ID", "TA", "SA", "AE"),
#         (0, None, None, None, None),
#         (AddressingType.PHYSICAL, 0x8213, 0x9A, 0x0B, 0xF1),
#     ])
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_ai_normal_fixed")
#     def test_validate_address_information__normal_fixed(self, mock_validate_ai_normal_fixed,
#                                                         addressing_format, addressing, can_id,
#                                                         target_address, source_address, address_extension):
#         CanPacket.validate_address_information(addressing_format=addressing_format,
#                                                addressing=addressing,
#                                                can_id=can_id,
#                                                target_address=target_address,
#                                                source_address=source_address,
#                                                address_extension=address_extension)
#         mock_validate_ai_normal_fixed.assert_called_once_with(addressing=addressing,
#                                                               can_id=can_id,
#                                                               target_address=target_address,
#                                                               source_address=source_address,
#                                                               address_extension=address_extension)
#
#     @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.EXTENDED_ADDRESSING,
#                                                    CanAddressingFormat.EXTENDED_ADDRESSING.value])
#     @pytest.mark.parametrize("addressing, can_id, target_address, source_address, address_extension", [
#         ("some addressing", "some CAN ID", "TA", "SA", "AE"),
#         (0, None, None, None, None),
#         (AddressingType.PHYSICAL, 0x8213, 0x9A, 0x0B, 0xF1),
#     ])
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_ai_extended")
#     def test_validate_address_information__extended(self, mock_validate_ai_extended,
#                                                     addressing_format, addressing, can_id,
#                                                     target_address, source_address, address_extension):
#         CanPacket.validate_address_information(addressing_format=addressing_format,
#                                                addressing=addressing,
#                                                can_id=can_id,
#                                                target_address=target_address,
#                                                source_address=source_address,
#                                                address_extension=address_extension)
#         mock_validate_ai_extended.assert_called_once_with(addressing=addressing,
#                                                           can_id=can_id,
#                                                           target_address=target_address,
#                                                           source_address=source_address,
#                                                           address_extension=address_extension)
#
#     @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.MIXED_11BIT_ADDRESSING,
#                                                    CanAddressingFormat.MIXED_11BIT_ADDRESSING.value])
#     @pytest.mark.parametrize("addressing, can_id, target_address, source_address, address_extension", [
#         ("some addressing", "some CAN ID", "TA", "SA", "AE"),
#         (0, None, None, None, None),
#         (AddressingType.PHYSICAL, 0x8213, 0x9A, 0x0B, 0xF1),
#     ])
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_ai_mixed_11bit")
#     def test_validate_address_information__mixed_11bit(self, mock_validate_ai_mixed_11bit,
#                                                        addressing_format, addressing, can_id,
#                                                        target_address, source_address, address_extension):
#         CanPacket.validate_address_information(addressing_format=addressing_format,
#                                                addressing=addressing,
#                                                can_id=can_id,
#                                                target_address=target_address,
#                                                source_address=source_address,
#                                                address_extension=address_extension)
#         mock_validate_ai_mixed_11bit.assert_called_once_with(addressing=addressing,
#                                                              can_id=can_id,
#                                                              target_address=target_address,
#                                                              source_address=source_address,
#                                                              address_extension=address_extension)
#
#     @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.MIXED_29BIT_ADDRESSING,
#                                                    CanAddressingFormat.MIXED_29BIT_ADDRESSING.value])
#     @pytest.mark.parametrize("addressing, can_id, target_address, source_address, address_extension", [
#         ("some addressing", "some CAN ID", "TA", "SA", "AE"),
#         (0, None, None, None, None),
#         (AddressingType.PHYSICAL, 0x8213, 0x9A, 0x0B, 0xF1),
#     ])
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_ai_mixed_29bit")
#     def test_validate_address_information__mixed_29bit(self, mock_validate_ai_mixed_29bit,
#                                                        addressing_format, addressing, can_id,
#                                                        target_address, source_address, address_extension):
#         CanPacket.validate_address_information(addressing_format=addressing_format,
#                                                addressing=addressing,
#                                                can_id=can_id,
#                                                target_address=target_address,
#                                                source_address=source_address,
#                                                address_extension=address_extension)
#         mock_validate_ai_mixed_29bit.assert_called_once_with(addressing=addressing,
#                                                              can_id=can_id,
#                                                              target_address=target_address,
#                                                              source_address=source_address,
#                                                              address_extension=address_extension)
#
#     # get_can_frame_dlc_single_frame
#
#     @pytest.mark.parametrize("payload_length, ai_bytes", [
#         (61, 2),
#         (62, 1),
#         (63, 0),
#         (100, 0),
#     ])
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_payload_length")
#     def test_get_can_frame_dlc_single_frame__inconsistency_error(self, mock_validate_payload_length,
#                                                        example_can_addressing_format, payload_length, ai_bytes):
#         self.mock_get_data_bytes_used_by_can_addressing_format.return_value = ai_bytes
#         with pytest.raises(InconsistentArgumentsError):
#             CanPacket.get_can_frame_dlc_single_frame(addressing_format=example_can_addressing_format,
#                                                      payload_length=payload_length)
#         self.mock_validate_can_addressing_format.assert_called_once_with(example_can_addressing_format)
#         mock_validate_payload_length.assert_called_once_with(payload_length)
#         self.mock_get_data_bytes_used_by_can_addressing_format.assert_called_once_with(example_can_addressing_format)
#
#     @pytest.mark.parametrize("payload_length, ai_bytes", [
#         (5, 0),
#         (6, 1),
#         (1, 0),
#         (2, 1),
#     ])
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_payload_length")
#     @patch(f"{SCRIPT_LOCATION}.CanDlcHandler.get_min_dlc")
#     def test_get_can_frame_dlc_single_frame__short_dlc(self, mock_get_min_dlc, mock_validate_payload_length,
#                                              example_can_addressing_format, payload_length, ai_bytes):
#         self.mock_get_data_bytes_used_by_can_addressing_format.return_value = ai_bytes
#         assert CanPacket.get_can_frame_dlc_single_frame(addressing_format=example_can_addressing_format,
#                                                         payload_length=payload_length) == mock_get_min_dlc.return_value
#         self.mock_validate_can_addressing_format.assert_called_once_with(example_can_addressing_format)
#         mock_validate_payload_length.assert_called_once_with(payload_length)
#         self.mock_get_data_bytes_used_by_can_addressing_format.assert_called_once_with(example_can_addressing_format)
#         mock_get_min_dlc.assert_called_once_with(payload_length + ai_bytes + CanPacket.SHORT_SF_DL_BYTES_USED)
#
#     @pytest.mark.parametrize("payload_length, ai_bytes", [
#         (61, 1),
#         (62, 0),
#         (31, 2),
#         (13, 0),
#     ])
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_payload_length")
#     @patch(f"{SCRIPT_LOCATION}.CanDlcHandler.get_min_dlc")
#     def test_get_can_frame_dlc_single_frame__long_dlc(self, mock_get_min_dlc, mock_validate_payload_length,
#                                             example_can_addressing_format, payload_length, ai_bytes):
#         self.mock_get_data_bytes_used_by_can_addressing_format.return_value = ai_bytes
#         assert CanPacket.get_can_frame_dlc_single_frame(addressing_format=example_can_addressing_format,
#                                                         payload_length=payload_length) == mock_get_min_dlc.return_value
#         self.mock_validate_can_addressing_format.assert_called_once_with(example_can_addressing_format)
#         mock_validate_payload_length.assert_called_once_with(payload_length)
#         self.mock_get_data_bytes_used_by_can_addressing_format.assert_called_once_with(example_can_addressing_format)
#         mock_get_min_dlc.assert_called_once_with(payload_length + ai_bytes + CanPacket.LONG_SF_DL_BYTES_USED)
#
#     # get_can_frame_dlc_first_frame
#
#     @pytest.mark.parametrize("dlc", [5, 7])
#     @pytest.mark.parametrize("payload_length, data_length", [
#         (20, 0xBAF),
#         (49, 0xE0F48C),
#     ])
#     @patch(f"{SCRIPT_LOCATION}.CanDlcHandler.encode")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_ff_dl")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_payload_length")
#     def test_get_can_frame_dlc_first_frame__inconsistency_error(self, mock_validate_payload_length, mock_validate_ff_dl,
#                                                       mock_encode_dlc,
#                                                       example_can_addressing_format, data_length, payload_length, dlc):
#         mock_encode_dlc.return_value = dlc
#         with pytest.raises(InconsistentArgumentsError):
#             CanPacket.get_can_frame_dlc_first_frame(addressing_format=example_can_addressing_format,
#                                                     data_length=data_length,
#                                                     payload_length=payload_length)
#         self.mock_validate_can_addressing_format.assert_called_once_with(example_can_addressing_format)
#         mock_validate_payload_length.assert_called_once_with(payload_length)
#         mock_validate_ff_dl.assert_called_once_with(data_length)
#         mock_encode_dlc.assert_called_once()
#         self.mock_get_data_bytes_used_by_can_addressing_format.assert_called_once_with(example_can_addressing_format)
#
#     @pytest.mark.parametrize("dlc", [8, 15])
#     @pytest.mark.parametrize("payload_length, data_length", [
#         (20, 0xBAF),
#         (49, 0xE0F48C),
#     ])
#     @patch(f"{SCRIPT_LOCATION}.CanDlcHandler.encode")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_ff_dl")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_payload_length")
#     def test_get_can_frame_dlc_first_frame__valid(self, mock_validate_payload_length, mock_validate_ff_dl,
#                                         mock_encode_dlc,
#                                         example_can_addressing_format, data_length, payload_length, dlc):
#         mock_encode_dlc.return_value = dlc
#         assert CanPacket.get_can_frame_dlc_first_frame(addressing_format=example_can_addressing_format,
#                                                        data_length=data_length,
#                                                        payload_length=payload_length) == dlc
#         self.mock_validate_can_addressing_format.assert_called_once_with(example_can_addressing_format)
#         mock_validate_payload_length.assert_called_once_with(payload_length)
#         mock_validate_ff_dl.assert_called_once_with(data_length)
#         mock_encode_dlc.assert_called_once()
#         self.mock_get_data_bytes_used_by_can_addressing_format.assert_called_once_with(example_can_addressing_format)
#
#     # get_can_frame_dlc_consecutive_frame
#
#     @pytest.mark.parametrize("payload_length, ai_bytes", [
#         (62, 1),
#         (63, 0),
#         (31, 2),
#         (13, 0),
#         (1, 0),
#     ])
#     @patch(f"{SCRIPT_LOCATION}.CanDlcHandler.get_min_dlc")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_payload_length")
#     def test_get_can_frame_dlc_consecutive_frame(self, mock_validate_payload_length, mock_get_min_dlc,
#                                        example_can_addressing_format, payload_length, ai_bytes):
#         self.mock_get_data_bytes_used_by_can_addressing_format.return_value = ai_bytes
#         assert CanPacket.get_can_frame_dlc_consecutive_frame(addressing_format=example_can_addressing_format,
#                                                              payload_length=payload_length) == mock_get_min_dlc.return_value
#         self.mock_validate_can_addressing_format.assert_called_once_with(example_can_addressing_format)
#         mock_validate_payload_length.assert_called_once_with(payload_length)
#         mock_get_min_dlc.assert_called_once_with(CanPacket.SN_BYTES_USED + payload_length + ai_bytes)
#         self.mock_get_data_bytes_used_by_can_addressing_format.assert_called_once_with(example_can_addressing_format)
#
#     # get_can_frame_dlc_flow_control
#
#     @pytest.mark.parametrize("ai_bytes", [0, 1, 2, 3])
#     @patch(f"{SCRIPT_LOCATION}.CanDlcHandler.get_min_dlc")
#     def test_get_can_frame_dlc_flow_control(self, mock_get_min_dlc, example_can_addressing_format, ai_bytes):
#         self.mock_get_data_bytes_used_by_can_addressing_format.return_value = ai_bytes
#         assert CanPacket.get_can_frame_dlc_flow_control(addressing_format=example_can_addressing_format) \
#                == mock_get_min_dlc.return_value
#         self.mock_validate_can_addressing_format.assert_called_once_with(example_can_addressing_format)
#         mock_get_min_dlc.assert_called_once_with(CanPacket.FS_BYTES_USED + ai_bytes)
#         self.mock_get_data_bytes_used_by_can_addressing_format.assert_called_once_with(example_can_addressing_format)
#
#     # create_can_frame_data_single_frame
#
#     @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
#         (None, "TA", "AE"),
#         ("some addressing format", 0x9A, 0x0B),
#     ])
#     @pytest.mark.parametrize("dlc, payload, filler_byte, data_bytes_number", [
#         (8, (0x01, 0x02), 0xB2, 8),
#         (8, (0x91, 0x90, 0x8F, 0x8E, 0x8D, 0x8C), 0xCC, 8),
#         (9, list(range(13, 5, -1)), 0x1F, 23),
#         (15, tuple(range(43)), 0x1F, 64),
#     ])
#     @pytest.mark.parametrize("ai_bytes", [[], [0xC1]])
#     @patch(f"{SCRIPT_LOCATION}.CanDlcHandler.decode")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket.get_can_frame_dlc_single_frame")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__get_can_frame_data_beginning")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_data_single_frame")
#     def test_create_can_frame_data_single_frame__dlc(self, mock_validate_data_single_frame, mock_get_can_frame_data_beginning,
#                                                      mock_get_can_frame_dlc_single_frame, mock_decode_dlc,
#                                                      addressing_format, target_address, address_extension,
#                                                      dlc, payload, filler_byte, data_bytes_number, ai_bytes):
#         mock_decode_dlc.return_value = data_bytes_number
#         mock_get_can_frame_data_beginning.return_value = ai_bytes
#         data = CanPacket.create_can_frame_data_single_frame(addressing_format=addressing_format,
#                                                             payload=payload,
#                                                             dlc=dlc,
#                                                             filler_byte=filler_byte,
#                                                             target_address=target_address,
#                                                             address_extension=address_extension)
#         mock_validate_data_single_frame.assert_called_once_with(addressing_format=addressing_format,
#                                                                 dlc=dlc,
#                                                                 payload=payload,
#                                                                 filler_byte=filler_byte)
#         mock_get_can_frame_data_beginning.assert_called_once_with(addressing_format=addressing_format,
#                                                                   target_address=target_address,
#                                                                   address_extension=address_extension)
#         mock_get_can_frame_dlc_single_frame.assert_not_called()
#         mock_decode_dlc.assert_called_once_with(dlc)
#         assert isinstance(data, tuple)
#         assert len(data) == data_bytes_number
#
#     @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
#         (None, "TA", "AE"),
#         ("some addressing format", 0x9A, 0x0B),
#     ])
#     @pytest.mark.parametrize("dlc, payload, filler_byte, data_bytes_number", [
#         (8, (0x01, 0x02), 0xB2, 8),
#         (8, (0x91, 0x90, 0x8F, 0x8E, 0x8D, 0x8C), 0xCC, 8),
#         (9, list(range(13, 5, -1)), 0x1F, 23),
#         (15, tuple(range(43)), 0x1F, 64),
#     ])
#     @pytest.mark.parametrize("ai_bytes", [[], [0xC1]])
#     @patch(f"{SCRIPT_LOCATION}.CanDlcHandler.decode")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket.get_can_frame_dlc_single_frame")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__get_can_frame_data_beginning")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_data_single_frame")
#     def test_create_can_frame_data_single_frame__no_dlc(self, mock_validate_data_single_frame, mock_get_can_frame_data_beginning,
#                                                         mock_get_can_frame_dlc_single_frame, mock_decode_dlc,
#                                                         addressing_format, target_address, address_extension,
#                                                         dlc, payload, filler_byte, data_bytes_number, ai_bytes):
#         mock_decode_dlc.return_value = data_bytes_number
#         mock_get_can_frame_data_beginning.return_value = ai_bytes
#         mock_get_can_frame_dlc_single_frame.return_value = dlc
#         data = CanPacket.create_can_frame_data_single_frame(addressing_format=addressing_format,
#                                                             payload=payload,
#                                                             dlc=None,
#                                                             filler_byte=filler_byte,
#                                                             target_address=target_address,
#                                                             address_extension=address_extension)
#         mock_validate_data_single_frame.assert_called_once_with(addressing_format=addressing_format,
#                                                                 dlc=None,
#                                                                 payload=payload,
#                                                                 filler_byte=filler_byte)
#         mock_get_can_frame_data_beginning.assert_called_once_with(addressing_format=addressing_format,
#                                                                   target_address=target_address,
#                                                                   address_extension=address_extension)
#         mock_get_can_frame_dlc_single_frame.assert_called_once_with(addressing_format=addressing_format,
#                                                                     payload_length=len(payload))
#         mock_decode_dlc.assert_called_once_with(dlc)
#         assert isinstance(data, tuple)
#         assert len(data) == data_bytes_number
#
#     # create_can_frame_data_first_frame
#
#     @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
#         (None, "TA", "AE"),
#         ("some addressing format", 0x9A, 0x0B),
#     ])
#     @pytest.mark.parametrize("dlc, data_length, payload, ai_bytes", [
#         (8, CanPacket.MAX_SHORT_FF_DL_VALUE, range(6), []),
#         (8, 15, range(5), [0xCC]),
#         (9, 8, range(6), [0xAA]),
#     ])
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__get_can_frame_data_beginning")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_data_first_frame")
#     def test_create_can_frame_data_first_frame__short_ff_dl(self, mock_validate_data_first_frame,
#                                                             mock_get_can_frame_data_beginning,
#                                                             dlc, data_length, payload, ai_bytes,
#                                                             addressing_format, target_address, address_extension):
#         mock_get_can_frame_data_beginning.return_value = ai_bytes
#         data = CanPacket.create_can_frame_data_first_frame(addressing_format=addressing_format,
#                                                            payload=payload,
#                                                            dlc=dlc,
#                                                            data_length=data_length,
#                                                            target_address=target_address,
#                                                            address_extension=address_extension)
#         mock_validate_data_first_frame.assert_called_once_with(addressing_format=addressing_format,
#                                                                dlc=dlc,
#                                                                payload=payload,
#                                                                data_length=data_length)
#         mock_get_can_frame_data_beginning.assert_called_once_with(addressing_format=addressing_format,
#                                                                   target_address=target_address,
#                                                                   address_extension=address_extension)
#         assert isinstance(data, tuple)
#         assert len(data) == len(ai_bytes) + len(payload) + CanPacket.SHORT_FF_DL_BYTES_USED
#
#     @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
#         (None, "TA", "AE"),
#         ("some addressing format", 0x9A, 0x0B),
#     ])
#     @pytest.mark.parametrize("dlc, data_length, payload, ai_bytes", [
#         (8, CanPacket.MAX_SHORT_FF_DL_VALUE + 1, [0x55], [0xAA]),
#         (15, CanPacket.MAX_LONG_FF_DL_VALUE, range(58), []),
#         (15, CanPacket.MAX_LONG_FF_DL_VALUE, range(57), [0x12]),
#     ])
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__get_can_frame_data_beginning")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_data_first_frame")
#     def test_create_can_frame_data_first_frame__long_ff_dl(self, mock_validate_data_first_frame,
#                                                            mock_get_can_frame_data_beginning,
#                                                            dlc, data_length, payload, ai_bytes,
#                                                            addressing_format, target_address, address_extension):
#         mock_get_can_frame_data_beginning.return_value = ai_bytes
#         data = CanPacket.create_can_frame_data_first_frame(addressing_format=addressing_format,
#                                                            payload=payload,
#                                                            dlc=dlc,
#                                                            data_length=data_length,
#                                                            target_address=target_address,
#                                                            address_extension=address_extension)
#         mock_validate_data_first_frame.assert_called_once_with(addressing_format=addressing_format,
#                                                                dlc=dlc,
#                                                                payload=payload,
#                                                                data_length=data_length)
#         mock_get_can_frame_data_beginning.assert_called_once_with(addressing_format=addressing_format,
#                                                                   target_address=target_address,
#                                                                   address_extension=address_extension)
#         assert isinstance(data, tuple)
#         assert len(data) == len(ai_bytes) + len(payload) + CanPacket.LONG_FF_DL_BYTES_USED
#
#     # create_can_frame_data_consecutive_frame
#
#     @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
#         (None, "TA", "AE"),
#         ("some addressing format", 0x9A, 0x0B),
#     ])
#     @pytest.mark.parametrize("dlc, data_bytes_number, payload, filler_byte, sequence_number", [
#         (8, 8, range(2), 0xBB, 0x5),
#         (4, 4, [0xFB], 0x00, 0xF),
#         (9, 9, range(7), 0x1F, 0x9),
#         (15, 64, range(20, 40), 0x00, 0xF),
#     ])
#     @pytest.mark.parametrize("ai_bytes", [[], [0xC1]])
#     @patch(f"{SCRIPT_LOCATION}.CanDlcHandler.decode")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket.get_can_frame_dlc_consecutive_frame")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__get_can_frame_data_beginning")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_data_consecutive_frame")
#     def test_create_can_frame_data_consecutive_frame__dlc(self, mock_validate_data_consecutive_frame,
#                                                           mock_get_can_frame_data_beginning,
#                                                           mock_get_can_frame_dlc_consecutive_frame, mock_decode_dlc,
#                                                           dlc, data_bytes_number, payload, filler_byte, sequence_number,
#                                                           addressing_format, target_address, address_extension, ai_bytes):
#         mock_decode_dlc.return_value = data_bytes_number
#         mock_get_can_frame_data_beginning.return_value = ai_bytes
#         data = CanPacket.create_can_frame_data_consecutive_frame(addressing_format=addressing_format,
#                                                                  payload=payload,
#                                                                  dlc=dlc,
#                                                                  sequence_number=sequence_number,
#                                                                  filler_byte=filler_byte,
#                                                                  target_address=target_address,
#                                                                  address_extension=address_extension)
#         mock_validate_data_consecutive_frame.assert_called_once_with(addressing_format=addressing_format,
#                                                                      dlc=dlc,
#                                                                      sequence_number=sequence_number,
#                                                                      payload=payload,
#                                                                      filler_byte=filler_byte)
#         mock_get_can_frame_data_beginning.assert_called_once_with(addressing_format=addressing_format,
#                                                                   target_address=target_address,
#                                                                   address_extension=address_extension)
#         mock_get_can_frame_dlc_consecutive_frame.assert_not_called()
#         mock_decode_dlc.assert_called_once_with(dlc)
#         assert isinstance(data, tuple)
#         assert len(data) == data_bytes_number
#
#     @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
#         (None, "TA", "AE"),
#         ("some addressing format", 0x9A, 0x0B),
#     ])
#     @pytest.mark.parametrize("dlc, data_bytes_number, payload, filler_byte, sequence_number", [
#         (8, 8, range(2), 0xBB, 0x5),
#         (4, 4, [0xFB], 0x00, 0xF),
#         (9, 9, range(7), 0x1F, 0x9),
#         (15, 64, range(20, 40), 0x00, 0xF),
#     ])
#     @pytest.mark.parametrize("ai_bytes", [[], [0xC1]])
#     @patch(f"{SCRIPT_LOCATION}.CanDlcHandler.decode")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket.get_can_frame_dlc_consecutive_frame")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__get_can_frame_data_beginning")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_data_consecutive_frame")
#     def test_create_can_frame_data_consecutive_frame__no_dlc(self, mock_validate_data_consecutive_frame,
#                                                              mock_get_can_frame_data_beginning,
#                                                              mock_get_can_frame_dlc_consecutive_frame, mock_decode_dlc,
#                                                              dlc, data_bytes_number, payload, filler_byte, sequence_number,
#                                                              addressing_format, target_address, address_extension, ai_bytes):
#         mock_decode_dlc.return_value = data_bytes_number
#         mock_get_can_frame_data_beginning.return_value = ai_bytes
#         mock_get_can_frame_dlc_consecutive_frame.return_value = dlc
#         data = CanPacket.create_can_frame_data_consecutive_frame(addressing_format=addressing_format,
#                                                                  payload=payload,
#                                                                  dlc=None,
#                                                                  sequence_number=sequence_number,
#                                                                  filler_byte=filler_byte,
#                                                                  target_address=target_address,
#                                                                  address_extension=address_extension)
#         mock_validate_data_consecutive_frame.assert_called_once_with(addressing_format=addressing_format,
#                                                                      dlc=None,
#                                                                      sequence_number=sequence_number,
#                                                                      payload=payload,
#                                                                      filler_byte=filler_byte)
#         mock_get_can_frame_data_beginning.assert_called_once_with(addressing_format=addressing_format,
#                                                                   target_address=target_address,
#                                                                   address_extension=address_extension)
#         mock_get_can_frame_dlc_consecutive_frame.assert_called_once_with(addressing_format=addressing_format,
#                                                                          payload_length=len(payload))
#         mock_decode_dlc.assert_called_once_with(dlc)
#         assert isinstance(data, tuple)
#         assert len(data) == data_bytes_number
#
#     # create_can_frame_data_flow_control
#
#     @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
#         (None, "TA", "AE"),
#         ("some addressing format", 0x9A, 0x0B),
#     ])
#     @pytest.mark.parametrize("dlc, data_bytes_number, filler_byte, flow_status, block_size, stmin", [
#         (8, 8, 0x12, CanFlowStatus.ContinueToSend.value, 0x55, 0x33),
#         (4, 4, 0xAA, CanFlowStatus.Overflow, None, None),
#         (9, 9, 0x55, CanFlowStatus.Wait, None, None),
#         (15, 64, 0x66, CanFlowStatus.Overflow, "something", "else"),
#     ])
#     @pytest.mark.parametrize("ai_bytes", [[], [0xC1]])
#     @patch(f"{SCRIPT_LOCATION}.CanDlcHandler.decode")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket.get_can_frame_dlc_flow_control")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__get_can_frame_data_beginning")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_data_flow_control")
#     def test_create_can_frame_data_flow_control__dlc(self, mock_validate_data_flow_control,
#                                                      mock_get_can_frame_data_beginning,
#                                                      mock_get_can_frame_dlc_flow_control, mock_decode_dlc,
#                                                      dlc, data_bytes_number, filler_byte, flow_status, block_size, stmin,
#                                                      addressing_format, target_address, address_extension, ai_bytes):
#         mock_decode_dlc.return_value = data_bytes_number
#         mock_get_can_frame_data_beginning.return_value = ai_bytes
#         data = CanPacket.create_can_frame_data_flow_control(addressing_format=addressing_format,
#                                                             dlc=dlc,
#                                                             flow_status=flow_status,
#                                                             block_size=block_size,
#                                                             stmin=stmin,
#                                                             filler_byte=filler_byte,
#                                                             target_address=target_address,
#                                                             address_extension=address_extension)
#         mock_validate_data_flow_control.assert_called_once_with(addressing_format=addressing_format,
#                                                                 dlc=dlc,
#                                                                 flow_status=flow_status,
#                                                                 block_size=block_size,
#                                                                 stmin=stmin,
#                                                                 filler_byte=filler_byte)
#         mock_get_can_frame_data_beginning.assert_called_once_with(addressing_format=addressing_format,
#                                                                   target_address=target_address,
#                                                                   address_extension=address_extension)
#         mock_get_can_frame_dlc_flow_control.assert_not_called()
#         mock_decode_dlc.assert_called_once_with(dlc)
#         assert isinstance(data, tuple)
#         assert len(data) == data_bytes_number
#
#     @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
#         (None, "TA", "AE"),
#         ("some addressing format", 0x9A, 0x0B),
#     ])
#     @pytest.mark.parametrize("dlc, data_bytes_number, filler_byte, flow_status, block_size, stmin", [
#         (8, 8, 0x12, CanFlowStatus.ContinueToSend.value, 0x55, 0x33),
#         (4, 4, 0xAA, CanFlowStatus.Overflow, None, None),
#         (9, 9, 0x55, CanFlowStatus.Wait, None, None),
#         (15, 64, 0x66, CanFlowStatus.Overflow, "something", "else"),
#     ])
#     @pytest.mark.parametrize("ai_bytes", [[], [0xC1]])
#     @patch(f"{SCRIPT_LOCATION}.CanDlcHandler.decode")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket.get_can_frame_dlc_flow_control")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__get_can_frame_data_beginning")
#     @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_data_flow_control")
#     def test_create_can_frame_data_flow_control__no_dlc(self, mock_validate_data_flow_control,
#                                                         mock_get_can_frame_data_beginning,
#                                                         mock_get_can_frame_dlc_flow_control, mock_decode_dlc,
#                                                         dlc, data_bytes_number, filler_byte, flow_status, block_size, stmin,
#                                                         addressing_format, target_address, address_extension, ai_bytes):
#         mock_decode_dlc.return_value = data_bytes_number
#         mock_get_can_frame_data_beginning.return_value = ai_bytes
#         mock_get_can_frame_dlc_flow_control.return_value = dlc
#         data = CanPacket.create_can_frame_data_flow_control(addressing_format=addressing_format,
#                                                             dlc=None,
#                                                             flow_status=flow_status,
#                                                             block_size=block_size,
#                                                             stmin=stmin,
#                                                             filler_byte=filler_byte,
#                                                             target_address=target_address,
#                                                             address_extension=address_extension)
#         mock_validate_data_flow_control.assert_called_once_with(addressing_format=addressing_format,
#                                                                 dlc=None,
#                                                                 flow_status=flow_status,
#                                                                 block_size=block_size,
#                                                                 stmin=stmin,
#                                                                 filler_byte=filler_byte)
#         mock_get_can_frame_data_beginning.assert_called_once_with(addressing_format=addressing_format,
#                                                                   target_address=target_address,
#                                                                   address_extension=address_extension)
#         mock_get_can_frame_dlc_flow_control.assert_called_once_with(addressing_format=addressing_format)
#         mock_decode_dlc.assert_called_once_with(dlc)
#         assert isinstance(data, tuple)
#         assert len(data) == data_bytes_number
#
#     # __get_can_frame_data_beginning
#
#     @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
#         ("some addressing", "TA", "AE"),
#         (0, 0x54, 0x76),
#         (None, None, None),
#     ])
#     @patch(f"{SCRIPT_LOCATION}.CanAddressingFormat")
#     def test_get_can_frame_data_beginning__empty(self, mock_can_addressing_format_class,
#                                                  addressing_format, target_address, address_extension):
#         mock_can_addressing_format_class.get_number_of_data_bytes_used.return_value = 0
#         assert CanPacket._CanPacket__get_can_frame_data_beginning(addressing_format=addressing_format,
#                                                                   target_address=target_address,
#                                                                   address_extension=address_extension) == []
#         mock_can_addressing_format_class.validate_member.assert_called_once_with(addressing_format)
#         mock_can_addressing_format_class.assert_called_once_with(addressing_format)
#         mock_can_addressing_format_class.get_number_of_data_bytes_used.assert_called_once_with(
#             mock_can_addressing_format_class.return_value)
#         self.mock_validate_raw_byte.assert_not_called()
#
#     @pytest.mark.parametrize("addressing_format, target_address, address_extension, data_bytes_used", [
#         ("some addressing", "TA", "AE", 1),
#         (CanAddressingFormat.EXTENDED_ADDRESSING, 0x55, None, 2),
#         (CanAddressingFormat.MIXED_11BIT_ADDRESSING, None, 0xFE, 2),
#         (CanAddressingFormat.MIXED_29BIT_ADDRESSING, 0xDC, 0xFE, 2),
#         ("another", 0xDC, 0xFE, 2),
#     ])
#     @patch(f"{SCRIPT_LOCATION}.CanAddressingFormat")
#     def test_get_can_frame_data_beginning__unknown(self, mock_can_addressing_format_class,
#                                                    addressing_format, target_address, address_extension, data_bytes_used):
#         mock_can_addressing_format_class.get_number_of_data_bytes_used.return_value = data_bytes_used
#         mock_can_addressing_format_class.return_value = addressing_format
#         with pytest.raises(NotImplementedError):
#             CanPacket._CanPacket__get_can_frame_data_beginning(addressing_format=addressing_format,
#                                                                target_address=target_address,
#                                                                address_extension=address_extension)
#         mock_can_addressing_format_class.validate_member.assert_called_once_with(addressing_format)
#         mock_can_addressing_format_class.assert_called_once_with(addressing_format)
#         mock_can_addressing_format_class.get_number_of_data_bytes_used.assert_called_once_with(
#             mock_can_addressing_format_class.return_value)
#         self.mock_validate_raw_byte.assert_not_called()
#
#     @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.EXTENDED_ADDRESSING,
#                                                    CanAddressingFormat.EXTENDED_ADDRESSING.value])
#     @pytest.mark.parametrize("target_address, address_extension", [
#         ("TA", "AE"),
#         (0x54, 0x76),
#         (None, None),
#     ])
#     def test_get_can_frame_data_beginning__extended(self, addressing_format, target_address, address_extension):
#         self.mock_get_data_bytes_used_by_can_addressing_format.return_value = 1
#         assert CanPacket._CanPacket__get_can_frame_data_beginning(addressing_format=addressing_format,
#                                                                   target_address=target_address,
#                                                                   address_extension=address_extension) == [target_address]
#         self.mock_get_data_bytes_used_by_can_addressing_format.assert_called_once_with(CanAddressingFormat.EXTENDED_ADDRESSING)
#         self.mock_validate_raw_byte.assert_called_once_with(target_address)
#
#     @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.MIXED_11BIT_ADDRESSING,
#                                                    CanAddressingFormat.MIXED_11BIT_ADDRESSING.value,
#                                                    CanAddressingFormat.MIXED_29BIT_ADDRESSING,
#                                                    CanAddressingFormat.MIXED_29BIT_ADDRESSING.value])
#     @pytest.mark.parametrize("target_address, address_extension", [
#         ("TA", "AE"),
#         (0x54, 0x76),
#         (None, None),
#     ])
#     def test_get_can_frame_data_beginning__mixed(self, addressing_format, target_address, address_extension):
#         self.mock_get_data_bytes_used_by_can_addressing_format.return_value = 1
#         assert CanPacket._CanPacket__get_can_frame_data_beginning(addressing_format=addressing_format,
#                                                                   target_address=target_address,
#                                                                   address_extension=address_extension) == [address_extension]
#         self.mock_get_data_bytes_used_by_can_addressing_format.assert_called_once()
#         self.mock_validate_raw_byte.assert_called_once_with(address_extension)
#
#
# class TestCanPacket:
#     """Tests for `CanPacket` class."""
#
#     SCRIPT_LOCATION = TestCanPacketClassMethods.SCRIPT_LOCATION
#
#     def setup(self):
#         self.mock_can_packet = Mock(spec=CanPacket,
#                                     MIN_SEQUENCE_NUMBER=CanPacket.MIN_SEQUENCE_NUMBER,
#                                     MAX_SEQUENCE_NUMBER=CanPacket.MAX_SEQUENCE_NUMBER,
#                                     MAX_DLC_VALUE_SHORT_SF_DL=CanPacket.MAX_DLC_VALUE_SHORT_SF_DL,
#                                     SHORT_SF_DL_BYTES_USED=CanPacket.SHORT_SF_DL_BYTES_USED,
#                                     LONG_SF_DL_BYTES_USED=CanPacket.LONG_SF_DL_BYTES_USED,
#                                     SHORT_FF_DL_BYTES_USED=CanPacket.SHORT_FF_DL_BYTES_USED,
#                                     LONG_FF_DL_BYTES_USED=CanPacket.LONG_FF_DL_BYTES_USED,
#                                     MAX_SHORT_FF_DL_VALUE=CanPacket.MAX_SHORT_FF_DL_VALUE,
#                                     SN_BYTES_USED=CanPacket.SN_BYTES_USED)
#         # patching
#         self._patcher_validate_addressing_type = patch(f"{self.SCRIPT_LOCATION}.AddressingType.validate_member")
#         self.mock_validate_addressing_type = self._patcher_validate_addressing_type.start()
#         self._patcher_validate_can_addressing_format = \
#             patch(f"{self.SCRIPT_LOCATION}.CanAddressingFormat.validate_member")
#         self.mock_validate_can_addressing_format = self._patcher_validate_can_addressing_format.start()
#         self._patcher_get_data_bytes_used_by_can_addressing_format = \
#             patch(f"{self.SCRIPT_LOCATION}.CanAddressingFormat.get_number_of_data_bytes_used")
#         self.mock_get_data_bytes_used_by_can_addressing_format = \
#             self._patcher_get_data_bytes_used_by_can_addressing_format.start()
#         self._patcher_validate_can_packet_type = patch(f"{self.SCRIPT_LOCATION}.CanPacketType.validate_member")
#         self.mock_validate_can_packet_type = self._patcher_validate_can_packet_type.start()
#         self._patcher_validate_can_id = patch(f"{self.SCRIPT_LOCATION}.CanIdHandler.validate_can_id")
#         self.mock_validate_can_id = self._patcher_validate_can_id.start()
#         self._patcher_decode_normal_fixed_addressed_can_id = \
#             patch(f"{self.SCRIPT_LOCATION}.CanIdHandler.decode_normal_fixed_addressed_can_id")
#         self.mock_decode_normal_fixed_addressed_can_id = self._patcher_decode_normal_fixed_addressed_can_id.start()
#         self._patcher_decode_mixed_addressed_29bit_can_id = \
#             patch(f"{self.SCRIPT_LOCATION}.CanIdHandler.decode_mixed_addressed_29bit_can_id")
#         self.mock_decode_mixed_addressed_29bit_can_id = self._patcher_decode_mixed_addressed_29bit_can_id.start()
#         self._patcher_validate_dlc = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler.validate_dlc")
#         self.mock_validate_dlc = self._patcher_validate_dlc.start()
#         self._patcher_decode_dlc = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler.decode")
#         self.mock_decode_dlc = self._patcher_decode_dlc.start()
#         self._patcher_validate_flow_status = patch(f"{self.SCRIPT_LOCATION}.CanFlowStatus.validate_member")
#         self.mock_validate_flow_status = self._patcher_validate_flow_status.start()
#         self._patcher_validate_raw_byte = patch(f"{self.SCRIPT_LOCATION}.validate_raw_byte")
#         self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
#         self._patcher_validate_raw_bytes = patch(f"{self.SCRIPT_LOCATION}.validate_raw_bytes")
#         self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
#         self._patcher_warn = patch(f"{self.SCRIPT_LOCATION}.warn")
#         self.mock_warn = self._patcher_warn.start()
#
#     def teardown(self):
#         self._patcher_validate_addressing_type.stop()
#         self._patcher_validate_can_addressing_format.stop()
#         self._patcher_validate_can_packet_type.stop()
#         self._patcher_validate_can_id.stop()
#         self._patcher_decode_normal_fixed_addressed_can_id.stop()
#         self._patcher_decode_mixed_addressed_29bit_can_id.stop()
#         self._patcher_validate_dlc.stop()
#         self._patcher_decode_dlc.stop()
#         self._patcher_validate_flow_status.stop()
#         self._patcher_validate_raw_byte.stop()
#         self._patcher_validate_raw_bytes.stop()
#         self._patcher_warn.stop()
#
#     # __init__
#
#     @pytest.mark.parametrize("packet_type", ["some packet type", 1])
#     @pytest.mark.parametrize("packet_type_specific_kwargs", [
#         {"v1": "some value", "v2": "Some other vlaue"},
#         {"p1": "something", "p2": "something else"}
#     ])
#     @pytest.mark.parametrize("addressing_type, addressing_format", [
#         (None, None),
#         (AddressingType.FUNCTIONAL, CanAddressingFormat.NORMAL_11BIT_ADDRESSING),
#     ])
#     @pytest.mark.parametrize("can_id, target_address, source_address, address_extension", [
#         (None, 1, 2, 3),
#         (0x675, None, None, None),
#     ])
#     @pytest.mark.parametrize("dlc, filler_byte", [
#         (None, 0xCC),
#         (8, 0xAA),
#     ])
#     def test_init(self, addressing_type, addressing_format, packet_type, can_id, dlc, filler_byte,
#                   target_address, source_address, address_extension, packet_type_specific_kwargs):
#         CanPacket.__init__(self=self.mock_can_packet,
#                            packet_type=packet_type,
#                            addressing=addressing_type,
#                            addressing_format=addressing_format,
#                            can_id=can_id,
#                            target_address=target_address,
#                            source_address=source_address,
#                            address_extension=address_extension,
#                            dlc=dlc,
#                            filler_byte=filler_byte,
#                            **packet_type_specific_kwargs)
#         assert self.mock_can_packet._CanPacket__addressing_format is None
#         self.mock_can_packet.set_address_information.assert_called_once_with(
#             addressing=addressing_type,
#             addressing_format=addressing_format,
#             can_id=can_id,
#             target_address=target_address,
#             source_address=source_address,
#             address_extension=address_extension)
#         self.mock_can_packet.set_packet_data.assert_called_once_with(
#             packet_type=packet_type,
#             dlc=dlc,
#             filler_byte=filler_byte,
#             **packet_type_specific_kwargs)
#
#     # raw_frame_data
#
#     @pytest.mark.parametrize("value", [None, "some", False, 5.5])
#     def test_raw_frame_data__get(self, value):
#         self.mock_can_packet._CanPacket__raw_frame_data = value
#         assert CanPacket.raw_frame_data.fget(self=self.mock_can_packet) == value
#
#     # addressing
#
#     @pytest.mark.parametrize("value", [None, "some", False, 5.5])
#     def test_addressing__get(self, value):
#         self.mock_can_packet._CanPacket__addressing = value
#         assert CanPacket.addressing.fget(self=self.mock_can_packet) == value
#
#     # addressing_format
#
#     @pytest.mark.parametrize("value", [None, "some", False, 5.5])
#     def test_addressing_format__get(self, value):
#         self.mock_can_packet._CanPacket__addressing_format = value
#         assert CanPacket.addressing_format.fget(self=self.mock_can_packet) == value
#
#     # packet_type
#
#     @pytest.mark.parametrize("value", [None, "some", False, 5.5])
#     def test_packet_type__get(self, value):
#         self.mock_can_packet._CanPacket__packet_type = value
#         assert CanPacket.packet_type.fget(self=self.mock_can_packet) == value
#
#     # can_id
#
#     @pytest.mark.parametrize("value", [None, "some", False, 5.5])
#     def test_can_id__get(self, value):
#         self.mock_can_packet._CanPacket__can_id = value
#         assert CanPacket.can_id.fget(self=self.mock_can_packet) == value
#
#     # dlc
#
#     @pytest.mark.parametrize("value", [None, "some", False, 5.5])
#     def test_dlc__get(self, value):
#         self.mock_can_packet._CanPacket__dlc = value
#         assert CanPacket.dlc.fget(self=self.mock_can_packet) == value
#
#     # address_extension
#
#     @pytest.mark.parametrize("value", [None, "some", False, 5.5])
#     def test_address_extension__get(self, value):
#         self.mock_can_packet._CanPacket__address_extension = value
#         assert CanPacket.address_extension.fget(self=self.mock_can_packet) == value
#
#     # target_address
#
#     @pytest.mark.parametrize("value", [None, "some", False, 5.5])
#     def test_target_address__get(self, value):
#         self.mock_can_packet._CanPacket__target_address = value
#         assert CanPacket.target_address.fget(self=self.mock_can_packet) == value
#
#     # source_address
#
#     @pytest.mark.parametrize("address_extension", [None, "unknown", CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
#                                                    CanAddressingFormat.EXTENDED_ADDRESSING,
#                                                    CanAddressingFormat.MIXED_11BIT_ADDRESSING])
#     def test_source_address__get__none(self, address_extension):
#         self.mock_can_packet.address_extension = address_extension
#         assert CanPacket.source_address.fget(self=self.mock_can_packet) is None
#
#     @pytest.mark.parametrize("value", [None, "some", False, 5.5])
#     def test_source_address__get__normal_fixed(self, value):
#         self.mock_decode_normal_fixed_addressed_can_id.return_value = ("addressing type", "target address", value)
#         self.mock_can_packet.addressing_format = CanAddressingFormat.NORMAL_FIXED_ADDRESSING
#         assert CanPacket.source_address.fget(self=self.mock_can_packet) is value
#         self.mock_decode_normal_fixed_addressed_can_id.assert_called_once_with(self.mock_can_packet.can_id)
#
#     @pytest.mark.parametrize("value", [None, "some", False, 5.5])
#     def test_source_address__get__mixed_29bit(self, value):
#         self.mock_decode_mixed_addressed_29bit_can_id.return_value = ("addressing type", "target address", value)
#         self.mock_can_packet.addressing_format = CanAddressingFormat.MIXED_29BIT_ADDRESSING
#         assert CanPacket.source_address.fget(self=self.mock_can_packet) is value
#         self.mock_decode_mixed_addressed_29bit_can_id.assert_called_once_with(self.mock_can_packet.can_id)
#
#     # payload
#
#     @pytest.mark.parametrize("packet_type", [None, CanPacketType.FLOW_CONTROL, "something new"])
#     def test_payload__none(self, packet_type):
#         self.mock_can_packet.packet_type = packet_type
#         assert CanPacket.payload.fget(self=self.mock_can_packet) is None
#
#     @pytest.mark.parametrize("raw_frame_data, ai_bytes_number, data_length", [
#         ([0x01, 0x54], 0, 1),
#         ([0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54], 1, 6),
#         ((0xA1, 0xB2, 0xC3, 0x55), 1, 2),
#         (tuple(range(8)), 0, 7),
#     ])
#     def test_payload__single_frame_short_sf_dl(self, raw_frame_data, ai_bytes_number, data_length):
#         self.mock_can_packet.packet_type = CanPacketType.SINGLE_FRAME
#         self.mock_can_packet.dlc = len(raw_frame_data)
#         self.mock_can_packet.raw_frame_data = raw_frame_data
#         self.mock_can_packet.data_length = data_length
#         self.mock_get_data_bytes_used_by_can_addressing_format.return_value = ai_bytes_number
#         payload_offset = ai_bytes_number+CanPacket.SHORT_SF_DL_BYTES_USED
#         assert CanPacket.payload.fget(self=self.mock_can_packet) == raw_frame_data[payload_offset:payload_offset+data_length]
#         self.mock_get_data_bytes_used_by_can_addressing_format.assert_called_once_with(self.mock_can_packet.addressing_format)
#
#     @pytest.mark.parametrize("raw_frame_data, ai_bytes_number, data_length", [
#         (list(range(64)), 0, 62),
#         (list(range(0xF0, 0x10, -5)), 1, 3),
#         ((0xA1, 0xB2, 0xC3, 0xD4, 0xE5, 0xF6, 0x07, 0x18, 0x29), 1, 7),
#     ])
#     def test_payload__single_frame_long_sf_dl(self, raw_frame_data, ai_bytes_number, data_length):
#         self.mock_can_packet.packet_type = CanPacketType.SINGLE_FRAME
#         self.mock_can_packet.dlc = len(raw_frame_data)
#         self.mock_can_packet.raw_frame_data = raw_frame_data
#         self.mock_can_packet.data_length = data_length
#         self.mock_get_data_bytes_used_by_can_addressing_format.return_value = ai_bytes_number
#         payload_offset = ai_bytes_number+CanPacket.LONG_SF_DL_BYTES_USED
#         assert CanPacket.payload.fget(self=self.mock_can_packet) == raw_frame_data[payload_offset:payload_offset+data_length]
#         self.mock_get_data_bytes_used_by_can_addressing_format.assert_called_once_with(
#             self.mock_can_packet.addressing_format)
#
#     @pytest.mark.parametrize("raw_frame_data, ai_bytes_number, data_length", [
#         ([0x1F, 0xFF, 0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10], 0, 0xFFF),
#         ([0x81, 0x12, 0x00, 0xFF, 0xEE, 0xDD, 0xCC, 0xBB], 1, 0x200),
#         ([0x54, 0x10, 0x01, 0x90, 0x81, 0x72], 1, 0x1),
#     ])
#     def test_payload__first_frame_short_ff_dl(self, raw_frame_data, ai_bytes_number, data_length):
#         self.mock_can_packet.packet_type = CanPacketType.FIRST_FRAME
#         self.mock_can_packet.raw_frame_data = raw_frame_data
#         self.mock_can_packet.data_length = data_length
#         self.mock_get_data_bytes_used_by_can_addressing_format.return_value = ai_bytes_number
#         payload_offset = ai_bytes_number + CanPacket.SHORT_FF_DL_BYTES_USED
#         assert CanPacket.payload.fget(self=self.mock_can_packet) == raw_frame_data[payload_offset:]
#         self.mock_get_data_bytes_used_by_can_addressing_format.assert_called_once_with(
#             self.mock_can_packet.addressing_format)
#
#     @pytest.mark.parametrize("raw_frame_data, ai_bytes_number, data_length", [
#         ([0x10, 0x00, 0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10], 0, 0x1000),
#         ([0x81, 0x10, 0x00, 0xFF, 0xEE, 0xDD, 0xCC, 0xBB], 1, 0xFFFFFFFF),
#         ([0x54, 0x10, 0x00, 0x90, 0x81, 0x72, 0x63, 0x54, 0x45, 0x70] + list(range(10)), 1, 0x109F),
#     ])
#     def test_payload__first_frame_long_ff_dl(self, raw_frame_data, ai_bytes_number, data_length):
#         self.mock_can_packet.packet_type = CanPacketType.FIRST_FRAME
#         self.mock_can_packet.raw_frame_data = raw_frame_data
#         self.mock_can_packet.data_length = data_length
#         self.mock_get_data_bytes_used_by_can_addressing_format.return_value = ai_bytes_number
#         payload_offset = ai_bytes_number + CanPacket.LONG_FF_DL_BYTES_USED
#         assert CanPacket.payload.fget(self=self.mock_can_packet) == raw_frame_data[payload_offset:]
#         self.mock_get_data_bytes_used_by_can_addressing_format.assert_called_once_with(
#             self.mock_can_packet.addressing_format)
#
#     @pytest.mark.parametrize("raw_frame_data, ai_bytes_number", [
#         ([0x20, 0x54], 0),
#         ([0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54], 1),
#         (tuple(range(60)), 1),
#     ])
#     def test_payload__consecutive_frame(self, raw_frame_data, ai_bytes_number):
#         self.mock_can_packet.packet_type = CanPacketType.CONSECUTIVE_FRAME
#         self.mock_can_packet.raw_frame_data = raw_frame_data
#         self.mock_get_data_bytes_used_by_can_addressing_format.return_value = ai_bytes_number
#         payload_offset = ai_bytes_number + CanPacket.SN_BYTES_USED
#         assert CanPacket.payload.fget(self=self.mock_can_packet) == raw_frame_data[payload_offset:]
#         self.mock_get_data_bytes_used_by_can_addressing_format.assert_called_once_with(
#             self.mock_can_packet.addressing_format)
#
#     # data_length
#
#     @pytest.mark.parametrize("packet_type", [None, CanPacketType.FLOW_CONTROL, CanPacketType.CONSECUTIVE_FRAME,
#                                              "something new"])
#     def test_data_length__none(self, packet_type):
#         self.mock_can_packet.packet_type = packet_type
#         assert CanPacket.data_length.fget(self=self.mock_can_packet) is None
#
#     @pytest.mark.parametrize("ai_bytes_number, raw_frame_data, expected_data_length", [
#         (0, (0x02, 0x12, 0x34, 0x56, 0x78, 0x9A), 2),
#         (0, [0x00, 0x12] + list(range(62)), 0x12),
#         (1, [0x02, 0x05, 0x08, 0x0A, 0xFE, 0xDC, 0xBA, 0x98], 5),
#         (1, [0x02, 0x00, 0x3D] + list(range(100, 163)), 0x3D),
#     ])
#     def test_data_length__single_frame(self, ai_bytes_number, raw_frame_data, expected_data_length):
#         self.mock_can_packet.packet_type = CanPacketType.SINGLE_FRAME
#         self.mock_can_packet.raw_frame_data = raw_frame_data
#         self.mock_can_packet.dlc = len(raw_frame_data)
#         self.mock_get_data_bytes_used_by_can_addressing_format.return_value = ai_bytes_number
#         assert CanPacket.data_length.fget(self=self.mock_can_packet) == expected_data_length
#         self.mock_get_data_bytes_used_by_can_addressing_format.assert_called_once_with(
#             self.mock_can_packet.addressing_format)
#
#     @pytest.mark.parametrize("ai_bytes_number, raw_frame_data, expected_data_length", [
#         (0, (0x10, 0x0A, 0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC), 10),
#         (0, [0x1F, 0xFF] + list(range(62)), 0xFFF),
#         (1, [0x1F, 0x1D, 0xAB] + list(range(100, 161)), 0xDAB),
#         (1, [0x10, 0x10, 0x00, 0xFF, 0xFF, 0xFF, 0xFF] + list(range(100, 157)), 0xFFFFFFFF),
#         (1, (0xAA, 0x10, 0x00, 0x00, 0x00, 0x10, 0x00, 0xAA), 0x1000),
#         (1, (0xF0, 0x10, 0x00, 0xF1, 0xE2, 0xD3, 0xC4, 0xAA), 0xF1E2D3C4),
#     ])
#     def test_data_length__first_frame(self, ai_bytes_number, raw_frame_data, expected_data_length):
#         self.mock_can_packet.packet_type = CanPacketType.FIRST_FRAME
#         self.mock_can_packet.raw_frame_data = raw_frame_data
#         self.mock_get_data_bytes_used_by_can_addressing_format.return_value = ai_bytes_number
#         assert CanPacket.data_length.fget(self=self.mock_can_packet) == expected_data_length
#         self.mock_get_data_bytes_used_by_can_addressing_format.assert_called_once_with(
#             self.mock_can_packet.addressing_format)
#
#     # sequence_number
#
#     @pytest.mark.parametrize("packet_type", [None, CanPacketType.FLOW_CONTROL, CanPacketType.FIRST_FRAME,
#                                              CanPacketType.SINGLE_FRAME, "something new"])
#     def test_sequence_number__none(self, packet_type):
#         self.mock_can_packet.packet_type = packet_type
#         assert CanPacket.sequence_number.fget(self=self.mock_can_packet) is None
#
#     @pytest.mark.parametrize("ai_bytes_number, raw_frame_data, expected_sequence_number", [
#         (0, (0x20, 0xFE), 0),
#         (0, [0x2F, 0x91, 0xDC, 0xBA] + list(range(50, 110)), 0xF),
#         (1, (0x2F, 0x2A, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25), 0xA),
#         (1, [0x55, 0x23] + list(range(30)), 0x3),
#     ])
#     def test_sequence_number__consecutive_frame(self, ai_bytes_number, raw_frame_data, expected_sequence_number):
#         self.mock_can_packet.packet_type = CanPacketType.CONSECUTIVE_FRAME
#         self.mock_can_packet.raw_frame_data = raw_frame_data
#         self.mock_get_data_bytes_used_by_can_addressing_format.return_value = ai_bytes_number
#         assert CanPacket.sequence_number.fget(self=self.mock_can_packet) == expected_sequence_number
#         self.mock_get_data_bytes_used_by_can_addressing_format.assert_called_once_with(
#             self.mock_can_packet.addressing_format)
#
#     # flow_status
#
#     @pytest.mark.parametrize("packet_type", [None, CanPacketType.CONSECUTIVE_FRAME, CanPacketType.FIRST_FRAME,
#                                              CanPacketType.SINGLE_FRAME, "something new"])
#     def test_flow_status__none(self, packet_type):
#         self.mock_can_packet.packet_type = packet_type
#         assert CanPacket.flow_status.fget(self=self.mock_can_packet) is None
#
#     @pytest.mark.parametrize("ai_bytes_number, raw_frame_data, expected_flow_status", [
#         (0, (0x30, 0x12, 0x34), 0),
#         (0, (0x3F, 0xED, 0xCB), 0xF),
#         (1, (0x3F, 0x3B, 0x3A, 0x39, 0x38, 0x37, 0x36, 0x35), 0xB),
#         (1, [0x33, 0x34] + list(range(62)), 0x4),
#     ])
#     @patch(f"{SCRIPT_LOCATION}.CanFlowStatus")
#     def test_flow_status__flow_control(self, mock_flow_status_class,
#                                        ai_bytes_number, raw_frame_data, expected_flow_status):
#         self.mock_can_packet.packet_type = CanPacketType.FLOW_CONTROL
#         self.mock_can_packet.raw_frame_data = raw_frame_data
#         self.mock_get_data_bytes_used_by_can_addressing_format.return_value = ai_bytes_number
#         assert CanPacket.flow_status.fget(self=self.mock_can_packet) == mock_flow_status_class.return_value
#         mock_flow_status_class.assert_called_once_with(expected_flow_status)
#         self.mock_get_data_bytes_used_by_can_addressing_format.assert_called_once_with(
#             self.mock_can_packet.addressing_format)
#
#     # block_size
#
#     @pytest.mark.parametrize("packet_type", [None, CanPacketType.CONSECUTIVE_FRAME, CanPacketType.FIRST_FRAME,
#                                              CanPacketType.SINGLE_FRAME, "something new"])
#     def test_block_size__none(self, packet_type):
#         self.mock_can_packet.packet_type = packet_type
#         assert CanPacket.block_size.fget(self=self.mock_can_packet) is None
#
#     @pytest.mark.parametrize("flow_status", [CanFlowStatus.Wait.value, CanFlowStatus.Overflow.value, "something", None])
#     def test_block_size__flow_control_not_cts(self, flow_status):
#         self.mock_can_packet.packet_type = CanPacketType.FLOW_CONTROL
#         self.mock_can_packet.flow_status = flow_status
#         assert CanPacket.block_size.fget(self=self.mock_can_packet) is None
#
#     @pytest.mark.parametrize("ai_bytes_number, raw_frame_data, expected_block_size", [
#         (0, (0x30, 0x12, 0x34), 0x12),
#         (0, (0x3F, 0xED, 0xCB), 0xED),
#         (1, (0x3F, 0x3B, 0x3A, 0x39, 0x38, 0x37, 0x36, 0x35), 0x3A),
#         (1, [0x33, 0x34] + list(range(62)), 0),
#     ])
#     def test_block_size__flow_control_cts(self, ai_bytes_number, raw_frame_data, expected_block_size):
#         self.mock_can_packet.packet_type = CanPacketType.FLOW_CONTROL
#         self.mock_can_packet.flow_status = CanFlowStatus.ContinueToSend
#         self.mock_can_packet.raw_frame_data = raw_frame_data
#         self.mock_get_data_bytes_used_by_can_addressing_format.return_value = ai_bytes_number
#         assert CanPacket.block_size.fget(self=self.mock_can_packet) == expected_block_size
#         self.mock_get_data_bytes_used_by_can_addressing_format.assert_called_once_with(
#             self.mock_can_packet.addressing_format)
#
#     # stmin
#
#     @pytest.mark.parametrize("packet_type", [None, CanPacketType.CONSECUTIVE_FRAME, CanPacketType.FIRST_FRAME,
#                                              CanPacketType.SINGLE_FRAME, "something new"])
#     def test_stmin__none(self, packet_type):
#         self.mock_can_packet.packet_type = packet_type
#         assert CanPacket.stmin.fget(self=self.mock_can_packet) is None
#
#     @pytest.mark.parametrize("flow_status", [CanFlowStatus.Wait.value, CanFlowStatus.Overflow.value, "something", None])
#     def test_stmin__flow_control_not_cts(self, flow_status):
#         self.mock_can_packet.packet_type = CanPacketType.FLOW_CONTROL
#         self.mock_can_packet.flow_status = flow_status
#         assert CanPacket.stmin.fget(self=self.mock_can_packet) is None
#
#     @pytest.mark.parametrize("ai_bytes_number, raw_frame_data, expected_stmin", [
#         (0, (0x30, 0x12, 0x34), 0x34),
#         (0, (0x3F, 0xED, 0xCB), 0xCB),
#         (1, (0x3F, 0x3B, 0x3A, 0x39, 0x38, 0x37, 0x36, 0x35), 0x39),
#         (1, [0x33, 0x34] + list(range(62)), 1),
#     ])
#     def test_stmin__flow_control_cts(self, ai_bytes_number, raw_frame_data, expected_stmin):
#         self.mock_can_packet.packet_type = CanPacketType.FLOW_CONTROL
#         self.mock_can_packet.flow_status = CanFlowStatus.ContinueToSend
#         self.mock_can_packet.raw_frame_data = raw_frame_data
#         self.mock_get_data_bytes_used_by_can_addressing_format.return_value = ai_bytes_number
#         assert CanPacket.stmin.fget(self=self.mock_can_packet) == expected_stmin
#         self.mock_get_data_bytes_used_by_can_addressing_format.assert_called_once_with(
#             self.mock_can_packet.addressing_format)
#
#     # set_address_information
#
#     @pytest.mark.parametrize("addressing_format", [None, "unknown addressing format"])
#     @pytest.mark.parametrize("addressing, can_id, target_address, source_address, address_extension", [
#         ("something", "CAN ID", "TA", "SA", "AE"),
#         (AddressingType.PHYSICAL, 0x754, 0x31, 0xD0, 0xE3),
#     ])
#     @patch(f"{SCRIPT_LOCATION}.CanAddressingFormat")
#     def test_set_address_information__unknown_addressing_format(self, mock_can_addressing_format_class,
#                                                                 addressing_format, addressing, can_id,
#                                                                 target_address, source_address, address_extension):
#         mock_can_addressing_format_class.return_value = addressing_format
#         with pytest.raises(NotImplementedError):
#             CanPacket.set_address_information(self=self.mock_can_packet,
#                                               addressing=addressing,
#                                               addressing_format=addressing_format,
#                                               can_id=can_id,
#                                               target_address=target_address,
#                                               source_address=source_address,
#                                               address_extension=address_extension)
#         self.mock_can_packet.validate_address_information.assert_not_called()
#         mock_can_addressing_format_class.assert_called_once_with(addressing_format)
#
#     @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
#                                                    CanAddressingFormat.NORMAL_11BIT_ADDRESSING.value])
#     @pytest.mark.parametrize("addressing, can_id", [
#         ("something", "CAN ID"),
#         (AddressingType.PHYSICAL, 0x754),
#     ])
#     def test_set_address_information__normal_11_bit(self, addressing_format, addressing, can_id):
#         CanPacket.set_address_information(self=self.mock_can_packet,
#                                           addressing=addressing,
#                                           addressing_format=addressing_format,
#                                           can_id=can_id)
#         self.mock_can_packet.set_address_information_normal_11bit.assert_called_once_with(addressing=addressing,
#                                                                                           can_id=can_id)
#         self.mock_warn.assert_not_called()
#
#     @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
#                                                    CanAddressingFormat.NORMAL_11BIT_ADDRESSING.value])
#     @pytest.mark.parametrize("addressing, can_id, target_address, source_address, address_extension", [
#         ("something", "CAN ID", "TA", "SA", "AE"),
#         (AddressingType.PHYSICAL, 0x754, 0x31, 0xD0, 0xE3),
#     ])
#     def test_set_address_information__normal_11_bit_with_warn(self, addressing_format, addressing, can_id,
#                                                               target_address, source_address, address_extension):
#         CanPacket.set_address_information(self=self.mock_can_packet,
#                                           addressing=addressing,
#                                           addressing_format=addressing_format,
#                                           can_id=can_id,
#                                           target_address=target_address,
#                                           source_address=source_address,
#                                           address_extension=address_extension)
#         self.mock_can_packet.set_address_information_normal_11bit.assert_called_once_with(addressing=addressing,
#                                                                                           can_id=can_id)
#         self.mock_warn.assert_called_once()
#
#     @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
#                                                    CanAddressingFormat.NORMAL_FIXED_ADDRESSING.value])
#     @pytest.mark.parametrize("addressing, can_id, target_address, source_address", [
#         ("something", "CAN ID", "TA", "SA"),
#         (AddressingType.PHYSICAL, 0x754, 0x31, 0xD0),
#     ])
#     def test_set_address_information__normal_fixed(self, addressing_format, addressing, can_id,
#                                                    target_address, source_address, ):
#         CanPacket.set_address_information(self=self.mock_can_packet,
#                                           addressing=addressing,
#                                           addressing_format=addressing_format,
#                                           can_id=can_id,
#                                           target_address=target_address,
#                                           source_address=source_address)
#         self.mock_can_packet.set_address_information_normal_fixed.assert_called_once_with(addressing=addressing,
#                                                                                           can_id=can_id,
#                                                                                           target_address=target_address,
#                                                                                           source_address=source_address)
#         self.mock_warn.assert_not_called()
#
#     @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
#                                                    CanAddressingFormat.NORMAL_FIXED_ADDRESSING.value])
#     @pytest.mark.parametrize("addressing, can_id, target_address, source_address, address_extension", [
#         ("something", "CAN ID", "TA", "SA", "AE"),
#         (AddressingType.PHYSICAL, 0x754, 0x31, 0xD0, 0xE3),
#     ])
#     def test_set_address_information__normal_fixed_warn(self, addressing_format, addressing, can_id,
#                                                         target_address, source_address, address_extension):
#         CanPacket.set_address_information(self=self.mock_can_packet,
#                                           addressing=addressing,
#                                           addressing_format=addressing_format,
#                                           can_id=can_id,
#                                           target_address=target_address,
#                                           source_address=source_address,
#                                           address_extension=address_extension)
#         self.mock_can_packet.set_address_information_normal_fixed.assert_called_once_with(addressing=addressing,
#                                                                                           can_id=can_id,
#                                                                                           target_address=target_address,
#                                                                                           source_address=source_address)
#         self.mock_warn.assert_called_once()
#
#     @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.EXTENDED_ADDRESSING,
#                                                    CanAddressingFormat.EXTENDED_ADDRESSING.value])
#     @pytest.mark.parametrize("addressing, can_id, target_address", [
#         ("something", "CAN ID", "TA"),
#         (AddressingType.PHYSICAL, 0x754, 0x31),
#     ])
#     def test_set_address_information__extended(self, addressing_format, addressing, can_id, target_address):
#         CanPacket.set_address_information(self=self.mock_can_packet,
#                                           addressing=addressing,
#                                           addressing_format=addressing_format,
#                                           can_id=can_id,
#                                           target_address=target_address)
#         self.mock_can_packet.set_address_information_extended.assert_called_once_with(addressing=addressing,
#                                                                                       can_id=can_id,
#                                                                                       target_address=target_address)
#         self.mock_warn.assert_not_called()
#
#     @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.EXTENDED_ADDRESSING,
#                                                    CanAddressingFormat.EXTENDED_ADDRESSING.value])
#     @pytest.mark.parametrize("addressing, can_id, target_address, source_address, address_extension", [
#         ("something", "CAN ID", "TA", "SA", "AE"),
#         (AddressingType.PHYSICAL, 0x754, 0x31, 0xD0, 0xE3),
#     ])
#     def test_set_address_information__extended_warn(self, addressing_format, addressing, can_id,
#                                                     target_address, source_address, address_extension):
#         CanPacket.set_address_information(self=self.mock_can_packet,
#                                           addressing=addressing,
#                                           addressing_format=addressing_format,
#                                           can_id=can_id,
#                                           target_address=target_address,
#                                           source_address=source_address,
#                                           address_extension=address_extension)
#         self.mock_can_packet.set_address_information_extended.assert_called_once_with(addressing=addressing,
#                                                                                       can_id=can_id,
#                                                                                       target_address=target_address)
#         self.mock_warn.assert_called_once()
#
#     @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.MIXED_11BIT_ADDRESSING,
#                                                    CanAddressingFormat.MIXED_11BIT_ADDRESSING.value])
#     @pytest.mark.parametrize("addressing, can_id, address_extension", [
#         ("something", "CAN ID", "AE"),
#         (AddressingType.PHYSICAL, 0x754, 0xE3),
#     ])
#     def test_set_address_information__mixed_11bit(self, addressing_format, addressing, can_id, address_extension):
#         CanPacket.set_address_information(self=self.mock_can_packet,
#                                           addressing=addressing,
#                                           addressing_format=addressing_format,
#                                           can_id=can_id,
#                                           address_extension=address_extension)
#         self.mock_can_packet.set_address_information_mixed_11bit.assert_called_once_with(addressing=addressing,
#                                                                                          can_id=can_id,
#                                                                                          address_extension=address_extension)
#         self.mock_warn.assert_not_called()
#
#     @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.MIXED_11BIT_ADDRESSING,
#                                                    CanAddressingFormat.MIXED_11BIT_ADDRESSING.value])
#     @pytest.mark.parametrize("addressing, can_id, target_address, source_address, address_extension", [
#         ("something", "CAN ID", "TA", "SA", "AE"),
#         (AddressingType.PHYSICAL, 0x754, 0x31, 0xD0, 0xE3),
#     ])
#     def test_set_address_information__mixed_11bit_warn(self, addressing_format, addressing, can_id,
#                                                        target_address, source_address, address_extension):
#         CanPacket.set_address_information(self=self.mock_can_packet,
#                                           addressing=addressing,
#                                           addressing_format=addressing_format,
#                                           can_id=can_id,
#                                           target_address=target_address,
#                                           source_address=source_address,
#                                           address_extension=address_extension)
#         self.mock_can_packet.set_address_information_mixed_11bit.assert_called_once_with(addressing=addressing,
#                                                                                          can_id=can_id,
#                                                                                          address_extension=address_extension)
#         self.mock_warn.assert_called_once()
#
#     @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.MIXED_29BIT_ADDRESSING,
#                                                    CanAddressingFormat.MIXED_29BIT_ADDRESSING.value])
#     @pytest.mark.parametrize("addressing, can_id, target_address, source_address, address_extension", [
#         ("something", "CAN ID", "TA", "SA", "AE"),
#         (AddressingType.PHYSICAL, 0x754, 0x31, 0xD0, 0xE3),
#     ])
#     def test_set_address_information__mixed_29bit(self, addressing_format, addressing, can_id,
#                                                   target_address, source_address, address_extension):
#         CanPacket.set_address_information(self=self.mock_can_packet,
#                                           addressing=addressing,
#                                           addressing_format=addressing_format,
#                                           can_id=can_id,
#                                           target_address=target_address,
#                                           source_address=source_address,
#                                           address_extension=address_extension)
#         self.mock_can_packet.set_address_information_mixed_29bit.assert_called_once_with(addressing=addressing,
#                                                                                          can_id=can_id,
#                                                                                          target_address=target_address,
#                                                                                          source_address=source_address,
#                                                                                          address_extension=address_extension)
#         self.mock_warn.assert_not_called()
#
#     # set_packet_data
#
#     @pytest.mark.parametrize("packet_type", [None, "unknown"])
#     @pytest.mark.parametrize("dlc, filler_byte, kwargs", [
#         ("some dlc", "some filler", {"p1": "v1", "p2": "v2"}),
#         (8, 0x55, {}),
#     ])
#     @patch(f"{SCRIPT_LOCATION}.CanPacketType")
#     def test_set_packet_data__unknown_packet_type(self, mock_packet_type_class,
#                                                   packet_type, dlc, filler_byte, kwargs):
#         with pytest.raises(NotImplementedError):
#             CanPacket.set_packet_data(self=self.mock_can_packet,
#                                       packet_type=packet_type,
#                                       dlc=dlc,
#                                       filler_byte=filler_byte,
#                                       **kwargs)
#         mock_packet_type_class.validate_member.assert_called_once_with(packet_type)
#         mock_packet_type_class.assert_called_once_with(packet_type)
#
#     @pytest.mark.parametrize("packet_type", [CanPacketType.SINGLE_FRAME, CanPacketType.SINGLE_FRAME.value])
#     @pytest.mark.parametrize("dlc, filler_byte, kwargs", [
#         ("some dlc", "some filler", {"p1": "v1", "p2": "v2"}),
#         (8, 0x55, {}),
#     ])
#     def test_set_packet_data__single_frame(self, packet_type, dlc, filler_byte, kwargs):
#         CanPacket.set_packet_data(self=self.mock_can_packet,
#                                   packet_type=packet_type,
#                                   dlc=dlc,
#                                   filler_byte=filler_byte,
#                                   **kwargs)
#         self.mock_can_packet.set_single_frame_data.assert_called_once_with(dlc=dlc,
#                                                                            filler_byte=filler_byte,
#                                                                            **kwargs)
#         self.mock_validate_can_packet_type.assert_called_once_with(packet_type)
#
#     @pytest.mark.parametrize("packet_type", [CanPacketType.FIRST_FRAME, CanPacketType.FIRST_FRAME.value])
#     @pytest.mark.parametrize("dlc, filler_byte, kwargs", [
#         ("some dlc", "some filler", {"p1": "v1", "p2": "v2"}),
#         (8, 0x55, {}),
#     ])
#     def test_set_packet_data__first_frame(self, packet_type, dlc, filler_byte, kwargs):
#         CanPacket.set_packet_data(self=self.mock_can_packet,
#                                   packet_type=packet_type,
#                                   dlc=dlc,
#                                   filler_byte=filler_byte,
#                                   **kwargs)
#         self.mock_can_packet.set_first_frame_data.assert_called_once_with(dlc=dlc,
#                                                                           **kwargs)
#         self.mock_validate_can_packet_type.assert_called_once_with(packet_type)
#
#     @pytest.mark.parametrize("packet_type", [CanPacketType.CONSECUTIVE_FRAME, CanPacketType.CONSECUTIVE_FRAME.value])
#     @pytest.mark.parametrize("dlc, filler_byte, kwargs", [
#         ("some dlc", "some filler", {"p1": "v1", "p2": "v2"}),
#         (8, 0x55, {}),
#     ])
#     def test_set_packet_data__consecutive_frame(self, packet_type, dlc, filler_byte, kwargs):
#         CanPacket.set_packet_data(self=self.mock_can_packet,
#                                   packet_type=packet_type,
#                                   dlc=dlc,
#                                   filler_byte=filler_byte,
#                                   **kwargs)
#         self.mock_can_packet.set_consecutive_frame_data.assert_called_once_with(dlc=dlc,
#                                                                                 filler_byte=filler_byte,
#                                                                                 **kwargs)
#         self.mock_validate_can_packet_type.assert_called_once_with(packet_type)
#
#     @pytest.mark.parametrize("packet_type", [CanPacketType.FLOW_CONTROL, CanPacketType.FLOW_CONTROL.value])
#     @pytest.mark.parametrize("dlc, filler_byte, kwargs", [
#         ("some dlc", "some filler", {"p1": "v1", "p2": "v2"}),
#         (8, 0x55, {}),
#     ])
#     def test_set_packet_data__flow_control(self, packet_type, dlc, filler_byte, kwargs):
#         CanPacket.set_packet_data(self=self.mock_can_packet,
#                                   packet_type=packet_type,
#                                   dlc=dlc,
#                                   filler_byte=filler_byte,
#                                   **kwargs)
#         self.mock_can_packet.set_flow_control_data.assert_called_once_with(dlc=dlc,
#                                                                            filler_byte=filler_byte,
#                                                                            **kwargs)
#         self.mock_validate_can_packet_type.assert_called_once_with(packet_type)
#
#     # set_single_frame_data
#
#     @pytest.mark.parametrize("payload", [range(10), [0x50, 0xBC]])
#     def test_set_single_frame_data__mandatory_args(self, payload):
#         CanPacket.set_single_frame_data(self=self.mock_can_packet,
#                                         payload=payload)
#         self.mock_can_packet._CanPacket__validate_data_single_frame.assert_called_once_with(
#             addressing_format=self.mock_can_packet.addressing_format,
#             dlc=None,
#             payload=payload,
#             filler_byte=DEFAULT_FILLER_BYTE)
#         self.mock_can_packet.create_can_frame_data_single_frame.assert_called_once_with(
#             addressing_format=self.mock_can_packet.addressing_format,
#             payload=payload,
#             dlc=None,
#             filler_byte=DEFAULT_FILLER_BYTE,
#             target_address=self.mock_can_packet.target_address,
#             address_extension=self.mock_can_packet.address_extension)
#         self.mock_can_packet.get_can_frame_dlc_single_frame.assert_called_once_with(
#             addressing_format=self.mock_can_packet.addressing_format,
#             payload_length=len(payload))
#         assert self.mock_can_packet._CanPacket__dlc == self.mock_can_packet.get_can_frame_dlc_single_frame.return_value
#         assert self.mock_can_packet._CanPacket__packet_type == CanPacketType.SINGLE_FRAME
#         assert self.mock_can_packet._CanPacket__raw_frame_data == \
#                self.mock_can_packet.create_can_frame_data_single_frame.return_value
#
#     @pytest.mark.parametrize("payload", [range(10), [0x50, 0xBC]])
#     @pytest.mark.parametrize("dlc", [4, 8, 15])
#     @pytest.mark.parametrize("filler_byte", [0xAA, 0x55])
#     def test_set_single_frame_data__all_args(self, payload, dlc, filler_byte):
#         CanPacket.set_single_frame_data(self=self.mock_can_packet,
#                                         payload=payload,
#                                         dlc=dlc,
#                                         filler_byte=filler_byte)
#         self.mock_can_packet._CanPacket__validate_data_single_frame.assert_called_once_with(
#             addressing_format=self.mock_can_packet.addressing_format,
#             dlc=dlc,
#             payload=payload,
#             filler_byte=filler_byte)
#         self.mock_can_packet.create_can_frame_data_single_frame.assert_called_once_with(
#             addressing_format=self.mock_can_packet.addressing_format,
#             payload=payload,
#             dlc=dlc,
#             filler_byte=filler_byte,
#             target_address=self.mock_can_packet.target_address,
#             address_extension=self.mock_can_packet.address_extension)
#         self.mock_can_packet.get_can_frame_dlc_single_frame.assert_not_called()
#         assert self.mock_can_packet._CanPacket__dlc == dlc
#         assert self.mock_can_packet._CanPacket__packet_type == CanPacketType.SINGLE_FRAME
#         assert self.mock_can_packet._CanPacket__raw_frame_data == \
#                self.mock_can_packet.create_can_frame_data_single_frame.return_value
#
#     # set_first_frame_data
#
#     @pytest.mark.parametrize("payload", [range(10), [0x50, 0xBC]])
#     @pytest.mark.parametrize("data_length", [0xF1, 0xFEBCA, 13])
#     @pytest.mark.parametrize("dlc", [8, 15])
#     def test_set_first_frame_data(self, payload, data_length, dlc):
#         CanPacket.set_first_frame_data(self=self.mock_can_packet,
#                                        payload=payload,
#                                        data_length=data_length,
#                                        dlc=dlc)
#         self.mock_can_packet._CanPacket__validate_data_first_frame.assert_called_once_with(
#             addressing_format=self.mock_can_packet.addressing_format,
#             dlc=dlc,
#             payload=payload,
#             data_length=data_length)
#         self.mock_can_packet.create_can_frame_data_first_frame.assert_called_once_with(
#             addressing_format=self.mock_can_packet.addressing_format,
#             target_address=self.mock_can_packet.target_address,
#             address_extension=self.mock_can_packet.address_extension,
#             payload=payload,
#             dlc=dlc,
#             data_length=data_length)
#         assert self.mock_can_packet._CanPacket__dlc == dlc
#         assert self.mock_can_packet._CanPacket__packet_type == CanPacketType.FIRST_FRAME
#         assert self.mock_can_packet._CanPacket__raw_frame_data == \
#                self.mock_can_packet.create_can_frame_data_first_frame.return_value
#
#     # set_consecutive_frame_data
#
#     @pytest.mark.parametrize("payload", [range(10), [0x50, 0xBC]])
#     @pytest.mark.parametrize("sequence_number", [0, 5, 15])
#     def test_set_consecutive_frame_data__mandatory_args(self, payload, sequence_number):
#         CanPacket.set_consecutive_frame_data(self=self.mock_can_packet,
#                                              payload=payload,
#                                              sequence_number=sequence_number)
#         self.mock_can_packet._CanPacket__validate_data_consecutive_frame.assert_called_once_with(
#             addressing_format=self.mock_can_packet.addressing_format,
#             dlc=None,
#             payload=payload,
#             sequence_number=sequence_number,
#             filler_byte=DEFAULT_FILLER_BYTE)
#         self.mock_can_packet.create_can_frame_data_consecutive_frame.assert_called_once_with(
#             addressing_format=self.mock_can_packet.addressing_format,
#             target_address=self.mock_can_packet.target_address,
#             address_extension=self.mock_can_packet.address_extension,
#             payload=payload,
#             sequence_number=sequence_number,
#             dlc=None,
#             filler_byte=DEFAULT_FILLER_BYTE)
#         self.mock_can_packet.get_can_frame_dlc_consecutive_frame.assert_called_once_with(
#             addressing_format=self.mock_can_packet.addressing_format,
#             payload_length=len(payload))
#         assert self.mock_can_packet._CanPacket__dlc == \
#                self.mock_can_packet.get_can_frame_dlc_consecutive_frame.return_value
#         assert self.mock_can_packet._CanPacket__packet_type == CanPacketType.CONSECUTIVE_FRAME
#         assert self.mock_can_packet._CanPacket__raw_frame_data == \
#                self.mock_can_packet.create_can_frame_data_consecutive_frame.return_value
#
#     @pytest.mark.parametrize("payload, sequence_number", [
#         (range(10), "some sequence number"),
#         ([0x10, 0xFE], 0x0),
#     ])
#     @pytest.mark.parametrize("dlc", [4, 8, 15])
#     @pytest.mark.parametrize("filler_byte", [0xAA, 0x55])
#     def test_set_consecutive_frame_data__all_args(self, payload, sequence_number, dlc, filler_byte):
#         CanPacket.set_consecutive_frame_data(self=self.mock_can_packet,
#                                              payload=payload,
#                                              sequence_number=sequence_number,
#                                              dlc=dlc,
#                                              filler_byte=filler_byte)
#         self.mock_can_packet._CanPacket__validate_data_consecutive_frame.assert_called_once_with(
#             addressing_format=self.mock_can_packet.addressing_format,
#             dlc=dlc,
#             payload=payload,
#             sequence_number=sequence_number,
#             filler_byte=filler_byte)
#         self.mock_can_packet.create_can_frame_data_consecutive_frame.assert_called_once_with(
#             addressing_format=self.mock_can_packet.addressing_format,
#             target_address=self.mock_can_packet.target_address,
#             address_extension=self.mock_can_packet.address_extension,
#             payload=payload,
#             sequence_number=sequence_number,
#             dlc=dlc,
#             filler_byte=filler_byte)
#         self.mock_can_packet.get_can_frame_dlc_consecutive_frame.assert_not_called()
#         assert self.mock_can_packet._CanPacket__dlc == dlc
#         assert self.mock_can_packet._CanPacket__packet_type == CanPacketType.CONSECUTIVE_FRAME
#         assert self.mock_can_packet._CanPacket__raw_frame_data == \
#                self.mock_can_packet.create_can_frame_data_consecutive_frame.return_value
#
#     # set_flow_control_data
#
#     @pytest.mark.parametrize("flow_status", ["som flow status", CanFlowStatus.Overflow])
#     def test_set_flow_control_data__mandatory_args(self, flow_status):
#         CanPacket.set_flow_control_data(self=self.mock_can_packet,
#                                         flow_status=flow_status)
#         self.mock_can_packet._CanPacket__validate_data_flow_control.assert_called_once_with(
#             addressing_format=self.mock_can_packet.addressing_format,
#             dlc=None,
#             flow_status=flow_status,
#             block_size=None,
#             stmin=None,
#             filler_byte=DEFAULT_FILLER_BYTE)
#         self.mock_can_packet.create_can_frame_data_flow_control.assert_called_once_with(
#             addressing_format=self.mock_can_packet.addressing_format,
#             target_address=self.mock_can_packet.target_address,
#             address_extension=self.mock_can_packet.address_extension,
#             flow_status=flow_status,
#             block_size=None,
#             stmin=None,
#             dlc=None,
#             filler_byte=DEFAULT_FILLER_BYTE)
#         self.mock_can_packet.get_can_frame_dlc_flow_control.assert_called_once_with(
#             addressing_format=self.mock_can_packet.addressing_format)
#         assert self.mock_can_packet._CanPacket__dlc == \
#                self.mock_can_packet.get_can_frame_dlc_flow_control.return_value
#         assert self.mock_can_packet._CanPacket__packet_type == CanPacketType.FLOW_CONTROL
#         assert self.mock_can_packet._CanPacket__raw_frame_data == \
#                self.mock_can_packet.create_can_frame_data_flow_control.return_value
#
#     @pytest.mark.parametrize("flow_status, block_size, stmin", [
#         (CanFlowStatus.ContinueToSend.value, 0x00, 0x7F),
#         ("some flow", "some block size", "some st min"),
#     ])
#     @pytest.mark.parametrize("dlc", [4, 8, 15])
#     @pytest.mark.parametrize("filler_byte", [0xAA, 0x55])
#     def test_set_flow_control_data__all_args(self, flow_status, block_size, stmin, dlc, filler_byte):
#         CanPacket.set_flow_control_data(self=self.mock_can_packet,
#                                         flow_status=flow_status,
#                                         block_size=block_size,
#                                         stmin=stmin,
#                                         dlc=dlc,
#                                         filler_byte=filler_byte)
#         self.mock_can_packet._CanPacket__validate_data_flow_control.assert_called_once_with(
#             addressing_format=self.mock_can_packet.addressing_format,
#             dlc=dlc,
#             flow_status=flow_status,
#             block_size=block_size,
#             stmin=stmin,
#             filler_byte=filler_byte)
#         self.mock_can_packet.create_can_frame_data_flow_control.assert_called_once_with(
#             addressing_format=self.mock_can_packet.addressing_format,
#             target_address=self.mock_can_packet.target_address,
#             address_extension=self.mock_can_packet.address_extension,
#             flow_status=flow_status,
#             block_size=block_size,
#             stmin=stmin,
#             dlc=dlc,
#             filler_byte=filler_byte)
#         self.mock_can_packet.get_can_frame_dlc_flow_control.assert_not_called()
#         assert self.mock_can_packet._CanPacket__dlc == dlc
#         assert self.mock_can_packet._CanPacket__packet_type == CanPacketType.FLOW_CONTROL
#         assert self.mock_can_packet._CanPacket__raw_frame_data == \
#                self.mock_can_packet.create_can_frame_data_flow_control.return_value
#
#     # set_address_information_normal_11bit
#
#     @pytest.mark.parametrize("addressing", ["some addressing", AddressingType.PHYSICAL])
#     @pytest.mark.parametrize("can_id", ["some CAN ID", 0x64A])
#     def test_set_address_information_normal_11bit(self, addressing, can_id):
#         CanPacket.set_address_information_normal_11bit(self=self.mock_can_packet,
#                                                        addressing=addressing,
#                                                        can_id=can_id)
#         self.mock_can_packet._CanPacket__validate_ai_normal_11bit.assert_called_once_with(addressing=addressing,
#                                                                                           can_id=can_id)
#         self.mock_can_packet._CanPacket__validate_unambiguous_ai_change.assert_called_once_with(
#             CanAddressingFormat.NORMAL_11BIT_ADDRESSING)
#         assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.NORMAL_11BIT_ADDRESSING
#         assert self.mock_can_packet._CanPacket__addressing == addressing
#         assert self.mock_can_packet._CanPacket__can_id == can_id
#         assert self.mock_can_packet._CanPacket__target_address is None
#         assert self.mock_can_packet._CanPacket__address_extension is None
#
#     # set_address_information_normal_fixed
#
#     @pytest.mark.parametrize("addressing", ["some addressing", AddressingType.PHYSICAL])
#     @pytest.mark.parametrize("can_id", ["some CAN ID", 0x64A])
#     @patch(f"{SCRIPT_LOCATION}.CanIdHandler.decode_normal_fixed_addressed_can_id")
#     @patch(f"{SCRIPT_LOCATION}.CanIdHandler.get_normal_fixed_addressed_can_id")
#     def test_set_address_information_normal_fixed__can_id(self, mock_get_normal_fixed_addressed_can_id,
#                                                           mock_decode_normal_fixed_addressed_can_id,
#                                                           addressing, can_id):
#         mock_decode_normal_fixed_addressed_can_id.return_value = ["addressing", "ta", "sa"]
#         CanPacket.set_address_information_normal_fixed(self=self.mock_can_packet,
#                                                        addressing=addressing,
#                                                        can_id=can_id)
#         self.mock_can_packet._CanPacket__validate_ai_normal_fixed.assert_called_once_with(addressing=addressing,
#                                                                                           can_id=can_id,
#                                                                                           target_address=None,
#                                                                                           source_address=None)
#         self.mock_can_packet._CanPacket__validate_unambiguous_ai_change.assert_called_once_with(
#             CanAddressingFormat.NORMAL_FIXED_ADDRESSING)
#         mock_get_normal_fixed_addressed_can_id.assert_not_called()
#         mock_decode_normal_fixed_addressed_can_id.assert_called_once_with(can_id)
#         assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.NORMAL_FIXED_ADDRESSING
#         assert self.mock_can_packet._CanPacket__addressing == addressing
#         assert self.mock_can_packet._CanPacket__can_id == can_id
#         assert self.mock_can_packet._CanPacket__target_address == mock_decode_normal_fixed_addressed_can_id.return_value[1]
#         assert self.mock_can_packet._CanPacket__address_extension is None
#
#     @pytest.mark.parametrize("addressing", ["some addressing", AddressingType.PHYSICAL])
#     @pytest.mark.parametrize("target_address, source_address", [
#         ("TA", "SA"),
#         (0x00, 0xFF),
#     ])
#     @pytest.mark.parametrize("can_id", ["some CAN ID", 0x64A])
#     @patch(f"{SCRIPT_LOCATION}.CanIdHandler.decode_normal_fixed_addressed_can_id")
#     @patch(f"{SCRIPT_LOCATION}.CanIdHandler.get_normal_fixed_addressed_can_id")
#     def test_set_address_information_normal_fixed__ta_sa(self, mock_get_normal_fixed_addressed_can_id,
#                                                          mock_decode_normal_fixed_addressed_can_id,
#                                                          addressing, target_address, source_address, can_id):
#         CanPacket.set_address_information_normal_fixed(self=self.mock_can_packet,
#                                                        addressing=addressing,
#                                                        target_address=target_address,
#                                                        source_address=source_address)
#         self.mock_can_packet._CanPacket__validate_ai_normal_fixed.assert_called_once_with(addressing=addressing,
#                                                                                           can_id=None,
#                                                                                           target_address=target_address,
#                                                                                           source_address=source_address)
#         self.mock_can_packet._CanPacket__validate_unambiguous_ai_change.assert_called_once_with(
#             CanAddressingFormat.NORMAL_FIXED_ADDRESSING)
#         mock_get_normal_fixed_addressed_can_id.assert_called_once_with(addressing_type=addressing,
#                                                                        target_address=target_address,
#                                                                        source_address=source_address)
#         mock_decode_normal_fixed_addressed_can_id.assert_not_called()
#         assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.NORMAL_FIXED_ADDRESSING
#         assert self.mock_can_packet._CanPacket__addressing == addressing
#         assert self.mock_can_packet._CanPacket__can_id == mock_get_normal_fixed_addressed_can_id.return_value
#         assert self.mock_can_packet._CanPacket__target_address == target_address
#         assert self.mock_can_packet._CanPacket__address_extension is None
#
#     # set_address_information_extended
#
#     @pytest.mark.parametrize("addressing", ["some addressing", AddressingType.PHYSICAL])
#     @pytest.mark.parametrize("can_id", ["some CAN ID", 0x64A])
#     @pytest.mark.parametrize("target_address", ["some ta", 0x5F])
#     def test_set_address_information_extended(self, addressing, can_id, target_address):
#         CanPacket.set_address_information_extended(self=self.mock_can_packet,
#                                                    addressing=addressing,
#                                                    can_id=can_id,
#                                                    target_address=target_address)
#         self.mock_can_packet._CanPacket__validate_ai_extended.assert_called_once_with(addressing=addressing,
#                                                                                       can_id=can_id,
#                                                                                       target_address=target_address)
#         self.mock_can_packet._CanPacket__validate_unambiguous_ai_change.assert_called_once_with(
#             CanAddressingFormat.EXTENDED_ADDRESSING)
#         assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.EXTENDED_ADDRESSING
#         assert self.mock_can_packet._CanPacket__addressing == addressing
#         assert self.mock_can_packet._CanPacket__can_id == can_id
#         assert self.mock_can_packet._CanPacket__target_address == target_address
#         assert self.mock_can_packet._CanPacket__address_extension is None
#
#     # set_address_information_mixed_11bit
#
#     @pytest.mark.parametrize("addressing", ["some addressing", AddressingType.PHYSICAL])
#     @pytest.mark.parametrize("can_id", ["some CAN ID", 0x64A])
#     @pytest.mark.parametrize("address_extension", ["some ae", 0x5F])
#     def test_set_address_information_mixed_11bit(self, addressing, can_id, address_extension):
#         CanPacket.set_address_information_mixed_11bit(self=self.mock_can_packet,
#                                                       addressing=addressing,
#                                                       can_id=can_id,
#                                                       address_extension=address_extension)
#         self.mock_can_packet._CanPacket__validate_ai_mixed_11bit.assert_called_once_with(addressing=addressing,
#                                                                                          can_id=can_id,
#                                                                                          address_extension=address_extension)
#         self.mock_can_packet._CanPacket__validate_unambiguous_ai_change.assert_called_once_with(
#             CanAddressingFormat.MIXED_11BIT_ADDRESSING)
#         assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.MIXED_11BIT_ADDRESSING
#         assert self.mock_can_packet._CanPacket__addressing == addressing
#         assert self.mock_can_packet._CanPacket__can_id == can_id
#         assert self.mock_can_packet._CanPacket__target_address is None
#         assert self.mock_can_packet._CanPacket__address_extension == address_extension
#
#     # set_address_information_mixed_29bit
#
#     @pytest.mark.parametrize("addressing", ["some addressing", AddressingType.PHYSICAL])
#     @pytest.mark.parametrize("address_extension", ["some ae", 0x5F])
#     @pytest.mark.parametrize("can_id", ["some CAN ID", 0x64A])
#     @patch(f"{SCRIPT_LOCATION}.CanIdHandler.decode_mixed_addressed_29bit_can_id")
#     @patch(f"{SCRIPT_LOCATION}.CanIdHandler.get_mixed_addressed_29bit_can_id")
#     def test_set_address_information_mixed_29bit__can_id(self, mock_get_mixed_addressed_29bit_can_id,
#                                                          mock_decode_mixed_addressed_29bit_can_id,
#                                                          addressing, address_extension, can_id):
#         mock_decode_mixed_addressed_29bit_can_id.return_value = ["addressing", "ta", "sa"]
#         CanPacket.set_address_information_mixed_29bit(self=self.mock_can_packet,
#                                                       addressing=addressing,
#                                                       address_extension=address_extension,
#                                                       can_id=can_id)
#         self.mock_can_packet._CanPacket__validate_ai_mixed_29bit.assert_called_once_with(addressing=addressing,
#                                                                                          address_extension=address_extension,
#                                                                                          can_id=can_id,
#                                                                                          target_address=None,
#                                                                                          source_address=None)
#         self.mock_can_packet._CanPacket__validate_unambiguous_ai_change.assert_called_once_with(
#             CanAddressingFormat.MIXED_29BIT_ADDRESSING)
#         mock_get_mixed_addressed_29bit_can_id.assert_not_called()
#         mock_decode_mixed_addressed_29bit_can_id.assert_called_once_with(can_id)
#         assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.MIXED_29BIT_ADDRESSING
#         assert self.mock_can_packet._CanPacket__addressing == addressing
#         assert self.mock_can_packet._CanPacket__can_id == can_id
#         assert self.mock_can_packet._CanPacket__target_address == mock_decode_mixed_addressed_29bit_can_id.return_value[1]
#         assert self.mock_can_packet._CanPacket__address_extension == address_extension
#
#     @pytest.mark.parametrize("addressing", ["some addressing", AddressingType.PHYSICAL])
#     @pytest.mark.parametrize("target_address, source_address", [
#         ("TA", "SA"),
#         (0x00, 0xFF),
#     ])
#     @pytest.mark.parametrize("address_extension", ["some ae", 0x5F])
#     @pytest.mark.parametrize("can_id", ["some CAN ID", 0x64A])
#     @patch(f"{SCRIPT_LOCATION}.CanIdHandler.decode_mixed_addressed_29bit_can_id")
#     @patch(f"{SCRIPT_LOCATION}.CanIdHandler.get_mixed_addressed_29bit_can_id")
#     def test_set_address_information_mixed_29bit__ta_sa(self, mock_get_mixed_addressed_29bit_can_id,
#                                                         mock_decode_mixed_addressed_29bit_can_id,
#                                                         addressing, address_extension, target_address, source_address,
#                                                         can_id):
#         CanPacket.set_address_information_mixed_29bit(self=self.mock_can_packet,
#                                                       addressing=addressing,
#                                                       address_extension=address_extension,
#                                                       target_address=target_address,
#                                                       source_address=source_address)
#         self.mock_can_packet._CanPacket__validate_ai_mixed_29bit.assert_called_once_with(addressing=addressing,
#                                                                                          address_extension=address_extension,
#                                                                                          can_id=None,
#                                                                                          target_address=target_address,
#                                                                                          source_address=source_address)
#         self.mock_can_packet._CanPacket__validate_unambiguous_ai_change.assert_called_once_with(
#             CanAddressingFormat.MIXED_29BIT_ADDRESSING)
#         mock_get_mixed_addressed_29bit_can_id.assert_called_once_with(addressing_type=addressing,
#                                                                       target_address=target_address,
#                                                                       source_address=source_address)
#         mock_decode_mixed_addressed_29bit_can_id.assert_not_called()
#         assert self.mock_can_packet._CanPacket__addressing_format == CanAddressingFormat.MIXED_29BIT_ADDRESSING
#         assert self.mock_can_packet._CanPacket__addressing == addressing
#         assert self.mock_can_packet._CanPacket__can_id == mock_get_mixed_addressed_29bit_can_id.return_value
#         assert self.mock_can_packet._CanPacket__target_address == target_address
#         assert self.mock_can_packet._CanPacket__address_extension == address_extension
#
#
#
#
#
#     # # __validate_data
#     #
#     # @pytest.mark.parametrize("dlc", [5.5, 8, "something"])
#     # @pytest.mark.parametrize("packet_type", [0, CanPacketType.FLOW_CONTROL, "some type"])
#     # @pytest.mark.parametrize("filler_byte", [0xFF, "some value"])
#     # @pytest.mark.parametrize("kwargs", [{}, {"a": "some a value", "b": "some b value"}])
#     # def test_validate_data__dlc_int(self, packet_type, filler_byte, dlc, kwargs):
#     #     CanPacket._CanPacket__validate_data(self=self.mock_can_packet,
#     #                                         packet_type=packet_type,
#     #                                         dlc=dlc,
#     #                                         filler_byte=filler_byte,
#     #                                         **kwargs)
#     #     self.mock_validate_dlc.assert_called_once_with(dlc)
#     #     self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
#     #     self.mock_validate_can_packet_type.assert_called_once_with(packet_type)
#     #     self.mock_can_packet._CanPacket__validate_data_consistency.assert_called_once_with(packet_type=packet_type,
#     #                                                                                        dlc=dlc,
#     #                                                                                        **kwargs)
#     #
#     # @pytest.mark.parametrize("packet_type", [0, CanPacketType.FLOW_CONTROL, "some type"])
#     # @pytest.mark.parametrize("filler_byte", [0xFF, "some value"])
#     # @pytest.mark.parametrize("kwargs", [{}, {"a": "some a value", "b": "some b value"}])
#     # def test_validate_data__dlc_none(self, packet_type, filler_byte, kwargs):
#     #     CanPacket._CanPacket__validate_data(self=self.mock_can_packet,
#     #                                         packet_type=packet_type,
#     #                                         dlc=None,
#     #                                         filler_byte=filler_byte,
#     #                                         **kwargs)
#     #     self.mock_validate_dlc.assert_not_called()
#     #     self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
#     #     self.mock_validate_can_packet_type.assert_called_once_with(packet_type)
#     #     self.mock_can_packet._CanPacket__validate_data_consistency.assert_called_once_with(packet_type=packet_type,
#     #                                                                                        dlc=None,
#     #                                                                                        **kwargs)
#     #
#     # # __validate_ai_consistency
#     #
#     # @pytest.mark.parametrize("addressing_format", [None, "some unknown addressing format"])
#     # @pytest.mark.parametrize("addressing, can_id, target_address, source_address, address_extension", [
#     #     (None, None, None, None, None),
#     #     (AddressingType.PHYSICAL, 0x7FF, None, None, None),
#     #     (AddressingType.FUNCTIONAL, 0x18091232, 0x98, 0xB1, 0xC0),
#     # ])
#     # @patch(f"{SCRIPT_LOCATION}.CanAddressingFormat")
#     # def test_validate_ai_consistency__unknown_addressing_format(self, mock_can_addressing_format_class,
#     #                                                             addressing_format, addressing, can_id,
#     #                                                             target_address, source_address, address_extension):
#     #     mock_can_addressing_format_class.return_value = addressing_format
#     #     with pytest.raises(NotImplementedError):
#     #         CanPacket._CanPacket__validate_ai_consistency(addressing=addressing,
#     #                                                       addressing_format=addressing_format,
#     #                                                       can_id=can_id,
#     #                                                       target_address=target_address,
#     #                                                       source_address=source_address,
#     #                                                       address_extension=address_extension)
#     #     mock_can_addressing_format_class.assert_called_once_with(addressing_format)
#     #
#     # @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
#     #                                                CanAddressingFormat.NORMAL_11BIT_ADDRESSING.value])
#     # @pytest.mark.parametrize("can_id, target_address, source_address, address_extension", [
#     #     (None, None, None, None),
#     #     (0x7FF, None, None, 0x97),
#     #     (0x612, 0x54, 0xAA, None),
#     #     (0x18091232, 0x98, 0xB1, 0xC0),
#     # ])
#     # @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_ai_consistency_normal_11bit")
#     # def test_validate_ai_consistency__normal_11bit(self, mock_validate_ai_consistency_normal_11bit,
#     #                                                addressing_format, example_addressing_type, can_id,
#     #                                                target_address, source_address, address_extension):
#     #     CanPacket._CanPacket__validate_ai_consistency(addressing=example_addressing_type,
#     #                                                   addressing_format=addressing_format,
#     #                                                   can_id=can_id,
#     #                                                   target_address=target_address,
#     #                                                   source_address=source_address,
#     #                                                   address_extension=address_extension)
#     #     mock_validate_ai_consistency_normal_11bit.assert_called_once_with(can_id=can_id,
#     #                                                                       target_address=target_address,
#     #                                                                       source_address=source_address,
#     #                                                                       address_extension=address_extension)
#     #
#     # @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
#     #                                                CanAddressingFormat.NORMAL_FIXED_ADDRESSING.value])
#     # @pytest.mark.parametrize("can_id, target_address, source_address, address_extension", [
#     #     (None, None, None, None),
#     #     (0x7FF, None, None, 0x97),
#     #     (0x612, 0x54, 0xAA, None),
#     #     (0x18091232, 0x98, 0xB1, 0xC0),
#     # ])
#     # @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_ai_consistency_normal_fixed")
#     # def test_validate_ai_consistency__normal_fixed(self, mock_validate_ai_consistency_normal_fixed,
#     #                                                addressing_format, example_addressing_type, can_id,
#     #                                                target_address, source_address, address_extension):
#     #     CanPacket._CanPacket__validate_ai_consistency(addressing=example_addressing_type,
#     #                                                   addressing_format=addressing_format,
#     #                                                   can_id=can_id,
#     #                                                   target_address=target_address,
#     #                                                   source_address=source_address,
#     #                                                   address_extension=address_extension)
#     #     mock_validate_ai_consistency_normal_fixed.assert_called_once_with(addressing=example_addressing_type,
#     #                                                                       can_id=can_id,
#     #                                                                       target_address=target_address,
#     #                                                                       source_address=source_address,
#     #                                                                       address_extension=address_extension)
#     #
#     # @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.EXTENDED_ADDRESSING,
#     #                                                CanAddressingFormat.EXTENDED_ADDRESSING.value])
#     # @pytest.mark.parametrize("can_id, target_address, source_address, address_extension", [
#     #     (None, None, None, None),
#     #     (0x7FF, None, None, 0x97),
#     #     (0x612, 0x54, 0xAA, None),
#     #     (0x18091232, 0x98, 0xB1, 0xC0),
#     # ])
#     # @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_ai_consistency_extended")
#     # def test_validate_ai_consistency__extended(self, mock_validate_ai_consistency_extended,
#     #                                            addressing_format, example_addressing_type, can_id,
#     #                                            target_address, source_address, address_extension):
#     #     CanPacket._CanPacket__validate_ai_consistency(addressing=example_addressing_type,
#     #                                                   addressing_format=addressing_format,
#     #                                                   can_id=can_id,
#     #                                                   target_address=target_address,
#     #                                                   source_address=source_address,
#     #                                                   address_extension=address_extension)
#     #     mock_validate_ai_consistency_extended.assert_called_once_with(can_id=can_id,
#     #                                                                   target_address=target_address,
#     #                                                                   source_address=source_address,
#     #                                                                   address_extension=address_extension)
#     #
#     # @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.MIXED_11BIT_ADDRESSING,
#     #                                                CanAddressingFormat.MIXED_11BIT_ADDRESSING.value])
#     # @pytest.mark.parametrize("can_id, target_address, source_address, address_extension", [
#     #     (None, None, None, None),
#     #     (0x7FF, None, None, 0x97),
#     #     (0x612, 0x54, 0xAA, None),
#     #     (0x18091232, 0x98, 0xB1, 0xC0),
#     # ])
#     # @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_ai_consistency_mixed_11bit")
#     # def test_validate_ai_consistency__mixed_11bit(self, mock_validate_ai_consistency_mixed_11bit,
#     #                                               addressing_format, example_addressing_type, can_id,
#     #                                               target_address, source_address, address_extension):
#     #     CanPacket._CanPacket__validate_ai_consistency(addressing=example_addressing_type,
#     #                                                   addressing_format=addressing_format,
#     #                                                   can_id=can_id,
#     #                                                   target_address=target_address,
#     #                                                   source_address=source_address,
#     #                                                   address_extension=address_extension)
#     #     mock_validate_ai_consistency_mixed_11bit.assert_called_once_with(can_id=can_id,
#     #                                                                      target_address=target_address,
#     #                                                                      source_address=source_address,
#     #                                                                      address_extension=address_extension)
#     #
#     # @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.MIXED_29BIT_ADDRESSING,
#     #                                                CanAddressingFormat.MIXED_29BIT_ADDRESSING.value])
#     # @pytest.mark.parametrize("can_id, target_address, source_address, address_extension", [
#     #     (None, None, None, None),
#     #     (0x7FF, None, None, 0x97),
#     #     (0x612, 0x54, 0xAA, None),
#     #     (0x18091232, 0x98, 0xB1, 0xC0),
#     # ])
#     # @patch(f"{SCRIPT_LOCATION}.CanPacket._CanPacket__validate_ai_consistency_mixed_29bit")
#     # def test_validate_ai_consistency__mixed_29bit(self, mock_validate_ai_consistency_mixed_29bit,
#     #                                               addressing_format, example_addressing_type, can_id,
#     #                                               target_address, source_address, address_extension):
#     #     CanPacket._CanPacket__validate_ai_consistency(addressing=example_addressing_type,
#     #                                                   addressing_format=addressing_format,
#     #                                                   can_id=can_id,
#     #                                                   target_address=target_address,
#     #                                                   source_address=source_address,
#     #                                                   address_extension=address_extension)
#     #     mock_validate_ai_consistency_mixed_29bit.assert_called_once_with(addressing=example_addressing_type,
#     #                                                                      can_id=can_id,
#     #                                                                      target_address=target_address,
#     #                                                                      source_address=source_address,
#     #                                                                      address_extension=address_extension)
#     #
#     # __validate_ai_consistency_normal_11bit
#
#     @pytest.mark.parametrize("can_id", [0x1234, 0x98FA])
#     @pytest.mark.parametrize("target_address, source_address, address_extension", [
#         (0, 0, 0),
#         (0x05, None, None),
#         (None, 0xFB, None),
#         (None, None, 0x9C),
#     ])
#     @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_11bit_addressed_can_id")
#     def test_validate_ai_consistency_normal_11bit__unused_args(self, mock_is_normal_11bit_addressed_can_id,
#                                                                can_id, target_address, source_address,
#                                                                address_extension):
#         mock_is_normal_11bit_addressed_can_id.return_value = True
#         with pytest.raises(UnusedArgumentError):
#             CanPacket._CanPacket__validate_ai_consistency_normal_11bit(can_id=can_id,
#                                                                        target_address=target_address,
#                                                                        source_address=source_address,
#                                                                        address_extension=address_extension)
#
#     @pytest.mark.parametrize("can_id", [0x1234, 0x98FA])
#     @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_11bit_addressed_can_id")
#     def test_validate_ai_consistency_normal_11bit__invalid_can_id(self, mock_is_normal_11bit_addressed_can_id, can_id):
#         mock_is_normal_11bit_addressed_can_id.return_value = False
#         with pytest.raises(InconsistentArgumentsError):
#             CanPacket._CanPacket__validate_ai_consistency_normal_11bit(can_id=can_id,
#                                                                        target_address=None,
#                                                                        source_address=None,
#                                                                        address_extension=None)
#
#     @pytest.mark.parametrize("can_id", [0x1234, 0x98FA])
#     @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_11bit_addressed_can_id")
#     def test_validate_ai_consistency_normal_11bit__valid(self, mock_is_normal_11bit_addressed_can_id, can_id):
#         mock_is_normal_11bit_addressed_can_id.return_value = True
#         CanPacket._CanPacket__validate_ai_consistency_normal_11bit(can_id=can_id,
#                                                                    target_address=None,
#                                                                    source_address=None,
#                                                                    address_extension=None)
#
#     # __validate_ai_consistency_normal_fixed
#
#     @pytest.mark.parametrize("can_id, target_address, source_address", [
#         (0xABCDEF, None, None),
#         (None, 0x12, 0x98),
#     ])
#     @pytest.mark.parametrize("address_extension", [0x00, 0x55, 0xFF])
#     def test_validate_ai_consistency_normal_fixed__unused_args(self, example_addressing_type,
#                                                                can_id, target_address, source_address,
#                                                                address_extension):
#         with pytest.raises(UnusedArgumentError):
#             CanPacket._CanPacket__validate_ai_consistency_normal_fixed(addressing=example_addressing_type,
#                                                                        can_id=can_id,
#                                                                        target_address=target_address,
#                                                                        source_address=source_address,
#                                                                        address_extension=address_extension)
#
#     @pytest.mark.parametrize("can_id, target_address, source_address", [
#         (0xABCDEF, 0x09, None),
#         (0x727384, None, 0xB1),
#         (0xABCDEF, 0x9E, 0xFD),
#     ])
#     def test_validate_ai_consistency_normal_fixed__redundant_args(self, example_addressing_type,
#                                                                   can_id, target_address, source_address):
#         with pytest.raises(InconsistentArgumentsError):
#             CanPacket._CanPacket__validate_ai_consistency_normal_fixed(addressing=example_addressing_type,
#                                                                        can_id=can_id,
#                                                                        target_address=target_address,
#                                                                        source_address=source_address,
#                                                                        address_extension=None)
#
#     @pytest.mark.parametrize("can_id, target_address, source_address", [
#         (None, 0x09, None),
#         (None, None, 0xB1),
#         (None, None, None),
#     ])
#     def test_validate_ai_consistency_normal_fixed__missing_args(self, example_addressing_type,
#                                                                 can_id, target_address, source_address):
#         with pytest.raises(InconsistentArgumentsError):
#             CanPacket._CanPacket__validate_ai_consistency_normal_fixed(addressing=example_addressing_type,
#                                                                        can_id=can_id,
#                                                                        target_address=target_address,
#                                                                        source_address=source_address,
#                                                                        address_extension=None)
#
#     @pytest.mark.parametrize("target_address", [0x00, 0x55, 0xFF])
#     @pytest.mark.parametrize("source_address", [0x00, 0xAA, 0xFF])
#     def test_validate_ai_consistency_normal_fixed__byte_params_validation(self, example_addressing_type,
#                                                                           target_address, source_address):
#         CanPacket._CanPacket__validate_ai_consistency_normal_fixed(addressing=example_addressing_type,
#                                                                    can_id=None,
#                                                                    target_address=target_address,
#                                                                    source_address=source_address,
#                                                                    address_extension=None)
#         self.mock_validate_raw_byte.assert_has_calls([call(target_address), call(source_address)])
#
#     @pytest.mark.parametrize("can_id", [0, "some CAN ID", 0x12343])
#     @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_fixed_addressed_can_id")
#     def test_validate_ai_consistency_normal_fixed__invalid_can_id(self, mock_is_normal_fixed_addressed_can_id,
#                                                                   example_addressing_type, can_id):
#         mock_is_normal_fixed_addressed_can_id.return_value = False
#         with pytest.raises(InconsistentArgumentsError):
#             CanPacket._CanPacket__validate_ai_consistency_normal_fixed(addressing=example_addressing_type,
#                                                                        can_id=can_id,
#                                                                        target_address=None,
#                                                                        source_address=None,
#                                                                        address_extension=None)
#         self.mock_validate_can_id.assert_called_once_with(can_id)
#         mock_is_normal_fixed_addressed_can_id.assert_called_once_with(can_id=can_id,
#                                                                       addressing=example_addressing_type)
#
#     @pytest.mark.parametrize("can_id", [0, "some CAN ID", 0x12343])
#     @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_normal_fixed_addressed_can_id")
#     def test_validate_ai_consistency_normal_fixed__valid(self, mock_is_normal_fixed_addressed_can_id,
#                                                          example_addressing_type, can_id):
#         mock_is_normal_fixed_addressed_can_id.return_value = True
#         CanPacket._CanPacket__validate_ai_consistency_normal_fixed(addressing=example_addressing_type,
#                                                                    can_id=can_id,
#                                                                    target_address=None,
#                                                                    source_address=None,
#                                                                    address_extension=None)
#         self.mock_validate_can_id.assert_called_once_with(can_id)
#         mock_is_normal_fixed_addressed_can_id.assert_called_once_with(can_id=can_id,
#                                                                       addressing=example_addressing_type)
#     #
#     # # __validate_ai_consistency_extended
#     #
#     # @pytest.mark.parametrize("can_id, target_address", [
#     #     (0x8572, 0x1B),
#     #     (0xF09B, 0xC5),
#     # ])
#     # @pytest.mark.parametrize("source_address, address_extension", [
#     #     (0x01, None),
#     #     (None, 0xFC),
#     #     (0x0F, 0x7A),
#     # ])
#     # def test_validate_ai_consistency_extended__unused_args(self, can_id, target_address,
#     #                                                        source_address, address_extension):
#     #     with pytest.raises(UnusedArgumentError):
#     #         CanPacket._CanPacket__validate_ai_consistency_extended(can_id=can_id,
#     #                                                                target_address=target_address,
#     #                                                                source_address=source_address,
#     #                                                                address_extension=address_extension)
#     #
#     # @pytest.mark.parametrize("can_id", [0x0, 0x7A2, 0x19FAB3])
#     # @pytest.mark.parametrize("target_address", [0x00, 0x8F, 0xFF])
#     # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_extended_addressed_can_id")
#     # def test_validate_ai_consistency_extended__invalid_can_id(self, mock_is_extended_addressed_can_id,
#     #                                                           can_id, target_address):
#     #     mock_is_extended_addressed_can_id.return_value = False
#     #     with pytest.raises(InconsistentArgumentsError):
#     #         CanPacket._CanPacket__validate_ai_consistency_extended(can_id=can_id,
#     #                                                                target_address=target_address,
#     #                                                                source_address=None,
#     #                                                                address_extension=None)
#     #     self.mock_validate_can_id.assert_called_once_with(can_id)
#     #     mock_is_extended_addressed_can_id.assert_called_once_with(can_id)
#     #
#     # @pytest.mark.parametrize("can_id", [0x0, 0x7A2, 0x19FAB3])
#     # @pytest.mark.parametrize("target_address", [0x00, 0x8F, 0xFF])
#     # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_extended_addressed_can_id")
#     # def test_validate_ai_consistency_extended__valid(self, mock_is_extended_addressed_can_id, can_id, target_address):
#     #     mock_is_extended_addressed_can_id.return_value = True
#     #     CanPacket._CanPacket__validate_ai_consistency_extended(can_id=can_id,
#     #                                                            target_address=target_address,
#     #                                                            source_address=None,
#     #                                                            address_extension=None)
#     #     self.mock_validate_can_id.assert_called_once_with(can_id)
#     #     mock_is_extended_addressed_can_id.assert_called_once_with(can_id)
#     #     self.mock_validate_raw_byte.assert_called_once_with(target_address)
#     #
#     # # __validate_ai_consistency_mixed_11bit
#     #
#     # @pytest.mark.parametrize("can_id, address_extension", [
#     #     (0x8572, 0x1B),
#     #     (0xF09B, 0xC5),
#     # ])
#     # @pytest.mark.parametrize("target_address, source_address", [
#     #     (0x01, None),
#     #     (None, 0xFC),
#     #     (0x0F, 0x7A),
#     # ])
#     # def test_validate_ai_consistency_mixed_11bit__unused_args(self, can_id, target_address,
#     #                                                           source_address, address_extension):
#     #     with pytest.raises(UnusedArgumentError):
#     #         CanPacket._CanPacket__validate_ai_consistency_mixed_11bit(can_id=can_id,
#     #                                                                   target_address=target_address,
#     #                                                                   source_address=source_address,
#     #                                                                   address_extension=address_extension)
#     #
#     # @pytest.mark.parametrize("can_id", [0x0, 0x7A2, 0x19FAB3])
#     # @pytest.mark.parametrize("address_extension", [0x00, 0x8F, 0xFF])
#     # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_mixed_11bit_addressed_can_id")
#     # def test_validate_ai_consistency_mixed_11bit__invalid_can_id(self, mock_is_mixed_11bit_addressed_can_id,
#     #                                                              can_id, address_extension):
#     #     mock_is_mixed_11bit_addressed_can_id.return_value = False
#     #     with pytest.raises(InconsistentArgumentsError):
#     #         CanPacket._CanPacket__validate_ai_consistency_mixed_11bit(can_id=can_id,
#     #                                                                   target_address=None,
#     #                                                                   source_address=None,
#     #                                                                   address_extension=address_extension)
#     #     self.mock_validate_can_id.assert_called_once_with(can_id)
#     #     mock_is_mixed_11bit_addressed_can_id.assert_called_once_with(can_id)
#     #
#     # @pytest.mark.parametrize("can_id", [0x0, 0x7A2, 0x19FAB3])
#     # @pytest.mark.parametrize("address_extension", [0x00, 0x8F, 0xFF])
#     # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_mixed_11bit_addressed_can_id")
#     # def test_validate_ai_consistency_mixed_11bit__valid(self, mock_is_mixed_11bit_addressed_can_id,
#     #                                                     can_id, address_extension):
#     #     mock_is_mixed_11bit_addressed_can_id.return_value = True
#     #     CanPacket._CanPacket__validate_ai_consistency_mixed_11bit(can_id=can_id,
#     #                                                               target_address=None,
#     #                                                               source_address=None,
#     #                                                               address_extension=address_extension)
#     #     self.mock_validate_can_id.assert_called_once_with(can_id)
#     #     mock_is_mixed_11bit_addressed_can_id.assert_called_once_with(can_id)
#     #     self.mock_validate_raw_byte.assert_called_once_with(address_extension)
#     #
#     # # __validate_ai_consistency_mixed_29bit
#     #
#     # @pytest.mark.parametrize("can_id, target_address, source_address", [
#     #     (0xABCDEF, 0x09, None),
#     #     (0x727384, None, 0xB1),
#     #     (0xABCDEF, 0x9E, 0xFD),
#     # ])
#     # @pytest.mark.parametrize("address_extension", [0x00, 0x8F, 0xFF])
#     # def test_validate_ai_consistency_mixed_29bit__redundant_args(self, example_addressing_type, address_extension,
#     #                                                              can_id, target_address, source_address):
#     #     with pytest.raises(InconsistentArgumentsError):
#     #         CanPacket._CanPacket__validate_ai_consistency_mixed_29bit(addressing=example_addressing_type,
#     #                                                                   can_id=can_id,
#     #                                                                   target_address=target_address,
#     #                                                                   source_address=source_address,
#     #                                                                   address_extension=address_extension)
#     #
#     # @pytest.mark.parametrize("address_extension", [0x00, 0xFF])
#     # @pytest.mark.parametrize("can_id, target_address, source_address", [
#     #     (None, None, None),
#     #     (None, None, 0x2F),
#     #     (None, 0xBA, None),
#     # ])
#     # def test_validate_ai_consistency_mixed_29bit__missing_can_id_args(self, example_addressing_type, address_extension,
#     #                                                                   can_id, target_address, source_address):
#     #     with pytest.raises(InconsistentArgumentsError):
#     #         CanPacket._CanPacket__validate_ai_consistency_mixed_29bit(addressing=example_addressing_type,
#     #                                                                   can_id=can_id,
#     #                                                                   target_address=target_address,
#     #                                                                   source_address=source_address,
#     #                                                                   address_extension=address_extension)
#     #
#     # @pytest.mark.parametrize("target_address", [0x55, 0x82])
#     # @pytest.mark.parametrize("source_address", [0x0B, 0xAA])
#     # @pytest.mark.parametrize("address_extension", [0xB3, 0xE7])
#     # def test_validate_ai_consistency_mixed_29bit__byte_params_validation(self, example_addressing_type,
#     #                                                                      address_extension,
#     #                                                                      target_address, source_address):
#     #     CanPacket._CanPacket__validate_ai_consistency_mixed_29bit(addressing=example_addressing_type,
#     #                                                               can_id=None,
#     #                                                               target_address=target_address,
#     #                                                               source_address=source_address,
#     #                                                               address_extension=address_extension)
#     #     self.mock_validate_raw_byte.assert_has_calls([call(address_extension),
#     #                                                   call(target_address),
#     #                                                   call(source_address)],
#     #                                                  any_order=True)
#     #
#     # @pytest.mark.parametrize("can_id", [0, "some CAN ID", 0x12343])
#     # @pytest.mark.parametrize("address_extension", [0xB3, 0xE7])
#     # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_mixed_29bit_addressed_can_id")
#     # def test_validate_ai_consistency_mixed_29bit__invalid_can_id(self, mock_is_mixed_29bit_addressed_can_id,
#     #                                                              example_addressing_type, can_id, address_extension):
#     #     mock_is_mixed_29bit_addressed_can_id.return_value = False
#     #     with pytest.raises(InconsistentArgumentsError):
#     #         CanPacket._CanPacket__validate_ai_consistency_mixed_29bit(addressing=example_addressing_type,
#     #                                                                   can_id=can_id,
#     #                                                                   target_address=None,
#     #                                                                   source_address=None,
#     #                                                                   address_extension=address_extension)
#     #     self.mock_validate_can_id.assert_called_once_with(can_id)
#     #     mock_is_mixed_29bit_addressed_can_id.assert_called_once_with(can_id=can_id,
#     #                                                                  addressing=example_addressing_type)
#     #
#     # @pytest.mark.parametrize("can_id", [0, "some CAN ID", 0x12343])
#     # @pytest.mark.parametrize("address_extension", [0xB3, 0xE7])
#     # @patch(f"{SCRIPT_LOCATION}.CanIdHandler.is_mixed_29bit_addressed_can_id")
#     # def test_validate_ai_consistency_mixed_29bit__valid(self, mock_is_mixed_29bit_addressed_can_id,
#     #                                                     example_addressing_type, can_id, address_extension):
#     #     mock_is_mixed_29bit_addressed_can_id.return_value = True
#     #     CanPacket._CanPacket__validate_ai_consistency_mixed_29bit(addressing=example_addressing_type,
#     #                                                               can_id=can_id,
#     #                                                               target_address=None,
#     #                                                               source_address=None,
#     #                                                               address_extension=address_extension)
#     #     self.mock_validate_can_id.assert_called_once_with(can_id)
#     #     mock_is_mixed_29bit_addressed_can_id.assert_called_once_with(can_id=can_id,
#     #                                                                  addressing=example_addressing_type)
#     #
#     # # __validate_unambiguous_ai_change
#     #
#     # @pytest.mark.parametrize("new_addressing_format", list(CanAddressingFormat))
#     # def test_validate_unambiguous_ai_change__none(self, new_addressing_format):
#     #     self.mock_can_packet.addressing_format = None
#     #     CanPacket._CanPacket__validate_unambiguous_ai_change(self=self.mock_can_packet,
#     #                                                          addressing_format=new_addressing_format)
#     #     self.mock_get_data_bytes_used_by_can_addressing_format.assert_not_called()
#     #
#     # @pytest.mark.parametrize("data_bytes_used", [0, 1])
#     # @pytest.mark.parametrize("new_addressing_format", ["value 1", "value 2"])
#     # @pytest.mark.parametrize("old_addressing_format", ["other 1", "other 2"])
#     # def test_validate_unambiguous_ai_change__compatible(self, new_addressing_format, old_addressing_format,
#     #                                                     data_bytes_used):
#     #     self.mock_can_packet.addressing_format = old_addressing_format
#     #     self.mock_get_data_bytes_used_by_can_addressing_format.return_value = data_bytes_used
#     #     CanPacket._CanPacket__validate_unambiguous_ai_change(self=self.mock_can_packet,
#     #                                                          addressing_format=new_addressing_format)
#     #     self.mock_get_data_bytes_used_by_can_addressing_format.assert_has_calls(
#     #         [call(new_addressing_format), call(old_addressing_format)], any_order=True)
#     #
#     # @pytest.mark.parametrize("data_bytes_used", [(0, 1), (1, 0)])
#     # @pytest.mark.parametrize("new_addressing_format", ["value 1", "value 2"])
#     # @pytest.mark.parametrize("old_addressing_format", ["other 1", "other 2"])
#     # def test_validate_unambiguous_ai_change__incompatible(self, new_addressing_format, old_addressing_format,
#     #                                                       data_bytes_used):
#     #     self.mock_can_packet.addressing_format = old_addressing_format
#     #     self.mock_get_data_bytes_used_by_can_addressing_format.side_effect = data_bytes_used
#     #     with pytest.raises(AmbiguityError):
#     #         CanPacket._CanPacket__validate_unambiguous_ai_change(self=self.mock_can_packet,
#     #                                                              addressing_format=new_addressing_format)
#     #     self.mock_get_data_bytes_used_by_can_addressing_format.assert_has_calls(
#     #         [call(new_addressing_format), call(old_addressing_format)], any_order=True)
#     #
#     # # __validate_data_consistency
#     #
#     # @pytest.mark.parametrize("packet_type", [None, "unknown packet type"])
#     # @pytest.mark.parametrize("dlc", [None, 8])
#     # @pytest.mark.parametrize("kwargs", [{}, {"a": "some a value", "b": "some b value"}])
#     # @patch(f"{SCRIPT_LOCATION}.CanPacketType")
#     # def test_validate_data_consistency__unknown_packet_type(self, mock_packet_type, packet_type, dlc, kwargs):
#     #     mock_packet_type.return_value = packet_type
#     #     with pytest.raises(NotImplementedError):
#     #         CanPacket._CanPacket__validate_data_consistency(self=self.mock_can_packet,
#     #                                                         packet_type=packet_type,
#     #                                                         dlc=dlc,
#     #                                                         **kwargs)
#     #     mock_packet_type.assert_called_once_with(packet_type)
#     #
#     # @pytest.mark.parametrize("packet_type", [CanPacketType.SINGLE_FRAME, CanPacketType.SINGLE_FRAME.value])
#     # @pytest.mark.parametrize("dlc", [None, 8])
#     # @pytest.mark.parametrize("kwargs", [{}, {"a": "some a value", "b": "some b value"}])
#     # def test_validate_data_consistency__single_frame(self, packet_type, dlc, kwargs):
#     #     with pytest.raises(NotImplementedError):
#     #         CanPacket._CanPacket__validate_data_consistency(self=self.mock_can_packet,
#     #                                                         packet_type=packet_type,
#     #                                                         dlc=dlc,
#     #                                                         **kwargs)
#     #     self.mock_can_packet._CanPacket__validate_data_single_frame.assert_called_once_with(dlc=dlc, **kwargs)
#     #
#     # @pytest.mark.parametrize("packet_type", [CanPacketType.FIRST_FRAME, CanPacketType.FIRST_FRAME.value])
#     # @pytest.mark.parametrize("dlc", [None, 8])
#     # @pytest.mark.parametrize("kwargs", [{}, {"a": "some a value", "b": "some b value"}])
#     # def test_validate_data_consistency__first_frame(self, packet_type, dlc, kwargs):
#     #     with pytest.raises(NotImplementedError):
#     #         CanPacket._CanPacket__validate_data_consistency(self=self.mock_can_packet,
#     #                                                         packet_type=packet_type,
#     #                                                         dlc=dlc,
#     #                                                         **kwargs)
#     #     self.mock_can_packet._CanPacket__validate_data_first_frame.assert_called_once_with(dlc=dlc, **kwargs)
#     #
#     # @pytest.mark.parametrize("packet_type", [CanPacketType.CONSECUTIVE_FRAME, CanPacketType.CONSECUTIVE_FRAME.value])
#     # @pytest.mark.parametrize("dlc", [None, 8])
#     # @pytest.mark.parametrize("kwargs", [{}, {"a": "some a value", "b": "some b value"}])
#     # def test_validate_data_consistency__consecutive_frame(self, packet_type, dlc, kwargs):
#     #     with pytest.raises(NotImplementedError):
#     #         CanPacket._CanPacket__validate_data_consistency(self=self.mock_can_packet,
#     #                                                         packet_type=packet_type,
#     #                                                         dlc=dlc,
#     #                                                         **kwargs)
#     #     self.mock_can_packet._CanPacket__validate_data_consecutive_frame.assert_called_once_with(dlc=dlc, **kwargs)
#     #
#     # @pytest.mark.parametrize("packet_type", [CanPacketType.FLOW_CONTROL, CanPacketType.FLOW_CONTROL.value])
#     # @pytest.mark.parametrize("dlc", [None, 8])
#     # @pytest.mark.parametrize("kwargs", [{}, {"a": "some a value", "b": "some b value"}])
#     # def test_validate_data_consistency__flow_control(self, packet_type, dlc, kwargs):
#     #     with pytest.raises(NotImplementedError):
#     #         CanPacket._CanPacket__validate_data_consistency(self=self.mock_can_packet,
#     #                                                         packet_type=packet_type,
#     #                                                         dlc=dlc,
#     #                                                         **kwargs)
#     #     self.mock_can_packet._CanPacket__validate_data_flow_control.assert_called_once_with(dlc=dlc, **kwargs)
#     #
#     # # __validate_data_single_frame
#     #
#     # @pytest.mark.parametrize("payload", [range(10), [0x55, 0xAA]])
#     # @pytest.mark.parametrize("required_dlc, dlc", [
#     #     (5, 5),
#     #     (13, 13),
#     #     (15, None),
#     #     (5, None),
#     #     (8, 10),
#     # ])
#     # def test_validate_data_single_frame__valid(self, dlc, payload, required_dlc):
#     #     self.mock_can_packet.get_single_frame_dlc.return_value = required_dlc
#     #     CanPacket._CanPacket__validate_data_single_frame(self=self.mock_can_packet,
#     #                                                      dlc=dlc,
#     #                                                      payload=payload)
#     #     self.mock_validate_raw_bytes.assert_called_once_with(payload)
#     #     self.mock_can_packet.get_single_frame_dlc.assert_called_once_with(
#     #         addressing_format=self.mock_can_packet.addressing_format,
#     #         payload_length=len(payload))
#     #
#     # @pytest.mark.parametrize("payload", [range(10), [0x55, 0xAA]])
#     # @pytest.mark.parametrize("required_dlc, dlc", [
#     #     (6, 5),
#     #     (14, 13),
#     #     (16, None),
#     #     (99, None),
#     #     (13, 10),
#     # ])
#     # def test_validate_data_single_frame__invalid(self, dlc, payload, required_dlc):
#     #     self.mock_can_packet.get_single_frame_dlc.return_value = required_dlc
#     #     with pytest.raises(InconsistentArgumentsError):
#     #         CanPacket._CanPacket__validate_data_single_frame(self=self.mock_can_packet,
#     #                                                          dlc=dlc,
#     #                                                          payload=payload)
#     #     self.mock_validate_raw_bytes.assert_called_once_with(payload)
#     #     self.mock_can_packet.get_single_frame_dlc.assert_called_once_with(
#     #         addressing_format=self.mock_can_packet.addressing_format,
#     #         payload_length=len(payload))
#     #
#     # # __validate_data_first_frame
#     #
#     # @pytest.mark.parametrize("payload", [range(10), [0x55, 0xAA]])
#     # @pytest.mark.parametrize("data_length", [0xFFFFFF, 0xB2C3])
#     # @pytest.mark.parametrize("required_dlc, dlc", [
#     #     (5, 5),
#     #     (13, 13),
#     #     (15, 15),
#     # ])
#     # def test_validate_data_first_frame__valid(self, dlc, payload, required_dlc, data_length):
#     #     self.mock_can_packet.get_first_frame_dlc.return_value = required_dlc
#     #     CanPacket._CanPacket__validate_data_first_frame(self=self.mock_can_packet,
#     #                                                     dlc=dlc,
#     #                                                     data_length=data_length,
#     #                                                     payload=payload)
#     #     self.mock_validate_raw_bytes.assert_called_once_with(payload)
#     #     self.mock_can_packet.get_first_frame_dlc.assert_called_once_with(
#     #         addressing_format=self.mock_can_packet.addressing_format,
#     #         data_length=data_length,
#     #         payload_length=len(payload))
#     #
#     # @pytest.mark.parametrize("payload", [range(10), [0x55, 0xAA]])
#     # @pytest.mark.parametrize("data_length", [0xFFFFFF, 0xB2C3])
#     # @pytest.mark.parametrize("required_dlc, dlc", [
#     #     (4, 5),
#     #     (6, 5),
#     #     (12, 13),
#     #     (15, 3),
#     # ])
#     # def test_validate_data_first_frame__invalid(self, dlc, payload, required_dlc, data_length):
#     #     self.mock_can_packet.get_first_frame_dlc.return_value = required_dlc
#     #     with pytest.raises(InconsistentArgumentsError):
#     #         CanPacket._CanPacket__validate_data_first_frame(self=self.mock_can_packet,
#     #                                                         dlc=dlc,
#     #                                                         data_length=data_length,
#     #                                                         payload=payload)
#     #     self.mock_validate_raw_bytes.assert_called_once_with(payload)
#     #     self.mock_can_packet.get_first_frame_dlc.assert_called_once_with(
#     #         addressing_format=self.mock_can_packet.addressing_format,
#     #         data_length=data_length,
#     #         payload_length=len(payload))
#     #
#     # # __validate_data_consecutive_frame
#     #
#     # @pytest.mark.parametrize("dlc", [None, 15])
#     # @pytest.mark.parametrize("payload", [range(10), [0x10, 0x20]])
#     # @pytest.mark.parametrize("sequence_number", [None, 5.5, "not a sequence number"])
#     # def test_validate_data_consecutive_frame__sequence_number_type_error(self, dlc, payload, sequence_number):
#     #     with pytest.raises(TypeError):
#     #         CanPacket._CanPacket__validate_data_consecutive_frame(self=self.mock_can_packet,
#     #                                                               dlc=dlc,
#     #                                                               payload=payload,
#     #                                                               sequence_number=sequence_number)
#     #
#     # @pytest.mark.parametrize("dlc", [None, 15])
#     # @pytest.mark.parametrize("payload", [range(10), [0x10, 0x20]])
#     # @pytest.mark.parametrize("sequence_number", [-5, -1, 0x10, 0xFF])
#     # def test_validate_data_consecutive_frame__sequence_number_value_error(self, dlc, payload, sequence_number):
#     #     with pytest.raises(ValueError):
#     #         CanPacket._CanPacket__validate_data_consecutive_frame(self=self.mock_can_packet,
#     #                                                               dlc=dlc,
#     #                                                               payload=payload,
#     #                                                               sequence_number=sequence_number)
#     #
#     # @pytest.mark.parametrize("payload", [range(10), [0x55, 0xAA]])
#     # @pytest.mark.parametrize("required_dlc, dlc", [
#     #     (15, 14),
#     #     (4, 3),
#     #     (9, 5),
#     # ])
#     # @pytest.mark.parametrize("sequence_number", [0, 5, 0xF])
#     # def test_validate_data_consecutive_frame__invalid(self, dlc, payload, required_dlc, sequence_number):
#     #     self.mock_can_packet.get_consecutive_frame_dlc.return_value = required_dlc
#     #     with pytest.raises(InconsistentArgumentsError):
#     #         CanPacket._CanPacket__validate_data_consecutive_frame(self=self.mock_can_packet,
#     #                                                               dlc=dlc,
#     #                                                               payload=payload,
#     #                                                               sequence_number=sequence_number)
#     #     self.mock_can_packet.get_consecutive_frame_dlc.assert_called_once_with(
#     #         addressing_format=self.mock_can_packet.addressing_format,
#     #         payload_length=len(payload))
#     #     self.mock_validate_raw_bytes.assert_called_once_with(payload)
#     #
#     # @pytest.mark.parametrize("payload", [range(10), [0x55, 0xAA]])
#     # @pytest.mark.parametrize("required_dlc, dlc", [
#     #     (15, 15),
#     #     (3, 3),
#     #     (3, 15),
#     #     (5, 5),
#     #     (5, 6),
#     # ])
#     # @pytest.mark.parametrize("sequence_number", [0, 5, 0xF])
#     # def test_validate_data_consecutive_frame__valid(self, dlc, payload, required_dlc, sequence_number):
#     #     self.mock_can_packet.get_consecutive_frame_dlc.return_value = required_dlc
#     #     CanPacket._CanPacket__validate_data_consecutive_frame(self=self.mock_can_packet,
#     #                                                           dlc=dlc,
#     #                                                           payload=payload,
#     #                                                           sequence_number=sequence_number)
#     #     self.mock_can_packet.get_consecutive_frame_dlc.assert_called_once_with(
#     #         addressing_format=self.mock_can_packet.addressing_format,
#     #         payload_length=len(payload))
#     #     self.mock_validate_raw_bytes.assert_called_once_with(payload)
#     #
#     # # __validate_data_flow_control
#     #
#     # @pytest.mark.parametrize("flow_status, block_size, stmin", [
#     #     (CanFlowStatus.ContinueToSend, 0, 0),
#     #     (CanFlowStatus.Overflow.value, None, None),
#     #     (CanFlowStatus.Wait, None, None),
#     # ])
#     # @pytest.mark.parametrize("dlc, min_dlc", [
#     #     (8, 8),
#     #     (8, 3),
#     #     (3, 3),
#     # ])
#     # def test_validate_data_flow_control__valid_dlc(self, dlc, min_dlc, flow_status, block_size, stmin):
#     #     self.mock_can_packet.get_flow_control_dlc.return_value = min_dlc
#     #     CanPacket._CanPacket__validate_data_flow_control(self=self.mock_can_packet,
#     #                                                      dlc=dlc,
#     #                                                      flow_status=flow_status,
#     #                                                      block_size=block_size,
#     #                                                      stmin=stmin)
#     #     self.mock_validate_dlc.assert_called_once_with(dlc)
#     #     self.mock_can_packet.get_flow_control_dlc.assert_called_once_with(
#     #         addressing_format=self.mock_can_packet.addressing_format)
#     #
#     # @pytest.mark.parametrize("flow_status, block_size, stmin", [
#     #     (CanFlowStatus.ContinueToSend, 0, 0),
#     #     (CanFlowStatus.Overflow.value, None, None),
#     #     (CanFlowStatus.Wait, None, None),
#     # ])
#     # @pytest.mark.parametrize("dlc, min_dlc", [
#     #     (8, 9),
#     #     (3, 4),
#     #     (2, 3),
#     # ])
#     # def test_validate_data_flow_control__invalid_dlc(self, dlc, min_dlc, flow_status, block_size, stmin):
#     #     self.mock_can_packet.get_flow_control_dlc.return_value = min_dlc
#     #     with pytest.raises(InconsistentArgumentsError):
#     #         CanPacket._CanPacket__validate_data_flow_control(self=self.mock_can_packet,
#     #                                                          dlc=dlc,
#     #                                                          flow_status=flow_status,
#     #                                                          block_size=block_size,
#     #                                                          stmin=stmin)
#     #     self.mock_validate_dlc.assert_called_once_with(dlc)
#     #     self.mock_can_packet.get_flow_control_dlc.assert_called_once_with(
#     #         addressing_format=self.mock_can_packet.addressing_format)
#     #
#     # @pytest.mark.parametrize("flow_status, block_size, stmin", [
#     #     (CanFlowStatus.ContinueToSend, 0, 0),
#     #     (CanFlowStatus.ContinueToSend.value, 0xFF, 0xFF),
#     #     (CanFlowStatus.ContinueToSend.value, 0x4B, 0x65),
#     # ])
#     # def test_validate_data_flow_control__valid_cts(self, flow_status, block_size, stmin):
#     #     CanPacket._CanPacket__validate_data_flow_control(self=self.mock_can_packet,
#     #                                                      dlc=None,
#     #                                                      flow_status=flow_status,
#     #                                                      block_size=block_size,
#     #                                                      stmin=stmin)
#     #     self.mock_validate_flow_status.assert_called_once_with(flow_status)
#     #     self.mock_validate_raw_byte.assert_has_calls([call(block_size), call(stmin)], any_order=True)
#     #
#     # @pytest.mark.parametrize("flow_status", [CanFlowStatus.Wait, CanFlowStatus.Wait.value, CanFlowStatus.Overflow])
#     # def test_validate_data_flow_control__valid_other_fs(self, flow_status):
#     #     CanPacket._CanPacket__validate_data_flow_control(self=self.mock_can_packet,
#     #                                                      dlc=None,
#     #                                                      flow_status=flow_status,
#     #                                                      block_size=None,
#     #                                                      stmin=None)
#     #     self.mock_validate_flow_status.assert_called_once_with(flow_status)
#     #     self.mock_validate_raw_byte.assert_not_called()
#     #
#     # @pytest.mark.parametrize("flow_status", [CanFlowStatus.Wait, CanFlowStatus.Overflow])
#     # @pytest.mark.parametrize("block_size, stmin", [
#     #     (None, 0x99),
#     #     (0xBA, None),
#     #     (0x00, 0x00),
#     # ])
#     # def test_validate_data_flow_control__invalid_other_fs(self, flow_status, block_size, stmin):
#     #     with pytest.raises(InconsistentArgumentsError):
#     #         CanPacket._CanPacket__validate_data_flow_control(self=self.mock_can_packet,
#     #                                                          dlc=None,
#     #                                                          flow_status=flow_status,
#     #                                                          block_size=block_size,
#     #                                                          stmin=stmin)
#     #     self.mock_validate_flow_status.assert_called_once_with(flow_status)
#     #     self.mock_validate_raw_byte.assert_not_called()
#     #
#     # # __validate_payload_length
#     #
#     # @pytest.mark.parametrize("payload_length", [None, 2., "not a payload length"])
#     # def test_validate_payload_length__type_error(self, payload_length):
#     #     with pytest.raises(TypeError):
#     #         CanPacket._CanPacket__validate_payload_length(payload_length)
#     #
#     # @pytest.mark.parametrize("payload_length", [-100, -1, 0])
#     # def test_validate_payload_length__value_error(self, payload_length):
#     #     with pytest.raises(ValueError):
#     #         CanPacket._CanPacket__validate_payload_length(payload_length)
#     #
#     # @pytest.mark.parametrize("payload_length", [1, 2, 32, 63])
#     # def test_validate_payload_length__valid(self, payload_length):
#     #     CanPacket._CanPacket__validate_payload_length(payload_length)
#     #
#     # # __validate_ff_dl
#     #
#     # @pytest.mark.parametrize("ff_dl", [None, 2., "not a payload length"])
#     # def test_validate_ff_dl__type_error(self, ff_dl):
#     #     with pytest.raises(TypeError):
#     #         CanPacket._CanPacket__validate_ff_dl(ff_dl)
#     #
#     # @pytest.mark.parametrize("ff_dl", [-100, -1, 0, CanPacket.MAX_LONG_FF_DL_VALUE + 1])
#     # def test_validate_ff_dl__value_error(self, ff_dl):
#     #     with pytest.raises(ValueError):
#     #         CanPacket._CanPacket__validate_ff_dl(ff_dl)
#     #
#     # @pytest.mark.parametrize("ff_dl", [5, 8, 32, 63, CanPacket.MAX_LONG_FF_DL_VALUE])
#     # def test_validate_ff_dl__valid(self, ff_dl):
#     #     CanPacket._CanPacket__validate_ff_dl(ff_dl)
#     #
#
#
#
# @pytest.mark.integration
# class TestCanPacketIntegration:
#     """Integration tests for `CanPacket` class."""
#
#     # TODO: tests for get_can_frame_dlc
#     # TODO: tests for create_can_frame_data
#     # TODO: tests for validate_address_information
#     # TODO: tests for CanPacket.__init__
#
#     # create_can_frame_data
#
#     @pytest.mark.parametrize("kwargs, expected_can_frame_data", [
#         # Single Frame
#         ({"packet_type": CanPacketType.SINGLE_FRAME,
#           "addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
#           "payload": (0xFF, ),
#           "dlc": 2},
#          (0x01, 0xFF)),
#         ({"packet_type": CanPacketType.SINGLE_FRAME,
#           "addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING.value,
#           "payload": [0xB4, 0xC2, 0xE8],
#           "dlc": 0xF,
#           "filler_byte": 0x67,
#           "target_address": 0xFE},
#          tuple([0x00, 0x03, 0xB4, 0xC2, 0xE8] + [0x67] * 59)),
#         ({"packet_type": CanPacketType.SINGLE_FRAME,
#           "addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
#           "payload": tuple(range(150, 212))},
#          tuple([0x00, 0x3E] + list(range(150, 212)))),
#         ({"packet_type": CanPacketType.SINGLE_FRAME,
#           "addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
#           "payload": list(range(1, 8))},
#          (0x07, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07)),
#         ({"packet_type": CanPacketType.SINGLE_FRAME,
#           "addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING.value,
#           "payload": tuple(range(100, 132)),
#           "target_address": 0xAF},
#          tuple([0xAF, 0x00, 0x20] + list(range(100, 132)) + [DEFAULT_FILLER_BYTE] * 13)),
#         ({"packet_type": CanPacketType.SINGLE_FRAME.value,
#           "addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING.value,
#           "payload": [0xF0, 0xE1, 0xD2],
#           "target_address": 0x00,
#           "address_extension": 0xCD},
#          (0xCD, 0x03, 0xF0, 0xE1, 0xD2)),
#         # First Frame
#         ({"packet_type": CanPacketType.FIRST_FRAME,
#           "addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
#           "payload": (0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54),
#           "dlc": 8,
#           "data_length": 0x175
#           }, (0x11, 0x75, 0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54)),
#         ({"packet_type": CanPacketType.FIRST_FRAME.value,
#           "addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING.value,
#           "payload": [0x67],
#           "dlc": 8,
#           "data_length": 0x380B21FC,
#           "address_extension": 0xA1
#           }, (0xA1, 0x10, 0x00, 0x38, 0x0B, 0x21, 0xFC, 0x67)),
#         ({"packet_type": CanPacketType.FIRST_FRAME,
#           "addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
#           "payload": list(range(120, 182)),
#           "dlc": 15,
#           "data_length": 0x987,
#           "target_address": 0x55,
#           }, tuple([0x19, 0x87] + list(range(120, 182)))),
#         # Consecutive Frame
#         ({"packet_type": CanPacketType.CONSECUTIVE_FRAME,
#           "addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
#           "payload": [0x9B],
#           "sequence_number": 0x1
#           }, (0x21, 0x9B)),
#         ({"packet_type": CanPacketType.CONSECUTIVE_FRAME.value,
#           "addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING.value,
#           "payload": [0x9B, 0x8C],
#           "dlc": 8,
#           "sequence_number": 0x0,
#           "target_address": 0x12,
#           "address_extension": 0x34,
#           }, (0x34, 0x20, 0x9B, 0x8C, 0xCC, 0xCC, 0xCC, 0xCC)),
#         ({"packet_type": CanPacketType.CONSECUTIVE_FRAME.value,
#           "addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING.value,
#           "payload": tuple(range(5, 35)),
#           "dlc": 0xE,
#           "sequence_number": 0xF,
#           "target_address": 0xFF,
#           "filler_byte": 0x54,
#           }, tuple([0xFF, 0x2F] + list(range(5, 35)) + [0x54] * 16)),
#         # Flow Control
#         ({"packet_type": CanPacketType.FLOW_CONTROL,
#           "addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
#           "flow_status": CanFlowStatus.ContinueToSend,
#           "block_size": 0x09,
#           "stmin": 0xAB,
#           "target_address": 0xFA},
#          (0x30, 0x09, 0xAB)),
#         ({"packet_type": CanPacketType.FLOW_CONTROL.value,
#           "addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING.value,
#           "flow_status": CanFlowStatus.Overflow.value},
#          (0x32, 0xCC, 0xCC)),
#         ({"packet_type": CanPacketType.FLOW_CONTROL.value,
#           "addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING.value,
#           "flow_status": CanFlowStatus.Overflow.value,
#           "dlc": 8,
#           "filler_byte": 0x66,
#           "address_extension": 0x9E},
#          (0x9E, 0x32, 0x66, 0x66, 0x66, 0x66, 0x66, 0x66)),
#     ])
#     def test_create_can_frame_data__valid(self, kwargs, expected_can_frame_data):
#         assert CanPacket.create_can_frame_data(**kwargs) == expected_can_frame_data
#
#     @pytest.mark.parametrize("kwargs", [
#         # Single Frame
#         {"packet_type": CanPacketType.SINGLE_FRAME,
#          "addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
#          "dlc": 8,
#          "payload": list(range(8))},
#         {"packet_type": CanPacketType.SINGLE_FRAME,
#          "addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
#          "dlc": 4,
#          "payload": [0x12, 0x34, 0x56],
#          "target_address": 0x01},
#         {"packet_type": CanPacketType.SINGLE_FRAME,
#          "addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
#          "payload": list(range(62)),
#          "address_extension": 0xFF},
#         {"packet_type": CanPacketType.SINGLE_FRAME,
#          "addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
#          "payload": [],
#          "address_extension": 0xFF},
#         # First Frame
#         {"packet_type": CanPacketType.FIRST_FRAME,
#          "addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
#          "dlc": 7,
#          "payload": list(range(5)),
#          "data_length": 0x123},
#         {"packet_type": CanPacketType.FIRST_FRAME,
#          "addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
#          "dlc": 8,
#          "payload": list(range(5)),
#          "data_length": 0x123},
#         {"packet_type": CanPacketType.FIRST_FRAME,
#          "addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
#          "dlc": 15,
#          "payload": list(range(58)),
#          "data_length": 0x1000,
#          "target_address": 0x01},
#         # Consecutive Frame
#         {"packet_type": CanPacketType.CONSECUTIVE_FRAME,
#          "addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
#          "payload": tuple(range(5, 52)),
#          "dlc": 0xE,
#          "sequence_number": 0xF,
#          "target_address": 0x66,
#          "filler_byte": 0x54},
#         {"packet_type": CanPacketType.CONSECUTIVE_FRAME,
#          "addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
#          "payload": [],
#          "sequence_number": 0xF,
#          "target_address": 0x04,
#          "address_extension": 0xB1,
#          "filler_byte": 0x66},
#         # Flow Control
#         {"packet_type": CanPacketType.FLOW_CONTROL,
#          "addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
#          "flow_status": CanFlowStatus.Overflow,
#          "dlc": 2},
#         {"packet_type": CanPacketType.FLOW_CONTROL,
#          "addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
#          "flow_status": CanFlowStatus.ContinueToSend,
#          "block_size": 0x09,
#          "stmin": 0xAB,
#          "dlc": 3,
#          "address_extension": 0xFA},
#     ])
#     def test_create_can_frame_data__invalid(self, kwargs):
#         with pytest.raises(ValueError):
#             CanPacket.create_can_frame_data(**kwargs)

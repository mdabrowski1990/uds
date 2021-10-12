import pytest

from mock import patch, Mock

from uds.packet.can_packet import CanPacketType, CanAddressingFormat, CanFlowStatus, CanSTminTranslator, CanPacket, \
    AddressingType
from uds.packet.abstract_packet import AbstractUdsPacketType
from uds.utilities import ValidatedEnum, NibbleEnum


class TestCanPacket:
    """Tests for 'CanPacket' class."""

    SCRIPT_LOCATION = "uds.packet.can_packet"

    def setup(self):
        self.mock_can_packet = Mock(spec=CanPacket)

    # __init__

    @pytest.mark.parametrize("packet_type", ["some packet type", "single frame", 1])
    @pytest.mark.parametrize("packet_type_specific_kwargs", [
        {"v1": "some value", "v2": "Some other vlaue"},
        {"p1": "something", "p2": "something else"}
    ])
    @pytest.mark.parametrize("addressing_type, addressing_format", [
        (None, None),
        (AddressingType.FUNCTIONAL, CanAddressingFormat.NORMAL_11BIT_ADDRESSING),
    ])
    @pytest.mark.parametrize("can_id, target_address, source_address, address_extension", [
        (None, 1, 2, 3),
        (0x675, None, None, None),
    ])
    @pytest.mark.parametrize("use_data_optimization, dlc, filler_byte", [
        (True, None, 0xCC),
        (False, 8, 0xAA),
    ])
    def test_init(self, packet_type, addressing_type, addressing_format, can_id, target_address, source_address,
                  address_extension, use_data_optimization, dlc, filler_byte, packet_type_specific_kwargs):
        CanPacket.__init__(self=self.mock_can_packet,
                           packet_type=packet_type,
                           addressing=addressing_type,
                           addressing_format=addressing_format,
                           can_id=can_id,
                           target_address=target_address,
                           source_address=source_address,
                           address_extension=address_extension,
                           use_data_optimization=use_data_optimization,
                           dlc=dlc,
                           filler_byte=filler_byte,
                           **packet_type_specific_kwargs)
        self.mock_can_packet.set_address_information.assert_called_once_with(
            addressing=addressing_type,
            addressing_format=addressing_format,
            can_id=can_id,
            target_address=target_address,
            source_address=source_address,
            address_extension=address_extension,
        )
        self.mock_can_packet.set_data.assert_called_once_with(
            packet_type=packet_type,
            use_data_optimization=use_data_optimization,
            dlc=dlc,
            filler_byte=filler_byte,
            **packet_type_specific_kwargs
        )

    # __validate_address_information

    @pytest.mark.parametrize("addressing", [AddressingType.PHYSICAL, AddressingType.FUNCTIONAL.value])
    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.EXTENDED_ADDRESSING,
                                                   CanAddressingFormat.NORMAL_FIXED_ADDRESSING.value,
                                                   CanAddressingFormat.MIXED_29BIT_ADDRESSING])
    @pytest.mark.parametrize("can_id", [None, 0, 0x1FFFFFFF])
    @pytest.mark.parametrize("target_address, source_address, address_extension", [
        (None, None, None),
        (0, 0, 0),
        (0x06, 0x92, 0xD1),
        (0xFF, 0xFF, 0xFF),
    ])
    def test_validate_address_information__valid(self, addressing, addressing_format, can_id, target_address,
                                                 source_address, address_extension):
        assert CanPacket._CanPacket__validate_address_information(addressing=addressing,
                                                                  addressing_format=addressing_format,
                                                                  can_id=can_id,
                                                                  target_address=target_address,
                                                                  source_address=source_address,
                                                                  address_extension=address_extension) is None

    @pytest.mark.parametrize("addressing", [None, "not an addressing type"])
    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.EXTENDED_ADDRESSING,
                                                   CanAddressingFormat.NORMAL_FIXED_ADDRESSING.value])
    @pytest.mark.parametrize("can_id", [None, 0x1FFFFFFF])
    @pytest.mark.parametrize("target_address, source_address, address_extension", [
        (None, None, None),
        (0xFF, 0xFF, 0xFF),
    ])
    def test_set_addressing_information__value_error__addressing(self, addressing, addressing_format, can_id,
                                                                 target_address, source_address, address_extension):
        with pytest.raises(ValueError):
            CanPacket._CanPacket__validate_address_information(addressing=addressing,
                                                               addressing_format=addressing_format,
                                                               can_id=can_id,
                                                               target_address=target_address,
                                                               source_address=source_address,
                                                               address_extension=address_extension) is None

    @pytest.mark.parametrize("addressing", [AddressingType.PHYSICAL, AddressingType.FUNCTIONAL.value])
    @pytest.mark.parametrize("addressing_format", [None, False, "not an addressing format"])
    @pytest.mark.parametrize("can_id", [None, 0x1FFFFFFF])
    @pytest.mark.parametrize("target_address, source_address, address_extension", [
        (None, None, None),
        (0xFF, 0xFF, 0xFF),
    ])
    def test_set_addressing_information__value_error__addressing_format(self, addressing, addressing_format, can_id,
                                                                        target_address, source_address, address_extension):
        with pytest.raises(ValueError):
            CanPacket._CanPacket__validate_address_information(addressing=addressing,
                                                               addressing_format=addressing_format,
                                                               can_id=can_id,
                                                               target_address=target_address,
                                                               source_address=source_address,
                                                               address_extension=address_extension) is None

    @pytest.mark.parametrize("addressing", [AddressingType.PHYSICAL, AddressingType.FUNCTIONAL.value])
    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.EXTENDED_ADDRESSING,
                                                   CanAddressingFormat.NORMAL_FIXED_ADDRESSING.value])
    @pytest.mark.parametrize("can_id", [5.65, "not a can id", (0,)])
    @pytest.mark.parametrize("target_address, source_address, address_extension", [
        (None, None, None),
        (0xFF, 0xFF, 0xFF),
    ])
    def test_set_addressing_information__type_error__can_id(self, addressing, addressing_format, can_id,
                                                            target_address, source_address, address_extension):
        with pytest.raises(TypeError):
            CanPacket._CanPacket__validate_address_information(addressing=addressing,
                                                               addressing_format=addressing_format,
                                                               can_id=can_id,
                                                               target_address=target_address,
                                                               source_address=source_address,
                                                               address_extension=address_extension) is None

    @pytest.mark.parametrize("addressing", [AddressingType.PHYSICAL, AddressingType.FUNCTIONAL.value])
    @pytest.mark.parametrize("addressing_format", [CanAddressingFormat.EXTENDED_ADDRESSING,
                                                   CanAddressingFormat.NORMAL_FIXED_ADDRESSING.value])
    @pytest.mark.parametrize("can_id", [-1, 0x20000000])
    @pytest.mark.parametrize("target_address, source_address, address_extension", [
        (None, None, None),
        (0xFF, 0xFF, 0xFF),
    ])
    def test_set_addressing_information__value_error__can_id(self, addressing, addressing_format, can_id,
                                                             target_address, source_address, address_extension):
        with pytest.raises(TypeError):
            CanPacket._CanPacket__validate_address_information(addressing=addressing,
                                                               addressing_format=addressing_format,
                                                               can_id=can_id,
                                                               target_address=target_address,
                                                               source_address=source_address,
                                                               address_extension=address_extension) is None

    @pytest.mark.parametrize("param_name", ["target_address", "source_address", "address_extension"])
    @pytest.mark.parametrize("value_invalid_type", [5.65, "not a can id", (0,)])
    def test_set_addressing_information__type_error__byte_arg(self, param_name, value_invalid_type,
                                                              example_addressing_type, example_can_addressing_format):
        with pytest.raises(TypeError):
            CanPacket.__validate_address_information(self=self.mock_can_packet,
                                              addressing=example_addressing_type,
                                              addressing_format=example_can_addressing_format,
                                              **{param_name: value_invalid_type})

    @pytest.mark.parametrize("param_name", ["target_address", "source_address", "address_extension"])
    @pytest.mark.parametrize("value_invalid_type", [-1000, -1, 0x100, 999999])
    def test_set_addressing_information__value_error__byte_arg(self, param_name, value_invalid_type,
                                                               example_addressing_type, example_can_addressing_format):
        with pytest.raises(ValueError):
            CanPacket.__validate_address_information(self=self.mock_can_packet,
                                              addressing=example_addressing_type,
                                              addressing_format=example_can_addressing_format,
                                              **{param_name: value_invalid_type})

    # packet_type

    @pytest.mark.parametrize("value_stored", [AddressingType.PHYSICAL, AddressingType.FUNCTIONAL])
    def test_addressing__get(self, value_stored):
        self.mock_can_packet._CanPacket__addressing = value_stored
        assert CanPacket.addressing.fget(self=self.mock_can_packet) is value_stored

    # raw_frame_data

    @pytest.mark.parametrize("value_stored", [
        (0x02, 0x3E, 0x00),
        (0x10, 0x0A, 0x22, 0x00, 0x01, 0x00, 0x02, 0x00),
        (0x21, 0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE),
        (0x30, 0x00, 0x00, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC),
    ])
    def test_raw_frame_data__get(self, value_stored):
        self.mock_can_packet._CanPacket__raw_frame_data = value_stored
        assert CanPacket.raw_frame_data.fget(self=self.mock_can_packet) is value_stored

    # packet_type

    @pytest.mark.parametrize("value_stored", [None, CanPacketType.SINGLE_FRAME, CanPacketType.FIRST_FRAME.value])
    def test_packet_type__get(self, value_stored):
        self.mock_can_packet._CanPacket__packet_type = value_stored
        assert CanPacket.packet_type.fget(self=self.mock_can_packet) is value_stored

    # addressing_format

    @pytest.mark.parametrize("value_stored", [None, CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                              CanAddressingFormat.EXTENDED_ADDRESSING])
    def test_addressing_format__get(self, value_stored):
        self.mock_can_packet._CanPacket__addressing_format = value_stored
        assert CanPacket.addressing_format.fget(self=self.mock_can_packet) is value_stored

    # can_id

    @pytest.mark.parametrize("value_stored", [0x7FF, 0x18DA4512, 0x18CEF0E2])
    def test_can_id__get(self, value_stored):
        self.mock_can_packet._CanPacket__can_id = value_stored
        assert CanPacket.can_id.fget(self=self.mock_can_packet) is value_stored

    # target_address

    @pytest.mark.parametrize("value_stored", [None, 0, 5, 0xFF])
    def test_target_address__get(self, value_stored):
        self.mock_can_packet._CanPacket__target_address = value_stored
        assert CanPacket.target_address.fget(self=self.mock_can_packet) is value_stored

    # source_address

    @pytest.mark.parametrize("value_stored", [None, 0, 5, 0xFF])
    def test_source_address__get(self, value_stored):
        self.mock_can_packet._CanPacket__source_address = value_stored
        assert CanPacket.source_address.fget(self=self.mock_can_packet) is value_stored

    # address_extension

    @pytest.mark.parametrize("value_stored", [None, 0, 5, 0xFF])
    def test_address_extension__get(self, value_stored):
        self.mock_can_packet._CanPacket__address_extension = value_stored
        assert CanPacket.address_extension.fget(self=self.mock_can_packet) is value_stored

    # dlc

    @pytest.mark.parametrize("value_stored", [2, 4, 5, 8, 9, 0xF])
    def test_dlc__get(self, value_stored):
        self.mock_can_packet._CanPacket__dlc = value_stored
        assert CanPacket.dlc.fget(self=self.mock_can_packet) is value_stored

    # use_data_optimization

    @pytest.mark.parametrize("value_stored", [True, False])
    def test_use_data_optimization__get(self, value_stored):
        self.mock_can_packet._CanPacket__use_data_optimization = value_stored
        assert CanPacket.use_data_optimization.fget(self=self.mock_can_packet) is value_stored

    # filler_byte

    @pytest.mark.parametrize("value_stored", [True, False])
    def test_filler_byte__get(self, value_stored):
        self.mock_can_packet._CanPacket__filler_byte = value_stored
        assert CanPacket.filler_byte.fget(self=self.mock_can_packet) is value_stored


@pytest.mark.integration
class TestCanSTminIntegration:
    """Integration tests for CanSTmin class."""

    @pytest.mark.parametrize("value", [0x00, 0x01, 0x12, 0x50, 0x6D, 0x7E, 0x7F, 0xF1, 0xF4, 0xF9])
    def test_encode_and_decode(self, value):
        value_encoded = CanSTminTranslator.encode(value)
        assert CanSTminTranslator.decode(value_encoded) == value

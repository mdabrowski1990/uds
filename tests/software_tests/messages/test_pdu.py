import pytest
from mock import Mock, patch

from uds.messages.pdu import AbstractNPDU, AbstractNPCI, AbstractNPDURecord, \
    AddressingType, ByteEnum, ValidatedEnum, ExtendableEnum, TransmissionDirection


class TestAbstractNPDUType:
    """Tests for 'AbstractNPDUType' class."""

    def test_inheritance__byte_enum(self):
        assert issubclass(AbstractNPCI, ByteEnum)

    def test_inheritance__validated_enum(self):
        assert issubclass(AbstractNPCI, ValidatedEnum)

    def test_inheritance__extendable_enum(self):
        assert issubclass(AbstractNPCI, ExtendableEnum)


class TestAbstractNPDU:
    """Tests for 'AbstractNPDU' class."""

    SCRIPT_LOCATION = "uds.messages.pdu"

    def setup(self):
        self.mock_abstract_npdu = Mock(spec=AbstractNPDU)
        # patching
        self._patcher_validate_raw_bytes = patch(f"{self.SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
        self._patcher_validate_addressing_type = patch(f"{self.SCRIPT_LOCATION}.AddressingType.validate_member")
        self.mock_validate_addressing_type = self._patcher_validate_addressing_type.start()

    def teardown(self):
        self._patcher_validate_raw_bytes.stop()
        self._patcher_validate_addressing_type.stop()

    # __init__

    @pytest.mark.parametrize("raw_bytes", [None, 1, "some value", (1, 2, 3), [0x00, 0xFF]])
    @pytest.mark.parametrize("addressing_type", [None, 1, "some addressing", AddressingType.PHYSICAL])
    def test_init__valid(self, raw_bytes, addressing_type):
        AbstractNPDU.__init__(self=self.mock_abstract_npdu, raw_data=raw_bytes, addressing=addressing_type)
        assert self.mock_abstract_npdu.raw_data == raw_bytes
        assert self.mock_abstract_npdu.addressing == addressing_type

    # raw_data

    @pytest.mark.parametrize("value_stored", [None, 0, (2, 3)])
    def test_raw_data__get(self, value_stored):
        self.mock_abstract_npdu._AbstractNPDU__raw_data = value_stored
        assert AbstractNPDU.raw_data.fget(self=self.mock_abstract_npdu) is value_stored

    def test_raw_data__set(self, example_raw_bytes):
        AbstractNPDU.raw_data.fset(self=self.mock_abstract_npdu, value=example_raw_bytes)
        self.mock_validate_raw_bytes.assert_called_once_with(value=example_raw_bytes)
        assert self.mock_abstract_npdu._AbstractNPDU__raw_data == tuple(example_raw_bytes)

    # addressing

    @pytest.mark.parametrize("value_stored", [None, 0, False, AddressingType.PHYSICAL])
    def test_addressing__get(self, value_stored):
        self.mock_abstract_npdu._AbstractNPDU__addressing = value_stored
        assert AbstractNPDU.addressing.fget(self=self.mock_abstract_npdu) is value_stored

    def test_addressing__set_instance(self, example_addressing_type):
        AbstractNPDU.addressing.fset(self=self.mock_abstract_npdu, value=example_addressing_type)
        self.mock_validate_addressing_type.assert_called_once_with(value=example_addressing_type)
        assert self.mock_abstract_npdu._AbstractNPDU__addressing == example_addressing_type

    def test_addressing__set_value(self, example_addressing_type):
        AbstractNPDU.addressing.fset(self=self.mock_abstract_npdu, value=example_addressing_type.value)
        self.mock_validate_addressing_type.assert_called_once_with(value=example_addressing_type.value)
        assert self.mock_abstract_npdu._AbstractNPDU__addressing == example_addressing_type


class TestAbstractNPDURecord:
    """Tests for 'AbstractNPDURecord' class."""

    SCRIPT_LOCATION = TestAbstractNPDU.SCRIPT_LOCATION

    def setup(self):
        self.mock_pdu_record = Mock(spec=AbstractNPDURecord)
        # patching
        self._patcher_validate_direction = patch(f"{self.SCRIPT_LOCATION}.TransmissionDirection.validate_member")
        self.mock_validate_direction = self._patcher_validate_direction.start()

    def teardown(self):
        self._patcher_validate_direction.stop()

    # __init__

    @pytest.mark.parametrize("frame", [None, Mock(), 1])
    @pytest.mark.parametrize("direction", ["Some Direction"] + list(TransmissionDirection))
    def test_init(self, frame, direction):
        AbstractNPDURecord.__init__(self=self.mock_pdu_record, frame=frame, direction=direction)
        assert self.mock_pdu_record.frame == frame
        assert self.mock_pdu_record.direction == direction

    # __get_raw_pdu_type

    @pytest.mark.parametrize("raw_data, expected_result", [
        ([0x12], 0x1),
        ([0x00, 0x11, 0x22, 0x33], 0x0),
        ((0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10), 0xF),
        ((0xA5, 0x55, 0x33), 0xA),
    ])
    def test_get_raw_pdu_type(self, raw_data, expected_result):
        self.mock_pdu_record.raw_data = raw_data
        assert AbstractNPDURecord._AbstractNPDURecord__get_raw_pci(self=self.mock_pdu_record) == expected_result

    # frame

    @pytest.mark.parametrize("frame", [None, 0, "some frame"])
    def test_frame__get(self, frame):
        self.mock_pdu_record._AbstractNPDURecord__frame = frame
        assert AbstractNPDURecord.frame.fget(self=self.mock_pdu_record) == frame

    @pytest.mark.parametrize("frame", [None, 0, "some frame"])
    def test_frame__set(self, frame):
        AbstractNPDURecord.frame.fset(self=self.mock_pdu_record, value=frame)
        assert self.mock_pdu_record._AbstractNPDURecord__frame == frame
        self.mock_pdu_record._AbstractNPDURecord__validate_frame.assert_called_once_with(value=frame)

    # direction

    @pytest.mark.parametrize("direction", [None, "some direction"] + list(TransmissionDirection))
    def test_direction__get(self, direction):
        self.mock_pdu_record._AbstractNPDURecord__direction = direction
        assert AbstractNPDURecord.direction.fget(self=self.mock_pdu_record) == direction

    def test_direction__set_instance(self, example_transmission_direction):
        AbstractNPDURecord.direction.fset(self=self.mock_pdu_record, value=example_transmission_direction)
        assert self.mock_pdu_record._AbstractNPDURecord__direction == example_transmission_direction
        self.mock_validate_direction.assert_called_once_with(value=example_transmission_direction)

    def test_direction__set_value(self, example_transmission_direction):
        AbstractNPDURecord.direction.fset(self=self.mock_pdu_record, value=example_transmission_direction.value)
        assert self.mock_pdu_record._AbstractNPDURecord__direction == example_transmission_direction
        self.mock_validate_direction.assert_called_once_with(value=example_transmission_direction.value)

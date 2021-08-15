import pytest
from mock import Mock, patch

from uds.messages.pdu import AbstractPDU, AddressingType


class TestAbstractPDU:
    """Tests for 'AbstractPDU' class."""

    SCRIPT_LOCATION = "uds.messages.pdu"

    def setup(self):
        self.mock_abstract_pdu = Mock(spec=AbstractPDU)
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
        AbstractPDU.__init__(self=self.mock_abstract_pdu, raw_data=raw_bytes, addressing=addressing_type)
        assert self.mock_abstract_pdu.raw_data == raw_bytes
        assert self.mock_abstract_pdu.addressing == addressing_type

    # raw_data

    @pytest.mark.parametrize("value_stored", [None, 0, (2, 3)])
    def test_raw_data__get(self, value_stored):
        self.mock_abstract_pdu._AbstractPDU__raw_data = value_stored
        assert AbstractPDU.raw_data.fget(self=self.mock_abstract_pdu) is value_stored

    def test_raw_data__set(self, example_raw_bytes):
        AbstractPDU.raw_data.fset(self=self.mock_abstract_pdu, value=example_raw_bytes)
        self.mock_validate_raw_bytes.assert_called_once_with(value=example_raw_bytes)
        assert self.mock_abstract_pdu._AbstractPDU__raw_data == tuple(example_raw_bytes)

    # addressing

    @pytest.mark.parametrize("value_stored", [None, 0, False, AddressingType.PHYSICAL])
    def test_addressing__get(self, value_stored):
        self.mock_abstract_pdu._AbstractPDU__addressing = value_stored
        assert AbstractPDU.addressing.fget(self=self.mock_abstract_pdu) is value_stored

    def test_addressing__set_instance(self, example_addressing_type):
        AbstractPDU.addressing.fset(self=self.mock_abstract_pdu, value=example_addressing_type)
        self.mock_validate_addressing_type.assert_called_once_with(value=example_addressing_type)
        assert self.mock_abstract_pdu._AbstractPDU__addressing == example_addressing_type

    def test_addressing__set_value(self, example_addressing_type):
        AbstractPDU.addressing.fset(self=self.mock_abstract_pdu, value=example_addressing_type.value)
        self.mock_validate_addressing_type.assert_called_once_with(value=example_addressing_type.value)
        assert self.mock_abstract_pdu._AbstractPDU__addressing == example_addressing_type

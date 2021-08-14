import pytest
from mock import Mock

from uds.messages.pdu import AbstractPDU


class TestAbstractPDU:
    """Tests for 'AbstractPDU' class."""

    def setup(self):
        self.mock_abstract_pdu = Mock(spec=AbstractPDU)

    def test_init__valid(self, example_raw_bytes, example_addressing_type):
        AbstractPDU.__init__(self=self.mock_abstract_pdu, raw_data=example_raw_bytes, addressing=example_addressing_type)
        assert self.mock_abstract_pdu.raw_data == example_raw_bytes
        assert self.mock_abstract_pdu.addressing == example_addressing_type
    #
    # @pytest.mark.parametrize("addressing_type", [None, "Not an Addressing", 0])
    # def test_init__invalid_type__addressing(self, example_raw_bytes, addressing_type):
    #     with pytest.raises(TypeError):
    #         AbstractPDU.__init__(self=self.mock_abstract_pdu, raw_data=example_raw_bytes, addressing=addressing_type)
    #
    # @pytest.mark.parametrize("raw_bytes", [None, "Not Raw Bytes", 0])
    # def test_init__invalid_type__raw_data(self, example_addressing_type, raw_bytes):
    #     with pytest.raises(TypeError):
    #         AbstractPDU.__init__(self=self.mock_abstract_pdu, raw_data=raw_bytes, addressing=example_addressing_type)
    #
    # @pytest.mark.parametrize("raw_bytes", [None, "Not Raw Bytes", 0])
    # def test_init__invalid_value__raw_data(self, example_addressing_type, raw_data):
    #     with pytest.raises(ValueError):
    #         AbstractPDU.__init__(self=self.mock_abstract_pdu, raw_data=raw_data, addressing=example_addressing_type)
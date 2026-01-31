import pytest

from uds.translator.data_record_definitions.other import BITS_NUMBER


class TestDataRecords:
    """Unit tests for other Data Records."""

    # BITS_NUMBER

    @pytest.mark.parametrize("raw_value, physical_value", [
        (0, 32),
        (1, 1),
        (31, 31),
    ])
    def test_bits_number__encoding_formula(self, raw_value, physical_value):
        assert BITS_NUMBER.encoding_formula(physical_value) == raw_value

    @pytest.mark.parametrize("raw_value, physical_value", [
        (0, 32),
        (1, 1),
        (31, 31),
    ])
    def test_bits_number__decoding_formula(self, raw_value, physical_value):
        assert BITS_NUMBER.decoding_formula(raw_value) == physical_value

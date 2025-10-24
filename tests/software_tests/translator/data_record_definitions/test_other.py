import pytest
from mock import patch, call

from uds.translator.data_record_definitions.other import get_memory_size_and_memory_address

SCRIPT_LOCATION = "uds.translator.data_record_definitions.other"

class TestFormulas:

    def setup_method(self):
        self._patcher_raw_data_record = patch(f"{SCRIPT_LOCATION}.RawDataRecord")
        self.mock_raw_data_record = self._patcher_raw_data_record.start()

    def teardown_method(self):
        self._patcher_raw_data_record.stop()

    # get_memory_size_and_memory_address

    @pytest.mark.parametrize("address_and_length_format_identifier", [-1, 0x01, 0xF0, 0x111])
    def test_get_memory_size_and_memory_address__value_error(self, address_and_length_format_identifier):
        with pytest.raises(ValueError):
            get_memory_size_and_memory_address(address_and_length_format_identifier)

    @pytest.mark.parametrize("memory_address_length, memory_size_length", [
        (0x1, 0x1),
        (0xD, 0x3),
        (0xF, 0xF),
    ])
    def test_get_memory_size_and_memory_address(self, memory_address_length, memory_size_length):
        assert (get_memory_size_and_memory_address((memory_size_length << 4) + memory_address_length)
                == (self.mock_raw_data_record.return_value, self.mock_raw_data_record.return_value))
        self.mock_raw_data_record.assert_has_calls([call(name="memoryAddress",
                                                         length=8 * memory_address_length),
                                                    call(name="memorySize",
                                                         length=8 * memory_size_length)],
                                                   any_order=False)

import pytest
from mock import Mock

from uds.server.response_rule import ResponseRule, AddressingType


class TestResponseRule:
    """Tests for `ResponseRule` class."""

    def setup(self):
        self.mock_response_rule = Mock(spec=ResponseRule)

    # __init__

    @pytest.mark.parametrize("addressing_types", [
        tuple(AddressingType),
        [AddressingType.PHYSICAL],
        {AddressingType.BROADCAST, AddressingType.FUNCTIONAL}
    ])
    @pytest.mark.parametrize("related_request_sids", [
        (0x10, 0x11),
        [0x01, 0x02, 0x03],
        {0xFF}
    ])
    def test_init(self, addressing_types, related_request_sids):
        ResponseRule.__init__(self=self.mock_response_rule, addressing_types=addressing_types,
                              related_request_sids=related_request_sids)
        # data validation
        self.mock_response_rule._ResponseRule__validate_addressing_types.assert_called_once_with(
            addressing_types=addressing_types)
        self.mock_response_rule._ResponseRule__validate_related_request_sids.assert_called_once_with(
            related_request_sids=related_request_sids)
        # verify attributes values
        assert ResponseRule.addressing_types.fget(self.mock_response_rule) == set(addressing_types)
        assert ResponseRule.related_request_sids.fget(self.mock_response_rule) == set(related_request_sids)

    # __validate_addressing_types

    @pytest.mark.parametrize("addressing_types", [
        tuple(AddressingType),
        [AddressingType.PHYSICAL],
        {AddressingType.BROADCAST, AddressingType.FUNCTIONAL}
    ])
    def test_validate_addressing_types__valid(self, addressing_types):
        assert ResponseRule._ResponseRule__validate_addressing_types(addressing_types=addressing_types) is None

    @pytest.mark.parametrize("addressing_types", [None, 1, 6.5, False])
    def test_validate_addressing_types__invalid_type(self, addressing_types):
        with pytest.raises(TypeError):
            ResponseRule._ResponseRule__validate_addressing_types(addressing_types=addressing_types)

    @pytest.mark.parametrize("addressing_types", [
        [None],
        {1, 2, 3, 4},
        ("xyz", "abcd"),
    ])
    def test_validate_addressing_types__invalid_value(self, addressing_types):
        with pytest.raises(ValueError):
            ResponseRule._ResponseRule__validate_addressing_types(addressing_types=addressing_types)

    # __validate_related_request_sids

    @pytest.mark.parametrize("related_request_sids", [
        (0x10, 0x11),
        [0x01, 0x02, 0x03],
        {0xFF}
    ])
    def test_validate_related_request_sids__valid(self, related_request_sids):
        assert ResponseRule._ResponseRule__validate_related_request_sids(
            related_request_sids=related_request_sids) is None

    @pytest.mark.parametrize("related_request_sids", [None, 1, 6.5, False])
    def test_validate_related_request_sids__invalid_type(self, related_request_sids):
        with pytest.raises(TypeError):
            ResponseRule._ResponseRule__validate_related_request_sids(related_request_sids=related_request_sids)

    @pytest.mark.parametrize("related_request_sids", [
        [None],
        {1.5, 2, 3, 4},
        ("xyz", "abcd")
    ])
    def test_validate_related_request_sids__invalid_value(self, related_request_sids):
        with pytest.raises(ValueError):
            ResponseRule._ResponseRule__validate_related_request_sids(related_request_sids=related_request_sids)

    # addressing_types

    def test_addressing_types__cannot_change(self, example_addressing_types):
        with pytest.raises(Exception):
            ResponseRule.addressing_types.fset(self.mock_response_rule, example_addressing_types)

    # related_request_sids

    def test_related_request_sids__cannot_change(self, example_request_sids):
        with pytest.raises(Exception):
            ResponseRule.related_request_sids.fset(self.mock_response_rule, example_request_sids)

import pytest
from mock import patch

from uds.utilities.byte_enum import ByteEnum


class TestByteEnum:
    """Tests for `ByteEnum` class."""

    SCRIPT_LOCATION = "uds.utilities.byte_enum"

    class ExampleByteEnum1(ByteEnum):
        A = 0
        B = 255

    class ExampleByteEnum2(ByteEnum):
        Value1 = 11
        Value2 = 93
        Value3 = 237

    # __new__

    @pytest.mark.parametrize("value", ["some text", 2.34, None, (0, 1)])
    def test_new__invalid_type(self, value):
        with pytest.raises(TypeError):
            class InvalidByteEnum(ByteEnum):
                Value = value

    @pytest.mark.parametrize("value", [-100, -1, 256, 1000])
    def test_new__invalid_value(self, value):
        with pytest.raises(ValueError):
            class InvalidByteEnum(ByteEnum):
                Value = value

    @pytest.mark.parametrize("value", [0, 1, 123, 254, 255])
    def test_new__valid(self, value):
        class ExampleByteEnum(ByteEnum):
            Value = value
        assert ExampleByteEnum.Value == value
        assert isinstance(ExampleByteEnum.Value, ExampleByteEnum)
        assert ExampleByteEnum.Value in list(ExampleByteEnum)

    # is_member

    @pytest.mark.parametrize("enum_class", [ExampleByteEnum1, ExampleByteEnum2])
    def test_is_member__true_instance(self, enum_class):
        assert all([enum_class.is_member(member) is True for member in list(enum_class)])

    @pytest.mark.parametrize("enum_class", [ExampleByteEnum1, ExampleByteEnum2])
    def test_is_member__true_value(self, enum_class):
        assert all([enum_class.is_member(member.value) is True for member in list(enum_class)])

    @pytest.mark.parametrize("enum_class, not_member", [
        (ExampleByteEnum1, ExampleByteEnum2.Value1),
        (ExampleByteEnum1, ExampleByteEnum2.Value2.value),
        (ExampleByteEnum1, None),
        (ExampleByteEnum2, ExampleByteEnum1.A),
        (ExampleByteEnum2, ExampleByteEnum1.B.value),
        (ExampleByteEnum2, "some crap"),
    ])
    def test_is_member__false(self, enum_class, not_member):
        assert enum_class.is_member(not_member) is False

    # validate_member

    @patch(f"{SCRIPT_LOCATION}.ByteEnum.is_member")
    @pytest.mark.parametrize("enum_class", [ExampleByteEnum1, ExampleByteEnum2])
    @pytest.mark.parametrize("value", [None, ExampleByteEnum1.A, ExampleByteEnum2.Value1.value, 5])
    def test_validate_member__valid(self, mock_is_member, enum_class, value):
        mock_is_member.return_value = True
        assert enum_class.validate_member(value) is None
        mock_is_member.assert_called_once_with(value=value)

    @patch(f"{SCRIPT_LOCATION}.ByteEnum.is_member")
    @pytest.mark.parametrize("enum_class", [ExampleByteEnum1, ExampleByteEnum2])
    @pytest.mark.parametrize("value", [None, ExampleByteEnum1.A, ExampleByteEnum2.Value1.value, 5])
    def test_validate_member__invalid(self, mock_is_member, enum_class, value):
        mock_is_member.return_value = False
        with pytest.raises(ValueError):
            enum_class.validate_member(value)
        mock_is_member.assert_called_once_with(value=value)


class TestByteEnumAddMember:
    """
    Tests for 'add_member' method of `ByteEnum` class.

    These test are separated as it very hard to restore initial test conditions after each test case.
    """

    class ExampleByteEnum1(ByteEnum):
        A = 0
        B = 255

    class ExampleByteEnum2(ByteEnum):
        Value1 = 11
        Value2 = 93
        Value3 = 237

    # add_member

    @pytest.mark.parametrize("enum_class, name, value", [
        (ExampleByteEnum1, "C", 111),
        (ExampleByteEnum1, "SomeOtherVariable", 254),
        (ExampleByteEnum2, "First", 0),
        (ExampleByteEnum2, "Last", 255),
    ])
    def test_add_member__valid(self, enum_class, name, value):
        enum_class.add_member(name=name, value=value)
        member = enum_class[name]
        assert member.name == name
        assert member.value == value
        assert isinstance(member, enum_class)
        assert member in list(enum_class)

    @pytest.mark.parametrize("enum_class, name, value", [
        (ExampleByteEnum1, list(ExampleByteEnum1)[0].name, 111),
        (ExampleByteEnum2, list(ExampleByteEnum1)[0].name, 0),
        (ExampleByteEnum2, list(ExampleByteEnum1)[-1].name, 255),
    ])
    def test_add_member__existing_name(self, enum_class, name, value):
        with pytest.raises(ValueError):
            enum_class.add_member(name=name, value=value)

    @pytest.mark.parametrize("enum_class, name, value", [
        (ExampleByteEnum1, "SomeName", ExampleByteEnum1.A.value),
        (ExampleByteEnum2, "SomeValue", ExampleByteEnum2.Value1.value),
        (ExampleByteEnum2, "SomeOtherValue", ExampleByteEnum2.Value2.value),
    ])
    def test_add_member__existing_value(self, enum_class, name, value):
        with pytest.raises(ValueError):
            enum_class.add_member(name=name, value=value)

    @pytest.mark.parametrize("enum_class, name, value", [
        (ExampleByteEnum1, "SomeName", -1),
        (ExampleByteEnum2, "SomeOtherValue", 256),
    ])
    def test_add_member__invalid_value(self, enum_class, name, value):
        with pytest.raises(ValueError):
            enum_class.add_member(name=name, value=value)

    @pytest.mark.parametrize("enum_class, name, value", [
        (ExampleByteEnum1, "SomeName", None),
        (ExampleByteEnum2, "SomeOtherValue", "some text"),
    ])
    def test_add_member__invalid_type(self, enum_class, name, value):
        with pytest.raises(TypeError):
            enum_class.add_member(name=name, value=value)

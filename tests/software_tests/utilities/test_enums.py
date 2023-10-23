import pytest
from mock import patch
from aenum import IntEnum, StrEnum

from uds.utilities.enums import ExtendableEnum, ValidatedEnum, ByteEnum, NibbleEnum


SCRIPT_LOCATION = "uds.utilities.enums"


class TestByteEnum:
    """
    Tests for `ByteEnum` class.

    Note:
        In fact these are integration tests, but we were unable to effectively mock enum and it is not worth the effort.
    """

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


class TestNibbleEnum:
    """
    Tests for `NibbleEnum` class.

    Note:
        In fact these are integration tests, but we were unable to effectively mock enum and it is not worth the effort.
    """
    # __new__

    @pytest.mark.parametrize("value", ["some text", 2.34, None, (0, 1)])
    def test_new__invalid_type(self, value):
        with pytest.raises(TypeError):
            class InvalidByteEnum(NibbleEnum):
                Value = value

    @pytest.mark.parametrize("value", [-100, -1, 16, 1000])
    def test_new__invalid_value(self, value):
        with pytest.raises(ValueError):
            class InvalidByteEnum(NibbleEnum):
                Value = value

    @pytest.mark.parametrize("value", [0, 1, 7, 14, 15])
    def test_new__valid(self, value):
        class ExampleNibbleEnum(NibbleEnum):
            Value = value
        assert ExampleNibbleEnum.Value == value
        assert isinstance(ExampleNibbleEnum.Value, ExampleNibbleEnum)


class TestValidatedEnum:
    """
    Tests for `ValidatedEnum` class.

    Note:
        In fact these are integration tests, but we were unable to effectively mock enum and it is not worth the effort.
    """

    class ExampleByteEnum1(ValidatedEnum):
        A = 0
        B = 987654321
        C = "Something"
        D = None
        E = False
        F = ("x", "y")

    class ExampleByteEnum2(ValidatedEnum):
        Value1 = "1"
        Value2 = 2
        Value3 = 3.

    # is_member

    @pytest.mark.parametrize("enum_class", [ExampleByteEnum1, ExampleByteEnum2])
    def test_is_member__true_instance(self, enum_class):
        assert all([enum_class.is_member(member) is True for member in enum_class])

    @pytest.mark.parametrize("enum_class", [ExampleByteEnum1, ExampleByteEnum2])
    def test_is_member__true_value(self, enum_class):
        assert all([enum_class.is_member(member.value) is True for member in enum_class])

    @pytest.mark.parametrize("enum_class, not_member", [
        (ExampleByteEnum1, ExampleByteEnum2.Value1),
        (ExampleByteEnum1, ExampleByteEnum2.Value2.value),
        (ExampleByteEnum1, "not a member"),
        (ExampleByteEnum2, ExampleByteEnum1.A),
        (ExampleByteEnum2, ExampleByteEnum1.B.value),
        (ExampleByteEnum2, "some crap"),
    ])
    def test_is_member__false(self, enum_class, not_member):
        assert enum_class.is_member(not_member) is False

    # validate_member

    @patch(f"{SCRIPT_LOCATION}.ValidatedEnum.is_member")
    @pytest.mark.parametrize("enum_class", [ExampleByteEnum1, ExampleByteEnum2])
    @pytest.mark.parametrize("value", [None, ExampleByteEnum1.A, ExampleByteEnum2.Value1.value, 5])
    def test_validate_member__valid(self, mock_is_member, enum_class, value):
        mock_is_member.return_value = True
        assert enum_class.validate_member(value) is None
        mock_is_member.assert_called_once_with(value)

    @patch(f"{SCRIPT_LOCATION}.ValidatedEnum.is_member")
    @pytest.mark.parametrize("enum_class", [ExampleByteEnum1, ExampleByteEnum2])
    @pytest.mark.parametrize("value", [None, ExampleByteEnum1.A, ExampleByteEnum2.Value1.value, 5])
    def test_validate_member__invalid(self, mock_is_member, enum_class, value):
        mock_is_member.return_value = False
        with pytest.raises(ValueError):
            enum_class.validate_member(value)
        mock_is_member.assert_called_once_with(value)


class TestExtendableEnum:
    """Unit tests for 'ExtendableEnum' class."""

    class ExampleByteEnum1(ExtendableEnum):
        A = 0
        B = 987654321
        C = "Something"
        D = None
        E = False
        F = ("x", "y")

    class ExampleByteEnum2(ExtendableEnum):
        Value1 = "1"
        Value2 = 2
        Value3 = 3.

    # add_member

    @pytest.mark.parametrize("enum_class, name, value", [
        (ExampleByteEnum1, "G", 111),
        (ExampleByteEnum1, "SomeOtherVariable", 254),
        (ExampleByteEnum2, "Zero", 0),
        (ExampleByteEnum2, "X", 255),
    ])
    def test_add_member__valid(self, enum_class, name, value):
        member = enum_class.add_member(name=name, value=value)
        assert member.name == name
        assert member.value == value
        assert isinstance(member, enum_class)

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
        (ExampleByteEnum1, "SomeName", ExampleByteEnum1.F.value),
        (ExampleByteEnum2, "SomeValue", ExampleByteEnum2.Value1.value),
        (ExampleByteEnum2, "SomeOtherValue", ExampleByteEnum2.Value2.value),
    ])
    def test_add_member__existing_value(self, enum_class, name, value):
        with pytest.raises(ValueError):
            enum_class.add_member(name=name, value=value)


@pytest.mark.integration
class TestMultipleEnums:
    """Integration tests for multiple Enum classes."""

    class ExtendableByteEnumWithValidated(ByteEnum, ValidatedEnum, ExtendableEnum):
        V1 = 11
        V2 = 0x11
        V3 = 0xE5

    class ExtendableStrEnum(StrEnum, ExtendableEnum):
        Text1 = "Text 1"
        Text2 = "ABCDEF"
        Text3 = "G H I J K"
        Text4 = "NoThInG"

    class ValidatedIntEnum(IntEnum, ValidatedEnum):
        Int1 = -5
        Int2 = 99

    # is_member

    @pytest.mark.parametrize("enum_class", [ExtendableByteEnumWithValidated, ValidatedIntEnum])
    def test_is_member__true_instance(self, enum_class):
        assert all([enum_class.is_member(member) is True for member in enum_class])

    @pytest.mark.parametrize("enum_class", [ExtendableByteEnumWithValidated, ValidatedIntEnum])
    def test_is_member__true_value(self, enum_class):
        assert all([enum_class.is_member(member.value) is True for member in enum_class])

    @pytest.mark.parametrize("enum_class, not_member", [
        (ExtendableByteEnumWithValidated, ExtendableStrEnum.Text1),
        (ExtendableByteEnumWithValidated, "not a member"),
        (ExtendableByteEnumWithValidated, 0xFF),
        (ExtendableByteEnumWithValidated, 0x00),
        (ValidatedIntEnum, -1),
        (ValidatedIntEnum, ExtendableByteEnumWithValidated.V1),
        (ValidatedIntEnum, None),
        (ValidatedIntEnum, "some crap"),
    ])
    def test_is_member__false(self, enum_class, not_member):
        assert enum_class.is_member(not_member) is False

    # validate_member

    @patch(f"{SCRIPT_LOCATION}.ValidatedEnum.is_member")
    @pytest.mark.parametrize("enum_class", [ExtendableByteEnumWithValidated, ValidatedIntEnum])
    @pytest.mark.parametrize("value", [None, ExtendableByteEnumWithValidated.V1, ValidatedIntEnum.Int1.value, 5])
    def test_validate_member__valid(self, mock_is_member, enum_class, value):
        mock_is_member.return_value = True
        assert enum_class.validate_member(value) is None
        mock_is_member.assert_called_once_with(value)

    @patch(f"{SCRIPT_LOCATION}.ValidatedEnum.is_member")
    @pytest.mark.parametrize("enum_class", [ExtendableByteEnumWithValidated, ValidatedIntEnum])
    @pytest.mark.parametrize("value", [None, ExtendableByteEnumWithValidated.V1, ValidatedIntEnum.Int1.value, 5])
    def test_validate_member__invalid(self, mock_is_member, enum_class, value):
        mock_is_member.return_value = False
        with pytest.raises(ValueError):
            enum_class.validate_member(value)
        mock_is_member.assert_called_once_with(value)

    # add_member

    @pytest.mark.parametrize("enum_class, name, value", [
        (ExtendableByteEnumWithValidated, "NewMember", -1),
        (ExtendableByteEnumWithValidated, "SomeName", 256),
    ])
    def test_add_member__invalid_value(self, enum_class, name, value):
        with pytest.raises(ValueError):
            enum_class.add_member(name=name, value=value)

    @pytest.mark.parametrize("enum_class, name, value", [
        (ExtendableByteEnumWithValidated, "SomeName", None),
        (ExtendableByteEnumWithValidated, "SomeName", 5.5),
        (ExtendableStrEnum, "MEMBER", None),
        (ExtendableStrEnum, "A", 6),
    ])
    def test_add_member__invalid_type(self, enum_class, name, value):
        with pytest.raises(TypeError):
            enum_class.add_member(name=name, value=value)

    @pytest.mark.parametrize("enum_class, name, value", [
        (ExtendableByteEnumWithValidated, "Min", 0x00),
        (ExtendableByteEnumWithValidated, "Max", 0xFF),
        (ExtendableStrEnum, "SomeOtherVariable", "Some non existing string"),
        (ExtendableStrEnum, "NewVar", "-=.,';[;31413n2qtgbhj6"),
    ])
    def test_add_member__valid(self, enum_class, name, value):
        member = enum_class.add_member(name=name, value=value)
        assert member.name == name
        assert member.value == value
        assert isinstance(member, enum_class)

"""
CAN bus specific implementation of UDS packets.

:ref:`CAN packets <knowledge-base-uds-can-packet>`.
"""

__all__ = ["CanPacketType", "CanAddressingFormat", "CanFlowStatus", "CanPacket", "CanPacketRecord"]

from typing import Any, Union, Optional
from warnings import warn

from aenum import StrEnum, unique

from uds.transmission_attributes import AddressingTypeMemberTyping, AddressingType
from uds.utilities import ValidatedEnum, NibbleEnum, TimeMilliseconds, \
    RawByte, RawBytes, RawBytesTuple, validate_raw_byte
from .abstract_packet import AbstractUdsPacketType, AbstractUdsPacket, AbstractUdsPacketRecord


DEFAULT_FILLER_BYTE = 0xCC
"""Default value of Filler Byte that is used for
:ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>`"""


class UnrecognizedSTminWarning(Warning):
    """
    Warning about :ref:`STmin <knowledge-base-can-st-min>` value is reserved and therefore not implemented.

    .. note:: If you have any documentation that defines meaning of a value for which this warning was raised, please
        create a request in `issues management system <https://github.com/mdabrowski1990/uds/issues/new/choose>`_ with
        details.
    """


@unique
class CanPacketType(AbstractUdsPacketType):
    """Definition of :ref:`CAN packet types <knowledge-base-can-n-pci>`."""

    SINGLE_FRAME = 0x0
    """:ref:`Single Frame (SF) <knowledge-base-can-single-frame>` on CAN bus."""
    FIRST_FRAME = 0x1
    """:ref:`First Frame (FF) <knowledge-base-can-first-frame>` on CAN bus."""
    CONSECUTIVE_FRAME = 0x2  # noqa: F841
    """:ref:`Consecutive Frame (CF) <knowledge-base-can-consecutive-frame>` on CAN bus."""
    FLOW_CONTROL = 0x3  # noqa: F841
    """:ref:`Flow Control (FC) <knowledge-base-can-flow-control>` on CAN bus."""

    @classmethod
    def is_initial_packet_type(cls, value: Any) -> bool:
        """
        Check whether given argument is a member or a value of packet type that initiates a diagnostic message.

        :param value: Value to check.

        :return: True if given argument is a packet type that initiates a diagnostic message, else False.
        """
        cls.validate_member(value)
        return cls(value) in (cls.SINGLE_FRAME, cls.FIRST_FRAME)


CanPacketTypeMemberTyping = Union[CanPacketType, int]
"""Typing alias that describes :class:`~uds.packet.can_packet.CanPacketTypeMemberTyping` member."""


@unique
class CanAddressingFormat(StrEnum, ValidatedEnum):
    """Definition of :ref:`CAN addressing formats <knowledge-base-can-addressing>`."""

    NORMAL_11BIT_ADDRESSING = "Normal 11-bit Addressing"  # noqa: F841
    """This value represents :ref:`normal addressing <knowledge-base-can-normal-addressing>` that uses
    11-bit CAN Identifiers."""
    NORMAL_FIXED_ADDRESSING = "Normal Fixed Addressing"  # noqa: F841
    """:ref:`Normal fixed addressing <knowledge-base-can-normal-fixed-addressing>` format.
    It uses 29-bit CAN Identifiers only."""
    EXTENDED_ADDRESSING = "Extended Addressing"  # noqa: F841
    """:ref:`Extended addressing <knowledge-base-can-extended-addressing>` format that uses either 11-bit or 29-bit
    CAN Identifiers."""
    MIXED_11BIT_ADDRESSING = "Mixed 11-bit Addressing"  # noqa: F841
    """:ref:`Mixed addressing with 11-bit CAN ID <knowledge-base-can-mixed-11-bit-addressing>`.
    Subformat of :ref:`mixed addressing <knowledge-base-can-mixed-addressing>` that uses 11-bit CAN Identifiers."""
    MIXED_29BIT_ADDRESSING = "Mixed 29-bit Addressing"  # noqa: F841
    """:ref:`Mixed addressing with 29-bit CAN ID <knowledge-base-can-mixed-29-bit-addressing>`.
    Subformat of :ref:`mixed addressing <knowledge-base-can-mixed-addressing>` that uses 29-bit CAN Identifiers."""


CanAddressingFormatTyping = Union[CanAddressingFormat, str]
"""Typing alias that describes :class:`~uds.packet.can_packet.CanAddressingFormat` member."""


@unique
class CanFlowStatus(NibbleEnum, ValidatedEnum):
    """Definition of :ref:`Flow Status (FS) <knowledge-base-can-flow-status>` values."""

    ContinueToSend = 0x0  # noqa: F841
    """Informs a sending entity to resume Consecutive Frames transmission."""
    Wait = 0x1  # noqa: F841
    """Inform a sending entity to pause Consecutive Frames transmission."""
    Overflow = 0x2  # noqa: F841
    """Informs a sending entity to abort transmission of a diagnostic message."""


CanFlowStatusTyping = Union[CanFlowStatus, int]


class CanSTminTranslator:
    """Helper class for :ref:`Separation Time minimum (STmin) <knowledge-base-can-st-min>` mapping."""

    MAX_STMIN_TIME: TimeMilliseconds = 127
    """Maximal time value of STmin."""

    MIN_VALUE_MS_RANGE: int = 0
    """Minimal value of STmin in milliseconds range (raw value and time value are equal)."""
    MAX_VALUE_MS_RANGE: int = 127
    """Maximal value of STmin in milliseconds range (raw value and time value are equal)."""

    MIN_RAW_VALUE_100US_RANGE: RawByte = 0xF1
    """Minimal raw value of STmin in 100 microseconds range."""
    MAX_RAW_VALUE_100US_RANGE: RawByte = 0xF9
    """Maximal raw value of STmin in 100 microseconds range."""
    MIN_TIME_VALUE_100US_RANGE: TimeMilliseconds = 0.1
    """Minimal time value of STmin in 100 microseconds range."""
    MAX_TIME_VALUE_100US_RANGE: TimeMilliseconds = 0.9
    """Maximal time value of STmin in 100 microseconds range."""

    _FLOATING_POINT_ACCURACY: int = 8
    """Accuracy of floating point values - when rounding is necessary due to float operation in python."""

    @classmethod
    def _is_ms_value(cls, value: TimeMilliseconds) -> bool:
        """
        Check if provided argument is STmin time value in milliseconds.

        :param value: Value to check.

        :return: True if provided valid value of STmin time in milliseconds, False otherwise.
        """
        if not cls.MIN_VALUE_MS_RANGE <= value <= cls.MAX_VALUE_MS_RANGE:
            return False
        return value % 1 == 0

    @classmethod
    def _is_100us_value(cls, value: TimeMilliseconds) -> bool:
        """
        Check if provided argument is STmin time value in 100 microseconds.

        :param value: Value to check.

        :return: True if provided valid value of STmin time in 100 microseconds, False otherwise.
        """
        if not cls.MIN_TIME_VALUE_100US_RANGE <= value <= cls.MAX_TIME_VALUE_100US_RANGE:
            return False
        return round(value % 0.1, cls._FLOATING_POINT_ACCURACY) in (0, 0.1)

    @classmethod
    def encode(cls, value: RawByte) -> TimeMilliseconds:
        """
        Map raw value of STmin into time value.

        .. note:: According to ISO 15765-2, if a raw value of STmin that is not recognized by its recipient,
            then the longest STmin time value (0x7F = 127 ms) shall be used instead.

        :param value: Raw value of STmin.

        :return: STmin time in milliseconds.
        """
        validate_raw_byte(value)
        if cls.MIN_VALUE_MS_RANGE <= value <= cls.MAX_VALUE_MS_RANGE:
            return value
        if cls.MIN_RAW_VALUE_100US_RANGE <= value <= cls.MAX_RAW_VALUE_100US_RANGE:
            return (value - 0xF0) * 0.1
        warn(message=f"STmin 0x{value:X} is not recognized by this version of the package.",
             category=UnrecognizedSTminWarning)
        return cls.MAX_STMIN_TIME

    @classmethod
    def decode(cls, value: TimeMilliseconds) -> RawByte:
        """
        Map time value of STmin into raw value.

        :param value: STmin time in milliseconds.

        :raise TypeError: Provided value is not time in milliseconds.
        :raise ValueError: Value out of supported range.

        :return: Raw value of STmin.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f"Provided value is not int or float type. Actual type: {type(value)}.")
        if cls._is_ms_value(value):
            return int(value)
        if cls._is_100us_value(value):
            return int(round(value * 10, 0) + 0xF0)
        raise ValueError(f"Provided value is out of valid STmin ranges. Actual value: {value}.")


class CanId:

    MIN_11BIT_VALUE: int = 0
    MAX_11BIT_VALUE: int = 0x7FF
    MIN_29BIT_VALUE: int = 0x800

    def is_can_id(self):
        ...


class CanPacket(AbstractUdsPacket):

    def __init__(self,
                 addressing: AddressingTypeMemberTyping,
                 addressing_format: CanAddressingFormatTyping,
                 packet_type: CanPacketTypeMemberTyping,
                 can_id: Optional[int] = None,
                 target_address: Optional[RawByte] = None,
                 source_address: Optional[RawByte] = None,
                 address_extension: Optional[RawByte] = None,
                 use_data_optimization: bool = True,
                 dlc: Optional[int] = None,
                 filler_byte: RawByte = DEFAULT_FILLER_BYTE,
                 **packet_type_specific_kwargs: Any) -> None:
        """
        Create a storage for a single CAN packet.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param addressing_format: CAN addressing format that this CAN packet uses.
        :param packet_type: Type of this CAN packet.
        :param can_id: CAN Identifier that is used to transmit this packet.
            If None, then an attempt would be made to assess the CAN ID value basing on other provided arguments.
        :param target_address: Target Address value carried by this CAN Packet.
            Leave None if provided `addressing_format` does not use Target Address parameter.
        :param source_address: Source Address value carried by this CAN packet.
            Leave None if provided `addressing_format` does not use Target Address parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            Leave None if provided `addressing_format` does not use Target Address parameter.
        :param use_data_optimization: Flag whether to use CAN Data Frame Optimization during CAN Packet creation.
            - False - CAN Frame Data Padding is used in all cases (`dlc` value must be provided).
            - True - CAN Frame Data Optimization is used whenever possible, CAN Frame Data Padding is used when
              sole CAN Frame Data Optimization is not enough.
        :param dlc: DLC value of a CAN frame that carries this CAN Packet.
            Leave None if `use_data_optimization` argument is set to True.
        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        :param packet_type_specific_kwargs: Arguments that are specific for provided CAN Packet Type.
            - payload (required for: SF, FF and CF): Diagnostic message data that are carried by this CAN packet.
            - data_length (required for: FF): Number of bytes that a diagnostic message carried by this CAN packet has.
            - sequence_number (required for: CF): Sequence number of a Consecutive Frame.
            - flow_status (required for: FC): Flow status information carried by a Flow Control frame.
            - block_size (optional for: FC): Block size information carried by a Flow Control frame.
            - stmin (optional for: FC): Separation Time minimum information carried by a Flow Control frame.
        """
        self.set_address_information(addressing=addressing,
                                     addressing_format=addressing_format,
                                     can_id=can_id,
                                     target_address=target_address,
                                     source_address=source_address,
                                     address_extension=address_extension)
        self.set_data(packet_type=packet_type,
                      use_data_optimization=use_data_optimization,
                      dlc=dlc,
                      filler_byte=filler_byte,
                      **packet_type_specific_kwargs)

    def set_address_information(self,
                                addressing: AddressingTypeMemberTyping,
                                addressing_format: CanAddressingFormatTyping,
                                *,
                                can_id: Optional[int] = None,
                                target_address: Optional[RawByte] = None,
                                source_address: Optional[RawByte] = None,
                                address_extension: Optional[RawByte] = None) -> None:
        """
        Set or change addressing information for this CAN packet.

        This function enables to set an entire :ref:`Network Address Information <knowledge-base-n-ai>`
        for a :ref:`CAN packet <knowledge-base-uds-can-packet>`.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param addressing_format: CAN addressing format that this CAN packet uses.
        :param can_id: CAN Identifier that is used to transmit this packet.
            If None, then an attempt would be made to assess the CAN ID value basing on other provided arguments.
        :param target_address: Target Address value carried by this CAN Packet.
            Leave None if provided `addressing_format` does not use Target Address parameter.
        :param source_address: Source Address value carried by this CAN packet.
            Leave None if provided `addressing_format` does not use Target Address parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            Leave None if provided `addressing_format` does not use Target Address parameter.
        """
        self.__validate_address_information(addressing=addressing, addressing_format=addressing_format, can_id=can_id,
                                            target_address=target_address, source_address=source_address,
                                            address_extension=address_extension)

        # convert arguments
        addressing_type_instance = AddressingType(addressing)
        can_addressing_format_instance = CanAddressingFormat(addressing_format)
        # set values
        if can_addressing_format_instance == CanAddressingFormat.NORMAL_11BIT_ADDRESSING:
            ...
        elif can_addressing_format_instance == CanAddressingFormat.NORMAL_FIXED_ADDRESSING:
            ...
        elif can_addressing_format_instance == CanAddressingFormat.EXTENDED_ADDRESSING:
            ...
        elif can_addressing_format_instance == CanAddressingFormat.MIXED_11BIT_ADDRESSING:
            ...
        elif can_addressing_format_instance == CanAddressingFormat.MIXED_29BIT_ADDRESSING:
            ...
        else:
            raise NotImplementedError

    def set_data(self,
                 packet_type: CanPacketTypeMemberTyping,
                 *,
                 use_data_optimization: bool = True,
                 dlc: Optional[int] = None,
                 filler_byte: RawByte = DEFAULT_FILLER_BYTE,
                 **packet_type_specific_kwargs: Any) -> None:
        """

        :param packet_type:
        :param use_data_optimization:
        :param dlc:
        :param filler_byte:
        :param packet_type_specific_kwargs:

        :raise TypeError:
        :raise ValueError:
        """

    @staticmethod
    def __validate_address_information(addressing: AddressingTypeMemberTyping,
                                       addressing_format: CanAddressingFormatTyping,
                                       can_id: Optional[int],
                                       target_address: Optional[RawByte],
                                       source_address: Optional[RawByte],
                                       address_extension: Optional[RawByte]) -> None:
        """
        Validate addressing information arguments has proper types and value in range.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param addressing_format: CAN addressing format that this CAN packet uses.
        :param can_id: CAN Identifier that is used to transmit this packet.
        :param target_address: Target Address value carried by this CAN Packet.
        :param source_address: Source Address value carried by this CAN packet.
        :param address_extension: Address Extension value carried by this CAN packet.

        :raise TypeError: At least one argument has invalid type (incompatible with annotation).
        :raise ValueError: At least one argument has invalid value.
        """
        AddressingType.validate_member(addressing)
        CanAddressingFormat.validate_member(addressing_format)
        if can_id is not None and not isinstance(can_id, int):
            # TODO: validate CAN ID
            raise TypeError(f"Provided can_id value is not int type. Actual type: {type(can_id)}.")
        if target_address is not None:
            validate_raw_byte(target_address)
        if source_address is not None:
            validate_raw_byte(source_address)
        if address_extension is not None:
            validate_raw_byte(address_extension)

    def __set_single_frame_data(self, payload: RawBytes) -> None:
        """

        :param payload:

        :raise TypeError:
        :raise ValueError:
        """

    def __set_first_frame_data(self, data_length: int, payload: RawBytes) -> None:
        """

        :param data_length:
        :param payload:

        :raise TypeError:
        :raise ValueError:
        """

    def __set_consecutive_frame_data(self, sequence_number: int, payload: RawBytes) -> None:
        """

        :param sequence_number:
        :param payload:

        :raise TypeError:
        :raise ValueError:
        """

    def __set_flow_control_data(self,
                                flow_status: CanFlowStatusTyping,
                                block_size: Optional[RawByte] = None,
                                stmin: Optional[RawByte] = None) -> None:
        """

        :param flow_status:
        :param block_size:
        :param stmin:

        :raise TypeError:
        :raise ValueError:
        """

    @property
    def addressing(self) -> AddressingType:
        """
        Addressing type for which this CAN packet is relevant.

        :ref:`Addressing type <_knowledge-base-addressing>` value in CAN packet is determined by CAN ID value.
        """
        return self.__addressing

    @property
    def raw_frame_data(self) -> RawBytesTuple:
        """
        Raw data bytes of a CAN frame that carries this CAN packet.

        Data field of a :ref:`CAN frame <knowledge-base-can-frame>` that is determined by CAN packet information.
        """
        return self.__raw_frame_data

    @property
    def packet_type(self) -> CanPacketType:
        """
        Type of this CAN packet.

        :ref:`CAN packet type <knowledge-base-can-n-pci>` provides CAN specific
        :ref:`Network Protocol Control Information <knowledge-base-n-pci>`.
        """
        return self.__packet_type

    @property
    def addressing_format(self) -> CanAddressingFormat:
        """
        CAN addressing format of this CAN packet.

        Each :ref:`CAN addressing format <knowledge-base-can-addressing>` describes a different way of providing
        :ref:`Network Address Information <_knowledge-base-n-ai>` to all recipients of CAN packets."""
        return self.__addressing_format

    @property
    def can_id(self) -> int:
        """
        CAN Identifier (CAN ID) of a CAN Frame that carries this CAN packet.

        CAN ID value informs every receiving CAN node about a sender and a content of
        :ref:`CAN Frames <knowledge-base-can-frame>`.
        """
        return self.__can_id

    @property
    def target_address(self) -> Optional[RawByte]:
        """
        Target Address (TA) value of this CAN Packet.

        TA specifies receiving entity during UDS communication over CAN.

        Target Address value is used with following :ref:`addressing formats <knowledge-base-can-addressing>`:
         - :ref:`Normal Fixed Addressing <knowledge-base-can-normal-fixed-addressing>`
         - :ref:`Extended Addressing <knowledge-base-can-extended-addressing>`
         - :ref:`Mixed 29-bit Addressing <knowledge-base-can-mixed-29-bit-addressing>`
        """
        return self.__target_address

    @property
    def source_address(self) -> Optional[RawByte]:
        """
        Source Address (SA) value of this CAN Packet.

        SA specifies sending entity during UDS communication over CAN.

        Source Address value is used with following :ref:`addressing formats <knowledge-base-can-addressing>`:
         - :ref:`Normal Fixed Addressing <knowledge-base-can-normal-fixed-addressing>`
         - :ref:`Mixed 29-bit Addressing <knowledge-base-can-mixed-29-bit-addressing>`
        """
        return self.__source_address

    @property
    def address_extension(self) -> Optional[RawByte]:
        """
        Address Extension (AE) value of this CAN Packet.

        AE and CAN ID values specifies sending and receiving entity during UDS communication over CAN.

        Address Extension is used with following :ref:`addressing formats <knowledge-base-can-addressing>`:
         - :ref:`Mixed Addressing <knowledge-base-can-mixed-addressing>` - either:
           - :ref:`Mixed 11-bit Addressing <knowledge-base-can-mixed-11-bit-addressing>`
           - :ref:`Mixed 29-bit Addressing <knowledge-base-can-mixed-29-bit-addressing>`
        """
        return self.__address_extension

    @property
    def dlc(self) -> int:
        """
        Data Length Code (DLC) of a CAN Frame that carries this CAN packet.

        DLC value determines number of bytes that :ref:`CAN Frame <knowledge-base-can-frame>` contains.
        """
        return self.__dlc

    @property
    def use_data_optimization(self) -> bool:
        """
        Information whether this UDS packet uses CAN Frame Data Optimization.

        Values mapping:
         - False - :ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>` is used in all cases
         - True - :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>` is used whenever possible
           with :ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>` being used in special cases that
           sole :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>` is not enough
        """
        return self.__use_data_optimization

    @property
    def filler_byte(self) -> RawByte:
        """
        Value of Filler Byte that is used for CAN Frame Data Padding.

        Frequency of Filler Byte use depends on :attr:`~uds.packet.can_packet.CanPacket.use_data_optimization` value as
        it determines in which cases :ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>` is used.
        """
        return self.__filler_byte


class CanPacketRecord(AbstractUdsPacketRecord):
    ...
"""CAN bus specific implementation of UDS packets records."""

__all__ = ["CanPacketRecord"]

from datetime import datetime
from typing import Any, Optional, Union

from can import Message as PythonCanMessage
from uds.can import (
    AbstractCanAddressingInformation,
    CanAddressingFormat,
    CanAddressingInformation,
    CanDlcHandler,
    CanIdHandler,
)
from uds.transmission_attributes import AddressingType, TransmissionDirection
from uds.utilities import InconsistentArgumentsError

from ..abstract_packet import AbstractUdsPacketRecord
from .abstract_can_container import AbstractCanPacketContainer
from .can_packet_type import CanPacketType

CanFrameAlias = Union[PythonCanMessage]
"""Alias of supported CAN frames objects."""


class CanPacketRecord(AbstractCanPacketContainer, AbstractUdsPacketRecord):
    """
    Definition of a CAN packet record.

    Objects of this class act as a storage for historic information about transmitted or received
    :ref:`CAN packet <knowledge-base-uds-can-packet>`.
    """

    def __init__(self,
                 frame: CanFrameAlias,
                 direction: TransmissionDirection,
                 addressing_type: AddressingType,
                 addressing_format: CanAddressingFormat,
                 transmission_time: datetime) -> None:
        """
        Create a record of historic information about a CAN packet that was either received or transmitted.

        :param frame: Either received or transmitted CAN frame that carried this CAN Packet.
        :param direction: Information whether this packet was transmitted or received.
        :param addressing_type: Addressing type for which this CAN packet is relevant.
        :param addressing_format: CAN addressing format that this CAN packet used.
        :param transmission_time: Time stamp when this packet was fully transmitted on a CAN bus.
        """
        super().__init__(frame=frame, direction=direction, transmission_time=transmission_time)
        self.__addressing_type = AddressingType.validate_member(addressing_type)
        self.__addressing_format = CanAddressingFormat.validate_member(addressing_format)
        self.__packet_type: CanPacketType
        self.__target_address: Optional[int]
        self.__source_address: Optional[int]
        self.__address_extension: Optional[int]
        self.__assess_packet_type()
        self.__assess_ai_attributes()

    @property
    def raw_frame_data(self) -> bytes:
        """Raw data bytes of a frame that carried this CAN packet."""
        if isinstance(self.frame, PythonCanMessage):
            return bytes(self.frame.data)
        raise NotImplementedError(f"Missing implementation for: {self.frame}")

    @property
    def can_id(self) -> int:
        """CAN Identifier (CAN ID) of a CAN Frame that carries this CAN packet."""
        if isinstance(self.frame, PythonCanMessage):
            return self.frame.arbitration_id
        raise NotImplementedError(f"Missing implementation for: {self.frame}")

    @property
    def addressing_format(self) -> CanAddressingFormat:
        """CAN addressing format used by this CAN packet."""
        return self.__addressing_format

    @property
    def addressing_type(self) -> AddressingType:
        """Addressing type over which this CAN packet was transmitted."""
        return self.__addressing_type

    @property
    def packet_type(self) -> CanPacketType:
        """CAN packet type value - N_PCI value of this N_PDU."""
        return self.__packet_type

    @property
    def target_address(self) -> Optional[int]:
        """
        Target Address (TA) value of this CAN Packet.

        Target Address value is used with following :ref:`addressing formats <knowledge-base-can-addressing>`:
         - :ref:`Normal Fixed Addressing <knowledge-base-can-normal-fixed-addressing>`
         - :ref:`Extended Addressing <knowledge-base-can-extended-addressing>`
         - :ref:`Mixed 29-bit Addressing <knowledge-base-can-mixed-29-bit-addressing>`

        None in other cases.
        """
        return self.__target_address

    @property
    def source_address(self) -> Optional[int]:
        """
        Source Address (SA) value of this CAN Packet.

        Source Address value is used with following :ref:`addressing formats <knowledge-base-can-addressing>`:
         - :ref:`Normal Fixed Addressing <knowledge-base-can-normal-fixed-addressing>`
         - :ref:`Mixed 29-bit Addressing <knowledge-base-can-mixed-29-bit-addressing>`

        None in other cases.
        """
        return self.__source_address

    @property
    def address_extension(self) -> Optional[int]:
        """
        Address Extension (AE) value of this CAN Packet.

        Address Extension is used with following :ref:`addressing formats <knowledge-base-can-addressing>`:
         - :ref:`Mixed Addressing <knowledge-base-can-mixed-addressing>` - either:
           - :ref:`Mixed 11-bit Addressing <knowledge-base-can-mixed-11-bit-addressing>`
           - :ref:`Mixed 29-bit Addressing <knowledge-base-can-mixed-29-bit-addressing>`

        None in other cases.
        """
        return self.__address_extension

    @staticmethod
    def _validate_frame(value: Any) -> None:
        """
        Validate a CAN frame argument.

        :param value: Value to validate.

        :raise TypeError: Provided frame object has unsupported type.
        :raise ValueError: At least one attribute of the frame object is missing or its value is unexpected.
        """
        if isinstance(value, PythonCanMessage):
            CanIdHandler.validate_can_id(value.arbitration_id)
            CanDlcHandler.validate_data_bytes_number(len(value.data))
            return None
        raise TypeError(f"Unsupported CAN Frame type was provided. Actual type: {type(value)}")

    def __assess_packet_type(self) -> None:
        """Assess and set value of Packet Type attribute."""
        ai_data_bytes = CanAddressingInformation.get_ai_data_bytes_number(self.addressing_format)
        n_pci_value = self.raw_frame_data[ai_data_bytes] >> 4
        self.__packet_type = CanPacketType.validate_member(n_pci_value)

    def __assess_ai_attributes(self) -> None:
        """
        Assess and set values of attributes with Addressing Information.

        :raise InconsistentArgumentsError: Value of Addressing Type that is already set does not match decoded one.
        """
        ai_data_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(self.addressing_format)
        ai_info = CanAddressingInformation.decode_packet_ai(addressing_format=self.addressing_format,
                                                            can_id=self.can_id,
                                                            ai_data_bytes=self.raw_frame_data[:ai_data_bytes_number])
        self.__target_address = ai_info[AbstractCanAddressingInformation.TARGET_ADDRESS_NAME]  # type: ignore
        self.__source_address = ai_info[AbstractCanAddressingInformation.SOURCE_ADDRESS_NAME]  # type: ignore
        self.__address_extension = ai_info[AbstractCanAddressingInformation.ADDRESS_EXTENSION_NAME]  # type: ignore
        _addressing_type = ai_info[AbstractCanAddressingInformation.ADDRESSING_TYPE_NAME]  # type: ignore
        if _addressing_type not in (self.addressing_type, None):  # type: ignore
            raise InconsistentArgumentsError("Decoded Addressing Type does not match the one that is already set.")

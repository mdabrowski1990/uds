"""CAN bus specific implementation of packets records."""

__all__ = ["CanPacketRecord", "CanFrameAlias"]

from datetime import datetime
from typing import Any, Union

from can import Message as PythonCanMessage
from uds.addressing import AddressingType
from uds.packet import AbstractPacketRecord
from uds.utilities import ReassignmentError, TransmissionDirection

from ..addressing import CanAddressingFormat, CanAddressingInformation
from .abstract_container import AbstractCanPacketContainer
from .can_packet_type import CanPacketType

CanFrameAlias = Union[PythonCanMessage]
"""Alias of supported CAN frames objects."""


class CanPacketRecord(AbstractCanPacketContainer, AbstractPacketRecord):
    """
    Definition of a CAN packet record.

    Objects of this class act as a storage for historic information about transmitted or received
    :ref:`CAN packet <knowledge-base-can-packet>`.
    """

    def __init__(self, *,
                 frame: CanFrameAlias,
                 addressing_format: CanAddressingFormat,
                 addressing_type: AddressingType,
                 direction: TransmissionDirection,
                 transmission_time: datetime) -> None:
        """
        Create a record of historic information about a CAN packet that was either received or transmitted.

        :param frame: Either received or transmitted CAN frame that carried this CAN Packet.
        :param addressing_format: CAN Addressing Format used.
        :param addressing_type: Addressing type for which this CAN packet is relevant.
        :param direction: Information whether this packet was transmitted or received.
        :param transmission_time: Time stamp when this packet was fully transmitted on a CAN bus.
        """
        self.addressing_format = addressing_format
        self.addressing_type = addressing_type
        super().__init__(frame=frame, direction=direction, transmission_time=transmission_time)

    def __str__(self) -> str:
        """Present object in string format."""
        payload_str = "None" if self.payload is None else f"[{', '.join(f'0x{byte:02X}' for byte in self.payload)}]"
        return (f"{self.__class__.__name__}("
                f"payload={payload_str},"
                f"addressing_type={self.addressing_type}, "
                f"addressing_format={self.addressing_format}, "
                f"packet_type={self.packet_type}, "
                f"raw_frame_data=[{', '.join(f'0x{byte:02X}' for byte in self.raw_frame_data)}], "
                f"can_id={self.can_id}, "
                f"direction={self.direction}, "
                f"transmission_time={self.transmission_time})")

    @property
    def can_id(self) -> int:
        """
        CAN Identifier (CAN ID) of a CAN Frame that carries this CAN packet.

        :raise NotImplementedError: There is missing implementation for the stored CAN Frame object type.
        """
        if isinstance(self.frame, PythonCanMessage):
            return self.frame.arbitration_id
        raise NotImplementedError(f"Missing implementation for: {self.frame}")

    @property
    def raw_frame_data(self) -> bytes:
        """
        Raw data bytes of a CAN frame that carried this CAN packet.

        :raise NotImplementedError: There is missing implementation for the stored CAN Frame object type.
        """
        if isinstance(self.frame, PythonCanMessage):
            return bytes(self.frame.data)
        raise NotImplementedError(f"Missing implementation for: {self.frame}")

    @property
    def addressing_format(self) -> CanAddressingFormat:
        """CAN Addressing Format used by this CAN packet record."""
        return self.__addressing_format

    @addressing_format.setter
    def addressing_format(self, value: CanAddressingFormat) -> None:
        """
        Set CAN Addressing Format used by this CAN packet record.

        :param value: Value of CAN Addressing Format.

        :raise ReassignmentError: An attempt to change the value after object creation.
        """
        try:
            getattr(self, "_CanPacketRecord__addressing_format")
        except AttributeError:
            self.__addressing_format = CanAddressingFormat.validate_member(value)
        else:
            raise ReassignmentError("You cannot change value of 'addressing_format' attribute once it is assigned. "
                                    "Create a new object instead.")

    @property
    def addressing_type(self) -> AddressingType:
        """Addressing type over which this CAN packet was transmitted."""
        return self.__addressing_type

    @addressing_type.setter
    def addressing_type(self, value: AddressingType) -> None:
        """
        Set addressing type over which this CAN packet was transmitted.

        :param value: Value of addressing type.
        """
        try:
            getattr(self, "_CanPacketRecord__addressing_type")
        except AttributeError:
            self.__addressing_type = AddressingType.validate_member(value)
        else:
            raise ReassignmentError("You cannot change value of 'addressing_type' attribute once it is assigned. "
                                    "Create a new object instead.")

    @staticmethod
    def _validate_frame(value: Any) -> None:
        """
        Validate a CAN frame argument.

        :param value: Value to validate.

        :raise TypeError: Provided frame object has unsupported type.
        """
        if isinstance(value, PythonCanMessage):
            return None
        raise TypeError(f"Unsupported CAN Frame type was provided. Actual type: {type(value)}")

    def _validate_attributes(self) -> None:
        """Validate whether attributes that were set are a valid for a CAN Packet record."""
        CanAddressingInformation.validate_addressing_params(addressing_format=self.addressing_format,
                                                            addressing_type=self.addressing_type,
                                                            can_id=self.can_id,
                                                            target_address=self.target_address,
                                                            source_address=self.source_address,
                                                            address_extension=self.address_extension)
        CanPacketType.validate_member(self.packet_type)

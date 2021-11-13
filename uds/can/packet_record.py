__all__ = ["CanPacketRecord"]

from typing import Union, Any, Optional

from can import Message as PythonCanMessage

from uds.utilities import RawByte, RawBytesTuple, TimeStamp
from uds.packet import AbstractUdsPacketRecord
from uds.transmission_attributes import TransmissionDirectionAlias, TransmissionDirection, \
    AddressingType, AddressingTypeAlias
from .addressing_format import CanAddressingFormat, CanAddressingFormatAlias
from .packet_type import CanPacketType
from .flow_control import CanFlowStatus
from .packet import CanPacket


CanFrameAlias = Union[PythonCanMessage]


class CanPacketRecord(AbstractUdsPacketRecord):
    """
    Definition of a CAN packet Record.

    Objects of this class act as a storage for historic information about transmitted or received
    :ref:`CAN packet <knowledge-base-uds-can-packet>`.
    """

    def __init__(self,
                 frame: CanFrameAlias,
                 direction: TransmissionDirectionAlias,
                 addressing_type: AddressingTypeAlias,
                 addressing_format: CanAddressingFormatAlias) -> None:
        """
        Create a record of a historic information about a CAN packet that was either received or transmitted.

        :param frame: Either received or transmitted CAN frame that carried this CAN Packet.
        :param direction: Information whether this packet was transmitted or received.
        :param addressing_type: Addressing type for which this CAN packet is relevant.
        :param addressing_format: CAN addressing format that this CAN packet used.
        """
        # TODO

    def __validate_frame(self, value: Any) -> None:
        """
        Validate a CAN frame argument.

        :param value: Value to validate.

        :raise TypeError: The frame argument has unsupported.
        :raise ValueError: Some attribute of the frame argument is missing or its value is unexpected.
        """
        # TODO

    @property
    def raw_frame_data(self) -> RawBytesTuple:
        """Raw data bytes of a frame that carried this CAN packet."""
        # TODO: PythonCanMessage.data

    @property
    def addressing_type(self) -> AddressingType:
        """Addressing type over which this CAN packet was transmitted."""
        # TODO: provided in init

    @property
    def transmission_time(self) -> TimeStamp:
        """Time stamp when this CAN packet was fully transmitted on a bus."""
        # TODO: ?? PythonCanMessage.timestamp + offset?

    @property
    def packet_type(self) -> CanPacketType:
        """CAN packet type value - N_PCI value of this N_PDU."""
        # TODO: extract from raw_frame_data

    @property
    def payload(self) -> Optional[RawBytesTuple]:
        """Payload bytes of a diagnostic message carried by this CAN packet."""
        # TODO: CanPacket.payload

    @property
    def data_length(self) -> Optional[int]:
        """Payload bytes number of a diagnostic message which was carried by this CAN packet."""
        # TODO: CanPacket.data_length

    @property
    def can_id(self) -> int:
        """CAN Identifier (CAN ID) of a CAN Frame that carries this CAN packet."""
        # TODO: PythonCanMessage.arbitration_id

    @property
    def dlc(self) -> int:
        """Value of Data Length Code (DLC) of a CAN Frame that carries this CAN packet."""
        # TODO: PythonCanMessage.dlc

    @property
    def target_address(self) -> Optional[RawByte]:
        """
        Target Address (TA) value of this CAN Packet.

        Target Address value is used with following :ref:`addressing formats <knowledge-base-can-addressing>`:
         - :ref:`Normal Fixed Addressing <knowledge-base-can-normal-fixed-addressing>`
         - :ref:`Extended Addressing <knowledge-base-can-extended-addressing>`
         - :ref:`Mixed 29-bit Addressing <knowledge-base-can-mixed-29-bit-addressing>`

        None in other cases.
        """
        # TODO: extract from raw_frame_data / can_id

    @property
    def source_address(self) -> Optional[RawByte]:
        """
        Source Address (SA) value of this CAN Packet.

        Source Address value is used with following :ref:`addressing formats <knowledge-base-can-addressing>`:
         - :ref:`Normal Fixed Addressing <knowledge-base-can-normal-fixed-addressing>`
         - :ref:`Mixed 29-bit Addressing <knowledge-base-can-mixed-29-bit-addressing>`

        None in other cases.
        """
        # TODO: extract from can_id

    @property
    def address_extension(self) -> Optional[RawByte]:
        """
        Address Extension (AE) value of this CAN Packet.

        Address Extension is used with following :ref:`addressing formats <knowledge-base-can-addressing>`:
         - :ref:`Mixed Addressing <knowledge-base-can-mixed-addressing>` - either:
           - :ref:`Mixed 11-bit Addressing <knowledge-base-can-mixed-11-bit-addressing>`
           - :ref:`Mixed 29-bit Addressing <knowledge-base-can-mixed-29-bit-addressing>`

        None in other cases.
        """
        # TODO: extract from raw_frame_data / can_id

    @property
    def sequence_number(self) -> Optional[int]:
        """
        Sequence Number carried by this CAN packet.

        :ref:`Sequence Number <knowledge-base-can-sequence-number>` is only provided by packets of following types:
         - :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`

        None in other cases.
        """
        # TODO: use CanPacket.sequence_number

    @property
    def flow_status(self) -> Optional[CanFlowStatus]:
        """
        Flow Status carried by this CAN packet.

        :ref:`Flow Status <knowledge-base-can-flow-status>` is only provided by packets of following types:
         - :ref:`Flow Control <knowledge-base-can-flow-control>`

        None in other cases.
        """
        # TODO: use CanPacket.flow_status

    @property
    def block_size(self) -> Optional[RawByte]:
        """
        Block Size value carried by this CAN packet.

        :ref:`Block Size <knowledge-base-can-flow-status>` is only provided by packets of following types:
         - :ref:`Flow Control <knowledge-base-can-block-size>`

        None in other cases.
        """
        # TODO: use CanPacket.block_size

    @property
    def st_min(self) -> Optional[RawByte]:
        """
        Separation Time minimum (STmin) value carried by this CAN packet.

        :ref:`STmin <knowledge-base-can-st-min>` is only provided by packets of following types:
         - :ref:`Flow Control <knowledge-base-can-block-size>`

        None in other cases.
        """
        # TODO: use CanPacket.st_min

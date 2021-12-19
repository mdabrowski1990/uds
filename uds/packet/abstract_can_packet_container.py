"""Abstract definition of CAN packets container."""

__all__ = ["AbstractCanPacketContainer"]

from abc import ABC, abstractmethod
from typing import Optional

from uds.utilities import RawByte, RawBytesTuple
from uds.transmission_attributes import AddressingTypeAlias
from uds.can import CanAddressingInformationHandler, CanDlcHandler, \
    CanSingleFrameHandler, CanFirstFrameHandler, CanConsecutiveFrameHandler, CanFlowControlHandler, \
    CanAddressingFormatAlias, CanFlowStatusAlias
from .can_packet_type import CanPacketTypeAlias, CanPacketType


class AbstractCanPacketContainer(ABC):
    """Abstract definition of CAN Packets containers."""

    @property
    @abstractmethod
    def raw_frame_data(self) -> RawBytesTuple:
        """Raw data bytes of a CAN frame that carries this CAN packet."""

    @property
    @abstractmethod
    def can_id(self) -> int:
        """CAN Identifier (CAN ID) of a CAN Frame that carries this CAN packet."""

    @property
    @abstractmethod
    def addressing_format(self) -> CanAddressingFormatAlias:
        """CAN addressing format used by this CAN packet."""

    @property
    @abstractmethod
    def addressing_type(self) -> AddressingTypeAlias:
        """Addressing type for which this CAN packet is relevant."""

    @property
    def dlc(self) -> int:
        """Value of Data Length Code (DLC) of a CAN Frame that carries this CAN packet."""
        return CanDlcHandler.encode_dlc(len(self.raw_frame_data))

    @property
    def packet_type(self) -> CanPacketTypeAlias:
        """Type (N_PCI value) of this CAN packet."""
        ai_data_bytes_number = CanAddressingInformationHandler.get_ai_data_bytes_number(self.addressing_format)
        return CanPacketType(self.raw_frame_data[ai_data_bytes_number] >> 4)

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
        return self.get_addressing_information()[CanAddressingInformationHandler.TARGET_ADDRESS_NAME]

    @property
    def source_address(self) -> Optional[RawByte]:
        """
        Source Address (SA) value of this CAN Packet.

        Source Address value is used with following :ref:`addressing formats <knowledge-base-can-addressing>`:
         - :ref:`Normal Fixed Addressing <knowledge-base-can-normal-fixed-addressing>`
         - :ref:`Mixed 29-bit Addressing <knowledge-base-can-mixed-29-bit-addressing>`

        None in other cases.
        """
        return self.get_addressing_information()[CanAddressingInformationHandler.SOURCE_ADDRESS_NAME]

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
        return self.get_addressing_information()[CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME]

    @property
    def data_length(self) -> Optional[int]:
        """
        Payload bytes number of a diagnostic message that is carried by this CAN packet.

        Data length is only provided by packets of following types:
         - :ref:`Single Frame <knowledge-base-can-single-frame>` -
           :ref:`Single Frame Data Length <knowledge-base-can-single-frame-data-length>`
         - :ref:`First Frame <knowledge-base-can-first-frame>` -
           :ref:`First Frame Data Length <knowledge-base-can-first-frame-data-length>`

        None in other cases.
        """
        if self.packet_type == CanPacketType.SINGLE_FRAME:
            return CanSingleFrameHandler.decode_sf_dl(addressing_format=self.addressing_format,
                                                      raw_frame_data=self.raw_frame_data)
        if self.packet_type == CanPacketType.FIRST_FRAME:
            return CanFirstFrameHandler.decode_ff_dl(addressing_format=self.addressing_format,
                                                     raw_frame_data=self.raw_frame_data)
        return None

    @property
    def sequence_number(self) -> Optional[int]:
        """
        Sequence Number carried by this CAN packet.

        :ref:`Sequence Number <knowledge-base-can-sequence-number>` is only provided by packets of following types:
         - :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`

        None in other cases.
        """
        if self.packet_type == CanPacketType.CONSECUTIVE_FRAME:
            return CanConsecutiveFrameHandler.decode_sequence_number(addressing_format=self.addressing_format,
                                                                     raw_frame_data=self.raw_frame_data)
        return None

    @property
    def payload(self) -> Optional[RawBytesTuple]:
        """
        Diagnostic message payload carried by this CAN packet.

        Payload is only provided by packets of following types:
         - :ref:`Single Frame <knowledge-base-can-single-frame>`
         - :ref:`First Frame <knowledge-base-can-first-frame>`
         - :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`

        None in other cases.

        .. warning:: For :ref:`Consecutive Frames <knowledge-base-can-consecutive-frame>` this value might contain
            additional filler bytes (they are not part of diagnostic message payload) that were added during
            :ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>`.
            The presence of filler bytes in :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`
            cannot be determined basing solely on the information contained in this packet object.
        """
        if self.packet_type == CanPacketType.SINGLE_FRAME:
            return tuple(CanSingleFrameHandler.decode_payload(addressing_format=self.addressing_format,
                                                              raw_frame_data=self.raw_frame_data))
        if self.packet_type == CanPacketType.FIRST_FRAME:
            return tuple(CanFirstFrameHandler.decode_payload(addressing_format=self.addressing_format,
                                                             raw_frame_data=self.raw_frame_data))
        if self.packet_type == CanPacketType.CONSECUTIVE_FRAME:
            return tuple(CanConsecutiveFrameHandler.decode_payload(addressing_format=self.addressing_format,
                                                                   raw_frame_data=self.raw_frame_data))
        return None

    @property
    def flow_status(self) -> Optional[CanFlowStatusAlias]:
        """
        Flow Status carried by this CAN packet.

        :ref:`Flow Status <knowledge-base-can-flow-status>` is only provided by packets of following types:
         - :ref:`Flow Control <knowledge-base-can-flow-control>`

        None in other cases.
        """
        if self.packet_type == CanPacketType.FLOW_CONTROL:
            return CanFlowControlHandler.decode_flow_status(addressing_format=self.addressing_format,
                                                            raw_frame_data=self.raw_frame_data)
        return None

    @property
    def block_size(self) -> Optional[RawByte]:
        """
        Block Size value carried by this CAN packet.

        :ref:`Block Size <knowledge-base-can-flow-status>` is only provided by packets of following types:
         - :ref:`Flow Control <knowledge-base-can-block-size>`

        None in other cases.
        """
        if self.packet_type == CanPacketType.FLOW_CONTROL:
            return CanFlowControlHandler.decode_block_size(addressing_format=self.addressing_format,
                                                           raw_frame_data=self.raw_frame_data)
        return None

    @property
    def st_min(self) -> Optional[RawByte]:
        """
        Separation Time minimum (STmin) value carried by this CAN packet.

        :ref:`STmin <knowledge-base-can-st-min>` is only provided by packets of following types:
         - :ref:`Flow Control <knowledge-base-can-block-size>`

        None in other cases.
        """
        if self.packet_type == CanPacketType.FLOW_CONTROL:
            return CanFlowControlHandler.decode_st_min(addressing_format=self.addressing_format,
                                                       raw_frame_data=self.raw_frame_data)
        return None

    def get_addressing_information(self) -> dict:
        """
        Get Addressing Information carried by this packet.

        :return: Addressing Information decoded from CAN ID and CAN Frame data of this packet.
        """
        ai_data_bytes_number = CanAddressingInformationHandler.get_ai_data_bytes_number(self.addressing_format)
        return CanAddressingInformationHandler.decode_ai(addressing_format=self.addressing_format,
                                                         can_id=self.can_id,
                                                         ai_data_bytes=self.raw_frame_data[:ai_data_bytes_number])

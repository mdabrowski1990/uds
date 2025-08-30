"""Abstract definition of a container for a CAN packet."""

__all__ = ["AbstractCanPacketContainer", "CanPacketsContainersSequence"]

from abc import ABC, abstractmethod
from typing import Optional, Sequence

from uds.addressing import AddressingType
from uds.packet.abstract_packet import AbstractPacketContainer

from ..addressing import CanAddressingFormat, CanAddressingInformation
from ..frame import CanDlcHandler
from .can_packet_type import CanPacketType
from .consecutive_frame import extract_consecutive_frame_payload, extract_sequence_number
from .first_frame import extract_ff_dl, extract_first_frame_payload
from .flow_control import CanFlowStatus, extract_block_size, extract_flow_status, extract_st_min
from .single_frame import extract_sf_dl, extract_single_frame_payload


class AbstractCanPacketContainer(AbstractPacketContainer, ABC):
    """Abstract definition of CAN Packets containers."""

    @property
    @abstractmethod
    def can_id(self) -> int:
        """CAN Identifier (CAN ID) of a CAN Frame that carries this CAN packet."""

    @property
    @abstractmethod
    def raw_frame_data(self) -> bytes:
        """Raw data bytes of a CAN frame that carries this CAN packet."""

    @property
    def dlc(self) -> int:
        """Value of Data Length Code (DLC) of a CAN Frame that carries this CAN packet."""
        return CanDlcHandler.encode_dlc(len(self.raw_frame_data))

    @property
    @abstractmethod
    def addressing_format(self) -> CanAddressingFormat:
        """CAN addressing format used by this CAN packet."""

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
        return CanAddressingInformation.decode_frame_ai_params(addressing_format=self.addressing_format,
                                                               can_id=self.can_id,
                                                               raw_frame_data=self.raw_frame_data)["target_address"]

    @property
    def source_address(self) -> Optional[int]:
        """
        Source Address (SA) value of this CAN Packet.

        Source Address value is used with following :ref:`addressing formats <knowledge-base-can-addressing>`:

        - :ref:`Normal Fixed Addressing <knowledge-base-can-normal-fixed-addressing>`
        - :ref:`Mixed 29-bit Addressing <knowledge-base-can-mixed-29-bit-addressing>`

        None in other cases.
        """
        return CanAddressingInformation.decode_frame_ai_params(addressing_format=self.addressing_format,
                                                               can_id=self.can_id,
                                                               raw_frame_data=self.raw_frame_data)["source_address"]

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
        return CanAddressingInformation.decode_frame_ai_params(addressing_format=self.addressing_format,
                                                               can_id=self.can_id,
                                                               raw_frame_data=self.raw_frame_data)["address_extension"]

    @property
    def packet_type(self) -> CanPacketType:
        """Type (N_PCI value) of this CAN packet."""
        ai_data_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(self.addressing_format)
        return CanPacketType(self.raw_frame_data[ai_data_bytes_number] >> 4)

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

        :raise NotImplementedError: There is missing implementation for the set CAN Packet Type.
        """
        if self.packet_type == CanPacketType.SINGLE_FRAME:
            return extract_sf_dl(addressing_format=self.addressing_format,
                                 raw_frame_data=self.raw_frame_data)
        if self.packet_type == CanPacketType.FIRST_FRAME:
            return extract_ff_dl(addressing_format=self.addressing_format,
                                 raw_frame_data=self.raw_frame_data)
        if self.packet_type in {CanPacketType.CONSECUTIVE_FRAME,
                                CanPacketType.FLOW_CONTROL}:
            return None
        raise NotImplementedError("There is missing implementation for the currently set CAN Packet Type: "
                                  f"{self.packet_type}.")

    @property
    def sequence_number(self) -> Optional[int]:
        """
        Sequence Number carried by this CAN packet.

        :ref:`Sequence Number <knowledge-base-can-sequence-number>` is only provided by packets of
        following types:

        - :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`

        None in other cases.

        :raise NotImplementedError: There is missing implementation for current CAN Packet Type.
        """
        if self.packet_type == CanPacketType.CONSECUTIVE_FRAME:
            return extract_sequence_number(addressing_format=self.addressing_format,
                                           raw_frame_data=self.raw_frame_data)
        if self.packet_type in {CanPacketType.SINGLE_FRAME,
                                CanPacketType.FIRST_FRAME,
                                CanPacketType.FLOW_CONTROL}:
            return None
        raise NotImplementedError("No handling for given CAN Packet Packet Type.")

    @property
    def flow_status(self) -> Optional[CanFlowStatus]:
        """
        Flow Status carried by this CAN packet.

        :ref:`Flow Status <knowledge-base-can-flow-status>` is only provided by packets of following types:

        - :ref:`Flow Control <knowledge-base-can-flow-control>`

        None in other cases.

        :raise NotImplementedError: There is missing implementation for current CAN Packet Type.
        """
        if self.packet_type == CanPacketType.FLOW_CONTROL:
            return extract_flow_status(addressing_format=self.addressing_format,
                                       raw_frame_data=self.raw_frame_data)
        if self.packet_type in {CanPacketType.SINGLE_FRAME,
                                CanPacketType.FIRST_FRAME,
                                CanPacketType.CONSECUTIVE_FRAME}:
            return None
        raise NotImplementedError("No handling for given CAN Packet Packet Type.")

    @property
    def block_size(self) -> Optional[int]:
        """
        Block Size value carried by this CAN packet.

        :ref:`Block Size <knowledge-base-can-flow-status>` is only provided by packets of following types:

        - :ref:`Flow Control <knowledge-base-can-block-size>`

        None in other cases.

        :raise NotImplementedError: There is missing implementation for current CAN Packet Type.
        """
        if self.packet_type == CanPacketType.FLOW_CONTROL:
            return extract_block_size(addressing_format=self.addressing_format,
                                      raw_frame_data=self.raw_frame_data)
        if self.packet_type in {CanPacketType.SINGLE_FRAME,
                                CanPacketType.FIRST_FRAME,
                                CanPacketType.CONSECUTIVE_FRAME}:
            return None
        raise NotImplementedError("No handling for given CAN Packet Packet Type.")

    @property
    def st_min(self) -> Optional[int]:
        """
        Separation Time minimum (STmin) value carried by this CAN packet.

        :ref:`STmin <knowledge-base-can-st-min>` is only provided by packets of following types:

        - :ref:`Flow Control <knowledge-base-can-block-size>`

        None in other cases.

        :raise NotImplementedError: There is missing implementation for current CAN Packet Type.
        """
        if self.packet_type == CanPacketType.FLOW_CONTROL:
            return extract_st_min(addressing_format=self.addressing_format,
                                  raw_frame_data=self.raw_frame_data)
        if self.packet_type in {CanPacketType.SINGLE_FRAME,
                                CanPacketType.FIRST_FRAME,
                                CanPacketType.CONSECUTIVE_FRAME}:
            return None
        raise NotImplementedError("No handling for given CAN Packet Packet Type.")

    @property
    @abstractmethod
    def addressing_type(self) -> AddressingType:
        """Addressing type for which this CAN packet is relevant."""

    @property
    def payload(self) -> Optional[bytes]:
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

        :raise NotImplementedError: There is missing implementation for current CAN Packet Type.
        """
        if self.packet_type == CanPacketType.SINGLE_FRAME:
            return bytes(extract_single_frame_payload(addressing_format=self.addressing_format,
                                                      raw_frame_data=self.raw_frame_data))
        if self.packet_type == CanPacketType.FIRST_FRAME:
            return bytes(extract_first_frame_payload(addressing_format=self.addressing_format,
                                                     raw_frame_data=self.raw_frame_data))
        if self.packet_type == CanPacketType.CONSECUTIVE_FRAME:
            return bytes(extract_consecutive_frame_payload(addressing_format=self.addressing_format,
                                                           raw_frame_data=self.raw_frame_data))
        if self.packet_type == CanPacketType.FLOW_CONTROL:
            return None
        raise NotImplementedError("No handling for given CAN Packet Packet Type.")


CanPacketsContainersSequence = Sequence[AbstractPacketContainer]
"""Alias for a sequence filled with CAN packet or packet record objects."""

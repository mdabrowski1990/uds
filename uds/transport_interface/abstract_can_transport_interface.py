"""Abstract definition of UDS Transport Interface for CAN bus."""

from typing import Optional, Union, Any, Tuple, Iterable
from abc import abstractmethod

from uds.utilities import TimeMilliseconds
from uds.packet import CanPacket
from .abstract_transport_interface import AbstractTransportInterface


FlowControlGenerator = Union[CanPacket, Iterable[CanPacket]]


class AbstractCanTransportInterface(AbstractTransportInterface):
    """
    Abstract definition of Transport Interface for CAN bus.

    CAN Transport Interfaces are meant to handle middle layers (Transport and Network) for CAN bus.
    """

    def __init__(self,
                 bus_handler: Any,  # noqa: F841
                 max_packet_records_stored: int,  # noqa: F841
                 max_message_records_stored: int,  # noqa: F841
                 addressing_format: CanAddressingFormatAlias,
                 physical_ai: AIArgsAlias,
                 functional_ai: AIArgsAlias,
                 **kwargs: Any) -> None:  # noqa: F841
        """
        Create Transport Interface (an object for handling UDS Transport and Network layers).

        :param bus_handler: An object that handles the bus (Physical and Data layers of OSI Model).
        :param max_packet_records_stored: Maximal number of UDS packet records to be stored in
            :attr:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.packet_records`.
        :param max_message_records_stored: Maximal number of UDS message records to be stored in
            :attr:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.message_records`.
        :param kwargs: TODO:
            - Network layer parameters (N_As, N_Ar, ...)
            - CAN Frame creation (dlc, use_data_optimization, filler_byte)
        """

    # N_As

    @property
    def n_as_timeout(self) -> TimeMilliseconds:
        ...

    @n_as_timeout.setter
    def n_as_timeout(self, value: TimeMilliseconds):
        ...

    # N_Ar

    @property
    def n_ar_timeout(self) -> TimeMilliseconds:
        ...

    @n_ar_timeout.setter
    def n_ar_timeout(self, value: TimeMilliseconds):
        ...

    # N_Bs

    @property
    def n_bs_timeout(self) -> TimeMilliseconds:
        ...

    @n_bs_timeout.setter
    def n_bs_timeout(self, value: TimeMilliseconds):
        ...

    # N_Br

    @property
    def n_br(self) -> Optional[TimeMilliseconds]:
        ...

    @n_br.setter
    def n_br(self, value: Optional[TimeMilliseconds]) -> None:
        ...

    @property
    def n_br_max(self) -> Optional[TimeMilliseconds]:
        ...

    # N_Cs

    @property
    def n_cs(self) -> Optional[TimeMilliseconds]:
        ...

    @n_cs.setter
    def n_cs(self, value: Optional[TimeMilliseconds]) -> None:
        ...

    @property
    def n_cs_max(self) -> Optional[TimeMilliseconds]:
        ...

    # N_Cr

    @property
    def n_cr_timeout(self) -> TimeMilliseconds:
        ...

    @n_cr_timeout.setter
    def n_cr_timeout(self, value: TimeMilliseconds):
        ...

    # Flow Control

    @property
    def flow_control(self) -> FlowControlGenerator:
        ...

    @flow_control.setter
    def flow_control(self, value: FlowControlGenerator) -> None:
        ...

    # TODO: properties - CAN Segmenter and CAN parameters (get them from segmenter to avoid variables duplicates)

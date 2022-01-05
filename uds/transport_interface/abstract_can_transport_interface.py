"""Abstract definition of UDS Transport Interface for CAN bus."""

from typing import Optional, Union, Any, Iterable

from uds.utilities import TimeMilliseconds, RawByte
from uds.packet import CanPacket
from uds.can import CanAddressingFormatAlias
from .abstract_transport_interface import AbstractTransportInterface


FlowControlGenerator = Union[CanPacket, Iterable[CanPacket]]


class AbstractCanTransportInterface(AbstractTransportInterface):
    """
    Abstract definition of Transport Interface for CAN bus.

    CAN Transport Interfaces are meant to handle middle layers (Transport and Network) for CAN bus.
    """

    def __init__(self,
                 bus_manager: Any,  # noqa: F841
                 max_packet_records_stored: int,  # noqa: F841
                 max_message_records_stored: int,  # noqa: F841
                 addressing_format: CanAddressingFormatAlias,
                 physical_ai: AIArgsAlias,
                 functional_ai: AIArgsAlias,
                 **kwargs: Any) -> None:  # noqa: F841
        """
        Create Transport Interface (an object for handling UDS Transport and Network layers).

        :param bus_manager: An object that handles the bus (Physical and Data layers of OSI Model).
        :param max_packet_records_stored: Maximal number of UDS packet records to be stored in
            :attr:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.packet_records`.
        :param max_message_records_stored: Maximal number of UDS message records to be stored in
            :attr:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.message_records`.
        :param kwargs: Optional arguments that are specific for CAN bus.

            - :parameter n_as_timeout: Timeout value for :ref:`N_As <knowledge-base-can-n-as>` time parameter.
            - :parameter n_ar_timeout: Timeout value for :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter.
            - :parameter n_bs_timeout: Timeout value for :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter.
            - :parameter n_br: Value of :ref:`N_Br <knowledge-base-can-n-br>` time parameter to use in communication.
            - :parameter n_cs: Value of :ref:`N_Cs <knowledge-base-can-n-cs>` time parameter to use in communication.
            - :parameter n_cr_timeout: Timeout value for :ref:`N_Cr <knowledge-base-can-n-cr>` time parameter.
            - :parameter dlc: Base CAN DLC value to use for CAN Packets.
            - :parameter use_data_optimization: Information whether to use CAN Frame Data Optimization.
            - :parameter filler_byte: Filler byte value to use for CAN Frame Data Padding.
            - :parameter flow_control_generator: Generator of Flow Control CAN packets.
        """
        raise NotImplementedError

    # Time parameter - CAN Network Layer

    @property
    def n_as_timeout(self) -> TimeMilliseconds:
        ...

    @n_as_timeout.setter
    def n_as_timeout(self, value: TimeMilliseconds):
        ...

    @property
    def n_as_measured(self) -> Optional[TimeMilliseconds]:
        ...

    @property
    def n_ar_timeout(self) -> TimeMilliseconds:
        ...

    @n_ar_timeout.setter
    def n_ar_timeout(self, value: TimeMilliseconds):
        ...

    @property
    def n_ar_measured(self) -> Optional[TimeMilliseconds]:
        ...

    @property
    def n_bs_timeout(self) -> TimeMilliseconds:
        ...

    @n_bs_timeout.setter
    def n_bs_timeout(self, value: TimeMilliseconds):
        ...

    @property
    def n_bs_measured(self) -> Optional[TimeMilliseconds]:
        ...

    @property
    def n_br(self) -> Optional[TimeMilliseconds]:
        ...

    @n_br.setter
    def n_br(self, value: Optional[TimeMilliseconds]) -> None:
        ...

    @property
    def n_br_max(self) -> Optional[TimeMilliseconds]:
        ...

    @property
    def n_cs(self) -> Optional[TimeMilliseconds]:
        ...

    @n_cs.setter
    def n_cs(self, value: Optional[TimeMilliseconds]) -> None:
        ...

    @property
    def n_cs_max(self) -> Optional[TimeMilliseconds]:
        ...

    @property
    def n_cr_timeout(self) -> TimeMilliseconds:
        ...

    @n_cr_timeout.setter
    def n_cr_timeout(self, value: TimeMilliseconds):
        ...

    @property
    def n_cr_measured(self) -> Optional[TimeMilliseconds]:
        ...

    # Communication parameters

    @property
    def addressing_format(self) -> CanAddressingFormatAlias:  # TODO: get from the segmenter
        ...

    @property
    def physical_ai(self) -> Optional[AIParamsAlias]:  # TODO: get from the segmenter
        ...

    @physical_ai.setter
    def physical_ai(self, value: Optional[AIArgsAlias]):  # TODO: set in the segmenter
        ...

    @property
    def functional_ai(self) -> AIParamsAlias:  # TODO: get from the segmenter
        ...

    @functional_ai.setter
    def functional_ai(self, value: Optional[AIArgsAlias]):  # TODO: set in the segmenter
        ...

    @property
    def dlc(self) -> int:  # TODO: get from the segmenter
        ...

    @dlc.setter
    def dlc(self, value: int):  # TODO: set in the segmenter
        ...

    @property
    def use_data_optimization(self) -> bool:  # TODO: get from the segmenter
        ...

    @use_data_optimization.setter
    def use_data_optimization(self, value: bool):  # TODO: set in the segmenter
        ...

    @property
    def filler_byte(self) -> RawByte:  # TODO: get from the segmenter
        ...

    @filler_byte.setter
    def filler_byte(self, value: RawByte):  # TODO: set in the segmenter
        ...

    # Flow Control configuration

    @property
    def flow_control_generator(self) -> FlowControlGenerator:
        ...

    @flow_control_generator.setter
    def flow_control_generator(self, value: FlowControlGenerator) -> None:
        ...

    # TODO: Packets Queues (received, scheduled)

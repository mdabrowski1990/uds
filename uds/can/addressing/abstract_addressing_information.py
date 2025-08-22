"""Abstract definition of Addressing Information handler."""

__all__ = ["AbstractCanAddressingInformation", "CANAddressingParams"]

from abc import ABC, abstractmethod
from typing import Any, Optional, TypedDict

from uds.addressing import AddressingType
from uds.addressing.abstract_addressing_information import AbstractAddressingInformation
from uds.can.addressing.addressing_format import CanAddressingFormat
from uds.utilities import RawBytesAlias


class CANAddressingParams(TypedDict, total=True):
    """:ref:`Addressing Information <knowledge-base-n-ai>` parameters collection for a single CAN Packet."""

    addressing_format: CanAddressingFormat
    addressing_type: AddressingType
    can_id: int
    target_address: Optional[int]
    source_address: Optional[int]
    address_extension: Optional[int]


class AbstractCanAddressingInformation(AbstractAddressingInformation, ABC):
    """Abstract definition of storage for addressing related parameters for UDS entity operating on CAN bus."""

    class InputAIParams(TypedDict, total=False):
        """:ref:`Addressing Information <knowledge-base-n-ai>` configuration parameters."""

        can_id: int
        target_address: Optional[int]
        source_address: Optional[int]
        address_extension: Optional[int]

    class CanIdAIParams(TypedDict, total=True):
        """ref:`Addressing Information <knowledge-base-n-ai>` parameters that are carried by CAN Identifier."""

        addressing_type: Optional[AddressingType]
        target_address: Optional[int]
        source_address: Optional[int]
        priority: Optional[int]

    class DataBytesAIParamsAlias(TypedDict, total=False):
        """Alias of :ref:`Addressing Information <knowledge-base-n-ai>` parameters encoded in data field."""

        target_address: int
        address_extension: int

    class DecodedAIParamsAlias(TypedDict, total=True):
        """Alias of :ref:`Addressing Information <knowledge-base-n-ai>` parameters encoded in CAN ID and data field."""

        addressing_type: Optional[AddressingType]
        target_address: Optional[int]
        source_address: Optional[int]
        address_extension: Optional[int]

    ADDRESSING_FORMAT: CanAddressingFormat
    """CAN Addressing Format used."""

    AI_DATA_BYTES_NUMBER: int
    """Number of CAN Frame data bytes that are used to carry UDS Addressing Information."""

    def __init__(self,
                 rx_physical_params: InputAIParams,
                 tx_physical_params: InputAIParams,
                 rx_functional_params: InputAIParams,
                 tx_functional_params: InputAIParams) -> None:
        """
        Configure Addresses of UDS Entity (either a server or a client) for UDS over CAN communication.

        :param rx_physical_params: Addressing parameters for incoming physically addressed communication.
        :param tx_physical_params: Addressing parameters for outgoing physically addressed communication.
        :param rx_functional_params: Addressing parameters for incoming functionally addressed communication.
        :param tx_functional_params: Addressing parameters for outgoing functionally addressed communication.
        """
        super().__init__(rx_physical_params=rx_physical_params,
                         tx_physical_params=tx_physical_params,
                         rx_functional_params=rx_functional_params,
                         tx_functional_params=tx_functional_params)

    @classmethod
    @abstractmethod
    def validate_addressing_params(cls,  # type: ignore  # pylint: disable=arguments-differ
                                   addressing_type: AddressingType,
                                   addressing_format: CanAddressingFormat,
                                   can_id: Optional[int] = None,
                                   target_address: Optional[int] = None,
                                   source_address: Optional[int] = None,
                                   address_extension: Optional[int] = None) -> CANAddressingParams:
        """
        Validate Addressing Information parameters of a CAN packet.

        :param addressing_type: Addressing type to validate.
        :param addressing_format: CAN Addressing Format used.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :raise UnusedArgumentError: At least one provided parameter is not supported by Addressing format used.
        :raise InconsistencyError: Provided values are not consistent with each other (cannot be used together)
            or with the Addressing format used.

        :return: Normalized dictionary with the provided information.
        """

    @staticmethod
    @abstractmethod
    def is_compatible_can_id(can_id: int,
                             addressing_type: Optional[AddressingType]) -> bool:
        """
        Check whether provided CAN ID is consistent with this CAN Addressing Format.

        :param can_id: Value of CAN ID to check.
        :param addressing_type: Addressing type for which consistency to be performed.
            Leave None to skip crosscheck between CAN Identifier and Addressing Type.

        :return: True if CAN ID value is compatible with this CAN Addressing Format, False otherwise.
        """

    @staticmethod
    @abstractmethod
    def decode_can_id_ai_params(can_id: int) -> CanIdAIParams:
        """
        Decode Addressing Information parameters from CAN Identifier.

        :param can_id: Value of a CAN Identifier.

        :return: Decoded Addressing Information parameters.
        """

    @staticmethod
    @abstractmethod
    def decode_data_bytes_ai_params(ai_data_bytes: RawBytesAlias) -> DataBytesAIParamsAlias:
        """
        Decode Addressing Information parameters from CAN data bytes.

        :param ai_data_bytes: Data bytes containing Addressing Information.

        :return: Decoded Addressing Information parameters.
        """

    @classmethod
    def decode_frame_ai_params(cls, can_id: int, raw_frame_data: RawBytesAlias) -> DecodedAIParamsAlias:
        """
        Decode Addressing Information parameters from a CAN Frame.

        :param can_id: CAN Identifier value of a CAN frame.
        :param raw_frame_data: Raw data bytes of a CAN frame.

        :return: Decoded Addressing Information parameters.
        """
        can_ai_params = cls.decode_can_id_ai_params(can_id)
        data_ai_params = cls.decode_data_bytes_ai_params(raw_frame_data[:cls.AI_DATA_BYTES_NUMBER])
        return cls.DecodedAIParamsAlias(
            addressing_type=can_ai_params["addressing_type"],
            target_address=data_ai_params.get("target_address", can_ai_params["target_address"]),
            source_address=can_ai_params["source_address"],
            address_extension=data_ai_params.get("address_extension", None)
        )

    @classmethod
    @abstractmethod
    def encode_ai_data_bytes(cls,
                             target_address: Optional[int] = None,
                             address_extension: Optional[int] = None) -> bytearray:
        """
        Generate data bytes that carry Addressing Information.

        :param target_address: Target Address value used.
        :param address_extension: Source Address value used.

        :return: Data bytes that carry Addressing Information in a CAN frame Data field.
        """

    def is_input_packet(self,  # type: ignore  # pylint: disable=arguments-differ
                        can_id: int,
                        raw_frame_data: RawBytesAlias,
                        **_: Any) -> Optional[AddressingType]:
        """
        Check if a frame with provided attributes is an input packet for this UDS Entity.

        :param raw_frame_data: Raw data bytes carried by a CAN frame to check.
        :param can_id: CAN Identifier of a CAN frame to check.

        :return: Addressing Type used for transmission of this packet, None otherwise.
        """
        decoded_frame_ai_params = self.decode_frame_ai_params(can_id=can_id, raw_frame_data=raw_frame_data)
        if (decoded_frame_ai_params["addressing_type"] in {None, AddressingType.PHYSICAL}
                and can_id == self.rx_physical_params["can_id"]
                and decoded_frame_ai_params["target_address"] == self.rx_physical_params["target_address"]
                and decoded_frame_ai_params["source_address"] == self.rx_physical_params["source_address"]
                and decoded_frame_ai_params["address_extension"] == self.rx_physical_params["address_extension"]):
            return AddressingType.PHYSICAL
        if (decoded_frame_ai_params["addressing_type"] in {None, AddressingType.FUNCTIONAL}
                and can_id == self.rx_functional_params["can_id"]
                and decoded_frame_ai_params["target_address"] == self.rx_functional_params["target_address"]
                and decoded_frame_ai_params["source_address"] == self.rx_functional_params["source_address"]
                and decoded_frame_ai_params["address_extension"] == self.rx_functional_params["address_extension"]):
            return AddressingType.FUNCTIONAL
        return None

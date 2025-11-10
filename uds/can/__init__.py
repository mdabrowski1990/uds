"""
A sub-package with CAN bus specific implementation.

It provides tools for:

- definition of CAN specific attributes:

    - CAN Addressing Formats
    - Flow Status

- handlers for CAN frame fields:

    - DLC
    - CAN ID

- handler for CAN specific packets:

    - Single Frame
    - First Frame
    - Consecutive Frame
    - Flow Status
"""
from .addressing import CanAddressingFormat, CanAddressingInformation
from .frame import DEFAULT_FILLER_BYTE, CanDlcHandler, CanIdHandler, CanVersion
from .packet import (
    AbstractFlowControlParametersGenerator,
    CanFlowStatus,
    CanPacket,
    CanPacketRecord,
    CanPacketType,
    CanSTminTranslator,
    DefaultFlowControlParametersGenerator,
)
from .segmenter import CanSegmenter
from .transport_interface import PyCanTransportInterface

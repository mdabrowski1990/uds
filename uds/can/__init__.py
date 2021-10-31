"""
A subpackage with CAN bus specific implementation.

It provides tools for:
 - creating new CAN packets
 - storing historic information about CAN packet that was either received or transmitted
 - definition of CAN specific attributes:
   - Packet Types
   - CAN Addressing Formats
   - Flow Status
 - handlers for CAN frame fields:
   - DLC
   - CAN ID
"""

from .addressing_format import CanAddressingFormat, CanAddressingFormatAlias
from .addressing_information import CanAddressingInformationHandler
from .can_frame_fields import DEFAULT_FILLER_BYTE, CanIdHandler, CanDlcHandler
from .packet_type import CanPacketType, CanPacketTypeAlias

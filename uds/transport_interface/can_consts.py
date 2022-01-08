"""Constants specific for CAN Transport Interfaces."""

__all__ = ["DEFAULT_FLOW_CONTROL_ARGS", "N_AS_TIMEOUT", "N_AR_TIMEOUT", "N_BS_TIMEOUT", "N_CR_TIMEOUT"]

from uds.transmission_attributes import AddressingType
from uds.packet import CanPacketType
from uds.can import CanFlowStatus, CanSTminTranslator


DEFAULT_FLOW_CONTROL_ARGS = {
    "packet_type": CanPacketType.FLOW_CONTROL,
    "flow_status": CanFlowStatus.ContinueToSend,
    "block_size": 0x10,
    "st_min": CanSTminTranslator.encode(0),
}
"""Default parameters of Flow Control CAN Packet."""

N_AS_TIMEOUT: int = 1000
"""Timeout value in milliseconds of :ref:`N_As <knowledge-base-can-n-as>` time parameter."""
N_AR_TIMEOUT: int = 1000
"""Timeout value in milliseconds of :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter."""
N_BS_TIMEOUT: int = 1000
"""Timeout value in milliseconds of :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter."""
N_CR_TIMEOUT: int = 1000
"""Timeout value in milliseconds of :ref:`N_Cr <knowledge-base-can-n-cr>` time parameter."""

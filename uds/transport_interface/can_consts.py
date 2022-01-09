"""Constants specific for CAN Transport Interfaces."""

__all__ = ["DEFAULT_FLOW_CONTROL_ARGS", "DEFAULT_N_BR", "DEFAULT_N_CS",
           "N_AS_TIMEOUT", "N_AR_TIMEOUT", "N_BS_TIMEOUT", "N_CR_TIMEOUT"]

from typing import Optional

from uds.utilities import TimeMilliseconds
from uds.packet import CanPacketType
from uds.can import CanFlowStatus, CanSTminTranslator


DEFAULT_FLOW_CONTROL_ARGS = {
    "packet_type": CanPacketType.FLOW_CONTROL,
    "flow_status": CanFlowStatus.ContinueToSend,
    "block_size": 0x10,
    "st_min": CanSTminTranslator.encode(0),
}
"""Default parameters of Flow Control CAN Packet."""

DEFAULT_N_BR: TimeMilliseconds = 0
# TODO: docstring
DEFAULT_N_CS: Optional[TimeMilliseconds] = None
# TODO: docstring

N_AS_TIMEOUT: TimeMilliseconds = 1000
"""Timeout value in milliseconds of :ref:`N_As <knowledge-base-can-n-as>` time parameter."""
N_AR_TIMEOUT: TimeMilliseconds = 1000
"""Timeout value in milliseconds of :ref:`N_Ar <knowledge-base-can-n-ar>` time parameter."""
N_BS_TIMEOUT: TimeMilliseconds = 1000
"""Timeout value in milliseconds of :ref:`N_Bs <knowledge-base-can-n-bs>` time parameter."""
N_CR_TIMEOUT: TimeMilliseconds = 1000
"""Timeout value in milliseconds of :ref:`N_Cr <knowledge-base-can-n-cr>` time parameter."""

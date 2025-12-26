""":ref:`ECUReset (SID 0x11) <knowledge-base-service-ecu-reset>` translation."""

__all__ = ["ECU_RESET"]

from uds.message import RequestSID

from ..data_record_definitions import CONDITIONAL_POWER_DOWN_TIME, ECU_RESET_SUB_FUNCTION
from ..service import Service

ECU_RESET = Service(request_sid=RequestSID.ECUReset,
                    request_structure=(ECU_RESET_SUB_FUNCTION,),
                    response_structure=(ECU_RESET_SUB_FUNCTION,
                                        CONDITIONAL_POWER_DOWN_TIME))
"""Default translator for :ref:`ECUReset <knowledge-base-service-ecu-reset>` service."""

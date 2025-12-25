"""Translation for :ref:`ControlDTCSetting (SID 0x85) <knowledge-base-service-control-dtc-setting>` service."""

__all__ = ["CONTROL_DTC_SETTING"]

from uds.message import RequestSID

from ..data_record_definitions import CONTROL_DTC_SETTING_SUB_FUNCTION, DTC_SETTING_CONTROL_OPTION_RECORD
from ..service import Service

CONTROL_DTC_SETTING = Service(request_sid=RequestSID.ControlDTCSetting,
                              request_structure=(CONTROL_DTC_SETTING_SUB_FUNCTION,
                                                 DTC_SETTING_CONTROL_OPTION_RECORD),
                              response_structure=(CONTROL_DTC_SETTING_SUB_FUNCTION,))
"""Default translator for :ref:`ControlDTCSetting <knowledge-base-service-control-dtc-setting>` service."""

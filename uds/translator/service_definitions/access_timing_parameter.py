"""Translation for :ref:`AccessTimingParameter (SID 0x83) <knowledge-base-service-access-timing-parameter>` service."""

__all__ = ["ACCESS_TIMING_PARAMETER_2013"]

from uds.message import RequestSID

from ..data_record_definitions import (
    ACCESS_TIMING_PARAMETER_SUB_FUNCTION_2013,
    CONDITIONAL_ACCESS_TIMING_PARAMETER_REQUEST_2013,
    CONDITIONAL_ACCESS_TIMING_PARAMETER_RESPONSE_2013,
)
from ..service import Service

ACCESS_TIMING_PARAMETER_2013 = Service(request_sid=RequestSID.AccessTimingParameter,
                                       request_structure=(ACCESS_TIMING_PARAMETER_SUB_FUNCTION_2013,
                                                          CONDITIONAL_ACCESS_TIMING_PARAMETER_REQUEST_2013),
                                       response_structure=(ACCESS_TIMING_PARAMETER_SUB_FUNCTION_2013,
                                                           CONDITIONAL_ACCESS_TIMING_PARAMETER_RESPONSE_2013))
"""Translator for :ref:`AccessTimingParameter <knowledge-base-service-access-timing-parameter>` service
compatible with ISO 14229-1:2013."""

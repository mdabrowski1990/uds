""":ref:`ClearDiagnosticInformation (SID 0x14) <knowledge-base-service-clear-diagnostic-information>` translation."""

__all__ = ["CLEAR_DIAGNOSTIC_INFORMATION", "CLEAR_DIAGNOSTIC_INFORMATION_2020", "CLEAR_DIAGNOSTIC_INFORMATION_2013"]

from uds.message import RequestSID

from ..data_record_definitions import GROUP_OF_DTC, OPTIONAL_MEMORY_SELECTION
from ..service import Service

CLEAR_DIAGNOSTIC_INFORMATION_2020 = Service(request_sid=RequestSID.ClearDiagnosticInformation,
                                            request_structure=(GROUP_OF_DTC, OPTIONAL_MEMORY_SELECTION),
                                            response_structure=())
"""Translator for :ref:`ClearDiagnosticInformation <knowledge-base-service-clear-diagnostic-information>` service
compatible with ISO 14229-1:2020."""

CLEAR_DIAGNOSTIC_INFORMATION_2013 = Service(request_sid=RequestSID.ClearDiagnosticInformation,
                                            request_structure=(GROUP_OF_DTC,),
                                            response_structure=())
"""Translator for :ref:`ClearDiagnosticInformation <knowledge-base-service-clear-diagnostic-information>` service
compatible with ISO 14229-1:2013."""

CLEAR_DIAGNOSTIC_INFORMATION = CLEAR_DIAGNOSTIC_INFORMATION_2020
"""Default translator for :ref:`ClearDiagnosticInformation <knowledge-base-service-clear-diagnostic-information>`
service."""

"""Translation for TesterPresent (SID 0x3E) service."""

__all__ = ["TESTER_PRESENT"]

from uds.message import RequestSID
from .service import Service
from ..data_record import RawDataRecord, MappingDataRecord

ZERO_SUB_FUNCTION = RawDataRecord(name="zeroSubFunction",
                                  length=7)
SPRMIB = MappingDataRecord(name="suppressPosRspMsgIndicationBit",
                           length=1,
                           values_mapping={
                               1: "yes",
                               0: "no",
                           })
TESTER_PRESENT_SUB_FUNCTION = RawDataRecord(name="SubFunction",
                                            length=8,
                                            children=[SPRMIB, ZERO_SUB_FUNCTION])
TESTER_PRESENT = Service(request_sid=RequestSID.TesterPresent,
                         request_structure=[TESTER_PRESENT_SUB_FUNCTION],
                         response_structure=[TESTER_PRESENT_SUB_FUNCTION])

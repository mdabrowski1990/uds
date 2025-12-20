""":ref:`RID <knowledge-base-rid>` related constants."""

__all__ = [
    "RID_BIT_LENGTH",
    "RID_MAPPING",
]

from typing import Dict

RID_BIT_LENGTH = 16

RID_MAPPING: Dict[int, str] = {
    0xE200: "Execute SPL",
    0xE201: "Execute DeployLoopRoutineID",
    0xFF00: "eraseMemory",
    0xFF01: "checkProgrammingDependencies",
}
""":ref:`:Routine Identifiers mapping according to ISO 14229-1 <knowledge-base-rid>`."""

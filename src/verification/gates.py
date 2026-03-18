from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class VerificationGate(str, Enum):
    GATE_A_INPUT_INTEGRITY = "gate_a_input_integrity"
    GATE_B_CONSENSUS_INTEGRITY = "gate_b_consensus_integrity"
    GATE_C_COMPLIANCE_INTEGRITY = "gate_c_compliance_integrity"
    GATE_D_CAUSALITY_INTEGRITY = "gate_d_causality_integrity"


@dataclass
class GateResult:
    gate: VerificationGate
    passed: bool
    notes: List[str]


def all_required_gates_passed(results: List[GateResult]) -> bool:
    return all(r.passed for r in results)

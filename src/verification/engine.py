from __future__ import annotations

from dataclasses import dataclass
from typing import List

from src.verification.gates import GateResult, all_required_gates_passed


@dataclass
class VerificationSummary:
    overall_passed: bool
    total_checks: int
    failed_checks: int


def summarize_gate_results(results: List[GateResult]) -> VerificationSummary:
    failed = len([r for r in results if not r.passed])
    return VerificationSummary(
        overall_passed=all_required_gates_passed(results),
        total_checks=len(results),
        failed_checks=failed,
    )

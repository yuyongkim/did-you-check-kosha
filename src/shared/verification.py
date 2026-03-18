"""Shared verification primitives used by all discipline verification modules.

Centralises ValidationIssue, LayerResult, issue_from_flag, has_blocking_issue,
split_flags, and dispersion so they are defined exactly once.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from statistics import median
from typing import Any, Dict, List

from src.shared.red_flags import get_flag, is_known_flag


@dataclass
class ValidationIssue:
    code: str
    severity: str
    message: str
    standard_reference: str
    auto_action: str


@dataclass
class LayerResult:
    layer: str
    passed: bool
    issues: List[ValidationIssue]
    details: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "layer": self.layer,
            "passed": self.passed,
            "issues": [asdict(i) for i in self.issues],
            "details": self.details,
        }


def issue_from_flag(code: str, message: str, standard_reference: str) -> ValidationIssue:
    if is_known_flag(code):
        flag = get_flag(code)
        return ValidationIssue(
            code=code,
            severity=flag.severity.value,
            message=message,
            standard_reference=standard_reference,
            auto_action=flag.auto_action,
        )
    return ValidationIssue(
        code=code,
        severity="high",
        message=message,
        standard_reference=standard_reference,
        auto_action="request_data_review",
    )


def has_blocking_issue(issues: List[ValidationIssue]) -> bool:
    return any(i.severity in {"critical", "high"} for i in issues)


def split_flags(issues: List[ValidationIssue]) -> Dict[str, List[str]]:
    red_flags: List[str] = []
    warnings: List[str] = []
    for issue in issues:
        if issue.severity in {"critical", "high"}:
            red_flags.append(issue.code)
        else:
            warnings.append(issue.code)
    return {"red_flags": sorted(set(red_flags)), "warnings": sorted(set(warnings))}


def dispersion(vals: List[float]) -> float:
    """Maximum pairwise relative difference across a list of values."""
    max_rel = 0.0
    for i in range(len(vals)):
        for j in range(i + 1, len(vals)):
            base = max(abs(vals[i]), abs(vals[j]), 1e-12)
            rel = abs(vals[i] - vals[j]) / base
            max_rel = max(max_rel, rel)
    return max_rel


def median_of(vals: List[float]) -> float:
    return float(median(vals))

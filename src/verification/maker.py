from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Literal

from src.shared.errors import ConsensusError


@dataclass
class NumericConsensusResult:
    agreed_value: float
    agreement_count: int
    tolerance: float


def numeric_consensus(values: List[float], tolerance: float = 0.01, k_threshold: int = 2) -> NumericConsensusResult:
    if len(values) < k_threshold:
        raise ConsensusError("Not enough values for k-threshold")

    best_group: List[float] = []
    for v in values:
        group = [x for x in values if _relative_diff(v, x) <= tolerance]
        if len(group) > len(best_group):
            best_group = group

    if len(best_group) < k_threshold:
        raise ConsensusError("No consensus within tolerance")

    agreed = sum(best_group) / len(best_group)
    return NumericConsensusResult(agreed_value=agreed, agreement_count=len(best_group), tolerance=tolerance)


def categorical_consensus(values: List[str], k_threshold: int = 2) -> str:
    counts = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    winner, score = max(counts.items(), key=lambda item: item[1])
    if score < k_threshold:
        raise ConsensusError("No categorical consensus")
    return winner


def _relative_diff(a: float, b: float) -> float:
    base = max(abs(a), abs(b), 1e-12)
    return abs(a - b) / base

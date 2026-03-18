from __future__ import annotations

from dataclasses import dataclass
from typing import List

from src.workflows.steps import STANDARD_WORKFLOW_STEPS


@dataclass(frozen=True)
class StandardWorkflow:
    workflow_id: str = "standard_calculation"

    def steps(self) -> List[str]:
        return list(STANDARD_WORKFLOW_STEPS)

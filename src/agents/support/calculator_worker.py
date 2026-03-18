from __future__ import annotations

from typing import Dict, Protocol


class CalculatorWorker(Protocol):
    def execute(self, task_name: str, inputs: Dict[str, object]) -> Dict[str, object]:
        ...

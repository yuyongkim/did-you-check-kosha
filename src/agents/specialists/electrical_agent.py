from __future__ import annotations

from typing import Dict

from src.agents.runtime import AgentRuntime
from src.electrical.service import ElectricalVerificationService


class ElectricalSpecialistAgent:
    """Electrical specialist agent backed by electrical verification engine."""

    def __init__(self, service: ElectricalVerificationService | None = None) -> None:
        self.service = service or ElectricalVerificationService()

    def handle_calculation(self, payload: Dict[str, object], runtime: AgentRuntime) -> Dict[str, object]:
        _ = runtime
        calculation_type = str(payload.get("calculation_type", "electrical_integrity"))
        input_data = payload.get("input_data", {})
        if not isinstance(input_data, dict):
            input_data = {}

        result = self.service.evaluate(input_data, calculation_type=calculation_type)
        flags = result.get("flags", {"red_flags": [], "warnings": []})
        red_flags = flags.get("red_flags", []) if isinstance(flags, dict) else []

        status = "success"
        if isinstance(red_flags, list) and red_flags:
            status = "error"

        final_results = result.get("final_results", {})
        if not isinstance(final_results, dict):
            final_results = {}

        references = []
        for step in result.get("calculation_steps", []):
            if isinstance(step, dict) and "standard_reference" in step:
                references.append(step["standard_reference"])

        return {
            "status": status,
            "discipline": "electrical",
            "results": final_results,
            "details": result,
            "references": references,
            "verification": {
                "layers": result.get("layer_results", []),
                "confidence": result.get("calculation_summary", {}).get("confidence", "low"),
            },
            "flags": flags,
        }


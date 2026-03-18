from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from src.agents.runtime import AgentRuntime


@dataclass
class MockSpecialist:
    name: str
    discipline: str

    def handle_calculation(self, payload: Dict[str, object], runtime: AgentRuntime) -> Dict[str, object]:
        calculator = runtime.require("calculator_worker")
        verifier = runtime.require("verification_agent")
        spec_explorer = runtime.require("spec_explorer")

        calc_type = str(payload.get("calculation_type", "generic"))
        input_data = payload.get("input_data", {})
        if not isinstance(input_data, dict):
            input_data = {}

        citation = spec_explorer.extract_table_value(
            standard="ASME B31.3",
            table="Table A-1",
            lookup_conditions={"discipline": self.discipline},
        )
        calc_result = calculator.execute(calc_type, input_data)
        verification = verifier.run_verification(
            "maker_voting",
            {"discipline": self.discipline, "calculation_type": calc_type, "result": calc_result},
        )

        return {
            "status": "success" if calc_result.get("status") == "success" else "error",
            "discipline": self.discipline,
            "results": calc_result.get("results", {}),
            "references": [citation.get("source", {})],
            "verification": verification,
            "flags": {"red_flags": [], "warnings": []},
        }


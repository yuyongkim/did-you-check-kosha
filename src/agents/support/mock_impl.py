from __future__ import annotations

from typing import Dict, List


class MockSpecExplorer:
    def search_standard(
        self,
        query: str,
        discipline: str | None = None,
        filters: Dict[str, object] | None = None,
    ) -> List[Dict[str, object]]:
        return [
            {
                "query": query,
                "discipline": discipline,
                "filters": filters or {},
                "citation": {
                    "standard": "ASME B31.3",
                    "section_or_table": "Table A-1",
                    "page": 123,
                    "version": "2020",
                },
                "conditions": ["mock_condition"],
            }
        ]

    def extract_table_value(
        self,
        standard: str,
        table: str,
        lookup_conditions: Dict[str, object],
    ) -> Dict[str, object]:
        return {
            "value": 19100,
            "unit": "psi",
            "source": {
                "standard": standard,
                "section_or_table": table,
                "page": 123,
                "version": "2020",
            },
            "conditions": [f"lookup:{lookup_conditions}"],
            "interpolation": {"required": False, "method": None, "reference": None},
        }


class MockCalculatorWorker:
    def execute(self, task_name: str, inputs: Dict[str, object]) -> Dict[str, object]:
        if task_name == "remaining_life":
            t_current = float(inputs.get("t_current_mm", 8.0))
            t_min = float(inputs.get("t_min_mm", 5.0))
            corrosion_rate = float(inputs.get("corrosion_rate_mm_per_year", 0.2))
            if corrosion_rate <= 0:
                return {"status": "error", "error": "invalid corrosion rate"}
            remaining_life = (t_current - t_min) / corrosion_rate
            return {
                "status": "success",
                "results": {
                    "remaining_life_years": round(remaining_life, 3),
                    "corrosion_rate_mm_per_year": corrosion_rate,
                    "minimum_thickness_mm": t_min,
                },
            }

        return {"status": "success", "results": {"task": task_name, "echo": dict(inputs)}}


class MockVerificationAgent:
    def run_verification(self, verification_type: str, payload: Dict[str, object]) -> Dict[str, object]:
        if verification_type == "maker_voting":
            return {
                "status": "success",
                "verification_type": verification_type,
                "passed": True,
                "flags": {"red_flags": [], "warnings": []},
            }
        return {
            "status": "success",
            "verification_type": verification_type,
            "passed": True,
            "flags": {"red_flags": [], "warnings": []},
        }


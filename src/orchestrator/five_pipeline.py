from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping

from src.cross_discipline.validator import CrossDisciplineValidator
from src.orchestrator.orchestrator import Orchestrator
from src.orchestrator.state_machine import OrchestratorState
from src.shared.message_factory import create_message
from src.workflows.runner import WorkflowRunner


@dataclass
class FivePipelineResult:
    status: str
    state: str
    piping: Mapping[str, Any]
    vessel: Mapping[str, Any]
    rotating: Mapping[str, Any]
    electrical: Mapping[str, Any]
    instrumentation: Mapping[str, Any]
    cross_discipline: Mapping[str, Any]
    blocking_flags: bool


class FiveDisciplinePipelineService:
    """Runs 5-discipline calculations and integrated cross-discipline checks."""

    def __init__(self, orchestrator: Orchestrator, cross_validator: CrossDisciplineValidator | None = None) -> None:
        self.orchestrator = orchestrator
        self.cross_validator = cross_validator or CrossDisciplineValidator()

    def run(
        self,
        *,
        piping_input: Mapping[str, Any],
        vessel_input: Mapping[str, Any],
        rotating_input: Mapping[str, Any],
        electrical_input: Mapping[str, Any],
        instrumentation_input: Mapping[str, Any],
    ) -> FivePipelineResult:
        run = self.orchestrator.start_run("standard_calculation")
        WorkflowRunner.run_standard_happy_path(self.orchestrator)

        piping_result = self.orchestrator.handle_message(
            create_message(
                message_type="calculation_request",
                from_agent="orchestrator",
                to_agent="piping_specialist",
                payload={"calculation_type": "remaining_life", "input_data": dict(piping_input)},
                correlation_id=run.trace.correlation_id,
                trace_id=run.trace.trace_id,
                meta={"workflow_id": "standard_calculation", "discipline": "piping"},
            )
        )
        vessel_result = self.orchestrator.handle_message(
            create_message(
                message_type="calculation_request",
                from_agent="orchestrator",
                to_agent="static_equipment_specialist",
                payload={"calculation_type": "vessel_integrity", "input_data": dict(vessel_input)},
                correlation_id=run.trace.correlation_id,
                trace_id=run.trace.trace_id,
                meta={"workflow_id": "standard_calculation", "discipline": "vessel"},
            )
        )
        rotating_result = self.orchestrator.handle_message(
            create_message(
                message_type="calculation_request",
                from_agent="orchestrator",
                to_agent="rotating_specialist",
                payload={"calculation_type": "rotating_integrity", "input_data": dict(rotating_input)},
                correlation_id=run.trace.correlation_id,
                trace_id=run.trace.trace_id,
                meta={"workflow_id": "standard_calculation", "discipline": "rotating"},
            )
        )
        electrical_result = self.orchestrator.handle_message(
            create_message(
                message_type="calculation_request",
                from_agent="orchestrator",
                to_agent="electrical_specialist",
                payload={"calculation_type": "electrical_integrity", "input_data": dict(electrical_input)},
                correlation_id=run.trace.correlation_id,
                trace_id=run.trace.trace_id,
                meta={"workflow_id": "standard_calculation", "discipline": "electrical"},
            )
        )
        instrumentation_result = self.orchestrator.handle_message(
            create_message(
                message_type="calculation_request",
                from_agent="orchestrator",
                to_agent="instrumentation_specialist",
                payload={"calculation_type": "instrumentation_integrity", "input_data": dict(instrumentation_input)},
                correlation_id=run.trace.correlation_id,
                trace_id=run.trace.trace_id,
                meta={"workflow_id": "standard_calculation", "discipline": "instrumentation"},
            )
        )

        cross_payload = self._build_cross_payload(
            piping_result,
            vessel_result,
            rotating_result,
            electrical_result,
            instrumentation_result,
        )
        cross_result = self.cross_validator.evaluate(cross_payload)

        for code in cross_result.get("flags", {}).get("red_flags", []):
            if isinstance(code, str):
                try:
                    self.orchestrator.add_flag(code)
                except Exception:
                    pass

        status = "completed"
        if self.orchestrator.has_blocking_flag() or cross_result.get("status") == "blocked":
            status = "blocked"
        elif self.orchestrator.can_release():
            self.orchestrator.advance(OrchestratorState.COMPLETED)
            status = "completed"

        return FivePipelineResult(
            status=status,
            state=run.state_machine.state.value,
            piping=piping_result,
            vessel=vessel_result,
            rotating=rotating_result,
            electrical=electrical_result,
            instrumentation=instrumentation_result,
            cross_discipline=cross_result,
            blocking_flags=self.orchestrator.has_blocking_flag(),
        )

    @staticmethod
    def _build_cross_payload(
        piping_result: Mapping[str, Any],
        vessel_result: Mapping[str, Any],
        rotating_result: Mapping[str, Any],
        electrical_result: Mapping[str, Any],
        instrumentation_result: Mapping[str, Any],
    ) -> Dict[str, Any]:
        p_details = piping_result.get("details", {})
        v_details = vessel_result.get("details", {})
        r_details = rotating_result.get("details", {})
        e_details = electrical_result.get("details", {})
        i_details = instrumentation_result.get("details", {})

        p_input = p_details.get("input_data", {}) if isinstance(p_details, Mapping) else {}
        v_input = v_details.get("input_data", {}) if isinstance(v_details, Mapping) else {}

        p_final = piping_result.get("results", {})
        v_final = vessel_result.get("results", {})
        r_final = rotating_result.get("results", {})
        e_final = electrical_result.get("results", {})
        i_final = instrumentation_result.get("results", {})

        return {
            "piping": {
                "current_thickness_mm": p_input.get("thickness_history", [{}])[-1].get("thickness_mm")
                if isinstance(p_input.get("thickness_history"), list) and p_input.get("thickness_history")
                else p_input.get("current_thickness_mm"),
                "t_min_mm": p_final.get("t_min_mm"),
                "remaining_life_years": p_final.get("remaining_life_years"),
                "nps_inch": p_input.get("nps"),
            },
            "vessel": {
                "current_thickness_mm": v_input.get("current_thickness_mm") or v_input.get("t_current_mm"),
                "t_required_shell_mm": v_final.get("t_required_shell_mm"),
                "remaining_life_years": v_final.get("remaining_life_years"),
            },
            "rotating": {
                "vibration_mm_per_s": r_final.get("vibration_mm_per_s"),
                "vibration_limit_mm_per_s": r_final.get("vibration_limit_mm_per_s"),
                "nozzle_load_ratio": r_final.get("nozzle_load_ratio"),
                "bearing_health_index": r_final.get("bearing_health_index"),
                "bearing_temperature_c": r_final.get("bearing_temperature_c"),
            },
            "electrical": {
                "motor_current_thd_percent": e_final.get("motor_current_thd_percent"),
                "thd_voltage_percent": e_final.get("thd_voltage_percent"),
                "power_factor": e_final.get("power_factor"),
            },
            "instrumentation": {
                "predicted_drift_pct": i_final.get("predicted_drift_pct"),
                "drift_r_squared": i_final.get("drift_r_squared"),
                "pfdavg": i_final.get("pfdavg"),
                "sil_target": i_final.get("sil_target"),
            },
        }

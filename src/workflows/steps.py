from __future__ import annotations

STANDARD_WORKFLOW_STEPS = [
    "input_validation",
    "discipline_classification",
    "standards_identification",
    "spec_extraction",
    "parallel_calculation",
    "cross_verification",
    "final_validation",
    "report_generation",
]

EMERGENCY_WORKFLOW_STEPS = [
    "input_validation",
    "discipline_classification",
    "critical_condition_check",
    "focused_spec_extraction",
    "focused_calculation",
    "strict_validation",
    "escalation_report_generation",
]

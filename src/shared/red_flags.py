from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict


class RedFlagSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RedFlagCategory(str, Enum):
    PHY = "PHY"
    STD = "STD"
    UNIT = "UNIT"
    LOG = "LOG"
    DATA = "DATA"
    FMT = "FMT"
    OPS = "OPS"


@dataclass(frozen=True)
class RedFlagDefinition:
    code: str
    severity: RedFlagSeverity
    category: RedFlagCategory
    blocking: bool
    auto_action: str
    human_review_required: bool


RED_FLAG_REGISTRY: Dict[str, RedFlagDefinition] = {
    "PHY.NEGATIVE_THICKNESS": RedFlagDefinition("PHY.NEGATIVE_THICKNESS", RedFlagSeverity.CRITICAL, RedFlagCategory.PHY, True, "terminate_workflow", True),
    "PHY.NEGATIVE_REMAINING_LIFE": RedFlagDefinition("PHY.NEGATIVE_REMAINING_LIFE", RedFlagSeverity.CRITICAL, RedFlagCategory.PHY, True, "terminate_workflow", True),
    "PHY.UNREALISTIC_CORROSION_RATE": RedFlagDefinition("PHY.UNREALISTIC_CORROSION_RATE", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.UNREALISTIC_REMAINING_LIFE": RedFlagDefinition("PHY.UNREALISTIC_REMAINING_LIFE", RedFlagSeverity.MEDIUM, RedFlagCategory.PHY, False, "request_data_review", False),
    "PHY.ALLOWABLE_STRESS_EXCEEDED": RedFlagDefinition("PHY.ALLOWABLE_STRESS_EXCEEDED", RedFlagSeverity.CRITICAL, RedFlagCategory.PHY, True, "terminate_workflow", True),
    "PHY.CURRENT_THICKNESS_BELOW_MINIMUM": RedFlagDefinition("PHY.CURRENT_THICKNESS_BELOW_MINIMUM", RedFlagSeverity.CRITICAL, RedFlagCategory.PHY, True, "terminate_workflow", True),
    "PHY.TEMPERATURE_LIMIT_EXCEEDED": RedFlagDefinition("PHY.TEMPERATURE_LIMIT_EXCEEDED", RedFlagSeverity.CRITICAL, RedFlagCategory.PHY, True, "terminate_workflow", True),
    "PHY.VIBRATION_LIMIT_EXCEEDED": RedFlagDefinition("PHY.VIBRATION_LIMIT_EXCEEDED", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.NOZZLE_LOAD_EXCEEDED": RedFlagDefinition("PHY.NOZZLE_LOAD_EXCEEDED", RedFlagSeverity.CRITICAL, RedFlagCategory.PHY, True, "terminate_workflow", True),
    "PHY.BEARING_TEMPERATURE_HIGH": RedFlagDefinition("PHY.BEARING_TEMPERATURE_HIGH", RedFlagSeverity.MEDIUM, RedFlagCategory.PHY, False, "monitor_closely", False),
    "PHY.STEAM_WETNESS_EROSION_RISK": RedFlagDefinition("PHY.STEAM_WETNESS_EROSION_RISK", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.STEAM_PHASE_CHANGE_RISK": RedFlagDefinition("PHY.STEAM_PHASE_CHANGE_RISK", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.NOZZLE_INTERFACE_OVERLOAD": RedFlagDefinition("PHY.NOZZLE_INTERFACE_OVERLOAD", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.VIBRATION_TO_PIPING_STRESS_RISK": RedFlagDefinition("PHY.VIBRATION_TO_PIPING_STRESS_RISK", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.VESSEL_PULSATION_RISK": RedFlagDefinition("PHY.VESSEL_PULSATION_RISK", RedFlagSeverity.MEDIUM, RedFlagCategory.PHY, False, "monitor_closely", False),
    "PHY.VESSEL_HIGH_LD_RATIO": RedFlagDefinition("PHY.VESSEL_HIGH_LD_RATIO", RedFlagSeverity.MEDIUM, RedFlagCategory.PHY, False, "monitor_closely", False),
    "PHY.VESSEL_EXTERNAL_PRESSURE_REVIEW": RedFlagDefinition("PHY.VESSEL_EXTERNAL_PRESSURE_REVIEW", RedFlagSeverity.MEDIUM, RedFlagCategory.PHY, False, "request_data_review", False),
    "PHY.VESSEL_EXTERNAL_PRESSURE_RISK": RedFlagDefinition("PHY.VESSEL_EXTERNAL_PRESSURE_RISK", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.VESSEL_NOZZLE_REINFORCEMENT_REVIEW": RedFlagDefinition("PHY.VESSEL_NOZZLE_REINFORCEMENT_REVIEW", RedFlagSeverity.MEDIUM, RedFlagCategory.PHY, False, "request_data_review", False),
    "PHY.VESSEL_NOZZLE_REINFORCEMENT_RISK": RedFlagDefinition("PHY.VESSEL_NOZZLE_REINFORCEMENT_RISK", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.TRANSFORMER_HEALTH_CRITICAL": RedFlagDefinition("PHY.TRANSFORMER_HEALTH_CRITICAL", RedFlagSeverity.CRITICAL, RedFlagCategory.PHY, True, "terminate_workflow", True),
    "PHY.ARC_FLASH_ENERGY_EXCEEDED": RedFlagDefinition("PHY.ARC_FLASH_ENERGY_EXCEEDED", RedFlagSeverity.CRITICAL, RedFlagCategory.PHY, True, "terminate_workflow", True),
    "PHY.VOLTAGE_DROP_EXCEEDED": RedFlagDefinition("PHY.VOLTAGE_DROP_EXCEEDED", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.BREAKER_INTERRUPT_RATING_EXCEEDED": RedFlagDefinition("PHY.BREAKER_INTERRUPT_RATING_EXCEEDED", RedFlagSeverity.CRITICAL, RedFlagCategory.PHY, True, "terminate_workflow", True),
    "PHY.HARMONIC_DISTORTION_EXCEEDED": RedFlagDefinition("PHY.HARMONIC_DISTORTION_EXCEEDED", RedFlagSeverity.MEDIUM, RedFlagCategory.PHY, False, "monitor_closely", False),
    "PHY.SIL_TARGET_NOT_MET": RedFlagDefinition("PHY.SIL_TARGET_NOT_MET", RedFlagSeverity.CRITICAL, RedFlagCategory.PHY, True, "terminate_workflow", True),
    "PHY.DRIFT_RATE_EXCEEDED": RedFlagDefinition("PHY.DRIFT_RATE_EXCEEDED", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.SENSOR_MTBF_LOW": RedFlagDefinition("PHY.SENSOR_MTBF_LOW", RedFlagSeverity.MEDIUM, RedFlagCategory.PHY, False, "monitor_closely", False),
    "PHY.CONTROL_VALVE_CAPACITY_LOW": RedFlagDefinition("PHY.CONTROL_VALVE_CAPACITY_LOW", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.ELECTRICAL_TO_ROTATING_COUPLING_RISK": RedFlagDefinition("PHY.ELECTRICAL_TO_ROTATING_COUPLING_RISK", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.INSTRUMENT_TO_PIPING_COUPLING_RISK": RedFlagDefinition("PHY.INSTRUMENT_TO_PIPING_COUPLING_RISK", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.ELECTRICAL_NOISE_TO_SIS_RISK": RedFlagDefinition("PHY.ELECTRICAL_NOISE_TO_SIS_RISK", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.STRUCTURAL_DC_CRITICAL": RedFlagDefinition("PHY.STRUCTURAL_DC_CRITICAL", RedFlagSeverity.CRITICAL, RedFlagCategory.PHY, True, "terminate_workflow", True),
    "PHY.STRUCTURAL_DC_OVERSTRESSED": RedFlagDefinition("PHY.STRUCTURAL_DC_OVERSTRESSED", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.STEEL_CORROSION_SECTION_LOSS_HIGH": RedFlagDefinition("PHY.STEEL_CORROSION_SECTION_LOSS_HIGH", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.STEEL_DEFLECTION_EXCEEDED": RedFlagDefinition("PHY.STEEL_DEFLECTION_EXCEEDED", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.CONNECTION_FAILURE_DETECTED": RedFlagDefinition("PHY.CONNECTION_FAILURE_DETECTED", RedFlagSeverity.CRITICAL, RedFlagCategory.PHY, True, "terminate_workflow", True),
    "PHY.CIVIL_FLEXURE_OVERSTRESS": RedFlagDefinition("PHY.CIVIL_FLEXURE_OVERSTRESS", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.CIVIL_SUBSTANTIAL_DAMAGE": RedFlagDefinition("PHY.CIVIL_SUBSTANTIAL_DAMAGE", RedFlagSeverity.CRITICAL, RedFlagCategory.PHY, True, "terminate_workflow", True),
    "PHY.CIVIL_CARBONATION_CORROSION_INITIATED": RedFlagDefinition("PHY.CIVIL_CARBONATION_CORROSION_INITIATED", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.CIVIL_CRACK_WIDTH_EXCEEDED": RedFlagDefinition("PHY.CIVIL_CRACK_WIDTH_EXCEEDED", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.CIVIL_SPALLING_SEVERE": RedFlagDefinition("PHY.CIVIL_SPALLING_SEVERE", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.CIVIL_FOUNDATION_SETTLEMENT_HIGH": RedFlagDefinition("PHY.CIVIL_FOUNDATION_SETTLEMENT_HIGH", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.STRUCTURE_TO_PIPING_OVERLOAD_RISK": RedFlagDefinition("PHY.STRUCTURE_TO_PIPING_OVERLOAD_RISK", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.STRUCTURE_TO_PIPING_DEFLECTION_RISK": RedFlagDefinition("PHY.STRUCTURE_TO_PIPING_DEFLECTION_RISK", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.FOUNDATION_TO_ROTATING_MISALIGNMENT_RISK": RedFlagDefinition("PHY.FOUNDATION_TO_ROTATING_MISALIGNMENT_RISK", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.FOUNDATION_CRACK_VIBRATION_COUPLING": RedFlagDefinition("PHY.FOUNDATION_CRACK_VIBRATION_COUPLING", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "PHY.STRUCTURE_SUPPORT_ELECTRICAL_RISK": RedFlagDefinition("PHY.STRUCTURE_SUPPORT_ELECTRICAL_RISK", RedFlagSeverity.MEDIUM, RedFlagCategory.PHY, False, "request_data_review", False),
    "PHY.STRUCTURE_TO_SIS_RELIABILITY_RISK": RedFlagDefinition("PHY.STRUCTURE_TO_SIS_RELIABILITY_RISK", RedFlagSeverity.HIGH, RedFlagCategory.PHY, True, "strict_revalidation", True),
    "STD.INVALID_REFERENCE": RedFlagDefinition("STD.INVALID_REFERENCE", RedFlagSeverity.CRITICAL, RedFlagCategory.STD, True, "terminate_workflow", True),
    "STD.OUT_OF_SCOPE_APPLICATION": RedFlagDefinition("STD.OUT_OF_SCOPE_APPLICATION", RedFlagSeverity.HIGH, RedFlagCategory.STD, True, "strict_revalidation", True),
    "STD.TEMPERATURE_OVERRIDE_REVIEW_REQUIRED": RedFlagDefinition("STD.TEMPERATURE_OVERRIDE_REVIEW_REQUIRED", RedFlagSeverity.MEDIUM, RedFlagCategory.STD, False, "request_data_review", True),
    "STD.STEAM_TABLE_LOOKUP_REQUIRED": RedFlagDefinition("STD.STEAM_TABLE_LOOKUP_REQUIRED", RedFlagSeverity.HIGH, RedFlagCategory.STD, True, "request_missing_data", True),
    "STD.UNAPPROVED_MATERIAL": RedFlagDefinition("STD.UNAPPROVED_MATERIAL", RedFlagSeverity.HIGH, RedFlagCategory.STD, True, "strict_revalidation", True),
    "STD.JOINT_EFFICIENCY_INVALID": RedFlagDefinition("STD.JOINT_EFFICIENCY_INVALID", RedFlagSeverity.HIGH, RedFlagCategory.STD, True, "strict_revalidation", True),
    "UNIT.MIXED_SYSTEM_DETECTED": RedFlagDefinition("UNIT.MIXED_SYSTEM_DETECTED", RedFlagSeverity.HIGH, RedFlagCategory.UNIT, True, "strict_revalidation", True),
    "UNIT.CONVERSION_MISMATCH": RedFlagDefinition("UNIT.CONVERSION_MISMATCH", RedFlagSeverity.HIGH, RedFlagCategory.UNIT, True, "strict_revalidation", True),
    "LOG.NO_CONSENSUS_AFTER_TIEBREAKER": RedFlagDefinition("LOG.NO_CONSENSUS_AFTER_TIEBREAKER", RedFlagSeverity.CRITICAL, RedFlagCategory.LOG, True, "escalate_human", True),
    "LOG.REVERSE_CHECK_DEVIATION": RedFlagDefinition("LOG.REVERSE_CHECK_DEVIATION", RedFlagSeverity.MEDIUM, RedFlagCategory.LOG, False, "request_data_review", False),
    "LOG.STEAM_STATE_INCONSISTENT": RedFlagDefinition("LOG.STEAM_STATE_INCONSISTENT", RedFlagSeverity.MEDIUM, RedFlagCategory.LOG, False, "request_data_review", False),
    "LOG.CROSS_DISCIPLINE_MISMATCH": RedFlagDefinition("LOG.CROSS_DISCIPLINE_MISMATCH", RedFlagSeverity.MEDIUM, RedFlagCategory.LOG, False, "request_data_review", False),
    "LOG.DRIFT_MODEL_LOW_CONFIDENCE": RedFlagDefinition("LOG.DRIFT_MODEL_LOW_CONFIDENCE", RedFlagSeverity.MEDIUM, RedFlagCategory.LOG, False, "request_data_review", False),
    "DATA.MISSING_MANDATORY_FIELD": RedFlagDefinition("DATA.MISSING_MANDATORY_FIELD", RedFlagSeverity.HIGH, RedFlagCategory.DATA, True, "request_missing_data", True),
    "DATA.INVALID_THICKNESS_HISTORY": RedFlagDefinition("DATA.INVALID_THICKNESS_HISTORY", RedFlagSeverity.HIGH, RedFlagCategory.DATA, True, "request_missing_data", True),
    "DATA.VESSEL_DIMENSION_CONTEXT_MISSING": RedFlagDefinition("DATA.VESSEL_DIMENSION_CONTEXT_MISSING", RedFlagSeverity.MEDIUM, RedFlagCategory.DATA, False, "request_data_review", False),
    "FMT.SCHEMA_VALIDATION_FAILED": RedFlagDefinition("FMT.SCHEMA_VALIDATION_FAILED", RedFlagSeverity.HIGH, RedFlagCategory.FMT, True, "strict_revalidation", False),
    "OPS.TIMEOUT_EXCEEDED": RedFlagDefinition("OPS.TIMEOUT_EXCEEDED", RedFlagSeverity.MEDIUM, RedFlagCategory.OPS, False, "retry_or_escalate", False),
}


def is_known_flag(code: str) -> bool:
    return code in RED_FLAG_REGISTRY


def get_flag(code: str) -> RedFlagDefinition:
    return RED_FLAG_REGISTRY[code]


def is_blocking(code: str) -> bool:
    return get_flag(code).blocking


def requires_human_review(code: str) -> bool:
    return get_flag(code).human_review_required

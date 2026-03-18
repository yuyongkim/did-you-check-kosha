from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional

from src.shared.red_flags import get_flag, is_known_flag


@dataclass(frozen=True)
class CrossDisciplineThresholds:
    piping_vessel_margin_diff_mm: float = 1.5
    piping_vessel_margin_ratio: float = 0.75
    piping_margin_low_mm: float = 1.0
    piping_remaining_life_low_years: float = 3.0
    piping_nozzle_margin_low_mm: float = 1.5
    rotating_nozzle_overload_ratio: float = 1.0
    vessel_nozzle_margin_low_mm: float = 1.0
    vessel_remaining_life_low_years: float = 5.0
    rotating_bearing_hi_low: float = 4.0
    electrical_current_thd_high_pct: float = 5.0
    rotating_bearing_temp_high_c: float = 80.0
    electrical_power_factor_low: float = 0.85
    instrumentation_drift_high_pct: float = 1.0
    instrumentation_r2_low: float = 0.3
    instrumentation_pfd_high: float = 1.0e-3
    instrumentation_sil_target_high: float = 2.0
    steel_dc_high: float = 0.9
    steel_corrosion_high_percent: float = 30.0
    steel_deflection_ratio_high: float = 1.0
    piping_large_bore_nps_in: float = 8.0
    civil_settlement_high_mm: float = 25.0
    civil_crack_width_high_mm: float = 0.4
    civil_spalling_high_percent: float = 20.0
    rotating_vibration_ratio_high: float = 1.0

    @staticmethod
    def from_mapping(data: Mapping[str, Any]) -> CrossDisciplineThresholds:
        return CrossDisciplineThresholds(
            piping_vessel_margin_diff_mm=float(data.get("piping_vessel_margin_diff_mm", 1.5)),
            piping_vessel_margin_ratio=float(data.get("piping_vessel_margin_ratio", 0.75)),
            piping_margin_low_mm=float(data.get("piping_margin_low_mm", 1.0)),
            piping_remaining_life_low_years=float(data.get("piping_remaining_life_low_years", 3.0)),
            piping_nozzle_margin_low_mm=float(data.get("piping_nozzle_margin_low_mm", 1.5)),
            rotating_nozzle_overload_ratio=float(data.get("rotating_nozzle_overload_ratio", 1.0)),
            vessel_nozzle_margin_low_mm=float(data.get("vessel_nozzle_margin_low_mm", 1.0)),
            vessel_remaining_life_low_years=float(data.get("vessel_remaining_life_low_years", 5.0)),
            rotating_bearing_hi_low=float(data.get("rotating_bearing_hi_low", 4.0)),
            electrical_current_thd_high_pct=float(data.get("electrical_current_thd_high_pct", 5.0)),
            rotating_bearing_temp_high_c=float(data.get("rotating_bearing_temp_high_c", 80.0)),
            electrical_power_factor_low=float(data.get("electrical_power_factor_low", 0.85)),
            instrumentation_drift_high_pct=float(data.get("instrumentation_drift_high_pct", 1.0)),
            instrumentation_r2_low=float(data.get("instrumentation_r2_low", 0.3)),
            instrumentation_pfd_high=float(data.get("instrumentation_pfd_high", 1.0e-3)),
            instrumentation_sil_target_high=float(data.get("instrumentation_sil_target_high", 2.0)),
            steel_dc_high=float(data.get("steel_dc_high", 0.9)),
            steel_corrosion_high_percent=float(data.get("steel_corrosion_high_percent", 30.0)),
            steel_deflection_ratio_high=float(data.get("steel_deflection_ratio_high", 1.0)),
            piping_large_bore_nps_in=float(data.get("piping_large_bore_nps_in", 8.0)),
            civil_settlement_high_mm=float(data.get("civil_settlement_high_mm", 25.0)),
            civil_crack_width_high_mm=float(data.get("civil_crack_width_high_mm", 0.4)),
            civil_spalling_high_percent=float(data.get("civil_spalling_high_percent", 20.0)),
            rotating_vibration_ratio_high=float(data.get("rotating_vibration_ratio_high", 1.0)),
        )


@dataclass
class CrossIssue:
    code: str
    severity: str
    message: str
    check: str
    blocking: bool


def _issue(code: str, message: str, check: str) -> CrossIssue:
    if is_known_flag(code):
        flag = get_flag(code)
        return CrossIssue(
            code=code,
            severity=flag.severity.value,
            message=message,
            check=check,
            blocking=flag.blocking,
        )
    return CrossIssue(code=code, severity="medium", message=message, check=check, blocking=False)


def _to_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (float, int)):
        return float(value)
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


class CrossDisciplineValidator:
    """Validates coupling risks across piping, vessel, rotating, electrical, instrumentation, steel, and civil outputs."""

    def __init__(self, thresholds: CrossDisciplineThresholds | None = None) -> None:
        self.thresholds = thresholds or CrossDisciplineThresholds()

    _CHECK_PAIRS = [
        ("piping", "vessel", "_check_piping_vessel"),
        ("piping", "rotating", "_check_piping_rotating"),
        ("vessel", "rotating", "_check_vessel_rotating"),
        ("electrical", "rotating", "_check_electrical_rotating"),
        ("instrumentation", "piping", "_check_instrumentation_piping"),
        ("electrical", "instrumentation", "_check_electrical_instrumentation"),
        ("steel", "piping", "_check_steel_piping"),
        ("civil", "rotating", "_check_civil_rotating"),
        ("steel", "electrical", "_check_structure_electrical"),
        ("civil", "instrumentation", "_check_structure_instrumentation"),
    ]

    def evaluate(self, payload: Mapping[str, Any]) -> Dict[str, Any]:
        disciplines = {key: payload.get(key) for key in ("piping", "vessel", "rotating", "electrical", "instrumentation", "steel", "civil")}

        issues: List[CrossIssue] = []
        checks_run = 0

        for key_a, key_b, method_name in self._CHECK_PAIRS:
            a, b = disciplines[key_a], disciplines[key_b]
            if isinstance(a, Mapping) and isinstance(b, Mapping):
                checks_run += 1
                issues.extend(getattr(self, method_name)(a, b))

        red_flags = sorted({i.code for i in issues if i.severity in {"critical", "high"}})
        warnings = sorted({i.code for i in issues if i.severity not in {"critical", "high"}})
        blocking = any(i.blocking for i in issues)
        recommendations = self._recommendations(issues)

        return {
            "status": "blocked" if blocking else "ok",
            "issues": [
                {
                    "code": i.code,
                    "severity": i.severity,
                    "message": i.message,
                    "check": i.check,
                    "blocking": i.blocking,
                }
                for i in issues
            ],
            "flags": {"red_flags": red_flags, "warnings": warnings},
            "recommendations": recommendations,
            "summary": {
                "checks_run": checks_run,
                "issues_found": len(issues),
                "blocking": blocking,
            },
        }

    def _check_piping_vessel(self, piping: Mapping[str, Any], vessel: Mapping[str, Any]) -> List[CrossIssue]:
        issues: List[CrossIssue] = []
        t = self.thresholds

        p_current = _to_float(piping.get("current_thickness_mm"))
        p_min = _to_float(piping.get("t_min_mm"))
        v_current = _to_float(vessel.get("current_thickness_mm"))
        v_required = _to_float(vessel.get("t_required_shell_mm"))

        if None in {p_current, p_min, v_current, v_required}:
            return issues

        p_margin = p_current - p_min
        v_margin = v_current - v_required

        if p_margin < 0 or v_margin < 0:
            issues.append(
                _issue(
                    "PHY.NOZZLE_INTERFACE_OVERLOAD",
                    "Negative interface margin detected between piping and vessel nozzle region",
                    "piping_vessel_nozzle_margin",
                )
            )
            return issues

        diff = abs(p_margin - v_margin)
        ratio = diff / max(abs(p_margin), abs(v_margin), 1e-9)
        if diff > t.piping_vessel_margin_diff_mm and ratio > t.piping_vessel_margin_ratio:
            issues.append(
                _issue(
                    "LOG.CROSS_DISCIPLINE_MISMATCH",
                    "Piping and vessel nozzle margins are significantly imbalanced",
                    "piping_vessel_nozzle_margin",
                )
            )
        return issues

    def _check_piping_rotating(self, piping: Mapping[str, Any], rotating: Mapping[str, Any]) -> List[CrossIssue]:
        issues: List[CrossIssue] = []
        t = self.thresholds

        p_current = _to_float(piping.get("current_thickness_mm"))
        p_min = _to_float(piping.get("t_min_mm"))
        p_rl = _to_float(piping.get("remaining_life_years"))
        vibration = _to_float(rotating.get("vibration_mm_per_s"))
        vibration_limit = _to_float(rotating.get("vibration_limit_mm_per_s"))
        nozzle_load_ratio = _to_float(rotating.get("nozzle_load_ratio"))

        if None in {p_current, p_min, p_rl, vibration, vibration_limit, nozzle_load_ratio}:
            return issues

        p_margin = p_current - p_min
        vib_ratio = vibration / max(vibration_limit, 1e-9)

        if vib_ratio > 1.0 and (p_margin < t.piping_margin_low_mm or p_rl < t.piping_remaining_life_low_years):
            issues.append(
                _issue(
                    "PHY.VIBRATION_TO_PIPING_STRESS_RISK",
                    "High vibration combined with low piping margin/remaining life indicates coupling risk",
                    "piping_rotating_vibration_coupling",
                )
            )

        if nozzle_load_ratio > t.rotating_nozzle_overload_ratio and p_margin < t.piping_nozzle_margin_low_mm:
            issues.append(
                _issue(
                    "PHY.NOZZLE_INTERFACE_OVERLOAD",
                    "Rotating nozzle load exceedance with low piping margin",
                    "piping_rotating_nozzle_load",
                )
            )
        return issues

    def _check_vessel_rotating(self, vessel: Mapping[str, Any], rotating: Mapping[str, Any]) -> List[CrossIssue]:
        issues: List[CrossIssue] = []
        t = self.thresholds

        v_current = _to_float(vessel.get("current_thickness_mm"))
        v_required = _to_float(vessel.get("t_required_shell_mm"))
        v_rl = _to_float(vessel.get("remaining_life_years"))
        nozzle_load_ratio = _to_float(rotating.get("nozzle_load_ratio"))
        bearing_hi = _to_float(rotating.get("bearing_health_index"))

        if None in {v_current, v_required, v_rl, nozzle_load_ratio, bearing_hi}:
            return issues

        v_margin = v_current - v_required
        if nozzle_load_ratio > t.rotating_nozzle_overload_ratio and v_margin < t.vessel_nozzle_margin_low_mm:
            issues.append(
                _issue(
                    "PHY.NOZZLE_INTERFACE_OVERLOAD",
                    "Rotating nozzle load exceedance with low vessel margin",
                    "vessel_rotating_nozzle_load",
                )
            )

        if bearing_hi < t.rotating_bearing_hi_low and v_rl < t.vessel_remaining_life_low_years:
            issues.append(
                _issue(
                    "PHY.VESSEL_PULSATION_RISK",
                    "Low rotating health index combined with low vessel remaining life",
                    "vessel_rotating_pulsation",
                )
            )
        return issues

    def _check_electrical_rotating(self, electrical: Mapping[str, Any], rotating: Mapping[str, Any]) -> List[CrossIssue]:
        issues: List[CrossIssue] = []
        t = self.thresholds

        current_thd = _to_float(electrical.get("motor_current_thd_percent"))
        power_factor = _to_float(electrical.get("power_factor"))
        bearing_temp = _to_float(rotating.get("bearing_temperature_c"))

        vibration = _to_float(rotating.get("vibration_mm_per_s"))
        vibration_limit = _to_float(rotating.get("vibration_limit_mm_per_s"))
        vib_ratio = None
        if vibration is not None and vibration_limit is not None and vibration_limit > 0:
            vib_ratio = vibration / vibration_limit

        if None in {current_thd, power_factor, bearing_temp}:
            return issues

        if current_thd > t.electrical_current_thd_high_pct and bearing_temp > t.rotating_bearing_temp_high_c:
            issues.append(
                _issue(
                    "PHY.ELECTRICAL_TO_ROTATING_COUPLING_RISK",
                    "Electrical current distortion with elevated bearing temperature indicates coupling risk",
                    "electrical_rotating_harmonic_bearing",
                )
            )

        if power_factor < t.electrical_power_factor_low and vib_ratio is not None and vib_ratio > 1.0:
            issues.append(
                _issue(
                    "LOG.CROSS_DISCIPLINE_MISMATCH",
                    "Low power factor and elevated vibration indicate motor-load mismatch",
                    "electrical_rotating_power_quality",
                )
            )
        return issues

    def _check_instrumentation_piping(self, instrumentation: Mapping[str, Any], piping: Mapping[str, Any]) -> List[CrossIssue]:
        issues: List[CrossIssue] = []
        t = self.thresholds

        drift_pred = _to_float(instrumentation.get("predicted_drift_pct"))
        r_squared = _to_float(instrumentation.get("drift_r_squared"))
        p_rl = _to_float(piping.get("remaining_life_years"))

        p_current = _to_float(piping.get("current_thickness_mm"))
        p_min = _to_float(piping.get("t_min_mm"))
        p_margin = None
        if p_current is not None and p_min is not None:
            p_margin = p_current - p_min

        if None in {drift_pred, r_squared, p_rl}:
            return issues

        if drift_pred > t.instrumentation_drift_high_pct and (
            p_rl < t.piping_remaining_life_low_years or (p_margin is not None and p_margin < t.piping_margin_low_mm)
        ):
            issues.append(
                _issue(
                    "PHY.INSTRUMENT_TO_PIPING_COUPLING_RISK",
                    "High instrumentation drift with low piping integrity margin indicates coupling risk",
                    "instrumentation_piping_drift_margin",
                )
            )

        if r_squared < t.instrumentation_r2_low and p_rl < t.vessel_remaining_life_low_years:
            issues.append(
                _issue(
                    "LOG.DRIFT_MODEL_LOW_CONFIDENCE",
                    "Low drift model confidence on near-term piping risk case",
                    "instrumentation_piping_model_confidence",
                )
            )
        return issues

    def _check_electrical_instrumentation(self, electrical: Mapping[str, Any], instrumentation: Mapping[str, Any]) -> List[CrossIssue]:
        issues: List[CrossIssue] = []
        t = self.thresholds

        thd_voltage = _to_float(electrical.get("thd_voltage_percent"))
        pfdavg = _to_float(instrumentation.get("pfdavg"))
        sil_target = _to_float(instrumentation.get("sil_target"))

        if None in {thd_voltage, pfdavg, sil_target}:
            return issues

        if thd_voltage > 8.0 and pfdavg > t.instrumentation_pfd_high and sil_target >= t.instrumentation_sil_target_high:
            issues.append(
                _issue(
                    "PHY.ELECTRICAL_NOISE_TO_SIS_RISK",
                    "Electrical distortion may degrade SIS reliability margin",
                    "electrical_instrumentation_noise_sis",
                )
            )
        return issues

    def _check_steel_piping(self, steel: Mapping[str, Any], piping: Mapping[str, Any]) -> List[CrossIssue]:
        issues: List[CrossIssue] = []
        t = self.thresholds

        dc_ratio = _to_float(steel.get("dc_ratio"))
        corrosion_loss = _to_float(steel.get("corrosion_loss_percent"))
        deflection_ratio = _to_float(steel.get("deflection_ratio"))
        piping_nps = _to_float(piping.get("nps_inch"))
        piping_rl = _to_float(piping.get("remaining_life_years"))

        if None in {dc_ratio, piping_nps, piping_rl, deflection_ratio, corrosion_loss}:
            return issues

        if dc_ratio > t.steel_dc_high and piping_nps >= t.piping_large_bore_nps_in:
            issues.append(
                _issue(
                    "PHY.STRUCTURE_TO_PIPING_OVERLOAD_RISK",
                    "Steel support utilization is high while carrying large-bore piping load",
                    "steel_piping_pipe_rack_load",
                )
            )

        if deflection_ratio > t.steel_deflection_ratio_high and piping_rl < t.piping_remaining_life_low_years:
            issues.append(
                _issue(
                    "PHY.STRUCTURE_TO_PIPING_DEFLECTION_RISK",
                    "Steel deflection exceeds limit with low piping remaining-life margin",
                    "steel_piping_deflection_coupling",
                )
            )

        if corrosion_loss > t.steel_corrosion_high_percent and piping_rl < t.vessel_remaining_life_low_years:
            issues.append(
                _issue(
                    "PHY.STRUCTURE_TO_PIPING_DEFLECTION_RISK",
                    "Steel corrosion loss is elevated at interface with near-term piping risk",
                    "steel_piping_corrosion_interface",
                )
            )
        return issues

    def _check_civil_rotating(self, civil: Mapping[str, Any], rotating: Mapping[str, Any]) -> List[CrossIssue]:
        issues: List[CrossIssue] = []
        t = self.thresholds

        settlement = _to_float(civil.get("foundation_settlement_mm"))
        crack_width = _to_float(civil.get("crack_width_mm"))
        vibration = _to_float(rotating.get("vibration_mm_per_s"))
        vibration_limit = _to_float(rotating.get("vibration_limit_mm_per_s"))

        if None in {settlement, crack_width, vibration, vibration_limit}:
            return issues
        vib_ratio = vibration / max(vibration_limit, 1e-9)

        if settlement > t.civil_settlement_high_mm and vib_ratio > t.rotating_vibration_ratio_high:
            issues.append(
                _issue(
                    "PHY.FOUNDATION_TO_ROTATING_MISALIGNMENT_RISK",
                    "Foundation settlement and rotating vibration indicate misalignment risk",
                    "civil_rotating_foundation_settlement",
                )
            )

        if crack_width > t.civil_crack_width_high_mm and vib_ratio > t.rotating_vibration_ratio_high:
            issues.append(
                _issue(
                    "PHY.FOUNDATION_CRACK_VIBRATION_COUPLING",
                    "Foundation crack severity is coupled with elevated machine vibration",
                    "civil_rotating_crack_vibration",
                )
            )
        return issues

    def _check_structure_electrical(self, steel: Mapping[str, Any], electrical: Mapping[str, Any]) -> List[CrossIssue]:
        issues: List[CrossIssue] = []
        t = self.thresholds

        corrosion_loss = _to_float(steel.get("corrosion_loss_percent"))
        thd_voltage = _to_float(electrical.get("thd_voltage_percent"))

        if None in {corrosion_loss, thd_voltage}:
            return issues

        if corrosion_loss > t.steel_corrosion_high_percent and thd_voltage > 8.0:
            issues.append(
                _issue(
                    "PHY.STRUCTURE_SUPPORT_ELECTRICAL_RISK",
                    "Steel support degradation is elevated while electrical distortion is high",
                    "structure_electrical_support_condition",
                )
            )
        return issues

    def _check_structure_instrumentation(self, civil: Mapping[str, Any], instrumentation: Mapping[str, Any]) -> List[CrossIssue]:
        issues: List[CrossIssue] = []
        t = self.thresholds

        spalling = _to_float(civil.get("spalling_area_percent"))
        pfdavg = _to_float(instrumentation.get("pfdavg"))
        sil_target = _to_float(instrumentation.get("sil_target"))

        if None in {spalling, pfdavg, sil_target}:
            return issues

        if spalling > t.civil_spalling_high_percent and pfdavg > t.instrumentation_pfd_high and sil_target >= t.instrumentation_sil_target_high:
            issues.append(
                _issue(
                    "PHY.STRUCTURE_TO_SIS_RELIABILITY_RISK",
                    "Civil degradation and SIS reliability margin indicate coupled risk",
                    "structure_instrumentation_sis_coupling",
                )
            )
        return issues

    @staticmethod
    def _recommendations(issues: List[CrossIssue]) -> List[Dict[str, str]]:
        recs: List[Dict[str, str]] = []

        if any(i.code == "PHY.NOZZLE_INTERFACE_OVERLOAD" for i in issues):
            recs.append(
                {
                    "priority": "high",
                    "action": "verify_nozzle_load_and_thickness_interface",
                    "timeline": "immediate",
                    "description": "Interface overload risk detected across connected assets",
                }
            )
        if any(i.code == "PHY.VIBRATION_TO_PIPING_STRESS_RISK" for i in issues):
            recs.append(
                {
                    "priority": "high",
                    "action": "perform_coupled_vibration_stress_assessment",
                    "timeline": "immediate",
                    "description": "Coupled vibration-to-piping stress risk requires expedited assessment",
                }
            )
        if any(i.code == "LOG.CROSS_DISCIPLINE_MISMATCH" for i in issues):
            recs.append(
                {
                    "priority": "medium",
                    "action": "review_interface_design_basis",
                    "timeline": "1month",
                    "description": "Cross-discipline margin mismatch should be reconciled",
                }
            )
        if any(i.code == "PHY.ELECTRICAL_TO_ROTATING_COUPLING_RISK" for i in issues):
            recs.append(
                {
                    "priority": "high",
                    "action": "evaluate_harmonic_mitigation_for_rotating_assets",
                    "timeline": "immediate",
                    "description": "Electrical distortion and rotating health coupling risk detected",
                }
            )
        if any(i.code == "PHY.INSTRUMENT_TO_PIPING_COUPLING_RISK" for i in issues):
            recs.append(
                {
                    "priority": "high",
                    "action": "reassess_sensor_installation_and_piping_stress",
                    "timeline": "immediate",
                    "description": "Instrumentation drift may be amplified by piping integrity degradation",
                }
            )
        if any(i.code == "PHY.ELECTRICAL_NOISE_TO_SIS_RISK" for i in issues):
            recs.append(
                {
                    "priority": "high",
                    "action": "strengthen_emi_controls_for_sis",
                    "timeline": "immediate",
                    "description": "Electrical noise risk to SIS reliability requires mitigation",
                }
            )
        if any(i.code == "PHY.STRUCTURE_TO_PIPING_OVERLOAD_RISK" for i in issues):
            recs.append(
                {
                    "priority": "high",
                    "action": "recheck_pipe_rack_load_and_reinforce",
                    "timeline": "immediate",
                    "description": "Steel support and piping load coupling risk detected",
                }
            )
        if any(i.code == "PHY.FOUNDATION_TO_ROTATING_MISALIGNMENT_RISK" for i in issues):
            recs.append(
                {
                    "priority": "high",
                    "action": "perform_alignment_and_foundation_assessment",
                    "timeline": "immediate",
                    "description": "Foundation settlement is impacting rotating asset integrity",
                }
            )
        if any(i.code == "PHY.STRUCTURE_TO_SIS_RELIABILITY_RISK" for i in issues):
            recs.append(
                {
                    "priority": "high",
                    "action": "verify_sis_reliability_under_structural_degradation",
                    "timeline": "immediate",
                    "description": "Civil degradation may be reducing SIS reliability margin",
                }
            )

        if not recs:
            recs.append(
                {
                    "priority": "low",
                    "action": "continue_integrated_monitoring",
                    "timeline": "nextyear",
                    "description": "No blocking cross-discipline coupling risks detected",
                }
            )
        return recs

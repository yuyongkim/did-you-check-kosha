from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class CalibrationPoint:
    days_since_ref: float
    error_pct: float


@dataclass(frozen=True)
class InstrumentationInput:
    instrument_type: str
    voting_architecture: str
    sil_target: int
    failure_rate_per_hour: float
    proof_test_interval_hours: float
    mttr_hours: float
    calibration_interval_days: float
    calibration_history: list[CalibrationPoint]
    tolerance_pct: float
    sensor_mtbf_years: float
    cv_required: float
    cv_rated: float
    uncertainty_components_pct: list[float]


class InputPayloadError(ValueError):
    pass


def _pick(payload: Mapping[str, Any], aliases: list[str], default: Any = None) -> Any:
    for key in aliases:
        if key in payload:
            return payload[key]
    return default


def parse_instrumentation_input(payload: Mapping[str, Any]) -> InstrumentationInput:
    instrument_type = str(_pick(payload, ["instrument_type"], "pressure_transmitter")).lower()
    voting_architecture = str(_pick(payload, ["voting_architecture"], "1oo1")).lower()
    sil_target = _pick(payload, ["sil_target"])
    failure_rate = _pick(payload, ["failure_rate_per_hour", "lambda_per_hour"])
    test_interval = _pick(payload, ["proof_test_interval_hours", "test_interval_hours"])
    mttr = _pick(payload, ["mttr_hours"], 8.0)
    cal_interval = _pick(payload, ["calibration_interval_days", "cal_interval_days"])
    history = _pick(payload, ["calibration_history"])
    tolerance = _pick(payload, ["tolerance_pct", "allowable_error_pct"])
    mtbf = _pick(payload, ["sensor_mtbf_years", "mtbf_years"])
    cv_required = _pick(payload, ["cv_required"])
    cv_rated = _pick(payload, ["cv_rated"])

    missing = []
    if sil_target is None:
        missing.append("sil_target")
    if failure_rate is None:
        missing.append("failure_rate_per_hour")
    if test_interval is None:
        missing.append("proof_test_interval_hours")
    if cal_interval is None:
        missing.append("calibration_interval_days")
    if history is None:
        missing.append("calibration_history")
    if tolerance is None:
        missing.append("tolerance_pct")
    if mtbf is None:
        missing.append("sensor_mtbf_years")
    if cv_required is None:
        missing.append("cv_required")
    if cv_rated is None:
        missing.append("cv_rated")

    if missing:
        raise InputPayloadError(f"Missing required fields: {missing}")

    if not isinstance(history, list) or len(history) < 3:
        raise InputPayloadError("calibration_history must contain at least three points")

    points: list[CalibrationPoint] = []
    for idx, item in enumerate(history):
        if not isinstance(item, Mapping):
            raise InputPayloadError(f"calibration_history[{idx}] must be object")
        d = _pick(item, ["days_since_ref", "days", "t_days"])
        e = _pick(item, ["error_pct", "error", "drift_pct"])
        if d is None or e is None:
            raise InputPayloadError(f"calibration_history[{idx}] missing days/error")
        points.append(CalibrationPoint(days_since_ref=float(d), error_pct=float(e)))

    uncertainty_components = _pick(payload, ["uncertainty_components_pct"], [0.2, 0.2, 0.2])
    if not isinstance(uncertainty_components, list) or not uncertainty_components:
        raise InputPayloadError("uncertainty_components_pct must be non-empty list")

    return InstrumentationInput(
        instrument_type=instrument_type,
        voting_architecture=voting_architecture,
        sil_target=int(sil_target),
        failure_rate_per_hour=float(failure_rate),
        proof_test_interval_hours=float(test_interval),
        mttr_hours=float(mttr),
        calibration_interval_days=float(cal_interval),
        calibration_history=points,
        tolerance_pct=float(tolerance),
        sensor_mtbf_years=float(mtbf),
        cv_required=float(cv_required),
        cv_rated=float(cv_rated),
        uncertainty_components_pct=[float(v) for v in uncertainty_components],
    )

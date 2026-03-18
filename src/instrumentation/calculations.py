from __future__ import annotations

import math
from typing import Iterable

from src.instrumentation.constants import SIL_TARGET_PFD_LIMIT
from src.instrumentation.models import CalibrationPoint


def relative_difference(a: float, b: float) -> float:
    base = max(abs(a), abs(b), 1e-12)
    return abs(a - b) / base


def linear_regression(points: list[CalibrationPoint]) -> tuple[float, float, float]:
    x = [p.days_since_ref for p in points]
    y = [p.error_pct for p in points]
    n = len(points)
    x_mean = sum(x) / n
    y_mean = sum(y) / n

    den = sum((xi - x_mean) ** 2 for xi in x)
    if den <= 0:
        return 0.0, y_mean, 0.0

    num = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, y))
    slope = num / den
    intercept = y_mean - slope * x_mean

    y_pred = [slope * xi + intercept for xi in x]
    ss_res = sum((yi - yp) ** 2 for yi, yp in zip(y, y_pred))
    ss_tot = sum((yi - y_mean) ** 2 for yi in y)
    if ss_tot <= 0:
        r2 = 1.0
    else:
        r2 = max(0.0, 1.0 - ss_res / ss_tot)
    return slope, intercept, r2


def calculate_pfdavg(*, failure_rate_per_hour: float, proof_test_interval_hours: float, mttr_hours: float) -> float:
    pfd = failure_rate_per_hour * ((proof_test_interval_hours / 2.0) + (mttr_hours / 2.0))
    return max(pfd, 0.0)


def reverse_failure_rate_from_pfdavg(*, pfdavg: float, proof_test_interval_hours: float, mttr_hours: float) -> float | None:
    den = (proof_test_interval_hours / 2.0) + (mttr_hours / 2.0)
    if den <= 0:
        return None
    return max(pfdavg / den, 0.0)


def sil_target_limit(sil_target: int) -> float:
    return SIL_TARGET_PFD_LIMIT.get(sil_target, SIL_TARGET_PFD_LIMIT[1])


def sil_achieved_from_pfd(pfdavg: float) -> int:
    if 1e-5 <= pfdavg < 1e-4:
        return 4
    if 1e-4 <= pfdavg < 1e-3:
        return 3
    if 1e-3 <= pfdavg < 1e-2:
        return 2
    if 1e-2 <= pfdavg < 1e-1:
        return 1
    return 0


def combined_uncertainty_pct(components_pct: Iterable[float]) -> float:
    return math.sqrt(sum(float(c) ** 2 for c in components_pct))


def predicted_drift_pct(*, slope_pct_per_day: float, intercept_pct: float, interval_days: float) -> float:
    return slope_pct_per_day * interval_days + intercept_pct


def optimal_calibration_interval_days(*, slope_pct_per_day: float, intercept_pct: float, tolerance_pct: float) -> float:
    if slope_pct_per_day <= 0:
        return 365.0
    remaining = tolerance_pct - intercept_pct
    if remaining <= 0:
        return 1.0
    return max(1.0, remaining / slope_pct_per_day)


# TODO: screen_signal_integrity_risk - requires signal noise/impedance inputs not yet available


def calculate_status(*, pfdavg: float, sil_target: int, predicted_drift: float, tolerance_pct: float, cv_required: float, cv_rated: float) -> str:
    if pfdavg > sil_target_limit(sil_target) or predicted_drift > tolerance_pct or cv_required > cv_rated:
        return "CRITICAL"
    if pfdavg > sil_target_limit(max(sil_target - 1, 1)) or predicted_drift > tolerance_pct * 0.8 or cv_required > cv_rated * 0.9:
        return "WARNING"
    return "NORMAL"


def screen_proof_test_adequacy(pfdavg: float, sil_target: int) -> str:
    """Screening whether proof test interval is adequate for SIL target."""
    limit = sil_target_limit(sil_target)
    ratio = pfdavg / max(limit, 1e-15)
    if ratio > 1.0:
        return "INADEQUATE"
    if ratio > 0.7:
        return "MARGINAL"
    return "ADEQUATE"


def screen_calibration_health(predicted_drift_pct: float, tolerance_pct: float) -> str:
    """Screening calibration health indicator."""
    if tolerance_pct <= 0:
        return "UNKNOWN"
    ratio = predicted_drift_pct / tolerance_pct
    if ratio > 1.0:
        return "EXCEEDED"
    if ratio > 0.7:
        return "AT_RISK"
    if ratio > 0.5:
        return "WATCH"
    return "HEALTHY"


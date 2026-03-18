from __future__ import annotations

from dataclasses import dataclass


# Screening-only anchor points for saturation temperature interpolation.
# Exact values must be verified against active steam tables (IAPWS IF97).
SATURATION_POINTS_BAR_C = [
    (1.0, 99.6),
    (5.0, 151.8),
    (10.0, 179.9),
    (20.0, 212.4),
    (40.0, 250.4),
    (60.0, 275.6),
    (80.0, 295.0),
    (100.0, 311.0),
    (160.0, 345.0),
    (220.0, 374.0),
]


@dataclass(frozen=True)
class SteamStateScreening:
    phase_region: str
    saturation_temp_c: float | None
    superheat_margin_c: float | None
    phase_change_risk_index: float
    effective_quality: float


def saturation_temp_from_pressure_bar(pressure_bar: float) -> float | None:
    if pressure_bar <= 0:
        return None

    first_p, first_t = SATURATION_POINTS_BAR_C[0]
    if pressure_bar <= first_p:
        return first_t

    last_p, last_t = SATURATION_POINTS_BAR_C[-1]
    if pressure_bar >= last_p:
        return last_t

    for (p0, t0), (p1, t1) in zip(SATURATION_POINTS_BAR_C, SATURATION_POINTS_BAR_C[1:]):
        if p0 <= pressure_bar <= p1:
            ratio = (pressure_bar - p0) / (p1 - p0)
            return t0 + ratio * (t1 - t0)

    return None


def classify_steam_phase(
    pressure_bar: float | None,
    temperature_c: float | None,
    quality_x: float | None,
) -> tuple[str, float | None, float | None]:
    if quality_x is not None:
        if quality_x < 1.0:
            return "two_phase_wet_steam", None, None
        if quality_x >= 1.0 and temperature_c is None:
            return "dry_or_superheated", None, None

    if pressure_bar is None or temperature_c is None:
        return "unknown", None, None

    sat_temp = saturation_temp_from_pressure_bar(pressure_bar)
    if sat_temp is None:
        return "unknown", None, None

    superheat_margin = temperature_c - sat_temp
    if superheat_margin >= 15.0:
        return "superheated", sat_temp, superheat_margin
    if superheat_margin <= -10.0:
        return "compressed_or_subcooled", sat_temp, superheat_margin
    return "near_saturation", sat_temp, superheat_margin


def steam_phase_change_risk_index(
    pressure_bar: float | None,
    temperature_c: float | None,
    quality_x: float | None,
) -> float:
    risk = 0.0

    if quality_x is not None:
        if quality_x < 0.85:
            risk += 8.0
        elif quality_x < 0.90:
            risk += 5.0
        elif quality_x < 0.95:
            risk += 2.0

    sat_temp = saturation_temp_from_pressure_bar(pressure_bar) if pressure_bar is not None else None
    if sat_temp is not None and temperature_c is not None:
        margin = temperature_c - sat_temp
        if margin < 3.0:
            risk += 4.0
        elif margin < 8.0:
            risk += 2.0

    return min(risk, 10.0)


def screen_steam_state(
    pressure_bar: float | None,
    temperature_c: float | None,
    quality_x: float | None,
) -> SteamStateScreening:
    phase_region, sat_temp, margin = classify_steam_phase(
        pressure_bar=pressure_bar,
        temperature_c=temperature_c,
        quality_x=quality_x,
    )
    risk = steam_phase_change_risk_index(
        pressure_bar=pressure_bar,
        temperature_c=temperature_c,
        quality_x=quality_x,
    )
    effective_quality = quality_x if quality_x is not None else 1.0

    return SteamStateScreening(
        phase_region=phase_region,
        saturation_temp_c=sat_temp,
        superheat_margin_c=margin,
        phase_change_risk_index=risk,
        effective_quality=effective_quality,
    )

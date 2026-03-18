from __future__ import annotations

from typing import Dict, Tuple

from src.piping.constants import (
    ALLOWABLE_STRESS_TABLE_MPA,
    DEFAULT_Y_COEFFICIENT,
    HYDROTEST_CHLORIDE_LIMIT_PPM,
    MATERIAL_GROUP,
    MATERIAL_TEMP_LIMIT_C,
    STANDARD_REFERENCES,
    TEMPERATURE_PROFILE,
    WELD_EFFICIENCY,
)


def supported_material(material: str) -> bool:
    return material in ALLOWABLE_STRESS_TABLE_MPA


def get_material_group(material: str) -> str | None:
    return MATERIAL_GROUP.get(material)


def get_allowable_stress_mpa(material: str, temperature_c: float) -> Tuple[float, str]:
    table = ALLOWABLE_STRESS_TABLE_MPA.get(material)
    if table is None:
        raise KeyError(f"Unsupported material: {material}")

    keys = sorted(table.keys())
    if temperature_c <= keys[0]:
        return table[keys[0]], STANDARD_REFERENCES["allowable_stress"]
    if temperature_c >= keys[-1]:
        return table[keys[-1]], STANDARD_REFERENCES["allowable_stress"]

    for i in range(len(keys) - 1):
        left = keys[i]
        right = keys[i + 1]
        if left <= temperature_c <= right:
            left_v = table[left]
            right_v = table[right]
            ratio = (temperature_c - left) / (right - left)
            interpolated = left_v + ratio * (right_v - left_v)
            return interpolated, STANDARD_REFERENCES["allowable_stress"]

    return table[keys[-1]], STANDARD_REFERENCES["allowable_stress"]


def get_weld_efficiency(weld_type: str) -> Tuple[float, str]:
    return WELD_EFFICIENCY.get(weld_type.lower(), 0.85), STANDARD_REFERENCES["weld_efficiency"]


def get_y_coefficient(material: str, temperature_c: float) -> Tuple[float, str]:
    # Conservative default for baseline automation.
    _ = material
    _ = temperature_c
    return DEFAULT_Y_COEFFICIENT, STANDARD_REFERENCES["thickness_formula"]


def get_material_temperature_limit_c(material: str) -> Tuple[float | None, str]:
    return MATERIAL_TEMP_LIMIT_C.get(material), STANDARD_REFERENCES["allowable_stress"]


def get_temperature_window_c(material: str, profile: str) -> Tuple[Tuple[float, float] | None, str]:
    group = MATERIAL_GROUP.get(material)
    if group is None:
        return None, STANDARD_REFERENCES["allowable_stress"]

    profile_key = profile if profile in TEMPERATURE_PROFILE else "strict_process"
    profile_data = TEMPERATURE_PROFILE[profile_key].get(group)
    if profile_data is None:
        return None, STANDARD_REFERENCES["allowable_stress"]

    return (profile_data["soft_c"], profile_data["hard_c"]), STANDARD_REFERENCES["allowable_stress"]


def get_chloride_limit_ppm(material: str) -> Tuple[float | None, str]:
    group = MATERIAL_GROUP.get(material)
    if group is None:
        return None, STANDARD_REFERENCES["hydrotest_chloride"]
    return HYDROTEST_CHLORIDE_LIMIT_PPM.get(group), STANDARD_REFERENCES["hydrotest_chloride"]


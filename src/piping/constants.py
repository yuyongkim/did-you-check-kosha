from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Final


# NOTE: Values are seeded for baseline engineering automation and must be
# re-validated against active code editions before production release.
CS_MATERIALS: Final[tuple[str, ...]] = (
    "SA-106 Gr.B",
    "A106 Gr.B",
    "SA-53 Gr.B",
    "SA-333 Gr.6",
    "A105",
    "A234 WPB",
    "API 5L Gr.B",
)

LOW_ALLOY_MATERIALS: Final[tuple[str, ...]] = (
    "SA-335 P11",
    "SA-335 P22",
    "SA-335 P5",
    "SA-335 P9",
    "SA-335 P91",
)

SUS_MATERIALS: Final[tuple[str, ...]] = (
    "SA-312 TP304",
    "SA-312 TP304L",
    "SA-312 TP316",
    "SA-312 TP316L",
    "SA-312 TP321",
    "SA-312 TP347",
)

DUPLEX_MATERIALS: Final[tuple[str, ...]] = (
    "SA-790 S31803",
    "SA-790 S32205",
    "SA-790 S32750",
)

NICKEL_MATERIALS: Final[tuple[str, ...]] = (
    "Alloy 825 (N08825)",
    "Alloy 625 (N06625)",
    "Monel 400 (N04400)",
)

_STRESS_PROFILES_MPA: Final[Dict[str, Dict[float, float]]] = {
    "cs_main": {20.0: 138.0, 100.0: 138.0, 200.0: 124.0, 250.0: 110.0, 300.0: 103.0, 350.0: 97.0, 400.0: 90.0},
    "cs_secondary": {20.0: 131.0, 100.0: 131.0, 200.0: 117.0, 250.0: 103.0, 300.0: 97.0, 350.0: 90.0, 400.0: 83.0},
    "low_alloy_p11": {20.0: 138.0, 100.0: 138.0, 200.0: 132.0, 250.0: 127.0, 300.0: 123.0, 350.0: 118.0, 400.0: 114.0, 500.0: 103.0, 550.0: 96.0},
    "low_alloy_p22": {20.0: 138.0, 100.0: 138.0, 200.0: 134.0, 250.0: 130.0, 300.0: 126.0, 350.0: 122.0, 400.0: 118.0, 500.0: 108.0, 550.0: 101.0},
    "low_alloy_p5": {20.0: 138.0, 100.0: 138.0, 200.0: 133.0, 250.0: 128.0, 300.0: 124.0, 350.0: 120.0, 400.0: 116.0, 500.0: 106.0, 550.0: 98.0},
    "low_alloy_p9": {20.0: 138.0, 100.0: 138.0, 200.0: 134.0, 250.0: 130.0, 300.0: 126.0, 350.0: 122.0, 400.0: 119.0, 500.0: 112.0, 550.0: 105.0},
    "low_alloy_p91": {20.0: 170.0, 100.0: 167.0, 200.0: 160.0, 250.0: 156.0, 300.0: 152.0, 350.0: 148.0, 400.0: 145.0, 500.0: 136.0, 550.0: 128.0, 600.0: 121.0},
    "ss_304": {20.0: 138.0, 100.0: 131.0, 200.0: 124.0, 250.0: 117.0, 300.0: 110.0, 350.0: 103.0, 400.0: 97.0, 500.0: 83.0, 550.0: 76.0},
    "ss_316": {20.0: 138.0, 100.0: 131.0, 200.0: 124.0, 250.0: 117.0, 300.0: 110.0, 350.0: 103.0, 400.0: 97.0, 500.0: 83.0, 550.0: 76.0},
    "ss_321": {20.0: 138.0, 100.0: 131.0, 200.0: 125.0, 250.0: 119.0, 300.0: 113.0, 350.0: 107.0, 400.0: 101.0, 500.0: 90.0, 550.0: 83.0},
    "ss_347": {20.0: 138.0, 100.0: 131.0, 200.0: 126.0, 250.0: 120.0, 300.0: 114.0, 350.0: 108.0, 400.0: 102.0, 500.0: 92.0, 550.0: 85.0},
    "duplex_2205": {20.0: 170.0, 100.0: 166.0, 200.0: 160.0, 250.0: 154.0, 300.0: 148.0, 350.0: 142.0, 400.0: 136.0, 450.0: 130.0},
    "duplex_2507": {20.0: 190.0, 100.0: 186.0, 200.0: 178.0, 250.0: 171.0, 300.0: 165.0, 350.0: 159.0, 400.0: 152.0, 450.0: 145.0},
    "ni_825": {20.0: 155.0, 100.0: 150.0, 200.0: 145.0, 250.0: 141.0, 300.0: 137.0, 350.0: 133.0, 400.0: 129.0, 500.0: 118.0, 550.0: 110.0},
    "ni_625": {20.0: 170.0, 100.0: 165.0, 200.0: 160.0, 250.0: 156.0, 300.0: 152.0, 350.0: 148.0, 400.0: 145.0, 500.0: 136.0, 550.0: 128.0, 600.0: 120.0},
    "ni_monel_400": {20.0: 145.0, 100.0: 140.0, 200.0: 134.0, 250.0: 130.0, 300.0: 126.0, 350.0: 121.0, 400.0: 116.0, 500.0: 106.0, 550.0: 98.0},
}

_MATERIAL_TO_STRESS_PROFILE: Final[Dict[str, str]] = {
    "SA-106 Gr.B": "cs_main",
    "A106 Gr.B": "cs_main",
    "SA-53 Gr.B": "cs_secondary",
    "SA-333 Gr.6": "cs_main",
    "A105": "cs_main",
    "A234 WPB": "cs_secondary",
    "API 5L Gr.B": "cs_main",
    "SA-335 P11": "low_alloy_p11",
    "SA-335 P22": "low_alloy_p22",
    "SA-335 P5": "low_alloy_p5",
    "SA-335 P9": "low_alloy_p9",
    "SA-335 P91": "low_alloy_p91",
    "SA-312 TP304": "ss_304",
    "SA-312 TP304L": "ss_304",
    "SA-312 TP316": "ss_316",
    "SA-312 TP316L": "ss_316",
    "SA-312 TP321": "ss_321",
    "SA-312 TP347": "ss_347",
    "SA-790 S31803": "duplex_2205",
    "SA-790 S32205": "duplex_2205",
    "SA-790 S32750": "duplex_2507",
    "Alloy 825 (N08825)": "ni_825",
    "Alloy 625 (N06625)": "ni_625",
    "Monel 400 (N04400)": "ni_monel_400",
}


def _build_allowable_stress_table() -> Dict[str, Dict[float, float]]:
    table: Dict[str, Dict[float, float]] = {}
    for material, profile in _MATERIAL_TO_STRESS_PROFILE.items():
        table[material] = dict(_STRESS_PROFILES_MPA[profile])
    return table


def _assign_material_group(store: Dict[str, str], materials: tuple[str, ...], group: str) -> None:
    for material in materials:
        store[material] = group


def _build_material_group_map() -> Dict[str, str]:
    groups: Dict[str, str] = {}
    _assign_material_group(groups, CS_MATERIALS, "carbon_steel")
    _assign_material_group(groups, LOW_ALLOY_MATERIALS, "low_alloy_steel")
    _assign_material_group(groups, SUS_MATERIALS, "stainless_steel")
    _assign_material_group(groups, DUPLEX_MATERIALS, "duplex_stainless")
    _assign_material_group(groups, NICKEL_MATERIALS, "nickel_alloy")
    return groups


MATERIAL_GROUP_TEMP_LIMIT_C: Dict[str, float] = {
    "carbon_steel": 425.0,
    "low_alloy_steel": 593.0,
    "stainless_steel": 538.0,
    "duplex_stainless": 315.0,
    "nickel_alloy": 650.0,
}

TEMPERATURE_PROFILE: Dict[str, Dict[str, Dict[str, float]]] = {
    # Soft limit: conservative code limit.
    # Hard limit: managed operation envelope requiring engineering review.
    "strict_process": {
        "carbon_steel": {"soft_c": 425.0, "hard_c": 425.0},
        "low_alloy_steel": {"soft_c": 593.0, "hard_c": 593.0},
        "stainless_steel": {"soft_c": 538.0, "hard_c": 538.0},
        "duplex_stainless": {"soft_c": 315.0, "hard_c": 315.0},
        "nickel_alloy": {"soft_c": 650.0, "hard_c": 650.0},
    },
    "high_temp_managed": {
        "carbon_steel": {"soft_c": 425.0, "hard_c": 500.0},
        "low_alloy_steel": {"soft_c": 593.0, "hard_c": 620.0},
        "stainless_steel": {"soft_c": 538.0, "hard_c": 600.0},
        "duplex_stainless": {"soft_c": 315.0, "hard_c": 350.0},
        "nickel_alloy": {"soft_c": 650.0, "hard_c": 700.0},
    },
    "legacy_power_steam": {
        "carbon_steel": {"soft_c": 425.0, "hard_c": 540.0},
        "low_alloy_steel": {"soft_c": 593.0, "hard_c": 650.0},
        "stainless_steel": {"soft_c": 538.0, "hard_c": 620.0},
        "duplex_stainless": {"soft_c": 315.0, "hard_c": 360.0},
        "nickel_alloy": {"soft_c": 650.0, "hard_c": 720.0},
    },
}

ALLOWABLE_STRESS_TABLE_MPA: Dict[str, Dict[float, float]] = _build_allowable_stress_table()
MATERIAL_GROUP: Dict[str, str] = _build_material_group_map()
MATERIAL_TEMP_LIMIT_C: Dict[str, float] = {
    material: MATERIAL_GROUP_TEMP_LIMIT_C[group]
    for material, group in MATERIAL_GROUP.items()
}

WELD_EFFICIENCY: Dict[str, float] = {
    "seamless": 1.0,
    "erw": 0.85,
    "smaw": 0.85,
    "spot_rt": 0.85,
    "no_rt": 0.80,
}

NPS_TO_OD_MM: Dict[float, float] = {
    1.0: 33.4,
    2.0: 60.3,
    3.0: 88.9,
    4.0: 114.3,
    6.0: 168.3,
    8.0: 219.1,
    10.0: 273.1,
    12.0: 323.9,
    14.0: 355.6,
    16.0: 406.4,
}

HYDROTEST_CHLORIDE_LIMIT_PPM: Dict[str, float] = {
    "carbon_steel": 250.0,
    "low_alloy_steel": 250.0,
    "stainless_steel": 30.0,
    "duplex_stainless": 30.0,
    "nickel_alloy": 50.0,
}

SERVICE_CORROSION_FACTOR: Dict[str, float] = {
    "general": 1.0,
    "sour": 1.35,
    "chloride": 1.2,
    "high_temp": 1.25,
}

FLUID_CORROSION_FACTOR: Dict[str, float] = {
    "hydrocarbon_dry": 0.95,
    "hydrocarbon_wet": 1.1,
    "steam_condensate": 1.15,
    "amine": 1.25,
    "h2s_sour": 1.35,
    "chloride_aqueous": 1.4,
    "caustic": 1.2,
    "seawater": 1.45,
    "oxygen_rich": 1.1,
}

DEFAULT_Y_COEFFICIENT = 0.4
CONSENSUS_REL_TOLERANCE = 0.01

STANDARD_REFERENCES = {
    "allowable_stress": "ASME B31.3 Table A-1 [verify edition]",
    "thickness_formula": "ASME B31.3 Para 304.1.2",
    "inspection_interval": "API 570 Section 7 [verify edition]",
    "corrosion_rate": "API 570 remaining life and corrosion rate method [verify edition]",
    "hydrotest_chloride": "API 570 hydrotest water quality guidance [verify edition]",
    "weld_efficiency": "ASME B31.3 weld joint efficiency guidance [verify edition]",
}


@dataclass(frozen=True)
class PipingThresholds:
    min_pressure_mpa: float = 0.0
    max_pressure_mpa: float = 50.0
    min_temperature_c: float = -50.0
    max_temperature_c: float = 650.0
    max_reasonable_rl_years: float = 50.0
    reverse_check_tolerance_percent: float = 5.0

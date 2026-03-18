# Piping User Guide

## 1) Run Full Piping Data Flow
1. Generate golden dataset:
```powershell
python scripts/generate_piping_golden_dataset.py
```
2. Run benchmark and generate report:
```powershell
python scripts/benchmark_piping_system.py
```
3. Run mock E2E pipeline:
```powershell
python examples/mock_e2e_pipeline.py
```

## 2) Required Input Schema (Core)
```json
{
  "material": "SA-106 Gr.B",
  "nps": 6,
  "design_pressure_mpa": 4.5,
  "design_temperature_c": 250,
  "thickness_history": [
    {"date": "2015-01-01", "thickness_mm": 10.0},
    {"date": "2020-01-01", "thickness_mm": 8.6},
    {"date": "2025-01-01", "thickness_mm": 7.3}
  ],
  "corrosion_allowance_mm": 1.5,
  "weld_type": "seamless",
  "service_type": "general",
  "has_internal_coating": false,
  "chloride_ppm": 100
}
```

## 3) Output Interpretation
- `final_results`:
  - `t_min_mm`
  - `cr_long_term_mm_per_year`
  - `cr_short_term_mm_per_year`
  - `cr_selected_mm_per_year`
  - `remaining_life_years`
  - `inspection_interval_years`
- `flags.red_flags`: blocking safety/compliance violations
- `flags.warnings`: non-blocking but review-required items
- `layer_results`: pass/fail and details for each verification layer

## 4) Safety Handling
- Any critical red flag must be treated as auto-blocked.
- `PHY.CURRENT_THICKNESS_BELOW_MINIMUM` means immediate integrity action.
- `PHY.TEMPERATURE_LIMIT_EXCEEDED` means material applicability breach.

## 5) Notes
- Standards numeric tables in baseline are automation seed values.
- Production release requires edition-specific SME validation.

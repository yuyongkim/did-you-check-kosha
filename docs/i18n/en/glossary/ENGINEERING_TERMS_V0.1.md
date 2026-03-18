# Engineering Terms and Code Glossary

Status: Draft  
Version: v0.1  
Last Updated: 2026-02-27

## Purpose
- Provide a single quick-reference for field engineers and reviewers.
- Reduce confusion from raw code numbers (`UG-27`, `UG-28`, `UG-37`) and variable keys (`t_min_mm`, `pfdavg`, etc.).

## Standards Code Quick Guide
- `ASME VIII Div.1 UG-27`: internal-pressure shell thickness.
- `ASME VIII Div.1 UG-28`: external-pressure buckling check.
- `ASME VIII Div.1 UG-37`: nozzle/opening reinforcement check.
- `ASME B31.3 Para 304.1.2`: process piping minimum thickness equation.
- `ASME B31.3 Table A-1`: material allowable stress table.
- `API 570 Section 7`: piping corrosion rate, remaining life, inspection interval.
- `API 510`: pressure vessel in-service integrity and inspection.
- `API 610`: pump vibration/nozzle-load/mechanical integrity context.
- `API 617`: compressor mechanical integrity context.
- `API 670`: machinery protection/monitoring context.

## Core Variable Guide (Examples)
- `t_min_mm`: minimum required thickness (mm).
- `t_required_shell_mm`: required vessel shell thickness (mm).
- `remaining_life_years`: estimated remaining life (years).
- `inspection_interval_years`: recommended inspection interval (years).
- `external_pressure_utilization`: applied external pressure / screening allowable.
- `nozzle_reinforcement_index`: available reinforcement area / required area.
- `pfdavg`: probability of failure on demand (instrumented safety context).
- `dc_ratio`: demand/capacity ratio for structural checks.

## UI Location
- Frontend page: `/glossary`
- Top bar button: `용어집`
- Sidebar shortcut: `용어집 / 코드설명`
- Discipline tabs: `All/Common/Piping/Vessel/Rotating/Electrical/Instrumentation/Steel/Civil`

## Update Rule
- Whenever new standard references or major output variables are added, this glossary and frontend glossary page should be updated in the same change set.

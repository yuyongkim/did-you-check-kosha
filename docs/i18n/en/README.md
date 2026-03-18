# EPC Maintenance AI User Guide (English)

## 1. Scope
This system is a multi-discipline integrity screening workbench for:
- Piping
- Vessel (Static Equipment)
- Rotating Equipment
- Electrical
- Instrumentation
- Steel Structure
- Civil/Concrete

It is designed for fast engineering screening with traceable formulas, standards references, red flags, and recommended actions.

## 2. Quick Start
```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

## 3. What You Are Calculating (Process Engineer Focus)
### 3.1 Piping (`/piping`)
- Purpose: wall-thickness integrity screening and inspection planning.
- Core metrics:
  - `t_min_mm`: minimum required thickness.
  - `cr_selected_mm_per_year`: selected corrosion rate.
  - `remaining_life_years` (RL): estimated remaining life.
  - `inspection_interval_years`: recommended inspection interval.
- Practical interpretation:
  - `t_current` close to `t_min` or high CR -> tighten interval and inspect hotspots.

### 3.2 Vessel (`/vessel`)
- Purpose: shell/nozzle integrity screening under pressure and geometry context.
- Core metrics:
  - `t_required_shell_mm`
  - `thickness_margin_mm`
  - `external_pressure_utilization`
  - `nozzle_reinforcement_index`

### 3.3 Rotating (`/rotating`)
- Purpose: machine condition and protection readiness screening.
- Core metrics:
  - `adjusted_vibration_limit_mm_per_s`
  - `mechanical_integrity_index`
  - `process_stability_index`
  - `protection_readiness_index`

## 4. How To Read the 3-Pane Screen
- Left pane: input case definition (design basis, operation, inspection history).
- Center pane: calculation summary, visual trend/schematic, and recommendations.
- Right pane: verification layers, standards references, and red/warning flags.

Use this order for decision support:
1. Confirm red flags and warning flags.
2. Check final key metrics (`t_min`, CR, RL, interval, margin/index values).
3. Review trace and standards references.
4. Approve continued service, tighten inspection, or escalate for repair/FFS.

## 5. Piping NDE Recommendation Logic
Material-based NDE guidance is now available in the piping visual panel.

- Carbon steel:
  - `UT Thickness (CML Grid)`, `PAUT/UT mapping`, `MT (targeted weld areas)`
- Low alloy:
  - `UT/PAUT weld-HAZ scan`, `MT/PT`, `replication metallography` (high-temp program)
- Stainless steel:
  - `UT mapping`, `PT`, `ECT` (as needed)
- Duplex stainless:
  - `UT mapping`, `PT`, `PMI/ferrite check`
- Nickel alloy:
  - `PT`, `PAUT/TOFD`, `PMI verification`

Cadence is adjusted by risk conditions (remaining life, corrosion rate, and temperature-limit mode).

## 6. Important Limits
- This tool is a screening assistant, not a direct replacement for final code-compliance sign-off.
- Final release and run/repair decisions still require site procedures, code edition checks, and SME judgment.

## 7. Related Documents
- Documentation hub: `docs/README.md`
- Docs navigation guideline: `docs/i18n/en/DOCS_NAVIGATION_GUIDELINE.md`
- Report submission template: `docs/i18n/en/REPORT_SUBMISSION_TEMPLATE.md`
- Sample piping submission report: `docs/i18n/en/reports/SAMPLE_PIPING_REPORT_SUBMISSION_V0.1.md`
- All-discipline sample pack: `docs/i18n/en/reports/README.md`
- Standards mapping: `docs/standards_index.md`
- Piping NDE detail: `docs/i18n/en/piping/NDE_RECOMMENDATIONS.md`
- Full bilingual index: `docs/BILINGUAL_INDEX.md`

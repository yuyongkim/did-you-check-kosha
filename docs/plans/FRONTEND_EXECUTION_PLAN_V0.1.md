# Frontend Execution Plan

Status: Completed
Version: v0.1
Last Updated: 2026-02-27

## 1) Context
- Backend seven-discipline runtime and verification layers are available.
- Frontend objective is to expose trusted, transparent engineering workflows.
- This plan follows docs-first governance and modular implementation.

## 2) Scope
In scope:
- Next.js frontend foundation
- 3-pane workbench UX
- seven discipline routes and forms
- backend API integration
- verification/standards evidence display

Out of scope (v0.1):
- advanced multi-user collaboration
- tenant billing portal
- custom report-builder engine

## 3) Work Breakdown

### Track A - Platform Setup
- [x] Initialize Next.js 14 + TypeScript project
- [x] Add Tailwind and shadcn-style primitives
- [x] Configure lint/type/build scripts

### Track B - UI Architecture
- [x] Build shell, navigation, route structure
- [x] Build 3-pane layout and responsive behavior
- [x] Implement shared status and alert primitives
- [x] Add top bar mobile discipline switch

### Track C - Domain Forms and Results
- [x] Build seven discipline form modules
- [x] Implement result cards and detail tables
- [x] Implement verification panel and standards panel
- [x] Add calculation trace card and blocked banner
- [x] Add discipline run history panel

### Track D - Integration
- [x] Build typed API client and mappers
- [x] Implement hooks (`useCalculation`, `useVerification`)
- [x] Connect pages to mock backend endpoints
- [x] Add UI setting-driven mock/backend mode switching
- [x] Connect to production Python backend endpoints

### Track E - Quality Gate
- [x] Unit/integration/e2e tests
- [x] Type/lint/build checks
- [x] Accessibility and performance checks
- [x] Release candidate sign-off checklist

## 4) Timeline (Target)
- Day 1 morning: Track A + Track B shell complete
- Day 1 evening: first three disciplines wired
- Day 2 morning: all seven disciplines wired
- Day 2 evening: quality gates and release candidate

## 5) Risks and Mitigations
- Risk: response contract drift
  - Mitigation: strict typed mappers and runtime guards
- Risk: overloaded UI density
  - Mitigation: consistent hierarchy and collapsible detail sections
- Risk: hidden safety states
  - Mitigation: fixed right-pane verification block and top-level blocked banner

## 6) Exit Criteria
- [x] Seven discipline pages operational.
- [x] 3-pane UX stable on desktop/tablet/mobile.
- [x] Verification layers + standards references always visible in result state.
- [x] QA checklist passed and runbook prepared.

## 7) Depth Parity Update (2026-02-27)
- [x] Piping plus all remaining six disciplines upgraded from minimal demo inputs to domain-rich forms.
- [x] Discipline outcome builders expanded with standards-aware guardrails and additional engineering metrics.
- [x] Full frontend QA rerun after parity update (lint, typecheck, unit, e2e, build).

## 8) Maintainability Update (2026-02-27)
- [x] Refactored oversized mock engine into discipline modules to keep files short and debuggable.
- [x] Extracted shared math/date helpers for reuse across all discipline builders.
- [x] Revalidated frontend and backend regression suites after modular split.

## 9) Backend E2E Update (2026-02-27)
- [x] Added Playwright backend-mode regression for all seven disciplines.
- [x] Connected Playwright startup to backend `/health` dependency.
- [x] Added dedicated `test:e2e:backend` command for repeatable integration checks.
- [x] Integrated into repository-level quality gate script for one-command execution.

## 10) CI Forensics Update (2026-02-27)
- [x] Added profile-based quality gate execution (`fast`/`strict`) for operational flexibility.
- [x] Enabled Playwright forensic outputs (html report, failure screenshot/video, fixed output directory).
- [x] Added CI artifact upload on strict-profile failure to speed root-cause analysis.

## 11) Visual Engineering Context Update (2026-02-27)
- [x] Added seven-discipline visual packs (3 cards each) to move from metric-only output to visual trust context.
- [x] Switched center-pane visualization entry from single chart to discipline-specific visual panel.
- [x] Added frontend visual context spec document:
  - `docs/specs/frontend/06_VISUAL_ENGINEERING_CONTEXT_V0.1.md`

## 12) Rotating Domain Split Update (Steam Turbine Context)
- [x] Added rotating form conditional fields for steam turbines:
  - `steam_pressure_bar`, `steam_temperature_c`, `steam_quality_x`,
  - `inlet_enthalpy_kj_per_kg`, `outlet_enthalpy_kj_per_kg`
- [x] Added steam-phase risk metrics to rotating mock result model:
  - phase-change risk index, superheat margin, steam specific energy drop
- [x] Added steam-specific right/center pane visualization content in rotating page.

## 13) UI Readability and Context Update (2026-02-27)
- [x] Applied chart tooltip contrast theme for dark UI readability (hover values are clearly visible).
- [x] Added richer hero context on dashboard (value pillars beyond title/subtitle).
- [x] Added per-discipline hero briefing cards (Focus / Core Checks / Output).
- [x] Upgraded piping visuals to respond dynamically to risk/result values:
  - ring color changes by risk band,
  - grid-point spread driven by corrosion rate,
  - forecast year and utilization messaging.

## 14) Terminology Help Update (2026-02-27)
- [x] Added per-term `(?)` help tooltip on input labels.
- [x] Added per-metric `(?)` help tooltip on summary cards.
- [x] Added verification-layer `(?)` help tooltip in right pane.
- [x] Added centralized glossary for consistent term definitions.

## 15) Static Equipment Dimension Context Update (2026-02-27)
- [x] Expanded VES form inputs with geometry context:
  - shell length, straight shell height, head type/depth, nozzle OD.
- [x] Updated VES visual panel to scale schematic and labels by live dimensions.
- [x] Added glossary coverage for new geometry terms and derived metrics.

## 16) Static Equipment Deepening Update (2026-02-27)
- [x] Added VES external pressure input and screening output panel fields.
- [x] Added VES nozzle reinforcement pad inputs and reinforcement index visibility.
- [x] Synced frontend term help with UG-28/UG-37 screening terminology.

## 17) Glossary Access Update (2026-02-27)
- [x] Added dedicated glossary route (`/glossary`) with search.
- [x] Added topbar/sidebar/home shortcut links to glossary.
- [x] Added standards-code quick guide (UG/API/B31.3 baseline) alongside engineering terms.
- [x] Added discipline tabs/filters for glossary browsing.
- [x] Added usage-priority sorting per discipline (high-frequency terms first).
- [x] Added Top 10 key standards/terms summary sections.
- [x] Added pin/favorites support with local persistence for standards/terms.

## 18) Optimization Sprint Update (30-item batch, 2026-02-27)
- [x] Fixed corrupted UI strings in home/topbar/sidebar.
- [x] Strengthened term-help `(?)` behavior (hover + click + outside-close).
- [x] Improved tooltip visibility and focus accessibility.
- [x] Upgraded glossary pin UX (reorder, import/export feedback, clear feedback).
- [x] Kept pinned entries stable under search/filter changes.
- [x] Added glossary filtered/total counters for standards and terms.
- [x] Improved chart contrast (ticks + tooltip legibility).
- [x] Reworked formula trace normalization and readability.
- [x] Expanded formula interpretation hints.
- [x] Added code-level red-flag taxonomy explanations in UI.
- [x] Added blocked banner cause details (code + meaning).
- [x] Added warnings/red flags explanation rows in Flags panel.
- [x] Added conditional VES dimension-field visibility by vessel type.
- [x] Expanded VES material coverage (additional alloy/stainless options).
- [x] Expanded piping fluid taxonomy (steam subtype coverage).
- [x] Expanded piping NPS-to-OD map up to large bore.
- [x] Added richer helper guidance for key piping input fields.
- [x] Expanded rotating machine-type options.
- [x] Added explicit steam-screening context text in rotating visuals.
- [x] Expanded electrical equipment-type options.
- [x] Expanded instrumentation instrument-type options.
- [x] Expanded steel grade options and grade-aware Fy fallback.
- [x] Expanded civil exposure environment options/factors.
- [x] Added glossary explicit definitions for UG-27/UG-28/UG-37 and key B31.3 references.
- [x] Added unit tests for glossary pin helpers.
- [x] Added unit tests for glossary label/definition fallback.
- [x] Typecheck pass.
- [x] Lint pass.
- [x] Unit tests pass.
- [x] Production build pass.

## 19) Hardening Wave Update (100-point batch, 2026-02-27)
- [x] Upgraded shared form engine with `unit` and `placeholder` field metadata support.
- [x] Added safer select-default behavior to reduce false required-blocking.
- [x] Added stronger field-level validation message quality.
- [x] Added auto range helper injection for numeric fields.
- [x] Added quick preset framework to discipline forms.
- [x] Added 4 presets for each of seven disciplines.
- [x] Expanded multi-discipline domain options (materials/equipment/environments/fluid classes).
- [x] Extended piping NPS-OD map for large-bore lines.
- [x] Extended rotating steam-aware and machine-class workflows.
- [x] Completed full frontend quality gate rerun (typecheck/lint/unit/build).

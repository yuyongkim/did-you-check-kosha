# Frontend Component System Specification

Status: Draft
Version: v0.1
Last Updated: 2026-02-27

## 1) Layout Components
- `AppShell`
  - global frame, header, navigation rail
- `ThreePaneLayout`
  - left/center/right slot container
- `DisciplineTabs`
  - route-aware discipline quick switch

## 2) Form Components
- `DisciplineFormContainer`
  - wraps React Hook Form + Zod schema
- `AssetSelector`
- `HistoryTableInput`
  - thickness history, calibration history, etc.
- `ExecuteButton`
  - loading, disabled, blocked interaction states

## 3) Result Components
- `ResultSummaryCard`
  - core KPIs and status badge
- `ResultDetailTable`
- `RecommendationsPanel`

## 4) Verification Components (Critical)
- `VerificationPanel`
  - Layer 1-4 status entries
- `VerificationLayerItem`
  - pass/warn/fail icon + message
- `StandardsReferencePanel`
  - standard + section/table + cited value
- `FlagPanel`
  - red flag/warning list with severity and action

## 5) Chart Components
- `ThicknessTrendChart` (piping/vessel)
- `VibrationSpectrumChart` (rotating)
- `DCRatioGauge` (steel/civil)
- `PowerQualityChart` (electrical)
- `DriftTrendChart` (instrumentation)

## 6) Reusable UI Patterns
- Status badge enum:
  - `ok`, `warning`, `blocked`, `error`
- Severity enum:
  - `critical`, `high`, `medium`, `low`
- Common section frame:
  - title + subtitle + optional evidence badge

## 7) Typed View Models
- `WorkbenchResultVM`
- `VerificationLayerVM`
- `ReferenceVM`
- `RecommendationVM`
- `FlagVM`

## 8) Component Test Expectations
- Rendering tests for each critical component.
- Interaction tests for form submit/validation flow.
- Snapshot tests only for stable layout primitives.
- No business-rule duplication in component tests.

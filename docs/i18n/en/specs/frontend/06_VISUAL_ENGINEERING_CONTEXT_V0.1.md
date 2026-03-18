# Frontend Visual Engineering Context Spec

Status: Draft
Version: v0.1
Last Updated: 2026-02-27

## 1) Objective
- Move from metric-only output to spec-book-level visual trust.
- Ensure every discipline page shows:
  - geometry/context view
  - trend/threshold chart
  - action-oriented inspection/diagnostic panel

## 2) Design Principles
- Copyright-safe rendering:
  - do not embed scanned ASME/API figures
  - render independent SVG/React schematic views
- Data-driven visuals:
  - all views respond to current input/result payload
  - no static placeholder image in production mode
- Verification visibility:
  - visual thresholds align with layer-3/4 checks
  - warnings and blocked conditions must be visually obvious

## 3) Discipline Visual Packs
- Piping:
  - dynamic pipe cross-section (OD, current thickness, minimum thickness)
  - corrosion trend with minimum threshold line
  - API-570 style CML grid readout
- Vessel:
  - vessel shell/head/nozzle concept schematic
  - temperature-stress trend with operating point
  - thickness integrity zone status
- Rotating:
  - API-limit-aware vibration spectrum
  - frequency marker trend/fault hints
  - nozzle/bearing condition status block
- Electrical:
  - single-line context schematic
  - HI/arc/power-quality breakdown chart
  - safety zone classification panel
- Instrumentation:
  - drift trend with tolerance threshold
  - SIL target vs achieved band visualization
  - calibration decision panel
- Steel:
  - member context schematic
  - D/C utilization gauge
  - serviceability/corrosion condition block
- Civil:
  - section/cover/carbonation context schematic
  - carbonation progression chart
  - damage classification block

## 4) Component Architecture
- Entry point:
  - `frontend/components/visualization/visual-engineering-panel.tsx`
- Discipline modules:
  - `piping-visuals.tsx`
  - `vessel-visuals.tsx`
  - `rotating-visuals.tsx`
  - `electrical-visuals.tsx`
  - `instrumentation-visuals.tsx`
  - `steel-visuals.tsx`
  - `civil-visuals.tsx`
- Shared:
  - `visual-section-card.tsx`
  - `utils.ts`

## 5) UX Behavior
- Show visual panel in center pane directly after summary cards.
- Keep each discipline visual pack to three compact cards to control complexity.
- Preserve responsive behavior:
  - mobile/tablet stacks as single-column cards
  - desktop uses three-column visual grid

## 6) Verification Alignment
- Visual thresholds should mirror runtime rules:
  - piping minimum thickness
  - rotating vibration limit
  - electrical arc-flash critical zone
  - instrumentation tolerance crossing
  - steel D/C and civil damage criteria
- If blocked status occurs, visual cards remain visible but must still show risk cues.

## 7) Exit Criteria
- Seven discipline pages each render a three-card visual context pack.
- Backend mode and mock mode both render without schema/UI breakage.
- Full quality gate passes for strict profile.

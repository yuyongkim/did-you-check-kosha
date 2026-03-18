# Frontend Information Architecture and Layout Specification

Status: Draft
Version: v0.1
Last Updated: 2026-02-27

## 1) Navigation Model
Top-level domains:
- Piping
- Static Equipment (Vessel)
- Rotating
- Electrical
- Instrumentation
- Steel
- Civil

Global actions:
- Project selection
- Asset selection
- Export
- Settings

## 2) 3-Pane Workbench Layout
Desktop default (>= 1280px):
- Left pane: 25%
- Center pane: 50%
- Right pane: 25%

Pane responsibilities:
- Left:
  - asset selector
  - discipline input form
  - history input blocks
  - execute button
- Center:
  - key result cards
  - charts and trend views
  - recommendations
- Right:
  - verification layer panel
  - standards reference panel
  - red-flag taxonomy summary

## 3) Responsive Behavior
Tablet (768px-1279px):
- Collapsible left pane
- Center and right stack with tab switch

Mobile (<768px):
- Single-column mode
- Sticky top tabs for:
  - Input
  - Results
  - Verification

## 4) Visual Hierarchy
- Priority 1 (always above fold):
  - status badge (OK/WARNING/BLOCKED)
  - major safety metrics (RL, D/C, vibration, arc-flash, SIL, etc.)
- Priority 2:
  - verification layers
  - red flags and warnings
- Priority 3:
  - historical trend charts
  - detailed calculation steps

## 5) State Views
- Idle:
  - empty-state guidance per discipline
- Loading:
  - skeleton cards for all three panes
- Success:
  - full result rendering + verification details
- Blocked:
  - prominent blocking banner + mandatory recommended actions
- Error:
  - actionable API/schema error card + request trace id

## 6) Accessibility Requirements
- Keyboard navigable form and panel controls.
- Focus indicators for all interactive elements.
- Color is not the only carrier of safety status.
- Contrast targets: WCAG AA minimum.

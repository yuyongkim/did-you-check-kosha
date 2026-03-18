# Frontend Overview and Architecture Specification

Status: Draft
Version: v0.1
Last Updated: 2026-02-27

## 1) Objective
Define a production-ready frontend architecture for the EPC Maintenance AI system
that exposes seven-discipline calculations, four-layer verification status, and
standards traceability in a single operator workspace.

## 2) Product Form
- Product type: B2B SaaS web application
- Core UX pattern: 3-pane workbench
- Primary users:
  - Maintenance engineer
  - Reliability engineer
  - Inspection lead
  - Technical manager

## 3) Core UX Principles
- Trust-Centric:
  - Every major result must show standards references and applied assumptions.
- Transparency:
  - Layer 1-4 verification outcomes are always visible.
- Safety-First:
  - Red flags and blocked states are explicit and impossible to miss.
- Professional Readability:
  - Dense but structured data presentation for industrial users.

## 4) Recommended Stack
- Framework: Next.js 14 (App Router) + TypeScript
- Styling/UI: Tailwind CSS + shadcn/ui
- Forms: React Hook Form + Zod
- Charts: Recharts
- Client state: Zustand
- Data fetching: fetch + typed API client (or React Query optional)

## 5) High-Level Frontend Topology
- `app/`
  - route-level pages for each discipline + integrated dashboard
- `components/layout/`
  - shell, navigation, 3-pane layout primitives
- `components/forms/`
  - discipline input forms and reusable field groups
- `components/verification/`
  - verification panel, standards references, red-flag summaries
- `components/charts/`
  - discipline-specific visualization modules
- `hooks/`
  - typed calculation and verification hooks
- `lib/`
  - api client, mappers, domain types, formatting

## 6) Primary Screens
- `/`
  - integrated workbench dashboard
- `/piping`, `/vessel`, `/rotating`, `/electrical`, `/instrumentation`, `/steel`, `/civil`
  - discipline-specific pages with same shell and panel pattern

## 7) Output Contract in UI
The UI should normalize backend responses into a common view model:
- `calculation_summary`
- `final_results`
- `layer_results`
- `flags.red_flags`
- `flags.warnings`
- `calculation_steps[].standard_reference`
- `recommendations`

## 8) Non-Goals (v0.1)
- No direct multi-user collaboration editing in v0.1.
- No custom report template builder in v0.1.
- No embedded admin CMS in v0.1.

## 9) Acceptance Gate
- All seven discipline routes render and run with typed API contracts.
- 3-pane workbench is stable on desktop and tablet.
- Verification and standards sections are always present in results view.

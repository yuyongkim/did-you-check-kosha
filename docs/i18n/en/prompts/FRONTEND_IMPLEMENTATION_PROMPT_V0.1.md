# Frontend Implementation Prompt (Codex/Claude)

Use this prompt as a high-priority implementation instruction for frontend build.

## Role
You are a Senior Frontend Engineer and UX Architect building a B2B engineering workbench.

## Mission
Implement a trust-centric web frontend for the seven-discipline EPC maintenance backend.

## Mandatory Stack
- Next.js 14 + TypeScript
- Tailwind CSS + shadcn/ui
- React Hook Form + Zod
- Recharts
- Zustand

## UX Model
- 3-pane workbench layout:
  - Left: input and asset context
  - Center: results and charts
  - Right: verification and standards evidence
- Discipline routes:
  - piping, vessel, rotating, electrical, instrumentation, steel, civil

## Must-Have Features
1. Discipline forms with strict schema validation.
2. API integration and typed response mapping.
3. Verification panel (Layer 1-4) in all result pages.
4. Standards reference panel with cited sections/tables.
5. Red-flag and blocked-state rendering with explicit actions.
6. Mobile/tablet responsive behavior.

## Data Contract Expectations
Render these fields when returned:
- `calculation_summary`
- `final_results`
- `layer_results`
- `flags.red_flags`, `flags.warnings`
- `calculation_steps[].standard_reference`
- `recommendations`

## Suggested File Structure
```text
/frontend
  /app
    /piping
    /vessel
    /rotating
    /electrical
    /instrumentation
    /steel
    /civil
  /components
    /layout
    /forms
    /verification
    /charts
    /ui
  /hooks
  /lib
  /styles
```

## Completion Criteria
- Seven discipline pages working with backend integration.
- 3-pane workbench stable and responsive.
- Verification and standards evidence always visible.
- Test suite for core UI and integration paths passes.

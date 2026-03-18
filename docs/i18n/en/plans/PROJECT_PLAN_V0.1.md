# EPC Intelligent Multi-Agent System Project Plan

Status: Draft  
Version: v0.1  
Last Updated: 2026-02-27

## 1) Context Summary
- Goal: Design a production-grade multi-agent system for 7 EPC maintenance disciplines with US code compliance and safety-first behavior.
- Constraint: Architecture and validation framework must be finalized before implementation.
- Operating principle: Modular design by topic/page/domain to keep debugging manageable.

## 2) Architecture Overview
- Docs-first architecture with five specification tracks:
  1. Master Orchestrator prompt/spec
  2. Multi-agent configuration spec
  3. Discipline agent persona specs
  4. Table-aware RAG spec for standards
  5. Verification framework spec (Golden Dataset + MAKER)
- 11-agent topology:
  - 7 discipline specialists
  - 4 support agents (Orchestrator, Spec Explorer, Calculator Worker, Verification Agent)
- Safety and traceability are hard requirements:
  - explicit standard references
  - unit consistency
  - conservative defaults under uncertainty
  - red-flag escalation

## 3) Detailed Execution Plan

### Phase 0 - Repository and Governance Foundation
Objective:
- Prepare docs and revision management before writing implementation code.

Deliverables:
- `docs/README.md`
- `docs/revisions/REVISION_POLICY.md`
- `docs/revisions/CHANGELOG.md`

Gate:
- Governance files exist and are accepted as project baseline.

### Phase 1 - Five Core Design Specs (No code)
Objective:
- Convert the provided five prompt blocks into implementable specifications.

Deliverables:
- `docs/specs/MASTER_ORCHESTRATOR_SPEC_V0.1.md`
- `docs/specs/MULTI_AGENT_CONFIG_SPEC_V0.1.md`
- `docs/specs/AGENT_PERSONA_TEMPLATE_SPEC_V0.1.md`
- `docs/specs/TABLE_AWARE_RAG_SPEC_V0.1.md`
- `docs/specs/VERIFICATION_FRAMEWORK_SPEC_V0.1.md`

Gate:
- Each spec includes scope, interfaces, assumptions, and validation criteria.

### Phase 2 - Interface and Schema Contracts
Objective:
- Define strict boundaries before implementation starts.

Deliverables:
- Agent communication schema (JSON)
- Input/output schemas per discipline
- Standardized report schema and red-flag taxonomy

Gate:
- Contract review pass:
  - no ambiguous field definitions
  - no mixed unit assumptions
  - explicit timeout/retry/escalation rules

### Phase 3 - Implementation Skeleton (Modular)
Objective:
- Build a thin and testable module skeleton only after spec approval.
Status:
- In progress (baseline scaffolding and contract tests created).
- In progress update: message routing, mock runtime binding, and E2E simulation tests added.
- In progress update: pipeline service added for orchestrator state + message dispatch integration.
- In progress update: piping subsystem implemented with 4-layer verification, 50-case golden dataset, and benchmark report artifacts.
- In progress update: vessel and rotating subsystems implemented with 4-layer verification and integrated runtime benchmark.

Planned module boundaries:
- `src/orchestrator/`
- `src/agents/specialists/`
- `src/agents/support/`
- `src/rag/` (ingestion, indexing, retrieval)
- `src/verification/` (maker voting, reverse checks, sanity checks)
- `src/workflows/` (standard and emergency flows)
- `src/shared/` (schemas, units, logging, errors)

Gate:
- Every module has clear input/output contract and unit test stubs.

### Phase 4 - Validation System Buildout
Objective:
- Implement safety-first validation stack.

Deliverables:
- Golden Dataset structure and loader
- MAKER voting flow
- Post-calculation reverse verification
- Physical plausibility rules and red-flag actions

Gate:
- Safety critical false negative rate target set to 0 in validation policy.

### Phase 5 - Integration and Acceptance
Objective:
- End-to-end workflow validation across selected discipline scenarios.

Deliverables:
- Standard workflow validation report
- Emergency workflow validation report
- Documentation update with known limitations

Gate:
- Predefined acceptance checklist passed.

## 4) Verification Strategy
- Multi-layer checks:
  - Pre-deployment: Golden Dataset benchmark
  - Runtime: stepwise MAKER voting and schema/unit validation
  - Post-run: reverse calculation + physical sanity + similar-case comparison
- Mandatory escalation:
  - critical red flag -> terminate and escalate
  - standards ambiguity -> conservative output + user confirmation required
- Traceability:
  - each result records formula source, standard section, assumptions, and verification status

## 5) Documentation and Revision Management Rules
- All design changes must be documented first, then implemented.
- Every major update must append one entry in `docs/revisions/CHANGELOG.md`.
- Every completed work round must append one entry in `docs/revisions/DELIVERY_LOG.md`.
- Keep specs small and topic-focused to avoid monolithic documents.
- If a requirement changes, publish impact notes:
  - impacted agent(s)
  - impacted workflow(s)
  - migration notes

Completion requirement:
- A round is treated as complete only when both Markdown records are updated:
  - `docs/revisions/CHANGELOG.md`
  - `docs/revisions/DELIVERY_LOG.md`

## 6) Immediate Next Steps
1. Freeze communication schema and red-flag taxonomy first.
2. Fill the five v0.1 specs in this fixed order: `1 -> 2 -> 4 -> 5 -> 3`.
3. Start implementation skeleton only after Phase 1 and 2 are approved.

## 7) Frontend Planning Addendum
Objective:
- Prepare a trust-centric frontend plan and specs before UI implementation.

Deliverables:
- `docs/specs/frontend/README.md`
- `docs/specs/frontend/00_OVERVIEW_AND_ARCHITECTURE_V0.1.md`
- `docs/specs/frontend/01_INFORMATION_ARCHITECTURE_AND_LAYOUT_V0.1.md`
- `docs/specs/frontend/02_COMPONENT_SYSTEM_V0.1.md`
- `docs/specs/frontend/03_API_INTEGRATION_AND_STATE_V0.1.md`
- `docs/specs/frontend/04_QUALITY_SECURITY_OPERATIONS_V0.1.md`
- `docs/specs/frontend/05_ROADMAP_V0.1.md`
- `docs/plans/FRONTEND_EXECUTION_PLAN_V0.1.md`
- `docs/prompts/FRONTEND_IMPLEMENTATION_PROMPT_V0.1.md`

Gate:
- Frontend architecture and delivery plan reviewed before code scaffold starts.

Status Update (2026-02-27):
- Frontend plan transitioned from docs-only to implemented MVP.
- Workbench UI, backend API integration mode, export flow, and QA gate are completed.
- Seven-discipline frontend depth parity completed (form/input coverage + discipline-specific mock logic expansion).
- Frontend mock engine modularized by discipline to keep code length controlled and debugging simple.
- Seven-discipline backend-mode Playwright E2E regression added and passing.
- Root-level full-stack quality gate automation added (local script + GitHub Actions workflow).
- Quality gate now supports `fast/strict` profiles and CI Playwright failure artifacts for rapid triage.
- Visual Engineering Context layer added to frontend center pane with discipline-specific SVG/chart context packs.
- Frontend 30-item optimization sprint completed:
  - glossary/tooltip reliability hardening,
  - formula and flag explainability upgrades,
  - multi-discipline input/domain option expansion,
  - full frontend quality gate rerun passed.
- See:
  - `docs/plans/FRONTEND_EXECUTION_PLAN_V0.1.md`
  - `docs/plans/FRONTEND_RELEASE_CHECKLIST_V0.1.md`

## 8) Domain-Depth Optimization Backlog
- Motivation:
  - Generic discipline templates are useful for scaffolding, but production trust requires discipline-native physics packs.
- Immediate priority:
  - Rotating `steam_turbine` deepening:
    - steam-table aware input contract
    - phase-change/wetness guardrails
    - dedicated verification and UI panels
- Expansion pattern (same strategy for other disciplines):
  - start from common template
  - split into domain-specific packs once critical physics diverges
  - keep modules short and isolated to preserve debugging speed.
- 2026-02-27 update (static equipment depth):
  - Added vessel dimension context track (height/length/head/nozzle).
  - Current UG-27 thickness core remains pressure-radius based.
  - Dimension set is now captured and surfaced for screening-level L/D, volume, and visual-context checks.
  - Added next depth step (screening): external pressure (UG-28 context) and nozzle reinforcement (UG-37 context).
  - Remaining depth step: support/load interaction modules and detailed code-edition procedures.

# EPC Maintenance AI System Overview
Status: Draft

## Purpose
- Provide one canonical starting point for system scope, document structure, and reading routes.
- Reduce root-level document sprawl by consolidating overview, navigation, and document-model guidance.

## System Scope
This repository supports a seven-discipline engineering screening and verification system for:
- Piping
- Vessel / Static Equipment
- Rotating Equipment
- Electrical
- Instrumentation
- Steel Structure
- Civil / Concrete

## Operating Model
### Agent Topology
- Orchestrator agent:
  - workflow control
  - routing
  - stage gates and escalation
- Domain agents:
  - piping
  - vessel
  - rotating
  - electrical
  - instrumentation
  - steel
  - civil
- Support agents:
  - standards checker
  - physics validator
  - reverse verifier

### Common Data Flow
1. Input ingestion and schema validation
2. Discipline classification and decomposition
3. Standards lookup and condition extraction
4. Domain calculation and design-decision execution
5. Regulatory and knowledge retrieval support
6. Deliverable generation
7. Four-layer verification
8. Cross-discipline consistency checks
9. Final report generation with confidence and flags

## Regulatory And Knowledge Layer
The platform is not only a discipline-calculation stack.
It also includes a local regulatory support layer built around:
- local KOSHA corpus snapshot sync
- KOSHA guide API sync and PDF parsing
- local SQLite FTS retrieval for RAG-style lookup
- frontend regulatory compliance and local-RAG panels
- optional local LLM answer generation on top of local retrieval

Primary artifact references:
- `README.md`
- `docs/KOSHA_DATA_SYNC_GUIDE.md`
- `outputs/api_specification.md`

Implementation anchors:
- `frontend/lib/kosha/*`
- `frontend/components/verification/local-rag-panel.tsx`
- `frontend/components/verification/regulatory-compliance-panel.tsx`
- `scripts/kosha_rag_local.py`
- `scripts/sync_kosha_corpus.py`
- `scripts/sync_kosha_guide_api.py`
- `scripts/parse_kosha_guide_pdfs.py`

## Verification Model
The common policy is a four-layer gate:
- Layer 1: input, unit, and range guard
- Layer 2: multi-path consensus
- Layer 3: physics and standards compliance
- Layer 4: reverse verification

Detailed discipline policy remains in `docs/verification_layers.md`.

## Compact Documentation Model
Use the following compact structure for each discipline:
- `README.md`
  - scope, standards, primary outputs, reading order
- `ENGINEERING_MODEL.md`
  - decision chain, factor taxonomy, deliverable logic
- `EXECUTION_CONTRACT.md`
  - input/output schema, layered verification, red flags
- `INTERFACES_AND_VALIDATION.md`
  - cross-discipline interfaces, golden cases, validation coverage

Current adoption:
- Vessel already uses the compact structure.
- Other disciplines can be migrated gradually from the previous split-file baseline.

## Unified Discipline Expansion Framework
Use one common expansion lens across all seven disciplines.
Each discipline should be described in the same order:
- basis:
  - design or operating conditions that define the problem
- decisions:
  - the engineering judgments or calculations that change the output package
- outputs:
  - the primary deliverables consumed by engineering, construction, QA, or maintenance
- validation:
  - the red flags, reverse checks, and cross-discipline interfaces that must hold

Detailed narrative guidance for the matrix below lives in:
- `docs/DISCIPLINE_EXPANSION_GUIDE.md`

## Discipline Expansion Matrix
| Discipline | Basis Focus | Decision Focus | Primary Outputs | Validation Focus |
| --- | --- | --- | --- | --- |
| Piping | fluid, pressure, temperature, line class, routing constraints | thickness, routing, spool split, support, field weld and test boundary | ISO, spool list, joint list, MTO, support list, test package inputs | spec mismatch, nozzle load, constructability, slope or vent-drain completeness |
| Vessel | pressure, temperature, material, geometry, damage state | required thickness, remaining life, FFS trigger, repair and interval logic | thickness package, FFS screening, interval recommendation, repair scope | thickness margin, external pressure, nozzle or opening concerns, damage mechanism basis |
| Rotating | asset type, duty, speed, condition indicators, protection settings | health status, nozzle-load impact, maintenance urgency, monitoring and trip logic | vibration baseline, health summary, maintenance action pack, protection review | vibration acceptance, bearing distress, alignment or foundation effects, protection consistency |
| Electrical | system topology, load profile, voltage class, protection settings | fault acceptance, coordination, arc-flash severity, transformer or feeder condition | load review, breaker margin, protection summary, arc-flash and PPE package | interrupting margin, arc-flash energy, harmonic or voltage-drop risk, equipment health |
| Instrumentation | measurement range, device type, SIL target, drift history | device adequacy, uncertainty, proof-test interval, calibration interval | loop package, SIL note, calibration plan, control-margin summary | PFDavg limit, drift tolerance, control capacity, signal integrity |
| Steel | member type, support condition, load path, section loss | capacity check, serviceability check, reinforcement or repair need | member capacity review, support loading summary, reinforcement actions | demand-capacity ratio, deflection, connection distress, external load transfer |
| Civil | foundation context, durability environment, distress observations | settlement assessment, damage-mode screening, repair priority, monitoring need | foundation review, concrete distress package, repair and monitoring plan | substantial damage, crack or spall severity, corrosion initiation, equipment tolerance |

## Discipline Directories and Main Deliverables
- `docs/piping/`
  - ISO, spool and joint list, MTO, support list, test package inputs
- `docs/vessel/`
  - thickness package, FFS screening, inspection interval, repair scope
- `docs/rotating/`
  - vibration baseline, alignment and nozzle-load review, maintenance action pack
- `docs/electrical/`
  - load and fault review, protection summary, arc-flash package
- `docs/instrumentation/`
  - loop package, SIL note, calibration and inspection plan
- `docs/steel/`
  - member capacity review, support loading, reinforcement actions
- `docs/civil/`
  - foundation review, concrete distress package, repair and monitoring plan

## Reading Routes
### Engineering Orientation
1. `docs/README.md`
2. `docs/SYSTEM_OVERVIEW.md`
3. `docs/standards_index.md`
4. `docs/DISCIPLINE_EXPANSION_GUIDE.md`
5. review the discipline expansion matrix in `docs/SYSTEM_OVERVIEW.md`
6. relevant discipline docs under `docs/<discipline>/`

### Verification and QA
1. `docs/SYSTEM_OVERVIEW.md`
2. `docs/verification_layers.md`
3. `docs/specs/VERIFICATION_FRAMEWORK_SPEC_V0.1.md`
4. `docs/golden_dataset_spec.md`

### Formal Report Preparation
1. `docs/README.md`
2. `docs/REPORT_SUBMISSION_TEMPLATE.md`
3. `docs/revisions/CHANGELOG.md`
4. `docs/revisions/DELIVERY_LOG.md`

## Migration Note
Some older root-level overview documents remain only as lightweight redirect pages for compatibility.
New overview and navigation updates should be made in this file first.

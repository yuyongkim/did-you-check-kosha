# EPC Maintenance AI Architecture Overview

## 1. Mission
Build a unified multi-agent verification system for seven maintenance disciplines:
- Piping (ASME B31.3, API 570/510)
- Static Equipment / Vessel (ASME VIII, API 510, API 579-1)
- Rotating Equipment (API 610, API 617, API 670)
- Electrical (IEEE 3000, C57.104, 1584, NFPA 70E)
- Instrumentation (IEC 61511, ISA 5.1, ISO GUM)
- Steel Structure (AISC 360 context)
- Civil/Concrete (ACI 318/562 context)

Design target:
- Integrated 4-layer verification for all disciplines
- Full standards traceability
- Cross-discipline risk checks with fail-closed safety gates

## 2. System Topology
- Orchestrator Agent:
  - workflow control
  - task routing
  - stage gates and escalation
- Domain Agents:
  - piping_agent
  - vessel_agent
  - rotating_agent
  - electrical_agent
  - instrumentation_agent
  - steel_agent
  - civil_agent
- Support Agents:
  - standards_checker_agent
  - physics_validator_agent
  - reverse_verifier_agent

## 3. Data Flow
1. Input payload ingestion and schema validation
2. Discipline classification and decomposition
3. Standards lookup and condition extraction
4. Domain calculation execution
5. 4-layer verification
6. Cross-discipline consistency checks
7. Final report generation with confidence and flags

## 4. Cross-Discipline Checks
- Piping <-> Vessel:
  - nozzle interface integrity
  - wall-thickness margin mismatch checks
- Piping <-> Rotating:
  - nozzle load transfer and vibration coupling
- Electrical <-> Rotating:
  - harmonic/power quality to machinery health coupling
- Instrumentation <-> Piping:
  - sensor drift to piping integrity coupling
- Steel <-> Piping:
  - pipe-rack overload and support deflection coupling
- Civil <-> Rotating:
  - foundation settlement/crack to vibration coupling
- Structure <-> E&I:
  - structural degradation to electrical/SIS reliability coupling

## 5. Safety and Fail-Closed Rules
- Any critical red flag blocks release.
- Any standards reference mismatch blocks release.
- Any unresolved consensus failure escalates to human review.

## 6. Deliverables
- docs/* architecture, standards, verification specs
- agents/* role-specific guidance
- config/* runtime config and policy
- golden/* 50/30/30/30/30/25/25 case specs
- outputs/* verification report, user guide, API spec

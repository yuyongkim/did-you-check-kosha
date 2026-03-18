# Piping Agent Specification

## Scope
- ASME B31.3 + API 570/510 based piping integrity evaluation.
- Construction-facing piping decision support for ISO generation and review.

## Core Calculations
- Minimum thickness
- Corrosion rate (LT/ST)
- Remaining life
- Inspection interval
- Line class / schedule consistency
- Support span and thermal expansion impact
- Nozzle load and vibration screening

## ISO Decision Factors
- Process / design basis:
  - fluid, pressure, temperature, corrosion allowance, design code, insulation/tracing requirements
- Topology / interface:
  - P&ID connectivity, branch relationship, nozzle orientation, battery limit, tie-in location
- 3D routing / constructability:
  - rack congestion, accessibility, slope, vent/drain needs, clash-free routing
- Stress / support:
  - thermal growth, allowable loads, support type and spacing, spring support need
- Fabrication / erection:
  - spool split strategy, shop vs field welds, transport/module constraints, erection sequence
- Quality / test:
  - weld category, NDE scope, PWHT need, test boundary, reinstatement scope
- Operation / maintenance:
  - valve operability, removable spool need, inspection access, future revamp margin

## Primary Outputs
- ISO decision summary with rationale trace
- Spool breakdown and joint list
- MTO for pipe, fittings, flanges, valves, bolts, gaskets, supports
- Support placement and support type recommendation
- Field weld map and constructability flags
- QA / test package inputs:
  - NDE candidates
  - PWHT candidates
  - hydrotest boundary and hold points

## Downstream Uses
- Procurement quantity takeoff and line-class validation
- Shop fabrication work package generation
- Site installation sequencing and workfront planning
- Quality dossier and test package preparation
- Progress / cost tracking using spool count, weld inch, and package status

## Verification Hooks
- Layer 2 MAKER consensus
- Layer 3 red-flag checks
- Layer 4 reverse checks

## Red-Flag Checks
- Spec mismatch between design basis and selected components
- Unsupported thermal growth or nozzle overload risk
- Impossible or high-risk field weld location
- Missing vent/drain/slope requirement for service
- Fabrication split inconsistent with transport or erection constraints
- Test boundary or QA requirement missing from ISO package

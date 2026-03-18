# Discipline Expansion Guide
Status: Draft

## Purpose
- Provide one detailed, readable guide for how each discipline expands from engineering basis to deliverables and validation.
- Complement the summary matrix in `docs/SYSTEM_OVERVIEW.md`.
- Make the intent understandable to reviewers who need more than a one-line table.

## How To Use This Guide
Read each discipline in the same order:
1. Basis
2. Main factors
3. Decision logic
4. Primary outputs
5. Downstream use
6. Validation focus

## Common Expansion Lens
Every discipline should be explainable with the same six questions:
- What defines the problem?
- Which factors actually change the engineering decision?
- What decisions are made from those factors?
- What deliverables come out of those decisions?
- Who uses those outputs downstream?
- What can invalidate the result?

## 1. Piping
### Basis
- Fluid, pressure, temperature, corrosion allowance, line class, code basis
- P&ID connectivity, equipment nozzles, branch logic, tie-in points
- 3D routing, access, slope, vent and drain requirements

### Main Factors
- Process and design basis
- Topology and interface conditions
- Routing and constructability constraints
- Stress and support constraints
- Fabrication, erection, QA, and maintenance constraints

### Decision Logic
- Determine line class, schedule, insulation, and test basis
- Fix route shape and dimensional break points
- Decide spool split, support arrangement, and field-weld locations
- Define QA and hydrotest boundaries

### Primary Outputs
- ISO
- Spool list and joint list
- MTO
- Support list
- QA and test package inputs

### Downstream Use
- Procurement quantity takeoff
- Shop fabrication work packs
- Site installation sequence and workfront planning
- Quality traceability and hydrotest preparation
- Progress and cost tracking through spool and weld metrics

### Validation Focus
- Spec mismatch with design basis
- Nozzle load or thermal-growth problems
- Impossible field-weld location
- Missing slope, vent, or drain requirement
- Missing QA or test boundary definition

## 2. Vessel
### Basis
- Pressure, temperature, material, corrosion allowance, code basis
- Shell, head, nozzle, and support geometry
- Damage observations, thickness history, and inspection history

### Main Factors
- Design basis
- Geometry and openings
- Damage mechanism and severity
- Fabrication and repair context
- Inspection criticality and accessibility

### Decision Logic
- Calculate required thickness and margin
- Screen remaining life and inspection interval
- Decide whether FFS or repair review is required
- Define inspection and repair scope

### Primary Outputs
- Thickness package
- Remaining-life summary
- FFS screening summary
- Inspection interval recommendation
- Repair scope

### Downstream Use
- RBI planning
- Shutdown and repair scope definition
- Inspection work-pack preparation
- Nozzle and piping interface review

### Validation Focus
- Thickness below required minimum
- External-pressure concern
- Nozzle or opening reinforcement concern
- Missing damage-mechanism basis
- Interval unsupported by remaining-life logic

## 3. Rotating
### Basis
- Asset type, duty, speed, driver, and criticality
- Vibration, bearing, lubrication, and thermal condition data
- Nozzle load, alignment, base, and foundation context

### Main Factors
- Asset and duty context
- Condition indicators and trends
- Mechanical interface condition
- Protection settings and trip philosophy
- Maintenance history and outage constraints

### Decision Logic
- Determine health status and urgency
- Separate internal condition problems from coupled external causes
- Decide monitoring escalation, maintenance action, and protection review needs

### Primary Outputs
- Vibration baseline
- Health summary
- Maintenance action pack
- Protection review

### Downstream Use
- Reliability review meetings
- Shutdown scope planning
- CMMS task generation
- Cross-discipline root-cause investigation

### Validation Focus
- Vibration limit exceedance
- Bearing or lubrication distress
- Alignment or foundation effects
- Piping-induced nozzle-load effects
- Protection inconsistency

## 4. Electrical
### Basis
- System topology, voltage level, source configuration, load profile
- Breaker settings, fault duty, transformer condition, and power-quality state

### Main Factors
- System basis and loading
- Protection and coordination settings
- Asset health condition
- Power-quality environment
- Arc-flash and work-practice constraints

### Decision Logic
- Assess fault-current acceptance and interrupting margin
- Decide coordination adequacy and protection concerns
- Screen transformer and feeder health
- Determine arc-flash severity and PPE implications

### Primary Outputs
- Load review
- Breaker and fault-margin summary
- Protection summary
- Arc-flash and PPE package

### Downstream Use
- Operations switching review
- Outage and maintenance planning
- Safety labeling and PPE management
- Motor and instrumentation power-impact review

### Validation Focus
- Fault current above interrupting rating
- Arc-flash severity beyond workable limit
- Harmonic or voltage-drop issues
- Transformer-health instability
- Protection mismatch with actual duty

## 5. Instrumentation
### Basis
- Measurement variable, range, required accuracy, response need
- Device type, loop architecture, SIL target, drift history
- Signal integrity, control-valve behavior, and proof-test philosophy

### Main Factors
- Measurement basis
- Device selection and installation context
- Safety logic and SIL requirements
- Drift, calibration, and reliability history
- Control performance and signal quality

### Decision Logic
- Decide device adequacy and uncertainty acceptability
- Screen SIL performance and proof-test interval
- Set calibration and inspection intervals
- Determine control-valve or loop-performance concerns

### Primary Outputs
- Loop package
- SIL note
- Calibration and inspection plan
- Control-margin summary

### Downstream Use
- Maintenance planning
- SIS review package
- Turnaround calibration work packs
- Cross-discipline troubleshooting

### Validation Focus
- PFDavg above target limit
- Drift beyond tolerance
- Control-capacity or valve-margin exhaustion
- Calibration interval unsupported by evidence
- Signal-integrity risk unresolved

## 6. Steel
### Basis
- Member type, material grade, span, support condition, and load path
- Piping, tray, equipment, and structural loads
- Section loss, deflection, and connection condition

### Main Factors
- Structural basis and boundary conditions
- Applied loading
- Degradation state
- Serviceability constraints
- Repair and reinforcement feasibility

### Decision Logic
- Assess capacity and governing demand ratio
- Check serviceability and deflection acceptability
- Decide reinforcement, repair, or load-redistribution needs

### Primary Outputs
- Member capacity review
- Support loading summary
- Connection review
- Reinforcement or repair actions

### Downstream Use
- Pipe-rack integrity review
- Maintenance and shutdown repair planning
- Fabrication scope definition
- Support coordination with piping and electrical

### Validation Focus
- Demand-capacity ratio exceedance
- Excess deflection
- Connection distress
- Section loss invalidating assumed capacity
- External load transfer not reflected in the model

## 7. Civil
### Basis
- Foundation and reinforced-concrete context
- Durability environment and exposure
- Settlement, cracking, spalling, and anchor condition observations

### Main Factors
- Structural and reinforcement basis
- Durability and corrosion initiation risk
- Distress mode and severity
- Interface with supported equipment and structures
- Repairability and monitoring needs

### Decision Logic
- Assess structural adequacy and serviceability
- Determine governing damage mode
- Decide repair priority and monitoring urgency
- Evaluate whether attached assets are affected

### Primary Outputs
- Foundation review
- Concrete distress package
- Repair priority
- Monitoring plan

### Downstream Use
- Repair planning
- Equipment support review
- Shutdown preparation
- Cross-discipline consequence analysis

### Validation Focus
- Substantial damage condition
- Crack or spall severity
- Corrosion initiation risk
- Settlement beyond equipment tolerance
- Anchor or support distress affecting attached systems

## Summary
The matrix in `docs/SYSTEM_OVERVIEW.md` is the quick map.
This document is the readable explanation of what that map means in practice.

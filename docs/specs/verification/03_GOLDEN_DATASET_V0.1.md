# Golden Dataset Design and Usage

Status: Draft  
Version: v0.1  
Last Updated: 2026-02-26

## Objective
Create a trusted benchmark set for pre-deployment and continuous runtime quality assurance.

## Coverage Policy
- Minimum 50 validated cases per discipline before production release of that discipline.
- Case mix target:
  - Real project cases
  - Standard example cases
  - Edge and error-injection cases

## Required Fields per Case
- case_id, discipline, calculation_type, complexity
- normalized input schema with units
- expected intermediate steps and references
- expected final results with tolerances
- safety critical flag
- SME verification metadata

## Quality Gates
- Two independent SME reviews for critical cases.
- Cross-check against commercial tools where applicable.
- Standards reference completeness check for every case.

## Evaluation Metrics
- Numerical accuracy and tolerance hit rate.
- Process compliance accuracy (correct references and step order).
- Safety miss rate (critical false negative), target = 0.
- Discipline-level and overall pass rates.

## Lifecycle Management
- Semantic versioning for dataset releases.
- Changelog entry for every case addition or correction.
- Periodic expansion based on observed runtime failures.

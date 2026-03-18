# Golden Dataset Specification

## 1. Discipline Targets
- Piping: 50 cases
- Vessel: 30 cases
- Rotating: 30 cases
- Electrical: 30 cases
- Instrumentation: 30 cases
- Steel: 25 cases
- Civil: 25 cases

## 2. Category Ratio
- Standard: 60%
- Boundary: 25%
- Failure mode: 15%

## 3. Required Case Schema
```json
{
  "case_id": "string",
  "discipline": "piping|vessel|rotating|electrical|instrumentation|steel|civil",
  "category": "standard|boundary|failure_mode",
  "subtype": "string",
  "inputs": {},
  "expected_outputs": {},
  "validation_points": ["string"],
  "standards_referenced": ["string"],
  "criticality_level": "normal|safety",
  "cross_discipline_checks": ["string"]
}
```

## 4. Evaluation Policy
- Critical cases tolerance: +/-1%
- Non-critical cases tolerance: +/-3%
- Standards citation coverage: 100%
- Red-flag detection target: 100% for critical conditions

## 5. Governance
- Dataset versioning required.
- Every update must be logged in changelog.
- Any edition change in standards requires impacted case refresh.

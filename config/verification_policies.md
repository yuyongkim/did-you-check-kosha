# Verification Policies

## Global Thresholds
- Layer 2 consensus tolerance: 1% relative
- Reverse check warning: >2%
- Reverse check escalation: >5%

## Red-Flag Policy
- Critical: block and escalate immediately
- High: block release and force revalidation
- Medium: warning with extra checks
- Low: log only

## Discipline-Specific Emphasis
- Piping:
  - thickness below minimum
  - temperature limit breach
  - unrealistic corrosion behavior
- Vessel:
  - required thickness shortfall
  - joint-efficiency misuse
  - local thinning trigger
- Rotating:
  - vibration threshold exceedance
  - nozzle load exceedance
  - protection logic mismatch
- Electrical:
  - transformer health criticality
  - arc-flash energy exceedance
  - breaker interrupt-rating exceedance
  - voltage drop and harmonic distortion limits
- Instrumentation:
  - SIL target non-compliance
  - drift exceedance and low-confidence regression
  - control valve capacity margin risk
- Steel:
  - structural D/C critical or overstressed range
  - excessive section loss due to corrosion
  - serviceability deflection exceedance
  - connection failure indication
- Civil:
  - ACI 562 substantial damage criteria
  - carbonation-driven corrosion initiation
  - crack width/spalling/settlement durability risks

## Human-in-the-Loop
Mandatory when:
- unresolved consensus failure
- standard reference conflict
- any critical red flag
- reverse-check escalation threshold breach

## Cross-Discipline Threshold Profiles
- File: `config/cross_discipline_threshold_profiles.json`
- Profiles:
  - `conservative`: lower risk tolerance, higher blocking rate expected
  - `balanced`: default runtime profile
  - `permissive`: reduced false-positive blocking for marginal cases
- Benchmark commands:
  - `python scripts/benchmark_cross_discipline.py --profile active`
  - `python scripts/benchmark_cross_discipline.py --profile all`
- Tuning command:
  - `python scripts/tune_cross_discipline_thresholds.py --rounds 50`

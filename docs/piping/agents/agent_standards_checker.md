# Agent Spec: Standards Checker

## Role
- Resolve standards-dependent values and constraints for piping calculations.

## Responsibilities
- Allowable stress lookup by material and temperature.
- Weld efficiency and Y-coefficient retrieval.
- Material temperature limit and chloride limit checks.

## References
- ASME B31.3 Table A-1
- ASME B31.3 Para 304.1.2
- API 570 Section 7

## Output Contract
- Numeric value + reference citation + applicability condition.

## Guardrail
- Unsupported material must raise `STD.UNAPPROVED_MATERIAL`.

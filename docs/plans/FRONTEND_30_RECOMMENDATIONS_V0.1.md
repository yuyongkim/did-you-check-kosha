# Frontend 30 Recommendations Sprint

Status: Completed  
Version: v0.1  
Last Updated: 2026-02-27

## Objective
- Execute 30 high-impact frontend improvements for trust, readability, and domain depth.
- Keep modules short and maintainable while improving real usability.

## Completed Items (30/30)
1. [x] Normalize corrupted home-page text content.
2. [x] Add concise `When To Use` section in homepage.
3. [x] Add concise `How To Use` quick steps in homepage.
4. [x] Normalize top-bar glossary button label.
5. [x] Normalize sidebar glossary shortcut label.
6. [x] Harden term-help `?` with hover + click behavior.
7. [x] Add outside-click close for term-help popover.
8. [x] Improve term-help keyboard focus visibility.
9. [x] Ensure term-help always resolves non-empty definition text.
10. [x] Add glossary filtered/total counters.
11. [x] Keep pinned glossary items stable under query filter.
12. [x] Add glossary pin export success feedback.
13. [x] Add glossary pin import success/failure feedback.
14. [x] Add glossary pin clear feedback.
15. [x] Add glossary pin reorder controls (`Up` / `Down`).
16. [x] Improve chart axis text contrast.
17. [x] Improve chart tooltip contrast and readability.
18. [x] Remove corrupted formula symbols in trace renderer.
19. [x] Normalize formula operator spacing.
20. [x] Expand formula hint coverage for core equations.
21. [x] Add red-flag taxonomy map (`code -> meaning`).
22. [x] Show code + meaning in blocked output banner.
23. [x] Show code + meaning in warnings/red flags panel.
24. [x] Add conditional visibility for vessel length/height fields.
25. [x] Expand vessel material options (alloy/stainless additions).
26. [x] Expand rotating machine types (including recip/expander).
27. [x] Add explicit steam-screening note in rotating visuals.
28. [x] Expand electrical equipment categories.
29. [x] Expand instrumentation device categories.
30. [x] Expand steel/civil/piping domain options:
   - steel grade expansion + grade-aware Fy fallback,
   - civil exposure expansion,
   - piping fluid taxonomy + NPS/OD table expansion.

## Validation
- `npm --prefix frontend run typecheck` passed.
- `npm --prefix frontend run lint` passed.
- `npm --prefix frontend run test:unit` passed.
- `npm --prefix frontend run build` passed.

## Notes
- This sprint prioritized deterministic UX and explainability first.
- Next optimization wave should target:
  - richer equation rendering (Math-like UI),
  - standards-source deep-linking by discipline,
  - scenario presets and batch comparison for engineer workflows.

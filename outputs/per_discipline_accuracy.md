# Per-Discipline Calculation Accuracy Breakdown

- Total cases: 220
- Passed cases: 220
- Overall accuracy: 1.0000
- Source dataset: `datasets/golden_standards/*_golden_dataset_v1.json`
- Code path: `scripts/benchmark_all_runtime.py` (re-used).

## Per-Discipline Table

| Discipline | Cases | Pass | Fail | Accuracy | Primary metric | Mean rel. err | Max rel. err | RF precision | RF recall |
|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| piping | 50 | 50 | 0 | 1.0000 | t_min_mm | 0.000000 | 0.000000 | 1.0000 | 1.0000 |
| vessel | 30 | 30 | 0 | 1.0000 | t_required_shell_mm | 0.000000 | 0.000000 | 1.0000 | 1.0000 |
| rotating | 30 | 30 | 0 | 1.0000 | vibration_mm_per_s | 0.000000 | 0.000000 | 1.0000 | 1.0000 |
| electrical | 30 | 30 | 0 | 1.0000 | transformer_health_index | 0.000000 | 0.000000 | 1.0000 | 1.0000 |
| instrumentation | 30 | 30 | 0 | 1.0000 | pfdavg | 0.000000 | 0.000000 | 1.0000 | 1.0000 |
| steel | 25 | 25 | 0 | 1.0000 | phi_pn_kn | 0.000000 | 0.000000 | 1.0000 | 1.0000 |
| civil | 25 | 25 | 0 | 1.0000 | phi_mn_knm | 0.000000 | 0.000000 | 1.0000 | 1.0000 |

## Red-flag Confusion (Per-Discipline)

Per-flag, per-case counts: TP = expected and predicted; FP = predicted but not expected; FN = expected but not predicted.

| Discipline | TP | FP | FN |
|---|---:|---:|---:|
| piping | 29 | 0 | 0 |
| vessel | 13 | 0 | 0 |
| rotating | 14 | 0 | 0 |
| electrical | 24 | 0 | 0 |
| instrumentation | 28 | 0 | 0 |
| steel | 26 | 0 | 0 |
| civil | 26 | 0 | 0 |

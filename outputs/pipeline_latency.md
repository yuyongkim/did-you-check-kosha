# Pipeline End-to-End Latency Report

- Platform: Windows 10 (AMD64)
- Python: 3.13.7
- CPU: AMD64 Family 25 Model 33 Stepping 2, AuthenticAMD
- Repetitions per stage: 5 (median + p95 reported)

## Per-Discipline Layered Stack (Layers 1-4 Combined, service.evaluate)

| Discipline | Case ID | Criticality | Median (ms) | p95 (ms) | Min (ms) | Max (ms) |
|---|---|---|---:|---:|---:|---:|
| piping | PIP-GOLD-001 | normal | 0.06 | 0.19 | 0.05 | 0.19 |
| vessel | VES-GOLD-001 | normal | 0.06 | 0.13 | 0.05 | 0.13 |
| rotating | ROT-GOLD-001 | normal | 0.04 | 0.10 | 0.04 | 0.10 |
| electrical | ELE-GOLD-001 | normal | 0.04 | 0.09 | 0.03 | 0.09 |
| instrumentation | INS-GOLD-001 | normal | 0.08 | 0.15 | 0.06 | 0.15 |
| steel | STL-GOLD-001 | normal | 0.03 | 0.07 | 0.03 | 0.07 |
| civil | CIV-GOLD-001 | normal | 0.03 | 0.08 | 0.03 | 0.08 |

## Piping Per-Layer Breakdown
_Case: PIP-GOLD-001_

| Layer | Median (ms) | p95 (ms) | Min (ms) | Max (ms) |
|---|---:|---:|---:|---:|
| layer1_input_validation | 0.002 | 0.004 | 0.001 | 0.004 |
| layer2_k_voting_3candidates_plus_consensus | 0.017 | 0.020 | 0.015 | 0.020 |
| layer3_physics_and_standards | 0.002 | 0.005 | 0.002 | 0.005 |
| layer4_reverse_checks | 0.003 | 0.005 | 0.002 | 0.005 |

## Cross-Discipline Validator (One Paired Call Across 7 Disciplines)

- Median: 0.028 ms
- p95: 0.045 ms
- Min/Max: 0.021 / 0.045 ms

## KOSHA RAG Retrieval (top-10)

- Query: `pressure vessel remaining life assessment`
- Hit count: 4
- Median: 1.151 ms
- p95: 3.351 ms
- Min/Max: 1.018 / 3.351 ms

## KOSHA RAG Generation (Qwen via Ollama)

- Model: qwen3:4b
- Prompt chars: 2054
- Median: 41725.0 ms
- p95: 62277.2 ms
- Min/Max: 31919.7 / 62277.2 ms

## End-to-End Median

Composition: piping `service.evaluate` median + cross-discipline validator median + RAG retrieval median (+ RAG generation median).

- End-to-end median: 41726.22 ms

# Submission Tables

Updated: 2026-03-16

## Table 3. Cross-Domain Validator Ablation

| Scenario Set | Validator OFF | Validator ON | Absolute Delta | Ratio Delta |
|---|---:|---:|---:|---:|
| aligned_standard | 0 / 10 | 0 / 10 | +0 | +0.00 |
| aligned_boundary | 0 / 6 | 6 / 6 | +6 | +1.00 |
| aligned_failure | 0 / 4 | 4 / 4 | +4 | +1.00 |
| mixed_first20 | 0 / 20 | 3 / 20 | +3 | +0.15 |
| mixed_random20 | 0 / 20 | 12 / 20 | +12 | +0.60 |
| **Overall** | **0 / 60** | **25 / 60** | **+25** | **+0.4167** |

## Table 6. KOSHA RAG Retrieval Benchmark

| Metric | Plain FTS | Enhanced FTS | Absolute Delta |
|---|---:|---:|---:|
| Recall@1 | 0.44 | 0.74 | +0.30 |
| Recall@3 | 0.74 | 0.86 | +0.12 |
| Recall@5 | 0.74 | 0.86 | +0.12 |
| MRR@10 | 0.5744 | 0.7933 | +0.2189 |

## Table 7. Code-Only vs Regulatory RAG Case Ablation

| Case | Code-Only Detected | Regulatory RAG Detected | First Relevant Rank |
|---|---:|---:|---:|
| VES-GOLD-001 | 0 | 1 | 1 |
| VES-GOLD-009 | 0 | 1 | 1 |
| PIP-GOLD-047 | 0 | 1 | 1 |
| **Total** | **0 / 3** | **3 / 3** | — |

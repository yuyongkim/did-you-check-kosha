# Layer-by-Layer Ablation Report (Table 7b)

- Profile: tuned_round_50

## Table 7b: Internal Ablation by System Layer

| Configuration | Cross-discipline blocks (60-case set) | KOSHA-jurisdiction detections (3-case set) |
|---|---:|---:|
| Calc engines only | 0 / 60 | 0 / 3 |
| Calc + Cross-discipline validator | 26 / 60 | 0 / 3 |
| Calc + KOSHA RAG (no K-voting, no validator) | 0 / 60 | 3 / 3 |
| Full system (Calc + K-voting + Validator + RAG) | 26 / 60 | 3 / 3 |

## K-voting Assumption

K-voting is a verification-quality layer that does not, by itself, change either of the two columns measured here. Per the manuscript (PAPER_JLP_REVISED_v2.md, §6.6, last paragraph of Layer-B), K-voting suppresses numerical-precision artefacts but does not contribute new cross-discipline blocks or new KOSHA detections. The K-voting toggle therefore has no effect on these two counts.

## Per-Configuration Detail

### Calc engines only

- validator_on=False, rag_on=False, k_voting_on=False
- cross-discipline blocks: 0 / 60
  - aligned_standard: 0/10
  - aligned_boundary: 0/6
  - aligned_failure: 0/4
  - mixed_first20: 0/20
  - mixed_random20: 0/20
- KOSHA detections: 0 / 3
  - VES-GOLD-001: rag_detected=False, first_relevant_rank=None
  - VES-GOLD-009: rag_detected=False, first_relevant_rank=None
  - PIP-GOLD-047: rag_detected=False, first_relevant_rank=None

### Calc + Cross-discipline validator

- validator_on=True, rag_on=False, k_voting_on=False
- cross-discipline blocks: 26 / 60
  - aligned_standard: 0/10
  - aligned_boundary: 6/6
  - aligned_failure: 4/4
  - mixed_first20: 3/20
  - mixed_random20: 13/20
- KOSHA detections: 0 / 3
  - VES-GOLD-001: rag_detected=False, first_relevant_rank=None
  - VES-GOLD-009: rag_detected=False, first_relevant_rank=None
  - PIP-GOLD-047: rag_detected=False, first_relevant_rank=None

### Calc + KOSHA RAG (no K-voting, no validator)

- validator_on=False, rag_on=True, k_voting_on=False
- cross-discipline blocks: 0 / 60
  - aligned_standard: 0/10
  - aligned_boundary: 0/6
  - aligned_failure: 0/4
  - mixed_first20: 0/20
  - mixed_random20: 0/20
- KOSHA detections: 3 / 3
  - VES-GOLD-001: rag_detected=True, first_relevant_rank=1
  - VES-GOLD-009: rag_detected=True, first_relevant_rank=1
  - PIP-GOLD-047: rag_detected=True, first_relevant_rank=1

### Full system (Calc + K-voting + Validator + RAG)

- validator_on=True, rag_on=True, k_voting_on=True
- cross-discipline blocks: 26 / 60
  - aligned_standard: 0/10
  - aligned_boundary: 6/6
  - aligned_failure: 4/4
  - mixed_first20: 3/20
  - mixed_random20: 13/20
- KOSHA detections: 3 / 3
  - VES-GOLD-001: rag_detected=True, first_relevant_rank=1
  - VES-GOLD-009: rag_detected=True, first_relevant_rank=1
  - PIP-GOLD-047: rag_detected=True, first_relevant_rank=1


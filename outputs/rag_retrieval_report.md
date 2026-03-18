# RAG Retrieval Benchmark Report

- Dataset: `datasets/kosha_rag/rag_eval_queries.json`
- Group Count: 5
- Query Count: 50
- Query design: 5 regulatory target groups x 10 curated queries each, mixing Korean/English phrasings, abbreviations, and variant wording.

## Overall Metrics
- Plain FTS: Recall@1=0.4400, Recall@3=0.7400, Recall@5=0.7400, MRR@10=0.5744
- Enhanced FTS: Recall@1=0.7400, Recall@3=0.8600, Recall@5=0.8600, MRR@10=0.7933
- Delta: Recall@1=0.3000, Recall@3=0.1200, Recall@5=0.1200, MRR@10=0.2189

## Group Metrics
- M-69 remaining life: Plain R@5=0.9000, Enhanced R@5=1.0000, delta=0.1000
- C-C-23 RBI: Plain R@5=0.9000, Enhanced R@5=0.9000, delta=0.0000
- B-M-18 piping life: Plain R@5=0.6000, Enhanced R@5=0.8000, delta=0.2000
- C-C-75 corrosion risk: Plain R@5=0.8000, Enhanced R@5=0.9000, delta=0.1000
- Article 256 corrosion prevention: Plain R@5=0.5000, Enhanced R@5=0.7000, delta=0.2000

## Code-Only vs Regulatory RAG Ablation
- `Code-only` here means international-code calculation outputs and engine red flags without Korean regulatory retrieval.
- Code-only detected cases: 0/3
- Regulatory RAG detected cases: 3/3
- VES-GOLD-001: code_only=False, rag=True, first_relevant_rank=1
- VES-GOLD-009: code_only=False, rag=True, first_relevant_rank=1
- PIP-GOLD-047: code_only=False, rag=True, first_relevant_rank=1

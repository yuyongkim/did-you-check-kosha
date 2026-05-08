# KOSHA RAG Bootstrap 95% CI Report

- Dataset: `datasets/kosha_rag/rag_eval_queries.json`
- Queries: 50
- Bootstrap draws: 1000
- Seed: 20260508

## Point Estimates (deterministic, full sample)

| Metric | Plain | Enhanced | Delta (E - P) |
|---|---:|---:|---:|
| recall_at_1 | 0.4400 | 0.7400 | +0.3000 |
| recall_at_3 | 0.7400 | 0.8600 | +0.1200 |
| recall_at_5 | 0.7400 | 0.8600 | +0.1200 |
| mrr_at_10 | 0.5744 | 0.7933 | +0.2189 |

## Bootstrap 95% CI (percentile method)

### Plain mode

| Metric | Mean | 2.5% | 97.5% |
|---|---:|---:|---:|
| recall_at_1 | 0.4390 | 0.3000 | 0.5600 |
| recall_at_3 | 0.7405 | 0.6200 | 0.8600 |
| recall_at_5 | 0.7405 | 0.6200 | 0.8600 |
| mrr_at_10 | 0.5741 | 0.4556 | 0.6845 |

### Enhanced mode

| Metric | Mean | 2.5% | 97.5% |
|---|---:|---:|---:|
| recall_at_1 | 0.7422 | 0.6200 | 0.8600 |
| recall_at_3 | 0.8621 | 0.7600 | 0.9405 |
| recall_at_5 | 0.8621 | 0.7600 | 0.9405 |
| mrr_at_10 | 0.7956 | 0.6933 | 0.8967 |

### Paired difference (Enhanced - Plain)

_This is the most meaningful CI for the manuscript improvement claim:_
_a CI strictly above zero supports the Enhanced-mode advantage._

| Metric | Mean | 2.5% | 97.5% | CI excludes 0? |
|---|---:|---:|---:|---|
| recall_at_1 | +0.3031 | +0.1400 | +0.4800 | yes |
| recall_at_3 | +0.1216 | -0.0200 | +0.2600 | no |
| recall_at_5 | +0.1216 | -0.0200 | +0.2600 | no |
| mrr_at_10 | +0.2215 | +0.0911 | +0.3534 | yes |

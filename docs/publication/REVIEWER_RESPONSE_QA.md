# Reviewer Response Q&A

Updated: 2026-03-16

This note is intended for submission-time reviewer response preparation.

## 1) Is synonym expansion actually applied during retrieval?
Yes. The live retrieval path in `src/rag/local_kosha_rag.py` calls the concept-aware query builder in `src/rag/engineering_synonyms.py`, which joins concepts with AND and synonyms within each concept with OR.

Evidence:
- `src/rag/local_kosha_rag.py`
- `src/rag/engineering_synonyms.py`

## 2) Isn’t BM25 weak for Korean regulatory retrieval?
The limitation is acknowledged. The current system mitigates this with concept-aware query construction, bilingual synonym expansion, and a loose fallback query when strict concept matching returns no hits. Retrieval quality is quantified separately from generation quality.

Evidence:
- `outputs/rag_retrieval_report.md`
- `scripts/benchmark_rag_retrieval.py`

## 3) Isn’t the 50-query benchmark curated?
Yes. It is a curated benchmark designed to test the manuscript’s explicit regulatory claims. The curation policy is transparent: five target groups, ten query variants each, mixing Korean, English, abbreviations, and wording variants.

Evidence:
- `datasets/kosha_rag/rag_eval_queries.json`
- `docs/publication/PAPER_EN_v2.md`

## 4) Is the “jurisdiction compliance gap” only a narrative claim?
No. The manuscript operationalizes the gap through case ablation: code-only outputs do not surface Korean regulatory obligations, while regulatory RAG does. The effect is shown at both benchmark level and manuscript case level.

Evidence:
- `outputs/rag_retrieval_report.md`
- `docs/publication/PAPER_EN_v2.md`

## 5) Does the cross-discipline validator add measurable value?
Yes. In the 60-scenario ablation, validator OFF blocks 0 scenarios and validator ON blocks 25. The aligned boundary and aligned failure subsets both rise from 0.0 to 1.0 blocking ratio.

Evidence:
- `outputs/cross_discipline_ablation_report.md`
- `scripts/benchmark_cross_discipline_ablation.py`

## 6) Are legal links stable enough for reviewer inspection?
For major law/rule categories, law-article metadata is normalized and direct article URLs are resolved to `lsScJoRltInfoR.do` where available. The runtime follows `resolved_url > direct_url > search_url`.

Evidence:
- `src/rag/law_article_metadata.py`
- `scripts/resolve_law_article_direct_urls.py`
- `config/law_article_link_overrides.json`

## 7) Why is the SQLite index not included in the submission package?
The submission package excludes the prebuilt SQLite index intentionally to keep the archive compact and source-oriented. Reproducibility is preserved via normalized datasets plus rebuild scripts.

Evidence:
- `README_SUBMISSION_PACKAGE.md`
- `docs/publication/SUBMISSION_CHECKLIST.md`

## 8) How is redistribution risk handled for regulatory content?
The package is curated to emphasize source code, normalized metadata, and manuscript-facing evidence rather than raw portal dumps or unnecessary binaries. The included datasets are the minimum needed to reconstruct the retrieval environment described in the manuscript.

Evidence:
- `README_SUBMISSION_PACKAGE.md`
- `docs/publication/PAPER_EN_v2.md`

## 9) How is hallucination risk controlled in the RAG layer?
The generation stage is grounded on retrieved context only and requires citation indices in the answer format. Retrieval is benchmarked separately so evidence quality can be evaluated independently of generation.

Evidence:
- `src/rag/local_kosha_rag.py`
- `outputs/rag_retrieval_report.md`

## 10) Can reviewers reproduce the package in a clean environment?
The package includes a copy-paste rebuild block, a verified environment note, the normalized datasets needed for reconstruction, and the benchmark scripts used in the paper. Final release/tag confirmation remains a manual submission-time step.

Evidence:
- `docs/publication/SUBMISSION_CHECKLIST.md`
- `README_SUBMISSION_PACKAGE.md`

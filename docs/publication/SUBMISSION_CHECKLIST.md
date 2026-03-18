# Paper Submission Checklist

Updated: 2026-03-16

## Done
- [x] Manuscript path and code path alignment checked against `docs/publication/CODE_MAP.md`
- [x] Cross-discipline ablation results generated
- [x] RAG retrieval benchmark results generated
- [x] Article 256 legal basis normalized to `산업안전보건기준에 관한 규칙`
- [x] Law-article metadata enriched with `law_name`, `article_label`, `query_seed`, and direct/reconstructed URLs
- [x] Repo-layout source bundle generation script prepared

## Manual Final Checks
- [ ] Click every bibliography DOI / landing URL once before submission
- [ ] Confirm the exact GitHub tag or release name to cite in the paper
- [ ] Do one final proofreading pass on the manuscript text
- [ ] Verify the final zip opens cleanly and key files are present

## Verified Environment
- Python: `3.13.7`
- Shell: `PowerShell`
- Platform used for final verification: `Windows`

## Copy-Paste Reproduction Block
```powershell
python -m pip install -r requirements.txt
python scripts/enrich_law_article_metadata.py
python scripts/resolve_law_article_direct_urls.py
python scripts/kosha_rag_local.py build --rebuild
python scripts/benchmark_all_runtime.py
python scripts/benchmark_cross_discipline.py --profile all
python scripts/benchmark_cross_discipline_ablation.py
python scripts/benchmark_rag_retrieval.py
python -m unittest tests.test_rag_synonyms
python scripts/build_paper_submission_package.py
```

## Install Note
- API serving uses `requirements.txt`
- Submission / benchmark environment can use `submission_requirements.txt`
- PDF parsing rebuilds additionally rely on `PyMuPDF` or `PyPDF2` as listed in `submission_requirements.txt`

## Expected Evidence Files
- `outputs/verification_report_runtime.md`
- `outputs/seven_pipeline_report.md`
- `outputs/cross_discipline_report.md`
- `outputs/cross_discipline_ablation_report.md`
- `outputs/rag_retrieval_report.md`

## Rebuild Commands
```powershell
python scripts/enrich_law_article_metadata.py
python scripts/resolve_law_article_direct_urls.py
python scripts/kosha_rag_local.py build --rebuild
python scripts/benchmark_all_runtime.py
python scripts/benchmark_cross_discipline.py --profile all
python scripts/benchmark_cross_discipline_ablation.py
python scripts/benchmark_rag_retrieval.py
python scripts/build_paper_submission_package.py
```

## Submission Package Goal
- Keep only manuscript-facing assets:
  - paper docs
  - mapped source code
  - benchmark / reproduction scripts
  - minimal datasets needed for reproducibility
  - generated reports

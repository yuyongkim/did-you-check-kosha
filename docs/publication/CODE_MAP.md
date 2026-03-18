# Paper Code Map
# PAPER_EN_v2.md <-> Source File Index
# Generated: 2026-03-15

## Paper Section -> Source File Mapping

### Section 3. System Architecture
- Orchestrator: src/orchestrator/
- API layer: src/api/
- Shared schema & types: src/shared/

### Section 4. KOSHA Regulatory Knowledge Layer
| Component | File |
|---|---|
| RAG pipeline (retrieval + generation) | src/rag/local_kosha_rag.py |
| RAG contracts / interfaces | src/rag/contracts.py |
| Engineering synonym dictionary (BM25 expansion) | src/rag/engineering_synonyms.py |
| Law-article metadata helper | src/rag/law_article_metadata.py |
| KOSHA corpus sync (smart-search API) | scripts/sync_kosha_corpus.py |
| KOSHA Guide API download | scripts/sync_kosha_guide_api.py |
| KOSHA Guide PDF parser | scripts/parse_kosha_guide_pdfs.py |
| Encoding validator / repair | scripts/validate_kosha_encoding.py |
| RAG CLI entrypoint | scripts/kosha_rag_local.py |
| Law-article metadata backfill | scripts/enrich_law_article_metadata.py |
| Law-article direct URL resolver | scripts/resolve_law_article_direct_urls.py |
| Law-article override config | config/law_article_link_overrides.json |
| SQLite FTS index | datasets/kosha_rag/kosha_local_rag.sqlite3 |
| Guide PDFs | datasets/kosha_guide/files/ |
| Law articles JSON | datasets/kosha/normalized/law_articles.json |
| Guide chunks (JSONL) | datasets/kosha_guide/normalized/guide_chunks.jsonl.gz |

### Section 5.1 Domain Calculation Engines
| Domain | Directory |
|---|---|
| Piping (ASME B31.3, API 570) | src/piping/ |
| Vessel (ASME VIII, API 510, 579) | src/vessel/ |
| Rotating (API 610/617/670) | src/rotating/ |
| Electrical (IEEE C57.104, 1584) | src/electrical/ |
| Instrumentation (IEC 61511) | src/instrumentation/ |
| Steel (AISC 360) | src/steel/ |
| Civil (ACI 318, 562) | src/civil/ |

### Section 5.2 Four-Layer Hybrid Verification Model
| Layer | File |
|---|---|
| Layer 1: Input validation | src/verification/gates.py |
| Layer 2: K-voting consensus | src/verification/maker.py |
| Layer 3: Physics/code compliance | src/verification/gates.py, src/shared/red_flags.py |
| Layer 4: Reverse verification | src/verification/reverse_check.py |
| Verification orchestration | src/verification/engine.py |

### Section 5.3 Cross-Domain Consistency Validator
| Component | File |
|---|---|
| Validator (10 domain pairs) | src/cross_discipline/validator.py |
| Threshold tuning script | scripts/tune_cross_discipline_thresholds.py |
| Cross-discipline benchmark | scripts/benchmark_cross_discipline.py |

### Section 6.1 Golden Dataset (220 cases)
| Domain | File |
|---|---|
| Piping (50 cases) | datasets/golden_standards/piping_golden_dataset_v1.json |
| Vessel (30 cases) | datasets/golden_standards/vessel_golden_dataset_v1.json |
| Rotating | datasets/golden_standards/rotating_golden_dataset_v1.json |
| Electrical | datasets/golden_standards/electrical_golden_dataset_v1.json |
| Instrumentation | datasets/golden_standards/instrumentation_golden_dataset_v1.json |
| Steel | datasets/golden_standards/steel_golden_dataset_v1.json |
| Civil | datasets/golden_standards/civil_golden_dataset_v1.json |

Dataset generation scripts: scripts/generate_*_golden_dataset.py

### Section 6.2 Pipeline Benchmark
| Benchmark | Script |
|---|---|
| All-runtime (7 disciplines) | scripts/benchmark_all_runtime.py |
| Seven-discipline pipeline | scripts/benchmark_seven_pipeline.py |
| Five-discipline pipeline | scripts/benchmark_five_pipeline.py |
| Piping only | scripts/benchmark_piping_system.py |
| Cross-discipline ablation (validator off/on) | scripts/benchmark_cross_discipline_ablation.py |
| RAG retrieval benchmark (plain vs enhanced FTS) | scripts/benchmark_rag_retrieval.py |

Retrieval benchmark dataset:
- `datasets/kosha_rag/rag_eval_queries.json`

Generated reports:
- `outputs/cross_discipline_ablation_report.md`
- `outputs/rag_retrieval_report.md`

### Paper Table 4 / Table 5 — RAG Case Data
Source cases from golden datasets:
- Case 1 (VES-GOLD-001): datasets/golden_standards/vessel_golden_dataset_v1.json
- Case 2 (VES-GOLD-009): datasets/golden_standards/vessel_golden_dataset_v1.json
- Case 3 (PIP-GOLD-047): datasets/golden_standards/piping_golden_dataset_v1.json

KOSHA documents retrieved:
- M-69-2012: datasets/kosha_guide/files/M-69-2012__압력용기의 잔여수명 평가에 관한 기술지침.pdf
- C-C-23-2026: datasets/kosha_guide/files/C-C-23-2026__위험기반검사(RBI) 기법에 의한 설비의 신뢰성 향상에 관한 기술지원규정.pdf
- B-M-18-2026: datasets/kosha_guide/files/B-M-18-2026__배관 수명관리 기술지원규정.pdf
- C-C-75-2026: datasets/kosha_guide/files/C-C-75-2026__화학설비의 부식 위험성평가에 관한 기술지원규정.pdf
- Article 256: datasets/kosha/normalized/law_articles.json (산업안전보건기준에 관한 규칙 제256조 부식 방지)

## Reproducibility Commands

# 1. Build KOSHA RAG index (from scratch)
python scripts/sync_kosha_corpus.py --force
python scripts/sync_kosha_guide_api.py --download
python scripts/parse_kosha_guide_pdfs.py
python scripts/enrich_law_article_metadata.py
python scripts/resolve_law_article_direct_urls.py
python scripts/kosha_rag_local.py build --rebuild

# 2. Run RAG query (Case 3 example)
python scripts/kosha_rag_local.py query "화학설비 배관 부식 방지 법령 요건 클로라이드 서비스" --top-k 8 --generate

# 3. Run all golden dataset benchmarks
python scripts/benchmark_all_runtime.py

# 4. Run seven-discipline pipeline benchmark
python scripts/benchmark_seven_pipeline.py

# 5. Run cross-discipline coupling benchmark
python scripts/benchmark_cross_discipline.py --profile all

# 6. Run cross-discipline ablation
python scripts/benchmark_cross_discipline_ablation.py

# 7. Run RAG retrieval benchmark
python scripts/benchmark_rag_retrieval.py

# 8. Rebuild repo-layout publication bundle
python scripts/build_publication_bundle.py

# 9. Tune cross-discipline thresholds
python scripts/tune_cross_discipline_thresholds.py --rounds 50

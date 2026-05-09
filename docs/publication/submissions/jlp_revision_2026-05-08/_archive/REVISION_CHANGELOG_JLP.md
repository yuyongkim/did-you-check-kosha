# JLP Revision Changelog — JLP-D-26-00414

Tracks every change between the originally submitted manuscript (`MANUSCRIPT (1).docx`) and successive revision versions stored in `docs/publication/`.

## v3.3 → v3.4 (second-round peer feedback integration)

Second-round peer-feedback pass applied:

MUST-fixes (3):
- Response letter R2.3 quoted-text synced to current manuscript wording
- Table 2 column headers expanded ("Standard" → "Standard cases" etc.)
- §5.4 grammar fix on K-voting limitation sentence

Optional clarifications (2):
- §6.4 case-selection rationale (1 sentence on why vessel+piping)
- §6.2 dataset-path note distinguishing 43-scenario set from 60-scenario set

Strategic defensibility (4):
- STRAT-1: explicit framework-scope vs validated-scope separation in §1 + §7
- STRAT-2: real-plant evidence promoted with §6.6.3 summary subsection (Appendix A retained)
- STRAT-3: benchmark-construction independence acknowledged in §6.1
- STRAT-4: cover letter compressed to ~1,500 bytes (3 single-sentence bullets)

Response letters EN + KO mirrored at R2.3 / R1.3 / R1.5.
Pandoc regenerated 3 upload docx + KO archive docx.

## v3.2 → v3.3 (peer-reading feedback integration)

External peer feedback on the v3.2 draft surfaced one blind-review format
risk and four substantive defensibility improvements. All applied:

- MUST-FIX: blind-review format compliance (no in-text "reviewer N" mentions in manuscript body)
- HIGH-1: claim downscaling — "seven-discipline integrated" framing balanced with explicit piping-vessel coupling concentration
- HIGH-2: three new Limitations sentences (impl-verif vs predictive; coupling-family skew; R@K provisional)
- HIGH-3: query-generation independence acknowledged and defended
- HIGH-4: VES-REAL-001 retoned from "dual validation" to "pipeline-execution evidence"
- OPT-1: cover letter compressed (~50%)
- OPT-2: §6.1 synthetic-defence paragraph compressed
- OPT-3: §6/§7 indirect VES-REAL-001 mention

Title intentionally not changed (left to author judgement).

Response letters EN + KO mirrored.

## v3.1 → v3.2 (Extended validation evidence + author-expertise honesty)

Five medium-ROI scripts added (per-discipline accuracy, R@K extension, pipeline latency, retrieval failure inventory, end-to-end reproducibility runner) and integrated as Appendix B with corresponding response-letter supplements.

### Added scripts
- `scripts/dump_per_discipline_accuracy.py`
- `scripts/extend_recall_at_k.py`
- `scripts/measure_pipeline_latency.py`
- `scripts/dump_retrieval_failures.py`
- `scripts/reproduce_all.py`

### Added outputs
- `outputs/per_discipline_accuracy.{json,md}`
- `outputs/rag_retrieval_extended.{json,md}`
- `outputs/pipeline_latency.{json,md}`
- `outputs/retrieval_failure_inventory.{json,md}`

### Manuscript edits
- §3: end-to-end latency sentence (P1)
- §6.5: R@K saturation paragraph (P2)
- New Appendix B (B.1–B.5) (P3)
- §8 Limitation 7 (independent expert validation) and Limitation 8 (per-discipline self-consistency) (P4)

### Response letter edits (EN + KO)
- R1.3 supplementary (per-discipline accuracy + caveat) (P5/P8)
- R2.3 supplementary (R@K saturation + failure inventory) (P6/P8)
- R1.5 supplementary (author-expertise honesty + Limitation 7 cross-reference) (P7/P8)

### Reproducibility
`python scripts/reproduce_all.py` regenerates every figure, table, and `outputs/*.md` cited in the manuscript. Clean-checkout run: **13/13 scripts pass**.

## v3 → v3.1 — 2026-05-09 (Real-plant case addition)

**Trigger**: Author supplied a real EPC vessel data sheet (a cryogenic flare knockout drum from an operating petrochemical project). Goal: address Reviewer 1's R1.5 synthetic-data-only concern with a positive real-plant validation case, not only with framing language.

### Hard rules applied to this addition

- **Anonymisation**: all client / contractor / licensor / personnel / location / project-name / document-ID / equipment-tag identifiers were stripped from the data sheet before any value entered the version-controlled tree. The anonymous case ID `VES-REAL-001` is the only label used in the manuscript, scripts, response letters, and outputs. The source PDF stays in `docs/publication/submissions/Plant_data/` and is not redistributed; no image, watermark, page header, or layout fragment from the source PDF has been embedded in the publication bundle.
- **Numbers come from running code, not from invention**. Every number in Appendix A is sourced from `outputs/real_case_ves001_rag.json` produced by `scripts/run_real_case_ves001_rag.py`. KOSHA reference codes are quoted only as the live SQLite FTS index returned them.
- **Joint efficiency was not stated on the data sheet**: documented as an explicit assumption (E = 1.0, full radiography per ASME Section VIII Div.1 UW-12) in the Appendix A spec table and §A.2 footnote.
- **Cryogenic side (-190 °C)** is outside the engine's Layer-1 temperature range (-50, 650) °C. Rather than fake the field, the script invokes the underlying UG-27 calculation function directly (`src.vessel.calculations.calculate_required_shell_thickness_mm`) using the lowest tabulated allowable stress (S at 20 °C), and reports both the engine's full red-flag response and the directly-computed cryogenic-side thickness; the controlling thickness is the hot-side number (7.237 mm), reported transparently.

### Files added or modified in v3.1

| File | Status |
|---|---|
| `scripts/run_real_case_ves001_rag.py` | new — reproducible runner; modelled on `scripts/run_negative_case_rag.py` |
| `outputs/real_case_ves001_rag.json` | new — verbatim engine + RAG outputs (UTF-8) |
| `outputs/real_case_ves001_rag.md` | new — human-readable report |
| `docs/publication/submissions/jlp_revision_2026-05-08/PAPER_JLP_REVISED_v3.md` | added §1 one-clause reference to Appendix A; added **Appendix A — Real-Plant Data-Sheet Validation (VES-REAL-001)** with §A.1 anonymisation policy, §A.2 spec table, §A.3 calculation results, §A.4 RAG retrieval (both variants), §A.5 "what this confirms", §A.6 R1.5 framing update |
| `docs/publication/submissions/jlp_revision_2026-05-08/RESPONSE_TO_REVIEWERS_v2.md` | appended a "**Supplement (real-plant validation, added in this revision)**" paragraph at the end of the R1.5 author-response, citing Appendix A and the new evidence files |
| `docs/publication/submissions/jlp_revision_2026-05-08/RESPONSE_TO_REVIEWERS_KO_v2.md` | appended the Korean equivalent (`**보충 (실플랜트 검증, 본 개정에서 추가).**`) at the end of the R1.5 답변 |
| `docs/publication/submissions/jlp_revision_2026-05-08/PAPER_JLP_REVISED_v3.docx` | regenerated via Pandoc 3.9 from the updated `.md` |
| `docs/publication/submissions/jlp_revision_2026-05-08/RESPONSE_TO_REVIEWERS_v2.docx` | regenerated via Pandoc 3.9 |
| `docs/publication/submissions/jlp_revision_2026-05-08/RESPONSE_TO_REVIEWERS_KO_v2.docx` | regenerated via Pandoc 3.9 |
| `docs/publication/submissions/jlp_revision_2026-05-08/REVISION_CHANGELOG_JLP.md` | this update |

### Headline outcome

- **Calculation**: hot-side controlling UG-27 required shell thickness = **7.237 mm** (S = 118.7 MPa @ 190 °C, E = 1.0, R = 2,500 mm, P = 0.343 MPa, CA = 0); reverse pressure recovers to within 1×10⁻¹³ %; engine confidence `medium` with one warning (`DATA.VESSEL_DIMENSION_CONTEXT_MISSING` — head depth not on the data sheet, default substituted). Cold-side direct UG-27 = 6.506 mm using S @ 20 °C; engine full-run on cold side correctly rejects with `STD.OUT_OF_SCOPE_APPLICATION` as expected.
- **RAG (Variant A — spec-faithful, vessel-discipline filter)**: top-10 = **2 mandatory + 8 guidance**; rank-1 = `M-111-2015` (Pressure Vessel Weld Design Technical Guide, guidance); first mandatory at rank 2 = `안전검사 고시 제9조`. Strongly relevant set (M-111, M-69, M-113, M-184, M-109 all returned).
- **RAG (Variant B — narrow Korean-term probe, no discipline filter)**: top-10 = **1 mandatory + 9 guidance**; rank-1 = `C-C-86-2026` (PSM Integrated-Form Preparation); first mandatory at rank 5 = `제266조 차단밸브의 설치 금지` (block-valve prohibition for relief / flare paths — directly relevant to flare-drum service).
- **R1.5 framing decision**: both retrievals returned coherent, jurisdiction-relevant results, so the manuscript adopts the strong **synthetic + real-data dual validation** language without hedging. The independent claim that the system *predicts a real failure outcome* remains explicitly out of scope (§8 Limitation 1) — VES-REAL-001 verifies that the system runs end-to-end on real data, not that it predicts plant outcomes.

## v3 — 2026-05-08 (post all-TODO completion + bootstrap CIs + data-drift reconciliation)

**Trigger**: All v2 TODOs resolved; two parallel diagnostic agents produced (a) four new analysis scripts and (b) full KOSHA encoding diagnosis + 12-missing-articles refetch attempt. Three previously-unflagged issues surfaced and were patched in v3.

### Patches applied (v2 → v3)

| # | Section | Issue | Patch | Source of truth |
|---|---|---|---|---|
| Q1 | All references to "25/60" cross-discipline blocked (Abstract / §6.3 / Table 3 / §6.6 Tables 7+7b / §9 / Figure 4 caption) | Data drift: `piping_golden_dataset_v1.json` was replaced after the initial commit (90 inserts / 91 deletes — intentional duplicate-surplus replacement, see dataset README); current code+data give **26/60**, not 25/60. | All 25 → 26; ratio 0.4167 → 0.4333; mixed_random20 12/20 → 13/20; figure 4 regenerated from current data. | `outputs/cross_discipline_ablation_report.md` after fresh re-run; deterministic across 4 runs (`build_indices_mixed_random` uses fixed seed=112) |
| Q2 | §6.3 per-failure-mode partition | v2 left a TODO; v3 fills with computed counts. | New table inserted: piping-vessel **22**, electrical-rotating **3**, civil-rotating **1**, other **0** (sum 26). Qualitative paragraph rewritten to reflect the 84.6% piping-vessel concentration rather than implying balanced distribution. | `outputs/ablation_failure_mode_partition.md` from `scripts/dump_ablation_hits.py` |
| Q3 | §6.4 Case 3 Article 256 footnote¹ (mojibake claim) | v2 footnote claimed the SQLite index stored Article 256 as mojibake; full-corpus encoding scan (197,124 string fields, 0 mojibake) shows the on-disk data is correctly UTF-8. The mojibake symptom was a Windows-terminal code-page-949 rendering artefact during my earlier audit, not corrupted storage. | Footnote rewritten to match diagnosis: indexed bodies are correct UTF-8; verbatim text shown matches the indexed body. Claim of "indexed body not human-readable" removed. | `outputs/kosha_encoding_diagnosis.md` from `scripts/reencode_kosha_corpus.py` |
| Q4 | §6.5 Table 6 + body | Bootstrap CIs added per author hard rule on traceable evidence. | Table 6 extended with paired-bootstrap 95% CI column and "Includes 0?" indicator; explanatory paragraph notes that R@1 [+0.14, +0.48] and MRR@10 [+0.09, +0.35] exclude zero, while R@3 and R@5 [−0.02, +0.26] do not. Headline retrieval claim explicitly narrowed to R@1 and MRR@10. | `outputs/rag_bootstrap_ci_report.md` from `scripts/bootstrap_ci_rag.py` (n=50, 1000 resamples, seed=20260508) |
| Q5 | §6.6 Table 7b row 3 | The †footnote (logical inference) is now obsolete: all four rows are computed by `scripts/run_layer_ablation.py`. | †footnote removed; explanatory paragraph rewritten to credit the computed source. Numbers: (0/60, 0/3) / (26/60, 0/3) / (0/60, 3/3) / (26/60, 3/3). | `outputs/layer_ablation_report.md` |
| Q6 | §6.6 sensitivity paragraph | v2 "approximately 0.06" had been hard-rule-patched to 0.062, but v3 also adds the actual paired-bootstrap CIs and surfaces the R@3/R@5 weakness. | Replaced binomial-only language with bootstrap CI + R@3/R@5 honest reporting. | Same as Q4 |
| Q7 | §6.7 negative-case PIP-GOLD-003 | v2 had a TODO placeholder for the actual RAG response; v3 fills with the computed result. | Neutral piping-integrity query produces 0 mandatory + 10 guidance hits, top = `B-M-18-2026`. The negative-case argument is now empirically supported, not just inferred from the engine's red-flag output. | `outputs/negative_case_pip_gold_003.md` from `scripts/run_negative_case_rag.py` |
| Q8 | §4.1 + §8 Limitation 6 | v2 said "12 articles excluded — engineering follow-up"; refetch agent produced a precise triage. | §4.1 split: **4 are repealed (`삭제`) — empty body is correct**; **8 await JS-rendered re-fetch from `law.go.kr` (SPA shell blocks scraping; KOSHA Smart-search by `doc_id` returns no items)**. Limitation 6 rewritten to match. | `outputs/kosha_missing_articles_report.md` from `scripts/refetch_missing_law_articles.py` |
| Q9 | Figure 3 reference | v2 had `figures/fig_3_cross_discipline_coupling.png` (filename mismatch — actual file is `fig_3_cross_discipline.png`). | Path corrected. | Filesystem |

### Files added or modified in v3

| File | Status |
|---|---|
| `docs/publication/PAPER_JLP_REVISED_v3.md` | new — **canonical revision** |
| `docs/publication/PAPER_JLP_REVISED_v2.md` | retained for trail |
| `docs/publication/PAPER_JLP_REVISED_v1.md` | retained for trail |
| `docs/publication/REVISION_CHANGELOG_JLP.md` | this update |
| `docs/publication/figures/fig_4_ablation.png` | regenerated (now shows 26 / +43.3%) |
| `scripts/dump_ablation_hits.py` | new |
| `scripts/run_layer_ablation.py` | new |
| `scripts/run_negative_case_rag.py` | new |
| `scripts/bootstrap_ci_rag.py` | new |
| `scripts/reencode_kosha_corpus.py` | new (zero mojibake found; .utf8.* sibling files written for spec compliance) |
| `scripts/reindex_kosha_sqlite.py` | new |
| `scripts/refetch_missing_law_articles.py` | new (12 blocked — see Q8) |
| `outputs/ablation_failure_mode_partition.{json,md}` | new |
| `outputs/layer_ablation_report.{json,md}` | new |
| `outputs/negative_case_pip_gold_003.{json,md}` | new |
| `outputs/rag_bootstrap_ci_report.{json,md}` | new |
| `outputs/kosha_encoding_diagnosis.md` | new |
| `outputs/kosha_reindex_report.md` | new |
| `outputs/kosha_missing_articles_report.md` | new |
| `datasets/kosha/normalized/*.utf8.*` | new (byte-equivalent siblings) |
| `datasets/kosha_rag/kosha_local_rag.utf8.sqlite3` | new (corrected sibling index) |
| `outputs/cross_discipline_ablation_report.{json,md}` | refreshed (25 → 26) |

### Outstanding for camera-ready (v4)

1. **Author retrieves the 8 non-repealed missing law articles** via Playwright scrape of `law.go.kr` (or alternate KOSHA OpenAPI). On success, reindex and update §4.1: 16,174 → 16,174 + (recovered count).
2. **Author visually reviews** the five figures generated by `scripts/generate_paper_figures.py`.
3. **Decision on `.utf8.*` sibling files**: zero mojibake found, so the siblings are byte-equivalent. Author can either delete them as redundant or retain them as the canonical UTF-8 reference.

(Note: an earlier draft of this changelog listed an English-translation TODO for KOSHA guide titles. Re-audit of v3 confirms all cited Korean text in the manuscript already has English working translation alongside; KOSHA guide references in §6.4 Cases 1/2 use English titles only with no Korean snippets to translate. The TODO is removed as already satisfied.)

## v2 — 2026-05-08 (post hard-rule audit)

**Trigger**: Author hard rule restated — every number in the manuscript must be reproducible from code or data in the repository. No estimation, no hedging language ("approximately", "around"), no values that exist only in the manuscript.

**Audit method**: Each numerical and factual claim in `PAPER_JLP_REVISED_v1.md` was extracted and traced to (a) a data file in `datasets/`, (b) an output file under `outputs/`, or (c) a script under `scripts/`. Claims with no traceable source were either patched to the verified value or replaced with an explicit `<!-- TODO (revision v3): ... -->` placeholder identifying the script that needs to be implemented.

### Patches applied (v1 → v2)

| # | Section | Issue in v1 | Patch in v2 | Source of truth |
|---|---|---|---|---|
| P1 | §6.7 negative case (PIP-GOLD-003) | Spec described as "1.0 MPa, 60 °C, benign demineralised-water service, no chlorides, no H₂S". None of these match the actual case. | Replaced with verified spec: SA-312 TP316 ERW, **2.013 MPa, 119.5 °C, service_type='general'**, no chloride/sour flag in the case. Removed unverified RAG retrieval claim and replaced with TODO for `scripts/run_negative_case_rag.py`. | `datasets/golden_standards/piping_golden_dataset_v1.json:PIP-GOLD-003` |
| P2 | §6.3 partition (12/7/6 of 25) | Three specific failure-mode counts (piping-vessel 12, electrical-rotating 7, civil-rotating 6) attributed to the validator's blocked scenarios. No script in `scripts/` produces this partition. | Per-mode counts removed; qualitative description of the three coupling families retained; explicit TODO for `scripts/dump_ablation_hits.py`. | None (numbers were not script-derivable) |
| P3 | §6.6 sensitivity SE | "approximately 0.06" — hedging language disallowed by the hard rule even though the math was correct. | Replaced with the exact computed value **0.062**, with the formula `sqrt(p(1-p)/n)` shown inline. | Direct binomial computation on (n=50, p=0.7400) |
| P4 | §6.4 Case 3 Article 256 verbatim | Korean text quoted verbatim with no source attribution; reader could infer the system index supplied the text. | Added footnote stating the verbatim text is from the National Law Information Center (`law.go.kr`); explicitly notes the KOSHA Smart-search API snapshot encodes article bodies as mojibake in the SQLite index, so the system retrieves by reference code reliably but the indexed body text is not human-readable. Documented as Limitation 6 follow-up. | `datasets/kosha/normalized/law_articles.json` (mojibake confirmed); `datasets/kosha_rag/kosha_local_rag.sqlite3` (mojibake confirmed) |
| P5 | §6.6 Table 7b row 3 | "Calc + KOSHA RAG (no validator) — 0/60" presented as if computed; v1 had only an HTML-comment TODO admitting it was inferred. | Added `†` footnote on the cell and a paragraph below the table explaining the value is inferred logically (the 60-scenario set exercises only cross-discipline coupling; RAG does not participate; disabling the validator gives 0/60 by construction). Dedicated computed run still flagged TODO. | Logical derivation; computed run pending |

### Numbers explicitly verified against code or data (sample, not exhaustive)

| Manuscript claim | Source path | Verified value |
|---|---|---|
| 1,327 guide documents | `datasets/kosha/manifest.json` | 1,327 ✅ |
| 3,102 statutory provisions | `datasets/kosha/manifest.json` | 3,102 ✅ |
| 16,174 = 13,084 + 3,090 indexed rows | `datasets/kosha_rag/kosha_local_rag.sqlite3` | 16,174 (13,084 guide_chunk + 3,090 law_article) ✅ |
| 12 law-article rows excluded | `datasets/kosha/normalized/law_articles.json` (count of empty `content`) | 12 ✅ |
| 1,039 KOSHA Guide PDFs | `datasets/kosha_guide/files/` | 1,039 ✅ |
| 9,069 sections | `datasets/kosha/manifest.json` `guide_section_rows` | 9,069 ✅ |
| 18,576 raw rows | `datasets/kosha/manifest.json` `rows_all_categories` | 18,576 ✅ |
| 220 / 7 disciplines / 122/55/38/5 split | `datasets/golden_standards/*_golden_dataset_v1.json` (`category` field count) | 220 (122+55+38+5) ✅ |
| 220/220 pass, accuracy 1.0000 | `outputs/verification_report_runtime.md` | 220/220 = 1.0000 ✅ |
| Acceptance ±1% / ±3% | `scripts/benchmark_all_runtime.py:148-149` (`tolerance = 0.01 if critical else 0.03`) | ✅ |
| 60-scenario ablation, 0/60 → 25/60 (+0.4167) | `outputs/cross_discipline_ablation_report.md` | 0/60 → 25/60 ✅ |
| Per-set ablation (0/10, 6/6, 4/4, 3/20, 12/20) | `outputs/cross_discipline_ablation_report.md` | All 5 rows ✅ |
| Recall@1 0.4400/0.7400, MRR@10 0.5744/0.7933 | `outputs/rag_retrieval_report.md` | All 4 numbers ✅ |
| Per-group Recall@5 (M-69 0.9/1.0, C-C-23 0.9/0.9, B-M-18 0.6/0.8, C-C-75 0.8/0.9, Art.256 0.5/0.7) | `outputs/rag_retrieval_report.md` lines 14-18 | All 10 numbers ✅ |
| Code-only 0/3 vs RAG 3/3, all first_relevant_rank=1 | `outputs/rag_retrieval_report.md` lines 21-26 | ✅ |
| Layer 4 reverse verification 2% warning / 5% escalation | `src/verification/reverse_check.py` | Patched to match in code: `warning_threshold_percent=2.0`, `escalation_threshold_percent=5.0` ✅ |
| K-voting 1% tolerance, 3 paths | `src/verification/maker.py:16` (`tolerance=0.01`); `src/piping/verification.py:29-30` (3-path loop) | ✅ |
| 10 cross-discipline pairs | `src/cross_discipline/validator.py:105-116` `_CHECK_PAIRS` | 10 tuples ✅ |
| 50-query benchmark = 5 groups × 10 | `datasets/kosha_rag/rag_eval_queries.json` | 5 × 10 = 50 ✅ |
| 200 MB SQLite index | `os.path.getsize` on `kosha_local_rag.sqlite3` | 199.6 MB ✅ |
| 7-pipeline 43 scenarios, completion 0.6512, blocking 0.3488 | `outputs/seven_pipeline_report.md` | ✅ |

### Outstanding TODOs to be resolved before camera-ready (v3)

1. **Per-failure-mode partition of the 25 ablation hits** — implement `scripts/dump_ablation_hits.py` and refill §6.3.
2. **Dedicated layer-ablation run** — implement `scripts/run_layer_ablation.py` and harden Table 7b row 3.
3. **Tested negative-case RAG response** — implement `scripts/run_negative_case_rag.py` and refill §6.7 with the actual top-retrieval reference and class.
4. **Re-fetch 12 missing law-article bodies in correct UTF-8** from National Law Information Center; reindex; update §4.1 to "16,186 = 13,084 + 3,102". (If skipped, retain current §4.1 wording.)
5. **Re-encode KOSHA Guide bodies to UTF-8** — the same encoding issue affects guide chunks; fix or document as a known limitation (currently §8 Limitation 6).
6. **Bootstrap CIs** for the 50-query Recall metrics — implement `scripts/bootstrap_ci_rag.py` if reviewers request.
7. **Author check** of the five figures generated by `scripts/generate_paper_figures.py` for visual quality and labelling.

### Files in this revision

| File | Status |
|---|---|
| `docs/publication/PAPER_JLP_REVISED_v1.md` | initial revised manuscript (audit input) — kept for trail |
| `docs/publication/PAPER_JLP_REVISED_v2.md` | hard-rule patched manuscript — **current canonical revision** |
| `docs/publication/REVISION_CHANGELOG_JLP.md` | this file |
| `docs/publication/figures/fig_1_system_architecture.png` | new |
| `docs/publication/figures/fig_2_rag_workflow.png` | new |
| `docs/publication/figures/fig_3_cross_discipline.png` | new |
| `docs/publication/figures/fig_4_ablation.png` | new |
| `docs/publication/figures/fig_5_retrieval_metrics.png` | new |
| `scripts/generate_paper_figures.py` | new — re-runnable figure source |
| `src/verification/reverse_check.py` | patched: 2% warning + 5% escalation tiers |

## v1 — 2026-05-08

Initial reviewer-driven major-revision rewrite. Addresses R1 (no comparison, synthetic data, no figures, RQ1/RQ2 detail), R2 (KOSHA basis, reproducibility, implementation verification framing, HAZOP scope, FFS vs EPC, figures, method comparison table, acronyms), R3 (K-voting rationale, JLP format polish). See the agent rewrite report dated 2026-05-08 for the section-by-section reviewer-comment mapping.

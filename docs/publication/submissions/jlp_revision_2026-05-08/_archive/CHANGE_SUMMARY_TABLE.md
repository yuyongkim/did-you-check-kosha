# Change Summary — JLP-D-26-00414 (revision 2026-05-10)

## Quantitative scope of revision

| Metric | Initial submission (2026-03-31) | Revised submission (this) | Change |
|---|---:|---:|---|
| Word count | 4,928 | 12,992 | 4,928 -> 12,992  (+8,064, +164%) |
| Sections (headings) | 50 | 60 | 50 -> 60  (+10, +20%) |
| Body paragraphs | 160 | 249 | 160 -> 249  (+89, +56%) |
| Tables | 7 | 24 | 7 -> 24  (+17, +243%) |
| Figures | 0 | 5 | 5 (new) |

**TL;DR.** The revised manuscript is **2.6x** the original word count, adds **17 new tables**, **5 new figures**, and **10 new sections**. This is a major rewrite, not a typo pass.

## Per-section change list

**39 sections changed: 16 NEW + 23 REVISED.** Reviewer coverage in this list: R1 in ~21 rows, R2 in ~20 rows, R3 in ~3 rows.

| # | Section | Type | Triggered by | What changed |
|---:|---|:--:|---|---|
| 1 | Abstract | **REVISED** | R1.4, R2.1 | Reframed synthetic results as implementation verification; tightened retrieval claims to stat-significant K (Recall@1, MRR@10 with paired-bootstrap 95% CI). |
| 2 | 1. Introduction | **REVISED** | R1.1, R2.1 | Tightened motivation; introduced jurisdiction compliance gap terminology; clarified two-RQ scope. |
| 3 | 2.1 AI Applications in Process Safety | **REVISED** | R2.x | Updated literature framing for process-safety AI. |
| 4 | 2.2 RAG in Technical and Regulatory Domains | **REVISED** | R2.x | Revised RAG-in-regulatory-domains positioning. |
| 5 | 2.3 Multi-Discipline Maintenance and AI | **REVISED** | R2.x | Clarified multi-discipline asset-integrity context. |
| 6 | 2.4 Verification Methodology — N-Version / K-Voting | **REVISED** | R3.1 | Strengthened N-version programming background relevant to K-voting rationale. |
| 7 | 2.5 Korean PSM Regulation and KOSHA | **REVISED** | R2.3 | Sharpened Korean-jurisdiction regulatory background. |
| 8 | 2.6 Position relative to HAZOP, RBI, Digital Twin | **NEW** | R2.2 | New subsection positioning the framework against HAZOP, RBI, and Digital Twin scope. |
| 9 | 3. System Architecture | **REVISED** | R1.1 | Named deterministic state machine and orchestrator (pipeline.py); added Figure 1. |
| 10 | 4.1 Corpus Construction | **REVISED** | R2.4 | Corrected corpus counts to 1,327 guides + 3,102 statutory rows -> 16,174 indexed entries (12 excluded for empty body). |
| 11 | 4.2 Retrieval and Generation Pipeline | **REVISED** | R1.1, R2.x | Formalised concept-aware query builder, synonym expansion, OR-fallback; added Figure 2. |
| 12 | 4.3 KOSHA Regulatory Grounding — Mandatory vs Guidance | **NEW** | R2.3 | New subsection separating mandatory law-articles from KOSHA guides for citation policy. |
| 13 | 4.4 Why standard EPC workflows do not cover these obligations | **NEW** | R2.3 | New subsection explaining the gap between EPC-standards review and KOSHA PSM coverage. |
| 14 | 5.1 Domain Calculation Engines | **REVISED** | R1.1 | Added Table 1 mapping seven engines -> standards -> source files. |
| 15 | 5.2 Four-Layer Hybrid Verification Model | **REVISED** | R1.1, R3.1 | Documented Layer-4 thresholds (2% warning, 5% escalation), aligned with reverse_check.py. |
| 16 | 5.3 Cross-Discipline Consistency Validator | **REVISED** | R1.1 | Documented ten-pair coupling set; Figure 3 added. |
| 17 | 5.4 Why three paths and a 1% tolerance? — K-voting design rationale | **NEW** | R3.1 | New subsection giving design rationale for K-voting (3 paths, 1% tolerance). |
| 18 | 6.1 Calculation Accuracy on the Golden Dataset (implementation verification) | **REVISED** | R1.5 | Reframed 220-case headline as implementation verification, not predictive validation; added benchmark-construction subsection. |
| 19 | 6.2 Seven-Discipline Pipeline Evaluation | **REVISED** | R1.x | Clarified 43-scenario pipeline-eval scope vs 60-scenario ablation in §6.3. |
| 20 | 6.3 Cross-Discipline Validator Ablation (RQ1) | **REVISED** | R1.1 | Updated headline to 26/60 (+0.4333, drift-corrected); added per-failure-mode 22/3/1 partition; Figure 4 added. |
| 21 | 6.4 KOSHA RAG Regulatory Grounding — Three Cases (RQ2) | **REVISED** | R2.3 | Each case now identifies the specific mandatory KOSHA article surfaced (Article 256 / 266 / B-M-18). |
| 22 | 6.5 Curated Retrieval Benchmark (RQ2) | **REVISED** | R1.4 | Added paired-bootstrap 95% CI; honest disclosure that Recall@3/@5 CI includes zero; Figure 5 added. |
| 23 | 6.6 Industry-Baseline Comparison and Internal Ablation | **NEW** | R1.1 | New subsection: industry baseline (ASME/API pass = compliance complete) 0/3 vs 3/3, plus four-layer ablation Table 7b. |
| 24 | 6.6.3 Real-plant pipeline-execution evidence | **NEW** | R1.5 | Body-level summary of VES-REAL-001 anonymised cryogenic flare-drum case; Article 266 surfaced naturally. |
| 25 | 6.7 Citation Traceability and Negative-Case Evidence | **NEW** | R1.5 | New subsection on citation-traceability precision (100% by construction) and PIP-GOLD-003 negative case. |
| 26 | 7.1 The jurisdiction compliance gap | **REVISED** | R1.x, R2.1 | Sharpened gap definition tying calculation-only review to KOSHA PSM obligations. |
| 27 | 7.2 Compliance co-pilot, not replacement | **NEW** | R2.2 | New subsection positioning the framework as a compliance co-pilot for HAZOP / RBI / Digital Twin / Regulatory RAG. |
| 28 | 7.3 HAZOP scope clarification | **NEW** | R2.2 | New subsection: knowledge-based / AI-assisted, not a replacement for dynamic HAZOP. |
| 29 | 7.4 Fitness-for-Service vs EPC standards | **NEW** | R2.5 | New subsection separating FFS workflows from EPC-standards verification scope. |
| 30 | 7.5 Process-safety contribution | **REVISED** | R2.x | Clarified the process-safety contribution narrative. |
| 31 | 7.6 Reproducibility and explainability | **NEW** | R1.x, R2.x | New subsection documenting end-to-end reproducibility (scripts/reproduce_all.py 13/13). |
| 32 | 8. Limitations and Future Work | **REVISED** | R1.5, R2.1 | Expanded from 3 -> 8 limitations including framework-vs-validated scope and benchmark-construction independence. |
| 33 | 9. Conclusion | **REVISED** | R1.x | Synthesised the revised contribution: integrated platform, four-layer verification, KOSHA RAG. |
| 34 | Acknowledgements | **REVISED** | blind-review | Acknowledgements reworded for strict blind-review compliance (no direct reviewer tokens in body). |
| 35 | Code and Data Availability | **NEW** | R1.x | New section with AGPL-3.0 code/data release statement. |
| 36 | Acronyms | **NEW** | JLP-style | New acronym glossary (JLP house style). |
| 37 | Key Definitions | **NEW** | JLP-style | New key-term definitions for clarity. |
| 38 | Appendix A. Real-Plant Data-Sheet Validation (VES-REAL-001) | **NEW** | R1.5 | New appendix: anonymised real-plant cryogenic flare-drum case with UG-27 calculation + KOSHA RAG retrieval (both probe variants). |
| 39 | Appendix B — Extended validation evidence | **NEW** | R1.x, R2.x | New appendix: per-discipline accuracy, Recall@K (K = 1..10), pipeline latency, retrieval failure inventory, full reproducibility manifest. |

*See `RESPONSE_TO_REVIEWERS_v2.docx` for the full per-comment author response, and `PAPER_JLP_REVISED_v3_MARKED.docx` for the word-level visual diff.*

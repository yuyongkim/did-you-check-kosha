# Cover Letter — Resubmission to Journal of Loss Prevention in the Process Industries

---

**Date:** 2026-05-08

**Manuscript number:** JLP-D-26-00414 (revised)

**To:** Professor Paul Amyotte
Receiving Editor
*Journal of Loss Prevention in the Process Industries*
Elsevier

**Re:** Resubmission of revised manuscript "Detecting Jurisdiction Compliance Gaps in Process Plant Engineering with Regulatory RAG"

---

Dear Professor Amyotte,

Thank you for the opportunity to revise our manuscript JLP-D-26-00414, and please convey our gratitude to the three reviewers, whose detailed comments substantially strengthened the work. We are pleased to resubmit the revised manuscript together with a point-by-point Response to Reviewers letter.

**Summary of key revisions.** All three reviewers' concerns have been addressed at both the structure and evidence level:

1. **Reviewer 1 — comparison and supporting data.** The revised §6.6 introduces a two-layer comparison framework: (i) an *industry-baseline* comparison — defining "ASME/API pass = compliance complete" as the prevailing current practice, against which the three case studies yield 0/3 detections versus our system's 3/3 — and (ii) an *internal four-layer ablation* (Table 7b) decomposing detection contributions by Calc / Cross-discipline / KOSHA RAG / Full system. The 25/60 → 26/60 cross-discipline ablation (+0.4333 absolute) is now accompanied by a per-failure-mode partition (piping-vessel 22, electrical-rotating 3, civil-rotating 1; sum = 26) and five new figures (system architecture, RAG workflow, cross-discipline coupling, ablation, retrieval). The synthetic-data concern is addressed by reframing the result as **implementation verification, not predictive validation**, with a three-component defence (regulatory inversion, medical-AI / AV simulation precedent, feasibility framing) and a tested negative case (PIP-GOLD-003) confirming no false-positive flag.

2. **Reviewer 2 — KOSHA basis, reproducibility, and method positioning.** A new §4.3 distinguishes **mandatory** (Act / Enforcement Decree / *Rules on Occupational Safety and Health Standards*) from **guidance** (KOSHA technical guidelines), with Article 256 quoted verbatim in §6.4 (Korean + English working translation). Reproducibility is strengthened with explicit file-path references for the seven engines, the four-layer verification, and the RAG prompting strategy. A new §7.2 positions the framework as a **compliance co-pilot** (not a replacement) for HAZOP / RBI / Digital Twin via Tables 8 and 9 and four operational touchpoints. A new §7.4 clarifies the FFS / EPC-standards relationship (API 579 treated as both design-validation and operational-assessment input). Acronyms and key definitions are consolidated in a dedicated section.

3. **Reviewer 3 — K-voting rationale and JLP format.** A new §5.4 justifies the K-voting design choices (3 paths, 1% tolerance, scope of independence) explicitly tied to the implementation in `src/verification/maker.py`. The manuscript has been reformatted to the standard JLP order (introduction → related work → method → experiments → discussion → limitations → conclusion → acknowledgements → data availability → references).

**Statistical rigour.** Per Reviewer 2's request, a 95% paired-bootstrap analysis of the 50-query retrieval benchmark (n = 50, 1000 resamples, seed = 20260508) is now reported in Table 6: Recall@1 [+0.14, +0.48] and MRR@10 [+0.09, +0.35] both exclude zero, while Recall@3 and Recall@5 paired CIs of [−0.02, +0.26] do include zero. The headline retrieval claim has been honestly narrowed to Recall@1 and MRR@10; Recall@3 and Recall@5 are reported for completeness rather than as primary evidence.

**Data integrity audit.** Every numerical claim in the revised manuscript was traced to a code path or data file in the public repository. The audit surfaced and corrected several issues: (a) the previously reported "16,186" was replaced with the actual SQLite count of **16,174** (= 13,084 guide chunks + 3,090 indexed law articles), with the 12 excluded law-article rows triaged into 4 repealed (`삭제`) and 8 pending Playwright re-fetch; (b) the §5.2 Layer 4 description (2% warning / 5% escalation) now matches the implementation in `src/verification/reverse_check.py`. A full revision changelog is provided in the supplementary `REVISION_CHANGELOG_JLP.md`.

**Reproducibility.** All source code, golden datasets (220 synthetic cases across seven disciplines), the 60-scenario cross-discipline ablation set, the 50-query curated retrieval benchmark, the SQLite FTS5 index manifest, and the orchestration scripts are publicly released under the AGPL-3.0 license. Eight new analysis scripts were added during this revision (`scripts/dump_ablation_hits.py`, `run_layer_ablation.py`, `run_negative_case_rag.py`, `bootstrap_ci_rag.py`, `generate_paper_figures.py`, `reencode_kosha_corpus.py`, `reindex_kosha_sqlite.py`, `refetch_missing_law_articles.py`) so that every table and figure in the manuscript is reproducible from the repository with a single command.

**Confirmations.** The manuscript remains exclusive to *Journal of Loss Prevention in the Process Industries*; it has not been published or submitted elsewhere. There are no conflicts of interest to declare.

We look forward to your decision and to any further comments from the reviewers.

Sincerely,

**Yuyong Kim**
University of Wisconsin–Madison
M.S. Data, Insights & Analytics Candidate; B.S. Chemical & Biological Engineering
12+ years of professional experience in petrochemical EPC and process plant engineering
[linkedin.com/in/yuyongkim](https://linkedin.com/in/yuyongkim)

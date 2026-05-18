**Date:** 2026-05-10

**Manuscript number:** JLP-D-26-00414 (revised)

**To:** Professor Paul Amyotte, Receiving Editor, *Journal of Loss Prevention in the Process Industries*

**Re:** Resubmission of "Detecting Jurisdiction Compliance Gaps in Process Plant Engineering with Regulatory RAG" (title preserved from initial submission)

---

Dear Professor Amyotte,

Thank you for the opportunity to revise JLP-D-26-00414. This is a substantially revised manuscript prepared directly in response to the reviewers' concerns, while preserving the manuscript's central research question and contribution (the *jurisdiction compliance gap* between international engineering codes and Korean PSM regulation, addressed via a multi-discipline AI verification platform with KOSHA-grounded RAG). Key changes:

- **Comparison axis added.** Industry baseline ("ASME/API pass = compliance complete": 0/3) and four-layer ablation now anchor §6.6 (Tables 7, 7b).
- **Synthetic framing corrected, real-plant evidence promoted.** The 220-case headline is repositioned as *implementation verification, not predictive validation*; a new §6.6.3 summarises the anonymised VES-REAL-001 cryogenic flare-drum case (Appendix A), in which a narrower Korean-term retrieval probe surfaces Article 266 (flare-path block-valve prohibition) at rank 5.
- **Claims narrowed to what survives statistical scrutiny.** Headline retrieval reduced to Recall@1 and MRR@10 (paired-bootstrap 95% CI excludes zero, n=50, 1000 resamples); Recall@3/@5 are disclosed as not statistically distinguishable from zero. Limitations expanded to eight items.

*Editorial note 1.* One headline number was corrected during revision: the cross-discipline ablation now reports **26/60 (+0.4333)**, not 25/60, following a duplicate-surplus correction to `piping_golden_dataset_v1.json` flagged during the reproducibility audit. The correction strengthens, not weakens, the evidence.

*Editorial note 2.* The revision is extensive — word count grew from 4,928 to 12,937 (+163%); at section level, **16 new sections** (incl. §6.6, §6.7, §7.2-7.4, §7.6, Appendix A, Appendix B) and **23 rewritten sections** were marked, totalling **39 section-level changes** (per `CHANGE_SUMMARY_TABLE.docx`); these expand to **72 sub-heading-level rows** when sub-headings within Appendix A and B are counted separately and the removed/folded original sub-sections are listed (per `BEFORE_AFTER_COMPARISON.docx`). We therefore provide a word-level marked manuscript together with two navigation aids. **PAPER_JLP_REVISED_v3_MARKED.docx** shows textual changes directly in the manuscript using native Word track-changes (`<w:ins>` / `<w:del>` with author/date attribution). **BEFORE_AFTER_COMPARISON.docx** (landscape, sub-heading-level side-by-side) and **CHANGE_SUMMARY_TABLE.docx** (section-level reviewer-comment mapping) are navigation aids only. The per-comment author response is in **RESPONSE_TO_REVIEWERS_v2.docx**, and the clean revised manuscript is **PAPER_JLP_REVISED_v3.docx**.

The revision is reproducible via `scripts/reproduce_all.py` (13/13 pass); code, data, and the FTS5 index manifest are released under AGPL-3.0. The manuscript is exclusive to *JLP* and we declare no conflicts of interest.

Sincerely,

**Yuyong Kim**
University of Wisconsin–Madison
M.S. Data, Insights & Analytics; B.S. Chemical & Biological Engineering; 12+ yr petrochemical EPC.
[linkedin.com/in/yuyongkim](https://linkedin.com/in/yuyongkim)

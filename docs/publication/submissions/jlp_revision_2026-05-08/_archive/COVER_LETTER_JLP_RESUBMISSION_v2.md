**Date:** 2026-05-10

**Manuscript number:** JLP-D-26-00414 (revised)

**To:** Professor Paul Amyotte, Receiving Editor, *Journal of Loss Prevention in the Process Industries*

**Re:** Resubmission of "A KOSHA Regulatory Knowledge-Grounded Multi-Discipline AI Verification Framework for Process Plant Engineering" (title revised from "Detecting Jurisdiction Compliance Gaps in Process Plant Engineering with Regulatory RAG" per Reviewer #2's framing concerns)

---

Dear Professor Amyotte,

Thank you for the opportunity to revise JLP-D-26-00414. The three reviewers' detailed comments substantially strengthened the work. Key changes:

- **Comparison axis added.** Industry baseline ("ASME/API pass = compliance complete": 0/3) and four-layer ablation now anchor §6.6 (Tables 7, 7b).
- **Synthetic framing corrected, real-plant evidence promoted.** The 220-case headline is repositioned as *implementation verification, not predictive validation*; a new §6.6.3 summarises the anonymised VES-REAL-001 cryogenic flare-drum case (Appendix A), in which Article 266 (flare-path block-valve prohibition) emerges naturally from retrieval.
- **Claims narrowed to what survives statistical scrutiny.** Headline retrieval reduced to Recall@1 and MRR@10 (paired-bootstrap 95% CI excludes zero, n=50, 1000 resamples); Recall@3/@5 are disclosed as not statistically distinguishable from zero. Limitations expanded to eight items.

*Editorial note.* One headline number was corrected during revision: the cross-discipline ablation now reports **26/60 (+0.4333)**, not 25/60, following a duplicate-surplus correction to `piping_golden_dataset_v1.json` flagged during the reproducibility audit. The correction strengthens, not weakens, the evidence.

The revision is reproducible via `scripts/reproduce_all.py` (13/13 pass); code, data, and the FTS5 index manifest are released under AGPL-3.0. The manuscript is exclusive to *JLP* and we declare no conflicts of interest.

Sincerely,

**Yuyong Kim**
University of Wisconsin–Madison
M.S. Data, Insights & Analytics; B.S. Chemical & Biological Engineering; 12+ yr petrochemical EPC.
[linkedin.com/in/yuyongkim](https://linkedin.com/in/yuyongkim)

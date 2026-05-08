# Adversarial Review of `RESPONSE_TO_REVIEWERS_v1.md`

**Reviewer persona:** 20-year senior process-safety academic, ~50 JLP-style peer reviews completed, history of recommending rejection on synthetic-data, no-comparison, and weak-evidence grounds.

**Rubric (1–5 each):**

- **A. Acknowledgement specificity** — does the response engage with the *specific* concern, or pivot to tangent
- **B. Manuscript change traceability** — can a reviewer find the change in the manuscript by section number in <30 s
- **C. Evidence sufficiency** — does the cited artefact actually support the claim, or is it generic gesturing
- **D. Honesty about limitations** — does the response over-claim where evidence is partial

A response is **acceptable** only if all four scores ≥ 4.

---

## Reviewer 1

### R1.1 — Comparison against state of the art and process experts

| Dimension | Score | Comment |
|---|---:|---|
| A. Acknowledgement | 4 | Engages directly: industry baseline + internal ablation + literature gap. Acceptable. |
| B. Traceability | 4 | §6.6 Layer A & Layer B, Tables 7 and 7b cited explicitly. Reviewer can find. |
| C. Evidence | 4 | `outputs/layer_ablation_report.md` and `outputs/rag_retrieval_report.md` both contain the cited 0/3 vs 3/3 numbers. |
| D. Honesty | 4 | Explicitly admits "no third-party head-to-head" and lists structural reason. |

**Verdict: PASS.**

### R1.2 — RQ1 25-scenario detail

| Dimension | Score | Comment |
|---|---:|---|
| A. Acknowledgement | 5 | Explicitly addresses the 25 → 26 correction and surfaces the data-drift cause. Strong. |
| B. Traceability | 5 | §6.3 + new failure-mode partition table cited verbatim. |
| C. Evidence | 5 | `outputs/ablation_failure_mode_partition.md` contains 22/3/1 partition with per-row blocking codes. Cited correctly. |
| D. Honesty | 4 | States "skew reflects construction of the 60-scenario set" rather than claiming it's a property of the validator. Good. |

**Verdict: PASS.**

### R1.3 — Strengths/weaknesses across disciplines

| Dimension | Score | Comment |
|---|---:|---|
| A. Acknowledgement | 4 | Three-level decomposition (per-coupling-family, per-discipline calc accuracy, per-target retrieval). |
| B. Traceability | 4 | §6.1 Table 2, §6.3, §6.5 Table 6b cited. |
| C. Evidence | 4 | Table 6b shows per-group R@5 +0.20 / 0.00 / +0.10 deltas — supports the claim. |
| D. Honesty | 4 | States explicitly "smallest gain is on C-C-23 RBI (+0.00) where plain BM25 already retrieves all relevant chunks." Good. |

**Verdict: PASS.**

### R1.4 — No figures; RQ2 three-gap discussion; basis for comparison

| Dimension | Score | Comment |
|---|---:|---|
| A. Acknowledgement | 4 | Four-part response (figures, significance, gaps-missed, comparison). |
| B. Traceability | 5 | All five figure paths listed. §6.4 Case 3 + §6.5 Table 6b + §6.6 cited. |
| C. Evidence | 4 | The five figure files exist (verified by ls); §6.4 Why-this-matters paragraphs are reproduced verbatim. |
| D. Honesty | 4 | Explicitly states "Article 256 at 0.7000 (not 1.0000 — three queries in that group still miss the target on the lossy paraphrasings). This is a real weakness and is now stated as such, not hidden." Good. |

**Verdict: PASS.**

### R1.5 — Synthetic-data circularity

| Dimension | Score | Comment |
|---|---:|---|
| A. Acknowledgement | 5 | Four-pronged response: framing, anti-circularity construction, empirical negative case, head-to-head limitation. Most thorough response in the letter. |
| B. Traceability | 5 | §6.1 framing paragraph, §6.7 negative-case paragraph quoted verbatim. |
| C. Evidence | 4 | `outputs/negative_case_pip_gold_003.md` exists and shows 0 mandatory + 10 guidance for the *generic_piping_integrity* variant. **HOWEVER** — the same report file shows that a *second* query variant (`mirrored_pip047_form_chloride_terms_removed`) returned 1 mandatory hit at rank 2 (Article 256) and the file's own headline says "WARNING — at least one query variant returned a *mandatory* (law_article) hit in its top-10. The negative-case argument in manuscript §6.7 is **weakened** and should be revisited." The response letter and the manuscript both cite *only* the friendly variant and never disclose the second variant or the file's own warning. **This is a serious honesty problem.** A senior reviewer reading the cited evidence file will see the warning at the top of the file and conclude the author cherry-picked. |
| D. Honesty | **2** | The file explicitly says the negative-case argument is *weakened* and the response repeats the friendly framing. Either the manuscript needs to acknowledge the second variant + Article-256-at-rank-2 result and explain why the *generic* variant is the correct test (because PIP-GOLD-003 has no chloride/sour flag, so a query that injects "Article 256 corrosion prevention" terms is no longer a true negative-case test of the case spec — it's a test of query robustness), or this response needs to lead with that nuance. As written, both the manuscript §6.7 and this response gloss over the warning the evidence file itself raises. |

**Verdict: FAIL on D.** The negative-case section needs to either (a) report both variants and explicitly justify why the *generic_piping_integrity* variant is the correct test of the original concern (the case spec has no chloride/sour flag, so a chloride/sour-laden query is not a test of the case but a test of query robustness — the latter is a separate question and the system's behaviour on it is informative but not a refutation of the negative-case claim), or (b) drop the negative-case paragraph entirely. Option (a) is stronger because it actually disposes of the warning the evidence file flags.

---

## Reviewer 2

### R2.1 — KOSHA relevance: clause-level citations, mandatory vs guidance, EPC-uncovered

| Dimension | Score | Comment |
|---|---:|---|
| A. Acknowledgement | 5 | Three-part structure (a/b/c) maps directly to the three sub-requests. |
| B. Traceability | 5 | §4.3, §4.4, §6.4 Case 3, Table 5 all cited. |
| C. Evidence | 4 | Article 256 verbatim text matches `outputs/kosha_encoding_diagnosis.md` content preview (`사업주는 화학설비 또는 그 배관…`). |
| D. Honesty | 4 | Acknowledges that mandatory/guidance label is derived from `source_type`, not LLM-inferred — this is the correct disclosure. |

**Verdict: PASS.**

### R2.2 — Reproducibility and methodological transparency

| Dimension | Score | Comment |
|---|---:|---|
| A. Acknowledgement | 5 | Three-part response (engines+orchestration / dataset generation / RAG query+prompting). |
| B. Traceability | 4 | §3, §4.2, §5.1 Table 1, §5.2, §5.3, §6.1 cited. |
| C. Evidence | 4 | `docs/publication/CODE_MAP.md` and the four scripts named (`run_layer_ablation.py`, `dump_ablation_hits.py`, `bootstrap_ci_rag.py`, `run_negative_case_rag.py`) all exist per the v3 changelog. |
| D. Honesty | 4 | Cites 100% citation-traceability "by construction" — accurate because the grounding generator refuses to emit advisories with non-matching citation indices. |

**Verdict: PASS.**

### R2.3 — Validation and statistical rigor

| Dimension | Score | Comment |
|---|---:|---|
| A. Acknowledgement | 5 | Adopts all three sub-requests verbatim (a/b/c). |
| B. Traceability | 5 | Table 6, Table 6b, §6.1, §6.5 sample-size paragraph, §6.6 sensitivity paragraph all cited. |
| C. Evidence | 5 | `outputs/rag_bootstrap_ci_report.md` confirms all four CI numbers. n=50, 1000 resamples, seed 20260508 all match. |
| D. Honesty | 5 | This is the strongest honesty disclosure in the letter: explicitly narrows headline retrieval claim to R@1 and MRR@10, calls out R@3/R@5 CIs as including zero, states "report Recall@3/Recall@5 for completeness rather than as primary evidence." Excellent. |

**Verdict: PASS.**

### R2.4 — HAZOP scope clarification

| Dimension | Score | Comment |
|---|---:|---|
| A. Acknowledgement | 5 | Adopts the reviewer's framing across four manuscript locations (§2.6, §7.2, §7.3, §9). |
| B. Traceability | 5 | All four locations named. |
| C. Evidence | 4 | §7.3 paragraph reproduced verbatim. |
| D. Honesty | 4 | Explicit "is not a replacement" statement. Good. |

**Verdict: PASS.**

### R2.5 — Fitness-for-Service vs EPC standards

| Dimension | Score | Comment |
|---|---:|---|
| A. Acknowledgement | 5 | Treats both axes (supplements + interfaces with regulatory) and answers the design-validation-vs-operational-assessment question explicitly with "both." |
| B. Traceability | 5 | §7.4 cited. |
| C. Evidence | 4 | §7.4 paragraph reproduced verbatim; reference [17] API 579-1 is in the reference list. |
| D. Honesty | 4 | The dual-mode treatment claim is qualitatively accurate. |

**Verdict: PASS.**

### R2.6 — Figures and structure

| Dimension | Score | Comment |
|---|---:|---|
| A. Acknowledgement | 5 | All three figure types requested (architecture, RAG workflow, cross-discipline) are listed plus two more. |
| B. Traceability | 5 | All five figure file paths listed. |
| C. Evidence | 4 | Files exist (verified by ls of `docs/publication/figures/`). |
| D. Honesty | 4 | No over-claim. |

**Verdict: PASS.**

### R2.7 — Method-comparison table (Regulatory RAG vs HAZOP/RBI/Digital Twin)

| Dimension | Score | Comment |
|---|---:|---|
| A. Acknowledgement | 5 | Reproduces the reviewer's table essentially verbatim as Table 8. |
| B. Traceability | 5 | §7.2 Table 8 + Table 9 cited. |
| C. Evidence | 5 | Table 8 wording reproduced. Auditor/Advisor framing also reproduced. |
| D. Honesty | 4 | Acknowledges weakness "Depends on corpus quality and freshness" in the table itself. |

**Verdict: PASS.**

### R2.8 — Acronyms and definitions

| Dimension | Score | Comment |
|---|---:|---|
| A. Acknowledgement | 5 | Both sections added with the specific terms the reviewer named. |
| B. Traceability | 5 | Acronyms table + Key Definitions section cited. |
| C. Evidence | 5 | The 19-row Acronyms table and 6-entry Key Definitions list exist in the v3 manuscript, verified. |
| D. Honesty | 5 | No over-claim possible here. |

**Verdict: PASS.**

---

## Reviewer 3

### R3.1 — K-voting design rationale

| Dimension | Score | Comment |
|---|---:|---|
| A. Acknowledgement | 5 | Three-part rationale (paths / tolerance / scope of independence). |
| B. Traceability | 5 | §5.4 cited, with §6.6 Table 7b for the orthogonality claim. |
| C. Evidence | 4 | §5.4 reproduced verbatim. Tolerance is calibrated against the §6.1 ±1% spec, which is stated. |
| D. Honesty | 5 | Explicit disclosure that "the three paths share the same author and the same standard-citation tables. K-voting here therefore protects primarily against numerical-precision and ordering bugs, not against systematic conceptual errors in the standard interpretation." This is exactly the disclosure a senior reviewer wants. Excellent. |

**Verdict: PASS.**

### R3.2 — JLP scientific-article style

| Dimension | Score | Comment |
|---|---:|---|
| A. Acknowledgement | 4 | Lists structural changes adopted. |
| B. Traceability | 4 | Section ordering enumerated; tables and figures counted. |
| C. Evidence | 4 | Abstract opening + §1 RQ1/RQ2 reproduced. |
| D. Honesty | 4 | No over-claim. |

**Verdict: PASS.**

---

## Summary

| Reviewer | Comment | A | B | C | D | Pass? |
|---|---|---:|---:|---:|---:|:---:|
| R1 | 1 | 4 | 4 | 4 | 4 | ✅ |
| R1 | 2 | 5 | 5 | 5 | 4 | ✅ |
| R1 | 3 | 4 | 4 | 4 | 4 | ✅ |
| R1 | 4 | 4 | 5 | 4 | 4 | ✅ |
| R1 | **5** | **5** | **5** | **4** | **2** | **❌** |
| R2 | 1 | 5 | 5 | 4 | 4 | ✅ |
| R2 | 2 | 5 | 4 | 4 | 4 | ✅ |
| R2 | 3 | 5 | 5 | 5 | 5 | ✅ |
| R2 | 4 | 5 | 5 | 4 | 4 | ✅ |
| R2 | 5 | 5 | 5 | 4 | 4 | ✅ |
| R2 | 6 | 5 | 5 | 4 | 4 | ✅ |
| R2 | 7 | 5 | 5 | 5 | 4 | ✅ |
| R2 | 8 | 5 | 5 | 5 | 5 | ✅ |
| R3 | 1 | 5 | 5 | 4 | 5 | ✅ |
| R3 | 2 | 4 | 4 | 4 | 4 | ✅ |

**One failure: R1.5 Honesty (D = 2).**

## Critique on the failing item

**R1.5 — Synthetic-data circularity, Honesty score = 2.**

The response cites `outputs/negative_case_pip_gold_003.md` and quotes the favourable result (0 mandatory + 10 guidance, top = B-M-18-2026). But the same evidence file's own headline reads:

> "**WARNING** — at least one query variant returned a *mandatory* (law_article) hit in its top-10. The negative-case argument in manuscript §6.7 is **weakened** and should be revisited."

The file shows two query variants. Variant 1 (`generic_piping_integrity`, derived strictly from PIP-GOLD-003 inputs) returned 0 mandatory in top-10 — the friendly result the response cites. Variant 2 (`mirrored_pip047_form_chloride_terms_removed`, which mirrors the PIP-GOLD-047 query shape with chloride/sour terms removed) returned 1 mandatory at rank 2 — Article 256.

A senior reviewer who opens the cited evidence file will read the WARNING headline first, see two variants, and conclude that the response cherry-picked.

**The fix is not to hide the second variant — it is to surface it and explain the methodology.** The defensible position is:

> The negative case is the case spec PIP-GOLD-003. The neutral query for that case spec is the generic-piping-integrity variant, which uses material/NPS/weld/service exactly as stated in the dataset and contains no chloride or sour-service terms because the case sets neither. That query returns 0 mandatory hits. We additionally probed query robustness with a second variant that injects Article-256-style corrosion-prevention terms (the same query shape used for PIP-GOLD-047 but with chloride/sour removed); that variant retrieves Article 256 at rank 2. The two results together separate two questions: (i) does the system flag a benign case from its own spec? — answer: no; (ii) does the system retrieve Article 256 when the query asks for corrosion-prevention statutes? — answer: yes (rank 2), which is correct retrieval behaviour, not a false positive. The negative-case argument concerns (i), not (ii).

This framing is intellectually honest and *strengthens* the paper: the reviewer can verify the cited evidence file end-to-end and find that everything in the response is consistent with what the file says. As currently written, the response loses on consistency.

**Recommendation to author:** Revise §6.7 of the manuscript and the R1.5 response to surface both variants and the (i)/(ii) separation. Either the manuscript footnote or the response letter must mention the second variant before a reviewer who opens `outputs/negative_case_pip_gold_003.md` reads the WARNING headline.

---

**Status: NOT YET ACCEPTED — one item (R1.5 Honesty) requires revision in pass 2.**

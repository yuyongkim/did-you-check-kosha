# Adversarial Review of `RESPONSE_TO_REVIEWERS_v2.md` — Pass 2

**Reviewer persona:** Same 20-year senior process-safety academic.

**Scope:** Re-review only the failing item from pass 1 (R1.5 Honesty). All other items already passed in pass 1.

---

## R1.5 — Synthetic-data circularity (re-review)

**What changed in v2:** The response now contains a new "Note on the secondary query variant" paragraph that:

1. Discloses the second probe variant (`mirrored_pip047_form_chloride_terms_removed`) and acknowledges it retrieves Article 256 at rank 2.
2. Quotes the WARNING headline of the evidence file verbatim.
3. Distinguishes question (i) — *does the system flag a benign case from its own spec?* — from question (ii) — *does the system retrieve Article 256 when the query asks for corrosion-prevention statutes?* — and explains that (i) and (ii) are different questions answered by different query variants.
4. Argues that penalising the system for retrieving Article 256 in response to a query that contains the literal phrase "Article 256" would amount to penalising the system for being a working retriever.
5. Commits to adding a footnote in §6.7 of the manuscript at camera-ready to surface the (i)/(ii) distinction in the manuscript itself.

| Dimension | Score (v2) | Comment |
|---|---:|---|
| A. Acknowledgement | 5 | The response now explicitly engages the WARNING in the cited file. Strong. |
| B. Traceability | 5 | The two variants are named with their exact labels from the file; the rank-2 finding is stated. |
| C. Evidence | 4 | The (i)/(ii) decomposition matches the file structure exactly. |
| D. Honesty | **5** | This is now a *strength* of the response, not a weakness. The two-variant disclosure pre-empts the senior-reviewer "you cherry-picked" objection. The argument that retrieving Article 256 in response to a "Article 256" keyword query is correct retrieval behaviour, not a false positive on a benign case, is intellectually sound. |

**Verdict: PASS.**

---

## Aggregate

All 15 comment-response pairs are now scoring ≥ 4 across all four dimensions.

**ACCEPTED — recommend forwarding to author.**

The response letter at `docs/publication/RESPONSE_TO_REVIEWERS_v2.md` is ready for journal submission.

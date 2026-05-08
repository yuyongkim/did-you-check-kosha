# Cover Letter — Journal of Loss Prevention in the Process Industries

---

**Date:** March 31, 2026

**To:** Editor-in-Chief
*Journal of Loss Prevention in the Process Industries*
Elsevier

**Re:** Submission of manuscript entitled "Detecting Jurisdiction Compliance Gaps with Regulatory RAG: An Expert Verification System for Multi-Discipline Process Plant Engineering"

---

Dear Editor,

I am writing to submit the above-titled manuscript for consideration for publication in the *Journal of Loss Prevention in the Process Industries*.

**Scope and relevance.** This paper directly addresses loss prevention in process plant engineering by presenting an integrated AI verification system that detects two classes of risks currently missed by standard engineering practice: (1) cross-discipline coupling hazards — such as piping nozzle loads degrading rotating equipment bearings, and foundation settlement causing alignment failure — that single-domain calculation tools cannot capture; and (2) Korean-jurisdiction regulatory obligations under the KOSHA PSM framework that international code calculations (ASME, API, IEEE, IEC) structurally omit.

**Connection to recent work in this journal.** Selvam et al. (2026), published in this journal, reviewed AI applications in process safety and identified regulatory uncertainty as a primary limitation. Our work directly addresses this limitation by assembling a publicly reproducible KOSHA-centered regulatory corpus from public APIs. The raw snapshot contains 1,327 guide documents and 3,102 statutory-provision rows, and the retrieval artifact used in evaluation retains 16,174 indexed searchable entries after parsing, normalization, and indexing. We then demonstrate the feasibility of using this corpus to detect jurisdiction-specific compliance requirements invisible to code-only engineering workflows.

**Key findings:**

1. A 60-scenario cross-discipline ablation shows that enabling coupling validation increases hazard blocking from 0 to 25 scenarios (+41.7%), with boundary and failure cases blocked at 100% — quantifying the loss-prevention value of integrated multi-discipline verification.

2. Three case studies demonstrate the **jurisdiction compliance gap**: cases where ASME/API calculations fully pass while Korean PSM obligations remain unaddressed, including Article 256 corrosion-prevention requirements for carbon steel piping in sour-chloride service. Undetected, such gaps can lead to unmonitored corrosion progression and potential leakage or rupture.

3. Enhanced regulatory retrieval improves Recall@1 from 0.44 to 0.74 over plain full-text search on a 50-query curated benchmark.

**Loss-prevention significance.** The system identifies accident-pathway risks — cross-discipline coupling hazards and regulatory compliance gaps — at the engineering calculation stage, before they can escalate into piping rupture, equipment failure, or facility leaks. This represents a proactive PSM-based approach to loss prevention relevant across the plant lifecycle from design through in-service inspection, while still requiring broader field validation.

**Reproducibility.** All source code, golden datasets (220 cases across seven disciplines), and benchmark scripts are publicly released under the AGPL-3.0 license on GitHub.

**Confirmations.** This manuscript has not been published previously and is not under consideration for publication elsewhere. There are no conflicts of interest to declare.

Thank you for your consideration.

Sincerely,

**Yuyong Kim**
University of Wisconsin–Madison
M.S. Data, Insights & Analytics; B.S. Chemical & Biological Engineering
12+ years of petrochemical EPC and process plant engineering experience
[linkedin.com/in/yuyongkim](https://linkedin.com/in/yuyongkim)

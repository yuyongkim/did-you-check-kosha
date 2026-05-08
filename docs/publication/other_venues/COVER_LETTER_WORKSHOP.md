# Cover Letter — AAAI/IJCAI/NeurIPS Workshop Submission

---

**Date:** March 31, 2026

**To:** Workshop Organizers
*AI for Engineering / Reliable AI / AI Safety Workshop*

**Re:** Submission of paper entitled "Jurisdiction Compliance Gaps in Process Plant Engineering: A KOSHA-Grounded Multi-Discipline AI Verification Framework"

---

Dear Workshop Organizers,

I am submitting the above-titled paper for consideration at your workshop.

**Summary.** This paper presents an AI verification platform for seven process plant engineering disciplines that integrates international code calculations (ASME, API, IEEE, IEC, ACI, AISC) with a local RAG layer grounded in the Korean Occupational Safety and Health Agency (KOSHA) regulatory corpus. The key finding is the **jurisdiction compliance gap**: cases where international engineering codes are fully satisfied but national regulatory obligations remain unaddressed.

**Why this fits your workshop.** The paper contributes to the intersection of AI safety, regulatory AI, and domain-specific expert systems:

- **AI Safety angle:** The four-layer verification model (input validation, K-voting consensus, physics/code compliance, reverse verification) provides a concrete example of layered safety verification for AI-assisted engineering decisions. The cross-discipline coupling validator demonstrates proactive hazard detection.

- **Reliable AI angle:** The K-voting consensus mechanism applies N-version programming principles to engineering calculation verification, providing a novel reliability mechanism for domain-specific AI systems.

- **Regulatory AI angle:** The jurisdiction compliance gap concept—where a system is technically code-compliant but legally non-compliant—represents a generalizable challenge for AI systems operating across regulatory boundaries. Our KOSHA RAG integration demonstrates one approach to addressing this challenge.

**Key results:**
- 220 golden cases, 100% pass rate
- Cross-discipline ablation: 0 → 25/60 scenarios blocked (+41.7%)
- RAG Recall@1: 0.44 → 0.74 (+68% relative improvement)
- 3/3 jurisdiction compliance gaps detected vs. 0/3 with code-only baseline

**Reproducibility.** Code and datasets are publicly released under AGPL-3.0.

Thank you for your consideration.

Sincerely,

**Yuyong Kim**
University of Wisconsin–Madison
[linkedin.com/in/yuyongkim](https://linkedin.com/in/yuyongkim)

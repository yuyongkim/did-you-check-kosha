# Mind the Compliance Gap: When International Engineering Codes Pass but National Regulations Don't

**Yuyong Kim**
*University of Wisconsin–Madison*

---

## Abstract

A pressure vessel that passes every ASME calculation may violate Korean safety law. We call this a **jurisdiction compliance gap** — the structural space where international engineering codes are satisfied but national regulatory obligations are not. We present a system that detects these gaps automatically: seven domain calculation engines, a four-layer verification model with K-voting consensus, and a regulatory RAG layer indexing 16,186 KOSHA (Korea Occupational Safety and Health Agency) entries. In 3/3 test cases, the RAG layer identifies Korean obligations (including Article 256 corrosion-prevention requirements) that ASME/API calculations structurally miss. A cross-discipline validator adds 25 blocked hazard scenarios (+41.7%) in ablation. Enhanced retrieval achieves Recall@1=0.74 vs 0.44 for plain search. The compliance gap concept generalises: any jurisdiction with national safety rules atop international codes — EU PED, Chinese GB, Saudi regulations — may exhibit analogous gaps. Code released under AGPL-3.0.

**Keywords:** jurisdiction compliance gap, regulatory AI, process safety, KOSHA, multi-discipline verification

---

## 1. Introduction

International engineering codes — ASME, API, IEEE, IEC — define the gold standard for process plant calculations worldwide. Korean petrochemical plants use these same codes. But Korean law also requires compliance with the KOSHA PSM (Process Safety Management) framework, which imposes obligations that these codes do not encode: documentation triggers, mandatory review conditions, and corrosion-prevention controls.

**The problem is structural.** International codes answer: *"Is the component technically adequate?"* Korean regulations additionally ask: *"Are procedural and documentation obligations satisfied?"* Calculation tools implement only the first question. The second requires jurisdiction-specific regulatory knowledge that lives outside the code books.

We make three contributions: (1) we define and demonstrate the **jurisdiction compliance gap**; (2) we build a regulatory RAG system to detect it using 16,186 indexed KOSHA entries; (3) we show that cross-discipline coupling validation catches 25 additional hazards that single-domain calculations miss.

---

## 2. The Jurisdiction Compliance Gap

**Definition.** The set of regulatory obligations from national statute or agency guidelines that are structurally absent from international code calculations, such that a system may be code-compliant while remaining legally non-compliant.

**Example.** An SA-106 Gr.B carbon steel piping system in sour-chloride service (7.804 MPa, 196 °C, 200 ppm Cl-) with remaining life 14.0 years. ASME B31.3 wall thickness: PASS. API 570 inspection: PASS. Zero red flags. But Article 256 of the Korean Rules on Occupational Safety and Health Standards (`산업안전보건기준에 관한 규칙`) requires corrosion-prevention controls for equipment in corrosive service — an obligation ASME and API do not address.

**This is not a Korean-only problem.** The EU Pressure Equipment Directive layers requirements atop ASME. Chinese GB standards add to ISO. Saudi GACA extends FAA. The pattern recurs wherever national regulations augment international codes.

---

## 3. System Design

**Seven domain engines** implement 16 major standards across piping, vessels, rotating equipment, electrical, instrumentation, steel, and civil disciplines.

**Four-layer verification:**
1. Input validation (field presence, units, ranges).
2. K-voting consensus: three calculation paths with varied numerics must agree within 1%.
3. Physics/code compliance: red-flag rules with standard citations.
4. Reverse verification: back-calculate inputs from outputs; >5% deviation escalates.

**Cross-discipline validator** checks ten domain pairs (piping↔vessel nozzle loads, electrical↔rotating harmonics, civil↔rotating settlement, etc.).

**KOSHA RAG layer.** 16,186 rows in SQLite FTS5 from 1,327 KOSHA guides + 3,102 statutory provisions. Concept-aware BM25 with Korean synonym expansion. On-premises Qwen 2.5 7B (4-bit) for regulatory grounding generation. No external data transmission.

---

## 4. Experiments

### 4.1. Calculation accuracy
220 synthetic golden cases, seven disciplines → **220/220 pass** (deterministic engines, expected result).

### 4.2. Cross-discipline ablation

| Scenario Set | Validator OFF | Validator ON | Delta |
|---|---:|---:|---:|
| aligned_boundary | 0/6 | 6/6 | +6 |
| aligned_failure | 0/4 | 4/4 | +4 |
| mixed_random20 | 0/20 | 12/20 | +12 |
| **Overall** | **0/60** | **25/60** | **+25 (+41.7%)** |

Zero false positives on standard cases. Boundary/failure subsets: 100% blocking.

### 4.3. RAG retrieval

| Metric | Plain FTS | Enhanced | Delta |
|---|---:|---:|---:|
| Recall@1 | 0.44 | 0.74 | +0.30 |
| MRR@10 | 0.5744 | 0.7933 | +0.22 |

### 4.4. Compliance gap detection

| Case | Code Result | RAG Finding |
|---|---|---|
| Vessel RL=136.3yr | ASME/API PASS | M-69-2012: RL documentation required |
| Vessel RL=40.2yr | API 510 PASS | C-C-23-2026: mandatory RBI trigger |
| Piping sour service | B31.3/570 PASS | **Article 256: corrosion prevention** |

Code-only: **0/3 detected**. With RAG: **3/3 detected**.

---

## 5. Discussion

**Why this matters for AI safety.** Engineering AI systems that check code compliance but not jurisdiction-specific regulations create a false sense of completeness. Users may trust a "PASS" result without realising that regulatory obligations remain unaddressed. The jurisdiction compliance gap is a concrete instance of the broader problem of AI systems operating across regulatory boundaries.

**The K-voting insight.** Three calculation paths with varied numerics catch the class of bugs where a single implementation appears correct but diverges at regulatory thresholds. In engineering, a 0.5% numerical difference can determine whether a component passes or fails inspection — making consensus verification practically important.

**Generalisability.** The architecture pattern — domain engine + jurisdiction RAG — is reusable. Replacing the KOSHA corpus with EU PED directives, Chinese GB standards, or Saudi regulations would address analogous gaps in those jurisdictions.

---

## 6. Limitations

- Synthetic-only evaluation; no field validation with real plant data.
- Curated 50-query benchmark; BM25 may miss semantically similar Korean text.
- Ten coupling pairs; not exhaustive.
- Single jurisdiction (Korea); cross-jurisdiction evaluation is future work.

---

## 7. Conclusion

We defined the **jurisdiction compliance gap** and showed it is detectable: a regulatory RAG layer over KOSHA data identifies 3/3 Korean-jurisdiction obligations missed by international code calculations. Cross-discipline coupling detection adds 25 blocked hazards. The concept generalises beyond Korea to any jurisdiction-code interaction. Code: [github.com/yuyongkim/did-you-check-kosha](https://github.com/yuyongkim/did-you-check-kosha).

---

## References

[1] Selvam et al. (2026). AI in process safety. *J. Loss Prevention.* [2] Woo et al. (2025). LLM for Process Systems Eng. *Korean J. Chem. Eng.* 42. [3] Lewis et al. (2020). RAG for Knowledge-Intensive NLP. *NeurIPS* 33. [4] Walker et al. (2026). RAGuard. *IMBSA 2025, LNCS 15755.* [5] Avizienis (1985). N-version programming. *IEEE TSE* SE-11(12). [6] Kim et al. (2022). KOSHA accident text mining. *J. Arch. Inst. Korea* 38(4). [7] Lee & Ahn (2025). LLM for construction safety. *Korean J. Constr. Eng. Mgmt.* 26(2). [8] Robertson & Zaragoza (2009). BM25. *Found. Trends IR* 3(4).

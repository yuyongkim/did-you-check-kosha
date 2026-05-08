# Detecting Jurisdiction Compliance Gaps with Regulatory RAG: An Expert Verification System for Multi-Discipline Process Plant Engineering

**Yuyong Kim**

*University of Wisconsin–Madison, Madison, WI 53706, USA*
*M.S. Data, Insights & Analytics; B.S. Chemical & Biological Engineering*

---

## Highlights

- We define and operationalize the **jurisdiction compliance gap** — the structural space where a system passes international engineering codes yet violates national safety regulations.
- A regulatory RAG layer over 16,186 KOSHA entries detects 3/3 Korean-jurisdiction obligations missed by ASME/API calculations, improving Recall@1 from 0.44 to 0.74.
- A four-layer verification pipeline — input validation, K-voting consensus, physics compliance, and reverse verification — achieves 220/220 golden-case accuracy across seven engineering disciplines.
- Cross-discipline coupling detection increases hazard blocking by 25 scenarios (+41.7%) in a 60-scenario ablation study.
- All code, datasets, and benchmark scripts are released under AGPL-3.0 for full reproducibility.

---

## Abstract

International engineering codes (ASME, API, IEEE, IEC, ACI, AISC) govern technical calculations in process plant projects worldwide, yet national safety regulations frequently impose additional obligations that these codes do not encode. We term this structural mismatch a **jurisdiction compliance gap** and demonstrate its existence in Korean process plant engineering, where the Korea Occupational Safety and Health Agency (KOSHA) PSM framework requires documentation, review triggers, and corrosion-prevention controls beyond what code calculations address. To detect such gaps automatically, we present an expert verification system with three components: (i) seven domain calculation engines covering piping, pressure vessels, rotating equipment, electrical systems, instrumentation, structural steel, and civil structures; (ii) a four-layer hybrid verification model employing input validation, K-voting consensus among three parallel calculation paths, physics/code compliance checks, and reverse verification; and (iii) a regulatory retrieval-augmented generation (RAG) layer that indexes 1,327 KOSHA guide documents and 3,102 statutory provisions into 16,186 searchable rows. Evaluation on 220 synthetic golden cases confirms 100% calculation accuracy. A 60-scenario ablation demonstrates that cross-discipline coupling validation increases hazard blocking from 0 to 25 scenarios. A 50-query retrieval benchmark shows Recall@1 improvement from 0.44 to 0.74 and MRR@10 from 0.5744 to 0.7933 with concept-aware synonym expansion. Three case studies empirically demonstrate jurisdiction compliance gaps: in each case, ASME/API calculations produce a clean pass while the KOSHA RAG layer surfaces mandatory Korean-jurisdiction requirements, most notably Article 256 of the Rules on Occupational Safety and Health Standards (`산업안전보건기준에 관한 규칙`). The concept generalises to any jurisdiction with national regulations layered atop international codes.

**Keywords:** expert system; jurisdiction compliance gap; regulatory RAG; process safety management; KOSHA; multi-discipline verification; K-voting consensus; large language model

---

## 1. Introduction

### 1.1. Motivation: when code compliance is not enough

A pressure vessel that satisfies every ASME Section VIII requirement may still violate Korean law. An API 570-compliant piping inspection program may omit mandatory review triggers defined by the Korea Occupational Safety and Health Agency (KOSHA). This is not a hypothetical risk: it is a structural property of how international engineering codes and national safety regulations interact.

International codes such as ASME, API, IEEE, and IEC define the technical basis for engineering calculations—minimum wall thickness, allowable stress, arc-flash energy, safety integrity level. These calculations are necessary for safe design and operation. However, they are not sufficient for legal compliance in jurisdictions that layer additional safety regulations on top of international codes. In Korea, the Occupational Safety and Health Act and its implementing regulations—including KOSHA technical guidelines and the Rules on Occupational Safety and Health Standards—impose procedural, documentation, and compliance obligations that are conditioned on calculation outputs but encoded outside the international standards.

We call this structural mismatch a **jurisdiction compliance gap**: the set of regulatory obligations imposed by national statute or agency guideline that are structurally absent from international engineering code calculations, such that a system may be technically code-compliant while remaining legally non-compliant under the applicable local jurisdiction.

This paper addresses two questions:

- **RQ1.** Can automated cross-discipline verification detect coupling hazards that single-domain calculations miss?
- **RQ2.** Can a regulatory RAG layer identify jurisdiction-specific compliance requirements that international code calculations structurally omit?

### 1.2. Scope and contributions

We present an expert verification system for seven process plant engineering disciplines. Its four contributions are:

1. **Jurisdiction compliance gap concept.** We define, operationalise, and empirically demonstrate this concept with three case studies spanning pressure vessels and piping in Korean jurisdiction.

2. **Regulatory RAG for KOSHA integration.** We construct the first regulatory corpus from KOSHA public APIs (16,186 indexed rows from 1,327 guides and 3,102 statutory provisions) and demonstrate its utility in detecting jurisdiction-specific obligations invisible to code calculations.

3. **Four-layer hybrid verification model.** Input validation, K-voting consensus (three parallel calculation paths with ≤1% deviation tolerance), physics/code compliance, and reverse verification—applied to seven engineering disciplines.

4. **Cross-discipline coupling detection.** Automatic hazard identification across ten predefined domain pairs, with quantified incremental value via ablation.

### 1.3. Paper organisation

Section 2 positions this work against related literature. Section 3 defines the jurisdiction compliance gap formally. Section 4 describes system architecture. Section 5 details the KOSHA RAG layer. Section 6 presents the verification model. Section 7 reports experiments. Section 8 discusses findings. Section 9 addresses limitations. Section 10 concludes.

---

## 2. Related Work

### 2.1. Expert systems for engineering verification

Expert systems have a long history in engineering domains, from early rule-based diagnostic systems to modern AI-assisted design tools. In process safety, Selvam et al. (2026) review AI applications across hazard detection and risk assessment, reporting 30–60% accuracy gains while noting regulatory uncertainty as a primary limitation. Woo et al. (2025) survey LLM applications in process systems engineering but do not address multi-discipline verification or regulatory corpus integration. Elhosary et al. (2024) propose an LLM-assisted HAZOP system using RAG, limited to single-process scope. None of these works address the systematic detection of jurisdiction compliance gaps.

### 2.2. Retrieval-augmented generation for regulatory domains

The RAG paradigm (Lewis et al., 2020; Gao et al., 2024) augments language models with retrieved evidence. Walker et al. (2026) apply safety-document RAG to offshore wind maintenance, the closest structural analogue to our work, but without cross-jurisdiction regulatory analysis. Klesel and Wittmann (2025) identify regulatory RAG as an open direction. The present work instantiates this direction with a concrete corpus construction and evaluation methodology for Korean industrial safety regulations.

### 2.3. Multi-discipline asset integrity

AI-based asset integrity frameworks (Jones et al., 2025) typically address single-asset or single-discipline scope. Predictive maintenance surveys (Hector and Panjanathan, 2024; Ait-Alla et al., 2022) cover sensor-driven monitoring without standards-based calculation verification or regulatory RAG.

### 2.4. N-version programming and consensus verification

Avizienis (1985) established the theoretical basis for N-version programming. Our K-voting consensus layer adapts this principle to engineering calculation verification—three independently varied calculation paths must agree within 1% relative deviation. To our knowledge, this application is novel in plant engineering.

### 2.5. Korean PSM and KOSHA in AI

Kim et al. (2022) apply text mining to KOSHA accident reports for classification. Lee and Ahn (2025) fine-tune an LLM on KOSHA construction safety guidelines for Q&A. Neither integrates KOSHA data into an engineering calculation verification layer. No prior work has reported automated detection of jurisdiction compliance gaps between international codes and Korean PSM regulations.

---

## 3. The Jurisdiction Compliance Gap

### 3.1. Definition

**Jurisdiction compliance gap.** The set of regulatory obligations imposed by national statute or agency guideline that are structurally absent from international engineering code calculations, such that a system may be technically code-compliant while remaining legally non-compliant under the applicable local jurisdiction.

### 3.2. Structural origin

International engineering codes define *what to calculate* and *what thresholds to apply*. National safety regulations define *what to do about the results*—documentation requirements, mandatory review triggers, additional control measures. These two regulatory layers address different questions:

| Layer | Question Answered | Example |
|---|---|---|
| International code (ASME, API) | Is the component technically adequate? | Remaining life = 136.3 years → PASS |
| National regulation (KOSHA PSM) | Are procedural/documentation obligations met? | RL > threshold → mandatory documentation per M-69-2012 |

The gap arises because calculation tools implement only the first layer. The second layer requires access to jurisdiction-specific regulatory knowledge that is external to the calculation engine.

### 3.3. Generalisability

While we demonstrate this gap in Korean jurisdiction, the concept applies wherever national regulations augment international codes: EU Pressure Equipment Directive layered on ASME; Saudi GACA requirements layered on FAA; Chinese GB standards layered on ISO. Any jurisdiction with a regulatory layer beyond international code calculations may exhibit analogous gaps.

---

## 4. System Architecture

### 4.1. Overview

The system comprises an orchestrator, seven domain calculation services, a cross-discipline validator, a KOSHA RAG layer, and an API layer. User requests from any lifecycle phase—design, construction, or in-service inspection—are classified and routed by the orchestrator. Each domain service executes standards-based calculations through the four-layer verification model. Cross-discipline coupling is checked across ten domain pairs. The KOSHA RAG layer provides regulatory grounding. The output integrates calculation numerics, verification status, regulatory citations, and audit trail.

### 4.2. Domain engines

| Domain | Standards | Key Outputs |
|---|---|---|
| Piping | ASME B31.3, API 570 | Wall thickness, hoop stress, remaining life, inspection interval |
| Pressure Vessels | ASME VIII Div.1, API 510, API 579-1 | Shell thickness, FFS screening, remaining life |
| Rotating Equipment | API 610, 617, 670 | Vibration limits, bearing health, steam state screening |
| Electrical | IEEE C57.104, 1584-2018 | Transformer HI, arc-flash energy, PPE category |
| Instrumentation | IEC 61511, ISA-TR84.00.02 | PFDavg, SIL verification, calibration health |
| Structural Steel | AISC 360 | D/C ratio, section loss, fatigue assessment |
| Civil / Concrete | ACI 318, 562 | Flexure D/C, carbonation depth, repair priority |

### 4.3. Technology constraints

All inference runs on-premises using Ollama with Qwen 2.5 7B Instruct (4-bit quantisation, 32,768-token context). No external data transmission occurs. The RAG index uses SQLite FTS5. This design satisfies industrial data-sovereignty requirements.

---

## 5. KOSHA Regulatory RAG Layer

### 5.1. Corpus construction

Two KOSHA public APIs were used:

1. **Smart-search API**: 18,576 rows of guide-section and statutory-provision metadata across categories 1–11, covering 1,327 guide documents (9,069 sections) and 3,102 statutory provisions.
2. **Guide API**: 1,039 technical guideline PDFs parsed page-by-page into 13,084 retrieval-optimised chunks.

After deduplication and normalisation, the SQLite FTS5 index contains **16,186 searchable rows** (13,084 guide chunks + 3,102 law-article entries; 200 MB total).

### 5.2. Retrieval pipeline

Domain calculation outputs are converted to Korean natural-language queries. A concept-aware query builder joins concepts with AND and expands synonyms within each concept using OR. When strict AND matching yields no results, a loose OR fallback is used. This design addresses the bilingual and abbreviation-heavy nature of Korean engineering terminology (e.g., "잔여수명" / "remaining life" / "RL").

### 5.3. Generation pipeline

Retrieved passages provide context for Qwen 2.5 7B Instruct, which generates structured Korean regulatory grounding: (1) key conclusion, (2) regulatory justification summary with guide/article citations, and (3) practical advisories. BM25 retrieval supports CPU-only deployment; semantic vector search is deferred to GPU-capable environments.

---

## 6. Four-Layer Hybrid Verification Model

### 6.1. Layer 1 — Input validation

Mandatory field presence, unit contract compliance, and domain-specific range constraints. Missing critical fields or unit violations trigger a blocking error that prevents downstream calculation. This layer gates all subsequent processing.

### 6.2. Layer 2 — K-voting consensus

Three calculation paths execute in parallel, each using deliberately varied numerical strategies:
- **Path A**: standard rounding order and linear interpolation.
- **Path B**: reversed rounding order and cubic interpolation.
- **Path C**: extended intermediate precision (double the significant figures).

The maximum relative deviation among outputs must not exceed 1%. This threshold balances sensitivity to numerical bugs against tolerance for legitimate precision differences. If exceeded, a tiebreaker path is invoked; persistent failure triggers a no-consensus flag requesting human review.

This mechanism adapts N-version programming (Avizienis, 1985) to engineering calculation verification, targeting numerical-consistency rather than full implementation independence.

### 6.3. Layer 3 — Physics and code compliance

Domain-specific red flags are enforced by rule-based checks. Examples:
- Piping: measured thickness < minimum required thickness → critical block.
- Vessel: remaining life < 0 → critical block.
- Rotating: vibration exceeds API 670 alert level → warning.
- Electrical: arc-flash energy > 40 cal/cm² → PPE Category 4 escalation.

All major calculation steps carry explicit standard citations (e.g., "ASME B31.3 §304.1.2").

### 6.4. Layer 4 — Reverse verification

Key inputs are back-calculated from outputs and compared against originals:
- Deviation < 2%: consistent (pass).
- Deviation 2–5%: warning with audit note.
- Deviation > 5%: escalation with confidence downgrade.

This layer detects internal inconsistencies that may indicate formula errors, unit conversion mistakes, or data corruption.

### 6.5. Cross-discipline coupling validator

Ten predefined domain pairs with coupling checks:

| Pair | Coupling Mechanism |
|---|---|
| Piping ↔ Vessel | Nozzle interface margin mismatch |
| Piping ↔ Rotating | Nozzle load → bearing degradation |
| Electrical ↔ Rotating | Harmonic distortion → bearing temperature |
| Civil ↔ Rotating | Foundation settlement → alignment failure |
| Electrical ↔ Instrumentation | Power quality → signal integrity |
| Steel ↔ Civil | Structural capacity → foundation demand |
| Vessel ↔ Piping | Nozzle load reciprocal check |
| Steel ↔ Rotating | Support structure → vibration transmission |
| Instrumentation ↔ Vessel | Safety function → equipment condition |
| Civil ↔ Piping | Settlement → pipe stress |

Threshold tuning over 50 optimisation rounds achieved: standard-case blocking rate 0.0 (no false positives on nominal cases), boundary/failure blocking rate 1.0, weighted accuracy 1.0, and hard-block recall 1.0.

---

## 7. Experiments and Evaluation

### 7.1. Golden dataset validation

**220 synthetic golden cases** across seven disciplines:

| Discipline | Standard | Boundary | Failure | Composite | Total |
|---|---:|---:|---:|---:|---:|
| Piping | 20 | 15 | 10 | 5 | 50 |
| Vessel | 18 | 7 | 5 | — | 30 |
| Rotating | 18 | 7 | 5 | — | 30 |
| Electrical | 18 | 7 | 5 | — | 30 |
| Instrumentation | 18 | 7 | 5 | — | 30 |
| Steel | 15 | 6 | 4 | — | 25 |
| Civil | 15 | 6 | 4 | — | 25 |
| **Total** | **122 (55%)** | **55 (25%)** | **38 (17%)** | **5 (2%)** | **220** |

Cases were derived from reference examples in applicable standards with systematic parameter perturbation. Runtime validation: **220/220 pass**, with accuracy, red-flag detection rate, and standard citation coverage all at 1.0000. These perfect scores are expected for deterministic rule-based engines evaluated against same-standard-derived cases; they confirm implementation correctness, not generalisation.

### 7.2. Seven-discipline pipeline

Across 43 pipeline scenarios: completion rate 0.6512, blocking rate 0.3488. Nominal and standard-aligned cases: 1.0000 completion. Boundary and failure cases: 1.0000 blocking. This confirms correct hazard identification without false positives on clean inputs.

### 7.3. Cross-discipline validator ablation (RQ1)

| Scenario Set | Validator OFF | Validator ON | Absolute Delta | Ratio Delta |
|---|---:|---:|---:|---:|
| aligned_standard | 0 / 10 | 0 / 10 | +0 | +0.00 |
| aligned_boundary | 0 / 6 | 6 / 6 | +6 | +1.00 |
| aligned_failure | 0 / 4 | 4 / 4 | +4 | +1.00 |
| mixed_first20 | 0 / 20 | 3 / 20 | +3 | +0.15 |
| mixed_random20 | 0 / 20 | 12 / 20 | +12 | +0.60 |
| **Overall** | **0 / 60** | **25 / 60** | **+25** | **+0.4167** |

**Finding (RQ1):** Cross-discipline validation adds 25 blocked scenarios (+41.7%) that single-domain calculations cannot detect. Boundary and failure subsets achieve perfect blocking (1.0). Zero false positives on standard-aligned cases.

### 7.4. KOSHA RAG retrieval benchmark (RQ2)

50-query curated benchmark across five regulatory target groups:

| Metric | Plain FTS | Enhanced FTS | Delta |
|---|---:|---:|---:|
| Recall@1 | 0.44 | 0.74 | +0.30 |
| Recall@3 | 0.74 | 0.86 | +0.12 |
| Recall@5 | 0.74 | 0.86 | +0.12 |
| MRR@10 | 0.5744 | 0.7933 | +0.2189 |

Concept-aware synonym expansion yields +68% relative improvement in Recall@1 and +38% relative improvement in MRR@10.

### 7.5. Jurisdiction compliance gap case studies (RQ2)

Three cases where all international code calculations pass cleanly:

**Case 1 — VES-GOLD-001 (Vessel Remaining Life).** SA-516-70 vessel, 1.858 MPa, 217.3 °C, current thickness 44.82 mm. Calculation: required thickness 14.99 mm (ASME VIII UG-27), remaining life 136.3 years, inspection interval 10 years (API 510). No red flags. **KOSHA RAG retrieves**: M-69-2012 (Technical Guideline for Remaining Life Assessment) — documentation requirements triggered when RL exceeds threshold. *Gap: ASME/API do not encode this documentation obligation.*

**Case 2 — VES-GOLD-009 (RBI Planning).** SA-516-70 vessel, 1.891 MPa, 241.9 °C, remaining life 40.2 years. API 510 recommends 10-year inspection. **KOSHA RAG retrieves**: C-C-23-2026 (RBI Technical Regulation) — mandatory RBI review trigger conditions under Korean PSM. *Gap: API 510 inspection scheduling does not address KOSHA mandatory review triggers.*

**Case 3 — PIP-GOLD-047 (Piping Corrosion Compliance).** SA-106 Gr.B carbon steel, sour-chloride service, 7.804 MPa, 196 °C, 200 ppm Cl-. Remaining life 14.0 years. ASME B31.3 and API 570 fully satisfied. **KOSHA RAG retrieves**: Article 256 of the Rules on Occupational Safety and Health Standards (`산업안전보건기준에 관한 규칙`) — corrosion-prevention control obligations. *Gap: ASME B31.3 and API 570 define how to calculate corrosion allowance and remaining life, but do not impose the obligation to establish corrosion-prevention controls that Article 256 requires.*

| Case | Code-Only | RAG Detected | Key Gap |
|---|---:|---:|---|
| VES-GOLD-001 | 0 | 1 | RL documentation per M-69-2012 |
| VES-GOLD-009 | 0 | 1 | RBI trigger per C-C-23-2026 |
| PIP-GOLD-047 | 0 | 1 | Corrosion prevention per Article 256 |
| **Total** | **0 / 3** | **3 / 3** | |

**Finding (RQ2):** The KOSHA RAG layer detects 3/3 jurisdiction-specific compliance requirements that code-only calculations structurally miss. The code-only baseline detects 0/3.

---

## 8. Discussion

### 8.1. Practical significance of jurisdiction compliance gaps

The jurisdiction compliance gap has direct consequences across the plant lifecycle:

- **Design phase**: Calculation packages satisfying ASME/API deliverables may miss KOSHA documentation obligations, creating audit risk.
- **Construction phase**: Commissioning based solely on international codes may skip Korean regulatory steps.
- **Operation phase**: Inspection programs following API 510/570 may not satisfy KOSHA-mandated review triggers.

The cost of detecting these gaps at the calculation stage is negligible (a RAG query). The cost of detecting them at regulatory audit—or after an incident—can be severe.

### 8.2. K-voting consensus as a verification strategy

The K-voting layer serves a different purpose than traditional software testing. It detects the class of bugs where a single implementation appears correct but produces numerically inconsistent results due to rounding, interpolation, or precision choices. In engineering calculations where small differences can cross regulatory thresholds, this class of error is practically significant.

### 8.3. Cross-discipline coupling as safety contribution

The 25 additional blocked scenarios represent coupling hazards that no single-domain tool would flag. In practice, these correspond to failure modes such as: piping nozzle overload degrading rotating equipment bearings; foundation settlement causing rotating equipment misalignment; electrical harmonics affecting instrumentation. These are documented accident pathways in plant engineering.

### 8.4. Limitations of the evaluation

The golden dataset is entirely synthetic. The retrieval benchmark is curated. Baselines are internal ablations, not external industrial workflow comparisons. These limitations are inherent to a first-generation system paper and are addressed in Section 9.

---

## 9. Limitations and Future Work

1. **Synthetic evaluation only.** No field validation with real plant data has been performed. Golden cases are derived from the same standards the engines implement, so perfect accuracy is expected and does not indicate generalisation capability.
2. **Screening-level outputs.** Domain outputs support engineering review but cannot substitute for detailed design calculations.
3. **Curated retrieval benchmark.** The 50-query benchmark measures variant robustness, not breadth. BM25 may miss semantically similar Korean documents despite synonym expansion.
4. **Ten coupling pairs.** Systematic expansion to additional domain pairs is needed.
5. **Internal baselines only.** Comparison against industrial engineering review workflows is planned for the field pilot phase.

**Future directions:**
- Field pilot with real plant data from both design and in-service inspection contexts.
- Integration with RBI (Risk-Based Inspection) and HAZOP (Hazard and Operability) workflows.
- Semantic vector search using a Korean embedding model for GPU-capable deployments.
- Evaluation of the jurisdiction compliance gap in other national contexts (EU PED, Chinese GB, Saudi regulations).

---

## 10. Conclusion

This paper has introduced the concept of the **jurisdiction compliance gap** and presented an expert verification system that detects it automatically. The system integrates seven domain calculation engines, a four-layer hybrid verification model with K-voting consensus, a cross-discipline coupling validator, and a KOSHA regulatory RAG layer.

Key findings:
- Cross-discipline validation increases hazard blocking from 0 to 25/60 scenarios (+41.7%), with zero false positives.
- Enhanced regulatory retrieval improves Recall@1 from 0.44 to 0.74 and MRR@10 from 0.5744 to 0.7933.
- Three case studies empirically demonstrate that ASME/API-compliant calculations can miss Korean-jurisdiction obligations, including Article 256 corrosion-prevention requirements.

The jurisdiction compliance gap is a structural property of how international codes and national regulations interact. It is not specific to Korea or to the engineering domains studied here. Any jurisdiction where national safety regulations augment international code calculations may exhibit analogous gaps. Automated detection of these gaps at the calculation stage—rather than at audit or after incident—represents a meaningful contribution to engineering expert systems and process safety management.

Code, datasets, and benchmark scripts are released under the AGPL-3.0 license.

---

## Code and Data Availability

Source code, golden datasets, benchmark scripts, and the KOSHA regulatory corpus index: [https://github.com/yuyongkim/did-you-check-kosha](https://github.com/yuyongkim/did-you-check-kosha) (AGPL-3.0). Code-to-paper mapping: `docs/publication/CODE_MAP.md`.

---

## CRediT Authorship Contribution Statement

**Yuyong Kim:** Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Data curation, Writing – original draft, Writing – review & editing, Visualization.

---

## Declaration of Competing Interest

The author declares no known competing financial interests or personal relationships that could have appeared to influence this work.

---

## Acknowledgements

The author acknowledges the Korea Occupational Safety and Health Agency (KOSHA) for public API access to technical guidelines and statutory provisions.

---

## References

Ait-Alla, A., Quandt, M., Lütjen, M., Freitag, M., 2022. On Predictive Maintenance in Industry 4.0: Overview, Models, and Challenges. Applied Sciences 12 (16), 8081.

Avizienis, A., 1985. The N-version approach to fault-tolerant software. IEEE Trans. Softw. Eng. SE-11 (12), 1491–1501.

Elhosary, M. et al., 2024. LLM-assisted HAZOP study using retrieval-augmented generation. IChemE Symposium Series No. 171: Hazards 34.

Gao, Y., Xiong, Y., Huang, X. et al., 2024. Retrieval-Augmented Generation for Large Language Models: A Survey. arXiv:2312.10997.

Hector, I., Panjanathan, R., 2024. Predictive maintenance in Industry 4.0: a survey of planning models and ML techniques. PeerJ Comput. Sci. 10, e2016.

Jones, J.F. et al., 2025. AI for asset integrity management of offshore oil and gas pipelines. Life Cycle Reliability and Safety Engineering.

Kim, H., Yi, J.-S., Jang, Y., 2022. Analyzing Patterns of Multi-cause Accidents From KOSHA's Case Reports Using Text Mining. J. Architectural Institute of Korea 38 (4), 237–244.

Klesel, M., Wittmann, H.F., 2025. Retrieval-Augmented Generation (RAG). Bus. Inf. Syst. Eng. 67 (4), 551–561.

Lee, J., Ahn, S., 2025. AI Prototype for Construction Safety Guidelines via Fine-Tuning LLM. Korean J. Constr. Eng. Mgmt. 26 (2), 20–31.

Lewis, P. et al., 2020. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. NeurIPS 2020, 33, 9459–9474.

Robertson, S., Zaragoza, H., 2009. The Probabilistic Relevance Framework: BM25 and Beyond. Found. Trends Inf. Ret. 3 (4), 333–389.

Selvam, D.C. et al., 2026. AI in process safety: opportunities, challenges, and future directions. J. Loss Prevention in the Process Industries.

Walavalkar, V. et al., 2021. ML and DL in Chemical Health and Safety: A Systematic Review. ACS Chem. Health Saf.

Walker, C. et al., 2026. RAGuard: Safe RAG for LLMs. IMBSA 2025, LNCS 15755.

Woo, T. et al., 2025. Leveraging Generative AI and LLM for Process Systems Engineering. Korean J. Chem. Eng. 42, 2787–2808.

ASME, 2022. ASME B31.3-2022: Process Piping. ASME, New York.

API, 2020. API 579-1/ASME FFS-1: Fitness-For-Service, 3rd ed. API, Washington, DC.

KOSHA, 2026. KOSHA Guide Technical Regulations Portal. https://www.kosha.or.kr

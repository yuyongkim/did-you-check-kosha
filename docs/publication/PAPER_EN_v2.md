# A KOSHA Regulatory Knowledge-Grounded Multi-Discipline AI Verification Framework for Process Plant Engineering

**Yuyong Kim**  
*University of Wisconsin–Madison*  
M.S. Data, Insights & Analytics Candidate; B.S. Chemical & Biological Engineering; 12+ years of professional experience in petrochemical EPC and process plant engineering  
[linkedin.com/in/yuyongkim](https://linkedin.com/in/yuyongkim)

---

## Abstract

Engineering calculation workflows in Korean process plant projects span seven disciplines—piping, pressure vessels, rotating equipment, electrical, instrumentation, structural steel, and civil—across the full plant lifecycle from design and construction through to operation and inspection. Existing practice relies on discipline-siloed tools that structurally miss cross-domain coupling hazards and cannot enforce Korean-jurisdiction regulatory requirements that go beyond international code compliance. This paper presents an integrated AI verification platform composed of three core layers: (1) seven domain calculation engines implementing ASME, API, IEEE, IEC, ACI, and AISC standards; (2) a four-layer hybrid verification model comprising input validation, K-voting consensus, physics/code compliance enforcement, and reverse verification; and (3) a local Retrieval-Augmented Generation (RAG) layer that indexes 1,039 KOSHA technical guidelines and 3,102 statutory provisions in a SQLite FTS index and generates regulatory grounding via an on-premises Qwen language model. All 220 synthetic golden cases pass end-to-end validation. A 60-scenario cross-discipline ablation increases blocking from 0 to 25 scenarios when the cross-validator is enabled, and a 50-query regulatory retrieval benchmark improves Recall@1 from 0.44 to 0.74 and MRR@10 from 0.5744 to 0.7933 over plain FTS retrieval. Three representative cases demonstrate that the KOSHA RAG layer identifies Korean-jurisdiction compliance requirements—including the corrosion-prevention obligation under Article 256 of the Rules on Occupational Safety and Health Standards (`산업안전보건기준에 관한 규칙`)—in scenarios where ASME and API calculations fully clear. The paper introduces and empirically demonstrates the concept of a **jurisdiction compliance gap**: the structural space between international engineering code compliance and Korean PSM regulatory fulfilment. Code and datasets are released under the AGPL license.

**Keywords:** KOSHA RAG · process safety management · process plant engineering · multi-discipline verification · jurisdiction compliance gap · large language model

---

## 1. Introduction

Engineering calculation and compliance verification in Korean petrochemical and process plant projects spans more than seven engineering disciplines—piping, pressure vessels (static equipment), rotating machinery, electrical systems, instrumentation, structural steel, and civil structures—across a broad lifecycle that includes process design, detailed engineering, construction and commissioning, and ongoing operation and inspection. Whether verifying that a new piping system meets minimum wall-thickness requirements under ASME B31.3 or assessing the remaining service life of an operating pressure vessel under API 579-1, the underlying calculation workflows share the same structural problem: discipline-specific tools and review procedures create a systematic gap in which cross-domain coupling hazards are not captured. Excessive piping nozzle loads can drive rotating equipment vibration; civil foundation settlement can propagate into rotating equipment alignment failure; neither is detectable by single-domain calculations alone.

When these cross-domain hazards and regulatory gaps are left unaddressed, they can escalate into major industrial accidents—piping rupture, rotating equipment over-vibration, facility leaks—with associated loss of life and environmental damage. The integrated verification framework proposed in this study identifies these accident-pathway risks at the calculation stage, contributing to process safety management (PSM)-based accident prevention across the plant lifecycle.

Korean plants subject to the Chemical Substances Control Act and the Occupational Safety and Health Act must comply with the PSM framework published by the Korea Occupational Safety and Health Agency (KOSHA), which imposes jurisdiction-specific requirements that go beyond what ASME, API, IEEE, and IEC code calculations satisfy. Whether a system is being designed for a new plant or inspected in an operating facility, the relevant KOSHA guidelines and statutory provisions impose procedural, documentation, and compliance obligations that are invisible to international-code-only calculation workflows. To date, no study has systematically integrated KOSHA regulations into an engineering AI verification system.

This study addresses the following two research questions:

**RQ1.** What additional cross-domain coupling hazards does the proposed multi-discipline verification architecture detect compared with independent single-domain calculations, across a predefined set of domain pairs?

**RQ2.** Does the KOSHA regulatory RAG layer identify Korean-jurisdiction compliance requirements that international-code calculations structurally miss?

The contributions of this paper are as follows. First, we propose a verification architecture that integrates seven engineering disciplines into a single orchestration pipeline and automatically detects coupling hazards across ten predefined domain pairs—with extension to additional pairs deferred to future work. Second, we present a methodology for integrating a KOSHA public-API regulatory corpus into engineering AI verification for the first time, enabling automatic identification of Korean-jurisdiction compliance requirements not captured by international code calculations. Third, we construct a quantitative evaluation framework comprising 220 synthetic golden cases, a 60-scenario cross-discipline ablation, and a 50-query curated regulatory retrieval benchmark. Code and datasets are released under the AGPL license.

---

## 2. Related Work

### 2.1 AI Applications in Process Safety

Large language models are increasingly studied for chemical process design, process optimisation, and maintenance knowledge extraction. Selvam et al. (2026) [1] review AI applications across hazard detection, dynamic risk assessment, and barrier management in the chemical process industries, reporting 30-60% gains in anomaly and near-miss detection accuracy, while identifying data bias, field validation, and regulatory uncertainty as primary limitations. Woo et al. (2025) [2] survey LLM applications in process systems engineering across chemical process design, hybrid process modelling, and autonomous control systems, but do not address seven-discipline integrated engineering verification or KOSHA regulatory RAG. Elhosary et al. (2024) [3] propose an LLM-assisted HAZOP system using RAG and vector search to retrieve historical incidents and guide analysis sessions, but the system is limited to single-process analysis and does not integrate multi-discipline calculation verification. Walavalkar et al. (2021) [4] systematically review more than one hundred ML and deep learning applications in chemical health and safety, covering exposure and risk assessment, but do not treat RAG-based regulatory grounding or multi-discipline engineering verification architectures.

### 2.2 RAG in Technical and Regulatory Domains

The foundational RAG architecture of Lewis et al. (2020) [5] targets general knowledge-intensive NLP tasks; the present work specialises this architecture for a KOSHA regulatory corpus integrated with domain-level engineering calculation context. Walker et al. (2026) [6] propose RAGuard, which uses parallel indexing of safety-critical documents alongside technical manuals in an offshore wind maintenance setting, demonstrating large gains in Safety Recall@K across BM25, dense, and hybrid retrieval paradigms—the closest structural precedent to our system, but limited to a single industry domain with no Korean PSM statutory linkage. Klesel and Wittmann (2025) [7] provide an enterprise RAG survey and pose the question of how RAG-based systems can fulfil regulatory requirements as an open research direction, but leave actual regulatory corpus construction and engineering calculation integration unexplored.

### 2.3 Multi-Discipline Maintenance and Asset Integrity

AI-based asset integrity management frameworks for offshore oil and gas pipelines [8] focus on single-asset scope and do not cover electrical, instrumentation, or structural disciplines. Hector and Panjanathan (2024) [9] comprehensively survey IoT-enabled predictive maintenance planning models in Industry 4.0 but do not address standards-based calculation engines or regulatory RAG integration. Ait-Alla et al. (2022) [10] provide an overview of predictive maintenance workflows in Industry 4.0, without process-plant-specific seven-discipline integrated verification or PSM regulatory linkage.

### 2.4 Verification Methodology -- K-Voting Consensus

The N-version programming literature of Avizienis (1985) [11] establishes the theoretical basis for reliability improvement through consensus among independently executed computational paths. The Layer 2 K-voting consensus mechanism proposed in this study applies this principle to plant engineering domain calculation services; to our knowledge, this is the first application of such a mechanism in this context.

### 2.5 Korean PSM Regulation and KOSHA

Korean plants subject to the Chemical Substances Control Act and the Occupational Safety and Health Act must fulfil regular safety review obligations for pressure equipment, rotating machinery, electrical systems, and structures under the KOSHA PSM framework. These obligations apply across the plant lifecycle—from design verification during detailed engineering through to periodic in-service inspection. Recent domestic studies have introduced AI-based PSM management systems and regulation-grounded safety chatbots; however, these works use KOSHA regulations primarily for question-answering and document retrieval and do not extend to an engineering calculation verification layer integrated with ASME/API engines. An automated multi-discipline engineering verification architecture specialised for KOSHA regulations has not been reported in the literature, and the present work is the first systematic treatment of this problem.

---

## 3. System Architecture

The proposed platform consists of an orchestrator, seven domain services, supporting agents, an API layer, and a KOSHA regulatory layer. User requests—whether arising from design calculations, construction commissioning checks, or in-service inspection assessments—are received by a Qwen-based orchestrator that performs domain classification and routing. Each domain service follows an identical four-layer verification structure. Calculation outputs are passed to a cross-domain validator for coupling hazard analysis across predefined domain pairs. The KOSHA RAG layer translates the domain calculation context into a natural-language query, retrieves relevant regulatory passages from a local SQLite FTS index, and uses Qwen to generate structured regulatory grounding covering key conclusions, regulatory justification, and practical advisories. The final output is an integrated report containing calculation numerics, verification layer status, KOSHA regulatory grounding, and a full audit trail. All inference runs on an on-premises Ollama server, with no external data transmission.

---

## 4. KOSHA Regulatory Knowledge Layer

### 4.1 Corpus Construction

The KOSHA regulatory corpus was assembled from two public APIs. The KOSHA smart-search API was used to collect 18,576 rows of guide-section and statutory-provision metadata across categories 1-11. The KOSHA Guide API was used to download metadata and PDF files for 1,039 technical guidelines. Downloaded PDFs were parsed page-by-page, segmented into retrieval-optimised chunks, and normalised. The final corpus comprises 1,327 guide documents, 3,102 statutory provisions, and 18,576 indexed rows; the resulting SQLite FTS5 database is 133 MB.

### 4.2 Retrieval and Generation Pipeline

At query time, domain calculation outputs and input context are converted into a Korean natural-language query. BM25-based FTS retrieval uses a concept-aware query builder that joins query concepts with AND while expanding synonyms within each concept using OR; when no strict hit is returned, a loose expanded OR fallback is used. Retrieved passages are passed to Qwen as context; the model generates a structured Korean response comprising (1) key conclusion, (2) regulatory justification summary, and (3) practical advisories with citation indices. The current implementation uses BM25 to support CPU-only on-premises deployment without GPU resources; transition to semantic vector search is deferred to future work.

---

## 5. Seven-Domain Calculation Engines and Four-Layer Verification

### 5.1 Domain Calculation Engines

The seven domain calculation engines implement the following standards:

| Domain | Standards | Source |
|---|---|---|
| Piping | ASME B31.3, API 570 | `src/piping/` |
| Pressure Vessels | ASME Section VIII Div.1, API 510, API 579-1 | `src/vessel/` |
| Rotating Equipment | API 610, 617, 670 | `src/rotating/` |
| Electrical | IEEE C57.104, 1584-2018 | `src/electrical/` |
| Instrumentation | IEC 61511, ISA-TR84.00.02 | `src/instrumentation/` |
| Structural Steel | AISC 360 | `src/steel/` |
| Civil / Concrete | ACI 318, 562 | `src/civil/` |

Each engine follows a common service pattern: input schema parsing, standards-based calculation, four-layer verification, and result serialisation. The engines support both design-phase calculations (e.g., minimum required wall thickness for a new piping system) and in-service assessment (e.g., remaining life and inspection interval for an operating vessel).

### 5.2 Four-Layer Hybrid Verification Model

Implementation: `src/verification/` (engine.py, gates.py, maker.py, reverse_check.py)

**Layer 1 -- Input Validation**  
Checks mandatory field presence, unit contract compliance, and domain-specific range constraints. Missing critical fields or unit inconsistencies trigger a blocking error that prevents downstream calculation.

**Layer 2 -- K-Voting Consensus** (`src/verification/maker.py`)  
Three independent calculation paths execute in parallel and the maximum relative deviation among numeric outputs must not exceed 1%. If the threshold is exceeded, a tiebreaker path is invoked; persistent consensus failure raises `LOG.NO_CONSENSUS_AFTER_TIEBREAKER` and requests human review.

**Layer 3 -- Physics and Code Compliance** (`src/verification/gates.py`)  
Domain-specific red flags are enforced. For example, a current measured thickness below the computed minimum required thickness raises `PHY.CURRENT_THICKNESS_BELOW_MINIMUM` and blocks output. All major calculation steps carry explicit standard citations.

**Layer 4 -- Reverse Verification** (`src/verification/reverse_check.py`)  
Key inputs are back-calculated from outputs and compared against original inputs to verify internal consistency. A deviation exceeding 2% triggers a warning; a deviation exceeding 5% triggers escalation with a confidence downgrade and a full audit trail entry.

### 5.3 Cross-Domain Consistency Validator

Implementation: `src/cross_discipline/validator.py`

The cross-domain validator performs coupling checks across ten predefined domain pairs, including piping-vessel nozzle interface margin mismatches, electrical-rotating equipment harmonic distortion and bearing health coupling, and civil-rotating equipment foundation settlement and vibration linkage. Threshold tuning was conducted over fifty optimisation rounds (`scripts/tune_cross_discipline_thresholds.py`); the optimal profile achieves a standard-case blocking rate of 0.0, a boundary-case and failure-mode blocking rate of 1.0, and a weighted accuracy of 1.0. Extension to additional coupling pairs is deferred to future work.

---

## 6. Experiments and Evaluation

### 6.1 Calculation Accuracy on the Golden Dataset

Golden datasets: `datasets/golden_standards/` (7 domain JSON files, 220 cases total)  
Benchmark script: `scripts/benchmark_all_runtime.py`

A total of 220 synthetic golden cases were constructed across seven disciplines: 60% standard cases, 25% boundary cases, and 15% failure-mode cases. Acceptance thresholds were set at +/-1% for critical cases and +/-3% for non-critical cases, with a target red-flag detection rate of 100% and standard citation coverage of 100%. Runtime validation achieved 220/220 case passes across all seven disciplines, with accuracy, citation accuracy, and red-flag detection rate all recorded at 1.0000.

### 6.2 Seven-Discipline Pipeline Evaluation

Benchmark script: `scripts/benchmark_seven_pipeline.py`

Across 43 pipeline scenarios, the platform recorded a completion rate of 0.6512 and a blocking rate of 0.3488. Nominal and standard-aligned cases achieved a completion rate of 1.0000; boundary-aligned and failure-mode-aligned cases were blocked at a rate of 1.0000, confirming correct hazard identification.

### 6.3 Cross-Domain Validator Ablation

Ablation script: `scripts/benchmark_cross_discipline_ablation.py`

To quantify the incremental contribution of cross-domain coupling logic for RQ1, we evaluated the same 60 benchmark scenarios with the cross-discipline validator disabled and enabled. With the validator disabled, 0/60 scenarios were blocked. With the validator enabled, 25/60 scenarios were blocked, corresponding to an absolute increase of 25 blocked scenarios and a blocking-ratio increase of 0.4167. The most informative subsets are the aligned boundary and aligned failure sets, where blocking rises from 0.0 to 1.0 in both cases. Mixed scenarios also show non-trivial deltas: `mixed_first20` rises from 0.0 to 0.15, and `mixed_random20` rises from 0.0 to 0.60. These ablations directly quantify the incremental hazard-detection contribution of the cross-domain validator beyond discipline-isolated calculation outputs.

---

**Table 3. Cross-Domain Validator Ablation**

| Scenario Set | Validator OFF | Validator ON | Absolute Delta | Ratio Delta |
|---|---:|---:|---:|---:|
| aligned_standard | 0 / 10 | 0 / 10 | +0 | +0.00 |
| aligned_boundary | 0 / 6 | 6 / 6 | +6 | +1.00 |
| aligned_failure | 0 / 4 | 4 / 4 | +4 | +1.00 |
| mixed_first20 | 0 / 20 | 3 / 20 | +3 | +0.15 |
| mixed_random20 | 0 / 20 | 12 / 20 | +12 | +0.60 |
| **Overall** | **0 / 60** | **25 / 60** | **+25** | **+0.4167** |

---

### 6.4 KOSHA RAG Regulatory Grounding Analysis

RAG pipeline: `src/rag/local_kosha_rag.py`, `src/rag/engineering_synonyms.py`  
Index: `datasets/kosha_rag/kosha_local_rag.sqlite3` (133 MB)

Three representative cases demonstrate the incremental regulatory value of the KOSHA RAG layer. Results are summarised in Table 4; KOSHA citation quality is detailed in Table 5.

#### Case 1 -- Vessel Remaining Life (VES-GOLD-001)

For an SA-516-70 pressure vessel (design pressure 1.858 MPa, 217.3 C, current thickness 44.82 mm), the calculation engine computes a required shell thickness of 14.99 mm under ASME Section VIII UG-27, a remaining life of 136.3 years, and an API 510 inspection interval of 10 years, with no red flags raised. The KOSHA RAG layer retrieves M-69-2012 (Technical Guideline for Remaining Life Assessment of Pressure Vessels) as the top-ranked passage and identifies documentation requirements triggered when remaining life exceeds a defined threshold—requirements absent from the calculation engine output.

#### Case 2 -- RBI Planning (VES-GOLD-009)

For a vessel with a remaining life of 40.2 years (SA-516-70, 1.891 MPa, 241.9 C), the calculation engine recommends a 10-year inspection interval per API 510. The KOSHA RAG layer retrieves C-C-23-2026 (Technical Regulation for Equipment Reliability via Risk-Based Inspection) and B-M-18-2026 (Technical Regulation for Piping Life Management), identifying the trigger conditions under which a mandatory RBI review must be initiated under the Korean PSM framework.

#### Case 3 -- Piping Corrosion Compliance (PIP-GOLD-047)

For an SA-106 Gr.B carbon steel line in sour-chloride service (7.804 MPa, 196 C, 200 ppm Cl-), the calculation engine reports a remaining life of 13.3 years with no red flags raised. The KOSHA RAG layer retrieves, in ranked order, B-M-18-2026, Article 256 of the Rules on Occupational Safety and Health Standards (`산업안전보건기준에 관한 규칙`, Corrosion Prevention Provision), and C-C-75-2026 (Technical Regulation for Corrosion Risk Assessment of Chemical Equipment). The retrieval of Article 256 identifies a regulatory obligation to establish corrosion-prevention controls that applies even when ASME B31.3 and API 570 are fully satisfied—demonstrating a **jurisdiction compliance gap** that is structurally invisible to calculation-only workflows.

---

**Table 4. KOSHA RAG Incremental Coverage Summary**

| Case | Discipline | Calc. Result | Red Flags | Top KOSHA RAG Retrieval |
|---|---|---|---|---|
| VES-GOLD-001 | Vessel | PASS (RL = 136.3 yr) | None | M-69-2012 Remaining Life Evaluation |
| VES-GOLD-009 | Vessel | PASS (RL = 40.2 yr) | None | C-C-23-2026 RBI Technical Regulation |
| PIP-GOLD-047 | Piping | PASS (RL = 13.3 yr) | None | B-M-18-2026, Art. 256, C-C-75-2026 |

---

**Table 5. KOSHA Citation Quality Analysis**

| Source Type | Guide No. | Document Title | Jurisdictional Basis | Triggered By |
|---|---|---|---|---|
| KOSHA Guide | M-69-2012 | Technical Guideline for Remaining Life Assessment of Pressure Vessels | PSM / KOSHA | Vessel remaining life context |
| KOSHA Guide | C-C-23-2026 | Technical Regulation for Equipment Reliability via RBI | PSM mandatory | Short RL + corrosion rate |
| KOSHA Guide | B-M-18-2026 | Technical Regulation for Piping Life Management | PSM / facility mgmt. | High CR + sour service |
| Korean Rule | Article 256 | Rules on Occupational Safety and Health Standards: Corrosion Prevention Provision | Regulatory (`산업안전보건기준에 관한 규칙`) | Chloride + sour service |
| KOSHA Guide | C-C-75-2026 | Technical Regulation for Corrosion Risk Assessment | PSM risk assessment | CR exceeds threshold |

---

### 6.5 Curated Retrieval Benchmark

Retrieval benchmark: `scripts/benchmark_rag_retrieval.py`  
Benchmark dataset: `datasets/kosha_rag/rag_eval_queries.json` (50 curated queries)

To quantify the retrieval effect of synonym-aware regulatory search for RQ2, we constructed a 50-query curated benchmark organised as five regulatory target groups with ten queries per group. The query set mixes Korean and English phrasings, abbreviations, and variant wording around M-69-2012, C-C-23-2026, B-M-18-2026, C-C-75-2026, and Article 256 of the Rules on Occupational Safety and Health Standards. Plain FTS achieves Recall@1 = 0.44, Recall@3 = 0.74, Recall@5 = 0.74, and MRR@10 = 0.5744. The enhanced retrieval configuration improves these to Recall@1 = 0.74, Recall@3 = 0.86, Recall@5 = 0.86, and MRR@10 = 0.7933, yielding absolute gains of +0.30, +0.12, +0.12, and +0.2189 respectively. On the three manuscript case queries, the code-only baseline, defined as international-code calculation outputs plus engine red flags without Korean regulatory retrieval, detects 0/3 Korean-jurisdiction regulatory obligations, whereas the regulatory RAG layer detects 3/3.

---

**Table 6. KOSHA RAG Retrieval Benchmark**

| Metric | Plain FTS | Enhanced FTS | Absolute Delta |
|---|---:|---:|---:|
| Recall@1 | 0.44 | 0.74 | +0.30 |
| Recall@3 | 0.74 | 0.86 | +0.12 |
| Recall@5 | 0.74 | 0.86 | +0.12 |
| MRR@10 | 0.5744 | 0.7933 | +0.2189 |

---

**Table 7. Code-Only vs Regulatory RAG Case Ablation**

| Case | Code-Only Detected | Regulatory RAG Detected | First Relevant Rank |
|---|---:|---:|---:|
| VES-GOLD-001 | 0 | 1 | 1 |
| VES-GOLD-009 | 0 | 1 | 1 |
| PIP-GOLD-047 | 0 | 1 | 1 |
| **Total** | **0 / 3** | **3 / 3** | — |

---

## 7. Discussion

The most significant finding of this study is the existence of the **jurisdiction compliance gap**. Even in cases where international code calculations produce a clean pass, the KOSHA RAG layer identifies additional Korean-jurisdiction compliance requirements. This occurs because ASME, API, and analogous international standards define technical calculation requirements, whereas KOSHA guidelines and Korean safety regulations—including Article 256 of the Rules on Occupational Safety and Health Standards—impose procedural, documentation, and compliance obligations that are conditioned on calculation outputs but are not encoded within the international standards themselves. This gap is structurally present regardless of whether the calculation arises from a design-phase check or an in-service inspection assessment.

The process-safety contribution of this system operates through two pathways. First, the cross-domain validator proactively identifies coupling hazards that single-domain calculations miss. Representative failure scenarios include excessive piping nozzle loads driving rotating equipment bearing degradation, and civil foundation settlement propagating into rotating equipment alignment failure—both well-documented failure modes in the mechanical and structural engineering literature. Second, as demonstrated in Case 3, the KOSHA RAG layer identifies the corrosion-prevention obligation under Article 256 of the Rules on Occupational Safety and Health Standards even when ASME B31.3 and API 570 are fully satisfied. If this obligation is left unaddressed, unmonitored corrosion progression in a high-temperature, high-pressure carbon steel line may result in leakage or rupture. In summary, the system provides a mechanism for automatically detecting the condition of being technically compliant with international standards while remaining legally non-compliant under Korean regulation.

Reproducibility and explainability are core strengths of the system. Every major calculation step carries an explicit standard citation, and the golden dataset and benchmark scripts are publicly released, enabling independent replication.

---

## 8. Limitations

This study has the following limitations. First, the golden dataset used for evaluation is entirely synthetic; no external validation against real plant operating or design-phase data has been performed. Second, some domain outputs represent screening-level assessments that cannot substitute for detailed engineering design review. Third, the regulatory retrieval benchmark is curated rather than drawn from production user logs, and BM25 keyword retrieval may still miss semantically similar Korean documents even with concept-aware synonym expansion and OR fallback. Fourth, the cross-domain coupling validation is limited to ten predefined domain pairs. Fifth, the baseline comparisons reported in this study are internal ablations (`validator off`, `plain FTS`, and `code-only`) rather than external industrial workflow baselines.

Future research directions include: (1) field pilot validation using real plant data—both design-phase engineering calculations and operating-plant inspection records—to calibrate synthetic thresholds and regulatory trigger conditions; (2) integration with RBI and HAZOP workflows to connect system outputs directly with existing PSM documentation; (3) transition to semantic vector search using a Korean embedding model in GPU-capable deployment environments; and (4) systematic expansion of the cross-domain coupling pair set beyond the current ten pairs.

---

## 9. Conclusion

This paper has presented an integrated platform combining standards-based calculation engines for seven process plant engineering disciplines, a four-layer hybrid verification model, and a KOSHA regulatory RAG layer applicable across the full plant lifecycle from design through operation. All 220 synthetic golden cases pass end-to-end validation. A 60-scenario cross-discipline ablation shows that enabling the cross-validator increases blocking from 0 to 25 scenarios, with aligned boundary and failure subsets rising from 0.0 to 1.0. A 50-query curated retrieval benchmark further shows that enhanced regulatory retrieval improves Recall@1 from 0.44 to 0.74 and MRR@10 from 0.5744 to 0.7933 over plain FTS retrieval. Three representative cases provide empirical evidence that the KOSHA RAG layer identifies jurisdiction compliance gaps structurally invisible to international-code-only calculation workflows. In particular, Case 3—in which Article 256 corrosion-prevention obligations are detected despite a full calculation pass—clearly delineates the structural limitation of calculation-only engineering review.

Code, golden datasets, and benchmark scripts are publicly released under the AGPL license via GitHub and available via arXiv preprint. Future work will focus on field pilot validation with real plant data, quantitative ablation of the four verification layers, and systematic evaluation of KOSHA RAG retrieval quality.

---

## References

**[1]** Selvam, D.C., Raja, T., Vaghela, D.R., Meena, M., Tripathy, S., Kumar, B., Manjunath, H.R., Mehar, K., Devarajan, Y. (2026). Artificial intelligence in process safety: A review of opportunities, challenges, and future directions for the chemical process industries. *Journal of Loss Prevention in the Process Industries.* DOI: 10.1016/j.jlp.2026.105917

**[2]** Woo, T., Kim, S., Tariq, S., Heo, S., Yoo, C. (2025). Leveraging Generative AI and Large Language Model for Process Systems Engineering: A State-of-the-Art Review. *Korean Journal of Chemical Engineering,* 42, 2787-2808. DOI: 10.1007/s11814-025-00524-y

**[3]** Elhosary, M. et al. (2024). LLM-assisted HAZOP study using retrieval-augmented generation. *IChemE Symposium Series No. 171: Hazards 34.*

**[4]** Walavalkar, V. et al. (2021). Machine Learning and Deep Learning in Chemical Health and Safety: A Systematic Review of Techniques and Applications. *ACS Chemical Health & Safety.* DOI: 10.1021/acs.chas.0c00075

**[5]** Lewis, P., Perez, E., Piktus, A. et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. *Advances in Neural Information Processing Systems (NeurIPS 2020),* 33, 9459-9474.

**[6]** Walker, C., Aslansefat, K., Akram, M.N., Papadopoulos, Y. (2026). RAGuard: A Novel Approach for In-Context Safe Retrieval Augmented Generation for LLMs. In: Katsaros, P. (ed.) *Model-Based Safety and Assessment. IMBSA 2025.* Lecture Notes in Computer Science, vol 15755. Springer, Cham. DOI: 10.1007/978-3-032-05073-1_13

**[7]** Klesel, M., Wittmann, H.F. (2025). Retrieval-Augmented Generation (RAG). *Business & Information Systems Engineering,* 67(4), 551-561. DOI: 10.1007/s12599-025-00945-3

**[8]** Jones, J.F., Raj, V., Abas, P.E., Petra, M.I., Sivan, D., Satheesh Kumar, K., Jose, R., Mathew, S. (2025). Application of artificial intelligence for asset integrity management of offshore oil and gas pipelines. *Life Cycle Reliability and Safety Engineering.* DOI: 10.1007/s41872-025-00353-2

**[9]** Hector, I., Panjanathan, R. (2024). Predictive maintenance in Industry 4.0: a survey of planning models and machine learning techniques. *PeerJ Computer Science,* 10, e2016. DOI: 10.7717/peerj-cs.2016

**[10]** Ait-Alla, A., Quandt, M., Lutjen, M., Freitag, M. (2022). On Predictive Maintenance in Industry 4.0: Overview, Models, and Challenges. *Applied Sciences,* 12(16), 8081. DOI: 10.3390/app12168081

**[11]** Avizienis, A. (1985). The N-version approach to fault-tolerant software. *IEEE Transactions on Software Engineering,* SE-11(12), 1491-1501.

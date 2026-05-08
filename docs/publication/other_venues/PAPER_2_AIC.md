# Automating Cross-Discipline Engineering Verification in EPC Plant Projects: A Seven-Domain Platform with KOSHA Regulatory Grounding

**Yuyong Kim**

*University of Wisconsin–Madison, Madison, WI 53706, USA*
*M.S. Data, Insights & Analytics; B.S. Chemical & Biological Engineering; 12+ years of petrochemical EPC and process plant engineering*

---

## Highlights

- Integrated verification of seven engineering disciplines (piping, vessels, rotating, electrical, instrumentation, steel, civil) automates a workflow currently fragmented across siloed EPC tools.
- Cross-discipline coupling validator identifies 25 additional hazards in 60 scenarios (+41.7%) that single-discipline calculations cannot detect — covering nozzle loads, foundation settlement, harmonic distortion, and other inter-discipline failure paths.
- KOSHA regulatory RAG layer detects Korean PSM obligations invisible to ASME/API/IEEE code calculations, including Article 256 corrosion-prevention requirements.
- Four-layer verification — input gates, K-voting consensus, physics compliance, reverse verification — provides auditable confidence for engineering deliverables across design, construction, and inspection phases.
- Open-source release (AGPL-3.0) with 220 golden test cases, benchmarks, and full code-to-paper mapping.

---

## Abstract

Engineering verification in EPC (Engineering, Procurement, and Construction) plant projects spans seven or more disciplines — piping, pressure vessels, rotating equipment, electrical systems, instrumentation, structural steel, and civil structures — and recurs at every lifecycle phase from design through in-service inspection. Current practice relies on discipline-specific tools operated by separate engineering groups, creating two gaps: cross-discipline coupling hazards are structurally undetectable, and Korean-jurisdiction regulatory obligations beyond international code compliance are not enforced. This paper presents a platform that automates multi-discipline verification with three integrated capabilities: (i) seven domain calculation engines implementing 16 major standards (ASME B31.3, ASME VIII, API 510/570/579-1, IEEE C57.104/1584, IEC 61511, ISA-TR84, AISC 360, ACI 318/562); (ii) a four-layer verification model combining input validation, K-voting consensus, physics/code compliance, and reverse verification; and (iii) a KOSHA regulatory RAG layer indexing 16,186 entries from 1,327 guide documents and 3,102 statutory provisions. On 220 synthetic golden cases, all seven disciplines achieve 100% accuracy and red-flag detection. A 60-scenario cross-discipline ablation shows that coupling validation adds 25 blocked hazard scenarios (+41.7%), with boundary and failure subsets blocked at 100% and zero false positives on standard cases. A 50-query retrieval benchmark improves Recall@1 from 0.44 to 0.74 over plain full-text search. Three case studies demonstrate that ASME/API/IEEE-compliant calculations can miss Korean-jurisdiction obligations — a **jurisdiction compliance gap** with direct consequences for EPC project delivery and plant operation under Korean PSM law.

**Keywords:** EPC engineering; construction automation; multi-discipline verification; process plant; KOSHA PSM; cross-discipline coupling; regulatory AI; asset integrity management

---

## 1. Introduction

### 1.1. The fragmentation problem in EPC engineering

In a typical Korean EPC project, engineering verification involves seven or more discipline groups working with separate tools, separate deliverable formats, and separate review procedures:

- **Piping engineers** verify wall thickness per ASME B31.3 and assess remaining life per API 570.
- **Static equipment engineers** check vessel shell thickness per ASME Section VIII and fitness-for-service per API 579-1.
- **Rotating equipment engineers** evaluate vibration per API 610/617 and bearing health per API 670.
- **Electrical engineers** assess transformer health per IEEE C57.104 and arc-flash per IEEE 1584.
- **Instrumentation engineers** verify SIL per IEC 61511 and calibration per ISA-TR84.
- **Structural engineers** check steel D/C ratios per AISC 360 and concrete adequacy per ACI 318/562.

Each group produces discipline-specific calculations that are correct within their domain. But the physical plant is not discipline-siloed — a pressure vessel connects to piping via nozzles, rotating equipment sits on civil foundations, electrical power quality affects instrumentation signals. Cross-discipline coupling hazards arise at these interfaces and are invisible to single-domain tools.

### 1.2. The regulatory compliance challenge

Korean plants under the Occupational Safety and Health Act must satisfy the KOSHA PSM framework. Unlike international codes that define calculation methodology, KOSHA guidelines impose additional obligations: documentation requirements when remaining life exceeds thresholds, mandatory RBI review triggers, corrosion-prevention controls for specific service conditions. These obligations are conditioned on calculation results but exist outside the scope of ASME/API/IEEE calculations.

An EPC contractor can deliver calculation packages that satisfy every international code requirement and still leave the plant owner exposed to Korean regulatory non-compliance. We term this a **jurisdiction compliance gap**.

### 1.3. Contributions

1. A platform automating verification across seven EPC disciplines with inter-discipline coupling detection across ten domain pairs.
2. A four-layer verification model providing auditable confidence for engineering deliverables.
3. The first KOSHA regulatory corpus integration into engineering AI verification (16,186 indexed entries).
4. Empirical demonstration that international-code-compliant calculations can miss Korean PSM obligations.

---

## 2. Related Work

### 2.1. Automation in plant engineering

AI applications in process plant engineering have focused primarily on anomaly detection (Selvam et al., 2026), process design optimisation (Woo et al., 2025), and HAZOP support (Elhosary et al., 2024). These approaches either address single-process scope or do not integrate standards-based calculation engines. Asset integrity management frameworks (Jones et al., 2025) cover single-asset pipelines without multi-discipline scope. Predictive maintenance surveys (Hector and Panjanathan, 2024; Ait-Alla et al., 2022) address sensor-driven monitoring without calculation verification or regulatory compliance.

The construction automation literature has explored BIM-based code checking, generative design, and robotic construction. However, the specific problem of multi-discipline engineering calculation verification across EPC lifecycle phases has not been systematically addressed.

### 2.2. Regulatory AI

RAG for regulatory domains remains an emerging direction (Klesel and Wittmann, 2025). Walker et al. (2026) demonstrate safety-document RAG for offshore wind maintenance. Kim et al. (2022) and Lee and Ahn (2025) use KOSHA data for accident classification and safety Q&A respectively, without calculation-integrated verification.

---

## 3. System Architecture and Technology

### 3.1. Platform overview

The platform receives calculation requests from any EPC lifecycle phase — detailed engineering design checks, construction commissioning verification, or in-service inspection assessment. A rule-based orchestrator classifies each request by discipline and routes it to the appropriate engine.

**Processing flow:**
1. Input validation (Layer 1) gates the request.
2. Three parallel calculation paths execute with varied numerical strategies.
3. K-voting consensus (Layer 2) verifies path agreement within 1%.
4. Physics/code compliance (Layer 3) checks domain-specific red flags.
5. Reverse verification (Layer 4) back-calculates inputs for consistency.
6. Cross-discipline validator checks coupling across applicable domain pairs.
7. KOSHA RAG queries retrieve jurisdiction-specific regulatory grounding.
8. Integrated report combines numerics, verification, regulatory citations, and audit trail.

### 3.2. Seven domain engines

Each engine follows a common service pattern — input schema parsing, standards-based calculation, four-layer verification, and result serialisation — while implementing discipline-specific calculation logic.

| Domain | Standards | Lifecycle Applications |
|---|---|---|
| Piping | ASME B31.3, API 570 | Design wall thickness; in-service remaining life and inspection interval |
| Vessels | ASME VIII, API 510, API 579-1 | Design shell thickness; FFS screening; remaining life assessment |
| Rotating | API 610, 617, 670 | Vibration acceptance; bearing health monitoring; steam state screening |
| Electrical | IEEE C57.104, 1584-2018 | Transformer condition; arc-flash hazard analysis |
| Instrumentation | IEC 61511, ISA-TR84 | SIL verification; calibration interval optimisation |
| Steel | AISC 360 | D/C ratio; fatigue assessment; section loss evaluation |
| Civil | ACI 318, 562 | Flexure adequacy; carbonation assessment; repair prioritisation |

### 3.3. Cross-discipline coupling

Ten predefined domain pairs address documented inter-discipline failure mechanisms:

| Pair | Failure Mechanism | EPC Phase Relevance |
|---|---|---|
| Piping ↔ Vessel | Nozzle load exceeds vessel reinforcement | Design & inspection |
| Piping ↔ Rotating | Nozzle force degrades bearings | Commissioning & operation |
| Electrical ↔ Rotating | Harmonic distortion overheats bearings | Operation |
| Civil ↔ Rotating | Settlement misaligns machinery | Construction & operation |
| Electrical ↔ Instrumentation | Power quality degrades signal accuracy | Commissioning |
| Steel ↔ Civil | Steel demand exceeds foundation capacity | Design |
| Vessel ↔ Piping | Reciprocal nozzle load check | Design |
| Steel ↔ Rotating | Support vibration amplification | Operation |
| Instrumentation ↔ Vessel | Safety function vs equipment condition | Inspection |
| Civil ↔ Piping | Settlement induces pipe stress | Operation |

Coupling thresholds were tuned over 50 optimisation rounds, achieving a composite score of 0.84 with: zero false positives on standard cases (blocking rate 0.0), perfect detection on boundary and failure cases (blocking rate 1.0), weighted accuracy 1.0, and hard-block recall 1.0.

### 3.4. KOSHA regulatory RAG

**Corpus:** 16,186 searchable rows in SQLite FTS5 — 13,084 guide document chunks (from 1,327 KOSHA guides, 1,039 PDFs parsed page-by-page) and 3,102 law-article entries (from 3,102 statutory provisions).

**Retrieval:** Concept-aware BM25 with Korean engineering synonym expansion. AND-joined concept queries with OR-expanded synonyms; fallback to loose OR matching on zero-hit results.

**Generation:** Qwen 2.5 7B Instruct on-premises (4-bit quantisation, no external data transmission) generates structured regulatory grounding from retrieved passages.

### 3.5. Technology stack

- Backend: Python FastAPI with WebSocket support for real-time updates
- LLM: Ollama + Qwen 2.5 7B Instruct, CPU-only, 32K context
- Index: SQLite FTS5, 200 MB
- Frontend: Next.js 14 with bilingual (English/Korean) interface
- Data sovereignty: all processing on-premises

---

## 4. Evaluation

### 4.1. Golden dataset (calculation correctness)

220 synthetic cases across seven disciplines: 55% standard, 25% boundary, 17% failure, 2% composite. All derived from reference examples in applicable standards with systematic perturbation.

**Result:** 220/220 pass. Accuracy, red-flag detection, and standard citation coverage: 1.0000 across all seven disciplines. Expected for deterministic rule-based engines; confirms implementation correctness.

### 4.2. Seven-discipline pipeline (end-to-end behaviour)

43 pipeline scenarios combining multiple discipline calculations:

| Scenario Type | Count | Completion | Blocking |
|---|---:|---:|---:|
| Nominal handcrafted | 5 | 1.000 | 0/5 |
| Standard aligned | 8 | 1.000 | 0/8 |
| Boundary aligned | 6 | 0.000 | 6/6 |
| Failure aligned | 4 | 0.000 | 4/4 |
| Mixed first 20 | 20 | 0.750 | 5/20 |
| **Total** | **43** | **0.651** | **15/43** |

Clean inputs complete successfully; hazardous inputs are correctly blocked.

### 4.3. Cross-discipline ablation (RQ1: coupling hazard detection)

60 scenarios evaluated with cross-discipline validator disabled vs. enabled:

| Scenario Set | OFF | ON | Delta |
|---|---:|---:|---:|
| aligned_standard | 0/10 | 0/10 | +0 |
| aligned_boundary | 0/6 | 6/6 | +6 |
| aligned_failure | 0/4 | 4/4 | +4 |
| mixed_first20 | 0/20 | 3/20 | +3 |
| mixed_random20 | 0/20 | 12/20 | +12 |
| **Overall** | **0/60** | **25/60** | **+25 (+41.7%)** |

**Key result:** 25 hazard scenarios detectable only through cross-discipline coupling analysis. These represent the exact class of inter-discipline failures that fragmented EPC workflows systematically miss.

### 4.4. KOSHA RAG retrieval (RQ2: regulatory gap detection)

50-query benchmark across five regulatory targets:

| Metric | Plain FTS | Enhanced | Delta |
|---|---:|---:|---:|
| Recall@1 | 0.44 | 0.74 | +0.30 |
| Recall@3 | 0.74 | 0.86 | +0.12 |
| MRR@10 | 0.5744 | 0.7933 | +0.2189 |

### 4.5. Jurisdiction compliance gap — three EPC case studies

| Case | Service | Code Result | KOSHA Finding | EPC Impact |
|---|---|---|---|---|
| VES-GOLD-001 | Vessel (SA-516-70, 1.858 MPa) | PASS, RL=136.3 yr | M-69-2012: RL documentation required | Design deliverable gap |
| VES-GOLD-009 | Vessel (SA-516-70, 1.891 MPa) | PASS, RL=40.2 yr | C-C-23-2026: mandatory RBI trigger | Inspection programme gap |
| PIP-GOLD-047 | Piping (SA-106 Gr.B, sour service) | PASS, RL=14.0 yr | Article 256: corrosion prevention obligation | Regulatory compliance gap |

**Code-only detection:** 0/3. **RAG detection:** 3/3.

**Case 3 in detail:** An SA-106 Gr.B carbon steel piping system in sour-chloride service (7.804 MPa, 196 °C, 200 ppm Cl-) with a calculated remaining life of 14.0 years passes all ASME B31.3 wall-thickness checks and API 570 inspection criteria. No red flags are raised. However, Article 256 of the Rules on Occupational Safety and Health Standards (`산업안전보건기준에 관한 규칙`) imposes an obligation to establish corrosion-prevention controls for equipment in corrosive service — an obligation structurally absent from the international code calculation scope. In an EPC context, this means a contractor's calculation package can satisfy all international deliverables while leaving the owner exposed to Korean regulatory non-compliance during the PSM audit cycle.

---

## 5. Discussion

### 5.1. Implications for EPC practice

**Design phase:** The platform enables discipline leads to identify both cross-discipline coupling issues and Korean regulatory obligations during the calculation stage — before deliverables are issued. Currently, coupling issues are typically caught during interdisciplinary design review (IDR) meetings, if at all, and KOSHA obligations are addressed manually by the owner's PSM team after handover.

**Construction phase:** Commissioning checklists derived from international codes may omit Korean-specific verification steps. The platform's regulatory layer provides an automated check against KOSHA requirements relevant to the commissioning context.

**Inspection phase:** In-service inspection programmes following API 510/570 schedules may not satisfy KOSHA-mandated review triggers. The platform identifies when KOSHA review conditions are activated by calculation results.

### 5.2. Cross-discipline coupling in practice

The 41.7% increase in blocked scenarios corresponds to real failure pathways documented in plant engineering:
- Piping thermal expansion generating nozzle loads that exceed vessel reinforcement — a common interface issue in FEED (Front-End Engineering Design).
- Foundation settlement from adjacent construction activity causing rotating equipment misalignment — frequently observed during commissioning.
- Electrical harmonic distortion from VFD (Variable Frequency Drive) installations degrading bearing life — an operational reliability concern.

These are not theoretical hazards; they are the subject of engineering change orders, warranty claims, and incident investigations in EPC projects.

### 5.3. Generalisability

The jurisdiction compliance gap concept extends beyond Korea. Any national jurisdiction with safety regulations layered atop international engineering codes — EU PED on ASME, Saudi regulations on API, Chinese GB on ISO — may exhibit analogous gaps detectable through the same architectural pattern: domain calculation engine + jurisdiction-specific regulatory RAG.

---

## 6. Limitations and Future Work

1. **Synthetic validation only.** Field validation with real EPC project data (both design calculations and inspection records) is the critical next step.
2. **Screening-level outputs.** Not a substitute for detailed engineering design review or fitness-for-service assessment.
3. **Curated retrieval benchmark.** BM25 with synonym expansion may still miss semantically similar Korean documents; transition to Korean embedding models is planned.
4. **Ten coupling pairs.** Systematic expansion through analysis of EPC change orders and incident databases.
5. **Internal baselines.** Comparison against actual EPC workflow efficiency and error rates is needed.

**Future directions:** Field pilot with an operating Korean petrochemical plant, RBI/HAZOP workflow integration, semantic vector search, and application of the jurisdiction compliance gap framework to other national regulatory contexts.

---

## 7. Conclusion

This paper presented a platform for automating multi-discipline engineering verification across seven EPC plant engineering domains. The cross-discipline validator detects 25 additional hazard scenarios (+41.7%) invisible to single-discipline tools. The KOSHA RAG layer identifies Korean-jurisdiction obligations in 3/3 cases where international codes fully pass. The jurisdiction compliance gap — the structural space between code compliance and regulatory fulfilment — has practical consequences for EPC project delivery and plant operation that this platform addresses at the calculation stage.

---

## Code and Data Availability

Source code, golden datasets, and benchmarks: [https://github.com/yuyongkim/did-you-check-kosha](https://github.com/yuyongkim/did-you-check-kosha) (AGPL-3.0).

---

## References

Ait-Alla, A. et al., 2022. On Predictive Maintenance in Industry 4.0. Applied Sciences 12 (16), 8081.

Avizienis, A., 1985. The N-version approach to fault-tolerant software. IEEE Trans. Softw. Eng. SE-11 (12), 1491–1501.

Elhosary, M. et al., 2024. LLM-assisted HAZOP study using RAG. IChemE Hazards 34.

Gao, Y. et al., 2024. RAG for Large Language Models: A Survey. arXiv:2312.10997.

Hector, I., Panjanathan, R., 2024. Predictive maintenance in Industry 4.0. PeerJ Comput. Sci. 10, e2016.

Jones, J.F. et al., 2025. AI for asset integrity of offshore pipelines. Life Cycle Rel. Safety Eng.

Kim, H. et al., 2022. Multi-cause Accident Analysis From KOSHA Reports. J. Arch. Inst. Korea 38 (4), 237–244.

Klesel, M., Wittmann, H.F., 2025. Retrieval-Augmented Generation (RAG). Bus. Inf. Syst. Eng. 67 (4), 551–561.

Lee, J., Ahn, S., 2025. AI for Construction Safety via Fine-Tuning LLM. Korean J. Constr. Eng. Mgmt. 26 (2), 20–31.

Lewis, P. et al., 2020. RAG for Knowledge-Intensive NLP Tasks. NeurIPS 2020, 33, 9459–9474.

Robertson, S., Zaragoza, H., 2009. BM25 and Beyond. Found. Trends Inf. Ret. 3 (4), 333–389.

Selvam, D.C. et al., 2026. AI in process safety. J. Loss Prevention in the Process Industries.

Walavalkar, V. et al., 2021. ML in Chemical Health and Safety. ACS Chem. Health Saf.

Walker, C. et al., 2026. RAGuard: Safe RAG for LLMs. IMBSA 2025, LNCS 15755.

Woo, T. et al., 2025. Generative AI for Process Systems Engineering. Korean J. Chem. Eng. 42, 2787–2808.

ASME, 2022. ASME B31.3-2022: Process Piping.

API, 2020. API 579-1/ASME FFS-1, 3rd ed.

KOSHA, 2026. KOSHA Guide Portal. https://www.kosha.or.kr

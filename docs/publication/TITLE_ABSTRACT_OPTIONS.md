# Title And Abstract Options
Status: Draft

## Option 1
### Working Title
A Seven-Discipline EPC Maintenance Verification Framework with Layered Validation and Cross-Discipline Consistency Checks

### Positioning
- Best for a systems or engineering-AI paper
- Emphasizes architecture, verification logic, and integrated workflow

### Abstract Draft
Engineering maintenance screening in process plants is often fragmented across discipline-specific tools, making integrated risk interpretation difficult. This work presents a seven-discipline EPC maintenance verification framework covering piping, vessel, rotating equipment, electrical, instrumentation, steel, and civil domains. The framework combines discipline-level calculation services, a four-layer verification model, cross-discipline consistency checks, and a regulatory support layer based on local KOSHA corpus synchronization, guide parsing, and local retrieval-augmented lookup. Layer 1 enforces input, unit, and range validity; Layer 2 applies multi-path consensus; Layer 3 performs physics and standards compliance checks; and Layer 4 executes reverse verification. In parallel, a local RAG path supports standards and guide-grounded regulatory review, with optional local-LLM answer generation on top of the retrieved corpus. To evaluate the framework, we define synthetic golden datasets across all seven disciplines and benchmark both discipline-level accuracy and multi-discipline orchestration behavior. The runtime verification report shows full pass coverage on 220 golden cases, while the seven-discipline pipeline and cross-discipline benchmarks demonstrate differentiated blocking behavior across nominal, boundary, failure, and mixed scenarios. The result is an explainable screening-oriented architecture that can support traceable engineering review while remaining extensible toward richer field inputs, stronger regulatory grounding, and real-site validation.

## Option 2
### Working Title
Explainable Multi-Agent Engineering Screening for EPC Maintenance Using Synthetic Golden Datasets and Cross-Discipline Threshold Tuning

### Positioning
- Best for a verification- and evaluation-focused paper
- Emphasizes explainability, datasets, and threshold tuning

### Abstract Draft
Reliable engineering screening for maintenance decisions requires more than isolated discipline calculations; it also requires traceability, verification, and coherent interpretation across interacting systems. This paper introduces an explainable multi-agent engineering screening framework for EPC maintenance applications. The framework integrates seven discipline services, a standards-aware audit trail, four-layer verification, a cross-discipline validator with tunable thresholds, and a local regulatory knowledge path using KOSHA corpus snapshots, guide ingestion, and local RAG retrieval. Optional local-LLM answer generation is supported on top of the retrieved corpus for offline or on-premise use cases. We further define synthetic golden datasets and scenario categories for standard, boundary, and failure conditions, enabling structured evaluation of discipline-level and integrated behavior. The proposed benchmark workflow includes runtime verification, seven-discipline orchestration assessment, and cross-discipline threshold tuning. Experimental artifacts in the repository show full golden-case pass performance at the discipline level and selective blocking behavior under cross-discipline failure scenarios. The study contributes a reusable architecture for explainable engineering-AI screening and regulatory-grounded review, together with a reproducible validation package that can be extended toward real industrial datasets and domain-specific deployment studies.

## Option 3
### Working Title
Design And Validation Of A Unified Engineering-AI Workbench For Seven-Domain EPC Maintenance Screening

### Positioning
- Best for an application-oriented paper
- Emphasizes practical integration and deployable workbench structure

### Abstract Draft
Industrial maintenance review in EPC environments spans multiple engineering domains but is frequently supported by disconnected calculation workflows and non-uniform validation practices. This paper describes the design and validation of a unified engineering-AI workbench for seven-domain maintenance screening. The proposed system integrates domain calculation modules, API-based execution, report packaging, synthetic dataset generation, local regulatory retrieval, and cross-discipline validation in a single runtime environment. Each discipline service follows a common pattern of models, calculations, verification, and service orchestration, while the platform-level pipeline adds auditability, blocking logic for multi-discipline risk interactions, and a local RAG path grounded in KOSHA corpus and guide assets with optional local-LLM generation support. Repository results indicate that the framework supports complete discipline-level runtime verification on the current golden dataset suite and produces interpretable blocking outcomes for seven-discipline scenarios. The work demonstrates a practical bridge between engineering code rules, local regulatory knowledge support, explainable software architecture, and reproducible screening workflows suitable for conference publication and later journal extension.

## Recommendation
- Best immediate submission candidate:
  - Option 1
- Reason:
  - it balances architecture, verification, datasets, and experimental results without over-claiming a novel learning model

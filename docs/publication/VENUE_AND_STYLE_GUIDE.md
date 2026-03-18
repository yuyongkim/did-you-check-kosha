# Venue And Style Guide
Status: Draft

## Recommendation
- Recommended first submission path:
  - domestic engineering or industrial-AI conference style paper
- Recommended second submission path:
  - expanded SCI-style journal manuscript after additional validation

## Why The Domestic Conference Route Is Better First
- The repository already has a strong systems implementation, reproducible artifacts, tests, and benchmark outputs.
- The current validation is solid for a framework paper, but still relies heavily on synthetic golden datasets.
- Several discipline outputs are explicitly screening-level rather than full high-fidelity design outputs.
- A conference paper can establish the architecture, verification model, and evaluation protocol without over-claiming.

## Domestic Conference Style
### Good Fit
- Applied engineering system
- Explainable verification framework
- Prototype plus reproducible benchmark package

### Typical Emphasis
- Problem definition
- System architecture
- Key calculation and verification logic
- Benchmark results
- Practical implications

### Writing Style
- Direct
- Implementation-centered
- Moderate literature review
- Strong figure and table usage

### Suggested Length
- About 6 to 8 pages for an initial paper

### Recommended Core Message
- We built and validated a seven-discipline engineering screening framework with layered verification, cross-discipline blocking logic, and a local regulatory support layer grounded in KOSHA corpus and guide retrieval.

## SCI-Style Journal Manuscript
### Good Fit
- Extended version after stronger validation
- Best once at least one of the following is added:
  - real plant case studies
  - external expert comparison
  - ablation or sensitivity study beyond current benchmark scripts
  - stronger quantitative comparison against a baseline workflow

### Typical Emphasis
- Clear novelty statement
- More formal related work section
- Stronger experimental methodology
- More detailed limitation analysis
- Broader reproducibility and generalization discussion

### Writing Style
- More cautious and formal
- More explicit claims-to-evidence mapping
- Stronger discussion of assumptions and threats to validity

### Suggested Length
- About 10 to 14 pages or journal-equivalent structure

### Recommended Core Message
- We propose an explainable, reproducible engineering verification framework and show that its layered validation architecture and local regulatory knowledge layer support robust cross-discipline screening behavior.

## Submission Strategy
### Stage 1
- Prepare domestic conference manuscript using:
  - `docs/publication/TITLE_ABSTRACT_OPTIONS.md`
  - `docs/publication/PAPER_OUTLINE_AND_SOURCE_MAP.md`
  - `docs/publication/MANUSCRIPT_SKELETON.md`

### Stage 2
- Expand to journal style by adding:
  - external validation
  - comparison with manual or single-discipline workflows
  - stronger ablation on verification layers and threshold tuning

## Claim Discipline
- Safe claims:
  - unified architecture
  - four-layer verification model
  - cross-discipline consistency checks
  - reproducible synthetic benchmark package
  - explainable screening outputs
  - local KOSHA-grounded RAG support
  - optional on-premise local-LLM answer generation path on top of retrieved guidance
- Claims to avoid without more evidence:
  - production-ready full engineering design automation
  - full FFS replacement
  - full ISO or repair-package automation
  - general superiority over human experts

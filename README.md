# did-you-check-kosha

**[한국어 README](README_KR.md)**

> ASME standards: $hundreds per document.  
> API codes: $thousands per suite.  
> KOSHA regulatory corpus: free, public API, 18,576 provisions.  
>
> Nobody had put it in an engineering AI. Until now.

---

Yuyong Kim is an M.S. Data, Insights & Analytics candidate at the University of Wisconsin–Madison and a University of Wisconsin–Madison B.S. Chemical & Biological Engineering alumnus with 12+ years of professional experience in petrochemical EPC and process plant engineering. His current work centers on AI-enabled engineering verification, regulatory knowledge integration, and reproducible evaluation for safety-critical industrial systems.

---

## What is this?

A multi-discipline AI verification platform for Korean process plant engineering.

It runs seven engineering calculation engines (piping, vessel, rotating, electrical, instrumentation, steel, civil), validates them through a four-layer hybrid verification model, and then checks the results against **KOSHA's free public regulatory corpus** — 1,039 technical guidelines and 3,102 statutory provisions — using a local RAG layer.

The core finding: **international code calculations can fully pass while Korean PSM regulations flag a compliance obligation**. We call this the *jurisdiction compliance gap*. This system catches it automatically.

---

## Why it exists

I spent 12 years as a process engineering manager at a petrochemical company (including a $3.2B ethane cracker project in Louisiana). Every time I reviewed a discipline calculation, the same thing happened:

- The ASME or API number was fine.
- Nobody had checked the KOSHA requirement attached to that result.
- Because KOSHA guidelines are in Korean, buried in PDFs, behind a portal most engineers don't know exists.

ASME and API charge hundreds to thousands of dollars per document. KOSHA publishes everything free via public API. The problem was never access — it was integration. Nobody had built the bridge.

---

## What it does

**Seven domain calculation engines**

| Domain | Standards |
|---|---|
| Piping | ASME B31.3, API 570 |
| Pressure Vessels | ASME Section VIII Div.1, API 510, API 579-1 |
| Rotating Equipment | API 610, 617, 670 |
| Electrical | IEEE C57.104, 1584-2018 |
| Instrumentation | IEC 61511, ISA-TR84.00.02 |
| Structural Steel | AISC 360 |
| Civil / Concrete | ACI 318, 562 |

**Four-layer hybrid verification**

1. Input validation — blocks garbage before calculation
2. K-voting consensus — runs three numerically varied paths, flags disagreement
3. Physics and code compliance — enforces domain-specific red flags
4. Reverse verification — back-calculates inputs from outputs to check consistency

**KOSHA regulatory RAG**

- 18,576 indexed rows (guides + statutory provisions)
- Local SQLite FTS5 — no cloud, no API key, no cost
- Concept-aware synonym expansion for Korean/English bilingual retrieval
- On-premises Qwen via Ollama — your data stays on your machine

**Cross-domain coupling validator**

Ten predefined domain pairs checked for coupling hazards invisible to single-discipline calculations:
- Piping nozzle load → rotating equipment bearing stress
- Civil foundation settlement → rotating equipment alignment
- Electrical harmonic distortion → rotating equipment bearing temperature
- ...and seven more

---

## Show me the numbers

**220 golden cases — 220 passed**

```
piping:          accuracy=1.0000, red_flag_detection=1.0000
vessel:          accuracy=1.0000, red_flag_detection=1.0000
rotating:        accuracy=1.0000, red_flag_detection=1.0000
electrical:      accuracy=1.0000, red_flag_detection=1.0000
instrumentation: accuracy=1.0000, red_flag_detection=1.0000
steel:           accuracy=1.0000, red_flag_detection=1.0000
civil:           accuracy=1.0000, red_flag_detection=1.0000
```

**Cross-domain ablation — 60 scenarios**

```
Validator OFF: 0/60 blocked
Validator ON:  25/60 blocked  (+0.4167 blocking ratio)
Aligned boundary cases: 0.0 → 1.0
Aligned failure cases:  0.0 → 1.0
```

**KOSHA RAG retrieval — 50 curated queries**

```
                Plain FTS    Enhanced FTS    Delta
Recall@1        0.44         0.74            +0.30
Recall@3        0.74         0.86            +0.12
Recall@5        0.74         0.86            +0.12
MRR@10          0.5744       0.7933          +0.2189
```

**The compliance gap — 3 representative cases**

```
                Code-only detected    RAG detected    First hit rank
VES-GOLD-001    0                     1 (M-69-2012)        1
VES-GOLD-009    0                     1 (C-C-23-2026)      1
PIP-GOLD-047    0                     1 (Article 256)      1
```

In all three cases: ASME and API calculations passed with no red flags.  
In all three cases: KOSHA RAG identified a Korean-jurisdiction obligation the calculation missed.

---

## The paper

This system is documented in a peer-reviewed manuscript submitted to  
*Process Safety and Environmental Protection* (Elsevier, IF ~7).

> *A KOSHA Regulatory Knowledge-Grounded Multi-Discipline AI Verification Framework for Process Plant Engineering*  
> Yuyong Kim — University of Wisconsin–Madison  
> arXiv preprint: [link coming after submission]

Full manuscript: [`docs/publication/PAPER_EN_v2.md`](docs/publication/PAPER_EN_v2.md)

---

## Quick start

```powershell
# 1. Install dependencies
pip install -r submission_requirements.txt

# 2. Build KOSHA RAG index (~10 min, one-time)
python scripts/sync_kosha_corpus.py --force
python scripts/sync_kosha_guide_api.py --download
python scripts/parse_kosha_guide_pdfs.py
python scripts/kosha_rag_local.py build --rebuild

# 3. Run a query
python scripts/kosha_rag_local.py query "배관 부식 방지 법령 요건" --top-k 8 --generate

# 4. Run all benchmarks
python scripts/benchmark_all_runtime.py
python scripts/benchmark_cross_discipline_ablation.py
python scripts/benchmark_rag_retrieval.py
```

> Qwen runs locally via [Ollama](https://ollama.ai). No GPU required for retrieval.  
> For generation: `ollama pull qwen2.5:7b-instruct` (or your preferred Qwen variant).

---

## Repository structure

```
src/
  piping/ vessel/ rotating/ electrical/ instrumentation/ steel/ civil/
  verification/       ← 4-layer engine (engine.py, gates.py, maker.py, reverse_check.py)
  cross_discipline/   ← coupling validator (10 domain pairs)
  rag/                ← KOSHA RAG + synonym expansion
  orchestrator/       ← 7-discipline pipeline

datasets/
  golden_standards/   ← 220 synthetic test cases (committed, 316 KB)
  kosha/normalized/   ← law articles + retrieval corpus (committed)
  kosha_rag/          ← eval queries (committed); SQLite index excluded (133 MB, rebuild locally)

scripts/              ← benchmarks + corpus sync + RAG rebuild
docs/publication/     ← manuscript + code map + reviewer Q&A
config/               ← threshold profiles + law link overrides
tools/kosha-ingestion ← KOSHA API ingestion source
```

---

## License

**AGPL-3.0** — free for individuals, researchers, and open-source projects.

If you use this in a commercial product or service without open-sourcing your stack,  
you need a commercial license. Contact me via LinkedIn.

See [`LICENSE`](LICENSE) for full terms including KOSHA data usage notice.

---

## Author

**Yuyong Kim**  
University of Wisconsin–Madison  
M.S. Data, Insights & Analytics Candidate  
B.S. Chemical & Biological Engineering  
12+ years of professional experience in petrochemical EPC and process plant engineering

[linkedin.com/in/yuyongkim](https://www.linkedin.com/in/yuyongkim/)

# EPC Maintenance Frontend

Trust-centric 7-discipline engineering workbench built with Next.js.  
신뢰 중심 7개 공종 엔지니어링 워크벤치 프론트엔드입니다.

## Who This Is For / 누구를 위한 화면인가
- EN: Engineers who need fast integrity screening with traceable formulas, standards references, and action-oriented outputs.
- KR: 공식/기준/조치 권고를 한 화면에서 확인하며 빠르게 설비 건전성 판단을 내려야 하는 엔지니어를 위한 화면입니다.

## Quick Start (EN/KR)
```powershell
cd frontend
npm install
npm run dev
```

- EN: Open `http://localhost:3012`.
- KR: 브라우저에서 `http://localhost:3012` 접속.

Clean start (recommended when static asset mismatch is suspected):
```powershell
npm run dev:fresh
```

## KOSHA API Setup
1. Create local env file:
```powershell
cd frontend
Copy-Item .env.example .env.local
```
2. Fill service key values in `.env.local`:
- `KOSHA_API_KEY_ENCODING`
- `KOSHA_API_KEY_DECODING`
3. Optional endpoint overrides:
- `KOSHA_GUIDE_API_ENDPOINT` (default: `https://apis.data.go.kr/B552468/koshaguide`)
- `KOSHA_SMART_SEARCH_API_ENDPOINT` (default: `https://apis.data.go.kr/B552468/srch/smartSearch`)
4. Restart dev server after env changes.

## Local RAG Panel Setup
The right-side `Local KOSHA RAG` card calls Python local retrieval from the frontend API route (`/api/rag/query`).

1. Build local index once (project root):
```powershell
python scripts/kosha_rag_local.py build --rebuild
```
2. Ensure `.env.local` includes:
- `KOSHA_LOCAL_RAG_ENABLED=true`
- `KOSHA_RAG_PYTHON_BIN=python`
- `KOSHA_RAG_SCRIPT=../scripts/kosha_rag_local.py`
- `KOSHA_RAG_INDEX_PATH=../datasets/kosha_rag/kosha_local_rag.sqlite3`
3. Restart `npm run dev`.

Optional generation mode (Ollama):
- Set `KOSHA_RAG_GENERATE=true`
- Set `KOSHA_RAG_MODEL=<your-local-model>`

## Regulatory Fallback Strategy (No Portal Dependency)
- Runtime regulatory mapping is now **offline-first enriched**:
  - Try KOSHA API (when key/network available)
  - If empty/fail, enrich from local snapshots:
    - `datasets/kosha/normalized/law_articles.json`
    - `datasets/kosha_guide/normalized/guide_documents_text.json`
- Guide links can open from local dataset via:
  - `/api/kosha/guide-file/{guideNo}`
- This means law/guide panel is still populated even when external portal or API calls are unstable.

## KOSHA Module Map
- Orchestrator: `frontend/lib/kosha-regulatory.ts`
- Config/env: `frontend/lib/kosha/env.ts`
- API fetch layer: `frontend/lib/kosha/fetchers.ts`
- Query builder: `frontend/lib/kosha/queries.ts`
- Item mapping: `frontend/lib/kosha/mappers.ts`
- Compliance scoring: `frontend/lib/kosha/compliance.ts`
- Crosswalk mapping: `frontend/lib/kosha/crosswalk.ts`
- Constants/helpers/types: `frontend/lib/kosha/constants.ts`, `frontend/lib/kosha/helpers.ts`, `frontend/lib/kosha/types.ts`

This split keeps each file focused and prevents a single long service file from growing unbounded.

## ASME/API ↔ KR Regulatory Linking
- The right regulatory panel now renders `ASME/API reference -> KOSHA guide -> Korean legal basis` crosswalk items.
- Includes practical Korean links for:
  - `산업안전보건기준` search
  - `고압가스 안전관리법` search
  - KGS portal
- Rule-based mapping is extendable in one place: `frontend/lib/kosha/crosswalk.ts`.

## What You Are Calculating (All Disciplines) / 공종별로 실제 계산하는 것

### 1) Piping (`/piping`)
- EN: Calculates minimum required thickness from pressure/temperature/material basis, then estimates corrosion rate, remaining life, and inspection interval using thickness history.
- KR: 압력/온도/재질 기준으로 최소 필요두께를 계산하고, 두께 이력으로 부식률·잔여수명·점검주기를 산정합니다.
- Key outputs: `t_min_mm`, `cr_selected_mm_per_year`, `remaining_life_years`, `inspection_interval_years`
- Decision: Keep operating, shorten interval, or prepare replacement.

### 2) Vessel (`/vessel`)
- EN: Screens required shell thickness, external pressure utilization, and nozzle reinforcement adequacy, then estimates remaining life.
- KR: 쉘 필요두께, 외압 안정성 활용도, 노즐 보강 적정성을 스크리닝하고 잔여수명을 산정합니다.
- Key outputs: `t_required_shell_mm`, `external_pressure_utilization`, `nozzle_reinforcement_index`, `remaining_life_years`
- Decision: Continue service, reinforce/repair, or re-rate review.

### 3) Rotating (`/rotating`)
- EN: Uses machine type + driver type + service criticality to evaluate vibration limits, mechanical/process/protection indices, surge/NPSH/steam-state risks, and monitoring interval.
- KR: 기기타입 + 구동타입 + 중요도 기준으로 진동한계, 기계/공정/보호 인덱스, 서지/NPSH/증기상태 리스크와 점검주기를 평가합니다.
- Key outputs: `adjusted_vibration_limit_mm_per_s`, `mechanical_integrity_index`, `process_stability_index`, `protection_readiness_index`, `inspection_interval_years`
- Decision: Normal monitoring, increased monitoring, immediate intervention.

### 4) Electrical (`/electrical`)
- EN: Screens arc-flash incident energy, fault current vs breaker interrupt rating, and power quality indicators.
- KR: 아크플래시 에너지, 고장전류 대비 차단기 차단용량, 전력품질 지표를 스크리닝합니다.
- Key outputs: `arc_flash_energy_cal_cm2`, `fault_current_ka`, `breaker_interrupt_rating_ka`, `voltage_drop_percent`, `transformer_health_index`
- Decision: PPE/setting change/mitigation plan.

### 5) Instrumentation (`/instrumentation`)
- EN: Evaluates SIS performance (`PFDavg`, SIL achieved), drift trend, and optimal calibration interval.
- KR: SIS 성능(`PFDavg`, 달성 SIL), 드리프트 추세, 최적 교정주기를 평가합니다.
- Key outputs: `pfdavg`, `sil_achieved`, `predicted_drift_pct`, `calibration_interval_optimal_days`
- Decision: Maintain current interval, tighten proof/calibration plan, redesign loop.

### 6) Steel (`/steel`)
- EN: Computes demand-capacity ratio and stability indicators for steel member integrity screening.
- KR: 철골 부재 건전성 스크리닝을 위해 D/C 비와 안정성 지표를 계산합니다.
- Key outputs: `dc_ratio`, `lambda_c`, `phi_pn_kn`, `deflection_mm`
- Decision: Continue, strengthen, or urgent structural review.

### 7) Civil (`/civil`)
- EN: Screens concrete flexural capacity and durability progression (carbonation/corrosion initiation).
- KR: 콘크리트 휨내력과 내구성 열화(탄산화/부식 개시)를 스크리닝합니다.
- Key outputs: `dc_ratio`, `carbonation_depth_mm`, `years_to_corrosion_init`, `substantial_damage`
- Decision: Monitoring, repair planning, or immediate repair.

## Start Here for Process Engineers (PIP/VES/ROT) / 공정엔지니어 시작 가이드
- EN: If you are most familiar with piping, vessel, and rotating, start with these three routes first: `/piping`, `/vessel`, `/rotating`.
- KR: 배관/정기기/회전기기가 익숙하면 `/piping`, `/vessel`, `/rotating`부터 먼저 보시면 됩니다.

1. Run one preset and click `Run Calculation`.
2. Check `Calculation Summary` for key metrics.
3. Open `Calculation Trace` to see formula-level logic.
4. Confirm `AI Verification`, `Flags`, and `Recommendations` for release decision.

## How To Read The Screen / 화면 읽는 순서
- `Input`: Current case conditions (design basis + inspection/operation data)
- `Calculation Summary`: Final key metrics you decide with
- `Calculation Trace`: Step-by-step formula evidence
- `AI Verification`: 4-layer verification status
- `Standards References`: Traceable code/standard links and guidance
- `Flags + Recommendations`: What action is needed now

## Implemented MVP Features
- Beginner / Standard / Master mode switch (top bar + dashboard role quick-start)
- Beginner guided run card + simple/expert result interpretation toggle
- Time-series + threshold overlay and cross-discipline impact map card
- Master tools: parallel Scenario Lab (variable range points) + table/sort/filter/search/pagination/selection/bulk re-run/CSV export/re-run/detail view, robust CSV Batch Screening (max rows/concurrency/template/cancel/progress/filter/search table/selection/bulk re-run/CSV export/re-run/detail view + CSV file import), keyboard shortcuts(Ctrl/Cmd+Enter, Ctrl/Cmd+Shift+Enter), adjustable risk thresholds + error-group summary + risk heatmap + local setting persistence, summary copy-to-clipboard, Evidence Pack export (MD/JSON)
- Backend Ops panel in Master tools: queued job execution/polling, sensitivity API run, and collaboration note posting (backend mode).
- Backend Ops panel also supports persistence stats fetch and backend ZIP report package download.
- Backend Ops also supports WebSocket job status streaming (`/ws/jobs/{job_id}`) in backend mode.
- Backend Ops also supports recent jobs/audit refresh, retry latest job, and bulk cancel active jobs.
- Backend Ops also supports audit summary view and optional auto-refresh polling.
- Pagination/state handling is modularized with `hooks/usePagination.ts` and `components/workbench/pagination-controls.tsx`.
- Master Tools helpers/UI are modularized into:
  - `components/workbench/master-tools-utils.ts`
  - `components/workbench/backend-ops-panel.tsx`
- Local persistence state is modularized via `hooks/useLocalStorageState.ts`.
- 3-pane engineering workbench (Input / Results / Verification)
- Seven discipline routes with discipline-specific forms
- Seven discipline visual context packs (discipline-specific schematic + trend + condition cards)
- Dynamic mock calculation responses per discipline
- Real-time verification panel (4 layers, warnings, red flags)
- Standards reference panel and traceable calculation steps
- Run history by discipline with confidence, runtime, and flag counts
- Export current result to JSON and Markdown
- API mode switch in UI:
  - `mock`: local Next route `/api/calculate/[discipline]`
  - `backend`: external prefix + `/api/calculate/{discipline}`
- Mobile discipline switcher in the top bar

## Stack
- Next.js 14 + TypeScript
- Tailwind CSS + shadcn-style UI primitives
- React Hook Form + Zod
- Recharts
- Zustand

## Quality Checks
```powershell
npm run lint
npm run typecheck
npm run build
```

## Test Suite
```powershell
npm run test:unit
npm run test:e2e
npm run test:e2e:backend
npm run qa
```

`test:e2e:backend` verifies seven-discipline pages in `Backend (external)` mode against `http://localhost:8000`.

For repository-level full stack validation, run from project root:

```powershell
python scripts/run_quality_gate.py
```

Profiles:

```powershell
python scripts/run_quality_gate.py --profile fast
python scripts/run_quality_gate.py --profile strict
```

## Backend API Mode (Real Python Services)
1. Run API server from project root:
```powershell
python scripts/run_api_server.py
```
2. Open frontend and click `Settings` in top bar.
3. Set:
- `API Mode`: `Backend (external)`
- `Backend API Prefix`: `http://localhost:8000`
4. Run calculation and verify responses are served by Python backend.

## Available Routes
- `/piping`
- `/vessel`
- `/rotating`
- `/electrical`
- `/instrumentation`
- `/steel`
- `/civil`

## Notes
- API mode and backend prefix are managed in the top bar `Settings`.
- In `backend` mode, prefix is required (example: `http://localhost:8000`).
- Optional env bootstrap:
  - `NEXT_PUBLIC_BACKEND_API_PREFIX=http://localhost:8000`
- First production build may append `.next/types/**/*.ts` to `tsconfig.json` (Next.js default behavior).
- `npm run typecheck` is pinned to `tsconfig.typecheck.json`, so it does not depend on `.next` artifacts.

## Troubleshooting
- If dev server shows webpack runtime module errors after heavy refactors, reset build cache:
```powershell
cd frontend
Remove-Item -Recurse -Force .next,.next-dev -ErrorAction SilentlyContinue
npm run dev
```
- If the page renders as plain text (unstyled) and browser/network shows `/_next/static/*` 404:
```powershell
cd frontend
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force
Remove-Item -Recurse -Force .next,.next-dev -ErrorAction SilentlyContinue
npm run dev
```
  - then hard-refresh the browser (`Ctrl+F5`).
- Root cause note:
  - Running `next dev` and `next build/start` concurrently can corrupt shared build artifacts.
  - This project isolates outputs by config:
    - dev -> `.next-dev`
    - build/start -> `.next`
- If favicon route errors appear (example: `Cannot find module './xxx.js'` from `app/icon.svg/route.js`):
  - this project serves icons from `frontend/public/` (`/icon.svg`, `/apple-icon.svg`)
  - stop duplicate dev servers, clear `.next` and `.next-dev`, then restart `npm run dev`.

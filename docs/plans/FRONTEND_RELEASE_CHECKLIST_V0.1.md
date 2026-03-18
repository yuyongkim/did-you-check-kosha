# Frontend Release Checklist

Status: Passed  
Version: v0.1  
Validated On: 2026-02-27

## 1) Functional Scope
- [x] Seven discipline routes available and navigable
- [x] Three-pane workbench layout stable on desktop/mobile
- [x] Input forms trigger calculation flow and update result state
- [x] Verification panel, standards references, and flags visible after run
- [x] Run history and export actions (JSON/Markdown) operational
- [x] Mock mode and backend mode switch available from top bar settings

## 2) Backend Integration
- [x] Python API endpoint implemented: `POST /api/calculate/{discipline}`
- [x] Supported disciplines: piping, vessel, rotating, electrical, instrumentation, steel, civil
- [x] Frontend backend mode verified against API contract mapping
- [x] Health endpoint available: `GET /health`

## 3) Quality Gate Commands
Executed and passed:

```powershell
# frontend
npm run lint
npm run typecheck
npm run test:unit
npm run test:e2e
npm run qa

# backend
python -m unittest discover -s tests -p "test_*.py"
```

## 4) Accessibility and Performance Checks
- [x] Keyboard-driven smoke navigation validated in E2E workflow
- [x] E2E smoke tests pass for home/disciplines and piping run flow
- [x] Production build succeeds with all seven routes pre-rendered
- [x] Bundle summary reviewed from `next build` output

## 5) Operational Runbook
- [x] Frontend run guide updated (`frontend/README.md`)
- [x] Root run guide updated (`README.md`)
- [x] Python API server run command documented (`scripts/run_api_server.py`)
- [x] Revision history updated (`docs/revisions/CHANGELOG.md`)
- [x] Final completion record updated (`docs/revisions/DELIVERY_LOG.md`)

## 6) Release Decision
Release candidate approved for v0.1 frontend MVP.

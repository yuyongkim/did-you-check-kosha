# EXPANSION IMPLEMENTATION PLAN (2026-03-08)

## 목적
현재 확장된 Master Tools/Backend를 기반으로, **초심자 친화성 + 숙련자 생산성 + 운영 신뢰성**을 동시에 높이는 후속 확장 계획.

## 범위 (8개 트랙)

### 1) Beginner Mode (초심자 가이드)
- 기능: 단계형 온보딩, 용어 툴팁, 권장 프리셋, 실수 방지 경고
- 구현:
  - `frontend/components/workbench/beginner-onboarding.tsx`
  - `frontend/components/workbench/context-tooltips.tsx`
  - `useLocalStorageState`로 사용자 모드 저장
- 완료 기준: 신규 사용자가 5분 내 첫 배치 실행 가능

### 2) Expert Workspace (숙련자 고속 워크플로우)
- 기능: 단축키, 멀티선택 액션 바, 커맨드 팔레트
- 구현:
  - `frontend/components/workbench/command-palette.tsx`
  - bulk action 함수 `master-tools-utils.ts` 확장
- 완료 기준: 주요 작업 클릭 수 30% 이상 감소

### 3) Visual Analytics 강화
- 기능: Job 상태 타임라인, 실패 원인 히트맵, discipline별 성능 차트
- 구현:
  - `frontend/components/workbench/analytics-charts.tsx`
  - `GET /api/audit/summary` + 추가 통계 endpoint 연계
- 완료 기준: 운영 상태 대시보드 1화면 요약

### 4) Pagination/Filter 표준화
- 기능: 전 페이지 공통 pagination/filter/sort 상태 관리
- 구현:
  - `usePagination` + `useQueryState` 신규 훅
  - URL query sync 도입
- 완료 기준: 새 목록 화면 추가 시 1시간 내 일관 UX 구현

### 5) Queue Reliability (신뢰성)
- 기능: 지수 백오프 재시도, DLQ(실패 큐), idempotency key
- 구현:
  - `src/api/server.py` job lifecycle 확장
  - `src/api/persistence.py`에 retry metadata 저장
- 완료 기준: 일시 장애 시 수동 개입 없이 자동 복구율 향상

### 6) Collaboration 2.0
- 기능: 코멘트 스레드, 멘션, 승인 플로우 템플릿
- 구현:
  - `collab_events` 스키마 확장
  - `backend-ops-panel.tsx`에 협업 이벤트 타임라인
- 완료 기준: 리뷰-승인 히스토리 추적 가능

### 7) Report/Export 고도화
- 기능: ZIP 패키지 템플릿, PDF/CSV 다중 포맷, 스냅샷 버전 태깅
- 구현:
  - `POST /api/report/package` 옵션 확장
  - 프론트 Download Preset UI 추가
- 완료 기준: 보고서 생성 표준화 및 재현성 확보

### 8) Validation/Quality Gate 강화
- 기능: smoke + e2e + perf 기준선 자동화
- 구현:
  - `scripts/regression_api_smoke.py` CI 분리
  - `scripts/run_quality_gate.py`에 단계별 실패 기준 강화
- 완료 기준: PR 단계에서 회귀 자동 차단

---

## 단계별 실행 일정

### Phase A (1주): UX/구조 기반
- Track 1, 2, 4
- 산출물: Beginner/Expert 모드, 공통 pagination/filter 표준화

### Phase B (1~2주): 운영/시각화
- Track 3, 5
- 산출물: 실시간 시각화 대시보드, queue 신뢰성 강화

### Phase C (1주): 협업/리포트/검증
- Track 6, 7, 8
- 산출물: 협업 고도화, 리포트 표준 패키지, CI 품질 게이트

---

## 우선순위
1. Pagination 표준화 + Beginner Mode
2. Queue Reliability
3. Visual Analytics
4. Collaboration/Report 고도화
5. Quality Gate 심화

---

## 리스크 및 대응
- 환경 의존성(pip/uvicorn) 문제: CI 컨테이너 표준 이미지로 고정
- 기능 확장으로 복잡도 증가: 모듈 경계 강제(컴포넌트/훅/유틸 분리)
- 성능 저하 가능성: 대시보드 API pagination + 집계 캐시 도입

---

## 최종 판단 기준
- 초심자 첫 작업 성공률 증가
- 숙련자 작업 시간/클릭 수 감소
- 운영 장애 대응 시간 단축
- 회귀 테스트 자동 차단률 향상

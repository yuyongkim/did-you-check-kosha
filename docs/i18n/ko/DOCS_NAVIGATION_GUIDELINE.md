# 문서 탐색 가이드라인

상태: Draft  
버전: v0.1  
최종 수정일: 2026-03-01

## 1) 이 문서의 목적
이 가이드는 아래를 빠르게 판단하도록 설계되었습니다.
- 어떤 문서를 먼저 봐야 하는지
- 역할/작업별로 어떤 문서가 필수인지
- 보고서 제출 전에 무엇을 확인해야 하는지

이 문서는 탐색 지도이며, 상세 기술 기준은 각 스펙 원문 문서를 따릅니다.

## 2) 1분 경로 선택
아래에서 현재 목적을 먼저 고르십시오.

1. `이 시스템이 뭘 계산하는지 이해하고 싶다`
  - 먼저: `docs/i18n/ko/README.md` (또는 `.en.md`)
  - 다음: `docs/standards_index.md`, `docs/verification_layers.md`

2. `구현 전에 아키텍처/스펙을 확인하고 싶다`
  - 먼저: `docs/architecture_overview.md`
  - 다음: `docs/specs/README.md`
  - 다음: 해당 공종/프론트/검증 스펙

3. `QA/검증 후 릴리즈 승인 판단이 필요하다`
  - 먼저: `docs/specs/VERIFICATION_FRAMEWORK_SPEC_V0.1.md`
  - 다음: `docs/golden_dataset_spec.md`
  - 다음: `docs/plans/FRONTEND_RELEASE_CHECKLIST_V0.1.md`

4. `정식 엔지니어링 보고서를 제출해야 한다`
  - 먼저: `docs/i18n/ko/REPORT_SUBMISSION_TEMPLATE.md` (또는 `.en.md`)
  - 다음: 템플릿 필수 증빙 항목 수집

## 3) 역할별 권장 읽기 순서
### 3.1 공정 엔지니어 (배관/정기기/회전기기)
1. `docs/i18n/ko/README.md`
2. `docs/i18n/ko/standards_index.md`
3. `docs/i18n/ko/piping/NDE_RECOMMENDATIONS.md`
4. `docs/piping/USER_GUIDE.md`
5. 필요한 공종 스펙(`docs/specs/` 하위)

### 3.2 프론트엔드 엔지니어
1. `docs/plans/PROJECT_PLAN_V0.1.md`
2. `docs/specs/frontend/README.md`
3. `docs/specs/frontend/00_OVERVIEW_AND_ARCHITECTURE_V0.1.md`
4. `docs/specs/frontend/02_COMPONENT_SYSTEM_V0.1.md`
5. `docs/plans/FRONTEND_RELEASE_CHECKLIST_V0.1.md`

### 3.3 검증/QA 엔지니어
1. `docs/verification_layers.md`
2. `docs/specs/VERIFICATION_FRAMEWORK_SPEC_V0.1.md`
3. `docs/specs/verification/README.md`
4. `docs/golden_dataset_spec.md`
5. `docs/revisions/REVISION_POLICY.md`

### 3.4 리뷰어/매니저
1. `docs/i18n/ko/README.md` (또는 `.en.md`)
2. `docs/plans/PROJECT_PLAN_V0.1.md`
3. `docs/revisions/CHANGELOG.md`
4. `docs/revisions/DELIVERY_LOG.md`
5. `docs/REPORT_SUBMISSION_TEMPLATE.*` 기반 최신 제출물

## 4) 의사결정 게이트별 필수 문서
### Gate A: 작업 라운드 시작 전
필수:
- `docs/plans/PROJECT_PLAN_V0.1.md`
- 영향받는 스펙 문서(`docs/specs/`)

### Gate B: 구현 머지 전
필수:
- 관련 프론트/스펙 문서
- 검증 전략 문서
- 릴리즈 체크리스트 항목

### Gate C: 보고서 제출 전
필수:
- 완성된 보고서 템플릿
- 검증 증빙 자료
- 표준 참조 근거
- `CHANGELOG` / `DELIVERY_LOG` 갱신

## 5) 자주 발생하는 실수
- 계획서만 보고 스펙을 확인하지 않는 경우
- 예외 케이스에서 `*.ko.md` 요약본만 보고 판단하는 경우
- 아래 없이 보고서를 제출하는 경우:
  - 표준 참조
  - red/warning 플래그 처리 결과
  - 실행 증빙 명령 및 산출 경로
- `CHANGELOG` / `DELIVERY_LOG` 갱신 누락

## 6) 이중언어 운영 원칙
- 기술 기준 원본: `*.md`
- 언어 동반본:
  - `*.en.md`: 영어 동반본
  - `*.ko.md`: 한국어 동반본
- 전체 매핑:
  - `docs/BILINGUAL_INDEX.md`

## 7) 완료 전 체크리스트
1. 내 역할에 맞는 읽기 경로를 확인했다.
2. 영향 문서를 갱신했다.
3. `docs/REPORT_SUBMISSION_TEMPLATE.*`로 제출본을 작성했다.
4. 아래 이력 문서를 갱신했다.
   - `docs/revisions/CHANGELOG.md`
   - `docs/revisions/DELIVERY_LOG.md`

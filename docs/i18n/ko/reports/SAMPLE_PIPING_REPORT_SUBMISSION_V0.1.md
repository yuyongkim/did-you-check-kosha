# 샘플 엔지니어링 보고서 제출본 (배관)

상태: Draft  
버전: v0.1  
최종 수정일: 2026-03-01

이 문서는 `docs/i18n/ko/REPORT_SUBMISSION_TEMPLATE.md`를 실제로 채운 샘플입니다.
실제 제출 시에는 프로젝트 데이터와 증빙 경로로 모두 교체하십시오.

## 0) 제출 메타데이터
- 보고서 ID: `RPT-PIP-2026-03-001`
- 제출일: `2026-03-01`
- 프로젝트 / 유닛 / 구역: `EPC Demo / CDU-2 / Pipe Rack A`
- 공종: `piping`
- 작성자: `Process Integrity Team (Demo)`
- 검토자: `Senior Mechanical Engineer (Demo)`
- 승인 상태: `Review`

## 1) 요약 (Executive Summary)
- 본 보고서의 목적:
  - 배관 두께 건전성 스크리닝 결과를 평가하고 단기 검사 조치를 정의한다.
- 핵심 결론:
  - 현재 두께는 최소 요구 두께보다 높다.
  - 본 스크리닝 실행에서는 미해결 critical red flag가 확인되지 않았다.
  - 부식 추세는 존재하므로 hotspot 중심 모니터링 밀도를 높여야 한다.
- 운전 의사결정:
  - `continue_with_tightened_monitoring`

## 2) 범위 및 경계조건
- 대상 설비/태그:
  - `10\"-P-2045-CS-001`
  - `6\"-P-2045-CS-009`
- 데이터 기간:
  - 2015-01-01 ~ 2025-01-01
- 데이터 출처:
  - 설계 기준서(압력/온도/재질)
  - 주기 검사 UT 두께 이력
  - 공정 유체 분류 데이터
- 제외 범위:
  - 브랜치 접속부 응력 상세해석
  - API 579 정밀 레벨 평가
  - 보온 해체 후 CUI 캠페인 결과 연계

## 3) 입력 스냅샷 (추적 가능성)
첨부 또는 참조:
- 입력 payload 경로:
  - 예시: `outputs/sample/piping_input_2026-03-01.json`
- 폼 프리셋 / 모드:
  - preset: `General CS`
- backend 또는 mock 모드:
  - `mock`
- 선택한 standards/profile 옵션:
  - `ASME B31.3 Para 304.1.2`, `Table A-1`, `API 570 Section 7`
  - temperature profile: `strict_process`

주요 입력값:
- material: `SA-106 Gr.B`
- nps: `6`
- design_pressure_mpa: `4.5`
- design_temperature_c: `250`
- weld_type: `seamless`
- service_type: `general`
- fluid_type: `hydrocarbon_dry`
- chloride_ppm: `120`
- thickness_history:
  - 2015-01-01: 10.00 mm
  - 2020-01-01: 8.60 mm
  - 2025-01-01: 7.30 mm

## 4) 계산 및 검증 요약
### 4.1 핵심 지표 테이블
| 지표 | 값 | 단위 | 상태 | 비고 |
| --- | --- | --- | --- | --- |
| t_min | 5.10 | mm | pass | 최소 요구 두께 기준 |
| t_current | 7.30 | mm | pass | 현재 측정 두께 |
| corrosion_rate_selected | 0.340 | mm/y | monitor | 감육 추세 진행 |
| remaining_life | 6.20 | years | monitor | 여유 수명 존재 |
| inspection_interval | 3.00 | years | tighten | hotspot 타겟 캠페인 권장 |
| allowable_stress | 110.0 | MPa | pass | 설계온도 기준 테이블 조회 |
| temperature_limit_mode | within_conservative_limit | - | pass | 온도 초과 트리거 없음 |

### 4.2 검증 레이어 결과
| 레이어 | Pass/Fail | Critical 이슈 | Warning 이슈 | 증빙 |
| --- | --- | --- | --- | --- |
| L1 (입력/스키마) | Pass | 0 | 0 | payload schema 검증 로그 |
| L2 (물리/계산) | Pass | 0 | 1 | 계산 trace 및 추세 일관성 검토 |
| L3 (표준) | Pass | 0 | 0 | 조항 참조 점검 |
| L4 (정책/교차검증) | Pass | 0 | 0 | 릴리즈 규칙 스크린 |

### 4.3 Red Flag / Warning 처리 현황
- Red flags:
  - 본 샘플 케이스에서는 없음.
- Warnings:
  - code: `DATA.CORROSION_ALLOWANCE_DEFAULTED_1P5MM`
  - disposition: 샘플 실행에서 허용, 다음 정식 실행에서 CA 명시 입력
  - owner: piping integrity engineer
  - due date: 2026-03-15

## 5) 표준 및 수식 추적 근거
표준 참조:
- ASME B31.3 Para 304.1.2 (최소 두께 계산 맥락)
- ASME B31.3 Table A-1 (허용응력)
- API 570 Section 7 (검사주기/부식률 판단 맥락)

수식 추적 근거:
- UI `Calculation Trace` 패널
- 보조 문서:
  - `docs/standards_index.md`
  - `docs/specs/shared/MESSAGE_SCHEMA_AND_RED_FLAG_TAXONOMY_V0.1.md`

가정 및 보수적 기본값:
- 본 샘플은 corrosion allowance default 처리 케이스를 포함
- strict temperature profile 적용
- 스크리닝 결과이며 FFS 정밀평가를 대체하지 않음

## 6) 공학적 해석 및 조치 계획
### 6.1 기술 해석
- `t_current > t_min`이므로 본 스크리닝 기준 즉시 교체 사유는 아님.
- 부식 추세가 있으므로 엘보/리듀서/저점 등 국부 감육 hotspot 관리가 필요함.
- 신뢰도:
  - 스크리닝 의사결정에는 medium-high
  - 국부 손상 분포 판단은 UT 맵 확장 전까지 제한적

### 6.2 권장 조치
| 우선순위 | 조치 | 일정 | 담당 | 완료 기준 |
| --- | --- | --- | --- | --- |
| High | 위험 위치 UT CML 재점검 수행 | 1개월 이내 | Piping Integrity | 갱신 두께 이력 업로드 완료 |
| Medium | 엘보/리듀서 대상 PAUT/UT mapping 수행 | 3개월 이내 | NDE Team | hotspot 맵과 판정서 발행 |
| Low | 입력 거버넌스에서 CA 명시 입력 강제 | 1개월 이내 | Data Steward | 폼/payload에 CA 필수 반영 |

### 6.3 NDE / 검사 계획
- 추천 NDE 방법:
  - UT Thickness (CML grid)
  - PAUT / UT mapping (targeted)
  - MT at selected weld toe areas (as needed)
- 위치/CML/중점 구간:
  - control valve 하류
  - elbow intrados/extrados
  - low-point drain 인근
  - dead-leg branch
- 제안 검사 주기:
  - 3~6개월 내 타겟 후속 점검
  - 기본 주기는 유지하되 hotspot 캠페인을 병행
- 운전 차단 기준:
  - 측정 지점 두께가 `t_min` 이하인 경우
  - 신규 critical flag 발생 시 (`PHY.THICKNESS_BELOW_MINIMUM`, `PHY.REMAINING_LIFE_CRITICAL` 등)

## 7) 증빙 첨부 목록
필수 첨부:
- export JSON 결과:
  - `outputs/sample/piping_result_2026-03-01.json`
- export Markdown 요약:
  - `outputs/sample/piping_summary_2026-03-01.md`
- 화면/차트 캡처:
  - pipe cross-section
  - `t_min` 기준선 포함 trend chart
  - NDE recommendation panel
- 실행 로그:
  - `npm --prefix frontend run dev`
  - UI 실행: piping preset `General CS`
- 이력 문서 증빙:
  - `docs/revisions/CHANGELOG.md`
  - `docs/revisions/DELIVERY_LOG.md`

체크리스트:
- [x] JSON 첨부
- [x] Markdown 첨부
- [x] Flag 처리 내용 포함
- [x] 표준 참조 포함
- [x] 조치 담당/일정 지정
- [x] Revision 로그 갱신

## 8) 최종 승인
- 기술 검토자: `Pending`
- 운전 검토자: `Pending`
- QA/컴플라이언스 검토자: `Pending`
- 최종 결정: `Pending review completion`
- 운전 전 조건:
  - hotspot UT mapping 완료
  - CA 명시 입력 warning 항목 종료


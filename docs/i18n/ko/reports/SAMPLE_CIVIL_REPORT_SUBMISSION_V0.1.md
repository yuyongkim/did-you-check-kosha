# 샘플 엔지니어링 보고서 제출본 (토목/콘크리트)

상태: Draft  
버전: v0.1  
최종 수정일: 2026-03-01

## 0) 제출 메타데이터
- 보고서 ID: `RPT-CIV-2026-03-001`
- 제출일: `2026-03-01`
- 프로젝트 / 유닛 / 구역: `EPC Demo / Pipe Support Foundation / Zone-C`
- 공종: `civil`
- 작성자: `Civil Integrity Team (Demo)`
- 검토자: `Senior Civil Engineer (Demo)`
- 승인 상태: `Review`

## 1) 요약
- 목적:
  - 휨 D/C와 내구성 열화 지표를 스크리닝한다.
- 핵심 결론:
  - 휨 D/C는 1.0 미만.
  - substantial damage 트리거 없음.
  - carbonation depth는 피복두께 이내.
- 운전 의사결정:
  - `continue`

## 2) 범위 및 경계조건
- 대상:
  - `FDN-C-14`
- 데이터 범위:
  - 최신 검사 캠페인 스냅샷
- 데이터 출처:
  - 재료/단면 입력값
  - 균열/박락/침하 관찰치
  - 탄산화 계수 및 사용연수
- 제외 범위:
  - 지반 정밀 재평가
  - 보강 상세설계

## 3) 입력 스냅샷
- input payload: `outputs/sample/civil_input_2026-03-01.json`
- preset: `Beam Normal`
- mode: `mock`
- standards: `ACI 318`, `ACI 562`

주요 입력값:
- element_type: `beam`
- environment_exposure: `outdoor_urban`
- fc_mpa: `35`
- fy_mpa: `420`
- demand_moment_knm: `280`
- service_years: `18`
- cover_thickness_mm: `40`
- crack_width_mm: `0.22`
- spalling_area_percent: `5`
- foundation_settlement_mm: `8`

## 4) 계산 및 검증 요약
### 4.1 핵심 지표
| 지표 | 값 | 단위 | 상태 | 비고 |
| --- | --- | --- | --- | --- |
| dc_ratio | 0.78 | - | pass | 휨 수요/용량 양호 |
| carbonation_depth | 9.5 | mm | pass | 피복두께 미만 |
| years_to_corrosion_init | 34 | years | pass | 내구성 여유 |
| substantial_damage | false | boolean | pass | ACI 562 트리거 없음 |
| inspection_interval | 2.0 | years | pass | 기본 주기 |
| crack_width | 0.22 | mm | pass | 고위험 기준 미달 |

### 4.2 검증 레이어 결과
| 레이어 | Pass/Fail | Critical | Warning | 증빙 |
| --- | --- | --- | --- | --- |
| L1 | Pass | 0 | 0 | 스키마 검증 |
| L2 | Pass | 0 | 0 | D/C 및 내구성 계산 |
| L3 | Pass | 0 | 0 | ACI 참조 매핑 |
| L4 | Pass | 0 | 0 | 정책 스크린 |

### 4.3 플래그 처리
- Red flags: 없음
- Warnings: 없음

## 5) 표준/수식 추적
- ACI 318
- ACI 562
- UI `Calculation Trace` (civil)

## 6) 해석 및 조치
- 해석:
  - 구조 및 내구성 스크린 모두 허용 범위.
- 조치:
  - 정기 모니터링 유지.
  - 균열/박락/침하 추세 악화 시 조기 재평가.

## 7) 첨부 증빙
- `outputs/sample/civil_result_2026-03-01.json`
- `outputs/sample/civil_summary_2026-03-01.md`
- 토목 패널 캡처(지표 카드 + 추세)

## 8) 최종 승인
- 기술 검토: `Pending`
- 운전 검토: `Pending`
- QA 검토: `Pending`
- 최종 결정: `Pending review completion`

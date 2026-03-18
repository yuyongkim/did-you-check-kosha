# 샘플 엔지니어링 보고서 제출본 (정기기)

상태: Draft  
버전: v0.1  
최종 수정일: 2026-03-01

## 0) 제출 메타데이터
- 보고서 ID: `RPT-VES-2026-03-001`
- 제출일: `2026-03-01`
- 프로젝트 / 유닛 / 구역: `EPC Demo / HCU / Separator Area`
- 공종: `vessel`
- 작성자: `Static Equipment Team (Demo)`
- 검토자: `Lead Mechanical Engineer (Demo)`
- 승인 상태: `Review`

## 1) 요약
- 목적:
  - 쉘 두께 건전성, 외압 여유, 노즐 보강 적정성을 스크리닝한다.
- 핵심 결론:
  - 요구 쉘 두께 대비 현재 두께 여유가 충분하다.
  - 본 샘플 실행에서 critical red flag는 없다.
  - 정기 모니터링 유지 + 다음 주기 노즐 주변 확인 권장.
- 운전 의사결정:
  - `continue`

## 2) 범위 및 경계조건
- 대상 설비:
  - `V-2045`
- 데이터 범위:
  - 2026년 1분기 스냅샷
- 데이터 출처:
  - 설계 압력/온도 기준
  - 운전중 두께 측정값
  - 형상/노즐/패드 치수
- 제외 범위:
  - 피로/파괴역학 상세평가
  - 외압 차트법 정식 계산 패키지

## 3) 입력 스냅샷
- input payload: `outputs/sample/vessel_input_2026-03-01.json`
- preset: `Horizontal Drum`
- mode: `mock`
- standards: `ASME VIII UG-27`, `UG-28`, `UG-37`, `API 510`

주요 입력값:
- material: `SA-516-70`
- vessel_type: `horizontal_drum`
- design_pressure_mpa: `2.0`
- design_temperature_c: `200`
- inside_radius_mm: `750`
- shell_length_mm: `3000`
- nozzle_od_mm: `350`
- external_pressure_mpa: `0.25`
- t_current_mm: `18`

## 4) 계산 및 검증 요약
### 4.1 핵심 지표
| 지표 | 값 | 단위 | 상태 | 비고 |
| --- | --- | --- | --- | --- |
| t_required_shell | 11.20 | mm | pass | UG-27 기반 |
| thickness_margin | 6.80 | mm | pass | 현재-요구 두께 |
| remaining_life | 8.70 | years | pass | 양의 수명 여유 |
| inspection_interval | 4.00 | years | pass | 정기 주기 |
| external_pressure_utilization | 0.62 | - | pass | 스크린 기준 이내 |
| nozzle_reinforcement_index | 1.12 | - | pass | 1.0 이상 |
| slenderness_ld_ratio | 2.00 | - | pass | L/D 이상 없음 |

### 4.2 검증 레이어 결과
| 레이어 | Pass/Fail | Critical | Warning | 증빙 |
| --- | --- | --- | --- | --- |
| L1 | Pass | 0 | 0 | 스키마 검증 로그 |
| L2 | Pass | 0 | 0 | 두께/RL 계산 근거 |
| L3 | Pass | 0 | 0 | UG/API 참조 매핑 |
| L4 | Pass | 0 | 0 | 정책 스크린 |

### 4.3 플래그 처리
- Red flags: 없음
- Warnings: 없음

## 5) 표준/수식 추적
- ASME VIII UG-27, UG-28, UG-37
- API 510
- UI `Calculation Trace` (vessel)

## 6) 해석 및 조치
- 해석:
  - 현재 가정에서 쉘/외압/노즐 지표 모두 스크린 허용 범위.
- 조치:
  - 다음 정지 시 노즐 주변 국부 UT 확인.
  - 표준 주기 유지 + 부식 추세 모니터링.

## 7) 첨부 증빙
- `outputs/sample/vessel_result_2026-03-01.json`
- `outputs/sample/vessel_summary_2026-03-01.md`
- vessel 화면 캡처(도면/추세/마진 카드)

## 8) 최종 승인
- 기술 검토: `Pending`
- 운전 검토: `Pending`
- QA 검토: `Pending`
- 최종 결정: `Pending review completion`

# 샘플 엔지니어링 보고서 제출본 (회전기기)

상태: Draft  
버전: v0.1  
최종 수정일: 2026-03-01

## 0) 제출 메타데이터
- 보고서 ID: `RPT-ROT-2026-03-001`
- 제출일: `2026-03-01`
- 프로젝트 / 유닛 / 구역: `EPC Demo / Utilities / Pump House`
- 공종: `rotating`
- 작성자: `Rotating Reliability Team (Demo)`
- 검토자: `Principal Rotating Engineer (Demo)`
- 승인 상태: `Review`

## 1) 요약
- 목적:
  - 진동/공정 안정성/보호계통 준비도를 스크리닝한다.
- 핵심 결론:
  - 진동 및 노즐하중은 조정 한계 이내.
  - API 670 커버리지와 trip test 실적이 충분.
  - critical red flag 없음.
- 운전 의사결정:
  - `continue`

## 2) 범위 및 경계조건
- 대상 설비:
  - `P-3301A`
- 데이터 범위:
  - 최신 월간 상태 스냅샷
- 데이터 출처:
  - 상태감시 데이터
  - 압력/속도 운전값
  - 보호계통 커버리지 및 trip test 기록
- 제외 범위:
  - 로터다이나믹 상세해석
  - 고장원인 상세 분석

## 3) 입력 스냅샷
- input payload: `outputs/sample/rotating_input_2026-03-01.json`
- preset: `Pump Normal`
- mode: `mock`
- standards: `API 610`, `API 670`, `ISO 20816-3`

주요 입력값:
- machine_type: `pump`
- driver_type: `electric_motor_fixed`
- service_criticality: `normal`
- vibration_mm_per_s: `2.5`
- nozzle_load_ratio: `0.85`
- speed_rpm: `1800`
- npsh_available_m: `5.6`
- npsh_required_m: `3.8`
- api670_coverage_pct: `96`
- trip_tests_last_12m: `4`

## 4) 계산 및 검증 요약
### 4.1 핵심 지표
| 지표 | 값 | 단위 | 상태 | 비고 |
| --- | --- | --- | --- | --- |
| vibration | 2.50 | mm/s | pass | 조정 한계 미만 |
| adjusted_vibration_limit | 3.00 | mm/s | pass | 기종/구동/중요도 반영 |
| nozzle_load_ratio | 0.85 | - | pass | 허용 1.0 이내 |
| mechanical_integrity_index | 8.5 | /10 | pass | 양호 |
| process_stability_index | 8.9 | /10 | pass | 안정 |
| protection_readiness_index | 8.8 | /10 | pass | 충분 |
| inspection_interval | 2.0 | years | pass | 기본 주기 |

### 4.2 검증 레이어 결과
| 레이어 | Pass/Fail | Critical | Warning | 증빙 |
| --- | --- | --- | --- | --- |
| L1 | Pass | 0 | 0 | 입력 스키마 검증 |
| L2 | Pass | 0 | 0 | 지표/한계 계산 근거 |
| L3 | Pass | 0 | 0 | API/ISO 매핑 |
| L4 | Pass | 0 | 0 | 정책 스크린 |

### 4.3 플래그 처리
- Red flags: 없음
- Warnings: 없음

## 5) 표준/수식 추적
- API 610
- API 670
- ISO 20816-3
- UI `Calculation Trace` (rotating)

## 6) 해석 및 조치
- 해석:
  - 기계/공정/보호 3축 모두 허용 범위.
  - NPSH margin 양수로 캐비테이션 스크린 경고 없음.
- 조치:
  - 기본 모니터링 주기 유지.
  - trip test 및 bypass 관리 지속.

## 7) 첨부 증빙
- `outputs/sample/rotating_result_2026-03-01.json`
- `outputs/sample/rotating_summary_2026-03-01.md`
- 회전기기 패널 캡처(스펙트럼/매트릭스/리스크 카드)

## 8) 최종 승인
- 기술 검토: `Pending`
- 운전 검토: `Pending`
- QA 검토: `Pending`
- 최종 결정: `Pending review completion`

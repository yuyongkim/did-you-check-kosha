# 샘플 엔지니어링 보고서 제출본 (전기)

상태: Draft  
버전: v0.1  
최종 수정일: 2026-03-01

## 0) 제출 메타데이터
- 보고서 ID: `RPT-ELE-2026-03-001`
- 제출일: `2026-03-01`
- 프로젝트 / 유닛 / 구역: `EPC Demo / Substation S-13.8kV / Switch Room`
- 공종: `electrical`
- 작성자: `Electrical Reliability Team (Demo)`
- 검토자: `Lead Electrical Engineer (Demo)`
- 승인 상태: `Review`

## 1) 요약
- 목적:
  - 변압기 건강지수, 아크플래시, 고장전류 여유, 전력품질을 스크리닝한다.
- 핵심 결론:
  - 건강지수는 허용 범위.
  - 고장전류는 차단기 정격 이내.
  - 아크플래시 에너지는 작업계획/PPE 관리가 필요한 수준.
- 운전 의사결정:
  - `continue_with_tightened_monitoring`

## 2) 범위 및 경계조건
- 대상 설비:
  - `TR-13A`, `SWGR-13.8-01`
- 데이터 범위:
  - 최신 분기 스냅샷
- 데이터 출처:
  - 단락전류 데이터
  - 차단기 정격/보호 설정
  - DGA/절연/오일 상태 점수
- 제외 범위:
  - 보호협조 정식 재계산
  - 고조파 발생원 상세 추적

## 3) 입력 스냅샷
- input payload: `outputs/sample/electrical_input_2026-03-01.json`
- preset: `Transformer Normal`
- mode: `mock`
- standards: `IEEE C57.104`, `IEEE 1584-2018`, `NFPA 70E`

주요 입력값:
- system_voltage_kv: `13.8`
- bolted_fault_current_ka: `22`
- breaker_interrupt_rating_ka: `31.5`
- arc 관련: clearing `0.2s`, distance `455mm`
- voltage_drop_percent: `3.2`
- thd_voltage_percent: `4.8`

## 4) 계산 및 검증 요약
### 4.1 핵심 지표
| 지표 | 값 | 단위 | 상태 | 비고 |
| --- | --- | --- | --- | --- |
| transformer_health_index | 7.8 | /10 | pass | 양호 |
| arc_flash_energy | 11.5 | cal/cm2 | monitor | PPE/작업통제 필요 |
| ppe_category | 3 | category | monitor | 스크린 기준 |
| fault_current | 22.0 | kA | pass | 차단기 정격 이내 |
| breaker_interrupt_rating | 31.5 | kA | pass | 여유 존재 |
| voltage_drop | 3.2 | % | pass | high-alert 미해당 |
| inspection_interval | 2.0 | years | pass | 기본 주기 |

### 4.2 검증 레이어 결과
| 레이어 | Pass/Fail | Critical | Warning | 증빙 |
| --- | --- | --- | --- | --- |
| L1 | Pass | 0 | 0 | 스키마 검증 |
| L2 | Pass | 0 | 0 | HI/arc/fault 계산 |
| L3 | Pass | 0 | 0 | IEEE/NFPA 매핑 |
| L4 | Pass | 0 | 0 | 정책 스크린 |

### 4.3 플래그 처리
- Red flags: 없음
- Warnings: 없음

## 5) 표준/수식 추적
- IEEE C57.104
- IEEE 1584-2018
- NFPA 70E
- UI `Calculation Trace` (electrical)

## 6) 해석 및 조치
- 해석:
  - 차단기 차단용량 관점의 즉시 위험은 없음.
  - 아크플래시 수준은 관리 필요.
- 조치:
  - PPE/작업허가 통제 유지.
  - 고조파/건강지수 추세 점검 유지.

## 7) 첨부 증빙
- `outputs/sample/electrical_result_2026-03-01.json`
- `outputs/sample/electrical_summary_2026-03-01.md`
- 전기 패널 캡처(아크/HI/품질 차트)

## 8) 최종 승인
- 기술 검토: `Pending`
- 운전 검토: `Pending`
- QA 검토: `Pending`
- 최종 결정: `Pending review completion`

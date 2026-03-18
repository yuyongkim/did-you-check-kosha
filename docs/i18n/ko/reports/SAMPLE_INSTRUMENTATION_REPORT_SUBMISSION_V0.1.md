# 샘플 엔지니어링 보고서 제출본 (계장)

상태: Draft  
버전: v0.1  
최종 수정일: 2026-03-01

## 0) 제출 메타데이터
- 보고서 ID: `RPT-INS-2026-03-001`
- 제출일: `2026-03-01`
- 프로젝트 / 유닛 / 구역: `EPC Demo / Reactor Train / SIS Loop B`
- 공종: `instrumentation`
- 작성자: `I&C Integrity Team (Demo)`
- 검토자: `Senior SIS Engineer (Demo)`
- 승인 상태: `Review`

## 1) 요약
- 목적:
  - SIL 목표 충족, 드리프트 추세, 보정주기 적정성을 스크리닝한다.
- 핵심 결론:
  - 샘플에서 달성 SIL은 목표 SIL보다 높다.
  - 예측 드리프트는 허용오차 이내.
  - 현재 보정주기는 추세 관점에서 유지 가능.
- 운전 의사결정:
  - `continue`

## 2) 범위 및 경계조건
- 대상:
  - `PT-4402` / `SIF-B-102`
- 데이터 범위:
  - 보정 이력 0~270일 구간
- 데이터 출처:
  - calibration history
  - failure rate/proof interval/MTTR
  - voting architecture와 target SIL
- 제외 범위:
  - SRS 재설계
  - 상세 배선 진단

## 3) 입력 스냅샷
- input payload: `outputs/sample/instrumentation_input_2026-03-01.json`
- preset: `PT Normal`
- mode: `mock`
- standards: `IEC 61511`, `ISA-TR84.00.02`, `ISO GUM`

주요 입력값:
- instrument_type: `pressure_transmitter`
- voting_architecture: `1oo1`
- sil_target: `2`
- failure_rate_per_hour: `1.0e-7`
- proof_test_interval_hours: `8760`
- mttr_hours: `8`
- calibration_interval_days: `180`
- tolerance_pct: `1.0`

## 4) 계산 및 검증 요약
### 4.1 핵심 지표
| 지표 | 값 | 단위 | 상태 | 비고 |
| --- | --- | --- | --- | --- |
| pfdavg | 0.00044 | - | pass | SIL2 한계 이내 |
| sil_target | 2 | level | pass | 목표 |
| sil_achieved | 3 | level | pass | 목표 초과 달성 |
| predicted_drift | 0.38 | % | pass | 허용오차 이내 |
| calibration_interval_optimal | 220 | days | pass | 현 주기와 유사 |
| combined_uncertainty | 0.37 | % | pass | 허용 범위 |

### 4.2 검증 레이어 결과
| 레이어 | Pass/Fail | Critical | Warning | 증빙 |
| --- | --- | --- | --- | --- |
| L1 | Pass | 0 | 0 | 스키마 검증 |
| L2 | Pass | 0 | 0 | pfd/drift 계산 |
| L3 | Pass | 0 | 0 | IEC/ISA 매핑 |
| L4 | Pass | 0 | 0 | 정책 스크린 |

### 4.3 플래그 처리
- Red flags: 없음
- Warnings: 없음

## 5) 표준/수식 추적
- IEC 61511
- ISA-TR84.00.02
- ISO GUM
- UI `Calculation Trace` (instrumentation)

## 6) 해석 및 조치
- 해석:
  - SIL과 드리프트 모두 현재는 허용 범위.
- 조치:
  - 현 주기 유지, 드리프트 회귀 품질(R2) 지속 추적.
  - 추세 급변 시 즉시 재평가.

## 7) 첨부 증빙
- `outputs/sample/instrumentation_result_2026-03-01.json`
- `outputs/sample/instrumentation_summary_2026-03-01.md`
- 계장 패널 캡처(드리프트 추세 + SIL 카드)

## 8) 최종 승인
- 기술 검토: `Pending`
- 운전 검토: `Pending`
- QA 검토: `Pending`
- 최종 결정: `Pending review completion`

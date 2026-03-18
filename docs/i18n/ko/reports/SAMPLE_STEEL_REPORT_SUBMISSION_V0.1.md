# 샘플 엔지니어링 보고서 제출본 (철골)

상태: Draft  
버전: v0.1  
최종 수정일: 2026-03-01

## 0) 제출 메타데이터
- 보고서 ID: `RPT-STL-2026-03-001`
- 제출일: `2026-03-01`
- 프로젝트 / 유닛 / 구역: `EPC Demo / Pipe Rack / Bay-3`
- 공종: `steel`
- 작성자: `Structural Integrity Team (Demo)`
- 검토자: `Lead Structural Engineer (Demo)`
- 승인 상태: `Review`

## 1) 요약
- 목적:
  - D/C 비율, 단면손실, 처짐 지표를 스크리닝한다.
- 핵심 결론:
  - D/C는 1.0 미만으로 여유가 있다.
  - 단면 손실은 중간 이하 수준.
  - critical 구조 플래그 없음.
- 운전 의사결정:
  - `continue`

## 2) 범위 및 경계조건
- 대상:
  - `PR-B3-COL-07`
- 데이터 범위:
  - 최신 검사 스냅샷
- 데이터 출처:
  - 부재 형상/강종
  - 하중조합 결과 수요값
  - 부식/처짐 현장 관찰값
- 제외 범위:
  - 비선형 골조 해석
  - 접합부 재설계 패키지

## 3) 입력 스냅샷
- input payload: `outputs/sample/steel_input_2026-03-01.json`
- preset: `Column Normal`
- mode: `mock`
- standards: `AISC 360 Chapter E`

주요 입력값:
- member_type: `column`
- steel_grade: `a572_gr50`
- section_label: `W310x60`
- axial_demand_kn: `650`
- corrosion_loss_percent: `8`
- deflection_mm: `10`
- span_mm: `6000`

## 4) 계산 및 검증 요약
### 4.1 핵심 지표
| 지표 | 값 | 단위 | 상태 | 비고 |
| --- | --- | --- | --- | --- |
| dc_ratio | 0.82 | - | pass | 1.0 미만 |
| lambda_c | 0.72 | - | pass | 압축 안정 영역 |
| phi_pn | 790 | kN | pass | 수요 대비 용량 여유 |
| corrosion_loss | 8.0 | % | pass | 중간 이하 손실 |
| deflection_ratio | 0.45 | - | pass | 처짐 기준 이내 |
| inspection_interval | 2.0 | years | pass | 기본 주기 |

### 4.2 검증 레이어 결과
| 레이어 | Pass/Fail | Critical | Warning | 증빙 |
| --- | --- | --- | --- | --- |
| L1 | Pass | 0 | 0 | 스키마 검증 |
| L2 | Pass | 0 | 0 | 용량/처짐 계산 |
| L3 | Pass | 0 | 0 | AISC 참조 매핑 |
| L4 | Pass | 0 | 0 | 정책 스크린 |

### 4.3 플래그 처리
- Red flags: 없음
- Warnings: 없음

## 5) 표준/수식 추적
- AISC 360 Chapter E
- UI `Calculation Trace` (steel)

## 6) 해석 및 조치
- 해석:
  - 샘플 기준 과응력 신호 없음.
  - 부식/처짐 지표는 현재 관리 가능 범위.
- 조치:
  - 현 주기 유지.
  - 하중 변경 또는 단면손실 증가 시 즉시 재스크린.

## 7) 첨부 증빙
- `outputs/sample/steel_result_2026-03-01.json`
- `outputs/sample/steel_summary_2026-03-01.md`
- 철골 패널 캡처(도식 + D/C 카드)

## 8) 최종 승인
- 기술 검토: `Pending`
- 운전 검토: `Pending`
- QA 검토: `Pending`
- 최종 결정: `Pending review completion`

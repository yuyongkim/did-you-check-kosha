# 엔지니어링 보고서 제출 템플릿

상태: Draft  
버전: v0.1  
최종 수정일: 2026-03-01

## 0) 제출 메타데이터
- 보고서 ID:
- 제출일:
- 프로젝트 / 유닛 / 구역:
- 공종:
- 작성자:
- 검토자:
- 승인 상태: `Draft` / `Review` / `Approved`

## 1) 요약 (Executive Summary)
- 본 보고서의 목적:
- 핵심 결론 (1~3줄):
- 운전 의사결정:
  - `continue`
  - `continue_with_tightened_monitoring`
  - `repair_or_replace_review_required`
  - `blocked_pending_action`

## 2) 범위 및 경계조건
- 대상 설비/태그:
- 데이터 기간:
- 데이터 출처:
  - 설계 기준
  - 검사 이력
  - 운전 조건 스냅샷
- 제외 범위:

## 3) 입력 스냅샷 (추적 가능성)
첨부 또는 참조:
- 입력 payload 경로:
- 폼 프리셋 / 모드:
- backend 또는 mock 모드:
- 선택한 standards/profile 옵션:

공종별 필수 입력 항목은 명시적으로 기록하십시오.

## 4) 계산 및 검증 요약
### 4.1 핵심 지표 테이블
| 지표 | 값 | 단위 | 상태 | 비고 |
| --- | --- | --- | --- | --- |
| t_min |  | mm |  |  |
| t_current |  | mm |  |  |
| corrosion_rate_selected |  | mm/y |  |  |
| remaining_life |  | years |  |  |
| inspection_interval |  | years |  |  |

필요 시 공종 전용 지표를 추가하십시오.

### 4.2 검증 레이어 결과
| 레이어 | Pass/Fail | Critical 이슈 | Warning 이슈 | 증빙 |
| --- | --- | --- | --- | --- |
| L1 |  |  |  |  |
| L2 |  |  |  |  |
| L3 |  |  |  |  |
| L4 |  |  |  |  |

### 4.3 Red Flag / Warning 처리 현황
각 플래그에 대해 처리 내용을 작성:
- Red flags:
  - code:
  - disposition:
  - owner:
  - due date:
- Warnings:
  - code:
  - disposition:
  - owner:
  - due date:

## 5) 표준 및 수식 추적 근거
정확한 문서/조항을 기록:
- Standard references:
  - ASME/API/IEC/IEEE 조항:
  - 사내 절차:
- Formula trace source:
  - UI Trace 섹션 또는 파일 경로:
- 사용한 가정 및 보수적 기본값:

## 6) 공학적 해석 및 조치 계획
### 6.1 기술 해석
- 수치의 물리적 의미:
- 열화 메커니즘 가설:
- 신뢰도 및 불확실성:

### 6.2 권장 조치
| 우선순위 | 조치 | 일정 | 담당 | 완료 기준 |
| --- | --- | --- | --- | --- |
| High |  |  |  |  |
| Medium |  |  |  |  |
| Low |  |  |  |  |

### 6.3 NDE / 검사 계획 (해당 시)
- 추천 NDE 방법:
- 위치/CML/중점 구간:
- 제안 검사 주기:
- 운전 차단 기준:

## 7) 증빙 첨부 목록
필수 첨부:
- export JSON 결과
- export Markdown 요약
- 해석에 사용한 화면/차트 캡처
- 실행 명령 로그 (결과 생성 방법)
- 이력 문서 증빙:
  - `docs/revisions/CHANGELOG.md` 항목
  - `docs/revisions/DELIVERY_LOG.md` 항목

체크리스트:
- [ ] JSON 첨부
- [ ] Markdown 첨부
- [ ] Flag 처리 내용 포함
- [ ] 표준 참조 포함
- [ ] 조치 담당/일정 지정
- [ ] Revision 로그 갱신

## 8) 최종 승인
- 기술 검토자:
- 운전 검토자:
- QA/컴플라이언스 검토자:
- 최종 결정:
- 운전 전 조건:

## 9) 빠른 작성 예시 (배관)
- Decision: `continue_with_tightened_monitoring`
- 근거:
  - `t_current`는 `t_min`보다 높으나, 부식 추세가 평탄하지 않음
  - 미해결 critical red flag 없음
  - warning 항목은 담당자/기한 지정 완료
- 조치:
  - 다음 정지 기간에 엘보/리듀서 UT mapping 수행
  - 3~6개월 내 두께 그리드 재측정

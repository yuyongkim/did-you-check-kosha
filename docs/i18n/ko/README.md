# EPC Maintenance AI 사용자 가이드 (한국어)

## 1. 문서 범위
이 시스템은 다음 7개 공종의 무결성 스크리닝 워크벤치입니다.
- 배관
- 정기기(압력용기/고정설비)
- 회전기기
- 전기
- 계장
- 철골
- 토목/콘크리트

목표는 계산 근거, 표준 참조, 경고 플래그, 추천 조치를 한 화면에서 빠르게 확인하는 것입니다.

## 2. 빠른 시작
```powershell
cd frontend
npm install
npm run dev
```

브라우저에서 `http://localhost:3000` 접속.

## 3. 공정 엔지니어 관점에서 무엇을 계산하는가
### 3.1 배관 (`/piping`)
- 목적: 두께 건전성 스크리닝과 검사 주기 설정.
- 핵심 지표:
  - `t_min_mm`: 최소 요구 두께
  - `cr_selected_mm_per_year`: 선택 부식률
  - `remaining_life_years` (RL): 잔여수명
  - `inspection_interval_years`: 권장 검사 주기
- 해석 포인트:
  - `t_current`가 `t_min`에 근접하거나 CR이 높으면 주기 단축 및 핫스팟 검사가 필요합니다.

### 3.2 정기기 (`/vessel`)
- 목적: 압력/형상 조건에서 쉘 및 노즐 건전성 스크리닝.
- 핵심 지표:
  - `t_required_shell_mm`
  - `thickness_margin_mm`
  - `external_pressure_utilization`
  - `nozzle_reinforcement_index`

### 3.3 회전기기 (`/rotating`)
- 목적: 기계 상태 및 보호계통 준비도 스크리닝.
- 핵심 지표:
  - `adjusted_vibration_limit_mm_per_s`
  - `mechanical_integrity_index`
  - `process_stability_index`
  - `protection_readiness_index`

## 4. 3-패널 화면 읽는 순서
- 좌측: 입력 조건(설계 기준, 운전 조건, 검사 이력)
- 중앙: 계산 요약, 시각화, 추천 조치
- 우측: 검증 레이어, 표준 참조, 레드/워닝 플래그

의사결정 권장 순서:
1. 레드 플래그/워닝 플래그 확인
2. 핵심 지표(`t_min`, CR, RL, interval, margin/index) 확인
3. 계산 Trace와 표준 근거 확인
4. 운전 지속/검사 강화/보수·FFS 검토 중 조치 결정

## 5. 배관 재질별 NDE 추천 로직
배관 시각화 패널에서 재질 그룹 기반 NDE 추천을 제공합니다.

- 탄소강:
  - `UT Thickness (CML Grid)`, `PAUT/UT mapping`, `MT(용접부 타겟)`
- 저합금강:
  - `UT/PAUT 용접 HAZ`, `MT/PT`, `복제금속조직(고온 프로그램)`
- 스테인리스:
  - `UT mapping`, `PT`, `ECT(필요 시)`
- 듀플렉스:
  - `UT mapping`, `PT`, `PMI/Ferrite 확인`
- 니켈합금:
  - `PT`, `PAUT/TOFD`, `PMI 확인`

권장 주기는 위험도(RL, CR, 온도 제한 상태)에 따라 자동으로 조정됩니다.

## 6. 중요 제한사항
- 본 시스템은 스크리닝 보조 도구이며, 최종 코드 적합성 승인 자체를 대체하지 않습니다.
- 최종 운전/보수 결정은 사내 절차, 코드 에디션 검토, SME 판단이 필요합니다.

## 7. 관련 문서
- 문서 허브: `docs/README.md`
- 문서 탐색 가이드: `docs/i18n/ko/DOCS_NAVIGATION_GUIDELINE.md`
- 보고서 제출 템플릿: `docs/i18n/ko/REPORT_SUBMISSION_TEMPLATE.md`
- 샘플 배관 제출본: `docs/i18n/ko/reports/SAMPLE_PIPING_REPORT_SUBMISSION_V0.1.md`
- 전 공종 샘플 팩: `docs/i18n/ko/reports/README.md`
- 표준 맵: `docs/standards_index.md`
- 배관 NDE 상세: `docs/i18n/ko/piping/NDE_RECOMMENDATIONS.md`
- 전체 이중언어 인덱스: `docs/BILINGUAL_INDEX.md`

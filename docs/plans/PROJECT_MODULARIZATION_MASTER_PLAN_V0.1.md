# Project Implementation Stabilization Plan

Status: Draft  
Version: v0.1  
Last Updated: 2026-03-03

## 1) 목적
- 1차 목표는 “전체 모듈화”가 아니라, 현재 프로젝트를 요구 수준으로 정확하게 구현/운영 가능한 상태로 고도화하는 것이다.
- 모듈화는 목표가 아니라 수단이며, 구현 정확도/안정성/검증 가능성을 높이는 범위에서만 적용한다.
- README 기준 전체 프로젝트(frontend + backend + scripts + dataset access path)를 점진적으로 재정렬하되, 기능 회귀 없이 납품 품질을 우선한다.

## 2) 범위
In Scope:
- `frontend/`: 화면/도메인 로직/콘텐츠/유틸 분리
- `src/`: 7개 공종 서비스 및 교차검증 모듈 분해
- `scripts/`: 실행 엔트리와 계산/튜닝 로직 분리
- `datasets/`: 대형 JSON 접근 경로 최적화(읽기 전략 및 캐시 경계)

Out of Scope (이번 라운드):
- “전체 파일 재구성” 자체를 목적으로 한 구조 변경
- 알고리즘/도메인 공식 변경
- API 계약 필드 변경
- UI 정보 구조 대규모 재설계

## 3) 현재 진단 스냅샷 (2026-03-03)

### 3.1 대형 파일(라인 수)
| 영역 | 파일 | 라인 |
|---|---|---:|
| Frontend | `frontend/lib/mock/rotating.ts` | 1281 |
| Frontend | `frontend/lib/glossary.ts` | 1109 |
| Frontend | `frontend/components/dashboard/engineering-console-dashboard.tsx` | 516 |
| Frontend | `frontend/components/visualization/piping-visuals-content.ts` | 505 |
| Frontend | `frontend/components/forms/discipline-form-localization.ts` | 497 |
| Backend | `src/vessel/service.py` | 654 |
| Backend | `src/piping/service.py` | 602 |
| Backend | `src/cross_discipline/validator.py` | 531 |
| Backend | `src/rotating/service.py` | 522 |
| Script | `scripts/tune_cross_discipline_thresholds.py` | 538 |

### 3.2 참조도(대표)
| 대상 | 참조도 |
|---|---:|
| `@/lib/glossary` | 13 |
| `@/lib/standards` | 12 |
| `CrossDisciplineValidator` | 24 |
| `PipingVerificationService` | 10 |
| `VesselVerificationService` | 10 |
| `RotatingVerificationService` | 10 |

### 3.3 대형 공통 데이터 파일
| 파일 | 크기(MB) |
|---|---:|
| `datasets/kosha_guide/normalized/guide_documents_text.json` | 29.18 |
| `datasets/kosha/normalized/guide_documents.json` | 24.12 |
| `datasets/kosha/normalized/law_articles.json` | 3.85 |

## 4) 목표 모듈 경계

### 4.1 Frontend
- `content/`: 도메인 상수/옵션/카피/매핑 데이터
- `utils/`: 순수 계산/정규화/점수화 함수
- `features/<discipline>/`: 공종별 엔트리(폼/결과/비주얼 조합)
- `services/`: API/외부 연계(`kosha` 등)
- `shared/`: 타입/공용 UI primitive/상태 접근

### 4.2 Backend
- `service.py`는 오케스트레이션만 담당
- `validation/`, `calculation/`, `consensus/`, `response_builder/`로 분해
- 교차검증(`cross_discipline`)은 `rules/` 단위로 분할

### 4.3 Data Access
- 대형 JSON 원본은 보존
- 런타임은 “경량 인덱스/요약 캐시”를 우선 사용
- 전체 문서 본문은 필요 시 지연 로드

## 5) 실행 원칙 (리스크 저감)
- 구현 가치(정확도/신뢰성/운영성) 없는 모듈 분할은 하지 않는다.
- 기존 export 경로는 1차에서 유지하고 내부만 분할한다.
- 리네임보다 “파일 추가 + 기존 파일 re-export”를 우선한다.
- 웨이브 단위로 `lint/typecheck/unit/build` 및 backend 테스트를 강제한다.
- 한 웨이브에서 화면·백엔드·데이터를 동시에 크게 바꾸지 않는다.

## 6) 1차 이관 대상 (Low Risk, 구조 분리 우선)

### 6.1 대상 파일 목록
| 영역 | 현재 파일 | 1차 분리 방향 |
|---|---|---|
| Frontend | `frontend/lib/mock/rotating.ts` | `frontend/lib/mock/rotating/` 하위로 `config.ts`, `constants.ts`, `presets.ts`, `calculators.ts`, `index.ts` 분리 |
| Frontend | `frontend/components/forms/discipline-form-localization.ts` | `frontend/content/forms/discipline-localization/`으로 데이터 분리, 컴포넌트는 로딩만 수행 |
| Frontend | `frontend/components/visualization/piping-visuals-content.ts` | `frontend/content/visualization/piping/` + `frontend/components/visualization/piping/` 분리 |
| Frontend | `frontend/lib/kosha/local-snapshot.ts` | `loader.ts`(파일 입출력), `scoring.ts`(검색 점수), `mappers.ts`(출력 매핑)로 분리 |
| Frontend | `frontend/lib/kosha/crosswalk.ts` | discipline rule map을 `content/kosha/crosswalk-rules/`로 분리 |
| Backend | `src/rag/local_kosha_rag.py` | CLI 엔트리/인덱스 빌드/검색 로직 분리 |
| Script | `scripts/benchmark_cross_discipline.py` | benchmark 프로파일/리포트 출력 함수 분리 |
| Script | `scripts/tune_cross_discipline_thresholds.py` | 탐색 알고리즘/입출력/리포팅 모듈 분리 |

### 6.2 완료 기준
- 외부 import 경로 호환(기존 경로 유지)
- 기능/응답 필드/UI 출력 동일
- 아래 검증 통과:
  - `npm --prefix frontend run lint`
  - `npm --prefix frontend run typecheck`
  - `npm --prefix frontend run test:unit`
  - `npm --prefix frontend run build`
  - `python -m unittest discover -s tests -p "test_*.py"`

## 7) 2차 이관 대상 (Medium Risk, 코어 서비스 분해)

### 7.1 대상 파일 목록
| 영역 | 현재 파일 | 2차 분리 방향 |
|---|---|---|
| Frontend | `frontend/lib/glossary.ts` | `content/glossary/{labels,definitions,guidance,priority}.ts` + `lib/glossary/index.ts` |
| Frontend | `frontend/lib/standards.ts` | `lib/standards/{entries,guidance,priority,index}.ts` |
| Frontend | `frontend/components/dashboard/engineering-console-dashboard.tsx` | `view-model hooks` + `presentational sections` 분리 |
| Backend | `src/cross_discipline/validator.py` | `rules/`(pair별), `thresholds.py`, `assembler.py`로 분리 |
| Backend | `src/piping/service.py` | `layer1.py`, `context_lookup.py`, `maker.py`, `layer3.py`, `layer4.py`, `response.py` |
| Backend | `src/vessel/service.py` | 입력검증/컨텍스트/계산/응답 빌더 분리 |
| Backend | `src/rotating/service.py` | steam-state 경로와 일반 경로 분리, 레이어 처리 모듈화 |

### 7.2 완료 기준
- 서비스 클래스 public API(`evaluate`) 유지
- 테스트 fixture 변경 최소화
- `scripts/run_quality_gate.py --profile fast` 통과 후 `--profile strict` 통과

## 8) 대형 공통 데이터 파일 처리 전략
- 원본:
  - `datasets/kosha_guide/normalized/guide_documents_text.json`
  - `datasets/kosha/normalized/guide_documents.json`
  - `datasets/kosha/normalized/law_articles.json`
- 전략:
  1. 빌드 시 경량 인덱스 생성(`id/title/keywords/offset` 중심)
  2. 런타임 검색은 인덱스 우선, 본문은 상위 N건만 지연 로드
  3. API 응답에는 요약 + 링크를 기본값으로 사용
  4. 캐시 무효화 키를 `manifest.json` 해시 기준으로 관리

## 9) 실행 순서
1. 1차 이관 대상부터 PR 단위로 분리 (파일군 1~2개씩)
2. 웨이브 종료마다 품질 게이트 실행 및 리포트 기록
3. 2차에서 코어 서비스 분해 진행
4. 마지막에 데이터 접근 최적화와 회귀 테스트 재실행

## 10) 운영 기록 규칙
- 각 웨이브 완료 시 아래 문서 동시 업데이트:
  - `docs/revisions/CHANGELOG.md`
  - `docs/revisions/DELIVERY_LOG.md`
- 권장 커맨드:
  - `python scripts/log_completion.py --version v0.xx --title \"modularization wave\" --scope \"scope summary\"`

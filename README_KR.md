# did-you-check-kosha

> ASME 표준: 문서당 수백 달러.
> API 코드: 세트당 수천 달러.
> KOSHA 규제 코퍼스: 무료, 공공 API, 18,576건.
>
> 누구도 이것을 엔지니어링 AI에 넣지 않았다. 지금까지는.

**[English README](README.md)**

---

Yuyong Kim은 University of Wisconsin-Madison M.S. Data, Insights & Analytics 과정 재학 중이며, UW-Madison 화학생물공학 학사, 석유화학 EPC 및 공정 플랜트 엔지니어링 분야 12년 이상의 실무 경력을 보유하고 있습니다.

---

## 이게 뭔가요?

한국 공정 플랜트 엔지니어링을 위한 **다분야 AI 검증 플랫폼**입니다.

7개 공학 계산 엔진(배관, 압력용기, 회전기기, 전기, 계장, 철골, 토목)을 실행하고, 4-계층 하이브리드 검증 모델로 검증한 뒤, **KOSHA 무료 공공 규제 코퍼스** — 1,327건의 기술지침 문서, 3,102건의 법령 조문, 16,174건의 인덱싱 행 — 에 대해 로컬 RAG로 규제 적합성을 확인합니다.

핵심 발견: **국제 코드 계산이 전부 통과해도 한국 PSM 규제가 준수 의무를 부과하는 경우가 존재합니다**. 이것을 *관할권 규제 격차(jurisdiction compliance gap)* 라 부릅니다. 이 시스템이 이를 자동으로 잡아냅니다.

---

## 왜 만들었나

저는 석유화학 회사에서 12년간 공정 엔지니어링 매니저로 일했습니다 (루이지애나 $3.2B 에탄 크래커 프로젝트 포함). 분야별 계산을 검토할 때마다 같은 일이 반복되었습니다:

- ASME나 API 계산 수치는 문제없음.
- 그 결과에 연결된 KOSHA 요건은 아무도 확인하지 않음.
- KOSHA 기술지침은 한국어이고, PDF로 되어 있고, 대부분의 엔지니어가 존재조차 모르는 포탈 뒤에 있기 때문.

ASME와 API는 문서당 수백~수천 달러를 청구합니다. KOSHA는 모든 것을 공공 API로 무료 공개합니다. 문제는 접근성이 아니라 통합이었습니다. 누구도 그 다리를 만들지 않았습니다.

---

## 무엇을 하는가

**7개 도메인 계산 엔진**

| 분야 | 표준 |
|---|---|
| 배관 | ASME B31.3, API 570 |
| 압력용기 | ASME Section VIII Div.1, API 510, API 579-1 |
| 회전기기 | API 610, 617, 670 |
| 전기 | IEEE C57.104, 1584-2018 |
| 계장 | IEC 61511, ISA-TR84.00.02 |
| 철골 | AISC 360 |
| 토목 / 콘크리트 | ACI 318, 562 |

**4-계층 하이브리드 검증**

1. 입력 검증 — 계산 전에 잘못된 데이터를 차단
2. K-투표 합의 — 수치적으로 다른 3개 경로를 실행, 불일치 감지
3. 물리/코드 적합성 — 도메인별 red flag 강제 적용
4. 역검증 — 출력으로부터 입력을 역산하여 일관성 확인

**KOSHA 규제 RAG**

- 16,174건 FTS 인덱싱 (기술지침 청크 13,084 + 법령 조문 3,090)
- 로컬 SQLite FTS5 — 클라우드 없음, API 키 없음, 비용 없음
- 개념 인식 동의어 확장으로 한/영 이중 언어 검색
- Ollama 기반 온프레미스 Qwen — 데이터가 외부로 나가지 않음

**교차분야 연성 검증기**

단일 분야 계산으로는 보이지 않는 연성 위험을 10개 정의된 도메인 쌍에 대해 검사합니다:
- 배관 노즐 하중 → 회전기기 베어링 응력
- 토목 기초 침하 → 회전기기 정렬 불량
- 전기 고조파 왜곡 → 회전기기 베어링 온도
- ...외 7개

---

## 실적 (숫자로)

**220건 골든 케이스 — 220건 통과**

```
piping:          accuracy=1.0000, red_flag_detection=1.0000
vessel:          accuracy=1.0000, red_flag_detection=1.0000
rotating:        accuracy=1.0000, red_flag_detection=1.0000
electrical:      accuracy=1.0000, red_flag_detection=1.0000
instrumentation: accuracy=1.0000, red_flag_detection=1.0000
steel:           accuracy=1.0000, red_flag_detection=1.0000
civil:           accuracy=1.0000, red_flag_detection=1.0000
```

**교차분야 절제 실험 — 60개 시나리오**

```
검증기 OFF: 0/60 차단
검증기 ON:  25/60 차단  (+0.4167 차단 비율)
경계 케이스: 0.0 → 1.0
고장 케이스: 0.0 → 1.0
```

**KOSHA RAG 검색 — 50개 큐레이션 쿼리**

```
                Plain FTS    Enhanced FTS    Delta
Recall@1        0.44         0.74            +0.30
Recall@3        0.74         0.86            +0.12
MRR@10          0.5744       0.7933          +0.2189
```

**규제 격차 — 3건 대표 사례**

```
                코드만 검출    RAG 검출        최초 히트 순위
VES-GOLD-001    0              1 (M-69-2012)        1
VES-GOLD-009    0              1 (C-C-23-2026)      1
PIP-GOLD-047    0              1 (제256조)           1
```

3건 모두: ASME/API 계산은 red flag 없이 통과.
3건 모두: KOSHA RAG가 계산에서 누락된 한국 관할권 의무를 식별.

---

## 논문

> *A KOSHA Regulatory Knowledge-Grounded Multi-Discipline AI Verification Framework for Process Plant Engineering*
> Yuyong Kim — University of Wisconsin-Madison
> arXiv preprint: [제출 후 링크 추가 예정]

전문: [`docs/publication/PAPER_EN_v2.md`](docs/publication/PAPER_EN_v2.md)

---

## 빠른 시작

```powershell
# 1. 의존성 설치
pip install -r submission_requirements.txt

# 2. KOSHA RAG 인덱스 빌드 (~10분, 1회)
python scripts/sync_kosha_corpus.py --force
python scripts/sync_kosha_guide_api.py --download
python scripts/parse_kosha_guide_pdfs.py
python scripts/kosha_rag_local.py build --rebuild

# 3. 쿼리 실행
python scripts/kosha_rag_local.py query "배관 부식 방지 법령 요건" --top-k 8 --generate

# 4. 벤치마크 전체 실행
python scripts/benchmark_all_runtime.py
python scripts/benchmark_cross_discipline_ablation.py
python scripts/benchmark_rag_retrieval.py
```

> Qwen은 [Ollama](https://ollama.ai)로 로컬 실행됩니다. 검색에는 GPU가 필요 없습니다.
> 생성 기능: `ollama pull qwen2.5:7b-instruct` (또는 원하는 Qwen 변형)

---

## 저장소 구조

```
src/
  piping/ vessel/ rotating/ electrical/ instrumentation/ steel/ civil/
  verification/       <- 4-계층 엔진 (engine.py, gates.py, maker.py, reverse_check.py)
  cross_discipline/   <- 연성 검증기 (10개 도메인 쌍)
  rag/                <- KOSHA RAG + 동의어 확장
  orchestrator/       <- 7-분야 파이프라인

datasets/
  golden_standards/   <- 220건 합성 테스트 케이스 (커밋됨, 316 KB)
  kosha/normalized/   <- 법령 조문 + 검색 코퍼스 (커밋됨)
  kosha_rag/          <- 평가 쿼리 (커밋됨); SQLite 인덱스 제외 (133 MB, 로컬 빌드)

scripts/              <- 벤치마크 + 코퍼스 동기화 + RAG 재빌드
docs/publication/     <- 논문 + 코드 맵 + 리뷰어 Q&A
config/               <- 임계값 프로파일 + 법령 링크 오버라이드
tools/kosha-ingestion <- KOSHA API 수집 소스
```

---

## 라이선스

**AGPL-3.0** — 개인, 연구자, 오픈소스 프로젝트에 무료.

상용 제품이나 서비스에서 스택을 오픈소스하지 않고 사용하려면 상용 라이선스가 필요합니다. LinkedIn으로 연락 바랍니다.

전체 조건은 [`LICENSE`](LICENSE)를 참조하세요 (KOSHA 데이터 사용 안내 포함).

---

## 저자

**Yuyong Kim**
University of Wisconsin-Madison
M.S. Data, Insights & Analytics Candidate
B.S. Chemical & Biological Engineering
석유화학 EPC 및 공정 플랜트 엔지니어링 12년 이상 실무 경력

[linkedin.com/in/yuyongkim](https://www.linkedin.com/in/yuyongkim/)

# Top 3 제출처 상세 분석

Updated: 2026-03-31

---

## 1순위: Expert Systems with Applications (Elsevier)

### 저널 정보
| 항목 | 내용 |
|------|------|
| **Publisher** | Elsevier |
| **Impact Factor** | ~8.5 (2024) |
| **CiteScore** | ~12.6 |
| **Q등급** | Q1 (Computer Science — AI) |
| **Article Type** | Research Article (제한 없음, 보통 25-40p) |
| **Review Period** | 8-12주 (1차 결정) |
| **Acceptance Rate** | ~18-22% |
| **Open Access Option** | Hybrid (OA 선택 가능, APC ~$3,390) |
| **Submission System** | Elsevier Editorial Manager |

### 논문 파일
`PAPER_1_ESWA.md`

### 적합성 분석

**왜 ESWA인가:**
- ESWA의 핵심 스코프는 "domain-specific AI/expert systems with real-world applications" — 본 논문이 정확히 이 범주
- 7개 공학 분야를 통합한 expert verification system 논문으로서 system paper 친화적
- RAG 기반 regulatory knowledge integration은 ESWA가 최근 활발히 수용하는 주제
- K-voting consensus, four-layer verification 등 방법론적 기여가 명확

**본 논문의 ESWA 차별화 포인트:**
1. **Jurisdiction compliance gap** — 새로운 개념 정의 및 실증 (Section 3에서 독립 섹션으로 정식 정의)
2. **Regulatory RAG** — 구체적 corpus 구축 방법론 + 정량 평가 (Recall@1 0.44→0.74)
3. **K-voting consensus** — 공학 계산 분야 최초 적용 (Avizienis 1985 기반)
4. **Reproducibility** — 전체 코드/데이터 AGPL 공개

**ESWA용 논문 서사 (PAPER_1_ESWA.md):**
- 리드: "코드 준수만으로는 부족하다" — jurisdiction compliance gap 개념을 전면에 배치
- 구조: Gap 정의(Section 3) → 시스템(Section 4-6) → 실증(Section 7) → 일반화(Section 8)
- 톤: AI/expert system 방법론 중심, 공학 실무는 배경으로 활용

**예상 리뷰어 관심사:**
- Synthetic data only → Limitation에서 명시적 인정
- BM25 vs vector search → 온프레미스 CPU 제약 설명, future work에 포함
- External baseline 부재 → Internal ablation의 타당성 논증

**커버레터:** `COVER_LETTER_ESWA.md`

---

## 2순위: Automation in Construction (Elsevier)

### 저널 정보
| 항목 | 내용 |
|------|------|
| **Publisher** | Elsevier |
| **Impact Factor** | ~10.3 (2024) |
| **CiteScore** | ~16.1 |
| **Q등급** | Q1 (Civil Engineering / Construction & Building Tech) |
| **Article Type** | Research Article (보통 20-35p) |
| **Review Period** | 10-16주 (1차 결정) |
| **Acceptance Rate** | ~15-20% |
| **Open Access Option** | Hybrid (APC ~$3,250) |
| **Submission System** | Elsevier Editorial Manager |

### 논문 파일
`PAPER_2_AIC.md`

### 적합성 분석

**왜 Automation in Construction인가:**
- IF 10.3으로 ESWA보다 높음 — 수용 시 더 높은 임팩트
- EPC (Engineering, Procurement, Construction) 프로젝트의 자동화가 저널의 정확한 스코프
- 플랜트 엔지니어링 + AI 검증은 이 저널의 핵심 독자층(건설/플랜트 엔지니어 + 연구자)에 직접 도달
- KOSHA/PSM 규제 통합은 한국 건설/플랜트 산업계에서 강력한 차별화

**본 논문의 AiC 차별화 포인트:**
1. **EPC 라이프사이클 전체** 커버 — 설계, 시공, 운영/검사 단계별 적용성 명시
2. **Cross-discipline coupling** — EPC 프로젝트 인터페이스 문제(nozzle load, settlement, harmonics)를 실무 맥락으로 설명
3. **7개 분야 통합** — 건설 자동화 분야에서 이 수준의 multi-discipline integration은 전례 없음
4. **실무 경험 기반** — 저자의 12년+ EPC 경력이 논문의 실용성을 뒷받침

**AiC용 논문 서사 (PAPER_2_AIC.md):**
- 리드: "EPC 공학 검증의 파편화 문제" — 실무 엔지니어가 공감하는 pain point에서 출발
- 구조: 문제 정의(fragmentation + regulation) → 플랫폼(Section 3) → 평가(Section 4) → EPC 실무 함의(Section 5)
- 톤: 공학 실무 + 산업 적용 중심, AI 방법론은 수단으로 서술
- 특별 포함: EPC 단계별 적용 시나리오 테이블, cross-discipline coupling의 실무 사례

**예상 리뷰어 관심사:**
- 실제 플랜트 데이터 부재 → "Field pilot with operating Korean petrochemical plant" as 최우선 future work
- Construction 단계 적용성 → Commissioning 시나리오 명시적 포함
- BIM 연계 → 현재 scope 외, future work에 언급 가능

**커버레터:** `COVER_LETTER_AIC.md`

**주의:** AiC는 CS 저널이 아니라 공학 저널이므로, AI 방법론보다 **공학적 가치와 실무 임팩트**를 강조해야 함

---

## 3순위: AAAI / IJCAI / NeurIPS Workshop

### 워크샵 정보
| 항목 | 내용 |
|------|------|
| **형식** | 4-8페이지 워크샵 논문 |
| **대상 워크샵** | AI for Engineering, Reliable AI, AI Safety, Regulation & AI |
| **Review Period** | 2-4주 |
| **Acceptance Rate** | ~40-60% (워크샵에 따라 다름) |
| **발표 형식** | Poster 또는 Oral (15-20분) |
| **비용** | 학회 등록비 (보통 $200-500 워크샵) |
| **Proceedings** | 워크샵별 상이 (일부 CEUR-WS 등) |

### 2026년 주요 대상 워크샵

| 학회 | 예상 워크샵 | 마감 예상 | 학회 일정 |
|------|-----------|----------|----------|
| **AAAI 2027** | AI for Engineering Systems | 2026년 9-10월 | 2027년 2월 |
| **IJCAI 2026** | AI Safety & Reliability | 2026년 5-6월 | 2026년 8월 |
| **NeurIPS 2026** | Regulation and AI | 2026년 9월 | 2026년 12월 |
| **ICML 2026** | AI for Science & Engineering | 2026년 5월 | 2026년 7월 |

### 논문 파일
`PAPER_3_WORKSHOP.md`

### 적합성 분석

**왜 워크샵인가:**
- **빠른 피드백**: 2-4주 리뷰로 저널 투고 전 학술 커뮤니티 반응 확인
- **네트워킹**: AI Safety / Regulatory AI 연구자와 직접 교류
- **Dual submission 가능**: 대부분의 워크샵은 저널 투고와 병행 가능 (non-archival)
- **arXiv 프리프린트와 시너지**: arXiv 등록 → 워크샵 발표 → 저널 투고 전략

**본 논문의 Workshop 차별화 포인트:**
1. **Catchy concept**: "Mind the Compliance Gap" — 기억에 남는 프레이밍
2. **Cross-domain relevance**: jurisdiction compliance gap은 공학뿐 아니라 법률AI, 규제AI, 안전AI 연구자 모두에게 해당
3. **Concrete demonstration**: 추상적 주장이 아니라 3/3 case detection + 수치 결과
4. **Generalisability argument**: 한국만이 아닌 EU/중국/사우디로 확장 가능

**Workshop용 논문 서사 (PAPER_3_WORKSHOP.md):**
- 리드: "ASME PASS인데 한국법 위반" — 한 줄로 문제 전달
- 구조: 압축된 4-page 형식, 개념 정의 → 시스템 요약 → 핵심 결과 → 일반화
- 톤: 도발적이고 간결, big picture 강조
- 특별 포함: 일반화 가능성(EU PED, Chinese GB, Saudi GACA) 명시적 논의

**커버레터:** `COVER_LETTER_WORKSHOP.md`

---

## 제출 전략 (권장 타임라인) — arXiv 미사용

> **참고:** arXiv 프리프린트 등록은 사용하지 않음. 저널/워크샵 직접 투고로 진행.

```
2026-04-07  ESWA 저널 투고 (1순위)
            ↓
2026-05-06  워크샵 마감에 맞춰 PAPER_3 제출 (IJCAI/ICML)
            (대부분 워크샵은 non-archival이므로 저널 투고와 병행 가능)
            ↓
2026-06~08  저널 1차 리뷰 결과 수신
            ↓
            Accept → 완료
            Revise → 수정 후 재제출
            Reject → AiC(2순위)로 전환 투고
```

### arXiv 미사용 시 대안

| 목적 | arXiv 대안 |
|------|-----------|
| 선행 공개 증거 | GitHub repo (tag: `arxiv-v1`) + Zenodo DOI 발급 가능 |
| 프리프린트 공유 | SSRN, TechRxiv (IEEE), 또는 ResearchGate 프리프린트 |
| 타임스탬프 확보 | GitHub release 날짜가 선행 연구 증거로 활용 가능 |

### 1순위 선택 가이드

| 기준 | ESWA 우선 | AiC 우선 |
|------|----------|---------|
| 독자층 | AI/CS 연구자 | EPC/건설 엔지니어+연구자 |
| 논문 강점 | Jurisdiction gap 개념, RAG 방법론 | 7분야 통합, 실무 임팩트 |
| IF | ~8.5 (충분히 높음) | ~10.3 (더 높음) |
| 수용 가능성 | 높음 (AI system paper 친화) | 중-높음 (field validation 요구 가능) |
| 리뷰 속도 | 빠름 (8-12주) | 느림 (10-16주) |
| 리스크 | 낮음 | 중간 (실무 데이터 없음 지적 가능) |

**추천:** synthetic data만으로 투고하는 현 시점에서는 **ESWA가 안전한 1순위**, AiC는 field pilot 데이터 확보 후 확장 투고에 적합.

---

## 파일 요약

| 파일명 | 용도 | 타겟 |
|--------|------|------|
| `PAPER_1_ESWA.md` | 저널 논문 (전문) | Expert Systems with Applications |
| `PAPER_2_AIC.md` | 저널 논문 (전문) | Automation in Construction |
| `PAPER_3_WORKSHOP.md` | 워크샵 논문 (축약) | AAAI/IJCAI/NeurIPS Workshop |
| `COVER_LETTER_ESWA.md` | 커버레터 | ESWA |
| `COVER_LETTER_AIC.md` | 커버레터 | AiC |
| `COVER_LETTER_WORKSHOP.md` | 커버레터 | Workshop |
| `PAPER_EN_v2.md` | 원본 논문 | GitHub 공개용 |
| `REVIEWER_RESPONSE_QA.md` | 리뷰어 예상 Q&A | 전체 (리뷰 대비) |

# 리뷰어 답변서 — JLP-D-26-00414 (개정판)

**원고 제목:** Detecting Jurisdiction Compliance Gaps in Process Plant Engineering with Regulatory RAG (개정 제목: *Detecting Jurisdiction Compliance Gaps in Process Plant Engineering with Regulatory RAG*)

**수신:** Prof. Paul Amyotte, Receiving Editor
**저널:** *Journal of Loss Prevention in the Process Industries*
**일자:** 2026-05-10

존경하는 Amyotte 교수님께,

원고를 개정할 기회를 주셔서 감사드리며, 세 분 리뷰어 분들의 상세하고 건설적인 의견에 깊이 감사드립니다. 리뷰어 분들의 피드백은 본 논문을 실질적으로 더 예리하게 만들어 주었습니다. 특히 Reviewer 1께서 비교 기준의 필요성을 강조해 주신 덕분에 산업 베이스라인 벤치마크와 4행 내부 레이어 절제(ablation) 실험을 정식화하게 되었고, Reviewer 2의 8개 항목에 걸친 비판은 규제 근거 서술(의무적(mandatory) vs. 권고적(guidance)), FFS 대 EPC 소절, 그리고 방법 비교 표(method comparison table)의 전면 재작성으로 이어졌으며, Reviewer 3께서 K-voting 설계 근거를 요구해 주셔서 새로 추가한 §5.4는 이제 본 논문에 필수적인 부분이라고 판단하고 있습니다. 개정 원고는 `docs/publication/PAPER_JLP_REVISED_v3.md`이며, 절·코멘트별 전수 추적 기록은 `docs/publication/REVISION_CHANGELOG_JLP.md`에 있습니다.

이하에서는 R1, R2, R3의 모든 코멘트에 대해 항목별로 답변드립니다. 각 답변은 (i) 구체적 우려를 인정하고, (ii) 무엇을 어디서 변경했는지를 적시하며, (iii) 검증 가능한 산출물(스크립트, `outputs/*.md` 파일, 도표, 또는 개정 원고의 절)을 인용하고, (iv) 개정 원고의 해당 구절을 그대로 인용합니다. 인용된 모든 수치는 현재의 코드와 데이터로부터 재계산된 값이며, 본 논문의 핵심 검색(retrieval) 주장은 이제 페어드 부트스트랩(paired-bootstrap) 95% CI가 0을 배제하는 Recall@1과 MRR@10으로 좁혀져 있고, Recall@3과 Recall@5는 CI가 0을 포함하는 점추정치로 정직하게 보고됩니다.

---

## 개정 요약 (Summary of revisions)

**아키텍처 수준 변경.** 본 논문은 명시적 3계층 아키텍처(7개 계산 엔진 + K-voting을 포함한 4계층 하이브리드 검증 + KOSHA Regulatory RAG)를 중심으로 재구조화되었으며, **관할권 컴플라이언스 갭(jurisdiction compliance gap)** 은 서술적 주장에서 정식으로 정의된 구성개념(§7.1)으로 격상되어, 정량적 절제(§6.6 Layer A: 산업 베이스라인 0/3 vs. Regulatory RAG 3/3)와 계층별 절제(§6.6 Layer B, Table 7b)를 통해 조작적으로 정의됩니다. 시스템은 이제 일관되게 HAZOP / RBI / Digital Twin에 대한 **컴플라이언스 코파일럿(compliance co-pilot)** (§2.6, §7.2, Table 8)으로 위치 지어지며, 대체재가 아닙니다. 이 재정립은 Reviewer 2의 HAZOP 범위 우려를 직접적으로 해결합니다. K-voting은 이제 경로 수, 1% 허용오차, 독립성의 범위라는, Reviewer 3께서 정당화를 요구하신 세 가지 구체적 항목을 다루는 전용 설계 근거 소절(§5.4)을 가지게 되었습니다.

**근거 기반.** 이제 특정 리뷰어 우려에 연계된 7가지 분석을 보고합니다: (a) 골든 데이터셋 기준 220/220 구현 검증 통과(§6.1) — Reviewer 2의 권고에 따라 명시적으로 **구현 검증(implementation verification)이며 예측 검증(predictive validation)이 아님**으로 프레이밍; (b) 0/60에서 26/60(+0.4333)으로 상승하는 60-시나리오 학제 간 절제, 실패 모드별 분할은 22/3/1 (`outputs/ablation_failure_mode_partition.md`); (c) 페어드 부트스트랩 95% CI를 갖는 50-쿼리 큐레이트 검색 벤치마크(`outputs/rag_bootstrap_ci_report.md`); (d) 산업 베이스라인 비교("ASME/API 통과 = 컴플라이언스 완료") — 제안 시스템이 0/3 vs. 3/3을 산출(Table 7); (e) 4행 내부 계층 절제(Table 7b, `outputs/layer_ablation_report.md`); (f) PIP-GOLD-003에 대해 일반 배관 무결성 쿼리로 top-10에서 0개 mandatory + 10개 guidance 히트를 반환하는 검증된 음성 사례 실행(`outputs/negative_case_pip_gold_003.md`); (g) Reviewer 1의 "도표 부재" 지적을 해결하는 5개의 신규 도표(시스템 아키텍처, RAG 워크플로우, 학제 간 결합, 절제, 검색 지표). 답변서와 원고의 모든 수치는 `outputs/` 또는 `datasets/` 내의 파일로 추적 가능합니다.

**프레이밍.** Reviewer 2의 의견에 따라 약어(Acronyms) 표와 핵심 정의(Key Definitions) 절을 추가하였고, 명시적인 의무적(Mandatory) 대 권고적(Guidance) 규제 분류 라벨(§4.3, Table 5), FFS 대 EPC 소절(§7.4), Reviewer 2께서 그대로 요청하신 방법 비교 표(§7.2 Table 8), §6.4 Case 3에 제256조 verbatim 한국어 원문과 영어 working translation 병기, 그리고 Recall@3/Recall@5에서 통계적 검정력의 한계를 숨기지 않고 드러내는 §6.6의 민감도 분석 단락을 추가하였습니다. 이 모든 사항은 정본 개정판 `PAPER_JLP_REVISED_v3.md`에 반영되어 있습니다.

**피어 리딩 피드백 (본 개정 패스에서 추가).** 개정 준비 과정에서 받은 피어 리딩 피드백에 따라 세 개의 추가 Limitations 문장(§8 항목 1, 3, 4)을 추가하여, implementation-verification 대 predictive 구분, piping-vessel coupling 집중, K≥3 retrieval CI-includes-zero caveat를 본문 인라인뿐 아니라 한계 수준에서도 명시적으로 만들었습니다. 동일 패스에서 §6.5에 쿼리 생성 독립성 인정을 추가하고, VES-REAL-001 프레이밍을 "이중 검증"에서 파이프라인 실행 증거로 재조정하였으며(§A.5/§A.6), 위에서 기술한 주장 다운스케일링 절을 적용하였습니다.

---

## Reviewer 1 답변

Reviewer 1께서는 주제가 흥미롭고 산업적으로 적용 가능하다고 평가하셨으나, 다섯 가지 연결된 우려를 제기하셨습니다: (R1.1) 최신 기술(state of the art) 및 공정 전문가와의 비교 부재, (R1.2) 결론을 뒷받침하는 데이터 부재; 25-시나리오 RQ1 주장에 대한 세부 정보 부족, (R1.3) 결론이 RQ1 형식의 검출만 보여주고 학제별 강·약점 분석이 없음, (R1.4) 도표 부재 및 데이터 최소화; RQ2가 추가 논의나 비교 없이 세 가지 갭을 나열함, (R1.5) 합성 데이터에 대한 의존이 모델이 찾을 줄 알았던 것을 그대로 산출했을 가능성. 아래에서 각 항목을 다룹니다.

### Comment R1.1: Comparison against state of the art and process experts

> *"Intro sections briefly discuss other AI methods for detecting gaps. I would generally like to see a comparison against the state of the art, but the tool presented here left me wondering how this method compares against process experts that do this assessment now. I think this is worth mentioning, otherwise the findings are presented in a vacuum and I don't really know how effective the model is."*

**저자 답변:** 이 우려에 대해 감사드립니다. 이 의견 덕분에 원래 초안에 결여되어 있던 비교 축을 정식화하게 되었습니다. §6.6에 두 가지 상호 보완적 비교를 추가하였습니다. **Layer A (산업 베이스라인)** 은 한국 EPC 배관/용기 검토 실무에서 지배적인 현행 검토 규칙 — "ASME/API 계산 통과 = 컴플라이언스 완료" — 을 명시적으로 부호화한 것으로, 이는 한국 관할권 오버레이가 부재할 때 공정 전문가가 적용하는 규칙입니다. 이 베이스라인 하에서 §6.4의 세 케이스 스터디는 **한국 관할권 의무에 대해 0/3 검출**을 산출하며, 제안 시스템은 **3/3** (Table 7)을 산출하고, 세 케이스 모두에서 첫 관련 검색 순위가 1입니다. **Layer B (내부 계층 절제)** 는 시스템을 4개의 구성 가능한 계층으로 분해하여, 학제 간 검증기와 KOSHA RAG 계층이 **직교적(orthogonal)** 임을 보입니다 — 각 계층은 다른 계층이 잡지 못하는 부류의 이슈를 잡습니다(Table 7b, `scripts/run_layer_ablation.py`로 계산). 동일 과업(KOSHA-인지, 다학제, ASME/API + 한국 법규)을 수행하는 또 다른 **출판된** 시스템과의 비교라는 더 넓은 질문에 관하여, §2와 §6.6은 이제 그러한 시스템이 문헌에 보고된 바 없음을 명시적으로 기술합니다. RAGuard [6]는 단일 도메인 비법규(non-statutory)이고, Elhosary HAZOP-RAG [3]는 법규가 아닌 과거 사고를 검색하며, [13]의 LLM 파인튜닝 작업은 공학 계산을 수행하지 않습니다. 따라서 우리는 산업 베이스라인 + 내부 절제 쌍을 가용한 가장 강한 비교로 제시하며, §8에서 한계를 정직하게 인정합니다.

**개정 원고 발췌** (§6.6, Layer A 및 Layer B):

> **Layer A — Industry baseline ("ASME/API pass = compliance complete").** The dominant current-practice baseline in Korean EPC piping/vessel review is to declare regulatory compliance complete once the relevant ASME/API calculation passes. Under that baseline the three case studies of §6.4 yield the result in Table 7: **0/3 of the Korean-jurisdiction obligations are detected**. The proposed system detects **3/3**. The first-relevant retrieval rank is 1 in all three cases.
>
> **Layer B — Internal four-layer ablation.** […] The decomposition shows that the cross-discipline validator and the KOSHA RAG layer carry **orthogonal** signal: each catches a class of issue the other does not. K-voting is a verification-quality layer that does not, by itself, contribute new detections; its role is to suppress false-positive numerical-precision artefacts that would otherwise pollute the upstream signal.
>
> *역문:* **Layer A — 산업 베이스라인("ASME/API 통과 = 컴플라이언스 완료").** 한국 EPC 배관/용기 검토에서 지배적인 현행 베이스라인은 해당 ASME/API 계산이 통과하면 규제 컴플라이언스가 완료된 것으로 선언하는 것이다. 이 베이스라인 하에서 §6.4의 세 케이스 스터디는 Table 7의 결과를 산출한다: **한국 관할권 의무 중 0/3이 검출**된다. 제안 시스템은 **3/3** 을 검출한다. 세 케이스 모두에서 첫 관련 검색 순위는 1이다.
>
> **Layer B — 내부 4계층 절제.** […] 분해 결과, 학제 간 검증기와 KOSHA RAG 계층은 **직교적** 신호를 운반함을 보인다: 각 계층은 다른 계층이 잡지 못하는 부류의 이슈를 잡는다. K-voting은 그 자체로는 새로운 검출에 기여하지 않는 검증 품질 계층이며, 그 역할은 그렇지 않으면 상위 신호를 오염시킬 수치 정밀도 거짓양성 인공물을 억제하는 데 있다.

**근거**: `scripts/run_layer_ablation.py`로 산출된 `outputs/layer_ablation_report.md`; `outputs/rag_retrieval_report.md` (Code-only vs Regulatory RAG, lines 21–26); `PAPER_JLP_REVISED_v3.md`의 §6.6 Tables 7 및 7b.

### Comment R1.2: No data presented; RQ1 25-scenario claim lacks detail (what was predicted, why, are findings significant)

> *"There's no data presented to support the conclusions and limited discussion of the results and the method's effectiveness. In your RQ1 there's a claim that the model predicts 25 cross discipline scenarios, but there are no further discussions into the details: what was predicted, why did this model find the scenarios, are they significant findings."*

**저자 답변:** 감사드립니다. 이 코멘트는 헤드라인 수치가 실패 모드별 분해 없이 제시되었던 원논문의 실제 갭을 드러내었습니다. 우리는 §6.3의 보고를 처음부터 끝까지 재구축하였습니다. 첫째, 헤드라인 수치 자체를 현재 코드와 데이터에 대해 재실행하였으며, 이제 **26/60(25/60이 아님)** 입니다: 데이터 드리프트 이후 데이터셋(`piping_golden_dataset_v1.json`이 초기 커밋 이후 중복-과잉(duplicate-surplus) 보정으로 교체됨)에서의 새 재실행은 4회 실행에 걸쳐 결정적으로 26/60을 산출합니다(`outputs/cross_discipline_ablation_report.md`; `build_indices_mixed_random`은 fixed seed=112 사용). 둘째, 이제 그 26개 검출을 실패 모드 패밀리별로 분해합니다(`outputs/ablation_failure_mode_partition.md`, `scripts/dump_ablation_hits.py`): **piping-vessel nozzle-margin 22개(84.6%), electrical-rotating bearing-coupling 3개(11.5%), civil-rotating foundation-vibration 1개(3.8%)**. 셋째, 각 패밀리가 **왜** 발화하는지(예: 열 하중 하의 배관 반력에 의해 ASME Section VIII 허용 노즐 하중이 초과됨 — 이는 B31.3와 Section VIII이 단독으로는 점검하지 않는 결합)와 **편향이 의미하는 바**(piping-vessel에 대한 집중은 검증기의 속성이라기보다는 60-시나리오 집합의 구성을 반영함; 다른 결합 패밀리를 더 조밀하게 다루도록 시드 집합을 확장하는 것은 향후 작업으로 문서화됨)를 명시적으로 기술합니다. 넷째, 신규 Figure 4가 검증기 OFF vs ON에서 집합별 차단 카운트를 시각화합니다.

**개정 원고 발췌** (§6.3, Significance of detections):

> **Significance of detections.** Per-failure-mode partition of the 26 blocked scenarios (`outputs/ablation_failure_mode_partition.md`, computed by `scripts/dump_ablation_hits.py`):
>
> | Coupling family | Blocked count | Share |
> |---|---:|---:|
> | Piping-vessel nozzle margin mismatch | 22 | 84.6% |
> | Electrical-rotating bearing-health coupling | 3 | 11.5% |
> | Civil-rotating foundation-vibration coupling | 1 | 3.8% |
> | **Total** | **26** | **100%** |
>
> Detections concentrate in the **piping-vessel nozzle margin mismatch** family (22/26 = 84.6%): ASME Section VIII allowable nozzle loadings exceeded by piping reaction forces under thermal load — a coupling neither B31.3 nor Section VIII checks in isolation.
>
> *역문:* **검출의 유의성.** 차단된 26 시나리오의 실패 모드별 분할(`outputs/ablation_failure_mode_partition.md`, `scripts/dump_ablation_hits.py`로 계산):
>
> | 결합 패밀리 | 차단 수 | 비율 |
> |---|---:|---:|
> | Piping-vessel 노즐 마진 불일치 | 22 | 84.6% |
> | Electrical-rotating 베어링 건전성 결합 | 3 | 11.5% |
> | Civil-rotating 기초 진동 결합 | 1 | 3.8% |
> | **합계** | **26** | **100%** |
>
> 검출은 **piping-vessel 노즐 마진 불일치** 패밀리(22/26 = 84.6%)에 집중된다: 열 하중 하의 배관 반력에 의해 ASME Section VIII 허용 노즐 하중이 초과되는 결합으로, 이는 B31.3와 Section VIII이 단독으로는 점검하지 않는 결합이다.

**근거**: `outputs/ablation_failure_mode_partition.md` (26개 모든 히트에 대한 차단 코드와 함께 행별 패밀리 할당); `outputs/cross_discipline_ablation_report.md`; Figure 4 (`docs/publication/figures/fig_4_ablation.png`); `PAPER_JLP_REVISED_v3.md`의 §6.3.

### Comment R1.3: Conclusions only show RQ1 detection; are there strengths and weaknesses across disciplines?

> *"Conclusions only show that errors can be detected by RQ1, is the model better at predicting particular problems (civil, electrical, etc) are there strengths and weaknesses"*

**저자 답변:** 감사드립니다. 원래의 결론에 대한 정당한 비판입니다. 개정 논문은 학제별 강·약점을 세 수준에서 보고합니다. (a) **결합 패밀리별** (§6.3, 위 표): 검증기의 신호는 piping-vessel 결합에서 가장 강하고(22/26 = 84.6%), civil-rotating에서 가장 약하며(1/26 = 3.8%), 이 편향은 시드 집합 구성에 기인하며 시나리오 집합 확장을 향후 작업으로 문서화합니다. (b) **학제별 계산 정확도** (§6.1 Table 2): 220-케이스 구현 검증은 7개 학제(Piping 50, Vessel 30, Rotating 30, Electrical 30, Instrumentation 30, Steel 25, Civil 25)에 걸쳐 균형 잡혀 있고 정확도는 모두에서 1.0000입니다 — 이는 동일 표준에서 파생된 케이스에 대한 구현 검증의 속성입니다(Reviewer 2의 권고에 따라 정직하게 프레이밍합니다: 이는 구현을 확인하는 것이지 예측 전이(predictive transfer)를 확인하는 것이 아닙니다). (c) **규제 대상별 검색 성능** (§6.5 Table 6b): 강화 검색의 가장 큰 이득은 제256조(부식 방지, +0.20 R@5)와 B-M-18 배관 수명(+0.20 R@5)에서 나옵니다 — 이는 일상적 한국어 용어가 정식 명칭과 가장 크게 분기되는 정확한 대상입니다. 가장 작은 이득은 평이한 BM25만으로도 모든 관련 청크를 검색하는 C-C-23 RBI(+0.00)에서 나옵니다. 또한 §6.5에 명시적인 약점 진술(Recall@3 및 Recall@5 페어드 부트스트랩 CI가 0을 포함 — R1.4 참조)과 §8(합성 데이터만, 10쌍 결합 한계, 단일 관할권)을 추가하였습니다.

**개정 원고 발췌** (§6.5 Table 6b 및 주변 단락):

> The Recall@3 = Recall@5 plateau in the overall numbers reflects the deliberately narrow target set (typically 1–2 relevant documents per query group in a 1,327-document corpus); in a broader evaluation, NDCG@K would differentiate further. The largest gains from the enhanced configuration come on the targets where casual Korean terminology diverges most from the formal title (Article 256, B-M-18) — exactly the cases the synonym expansion was designed for.
>
> *역문:* 전체 수치에서 Recall@3 = Recall@5의 정체는 의도적으로 좁힌 대상 집합(전형적으로 1,327-문서 코퍼스에서 쿼리 그룹당 1–2개 관련 문서)을 반영하며, 더 넓은 평가에서는 NDCG@K가 추가로 변별할 것이다. 강화 설정에서의 가장 큰 이득은 일상적 한국어 용어가 정식 명칭과 가장 크게 분기되는 대상(제256조, B-M-18)에서 발생한다 — 이는 동의어 확장이 설계된 정확한 케이스이다.

**근거**: `outputs/rag_retrieval_report.md` (그룹별 R@5); `outputs/ablation_failure_mode_partition.md` (패밀리별 분해); `PAPER_JLP_REVISED_v3.md`의 §6.1 Table 2 + §6.3 + §6.5 Table 6b.

*후기 보강 (개정 이후):* Appendix B.1은 `outputs/per_discipline_accuracy.md`에서 학제별 계산 정확도를 그대로 보고합니다 — piping 50/50, vessel 30/30, rotating 30/30, electrical 30/30, instrumentation 30/30, steel 25/25, civil 25/25 — 모두 1.0000이며 red-flag precision과 recall도 모든 학제에서 1.0000입니다. 이 균일한 정확도가 외부 ground-truth fidelity가 아닌 self-consistency를 측정한다는 caveat을 §8 Limitation 8로 명시적으로 표면화하여 over-read를 방지합니다.

*후기 보강 (주장 다운스케일링, 피어 리딩 피드백 반영):* Abstract, §1 contributions, §9 Conclusion은 이제 학제 간 증거가 piping-vessel 결합(26건 중 22건 검출)에 집중되며 나머지 쌍에 대해서는 탐색적이라는 점을 명시적으로 진술합니다. "7-discipline integrated framework" 프레이밍은 아키텍처적 주장으로 보존되지만, 7개 학제 전반에 걸쳐 균등하게 검증된 경험적 증거로는 더 이상 제시되지 않습니다. §1의 신설 **Scope statement** (및 §7 시작부의 짧은 §7.1 이전 단락)은 *framework scope* (7개 학제와 4개 검증 계층에 걸친 아키텍처)와 *validated scope* (가장 조밀한 경험적 근거는 piping-vessel에 집중; 나머지 학제 쌍은 탐색적)를 명시적으로 분리하여, 독자가 아키텍처적 7-discipline 주장을 균등하게 검증된 경험적 커버리지로 오독하지 못하도록 합니다.

### Comment R1.4: No figures; RQ2 three gaps without further discussion; basis for comparison

> *"No Figures and minimal data to support conclusions. RQ2 for example lists three gaps detected, but there's no further discussion, was this expected, is it significant, were any gaps missed? There really needs to be a basis for comparison, otherwise it is difficult for me to accept the results."*

**저자 답변:** 감사드립니다. 이 코멘트가 네 가지 실질적 추가를 이끌었습니다. **(a) 도표.** 5개의 도표가 추가되었습니다: Figure 1(시스템 아키텍처), Figure 2(RAG 워크플로우), Figure 3(학제 간 결합 로직), Figure 4(절제 60-시나리오 차단 카운트 검증기 OFF vs ON), Figure 5(규제 대상 그룹별 Recall 및 MRR, Plain vs Enhanced). 5개 모두 `scripts/generate_paper_figures.py`로부터 재생성되었으며 실제 수치를 반영합니다(v3 절제 Figure 4는 옛 25/+41.7%가 아닌 보정된 26/+43.3% 수치를 반영). **(b) 세 개 RQ2 갭의 유의성.** §6.4는 이제 케이스별로 *각 갭이 운영적으로 왜 중요한지* 를 설명합니다: M-69-2012는 누락 시 "매우 안전한" 용기에서도 운영자를 PSM 감사 지적에 노출시키는 문서화 의무를 발동합니다; C-C-23 + B-M-18은 API 510 달력 주기보다 일찍 발화할 수 있는 관할권 특이적 RBI 트리거를 추가합니다(점검 부족(under-inspection) 갭); 그리고 제256조(법률상 의무)는 ASME B31.3 및 API 570이 부호화하지 않는 유체 화학에 조건화된 부식 방지 의무를 부과합니다. **(c) 누락된 갭이 있는가?** §6.5는 그룹별 Recall@5(Table 6b)를 보고합니다: 시스템은 Enhanced 모드에서 다섯 개의 모든 규제 대상을 Recall@5 ≥ 0.7000으로 검색하며, 제256조는 0.7000입니다(1.0000이 아님 — 그 그룹의 세 쿼리는 손실된 패러프레이징에서 여전히 대상을 놓침). 이는 실제 약점이며, 이제는 숨기지 않고 그렇게 진술합니다. **(d) 비교 기준** 은 §6.6 Layer A(산업 베이스라인 0/3 vs RAG 3/3)와 Layer B(내부 계층 절제 Table 7b)에 의해 다루어집니다 — 위의 R1.1 참조.

**개정 원고 발췌** (Figure 4 캡션 + §6.4 Case 3 Why-this-matters):

> *Figure 4. Cross-discipline ablation (60 scenarios): blocked counts by scenario set, validator OFF vs ON. Total rises 0 → 26 (+43.3%); aligned-boundary and aligned-failure subsets rise from 0/n to n/n; mixed sets show partial coverage proportional to coupling density.*
>
> [§6.4 Case 3] The provision is **mandatory** under the Act. The linkage from calculation context to the obligation is: `200 ppm Cl⁻ + sour service + carbon steel` → recognised corrosion-aggressive condition → Article 256 corrosion-prevention measures **shall** be in place. ASME B31.3 and API 570 calculations are silent on this obligation; they do not require a corrosion-prevention plan as a function of fluid chemistry. The system therefore detects a regulatory obligation that is structurally invisible to international-code-only calculation workflows — a concrete instance of the **jurisdiction compliance gap** defined in §7.
>
> *역문:* *Figure 4. 학제 간 절제 (60 시나리오): 시나리오 집합별 차단 카운트, 검증기 OFF vs ON. 총합은 0 → 26 (+43.3%)으로 상승하고, aligned-boundary 및 aligned-failure 하위집합은 0/n에서 n/n으로 상승하며, 혼합 집합은 결합 밀도에 비례하는 부분 커버리지를 보인다.*
>
> [§6.4 Case 3] 해당 조항은 법률상 **의무적(mandatory)** 이다. 계산 맥락에서 의무로의 연결은 다음과 같다: `200 ppm Cl⁻ + sour service + carbon steel` → 인정된 부식 공격성 조건 → 제256조의 부식 방지 조치가 갖춰져야(shall) 한다. ASME B31.3와 API 570 계산은 이 의무에 대해 침묵한다; 이들은 유체 화학의 함수로서 부식 방지 계획을 요구하지 않는다. 따라서 시스템은 국제 코드 전용 계산 워크플로우에 구조적으로 보이지 않는 규제 의무 — §7에서 정의한 **관할권 컴플라이언스 갭** 의 구체적 사례 — 를 검출한다.

**근거**: `docs/publication/figures/fig_1_system_architecture.png` … `fig_5_retrieval_metrics.png`; `scripts/generate_paper_figures.py`; §6.4 (케이스별 Why-this-matters 단락); §6.5 Table 6b (그룹별 R@5); `PAPER_JLP_REVISED_v3.md`의 §6.6 Tables 7 및 7b.

### Comment R1.5: Synthetic-data circularity — "did you find what you knew the model would find?"

> *"Relies on synthetic data that could skew the results. Did you find exactly what you know the model would find? This is why I feel a comparison to another methodology is needed."*

**저자 답변:** 감사드립니다. 이는 R1 리뷰의 가장 근본적인 우려이며, 개정 논문에서 네 측면에서 다루었습니다. **첫째, 프레이밍.** §6.1은 220/220 결과를 명시적으로 **구현 검증이며 예측 검증이 아님(implementation verification, not predictive validation)** 으로 재프레이밍합니다 — 엔진은 자신이 구현하는 동일 표준에서 파생된 케이스에 대해 평가되는 결정론적 규칙 기반 계산기이므로, 만점은 구현이 표준을 충실히 부호화하였음을 확인하는 것이지 시스템이 보정 분포 외부의 플랜트 데이터로 일반화됨을 확인하는 것이 *아닙니다*. §6.1의 제목도 "Calculation Accuracy on the Golden Dataset (implementation verification)"으로 재라벨링하고, 결론에도 동일한 프레이밍을 추가합니다. **둘째, 반순환성(anti-circularity) 구성.** §6.1은 이제 테스트 케이스가 규제 텍스트로부터 *역방향으로 도출됨* 을 적시하는 방어 및 선례 단락을 포함합니다: 각 KOSHA RAG 대상은 실제 KOSHA 조항을 먼저 읽어 선택된 후, 이를 발동시켜야 하는 계산 맥락이 합성됩니다. 따라서 검출은 계산 입력이 구성된 것이라 하더라도 실제 규제 의무에 근거를 둡니다. 또한 이 구성 패턴이 안전 임계 AI 평가에서 확립된 관행임을 적시합니다(알려진 정답 라벨을 가진 의료 AI 합성 코호트; 자율 주행 차량 시뮬레이션 시나리오). **셋째, 경험적 음성 사례.** §6.7은 이제 일반(비부식) 서비스 하의 SA-312 TP316 ERW 라인(2.013 MPa, 119.5 °C; 염화물이나 sour-service 플래그 없음)인 **PIP-GOLD-003**에 대한 검증된 음성 사례 실행을 보고합니다 — 케이스 명세에서 엄격히 도출된 일반 배관 무결성 쿼리(material, NPS, weld-type, `service_type='general'`, 케이스가 둘 다 설정하지 않으므로 chloride/sour 용어 없음)를 실제 RAG 파이프라인(`scripts/run_negative_case_rag.py`)을 통해 사용한 결과, 시스템은 top-10에서 **0 mandatory + 10 guidance 히트** 를 반환하며, 최상위 결과는 `B-M-18-2026` (KOSHA 배관 수명 관리, guidance 분류)입니다. 어떤 mandatory 의무도 발동되지 않습니다.

**동일 근거 파일의 보조 쿼리 변형에 관한 주.** 완전한 투명성을 위해 우리는 `outputs/negative_case_pip_gold_003.md`가 `mirrored_pip047_form_chloride_terms_removed`로 라벨링된 *두 번째* 프로브 변형을 기록함을 공개합니다. 이 변형은 PIP-GOLD-047 쿼리의 *형태* — 문자 그대로의 어구 `Article 256` 및 `corrosion prevention` 포함 — 를 유지하며 chloride/sour 용어만 제거한 것으로, Article 256을 순위 2에서 검색합니다. 따라서 보고서의 헤드라인에는 "WARNING — at least one query variant returned a *mandatory* (law_article) hit in its top-10."라고 기록되어 있습니다. 우리는 이 두 번째 변형을 보고서에서 억제하지 않고 의도적으로 보존하였는데, 이는 음성 사례 테스트와 *다른* 질문에 답하기 때문입니다. 두 변형은 두 가지 질문을 분리합니다: **(i)** *시스템이 자신의 명세에서 도출된 양성(benign) 케이스에 대해 플래그를 띄우는가?* — 본래의 음성 사례 질문. 이 질문에 대한 올바른 쿼리는 명세에 충실한 일반 배관 무결성 변형(케이스 명세가 주장하지 않는 어떤 용어도 없음)이며, 답은 **아니오** 입니다(top-10 내 0 mandatory, 최상위 결과는 guidance 분류의 B-M-18-2026). **(ii)** *쿼리가 부식 방지 법규를 명시적으로 요청할 때 시스템이 제256조를 검색하는가?* — 이는 음성 사례 행위가 아닌 검색 정확성의 질문. 답은 **예** (Article 256 순위 2)이며, 이는 *바람직한* 검색 행위입니다. 왜냐하면 제256조는 사실 한국의 부식 방지 법규이고 BM25는 쿼리가 공급한 키워드에 정확히 응답하고 있기 때문입니다. "Article 256"을 포함한 쿼리에 대해 제256조를 검색하였다고 시스템에 벌점을 부과하는 것은 작동하는 검색기에 벌점을 부과하는 것에 해당합니다. §6.7의 음성 사례 논의는 (i)에 관한 것이며, (ii)의 프로브는 (i)에 대한 반박이 아니라 정직한 공개를 위해 동일 근거 파일에 보고됩니다. (i)/(ii) 구분은 이제 개정 원고 §6.7에 명시적으로 기술되어 있습니다.

**넷째, 정면 비교(head-to-head).** R1.1에서 언급한 바와 같이 출판된 KOSHA-인지 다학제 시스템은 존재하지 않습니다. 따라서 우리는 산업 베이스라인 + 내부 절제 쌍(§6.6)을 비교 축으로 사용하고, 제3자 정면 비교의 부재를 한계로 인정합니다(§8 Limitation 5: "Comparison scope"). 또한 §8 Future research directions의 항목 (5)에서 동일 플랜트 패키지에 대한 독립적 KOSHA PSM 감사관의 발견 사항과 시스템이 플래그한 규제 의무를 비교하는 전향적(prospective) 연구를 약속합니다.

**개정 원고 발췌** (§6.1 프레이밍 단락 및 §6.7 음성 사례 단락):

> We deliberately frame these results as **implementation verification, not predictive validation**, in the sense developed in recent methodological discussions of synthetic-data evaluation: the engines are deterministic rule-based calculators evaluated against cases derived from the same standards they implement. Perfect scores confirm that the implementation faithfully encodes the standards, *not* that the system generalises to plant data outside the calibration distribution. Predictive validation against real plant operating or design records is a separate, higher bar that requires field-pilot deployment (Section 8).
>
> [§6.7] **Negative case (no false-positive flag).** […] Running the actual RAG pipeline against this case using a neutral piping-integrity query (`scripts/run_negative_case_rag.py`, `outputs/negative_case_pip_gold_003.md`), the system returns **0 mandatory hits and 10 guidance hits in the top-10**, with the top result being `B-M-18-2026` (KOSHA Technical Regulation for Piping Life Management, guidance class). No jurisdiction-specific mandatory obligation is triggered. This empirically demonstrates that the KOSHA RAG layer is not biased to fire on every input.
>
> *역문:* 우리는 이러한 결과를 합성 데이터 평가에 관한 최근 방법론적 논의에서 발전된 의미에서 의도적으로 **구현 검증이며 예측 검증이 아님(implementation verification, not predictive validation)** 으로 프레이밍한다: 엔진은 자신이 구현하는 동일 표준에서 파생된 케이스에 대해 평가되는 결정론적 규칙 기반 계산기이다. 만점은 구현이 표준을 충실히 부호화하였음을 확인하며, 시스템이 보정 분포 외부의 플랜트 데이터로 일반화됨을 *확인하지 않는다*. 실제 플랜트 운영 또는 설계 기록에 대한 예측 검증은 현장 파일럿 배치를 요구하는 별개의 더 높은 기준이다(§8).
>
> [§6.7] **음성 사례(거짓양성 플래그 없음).** […] 중립적 배관 무결성 쿼리(`scripts/run_negative_case_rag.py`, `outputs/negative_case_pip_gold_003.md`)를 사용하여 이 케이스에 대해 실제 RAG 파이프라인을 실행하면, 시스템은 top-10에서 **0개 mandatory 히트와 10개 guidance 히트** 를 반환하며 최상위 결과는 `B-M-18-2026` (KOSHA 배관 수명 관리 기술 기준, guidance 분류)이다. 어떤 관할권 특이적 mandatory 의무도 발동되지 않는다. 이는 KOSHA RAG 계층이 모든 입력에 대해 발화하는 편향이 없음을 경험적으로 입증한다.

**근거**: `scripts/run_negative_case_rag.py`로 산출된 `outputs/negative_case_pip_gold_003.md`; `datasets/golden_standards/piping_golden_dataset_v1.json:PIP-GOLD-003` (검증된 명세); §6.1 구현 검증 프레이밍; §6.7 음성 사례 단락; `PAPER_JLP_REVISED_v3.md`의 §8 Limitations 1 및 5.

**보충 (실플랜트 파이프라인 실행 증거, 본 개정에서 추가).** 합성 데이터만에 의존한다는 우려를 프레이밍 논리뿐 아니라 양성적 증거로도 다루기 위해, 원고에 **Appendix A — Real-Plant Data-Sheet Validation (VES-REAL-001)** 을 추가하였습니다. VES-REAL-001은 가동 중인 석유화학 프로젝트에서 가져온 익명화된 저온 플레어 KO 드럼(SA-240 304/304L, 0.343 MPa(g) + 완전진공, 190 °C / -190 °C, ID 5,000 mm, T-T 20,400 mm)이며, 발주처/시공사/라이선서/인명/위치/문서 ID 식별자는 모두 사전에 제거되었습니다. 미수정 파이프라인 실행 결과 +190 °C 측에서 결정론적 UG-27 지배 두께 **7.237 mm** (엔진 신뢰도 `medium`, red flag 없음)가 산출되고, 명세 충실 쿼리에 대한 KOSHA RAG 검색은 top-10에서 **mandatory law_article 2건 + KOSHA 기술지침 8건**을 반환합니다(top-1 guidance: `M-111-2015` 압력용기의 용접설계에 관한 기술지침; rank-2 mandatory: 안전검사 고시 제9조). 좁은 한국어 용어 프로브는 추가로 **산업안전보건기준에 관한 규칙 제266조** (플레어·릴리프 라인 차단밸브 설치 금지)를 rank 5에서 표면화합니다. 전체 증거는 `scripts/run_real_case_ves001_rag.py` → `outputs/real_case_ves001_rag.{json,md}` 로 재현 가능합니다. 본 개정은 이를 외부 이중 검증이 아니라 **합성 골든 케이스 + 실플랜트 파이프라인 실행 증거(synthetic golden cases + real-plant pipeline-execution evidence)** 로 위치 짓습니다: 본 부록은 엔진과 검색 파이프라인이 실제 EPC 데이터 시트에서 깨끗하게 실행되고 관할권 관련 mandatory 조항을 표면화함을 입증하지만, 독립 감사된 참조에 대한 외부 정확도 검증을 구성하지는 않습니다(데이터 시트는 설계 입력을 제공하나 독립적으로 측정된 출력은 제공하지 않음). 실제 실패 결과에 대한 예측 검증은 여전히 미해결 향후 과제 항목으로 남습니다(§8 Limitation 1).

*독립 전문가 검증에 관하여:* 주 저자는 12년 이상의 석유화학 EPC 경력을 가진 공정 플랜트 엔지니어이며, 계산 엔진 규칙과 케이스 구성은 해당 도메인 실무를 인코딩한 것입니다. 이를 독립 검증으로 주장하지 않으며 — 그것은 분리된 전문가 패널을 요구합니다 — §8 Limitation 7로 명시하고 외부 KOSHA PSM 감사관 대비 전향적 향후 연구 항목으로 문서화합니다.

*벤치마크 구성 독립성에 관하여 (본 개정 패스에서 확장):* R2.3에서 이미 다룬 쿼리 집합 작성자 caveat에 더하여, §6.1은 이제 **Benchmark construction independence — known limitation** 단락을 명시적으로 포함하여, 본 논문의 세 합성 케이스 데이터셋(§6.1의 220 골든 케이스, §6.3의 60 학제 간 시나리오, §6.5의 50 검색 쿼리) 전부가 시스템 저자에 의해 구성되었음을 인정합니다. 독립적 현장 일반화를 주장하지 않으며, 벤치마크는 아키텍처 커버리지를 시험하기 위해 설계되었고 어느 독자라도 독립적인 벤치마크를 구성하여 재실행할 수 있도록 전체 공개됩니다. 독립적 제3자 벤치마크 구성은 향후 작업으로 문서화되어 있으며(§8 Limitation 7), 합성 케이스 편향 인정과 R2.3의 쿼리 편향 인정을 정렬시킵니다.

---

## Reviewer 2 답변

Reviewer 2께서는 본 주제를 *"highly aligned with modern challenges in digitalisation, PSM compliance, and multi-standard environments"* 로 지지해 주셨고, 출판 전에 강화가 필요한 8개 항목을 식별해 주셨습니다. 첨부된 리뷰 노트의 순서대로 각각을 아래에서 다룹니다.

### Comment R2.1: Clarification and strengthening of the regulatory basis (KOSHA relevance)

> *"While the manuscript clearly references KOSHA guidance (e.g., M-69-2012, C-C-23-2026, Article 256), the link between engineering outputs and regulatory obligations should be made more explicit. The authors should: provide clause-level citations and short extracts where possible; clarify whether requirements are mandatory vs guidance; demonstrate more explicitly how each obligation is not already covered in standard EPC workflows."*

**저자 답변:** 이 코멘트가 개정 논문 §4의 구조를 잡아 주었습니다. 감사드립니다. 세 개의 하위 요청을 직접적으로 다루었습니다. **(a) 조항 수준 인용 및 짧은 발췌.** §6.4 Case 3은 이제 영문 작업 번역(working translation)을 병기하여 **제256조의 한국어 원문 그대로** 를 재현합니다(한국어는 국가법령정보센터에 게재된 그대로, 그리고 시스템의 UTF-8 SQLite 인덱스에 있는 그대로 정확히 보존됨). 검색된 각 KOSHA Guide 참조(M-69-2012, C-C-23-2026, B-M-18-2026, C-C-75-2026)에 대해 Table 5는 영문 표제를 운반하며, 패시지별 인용은 인덱스로 추적 가능한 `(reference_code, chunk_id)` 튜플로 분해됩니다. **(b) 의무적(Mandatory) vs. 권고적(Guidance).** §4.3은 이제 검색된 모든 패시지에 부착되는 두 분류 규제 라벨을 정식화합니다: `mandatory` (법(Act) / 시행령 / 산업안전보건기준에 관한 규칙의 조항 — 미이행 시 운영자가 행정적·형사적 책임에 노출됨) 대 `guidance` (KOSHA 기술지침 — 그 자체로는 법적 구속력이 없으나 PSM 제출 패키지에 정기적으로 참조 편입됨). 이 라벨은 파싱 파이프라인의 `source_type` (`law_article` → mandatory; `guide_section` / `guide_chunk` → guidance)에서 도출되며 **LLM에 의해 추론되지 않습니다**. 제256조는 mandatory이고, 인용된 4개의 KOSHA Guide는 guidance입니다. Table 5는 이 라벨을 명시적으로 표면화합니다. **(c) 표준 EPC 워크플로우가 이를 다루지 않는 이유.** §4.4는 신설 소절로, 표준 EPC 배관/용기 패키지가 계산된 두께, 허용 응력, 점검 주기를 코드 한도와 대조하여 표화함으로써 해당 ASME/API 코드와의 컴플라이언스를 실증함을 설명합니다. 검토는 자기 분야의 국제 코드에는 전문이지만 일반적으로 한국의 *산업안전보건기준에 관한 규칙* 에는 전문이 아닌 학제 리드(discipline leads)에 의해 수행됩니다. KOSHA 측 컴플라이언스는 전통적으로 별도의 PSM 컨설턴트에 의해 별도의 문서 트랙에서 처리되며, 종종 EPC 설계가 동결된 이후입니다. 두 트랙은 KOSHA가 제출을 거부할 때에만 만납니다. 본 시스템은 그 갭 검출을 공학 계산 시점 자체로 옮깁니다.

**개정 원고 발췌** (§4.3 + §4.4):

> [§4.3] We distinguish two categories throughout this paper:
>
> - **Mandatory** (`mandatory`): provisions of *the Act* (`산업안전보건법`), *the Enforcement Decree*, or the *Rules on Occupational Safety and Health Standards* (`산업안전보건기준에 관한 규칙`). Article 256 ("Corrosion prevention") falls in this class. Non-fulfilment exposes the operator to administrative or criminal liability under the Act.
> - **Guidance** (`guidance`): KOSHA *technical guidelines* (e.g., `M-69-2012`, `C-C-23-2026`, `B-M-18-2026`, `C-C-75-2026`). These are not legally binding by themselves, but are routinely incorporated by reference into PSM submission packages and ministerial inspections, and a measurable deviation from a guideline is treated as a material finding in PSM audits.
>
> [§4.4] In Korean practice, KOSHA-side compliance is traditionally handled by a separate PSM consultant on a different documentation track, often after the EPC design has frozen. The two tracks meet only when KOSHA rejects a submission. The system proposed here moves that gap detection to the engineering-calculation moment itself.
>
> *역문:* [§4.3] 본 논문 전반에 걸쳐 두 분류를 구분한다:
>
> - **Mandatory** (`mandatory`): *산업안전보건법*, *시행령*, 또는 *산업안전보건기준에 관한 규칙* 의 조항. 제256조("부식 방지")가 이 분류에 속한다. 미이행은 법에 따라 운영자를 행정적 또는 형사적 책임에 노출시킨다.
> - **Guidance** (`guidance`): KOSHA *기술지침* (예: `M-69-2012`, `C-C-23-2026`, `B-M-18-2026`, `C-C-75-2026`). 그 자체로는 법적 구속력이 없으나, PSM 제출 패키지와 부처 점검에 정기적으로 참조 편입되며, 지침으로부터의 측정 가능한 이탈은 PSM 감사에서 실질적 지적사항으로 처리된다.
>
> [§4.4] 한국 실무에서 KOSHA 측 컴플라이언스는 전통적으로 별도의 PSM 컨설턴트에 의해 별도의 문서 트랙에서 처리되며, 종종 EPC 설계가 동결된 이후이다. 두 트랙은 KOSHA가 제출을 거부할 때에만 만난다. 본 논문이 제안하는 시스템은 그 갭 검출을 공학 계산 시점 자체로 옮긴다.

**근거**: `PAPER_JLP_REVISED_v3.md`의 §4.3 (Mandatory vs Guidance), §4.4 (표준 EPC 워크플로우가 이를 다루지 않는 이유), §6.4 Case 3 제256조 verbatim 한국어 원문과 영어 working translation 병기, Table 5 (KOSHA 인용 품질 및 규제 분류).

### Comment R2.2: Reproducibility and methodological transparency

> *"The architecture is well described conceptually, but the study would benefit from: more detailed explanation of the calculation engines and orchestration logic; clearer description of synthetic dataset generation; formalisation of the RAG query and prompting strategy."*

**저자 답변:** 이 코멘트로 인해 세 가지 구체적 추가가 이루어졌습니다. 감사드립니다. **(a) 계산 엔진 및 오케스트레이션.** §3은 라우팅에 사용되는 결정론적 상태 기계(`src/orchestrator/state_machine.py`)와 오케스트레이터(`src/orchestrator/pipeline.py`)를 명명합니다. §5.1 (Table 1)은 7개 엔진, 각각이 구현하는 표준, 소스 파일 경로를 나열합니다. §5.2는 명시적 Layer-4 임계값(2% 경고, 5% 에스컬레이션)을 포함한 4계층 하이브리드 검증을 상술하고, §5.3은 10개의 사전 정의된 도메인 쌍에 대한 학제 간 검증기를 문서화합니다(`src/cross_discipline/validator.py`, 쌍 집합은 `docs/specs/MASTER_ORCHESTRATOR_SPEC_V0.1.md`에 문서화됨). §6.6 내부 절제 표(Table 7b)는 `scripts/run_layer_ablation.py`로 계산되며, 완전히 재현 가능합니다. **(b) 합성 데이터셋 생성.** §6.1은 이제 생성 절차를 기술합니다: 각 케이스는 적용 가능한 표준 [16, 17] (ASME, API, IEEE, IEC, ACI, AISC)의 참조 계산 예제에서 도출됩니다. 경계 및 실패 모드 케이스는 **체계적 파라미터 섭동(systematic parameter perturbation)** (예: 벽두께를 계산된 최소치를 향해 감소, 유체 염화물 농도를 부식 속도 임계값을 가로질러 상승)에 의해 생성되며, 섭동된 파라미터와 예상되는 적색 플래그 분류가 각 케이스와 함께 기록됩니다. 수용 임계값은 임계 케이스에 대해 ±1%, 비임계 케이스에 대해 ±3%로 진술되며, 목표 적색 플래그 검출률 100%, 표준 인용 커버리지 100%입니다. 220-케이스 전체 데이터셋은 AGPL-3.0으로 공개됩니다. **(c) RAG 쿼리 및 프롬프팅 전략.** §4.2는 이제 검색 파이프라인을 정식화합니다: 개념 인지 쿼리 빌더가 계산 맥락을 한국어 자연어 쿼리로 변환합니다. 각 쿼리 개념은 큐레이트된 동의어로 확장됩니다(`corrosion ↔ 부식 ↔ corrosion rate ↔ CR`); 개념 절은 `AND`로 결합되고 한 개념 내의 동의어 변형은 `OR`로 결합됩니다. 엄격 확장이 히트를 반환하지 않을 때 **느슨한 확장 `OR` 폴백(loose expanded `OR` fallback)** 이 호출됩니다. 기본 top-k = 10. Qwen 2.5 7B Instruct 시스템 프롬프트는 출력을 세 절(핵심 결론 / 패시지 인덱스가 있는 규제 정당화 / 인용 인덱스가 있는 실무적 권고)로 제약하며, 모델은 공급된 맥락에 존재하지 않는 규제 사실을 결코 도입하지 않도록 지시받습니다 — 인용 추적 가능성 정밀도는 **구성에 의해 100%** 입니다(§6.7).

**개정 원고 발췌** (§4.2):

> At query time, the calculation context (material, fluid composition, design pressure / temperature, computed remaining life, red-flag set) is converted into a Korean natural-language query by a **concept-aware query builder**. Each query concept is expanded with curated synonyms (e.g., `corrosion ↔ 부식 ↔ corrosion rate ↔ CR`), concept clauses are joined with `AND`, and synonym variants within a concept are joined with `OR`. When the strict expansion returns no hits, a **loose expanded `OR` fallback** is invoked. […] The model is instructed never to introduce regulatory facts not present in the supplied context. Every advisory must point back to a retrievable `(reference_code, chunk_id)` tuple in the SQLite index, giving citation-traceability precision of 100% by construction.
>
> *역문:* 쿼리 시점에, 계산 맥락(material, fluid composition, design pressure / temperature, computed remaining life, red-flag set)은 **개념 인지 쿼리 빌더(concept-aware query builder)** 에 의해 한국어 자연어 쿼리로 변환된다. 각 쿼리 개념은 큐레이트된 동의어로 확장되고(예: `corrosion ↔ 부식 ↔ corrosion rate ↔ CR`), 개념 절은 `AND`로 결합되며 한 개념 내의 동의어 변형은 `OR`로 결합된다. 엄격 확장이 히트를 반환하지 않을 때 **느슨한 확장 `OR` 폴백** 이 호출된다. […] 모델은 공급된 맥락에 존재하지 않는 규제 사실을 결코 도입하지 않도록 지시받는다. 모든 권고는 SQLite 인덱스의 검색 가능한 `(reference_code, chunk_id)` 튜플로 다시 가리켜야 하며, 이는 구성에 의해 100%의 인용 추적 가능성 정밀도를 부여한다.

**근거**: §3 (오케스트레이터 + 상태 기계), §4.2 (RAG 쿼리 및 프롬프팅), §5.1 Table 1 (엔진 및 표준), §5.2 (명시적 임계값 포함 4계층), §5.3 (학제 간 검증기), §6.1 (골든 데이터셋 생성 절차), `docs/publication/CODE_MAP.md` (코드-논문 매핑); `scripts/run_layer_ablation.py`, `scripts/dump_ablation_hits.py`, `scripts/bootstrap_ci_rag.py`, `scripts/run_negative_case_rag.py` (모두 원고에서 참조됨).

### Comment R2.3: Validation and statistical rigor

> *"The evaluation relies heavily on synthetic datasets with near-perfect scores. This is acceptable for a proof-of-feasibility study, but the authors should: clearly position results as implementation verification rather than predictive validation; add uncertainty discussion or sensitivity analysis; expand or better justify the retrieval benchmark size and representativeness."*

**저자 답변:** 감사드립니다. 세 가지 하위 요청을 그대로 채택하였습니다. **(a) 구현 검증 프레이밍.** §6.1은 이제 "Calculation Accuracy on the Golden Dataset (**implementation verification**)"으로 재제목화되었으며, 프레이밍 단락은 이 구분을 채택합니다: *"We deliberately frame these results as **implementation verification, not predictive validation**, in the sense developed in recent methodological discussions of synthetic-data evaluation"* (블라인드 리뷰 형식 준수를 위해 본문 표현은 리뷰어 직접 귀속(attribution)을 피합니다). 결론도 이 프레이밍을 반영합니다. **(b) 불확실성 논의 / 민감도 분석.** §6.6은 이제 불확실성의 주요 원천을 표면화하는 민감도 분석 단락을 포함합니다: 합성 시드(더 넓은 시드 집합은 차단 비율을 이동시킬 수 있음)와 벤치마크 크기(1,327-문서 코퍼스에 대해 50개 쿼리, 구성에 의해 표적화됨). 헤드라인 검색 지표에 대해서는 **페어드 부트스트랩 95% CI** (Table 6, `outputs/rag_bootstrap_ci_report.md`, n=50, 1,000회 재표집, seed = 20260508)를 보고합니다: Recall@1 +0.30 페어드 CI [+0.14, +0.48] (0 배제); MRR@10 +0.2189 페어드 CI [+0.09, +0.35] (0 배제); **Recall@3 +0.12 페어드 CI [−0.02, +0.26] (0 포함); Recall@5 +0.12 페어드 CI [−0.02, +0.26] (0 포함)** — 이는 정직하게 보고되며, 헤드라인 검색 주장은 §6.5, §6.6, §9에서 Recall@1과 MRR@10만으로 좁혀지고, Recall@3/Recall@5는 1차 근거가 아닌 완전성을 위한 점추정치로 보고됩니다. 또한 전체 Recall@1 (Enhanced)에 대한 표준 오차를 `sqrt(p(1-p)/n)` (n=50, p=0.7400)로부터 0.062로 보고합니다. 학제 간 절제의 aligned-boundary와 aligned-failure에 대한 +1.0 델타는 범주적이며 CI를 요구하지 않습니다. **(c) 벤치마크 크기 및 대표성.** §6.5는 표본 크기 정당화 단락을 포함합니다: 다섯 규제 대상 그룹은 케이스 스터디가 입증한 세 KOSHA 부가 가치 패턴(잔여 수명 문서화, RBI 트리거, 부식 방지)을 모두 커버하기 위해 선택되었습니다. 그룹당 10개 쿼리는 각 기저 규제 대상의 가용한 별개 패러프레이징을 포화시키지 않으면서 Recall@K 분산 분석을 지원하는 최소치입니다. 그룹 수준 지표는 그룹 특이적 약점(예: 제256조가 1.0000이 아닌 0.7000 Enhanced R@5)을 가시화하기 위해 전체 평균 외에 Table 6b에서도 보고됩니다. 큐레이트 특성을 명시적으로 한계 3(§8)으로 인정합니다.

**개정 원고 발췌** (§6.5 + §6.6 민감도 단락):

> The Recall@1 and MRR@10 improvements are statistically distinguishable from zero at the 95% paired-bootstrap level. The Recall@3 and Recall@5 improvements are *not* statistically distinguishable from zero on this benchmark (lower-bound = −0.02 in both cases) — the point estimates are positive but a benchmark of this size and target distribution cannot rule out chance for K ∈ {3, 5}. The headline retrieval claim of the paper therefore relies on the Recall@1 and MRR@10 improvements; we report Recall@3/Recall@5 for completeness rather than as primary evidence.
>
> [§6.6 sensitivity] The Recall@3 and Recall@5 deltas of +0.12 each have paired CIs of **[−0.02, +0.26]** and are *not* statistically distinguishable from zero on a benchmark of this size. The cross-discipline ablation deltas of +1.0 on aligned boundary and aligned failure subsets are categorical (every case in those subsets is blocked under the validator and none are blocked without it), giving a deterministic separation that does not require a confidence interval.
>
> *역문:* Recall@1과 MRR@10의 개선은 95% 페어드 부트스트랩 수준에서 0과 통계적으로 구분 가능하다. Recall@3과 Recall@5의 개선은 이 벤치마크에서 0과 통계적으로 구분 *되지 않는다* (두 경우 모두 하한 = −0.02) — 점추정치는 양이지만, 이 크기와 표적 분포의 벤치마크는 K ∈ {3, 5}에 대해 우연을 배제할 수 없다. 따라서 본 논문의 헤드라인 검색 주장은 Recall@1과 MRR@10의 개선에 의존하며, Recall@3/Recall@5는 1차 근거가 아닌 완전성을 위해 보고한다.
>
> [§6.6 민감도] Recall@3과 Recall@5의 +0.12 델타는 각각 페어드 CI **[−0.02, +0.26]** 을 가지며 이 크기의 벤치마크에서 0과 통계적으로 구분 *되지 않는다*. 학제 간 절제의 aligned boundary 및 aligned failure 하위집합에 대한 +1.0 델타는 범주적이며(이들 하위집합의 모든 케이스가 검증기 하에서 차단되고 검증기 없이는 어느 케이스도 차단되지 않음), 신뢰 구간을 요구하지 않는 결정론적 분리를 제공한다.

**근거**: §6.1 구현 검증 프레이밍; §6.5 표본 크기 정당화 + Tables 6 및 6b; §6.6 민감도 단락; `scripts/bootstrap_ci_rag.py` (n=50, 1,000회 재표집, seed = 20260508)에서 산출된 `outputs/rag_bootstrap_ci_report.md`; §8 Limitations 1 및 3.

*후기 보강 (개정 이후):* recall 분석을 K=10까지 확장했습니다 (Appendix B.2, `outputs/rag_retrieval_extended.md`). Enhanced FTS 곡선은 K=3부터 0.8621에서 포화하고, Plain FTS 곡선은 K∈{9, 10}에서 0.8012까지 계속 상승합니다; Enhanced − Plain 페어드 차이의 95% 부트스트랩 CI는 K∈{1, 2}에서만 0을 배제합니다. 또한 검색 실패 인벤토리 (Appendix B.4)를 공개하여 K=5 miss 모두를 두 진단 카테고리 중 하나로 태그합니다 — 7건 중 6건이 `paraphrase_too_loose`에 해당 — 잔존하는 약점을 숨기지 않고 검사 가능하게 만들었습니다.

*후기 보강 (쿼리 생성 독립성, 피어 리딩 피드백 반영):* §6.5는 이제 50개 쿼리가 시스템 설계자와 동일인에 의해 작성되었음을 명시적으로 인정합니다. 편향 위험을 완화하기 위해 (a) 시스템 내부 동의어 목록이 아닌 KOSHA 기술지침 표제 및 확립된 한국 공학 어휘에서 도출된 그럴듯한 공학적 패러프레이징으로 쿼리 구성을 제한하였고, (b) 전체 쿼리 집합을 `datasets/kosha_rag/rag_eval_queries.json` 으로 독립 검사를 위해 공개하였으며, (c) 위의 실패 인벤토리를 보고하였습니다 — 7건 중 6건이 `paraphrase_too_loose`에 속하며, 이는 독립적으로 작성된 쿼리 집합도 노출시킬 실패 모드입니다. 분리된 어노테이터 풀에 의한 독립 쿼리 집합 작성은 향후 작업 항목으로 문서화되어 있습니다(§8 Limitation 7).

### Comment R2.4: Application scope — HAZOP clarification

> *"The manuscript would benefit from clarifying that the proposed approach is best suited for: knowledge-based or AI-assisted HAZOP support, where structured data and rules can be leveraged and not a replacement for conventional dynamic HAZOP, which remains a brainstorming-based, multidisciplinary workshop process relying on expert judgement and interaction."*

**저자 답변:** 감사드립니다. 이 입장을 그대로 채택하여 네 곳에서 명시화하였습니다. **§2.6** 은 이제 다음과 같이 진술합니다: *"The proposed framework is intentionally complementary to — not a replacement for — established process-safety methods […] HAZOP identifies process deviations through expert-led, multidisciplinary workshops […] None of these methods natively encodes jurisdiction-specific statutory obligations. The present system fills that gap as a **compliance co-pilot** active at four touchpoints."* **§7.2** 는 이를 Table 8(리뷰어가 요청한 방법 비교 표 — R2.7 참조)과 네 가지 운영 접점(HAZOP 이전, 설계 검토, RBI, 디지털 트윈 운영)으로 정교화합니다. **§7.3** 은 *"HAZOP scope: knowledge-based / AI-assisted, not a replacement for dynamic HAZOP"* 라는 전용 소절로, 리뷰어의 표현을 거의 그대로 사용합니다. **§9 결론** 은 다음과 같이 위치를 재진술합니다: *"The framework is positioned as a **compliance co-pilot** for HAZOP, RBI, and digital-twin workflows, not as a replacement for them."* **핵심 정의(Key Definitions)** 의 "Compliance co-pilot" 항목이 포함됩니다.

**개정 원고 발췌** (§7.3):

> The system supports **knowledge-based or AI-assisted HAZOP**: it surfaces structured regulatory data and rule-based prompts that a HAZOP facilitator can incorporate into the workshop. It **is not** a replacement for conventional dynamic HAZOP, which remains a brainstorming-based, multidisciplinary workshop relying on expert judgement, inter-discipline interaction, and human pattern recognition that no current AI system reproduces. The role of the proposed framework in a HAZOP context is to ensure that the workshop starts with a regulatory baseline that already encodes the jurisdiction-specific obligations and to flag during the workshop any deviation node that maps to a known KOSHA trigger.
>
> *역문:* 시스템은 **지식 기반 또는 AI 보조 HAZOP** 을 지원한다: HAZOP 진행자가 워크숍에 통합할 수 있는 구조화된 규제 데이터와 규칙 기반 프롬프트를 표면화한다. 시스템은 전통적 동적 HAZOP의 대체재가 **아니며**, 동적 HAZOP은 전문가 판단, 학제 간 상호작용, 그리고 어떤 현재 AI 시스템도 재현하지 못하는 인간 패턴 인식에 의존하는 브레인스토밍 기반의 다학제 워크숍으로 남는다. HAZOP 맥락에서 제안 프레임워크의 역할은 워크숍이 관할권 특이적 의무를 이미 부호화한 규제 베이스라인으로 시작되도록 보장하고, 워크숍 동안 알려진 KOSHA 트리거에 매핑되는 모든 일탈 노드를 플래그하는 데에 있다.

**근거**: `PAPER_JLP_REVISED_v3.md`의 §2.6, §7.2 + Table 8, §7.3 (전용 HAZOP 범위 소절), §9 결론, 핵심 정의 ("Compliance co-pilot").

### Comment R2.5: Fitness-for-Service (FFS) vs EPC standards

> *"The relationship between fitness-for-service (e.g., API 579) and EPC design standards (e.g., ASME, API design codes) should be explained more clearly. In particular: how FFS outputs interact with regulatory obligations; whether the system treats FFS as design validation, operational assessment, or both; how this affects compliance detection in the proposed framework."*

**저자 답변:** 감사드립니다. 이 코멘트는 이제 §7.4(논의의 전용 소절)입니다. 본 소절은 API 579-1 적합성 평가(fitness-for-service) [17]가 EPC 설계 표준(ASME, API 설계 코드)과 두 개의 독립 축을 따라 상호작용함을 설명합니다: 사용 중 열화에 대한 정량적 잔여 수명 및 수용 방법론으로 설계 단계 코드를 **보완(supplement)** 하며, 일부 KOSHA 점검 트리거 및 문서화 요건이 그 자체로 FFS-도출 양(잔여 수명, 부식 속도)에 조건화되어 있기 때문에 규제 의무와 **인터페이스(interface)** 합니다. 제안 시스템은 FFS를 **둘 모두** 로 취급합니다 — 설계 단계에서 열화 시나리오에 적용될 때는 설계 검증 입력으로, 사용 중 점검 데이터에 적용될 때는 운영 평가로. 오케스트레이션은 두 모드에서 동일합니다: 계산 엔진이 FFS 양을 산출하고, 4계층 검증이 수치 일관성을 확인하며, 학제 간 검증기가 하류 결합 효과를 점검하고, KOSHA RAG 계층이 FFS 양을 그것이 발동하는 모든 관할권 특이적 의무에 다시 매핑합니다(예: 임계값 미만의 잔여 수명은 M-69-2012 문서화를 발동; 임계값 초과의 부식 속도는 제256조 절차적 의무를 발동). 이 이중 모드 처리는 컴플라이언스 검출이 방법론 전환 없이 자산의 수명 주기에 걸쳐 따르도록 합니다.

**개정 원고 발췌** (§7.4):

> API 579-1 fitness-for-service (FFS) [17] interacts with EPC design standards (ASME, API design codes) along two independent axes: it **supplements** design-stage codes with a quantitative remaining-life and acceptance methodology for in-service degradation, and it **interfaces** with regulatory obligations because some KOSHA inspection-trigger and documentation requirements are themselves conditioned on FFS-derived quantities (remaining life, corrosion rate). The present system treats FFS as **both** a design-validation input (when applied at the engineering stage to a degraded scenario) **and** an operational assessment (when applied to in-service inspection data). The orchestration is identical in both modes […] This dual-mode treatment allows compliance detection to follow the asset across its lifecycle without a methodology switch.
>
> *역문:* API 579-1 적합성 평가(FFS) [17]는 EPC 설계 표준(ASME, API 설계 코드)과 두 개의 독립 축을 따라 상호작용한다: 사용 중 열화에 대한 정량적 잔여 수명 및 수용 방법론으로 설계 단계 코드를 **보완(supplement)** 하고, 일부 KOSHA 점검 트리거 및 문서화 요건이 그 자체로 FFS-도출 양(잔여 수명, 부식 속도)에 조건화되어 있기 때문에 규제 의무와 **인터페이스(interface)** 한다. 본 시스템은 FFS를 **둘 모두** 로 취급한다 — 설계 단계에서 열화 시나리오에 적용될 때는 설계 검증 입력, 사용 중 점검 데이터에 적용될 때는 운영 평가. 오케스트레이션은 두 모드에서 동일하다 […] 이 이중 모드 처리는 컴플라이언스 검출이 방법론 전환 없이 자산의 수명 주기에 걸쳐 따르도록 한다.

**근거**: `PAPER_JLP_REVISED_v3.md`의 §7.4 (FFS vs EPC 표준) 및 ASME Section VIII Div.1과 API 510에 더하여 API 579-1을 이미 나열하는 Table 1의 "Pressure Vessels" 행; 참고문헌 [17].

### Comment R2.6: Figures and structure improvements

> *"The manuscript would benefit significantly from: a system architecture diagram; a RAG workflow diagram; improved visualisation of cross-discipline coupling logic."*

**저자 답변:** 감사드립니다. 이 코멘트는 R1.4와 중첩됩니다. 5개의 도표가 추가되었습니다(모두 라이브 데이터에 대해 `scripts/generate_paper_figures.py`로부터 생성됨): **Figure 1** (전체 시스템 아키텍처: 오케스트레이터, 공유 4계층 검증을 갖는 7개 도메인 계산 서비스, 학제 간 검증기, 온프레미스 LLM을 갖는 KOSHA Regulatory RAG 계층); **Figure 2** (Regulatory RAG 워크플로우: 계산 맥락 → 개념 인지 한국어 쿼리 구성 → 동의어 확장 및 OR 폴백을 갖는 BM25 FTS5 검색 → 인용 인덱스를 갖는 구조화된 그라운딩 생성); **Figure 3** (학제 간 결합 로직: 10개 사전 정의된 도메인 쌍, 트리거 조건, 결합 차단 결정의 오케스트레이션 파이프라인 하류 효과); **Figure 4** (학제 간 절제 60 시나리오: 시나리오 집합별 차단 카운트, 검증기 OFF vs ON; 총 0 → 26, +43.3%); **Figure 5** (규제 대상 그룹별 Recall 및 MRR, Plain BM25 vs Enhanced). Figure 4 캡션은 옛 25가 아닌 v3-보정된 26 수치를 반영합니다.

**개정 원고 발췌** (Figure 1, 2, 3 캡션):

> *Figure 1. Overall system architecture: orchestrator, seven domain calculation services with shared four-layer verification, cross-discipline validator, and KOSHA Regulatory RAG layer with on-premises LLM.*
>
> *Figure 2. Regulatory RAG workflow: calculation context to concept-aware Korean query construction, BM25 FTS5 retrieval with synonym expansion and OR fallback, structured grounding generation with citation indices.*
>
> *Figure 3. Cross-discipline coupling logic: ten predefined domain pairs (piping-vessel, electrical-rotating, civil-rotating, instrumentation-electrical, etc.), trigger conditions, and downstream effect of a coupling-block decision on the orchestration pipeline.*
>
> *역문:* *Figure 1. 전체 시스템 아키텍처: 오케스트레이터, 공유 4계층 검증을 갖는 7개 도메인 계산 서비스, 학제 간 검증기, 그리고 온프레미스 LLM을 갖는 KOSHA Regulatory RAG 계층.*
>
> *Figure 2. Regulatory RAG 워크플로우: 계산 맥락에서 개념 인지 한국어 쿼리 구성으로, 동의어 확장 및 OR 폴백을 갖는 BM25 FTS5 검색, 인용 인덱스를 갖는 구조화된 그라운딩 생성.*
>
> *Figure 3. 학제 간 결합 로직: 10개 사전 정의된 도메인 쌍(piping-vessel, electrical-rotating, civil-rotating, instrumentation-electrical 등), 트리거 조건, 그리고 결합 차단 결정의 오케스트레이션 파이프라인 하류 효과.*

**근거**: `docs/publication/figures/fig_1_system_architecture.png`, `fig_2_rag_workflow.png`, `fig_3_cross_discipline.png`, `fig_4_ablation.png`, `fig_5_retrieval_metrics.png`; `scripts/generate_paper_figures.py`.

### Comment R2.7: Method-comparison table — Regulatory RAG vs HAZOP / RBI / Digital Twin

> *"Method | Main purpose | Weakness | Regulatory RAG value: HAZOP — Identify process deviations — Often manual and workshop-based — Adds regulation-linked prompts and missing legal obligations; RBI — Optimize inspection based on risk — Focuses mainly on equipment degradation — Adds jurisdiction-specific inspection duties; Digital Twin — Live/near-live plant model — May not know legal obligations — Adds compliance intelligence layer; Regulatory RAG — Retrieve applicable laws/standards — Depends on corpus quality — Bridges engineering + legal compliance. Best use is not to replace HAZOP/RBI, but to act as a compliance co-pilot. […] Auditor — After work is done; Advisor — While work is being done."*

**저자 답변:** 감사드립니다. 리뷰어가 작성한 방법 비교 표는 §7.2에 **Table 8** 로 본질적으로 그대로 재현되며, 저널 스타일을 위한 사소한 표현 다듬기가 있습니다. 네 가지 운영 접점(HAZOP 이전, 설계 검토, RBI, 디지털 트윈 운영)이 표 아래에 나열됩니다. Auditor 대 Advisor 시간적 역할 대비는 §7.2 끝의 별도 표(**Table 9**)로 다룹니다. 시스템을 *Digital Compliance Auditor*, *Automated PSM Checker* (PSM = SEVESO / OSHA / KOSHA 프레임워크), 그리고 *Real-time Regulatory Advisor* 로 보는 리뷰어의 프레이밍을 채택하며, 이러한 어구는 §7.2에 작성된 그대로 등장합니다.

**개정 원고 발췌** (Table 8 + Auditor/Advisor):

> **Table 8. Method Comparison — HAZOP / RBI / Digital Twin / Regulatory RAG**
>
> | Method | Main purpose | Weakness | Regulatory RAG value-add |
> |---|---|---|---|
> | HAZOP | Identify process deviations | Manual, workshop-based; expert-availability dependent | Adds regulation-linked prompts and surfaces missing legal obligations to the workshop |
> | RBI | Optimise inspection based on risk | Focuses primarily on equipment degradation; jurisdiction-blind | Adds jurisdiction-specific inspection-trigger duties (e.g., KOSHA RBI triggers above API 510 calendar) |
> | Digital Twin | Live or near-live plant model | Models physical state, not legal state | Adds a compliance intelligence layer over the live state |
> | **Regulatory RAG (this work)** | Retrieve applicable laws and standards conditioned on calculation context | Depends on corpus quality and freshness | Bridges engineering calculations and legal compliance |
>
> In process-safety terms, the system functions as a *Digital Compliance Auditor*, an *Automated PSM Checker* (PSM = SEVESO / OSHA / KOSHA frameworks), and a *Real-time Regulatory Advisor*.
>
> *역문:* **Table 8. 방법 비교 — HAZOP / RBI / Digital Twin / Regulatory RAG**
>
> | 방법 | 주된 목적 | 약점 | Regulatory RAG 부가가치 |
> |---|---|---|---|
> | HAZOP | 공정 일탈 식별 | 수작업, 워크숍 기반; 전문가 가용성 의존 | 규제 연계 프롬프트를 추가하고 누락된 법적 의무를 워크숍에 표면화 |
> | RBI | 위험 기반 점검 최적화 | 주로 장비 열화에 집중; 관할권 무시 | 관할권 특이적 점검 트리거 의무를 추가(예: API 510 달력을 상회하는 KOSHA RBI 트리거) |
> | Digital Twin | 라이브 또는 준-라이브 플랜트 모델 | 물리 상태를 모델링하나 법적 상태는 모델링하지 않음 | 라이브 상태 위에 컴플라이언스 인텔리전스 계층 추가 |
> | **Regulatory RAG (본 연구)** | 계산 맥락에 조건화된 적용 가능 법규 및 표준 검색 | 코퍼스 품질 및 최신성에 의존 | 공학 계산과 법적 컴플라이언스를 가교 |
>
> 공정 안전 용어로, 시스템은 *Digital Compliance Auditor*, *Automated PSM Checker* (PSM = SEVESO / OSHA / KOSHA 프레임워크), 그리고 *Real-time Regulatory Advisor* 로 기능한다.

**근거**: `PAPER_JLP_REVISED_v3.md`의 §7.2 Table 8 (방법 비교) 및 Table 9 (Auditor vs Advisor); 동일 표현이 §2.6에 요약됨.

### Comment R2.8: Acronyms and definitions section

> *"Given the multidisciplinary nature of the paper, a dedicated section listing: acronyms (e.g., RAG, PSM, RBI, FFS, KOSHA, EPC); key definitions (e.g., jurisdiction compliance gap, K-voting, coupling validation) would greatly improve readability and accessibility."*

**저자 답변:** 감사드립니다. Code-and-Data-Availability 절 다음에 두 전용 절을 추가하였습니다. **Acronyms** 는 ACI, AGPL, AISC, API, ASME, BM25, CR, EPC, FFS (per API 579-1/ASME FFS-1), FTS5, HAZOP, IEC, IEEE, KOSHA, LLM, MRR, PSM, RAG, RBI, RL을 다루는 19행 표입니다. **Key Definitions** 는 리뷰어가 명시한 정확한 용어(jurisdiction compliance gap, K-voting, coupling validation)와 본 논문에서 실질적으로 사용되는 세 추가 용어(implementation verification, compliance co-pilot, mandatory vs guidance)를 다루는 6개 항목 목록이며, 각 항목은 그것이 조작화되는 절을 가리킵니다.

**개정 원고 발췌** (Acronyms + Key Definitions):

> | Acronym | Expansion |
> |---|---|
> | EPC | Engineering, Procurement, and Construction |
> | FFS | Fitness-For-Service (per API 579-1/ASME FFS-1) |
> | KOSHA | Korea Occupational Safety and Health Agency |
> | PSM | Process Safety Management |
> | RAG | Retrieval-Augmented Generation |
> | RBI | Risk-Based Inspection |
> *(full table includes 19 entries)*
>
> - **Jurisdiction compliance gap** — the set of regulatory obligations imposed by national statute or agency guideline (here, Korean PSM law and KOSHA technical guidelines) that are structurally absent from international engineering code calculations, such that a system may be technically code-compliant while remaining legally non-compliant under the applicable local jurisdiction (§7.1).
> - **K-voting** — a Layer-2 verification mechanism in which K=3 calculation paths execute in parallel using deliberately varied numerical strategies, with maximum relative deviation among outputs constrained to ≤ 1%; failure invokes a tiebreaker and, on persistence, raises a `no_consensus` flag (§5.2, §5.4).
> - **Coupling validation** — the cross-discipline check across ten predefined domain pairs that fires when an output of one discipline crosses a coupling threshold defined relative to another (§5.3).
>
> *역문:* | 약어 | 풀이 |
> |---|---|
> | EPC | Engineering, Procurement, and Construction (설계·조달·시공) |
> | FFS | Fitness-For-Service (적합성 평가, API 579-1/ASME FFS-1 기준) |
> | KOSHA | 한국산업안전보건공단 |
> | PSM | Process Safety Management (공정안전관리) |
> | RAG | Retrieval-Augmented Generation (검색 증강 생성) |
> | RBI | Risk-Based Inspection (위험 기반 점검) |
> *(전체 표는 19개 항목 포함)*
>
> - **관할권 컴플라이언스 갭(Jurisdiction compliance gap)** — 국가 법령 또는 기관 지침에 의해 부과된 규제 의무(여기서는 한국 PSM 법령 및 KOSHA 기술지침) 중 국제 공학 코드 계산에 구조적으로 부재한 집합으로서, 시스템이 기술적으로 코드 컴플라이언트이면서도 적용 가능한 현지 관할권 하에서 법적으로 비컴플라이언트인 상태로 남을 수 있도록 하는 것(§7.1).
> - **K-voting** — K=3개의 계산 경로가 의도적으로 다양화된 수치 전략을 사용하여 병렬 실행되는 Layer-2 검증 기제로, 출력 간 최대 상대 편차가 ≤ 1%로 제약된다. 실패는 타이브레이커를 호출하고, 지속 시 `no_consensus` 플래그를 띄운다(§5.2, §5.4).
> - **결합 검증(Coupling validation)** — 한 학제의 출력이 다른 학제에 대해 정의된 결합 임계값을 가로지를 때 발화하는 10개 사전 정의된 도메인 쌍에 걸친 학제 간 점검(§5.3).

**근거**: `PAPER_JLP_REVISED_v3.md`의 Acronyms 표(19개 항목) 및 Key Definitions 절(6개 항목).

---

## Reviewer 3 답변

Reviewer 3께서는 본 주제를 *"very interesting"* 으로, 공학 정확성과 규제 컴플라이언스 간의 사각지대를 *"rare and valuable"* 로 평가하셨고, 두 별개 항목을 지적하셨습니다: K-voting 설계 근거의 부재와 JLP 형식 스타일.

### Comment R3.1: K-voting design rationale — why this choice and why those layers

> *"The author should explain why K-voting is chosen and why it needs those layers."*

**저자 답변:** 감사드립니다. 이 코멘트가 §5.4(*"Why three paths and a 1% tolerance? — K-voting design rationale"* 라는 제목의 신규 전용 소절)를 촉발하였습니다. 본 소절은 세 가지 직교적 설계 결정을 명시적으로 정당화합니다. **(i) 경로 수.** 두 경로는 불일치를 검출할 수 있으나 해소할 수 없습니다. 세 경로는 단일 비교로 다수결 의미를 부여하며, 이는 전형적인 수치 공학 실패 모드(두 경로가 일치하는 가운데 한 경로가 표류)를 포착합니다. 다섯 경로 이상은 비례적으로 더 높은 구현 비용 및 동기화 오버헤드로 한계 커버리지 이득을 제공합니다. 이 선택은 [11]에서 연구된 원래의 3-버전 베이스라인과 일치합니다. **(ii) 허용오차.** 1% 임계값은 골든 데이터셋에서 가장 엄격한 수용 허용오차(§6.1에 따라 임계 케이스에 대해 ±1%)에 대해 보정된 것입니다. 이보다 엄격한 임계값은 경로 간 합법적 부동소수점 반올림 차이로부터 발생하는 거짓양성 합의 실패를 생성할 것이고, 더 느슨한 임계값은 실제 코딩 오류를 가릴 것입니다. **(iii) 독립성의 범위.** 완전한 N-버전 프로그래밍은 상관 버그(correlated bugs)를 격퇴하기 위해 독립적으로 작성된 구현을 요구합니다. 우리는 그 수준의 독립성을 주장하지 않습니다 — 세 경로는 동일 저자와 동일 표준 인용 표를 공유합니다. 이 한계를 명시화하여 리뷰어가 계층을 정확히 위치 지을 수 있게 합니다: 여기서 K-voting은 주로 수치 정밀도 및 순서 버그를 보호하며, 표준 해석의 체계적 개념적 오류를 보호하는 것은 **아닙니다**. 또한 §6.6 (Layer-B 절제, Table 7b)에서 K-voting이 그 자체로는 새로운 검출에 기여하지 않는 **검증 품질** 계층임을 적시합니다 — 그 역할은 거짓양성 수치 정밀도 인공물을 억제하는 것입니다. 이 위치 짓기는 각 계층의 책임을 별개이고 시험 가능하게 함으로써 리뷰어의 "그 계층이 왜 필요한가" 질문을 다룹니다.

**개정 원고 발췌** (§5.4):

> *Number of paths.* Two paths can detect inconsistency but cannot resolve it (the system has no tiebreaker). Three paths give a majority-vote semantics: the typical failure mode in numerical engineering code is one path drifting from two that agree, which a 3-path configuration captures with a single comparison. […]
>
> *Tolerance.* The 1% relative-deviation threshold is calibrated against the tightest acceptance tolerance in the golden dataset (±1% for critical cases; §6.1). A tolerance smaller than this would generate false-positive consensus failures arising from legitimate floating-point rounding differences between the three paths; a larger tolerance would mask real coding errors.
>
> *Scope of independence.* Full N-version programming requires independently authored implementations to defeat correlated bugs. We do not claim that level of independence; the three paths share the same author and the same standard-citation tables. K-voting here therefore protects primarily against numerical-precision and ordering bugs, not against systematic conceptual errors in the standard interpretation. We make this limitation explicit so reviewers can correctly position the layer.
>
> *역문:* *경로 수.* 두 경로는 불일치를 검출할 수 있으나 해소할 수 없다(시스템에 타이브레이커가 없음). 세 경로는 다수결 의미를 부여한다: 수치 공학 코드에서 전형적 실패 모드는 두 경로가 일치하는 가운데 한 경로가 표류하는 것이며, 이를 3-경로 구성이 단일 비교로 포착한다. […]
>
> *허용오차.* 1% 상대 편차 임계값은 골든 데이터셋에서 가장 엄격한 수용 허용오차(§6.1에 따라 임계 케이스에 대해 ±1%)에 대해 보정된 것이다. 이보다 작은 허용오차는 세 경로 간 합법적 부동소수점 반올림 차이로부터 발생하는 거짓양성 합의 실패를 생성할 것이고, 더 큰 허용오차는 실제 코딩 오류를 가릴 것이다.
>
> *독립성의 범위.* 완전한 N-버전 프로그래밍은 상관 버그를 격퇴하기 위해 독립적으로 작성된 구현을 요구한다. 우리는 그 수준의 독립성을 주장하지 않는다; 세 경로는 동일 저자와 동일 표준 인용 표를 공유한다. 따라서 여기서 K-voting은 주로 수치 정밀도 및 순서 버그를 보호하며, 표준 해석의 체계적 개념적 오류를 보호하지 않는다. 우리는 이 한계를 명시화하여 리뷰어가 계층을 정확히 위치 지을 수 있게 한다.

**근거**: §5.4 (Why three paths and a 1% tolerance? — K-voting 설계 근거); §5.2 (4계층 아키텍처 자체); §6.6 Table 7b (`scripts/run_layer_ablation.py`로 계산되는 계층의 직교성); 참고문헌 [11] Avizienis 1985.

### Comment R3.2: JLP formatting and scientific-article style

> *"The manuscript is written in a more technical and professional style than a typical scientific article. The author should carefully review the manuscript formatting guidelines."*

**저자 답변:** 이 관찰에 감사드립니다. 개정 원고는 전반적으로 JLP 과학 논문 스타일로 재구조화되었습니다: 명시적 수치와 CI를 갖는 단일 단락 초록(Abstract); Introduction → Related Work → System Architecture → KOSHA Regulatory Knowledge Layer → Engines & Verification → Experiments → Discussion → Limitations → Conclusion → Acknowledgements → Code/Data Availability → Acronyms → Key Definitions → References의 구조화된 순서; 본문에서 번호로 참조되는 번호화된 표와 도표(Table 1부터 Table 9까지; Figure 1부터 Figure 5까지); §1에서 명시적 연구 질문(RQ1, RQ2) 진술; 전반에 걸쳐 1인칭 복수("We have…"); 가용 시 전체 DOI를 갖는 JLP 번호 스타일 참고문헌. 또한 잔존하는 기술 보고서 관용구를 제거하고, 인라인 서술이 아닌 해당 절 본문 옆의 소스 파일 인용으로 구현 경로를 통합하였습니다. 길이, 인용 수, 절 순서는 인접 주제 영역의 최근 JLP 논문을 따릅니다.

**개정 원고 발췌** (Abstract 도입부 + §1 RQ1/RQ2):

> [Abstract] Engineering calculation workflows in Korean process plant projects span seven disciplines across the full plant lifecycle. Existing practice relies on discipline-siloed tools that miss cross-discipline coupling hazards and cannot enforce Korean-jurisdiction regulatory requirements beyond international code compliance. […]
>
> [§1] **RQ1.** What additional cross-discipline coupling hazards does the proposed multi-discipline verification architecture detect compared with independent single-domain calculations, across a predefined set of domain pairs?
>
> **RQ2.** Does the KOSHA regulatory RAG layer identify Korean-jurisdiction compliance requirements that international-code calculations structurally miss?
>
> *역문:* [Abstract] 한국 공정 플랜트 프로젝트의 공학 계산 워크플로우는 전체 플랜트 수명 주기에 걸쳐 7개 학제에 걸친다. 기존 실무는 학제별 사일로 도구에 의존하여 학제 간 결합 위험을 놓치며 국제 코드 컴플라이언스를 넘어선 한국 관할권 규제 요건을 강제할 수 없다. […]
>
> [§1] **RQ1.** 제안된 다학제 검증 아키텍처는 사전 정의된 도메인 쌍 집합에 걸쳐 독립적인 단일 도메인 계산과 비교하여 어떤 추가적 학제 간 결합 위험을 검출하는가?
>
> **RQ2.** KOSHA regulatory RAG 계층은 국제 코드 계산이 구조적으로 놓치는 한국 관할권 컴플라이언스 요건을 식별하는가?

**근거**: `PAPER_JLP_REVISED_v3.md`의 절 순서 및 구조(Abstract → §1 → §2 → … → §9 → Acknowledgements → Code/Data → Acronyms → Definitions → References); Tables 1–9; Figures 1–5; 19개 번호 항목과 DOI를 갖는 참고문헌 목록.

---

## 마무리

편집장님과 세 분 리뷰어 분들께 다시 한번 감사드립니다. 본 개정은 논문의 엄밀성, 명확성, 정직성을 실질적으로 향상시켰습니다 — 특히 계산 결과의 구현 검증 프레이밍, Recall@3/Recall@5에서 통계적 검정력의 한계를 드러내는 페어드 부트스트랩 CI, 26개 학제 간 히트의 실패 모드별 분할, PIP-GOLD-003에 대한 검증된 음성 사례 실행, FFS 대 EPC 소절, K-voting 설계 근거, 그리고 방법 비교 표가 그러합니다. 개정 원고가 이제 *Journal of Loss Prevention in the Process Industries* 의 기준을 충족하기를 바라며, 추가 피드백을 기다리겠습니다.

진심으로 감사드리며,

김유용

위스콘신-매디슨 대학교

ykim288@wisc.edu / yuyongkim@gmail.com

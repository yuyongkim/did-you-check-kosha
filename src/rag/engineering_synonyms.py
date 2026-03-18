"""
Engineering domain synonym dictionary for KOSHA RAG BM25 query expansion.
Used in src/rag/local_kosha_rag.py :: make_fts_query()

Usage:
    from src.rag.engineering_synonyms import ENGINEERING_SYNONYMS, expand_query_tokens

    expanded = expand_query_tokens(["부식", "배관"])
    # -> ["부식", "corrosion", "손상", "열화", "침식", "녹", "배관", "piping", "pipe", ...]
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

ENGINEERING_SYNONYMS: Dict[str, List[str]] = {

    # ── 공통 ──────────────────────────────────────────────────────────────────
    "부식": ["corrosion", "손상", "열화", "침식", "녹"],
    "잔여수명": ["remaining life", "잔존수명", "수명", "잔여내용연수", "remaining_life"],
    "검사": ["inspection", "점검", "시험", "확인", "진단"],
    "두께": ["thickness", "벽두께", "판두께"],
    "안전밸브": ["safety valve", "압력방출밸브", "relief valve", "PRV", "PSV"],
    "위험성평가": ["risk assessment", "위험도평가", "리스크평가", "HAZOP", "PHA"],
    "유지보수": ["maintenance", "정비", "보수", "수리"],
    "설계압력": ["design pressure", "최고허용압력", "MAWP"],
    "설계온도": ["design temperature", "최고허용온도"],
    "결함": ["defect", "결점", "이상", "불량", "손상부위"],
    "누출": ["leak", "누설", "유출"],
    "비파괴검사": ["NDT", "비파괴시험", "NDE", "초음파탐상", "방사선투과"],
    "법령": ["statute", "법규", "규정", "고시", "조항"],
    "안전보건": ["occupational safety", "산업안전", "OSHA"],
    "공정안전": ["process safety", "PSM", "process safety management"],
    "위험성": ["risk", "hazard", "위험", "리스크"],
    "모니터링": ["monitoring", "감시", "관리", "점검"],

    # ── 배관 (Piping) ──────────────────────────────────────────────────────────
    "배관": ["piping", "pipe", "관", "배관계통", "배관시스템"],
    "배관재질": ["pipe material", "관재료", "배관재료"],
    "부식속도": ["corrosion rate", "부식률", "침식속도", "CR"],
    "최소두께": ["minimum thickness", "최소요구두께", "t_min"],
    "검사주기": ["inspection interval", "검사간격", "점검주기"],
    "수압시험": ["hydrotest", "수압검사", "압력시험"],
    "배관지지": ["pipe support", "지지물", "행거"],
    "플랜지": ["flange", "플랜지이음", "플랜지접합"],
    "용접": ["weld", "welding", "용접부", "용접이음"],
    "배관수명": ["piping life", "pipe life", "배관 잔여수명"],
    "사워서비스": ["sour service", "황화수소", "H2S", "sour", "NACE"],
    "클로라이드": ["chloride", "염소이온", "Cl", "chloride stress corrosion"],

    # ── 정기기 / 압력용기 (Vessel / Static Equipment) ─────────────────────────
    "압력용기": ["pressure vessel", "용기", "반응기", "탑", "드럼", "열교환기"],
    "정기기": ["static equipment", "pressure vessel", "heat exchanger", "tower", "drum"],
    "동체": ["shell", "동판", "몸체"],
    "경판": ["head", "끝판"],
    "노즐": ["nozzle", "관접속부", "개구부"],
    "부식여유": ["corrosion allowance", "부식허용량", "CA"],
    "잔여두께": ["remaining thickness", "현재두께", "실측두께", "actual thickness"],
    "FFS": ["fitness for service", "사용적합성평가", "운전적합성", "API 579"],
    "RBI": ["risk based inspection", "위험기반검사", "위험도기반검사", "C-C-23"],
    "API510": ["API 510", "압력용기검사", "vessel inspection"],
    "내압": ["internal pressure", "내부압력"],
    "잔여수명평가": ["remaining life assessment", "수명평가", "M-69", "API 579-1"],

    # ── 회전기기 (Rotating Equipment) ─────────────────────────────────────────
    "회전기기": ["rotating equipment", "회전기계", "펌프", "압축기", "터빈"],
    "진동": ["vibration", "떨림", "이상진동", "vibration_mm_per_s"],
    "베어링": ["bearing", "베어링온도", "축받이", "bearing temperature"],
    "정렬": ["alignment", "축정렬", "얼라인먼트"],
    "씰": ["seal", "mechanical seal", "메카니컬씰", "패킹"],
    "윤활": ["lubrication", "윤활유", "오일"],
    "임펠러": ["impeller", "회전차", "날개차"],
    "오버홀": ["overhaul", "분해점검", "대수리"],

    # ── 전기 (Electrical) ──────────────────────────────────────────────────────
    "전기설비": ["electrical equipment", "전기기기", "전력설비"],
    "아크플래시": ["arc flash", "아크섬광", "아크방전"],
    "차단기": ["circuit breaker", "breaker", "개폐기"],
    "변압기": ["transformer", "변압기건전도"],
    "접지": ["grounding", "earthing", "접지설비"],
    "방폭": ["explosion proof", "방폭설비", "방폭기기", "Ex"],
    "고조파": ["harmonic", "THD", "고조파왜곡", "total harmonic distortion"],
    "절연": ["insulation", "절연저항", "절연내력"],

    # ── 계장 (Instrumentation / SIS) ──────────────────────────────────────────
    "계장": ["instrumentation", "instrument", "계측기기"],
    "SIL": ["safety integrity level", "안전무결성수준", "SIL2", "SIL3"],
    "SIS": ["safety instrumented system", "안전계장시스템", "ESD"],
    "교정": ["calibration", "검교정", "조정"],
    "드리프트": ["drift", "편차", "오차", "drift_pct"],
    "센서": ["sensor", "감지기", "검출기", "transmitter", "발신기"],
    "제어밸브": ["control valve", "조절밸브", "CV"],
    "PFD": ["probability of failure on demand", "요구시고장확률", "pfdavg"],

    # ── 철골 (Steel Structure) ─────────────────────────────────────────────────
    "철골": ["steel structure", "강구조물", "철구조물"],
    "부재": ["member", "구조부재", "강재"],
    "처짐": ["deflection", "변형", "휨", "deflection_ratio"],
    "좌굴": ["buckling", "좌굴하중"],
    "부식손실": ["corrosion loss", "단면손실", "두께손실", "corrosion_loss_percent"],
    "파이프랙": ["pipe rack", "배관지지대", "배관랙"],
    "활용률": ["utilization", "demand-capacity ratio", "DC ratio", "dc_ratio"],

    # ── 토목 / 콘크리트 (Civil) ────────────────────────────────────────────────
    "콘크리트": ["concrete", "RC구조", "철근콘크리트"],
    "균열": ["crack", "크랙", "균열폭", "crack_width"],
    "박리": ["spalling", "박락", "탈락", "spalling_area_percent"],
    "기초": ["foundation", "기초구조물", "푸팅"],
    "침하": ["settlement", "기초침하", "부동침하", "foundation_settlement_mm"],
    "중성화": ["carbonation", "탄산화", "콘크리트중성화"],
    "철근부식": ["rebar corrosion", "철근열화", "염해"],

    # ── KOSHA / 법령 특화 ─────────────────────────────────────────────────────
    "공정안전관리": ["PSM", "공정안전", "process safety management", "공정안전보고서"],
    "안전검사": ["safety inspection", "정기검사", "법정검사", "KOSHA 검사"],
    "중대산업사고": ["major industrial accident", "중대사고", "major accident"],
    "MSDS": ["물질안전보건자료", "SDS", "화학물질정보", "safety data sheet"],
    "유해위험설비": ["hazardous equipment", "유해설비", "위험설비"],
    "안전작업허가": ["PTW", "작업허가서", "permit to work"],
    "변경관리": ["MOC", "management of change", "설비변경"],
    "비상조치": ["emergency response", "비상계획", "ERP"],
    "HAZOP": ["위험과운전분석", "공정위험성분석", "hazard and operability study"],
    "부식방지": ["corrosion prevention", "부식 방지", "제256조", "Article 256"],
    "위험기반검사": ["RBI", "risk based inspection", "C-C-23-2026"],
    "배관수명관리": ["piping life management", "B-M-18-2026", "배관 수명관리"],
    "부식위험성": ["corrosion risk", "부식 위험성평가", "C-C-75-2026"],
}

def _dedupe_preserve_order(values: Iterable[str]) -> List[str]:
    seen: set[str] = set()
    result: List[str] = []
    for value in values:
        item = value.strip()
        if not item or item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def _build_phrase_candidates() -> List[Tuple[str, List[str]]]:
    candidates: List[Tuple[str, List[str]]] = []
    for head, variants in ENGINEERING_SYNONYMS.items():
        for candidate in [head, *variants]:
            if " " not in candidate:
                continue
            tokens = [part.lower() for part in candidate.split() if part]
            if tokens:
                candidates.append((candidate, tokens))
    candidates.sort(key=lambda item: len(item[1]), reverse=True)
    return candidates


PHRASE_CANDIDATES = _build_phrase_candidates()


def extract_query_terms(query: str) -> List[str]:
    """
    Collect query terms for synonym expansion.

    Besides raw whitespace tokens, this also preserves multi-word dictionary
    heads and variants already present in the query so reverse lookup can map
    phrases like "pressure vessel" back to the Korean head term.
    """
    raw_tokens = [token.strip() for token in query.split() if token.strip()]
    if not raw_tokens:
        return []

    lowered = [token.lower() for token in raw_tokens]
    matched_terms: List[str] = []
    index = 0
    while index < len(raw_tokens):
        matched = False
        for phrase, phrase_tokens in PHRASE_CANDIDATES:
            width = len(phrase_tokens)
            if lowered[index : index + width] == phrase_tokens:
                matched_terms.append(phrase)
                index += width
                matched = True
                break
        if matched:
            continue
        matched_terms.append(raw_tokens[index])
        index += 1

    return _dedupe_preserve_order(matched_terms)


def expand_query_tokens(tokens: List[str]) -> List[str]:
    """
    Given a list of query tokens, expand each token with its synonyms.
    Returns a flat deduplicated list preserving original order first.

    Example:
        expand_query_tokens(["부식", "배관"])
        -> ["부식", "corrosion", "손상", ..., "배관", "piping", ...]
    """
    seen: set[str] = set()
    result: List[str] = []

    for token in _dedupe_preserve_order(tokens):
        seen.add(token)
        result.append(token)

        # Forward lookup: Korean -> English/variants
        synonyms = ENGINEERING_SYNONYMS.get(token, [])
        for syn in synonyms:
            if syn not in seen:
                seen.add(syn)
                result.append(syn)

        # Reverse lookup: if token is an English/code term, find its Korean head
        if not synonyms:
            token_lower = token.lower()
            for head, variants in ENGINEERING_SYNONYMS.items():
                if any(v.lower() == token_lower for v in variants):
                    if head not in seen:
                        seen.add(head)
                        result.append(head)
                    for v in variants:
                        if v not in seen:
                            seen.add(v)
                            result.append(v)
                    break

    return result


def expand_query(query: str) -> List[str]:
    """
    Expand a natural-language query into a deduplicated BM25 term list.
    """
    return expand_query_tokens(extract_query_terms(query))


def expand_query_groups(query: str) -> List[List[str]]:
    """
    Expand a natural-language query into concept groups.

    The caller can join groups with AND while keeping synonyms within each
    group joined with OR.
    """
    groups: List[List[str]] = []
    for term in extract_query_terms(query):
        groups.append(expand_query_tokens([term]))
    return groups


def make_expanded_fts_query(query: str) -> str:
    """
    Build a concept-aware FTS query for the live retrieval path.

    Concepts are joined with AND, while synonyms within each concept are joined
    with OR.
    """
    groups = expand_query_groups(query)
    if not groups:
        return query.strip()

    clauses = ["(" + " OR ".join(f'"{term}"' for term in group) + ")" for group in groups]
    return " AND ".join(clauses)


def make_loose_fts_query(query: str) -> str:
    """
    Build a recall-oriented fallback query by OR-joining all expanded terms.
    """
    expanded_terms = expand_query(query)
    if not expanded_terms:
        return query.strip()

    return " OR ".join(f'"{term}"' for term in expanded_terms)

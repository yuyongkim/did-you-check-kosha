#!/usr/bin/env python3
"""Resolve stable direct article URLs for major law/rule corpora on law.go.kr."""

from __future__ import annotations

import gzip
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.rag.law_article_metadata import parse_article_parts


LAW_ARTICLES_PATH = ROOT / "datasets" / "kosha" / "normalized" / "law_articles.json"
RETRIEVAL_CORPUS_PATH = ROOT / "datasets" / "kosha" / "normalized" / "retrieval_corpus.jsonl.gz"
SEARCH_URL = "https://www.law.go.kr/lsScListR.do?menuId=1&subMenuId=15&tabMenuId=81"
JO_TREE_URL = "https://www.law.go.kr/joListTreeRInc.do"
TARGET_CATEGORIES = {"1", "2", "3", "4", "8", "9"}


def fetch_text(url: str, *, data: bytes | None = None) -> str:
    request = Request(
        url,
        data=data,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
        },
    )
    with urlopen(request, timeout=30) as response:  # noqa: S310
        return response.read().decode("utf-8", errors="ignore")


def strip_tags(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text)).strip()


def search_current_law(law_name: str) -> Dict[str, str] | None:
    params = {
        "q": law_name,
        "section": "lawNm",
        "outmax": "20",
        "p2": "3",
        "p9": "2,4",
        "p18": "0",
        "p19": "1,3",
        "fsort": "10,41,21,31",
        "pg": "1",
    }
    html = fetch_text(SEARCH_URL, data=urlencode(params).encode("utf-8"))
    direct_lsi_seq = re.search(r'id="direct1" value="([^"]+)"', html)
    direct_title = re.search(r'id="direct3" value="([^"]+)"', html)
    direct_ef_yd = re.search(r'id="direct4" value="([^"]+)"', html)
    if direct_lsi_seq and direct_title and direct_ef_yd:
        if strip_tags(direct_title.group(1)) == law_name:
            return {"lsiSeq": direct_lsi_seq.group(1), "efYd": direct_ef_yd.group(1)}

    pattern = re.compile(
        r"<td class=\"tl\">\s*<a href=\"#\" onclick=\"lsViewWideAll\('([^']+)','([^']+)','([^']+)',\$\(this\),'([^']*)','([^']*)','([^']*)','([^']*)'\);[^\"]*\">\s*(.*?)\s*</a>",
        re.S,
    )
    for match in pattern.finditer(html):
        lsi_seq, ef_yd, _li_id, _p4, _p7, _nw_yn, _tab, raw_title = match.groups()
        title = strip_tags(raw_title.split("[시행", 1)[0])
        if title == law_name:
            return {"lsiSeq": lsi_seq, "efYd": ef_yd}
    return None


def fetch_jo_tree(lsi_seq: str, ef_yd: str) -> List[Dict[str, Any]]:
    params = {
        "lsiSeq": lsi_seq,
        "section": "Jo",
        "chrClsCd": "010202",
        "efYd": ef_yd,
        "joEfYd": ef_yd,
        "ancYnChk": "0",
    }
    payload = fetch_text(f"{JO_TREE_URL}?{urlencode(params)}")
    data = json.loads(payload)
    if not isinstance(data, list):
        return []
    return [item for item in data if isinstance(item, dict)]


def build_direct_url(lsi_seq: str, ef_yd: str, jo_no: str, jo_br_no: str) -> str:
    params = {
        "docCls": "jo",
        "lsiSeq": lsi_seq,
        "joNo": jo_no,
        "joBrNo": jo_br_no,
        "chrClsCd": "010202",
        "ancYnChk": "0",
        "efYd": ef_yd,
        "docTypeNo": "0",
        "nwYn": "Y",
        "paras": f"joa1{jo_no}a2{jo_br_no}",
    }
    return "https://www.law.go.kr/lsScJoRltInfoR.do?" + urlencode(params)


def update_rows(rows: Iterable[Dict[str, Any]]) -> tuple[List[Dict[str, Any]], Dict[str, Any]]:
    rows = [dict(row) for row in rows]
    law_names = sorted({str(row.get("law_name") or "") for row in rows if str(row.get("category")) in TARGET_CATEGORIES and row.get("law_name")})
    law_index: Dict[str, Dict[str, str]] = {}
    jo_tree_index: Dict[str, Dict[tuple[str, str], Dict[str, Any]]] = {}

    for law_name in law_names:
        search_info = search_current_law(law_name)
        if not search_info:
            continue
        law_index[law_name] = search_info
        jo_tree = fetch_jo_tree(search_info["lsiSeq"], search_info["efYd"])
        jo_tree_index[law_name] = {
            (str(item.get("joNo") or ""), str(item.get("joBrNo") or "")): item
            for item in jo_tree
            if item.get("joYn") == "Y"
        }

    resolved = 0
    for row in rows:
        category = str(row.get("category") or "")
        if category not in TARGET_CATEGORIES:
            continue
        law_name = str(row.get("law_name") or "")
        if law_name not in law_index:
            continue
        article_parts = parse_article_parts(str(row.get("title") or ""))
        if not article_parts:
            continue
        jo_no, jo_br_no = article_parts
        tree_item = jo_tree_index.get(law_name, {}).get((jo_no, jo_br_no))
        if tree_item is None:
            continue
        search_info = law_index[law_name]
        direct_url = build_direct_url(search_info["lsiSeq"], search_info["efYd"], jo_no, jo_br_no)
        row["direct_url"] = direct_url
        row["resolved_url"] = direct_url
        row["search_url"] = row.get("search_url") or row.get("resolved_url")
        row["lsiSeq"] = search_info["lsiSeq"]
        row["efYd"] = search_info["efYd"]
        resolved += 1

    stats = {
        "resolved_rows": resolved,
        "target_laws": len(law_names),
        "laws_with_search_hits": len(law_index),
    }
    return rows, stats


def rewrite_retrieval_corpus(rows: List[Dict[str, Any]]) -> None:
    with gzip.open(RETRIEVAL_CORPUS_PATH, "wt", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False))
            stream.write("\n")


def main() -> int:
    law_rows = json.loads(LAW_ARTICLES_PATH.read_text(encoding="utf-8"))
    if not isinstance(law_rows, list):
        raise RuntimeError("law_articles.json must contain a list")
    updated_laws, stats = update_rows(law_rows)
    LAW_ARTICLES_PATH.write_text(json.dumps(updated_laws, ensure_ascii=False, indent=2), encoding="utf-8")

    corpus_rows: List[Dict[str, Any]] = []
    with gzip.open(RETRIEVAL_CORPUS_PATH, "rt", encoding="utf-8") as stream:
        for line in stream:
            item = json.loads(line)
            if isinstance(item, dict):
                corpus_rows.append(item)
    updated_corpus, _ = update_rows(corpus_rows)
    rewrite_retrieval_corpus(updated_corpus)

    print(f"TARGET_LAWS={stats['target_laws']}")
    print(f"LAWS_WITH_SEARCH_HITS={stats['laws_with_search_hits']}")
    print(f"RESOLVED_ROWS={stats['resolved_rows']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

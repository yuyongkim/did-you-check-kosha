from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict
from urllib.parse import urlencode


REPO_ROOT = Path(__file__).resolve().parents[2]
LAW_SEARCH_BASE = "https://www.law.go.kr/lsSc.do"
OVERRIDE_PATH = REPO_ROOT / "config" / "law_article_link_overrides.json"


@lru_cache(maxsize=1)
def read_override_config() -> Dict[str, Any]:
    if not OVERRIDE_PATH.exists():
        return {"category_names": {}, "article_overrides": {}}
    return json.loads(OVERRIDE_PATH.read_text(encoding="utf-8"))


def law_search_url(query: str) -> str:
    params = urlencode({"query": query})
    return f"{LAW_SEARCH_BASE}?{params}"


def parse_article_label(title: str) -> str | None:
    match = re.match(r"(제\d+조(?:의\d+)?)", title.strip())
    if not match:
        return None
    return match.group(1)


def parse_article_number(title: str) -> int | None:
    match = re.match(r"제(\d+)조", title.strip())
    if not match:
        return None
    return int(match.group(1))


def parse_article_parts(title: str) -> tuple[str, str] | None:
    match = re.match(r"제(\d+)조(?:의(\d+))?", title.strip())
    if not match:
        return None
    jo_no = f"{int(match.group(1)):04d}"
    jo_br_no = f"{int(match.group(2) or 0):02d}"
    return jo_no, jo_br_no


def law_category_name(category: str) -> str:
    config = read_override_config()
    category_names = config.get("category_names", {})
    if isinstance(category_names, dict):
        return str(category_names.get(category, ""))
    return ""


def law_article_override(raw_id: str) -> Dict[str, Any]:
    config = read_override_config()
    overrides = config.get("article_overrides", {})
    if isinstance(overrides, dict):
        item = overrides.get(raw_id, {})
        if isinstance(item, dict):
            return item
    return {}


def build_law_article_metadata(raw_id: str, title: str, category: str, filepath: str = "") -> Dict[str, Any]:
    override = law_article_override(raw_id)
    law_name = str(override.get("law_name") or law_category_name(category) or "").strip()
    article_label = str(override.get("article_label") or parse_article_label(title) or "").strip()
    article_number = override.get("article_number")
    if article_number is None:
        article_number = parse_article_number(title)
    query_seed = str(override.get("query") or "").strip()
    if not query_seed:
        query_seed = " ".join(token for token in [law_name, title] if token).strip()

    direct_url = str(override.get("direct_url") or "").strip() or None
    search_url = str(override.get("search_url") or "").strip() or None
    if not search_url and query_seed:
        search_url = law_search_url(query_seed)

    resolved_url = filepath.strip() or direct_url or search_url
    return {
        "law_name": law_name or None,
        "article_label": article_label or None,
        "article_number": article_number,
        "query_seed": query_seed or None,
        "direct_url": direct_url,
        "search_url": search_url,
        "resolved_url": resolved_url,
    }

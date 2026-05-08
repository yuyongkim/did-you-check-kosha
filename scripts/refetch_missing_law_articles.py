#!/usr/bin/env python3
"""
Re-fetch the 12 KOSHA law-article rows whose `content` is empty.

Background
----------
`datasets/kosha/normalized/law_articles.json` has 3,102 rows; 12 have empty
`content`. They are silently dropped from the local SQLite FTS index by
`src/rag/local_kosha_rag.py:185-186` (the `if not raw_id or not content`
guard). For each missing row we try, in order:

  1. **KOSHA Smart-search API** — re-call
     `https://apis.data.go.kr/B552468/srch/smartSearch` with the row's
     ``doc_id`` (and the same category) using the service key from env or
     `frontend/.env.local`. Most rows whose title contains `삭제` (repealed
     article) are expected to return empty bodies — that is the *correct*
     answer, not a fix.
  2. **National Law Information Center direct URL** — when the row already
     has a `direct_url` field that points at `lsScJoRltInfoR.do`, fetch the
     HTML and extract the article body (best-effort scrape).

Outputs
-------
- ``outputs/kosha_missing_articles_report.md`` — per-id outcome:
  refetched OK, refetched but still empty (truly empty in source),
  refetch failed (network/auth blocker).
- If any row produced a non-empty body, the script writes
  ``datasets/kosha/normalized/law_articles.utf8.json`` with the new bodies
  patched in (only when that file already exists from
  `scripts/reencode_kosha_corpus.py`). Original `law_articles.json` is NEVER
  modified.

Hard rules
----------
- **No fabrication.** If both routes fail or return empty, the row is left
  empty and reported. We never invent body text.
- **Network may be blocked.** If the KOSHA API returns 401/403/blocked, we
  document the blocker and the author must re-run with credentials.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlencode
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "tools" / "kosha-ingestion" / "src"))

from kosha_ingestion.text_encoding import parse_json_bytes  # noqa: E402

DEFAULT_LAW_ORIGINAL = REPO_ROOT / "datasets" / "kosha" / "normalized" / "law_articles.json"
DEFAULT_LAW_UTF8 = REPO_ROOT / "datasets" / "kosha" / "normalized" / "law_articles.utf8.json"
DEFAULT_REPORT = REPO_ROOT / "outputs" / "kosha_missing_articles_report.md"

KOSHA_ENDPOINT = "https://apis.data.go.kr/B552468/srch/smartSearch"
ENV_KEYS = [
    "KOSHA_API_KEY_ENCODING",
    "KOSHA_API_KEY_ENCODED",
    "KOSHA_SERVICE_KEY",
    "KOSHA_API_KEY",
    "KOSHA_API_KEY_DECODING",
    "KOSHA_API_KEY_DECODED",
]


@dataclass
class Outcome:
    doc_id: str
    title: str
    category: str
    direct_url: Optional[str]
    is_repealed: bool  # title contains 삭제
    refetch_route: str = "none"  # "kosha_api" | "law_go_kr" | "none"
    refetched_ok: bool = False
    new_content_len: int = 0
    new_content_preview: str = ""
    blocker: Optional[str] = None  # short reason if not OK


# ---------- Service key helpers ---------- #

def parse_env_file(path: Path) -> Dict[str, str]:
    data: Dict[str, str] = {}
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        item = line.strip()
        if not item or item.startswith("#") or "=" not in item:
            continue
        k, v = item.split("=", 1)
        if k.strip():
            data[k.strip()] = v.strip()
    return data


def resolve_service_key() -> str:
    for key in ENV_KEYS:
        v = os.environ.get(key, "").strip()
        if v:
            return unquote(v)
    env_local = parse_env_file(REPO_ROOT / "frontend" / ".env.local")
    for key in ENV_KEYS:
        v = env_local.get(key, "").strip()
        if v:
            return unquote(v)
    return ""


# ---------- HTTP ---------- #

def fetch_url(url: str, timeout: int = 25, retries: int = 2) -> tuple[bytes, str, Optional[str]]:
    """Returns (body, content_type, error). Error is non-None when fetch failed."""
    last_err: Optional[str] = None
    for attempt in range(1, retries + 1):
        try:
            req = Request(url, headers={"Accept": "application/json, text/html"})
            with urlopen(req, timeout=timeout) as r:  # noqa: S310
                return r.read(), str(r.headers.get("Content-Type") or ""), None
        except HTTPError as e:
            last_err = f"HTTP {e.code} {e.reason}"
            if e.code not in {408, 429, 500, 502, 503, 504} or attempt >= retries:
                return b"", "", last_err
        except (URLError, TimeoutError) as e:
            last_err = f"{type(e).__name__}: {e}"
            if attempt >= retries:
                return b"", "", last_err
        time.sleep(min(2.0, 0.5 * attempt))
    return b"", "", last_err or "unknown error"


# ---------- Refetch routes ---------- #

def refetch_via_kosha_api(doc_id: str, category: str, service_key: str) -> tuple[Optional[str], Optional[str]]:
    """Returns (content_or_None, error_or_None). content_or_None == '' means API
    explicitly returned an empty body (truly empty in source)."""
    if not service_key:
        return None, "no service key (set KOSHA_API_KEY_ENCODING / KOSHA_SERVICE_KEY)"
    # The smart-search endpoint doesn't accept a doc_id filter directly; we issue
    # a search by the row's title text scoped to its category and look for the
    # row by exact doc_id.
    params = {
        "serviceKey": service_key,
        "pageNo": "1",
        "numOfRows": "10",
        "searchValue": doc_id,
        "category": category,
    }
    url = f"{KOSHA_ENDPOINT}?{urlencode(params)}"
    body, content_type, err = fetch_url(url)
    if err:
        return None, err
    try:
        data = parse_json_bytes(body, content_type=content_type)
    except Exception as e:  # noqa: BLE001
        return None, f"parse error: {e}"
    response = data.get("response") or {}
    header = response.get("header") or {}
    if str(header.get("resultCode") or "") not in {"00", ""}:
        return None, f"API resultCode={header.get('resultCode')} resultMsg={header.get('resultMsg')}"
    body_obj = response.get("body") or {}
    items_node = body_obj.get("items")
    items: List[Dict[str, Any]] = []
    if isinstance(items_node, dict):
        node = items_node.get("item")
        if isinstance(node, list):
            items.extend(x for x in node if isinstance(x, dict))
        elif isinstance(node, dict):
            items.append(node)
    for item in items:
        if str(item.get("doc_id") or "") == doc_id:
            content = str(item.get("content") or item.get("highlight_content") or "").strip()
            content = re.sub(r"<[^>]+>", " ", content)
            content = re.sub(r"\s+", " ", content).strip()
            return content, None  # may be empty string ("truly empty")
    return None, f"doc_id not found in {len(items)} returned items"


HTML_TAG_RE = re.compile(r"<[^>]+>")
SCRIPT_BLOCK_RE = re.compile(r"<script\b[^>]*>.*?</script>", flags=re.DOTALL | re.IGNORECASE)
STYLE_BLOCK_RE = re.compile(r"<style\b[^>]*>.*?</style>", flags=re.DOTALL | re.IGNORECASE)
# Heuristic markers that indicate we got the SPA shell instead of real content.
SPA_NOISE_MARKERS = (
    "function fileLayer",
    "ancYnChk 파라미터",
    "$('#hwptext",
    'jQuery("#hwptext',
)


def refetch_via_law_go_kr(direct_url: str) -> tuple[Optional[str], Optional[str]]:
    """Best-effort scrape of the NLIC (law.go.kr) article HTML.

    Returns (content, err) where:
      - content == non-empty str: real article body found
      - content == "": page found, body explicitly empty (repealed)
      - content is None: scrape failed (err describes why)

    The NLIC site is a SPA — many endpoints return only a JavaScript shell
    where the article is loaded asynchronously. We detect that and refuse to
    return the JS noise as a "recovered body".
    """
    if not direct_url:
        return None, "no direct_url"
    body, _, err = fetch_url(direct_url)
    if err:
        return None, err
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError:
        try:
            text = body.decode("euc-kr")
        except UnicodeDecodeError:
            return None, "could not decode HTML body"

    # Reject SPA shells outright.
    for marker in SPA_NOISE_MARKERS:
        if marker in text:
            return None, "law.go.kr returned SPA shell (no article body in HTML); needs JS-rendered fetch"

    # Strip script/style blocks first.
    cleaned = SCRIPT_BLOCK_RE.sub(" ", text)
    cleaned = STYLE_BLOCK_RE.sub(" ", cleaned)

    # Try to grab the article body div. The NLIC layout puts article text in
    # nodes like <div class="lsContent"> or <div class="bodyOnly">.
    m = re.search(
        r'<div[^>]*class="(?:lsContent|bodyOnly|contentBox|conScroll)[^"]*"[^>]*>(.*?)</div>',
        cleaned,
        flags=re.DOTALL,
    )
    chunk = m.group(1) if m else cleaned
    chunk = HTML_TAG_RE.sub(" ", chunk)
    chunk = chunk.replace("&nbsp;", " ").replace("&amp;", "&").replace("&quot;", '"').replace("&#39;", "'")
    chunk = re.sub(r"\s+", " ", chunk).strip()

    # If the chunk has too little Korean text to be a real article, treat as failure.
    hangul = sum(1 for c in chunk if "가" <= c <= "힣")
    if hangul < 10:
        return None, f"law.go.kr scrape produced no recognizable Korean body (hangul_chars={hangul})"

    if "삭제" in chunk[:40]:
        return chunk, None  # truly empty (repealed)
    return chunk, None


# ---------- Main ---------- #

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--law-articles-original", default=str(DEFAULT_LAW_ORIGINAL))
    p.add_argument("--law-articles-utf8", default=str(DEFAULT_LAW_UTF8))
    p.add_argument("--report-path", default=str(DEFAULT_REPORT))
    p.add_argument("--skip-network", action="store_true",
                   help="Don't attempt network calls; produce a report listing the 12 ids only.")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    src = Path(args.law_articles_original).resolve()
    utf8_path = Path(args.law_articles_utf8).resolve()
    report_path = Path(args.report_path).resolve()

    data = json.loads(src.read_text(encoding="utf-8"))
    missing = [r for r in data if not str(r.get("content", "") or "").strip()]
    print(f"[OK] found {len(missing)} rows with empty content (of {len(data)} total)")

    service_key = resolve_service_key()
    if args.skip_network:
        print("[INFO] --skip-network set; will not attempt API/HTTP refetch")
    elif not service_key:
        print("[WARN] no KOSHA service key found in env or frontend/.env.local")
    else:
        print(f"[OK] KOSHA service key resolved (len={len(service_key)})")

    outcomes: List[Outcome] = []
    new_bodies: Dict[str, str] = {}

    for row in missing:
        doc_id = str(row.get("id") or "")
        title = str(row.get("title") or "")
        category = str(row.get("category") or "")
        direct_url = row.get("direct_url")
        oc = Outcome(
            doc_id=doc_id,
            title=title,
            category=category,
            direct_url=direct_url if isinstance(direct_url, str) else None,
            is_repealed="삭제" in title,
        )

        if args.skip_network:
            oc.blocker = "network skipped (--skip-network)"
            outcomes.append(oc)
            continue

        # Route 1: KOSHA Smart-search API
        api_content: Optional[str] = None
        api_err: Optional[str] = None
        if service_key:
            api_content, api_err = refetch_via_kosha_api(doc_id, category, service_key)
            oc.refetch_route = "kosha_api"
            if api_content is not None:
                if api_content == "":
                    oc.refetched_ok = True
                    oc.blocker = "API returned empty content (truly empty / repealed)"
                else:
                    oc.refetched_ok = True
                    oc.new_content_len = len(api_content)
                    oc.new_content_preview = api_content[:200]
                    new_bodies[doc_id] = api_content
                    outcomes.append(oc)
                    continue
            else:
                oc.blocker = f"KOSHA API: {api_err}"

        # Route 2: law.go.kr direct URL (only if API didn't already return empty/OK)
        if oc.direct_url and not oc.refetched_ok:
            html_content, html_err = refetch_via_law_go_kr(oc.direct_url)
            oc.refetch_route = "law_go_kr"
            if html_content is not None:
                if html_content == "":
                    oc.refetched_ok = True
                    oc.blocker = (oc.blocker + " | " if oc.blocker else "") + "law.go.kr returned empty content"
                else:
                    oc.refetched_ok = True
                    oc.new_content_len = len(html_content)
                    oc.new_content_preview = html_content[:200]
                    new_bodies[doc_id] = html_content
            else:
                oc.blocker = (oc.blocker + " | " if oc.blocker else "") + f"law.go.kr: {html_err}"

        outcomes.append(oc)
        time.sleep(0.2)

    # If any new bodies AND utf8 file exists, patch them in.
    patched = 0
    if new_bodies and utf8_path.exists():
        utf8_data = json.loads(utf8_path.read_text(encoding="utf-8"))
        for r in utf8_data:
            rid = str(r.get("id") or "")
            if rid in new_bodies:
                r["content"] = new_bodies[rid]
                patched += 1
        utf8_path.write_text(json.dumps(utf8_data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[OK] patched {patched} new bodies into {utf8_path}")
    elif new_bodies and not utf8_path.exists():
        print(f"[WARN] {utf8_path} does not exist; new bodies NOT persisted. "
              "Run scripts/reencode_kosha_corpus.py first.")

    # Report
    write_report(outcomes, patched, report_path, service_key_present=bool(service_key))
    print(f"[OK] report -> {report_path}")
    return 0


def write_report(outcomes: List[Outcome], patched: int, path: Path, service_key_present: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    L: List[str] = []
    L.append("# KOSHA Missing Law-Article Bodies — Refetch Report\n\n")
    L.append(f"Total empty-content rows identified: **{len(outcomes)}** (of 3,102 in `law_articles.json`)\n\n")
    L.append(f"- KOSHA service key available: **{service_key_present}**\n")
    L.append(f"- Rows patched into `law_articles.utf8.json`: **{patched}**\n\n")

    ok = [o for o in outcomes if o.refetched_ok and o.new_content_len > 0]
    truly_empty = [o for o in outcomes if o.refetched_ok and o.new_content_len == 0]
    failed = [o for o in outcomes if not o.refetched_ok]
    repealed = [o for o in outcomes if o.is_repealed]

    L.append("## Summary\n\n")
    L.append(f"- Refetched OK with new body: **{len(ok)}**\n")
    L.append(f"- Refetched but source is truly empty (incl. repealed `삭제` articles): **{len(truly_empty)}**\n")
    L.append(f"- Refetch failed (network / auth blocker): **{len(failed)}**\n")
    L.append(f"- Rows whose title contains `삭제` (repealed): **{len(repealed)}** "
             "— for these an empty body is the *correct* state, not corruption.\n\n")

    L.append("## Per-id outcome\n\n")
    L.append("| # | doc_id | title | repealed | route | OK | new len | blocker |\n")
    L.append("|---|--------|-------|---------:|-------|----|--------:|---------|\n")
    for i, o in enumerate(outcomes, 1):
        title_short = (o.title[:60] + "…") if len(o.title) > 60 else o.title
        blocker = (o.blocker or "")[:120].replace("|", "\\|")
        L.append(
            f"| {i} | `{o.doc_id}` | {title_short} | {'Y' if o.is_repealed else ''} | "
            f"{o.refetch_route} | {'Y' if o.refetched_ok else 'N'} | "
            f"{o.new_content_len} | {blocker} |\n"
        )

    if ok:
        L.append("\n## Recovered bodies (preview)\n\n")
        for o in ok:
            L.append(f"### `{o.doc_id}` — {o.title}\n\n")
            L.append(f"length: {o.new_content_len} chars\n\n")
            L.append(f"```\n{o.new_content_preview}\n```\n\n")

    if failed and not service_key_present:
        L.append("\n## Author follow-up required\n\n")
        L.append(
            "The KOSHA Smart-search API requires a service key. None was found in\n"
            "the environment or `frontend/.env.local`. Re-run with the service\n"
            "key set:\n\n"
            "```\nKOSHA_API_KEY_ENCODING='<your encoded key>' "
            "python scripts/refetch_missing_law_articles.py\n```\n"
        )
    elif failed:
        L.append("\n## Author follow-up required\n\n")
        L.append(
            "The following ids could not be refetched. Inspect each `direct_url`\n"
            "manually on https://www.law.go.kr to confirm whether the source is\n"
            "truly empty (repealed) or the body needs to be backfilled.\n\n"
        )

    path.write_text("".join(L), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())

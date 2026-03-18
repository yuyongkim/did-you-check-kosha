#!/usr/bin/env python3
"""Download KOSHA smart-search corpus and build local snapshot files."""

from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlencode
from urllib.request import Request, urlopen

from kosha_ingestion.text_encoding import parse_json_bytes


REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.rag.law_article_metadata import build_law_article_metadata

DEFAULT_ENDPOINT = "https://apis.data.go.kr/B552468/srch/smartSearch"
DEFAULT_CATEGORIES = ["1", "2", "3", "4", "5", "7", "8", "9", "11"]
ENV_KEYS = [
    "KOSHA_API_KEY_ENCODING",
    "KOSHA_API_KEY_ENCODED",
    "KOSHA_SERVICE_KEY",
    "KOSHA_API_KEY",
    "KOSHA_API_KEY_DECODING",
    "KOSHA_API_KEY_DECODED",
]
RETRYABLE_STATUS = {408, 429, 500, 502, 503, 504}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync KOSHA smart-search corpus into local datasets.")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help="Smart search endpoint URL.")
    parser.add_argument(
        "--categories",
        default=",".join(DEFAULT_CATEGORIES),
        help="Comma-separated KOSHA categories (default: 1,2,3,4,5,7,8,9,11).",
    )
    parser.add_argument("--query", default="", help="Search query. Empty string means full category crawl.")
    parser.add_argument("--num-rows", type=int, default=200, help="Rows per page (default: 200).")
    parser.add_argument("--max-pages", type=int, default=0, help="Optional hard page cap (0 means unlimited).")
    parser.add_argument("--timeout", type=int, default=25, help="HTTP timeout seconds.")
    parser.add_argument("--retries", type=int, default=3, help="Retry attempts for transient failures.")
    parser.add_argument("--sleep-ms", type=int, default=120, help="Inter-page delay in milliseconds.")
    parser.add_argument(
        "--out-dir",
        default=str(REPO_ROOT / "datasets" / "kosha"),
        help="Output directory root.",
    )
    parser.add_argument("--service-key", default="", help="Optional service key override.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing output files.")
    return parser.parse_args(argv)


def parse_env_file(path: Path) -> Dict[str, str]:
    data: Dict[str, str] = {}
    if not path.exists():
        return data

    for line in path.read_text(encoding="utf-8").splitlines():
        item = line.strip()
        if not item or item.startswith("#") or "=" not in item:
            continue
        key, value = item.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key:
            data[key] = value
    return data


def resolve_service_key(explicit_value: str) -> str:
    if explicit_value.strip():
        return unquote(explicit_value.strip())

    for key in ENV_KEYS:
        value = os.environ.get(key, "").strip()
        if value:
            return unquote(value)

    env_local = parse_env_file(REPO_ROOT / "frontend" / ".env.local")
    for key in ENV_KEYS:
        value = env_local.get(key, "").strip()
        if value:
            return unquote(value)

    raise RuntimeError(
        "KOSHA service key is empty. Provide --service-key or set one of "
        + ", ".join(ENV_KEYS)
        + " in environment/frontend/.env.local."
    )


def ensure_list(value: Any) -> List[Dict[str, Any]]:
    if value is None:
        return []
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        return [value]
    return []


def request_json(url: str, timeout_sec: int, retries: int) -> Dict[str, Any]:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            request = Request(url, headers={"Accept": "application/json"}, method="GET")
            with urlopen(request, timeout=timeout_sec) as response:  # noqa: S310
                payload = response.read()
                content_type = str(response.headers.get("Content-Type") or "")
            return parse_json_bytes(payload, content_type=content_type)
        except HTTPError as exc:
            last_error = exc
            if exc.code not in RETRYABLE_STATUS or attempt >= retries:
                break
        except (URLError, TimeoutError) as exc:
            last_error = exc
            if attempt >= retries:
                break
        time.sleep(min(2.0, 0.35 * attempt))

    raise RuntimeError(f"Request failed after retries: {last_error}") from last_error


def extract_items(payload: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], int]:
    response = payload.get("response") or {}
    header = response.get("header") or {}
    result_code = str(header.get("resultCode", ""))
    result_msg = str(header.get("resultMsg", ""))
    if result_code != "00":
        raise RuntimeError(f"KOSHA API error: resultCode={result_code}, resultMsg={result_msg}")

    body = response.get("body") or {}
    total_count = int(body.get("totalCount") or 0)
    items_node = ((body.get("items") or {}).get("item")) if isinstance(body.get("items"), dict) else None
    items = ensure_list(items_node)

    total_media_node = body.get("total_media")
    if isinstance(total_media_node, dict):
        items.extend(ensure_list(total_media_node.get("media")))
    elif isinstance(total_media_node, list):
        items.extend(ensure_list(total_media_node))

    return items, total_count


def normalize_text(value: Any) -> str:
    text = str(value or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = (
        text.replace("&nbsp;", " ")
        .replace("&amp;", "&")
        .replace("&quot;", "\"")
        .replace("&#39;", "'")
    )
    text = re.sub(r"\s+", " ", text).strip()
    return text


def derive_guide_key(doc_id: str, title: str) -> str:
    item = doc_id.strip()
    if item.startswith("KOSHA07_") and re.search(r"_\d+$", item):
        return re.sub(r"_\d+$", "", item)
    title_base = title.split(" - ")[0].strip() if " - " in title else title.strip()
    return title_base or item or "UNKNOWN_GUIDE"


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_jsonl_gz(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, mode="wt", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False))
            stream.write("\n")


def fetch_category(
    endpoint: str,
    service_key: str,
    category: str,
    query: str,
    num_rows: int,
    timeout_sec: int,
    retries: int,
    sleep_ms: int,
    max_pages: int,
) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    page = 1
    api_total_count = 0
    dedup: Dict[str, Dict[str, Any]] = {}
    raw_rows = 0
    duplicate_count = 0

    while True:
        params = {
            "serviceKey": service_key,
            "pageNo": str(page),
            "numOfRows": str(num_rows),
            "searchValue": query,
            "category": category,
        }
        url = f"{endpoint}?{urlencode(params)}"
        payload = request_json(url, timeout_sec=timeout_sec, retries=retries)
        items, total_count = extract_items(payload)
        api_total_count = max(api_total_count, total_count)

        if not items:
            break

        for idx, item in enumerate(items, start=1):
            raw_rows += 1
            key = str(item.get("doc_id") or f"{category}:{page}:{idx}:{normalize_text(item.get('title'))}")
            if key in dedup:
                duplicate_count += 1
                continue
            row = dict(item)
            row["_fetched_category"] = category
            row["_fetched_page"] = page
            dedup[key] = row

        if (max_pages > 0 and page >= max_pages) or len(items) < num_rows:
            break

        page += 1
        if sleep_ms > 0:
            time.sleep(sleep_ms / 1000.0)

    stats = {
        "api_total_count": api_total_count,
        "raw_rows": raw_rows,
        "dedup_rows": len(dedup),
        "duplicate_rows": duplicate_count,
        "pages_fetched": page,
    }
    return list(dedup.values()), stats


def build_normalized_views(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    guides: Dict[str, Dict[str, Any]] = {}
    guide_sections: List[Dict[str, Any]] = []
    laws: List[Dict[str, Any]] = []
    retrieval_corpus: List[Dict[str, Any]] = []

    for row in rows:
        category = str(row.get("category") or row.get("_fetched_category") or "")
        doc_id = str(row.get("doc_id") or "")
        title = normalize_text(row.get("title"))
        content = normalize_text(row.get("content") or row.get("highlight_content"))
        score = float(row.get("score") or 0)
        filepath = str(row.get("filepath") or "").strip()
        keyword = normalize_text(row.get("keyword"))

        normalized = {
            "id": doc_id,
            "category": category,
            "title": title,
            "content": content,
            "score": score,
            "filepath": filepath or None,
            "keyword": keyword or None,
        }
        if category in {"1", "2", "3", "4", "5", "8", "9", "11"}:
            law_meta = build_law_article_metadata(
                raw_id=doc_id,
                title=title,
                category=category,
                filepath=filepath,
            )
            normalized.update(
                {
                    "law_name": law_meta.get("law_name"),
                    "article_label": law_meta.get("article_label"),
                    "article_number": law_meta.get("article_number"),
                    "query_seed": law_meta.get("query_seed"),
                    "direct_url": law_meta.get("direct_url"),
                    "search_url": law_meta.get("search_url"),
                    "resolved_url": law_meta.get("resolved_url"),
                }
            )
        retrieval_corpus.append(normalized)

        if category == "7":
            guide_key = derive_guide_key(doc_id, title)
            guide = guides.setdefault(
                guide_key,
                {
                    "guide_key": guide_key,
                    "guide_title": title.split(" - ")[0].strip() if " - " in title else title,
                    "section_count": 0,
                    "sections": [],
                    "keywords": set(),
                },
            )
            guide["sections"].append(
                {
                    "doc_id": doc_id,
                    "section_title": title,
                    "content": content,
                    "score": score,
                    "filepath": filepath or None,
                }
            )
            guide["section_count"] += 1
            if keyword:
                guide["keywords"].add(keyword)
            guide_sections.append(normalized)
        elif category in {"1", "2", "3", "4", "5", "8", "9", "11"}:
            laws.append(normalized)

    guide_docs: List[Dict[str, Any]] = []
    for item in guides.values():
        sections = sorted(item["sections"], key=lambda section: section["doc_id"])
        guide_docs.append(
            {
                "guide_key": item["guide_key"],
                "guide_title": item["guide_title"],
                "section_count": item["section_count"],
                "keywords": sorted(item["keywords"]),
                "sections": sections,
            }
        )
    guide_docs.sort(key=lambda entry: entry["guide_key"])

    laws.sort(key=lambda entry: entry["id"])
    guide_sections.sort(key=lambda entry: entry["id"])
    retrieval_corpus.sort(key=lambda entry: (entry["category"], entry["id"]))

    return {
        "guide_documents": guide_docs,
        "guide_sections": guide_sections,
        "law_articles": laws,
        "retrieval_corpus": retrieval_corpus,
    }


def maybe_remove_existing(paths: Iterable[Path], force: bool) -> None:
    existing = [path for path in paths if path.exists()]
    if not existing:
        return
    if not force:
        joined = "\n".join(f"- {path}" for path in existing)
        raise RuntimeError(
            "Output files already exist. Use --force to overwrite:\n" + joined
        )
    for path in existing:
        path.unlink()


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    started_at = datetime.now(timezone.utc)

    categories = [item.strip() for item in args.categories.split(",") if item.strip()]
    if not categories:
        raise RuntimeError("At least one category is required.")
    if args.num_rows < 1:
        raise RuntimeError("--num-rows must be >= 1.")

    service_key = resolve_service_key(args.service_key)
    out_dir = Path(args.out_dir).resolve()
    raw_dir = out_dir / "raw"
    normalized_dir = out_dir / "normalized"

    raw_paths = [raw_dir / f"category_{category}.jsonl.gz" for category in categories]
    meta_paths = [
        out_dir / "manifest.json",
        normalized_dir / "guide_documents.json",
        normalized_dir / "law_articles.json",
        normalized_dir / "guide_sections.jsonl.gz",
        normalized_dir / "retrieval_corpus.jsonl.gz",
    ]
    maybe_remove_existing(raw_paths + meta_paths, force=args.force)

    all_rows: List[Dict[str, Any]] = []
    per_category_stats: Dict[str, Dict[str, int]] = {}

    for category in categories:
        rows, stats = fetch_category(
            endpoint=args.endpoint,
            service_key=service_key,
            category=category,
            query=args.query,
            num_rows=args.num_rows,
            timeout_sec=args.timeout,
            retries=args.retries,
            sleep_ms=args.sleep_ms,
            max_pages=args.max_pages,
        )
        per_category_stats[category] = stats
        all_rows.extend(rows)
        write_jsonl_gz(raw_dir / f"category_{category}.jsonl.gz", rows)
        print(
            f"[OK] category={category} pages={stats['pages_fetched']} "
            f"raw={stats['raw_rows']} dedup={stats['dedup_rows']} api_total={stats['api_total_count']}"
        )

    normalized = build_normalized_views(all_rows)
    write_json(normalized_dir / "guide_documents.json", normalized["guide_documents"])
    write_json(normalized_dir / "law_articles.json", normalized["law_articles"])
    write_jsonl_gz(normalized_dir / "guide_sections.jsonl.gz", normalized["guide_sections"])
    write_jsonl_gz(normalized_dir / "retrieval_corpus.jsonl.gz", normalized["retrieval_corpus"])

    finished_at = datetime.now(timezone.utc)
    manifest = {
        "generated_at_utc": finished_at.isoformat(),
        "duration_sec": round((finished_at - started_at).total_seconds(), 3),
        "endpoint": args.endpoint,
        "categories": categories,
        "query": args.query,
        "num_rows": args.num_rows,
        "max_pages": args.max_pages,
        "totals": {
            "rows_all_categories": len(all_rows),
            "guide_section_rows": len(normalized["guide_sections"]),
            "guide_documents": len(normalized["guide_documents"]),
            "law_articles": len(normalized["law_articles"]),
            "retrieval_corpus_rows": len(normalized["retrieval_corpus"]),
        },
        "category_stats": per_category_stats,
        "files": {
            "raw_dir": str(raw_dir),
            "normalized_dir": str(normalized_dir),
        },
    }
    write_json(out_dir / "manifest.json", manifest)

    print("[DONE] KOSHA sync completed")
    print(f"- out_dir: {out_dir}")
    print(f"- guide_documents: {manifest['totals']['guide_documents']}")
    print(f"- law_articles: {manifest['totals']['law_articles']}")
    print(f"- retrieval_rows: {manifest['totals']['retrieval_corpus_rows']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(f"[FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1)

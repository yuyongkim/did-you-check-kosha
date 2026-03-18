#!/usr/bin/env python3
"""Sync KOSHA Guide API index and optional direct PDF downloads."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

from kosha_ingestion.sync_corpus import RETRYABLE_STATUS, REPO_ROOT, resolve_service_key
from kosha_ingestion.text_encoding import parse_json_bytes


GUIDE_ENDPOINT = "https://apis.data.go.kr/B552468/koshaguide/getKoshaGuide"
DEFAULT_CALL_API_ID = "1050"


@dataclass
class DownloadItem:
  tech_gdln_no: str
  tech_gdln_nm: str
  tech_gdln_ofanc_ymd: str
  file_download_url: str
  status: str
  message: str
  filename: str = ""
  bytes: int = 0


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
  parser = argparse.ArgumentParser(description="Sync KOSHA Guide API index and optional PDF files.")
  parser.add_argument("--endpoint", default=GUIDE_ENDPOINT, help="Guide API endpoint URL.")
  parser.add_argument("--call-api-id", default=DEFAULT_CALL_API_ID, help="Required KOSHA Guide callApiId.")
  parser.add_argument("--page-size", type=int, default=200, help="Rows per page.")
  parser.add_argument("--max-pages", type=int, default=0, help="Optional page cap (0 = no cap).")
  parser.add_argument("--sleep-ms", type=int, default=120, help="Inter-page delay in milliseconds.")
  parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout seconds.")
  parser.add_argument("--retries", type=int, default=3, help="Retry attempts for transient errors.")
  parser.add_argument("--service-key", default="", help="Optional service key override.")
  parser.add_argument(
    "--out-dir",
    default=str(REPO_ROOT / "datasets" / "kosha_guide"),
    help="Output directory root.",
  )
  parser.add_argument("--download", action="store_true", help="Download files from fileDownloadUrl.")
  parser.add_argument("--max-downloads", type=int, default=0, help="Optional file download cap (0 = all).")
  parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
  return parser.parse_args(argv)


def request_bytes(url: str, timeout_sec: int, retries: int) -> bytes:
  last_error: Exception | None = None
  for attempt in range(1, retries + 1):
    try:
      req = Request(url, headers={"Accept": "application/json"}, method="GET")
      with urlopen(req, timeout=timeout_sec) as response:  # noqa: S310
        return response.read()
    except HTTPError as exc:
      last_error = exc
      if exc.code not in RETRYABLE_STATUS or attempt >= retries:
        break
    except (URLError, TimeoutError) as exc:
      last_error = exc
      if attempt >= retries:
        break
    time.sleep(min(2.0, 0.35 * attempt))
  raise RuntimeError(f"request failed: {url} error={last_error}") from last_error


def request_json(url: str, timeout_sec: int, retries: int) -> Dict[str, Any]:
  body = request_bytes(url, timeout_sec=timeout_sec, retries=retries)
  return parse_json_bytes(body, content_type="application/json")


def parse_response(payload: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], int]:
  # API currently returns {header, body}. Keep fallback for {response:{header,body}} variants.
  if "response" in payload:
    node = payload.get("response") or {}
  else:
    node = payload

  header = node.get("header") or {}
  result_code = str(header.get("resultCode") or "")
  if result_code and result_code != "00":
    result_msg = str(header.get("resultMsg") or "")
    raise RuntimeError(f"KOSHA Guide API error: resultCode={result_code}, resultMsg={result_msg}")

  body = node.get("body") or {}
  total_count = int(body.get("totalCount") or 0)
  items_node = ((body.get("items") or {}).get("item")) if isinstance(body.get("items"), dict) else None

  if items_node is None:
    return [], total_count
  if isinstance(items_node, dict):
    return [items_node], total_count
  if isinstance(items_node, list):
    return [item for item in items_node if isinstance(item, dict)], total_count
  return [], total_count


def normalize_text(value: Any) -> str:
  text = str(value or "")
  text = re.sub(r"\s+", " ", text).strip()
  return text


def safe_ascii_token(value: str, fallback: str) -> str:
  text = normalize_text(value)
  text = re.sub(r"[^0-9A-Za-z._-]+", "_", text).strip("._")
  return text or fallback


def safe_title_token(value: str, fallback: str = "untitled", max_len: int = 140) -> str:
  text = normalize_text(value)
  # Keep Korean/Unicode letters but remove filesystem-invalid characters.
  text = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', " ", text)
  text = re.sub(r"\s+", " ", text).strip(" .")
  if not text:
    return fallback
  if len(text) > max_len:
    text = text[:max_len].rstrip(" .")
  return text or fallback


def collect_index(
  endpoint: str,
  service_key: str,
  call_api_id: str,
  page_size: int,
  max_pages: int,
  timeout_sec: int,
  retries: int,
  sleep_ms: int,
) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
  page = 1
  api_total_count = 0
  dedup: Dict[str, Dict[str, Any]] = {}
  raw_rows = 0
  duplicate_rows = 0

  while True:
    query = urlencode(
      {
        "serviceKey": service_key,
        "pageNo": str(page),
        "numOfRows": str(page_size),
        "callApiId": call_api_id,
      }
    )
    url = f"{endpoint}?{query}"
    payload = request_json(url, timeout_sec=timeout_sec, retries=retries)
    items, total_count = parse_response(payload)
    api_total_count = max(api_total_count, total_count)

    if not items:
      break

    for idx, item in enumerate(items, start=1):
      raw_rows += 1
      tech_gdln_no = normalize_text(item.get("techGdlnNo"))
      tech_gdln_nm = normalize_text(item.get("techGdlnNm"))
      tech_gdln_ofanc_ymd = normalize_text(item.get("techGdlnOfancYmd"))
      file_download_url = normalize_text(item.get("fileDownloadUrl"))

      key = tech_gdln_no or f"{page}:{idx}:{tech_gdln_nm}"
      if key in dedup:
        duplicate_rows += 1
        continue

      dedup[key] = {
        "techGdlnNo": tech_gdln_no or None,
        "techGdlnNm": tech_gdln_nm or None,
        "techGdlnOfancYmd": tech_gdln_ofanc_ymd or None,
        "fileDownloadUrl": file_download_url or None,
      }

    if (max_pages > 0 and page >= max_pages) or len(items) < page_size:
      break

    page += 1
    if sleep_ms > 0:
      time.sleep(sleep_ms / 1000.0)

  stats = {
    "api_total_count": api_total_count,
    "raw_rows": raw_rows,
    "dedup_rows": len(dedup),
    "duplicate_rows": duplicate_rows,
    "pages_fetched": page,
  }
  rows = sorted(
    dedup.values(),
    key=lambda row: (
      normalize_text(str(row.get("techGdlnNo") or "")),
      normalize_text(str(row.get("techGdlnNm") or "")),
    ),
  )
  return rows, stats


def request_file(url: str, timeout_sec: int, retries: int) -> Tuple[bytes, Dict[str, str]]:
  last_error: Exception | None = None
  for attempt in range(1, retries + 1):
    try:
      req = Request(url, headers={"Accept": "*/*"}, method="GET")
      with urlopen(req, timeout=timeout_sec) as response:  # noqa: S310
        body = response.read()
        headers = {k: v for (k, v) in response.headers.items()}
      return body, headers
    except HTTPError as exc:
      last_error = exc
      if exc.code not in RETRYABLE_STATUS or attempt >= retries:
        break
    except (URLError, TimeoutError) as exc:
      last_error = exc
      if attempt >= retries:
        break
    time.sleep(min(2.0, 0.35 * attempt))
  raise RuntimeError(f"download failed: {url} error={last_error}") from last_error


def guess_extension(url: str, headers: Dict[str, str]) -> str:
  content_type = str(headers.get("Content-Type") or headers.get("content-type") or "").lower()
  if "pdf" in content_type:
    return ".pdf"
  if "zip" in content_type:
    return ".zip"
  path_name = Path(urlparse(url).path).name.lower()
  if path_name.endswith(".pdf"):
    return ".pdf"
  if path_name.endswith(".zip"):
    return ".zip"
  return ".bin"


def download_files(
  rows: List[Dict[str, Any]],
  files_dir: Path,
  timeout_sec: int,
  retries: int,
  force: bool,
  max_downloads: int,
) -> Tuple[List[DownloadItem], Dict[str, int]]:
  files_dir.mkdir(parents=True, exist_ok=True)

  results: List[DownloadItem] = []
  downloaded = 0
  skipped = 0
  failed = 0
  bytes_total = 0
  selected = 0

  for row in rows:
    url = str(row.get("fileDownloadUrl") or "").strip()
    if not url:
      results.append(
        DownloadItem(
          tech_gdln_no=str(row.get("techGdlnNo") or ""),
          tech_gdln_nm=str(row.get("techGdlnNm") or ""),
          tech_gdln_ofanc_ymd=str(row.get("techGdlnOfancYmd") or ""),
          file_download_url="",
          status="no_url",
          message="fileDownloadUrl missing",
        )
      )
      continue

    selected += 1
    if max_downloads > 0 and selected > max_downloads:
      break

    no_token = safe_ascii_token(str(row.get("techGdlnNo") or ""), "NO")
    title_token = safe_title_token(str(row.get("techGdlnNm") or ""), fallback="TITLE")

    try:
      body, headers = request_file(url, timeout_sec=timeout_sec, retries=retries)
      if len(body) == 0:
        raise RuntimeError("empty_file_body")
      ext = guess_extension(url, headers)
      base_name = f"{no_token}__{title_token}"
      target = files_dir / f"{base_name}{ext}"

      if target.exists() and not force:
        skipped += 1
        results.append(
          DownloadItem(
            tech_gdln_no=str(row.get("techGdlnNo") or ""),
            tech_gdln_nm=str(row.get("techGdlnNm") or ""),
            tech_gdln_ofanc_ymd=str(row.get("techGdlnOfancYmd") or ""),
            file_download_url=url,
            status="skipped",
            message="already exists",
            filename=str(target),
            bytes=target.stat().st_size,
          )
        )
        continue

      target.write_bytes(body)
      downloaded += 1
      bytes_total += len(body)
      results.append(
        DownloadItem(
          tech_gdln_no=str(row.get("techGdlnNo") or ""),
          tech_gdln_nm=str(row.get("techGdlnNm") or ""),
          tech_gdln_ofanc_ymd=str(row.get("techGdlnOfancYmd") or ""),
          file_download_url=url,
          status="downloaded",
          message="ok",
          filename=str(target),
          bytes=len(body),
        )
      )
    except Exception as exc:  # noqa: BLE001
      failed += 1
      results.append(
        DownloadItem(
          tech_gdln_no=str(row.get("techGdlnNo") or ""),
          tech_gdln_nm=str(row.get("techGdlnNm") or ""),
          tech_gdln_ofanc_ymd=str(row.get("techGdlnOfancYmd") or ""),
          file_download_url=url,
          status="error",
          message=str(exc),
        )
      )

  totals = {
    "selected_for_download": selected if max_downloads == 0 else min(selected, max_downloads),
    "downloaded": downloaded,
    "skipped": skipped,
    "failed": failed,
    "bytes": bytes_total,
  }
  return results, totals


def main(argv: List[str] | None = None) -> int:
  args = parse_args(argv)
  out_dir = Path(args.out_dir).resolve()
  files_dir = out_dir / "files"
  guides_json = out_dir / "guides.json"
  download_manifest_path = out_dir / "downloads_manifest.json"
  manifest_path = out_dir / "manifest.json"

  service_key = resolve_service_key(args.service_key)

  started = time.perf_counter()
  rows, stats = collect_index(
    endpoint=args.endpoint,
    service_key=service_key,
    call_api_id=args.call_api_id,
    page_size=args.page_size,
    max_pages=args.max_pages,
    timeout_sec=args.timeout,
    retries=args.retries,
    sleep_ms=args.sleep_ms,
  )

  out_dir.mkdir(parents=True, exist_ok=True)
  guides_json.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

  download_results: List[DownloadItem] = []
  download_totals = {
    "selected_for_download": 0,
    "downloaded": 0,
    "skipped": 0,
    "failed": 0,
    "bytes": 0,
  }
  if args.download:
    download_results, download_totals = download_files(
      rows=rows,
      files_dir=files_dir,
      timeout_sec=args.timeout,
      retries=args.retries,
      force=args.force,
      max_downloads=args.max_downloads,
    )
    download_manifest = {
      "generated_at_utc": datetime.now(timezone.utc).isoformat(),
      "out_dir": str(out_dir),
      "download_enabled": True,
      "max_downloads": args.max_downloads,
      "totals": download_totals,
      "items": [item.__dict__ for item in download_results],
    }
    download_manifest_path.write_text(json.dumps(download_manifest, ensure_ascii=False, indent=2), encoding="utf-8")

  elapsed = round(time.perf_counter() - started, 3)
  manifest = {
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    "duration_sec": elapsed,
    "endpoint": args.endpoint,
    "callApiId": args.call_api_id,
    "totals": {
      "guide_rows": len(rows),
      "rows_with_file_url": sum(1 for row in rows if row.get("fileDownloadUrl")),
    },
    "fetch_stats": stats,
    "download": {
      "enabled": bool(args.download),
      **download_totals,
    },
    "files": {
      "guides_json": str(guides_json),
      "downloads_manifest": str(download_manifest_path) if args.download else None,
      "files_dir": str(files_dir),
    },
  }
  manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

  print("[DONE] KOSHA Guide API sync finished")
  print(f"- guide_rows: {manifest['totals']['guide_rows']}")
  print(f"- rows_with_file_url: {manifest['totals']['rows_with_file_url']}")
  print(f"- download_enabled: {args.download}")
  if args.download:
    print(f"- downloaded: {download_totals['downloaded']}")
    print(f"- skipped: {download_totals['skipped']}")
    print(f"- failed: {download_totals['failed']}")
    print(f"- bytes: {download_totals['bytes']}")
  print(f"- manifest: {manifest_path}")
  return 0


if __name__ == "__main__":
  try:
    raise SystemExit(main())
  except Exception as exc:  # noqa: BLE001
    print(f"[FAIL] {exc}", file=sys.stderr)
    raise SystemExit(1)

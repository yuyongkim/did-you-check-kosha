#!/usr/bin/env python3
"""Best-effort KOSHA asset downloader (PDF and attachments)."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, quote, urlencode, urljoin, urlparse
from urllib.request import Request, urlopen

from kosha_ingestion.text_encoding import parse_json_bytes


REPO_ROOT = Path(__file__).resolve().parents[4]
PORTAL_BASE_URL = "https://portal.kosha.or.kr"
FILE_LIST_URL = f"{PORTAL_BASE_URL}/api/portal24/bizA/p/files/getFileList"
FILE_DOWNLOAD_URL = f"{PORTAL_BASE_URL}/api/portal24/bizA/p/files/downloadAtchFile"
RETRYABLE_STATUS = {408, 429, 500, 502, 503, 504}


@dataclass
class AssetItem:
  source_id: str
  source_category: str
  source_url: str
  resolved_url: str
  filename: str
  status: str
  message: str
  bytes: int = 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
  parser = argparse.ArgumentParser(description="Download KOSHA corpus-linked file assets.")
  parser.add_argument(
    "--corpus",
    default=str(REPO_ROOT / "datasets" / "kosha" / "normalized" / "retrieval_corpus.jsonl.gz"),
    help="Path to retrieval_corpus.jsonl.gz",
  )
  parser.add_argument(
    "--out-dir",
    default=str(REPO_ROOT / "datasets" / "kosha" / "assets"),
    help="Output directory for downloaded files.",
  )
  parser.add_argument(
    "--manifest",
    default=str(REPO_ROOT / "datasets" / "kosha" / "assets_manifest.json"),
    help="Output manifest path.",
  )
  parser.add_argument("--max-items", type=int, default=0, help="Optional limit of corpus rows to process.")
  parser.add_argument("--sleep-ms", type=int, default=100, help="Delay between records.")
  parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds.")
  parser.add_argument("--retries", type=int, default=3, help="Retry attempts for transient errors.")
  parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
  parser.add_argument("--dry-run", action="store_true", help="Do not write files, only resolve links.")
  return parser.parse_args(argv)


def ensure_parent(path: Path) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)


def read_jsonl_gz(path: Path) -> Iterable[Dict[str, Any]]:
  with gzip.open(path, mode="rt", encoding="utf-8") as stream:
    for line in stream:
      line = line.strip()
      if not line:
        continue
      try:
        obj = json.loads(line)
      except json.JSONDecodeError:
        continue
      if isinstance(obj, dict):
        yield obj


def request_bytes(url: str, method: str = "GET", payload: Optional[dict] = None, timeout_sec: int = 30, retries: int = 3) -> bytes:
  encoded_payload = None
  headers: Dict[str, str] = {"Accept": "*/*", "chnlId": "portal24"}
  if payload is not None:
    encoded_payload = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers["Content-Type"] = "application/json"

  last_error: Exception | None = None
  for attempt in range(1, retries + 1):
    try:
      req = Request(url, data=encoded_payload, headers=headers, method=method)
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


def request_json(url: str, method: str = "GET", payload: Optional[dict] = None, timeout_sec: int = 30, retries: int = 3) -> Dict[str, Any]:
  data = request_bytes(url, method=method, payload=payload, timeout_sec=timeout_sec, retries=retries)
  return parse_json_bytes(data, content_type="application/json")


def parse_med_seq(url: str) -> Optional[str]:
  parsed = urlparse(url)
  query = parse_qs(parsed.query)
  med_seq = query.get("medSeq", [None])[0]
  if med_seq:
    return str(med_seq).strip()
  return None


def candidate_file_ids(source_id: str, source_url: str) -> List[str]:
  values: List[str] = []
  med_seq = parse_med_seq(source_url)
  if med_seq:
    values.append(med_seq)

  sid = (source_id or "").strip()
  if sid:
    values.append(sid)
    match = re.match(r"^KOSHA06_(\d+)_\d+$", sid)
    if match:
      values.append(match.group(1))

  dedup: List[str] = []
  seen = set()
  for item in values:
    if item and item not in seen:
      dedup.append(item)
      seen.add(item)
  return dedup


def resolve_file_payload(source_id: str, source_url: str, timeout_sec: int, retries: int) -> List[Dict[str, Any]]:
  for file_id in candidate_file_ids(source_id, source_url):
    for payload in ({"fileId": file_id}, {"atcflNo": file_id}):
      data = request_json(FILE_LIST_URL, method="POST", payload=payload, timeout_sec=timeout_sec, retries=retries)
      rows = data.get("payload")
      if isinstance(rows, list) and rows:
        return [row for row in rows if isinstance(row, dict)]
  return []


def build_download_url(row: Dict[str, Any]) -> Optional[str]:
  atcfl_no = str(row.get("atcflNo") or "").strip()
  atcfl_seq = str(row.get("atcflSeq") or "").strip()
  if not atcfl_no or not atcfl_seq:
    return None

  params = {
    "atcflNo": atcfl_no,
    "atcflSeq": atcfl_seq,
    "isDirect": "N",
  }
  task_se_cd = str(row.get("taskSeCd") or "").strip()
  if task_se_cd:
    params["taskSeCd"] = task_se_cd

  file_name = str(row.get("orgnlAtchFileNm") or "").strip()
  if file_name:
    params["fileName"] = quote(file_name, safe="")

  mime_type = str(row.get("mimeType") or "").strip()
  if mime_type:
    params["mimeType"] = mime_type

  return f"{FILE_DOWNLOAD_URL}?{urlencode(params)}"


def extract_html_links(url: str, timeout_sec: int, retries: int) -> List[str]:
  try:
    body = request_bytes(url, timeout_sec=timeout_sec, retries=retries).decode("utf-8", errors="ignore")
  except Exception:
    return []

  links = re.findall(r"""(?:href|src)=['"]([^'"]+)['"]""", body)
  resolved: List[str] = []
  for item in links:
    lower = item.lower()
    if ".pdf" in lower or "downloadatchfile" in lower or "/p/files/download" in lower:
      resolved.append(urljoin(url, item))
  dedup = list(dict.fromkeys(resolved))
  return dedup


def sanitize_filename(name: str) -> str:
  cleaned = name.strip().replace("\\", "_").replace("/", "_")
  cleaned = re.sub(r"\s+", " ", cleaned)
  cleaned = re.sub(r"[^A-Za-z0-9._()\- ]", "_", cleaned)
  cleaned = cleaned.strip(" .")
  return cleaned or "asset.bin"


def extension_from_content_type(content_type: str) -> str:
  value = content_type.lower()
  if "pdf" in value:
    return ".pdf"
  if "zip" in value:
    return ".zip"
  if "msword" in value:
    return ".doc"
  if "officedocument.wordprocessingml" in value:
    return ".docx"
  if "spreadsheetml" in value:
    return ".xlsx"
  if "excel" in value:
    return ".xls"
  return ""


def infer_filename(source_id: str, source_url: str, resolved_url: str, headers: Dict[str, str]) -> str:
  disp = headers.get("Content-Disposition") or headers.get("content-disposition") or ""
  match_utf8 = re.search(r"filename\*=UTF-8''([^;]+)", disp)
  if match_utf8:
    return sanitize_filename(match_utf8.group(1))
  match_plain = re.search(r'filename="([^"]+)"', disp)
  if match_plain:
    return sanitize_filename(match_plain.group(1))

  name = Path(urlparse(resolved_url).path).name
  if name and "." in name:
    return sanitize_filename(name)

  base = sanitize_filename(source_id or "asset")
  ext = extension_from_content_type(headers.get("Content-Type", ""))
  if not ext:
    ext = extension_from_content_type(headers.get("content-type", ""))
  return f"{base}{ext or '.bin'}"


def download_url(resolved_url: str, timeout_sec: int, retries: int) -> tuple[bytes, Dict[str, str]]:
  last_error: Exception | None = None
  headers = {"Accept": "*/*", "chnlId": "portal24"}
  for attempt in range(1, retries + 1):
    try:
      req = Request(resolved_url, headers=headers, method="GET")
      with urlopen(req, timeout=timeout_sec) as response:  # noqa: S310
        body = response.read()
        resp_headers = {k: v for (k, v) in response.headers.items()}
      return body, resp_headers
    except HTTPError as exc:
      last_error = exc
      if exc.code not in RETRYABLE_STATUS or attempt >= retries:
        break
    except (URLError, TimeoutError) as exc:
      last_error = exc
      if attempt >= retries:
        break
    time.sleep(min(2.0, 0.35 * attempt))

  raise RuntimeError(f"download failed url={resolved_url} error={last_error}") from last_error


def write_file(path: Path, body: bytes, force: bool) -> None:
  ensure_parent(path)
  if path.exists() and not force:
    raise FileExistsError(f"file exists: {path}")
  path.write_bytes(body)


def resolve_candidate_urls(item: Dict[str, Any], timeout_sec: int, retries: int) -> List[str]:
  source_id = str(item.get("id") or "")
  source_url = str(item.get("filepath") or "")
  urls: List[str] = []

  for row in resolve_file_payload(source_id, source_url, timeout_sec=timeout_sec, retries=retries):
    built = build_download_url(row)
    if built:
      urls.append(built)

  # Fallback: parse direct links from the portal detail page itself.
  if not urls and source_url:
    urls.extend(extract_html_links(source_url, timeout_sec=timeout_sec, retries=retries))

  return list(dict.fromkeys(urls))


def select_records(corpus_path: Path, max_items: int) -> List[Dict[str, Any]]:
  selected: List[Dict[str, Any]] = []
  for row in read_jsonl_gz(corpus_path):
    filepath = str(row.get("filepath") or "").strip()
    if not filepath:
      continue
    selected.append(row)
    if max_items > 0 and len(selected) >= max_items:
      break
  return selected


def main(argv: list[str] | None = None) -> int:
  args = parse_args(argv)
  corpus_path = Path(args.corpus).resolve()
  out_dir = Path(args.out_dir).resolve()
  manifest_path = Path(args.manifest).resolve()

  if not corpus_path.exists():
    raise RuntimeError(f"corpus file not found: {corpus_path}")

  records = select_records(corpus_path, max_items=args.max_items)
  results: List[AssetItem] = []
  downloaded = 0
  total_bytes = 0
  unresolved = 0
  failed = 0

  for index, row in enumerate(records, start=1):
    source_id = str(row.get("id") or "")
    source_category = str(row.get("category") or "")
    source_url = str(row.get("filepath") or "")

    try:
      candidate_urls = resolve_candidate_urls(row, timeout_sec=args.timeout, retries=args.retries)
    except Exception as exc:  # noqa: BLE001
      failed += 1
      results.append(
        AssetItem(
          source_id=source_id,
          source_category=source_category,
          source_url=source_url,
          resolved_url="",
          filename="",
          status="error",
          message=f"resolve_failed: {exc}",
        )
      )
      continue

    if not candidate_urls:
      unresolved += 1
      results.append(
        AssetItem(
          source_id=source_id,
          source_category=source_category,
          source_url=source_url,
          resolved_url="",
          filename="",
          status="unresolved",
          message="no downloadable link resolved",
        )
      )
      continue

    for candidate in candidate_urls:
      try:
        body, headers = download_url(candidate, timeout_sec=args.timeout, retries=args.retries)
        digest = hashlib.sha1(f"{source_id}|{candidate}".encode("utf-8")).hexdigest()[:10]
        filename = infer_filename(source_id=source_id, source_url=source_url, resolved_url=candidate, headers=headers)
        filename = sanitize_filename(filename)
        target = out_dir / f"{source_category}_{digest}_{filename}"

        if not args.dry_run:
          write_file(target, body, force=args.force)

        downloaded += 1
        total_bytes += len(body)
        results.append(
          AssetItem(
            source_id=source_id,
            source_category=source_category,
            source_url=source_url,
            resolved_url=candidate,
            filename=str(target),
            status="downloaded" if not args.dry_run else "resolved",
            message="ok",
            bytes=len(body),
          )
        )
      except Exception as exc:  # noqa: BLE001
        failed += 1
        results.append(
          AssetItem(
            source_id=source_id,
            source_category=source_category,
            source_url=source_url,
            resolved_url=candidate,
            filename="",
            status="error",
            message=f"download_failed: {exc}",
          )
        )

    if args.sleep_ms > 0:
      time.sleep(args.sleep_ms / 1000.0)
    if index % 250 == 0:
      print(f"[PROGRESS] processed={index} downloaded={downloaded} unresolved={unresolved} failed={failed}")

  payload = {
    "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "corpus": str(corpus_path),
    "out_dir": str(out_dir),
    "max_items": args.max_items,
    "dry_run": args.dry_run,
    "totals": {
      "records_with_filepath": len(records),
      "downloaded": downloaded,
      "unresolved": unresolved,
      "failed": failed,
      "bytes": total_bytes,
    },
    "items": [item.__dict__ for item in results],
  }

  ensure_parent(manifest_path)
  manifest_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

  print("[DONE] KOSHA asset pass finished")
  print(f"- records_with_filepath: {len(records)}")
  print(f"- downloaded: {downloaded}")
  print(f"- unresolved: {unresolved}")
  print(f"- failed: {failed}")
  print(f"- bytes: {total_bytes}")
  print(f"- manifest: {manifest_path}")
  return 0


if __name__ == "__main__":
  try:
    raise SystemExit(main())
  except Exception as exc:  # noqa: BLE001
    print(f"[FAIL] {exc}", file=sys.stderr)
    raise SystemExit(1)

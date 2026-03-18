"""Encoding helpers for KOSHA ingestion payloads."""

from __future__ import annotations

import json
import re
from typing import Any, Dict, Iterable, List


DEFAULT_ENCODING_CANDIDATES = ["utf-8", "utf-8-sig", "cp949", "euc-kr", "latin-1"]


def _unique(items: Iterable[str]) -> List[str]:
  seen: set[str] = set()
  out: List[str] = []
  for item in items:
    token = (item or "").strip().lower()
    if token and token not in seen:
      seen.add(token)
      out.append(token)
  return out


def _charset_from_content_type(content_type: str) -> str:
  match = re.search(r"charset=([A-Za-z0-9._-]+)", content_type or "", flags=re.IGNORECASE)
  return match.group(1).strip().lower() if match else ""


def _encoding_candidates(content_type: str) -> List[str]:
  hinted = _charset_from_content_type(content_type)
  if not hinted:
    return DEFAULT_ENCODING_CANDIDATES
  return _unique([hinted, *DEFAULT_ENCODING_CANDIDATES])


def _hangul_syllable_count(text: str) -> int:
  return sum(1 for ch in text if "\uac00" <= ch <= "\ud7a3")


def _suspicious_char_count(text: str) -> int:
  # Typical mojibake indicators from UTF-8<->CP949 confusion.
  return sum(
    1
    for ch in text
    if ("\u0370" <= ch <= "\u04ff") or ("\ufffd" <= ch <= "\ufffd") or ("?" == ch)
  )


def _quality_score(text: str) -> int:
  hangul = _hangul_syllable_count(text)
  suspicious = _suspicious_char_count(text)
  return (hangul * 2) - suspicious


def _try_redecode(text: str, source: str, target: str) -> str | None:
  try:
    return text.encode(source).decode(target)
  except (UnicodeEncodeError, UnicodeDecodeError):
    return None


def maybe_fix_mojibake_text(value: str) -> str:
  text = str(value or "")
  if not text:
    return text

  candidates = [text]
  cp949_fix = _try_redecode(text, "cp949", "utf-8")
  if cp949_fix:
    candidates.append(cp949_fix)
  latin_fix = _try_redecode(text, "latin-1", "utf-8")
  if latin_fix:
    candidates.append(latin_fix)

  best = max(candidates, key=_quality_score)
  # Avoid over-correcting: only replace if quality gain is meaningful.
  if _quality_score(best) >= _quality_score(text) + 2:
    return best
  return text


def repair_mojibake_in_object(value: Any) -> Any:
  if isinstance(value, dict):
    return {k: repair_mojibake_in_object(v) for k, v in value.items()}
  if isinstance(value, list):
    return [repair_mojibake_in_object(item) for item in value]
  if isinstance(value, str):
    return maybe_fix_mojibake_text(value)
  return value


def parse_json_bytes(payload: bytes, content_type: str = "") -> Dict[str, Any]:
  for encoding in _encoding_candidates(content_type):
    try:
      text = payload.decode(encoding)
      parsed = json.loads(text)
      parsed = repair_mojibake_in_object(parsed)
      return parsed if isinstance(parsed, dict) else {}
    except (UnicodeDecodeError, json.JSONDecodeError):
      continue
  return {}

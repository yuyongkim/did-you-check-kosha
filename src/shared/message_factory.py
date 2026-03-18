from __future__ import annotations

from typing import Any, Dict, Mapping

from src.shared.types import new_id, utc_now_iso


def create_message(
    *,
    message_type: str,
    from_agent: str,
    to_agent: str,
    payload: Mapping[str, Any],
    priority: str = "normal",
    timeout_sec: int = 300,
    correlation_id: str | None = None,
    trace_id: str | None = None,
    meta: Mapping[str, Any] | None = None,
) -> Dict[str, Any]:
    return {
        "message_id": new_id(),
        "message_type": message_type,
        "correlation_id": correlation_id or new_id(),
        "trace_id": trace_id or new_id(),
        "from_agent": from_agent,
        "to_agent": to_agent,
        "timestamp_utc": utc_now_iso(),
        "priority": priority,
        "timeout_sec": timeout_sec,
        "payload": dict(payload),
        "meta": dict(meta or {}),
    }


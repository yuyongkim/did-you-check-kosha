from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def new_id() -> str:
    return str(uuid.uuid4())


@dataclass
class TraceContext:
    correlation_id: str = field(default_factory=new_id)
    trace_id: str = field(default_factory=new_id)
    workflow_id: str = "standard_calculation"
    started_at_utc: str = field(default_factory=utc_now_iso)

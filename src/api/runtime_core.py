from __future__ import annotations

import threading
import time
import uuid
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from typing import Any, Dict, List, Mapping

from src.api import persistence
from src.civil.service import CivilVerificationService
from src.electrical.service import ElectricalVerificationService
from src.instrumentation.service import InstrumentationVerificationService
from src.piping.service import PipingVerificationService
from src.rotating.service import RotatingVerificationService
from src.steel.service import SteelVerificationService
from src.vessel.service import VesselVerificationService


@dataclass(frozen=True)
class DisciplineRuntime:
    default_calculation_type: str
    service: Any


RUNTIMES: Dict[str, DisciplineRuntime] = {
    "piping": DisciplineRuntime(default_calculation_type="remaining_life", service=PipingVerificationService()),
    "vessel": DisciplineRuntime(default_calculation_type="vessel_integrity", service=VesselVerificationService()),
    "rotating": DisciplineRuntime(default_calculation_type="rotating_integrity", service=RotatingVerificationService()),
    "electrical": DisciplineRuntime(default_calculation_type="electrical_integrity", service=ElectricalVerificationService()),
    "instrumentation": DisciplineRuntime(
        default_calculation_type="instrumentation_integrity",
        service=InstrumentationVerificationService(),
    ),
    "steel": DisciplineRuntime(default_calculation_type="steel_integrity", service=SteelVerificationService()),
    "civil": DisciplineRuntime(default_calculation_type="civil_integrity", service=CivilVerificationService()),
}

CACHE_TTL_SEC = 180.0
_CACHE: Dict[str, Dict[str, Any]] = {}
_CACHE_LOCK = threading.Lock()
_CACHE_HITS = 0
_CACHE_MISSES = 0

_AUDIT_MAX = 5000
_AUDIT_LOGS: List[Dict[str, Any]] = []
_AUDIT_LOCK = threading.Lock()

_JOBS: Dict[str, Dict[str, Any]] = {}
_JOB_FUTURES: Dict[str, Future[None]] = {}
_JOBS_LOCK = threading.Lock()
_JOB_EXECUTOR = ThreadPoolExecutor(max_workers=6)

_COLLAB_SESSIONS: Dict[str, Dict[str, Any]] = {}
_COLLAB_LOCK = threading.Lock()

persistence.init_db()


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def audit(event_type: str, details: Mapping[str, Any]) -> None:
    record = {
        "id": str(uuid.uuid4()),
        "timestamp": utc_now_iso(),
        "event_type": event_type,
        "details": dict(details),
    }
    with _AUDIT_LOCK:
        _AUDIT_LOGS.append(record)
        if len(_AUDIT_LOGS) > _AUDIT_MAX:
            del _AUDIT_LOGS[: len(_AUDIT_LOGS) - _AUDIT_MAX]
    persistence.persist_audit(record)


def recent_audit_logs(limit: int | None = None) -> List[Dict[str, Any]]:
    with _AUDIT_LOCK:
        rows = list(_AUDIT_LOGS)
    rows.sort(key=lambda row: row["timestamp"], reverse=True)
    return rows if limit is None else rows[:limit]


def supported_disciplines() -> List[str]:
    return sorted(RUNTIMES.keys())


def normalize_flags(payload: Mapping[str, Any]) -> Dict[str, List[str]]:
    raw = payload.get("flags", {})
    red = list(raw.get("red_flags", [])) if isinstance(raw, Mapping) else []
    warnings = list(raw.get("warnings", [])) if isinstance(raw, Mapping) else []
    return {
        "red_flags": red,
        "warnings": warnings,
    }


def _status_from_result(*, flags: Dict[str, List[str]], final_results: Mapping[str, Any]) -> str:
    if flags["red_flags"]:
        return "blocked"
    if not final_results:
        return "error"
    return "success"


def transform_to_frontend_response(
    discipline: str,
    backend_result: Mapping[str, Any],
) -> Dict[str, Any]:
    summary = backend_result.get("calculation_summary", {})
    final_results = backend_result.get("final_results", {})
    layer_results = backend_result.get("layer_results", [])
    references = summary.get("standards_applied", [])
    flags = normalize_flags(backend_result)
    confidence = summary.get("confidence", "low")
    status = _status_from_result(flags=flags, final_results=final_results if isinstance(final_results, Mapping) else {})

    details = {
        "calculation_summary": {
            "discipline": discipline,
            "calculation_type": summary.get("calculation_type", f"{discipline}_integrity"),
            "standards_applied": references if isinstance(references, list) else [],
            "confidence": confidence,
            "execution_time_sec": summary.get("execution_time_sec", 0),
        },
        "input_data": backend_result.get("input_data", {}),
        "calculation_steps": backend_result.get("calculation_steps", []),
        "layer_results": layer_results if isinstance(layer_results, list) else [],
        "final_results": final_results if isinstance(final_results, Mapping) else {},
        "recommendations": backend_result.get("recommendations", []),
        "flags": flags,
    }

    return {
        "status": status,
        "discipline": discipline,
        "results": details["final_results"],
        "details": details,
        "references": details["calculation_summary"]["standards_applied"],
        "verification": {
            "layers": details["layer_results"],
            "confidence": confidence,
        },
        "flags": flags,
    }


def _cache_key(discipline: str, payload: Mapping[str, Any], calculation_type: str | None) -> str:
    normalized_payload = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str)
    return f"{discipline}::{calculation_type or ''}::{normalized_payload}"


def dispatch_calculation(
    discipline: str,
    payload: Mapping[str, Any],
    calculation_type: str | None = None,
) -> Dict[str, Any]:
    global _CACHE_HITS, _CACHE_MISSES

    runtime = RUNTIMES.get(discipline)
    if runtime is None:
        raise ValueError(f"Unsupported discipline: {discipline}")

    key = _cache_key(discipline, payload, calculation_type)
    now_ts = time.time()

    with _CACHE_LOCK:
        cached = _CACHE.get(key)
        if cached and (now_ts - cached["ts"]) <= CACHE_TTL_SEC:
            _CACHE_HITS += 1
            response = cached["value"]
            audit("calculation.cache_hit", {"discipline": discipline})
            return response

    _CACHE_MISSES += 1
    effective_calculation_type = calculation_type or runtime.default_calculation_type
    backend_result = runtime.service.evaluate(payload, calculation_type=effective_calculation_type)
    response = transform_to_frontend_response(discipline, backend_result)

    with _CACHE_LOCK:
        _CACHE[key] = {"ts": now_ts, "value": response}

    audit(
        "calculation.executed",
        {
            "discipline": discipline,
            "status": response.get("status"),
            "red_flags": len(response.get("flags", {}).get("red_flags", [])),
            "warnings": len(response.get("flags", {}).get("warnings", [])),
        },
    )
    return response


def execute_job(job_id: str) -> None:
    with _JOBS_LOCK:
        job = _JOBS.get(job_id)
        if not job or job["status"] == "cancelled":
            return
        job["status"] = "running"
        job["started_at"] = utc_now_iso()
        persistence.upsert_job(job)

    try:
        response = dispatch_calculation(
            discipline=job["discipline"],
            payload=job["payload"],
            calculation_type=job.get("calculation_type"),
        )
        with _JOBS_LOCK:
            target = _JOBS.get(job_id)
            if not target:
                return
            if target["status"] != "cancelled":
                target["status"] = "success"
                target["result"] = response
                target["completed_at"] = utc_now_iso()
                persistence.upsert_job(target)
        audit("job.success", {"job_id": job_id, "discipline": job["discipline"]})
    except Exception as exc:  # noqa: BLE001
        with _JOBS_LOCK:
            target = _JOBS.get(job_id)
            if not target:
                return
            if target["status"] != "cancelled":
                target["status"] = "error"
                target["error"] = str(exc)
                target["completed_at"] = utc_now_iso()
                persistence.upsert_job(target)
        audit("job.error", {"job_id": job_id, "discipline": job["discipline"], "error": str(exc)})


def get_session_key(discipline: str, project_id: str, asset_id: str) -> str:
    return f"{discipline}::{project_id}::{asset_id}"


def ensure_collab_session(discipline: str, project_id: str, asset_id: str) -> Dict[str, Any]:
    key = get_session_key(discipline, project_id, asset_id)
    with _COLLAB_LOCK:
        session = _COLLAB_SESSIONS.get(key)
        if session is None:
            session = {
                "key": key,
                "discipline": discipline,
                "project_id": project_id,
                "asset_id": asset_id,
                "comments": [],
                "approvals": [],
                "updated_at": utc_now_iso(),
            }
            _COLLAB_SESSIONS[key] = session
        return session


def new_job_record(
    *,
    discipline: str,
    payload: Mapping[str, Any],
    calculation_type: str | None,
) -> Dict[str, Any]:
    return {
        "job_id": str(uuid.uuid4()),
        "discipline": discipline,
        "payload": dict(payload),
        "calculation_type": calculation_type,
        "status": "pending",
        "created_at": utc_now_iso(),
        "started_at": None,
        "completed_at": None,
        "result": None,
        "error": None,
    }


def cache_stats_snapshot() -> Dict[str, Any]:
    with _CACHE_LOCK:
        size = len(_CACHE)
    return {
        "cache_size": size,
        "cache_hits": _CACHE_HITS,
        "cache_misses": _CACHE_MISSES,
        "cache_ttl_sec": CACHE_TTL_SEC,
    }


def clear_cache() -> None:
    with _CACHE_LOCK:
        _CACHE.clear()


def jobs_snapshot() -> List[Dict[str, Any]]:
    with _JOBS_LOCK:
        jobs = list(_JOBS.values())
    jobs.sort(key=lambda row: row["created_at"], reverse=True)
    return jobs


def get_job(job_id: str) -> Dict[str, Any] | None:
    with _JOBS_LOCK:
        job = _JOBS.get(job_id)
        return dict(job) if job else None


def create_job(job_record: Dict[str, Any]) -> str:
    job_id = job_record["job_id"]
    with _JOBS_LOCK:
        _JOBS[job_id] = job_record
        _JOB_FUTURES[job_id] = _JOB_EXECUTOR.submit(execute_job, job_id)
    persistence.upsert_job(job_record)
    return job_id


def cancel_job(job_id: str) -> Dict[str, Any] | None:
    with _JOBS_LOCK:
        job = _JOBS.get(job_id)
        if not job:
            return None
        if job["status"] in {"success", "error", "cancelled"}:
            return dict(job)

        job["status"] = "cancelled"
        job["completed_at"] = utc_now_iso()
        future = _JOB_FUTURES.get(job_id)
        if future:
            future.cancel()
        persistence.upsert_job(job)
        return dict(job)


def cancel_all_jobs() -> int:
    cancelled = 0
    with _JOBS_LOCK:
        for key, job in _JOBS.items():
            if job["status"] not in {"pending", "running"}:
                continue
            job["status"] = "cancelled"
            job["completed_at"] = utc_now_iso()
            future = _JOB_FUTURES.get(key)
            if future:
                future.cancel()
            persistence.upsert_job(job)
            cancelled += 1
    return cancelled


def retry_job(job_id: str) -> Dict[str, Any] | None:
    with _JOBS_LOCK:
        original = _JOBS.get(job_id)
        if not original:
            return None
        if original.get("discipline") not in RUNTIMES:
            raise ValueError("Unsupported discipline")

        cloned = new_job_record(
            discipline=str(original["discipline"]),
            payload=original.get("payload", {}),
            calculation_type=original.get("calculation_type"),
        )
        cloned_id = cloned["job_id"]
        _JOBS[cloned_id] = cloned
        _JOB_FUTURES[cloned_id] = _JOB_EXECUTOR.submit(execute_job, cloned_id)
        persistence.upsert_job(cloned)
        return {"job_id": cloned_id, "status": "pending"}


def pending_job_count() -> int:
    with _JOBS_LOCK:
        return sum(1 for item in _JOBS.values() if item["status"] in {"pending", "running"})

from __future__ import annotations

import asyncio
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timezone
from io import BytesIO
import json
import threading
import time
from typing import Any, Dict, List, Mapping, MutableMapping
import uuid
import zipfile

from fastapi import Body, FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from src.civil.service import CivilVerificationService
from src.electrical.service import ElectricalVerificationService
from src.instrumentation.service import InstrumentationVerificationService
from src.piping.service import PipingVerificationService
from src.rotating.service import RotatingVerificationService
from src.steel.service import SteelVerificationService
from src.vessel.service import VesselVerificationService
from src.api import persistence


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

# ----------------------------
# Runtime state (in-memory)
# ----------------------------
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


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _audit(event_type: str, details: Mapping[str, Any]) -> None:
    record = {
        "id": str(uuid.uuid4()),
        "timestamp": _utc_now_iso(),
        "event_type": event_type,
        "details": dict(details),
    }
    with _AUDIT_LOCK:
        _AUDIT_LOGS.append(record)
        if len(_AUDIT_LOGS) > _AUDIT_MAX:
            del _AUDIT_LOGS[: len(_AUDIT_LOGS) - _AUDIT_MAX]
    persistence.persist_audit(record)


def supported_disciplines() -> List[str]:
    return sorted(RUNTIMES.keys())


def _normalize_flags(payload: Mapping[str, Any]) -> Dict[str, List[str]]:
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
    flags = _normalize_flags(backend_result)
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
            _audit("calculation.cache_hit", {"discipline": discipline})
            return response

    _CACHE_MISSES += 1
    effective_calculation_type = calculation_type or runtime.default_calculation_type
    backend_result = runtime.service.evaluate(payload, calculation_type=effective_calculation_type)
    response = transform_to_frontend_response(discipline, backend_result)

    with _CACHE_LOCK:
        _CACHE[key] = {"ts": now_ts, "value": response}

    _audit(
        "calculation.executed",
        {
            "discipline": discipline,
            "status": response.get("status"),
            "red_flags": len(response.get("flags", {}).get("red_flags", [])),
            "warnings": len(response.get("flags", {}).get("warnings", [])),
        },
    )
    return response


def _execute_job(job_id: str) -> None:
    with _JOBS_LOCK:
        job = _JOBS.get(job_id)
        if not job:
            return
        if job["status"] == "cancelled":
            return
        job["status"] = "running"
        job["started_at"] = _utc_now_iso()
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
                target["completed_at"] = _utc_now_iso()
                persistence.upsert_job(target)
        _audit("job.success", {"job_id": job_id, "discipline": job["discipline"]})
    except Exception as exc:  # noqa: BLE001
        with _JOBS_LOCK:
            target = _JOBS.get(job_id)
            if not target:
                return
            if target["status"] != "cancelled":
                target["status"] = "error"
                target["error"] = str(exc)
                target["completed_at"] = _utc_now_iso()
                persistence.upsert_job(target)
        _audit("job.error", {"job_id": job_id, "discipline": job["discipline"], "error": str(exc)})


def _get_session_key(discipline: str, project_id: str, asset_id: str) -> str:
    return f"{discipline}::{project_id}::{asset_id}"


def _ensure_collab_session(discipline: str, project_id: str, asset_id: str) -> Dict[str, Any]:
    key = _get_session_key(discipline, project_id, asset_id)
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
                "updated_at": _utc_now_iso(),
            }
            _COLLAB_SESSIONS[key] = session
        return session


def _new_job_record(
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
        "created_at": _utc_now_iso(),
        "started_at": None,
        "completed_at": None,
        "result": None,
        "error": None,
    }


def create_app() -> FastAPI:
    app = FastAPI(
        title="EPC Engineering Calculation API",
        version="0.2.0",
        description="Seven-discipline verification API with queue/collab/audit/report extensions.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health() -> Dict[str, Any]:
        with _JOBS_LOCK:
            pending_jobs = sum(1 for item in _JOBS.values() if item["status"] in {"pending", "running"})
        return {
            "status": "ok",
            "disciplines": supported_disciplines(),
            "pending_jobs": pending_jobs,
            "version": "0.2.0",
        }

    @app.post("/api/calculate/{discipline}")
    def calculate(
        discipline: str,
        payload: Dict[str, Any] = Body(default_factory=dict),
        calculation_type: str | None = Query(default=None),
    ) -> Dict[str, Any]:
        if discipline not in RUNTIMES:
            raise HTTPException(status_code=400, detail=f"Unsupported discipline: {discipline}")
        try:
            return dispatch_calculation(discipline, payload, calculation_type=calculation_type)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except Exception as exc:  # noqa: BLE001
            raise HTTPException(status_code=500, detail=f"Calculation failed: {exc}") from exc

    @app.post("/api/jobs/cancel-all")
    def cancel_all_jobs() -> Dict[str, Any]:
        cancelled = 0
        with _JOBS_LOCK:
            for key, job in _JOBS.items():
                if job["status"] not in {"pending", "running"}:
                    continue
                job["status"] = "cancelled"
                job["completed_at"] = _utc_now_iso()
                future = _JOB_FUTURES.get(key)
                if future:
                    future.cancel()
                persistence.upsert_job(job)
                cancelled += 1
        _audit("job.cancelled.bulk", {"count": cancelled})
        return {"status": "ok", "cancelled": cancelled}

    @app.post("/api/jobs/{job_id}/retry")
    def retry_job(job_id: str) -> Dict[str, Any]:
        with _JOBS_LOCK:
            original = _JOBS.get(job_id)
            if not original:
                raise HTTPException(status_code=404, detail="Job not found")
            if original.get("discipline") not in RUNTIMES:
                raise HTTPException(status_code=400, detail="Unsupported discipline")

            cloned = _new_job_record(
                discipline=str(original["discipline"]),
                payload=original.get("payload", {}),
                calculation_type=original.get("calculation_type"),
            )
            cloned_id = cloned["job_id"]
            _JOBS[cloned_id] = cloned
            _JOB_FUTURES[cloned_id] = _JOB_EXECUTOR.submit(_execute_job, cloned_id)
            persistence.upsert_job(cloned)

        _audit("job.retried", {"source_job_id": job_id, "new_job_id": cloned_id})
        return {"job_id": cloned_id, "status": "pending"}

    @app.post("/api/jobs/{job_id}/cancel")
    def cancel_job(job_id: str) -> Dict[str, Any]:
        with _JOBS_LOCK:
            job = _JOBS.get(job_id)
            if not job:
                raise HTTPException(status_code=404, detail="Job not found")
            if job["status"] in {"success", "error", "cancelled"}:
                return {"job_id": job_id, "status": job["status"]}

            job["status"] = "cancelled"
            job["completed_at"] = _utc_now_iso()
            future = _JOB_FUTURES.get(job_id)
            if future:
                future.cancel()
            persistence.upsert_job(job)

        _audit("job.cancelled", {"job_id": job_id})
        return {"job_id": job_id, "status": "cancelled"}

    @app.post("/api/jobs/{discipline}")
    def create_job(
        discipline: str,
        payload: Dict[str, Any] = Body(default_factory=dict),
        calculation_type: str | None = Query(default=None),
    ) -> Dict[str, Any]:
        if discipline not in RUNTIMES:
            raise HTTPException(status_code=400, detail=f"Unsupported discipline: {discipline}")

        job_record = _new_job_record(discipline=discipline, payload=payload, calculation_type=calculation_type)
        job_id = job_record["job_id"]

        with _JOBS_LOCK:
            _JOBS[job_id] = job_record
            _JOB_FUTURES[job_id] = _JOB_EXECUTOR.submit(_execute_job, job_id)
        persistence.upsert_job(job_record)

        _audit("job.created", {"job_id": job_id, "discipline": discipline})
        return {
            "job_id": job_id,
            "status": "pending",
        }

    @app.get("/api/jobs/{job_id}")
    def get_job(job_id: str) -> Dict[str, Any]:
        with _JOBS_LOCK:
            job = _JOBS.get(job_id)
            if not job:
                raise HTTPException(status_code=404, detail="Job not found")
            return dict(job)

    @app.get("/api/jobs")
    def list_jobs(status: str | None = Query(default=None), limit: int = Query(default=100, ge=1, le=1000)) -> Dict[str, Any]:
        with _JOBS_LOCK:
            jobs = list(_JOBS.values())
        jobs.sort(key=lambda row: row["created_at"], reverse=True)
        if status:
            jobs = [row for row in jobs if row.get("status") == status]
        return {
            "jobs": jobs[:limit],
            "count": len(jobs),
        }

    @app.post("/api/analysis/sensitivity/{discipline}")
    def sensitivity_analysis(
        discipline: str,
        body: Dict[str, Any] = Body(default_factory=dict),
    ) -> Dict[str, Any]:
        if discipline not in RUNTIMES:
            raise HTTPException(status_code=400, detail=f"Unsupported discipline: {discipline}")

        base_input = body.get("base_input") if isinstance(body.get("base_input"), Mapping) else {}
        variable = str(body.get("variable") or "")
        delta_pct = float(body.get("delta_pct") or 10)
        points = int(body.get("points") or 5)
        points = max(3, min(9, points if points % 2 == 1 else points + 1))

        if not variable:
            raise HTTPException(status_code=400, detail="variable is required")

        current = float(base_input.get(variable, 0))
        half = points // 2
        step = delta_pct / half if half else delta_pct

        rows: List[Dict[str, Any]] = []
        for index in range(-half, half + 1):
            pct = index * step
            factor = 1 + (pct / 100.0)
            adjusted = current * factor
            payload = dict(base_input)
            payload[variable] = adjusted
            result = dispatch_calculation(discipline, payload, calculation_type=None)
            rows.append(
                {
                    "label": f"{pct:+.2f}%",
                    "value": adjusted,
                    "status": result.get("status"),
                    "red_flags": len(result.get("flags", {}).get("red_flags", [])),
                    "warnings": len(result.get("flags", {}).get("warnings", [])),
                    "result": result.get("results", {}),
                }
            )

        _audit("analysis.sensitivity", {"discipline": discipline, "variable": variable, "points": points})
        return {
            "discipline": discipline,
            "variable": variable,
            "delta_pct": delta_pct,
            "points": points,
            "rows": rows,
        }

    @app.get("/api/audit/logs")
    def list_audit_logs(
        event_type: str | None = Query(default=None),
        limit: int = Query(default=200, ge=1, le=2000),
    ) -> Dict[str, Any]:
        with _AUDIT_LOCK:
            rows = list(_AUDIT_LOGS)
        rows.sort(key=lambda row: row["timestamp"], reverse=True)
        if event_type:
            rows = [row for row in rows if row.get("event_type") == event_type]
        return {
            "logs": rows[:limit],
            "count": len(rows),
        }

    @app.get("/api/audit/summary")
    def audit_summary() -> Dict[str, Any]:
        with _AUDIT_LOCK:
            rows = list(_AUDIT_LOGS)
        counts: MutableMapping[str, int] = {}
        for row in rows:
            key = str(row.get("event_type") or "unknown")
            counts[key] = counts.get(key, 0) + 1
        top = sorted(counts.items(), key=lambda item: item[1], reverse=True)[:20]
        return {
            "total": len(rows),
            "by_event_type": [{"event_type": key, "count": value} for key, value in top],
        }

    @app.get("/api/perf/cache-stats")
    def cache_stats() -> Dict[str, Any]:
        with _CACHE_LOCK:
            size = len(_CACHE)
        return {
            "cache_size": size,
            "cache_hits": _CACHE_HITS,
            "cache_misses": _CACHE_MISSES,
            "cache_ttl_sec": CACHE_TTL_SEC,
        }

    @app.post("/api/perf/cache-clear")
    def clear_cache() -> Dict[str, Any]:
        with _CACHE_LOCK:
            _CACHE.clear()
        _audit("cache.cleared", {})
        return {"status": "ok"}

    @app.get("/api/perf/persistence-stats")
    def persistence_stats() -> Dict[str, Any]:
        return persistence.stats()

    @app.get("/api/collab/{discipline}/{project_id}/{asset_id}")
    def get_collab_session(discipline: str, project_id: str, asset_id: str) -> Dict[str, Any]:
        if discipline not in RUNTIMES:
            raise HTTPException(status_code=400, detail=f"Unsupported discipline: {discipline}")
        session = _ensure_collab_session(discipline, project_id, asset_id)
        return dict(session)

    @app.post("/api/collab/{discipline}/{project_id}/{asset_id}/comments")
    def add_comment(
        discipline: str,
        project_id: str,
        asset_id: str,
        body: Dict[str, Any] = Body(default_factory=dict),
    ) -> Dict[str, Any]:
        session = _ensure_collab_session(discipline, project_id, asset_id)
        author = str(body.get("author") or "anonymous")
        message = str(body.get("message") or "").strip()
        if not message:
            raise HTTPException(status_code=400, detail="message is required")

        comment = {
            "id": str(uuid.uuid4()),
            "author": author,
            "message": message,
            "created_at": _utc_now_iso(),
        }
        with _COLLAB_LOCK:
            session["comments"].append(comment)
            session["updated_at"] = _utc_now_iso()
        persistence.persist_collab_event(
            {
                "id": comment["id"],
                "timestamp": comment["created_at"],
                "discipline": discipline,
                "project_id": project_id,
                "asset_id": asset_id,
                "event_type": "comment",
                "actor": author,
                "payload": comment,
            }
        )
        _audit("collab.comment", {"discipline": discipline, "project_id": project_id, "asset_id": asset_id, "author": author})
        return {"comment": comment}

    @app.post("/api/collab/{discipline}/{project_id}/{asset_id}/approvals")
    def add_approval(
        discipline: str,
        project_id: str,
        asset_id: str,
        body: Dict[str, Any] = Body(default_factory=dict),
    ) -> Dict[str, Any]:
        session = _ensure_collab_session(discipline, project_id, asset_id)
        reviewer = str(body.get("reviewer") or "anonymous")
        decision = str(body.get("decision") or "review")
        note = str(body.get("note") or "")

        approval = {
            "id": str(uuid.uuid4()),
            "reviewer": reviewer,
            "decision": decision,
            "note": note,
            "created_at": _utc_now_iso(),
        }
        with _COLLAB_LOCK:
            session["approvals"].append(approval)
            session["updated_at"] = _utc_now_iso()
        persistence.persist_collab_event(
            {
                "id": approval["id"],
                "timestamp": approval["created_at"],
                "discipline": discipline,
                "project_id": project_id,
                "asset_id": asset_id,
                "event_type": "approval",
                "actor": reviewer,
                "payload": approval,
            }
        )
        _audit(
            "collab.approval",
            {
                "discipline": discipline,
                "project_id": project_id,
                "asset_id": asset_id,
                "reviewer": reviewer,
                "decision": decision,
            },
        )
        return {"approval": approval}

    @app.post("/api/report/package")
    def report_package(body: Dict[str, Any] = Body(default_factory=dict)) -> StreamingResponse:
        discipline = str(body.get("discipline") or "")
        if not discipline:
            raise HTTPException(status_code=400, detail="discipline is required")

        project_id = str(body.get("project_id") or "PROJECT-UNKNOWN")
        asset_id = str(body.get("asset_id") or "ASSET-UNKNOWN")
        active_result = body.get("active_result") if isinstance(body.get("active_result"), Mapping) else None
        scenario_results = body.get("scenario_results") if isinstance(body.get("scenario_results"), list) else []
        batch_results = body.get("batch_results") if isinstance(body.get("batch_results"), list) else []

        summary_md = [
            f"# Report Package ({discipline.upper()})",
            "",
            f"- Project: {project_id}",
            f"- Asset: {asset_id}",
            f"- Generated: {_utc_now_iso()}",
            "",
            "## Scenario Results",
            f"- Count: {len(scenario_results)}",
            "",
            "## Batch Results",
            f"- Count: {len(batch_results)}",
            "",
        ]

        pack_json = {
            "generated_at": _utc_now_iso(),
            "discipline": discipline,
            "project_id": project_id,
            "asset_id": asset_id,
            "active_result": active_result,
            "scenario_results": scenario_results,
            "batch_results": batch_results,
        }

        with _AUDIT_LOCK:
            logs = list(_AUDIT_LOGS)[-200:]

        stream = BytesIO()
        with zipfile.ZipFile(stream, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("report_summary.md", "\n".join(summary_md))
            archive.writestr("report_payload.json", json.dumps(pack_json, indent=2, ensure_ascii=False, default=str))
            archive.writestr("audit_logs.json", json.dumps(logs, indent=2, ensure_ascii=False, default=str))
            archive.writestr("README.txt", "Package includes summary, payload, and audit logs.")

        stream.seek(0)
        _audit("report.package", {"discipline": discipline, "project_id": project_id, "asset_id": asset_id})
        return StreamingResponse(
            stream,
            media_type="application/zip",
            headers={"Content-Disposition": f'attachment; filename="report_package_{discipline}_{int(time.time())}.zip"'},
        )

    @app.websocket("/ws/jobs/{job_id}")
    async def ws_job_status(websocket: WebSocket, job_id: str) -> None:
        await websocket.accept()
        try:
            while True:
                with _JOBS_LOCK:
                    job = _JOBS.get(job_id)
                    if not job:
                        await websocket.send_json({"job_id": job_id, "status": "not_found"})
                        break
                    snapshot = dict(job)
                await websocket.send_json(snapshot)
                if snapshot.get("status") in {"success", "error", "cancelled"}:
                    break
                await asyncio.sleep(0.5)
        except WebSocketDisconnect:
            return

    return app


app = create_app()

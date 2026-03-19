from __future__ import annotations

import asyncio
from io import BytesIO
import json
import time
from typing import Any, Dict, List, Mapping, MutableMapping
import uuid
import zipfile

from fastapi import Body, FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from src.api import persistence
from src.api import runtime_core

dispatch_calculation = runtime_core.dispatch_calculation
supported_disciplines = runtime_core.supported_disciplines


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
        pending_jobs = runtime_core.pending_job_count()
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
        if discipline not in runtime_core.RUNTIMES:
            raise HTTPException(status_code=400, detail=f"Unsupported discipline: {discipline}")
        try:
            return dispatch_calculation(discipline, payload, calculation_type=calculation_type)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except Exception as exc:  # noqa: BLE001
            raise HTTPException(status_code=500, detail=f"Calculation failed: {exc}") from exc

    @app.post("/api/jobs/cancel-all")
    def cancel_all_jobs() -> Dict[str, Any]:
        cancelled = runtime_core.cancel_all_jobs()
        runtime_core.audit("job.cancelled.bulk", {"count": cancelled})
        return {"status": "ok", "cancelled": cancelled}

    @app.post("/api/jobs/{job_id}/retry")
    def retry_job(job_id: str) -> Dict[str, Any]:
        try:
            retried = runtime_core.retry_job(job_id)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        if retried is None:
            raise HTTPException(status_code=404, detail="Job not found")
        runtime_core.audit("job.retried", {"source_job_id": job_id, "new_job_id": retried["job_id"]})
        return retried

    @app.post("/api/jobs/{job_id}/cancel")
    def cancel_job(job_id: str) -> Dict[str, Any]:
        job = runtime_core.cancel_job(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found")
        runtime_core.audit("job.cancelled", {"job_id": job_id})
        return {"job_id": job_id, "status": job["status"]}

    @app.post("/api/jobs/{discipline}")
    def create_job(
        discipline: str,
        payload: Dict[str, Any] = Body(default_factory=dict),
        calculation_type: str | None = Query(default=None),
    ) -> Dict[str, Any]:
        if discipline not in runtime_core.RUNTIMES:
            raise HTTPException(status_code=400, detail=f"Unsupported discipline: {discipline}")

        job_record = runtime_core.new_job_record(discipline=discipline, payload=payload, calculation_type=calculation_type)
        job_id = runtime_core.create_job(job_record)
        runtime_core.audit("job.created", {"job_id": job_id, "discipline": discipline})
        return {
            "job_id": job_id,
            "status": "pending",
        }

    @app.get("/api/jobs/{job_id}")
    def get_job(job_id: str) -> Dict[str, Any]:
        job = runtime_core.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job

    @app.get("/api/jobs")
    def list_jobs(status: str | None = Query(default=None), limit: int = Query(default=100, ge=1, le=1000)) -> Dict[str, Any]:
        jobs = runtime_core.jobs_snapshot()
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
        if discipline not in runtime_core.RUNTIMES:
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

        runtime_core.audit("analysis.sensitivity", {"discipline": discipline, "variable": variable, "points": points})
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
        rows = runtime_core.recent_audit_logs()
        if event_type:
            rows = [row for row in rows if row.get("event_type") == event_type]
        return {
            "logs": rows[:limit],
            "count": len(rows),
        }

    @app.get("/api/audit/summary")
    def audit_summary() -> Dict[str, Any]:
        rows = runtime_core.recent_audit_logs(limit=None)
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
        return runtime_core.cache_stats_snapshot()

    @app.post("/api/perf/cache-clear")
    def clear_cache() -> Dict[str, Any]:
        runtime_core.clear_cache()
        runtime_core.audit("cache.cleared", {})
        return {"status": "ok"}

    @app.get("/api/perf/persistence-stats")
    def persistence_stats() -> Dict[str, Any]:
        return persistence.stats()

    @app.get("/api/collab/{discipline}/{project_id}/{asset_id}")
    def get_collab_session(discipline: str, project_id: str, asset_id: str) -> Dict[str, Any]:
        if discipline not in runtime_core.RUNTIMES:
            raise HTTPException(status_code=400, detail=f"Unsupported discipline: {discipline}")
        session = runtime_core.ensure_collab_session(discipline, project_id, asset_id)
        return dict(session)

    @app.post("/api/collab/{discipline}/{project_id}/{asset_id}/comments")
    def add_comment(
        discipline: str,
        project_id: str,
        asset_id: str,
        body: Dict[str, Any] = Body(default_factory=dict),
    ) -> Dict[str, Any]:
        session = runtime_core.ensure_collab_session(discipline, project_id, asset_id)
        author = str(body.get("author") or "anonymous")
        message = str(body.get("message") or "").strip()
        if not message:
            raise HTTPException(status_code=400, detail="message is required")

        comment = {
            "id": str(uuid.uuid4()),
            "author": author,
            "message": message,
            "created_at": runtime_core.utc_now_iso(),
        }
        with runtime_core._COLLAB_LOCK:
            session["comments"].append(comment)
            session["updated_at"] = runtime_core.utc_now_iso()
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
        runtime_core.audit("collab.comment", {"discipline": discipline, "project_id": project_id, "asset_id": asset_id, "author": author})
        return {"comment": comment}

    @app.post("/api/collab/{discipline}/{project_id}/{asset_id}/approvals")
    def add_approval(
        discipline: str,
        project_id: str,
        asset_id: str,
        body: Dict[str, Any] = Body(default_factory=dict),
    ) -> Dict[str, Any]:
        session = runtime_core.ensure_collab_session(discipline, project_id, asset_id)
        reviewer = str(body.get("reviewer") or "anonymous")
        decision = str(body.get("decision") or "review")
        note = str(body.get("note") or "")

        approval = {
            "id": str(uuid.uuid4()),
            "reviewer": reviewer,
            "decision": decision,
            "note": note,
            "created_at": runtime_core.utc_now_iso(),
        }
        with runtime_core._COLLAB_LOCK:
            session["approvals"].append(approval)
            session["updated_at"] = runtime_core.utc_now_iso()
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
        runtime_core.audit(
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
            f"- Generated: {runtime_core.utc_now_iso()}",
            "",
            "## Scenario Results",
            f"- Count: {len(scenario_results)}",
            "",
            "## Batch Results",
            f"- Count: {len(batch_results)}",
            "",
        ]

        pack_json = {
            "generated_at": runtime_core.utc_now_iso(),
            "discipline": discipline,
            "project_id": project_id,
            "asset_id": asset_id,
            "active_result": active_result,
            "scenario_results": scenario_results,
            "batch_results": batch_results,
        }

        logs = runtime_core.recent_audit_logs(limit=200)

        stream = BytesIO()
        with zipfile.ZipFile(stream, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("report_summary.md", "\n".join(summary_md))
            archive.writestr("report_payload.json", json.dumps(pack_json, indent=2, ensure_ascii=False, default=str))
            archive.writestr("audit_logs.json", json.dumps(logs, indent=2, ensure_ascii=False, default=str))
            archive.writestr("README.txt", "Package includes summary, payload, and audit logs.")

        stream.seek(0)
        runtime_core.audit("report.package", {"discipline": discipline, "project_id": project_id, "asset_id": asset_id})
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
                snapshot = runtime_core.get_job(job_id)
                if not snapshot:
                    await websocket.send_json({"job_id": job_id, "status": "not_found"})
                    break
                await websocket.send_json(snapshot)
                if snapshot.get("status") in {"success", "error", "cancelled"}:
                    break
                await asyncio.sleep(0.5)
        except WebSocketDisconnect:
            return

    return app


app = create_app()

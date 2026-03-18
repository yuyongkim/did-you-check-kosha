from __future__ import annotations

import atexit
import json
import sqlite3
import threading
from pathlib import Path
from typing import Any, Mapping

_DB_PATH = Path("logs/api_runtime.sqlite3")
_LOCK = threading.Lock()


def _connect() -> sqlite3.Connection:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(_DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn


_CONN = _connect()


def close_db() -> None:
    with _LOCK:
        try:
            _CONN.close()
        except Exception:
            pass


atexit.register(close_db)


def init_db() -> None:
    with _LOCK:
        _CONN.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_logs (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                details_json TEXT NOT NULL
            )
            """
        )
        _CONN.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                job_id TEXT PRIMARY KEY,
                discipline TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                started_at TEXT,
                completed_at TEXT,
                error TEXT,
                payload_json TEXT,
                result_json TEXT
            )
            """
        )
        _CONN.execute(
            """
            CREATE TABLE IF NOT EXISTS collab_events (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                discipline TEXT NOT NULL,
                project_id TEXT NOT NULL,
                asset_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                actor TEXT,
                payload_json TEXT NOT NULL
            )
            """
        )
        _CONN.commit()


def persist_audit(record: Mapping[str, Any]) -> None:
    with _LOCK:
        _CONN.execute(
            "INSERT OR REPLACE INTO audit_logs (id, timestamp, event_type, details_json) VALUES (?, ?, ?, ?)",
            (
                str(record.get("id", "")),
                str(record.get("timestamp", "")),
                str(record.get("event_type", "")),
                json.dumps(record.get("details", {}), ensure_ascii=False, default=str),
            ),
        )
        _CONN.commit()


def upsert_job(job: Mapping[str, Any]) -> None:
    with _LOCK:
        _CONN.execute(
            """
            INSERT OR REPLACE INTO jobs (
                job_id, discipline, status, created_at, started_at, completed_at, error, payload_json, result_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(job.get("job_id", "")),
                str(job.get("discipline", "")),
                str(job.get("status", "")),
                str(job.get("created_at", "")),
                str(job.get("started_at") or ""),
                str(job.get("completed_at") or ""),
                str(job.get("error") or ""),
                json.dumps(job.get("payload", {}), ensure_ascii=False, default=str),
                json.dumps(job.get("result", {}), ensure_ascii=False, default=str),
            ),
        )
        _CONN.commit()


def persist_collab_event(event: Mapping[str, Any]) -> None:
    with _LOCK:
        _CONN.execute(
            """
            INSERT OR REPLACE INTO collab_events (
                id, timestamp, discipline, project_id, asset_id, event_type, actor, payload_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(event.get("id", "")),
                str(event.get("timestamp", "")),
                str(event.get("discipline", "")),
                str(event.get("project_id", "")),
                str(event.get("asset_id", "")),
                str(event.get("event_type", "")),
                str(event.get("actor") or ""),
                json.dumps(event.get("payload", {}), ensure_ascii=False, default=str),
            ),
        )
        _CONN.commit()


def stats() -> dict[str, int]:
    with _LOCK:
        audit = _CONN.execute("SELECT COUNT(*) FROM audit_logs").fetchone()[0]
        jobs = _CONN.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
        collab = _CONN.execute("SELECT COUNT(*) FROM collab_events").fetchone()[0]
    return {
        "audit_rows": int(audit),
        "job_rows": int(jobs),
        "collab_rows": int(collab),
    }

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


def request_json(method: str, url: str, payload: dict | None = None) -> tuple[int, dict]:
    data = None
    headers = {"Content-Type": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        status = resp.getcode()
        body = resp.read().decode("utf-8")
    return status, json.loads(body) if body else {}


def main() -> int:
    parser = argparse.ArgumentParser(description="API regression smoke")
    parser.add_argument("--base-url", default="http://localhost:8000")
    parser.add_argument("--spawn-server", action="store_true")
    args = parser.parse_args()

    base = args.base_url.rstrip("/")
    spawned: subprocess.Popen[str] | None = None
    host = urllib.parse.urlparse(base).hostname or "127.0.0.1"
    port = urllib.parse.urlparse(base).port or 8000

    checks: list[tuple[str, bool, str]] = []

    try:
        if args.spawn_server:
            cmd = [sys.executable, "scripts/run_api_server.py"]
            env = os.environ.copy()
            env["EPC_API_HOST"] = host
            env["EPC_API_PORT"] = str(port)
            spawned = subprocess.Popen(cmd, env=env)  # noqa: S603
            for _ in range(100):
                try:
                    status, _ = request_json("GET", f"{base}/health")
                    if status == 200:
                        break
                except Exception:  # noqa: BLE001
                    pass
                time.sleep(0.1)

        status, body = request_json("GET", f"{base}/health")
        checks.append(("health", status == 200 and body.get("status") == "ok", str(body)))

        create_payload = {
            "design_pressure_mpa": 1.2,
            "design_temperature_c": 120,
            "od_mm": 168.3,
            "t_current_mm": 8.2,
            "corrosion_allowance_mm": 3.0,
            "allowable_stress_mpa": 120,
            "joint_efficiency": 1.0,
        }
        status, calc = request_json("POST", f"{base}/api/calculate/piping", create_payload)
        checks.append(("calculate", status == 200 and "status" in calc, calc.get("status", "")))

        status, job = request_json("POST", f"{base}/api/jobs/piping", create_payload)
        job_id = str(job.get("job_id", ""))
        checks.append(("job.create", status == 200 and bool(job_id), job_id))

        final_status = "pending"
        if job_id:
            for _ in range(80):
                status, info = request_json("GET", f"{base}/api/jobs/{job_id}")
                if status != 200:
                    break
                final_status = str(info.get("status"))
                if final_status in {"success", "error", "cancelled"}:
                    break
                time.sleep(0.1)
        checks.append(("job.poll", final_status in {"success", "error", "cancelled"}, final_status))

        if job_id:
            status, retried = request_json("POST", f"{base}/api/jobs/{job_id}/retry")
            checks.append(("job.retry", status == 200 and bool(retried.get("job_id")), str(retried)))

        status, cancelled = request_json("POST", f"{base}/api/jobs/cancel-all")
        checks.append(("job.cancel_all", status == 200 and "cancelled" in cancelled, str(cancelled)))

        status, sens = request_json(
            "POST",
            f"{base}/api/analysis/sensitivity/piping",
            {
                "base_input": create_payload,
                "variable": "design_pressure_mpa",
                "delta_pct": 20,
                "points": 5,
            },
        )
        checks.append(("analysis.sensitivity", status == 200 and len(sens.get("rows", [])) == 5, str(len(sens.get("rows", [])))))

        status, collab = request_json("POST", f"{base}/api/collab/piping/PROJECT-A/ASSET-1/comments", {"author": "smoke", "message": "ok"})
        checks.append(("collab.comment", status == 200 and "comment" in collab, "comment"))

        status, audit = request_json("GET", f"{base}/api/audit/logs?limit=20")
        checks.append(("audit.logs", status == 200 and isinstance(audit.get("logs"), list), str(audit.get("count", 0))))

        status, audit_summary = request_json("GET", f"{base}/api/audit/summary")
        checks.append(("audit.summary", status == 200 and "total" in audit_summary, str(audit_summary.get("total"))))

        status, cache = request_json("GET", f"{base}/api/perf/cache-stats")
        checks.append(("cache.stats", status == 200 and "cache_hits" in cache, str(cache)))

        status, persistence = request_json("GET", f"{base}/api/perf/persistence-stats")
        checks.append(("persistence.stats", status == 200 and "audit_rows" in persistence, str(persistence)))

    except urllib.error.URLError as exc:
        print(f"[ERROR] Unable to reach API: {exc}")
        return 2
    finally:
        if spawned is not None:
            spawned.terminate()
            try:
                spawned.wait(timeout=10)
            except subprocess.TimeoutExpired:
                spawned.kill()

    passed = sum(1 for _, ok, _ in checks if ok)
    total = len(checks)
    print("\n== API Regression Smoke ==")
    for name, ok, detail in checks:
        print(f"- {'PASS' if ok else 'FAIL'} | {name} | {detail}")

    print(f"\nSummary: {passed}/{total} passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())

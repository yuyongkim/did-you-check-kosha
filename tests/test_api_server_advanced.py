from __future__ import annotations

import time
import unittest

from fastapi.testclient import TestClient

from src.api.server import create_app


class ApiServerAdvancedTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(create_app())

    def test_job_queue_lifecycle(self) -> None:
        create = self.client.post("/api/jobs/piping", json={"design_pressure_mpa": 1.0, "design_temperature_c": 100, "od_mm": 168.3, "t_current_mm": 8.0})
        self.assertEqual(create.status_code, 200)
        job_id = create.json()["job_id"]

        status = "pending"
        for _ in range(60):
            resp = self.client.get(f"/api/jobs/{job_id}")
            self.assertEqual(resp.status_code, 200)
            status = resp.json()["status"]
            if status in {"success", "error", "cancelled"}:
                break
            time.sleep(0.02)

        self.assertIn(status, {"success", "error", "cancelled"})

        retry = self.client.post(f"/api/jobs/{job_id}/retry")
        self.assertEqual(retry.status_code, 200)
        self.assertIn("job_id", retry.json())

        cancel_all = self.client.post("/api/jobs/cancel-all")
        self.assertEqual(cancel_all.status_code, 200)
        self.assertIn("cancelled", cancel_all.json())

    def test_sensitivity_and_cache_stats(self) -> None:
        response = self.client.post(
            "/api/analysis/sensitivity/piping",
            json={
                "base_input": {
                    "design_pressure_mpa": 1.2,
                    "design_temperature_c": 120,
                    "od_mm": 168.3,
                    "t_current_mm": 8.0,
                    "corrosion_allowance_mm": 3.0,
                    "allowable_stress_mpa": 120,
                    "joint_efficiency": 1.0,
                },
                "variable": "design_pressure_mpa",
                "delta_pct": 20,
                "points": 5,
            },
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["points"], 5)
        self.assertEqual(len(body["rows"]), 5)

        cache = self.client.get("/api/perf/cache-stats")
        self.assertEqual(cache.status_code, 200)
        self.assertIn("cache_hits", cache.json())

        summary = self.client.get("/api/audit/summary")
        self.assertEqual(summary.status_code, 200)
        self.assertIn("total", summary.json())

        persistence = self.client.get("/api/perf/persistence-stats")
        self.assertEqual(persistence.status_code, 200)
        self.assertIn("audit_rows", persistence.json())

    def test_collab_and_report_package(self) -> None:
        comment = self.client.post(
            "/api/collab/piping/PROJECT-A/ASSET-1/comments",
            json={"author": "qa", "message": "Need review"},
        )
        self.assertEqual(comment.status_code, 200)

        approval = self.client.post(
            "/api/collab/piping/PROJECT-A/ASSET-1/approvals",
            json={"reviewer": "lead", "decision": "approved", "note": "ok"},
        )
        self.assertEqual(approval.status_code, 200)

        session = self.client.get("/api/collab/piping/PROJECT-A/ASSET-1")
        self.assertEqual(session.status_code, 200)
        session_body = session.json()
        self.assertGreaterEqual(len(session_body["comments"]), 1)
        self.assertGreaterEqual(len(session_body["approvals"]), 1)

        package = self.client.post(
            "/api/report/package",
            json={
                "discipline": "piping",
                "project_id": "PROJECT-A",
                "asset_id": "ASSET-1",
                "scenario_results": [{"label": "case1"}],
                "batch_results": [{"rowId": "A1"}],
            },
        )
        self.assertEqual(package.status_code, 200)
        self.assertTrue(package.headers["content-type"].startswith("application/zip"))

    def test_websocket_job_stream(self) -> None:
        create = self.client.post(
            "/api/jobs/piping",
            json={
                "design_pressure_mpa": 1.2,
                "design_temperature_c": 120,
                "od_mm": 168.3,
                "t_current_mm": 8.0,
                "corrosion_allowance_mm": 3.0,
                "allowable_stress_mpa": 120,
                "joint_efficiency": 1.0,
            },
        )
        self.assertEqual(create.status_code, 200)
        job_id = create.json()["job_id"]
        with self.client.websocket_connect(f"/ws/jobs/{job_id}") as websocket:
            message = websocket.receive_json()
            self.assertIn("status", message)


if __name__ == "__main__":
    unittest.main()

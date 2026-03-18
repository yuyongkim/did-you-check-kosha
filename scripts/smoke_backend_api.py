from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Dict

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
EXPECTED_DISCIPLINES = {
    "piping",
    "vessel",
    "rotating",
    "electrical",
    "instrumentation",
    "steel",
    "civil",
}


def health_url(host: str, port: int) -> str:
    return f"http://{host}:{port}/health"


def calculate_url_prefix(host: str, port: int) -> str:
    return f"http://{host}:{port}/api/calculate/"


def sample_payloads() -> Dict[str, Dict[str, Any]]:
    return {
        "piping": {
            "material": "SA-106 Gr.B",
            "nps": 6.0,
            "design_pressure_mpa": 4.5,
            "design_temperature_c": 250.0,
            "thickness_history": [
                {"date": "2015-01-01", "thickness_mm": 10.0},
                {"date": "2020-01-01", "thickness_mm": 8.6},
                {"date": "2025-01-01", "thickness_mm": 7.3},
            ],
            "corrosion_allowance_mm": 1.5,
            "weld_type": "seamless",
            "service_type": "general",
            "has_internal_coating": False,
        },
        "vessel": {
            "material": "SA-516-70",
            "design_pressure_mpa": 2.0,
            "design_temperature_c": 200.0,
            "inside_radius_mm": 750.0,
            "joint_efficiency": 0.85,
            "t_current_mm": 18.0,
            "corrosion_allowance_mm": 1.5,
            "assumed_corrosion_rate_mm_per_year": 0.2,
        },
        "rotating": {
            "machine_type": "pump",
            "vibration_mm_per_s": 2.5,
            "nozzle_load_ratio": 0.85,
            "bearing_temperature_c": 72.0,
            "speed_rpm": 1800,
        },
        "electrical": {
            "system_voltage_kv": 13.8,
            "bolted_fault_current_ka": 22.0,
            "clearing_time_sec": 0.2,
            "working_distance_mm": 455.0,
            "breaker_interrupt_rating_ka": 31.5,
            "voltage_drop_percent": 3.2,
            "thd_voltage_percent": 4.8,
            "dga_score": 8.2,
            "oil_quality_score": 7.9,
            "insulation_score": 8.3,
            "load_factor_score": 7.5,
            "motor_current_thd_percent": 4.5,
            "power_factor": 0.91,
        },
        "instrumentation": {
            "sil_target": 2,
            "failure_rate_per_hour": 1.0e-7,
            "proof_test_interval_hours": 8760.0,
            "mttr_hours": 8.0,
            "calibration_interval_days": 180.0,
            "calibration_history": [
                {"days_since_ref": 0.0, "error_pct": 0.05},
                {"days_since_ref": 90.0, "error_pct": 0.16},
                {"days_since_ref": 180.0, "error_pct": 0.28},
                {"days_since_ref": 270.0, "error_pct": 0.39},
            ],
            "tolerance_pct": 1.0,
            "sensor_mtbf_years": 8.0,
            "cv_required": 45.0,
            "cv_rated": 80.0,
            "uncertainty_components_pct": [0.2, 0.3, 0.1],
        },
        "steel": {
            "member_type": "column",
            "section_label": "W310x60",
            "length_m": 6.0,
            "k_factor": 1.0,
            "radius_of_gyration_mm": 90.0,
            "yield_strength_mpa": 345.0,
            "elasticity_mpa": 200000.0,
            "gross_area_mm2": 7600.0,
            "corrosion_loss_percent": 8.0,
            "axial_demand_kn": 650.0,
            "moment_demand_knm": 90.0,
            "deflection_mm": 10.0,
            "span_mm": 6000.0,
            "connection_failure_detected": False,
        },
        "civil": {
            "element_type": "beam",
            "fc_mpa": 35.0,
            "fy_mpa": 420.0,
            "width_mm": 300.0,
            "effective_depth_mm": 550.0,
            "rebar_area_mm2": 2450.0,
            "demand_moment_knm": 280.0,
            "lateral_capacity_loss_percent": 8.0,
            "affected_area_percent": 12.0,
            "vertical_capacity_loss_percent": 6.0,
            "carbonation_coeff_mm_sqrt_year": 1.8,
            "service_years": 18.0,
            "cover_thickness_mm": 40.0,
            "crack_width_mm": 0.22,
            "spalling_area_percent": 5.0,
            "foundation_settlement_mm": 8.0,
        },
    }


def fetch_json(url: str, payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
    data = None
    headers = {}
    method = "GET"
    if payload is not None:
        method = "POST"
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=20) as response:
        body = response.read().decode("utf-8")
    return json.loads(body)


def is_backend_healthy(host: str, port: int) -> bool:
    try:
        health = fetch_json(health_url(host, port))
        return health.get("status") == "ok"
    except Exception:  # noqa: BLE001
        return False


def wait_for_backend(host: str, port: int, timeout_sec: int = 30) -> bool:
    started = time.perf_counter()
    while time.perf_counter() - started < timeout_sec:
        if is_backend_healthy(host, port):
            return True
        time.sleep(0.5)
    return False


def run(spawn_server: bool, host: str, port: int) -> int:
    spawned: subprocess.Popen[str] | None = None
    try:
        if spawn_server and not is_backend_healthy(host, port):
            cmd = [sys.executable, "scripts/run_api_server.py"]
            env = os.environ.copy()
            env["EPC_API_HOST"] = host
            env["EPC_API_PORT"] = str(port)
            print("$", " ".join(cmd))
            spawned = subprocess.Popen(cmd, env=env)  # noqa: S603
            if not wait_for_backend(host, port):
                print("[FAIL] backend did not become healthy after spawn")
                return 1

        health = fetch_json(health_url(host, port))
    except urllib.error.URLError as exc:
        print(f"[FAIL] backend health request failed: {exc}")
        return 1
    finally:
        # keep server alive during checks below; cleanup handled in outer finally
        pass

    try:
        disciplines = set(health.get("disciplines", []))
        if health.get("status") != "ok":
            print(f"[FAIL] backend health status is not ok: {health}")
            return 1
        if disciplines != EXPECTED_DISCIPLINES:
            print(f"[FAIL] backend disciplines mismatch: expected={sorted(EXPECTED_DISCIPLINES)} got={sorted(disciplines)}")
            return 1

        print("[OK] health check passed")
        print("discipline status confidence red warnings fields")
        calculate_prefix = calculate_url_prefix(host, port)

        for discipline, payload in sample_payloads().items():
            try:
                result = fetch_json(f"{calculate_prefix}{discipline}", payload)
            except urllib.error.URLError as exc:
                print(f"[FAIL] {discipline} request failed: {exc}")
                return 1

            status = result.get("status")
            confidence = ((result.get("verification") or {}).get("confidence")) or "-"
            flags = result.get("flags") or {}
            red_count = len(flags.get("red_flags") or [])
            warn_count = len(flags.get("warnings") or [])
            field_count = len((result.get("results") or {}).keys())

            print(f"{discipline:15} {status:7} {confidence:10} {red_count:3d} {warn_count:8d} {field_count:6d}")

            if status != "success":
                print(f"[FAIL] {discipline} did not return success: status={status}")
                return 1

        print("[OK] backend seven-discipline smoke passed")
        return 0
    finally:
        if spawned is not None:
            spawned.terminate()
            try:
                spawned.wait(timeout=10)
            except subprocess.TimeoutExpired:
                spawned.kill()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smoke-test backend API for seven disciplines.")
    parser.add_argument(
        "--spawn-server",
        action="store_true",
        help="Start API server automatically if not running on selected host/port.",
    )
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help=f"API host for health/calculate requests (default: {DEFAULT_HOST}).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"API port for health/calculate requests (default: {DEFAULT_PORT}).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return run(spawn_server=args.spawn_server, host=args.host, port=args.port)


if __name__ == "__main__":
    sys.exit(main())

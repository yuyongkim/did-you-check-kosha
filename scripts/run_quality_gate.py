from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]


def npm_command(*args: str) -> list[str]:
    if os.name == "nt":
        return ["cmd", "/c", "npm", *args]
    return ["npm", *args]


def assert_paths_command(paths: Iterable[str]) -> list[str]:
    joined = ",".join(repr(path) for path in paths)
    snippet = (
        "from pathlib import Path; "
        f"required=[{joined}]; "
        "missing=[p for p in required if not Path(p).exists()]; "
        "print('[OK] required artifacts present' if not missing else '[MISSING] ' + ', '.join(missing)); "
        "raise SystemExit(1 if missing else 0)"
    )
    return [sys.executable, "-c", snippet]


def run_step(name: str, command: list[str]) -> None:
    print(f"\n=== {name} ===", flush=True)
    print("$", " ".join(command), flush=True)
    started = time.perf_counter()
    completed = subprocess.run(command, cwd=ROOT, check=False)
    elapsed = time.perf_counter() - started
    if completed.returncode != 0:
        raise RuntimeError(f"{name} failed (exit={completed.returncode}, elapsed={elapsed:.1f}s)")
    print(f"[OK] {name} ({elapsed:.1f}s)", flush=True)


def steps(profile: str) -> Iterable[tuple[str, list[str]]]:
    py = sys.executable
    yield ("Backend unit tests", [py, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"])
    yield (
        "Backend API smoke",
        [py, "scripts/smoke_backend_api.py", "--spawn-server", "--host", "127.0.0.1", "--port", "18000"],
    )
    if profile in {"strict", "implementation"}:
        yield (
            "Backend extended regression smoke",
            [py, "scripts/regression_api_smoke.py", "--base-url", "http://127.0.0.1:18000", "--spawn-server"],
        )
    yield ("Frontend lint", npm_command("--prefix", "frontend", "run", "lint"))
    yield ("Frontend typecheck", npm_command("--prefix", "frontend", "run", "typecheck"))
    yield ("Frontend unit tests", npm_command("--prefix", "frontend", "run", "test:unit"))
    if profile in {"strict", "implementation"}:
        yield ("Frontend backend-mode E2E", npm_command("--prefix", "frontend", "run", "test:e2e:backend"))
        yield ("Frontend E2E", npm_command("--prefix", "frontend", "run", "test:e2e"))
        yield ("Frontend build", npm_command("--prefix", "frontend", "run", "build"))
    if profile == "implementation":
        yield (
            "Implementation artifacts presence",
            assert_paths_command(
                [
                    "docs/proposals/EPC_MAINTENANCE_AI_PROJECT_BRIEF_V0.1.ko.md",
                    "docs/proposals/EPC_MAINTENANCE_AI_PROJECT_BRIEF_V0.1.ko.docx",
                    "datasets/kosha/manifest.json",
                    "datasets/kosha_guide/manifest.json",
                    "frontend/README.md",
                    "README.md",
                ]
            ),
        )
        yield (
            "Proposal screenshot pack completeness",
            assert_paths_command(
                [
                    "docs/proposals/assets/project-intro/screenshots/01_main_landing.png",
                    "docs/proposals/assets/project-intro/screenshots/02_core_feature_piping.png",
                    "docs/proposals/assets/project-intro/screenshots/03_dashboard_management.png",
                    "docs/proposals/assets/project-intro/screenshots/04_settings_panel.png",
                    "docs/proposals/assets/project-intro/screenshots/05_mobile_responsive_rotating.png",
                    "docs/proposals/assets/project-intro/screenshots/06_result_outcome_rotating.png",
                ]
            ),
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run full-stack quality gate.")
    parser.add_argument(
        "--profile",
        choices=["fast", "strict", "implementation"],
        default="strict",
        help=(
            "Validation depth profile. "
            "strict=full (default), "
            "fast=skip frontend e2e/build, "
            "implementation=full + proposal/data artifact checks."
        ),
    )
    parser.add_argument(
        "--skip-e2e",
        action="store_true",
        help="Legacy option. Equivalent to --profile fast.",
    )
    args = parser.parse_args()
    profile = "fast" if args.skip_e2e else args.profile

    started = time.perf_counter()
    try:
        print(f"[INFO] quality gate profile: {profile}", flush=True)
        for name, command in steps(profile=profile):
            run_step(name, command)
    except RuntimeError as exc:
        print(f"\n[FAIL] {exc}", flush=True)
        return 1

    elapsed = time.perf_counter() - started
    print(f"\n[SUCCESS] quality gate passed in {elapsed:.1f}s", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

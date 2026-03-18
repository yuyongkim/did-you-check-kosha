from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.agents.runtime_builder import build_mock_runtime
from src.shared.config_loader import load_and_validate_config


def main() -> int:
    config_path = ROOT / "configs" / "sample_config.json"
    config, errors = load_and_validate_config(config_path)

    if errors:
        print("CONFIG_INVALID")
        for error in errors:
            print(f"- {error}")
        return 1

    runtime = build_mock_runtime(config)
    print("CONFIG_VALID")
    print(f"REGISTERED_AGENTS={len(list(runtime.names()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

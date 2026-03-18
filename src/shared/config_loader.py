from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, Tuple

from src.agents.registry import missing_required_agents
from src.shared.config_schema import validate_config


def load_json_config(path: str | Path) -> Dict[str, Any]:
    config_path = Path(path)
    return json.loads(config_path.read_text(encoding="utf-8"))


def validate_config_with_required_agents(config: Mapping[str, Any]) -> List[str]:
    errors = validate_config(config)
    agent_names = list(config.get("agents", {}).keys()) if isinstance(config.get("agents"), Mapping) else []
    missing = missing_required_agents(agent_names)
    if missing:
        errors.append(f"Missing required agents: {missing}")
    return errors


def load_and_validate_config(path: str | Path) -> Tuple[Dict[str, Any], List[str]]:
    config = load_json_config(path)
    errors = validate_config_with_required_agents(config)
    return config, errors


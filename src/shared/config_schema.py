from __future__ import annotations

from typing import Any, Dict, List, Mapping


REQUIRED_TOP_LEVEL = {
    "system",
    "models",
    "timeouts",
    "verification",
    "logging",
    "security",
    "agents",
    "workflows",
}

REQUIRED_SYSTEM_FIELDS = {"max_threads", "max_depth", "default_workflow", "default_model"}
REQUIRED_TIMEOUT_FIELDS = {"default_agent_timeout_sec", "spec_lookup_timeout_sec", "verification_timeout_sec"}
REQUIRED_VERIFICATION_FIELDS = {
    "golden_dataset_path",
    "maker_voting_threshold",
    "red_flag_auto_escalation",
    "critical_fail_closed",
}


def validate_config(config: Mapping[str, Any]) -> List[str]:
    errors: List[str] = []

    missing = REQUIRED_TOP_LEVEL - set(config.keys())
    if missing:
        errors.append(f"Missing top-level sections: {sorted(missing)}")

    system = config.get("system", {})
    timeout = config.get("timeouts", {})
    verification = config.get("verification", {})

    if isinstance(system, Mapping):
        missing_system = REQUIRED_SYSTEM_FIELDS - set(system.keys())
        if missing_system:
            errors.append(f"Missing [system] fields: {sorted(missing_system)}")
    else:
        errors.append("[system] must be a mapping")

    if isinstance(timeout, Mapping):
        missing_timeout = REQUIRED_TIMEOUT_FIELDS - set(timeout.keys())
        if missing_timeout:
            errors.append(f"Missing [timeouts] fields: {sorted(missing_timeout)}")
    else:
        errors.append("[timeouts] must be a mapping")

    if isinstance(verification, Mapping):
        missing_ver = REQUIRED_VERIFICATION_FIELDS - set(verification.keys())
        if missing_ver:
            errors.append(f"Missing [verification] fields: {sorted(missing_ver)}")
    else:
        errors.append("[verification] must be a mapping")

    return errors

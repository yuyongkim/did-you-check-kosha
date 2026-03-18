from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Mapping
import uuid
from datetime import datetime


class MessageType(str, Enum):
    CALCULATION_REQUEST = "calculation_request"
    SPEC_LOOKUP_REQUEST = "spec_lookup_request"
    VERIFICATION_REQUEST = "verification_request"
    CALCULATION_RESULT = "calculation_result"
    ESCALATION_EVENT = "escalation_event"


class Priority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


REQUIRED_ENVELOPE_FIELDS = {
    "message_id",
    "message_type",
    "correlation_id",
    "trace_id",
    "from_agent",
    "to_agent",
    "timestamp_utc",
    "priority",
    "timeout_sec",
    "payload",
    "meta",
}

REQUIRED_PAYLOAD_FIELDS = {
    MessageType.CALCULATION_REQUEST.value: {"calculation_type", "input_data"},
    MessageType.SPEC_LOOKUP_REQUEST.value: {"query", "filters"},
    MessageType.VERIFICATION_REQUEST.value: {"verification_type", "inputs", "results"},
    MessageType.CALCULATION_RESULT.value: {"status", "results", "flags"},
    MessageType.ESCALATION_EVENT.value: {"reason_code", "severity", "summary", "recommended_action", "blocking"},
}


@dataclass
class ValidationReport:
    valid: bool
    errors: List[str]


def _is_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
        return True
    except (TypeError, ValueError):
        return False


def _is_iso8601_utc(value: str) -> bool:
    try:
        if value.endswith("Z"):
            datetime.fromisoformat(value.replace("Z", "+00:00"))
            return True
        return False
    except ValueError:
        return False


def validate_message_envelope(message: Mapping[str, Any]) -> ValidationReport:
    errors: List[str] = []

    missing = REQUIRED_ENVELOPE_FIELDS - set(message.keys())
    if missing:
        errors.append(f"Missing envelope fields: {sorted(missing)}")

    if "message_id" in message and not _is_uuid(str(message["message_id"])):
        errors.append("message_id must be UUID")
    if "correlation_id" in message and not _is_uuid(str(message["correlation_id"])):
        errors.append("correlation_id must be UUID")
    if "trace_id" in message and not _is_uuid(str(message["trace_id"])):
        errors.append("trace_id must be UUID")

    if "timestamp_utc" in message and not _is_iso8601_utc(str(message["timestamp_utc"])):
        errors.append("timestamp_utc must be ISO8601 UTC with Z suffix")

    if "priority" in message and message["priority"] not in {p.value for p in Priority}:
        errors.append("priority must be one of low|normal|high|critical")

    if "timeout_sec" in message:
        timeout = message["timeout_sec"]
        if not isinstance(timeout, int) or timeout < 1 or timeout > 1800:
            errors.append("timeout_sec must be integer in range 1..1800")

    msg_type = message.get("message_type")
    if msg_type not in {m.value for m in MessageType}:
        errors.append("message_type is invalid")

    payload = message.get("payload")
    if msg_type in REQUIRED_PAYLOAD_FIELDS:
        if not isinstance(payload, Mapping):
            errors.append("payload must be object")
        else:
            required_payload = REQUIRED_PAYLOAD_FIELDS[msg_type]
            payload_missing = required_payload - set(payload.keys())
            if payload_missing:
                errors.append(
                    f"Missing payload fields for {msg_type}: {sorted(payload_missing)}"
                )

    meta = message.get("meta")
    if meta is not None and not isinstance(meta, Mapping):
        errors.append("meta must be object")

    return ValidationReport(valid=not errors, errors=errors)

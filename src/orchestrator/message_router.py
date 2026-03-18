from __future__ import annotations

from typing import Any, Dict, Mapping

from src.agents.runtime import AgentRuntime
from src.shared.errors import SchemaValidationError
from src.shared.message_schema import MessageType, validate_message_envelope


class MessageRouter:
    """Routes validated messages to runtime agent implementations."""

    def __init__(self, runtime: AgentRuntime) -> None:
        self.runtime = runtime

    def dispatch(self, message: Mapping[str, Any]) -> Dict[str, Any]:
        report = validate_message_envelope(message)
        if not report.valid:
            raise SchemaValidationError("; ".join(report.errors))

        msg_type = str(message["message_type"])
        to_agent = str(message["to_agent"])
        payload = message["payload"]
        assert isinstance(payload, Mapping)

        if msg_type == MessageType.CALCULATION_REQUEST.value:
            return self._handle_calculation_request(to_agent, payload)
        if msg_type == MessageType.SPEC_LOOKUP_REQUEST.value:
            return self._handle_spec_lookup_request(to_agent, payload)
        if msg_type == MessageType.VERIFICATION_REQUEST.value:
            return self._handle_verification_request(to_agent, payload)
        if msg_type == MessageType.CALCULATION_RESULT.value:
            return {
                "status": str(payload.get("status", "success")),
                "results": payload.get("results", {}),
                "flags": payload.get("flags", {"red_flags": [], "warnings": []}),
            }
        if msg_type == MessageType.ESCALATION_EVENT.value:
            return {
                "status": "escalated",
                "results": {},
                "flags": {"red_flags": [str(payload.get("reason_code"))], "warnings": []},
                "escalation": dict(payload),
            }

        raise SchemaValidationError(f"Unsupported message type: {msg_type}")

    def _handle_calculation_request(
        self,
        to_agent: str,
        payload: Mapping[str, Any],
    ) -> Dict[str, Any]:
        agent = self.runtime.require(to_agent)
        if hasattr(agent, "handle_calculation"):
            return agent.handle_calculation(dict(payload), self.runtime)  # type: ignore[attr-defined]
        if hasattr(agent, "execute"):
            calc_type = str(payload.get("calculation_type", "generic"))
            input_data = payload.get("input_data", {})
            if not isinstance(input_data, dict):
                input_data = {}
            result = agent.execute(calc_type, input_data)  # type: ignore[attr-defined]
            return {
                "status": result.get("status", "success"),
                "results": result.get("results", {}),
                "flags": {"red_flags": [], "warnings": []},
            }
        raise SchemaValidationError(f"Target agent cannot process calculation_request: {to_agent}")

    def _handle_spec_lookup_request(
        self,
        to_agent: str,
        payload: Mapping[str, Any],
    ) -> Dict[str, Any]:
        agent = self.runtime.require(to_agent)
        query = str(payload.get("query", ""))
        filters = payload.get("filters", {})
        if not isinstance(filters, dict):
            filters = {}
        discipline = filters.get("discipline")
        discipline_str = str(discipline) if discipline else None

        if hasattr(agent, "search_standard"):
            results = agent.search_standard(query=query, discipline=discipline_str, filters=filters)  # type: ignore[attr-defined]
            return {"status": "success", "results": results, "flags": {"red_flags": [], "warnings": []}}
        raise SchemaValidationError(f"Target agent cannot process spec_lookup_request: {to_agent}")

    def _handle_verification_request(
        self,
        to_agent: str,
        payload: Mapping[str, Any],
    ) -> Dict[str, Any]:
        agent = self.runtime.require(to_agent)
        verification_type = str(payload.get("verification_type", "generic"))
        if hasattr(agent, "run_verification"):
            result = agent.run_verification(verification_type, dict(payload))  # type: ignore[attr-defined]
            return {
                "status": result.get("status", "success"),
                "results": result,
                "flags": result.get("flags", {"red_flags": [], "warnings": []}),
            }
        raise SchemaValidationError(f"Target agent cannot process verification_request: {to_agent}")


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Mapping

from src.agents.runtime import AgentRuntime
from src.orchestrator.message_router import MessageRouter
from src.orchestrator.state_machine import OrchestratorState, StateMachine
from src.shared.red_flags import is_blocking, is_known_flag
from src.shared.types import TraceContext


@dataclass
class RunContext:
    trace: TraceContext = field(default_factory=TraceContext)
    state_machine: StateMachine = field(default_factory=StateMachine)
    flags: List[str] = field(default_factory=list)


class Orchestrator:
    """Minimal orchestrator control-plane scaffold."""

    def __init__(self, runtime: AgentRuntime | None = None) -> None:
        self.current_run: RunContext | None = None
        self.runtime = runtime
        self.router = MessageRouter(runtime) if runtime is not None else None

    def start_run(self, workflow_id: str = "standard_calculation") -> RunContext:
        ctx = RunContext()
        ctx.trace.workflow_id = workflow_id
        self.current_run = ctx
        return ctx

    def bind_runtime(self, runtime: AgentRuntime) -> None:
        self.runtime = runtime
        self.router = MessageRouter(runtime)

    def add_flag(self, code: str) -> None:
        if not is_known_flag(code):
            raise ValueError(f"Unknown red flag: {code}")
        if self.current_run is None:
            raise RuntimeError("No active run")
        self.current_run.flags.append(code)

    def has_blocking_flag(self) -> bool:
        if self.current_run is None:
            return False
        return any(is_blocking(code) for code in self.current_run.flags)

    def advance(self, target: OrchestratorState) -> None:
        if self.current_run is None:
            raise RuntimeError("No active run")
        self.current_run.state_machine.transition(target, blocking_flag_present=self.has_blocking_flag())

    def can_release(self) -> bool:
        if self.current_run is None:
            return False
        return (
            self.current_run.state_machine.state == OrchestratorState.READY_FOR_REPORT
            and not self.has_blocking_flag()
        )

    def handle_message(self, message: Mapping[str, Any]) -> Mapping[str, Any]:
        if self.router is None:
            raise RuntimeError("Runtime is not bound to orchestrator")

        if self.current_run is None:
            workflow_id = "standard_calculation"
            meta = message.get("meta")
            if isinstance(meta, Mapping):
                workflow_id = str(meta.get("workflow_id", workflow_id))
            self.start_run(workflow_id=workflow_id)

        result = self.router.dispatch(message)
        self._consume_flags(result)
        return result

    def _consume_flags(self, result: Mapping[str, Any]) -> None:
        if self.current_run is None:
            return
        flags = result.get("flags")
        if not isinstance(flags, Mapping):
            return

        red_flags = flags.get("red_flags", [])
        if not isinstance(red_flags, list):
            return

        for code in red_flags:
            if isinstance(code, str) and is_known_flag(code):
                self.current_run.flags.append(code)

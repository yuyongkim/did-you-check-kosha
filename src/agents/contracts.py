from __future__ import annotations

from dataclasses import dataclass
from typing import List


REQUIRED_AGENT_FIELDS = {
    "description",
    "persona_file",
    "model",
    "reasoning_effort",
    "tools_allowed",
    "dependencies",
    "max_tokens",
    "temperature",
    "timeout_sec",
    "retry_policy",
}


@dataclass
class AgentConfig:
    name: str
    description: str
    persona_file: str
    model: str
    reasoning_effort: str
    tools_allowed: List[str]
    dependencies: List[str]
    max_tokens: int
    temperature: float
    timeout_sec: int
    retry_policy: str

    def validate(self) -> List[str]:
        errors: List[str] = []
        if self.timeout_sec < 1:
            errors.append("timeout_sec must be positive")
        if self.max_tokens < 128:
            errors.append("max_tokens too small")
        if not 0.0 <= self.temperature <= 1.0:
            errors.append("temperature must be between 0 and 1")
        if self.reasoning_effort not in {"low", "medium", "high"}:
            errors.append("reasoning_effort must be low|medium|high")
        return errors

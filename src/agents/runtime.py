from __future__ import annotations

from typing import Dict, Iterable


class AgentRuntime:
    """Runtime registry for agent instances."""

    def __init__(self) -> None:
        self._agents: Dict[str, object] = {}

    def register(self, name: str, agent: object) -> None:
        self._agents[name] = agent

    def has(self, name: str) -> bool:
        return name in self._agents

    def require(self, name: str) -> object:
        if name not in self._agents:
            raise KeyError(f"Agent not registered: {name}")
        return self._agents[name]

    def names(self) -> Iterable[str]:
        return self._agents.keys()

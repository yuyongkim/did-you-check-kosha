from __future__ import annotations

from typing import Dict, Protocol


class VerificationAgent(Protocol):
    def run_verification(self, verification_type: str, payload: Dict[str, object]) -> Dict[str, object]:
        ...
